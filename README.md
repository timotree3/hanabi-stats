# Hanabi stats

The program parses users' statistics from https://hanab.live/, calculates percentage of winnings and losings for each type of variants (easy, single dark, double dark, easy null variants which are neither single nor double dark), filters it by each player, gets highest winrate and saves all statistics to the files in tsv format.

Last available stats for active users can be found here: [click](https://github.com/Aigul9/hanabi-stats/blob/master/output/up_to_date_stats.tsv) (19/04/2021).<br/>
Highest winrate: [WR](https://github.com/Aigul9/hanabi-stats/blob/master/output/highest_wr_all.tsv)<br/>
Highest winrate for bga variants: [WR bga](https://github.com/Aigul9/hanabi-stats/blob/master/output/highest_wr_bga.tsv)<br/>
Highest winrate for non-bga variants: [WR non-bga](https://github.com/Aigul9/hanabi-stats/blob/master/output/highest_wr_not_bga.tsv)

## Stack of technologies
- [Python 3.9](https://www.python.org/)

## Folders content
- ```input```: data which should be provided to the program;
- ```output```: results;
- ```py```: python scripts to download and parse statistics, calculate user data;
- ```resources```: list of available variants and their efficiency;
- ```temp```: temporary files generated by the program. Files ```[username]_stats.txt``` and ```[username]_players.txt``` contain table of games and list of players respectively.

## Usage
1. Type list of players in ```input/list_of_users.txt```
2. Run script ```main.py```
3. See the results in the ```output``` folder.
4. See win/loss ratio for each player in the ```output/filtered_by_players/[username]_wl_by_players.tsv```

The tables structure:

symbol | description
-|-
W | number of wins
L | number of losses
W/L | win/loss ratio
% | percentage
\# | count (speedruns included)
2p | 2-player games
3p+ | 3-6 player games
