CREATE DATABASE zomato_db;

USE zomato_db;

DROP TABLE IF EXISTS zomato_restaurants;

CREATE TABLE zomato_restaurants (
    name VARCHAR(255),
    rate_clean DECIMAL(3,1),
    sentiment_score DECIMAL(6,4),
    sentiment VARCHAR(20),
    votes INT,
    approx_cost_for_two INT,
    online_order TINYINT,
    book_table TINYINT,
    rest_type VARCHAR(150),
    listed_in_type VARCHAR(100),
    listed_in_city VARCHAR(100),
    cuisines TEXT,
    cost_category VARCHAR(20),
    clean_reviews LONGTEXT
);


-- Check total records
SELECT COUNT(*) AS total_restaurants
FROM zomato_restaurants;

-- See table structure
DESCRIBE zomato_restaurants;

-- Preview data
SELECT *
FROM zomato_restaurants
LIMIT 10;

-- Check NULL values
SELECT
    COUNT(*) AS total_rows,
    SUM(rate_clean IS NULL) AS missing_rate,
    SUM(sentiment_score IS NULL) AS missing_sentiment,
    SUM(clean_reviews IS NULL) AS missing_reviews
FROM zomato_restaurants;

-- Check NULL values
SELECT sentiment, COUNT(*) AS count
FROM zomato_restaurants
GROUP BY sentiment;

-- Overall sentiment distribution
SELECT
    sentiment,
    COUNT(*) AS review_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM zomato_restaurants
GROUP BY sentiment;

-- Average rating vs average sentiment
SELECT
    ROUND(AVG(rate_clean), 2) AS avg_rating,
    ROUND(AVG(sentiment_score), 3) AS avg_sentiment
FROM zomato_restaurants;

-- Restaurants with most NEGATIVE sentiment
SELECT
    name,
    ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
    COUNT(*) AS total_reviews
FROM zomato_restaurants
GROUP BY name
HAVING avg_sentiment < 0
ORDER BY avg_sentiment ASC
LIMIT 10;

-- Top restaurants by POSITIVE sentiment
SELECT
    name,
    ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
    COUNT(*) AS total_reviews
FROM zomato_restaurants
GROUP BY name
HAVING total_reviews >= 50
ORDER BY avg_sentiment DESC
LIMIT 10;

-- Sentiment by cost category
SELECT
    cost_category,
    ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
    ROUND(AVG(rate_clean), 2) AS avg_rating,
    COUNT(*) AS reviews
FROM zomato_restaurants
GROUP BY cost_category
ORDER BY avg_sentiment DESC;

-- Online order vs dine-in sentiment
SELECT
    online_order,
    ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
    COUNT(*) AS reviews
FROM zomato_restaurants
GROUP BY online_order;

-- Book-table vs walk-in experience
SELECT
    book_table,
    ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
    COUNT(*) AS reviews
FROM zomato_restaurants
GROUP BY book_table;

-- Cuisine-wise sentiment
SELECT
    cuisines,
    ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
    COUNT(*) AS reviews
FROM zomato_restaurants
WHERE cuisines IS NOT NULL
GROUP BY cuisines
HAVING reviews >= 100
ORDER BY avg_sentiment DESC;

-- City-wise sentiment comparison
SELECT
    listed_in_city,
    ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
    COUNT(*) AS reviews
FROM zomato_restaurants
GROUP BY listed_in_city
ORDER BY avg_sentiment DESC;

-- Detect rating–sentiment mismatch
SELECT
    name,
    ROUND(AVG(rate_clean), 2) AS avg_rating,
    ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
    COUNT(*) AS reviews
FROM zomato_restaurants
GROUP BY name
HAVING avg_rating >= 4
   AND avg_sentiment < 0
ORDER BY avg_sentiment ASC;

CREATE TABLE zomato_restaurants_clean AS
SELECT
    name,
    listed_in_city,
    ROUND(AVG(rate_clean), 2) AS avg_rating,
    ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
    MAX(votes) AS votes,
    MAX(approx_cost_for_two) AS approx_cost_for_two,
    MAX(cost_category) AS cost_category,
    MAX(online_order) AS online_order,
    MAX(book_table) AS book_table,
    MAX(rest_type) AS rest_type,
    MAX(listed_in_type) AS listed_in_type,
    MAX(cuisines) AS cuisines
FROM zomato_restaurants
GROUP BY name, listed_in_city;

-- Rank restaurants by sentiment within each city
SELECT
    name,
    listed_in_city,
    avg_sentiment,
    avg_rating,
    RANK() OVER (
        PARTITION BY listed_in_city
        ORDER BY avg_sentiment DESC
    ) AS city_rank
FROM zomato_restaurants_clean;

-- Top 5 restaurants per city
WITH ranked_restaurants AS (
    SELECT
        name,
        listed_in_city,
        ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
        COUNT(*) AS reviews,
        ROW_NUMBER() OVER (
            PARTITION BY listed_in_city
            ORDER BY AVG(sentiment_score) DESC
        ) AS rn
    FROM zomato_restaurants
    GROUP BY name, listed_in_city
)
SELECT *
FROM ranked_restaurants
WHERE rn <= 5;

-- Compare sentiment vs rating gap
SELECT
    name,
    ROUND(AVG(rate_clean), 2) AS avg_rating,
    ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
    ROUND(AVG(rate_clean) - AVG(sentiment_score), 2) AS rating_sentiment_gap
FROM zomato_restaurants
GROUP BY name
HAVING avg_rating >= 4
ORDER BY rating_sentiment_gap DESC;

