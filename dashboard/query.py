
import pandas as pd
from db import get_connection

# ==================================================
# HOMEPAGE / MAIN DASHBOARD QUERIES
# ==================================================

# --------------------------------------------------
# 1. EXECUTIVE KPIs (TOP STRIP)
# --------------------------------------------------
def homepage_kpis(filter_query=""):
    conn = get_connection()
    query = f"""
    SELECT
        COUNT(DISTINCT name) AS total_restaurants,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        ROUND(AVG(rate_clean) - AVG(sentiment_score), 2) AS trust_gap,
        SUM(votes) AS total_votes
    FROM zomato_restaurants
    {filter_query};
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# 2. TOP TRUSTED RESTAURANTS (RECOMMENDED)
# High rating + high sentiment
# --------------------------------------------------
def top_trusted_restaurants(filter_query=""):
    conn = get_connection()
    query = f"""
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
    ORDER BY avg_sentiment DESC, avg_rating DESC
    LIMIT 10;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# 3. RISKY RESTAURANTS
# High rating but negative sentiment
# --------------------------------------------------
def risky_restaurants(filter_query=""):
    conn = get_connection()
    query = f"""
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
    ORDER BY avg_sentiment ASC
    LIMIT 10;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# 4. HIDDEN GEMS (UNDERRATED)
# Low rating but very positive sentiment
# --------------------------------------------------
def hidden_gems(filter_query=""):
    conn = get_connection()
    query = f"""
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
    ORDER BY avg_sentiment DESC
    LIMIT 10;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# 5. BEST EXPERIENCE SCORE
# Business metric (60% rating + 40% sentiment)
# --------------------------------------------------
def best_experience_restaurants(filter_query=""):
    conn = get_connection()
    query = f"""
    SELECT
        name,
        ROUND(
            (AVG(rate_clean) * 0.6 + AVG(sentiment_score) * 0.4),
            2
        ) AS experience_score,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        COUNT(*) AS reviews
    FROM zomato_restaurants
    {filter_query}
    GROUP BY name
    HAVING reviews >= 30
    ORDER BY experience_score DESC
    LIMIT 10;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# 6. OVERALL SENTIMENT DISTRIBUTION
# --------------------------------------------------
def sentiment_pulse(filter_query=""):
    conn = get_connection()
    query = f"""
    SELECT
        sentiment,
        COUNT(*) AS count
    FROM zomato_restaurants
    {filter_query}
    GROUP BY sentiment;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# 7. COST CATEGORY vs CUSTOMER HAPPINESS
# --------------------------------------------------
def homepage_cost_vs_sentiment(filter_query=""):
    conn = get_connection()
    query = f"""
    SELECT
        cost_category,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        COUNT(*) AS restaurants
    FROM zomato_restaurants
    {filter_query}
    GROUP BY cost_category
    ORDER BY avg_sentiment DESC;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# 8. CITY PERFORMANCE (QUICK VIEW)
# --------------------------------------------------
def homepage_city_performance(filter_query=""):
    conn = get_connection()
    query = f"""
    SELECT
        listed_in_city,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        COUNT(DISTINCT name) AS restaurants
    FROM zomato_restaurants
    {filter_query}
    GROUP BY listed_in_city
    HAVING restaurants >= 20
    ORDER BY avg_sentiment DESC;
    """
    return pd.read_sql(query, conn)

# --------------------------------------------------
# SENTIMENT DISTRIBUTION (Pie)
# --------------------------------------------------
def sentiment_distribution(filter_query=""):
    conn = get_connection()
    query = f"""
    SELECT
        sentiment,
        COUNT(*) AS restaurant_count
    FROM zomato_restaurants
    {filter_query}
    GROUP BY sentiment;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# COST CATEGORY vs SENTIMENT (Bar)
