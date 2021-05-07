players_stats = []

with open("input/list_of_players.txt") as players:
    worst_seq = 0
    worst_player = None
    for player in players:
        player = player.strip()
        print(player)
        with open("temp/{}_stats.txt".format(player)) as f:
            seq = 0
            max_seq = 0
            max_seq_ender = None
            for line in f:
                fields = line.split("\t")
                if fields[2] == "0":
                    seq += 1
                else:
                    if seq > max_seq:
                        max_seq = seq
                        max_seq_ender = fields
                    seq = 0
        print(max_seq)
        print(max_seq_ender)
        players_stats.append([player, max_seq, max_seq_ender])

players_stats = sorted(players_stats, key=lambda player: player[1], reverse=True)

with open("output/consecutive_strikeouts.tsv", "w") as output:
    output.write("Player\tMax Consecutive Strikeouts\tStart of Sequence\n")
    for [player, max_seq, max_seq_ender] in players_stats:
        output.write("{}\t{}\t{}\n".format(player, max_seq, max_seq_ender[0]))
