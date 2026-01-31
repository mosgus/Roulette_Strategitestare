# Roulette Lab 🎰🧪

(FREE American Roulette Datasets in /sequences)

A Python (3.x) sandbox for simulating American Roulette, generating deterministic spin sequences, and testing betting strategies (currently Martingale). Includes CSV outputs and simple charting for win rate and balance curves.

The **⚪️ Sequence Generator ⚪️** creates reproducible roulette spin CSVs in `/sequences`, while the **🔴 Martingale Strategy 🔴** can run live RNG or replay a sequence file and export run stats to `/strats/strat_data`.

### Features ⛮

+ **Sequence Generation** ◻️  
  + `generate_seq.py` produces `roulette_sequence_<N>.csv` in `/sequences`.  
  + Columns: `Round, Winning Number, Winning Index, Color`.  
  + Built-in limits and validation for large sequences.  

+ **Strategy Simulation (Martingale)** ◻️  
  + Run with live RNG or a sequence CSV.  
  + Tracks per-round output and saves CSV results to `/strats/strat_data`.  
  + Output columns: `Round, Bet, Winning Number, Color, Net, Balance`.  

+ **Bet Builder (Modular)** ◻️  
  + `build_bet_from_spec` supports common bets, combined bets, and custom arrays.  
  + Uses `combine_bets` to stack multiple bet types.  

+ **Charts & Analysis** ◻️  
  + `strats/strat_data/chart.py` overlays all martingale runs on two charts.  
  + Outputs to `/strats/strat_data/charts`:  
    + `win_probability.png` (cumulative win rate)  
    + `balance.png` (balance over rounds)  


### Dependencies
Conda 🐍
```bash
conda install -c conda-forge matplotlib
```

Bash 🐧
```bash
pip install --upgrade pip
pip install matplotlib
```

PowerShell 📎
```powershell
python -m pip install --upgrade pip
python -m pip install matplotlib
```


### How to Run

**Generate a sequence**
```bash
python generate_seq.py 200
```

**Run Martingale (live RNG)**
```bash
python -m strats.martingale 100 80 red
```

**Run Martingale (sequence CSV)**
```bash
python -m strats.martingale 100 80 ./sequences/roulette_sequence_200.csv red
```

**Make charts from all runs**
```bash
python strats/strat_data/chart.py
```


### Bet Spec Examples
Single bet:
```bash
red
```
Combined bets:
```bash
red+1st12
```
Single number:
```bash
number:17
```
Custom 38-slot array (scaled to wager):
```bash
custom:0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
```

Supported bet keywords:
`red, black, green, even, odd, low, high, 1st12, 2nd12, 3rd12, col_a, col_b, col_c, number:<tile>, custom:<38 values>`


### File Outputs
- **Sequences** → `/sequences/roulette_sequence_<N>.csv`  
- **Strategy Runs** → `/strats/strat_data/martingale_<N>n<M>m<Bet>.csv`  
- **Charts** → `/strats/strat_data/charts/*.png`  


### Future Developments
- Add more strategies (Fibonacci, custom progressions).  
- Expand charting (rolling win rate, drawdown, ROI).  
- Add unit tests and validation of sequence files.  


### Contributions
Gus created the Roulette Lab and strategy framework, iterating on simulations, bet tooling, and analysis output.
