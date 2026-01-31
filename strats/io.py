"""
    Shared I/O helpers for strategy scripts.
"""

import csv
import os


def load_sequence(sequence_path):
    if not sequence_path or not os.path.exists(sequence_path):
        return []
    with open(sequence_path, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_results(rows, out_dir, filename, fieldnames):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, filename)
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)
    return path
