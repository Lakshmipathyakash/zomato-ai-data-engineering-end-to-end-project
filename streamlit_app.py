import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import snowflake.connector

# Load Snowflake credentials
load_dotenv("airflow/.env")

# Page configuration
st.set_page_config(
    page_title="Zomato AI Analytics",
    page_icon="🍽️",
    layout="wide"
)

st.title("🍽️ Zomato AI Analytics Dashboard")
st.caption("Zomato Data Engineering & AI Analytics Platform")


@st.cache_resource
def get_connection():
    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse="ZOMATO_WH",
        database="ZOMATO",
        schema="MARTS",
        role="ACCOUNTADMIN"
    )


try:
    conn = get_connection()

    st.success("✅ Connected to Snowflake")

    query = """
        SELECT
            ORDER_DATE,
            CITY,
            ORDERS,
            DELIVERED_ORDERS,
            CANCEL_RATE,
            GMV,
            AOV
        FROM ZOMATO.MARTS.MART_DAILY_CITY_REVENUNE
        ORDER BY ORDER_DATE
    """

    df = pd.read_sql(query, conn)

    restaurant_query = """
        SELECT
            RESTAURANT_ID,
            RESTAURANT_NAME,
            CITY,
            CUISINE,
            ORDERS,
            REVENUE,
            AVG_CUSTOMER_RATING,
            AVG_DELIVERY_MIN
        FROM ZOMATO.MARTS.MART_RESTAURANT_PERFORMANCE
        """

    df_restaurant = pd.read_sql(restaurant_query, conn)

    # =====================================================
    # LOAD DELIVERY SLA DATA
    # =====================================================
    
    sla_query = """
    SELECT
        CITY,
        ORDER_HOUR,
        DELIVERED_ORDERS,
        P50,
        P90
    FROM ZOMATO.MARTS.MART_DELIVERY_SLA
    """
    
    df_sla = pd.read_sql(sla_query, conn)

    # =====================================================
    # LOAD AI REVIEW INSIGHTS
    # =====================================================

    review_query = """
    SELECT
        CITY,
        TOPIC,
        SENTIMENT_LABEL,
        REVIEWS,
        AVG_SENTIMENT_SCORE,
        AVG_STAR_RATING,
        FLAGGED_ISSUES
    FROM ZOMATO.MARTS.MART_REVIEW_INSIGHTS
    """

    df_reviews = pd.read_sql(review_query, conn)
    # -------------------------
    # KPI SECTION
    # -------------------------

    st.subheader("📊 Business Overview")

    total_orders = df["ORDERS"].sum()
    total_gmv = df["GMV"].sum()
    average_aov = df["AOV"].mean()
    cancel_rate = df["CANCEL_RATE"].mean() * 100

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🛒 Total Orders",
            f"{total_orders:,.0f}"
        )

    with col2:
        st.metric(
            "💰 Total GMV",
            f"₹{total_gmv:,.0f}"
        )

    with col3:
        st.metric(
            "💳 Average AOV",
            f"₹{average_aov:,.2f}"
        )

    with col4:
        st.metric(
            "❌ Cancellation Rate",
            f"{cancel_rate:.2f}%"
        )

    st.divider()
