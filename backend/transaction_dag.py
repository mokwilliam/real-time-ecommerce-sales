from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from e_commerce.gen_fake_data import get_fake_data
from e_commerce.process_data import process_transaction

default_args = {
    "owner": "e_commerce",
    "depends_on_past": False,
    "start_date": datetime.now(),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

# Create the DAG instance
dag = DAG(
    "transaction_dag",
    default_args=default_args,
    description="This DAG processes the transaction of the data",
    schedule_interval=timedelta(minutes=2),
)

# Define the tasks

# Task 1: Generate fake data
task_1 = PythonOperator(
    task_id="generate_fake_data",
    python_callable=get_fake_data,
    dag=dag,
)

# Task 2: Process the transaction
task_2 = PythonOperator(
    task_id="process_transaction",
    python_callable=process_transaction,
    dag=dag,
)

# Define the order of the tasks
task_1 >> task_2
