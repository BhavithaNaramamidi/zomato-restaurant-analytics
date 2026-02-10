import streamlit as st
import plotly.express as px
import pandas as pd

from queries import (
    get_kpis,
    sentiment_distribution,
    cost_vs_sentiment,
    online_order_sentiment,
    top_positive_restaurants,
    risk_restaurants,
    undervalued_restaurants
)
from db import get_connection

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Zomato Sentiment Dashboard",
    page_icon="🍽️",
    layout="wide"
)

st.title("Zomato Restaurant Sentiment Dashboard")
st.caption(
    "End-to-End Analytics • SQL • Python • Sentiment Analysis • Streamlit"
)

st.divider()

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.header("🎛 Dashboard Controls")
enable_filters = st.sidebar.toggle("Enable Filters", value=False)

conn = get_connection()
filter_query = " WHERE 1=1 "

if enable_filters:
    st.sidebar.subheader("🔍 Apply Filters")

    cities = pd.read_sql(
        "SELECT DISTINCT listed_in_city FROM zomato_restaurants ORDER BY listed_in_city",
        conn
    )["listed_in_city"].dropna().tolist()

    cost_categories = pd.read_sql(
        "SELECT DISTINCT cost_category FROM zomato_restaurants ORDER BY cost_category",
        conn
    )["cost_category"].dropna().tolist()

    city_filter = st.sidebar.multiselect("📍 City", cities)
    cost_filter = st.sidebar.multiselect("💰 Cost Category", cost_categories)
    online_filter = st.sidebar.selectbox("🛵 Online Order", ["All", "Yes", "No"])

    if city_filter:
        filter_query += (
            f" AND listed_in_city = '{city_filter[0]}'"
            if len(city_filter) == 1
            else f" AND listed_in_city IN {tuple(city_filter)}"
        )

    if cost_filter:
        filter_query += (
            f" AND cost_category = '{cost_filter[0]}'"
            if len(cost_filter) == 1
            else f" AND cost_category IN {tuple(cost_filter)}"
        )

    if online_filter != "All":
        filter_query += f" AND online_order = {1 if online_filter == 'Yes' else 0}"

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------
kpi_df = pd.read_sql(
    f"""
    SELECT
        COUNT(DISTINCT name) AS total_restaurants,
        ROUND(AVG(rate_clean), 2) AS avg_rating,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        SUM(votes) AS total_votes
    FROM zomato_restaurants
    {filter_query};
    """,
    conn
)

k1, k2, k3, k4 = st.columns(4)

k1.metric("🍴 Restaurants", f"{int(kpi_df.total_restaurants[0]):,}")
k2.metric("⭐ Avg Rating", kpi_df.avg_rating[0] or 0)
k3.metric("😊 Avg Sentiment", kpi_df.avg_sentiment[0] or 0)
k4.metric("🗳️ Total Votes", f"{int(kpi_df.total_votes[0] or 0):,}")

st.divider()

# --------------------------------------------------
# SENTIMENT DISTRIBUTION
# --------------------------------------------------
st.subheader("😊 Customer Sentiment Distribution")

sent_df = pd.read_sql(
    f"""
    SELECT sentiment, COUNT(*) AS count
    FROM zomato_restaurants
    {filter_query}
    GROUP BY sentiment;
    """,
    conn
)

fig1 = px.pie(
    sent_df,
    names="sentiment",
    values="count",
    hole=0.45,
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(fig1, use_container_width=True)
st.caption("Shows how customers emotionally perceive restaurants overall.")

# --------------------------------------------------
# COST VS SENTIMENT
# --------------------------------------------------
st.subheader("💰 Cost Category vs Customer Sentiment")

cost_df = pd.read_sql(
    f"""
    SELECT
        cost_category,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        COUNT(*) AS restaurants
    FROM zomato_restaurants
    {filter_query}
    GROUP BY cost_category
    ORDER BY avg_sentiment DESC;
    """,
    conn
)

fig2 = px.bar(
    cost_df,
    x="cost_category",
    y="avg_sentiment",
    text="restaurants",
    color="avg_sentiment",
    color_continuous_scale="Teal"
)
st.plotly_chart(fig2, use_container_width=True)
st.caption("Higher pricing does not always guarantee better customer experience.")

# --------------------------------------------------
# ONLINE ORDER IMPACT
# --------------------------------------------------
st.subheader("🛵 Online Ordering Impact")

online_df = pd.read_sql(
    f"""
    SELECT
        online_order,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment
    FROM zomato_restaurants
    {filter_query}
    GROUP BY online_order;
    """,
    conn
)

online_df["online_order"] = online_df["online_order"].map({1: "Yes", 0: "No"})

fig3 = px.bar(
    online_df,
    x="online_order",
    y="avg_sentiment",
    text="avg_sentiment",
    color="avg_sentiment",
    color_continuous_scale="Blues"
)
st.plotly_chart(fig3, use_container_width=True)
st.caption("Evaluates whether online ordering improves customer satisfaction.")

st.divider()

# --------------------------------------------------
# INSIGHT TABLES
# --------------------------------------------------
st.subheader("🌟 Top Positive Restaurants")
st.dataframe(top_positive_restaurants(), use_container_width=True, height=300)

st.subheader("🚨 Restaurants Needing Attention")
st.dataframe(risk_restaurants(), use_container_width=True, height=300)

st.subheader("💎 Undervalued Restaurants")
st.dataframe(undervalued_restaurants(), use_container_width=True, height=300)

st.divider()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.caption(
    "📊 Built as a professional data analytics project using MySQL, Python, NLP & Streamlit"
)