# =====================================================
# AI REVIEW INSIGHTS
# =====================================================

    st.subheader("🤖 AI Review Insights")
    
    st.caption(
        "AI-enriched customer review topics, sentiment and flagged issues"
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_reviews = df_reviews["REVIEWS"].sum()
        st.metric(
            "📝 Total Reviews",
            f"{total_reviews:,.0f}"
        )
    
    with col2:
        flagged_issues = df_reviews["FLAGGED_ISSUES"].sum()
        st.metric(
            "🚩 Flagged Issues",
            f"{flagged_issues:,.0f}"
        )
    
    with col3:
        avg_rating = df_reviews["AVG_STAR_RATING"].mean()
        st.metric(
            "⭐ Average Rating",
            f"{avg_rating:.2f}"
        )
    
    st.divider()
    
    st.markdown("### 📌 Reviews by Topic")
    
    topic_reviews = (
        df_reviews
        .groupby("TOPIC", as_index=False)["REVIEWS"]
        .sum()
        .sort_values("REVIEWS", ascending=False)
    )
    
    st.bar_chart(
        topic_reviews.set_index("TOPIC")["REVIEWS"],
        width="stretch"
    )
    
    st.markdown("### 😊 Sentiment Distribution")
    
    sentiment_reviews = (
        df_reviews
        .groupby("SENTIMENT_LABEL", as_index=False)["REVIEWS"]
        .sum()
        .sort_values("REVIEWS", ascending=False)
    )
    
    st.bar_chart(
        sentiment_reviews.set_index("SENTIMENT_LABEL")["REVIEWS"],
        width="stretch"
    )
    
    st.markdown("### 🚩 Flagged Issues by City")
    
    city_issues = (
        df_reviews
        .groupby("CITY", as_index=False)["FLAGGED_ISSUES"]
        .sum()
        .sort_values("FLAGGED_ISSUES", ascending=False)
    )

    st.bar_chart(
        city_issues.set_index("CITY")["FLAGGED_ISSUES"],
        width="stretch"
    )
    
    st.dataframe(
        df_reviews,
        width="stretch"
    )
    
    st.divider()
    # =====================================================
    # DELIVERY SLA ANALYSIS
    # =====================================================
    
    st.subheader("🚚 Delivery SLA Analysis")
    
    st.caption("Median and 90th percentile delivery time by order hour")
    
    sla_chart = (
        df_sla
        .groupby("ORDER_HOUR", as_index=False)
        .agg(
            P50=("P50", "mean"),
            P90=("P90", "mean")
        )
        .sort_values("ORDER_HOUR")
    )
    
    st.line_chart(
        sla_chart.set_index("ORDER_HOUR")[["P50", "P90"]],
        width="stretch"
    )
    
    st.dataframe(
        df_sla,
        width="stretch"
    )
    
    st.divider()

    # -------------------------
    # DATA TABLE
    # -------------------------

    st.subheader("📋 Daily City Revenue")

    st.write(f"Rows loaded: **{len(df):,}**")

    st.dataframe(
        df,
        use_container_width=True
    )

except Exception as e:
    st.error("❌ Failed to load data")
    st.exception(e)
# -------------------------
# REVENUE TREND
# -------------------------

st.subheader("📈 Revenue Trend")

revenue_trend = (
    df.groupby("ORDER_DATE", as_index=False)["GMV"]
    .sum()
    .sort_values("ORDER_DATE")
)

st.line_chart(
    revenue_trend,
    x="ORDER_DATE",
    y="GMV"
)

st.divider()
# -------------------------
# CITY PERFORMANCE
# -------------------------

st.subheader("🏙️ City Performance")

city_performance = (
    df.groupby("CITY", as_index=False)
    .agg(
        ORDERS=("ORDERS", "sum"),
        GMV=("GMV", "sum"),
        AOV=("AOV", "mean"),
        CANCEL_RATE=("CANCEL_RATE", "mean")
    )
    .sort_values("GMV", ascending=False)
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**💰 GMV by City**")
    st.bar_chart(
        city_performance.set_index("CITY")["GMV"]
    )

with col2:
    st.markdown("**🛒 Orders by City**")
    st.bar_chart(
        city_performance.set_index("CITY")["ORDERS"]
    )

st.dataframe(
    city_performance,
    use_container_width=True
)

st.divider()
# -------------------------
# TOP RESTAURANTS
# -------------------------

st.subheader("🏆 Top Restaurant Performance")

top_restaurants = (
    df_restaurant
    .sort_values("REVENUE", ascending=False)
    .head(10)
)

st.bar_chart(
    top_restaurants.set_index("RESTAURANT_NAME")["REVENUE"]
)

st.dataframe(
    top_restaurants,
    width="stretch"
)

st.divider()
