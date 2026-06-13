# 🇮🇳 Indian Stock Market Scanner Dashboard

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=rohanp9016-star/india-stock-dashboard&branch=main&mainModule=app.py)

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

## ☁️ Deploy on Streamlit Cloud (Free, No Install)

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Sign in with your **GitHub account** (`rohanp9016-star`)
3. Click **"New app"**
4. Fill in:
   - **Repository:** `rohanp9016-star/india-stock-dashboard`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **"Deploy!"**

Your app will be live at:
```
https://rohanp9016-star-india-stock-dashboard-app-XXXX.streamlit.app
```

---

## 🚀 Local Quick Start

```bash
git clone https://github.com/rohanp9016-star/india-stock-dashboard.git
cd india-stock-dashboard
pip install -r requirements.txt
streamlit run app.py
```

Opens at **http://localhost:8501**

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

This tool is for **educational purposes only**. Not SEBI-registered investment advice.
