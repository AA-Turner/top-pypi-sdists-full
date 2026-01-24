from anc.api.connection import Connection
from requests.exceptions import RequestException
import os
import sys
import json
from rich.console import Console
from rich.table import Table, box
from rich.text import Text
import uuid
import yaml
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def _format_and_print_logs(log_text):
    """Format and print workflow logs with better readability"""
    import re
    from datetime import datetime
    
    lines = log_text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Try to parse JSON logs first
        if line.startswith('{"result":'):
            try:
                import json
                log_entry = json.loads(line)
                result = log_entry.get('result', {})
                content = result.get('content', '')
                pod_name = result.get('podName', '')
                
                if content:
                    # Extract and format timestamp if present in content
                    timestamp_match = re.search(r'time="([^"]+)"', content)
                    if timestamp_match:
                        timestamp_str = timestamp_match.group(1)
                        try:
                            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                            formatted_time = dt.strftime('%H:%M:%S')
                            content = re.sub(r'time="[^"]+" level=info msg="', f'[{formatted_time}] ', content)
                            content = re.sub(r'" argo=true.*$', '', content)
                        except:
                            pass
                    
                    print(content)
                elif not content and pod_name:
                    # Empty content but has podName, skip these empty entries
                    continue
                continue
            except:
                pass
        
        # Handle regular text logs
        # Extract and format timestamp if present
        timestamp_match = re.search(r'time="([^"]+)"', line)
        if timestamp_match:
            timestamp_str = timestamp_match.group(1)
            try:
                dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                formatted_time = dt.strftime('%H:%M:%S')
                line = re.sub(r'time="[^"]+" level=info msg="', f'[{formatted_time}] ', line)
                line = re.sub(r'" argo=true.*$', '', line)
            except:
                pass
        
        # Clean up common patterns and print
        # Remove excessive whitespace and format nicely
        if line.startswith('==='):
            print(f"\n{line}")
        elif line.startswith('ERROR:') or line.startswith('WARNING:'):
            print(f"⚠️  {line}")
        elif line.startswith('Successfully installed') or line.startswith('Saved'):
            print(f"✅ {line}")
        elif 'MB/s eta' in line or '━━━━━' in line:
            # Skip download progress bars
            continue
        elif line.startswith('[notice]'):
            print(f"ℹ️  {line}")
        else:
            print(line)

def _format_and_print_single_line(line):
    """Format and print a single log line"""
    import re
    from datetime import datetime
    
    line = line.strip()
    if not line:
        return
        
    # Try to parse JSON logs first
    if line.startswith('{"result":'):
        try:
            import json
            log_entry = json.loads(line)
            result = log_entry.get('result', {})
            content = result.get('content', '')
            
            if content:
                # Extract and format timestamp if present in content
                timestamp_match = re.search(r'time="([^"]+)"', content)
                if timestamp_match:
                    timestamp_str = timestamp_match.group(1)
                    try:
                        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        formatted_time = dt.strftime('%H:%M:%S')
                        content = re.sub(r'time="[^"]+" level=info msg="', f'[{formatted_time}] ', content)
                        content = re.sub(r'" argo=true.*$', '', content)
                    except:
                        pass
                
                print(content)
            return
        except:
            pass
    
    # Handle regular text logs
    # Extract and format timestamp if present
    timestamp_match = re.search(r'time="([^"]+)"', line)
    if timestamp_match:
        timestamp_str = timestamp_match.group(1)
        try:
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            formatted_time = dt.strftime('%H:%M:%S')
            line = re.sub(r'time="[^"]+" level=info msg="', f'[{formatted_time}] ', line)
            line = re.sub(r'" argo=true.*$', '', line)
        except:
            pass
    
    # Clean up common patterns and print
    if line.startswith('==='):
        print(f"\n{line}")
    elif line.startswith('ERROR:') or line.startswith('WARNING:'):
        print(f"⚠️  {line}")
    elif line.startswith('Successfully installed') or line.startswith('Saved'):
        print(f"✅ {line}")
    elif 'MB/s eta' in line or '━━━━━' in line:
        # Skip download progress bars
        return
    elif line.startswith('[notice]'):
        print(f"ℹ️  {line}")
    else:
        print(line)

MM_BASE_URL = "http://model-management-service.infra.svc.cluster.local:5000"


