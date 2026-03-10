# VVIX-Based Energy Pairs Trading Strategy

An automated trading algorithm that uses volatility-of-volatility signals to execute pairs trades in energy commodity ETFs.

---

## 📊 Strategy Overview

This algorithm monitors the CBOE VVIX index (volatility of VIX) to generate trading signals for a long/short position in energy ETFs:
- **Long**: UGA (United States Gasoline Fund)
- **Short**: USO (United States Oil Fund)

---

## 🎯 Signal Logic

### Entry Conditions
Both conditions must be met:
- VVIX z-score > 1.5 (20-day rolling window)
- Current day is Thursday or Friday

### Exit Conditions
- VVIX z-score < 0.5

---

## 🛠️ Technical Implementation

| Component | Technology |
|-----------|------------|
| Data Source | Yahoo Finance API |
| Execution | Alpaca Trading API (Paper) |
| Position Sizing | Fixed 10 shares per leg |
| Order Type | Market orders, day duration |

---

## 📦 Dependencies
```python
pandas        # Data manipulation and rolling statistics
numpy         # Numerical computations
yfinance      # Market data retrieval
alpaca-py     # Trade execution
```

---

## 📁 Project Structure
```
.
├── strategy.py          # Main strategy logic and execution
├── README.md           # This file
└── requirements.txt    # Python dependencies
```

---

## 🚀 Getting Started

1. **Clone the repository**
```bash
   git clone https://github.com/yourusername/vvix-energy-pairs.git
   cd vvix-energy-pairs
```

2. **Install dependencies**
```bash
   pip install -r requirements.txt
```

3. **Set environment variables**
```bash
   export ALPACA_API_KEY="your_key_here"
   export ALPACA_SECRET_KEY="your_secret_here"
```

4. **Run the strategy**
```bash
   python strategy.py
```

---

## ⚠️ Risk Disclosure

This is an experimental algorithmic trading strategy developed for **educational purposes only**. 

- Past performance does not guarantee future results
- Trading involves substantial risk of loss
- This strategy has not been validated on out-of-sample data
- Use paper trading to test before risking real capital

---

## 📝 License

MIT License - See LICENSE file for details

---

## 👤 Author

**Nicolas Sandoval**
- High School Student, Coral Reef Senior High
- Interested in Quantitative Finance & Algorithmic Trading

---

## 🤝 Contributing

Feedback and suggestions welcome! Feel free to open an issue or submit a pull request.
