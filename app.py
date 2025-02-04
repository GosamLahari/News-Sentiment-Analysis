from flask import Flask, request, jsonify, render_template
import requests
from textblob import TextBlob
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

NEWS_API_KEY = "ac39e2eca7c34ad6bd4c9a2ace08fef1"

# Function to fetch news from NewsAPI
def fetch_news(query):
    url = f"https://newsapi.org/v2/everything?q={query}&pageSize=10&apiKey={NEWS_API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code != 200:
            return []  # Return empty list if NewsAPI fails

        articles = []
        for article in data.get("articles", []):
            title = article.get("title", "No title available")
            description = article.get("description", "No description available")
            url = article.get("url", "#")

            sentiment = analyze_sentiment(f"{title} {description}")
            articles.append({"title": title, "url": url, "sentiment": sentiment})
        
        return articles
    
    except Exception as e:
        print("Error fetching news:", e)
        return []

# Function to analyze sentiment using TextBlob
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# API Route to Serve HTML Page
@app.route("/")
def index():
    return render_template("index.html")

# API Endpoint for Fetching News
@app.route("/search", methods=["GET"])
def search():
    keyword = request.args.get("keyword")
    if not keyword:
        return jsonify([])  # Return empty JSON array if no keyword is provided

    articles = fetch_news(keyword)
    return jsonify(articles)  # Return articles as JSON

if __name__ == "__main__":
    app.run(debug=True)
