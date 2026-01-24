import click
import os
from anc.cli.load_test.load_testing_operator import LoadTestingOperator
from anc.cli.load_test.backend_request_func import ASYNC_REQUEST_FUNCS
from anc.cli.load_test.data_analysis import analyze_benchmark_results
import argparse
import json
from .util import click_group
import logging
logger = logging.getLogger("anc")
# there are two subcommands: run and plot
# run is used to start the server and send the benchmark requests, this will generate a json file with the results, by default it will also plot the results
# plot is used to plot the results from the json file. 

defaults = {
            # 'enable_chunked_prefill': "False",
            'enable_prefix_caching': "True",
            'use_v2_block_manager': "False",
            'gpu_memory_utilization': "0.95",
            'max-model-len': "8000",
            'multi_step_stream_outputs': "True",
            'tensor_parallel_size': "4",
            'num-speculative-tokens': "5",
            "speculative-draft-tensor-parallel-size": "1",
        }
def parse_arg_list(ctx, param, value):
    if value is None:
        return None
    try:
        return [int(x.strip()) for x in value.split(',')]
    except ValueError:
        raise click.BadParameter('values must be integers')

def parse_arg_float(ctx, param, value):
    if value is None:
        return None
    try:
        return [float(x.strip()) for x in value.split(',')]
    except ValueError:
        raise click.BadParameter('values must be integers')

def parse_arg_str(ctx, param, value):
    if value is None:
        return None
    return [str(x.strip()) for x in value.split(',')]

def validate_dataset_path(ctx, param, value):
    if ctx.params.get("dataset_name") == "anc" and not value:
        raise click.BadParameter("dataset-path is required when dataset-name is 'anc'.")
    return value

@click_group()
def loadtest():
    """Commands for load testing and benchmark analysis."""
    pass

@loadtest.command(name="run")
# Server configuration options
@click.option("--backend", default="vllm", type=click.Choice(list(ASYNC_REQUEST_FUNCS.keys())), help="Backend to use, for anc data set, we will use openai-chat backend")
@click.option("--model", type=str, required=True, help="Path of the model and tokenizer")
@click.option("--model-id", type=str, required=False, help="model name or id to use during load testing")
@click.option("--speculative-model", callback=parse_arg_str, required=False, help="path to draft model")
@click.option("--speculative-draft-tensor-parallel-size", callback=parse_arg_str, default= "1", type=str, required=False, help="Name of the model.")
@click.option("--num-speculative-tokens", callback=parse_arg_str, type=str, default="5",required=False, help="Number of speculative tokens.")
@click.option("--speculative-disable-by-batch-size", type=str, default="1000",required=False, help="turn off speculative decoding if the batch size is larger than the specified value")
@click.option("--host", type=str, default="localhost", help="Host address.")
@click.option("--port", type=int, default=8000, help="Port number.")
@click.option("--base-url", type=str, default=None, help="Server or API base url if not using http host and port.")
@click.option("--start_server_only", is_flag=True, help="Start the server only, do not send the benchmark requests. this is useful for debugging")
@click.option("--start_otlp_server", is_flag=True, help="Start the otlp to collect metrics from server")
@click.option("--skip-server", is_flag=True, help="Skip server start. This is useful for debugging")
@click.option("--dry-run", is_flag=True, help="Dry run. This is useful for debugging")
@click.option("--reuse-server-each-concur", is_flag=True, help="reuse the server for each concurrency level. you can turn this off without prefix caching")
@click.option("--tensor-parallel-size", 
              callback=parse_arg_str,
              default=defaults["tensor_parallel_size"], 
              help="Tensor parallel size for model parallelism. Specify multiple values separated by commas (e.g., --tensor-parallel-size '1,2,4').")
# @click.option("--enable-chunked-prefill", 
#               callback=parse_arg_str,
#               default=defaults["enable_chunked_prefill"], 
#               help="Enable chunked prefill for vLLM. Specify multiple values separated by commas.")
@click.option("--enable-prefix-caching", 
              callback=parse_arg_str,
              default=defaults["enable_prefix_caching"], 
              help="Enable prefix caching for vLLM. Specify multiple values separated by commas.")
@click.option("--use-v2-block-manager", 
              callback=parse_arg_str,
              default=defaults["use_v2_block_manager"], 
              help="Use v2 block manager for vLLM. Specify multiple values separated by commas.")
@click.option("--gpu-memory-utilization", 
              default=defaults["gpu_memory_utilization"], 
              help="GPU memory utilization for vLLM. Specify multiple values separated by commas.")
@click.option("--max-model-len", 
              callback=parse_arg_str,
              default=defaults["max-model-len"], 
              help="Maximum model length for vLLM. Specify multiple values separated by commas.")

