games = {}
current_strength_per_player = {}
num_games_per_player = {}
games_per_player = {}

# Load dataset
with open("input/list_of_players.txt") as players:
    for player in players:
        current_strength_per_player[player.strip()] = 0
    for player in current_strength_per_player:
        num_games = 0
        games_per_player[player] = []
        with open("temp/{}_stats.txt".format(player)) as player_history_file:
            for game in player_history_file:
                game = game.strip().split("\t")
                [
                    replay,
                    num_players,
                    score,
                    variant,
                    time,
                    players,
                    other_games_same_seed,
                    num_suits,
                    max_score,
                ] = game

                fraction_max_score = int(score) / int(max_score)
                players = players.split(", ")
                if all([player in current_strength_per_player for player in players]):
                    game = {
                        "fraction_max_score": fraction_max_score,
                        "variant": variant,
                        "players": players,
                    }
                    games[replay] = game
                    num_games += 1
                    games_per_player[player].append(game)

        num_games_per_player[player] = num_games


for player in current_strength_per_player:
    print(player, current_strength_per_player[player], num_games_per_player[player])

while min(num_games_per_player.values()) < 50:
    too_small_sample_size_player = None
    for player in num_games_per_player:
        if num_games_per_player[player] < 50:
            too_small_sample_size_player = player
            break
    print(too_small_sample_size_player)
    num_games_per_player.pop(too_small_sample_size_player)
    current_strength_per_player.pop(too_small_sample_size_player)
    replays_to_remove = []
    for replay in games:
        game = games[replay]
        if too_small_sample_size_player in game["players"]:
            replays_to_remove.append(replay)
            for player in game["players"]:
                if player == too_small_sample_size_player:
                    continue

                num_games_per_player[player] -= 1
                games_per_player[player].remove(game)

    for replay in replays_to_remove:
        games.pop(replay)

for player in current_strength_per_player:
    print(player, current_strength_per_player[player], num_games_per_player[player])

for iteration in range(100):
    sum_performances_per_player = dict(
        [(player, 0) for player in current_strength_per_player]
    )
    for replay in games:
        game = games[replay]

        sum_strengths = sum(
            [current_strength_per_player[player] for player in game["players"]]
        )
        for alice in game["players"]:
            sum_strengths_excluding_alice = (
                sum_strengths - current_strength_per_player[alice]
            )
            avg_strength_excluding_alice = sum_strengths_excluding_alice / (
                len(game["players"]) - 1
            )

            alice_performance = (
                game["fraction_max_score"] - avg_strength_excluding_alice
            )

            sum_performances_per_player[alice] += alice_performance

    next_strength_per_player = {}
    for player in sum_performances_per_player:
        next_strength_per_player[player] = (
            sum_performances_per_player[player] / num_games_per_player[player]
        )

    current_strength_per_player = next_strength_per_player

    with open("output/iteration_{}.tsv".format(iteration), "w") as output:
        for [player, current_strength] in sorted(
            current_strength_per_player.items(), key=lambda item: item[1], reverse=True
        ):
            output.write("{}\t{}\n".format(player, current_strength))
