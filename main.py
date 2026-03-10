import os
import pandas as pd
import numpy as np
import datetime as dt
import yfinance as yf
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

# Load API keys from environment variables
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')

if not ALPACA_API_KEY or not ALPACA_SECRET_KEY:
    raise ValueError("Please set ALPACA_API_KEY and ALPACA_SECRET_KEY environment variables")

BASE_URL = "https://paper-api.alpaca.markets/v2"

# Initialize the trading client
trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)


def get_vol_data():
    """Fetch VIX and VVIX data from Yahoo Finance."""
    tickers = ["^VIX", "^VVIX"]
    data = yf.download(tickers, period="3mo", interval="1d")["Close"]
    return data.dropna()


def zscore(series, window=20):
    """Calculate z-score using rolling mean and std deviation."""
    mean = series.rolling(window).mean()
    std = series.rolling(window).std()
    return (series - mean) / std


def generate_signal():
    """
    Generate trading signal based on VVIX z-score and day of week.
    
    Returns:
        str: 'ENTER', 'EXIT', or 'HOLD'
    """
    vol = get_vol_data()
    vvix = vol["^VVIX"]
    z_vvix = zscore(vvix).iloc[-1]
    
    today = dt.datetime.utcnow().weekday()
    is_late_week = today in [3, 4]  # Thursday=3, Friday=4
    
    if z_vvix > 1.5 and is_late_week:
        return "ENTER"
    elif z_vvix < 0.5:
        return "EXIT"
    else:
        return "HOLD"


def get_position(symbol):
    """Get current position for a symbol."""
    try:
        return trading_client.get_open_position(symbol)
    except Exception as e:
        print(f"No position found for {symbol}: {e}")
        return None


def place_order(symbol, side, qty):
    """Place a market order."""
    order = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=side,
        time_in_force=TimeInForce.DAY
    )
    trading_client.submit_order(order)


def run_strategy():
    """Main strategy execution loop."""
    try:
        print("Starting strategy execution...")
        
        signal = generate_signal()
        print(f"Generated Signal: {signal}")
        
        # Display current market conditions
        vol = get_vol_data()
        vvix = vol["^VVIX"]
        z_vvix = zscore(vvix).iloc[-1]
        print(f"Current VVIX Z-Score: {z_vvix:.2f}")
        print(f"Day of week: {dt.datetime.utcnow().strftime('%A')}")
        
        # Check current positions
        uga_pos = get_position("UGA")
        uso_pos = get_position("USO")
        
        if signal == "ENTER":
            print("ENTER signal - Opening positions...")
            if uga_pos is None:
                place_order("UGA", OrderSide.BUY, qty=10)
                print("✓ Bought 10 UGA")
            if uso_pos is None:
                place_order("USO", OrderSide.SELL, qty=10)
                print("✓ Sold 10 USO")
        
        elif signal == "EXIT":
            print("EXIT signal - Closing positions...")
            if uga_pos:
                place_order("UGA", OrderSide.SELL, qty=abs(int(uga_pos.qty)))
                print(f"✓ Sold {uga_pos.qty} UGA")
            if uso_pos:
                place_order("USO", OrderSide.BUY, qty=abs(int(uso_pos.qty)))
                print(f"✓ Bought back {uso_pos.qty} USO")
        
        else:
            print("HOLD signal - No action taken")
        
        print("Strategy execution complete.")
    
    except Exception as e:
        print(f"ERROR in run_strategy: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_strategy()
```
