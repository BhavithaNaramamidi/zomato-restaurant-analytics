## Zomato Sentiment Intelligence Dashboard

An end-to-end data analytics & sentiment intelligence project that transforms raw restaurant reviews into actionable business insights using SQL, Python, NLP, and Streamlit.

This project goes beyond basic dashboards by combining ratings + customer sentiment to uncover trust gaps, hidden gems, risk restaurants, and expansion opportunities — similar to how real-world product and business intelligence teams operate.

## Project Overview

Goal:
To analyze Zomato restaurant data and customer reviews to answer critical business questions such as:

Are highly rated restaurants actually loved by customers?

Which restaurants are risky despite high ratings?

Which cities and cuisines perform best in customer sentiment?

Does cost, online ordering, or table booking impact customer happiness?

Where are the best expansion opportunities?

## Key Concepts Used

Sentiment Analysis (NLP)

Business Metrics & KPIs

Advanced SQL Analytics

Feature Engineering

Risk & Opportunity Detection

Interactive BI Dashboards (Power BI–like UX)

## 🛠️ Tech Stack
Layer	Tools
Database	MySQL
Language	Python
Data Analysis	Pandas, NumPy
NLP	VADER Sentiment Analyzer
Visualization	Plotly
Dashboard	Streamlit
Version Control	Git & GitHub

## 📊 Dashboard Pages & Insights
🏠 1. Executive Overview (C-Level View)

Answers:

Overall customer sentiment health

Are customers actually happy?

Does price affect satisfaction?

Which cities perform best?

KPIs:

Total Restaurants

Average Rating

Average Sentiment

Trust Gap (Rating vs Sentiment)

Total Votes

🚨 2. Risk & Opportunity Analysis

Identifies:

⚠️ Risky Restaurants: High rating but negative sentiment

💎 Hidden Gems: Low rating but very positive sentiment

🌪️ Unstable Restaurants: Inconsistent customer experience

⭐ Best Experience Score (custom business metric)

⚙️ 3. Operations & Customer Behavior

Analyzes:

Online Order vs Dine-In performance

Table booking impact on sentiment

Review volume vs customer happiness

Cost efficiency across segments

🌍 4. Market & Cuisine Intelligence

Insights:

Best & worst performing cities

High-performing cuisines

Underserved markets

Expansion opportunities based on sentiment

🧠 5. Trust & Experience Intelligence

Advanced Signals:

Trust risk restaurants

Rating–sentiment gap

Experience risk flags

Business-ready risk classification

🧪 Advanced Data Cleaning & Feature Engineering

Missing value handling

Duplicate detection

Data type corrections

Outlier detection (IQR method)

Sentiment bucketing (Positive / Neutral / Negative)

Cost category engineering

Experience score (60% rating + 40% sentiment)

Review volume buckets

## 📁 Project Structure
```text
zomato-restaurant-analytics/
│
├── dashboard/
│   ├── app.py              # Streamlit dashboard
│   ├── query.py            # All SQL analytics queries
│   ├── db.py               # MySQL connection
│
├── notebooks/
│   ├── Zomato.ipynb
│
├── sql/
│   ├── schema.sql
│
├── docs/
│   ├── dataset_link.md     # Dataset download link
│
├── requirements.txt
└── README.md
```
## 📦 Dataset

Due to GitHub file size limitations, the dataset is not uploaded directly.

📎 Dataset download link is provided here:
👉 docs/dataset_link.md

## ▶️ How to Run the Project
1️⃣ Clone the Repository
git clone https://github.com/your-username/zomato-restaurant-analytics.git
cd zomato-restaurant-analytics

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Setup Database

Create MySQL database

Run SQL scripts from sql/schema.sql

Load dataset into MySQL

4️⃣ Run Dashboard
streamlit run dashboard/app.py

## 📈 Business Value Delivered
```
✔ Identifies restaurants with fake-high ratings
✔ Helps platforms improve trust & transparency
✔ Guides restaurant owners on experience gaps
✔ Enables market expansion decisions
✔ Simulates real-world BI & product analytics
```