@click.option("--extra-vllm-args", type=str, default="--max-seq-len-to-capture 8192", help="Extra arguments for vLLM. Specify multiple values separated by commas")
@click.option("--max-num-seqs", 
              callback=parse_arg_str,
              help="Maximum number of sequences for vLLM. Specify multiple values separated by commas.")
@click.option("--multi-step-stream-outputs", 
              callback=parse_arg_str,
              default=defaults["multi_step_stream_outputs"], 
              help="Enable multi-step stream outputs for vLLM. Specify multiple values separated by commas.")
# Load testing configuration options
@click.option("--endpoint", type=str, default="/v1/completions", help="API endpoint.")
@click.option("--dataset-name", type=click.Choice(["anc", "random", "hf"]), default="random", help="Name of the dataset to benchmark on.")
@click.option("--dataset-path", type=str, default=None, help="Path to the load testing dataset, required if using anc dataset.",callback=validate_dataset_path)
@click.option("--multi-turn", type=bool, default=False, help="Use multi-turn conversations, only used for anc dataset. if True, then we will send each prompt in multi-turn conversations in order. num_requests is the total number of conversations")
@click.option("--max-concurrency", 
              callback=parse_arg_list,
              help="Maximum number of concurrent requests. Specify multiple values separated by commas (e.g., --max-concurrency '1,4,8,16')")
@click.option("--tokenizer", type=str, help="Name or path of the tokenizer, if not using the default tokenizer.")
@click.option("--best-of", type=int, default=1, help="Generates `best_of` sequences per prompt and returns the best one.")
@click.option("--use-beam-search", is_flag=True, help="Use beam search.")
@click.option("--num-prompts", type=int, default=1000, help="Number of prompts to process.")
@click.option("--num-prompts-per-concurrency", type=int, default=None, help="Number of prompts for concurrency test. if specified, we will set num_prompts to num_prompts_per_concurrency * max_concurrency")
@click.option("--num-warmup-requests", type=int, default=0, help="Number of warmup requests to send before the actual load test.")
@click.option("--logprobs", type=int, default=None, help="Number of logprobs-per-token to compute & return as part of the request.")
@click.option("--request-rate", type=float, default=float("inf"), help="Number of requests per second.")
@click.option("--burstiness", type=float, default=1.0, help="Burstiness factor of the request generation.")
@click.option("--seed", type=int, default=None, required=False, help="if specified, we will set the random seed to the specified value. this insures same requests are sent for each concurrency")
@click.option("--trust-remote-code", is_flag=True, help="Trust remote code from huggingface.")
@click.option("--disable-tqdm", is_flag=True, help="Disable tqdm progress bar.")
@click.option("--profile", is_flag=True, help="Use Torch Profiler.")
@click.option("--save-result", is_flag=True, help="Save benchmark results to a json file.")
@click.option("--metadata", type=str, multiple=True, help="Key-value pairs for metadata of this run.")
@click.option("--result-dir", type=str, default=None, help="Directory to save benchmark json results.")
@click.option("--result-filename", type=str, default=None, help="Filename to save benchmark json results.")
@click.option("--ignore-eos", is_flag=True, help="Set ignore_eos flag when sending the benchmark request.")
@click.option("--percentile-metrics", type=str, default="input_token,output_token,fs_token,ttft,ttfs,tpot,itl,e2el", help="Comma-separated list of selected metrics to report percentiles.")
@click.option("--metric-percentiles", type=str, default="90", help="Comma-separated list of percentiles for selected metrics.")
@click.option("--goodput", type=str, multiple=True, help="Specify service level objectives for goodput as `KEY:VALUE` pairs.")

# Dataset-specific options
@click.option("--anc-output-len", type=int, default=None, help="Output length for each request. Overrides the output length from the anc dataset.")
@click.option("--random-input-len", 
              callback=parse_arg_list,
              default="1024", 
              help="Number of input tokens per request, used only for random sampling. Specify multiple values separated by commas.")
@click.option("--random-output-len", 
              callback=parse_arg_list,
              default="128", 
              help="Number of output tokens per request, used only for random sampling. Specify multiple values separated by commas.")
@click.option("--random-range-ratio", 
              default=1.0, 
              help="Range of sampled ratio of input/output length, used only for random sampling")
@click.option("--random-prefix-len", 
              callback=parse_arg_list,
              default="0", 
              help="Number of fixed prefix tokens before random context. Specify multiple values separated by commas.")