# --------------------------------------------------
def cost_vs_sentiment(filter_query=""):
    conn = get_connection()
    query = f"""
    SELECT
        cost_category,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        COUNT(*) AS restaurants
    FROM zomato_restaurants
    {filter_query}
    GROUP BY cost_category
    ORDER BY avg_sentiment DESC;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# CITY-WISE AVERAGE SENTIMENT (Bar)
# --------------------------------------------------
def city_wise_sentiment(filter_query=""):
    conn = get_connection()
    query = f"""
    SELECT
        listed_in_city,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        COUNT(*) AS restaurants
    FROM zomato_restaurants
    {filter_query}
    GROUP BY listed_in_city
    HAVING COUNT(*) >= 20
    ORDER BY avg_sentiment DESC;
    """
    return pd.read_sql(query, conn)

# ==================================================
# PAGE 2: RISK & OPPORTUNITY ANALYSIS
# ==================================================

import pandas as pd
from db import get_connection


# --------------------------------------------------
# HIGH RATING BUT LOW SENTIMENT (RISK RESTAURANTS)
# --------------------------------------------------
def risk_restaurants(filter_query=""):
    """
    Restaurants that look good by rating
    but customers are unhappy (danger zone)
    """
    conn = get_connection()
    query = f"""
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
       AND reviews >= 20
    ORDER BY avg_sentiment ASC
    LIMIT 15;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# LOW RATING BUT HIGH SENTIMENT (UNDERVALUED)
# --------------------------------------------------
def undervalued_restaurants(filter_query=""):
    """
    Restaurants customers LOVE
    but ratings are low (hidden gems)
    """
    conn = get_connection()
    query = f"""
    SELECT
        name,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        COUNT(*) AS reviews
    FROM zomato_restaurants
    {filter_query}
    GROUP BY name
    HAVING avg_rating < 3.8
       AND avg_sentiment > 0.25
       AND reviews >= 20
    ORDER BY avg_sentiment DESC
    LIMIT 15;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# MOST UNSTABLE RESTAURANTS (INCONSISTENT EXPERIENCE)
# --------------------------------------------------
def unstable_restaurants(filter_query=""):
    """
    Restaurants with highly inconsistent sentiment
    (customers have mixed experiences)
    """
    conn = get_connection()
    query = f"""
    SELECT
        name,
        ROUND(STDDEV(sentiment_score), 3) AS sentiment_variance,
        COUNT(*) AS reviews
    FROM zomato_restaurants
    {filter_query}
    GROUP BY name
    HAVING reviews >= 30
    ORDER BY sentiment_variance DESC
    LIMIT 15;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# EXPERIENCE SCORE (BUSINESS METRIC)
# --------------------------------------------------
def experience_score(filter_query=""):
    """
    Combined metric:
    60% Rating + 40% Sentiment
    """
    conn = get_connection()
    query = f"""
    SELECT
        name,
        ROUND(
            (AVG(rate_clean) * 0.6 + AVG(sentiment_score) * 0.4),
            2
        ) AS experience_score,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        COUNT(*) AS reviews
    FROM zomato_restaurants
    {filter_query}
    GROUP BY name
    HAVING reviews >= 20
    ORDER BY experience_score DESC
    LIMIT 15;
    """
    return pd.read_sql(query, conn)

# ==================================================
# PAGE 3: OPERATIONS & CUSTOMER BEHAVIOR
# ==================================================

import pandas as pd
from db import get_connection


# --------------------------------------------------
# ONLINE ORDER VS DINE-IN PERFORMANCE
# --------------------------------------------------
def online_vs_dinein(filter_query=""):
    """
    Compare customer sentiment and ratings
    for online ordering vs dine-in restaurants
    """
    conn = get_connection()
    query = f"""
    SELECT
        CASE
            WHEN online_order = 1 THEN 'Online Order'
            ELSE 'Dine-In Only'
        END AS order_type,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        COUNT(*) AS restaurants
    FROM zomato_restaurants
    {filter_query}
    GROUP BY order_type;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# BOOK TABLE IMPACT
# --------------------------------------------------
def book_table_impact(filter_query=""):
    """
    Does table booking improve customer experience?
    """
    conn = get_connection()
    query = f"""
    SELECT
        CASE
            WHEN book_table = 1 THEN 'Table Booking Available'
            ELSE 'No Table Booking'
        END AS booking_type,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        COUNT(*) AS restaurants
    FROM zomato_restaurants
    {filter_query}
    GROUP BY booking_type;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# COST EFFICIENCY ANALYSIS
