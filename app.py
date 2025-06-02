# app.py
import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
from utils.data_fetcher import fetch_data
from utils.indicators import compute_indicators
from utils.visuals import plot_rsi_chart, plot_candlestick_chart
from utils.portfolio import calculate_portfolio, get_allocation_data, get_portfolio_history

# --- Page Setup ---
st.set_page_config(page_title="📈 StockMarket Bot v2", layout="wide")
st.markdown("""
    <style>
        html, body, .main {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f8f9fa;
            color: #212529;
        }
        .block-container {
            padding: 2rem 2rem 3rem;
        }
        h1, h2, h3, .stMarkdown h2 {
            color: #003262;
        }
        .stTextInput > label, .stDateInput > label, .stTextArea > label {
            font-weight: 600;
        }
        .css-1aumxhk, .css-1v3fvcr {
            padding-top: 1rem !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
# 📈 StockMarket Bot v2
*Smart Stock Analysis & Portfolio Insights.*
""")

# Sidebar - Global Ticker Input
st.sidebar.header("🔍 Search Global Stocks")
ticker_symbol = st.sidebar.text_input("Stock Ticker (e.g., AAPL, NVDA, TCS.NS, BABA, SHOP.TO)", value="AAPL")

today = datetime.date.today()
start_date = st.sidebar.date_input("Start Date", today - datetime.timedelta(days=180))
end_date = st.sidebar.date_input("End Date", today)

st.markdown("---")

# --- Stock Analysis Section ---
st.markdown("## 🧾 Stock Technical Analysis")
if ticker_symbol:
    with st.spinner("📡 Fetching data..."):
        stock_data = fetch_data(ticker_symbol, start_date, end_date)

    if stock_data is not None and not stock_data.empty:
        st.write(f"📦 Data points retrieved: {stock_data.shape[0]}")

        if stock_data.shape[0] < 10:
            st.warning("Not enough data to compute meaningful indicators. Try a wider date range.")
        else:
            stock_data = compute_indicators(stock_data)
            stock_data.index = pd.to_datetime(stock_data.index)

            st.subheader(f"📊 SMA/EMA Price Chart for {ticker_symbol}")
            st.caption("Shows candlesticks with overlays for Simple and Exponential Moving Averages")
            st.plotly_chart(plot_candlestick_chart(stock_data), use_container_width=True)

            st.subheader(f"📈 RSI Trend for {ticker_symbol}")
            st.caption("Relative Strength Index (RSI): Below 30 = Oversold, Above 70 = Overbought")
            st.plotly_chart(plot_rsi_chart(stock_data), use_container_width=True)

            st.subheader("📌 RSI-Based Signal")
            latest_rsi = stock_data['RSI'].iloc[-1]
            st.write(f"**Latest RSI for {ticker_symbol}:** {latest_rsi:.2f}")

            if latest_rsi < 30:
                st.success("🟢 RSI is below 30 → Stock is oversold. **Buy signal.**")
            elif latest_rsi > 70:
                st.error("🔴 RSI is above 70 → Stock is overbought. **Sell signal.**")
            else:
                st.info("🟡 RSI is neutral. **Hold / Wait.**")

            st.subheader(f"📄 Raw Data for {ticker_symbol} (Last 10 Days)")
            styled_table = stock_data.tail(10).style.format({
                'Open': '${:,.2f}', 'High': '${:,.2f}', 'Low': '${:,.2f}',
                'Close': '${:,.2f}', 'SMA_20': '${:,.2f}', 'EMA_20': '${:,.2f}'
            })
            st.dataframe(styled_table)
    else:
        st.warning("No data available for the selected ticker or range. Please check the symbol and try again.")
else:
    st.info("Please enter a stock ticker to view data.")

# --- Portfolio Tracker Section ---
st.markdown("---")
st.markdown("## 💼 Portfolio Tracker")

portfolio_result_df = None
portfolio_input = []
with st.form("portfolio_form"):
    st.write("Enter your stock portfolio below:")
    col1, col2, col3 = st.columns(3)
    with col1:
        tickers = st.text_area("Tickers", placeholder="e.g., AAPL,TSLA,NVDA")
    with col2:
        quantities = st.text_area("Quantities", placeholder="e.g., 5,10,3")
    with col3:
        buy_prices = st.text_area("Buy Prices", placeholder="e.g., 150,700,200")

    submitted = st.form_submit_button("Calculate Portfolio")

    if submitted:
        with st.spinner("🔄 Calculating your portfolio..."):
            try:
                if not tickers or not quantities or not buy_prices:
                    raise ValueError("All fields must be filled.")

                ticker_list = [x.strip().upper() for x in tickers.split(",")]
                quantity_list = [int(x.strip()) for x in quantities.split(",")]
                price_list = [float(x.strip()) for x in buy_prices.split(",")]

                if len(ticker_list) != len(quantity_list) or len(ticker_list) != len(price_list):
                    raise ValueError("All lists must have the same length.")

                for i in range(len(ticker_list)):
                    portfolio_input.append({
                        "ticker": ticker_list[i],
                        "quantity": quantity_list[i],
                        "buy_price": price_list[i]
                    })

                portfolio_result_df = calculate_portfolio(portfolio_input)
                st.success("✅ Portfolio calculated successfully!")
                st.subheader("📊 Portfolio Summary")
                st.dataframe(portfolio_result_df[portfolio_result_df['Ticker'] != 'TOTAL'])

            except Exception as e:
                st.error(f"❌ Error: {e}. Please check your inputs.")

# 📥 Download + Allocation Chart + History
if portfolio_result_df is not None and not portfolio_result_df.empty:
    csv = portfolio_result_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Portfolio as CSV",
        data=csv,
        file_name='portfolio_summary.csv',
        mime='text/csv'
    )

    st.subheader("📈 Portfolio Allocation")
    alloc_df = get_allocation_data(portfolio_result_df)
    if not alloc_df.empty:
        fig = px.pie(alloc_df, names='Ticker', values='Value', title='Portfolio Allocation by Value')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("🧺 No allocation data to display yet.")

    st.subheader("📅 Historical Portfolio Value")
    with st.spinner("🔁 Retrieving history data..."):
        history_df = get_portfolio_history(portfolio_input, start_date, end_date)
    if not history_df.empty:
        fig2 = px.line(history_df, x=history_df.index, y='Total Value', title='Portfolio Value Over Time')
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("📭 No historical data found for the selected stocks and range.")

# Footer
st.markdown("""
---
<center><sub>🚀 Built with ❤️ by Parth Patel • <a href='https://github.com/CodingRaemajor' target='_blank'><img src='https://cdn-icons-png.flaticon.com/512/733/733553.png' width='18' style='vertical-align:middle; margin-left:4px;'/></a></sub></center>
""", unsafe_allow_html=True)