# roulette.py
"""
    Wheel Spin Logic for American Roulette:

        input: bet_array (list): A list of 38 numbers representing bets on [0, 00, 1, 2, ..., 36]
        output: payout (float): The net earnings (e.g. +35.0 or -10.0)

"""
import random

''' INDEX/NUMBER MAPPING '''
def index_to_num(index):
    if index == 0:
        return '0'
    if index == 1:
        return '00'
    return str(index - 1)

def num_to_color(num):
    if num == '0' or num == '00':
        return 'Green'
    n = int(num)
    from game_engine import build_bet as bb
    if n in bb.RED_SET:
        return 'Red'
    if n in bb.BLACK_SET:
        return 'Black'
    return 'Unknown'
''' # useless currently
def num_to_index(num):
    if num == '0':
        return 0
    if num == '00':
        return 1
    return int(num) + 1
'''

''' RNG HELPER '''
def get_rng(seed=None):
    if seed is None:
        return random
    return random.Random(seed)

''' "SPIN" ROULETTE WHEEL '''
def spin(rng=None, seed=None):
    if rng is None:
        rng = get_rng(seed)
    return rng.randint(0, 37) # pick a random winning index(0 to 37)

''' DETERMINE PAYOUT '''
def payout(bet_array, winning_index):
    total_wagered = sum(bet_array)              # 1. measure user bet
    amount_on_winner = bet_array[winning_index]  # 2. check amount bet on winning index

    ''' ? WIN or LOSE ¿ '''
    if amount_on_winner > 0: payout = amount_on_winner + (amount_on_winner * 35) # WIN
    else: payout = 0 # LOSE

    ''' output'''
    return payout - total_wagered # 3. Return result

''' ROULETTE '''
def roulette(bet_array, rng=None, seed=None):
    winning_index = spin(rng, seed)
    winning_num = index_to_num(winning_index)
    net_payout = payout(bet_array, winning_index)
    if net_payout > 0: dub = 1
    else: dub = 0

    return dub, winning_index, winning_num, net_payout

# USAGE EXAMPLE 1:1
'''
if __name__ == "__main__":
    # Simulate a $10 bet on the number '7' (index 8)
    test_bet = [0] * 38

    bet_amount_per_number = 10 / 18
    for i in range(2, 20):
        test_bet[i] = bet_amount_per_number

    dub, winner, winner_num, net = roulette(test_bet)

    print(f"Winning Index: {winner}")
    print(f"Winning Number: {winner_num}")
    if dub > 0:
        print(f"You win: +{net:.2f}")
    else:
        print(f"You lose: {net:.2f}")
'''
