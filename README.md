# 📈 StockMarket Bot v2

An elegant and powerful Streamlit-based web app to:
- 🔍 Analyze global stocks with RSI, SMA, EMA
- 💡 Get Buy/Hold/Sell signals based on RSI
- 💼 Track your portfolio with real-time profit/loss
- 📊 Visualize your portfolio allocation and growth

---

## 🚀 Features

### 📊 Technical Analysis
- Real-time stock price chart with SMA and EMA overlays
- RSI chart with Buy/Sell/Hold signal interpretation
- Global stock support (e.g., `AAPL`, `TSLA`, `TCS.NS`, `SHOP.TO`, `BABA`)

### 💼 Portfolio Tracker
- Enter stocks, quantity, and buy price
- Calculates total P/L and % gain/loss
- Downloadable CSV summary
- Pie chart for allocation
- Historical value graph

---

## 🧪 Preview

![App Screenshot](https://github.com/CodingRaemajor/StockMarketBot/blob/main/screenshot.png)

---

## 🛠️ Tech Stack

- **Frontend/UI**: Streamlit
- **Data**: yfinance, pandas
- **Charts**: Plotly
- **Optional Tools**: pyarrow, vaderSentiment (if enabled later)

---

## 📦 Setup & Installation

```bash
git clone https://github.com/CodingRaemajor/StockMarketBot.git
cd StockMarketBot
pip install -r requirements.txt
streamlit run app.py

☁️ Deploy to Streamlit Cloud
Push this repo to GitHub

Go to "https://stockmarketbot.streamlit.app/"

Link your GitHub and select app.py to deploy

Done! 🎉

👨‍💻 Author
Built with 💙 by Parth Patel


Would you like a matching `screenshot.png` for your repo or a walkthrough GIF for better visuals on the README?
