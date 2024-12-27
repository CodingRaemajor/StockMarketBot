import yfinance as yf #imported yfinance which is yahpp finance for the data for the shares
data = yf.download("NKE", start = "2021-01-01", end = "2023-01-01") # assign the name and dates of the shares. Then , the data from yahoo finance will be as a output.
print(data.head())
data = data.dropna()
data ['MA20'] =data['Close'].rolling(window=20).mean()
data['Volatility'] = data['Close'].rolling(window=20).std()
print(data) # to print the deep data of shares named "Apple in here" or any shares

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
data[['Close','MA20','Volatility']] = scaler.fit_transform(data[['Close','MA20','Volatility']])
from sklearn.model_selection import train_test_split
X = data[['MA20','Volatility']]
y = data['Close']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle =False)

from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

# Create an imputer transformer to fill in missing values with the mean
imputer = SimpleImputer(strategy='mean')

# Create a pipeline to preprocess the data
pipeline = Pipeline(steps=[('imputer', imputer)])

# Fit the pipeline on the training data and transform both the training and test data
X_train = pipeline.fit_transform(X_train)
X_test = pipeline.transform(X_test)

from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

from sklearn.metrics import mean_squared_error
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor

param_grid = {'max_depth': [3,5,10],'n_estimators' : [50,100,200]}
grid = GridSearchCV(RandomForestRegressor(), param_grid, cv = 5)

import yfinance as yf
from flask import Flask, render_template
import plotly.graph_objs as go
import plotly.io as pio

# New Recommendation Function
def make_recommendation(data):
    if 'Close' in data.columns and 'MA20' in data.columns:
        if data['Close'].iloc[-1] > data['MA20'].iloc[-1]:
            return "Buy"
        else:
            return "Sell"
    else:
        return "Data Insufficient"

app = Flask(__name__)

@app.route('/')
def home():
    stock_name = "NKE"  # ticker symbol for Nike, can be changed dynamically
    start_date = "2021-01-01"
    end_date = "2023-01-01"

    try:
        # Download stock data from Yahoo Finance
        data = yf.download(stock_name, start=start_date, end=end_date)
        if data.empty:
            return "No data available for the selected stock and date range."

        # Drop any rows with missing data
        data = data.dropna()

        # Calculate Moving Average and Volatility
        data['MA20'] = data['Close'].rolling(window=20).mean()
        data['Volatility'] = data['Close'].rolling(window=20).std()

        # Make a recommendation based on the latest data
        recommendation = make_recommendation(data)

        # Graph creation using Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
        fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], mode='lines', name='MA20'))
        fig.update_layout(title=f'{stock_name} Stock Prices',
                          xaxis_title='Date', yaxis_title='Price')

        # Convert Plotly graph to HTML
        graph_html = pio.to_html(fig, full_html=False)

        # Prepare data for the table
        table_data = data[['Close', 'MA20', 'Volatility']].reset_index()
        table_html = table_data.to_html(classes='table table-striped table-bordered', index=False)

        # Get real-time price
        real_time_data = yf.Ticker(stock_name)
        real_time_price = real_time_data.history(period="1D")
        if 'Close' not in real_time_price.columns:
            return "Error fetching real-time data."

        real_time_price = real_time_price['Close'].iloc[0]

        return render_template('html.html',
                               stock_name=stock_name,
                               real_time_price=real_time_price,
                               graph_html=graph_html,
                               recommendation=recommendation,
                               table_html=table_html)

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
