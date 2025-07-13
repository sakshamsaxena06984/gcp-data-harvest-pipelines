from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.operators.datafusion import CloudDataFusionStartPipelineOperator
from airflow.providers.google.cloud.sensors.datafusion import CloudDataFusionPipelineStateSensor

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 7, 12),
    'depends_on_past': False,
    'email': ['saxena123saksham@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=3)
}

dag = DAG('elt_employee_data',
          default_args=default_args,
          description='Runs an external Python script',
          schedule_interval='@daily',
          catchup=False
          )

with dag:
    run_script_task = BashOperator(
        task_id='elt_employee_data',
        bash_command='python /home/airflow/gcs/dags/scripts/extract.py'
    )

    start_datafusion_pipeline = CloudDataFusionStartPipelineOperator(
        location='us-central1',
        pipeline_name='emp-etl-pipeline',
        instance_name='datafusion-uses',
        task_id='start_datafusion_pipeline',
        asynchronous=True,
        do_xcom_push=True
    )

    wait_for_pipeline = CloudDataFusionPipelineStateSensor(
        pipeline_name='emp-etl-pipeline',
        task_id='wait_for_pipeline',
        instance_name='datafusion-uses',
        location='us-central1',
        pipeline_id="{{ ti.xcom_pull(task_ids='start_datafusion_pipeline') }}",
        expected_statuses=['COMPLETED'],
        failure_statuses=['FAILED', 'CANCELLED'],
        poke_interval=30,
        timeout=1800
    )

    run_script_task >> start_datafusion_pipeline >> wait_for_pipeline
