players_stats = []

with open("input/list_of_players.txt") as players:
    for player in players:
        player = player.strip()
        print(player)
        worst_finish = None
        worst_finish_max_score = None
        worst_finish_replay = None
        with open("stats/{}_stats.txt".format(player)) as f:
            for line in f:
                line = line.strip()
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
                ] = line.split("\t")
                score = int(score)
                max_score = int(max_score)
                if score == 0:
                    continue
                if (
                    worst_finish == None
                    or score / max_score < worst_finish / worst_finish_max_score
                    or (
                        score / max_score == worst_finish / worst_finish_max_score
                        and max_score > worst_finish_max_score
                    )
                ):
                    worst_finish = score
                    worst_finish_max_score = max_score
                    worst_finish_replay = replay
        print(worst_finish)
        print(worst_finish_max_score)
        print(worst_finish_replay)
        players_stats.append(
            [player, worst_finish, worst_finish_max_score, worst_finish_replay]
        )

players_stats = sorted(players_stats, key=lambda player: player[1] / player[2])

with open("output/worst_finish.tsv", "w") as output:
    output.write("Player\tGame with Worst %Max Score\tScore\tMax Score\n")
    for [
        player,
        worst_finish,
        worst_finish_max_score,
        worst_finish_replay,
    ] in players_stats:
        output.write(
            "{}\t{}\t{}\t{}\n".format(
                player,
                worst_finish_replay or "N/A",
                worst_finish or "N/A",
                worst_finish_max_score or "N/A",
            )
        )