def trigger_eval_job(
    run_id: str,
    model_name: str,
    project_name: str,
    ckpt_list: list[str],
    dataset_list: list[str],
    tp: int,
    pp: int,
    ep: int,
    seq_len: int,
    batch_size: int,
    tokenizer_path: str,
    validation_batch_size: int,
    dataset_tasks: str = None,
    model_args: str = None,
    wandb_project: str = None,
    wandb_api_key: str = None,
    custom_code_base_string: str = None,
    harness_backend: str = 'mix'
) -> bool:
    cluster = os.environ.get("MLP_CLUSTER", "il2")
    project = os.environ.get("MLP_PROJECT", "llm")
    
    data = {
        "evaluation_id": run_id,
        "modality": "nlp",
        "model_name": model_name,
        "project_name": project_name,
        "eval_ckpt_list": ckpt_list,
        "eval_dataset_list": dataset_list,
        "project": project,
        "cluster": cluster,
        "eval_tp": tp,
        "eval_pp": pp,
        "eval_ep": ep,
        "eval_seqlen": seq_len,
        "eval_batch_size": batch_size,
        "eval_tokenizer_path": tokenizer_path,
        "status": "start",
        "validation_batch_size": validation_batch_size,
        "code_info": {
            "CUSTOM_CODE_BASE_STRING": custom_code_base_string.strip() if custom_code_base_string else ""
        },
        "harness_backend": harness_backend,
    }
    
    # Add dataset_tasks to data if provided
    if dataset_tasks:
        data["eval_tasks"] = dataset_tasks
    
    if model_args:
        data["model_args"] = model_args
    
    if wandb_project and wandb_api_key:
        data["wandb_project"] = wandb_project
        data["wandb_api_key"] = wandb_api_key

    try:
        conn = Connection(url=MM_BASE_URL)
        response = conn.post("/evaluations", json=data)

        # Check if the status code is in the 2xx range
        if 200 <= response.status_code < 300:
            response_data = response.json()
            evaluation_id = response_data.get('evaluation_id')
            if evaluation_id:
                print(f"Evaluation task added successfully. Your Eval ID is: \033[92m{evaluation_id}\033[0m")
                # print(f"You can check the status of your evaluation using: \033[96manc eval status {evaluation_id}\033[0m")
                # print(f"All historical results can be viewed at: \033[94mhttp://model.anuttacon.ai/models/467e151d-a52a-47f9-8791-db9c776635db/evaluations\033[0m")
            else:
                print("Evaluation failed, didn't get the evaluation id")
        else:
            #print(f"Error: Server responded with status code {response.status_code}")
            print(f"{response.text}")

    except RequestException as e:
        print(f"Sorry, you can't add dataset out of clusters, please use it in a notebook")
    except json.JSONDecodeError:
        print("Sorry: received invalid JSON response from server")
    except KeyboardInterrupt:
        print(f"Operation interrupted.")
        sys.exit(0)
    except Exception as e:
        print(f"Sorry, your command run failed, you can try again or reach out infra team")


def display_evaluation_status(evaluation_id: str):
    conn = Connection(url=MM_BASE_URL)
    response = conn.get(f"/evaluations/{evaluation_id}")
    
    if response.status_code == 200:
        data = response.json()
        
        # Create a Rich console instance
        console = Console(width=200)  # Set wider console width
        
        # Display basic evaluation information
        eval_info = Table(title=f"Evaluation ID: {evaluation_id}", box=box.ROUNDED)
        eval_info.add_column("Parameter", style="cyan")
        eval_info.add_column("Value", style="green")
        
        # Add some key evaluation parameters
        eval_info.add_row("Model Name", data.get('model_name') or 'N/A')
        eval_info.add_row("Project", data.get('project') or 'N/A')
        eval_info.add_row("Submitted At", data.get('submitted_at') or 'N/A')
        
        console.print(eval_info)
        console.print()
        
        # Parse and display the evaluation_results_info
        if data.get('evaluation_results_info'):
            try:
                results_info = json.loads(data['evaluation_results_info'])
                
                # Create table for evaluation results with expanded width
                results_table = Table(title="Evaluation Results", box=box.ROUNDED, show_lines=True)
                results_table.add_column("Checkpoint", style="magenta", width=50, no_wrap=True)
                results_table.add_column("Dataset", style="blue", width=25, no_wrap=True)
                results_table.add_column("Endpoint URL", style="yellow", no_wrap=True)
                
                # Add rows for each checkpoint and dataset combination
                for ckpt_path, dataset_list in results_info.items():
                    # Get basename for the checkpoint
                    ckpt_basename = os.path.basename(ckpt_path)
                    
                    # Handle the case where each checkpoint has multiple datasets
                    for dataset_info in dataset_list:
                        if len(dataset_info) >= 4:
                            # Extract dataset info
                            dataset_path = dataset_info[0]
                            endpoint_url = dataset_info[1]
                            job_id = dataset_info[2]
                            status = dataset_info[3]
                            
                            # Get basename for dataset
                            dataset_basename = os.path.basename(dataset_path)
                            
                            results_table.add_row(
                                ckpt_basename,
                                dataset_basename,
                                endpoint_url
                            )
                
                # Ensure the table doesn't truncate content
                console.print(results_table)
            except json.JSONDecodeError:
                console.print(f"[red]Error parsing evaluation results info: {data['evaluation_results_info']}[/red]")
        else:
            console.print("[yellow]No evaluation results information available.[/yellow]")
    else:
        console.print(f"[red]Error retrieving evaluation status: {response.text}[/red]")


