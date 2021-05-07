def product(iter):
    from functools import reduce

    return reduce(lambda x, y: x * y, iter)


games = {}
current_strength_per_player = {}
num_games_per_player = {}
games_per_player = {}

# Load dataset
with open("input/list_of_players.txt") as players:
    for player in players:
        current_strength_per_player[player.strip()] = 1
    for player in current_strength_per_player:
        num_games = 0
        games_per_player[player] = []
        with open("stats/{}_stats.txt".format(player)) as player_history_file:
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
                if (
                    # len(players) == 2 and
                    all([player in current_strength_per_player for player in players])
                    # and variant == "No Variant"
                ):
                    game = {
                        "fraction_max_score": fraction_max_score,
                        "variant": variant,
                        "players": players,
                    }
                    games[replay] = game
                    num_games += 1
                    games_per_player[player].append(game)

        num_games_per_player[player] = num_games

# games = {
#     0: {"players": ["alice", "bob"], "fraction_max_score": 1.0},
#     1: {"players": ["alice", "bob"], "fraction_max_score": 1.0},
#     2: {"players": ["alice", "bob"], "fraction_max_score": 0.0},
#     3: {"players": ["cathy", "bob"], "fraction_max_score": 1.0},
#     4: {"players": ["cathy", "bob"], "fraction_max_score": 1.0},
#     5: {"players": ["cathy", "bob"], "fraction_max_score": 1.0},
# }
# num_games_per_player = {"alice": 3, "bob": 6, "cathy": 3}
# current_strength_per_player = {"alice": 1, "bob": 1, "cathy": 1}
# # num_games_per_player = {"bob": 3, "cathy": 3}
# # current_strength_per_player = {"bob": 1, "cathy": 1}

for player in current_strength_per_player:
    print(player, current_strength_per_player[player], num_games_per_player[player])

while min(num_games_per_player.values()) < 1:
    too_small_sample_size_player = None
    for player in num_games_per_player:
        if num_games_per_player[player] < 1:
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

        product_strengths = product(
            [current_strength_per_player[player] for player in game["players"]],
        )
        for alice in game["players"]:
            if current_strength_per_player[alice] == 0:
                continue
            product_strengths_excluding_alice = (
                product_strengths / current_strength_per_player[alice]
            )
            if product_strengths_excluding_alice == 0:
                sum_performances_per_player[alice] += game["fraction_max_score"]
                continue
            alice_strength_producing_perfect_prediction = (
                game["fraction_max_score"] / product_strengths_excluding_alice
            )
            alice_performance = alice_strength_producing_perfect_prediction ** (
                1 / float(len(game["players"]))
            )
            avg_strength_excluding_alice = product_strengths_excluding_alice / (
                len(game["players"]) - 1
            )

            sum_performances_per_player[alice] += alice_performance

    next_strength_per_player = {}
    for player in sum_performances_per_player:
        next_strength_per_player[player] = (
            sum_performances_per_player[player] / num_games_per_player[player]
        )
        if next_strength_per_player[player] > 1:
            next_strength_per_player[player] = 1

    current_strength_per_player = next_strength_per_player

    total_error = 0
    for replay in games:
        game = games[replay]
        prediction = product(
            [current_strength_per_player[player] for player in game["players"]]
        )
        error = prediction - game["fraction_max_score"]
        total_error += error

    print(total_error / len(games))

    with open("output/iteration_{}.tsv".format(iteration), "w") as output:
        for [player, current_strength] in sorted(
            current_strength_per_player.items(), key=lambda item: item[1], reverse=True
        ):
            output.write("{}\t{}\n".format(player, current_strength))
