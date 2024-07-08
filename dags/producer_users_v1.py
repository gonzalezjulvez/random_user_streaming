import os
import sys
from datetime import datetime, timedelta
from typing import Any

from airflow import DAG
from airflow.decorators import task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

# Añadir src al path para importar módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.user_random import format_data as process_data
from src.user_random import get_data as fetch_data

default_args = {
    "owner": "gonzalezjulvez",
    "depends_on_past": False,
    "email_on_failure": ["gonzalezjulvez@gmail.com"],
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(seconds=10),
}

dag = DAG(
    "random_user_dag",
    default_args=default_args,
    description="A simple DAG to fetch and format random user data",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 6, 10),
    catchup=False,
)


@task(dag=dag)
def get_data() -> Any:
    return fetch_data()


@task(dag=dag)
def format_data(data: Any):
    formatted_data = process_data(data)
    return formatted_data


# Definimos la tarea de inserción fuera de la función de Python
insert_data = SQLExecuteQueryOperator(
    task_id="insert_persons",
    conn_id="postgres_default",
    sql="""
    INSERT INTO persons (id, first_name, last_name, gender, dob, registered_date) VALUES (
    '{{ ti.xcom_pull(task_ids='format_data')['id'] }}',
    '{{ ti.xcom_pull(task_ids='format_data')['first_name'] }}',
    '{{ ti.xcom_pull(task_ids='format_data')['last_name'] }}',
    '{{ ti.xcom_pull(task_ids='format_data')['gender'] }}',
    '{{ ti.xcom_pull(task_ids='format_data')['dob'] }}',
    '{{ ti.xcom_pull(task_ids='format_data')['registered_date'] }}'
    );
    """,
    dag=dag,
)

insert_contact_details_data = SQLExecuteQueryOperator(
    task_id="insert_contact_details_data",
    conn_id="postgres_default",
    sql="""
    INSERT INTO contact_details (person_id, email, username, phone, picture) VALUES (
    '{{ ti.xcom_pull(task_ids='format_data')['id'] }}',
    '{{ ti.xcom_pull(task_ids='format_data')['email'] }}',
    '{{ ti.xcom_pull(task_ids='format_data')['username'] }}',
    '{{ ti.xcom_pull(task_ids='format_data')['phone'] }}',
    '{{ ti.xcom_pull(task_ids='format_data')['picture'] }}'
    );
    """,
    dag=dag,
)

insert_addresses_data = SQLExecuteQueryOperator(
    task_id="insert_addresses_data",
    conn_id="postgres_default",
    sql="""
    INSERT INTO addresses (person_id, address, post_code) VALUES (
    '{{ ti.xcom_pull(task_ids='format_data')['id'] }}',
    '{{ ti.xcom_pull(task_ids='format_data')['address'] }}',
    '{{ ti.xcom_pull(task_ids='format_data')['post_code'] }}'
    );
    """,
    dag=dag,
)

with dag:
    data = get_data()
    formatted_data = format_data(data)
    formatted_data >> [
        insert_data,
        insert_contact_details_data,
        insert_addresses_data,
    ]  # Encadenamos las tareas