# --------------------------------------------------
def cost_efficiency(filter_query=""):
    """
    Which cost category gives the best experience
    per price segment
    """
    conn = get_connection()
    query = f"""
    SELECT
        cost_category,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        COUNT(*) AS restaurants
    FROM zomato_restaurants
    {filter_query}
    GROUP BY cost_category
    ORDER BY avg_sentiment DESC;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# REVIEW VOLUME VS SENTIMENT
# --------------------------------------------------
def review_volume_impact(filter_query=""):
    """
    Check if highly reviewed restaurants
    have better or worse sentiment
    """
    conn = get_connection()
    query = f"""
    SELECT
        CASE
            WHEN votes < 100 THEN 'Low Reviews'
            WHEN votes BETWEEN 100 AND 500 THEN 'Medium Reviews'
            ELSE 'High Reviews'
        END AS review_bucket,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        COUNT(*) AS restaurants
    FROM zomato_restaurants
    {filter_query}
    GROUP BY review_bucket
    ORDER BY avg_sentiment DESC;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# PRICE VS CUSTOMER HAPPINESS TRADEOFF
# --------------------------------------------------
def price_vs_happiness(filter_query=""):
    """
    Identify if higher cost guarantees
    better customer happiness
    """
    conn = get_connection()
    query = f"""
    SELECT
        approx_cost_for_two,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        COUNT(*) AS restaurants
    FROM zomato_restaurants
    {filter_query}
    GROUP BY approx_cost_for_two
    HAVING COUNT(*) >= 10
    ORDER BY approx_cost_for_two;
    """
    return pd.read_sql(query, conn)

# ==================================================
# PAGE 4: MARKET & CUISINE INTELLIGENCE
# ==================================================

import pandas as pd
from db import get_connection


# --------------------------------------------------
# CITY PERFORMANCE OVERVIEW
# --------------------------------------------------
def city_performance(filter_query=""):
    """
    Identify top and bottom performing cities
    based on customer sentiment and ratings
    """
    conn = get_connection()
    query = f"""
    SELECT
        listed_in_city,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        COUNT(DISTINCT name) AS restaurants
    FROM zomato_restaurants
    {filter_query}
    GROUP BY listed_in_city
    HAVING restaurants >= 20
    ORDER BY avg_sentiment DESC;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# CUISINE PERFORMANCE ANALYSIS
# --------------------------------------------------
def cuisine_performance(filter_query=""):
    conn = get_connection()
    query = f"""
    SELECT
        cuisines,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        COUNT(*) AS restaurants
    FROM zomato_restaurants
    {filter_query}
    AND cuisines IS NOT NULL
    GROUP BY cuisines
    HAVING restaurants >= 50
    ORDER BY avg_sentiment DESC;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# CUISINE DEMAND VS SATISFACTION
# --------------------------------------------------
def cuisine_demand_vs_quality(filter_query=""):
    """
    High demand cuisines vs customer satisfaction
    """
    conn = get_connection()
    query = f"""
    SELECT
        cuisines,
        COUNT(*) AS demand,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment
    FROM zomato_restaurants
    {filter_query}
    WHERE cuisines IS NOT NULL
    GROUP BY cuisines
    HAVING demand >= 100
    ORDER BY demand DESC;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# CITY + CUISINE OPPORTUNITY MATRIX
# --------------------------------------------------
def city_cuisine_opportunity(filter_query=""):
    """
    Identify city-cuisine combinations
    with high sentiment but low competition
    """
    conn = get_connection()
    query = f"""
    SELECT
        listed_in_city,
        cuisines,
        COUNT(*) AS restaurants,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment
    FROM zomato_restaurants
    {filter_query}
    WHERE cuisines IS NOT NULL
    GROUP BY listed_in_city, cuisines
    HAVING restaurants BETWEEN 10 AND 40
       AND avg_sentiment >= 0.2
    ORDER BY avg_sentiment DESC;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# OVERCROWDED MARKET DETECTION
