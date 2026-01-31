"""
    Color constants and helpers for American Roulette.
"""

# Sets for RED and BLACK numbers
RED_SET = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
BLACK_SET = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}


def num_to_color(num):
    if num == '0' or num == '00':
        return 'Green'
    n = int(num)
    if n in RED_SET:
        return 'Red'
    if n in BLACK_SET:
        return 'Black'
    return 'Unknown'
