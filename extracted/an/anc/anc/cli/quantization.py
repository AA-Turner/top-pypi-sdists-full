import click
import sys
import os
import json
from pathlib import Path
from anc.cli.util import click_group
from .operators.airflow_operator import trigger_airflow_dag, \
    get_airflow_dag_status, get_airflow_dag_logs, get_list_dags
from .util import ConfigManager
import uuid



def modify_path(project_path, project):
    path_parts = project_path.split('/')
    if project_path.startswith("/mnt/project"):
        if "llm" in project:
            path_parts.insert(3, "project-llm")
        elif "voice" in project:
            path_parts.insert(3, "project-voice")
    return '/'.join(path_parts)


def get_model_size(model_path):
   config_path = os.path.join(model_path, "config.json")
   if not os.path.exists(config_path):
       return None
       
   try:
       with open(config_path, 'r') as f:
           config = json.load(f)
       
       hidden_size = config.get('hidden_size')
       n_layers = config.get('num_hidden_layers')
       vocab_size = config.get('vocab_size')
       intermediate_size = config.get('intermediate_size')
       
       if not all([hidden_size, n_layers, vocab_size, intermediate_size]):
           return None
       
       embedding_params = hidden_size * vocab_size
       attention_params = 4 * hidden_size * hidden_size
       ffn_params = hidden_size * intermediate_size * 2
       ln_params = 2 * hidden_size
       
       params_per_layer = attention_params + ffn_params + ln_params
       total_params = embedding_params + (params_per_layer * n_layers)
       total_params_b = total_params / (1024 * 1024 * 1024)
       
       return "large" if total_params_b > 70 else "small"
       
   except Exception as e:
       print(f"Error processing config file: {e}")
       return None


@click_group()
def quant():
    pass

@quant.command()
@click.argument('model_input', type=str)
@click.option(
    '--schema',
    type=str,
    default="FP8_DYNAMIC",
    required=False,
    help='Number of GPUs to deploy'
)
@click.option(
    '--mode',
    type=str,
    default="quant_only",
    required=False,
    help='Mode: quant_only (only quantization), full (trigger both quantization and baseline pipelines for comparison)'
)
@click.pass_context
def model(ctx, model_input, schema, mode):
    """
    Run quantization pipeline on a model.
    
    Modes:
    - quant_only: Only perform quantization 
    - full: Trigger both quantization and baseline pipelines for comparison
            (uses flexible_quant_pipeline with skip_quant=False/True)
    
    Example: anc quant model path/to/model --mode full
    """
    print("model_input:", model_input)
    if  not model_input.startswith("/mnt/project") and not model_input.startswith("/mnt/share"):
        print("model input path is invalid, must be start with /mnt/project or /mnt/share")
        sys.exit(0)
    model_size = get_model_size(model_input)
    if model_size is None:
        print("This is not a validate model path, can't find a config.json file")
        sys.exit(0)

    config_manager = ConfigManager()
    _, cluster, _ = config_manager.get_environment()
    if "va" in cluster.lower():
        cluster = 'va'
    elif "sea" in cluster.lower():
        cluster = 'sea'
    
    dag_id = ""
    if cluster == "va":
        dag_id = "only_quant_pipeline"
    elif cluster == "sea":
        dag_id = "only_quant_sea_pipeline"

    # full steps include output loss and evaluations.
    if mode == "full" and cluster == "va":
        # For full mode, trigger two pipelines: one with quant, one without (baseline)
        model_output_quant = str(Path(model_input) / f"quant_{schema}")
        model_output_baseline = str(Path(model_input) / "baseline_results")
        
        dag_id_flexible = "flexible_quant_pipeline"
        
        # First DAG: quantization pipeline
        job_name_quant = f"quant-serving-{str(uuid.uuid4())[:8]}"
        conf_quant = {
            "model_input": model_input,
            "model_output": model_output_quant,
            "scheme": schema,
            "job_name": job_name_quant,
            "model_size": model_size,
            "skip_quant": False,
            "serving_gpus": 0,
        }
        
        # Second DAG: baseline pipeline (skip quantization)
        job_name_baseline = f"baseline-serving-{str(uuid.uuid4())[:8]}"
        conf_baseline = {
            "model_input": model_input,
            "model_output": model_output_baseline,
            "scheme": schema,  # Not used when skip_quant=True
            "job_name": job_name_baseline,
            "model_size": model_size,
            "skip_quant": True,
            "serving_gpus": 0,
        }
        
        print(f"Triggering quantization pipeline...")
        created_run_quant = trigger_airflow_dag(dag_id_flexible, conf_quant, cluster)
        
        print(f"Triggering baseline pipeline...")
        created_run_baseline = trigger_airflow_dag(dag_id_flexible, conf_baseline, cluster)
        
        if created_run_quant and created_run_baseline:
            print(f"\n=== Quantization Pipeline ===")
            print(f"DAG Run ID: {created_run_quant.dag_run_id}")
            print(f"Job Name: {job_name_quant}")
            print(f"Output: {model_output_quant}")
            print(f"Schema: {schema}")
            print(f"Skip Quant: False")
            
            print(f"\n=== Baseline Pipeline ===")
            print(f"DAG Run ID: {created_run_baseline.dag_run_id}")
            print(f"Job Name: {job_name_baseline}")
            print(f"Output: {model_output_baseline}")
            print(f"Skip Quant: True")
            
            print(f"\nTo check status:")
            print(f"  \033[36manc quant status --run-id {created_run_quant.dag_run_id} --dag-id {dag_id_flexible}\033[0m")
            print(f"  \033[36manc quant status --run-id {created_run_baseline.dag_run_id} --dag-id {dag_id_flexible}\033[0m")
            
            print(f"\nTo view logs:")
            print(f"  \033[36manc quant logs --run-id {created_run_quant.dag_run_id} --dag-id {dag_id_flexible}\033[0m")
            print(f"  \033[36manc quant logs --run-id {created_run_baseline.dag_run_id} --dag-id {dag_id_flexible}\033[0m")
        
        return  # Exit early for full mode
    
    assert dag_id != ""

    model_output = str(Path(model_input) / f"quant_{schema}")
    job_name = f"quant-serving-{str(uuid.uuid4())[:8]}"
    conf = {
        "model_input": model_input,
        "model_output": model_output,
        "schema": schema,
        "job_name": job_name,
        "model_size": model_size,
    }
    created_run = trigger_airflow_dag(dag_id, conf, cluster)
    if created_run:
        dag_run_id = created_run.dag_run_id
        print(f"\nDAG Run ID: {dag_run_id}")
        print(f"\nTo check status:")
        print(f"  \033[36manc quant status --run-id {dag_run_id} --dag-id {dag_id}\033[0m")
        print(f"\nTo view logs:")
        print(f"  \033[36manc quant logs --run-id {dag_run_id} --dag-id {dag_id}\033[0m")

