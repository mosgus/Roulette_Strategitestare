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


def _slugify_label(label):
    return ''.join(c for c in label if c.isalnum() or c in ('-', '_'))


def run_martingale(initial_balance, buyout, sequence_path=None, bet_spec=None):
    balance = initial_balance
    target_balance = initial_balance + buyout
    current_wager = 1.0
    round_count = 0
    rows = []
    bet_label_for_file = bb.build_bet_from_spec(bet_spec, 1.0)[1]

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
            print(f"Can't afford wager of ${current_wager:.2f}. Going all-in with ${balance:.2f} - 🟡")
            current_wager = balance

        # 2. Construct the bet
        bet_array, bet_label = bb.build_bet_from_spec(bet_spec, current_wager)

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

        rows.append({
            'Round': round_count,
            'Bet': bet_label,
            'Winning Number': win_label,
            'Color': color,
            'Net': f"{net_result:+.2f}",
            'Balance': f"{balance:.2f}",
        })

        print(f"Round {round_count}: Bet on {bet_label} | Landed on {win_label} ({color}) | Net: ${net_result:+.2f} | Balance: ${balance:.2f}")

    # Termination Summary
    if balance >= target_balance:
        outcome_label = "SUCCESS"
        print(f"{outcome_label}: Hit buyout target in {round_count} rounds! - 🔴")
    elif max_rounds is not None and round_count >= max_rounds:
        outcome_label = "DONE"
        print(f"{outcome_label}: Reached end of sequence in {round_count} rounds. - 🔴")
    else:
        outcome_label = "BUST"
        print(f"{outcome_label}: Bankroll hit zero in {round_count} rounds. - 🔴")

    n_str = int(initial_balance)
    m_str = int(buyout)
    bet_slug = _slugify_label(bet_label_for_file)
    filename = f"martingale_{n_str}n{m_str}m{bet_slug}.csv"

    dir = './strat_data'
    os.makedirs(dir, exist_ok=True)
    path = os.path.join(dir, filename)
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=['Round', 'Bet', 'Winning Number', 'Color', 'Net', 'Balance'],
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nSaved results to {path}")


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
