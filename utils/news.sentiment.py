import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def fectch_news(ticker):
    url = f'https://query1.finance.yahoo.com/v1/finance/search?q={ticker}'
    try:
        response = requests.get(url).json()
        return response.get("quotes", [])
    except:
        return []
    
def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)
    return score['compound']