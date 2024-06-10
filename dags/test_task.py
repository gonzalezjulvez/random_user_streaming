import logging
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "test_dag",
    default_args=default_args,
    description="A simple test DAG",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 6, 10),
    catchup=False,
)


def test_function():
    logging.info("This is a test log message.")


test_task = PythonOperator(
    task_id="test_task",
    python_callable=test_function,
    dag=dag,
)

test_task
