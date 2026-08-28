# 🍔 Zomato AI Data Engineering Platform

An end-to-end data engineering platform built around Zomato-style food delivery data.

The project combines **Snowflake, dbt, Apache Airflow, AI-powered review enrichment, and Streamlit** to build an automated data pipeline, transform raw data into analytics-ready models, generate customer insights, and present business metrics through an interactive dashboard.

---

## 🚀 Project Overview

This project demonstrates a modern data engineering workflow:

```text
                    ZOMATO DATA PLATFORM
                           │
                           ▼
                    📥 Raw Data Sources
                           │
                           ▼
                    ❄️ Snowflake
                           │
                           ▼
                    🔄 dbt Transformations
                           │
                           ▼
                    ⚙️ Apache Airflow
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
       🤖 AI Review               📊 Analytics
        Enrichment                Dashboard
              │                         │
              └────────────┬────────────┘
                           ▼
                    💡 Business Insights
