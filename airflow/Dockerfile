FROM apache/airflow:3.0.3

# Airflow providers + packages needed by the Zomato pipeline
RUN pip install --no-cache-dir \
      apache-airflow-providers-snowflake \
      apache-airflow-providers-fab \
      ollama \
      snowflake-connector-python \
      python-dotenv

# Separate dbt environment
RUN python -m venv /opt/airflow/dbt_venv && \
    /opt/airflow/dbt_venv/bin/pip install --no-cache-dir "dbt-snowflake==1.8.*"
