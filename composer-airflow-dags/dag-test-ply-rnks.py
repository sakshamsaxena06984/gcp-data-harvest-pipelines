from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.operators.dataflow import DataflowTemplatedJobStartOperator


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 7, 13),
    'depends_on_past': False,
    'email': ['saxena123saksham@gamil.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('run_external_script',
          default_args=default_args,
          schedule_interval='@daily',
          catchup=False)


run_script_task = BashOperator(
    task_id='run_script',
    bash_command='python /home/airflow/gcs/dags/scripts/extract_data.py',
    dag=dag
)

trigger_dataflow_task = DataflowTemplatedJobStartOperator(
    task_id='trigger_dataflow_job',
    template='gs://dataflow-templates-us-central1/latest/GCS_Text_to_BigQuery',
    project_id='enduring-guard-465218-f5',
    location='us-central1',
    parameters={
        "javascriptTextTransformGcsPath": "gs://bkt-dataflow-metadata-uses/udf.js",
        "JSONPath": "gs://bkt-dataflow-metadata-uses/bq.json",
        "javascriptTextTransformFunctionName": "transform",
        "outputTable": "enduring-guard-465218-f5.projectuses.icc_test_batsman_ranking",
        "inputFilePattern": "gs://bkt-ranking-data-uses/batsmen_ranking.csv",
        "bigQueryLoadingTemporaryDirectory": "gs://bkt-dataflow-metadata-uses/tmp/"
    }
)


# Set dependency
run_script_task >> trigger_dataflow_task
