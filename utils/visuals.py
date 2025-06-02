# utils/visuals.py
import plotly.graph_objects as go

# RSI = Relative Strength Index
# It measures the magnitude of recent price changes to evaluate overbought or oversold conditions in the price of a stock.
# RSI ranges from 0 to 100:
# - Above 70 = overbought (potential sell signal)
# - Below 30 = oversold (potential buy signal)

def plot_price_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Close'))
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], name='SMA 20'))
    fig.add_trace(go.Scatter(x=data.index, y=data['EMA_20'], name='EMA 20'))
    fig.update_layout(title='Stock Price & Moving Averages', xaxis_title='Date', yaxis_title='Price')
    return fig

def plot_rsi_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], name='RSI'))
    fig.update_layout(title='RSI Indicator', xaxis_title='Date', yaxis_title='RSI')
    return fig

def plot_candlestick_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], mode='lines', name='SMA 20'))
    fig.add_trace(go.Scatter(x=data.index, y=data['EMA_20'], mode='lines', name='EMA 20'))
    fig.update_layout(title='SMA and EMA Chart', xaxis_title='Date', yaxis_title='Price')
    return fig