-- Sentiment distribution using conditional aggregation
SELECT
    name,
    COUNT(*) AS total_reviews,
    SUM(CASE WHEN sentiment = 'positive' THEN 1 ELSE 0 END) AS positive_reviews,
    SUM(CASE WHEN sentiment = 'negative' THEN 1 ELSE 0 END) AS negative_reviews,
    SUM(CASE WHEN sentiment = 'neutral' THEN 1 ELSE 0 END) AS neutral_reviews
FROM zomato_restaurants
GROUP BY name
HAVING total_reviews >= 50;

-- Running average sentiment
SELECT
    name,
    sentiment_score,
    AVG(sentiment_score) OVER (
        PARTITION BY name
        ORDER BY sentiment_score
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_avg_sentiment
FROM zomato_restaurants;

-- Cuisine performance vs global average
WITH global_avg AS (
    SELECT AVG(sentiment_score) AS overall_sentiment
    FROM zomato_restaurants
)
SELECT
    cuisines,
    ROUND(AVG(sentiment_score), 3) AS cuisine_sentiment,
    ROUND(AVG(sentiment_score) - (SELECT overall_sentiment FROM global_avg), 3) AS diff_from_avg
FROM zomato_restaurants
WHERE cuisines IS NOT NULL
GROUP BY cuisines
HAVING COUNT(*) >= 100
ORDER BY diff_from_avg DESC;

-- Cost vs sentiment quartile analysis
WITH cost_buckets AS (
    SELECT
        approx_cost_for_two,
        sentiment_score,
        rate_clean,
        NTILE(4) OVER (ORDER BY approx_cost_for_two) AS cost_quartile
    FROM zomato_restaurants
    WHERE approx_cost_for_two IS NOT NULL
)
SELECT
    cost_quartile,
    CASE cost_quartile
        WHEN 1 THEN 'Budget'
        WHEN 2 THEN 'Mid-Low'
        WHEN 3 THEN 'Mid-High'
        WHEN 4 THEN 'Premium'
    END AS cost_segment,
    ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
    ROUND(AVG(rate_clean), 2) AS avg_rating,
    COUNT(*) AS restaurant_count
FROM cost_buckets
GROUP BY cost_quartile
ORDER BY cost_quartile;

-- Identify unstable restaurants
SELECT
    name,
    ROUND(STDDEV(sentiment_score), 3) AS sentiment_variance,
    COUNT(*) AS reviews
FROM zomato_restaurants
GROUP BY name
HAVING reviews >= 50
ORDER BY sentiment_variance DESC;

-- Experience score
SELECT
    name,
    ROUND(
        (AVG(rate_clean) * 0.6 + AVG(sentiment_score) * 0.4),
        2
    ) AS experience_score
FROM zomato_restaurants
GROUP BY name
ORDER BY experience_score DESC;

-- Executive summary query
SELECT
    COUNT(DISTINCT name) AS total_restaurants,
    COUNT(*) AS total_reviews,
    ROUND(AVG(rate_clean), 2) AS avg_rating,
    ROUND(AVG(sentiment_score), 3) AS avg_sentiment
FROM zomato_restaurants;


-- Are high-rated restaurants always positively perceived?
SELECT
    CASE
        WHEN rate_clean >= 4 THEN 'High Rated'
        WHEN rate_clean >= 3 THEN 'Medium Rated'
        ELSE 'Low Rated'
    END AS rating_bucket,
    ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
    COUNT(*) AS restaurants
FROM zomato_restaurants
GROUP BY rating_bucket;

-- Does online ordering affect customer sentiment?
SELECT
    online_order,
    ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
    COUNT(*) AS restaurants
FROM zomato_restaurants
GROUP BY online_order;

-- Cost vs Sentiment Analysis
SELECT
    cost_category,
    ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
    COUNT(*) AS restaurants
FROM zomato_restaurants
GROUP BY cost_category
ORDER BY avg_sentiment DESC;

-- High rating but low sentiment (RED FLAG)
SELECT
    name,
    rate_clean,
    sentiment_score
FROM zomato_restaurants
WHERE rate_clean >= 4
  AND sentiment_score < 0
ORDER BY sentiment_score ASC;

-- Low rating but high sentiment (UNDERVALUED)
SELECT
    name,
    rate_clean,
    sentiment_score
FROM zomato_restaurants
WHERE rate_clean < 3.5
  AND sentiment_score > 0.2
ORDER BY sentiment_score DESC;

-- Best areas by sentiment
SELECT
    listed_in_city,
    ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
    COUNT(*) AS restaurants
FROM zomato_restaurants
GROUP BY listed_in_city
HAVING COUNT(*) >= 30
ORDER BY avg_sentiment DESC;

-- Create sentiment bucket
ALTER TABLE zomato_restaurants
ADD sentiment_label VARCHAR(20);

ALTER TABLE zomato_restaurants
ADD COLUMN restaurant_id INT AUTO_INCREMENT PRIMARY KEY;

UPDATE zomato_restaurants
SET sentiment_label =
    CASE
        WHEN sentiment_score >= 0.05 THEN 'positive'
        WHEN sentiment_score <= -0.05 THEN 'negative'
        ELSE 'neutral'
    END
WHERE restaurant_id > 0;



-- Verification
DESCRIBE zomato_restaurants;

SELECT
    sentiment_score,
    sentiment_label
FROM zomato_restaurants
LIMIT 10;

SELECT
    sentiment_label,
    COUNT(*) AS count
FROM zomato_restaurants
GROUP BY sentiment_label;

SELECT
    listed_in_city,
    sentiment_label,
    COUNT(*) AS count
FROM zomato_restaurants
GROUP BY listed_in_city, sentiment_label;








