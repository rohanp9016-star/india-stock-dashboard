# 🇮🇳 Indian Stock Market Scanner Dashboard

A **live, browser-based dashboard** that scans NSE-listed Indian stocks and displays:

- 📈 **Real-time CMP** (Current Market Price) via Yahoo Finance
- 🛑 **Stop Loss (SL)** levels auto-calculated from CMP
- 🎯 **Target (TG)** prices with configurable % upside
- ⚖️ **Risk:Reward (R:R)** ratio per stock
- 🕯️ **Candlestick chart** with SL & Target overlays
- 🏭 **Sector diversification** pie chart
- 🟢 **Buy / Watch / Avoid** signal labels
- ⚙️ **Sidebar filters** — sector, R:R threshold, stock picker
- 🔄 **Auto-refresh** every 2 minutes

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/rohanp9016-star/india-stock-dashboard.git
cd india-stock-dashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the dashboard
```bash
streamlit run app.py
```

The dashboard will open at **http://localhost:8501** in your browser.

---

## 📦 Tech Stack

| Tool | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web app framework |
| [yfinance](https://github.com/ranaroussi/yfinance) | NSE/BSE live data |
| [Plotly](https://plotly.com) | Interactive charts |
| [Pandas](https://pandas.pydata.org) | Data wrangling |

---

## 🗂️ Stocks Covered (Nifty 50 + Mid-caps)

RELIANCE, TCS, HDFCBANK, INFY, ICICIBANK, HINDUNILVR, WIPRO, TATAMOTORS, SUNPHARMA, BAJFINANCE, ADANIENT, AXISBANK, KOTAKBANK, LT, MARUTI, NTPC, ONGC, POWERGRID, SBIN, TATASTEEL, TECHM, TITAN, ULTRACEMCO, ZOMATO, PAYTM

---

## ⚠️ Disclaimer

This tool is for **educational purposes only**. Not SEBI-registered investment advice. Always consult a SEBI-registered advisor before making investment decisions.
