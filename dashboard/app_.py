import streamlit as st
import pandas as pd
import plotly.express as px

from db import get_connection
import query as q

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Zomato Sentiment Intelligence",
    layout="wide",
)

st.title("🍽️ Zomato Sentiment Intelligence Dashboard")
st.caption("SQL • Sentiment Analysis • Business Intelligence • Streamlit")

# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------
st.sidebar.title("📊 Dashboard Pages")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Executive Overview",
        "🚨 Risk & Opportunity",
        "⚙️ Operations & Behavior",
        "🌍 Market & Cuisine",
        "🧠 Trust & Experience",
    ]
)

# --------------------------------------------------
# GLOBAL FILTERS (City + Cost only)
# --------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Global Filters")

conn = get_connection()
filter_query = "WHERE 1=1"

cities = pd.read_sql(
    "SELECT DISTINCT listed_in_city FROM zomato_restaurants ORDER BY listed_in_city",
    conn
)["listed_in_city"].dropna().tolist()

costs = pd.read_sql(
    "SELECT DISTINCT cost_category FROM zomato_restaurants",
    conn
)["cost_category"].dropna().tolist()

city_filter = st.sidebar.multiselect("City", cities)
cost_filter = st.sidebar.multiselect("Cost Category", costs)

if city_filter:
    filter_query += f" AND listed_in_city IN ({','.join([repr(c) for c in city_filter])})"

if cost_filter:
    filter_query += f" AND cost_category IN ({','.join([repr(c) for c in cost_filter])})"

# ==================================================
# 🏠 PAGE 1 — EXECUTIVE OVERVIEW
# ==================================================
if page == "🏠 Executive Overview":

    st.subheader("🏠 Executive Overview (C-Level View)")

    # Page-level ranking
    top_n = st.selectbox("Show Top Restaurants", [5, 10, 20], index=1)

    kpi = q.homepage_kpis(filter_query)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Restaurants", f"{kpi.total_restaurants[0]:,}")
    c2.metric("Avg Rating", kpi.avg_rating[0])
    c3.metric("Avg Sentiment", kpi.avg_sentiment[0])
    c4.metric("Trust Gap", kpi.trust_gap[0])
    c5.metric("Total Votes", f"{int(kpi.total_votes[0]):,}")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        df = q.sentiment_pulse(filter_query)
        fig = px.pie(df, names="sentiment", values="count", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        df = q.homepage_cost_vs_sentiment(filter_query)
        fig = px.bar(df, x="cost_category", y="avg_sentiment", text="restaurants")
        st.plotly_chart(fig, use_container_width=True)

    df = q.homepage_city_performance(filter_query)
    fig = px.bar(df, x="listed_in_city", y="avg_sentiment", text="restaurants")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### ⭐ Recommended Restaurants (High Rating + High Sentiment)")
    df = q.top_trusted_restaurants(filter_query)
    st.dataframe(df.head(top_n), use_container_width=True)

# ==================================================
# 🚨 PAGE 2 — RISK & OPPORTUNITY
# ==================================================
elif page == "🚨 Risk & Opportunity":

    st.subheader("🚨 Risk & Opportunity Analysis")

    risk_n = st.selectbox("Show Top / Bottom", [5, 10, 20], index=1)

    st.markdown("### ⚠️ Risky Restaurants (High Rating, Low Sentiment)")
    df = q.risky_restaurants(filter_query)
    st.dataframe(df.head(risk_n), use_container_width=True)

    st.markdown("### 💎 Hidden Gems (Low Rating, High Sentiment)")
    df = q.hidden_gems(filter_query)
    st.dataframe(df.head(risk_n), use_container_width=True)

    st.markdown("### 🌪️ Unstable Experience (High Variance)")
    df = q.unstable_restaurants(filter_query)
    st.dataframe(df.head(risk_n), use_container_width=True)

    st.markdown("### ⭐ Best Experience Score")
    df = q.best_experience_restaurants(filter_query)
    st.dataframe(df.head(risk_n), use_container_width=True)

# ==================================================
# ⚙️ PAGE 3 — OPERATIONS & BEHAVIOR
# ==================================================
elif page == "⚙️ Operations & Behavior":

    st.subheader("⚙️ Operations & Customer Behavior")

    col1, col2 = st.columns(2)

    with col1:
        df = q.online_vs_dinein(filter_query)
        fig = px.bar(df, x="order_type", y="avg_sentiment", text="restaurants")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        df = q.book_table_impact(filter_query)
        fig = px.bar(df, x="booking_type", y="avg_sentiment", text="restaurants")
        st.plotly_chart(fig, use_container_width=True)

    df = q.review_volume_impact(filter_query)
    fig = px.bar(df, x="review_bucket", y="avg_sentiment", text="restaurants")
    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# 🌍 PAGE 4 — MARKET & CUISINE
# ==================================================
elif page == "🌍 Market & Cuisine":

    st.subheader("🌍 Market & Cuisine Intelligence")

    st.markdown("### 🏙️ City Performance")
    st.dataframe(q.city_performance(filter_query), use_container_width=True)

    st.markdown("### 🍜 Cuisine Performance")
    st.dataframe(q.cuisine_performance(filter_query), use_container_width=True)

    st.markdown("### 🚀 Expansion Opportunities")
    st.dataframe(q.expansion_opportunities(filter_query), use_container_width=True)

# ==================================================
# 🧠 PAGE 5 — TRUST & EXPERIENCE
# ==================================================
elif page == "🧠 Trust & Experience":

    st.subheader("🧠 Trust & Experience Intelligence")

    trust_n = st.selectbox("Show Top Issues", [5, 10, 20], index=1)

    st.markdown("### 🚨 Trust Risk Restaurants")
    df = q.trust_risk_restaurants(filter_query)
    st.dataframe(df.head(trust_n), use_container_width=True)

    st.markdown("### 📉 Trust Gap Analysis")
    df = q.trust_gap_analysis(filter_query)
    st.dataframe(df.head(trust_n), use_container_width=True)

    st.markdown("### 🚩 Experience Risk Flags")
    st.dataframe(q.experience_risk_flags(filter_query), use_container_width=True)

# --------------------------------------------------
st.markdown("---")
st.caption("Built with ❤️ | MySQL • Pandas • Streamlit • Plotly")
