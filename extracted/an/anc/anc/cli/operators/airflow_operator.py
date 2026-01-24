
from typing import Dict, Optional, List
from datetime import datetime, timezone
try:
    from airflow_client.client import Configuration, ApiClient
    from airflow_client.client.api.dag_api import DAGApi
    from airflow_client.client.model.dag import DAG
    from airflow_client.client.api.dag_run_api import DAGRunApi
    from airflow_client.client.model.dag_run import DAGRun

    from airflow_client.client.api.task_instance_api import TaskInstanceApi
except ImportError:
    #print("Please install the airflow-client package: pip install airflow-client")
    pass

VA_API_BASE="http://10.27.100.126:8080/api/v1"

SEA_API_BASE="http://10.208.60.181:8080/api/v1"

def trigger_airflow_dag(
    dag_id: str,
    conf: Dict,
    cluster: str,
    logical_date: Optional[datetime] = None
):
    """
    Triggers an Airflow DAG run with specified configuration.
    
    Args:
        dag_id (str): The ID of the DAG to trigger
        conf (Dict): Configuration dictionary to pass to the DAG run
        airflow_api_base (str): Base URL for the Airflow API
        logical_date (datetime, optional): Logical date for the DAG run. Defaults to current UTC time
        
    Returns:
        Optional[DAGRun]: Created DAG run object if successful, None if failed
        
    Raises:
        Exception: Any exception that occurs during the API call
    """
    if cluster == "va":
        airflow_api_base = VA_API_BASE
    else:
        airflow_api_base = SEA_API_BASE
    configuration = Configuration(
        host=airflow_api_base,
    )
    
    api_client = ApiClient(configuration)
    dag_run_api = DAGRunApi(api_client)
    
    try:
        # Use provided logical date or current UTC time
        run_date = logical_date if logical_date else datetime.now(timezone.utc)
        
        # Create a DAGRun object
        dag_run = DAGRun(
            dag_run_id=f"manual__{run_date.isoformat()}",
            logical_date=run_date,
            conf=conf
        )
        
        # Trigger the DAG run
        created_run = dag_run_api.post_dag_run(
            dag_id=dag_id,
            dag_run=dag_run
        )
        print(f"Successfully created DAG run: {created_run}")
        return created_run
        
    except Exception as e:
        print(f"Error triggering DAG run: {e}")
        return None
        
    finally:
        api_client.close()


def get_airflow_dag_status(
    dag_id: str,
    dag_run_id: str,
    cluster: str
) -> Optional[str]:
    """
    Get status of an Airflow DAG run.
    
    Args:
        dag_id: DAG identifier
        dag_run_id: Specific run identifier
        cluster: Cluster name ('va' or 'sea')
        
    Returns:
        Optional[str]: DAG run status if successful, None if failed
    """
    airflow_api_base = VA_API_BASE if cluster == "va" else SEA_API_BASE
    
    configuration = Configuration(host=airflow_api_base)
    api_client = ApiClient(configuration)
    dag_run_api = DAGRunApi(api_client)
    
    try:
        dag_run = dag_run_api.get_dag_run(
            dag_id=dag_id,
            dag_run_id=dag_run_id
        )
        return dag_run.state
        
    except Exception as e:
        print(f"Error getting DAG status: {e}")
        return None
        
    finally:
        api_client.close()


def get_airflow_dag_logs(dag_id: str, run_id: str, cluster: str) -> Optional[str]:
    configuration = Configuration(host=VA_API_BASE if cluster == "va" else SEA_API_BASE)
    api_client = ApiClient(configuration)
    task_api = TaskInstanceApi(api_client)

    try:
        tasks = task_api.get_task_instances(dag_id=dag_id, dag_run_id=run_id)
        sorted_tasks = sorted(tasks.task_instances, key=lambda x: x.start_date or "")

        for task in sorted_tasks:
                try:
                    log_response = task_api.get_log(
                        dag_id=dag_id,
                        dag_run_id=run_id,
                        task_id=task.task_id,
                        task_try_number=1
                    )
                    
                    content = eval(log_response['content'])[0][1]
                    for line in content.split('\n'):
                        if '[base]' in line:
                            log_content = line.split('[base]')[1].strip()
                            if log_content:
                                print(log_content)
                except Exception as e:
                    print(f"Error getting logs: {e}")
    finally:
        api_client.close()


def get_list_dags(dag_id: str, cluster: str, limit: int = 100) -> List[Dict]:
    configuration = Configuration(host=VA_API_BASE if cluster == "va" else SEA_API_BASE)
    api_client = ApiClient(configuration)
    dag_run_api = DAGRunApi(api_client)
    try:
        runs = dag_run_api.get_dag_runs(dag_id, limit=limit)
        results = []
        for run in runs.dag_runs:
            results.append({
                "run_id": run.dag_run_id,
                "state": run.state,
                "start_date": run.start_date,
                "end_date": run.end_date
            })
        return results
    finally:
        api_client.close()