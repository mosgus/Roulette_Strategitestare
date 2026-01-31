# build_bet.py
"""
    Bet Constructor for American Roulette:

        input: bet parameters
        output: bet_array (list): A list of 38 numbers representing bets on [0, 00, 1, 2, ..., 36]

"""

# Sets for RED and BLACK numbers
RED_SET = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
BLACK_SET = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}

# NUMBER + 1 = ARRAY INDEX
RED_INDICES = {n + 1 for n in RED_SET}
BLACK_INDICES = {n + 1 for n in BLACK_SET}

'''🟢 BET FUNCTIONS 🟢'''

''' SINGLE NUMBER/TILE '''
def bet_one(tile, amount):
    bet = empty_bet()
    if tile == '0':
        bet[0] = amount
    elif tile == '00':
        bet[1] = amount
    else:
        n = int(tile) + 1
        bet[n] = amount
    return bet

''' RGB '''
def bet_green(amount):
    bet = empty_bet()
    bet[0] = amount / 2
    bet[1] = amount / 2
    return bet
def bet_red(amount):
    bet = empty_bet()
    per_slot = amount / 18
    for n in RED_INDICES:
        bet[n] = per_slot
    return bet
def bet_black(amount):
    bet = empty_bet()
    per_slot = amount / 18
    for n in BLACK_INDICES:
        bet[n] = per_slot
    return bet

''' EVEN/ODD '''
def bet_even(amount):
    """Bets on 2, 4, ..., 36 (Indices 3, 5, ..., 37)"""
    bet = empty_bet()
    per_slot = amount / 18
    for n in range(2, 37, 2):
        bet[n + 1] = per_slot
    return bet
def bet_odd(amount):
    """Bets on 1, 3, ..., 35 (Indices 2, 4, ..., 36)"""
    bet = empty_bet()
    per_slot = amount / 18
    for n in range(1, 36, 2):
        bet[n + 1] = per_slot
    return bet

''' 12s '''
def bet_1st_12(amount):
    bet = empty_bet()
    per_slot = amount / 12  # Divide total bet by the 12 numbers covered
    for n in range(1, 13):  # Numbers 1 through 12
        bet[n + 1] = per_slot
    return bet
def bet_2nd_12(amount):
    bet = empty_bet()
    per_slot = amount / 12
    for n in range(13, 25):  # Numbers 13 through 24
        bet[n + 1] = per_slot
    return bet
def bet_3rd_12(amount):
    bet = empty_bet()
    per_slot = amount / 12
    for n in range(25, 37):  # Numbers 25 through 36
        bet[n + 1] = per_slot
    return bet

''' 2:1 Lines '''
def bet_column_a(amount):
    bet = empty_bet()
    per_slot = amount / 12
    for n in range(1, 35, 3): # Start at 1, go to 34, jump by 3
        bet[n + 1] = per_slot
    return bet
def bet_column_b(amount):
    bet = empty_bet()
    per_slot = amount / 12
    for n in range(2, 36, 3): # Start at 2, go to 35, jump by 3
        bet[n + 1] = per_slot
    return bet
def bet_column_c(amount):
    bet = empty_bet()
    per_slot = amount / 12
    for n in range(3, 37, 3): # Start at 3, go to 36, jump by 3
        bet[n + 1] = per_slot
    return bet

''' Halves'''
def bet_low(amount):
    bet = empty_bet()
    per_slot = amount / 18
    for n in range(1, 19):  # Numbers 1 through 18
        bet[n + 1] = per_slot
    return bet
def bet_high(amount):
    bet = empty_bet()
    per_slot = amount / 18
    for n in range(19, 37):  # Numbers 19 through 36
        bet[n + 1] = per_slot
    return bet

'''🔴 BET FUNCTIONS 🔴'''

''' base empty bet '''
def empty_bet():
    return [0.0] * 38

''' VECTOR ADDITION of bets'''
def combine_bets(*bets):
    return [sum(n) for n in zip(*bets)]


''' VALIDATION '''
def validate_bet_array(bet_array):
    # ensure 38 slots, numeric, and non-negative
    if len(bet_array) != 38:
        raise ValueError("bet_array must have 38 slots for [0, 00, 1..36].")
    for n in bet_array:
        if not isinstance(n, (int, float)):
            raise TypeError("bet_array values must be numeric.")
        if n < 0:
            raise ValueError("bet_array values must be non-negative.")


def build_bet_from_spec(bet_spec, amount):
    if not bet_spec:
        bet_spec = 'red'
    parts = [p.strip().lower() for p in bet_spec.split('+') if p.strip()]
    if not parts:
        parts = ['red']
    per_amount = amount / len(parts)

    def _one_bet(part):
        if part.startswith('custom:'):
            raw = part[len('custom:'):]
            values = [float(x) for x in raw.split(',')]
            validate_bet_array(values)
            total = sum(values)
            if total <= 0:
                raise ValueError("custom bet must sum to a positive value.")
            scale = per_amount / total
            return [v * scale for v in values], 'Custom'

        mapping = {
            'red': (bet_red, 'Red'),
            'black': (bet_black, 'Black'),
            'green': (bet_green, 'Green'),
            'even': (bet_even, 'Even'),
            'odd': (bet_odd, 'Odd'),
            'low': (bet_low, 'Low (1-18)'),
            'high': (bet_high, 'High (19-36)'),
            '1st12': (bet_1st_12, '1st 12'),
            '2nd12': (bet_2nd_12, '2nd 12'),
            '3rd12': (bet_3rd_12, '3rd 12'),
            'col_a': (bet_column_a, 'Column A'),
            'col_b': (bet_column_b, 'Column B'),
            'col_c': (bet_column_c, 'Column C'),
        }
        if part.startswith('number:'):
            tile = part.split(':', 1)[1].strip()
            return bet_one(tile, per_amount), f'Number {tile}'
        if part not in mapping:
            raise ValueError(f"Unknown bet spec: {part}")
        fn, label = mapping[part]
        return fn(per_amount), label

    bets = []
    labels = []
    for part in parts:
        bet, label = _one_bet(part)
        bets.append(bet)
        labels.append(label)

    return combine_bets(*bets), ' + '.join(labels)
