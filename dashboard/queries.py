import pandas as pd
from db import get_connection


# ---------- KPI ----------
def get_kpis():
    conn = get_connection()
    query = """
    SELECT
        COUNT(DISTINCT name) AS total_restaurants,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        SUM(votes) AS total_votes
    FROM zomato_restaurants;
    """
    return pd.read_sql(query, conn)


# ---------- Sentiment Distribution ----------
def sentiment_distribution():
    conn = get_connection()
    query = """
    SELECT
        sentiment,
        COUNT(*) AS count
    FROM zomato_restaurants
    GROUP BY sentiment;
    """
    return pd.read_sql(query, conn)


# ---------- Cost vs Sentiment ----------
def cost_vs_sentiment():
    conn = get_connection()
    query = """
    SELECT
        cost_category,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        COUNT(*) AS restaurants
    FROM zomato_restaurants
    GROUP BY cost_category
    ORDER BY avg_sentiment DESC;
    """
    return pd.read_sql(query, conn)


# ---------- Online Order Impact ----------
def online_order_sentiment():
    conn = get_connection()
    query = """
    SELECT
        online_order,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment
    FROM zomato_restaurants
    GROUP BY online_order;
    """
    return pd.read_sql(query, conn)


# ---------- Top Positive Restaurants ----------
def top_positive_restaurants(limit=10):
    conn = get_connection()
    query = f"""
    SELECT
        name,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        SUM(votes) AS votes
    FROM zomato_restaurants
    GROUP BY name
    HAVING COUNT(*) >= 30
    ORDER BY avg_sentiment DESC
    LIMIT {limit};
    """
    return pd.read_sql(query, conn)


# ---------- Risk Restaurants (Actionable) ----------
def risk_restaurants():
    conn = get_connection()
    query = """
    SELECT
        name,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        SUM(votes) AS votes
    FROM zomato_restaurants
    GROUP BY name
    HAVING avg_sentiment < -0.05
       AND votes >= 500
    ORDER BY avg_sentiment ASC;
    """
    return pd.read_sql(query, conn)


# ---------- Undervalued Restaurants ----------
def undervalued_restaurants():
    conn = get_connection()
    query = """
    SELECT
        name,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment
    FROM zomato_restaurants
    GROUP BY name
    HAVING avg_rating < 3.5
       AND avg_sentiment > 0.2
    ORDER BY avg_sentiment DESC;
    """
    return pd.read_sql(query, conn)
