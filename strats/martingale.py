# martingale.py
"""
    Martingale Betting Strategy Implementation for American Roulette:

        input: initial_balance (float), buyout_profit (float), optional_sequence_file (str)
        output: Game Summary
"""

import sys
import csv
import os
from game_engine import build_bet as bb
from game_engine import roulette


def build_bet(bet_spec, amount):
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
            bb.validate_bet_array(values)
            total = sum(values)
            if total <= 0:
                raise ValueError("custom bet must sum to a positive value.")
            scale = per_amount / total
            return [v * scale for v in values], 'Custom'

        mapping = {
            'red': (bb.bet_red, 'Red'),
            'black': (bb.bet_black, 'Black'),
            'green': (bb.bet_green, 'Green'),
            'even': (bb.bet_even, 'Even'),
            'odd': (bb.bet_odd, 'Odd'),
            'low': (bb.bet_low, 'Low (1-18)'),
            'high': (bb.bet_high, 'High (19-36)'),
            '1st12': (bb.bet_1st_12, '1st 12'),
            '2nd12': (bb.bet_2nd_12, '2nd 12'),
            '3rd12': (bb.bet_3rd_12, '3rd 12'),
            'col_a': (bb.bet_column_a, 'Column A'),
            'col_b': (bb.bet_column_b, 'Column B'),
            'col_c': (bb.bet_column_c, 'Column C'),
        }
        if part.startswith('number:'):
            tile = part.split(':', 1)[1].strip()
            return bb.bet_one(tile, per_amount), f'Number {tile}'
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

    return bb.combine_bets(*bets), ' + '.join(labels)


def run_martingale(initial_balance, buyout, sequence_path=None, bet_spec=None):
    balance = initial_balance
    target_balance = initial_balance + buyout
    current_wager = 1.0
    round_count = 0

    # Optional: Load sequence data if a file path is provided
    outcomes = []
    if sequence_path and os.path.exists(sequence_path):
        with open(sequence_path, 'r') as f:
            reader = csv.DictReader(f)
            outcomes = list(reader)

    max_rounds = len(outcomes) if outcomes else None

    print(f"\nStarting Martingale: Balance ${balance}, Target ${target_balance} - 🟢")

    while 0 < balance < target_balance and (max_rounds is None or round_count < max_rounds):
        round_count += 1

        # 1. Check if we can afford the current wager
        if current_wager > balance:
            print(f"\nCan't afford wager of ${current_wager:.2f}. Going all-in with ${balance:.2f}.")
            current_wager = balance

        # 2. Construct the bet
        bet_array, bet_label = build_bet(bet_spec, current_wager)

        # 3. Get the winning index (From file or live RNG)
        if outcomes and (round_count - 1) < len(outcomes):
            row = outcomes[round_count - 1]
            win_index = int(row['Winning Index'])
            win_label = row['Winning Number']
            color = row['Color']
        else:
            win_index = roulette.spin()
            win_label = roulette.index_to_num(win_index)
            color = roulette.num_to_color(win_label)

        # 4. Calculate Payout
        net_result = roulette.payout(bet_array, win_index)
        balance += net_result

        # 5. Martingale Logic: Double on loss, reset on win
        if net_result > 0:
            current_wager = 1.0  # Reset
        else:
            current_wager *= 2  # Double down

        print(f"{round_count} - Bet on {bet_label} | Landed on {win_label} ({color}) | Net: {net_result:+.2f} | Balance: {balance:.2f}")

    # Termination Summary
    if balance >= target_balance:
        print(f"SUCCESS: Hit buyout target in {round_count} rounds! - 🔴")
    elif max_rounds is not None and round_count >= max_rounds:
        print(f"DONE: Reached end of sequence in {round_count} rounds. - 🔴")
    else:
        print(f"BUST: Bankroll hit zero in {round_count} rounds. - 🔴")


if __name__ == "__main__":
    # Handle CLI arguments: python martingale.py <initial_balance> <buyout_profit> <optional_file> <optional_bet>
    try:
        if len(sys.argv) >= 3:
            init_bal = float(sys.argv[1])
            buy_prof = float(sys.argv[2])
            seq_file = None
            bet_spec = None
            if len(sys.argv) > 3:
                candidate = sys.argv[3]
                if os.path.exists(candidate):
                    seq_file = candidate
                    bet_spec = sys.argv[4] if len(sys.argv) > 4 else None
                else:
                    bet_spec = candidate
        elif len(sys.argv) == 2:
            init_bal = float(sys.argv[1])
            buy_prof = float(input("Enter target profit (M): "))
            seq_file = None
            bet_spec = None
        else:
            init_bal = float(input("Enter initial balance (N): "))
            buy_prof = float(input("Enter target profit (M): "))
            print("\nExisting files in ../sequences/:", os.listdir('../sequences'))
            print("Example path to sequence CSV files:  ../sequences/roulette_sequence_100.csv")
            seq_file = input("\nEnter sequence CSV path (or press Enter for live): ").strip()
            if not seq_file:
                seq_file = None
            bet_spec = input("Enter bet spec (default red): ").strip()
            if not bet_spec:
                bet_spec = None

        run_martingale(init_bal, buy_prof, seq_file, bet_spec)
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