@click.option("--hf-subset", type=str, default=None, help="Subset of the HF dataset.")
@click.option("--hf-split", type=str, default=None, help="Split of the HF dataset.")
@click.option("--hf-output-len", type=int, default=None, help="Output length for each request. Overrides the output lengths from the sampled HF dataset.")
@click.option("--tokenizer_mode", type=click.Choice(['auto', 'slow', 'mistral']), default="auto", help="The tokenizer mode.")
def run_loadtest(**kwargs):
    """Run load testing with the specified parameters."""
    # Convert kwargs to argparse.Namespace
    args = argparse.Namespace(**kwargs)
    
    reset_result_output_argument(args)
    op = LoadTestingOperator()
    
    # Print key server configuration parameters for better debugging
    # Define all server parameters that can have multiple values
    grid_search_server_params = {
        'tensor_parallel_size': args.tensor_parallel_size,
        # 'enable_chunked_prefill': args.enable_chunked_prefill,
        'enable_prefix_caching': args.enable_prefix_caching,
        'use-v2-block-manager': args.use_v2_block_manager,
        'max-model-len': args.max_model_len,
        'multi_step_stream_outputs': args.multi_step_stream_outputs,
        # Add more parameters here as needed
    }
    if args.speculative_model:
        grid_search_server_params.update({
            'speculative-model': args.speculative_model,
            'speculative-draft-tensor-parallel-size': args.speculative_draft_tensor_parallel_size,
            'num-speculative-tokens': args.num_speculative_tokens,
        })
    # Generate all combinations of parameters
    import itertools
    param_names = list(grid_search_server_params.keys())
    param_values = [grid_search_server_params[name] for name in param_names]

    max_concurrency_list = args.max_concurrency
    random_prefix_len_list = args.random_prefix_len
    random_input_len_list = args.random_input_len
    random_output_len_list = args.random_output_len
    benchmark_results_list = []
    base_result_dir = args.result_dir if args.result_dir else "./"
    for values in itertools.product(*param_values):
        # Create a dictionary with the current combination of parameters
        param_dict = dict(zip(param_names, values))
        
        # Create the server configuration with fixed and variable parameters
        server_config = {
            'backend': args.backend,
            'model': args.model,
            'host': args.host,
            'port': args.port,
            'gpu_memory_utilization': args.gpu_memory_utilization,
            'speculative_disable_by_batchsize': args.speculative_disable_by_batch_size,
            'max_num_seqs': args.max_num_seqs,
            'extra_vllm_args': args.extra_vllm_args,
            **param_dict  # Unpack the current parameter combination
        }
        logger.info(f'server_config: {server_config}')

        for key, value in server_config.items():
            print(f'  {key}: {value}')

        print(f'\n\n{"="*100}\n\n')
        set_result_dir(base_result_dir, args, param_dict)
       
       
        start_server(args, op, server_config)
        if args.dry_run:
            continue
        for i in range(len(max_concurrency_list)):
            max_concurrency = max_concurrency_list[i]
            # skip restarting server for the first concurrency run
            if i!=0 and not args.reuse_server_each_concur and not args.skip_server:
                op.stop_server()
                start_server(args, op, server_config)
            if args.num_prompts_per_concurrency:
                args.num_prompts = args.num_prompts_per_concurrency * max_concurrency
            if args.dataset_name == "random":
                for random_prefix_len in random_prefix_len_list:
                    for input_len in random_input_len_list:
                        for output_len in random_output_len_list:
                                args.max_concurrency = max_concurrency
                                args.random_prefix_len = random_prefix_len
                                args.random_input_len = input_len
                                args.random_output_len = output_len
                                args.result_filename = f"all_results.json"
                                benchmark_result = op.load_test(args)
                                client_config = {
                                    'max_concurrency': max_concurrency,
                                    'random_prefix_len': random_prefix_len,
                                    'random_input_len': input_len,
                                    'random_output_len': output_len,
                                }
                                # Combine server and client configs with benchmark results
                                result_json = {
                                    **server_config,
                                    **client_config,
                                    **benchmark_result
                                }
                                benchmark_results_list.append(result_json)
                                # Save all benchmark results to a JSON file
                                result_file_path = os.path.join(base_result_dir, args.result_filename)
                                with open(result_file_path, "w") as f:
                                    json.dump(benchmark_results_list, f, indent=2)
            else:
                client_config = {
                    'max_concurrency': max_concurrency,
                }
                args.max_concurrency = max_concurrency
                args.result_filename = f"all_results.json"
                benchmark_result = op.load_test(args)
                client_config = {
                    'max_concurrency': max_concurrency,
                }
                                # Combine server and client configs with benchmark results
                result_json = {
                                    **server_config,
                                    **client_config,
                                    **benchmark_result
                                }
                benchmark_results_list.append(result_json)
                                # Save all benchmark results to a JSON file
                result_file_path = os.path.join(base_result_dir, args.result_filename)
                with open(result_file_path, "w") as f:
                    json.dump(benchmark_results_list, f, indent=2)
        if not hasattr(args, 'skip_server') or not args.skip_server:
            op.stop_server()
    
    # After all tests are complete, analyze the results
    if args.result_filename:
        result_file_path = os.path.join(base_result_dir, args.result_filename)
        if os.path.exists(result_file_path):
            analyze_benchmark_results(result_file_path, base_result_dir)
            logger.info(f"Analysis complete. Results saved to {base_result_dir}")