@quant.command()
@click.option('--run-id', type=str, help='DAG run ID')
@click.option('--dag-id', type=str, help='DAG ID')
def status(run_id, dag_id):
    """Check quantization status: anc quant status --run-id <id> --dag-id <id>"""
    config_manager = ConfigManager()
    _, cluster, _ = config_manager.get_environment()
    cluster = 'va' if "va" in cluster.lower() else 'sea'
    
    if run_id:
        status = get_airflow_dag_status(dag_id, run_id, cluster)
        print(f"Status: {status}")

@quant.command(name='logs')
@click.option('--run-id', type=str, help='DAG run ID')
@click.option('--dag-id', type=str, help='DAG ID')
@click.option('--latest', is_flag=True, help='Show latest run logs')
def quant_logs(run_id, dag_id, latest):
    """Get quantization logs: anc quant logs --run-id <id> --dag-id <id>"""
    config_manager = ConfigManager()
    _, cluster, _ = config_manager.get_environment()
    cluster = 'va' if "va" in cluster.lower() else 'sea'
    
    try:
        if run_id:
            get_airflow_dag_logs(dag_id, run_id, cluster)
    except Exception as e:
        print(f"Error getting logs: {e}")

@quant.command(name='list')
@click.option('--run-id', type=str, help='Show specific run status')
@click.option(
   '--dag-id',
   required=True,
   help='DAG ID: only_quant_pipeline/quant_pipeline/only_quant_sea_pipeline/flexible_quant_pipeline/flexible_quant_sea_pipeline',
   type=click.Choice([
       'only_quant_pipeline', 
       'quant_pipeline', 
       'only_quant_sea_pipeline',
       'flexible_quant_pipeline',
   ])
)
@click.option('--latest', is_flag=True, help='Show latest runs')
def quant_list(run_id, dag_id, latest):
   """List quantization runs: anc quant list --dag-id only_quant_pipeline """
   config_manager = ConfigManager()
   _, cluster, _ = config_manager.get_environment()
   cluster = 'va' if "va" in cluster.lower() else 'sea'

   runs = get_list_dags(dag_id, cluster, limit=10 if latest else 100)
   for run in runs:
       print(f"Run ID: {run['run_id']}")
       print(f"State: {run['state']}")
       print(f"Start: {run['start_date']}")
       print("---")

def add_command(cli_group):
    cli_group.add_command(quant)