import pandas as pd
from db import get_connection

# ==================================================
# HELPERS
# ==================================================
def run_query(sql):
    conn = get_connection()
    return pd.read_sql(sql, conn)

# ==================================================
# 🏠 HOMEPAGE / EXECUTIVE OVERVIEW
# ==================================================

def homepage_kpis(filter_query="WHERE 1=1"):
    sql = f"""
    SELECT
        COUNT(DISTINCT name) AS total_restaurants,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        ROUND(AVG(rate_clean) - AVG(sentiment_score), 2) AS trust_gap,
        SUM(votes) AS total_votes
    FROM zomato_restaurants
    {filter_query};
    """
    return run_query(sql)


def sentiment_pulse(filter_query="WHERE 1=1"):
    sql = f"""
    SELECT sentiment, COUNT(*) AS count
    FROM zomato_restaurants
    {filter_query}
    GROUP BY sentiment;
    """
    return run_query(sql)


def homepage_cost_vs_sentiment(filter_query="WHERE 1=1"):
    sql = f"""
    SELECT
        cost_category,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        COUNT(*) AS restaurants
    FROM zomato_restaurants
    {filter_query}
    GROUP BY cost_category
    ORDER BY avg_sentiment DESC;
    """
    return run_query(sql)


def homepage_city_performance(filter_query="WHERE 1=1"):
    sql = f"""
    SELECT
        listed_in_city,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        COUNT(DISTINCT name) AS restaurants
    FROM zomato_restaurants
    {filter_query}
    GROUP BY listed_in_city
    ORDER BY avg_sentiment DESC;
    """
    return run_query(sql)


def top_trusted_restaurants(filter_query="WHERE 1=1"):
    sql = f"""
    SELECT
        name,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        COUNT(*) AS reviews
    FROM zomato_restaurants
    {filter_query}
    GROUP BY name
    HAVING avg_rating >= 4
       AND avg_sentiment >= 0.25
       AND reviews >= 30
    ORDER BY avg_sentiment DESC
    LIMIT 10;
    """
    return run_query(sql)

# ==================================================
# 🚨 PAGE 2 — RISK & OPPORTUNITY
# ==================================================

def risky_restaurants(filter_query="WHERE 1=1"):
    sql = f"""
    SELECT
        name,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        COUNT(*) AS reviews
    FROM zomato_restaurants
    {filter_query}
    GROUP BY name
    HAVING avg_rating >= 4
       AND avg_sentiment < 0
       AND reviews >= 30
    ORDER BY avg_sentiment ASC;
    """
    return run_query(sql)


def hidden_gems(filter_query="WHERE 1=1"):
    sql = f"""
    SELECT
        name,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        COUNT(*) AS reviews
    FROM zomato_restaurants
    {filter_query}
    GROUP BY name
    HAVING avg_rating < 3.8
       AND avg_sentiment >= 0.3
       AND reviews >= 30
    ORDER BY avg_sentiment DESC;
    """
    return run_query(sql)


def unstable_restaurants(filter_query="WHERE 1=1"):
    sql = f"""
    SELECT
        name,
        ROUND(STDDEV(sentiment_score), 3) AS sentiment_variance,
        COUNT(*) AS reviews
    FROM zomato_restaurants
    {filter_query}
    GROUP BY name
    HAVING reviews >= 30
    ORDER BY sentiment_variance DESC;
    """
    return run_query(sql)


def best_experience_restaurants(filter_query="WHERE 1=1"):
    sql = f"""
    SELECT
        name,
        ROUND((AVG(rate_clean)*0.6 + AVG(sentiment_score)*0.4), 2) AS experience_score,
        COUNT(*) AS reviews
    FROM zomato_restaurants
    {filter_query}
    GROUP BY name
    HAVING reviews >= 30
    ORDER BY experience_score DESC;
    """
    return run_query(sql)

# ==================================================
# ⚙️ PAGE 3 — OPERATIONS & BEHAVIOR
# ==================================================

