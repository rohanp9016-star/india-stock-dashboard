import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time

st.set_page_config(
    page_title="🇮🇳 Indian Stock Scanner",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0D1117; color: #E6EDF3; }
    .stApp { background-color: #0D1117; }
    .metric-card {
        background: #161B22;
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid #21262D;
        margin-bottom: 10px;
    }
    .up   { color: #00D4AA; font-weight: bold; }
    .down { color: #FF4D6D; font-weight: bold; }
    .neutral { color: #FFB830; font-weight: bold; }
    h1, h2, h3 { color: #E6EDF3; }
    .stDataFrame { border-radius: 8px; }
    div[data-testid="metric-container"] {
        background: #161B22;
        border: 1px solid #21262D;
        border-radius: 10px;
        padding: 10px 14px;
    }
</style>
""", unsafe_allow_html=True)

# ── Stock Universe ───────────────────────────────────────────────────────────
NSE_STOCKS = {
    # Nifty 50 + popular mid-caps
    "RELIANCE":    {"sl_pct": 4.0, "tg_pct": 7.0},
    "TCS":         {"sl_pct": 4.5, "tg_pct": 6.5},
    "HDFCBANK":    {"sl_pct": 4.0, "tg_pct": 7.5},
    "INFY":        {"sl_pct": 4.5, "tg_pct": 7.0},
    "ICICIBANK":   {"sl_pct": 4.5, "tg_pct": 6.0},
    "HINDUNILVR":  {"sl_pct": 3.5, "tg_pct": 6.0},
    "WIPRO":       {"sl_pct": 5.0, "tg_pct": 8.0},
    "TATAMOTORS":  {"sl_pct": 5.5, "tg_pct": 9.0},
    "SUNPHARMA":   {"sl_pct": 4.0, "tg_pct": 7.0},
    "BAJFINANCE":  {"sl_pct": 5.0, "tg_pct": 9.0},
    "ADANIENT":    {"sl_pct": 6.0, "tg_pct":10.0},
    "AXISBANK":    {"sl_pct": 4.5, "tg_pct": 7.5},
    "KOTAKBANK":   {"sl_pct": 4.0, "tg_pct": 6.5},
    "LT":          {"sl_pct": 4.0, "tg_pct": 7.0},
    "MARUTI":      {"sl_pct": 4.5, "tg_pct": 8.0},
    "NTPC":        {"sl_pct": 3.5, "tg_pct": 6.5},
    "ONGC":        {"sl_pct": 4.0, "tg_pct": 7.0},
    "POWERGRID":   {"sl_pct": 3.5, "tg_pct": 6.0},
    "SBIN":        {"sl_pct": 5.0, "tg_pct": 9.0},
    "TATASTEEL":   {"sl_pct": 5.5, "tg_pct": 9.5},
    "TECHM":       {"sl_pct": 5.0, "tg_pct": 8.5},
    "TITAN":       {"sl_pct": 4.0, "tg_pct": 7.0},
    "ULTRACEMCO":  {"sl_pct": 4.0, "tg_pct": 7.5},
    "ZOMATO":      {"sl_pct": 6.0, "tg_pct":11.0},
    "PAYTM":       {"sl_pct": 7.0, "tg_pct":13.0},
}

SECTOR_MAP = {
    "RELIANCE": "Energy",   "ONGC": "Energy",
    "TCS": "IT",            "INFY": "IT",    "WIPRO": "IT",  "TECHM": "IT",
    "HDFCBANK": "Banking",  "ICICIBANK": "Banking", "AXISBANK": "Banking",
    "KOTAKBANK": "Banking", "SBIN": "Banking",
    "TATAMOTORS": "Auto",   "MARUTI": "Auto",
    "SUNPHARMA": "Pharma",
    "BAJFINANCE": "NBFC",
    "ADANIENT": "Conglomerate",
    "LT": "Infra",          "NTPC": "Power", "POWERGRID": "Power",
    "HINDUNILVR": "FMCG",   "TITAN": "Consumer",
    "TATASTEEL": "Metals",  "ULTRACEMCO": "Cement",
    "ZOMATO": "Internet",   "PAYTM": "Fintech",
}

# ── Helpers ──────────────────────────────────────────────────────────────────
@st.cache_data(ttl=120)  # refresh every 2 minutes
def fetch_stock_data(symbols: list) -> pd.DataFrame:
    rows = []
    for sym in symbols:
        ticker = sym + ".NS"
        try:
            info = yf.Ticker(ticker).fast_info
            cmp  = round(info.last_price, 2)
            prev = round(info.previous_close, 2)
            chg  = round((cmp - prev) / prev * 100, 2)
            cfg  = NSE_STOCKS[sym]
            sl   = round(cmp * (1 - cfg["sl_pct"] / 100), 2)
            tg   = round(cmp * (1 + cfg["tg_pct"] / 100), 2)
            rr   = round((tg - cmp) / (cmp - sl), 2)
            sl_d = round((cmp - sl) / cmp * 100, 2)
            tg_d = round((tg - cmp) / cmp * 100, 2)
            rows.append({
                "Symbol":    sym,
                "Sector":    SECTOR_MAP.get(sym, "Other"),
                "CMP (₹)":   cmp,
                "Prev Close":prev,
                "Day Chg %": chg,
                "Stop Loss": sl,
                "Target":    tg,
                "SL Dist %": sl_d,
                "TG Dist %": tg_d,
                "R:R Ratio": rr,
                "Signal":    "🟢 BUY" if (chg > 0 and rr >= 1.5) else ("🔴 AVOID" if chg < -1 else "🟡 WATCH"),
            })
        except Exception:
            pass
    return pd.DataFrame(rows)


def color_row(val, col):
    if col == "Day Chg %":
        return "color: #00D4AA" if val > 0 else "color: #FF4D6D"
    if col == "R:R Ratio":
        if val >= 2: return "color: #00D4AA; font-weight:bold"
        if val >= 1.5: return "color: #FFB830"
        return "color: #FF4D6D"
    return ""


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/4/41/Flag_of_India.svg/320px-Flag_of_India.svg.png", width=60)
    st.title("⚙️ Scanner Settings")
    selected = st.multiselect(
        "Select Stocks",
        options=list(NSE_STOCKS.keys()),
        default=list(NSE_STOCKS.keys())[:10]
    )
    min_rr = st.slider("Min R:R Ratio Filter", 0.5, 4.0, 1.5, 0.1)
    sectors = st.multiselect(
        "Filter by Sector",
        options=sorted(set(SECTOR_MAP.values())),
        default=[]
    )
    auto_refresh = st.checkbox("Auto-refresh (2 min)", value=True)
    st.markdown("---")
    st.caption("Data via Yahoo Finance (NSE). Refreshes every 2 min.")
    st.caption(f"🕒 Last loaded: {datetime.now().strftime('%H:%M:%S')}")

if not selected:
    st.warning("Please select at least one stock from the sidebar.")
    st.stop()

# ── Fetch Data ───────────────────────────────────────────────────────────────
with st.spinner("📡 Scanning NSE stocks..."):
    df = fetch_stock_data(selected)

if df.empty:
    st.error("Could not fetch data. Check internet connection or try again.")
    st.stop()

if sectors:
    df = df[df["Sector"].isin(sectors)]

df_filtered = df[df["R:R Ratio"] >= min_rr].reset_index(drop=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("## 🇮🇳 Indian Stock Market Scanner Dashboard")
st.markdown(f"**{datetime.now().strftime('%A, %d %B %Y  |  %H:%M IST')}** &nbsp;|&nbsp; Powered by NSE data via Yahoo Finance")
st.markdown("---")

# ── KPI Metrics Row ──────────────────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("📋 Stocks Scanned", len(df))
col2.metric("🟢 Buy Signals",    len(df[df["Signal"] == "🟢 BUY"]))
col3.metric("🟡 Watch",          len(df[df["Signal"] == "🟡 WATCH"]))
col4.metric("🔴 Avoid",          len(df[df["Signal"] == "🔴 AVOID"]))
col5.metric("⭐ High R:R (≥2x)", len(df[df["R:R Ratio"] >= 2]))

st.markdown("---")

# ── Main Table ───────────────────────────────────────────────────────────────
st.subheader("📊 Full Watchlist")
st.dataframe(
    df.style.applymap(lambda v: "color:#00D4AA;font-weight:bold" if v > 0 else "color:#FF4D6D;font-weight:bold",
                      subset=["Day Chg %"])
           .applymap(lambda v: "color:#00D4AA;font-weight:bold" if v >= 2
                               else ("color:#FFB830" if v >= 1.5 else "color:#FF4D6D"),
                     subset=["R:R Ratio"]),
    use_container_width=True, height=420
)

st.markdown("---")

# ── Two Column Charts ────────────────────────────────────────────────────────
chart_left, chart_right = st.columns(2)

with chart_left:
    st.subheader("📈 Day % Change")
    fig_chg = go.Figure(go.Bar(
        x=df["Symbol"], y=df["Day Chg %"],
        marker_color=["#00D4AA" if c >= 0 else "#FF4D6D" for c in df["Day Chg %"]],
        text=[f"{c:+.2f}%" for c in df["Day Chg %"]],
        textposition="outside"
    ))
    fig_chg.update_layout(
        paper_bgcolor="#161B22", plot_bgcolor="#0D1117",
        font=dict(color="#E6EDF3"), margin=dict(t=30,b=30,l=20,r=20),
        yaxis=dict(gridcolor="#21262D", zeroline=True, zerolinecolor="#7B8FA1"),
        xaxis=dict(gridcolor="#21262D")
    )
    st.plotly_chart(fig_chg, use_container_width=True)

with chart_right:
    st.subheader("⚖️ Risk:Reward Ratio")
    rr_colors = ["#00D4AA" if r >= 2 else ("#FFB830" if r >= 1.5 else "#FF4D6D") for r in df["R:R Ratio"]]
    fig_rr = go.Figure(go.Bar(
        x=df["Symbol"], y=df["R:R Ratio"],
        marker_color=rr_colors,
        text=[f"{r:.2f}x" for r in df["R:R Ratio"]],
        textposition="outside"
    ))
    fig_rr.add_hline(y=2, line_dash="dash", line_color="#00D4AA",
                     annotation_text="Ideal ≥ 2x", annotation_font_color="#00D4AA")
    fig_rr.update_layout(
        paper_bgcolor="#161B22", plot_bgcolor="#0D1117",
        font=dict(color="#E6EDF3"), margin=dict(t=30,b=30,l=20,r=20),
        yaxis=dict(gridcolor="#21262D"),
        xaxis=dict(gridcolor="#21262D")
    )
    st.plotly_chart(fig_rr, use_container_width=True)

st.markdown("---")

# ── CMP vs SL vs Target ──────────────────────────────────────────────────────
st.subheader("🎯 CMP vs Stop Loss vs Target (₹)")
fig_levels = go.Figure()
fig_levels.add_trace(go.Bar(name="Stop Loss", x=df["Symbol"], y=df["Stop Loss"],  marker_color="#FF4D6D"))
fig_levels.add_trace(go.Bar(name="CMP",       x=df["Symbol"], y=df["CMP (₹)"],    marker_color="#00D4AA"))
fig_levels.add_trace(go.Bar(name="Target",    x=df["Symbol"], y=df["Target"],     marker_color="#FFB830"))
fig_levels.update_layout(
    barmode="group",
    paper_bgcolor="#161B22", plot_bgcolor="#0D1117",
    font=dict(color="#E6EDF3"), margin=dict(t=10,b=30,l=20,r=20),
    legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="center", x=0.5),
    yaxis=dict(gridcolor="#21262D"),
    xaxis=dict(gridcolor="#21262D")
)
st.plotly_chart(fig_levels, use_container_width=True)

st.markdown("---")

# ── Sector Breakdown ─────────────────────────────────────────────────────────
row3_left, row3_right = st.columns([1, 2])

with row3_left:
    st.subheader("🏭 Sector Breakdown")
    sec_df = df["Sector"].value_counts().reset_index()
    sec_df.columns = ["Sector", "Count"]
    fig_pie = go.Figure(go.Pie(
        labels=sec_df["Sector"], values=sec_df["Count"],
        hole=0.45, textinfo="label+percent"
    ))
    fig_pie.update_layout(
        paper_bgcolor="#161B22", font=dict(color="#E6EDF3"),
        margin=dict(t=10,b=10,l=10,r=10),
        legend=dict(orientation="v", x=1.0)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with row3_right:
    st.subheader(f"⭐ Top Picks (R:R ≥ {min_rr}x)")
    if df_filtered.empty:
        st.info("No stocks match the current R:R filter. Lower the threshold in the sidebar.")
    else:
        for _, row in df_filtered.iterrows():
            chg_color = "up" if row["Day Chg %"] > 0 else "down"
            st.markdown(f"""
            <div class='metric-card'>
                <b style='font-size:18px;'>{row['Symbol']}</b>
                &nbsp;<span style='color:#7B8FA1;font-size:13px;'>{row['Sector']}</span>
                &nbsp;&nbsp;<span class='{chg_color}'>{row['Day Chg %']:+.2f}%</span>
                &nbsp;&nbsp;<span class='neutral'>{row['Signal']}</span><br>
                <span style='color:#aaa;font-size:13px;'>
                    CMP: <b style='color:#E6EDF3;'>₹{row['CMP (₹)']:,.2f}</b>
                    &nbsp;| SL: <b style='color:#FF4D6D;'>₹{row['Stop Loss']:,.2f}</b>
                    &nbsp;| TG: <b style='color:#FFB830;'>₹{row['Target']:,.2f}</b>
                    &nbsp;| R:R: <b style='color:#00D4AA;'>{row['R:R Ratio']}x</b>
                </span>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")

# ── Candlestick for selected stock ───────────────────────────────────────────
st.subheader("🕯️ Candlestick Chart")
candle_sym = st.selectbox("Pick a stock for detailed view", df["Symbol"].tolist())

@st.cache_data(ttl=300)
def get_candle(sym):
    hist = yf.Ticker(sym + ".NS").history(period="3mo", interval="1d")
    return hist

candle_df = get_candle(candle_sym)
if not candle_df.empty:
    fig_c = go.Figure(go.Candlestick(
        x=candle_df.index,
        open=candle_df["Open"], high=candle_df["High"],
        low=candle_df["Low"],   close=candle_df["Close"],
        increasing_line_color="#00D4AA",
        decreasing_line_color="#FF4D6D"
    ))
    # Overlay SL & Target lines
    sym_row = df[df["Symbol"] == candle_sym].iloc[0]
    fig_c.add_hline(y=sym_row["Stop Loss"], line_dash="dash", line_color="#FF4D6D",
                    annotation_text=f"SL ₹{sym_row['Stop Loss']:,.0f}", annotation_font_color="#FF4D6D")
    fig_c.add_hline(y=sym_row["Target"],    line_dash="dash", line_color="#FFB830",
                    annotation_text=f"TG ₹{sym_row['Target']:,.0f}",    annotation_font_color="#FFB830")
    fig_c.update_layout(
        paper_bgcolor="#161B22", plot_bgcolor="#0D1117",
        font=dict(color="#E6EDF3"), xaxis_rangeslider_visible=False,
        margin=dict(t=10,b=10,l=10,r=10),
        yaxis=dict(gridcolor="#21262D"), xaxis=dict(gridcolor="#21262D")
    )
    st.plotly_chart(fig_c, use_container_width=True)

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("⚠️ This dashboard is for **educational purposes only**. Not SEBI-registered investment advice. Always do your own research before trading.")

if auto_refresh:
    time.sleep(120)
    st.rerun()
