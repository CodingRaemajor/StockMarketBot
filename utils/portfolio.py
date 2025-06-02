import yfinance as yf
import pandas as pd

def calculate_portfolio(stocks):
    data = []
    total_cost = 0
    total_value = 0

    for stock in stocks:
        ticker = stock['ticker']
        quantity = stock['quantity']
        buy_price = stock['buy_price']

        info = yf.Ticker(ticker).history(period="1d")
        if info.empty:
            continue

        current_price = info['Close'].iloc[-1] # iloc: a way to access rows and cloumns of a DataFrame by their integer position
        cost = quantity * buy_price
        value = quantity * current_price

        total_cost += cost
        total_value += value


        profit_loss = total_value - total_cost
        return_pct = (profit_loss / total_cost) * 100 if total_cost > 0 else 0

        data.append({
            "Ticker" : ticker.upper(),
            "Quantity" : quantity,
            "Buy Price" : f"${buy_price:.2f}",
            "Current Price" : f"${current_price:.2f}",
            "Total Cost" : f"${total_cost:.2f}",
            "Current Value" : f"${total_value:.2f}",
            "P/L ($)" : f"${profit_loss:.2f}",
            "P/L (%)" : f"{return_pct:.2f}%",
            "_raw_value" : value # for plotting
        })

    df = pd.DataFrame(data)

    if not df.empty:
        total_pl = total_value = total_cost
        total_return_pct = (total_pl / total_cost) * 100 if total_cost > 0 else 0
        total_summary = pd.DataFrame([{
            "Ticker": "TOTAL",
            "Quantity": None,
            "Buy Price": None,
            "Current Price": None,
            "Total Cost": f"${total_cost:.2f}",
            "Current Value": f"${total_value:.2f}",
            "P/L ($)": f"${total_pl:.2f}",
            "P/L (%)": f"{total_return_pct:.2f}%",
            "_raw_value": total_value
        }])
        df = pd.concat([df, total_summary], ignore_index=True)
    
    return df

def get_allocation_data(df):
    df = df[df['Ticker'] != 'TOTAL']
    return df[['Ticker', '_raw_value']].rename(columns={'_raw_value': 'Value'})

def get_portfolio_history(portfolio, start_date, end_date):
    prices_df = pd.DataFrame()

    for stock in portfolio:
        ticker = stock['ticker']
        quantity = stock['quantity']

        hist = yf.download(ticker, start=start_date, end=end_date)['Close']
        if hist.empty:
            continue
        prices_df[ticker] = hist * quantity

    prices_df['Total Value'] = prices_df.sum(axis=1)
    return prices_df[['Total Value']].dropna()
