__author__ = 'bwright'

import Numbrix
import Link

# Test calls on Link

chains = [range(1, 31), range(37, 38), range(48, 82)]
links = Link.create_link_tuples_from_chains(chains)
print links

chains = [range(5, 31), range(37, 38), range(48, 81)]
links = Link.create_link_tuples_from_chains(chains)
print links

NUM_ROWS = 9
CELL_DIMENSION = 60

game_1 = [13, 15, 17, 21, 25,
          9, 27,
          37, 51,
          81, 55,
          79, 75, 69, 61, 59]

game_2 = [61, 71, 81, 1, 5,
          59, 7,
          57, 13,
          53, 29,
          51, 45, 41, 39, 37]

nov_30_2013_beginner = [5, 6, 7, 8, 9, 24, 25, 30, 31,
                        4, None, None, None, None, None, None, None, 32,
                        15, None, None, None, None, None, None, None, 33,
                        16, None, None, None, None, None, None, None, 34,
                        65, None, None, None, None, None, None, None, 39,
                        66, None, None, None, None, None, None, None, 40,
                        69, None, None, None, None, None, None, None, 45,
                        70, None, None, None, None, None, None, None, 46,
                        71, 72, 81, 80, 79, 52, 51, 48, 47]

dec_1_2013_expert = [81, 75, 69, 67, 65,
                     79, 51,
                     21, 45,
                     19, 37,
                     5, 7, 9, 33, 35]

dec_2_2013_advanced = [None, None, None, None, None, None, None, None, None,
                       None, None, 42, 41, None, 39, 52, None, None,
                       None, 30, None, None, 33, None, None, 58, None,
                       None, 27, None, None, None, None, None, 79, None,
                       None, None, 23, None, None, None, 61, None, None,
                       None, 19, None, None, None, None, None, 81, None,
                       None, 8, None, None, 15, None, None, 70, None,
                       None, None, 6, 11, None, 65, 68, None, None,
                       None, None, None, None, None, None, None, None, None]

dec_3_2013_intermediate = [None, None, None, None, None, None, None, None, None,
                           None, 61, 56, 53, 48, 45, 2, 7, None,
                           None, 60, None, None, None, None, None, 6, None,
                           None, 59, None, None, None, None, None, 5, None,
                           None, 68, None, None, None, None, None, 22, None,
                           None, 69, None, None, None, None, None, 21, None,
                           None, 72, None, None, None, None, None, 20, None,
                           None, 73, 78, 35, 32, 31, 28, 19, None,
                           None, None, None, None, None, None, None, None, None]

dec_22_2013_expert = [31, 33, 39, 45, 47,
                     25, 51,
                     9, 79,
                     7, 81,
                     5, 15, 65, 69, 71]

# This was a super hard one: 1891 backtracks!
mar_30_2014 = [55, 61, 69, 79, 77,
                     53, 75,
                     47, 31,
                     45, 17,
                     5, 7, 9, 13, 15]

# Super easy - just 5 backtracks
apr_6_2014 = [51, 53, 57, 79, 77,
                     43, 73,
                     41, 5,
                     35, 7,
                     33, 27, 25, 17, 9]

# Pretty hard - 436 backtracks
apr_13_2014 = [29, 31, 35, 49, 51,
                     23, 55,
                     21, 59,
                     13, 81,
                     11, 5, 69, 77, 79]

# Number of backtracks: 1369
may_18_2014 = [79, 77, 57, 55, 53,
                     69, 49,
                     67, 17,
                     31, 15,
                     29, 27, 1, 5, 13]

test_games = [game_1, game_2, nov_30_2013_beginner, dec_1_2013_expert, dec_2_2013_advanced, dec_3_2013_intermediate]
test_games = [may_18_2014]

for game in test_games:
    board = Numbrix.Numbrix(NUM_ROWS, CELL_DIMENSION, game)

    print board

    board.solve()

    print "\n---------- Results ----------\n"
    if board.is_done():
        print "SUCCESS! Puzzle is solved"
    else:
        print "Bummer. Did not solve puzzle. Something went wrong..."

    print board
