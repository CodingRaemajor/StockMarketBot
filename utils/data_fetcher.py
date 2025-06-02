import yfinance as yf

def fetch_data(symbol, start, end):
    try:
        data = yf.download(symbol, start=start, end=end)
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None