import click
import sys
import os
import json
from pathlib import Path
from anc.cli.util import click_group, console
from .util import get_custom_code_base_from_env, is_hf_ckpt
import uuid
import datetime
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.console import Console
from rich import box
from .operators.eval_operator import trigger_eval_job, display_evaluation_status, trigger_eval_sweep, eval_log_print, eval_stop
from typing import Optional, Set, Tuple
import re

_ALLOWED_KEYS = {"task", "tp_size", "num_fewshot", "batch_size", "seq_length", "dp_size", "pp_size", "limit", "max_seq_len", "max_out_len"}
_TASK_NAME_RE = re.compile(r"^[A-Za-z0-9_.:\-\/]+$")

def _validate_task_and_reason(task: str, allowed_tasks: Optional[Set[str]] = None) -> Tuple[bool, str]:
    if task is None:
        return False, "empty input"

    s = task.strip()
    if not s:
        return False, "empty input"
    
    if "=" not in s:
        parts = [p.strip() for p in s.split("|")]
        if not parts or any(not p for p in parts):
            return False, "empty task in basic mode"
        for t in parts:
            if not _TASK_NAME_RE.match(t):
                return False, f"invalid task name: {t}"
            if allowed_tasks is not None and t not in allowed_tasks:
                return False, f"task not allowed: {t}"
        return True, "basic"
    
    groups = [g.strip() for g in s.split("|")]
    if not groups or any(not g for g in groups):
        return False, "empty group in advanced mode"

    for grp in groups:
        kvs = [p.strip() for p in grp.split(",") if p.strip()]
        if not kvs:
            return False, "empty kv list in group"

        seen = {}
        for kv in kvs:
            if "=" not in kv:
                return False, f"missing '=' in '{kv}'"
            k, v = kv.split("=", 1)
            k, v = k.strip(), v.strip()

            if k not in _ALLOWED_KEYS:
                return False, f"unknown key '{k}'"
            if k in seen:
                return False, f"duplicate key '{k}'"
            if k == "task":
                if not v:
                    return False, "empty task value"
                if not _TASK_NAME_RE.match(v):
                    return False, f"invalid task name: {v}"
                if allowed_tasks is not None and v not in allowed_tasks:
                    return False, f"task not allowed: {v}"
            # else:
            #     if not re.fullmatch(r"\d+", v):
            #         return False, f"value for '{k}' must be a non-negative integer: {v}"

            seen[k] = v

        if "task" not in seen:
            return False, "missing required key 'task' in group"
    
    return True, "advanced"
    
@click_group()
def eval():
    pass