def start_server(args, op, server_config):
    logger.info(f'Result directory: {args.result_dir}')
    if not hasattr(args, 'skip_server') or not args.skip_server:
        logger.info(f'Starting server with configuration:')
        op.start_server(args.dry_run, args.result_dir, start_otlp_server=args.start_otlp_server, **server_config)
        if args.start_server_only:
            print(f'Server started. Exiting.')
            exit()
    else:
        print(f'Skipping server start as requested')

@loadtest.command(name="plot")
@click.argument("result_file", type=click.Path(exists=True))
@click.option("--output-dir", type=str, default=None, help="Directory to save analysis results")
# @click.option("--dataset-name", type=click.Choice(["anc", "random", "hf"]), default="anc", help="Name of the dataset used to generated the result file. default is random ")
def plot_results(result_file, output_dir):
    """Analyze and plot benchmark results from a previously saved JSON file."""
    print(f"result_file: {result_file}")
    print(f"output_dir: {output_dir}")
    # print(f"dataset_name: {dataset_name}")
    if not output_dir:
        output_dir = os.path.dirname(result_file)
        if not output_dir:
            output_dir = "."
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"Analyzing benchmark results from {result_file}")
    analyze_benchmark_results(result_file, output_dir)

def reset_result_output_argument(args):
    if args.dataset_name == "random":
        args.ignore_eos = True

    if args.result_filename and not args.result_dir:
        print(f'Warning: --result-filename is specified but --result-dir is not. Using the current directory {os.getcwd()} as the result directory.')
        args.result_dir = os.path.dirname("")
        
    if args.result_dir and not os.path.exists(args.result_dir):
        print(f'Warning: --result-dir {args.result_dir} does not exist. Creating it.')
        os.makedirs(args.result_dir)
    
    if args.result_dir or args.result_filename:
        args.save_result = True

    if args.dataset_name == "anc":
        args.backend = "openai-chat"
        args.endpoint = "/v1/chat/completions"

def set_result_dir(base_result_dir, args, param_dict):
    # Add this line to use the base_result_dir from args
    
    dir_components = []
    # Define abbreviations and default values for parameters
    abbreviations = {
        'tensor_parallel_size': 'tp',
        'enable_chunked_prefill': 'chunk',
        'enable_prefix_caching': 'prefix',
        'use-v2-block-manager': 'v2block',
        'multi_step_stream_outputs': 'multistep',
    }
    
    # Default values to skip
    for key, value in param_dict.items():
        # Skip if using default value
        if key in defaults and value == defaults[key]:
            continue
            
        # Use abbreviation if available
        param_name = abbreviations.get(key, key.replace('-', '_'))
        dir_components.append(f'{param_name}_{value}')
    
    config_dir_name = '_'.join(dir_components)
    args.result_dir = os.path.join(base_result_dir, config_dir_name)
    if not os.path.exists(args.result_dir):
        os.makedirs(args.result_dir)

@loadtest.command(name="analyze_input")
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--output-dir", type=str, default=None, help="Directory to save analysis results")
@click.option("--seed", type=int, default=None, required=False, help="if specified, we will set the random seed to the specified value. this insures same requests are sent for each concurrency")
@click.option("--num-prompts", type=int, default=1000, help="Number of prompts to process.")
@click.option("--sample-size", type=int, default=10, help="Number of prompts to sample for common prefix analysis.")
@click.option("--tokenizer", type=str, help="Name or path of the tokenizer, if not we will onlly count words stats.")
def analyze_input_data(input_file, output_dir, seed, num_prompts, sample_size, tokenizer):
    """Analyze and plot benchmark results from a previously saved JSON file."""
    from anc.cli.load_test.input_data_analysis import process_input_data
    print(f"input_file: {input_file}")
    print(f"output_dir: {output_dir}")
    print(f"seed: {seed}")
    print(f"num_prompts: {num_prompts}")
    print(f"sample_size: {sample_size}")
    print(f"tokenizer: {tokenizer}")
    # print(f"dataset_name: {dataset_name}")
    if not output_dir:
        output_dir = os.path.dirname(input_file)
        if not output_dir:
            output_dir = "."
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, "input_data_stats.json")
    process_input_data(input_file, tokenizer, sample_size)