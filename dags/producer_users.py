import os
import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.UserRandom import RandomUser

defaults_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "random_user_dag",
    default_args=defaults_args,
    description="A simple DAG to fetch and format random user data",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 6, 10),
    catchup=False,
)


def fetch_and_format_user():
    user = RandomUser()
    user.get_data()
    formatted_data = user.format_data()
    print(formatted_data)


fetch_and_format_user_task = PythonOperator(
    task_id="fetch_and_format_user_task",
    python_callable=fetch_and_format_user,
    dag=dag,
)

fetch_and_format_user_task