# --------------------------------------------------
def overcrowded_cuisines(filter_query=""):
    """
    Cuisines with high competition but
    low customer satisfaction
    """
    conn = get_connection()
    query = f"""
    SELECT
        cuisines,
        COUNT(*) AS restaurants,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment
    FROM zomato_restaurants
    {filter_query}
    WHERE cuisines IS NOT NULL
    GROUP BY cuisines
    HAVING restaurants >= 200
       AND avg_sentiment < 0
    ORDER BY restaurants DESC;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# MARKET EXPANSION SUGGESTIONS
# --------------------------------------------------
def expansion_opportunities(filter_query=""):
    """
    Cities with high sentiment but
    relatively fewer restaurants
    """
    conn = get_connection()
    query = f"""
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
    return pd.read_sql(query, conn)

# ==================================================
# PAGE 5: RISK, TRUST & EXPERIENCE INTELLIGENCE
# ==================================================

import pandas as pd
from db import get_connection


# --------------------------------------------------
# HIGH RATING BUT LOW SENTIMENT (TRUST RISK)
# --------------------------------------------------
def trust_risk_restaurants(filter_query=""):
    """
    Restaurants that look good on ratings
    but customers feel unhappy
    """
    conn = get_connection()
    query = f"""
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
    return pd.read_sql(query, conn)


# --------------------------------------------------
# LOW RATING BUT HIGH SENTIMENT (UNDERVALUED)
# --------------------------------------------------
def underrated_gems(filter_query=""):
    """
    Restaurants customers love
    but ratings don't reflect it
    """
    conn = get_connection()
    query = f"""
    SELECT
        name,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        COUNT(*) AS reviews
    FROM zomato_restaurants
    {filter_query}
    GROUP BY name
    HAVING avg_rating < 3.5
       AND avg_sentiment >= 0.2
       AND reviews >= 30
    ORDER BY avg_sentiment DESC;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# SENTIMENT VOLATILITY (EXPERIENCE INSTABILITY)
# --------------------------------------------------
def unstable_restaurants(filter_query=""):
    """
    Restaurants with inconsistent experience
    """
    conn = get_connection()
    query = f"""
    SELECT
        name,
        ROUND(STDDEV(sentiment_score), 3) AS sentiment_volatility,
        COUNT(*) AS reviews
    FROM zomato_restaurants
    {filter_query}
    GROUP BY name
    HAVING reviews >= 50
    ORDER BY sentiment_volatility DESC;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# EXPERIENCE SCORE (COMBINED METRIC)
# --------------------------------------------------
def experience_score(filter_query=""):
    """
    Weighted score combining rating + sentiment
    """
    conn = get_connection()
    query = f"""
    SELECT
        name,
        ROUND(
            (AVG(rate_clean) * 0.6 + AVG(sentiment_score) * 0.4),
            2
        ) AS experience_score,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        COUNT(*) AS reviews
    FROM zomato_restaurants
    {filter_query}
    GROUP BY name
    HAVING reviews >= 30
    ORDER BY experience_score DESC;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# CUSTOMER TRUST GAP ANALYSIS
# --------------------------------------------------
def trust_gap_analysis(filter_query=""):
    """
    Difference between rating perception
    and real customer sentiment
    """
    conn = get_connection()
    query = f"""
    SELECT
        name,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        ROUND(
            AVG(rate_clean) - AVG(sentiment_score),
            2
        ) AS trust_gap,
        COUNT(*) AS reviews
    FROM zomato_restaurants
    {filter_query}
    GROUP BY name
    HAVING reviews >= 30
    ORDER BY trust_gap DESC;
    """
    return pd.read_sql(query, conn)


# --------------------------------------------------
# CUSTOMER EXPERIENCE RISK FLAGS
# --------------------------------------------------
def experience_risk_flags(filter_query=""):
    """
    Flag restaurants needing urgent action
    """
    conn = get_connection()
    query = f"""
    SELECT
        name,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        COUNT(*) AS reviews,
        CASE
            WHEN AVG(rate_clean) >= 4 AND AVG(sentiment_score) < 0
                THEN 'HIGH RISK'
            WHEN AVG(rate_clean) < 3 AND AVG(sentiment_score) >= 0.2
                THEN 'OPPORTUNITY'
            WHEN STDDEV(sentiment_score) >= 0.5
                THEN 'UNSTABLE'
            ELSE 'NORMAL'
        END AS risk_flag
    FROM zomato_restaurants
    {filter_query}
    GROUP BY name
    HAVING reviews >= 30
    ORDER BY reviews DESC;
    """
    return pd.read_sql(query, conn)
