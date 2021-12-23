from airflow import DAG

from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator    # Execute Spark Job
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor        # Monitor Spark Job
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
import boto3



from airflow.utils.dates import days_ago





with DAG(
    'enem_batch_spark_k8s',
    default_args={
        'owner': 'Manoel',
        'depends_on_past': False,
        'email': ['manosk88@gmail.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'max_active_runs': 1,
    },
    description='submit spark-pi as sparkApplication on kubernetes',
    schedule_interval="0 */2 * * *",    # Run for each 2 hours
    start_date=days_ago(1),
    catchup=False,
    tags=['spark', 'kubernetes', 'batch', 'enem'],
) as dag:

    converte_parquet = SparkKubernetesOperator(
        task_id='conv_parq',                           # Mudei pra ver se resolveria um problema de conexão
        namespace="airflow",
        application_file="enem_converte_parquet.yaml",
        kubernetes_conn_id="kubernetes_default",
        do_xcom_push=True                 # True to make possible the Sensor retrieve the status to monitor
    )


converte_parquet 