def online_vs_dinein(filter_query="WHERE 1=1"):
    sql = f"""
    SELECT
        CASE WHEN online_order = 1 THEN 'Online Order' ELSE 'Dine-In Only' END AS order_type,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        COUNT(*) AS restaurants
    FROM zomato_restaurants
    {filter_query}
    GROUP BY order_type;
    """
    return run_query(sql)


def book_table_impact(filter_query="WHERE 1=1"):
    sql = f"""
    SELECT
        CASE WHEN book_table = 1 THEN 'Booking Available' ELSE 'No Booking' END AS booking_type,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        COUNT(*) AS restaurants
    FROM zomato_restaurants
    {filter_query}
    GROUP BY booking_type;
    """
    return run_query(sql)


def review_volume_impact(filter_query="WHERE 1=1"):
    sql = f"""
    SELECT
        CASE
            WHEN votes < 100 THEN 'Low'
            WHEN votes BETWEEN 100 AND 500 THEN 'Medium'
            ELSE 'High'
        END AS review_bucket,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        COUNT(*) AS restaurants
    FROM zomato_restaurants
    {filter_query}
    GROUP BY review_bucket;
    """
    return run_query(sql)

# ==================================================
# 🌍 PAGE 4 — MARKET & CUISINE
# ==================================================

def city_performance(filter_query="WHERE 1=1"):
    sql = f"""
    SELECT
        listed_in_city,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        COUNT(DISTINCT name) AS restaurants
    FROM zomato_restaurants
    {filter_query}
    GROUP BY listed_in_city
    ORDER BY avg_sentiment DESC;
    """
    return run_query(sql)


def cuisine_performance(filter_query="WHERE 1=1"):
    sql = f"""
    SELECT
        cuisines,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        COUNT(*) AS restaurants
    FROM zomato_restaurants
    {filter_query}
    AND cuisines IS NOT NULL
    GROUP BY cuisines
    HAVING restaurants >= 50
    ORDER BY avg_sentiment DESC;
    """
    return run_query(sql)


def expansion_opportunities(filter_query="WHERE 1=1"):
    sql = f"""
    SELECT
        listed_in_city,
        COUNT(DISTINCT name) AS restaurants,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment
    FROM zomato_restaurants
    {filter_query}
    GROUP BY listed_in_city
    HAVING restaurants BETWEEN 20 AND 80
       AND avg_sentiment >= 0.25
    ORDER BY avg_sentiment DESC;
    """
    return run_query(sql)

# ==================================================
# 🧠 PAGE 5 — TRUST & EXPERIENCE
# ==================================================

def trust_risk_restaurants(filter_query="WHERE 1=1"):
    sql = f"""
    SELECT
        name,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        COUNT(*) AS reviews
    FROM zomato_restaurants
    {filter_query}
    GROUP BY name
    HAVING avg_rating >= 4
       AND avg_sentiment < 0
       AND reviews >= 30;
    """
    return run_query(sql)


def trust_gap_analysis(filter_query="WHERE 1=1"):
    sql = f"""
    SELECT
        name,
        ROUND(AVG(rate_clean) - AVG(sentiment_score), 2) AS trust_gap,
        COUNT(*) AS reviews
    FROM zomato_restaurants
    {filter_query}
    GROUP BY name
    HAVING reviews >= 30
    ORDER BY trust_gap DESC;
    """
    return run_query(sql)


def experience_risk_flags(filter_query="WHERE 1=1"):
    sql = f"""
    SELECT
        name,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        COUNT(*) AS reviews,
        CASE
            WHEN AVG(rate_clean) >= 4 AND AVG(sentiment_score) < 0 THEN 'HIGH RISK'
            WHEN AVG(rate_clean) < 3 AND AVG(sentiment_score) >= 0.25 THEN 'OPPORTUNITY'
            WHEN STDDEV(sentiment_score) >= 0.5 THEN 'UNSTABLE'
            ELSE 'NORMAL'
        END AS risk_flag
    FROM zomato_restaurants
    {filter_query}
    GROUP BY name
    HAVING reviews >= 30;
    """
    return run_query(sql)
