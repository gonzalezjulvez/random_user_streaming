from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

default_args = {
    "owner": "gonzalezjulvez",
    "depends_on_past": False,
    "email_on_failure": ["gonzalezjulvez@gmail.com"],
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(seconds=10),
}

with DAG(
    "CREATE_TABLES",
    default_args=default_args,
    description="A simple DAG to manage Postgres",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 6, 10),
    catchup=False,
) as dag:
    task1 = SQLExecuteQueryOperator(
        task_id="table_person",
        conn_id="postgres_default",
        sql="sql/Persons.sql",
    )
    task2 = SQLExecuteQueryOperator(
        task_id="table_addresses",
        conn_id="postgres_default",
        sql="sql/Addresses.sql",
    )
    task3 = SQLExecuteQueryOperator(
        task_id="table_details",
        conn_id="postgres_default",
        sql="sql/Contact_details.sql",
    )

    task1 >> task2 >> task3