def trigger_eval_sweep(spec: dict, cluster, project, run_id=None):
    if run_id is None:
        
        run_id = str(uuid.uuid4())

    cluster = os.environ.get("MLP_CLUSTER", "il2")
    project = os.environ.get("MLP_PROJECT", "llm")
    config = None
    try:
        with open(spec, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading {spec}: \n {e}")
        return

    if config is None or len(config) == 0:
        print("YAML file is empty or invalid.")
        return

    models = config['generation']['models']
    if len(models) == 0:
        print("No models specified in the spec file.")
        return

    unique_model_names = set()
    for model in models:
        if 'model_name' in model and model['model_name'] in unique_model_names:
            print(f"Duplicate model_name found in spec: {model['model_name']}. Please ensure all model names are unique.")
            return
        unique_model_names.add(model['model_name'])

    data = {
        "evaluation_id": run_id,
        "spec": config,
        "cluster": cluster,
        "project": project,
        "model_name": "sweep",
    }
    try:
        conn = Connection(url=MM_BASE_URL)
        response = conn.post("/evaluations", json=data)

        # Check if the status code is in the 2xx range
        if 200 <= response.status_code < 300:
            response_data = response.json()
            evaluation_id = response_data.get('evaluation_id')
            if evaluation_id:
                print(f"Sweep workflow submmited. you can use the highlight command: \033[92manc eval log {evaluation_id}\033[0m to check the logs")
                print(f"You can use the highlight command to stop it: \033[93manc eval stop {evaluation_id}\033[0m if needed")
            else:
                print("Evaluation failed, didn't get the evaluation id")
        else:
            #print(f"Error: Server responded with status code {response.status_code}")
            print(f"{response.text}")

    except RequestException as e:
        print(f"Sorry, you can't add dataset out of clusters, please use it in a notebook")
    except json.JSONDecodeError:
        print("Sorry: received invalid JSON response from server")
    except KeyboardInterrupt:
        print(f"Operation interrupted.")
        sys.exit(0)
    except Exception as e:
        print(f"Sorry, your command run failed, you can try again or reach out infra team")

def _resolve_argo_server_url(cluster_name):
        if cluster_name == "il2":
            return "https://10.218.61.160"
        elif cluster_name == "hb":
            return "https://10.53.139.209:2746"
        raise ValueError(f"Unsupported cluster: {cluster_name} for argo server url")

def eval_log_print(evaluation_id, cluster, follow=True):
    import time
    
    namespace = "argo"

    # First, get workflow_name from evaluation service
    conn = Connection(url=MM_BASE_URL)
    response = conn.get(f"/evaluations/{evaluation_id}")
    
    if response.status_code != 200:
        print(f"Failed to get evaluation info: HTTP {response.status_code} {response.text}")
        return
    
    try:
        data = response.json()
        workflow_name = data.get('train_job_url')
        if not workflow_name or workflow_name.startswith("http"):
            print(f"No workflow found for evaluation {evaluation_id}.")
            return
        
        print(f"Found workflow: {workflow_name} for evaluation {evaluation_id}")
        if follow:
            print("Following logs (Ctrl+C to stop)...")
    except Exception as e:
        print(f"Failed to parse evaluation response: {e}")
        return
    
    base_url = _resolve_argo_server_url(cluster)
    logs_url = f"{base_url}/api/v1/workflows/{namespace}/{workflow_name}/log"
    
    # Stream logs with follow capability
    last_log_content = ""
    last_log_lines_count = 0
    first_run = True
    
    try:
        while True:
            # Get workflow status to check if it's still running
            wf_url = f"{base_url}/api/v1/workflows/{namespace}/{workflow_name}"
            try:
                wf_resp = requests.get(wf_url, verify=False)
                if wf_resp.status_code == 200:
                    wf = wf_resp.json()
                    phase = wf.get('status', {}).get('phase', 'Unknown')
                    
                    # Get aggregated logs - try multiple parameter combinations
                    param_variants = [
                        {},  # No parameters
                        {"logOptions.follow": "false"},
                        {"follow": "false"},
                        {"logOptions.container": "main"},
                    ]
                    
                    log_found = False
                    for params in param_variants:
                        agg_resp = requests.get(logs_url, params=params, verify=False)
                        
                        if first_run:
                            print(f"Debug: Trying logs with params {params}: HTTP {agg_resp.status_code}")
                        
                        if agg_resp.status_code == 200:
                            current_log_content = agg_resp.text.strip()
                            
                            if current_log_content:
                                log_found = True
                                if current_log_content != last_log_content:
                                    current_lines = current_log_content.split('\n')
                                    
                                    if first_run:
                                        # First run: show all existing logs
                                        print("==== Workflow Logs ====")
                                        _format_and_print_logs(current_log_content)
                                        first_run = False
                                    else:
                                        # Subsequent runs: only print new lines
                                        new_lines = current_lines[last_log_lines_count:]
                                        
                                        if new_lines and (new_lines[0] or len(new_lines) > 1):  # Skip if only empty line
                                            for line in new_lines:
                                                if line.strip():  # Only print non-empty lines
                                                    _format_and_print_single_line(line)
                                    
                                    last_log_content = current_log_content
                                    last_log_lines_count = len(current_lines)
                                break
                    
                    if first_run and not log_found:
                        print(f"No logs found with any parameter combination. Workflow phase: {phase}")
                        first_run = False
                    
                    # Check if workflow is completed
                    if not follow or phase in ['Succeeded', 'Failed', 'Error']:
                        if phase in ['Succeeded']:
                            print(f"\n✅ Workflow {workflow_name} completed successfully!")
                        elif phase in ['Failed', 'Error']:
                            print(f"\n❌ Workflow {workflow_name} failed with status: {phase}")
                        break
                        
                else:
                    print(f"Failed to get workflow status: HTTP {wf_resp.status_code}")
                    if not follow:
                        break
                        
            except Exception as e:
                print(f"Error fetching logs: {e}")
                if not follow:
                    break
            
            if follow and phase not in ['Succeeded', 'Failed', 'Error']:
                time.sleep(2)  # Wait 2 seconds before next poll
            else:
                break
                
    except KeyboardInterrupt:
        print(f"\n🛑 Log following stopped by user")
    except Exception as e:
        print(f"\n❌ Error in log streaming: {e}")
    

def eval_stop(evaluation_id: str, cluster):
    namespace = "argo"

    # First, get workflow_name from evaluation service
    conn = Connection(url=MM_BASE_URL)
    response = conn.get(f"/evaluations/{evaluation_id}")
    
    if response.status_code != 200:
        print(f"Failed to get evaluation info: HTTP {response.status_code} {response.text}")
        return
    
    try:
        data = response.json()
        workflow_name = data.get('train_job_url')
        if not workflow_name or workflow_name.startswith("http"):
            print(f"No workflow found for evaluation {evaluation_id}.")
            return
        
        print(f"Found workflow: {workflow_name} for evaluation {evaluation_id}")
    except Exception as e:
        print(f"Failed to parse evaluation response: {e}")
        return
    
    base_url = _resolve_argo_server_url(cluster)
    
    # First check workflow status
    wf_url = f"{base_url}/api/v1/workflows/{namespace}/{workflow_name}"
    try:
        wf_resp = requests.get(wf_url, verify=False)
        if wf_resp.status_code == 200:
            wf = wf_resp.json()
            phase = wf.get('status', {}).get('phase', 'Unknown')
            print(f"Current workflow status: {phase}")
            
            if phase in ['Succeeded', 'Failed', 'Error']:
                print(f"⚠️  Workflow is already completed with status: {phase}")
                return
        else:
            print(f"Failed to get workflow status: HTTP {wf_resp.status_code}")
            return
    except Exception as e:
        print(f"Error getting workflow status: {e}")
        return
    
    # Stop the workflow using Argo API
    stop_url = f"{base_url}/api/v1/workflows/{namespace}/{workflow_name}/stop"
    
    try:
        print(f"Stopping workflow {workflow_name}...")
        stop_resp = requests.put(stop_url, verify=False)
        
        if stop_resp.status_code == 200:
            print(f"Successfully stop for workflow {workflow_name}")
            
        else:
            print(f"❌ Failed to stop workflow: HTTP {stop_resp.status_code}")
            print(f"Response: {stop_resp.text}")
            
    except Exception as e:
        print(f"❌ Error stopping workflow: {e}")
