from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args ={
    "owner: Jack",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    
}

with DAG(
    dag_id = "agentic_maintenance",
    start_date=datetime(2025,11,21),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    tags=["agentic", "rag"]

) as dag:
    
    ingest = BashOperator(
        task_id="ingest_docs",
        bash_command="python -m rag.ingest" #
    )
    ## don't need separate embedding as it's built into ingestionok
    # embed = BashOperator(
    #     task_id="embed_index",
    #     bash_command="python -m scripts.embed --in data/processed --vs vectordb"
    # )
    evaluate = BashOperator(
        "task_id="run_eval",
        bash_command-"python -m  scripts.evaluate --qs eval/qa.json --out metrics.csv"

    )

    ingest >> embed >> evaluate