@eval.command()
@click.argument('model_name', required=True, type=str)
@click.option(
    '--dataset_paths', '--eval_dataset_paths',
    type=str,
    required=False,
    help='the eval dataset path of list/single of dataset'
)
@click.option(
    '--ckpt_paths',
    type=str,
    required=False,
    help='the eval ckpt path of list of ckpt'
)
@click.option(
    '--ckpt_list',
    type=str,
    required=False,
    help='comma-separated list of checkpoint full paths start with /mnt/project or /mnt/share'
)
@click.option(
    '--dataset_list', '--eval_dataset_list',
    type=str,
    required=False,
    help='comma-separated list of dataset full paths start with /mnt/project or /mnt/share'
)
@click.option(
    '--dataset_tasks', '--eval_tasks',
    type=str,
    required=False,
    help='string of dataset tasks, like "wikitext,games,reddits,openwebtext;hellaswag,truthfulqa"'
)
@click.option(
    '--tp', '--eval_tp',
    type=int,
    required=False,
    default=1,
    help='the evaltensor parallel size'
)
@click.option(
    '--pp', '--eval_pp',
    type=int,
    required=False,
    default=1,
    help='the eval pipeline parallel size'
)
@click.option(
    '--ep', '--eval_ep',
    type=int,
    required=False,
    default=1,
    help='the eval expert parallel size'
)
@click.option(
    '--seq_len', '--eval_seqlen', '--seq_length',
    type=int,
    required=False,
    default=1024,
    help='the eval sequence length'
)
@click.option(
    '--batch_size', '--eval_batch_size',
    type=int,
    required=False,
    default=1,
    help='the eval batch size'
)
@click.option(
    '--tokenizer_path', '--eval_tokenizer_path',
    type=str,
    default="",
    help='the project name'
)
@click.option(
    '--project_name',
    type=str,
    required=False,
    default="my_test",
    help='the project name'
)
@click.option(
    '--validation_batch_size',
    type=int,
    required=False,
    default=100000000,
    help='to control the max evaluation step on job side'
)
@click.option(
    '--harness_backend',
    required=False,
    type=click.Choice(['mix', 'nemo', 'vllm'], case_sensitive=False),
    help='mix, nemo, vllm, where mix: use both nemo and vllm where vllm only for long context tasks',
    default='mix',
)
@click.option(
    '--model_args',
    type=str,
    required=False,
    default="",
    help='model args'
)
@click.option(
    '--wandb_project',
    type=str,
    required=False,
    default="llm_pretraining",
    help='wandb project name'
)
@click.pass_context
def model(ctx, 
          model_name, 
          ckpt_paths, 
          dataset_paths, 
          ckpt_list, 
          dataset_list, 
          tp, 
          pp, 
          ep, 
          seq_len, 
          batch_size, 
          tokenizer_path, 
          project_name, 
          validation_batch_size,
          harness_backend,
          dataset_tasks,
          model_args,
          wandb_project):
    """command like: anc eval ds_v2 --ckpt_paths ckpt_paths --dataset_paths dataset_paths or --ckpt_list path1,path2 --dataset_list path1,path2"""
    
    # Validate that either paths or lists are provided, but not both
    if (ckpt_paths and ckpt_list) or (not ckpt_paths and not ckpt_list):
        print("Error: Please provide either --ckpt_paths OR --ckpt_list, but not both or neither")
        sys.exit(1)
    
    if (dataset_paths and dataset_list) or (not dataset_paths and not dataset_list and not dataset_tasks):
        print("Error: Please provide either --dataset_paths OR --dataset_list, but not both or neither")
        sys.exit(1)
    
    if not tokenizer_path and "tokenizer_path" not in model_args:
        print("Error: Please provide --tokenizer_path")
        sys.exit(1)
    
    # Process checkpoint paths
    eval_ckpt_paths_list = []
    if ckpt_paths:
        if not ckpt_paths.startswith("/mnt/project") and not ckpt_paths.startswith("/mnt/share"):
            print("❌ Checkpoint path is invalid, must start with /mnt/project or /mnt/share")
            print(f"   Provided path: {ckpt_paths}")
            sys.exit(1)
        
        if not os.path.exists(ckpt_paths):
            print("❌ Checkpoint path does not exist:")
            print(f"   Path: {ckpt_paths}")
            sys.exit(1)
        
        if not os.path.isdir(ckpt_paths):
            print("❌ Checkpoint path is not a directory:")
            print(f"   Path: {ckpt_paths}")
            print("   Please provide a directory containing checkpoint files.")
            sys.exit(1)
        
        # List all items in the checkpoint directory
        ckpt_items = os.listdir(ckpt_paths)
        if not ckpt_items:
            print("❌ Checkpoint directory is empty:")
            print(f"   Path: {ckpt_paths}")
            sys.exit(1)
        
        for ckpt_path in ckpt_items:
            eval_ckpt_paths_list.append(os.path.join(ckpt_paths, ckpt_path))
    else:  # ckpt_list is provided
        ckpt_list_paths = [path.strip() for path in ckpt_list.split(',')]
        
        # Check each checkpoint path individually
        valid_paths = []
        invalid_paths = []
        
        for i, ckpt_path in enumerate(ckpt_list_paths, 1):
            # Check if path starts with valid prefix
            if not (ckpt_path.startswith("/mnt/project") or ckpt_path.startswith("/mnt/share")):
                print(f"⚠️  WARNING: Checkpoint {i} path is invalid (must start with /mnt/project or /mnt/share):")
                print(f"   Path: {ckpt_path}")
                invalid_paths.append(ckpt_path)
                continue
            
            # Check if path exists
            if not os.path.exists(ckpt_path):
                print(f"⚠️  WARNING: Checkpoint {i} path does not exist:")
                print(f"   Path: {ckpt_path}")
                invalid_paths.append(ckpt_path)
                continue
            
            # Path is valid
            print(f"✅ Checkpoint {i} path validated: {os.path.basename(ckpt_path)}")
            valid_paths.append(ckpt_path)
            eval_ckpt_paths_list.append(ckpt_path)
        
        # Summary
        print(f"\n📊 Checkpoint Path Summary:")
        print(f"   ✅ Valid paths: {len(valid_paths)}")
        print(f"   ❌ Invalid paths: {len(invalid_paths)}")
        
        if invalid_paths:
            print(f"\n❌ Found {len(invalid_paths)} invalid checkpoint path(s). Cannot proceed.")
            for path in invalid_paths:
                print(f"   - {path}")
            print("\nPlease fix the invalid paths and try again.")
            sys.exit(1)
        
        if not valid_paths:
            print("❌ No valid checkpoint paths found. Cannot proceed.")
            sys.exit(1)
    
    # Sort by the numeric value that follows 'step=' in the filename
    def _extract_step_from_path(path: str) -> int:
        try:
            if 'step=' in path:
                tail = path.split('step=')[1]
                digits = []
                for ch in tail:
                    if ch.isdigit():
                        digits.append(ch)
                    else:
                        break
                return int(''.join(digits)) if digits else 0
        except Exception:
            pass
        return 0
    # Ensure a consistent order in list mode as well: sort by 'step='
    eval_ckpt_paths_list.sort(key=_extract_step_from_path)
    # Process dataset paths
    final_dataset_paths = None
    if dataset_paths:
        if not dataset_paths.startswith("/mnt/project") and not dataset_paths.startswith("/mnt/share"):
            print("❌ Dataset path is invalid, must start with /mnt/project or /mnt/share")
            print(f"   Provided path: {dataset_paths}")
            sys.exit(1)
        
        if not os.path.exists(dataset_paths):
            print("❌ Dataset path does not exist:")
            print(f"   Path: {dataset_paths}")
            sys.exit(1)
        
        if not os.path.isdir(dataset_paths):
            print("❌ Dataset path is not a directory:")
            print(f"   Path: {dataset_paths}")
            print("   Please provide a directory containing dataset files.")
            sys.exit(1)
        
        # Validate each dataset file in the directory
        dataset_files = [f for f in os.listdir(dataset_paths) if os.path.isfile(os.path.join(dataset_paths, f)) or os.path.isdir(os.path.join(dataset_paths, f))]
        valid_dataset_files = []
        invalid_dataset_files = []
        
        print(f"\n🔍 Validating datasets in directory: {dataset_paths}")
        
        for i, dataset_file in enumerate(dataset_files, 1):
            full_path = os.path.join(dataset_paths, dataset_file)
            
            # Check if the file/directory exists and is accessible
            if not os.path.exists(full_path):
                print(f"⚠️  WARNING: Dataset {i} does not exist:")
                print(f"   Path: {full_path}")
                invalid_dataset_files.append(dataset_file)
                continue
            
            # Check if it's readable
            if not os.access(full_path, os.R_OK):
                print(f"⚠️  WARNING: Dataset {i} is not readable:")
                print(f"   Path: {full_path}")
                invalid_dataset_files.append(dataset_file)
                continue
            
            # Path is valid
            print(f"✅ Dataset {i} validated: {dataset_file}")
            valid_dataset_files.append(dataset_file)
        
        # Summary
        print(f"\n📊 Dataset Directory Summary:")
        print(f"   ✅ Valid datasets: {len(valid_dataset_files)}")
        print(f"   ❌ Invalid datasets: {len(invalid_dataset_files)}")
        
        if invalid_dataset_files:
            print(f"\n❌ Found {len(invalid_dataset_files)} invalid dataset file(s). Cannot proceed.")
            for file in invalid_dataset_files:
                print(f"   - {file}")
            print("\nPlease fix the invalid dataset files and try again.")
            sys.exit(1)
        
        if not valid_dataset_files:
            print("❌ No valid dataset files found in directory. Cannot proceed.")
            sys.exit(1)
        
        final_dataset_paths = dataset_paths
    elif dataset_list:  # dataset_list is provided
        dataset_list_paths = [path.strip() for path in dataset_list.split(',')]
        
        # Check each dataset path individually
        valid_dataset_paths = []
        invalid_dataset_paths = []
        
        for i, dataset_path in enumerate(dataset_list_paths, 1):
            # Check if path starts with valid prefix
            if not (dataset_path.startswith("/mnt/project") or dataset_path.startswith("/mnt/share")):
                print(f"⚠️  WARNING: Dataset {i} path is invalid (must start with /mnt/project or /mnt/share):")
                print(f"   Path: {dataset_path}")
                invalid_dataset_paths.append(dataset_path)
                continue
            
            # Check if path exists
            if not os.path.exists(dataset_path):
                print(f"⚠️  WARNING: Dataset {i} path does not exist:")
                print(f"   Path: {dataset_path}")
                invalid_dataset_paths.append(dataset_path)
                continue
            
            # Path is valid
            print(f"✅ Dataset {i} path validated: {os.path.basename(dataset_path)}")
            valid_dataset_paths.append(dataset_path)
        
        # Summary
        print(f"\n📊 Dataset Path Summary:")
        print(f"   ✅ Valid paths: {len(valid_dataset_paths)}")
        print(f"   ❌ Invalid paths: {len(invalid_dataset_paths)}")
        
        if invalid_dataset_paths:
            print(f"\n❌ Found {len(invalid_dataset_paths)} invalid dataset path(s). Cannot proceed.")
            for path in invalid_dataset_paths:
                print(f"   - {path}")
            print("\nPlease fix the invalid paths and try again.")
            sys.exit(1)
        
        if not valid_dataset_paths:
            print("❌ No valid dataset paths found. Cannot proceed.")
            sys.exit(1)
        
        # For now, we'll use the first valid dataset path as the main path
        final_dataset_paths = valid_dataset_paths[0] if valid_dataset_paths else None
    
    # the recipt of the eval
    run_id = str(uuid.uuid4())
    
    # Create a rich Table for configuration details
    config_table = Table(box=box.ROUNDED, show_header=False, border_style="blue", expand=True)
    config_table.add_column("Parameter", style="cyan", no_wrap=True, width=30)
    config_table.add_column("Value", style="green", no_wrap=False, overflow="fold")
    
    # Add basic info
    config_table.add_row("Model Name", model_name)
    
    # Display checkpoint paths
    if ckpt_paths:
        #config_table.add_row("Checkpoint Directory", ckpt_paths)
        config_table.add_row("Found Checkpoints", f"{len(eval_ckpt_paths_list)} checkpoints")
        for i, ckpt_path in enumerate(eval_ckpt_paths_list, 1):
            config_table.add_row(f"  Checkpoint {i}", ckpt_path)
    else:
        config_table.add_row("Checkpoint Mode", "List Mode")
        config_table.add_row("Total Checkpoints", f"{len(eval_ckpt_paths_list)} checkpoints")
        for i, ckpt_path in enumerate(eval_ckpt_paths_list, 1):
            config_table.add_row(f"  Checkpoint {i}", ckpt_path)
    
    # Display dataset paths
    if dataset_paths:
        #config_table.add_row("Dataset Directory", dataset_paths)
        # List contents of the dataset directory
        if os.path.isdir(dataset_paths):
            dataset_files = [f for f in os.listdir(dataset_paths) if os.path.isfile(os.path.join(dataset_paths, f)) or os.path.isdir(os.path.join(dataset_paths, f))]
            config_table.add_row("Found Datasets", f"{len(dataset_files)} items")
            for i, dataset_file in enumerate(dataset_files, 1):
                full_path = os.path.join(dataset_paths, dataset_file)
                config_table.add_row(f"  Dataset {i}", full_path)
    elif dataset_list:
        config_table.add_row("Dataset Mode", "List Mode")
        dataset_list_paths = [path.strip() for path in dataset_list.split(',')]
        config_table.add_row("Total Datasets", f"{len(dataset_list_paths)} datasets")
        for i, dataset_path in enumerate(dataset_list_paths, 1):
            config_table.add_row(f"  Dataset {i}", dataset_path)
    
    config_table.add_row("Tokenizer Path", tokenizer_path)
    config_table.add_row("Project Name", project_name)
    
    # Display dataset tasks if provided
    
    if dataset_tasks:
        valid, reason = _validate_task_and_reason(dataset_tasks)
        if not valid:
            print(f"❌ Invalid dataset tasks: {reason}")
            sys.exit(1)
        
        # Split dataset_tasks by "|" and display each task on a separate line
        tasks_list = [task.strip() for task in dataset_tasks.split("|")]
        for task in tasks_list:
            if task.startswith(";"):
                tasks_list.remove(task)
                tasks_list.insert(0, task)
        
        config_table.add_row("Dataset Tasks Mode", "List Mode")
        config_table.add_row("Total Tasks", f"{len(tasks_list)} tasks")
        for i, task in enumerate(tasks_list, 1):
            config_table.add_row(f"  Task {i}", task)
    
    if model_args:
        config_table.add_row("Model Args", model_args)
    
    wandb_api_key = os.environ.get("WANDB_API_KEY", "a5c281c2ae6c3e5d473072cf64f8c98e7a68b00d")
    if wandb_project:
        config_table.add_row("Wandb project", wandb_project)
        if wandb_api_key:
            config_table.add_row("Wandb API Key", wandb_api_key)
        else:
            config_table.add_row("Wandb API Key", "❌ No set")
    
    custom_code_base_string = get_custom_code_base_from_env()
    if len(custom_code_base_string) > 0:
        config_table.add_row("Custom Code Base", custom_code_base_string)
    
    # Add parallelism config
    config_table.add_section()
    config_table.add_row("Tensor Parallel", str(tp))
    config_table.add_row("Pipeline Parallel", str(pp))
    config_table.add_row("Expert Parallel", str(ep))
    
    # Add run parameters
    config_table.add_section()
    config_table.add_row("Batch Size", str(batch_size))
    config_table.add_row("Sequence Length", str(seq_len))
    config_table.add_row("Validation Batch Size", str(validation_batch_size))

    # Create title with run ID
    title = Text(f"✨ EVALUATION RECEIPT [ID: {run_id}] ✨", style="bold magenta")
    
    # Print the title and table directly without panel wrapper
    console.print("\n")
    console.print(title, justify="center")
    console.print("\n")
    console.print(config_table)
    console.print("\n")
    # TODO: Implement need the user confirm the evaluation receipt
    user_confirm = input("Do you want to start the evaluation? (y/n): ")
    if user_confirm.lower() != 'y':
        print("Evaluation cancelled.")
        sys.exit(0)
    
    # Prepare dataset list for the API call
    dataset_list_for_api = []
    if dataset_paths:
        # For directory mode, create a list of full paths to all dataset files
        if os.path.isdir(dataset_paths):
            dataset_files = [f for f in os.listdir(dataset_paths) if os.path.isfile(os.path.join(dataset_paths, f)) or os.path.isdir(os.path.join(dataset_paths, f))]
            for dataset_file in dataset_files:
                full_path = os.path.join(dataset_paths, dataset_file)
                dataset_list_for_api.append(full_path)
    elif dataset_list:
        # For list mode, use the validated dataset paths
        dataset_list_for_api = valid_dataset_paths


    # for hf ckpt, force use vllm backend
    harness_backend = "vllm" if is_hf_ckpt(eval_ckpt_paths_list[0]) else harness_backend
    
    trigger_eval_job(run_id, 
                     model_name, 
                     project_name, 
                     eval_ckpt_paths_list,  # This is already a list
                     dataset_list_for_api,  # This is now a list
                     tp, 
                     pp, 
                     ep, 
                     seq_len, 
                     batch_size, 
                     tokenizer_path, 
                     validation_batch_size,
                     dataset_tasks,
                     model_args,
                     wandb_project,
                     wandb_api_key,
                     custom_code_base_string,
                     harness_backend)

@eval.command(name='status')
@click.argument('eval_id', required=True, type=str)
def status(eval_id):
   """check eval job: anc eval status xxx """
   display_evaluation_status(eval_id)


@eval.command()
@click.argument('spec', required=True, type=str)
@click.pass_context
def sweep(ctx, 
          spec):
    project = os.getenv("MLP_PROJECT", "llm")
    cluster = os.getenv("MLP_CLUSTER", "il2")
    trigger_eval_sweep(spec, cluster, project)

@eval.command()
@click.argument('evalution_id', required=True, type=str)
@click.pass_context
def log(ctx, 
          evalution_id):
    project = os.getenv("MLP_PROJECT", "llm")
    cluster = os.getenv("MLP_CLUSTER", "il2")
    eval_log_print(evalution_id, cluster)


@eval.command()
@click.argument('evalution_id', required=True, type=str)
@click.pass_context
def stop(ctx, 
          evalution_id):
    project = os.getenv("MLP_PROJECT", "llm")
    cluster = os.getenv("MLP_CLUSTER", "il2")
    eval_stop(evalution_id, cluster)


def add_command(cli_group):
    cli_group.add_command(eval)
