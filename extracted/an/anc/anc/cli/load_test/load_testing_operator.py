import argparse
import asyncio
import base64
import io
import json
import os
import random
import time
import warnings
from dataclasses import dataclass
from datetime import datetime
from typing import Any, AsyncGenerator, Collection, Dict, List, Optional, Tuple

import numpy as np
from .backend_request_func import (ASYNC_REQUEST_FUNCS, RequestFuncInput,
                                  RequestFuncOutput)
from datasets import load_dataset
from PIL.Image import Image
from tqdm.asyncio import tqdm

from anc.data.jsonl_dataset import JsonlDataset
from anc.data.anc_processor import Processor  
from .multidialog_processor import MultiDialogProcessor
from .metric_collector import MetricCollector

try:
    from vllm.transformers_utils.tokenizer import get_tokenizer
except ImportError:
    from .backend_request_func import get_tokenizer

try:
    from vllm.utils import FlexibleArgumentParser
except ImportError:
    from argparse import ArgumentParser as FlexibleArgumentParser

MILLISECONDS_TO_SECONDS_CONVERSION = 1000

from .server import ServerFactory 
class LoadTestingOperator:
    def __init__(self):
        self.server = None
        self.metric_collector = None
    def start_server(self, dry_run, server_log_dir, start_otlp_server=False, **kwargs):
        """
        Start a server for load testing based on the specified backend.
        
        Args:
            **kwargs: Arguments for server initialization, must include 'backend'
        
        Returns:
            bool: True if server started successfully, False otherwise
        """
        # If args is a Namespace, convert to dict
        if hasattr(kwargs, '__dict__'):
            kwargs = vars(kwargs)
            
        # Extract backend type from kwargs or use default
        backend = kwargs.get('backend', 'vllm')
        try:
            if self.server:
                self.server.stop()
            #start vllm server
            self.server = ServerFactory.create_server(backend, **kwargs)
            self.server.start(dry_run=dry_run, server_log_dir=server_log_dir, start_otlp_server=start_otlp_server)
            # Start the metric collector
            if start_otlp_server:
                self.start_metric_collector(server_log_dir)
        except Exception as e:
            print(f"Failed to start {backend} server: {e}")
            raise e 

    def start_metric_collector(self, server_log_dir):
        server_metric_path = os.path.join(server_log_dir, f"otlp_metric_{int(time.time())}.json")
        self.metric_collector = MetricCollector(export_file_path=server_metric_path)
        self.metric_collector.start()
        print(f"\n{'-'*100}")
        print(f"Metric collector will save data to {server_metric_path}")
        print(f"{'-'*100}\n")
             
    def stop_server(self):
        self.server.stop()
        # Stop the metric collector
        if self.metric_collector:
            self.metric_collector.stop()

    def load_test(self, args: argparse.Namespace):
        """
        Start a load test with the given parameters.
        
        :param test_plan: Path to the test plan file
        :param duration: Duration of the load test in seconds
        :param concurrency: Number of concurrent users
        """
        print(args)
        if args.seed is not None:
            random.seed(args.seed)
            np.random.seed(args.seed)
        max_concurrency = args.max_concurrency

        backend = args.backend
        model_id = args.model_id if args.model_id is not None else args.model
        tokenizer_id = args.tokenizer if args.tokenizer is not None else args.model

        if args.base_url is not None:
            api_url = f"{args.base_url}{args.endpoint}"
            base_url = f"{args.base_url}"
        else:
            api_url = f"http://{args.host}:{args.port}{args.endpoint}"
            base_url = f"http://{args.host}:{args.port}"

        tokenizer = get_tokenizer(tokenizer_id,
                                trust_remote_code=args.trust_remote_code)


        if args.dataset_name == "anc":
            if args.backend == "vllm":
                input_requests = sample_anc_requests(
                    dataset_path=args.dataset_path,
                    num_requests=args.num_prompts,
                    tokenizer=tokenizer,
                    processor_class=MultiDialogProcessor,
                    fixed_output_len=args.anc_output_len,
                    multi_turn=args.multi_turn
                )
            elif args.backend == "openai-chat":
                input_requests = sample_anc_requests_openai_chat(
                    dataset_path=args.dataset_path,
                    num_requests=args.num_prompts,
                    fixed_output_len=args.anc_output_len
                )
            else:
                raise ValueError(f"backend: {args.backend} is not supported for anc dataset yet")

        elif args.dataset_name == "hf":
            input_requests = sample_hf_requests(
                dataset_path=args.dataset_path,
                dataset_subset=args.hf_subset,
                dataset_split=args.hf_split,
                num_requests=args.num_prompts,
                tokenizer=tokenizer,
                random_seed=args.seed,
                fixed_output_len=args.hf_output_len,
            )

        elif args.dataset_name == "random":
            input_requests = sample_random_requests(
                prefix_len=args.random_prefix_len,
                input_len=args.random_input_len,
                output_len=args.random_output_len,
                num_prompts=args.num_prompts,
                range_ratio=args.random_range_ratio,
                tokenizer=tokenizer,
            )

        else:
            raise ValueError(f"Unknown dataset: {args.dataset_name}")

        gootput_config_dict = check_goodput_args(args)
        try:
            benchmark_result = asyncio.run(
            benchmark(
                backend=backend,
                api_url=api_url,
                base_url=base_url,
                model_id=model_id,
                tokenizer=tokenizer,
                input_requests=input_requests,
                logprobs=args.logprobs,
                best_of=args.best_of,
                request_rate=args.request_rate,
                burstiness=args.burstiness,
                disable_tqdm=args.disable_tqdm,
                profile=args.profile,
                selected_percentile_metrics=args.percentile_metrics.split(","),
                selected_percentiles=[
                    float(p) for p in args.metric_percentiles.split(",")
                ],
                ignore_eos=args.ignore_eos,
                gootput_config_dict=gootput_config_dict,
                max_concurrency=max_concurrency,
                    num_warmup_requests=int(args.num_warmup_requests),
                ))
            self.process_and_save_results(args, max_concurrency, backend, model_id, tokenizer_id, benchmark_result)

            try:
                print(f'\n{"-"*100}')
                print(f'Collecting prometheus metrics')
                print(f"\n{'-'*100}")
                from .prometheus_metric import collect_prometheus_metrics, analyze_metrics 
                current_time = int(time.time())
                raw_prometheus_metrics_path = os.path.join(args.result_dir, f"raw_prometheus_metrics_{current_time}.txt")
                processed_prometheus_metrics_path = os.path.join(args.result_dir, f"processed_prometheus_metrics_{current_time}.json")
                raw_prometheus_metrics = collect_prometheus_metrics(server_url=f"{base_url}", save_raw_path=raw_prometheus_metrics_path)
                analyze_metrics(raw_prometheus_metrics, save_results_path=processed_prometheus_metrics_path)
                print(f'Prometheus metrics saved to {processed_prometheus_metrics_path}')
            except Exception as e:
                print(f"Warning: Failed to collect prometheus metrics: {e}")

            if self.metric_collector:
                print(f"\n{'-'*100}")
                print(f"Waiting for metric collector to flush data")
                print(f"\n{'-'*100}")
                time.sleep(10) # wait for metric collector to flush data
                self.metric_collector._analyze()
        except Exception as e:
            print(f"Failed to run benchmark: {e}")
            raise e
        finally:
            # keep the metric collector running if user wants to keep vllm server running. for debugging purpose
            if self.metric_collector and not args.skip_server:
                self.metric_collector.stop()
        # Save config and results to json

        return benchmark_result

        def stop_test(self, test_id):
            """
            Stop a load test with the given test ID.
            
            :param test_id: ID of the test to stop
            """
            # Implement the logic to stop the load test
            print(f"Stopping load test with ID {test_id}.")
            # Add your load testing logic here

        def get_test_status(self, test_id):
            """
            Get the status of a load test with the given test ID.
            
            :param test_id: ID of the test to get status
            """
            # Implement the logic to get the status of the load test
            print(f"Getting status for load test with ID {test_id}.")

    def process_and_save_results(self, args, max_concurrency, backend, model_id, tokenizer_id, benchmark_result):
        if args.save_result:
            result_json: Dict[str, Any] = {}

            # Setup
            current_dt = datetime.now().strftime("%Y%m%d-%H%M%S")
            result_json["date"] = current_dt
            result_json["backend"] = backend
            result_json["model_id"] = model_id
            result_json["tokenizer_id"] = tokenizer_id
            result_json["best_of"] = args.best_of
            result_json["num_prompts"] = args.num_prompts

            # Metadata
            if args.metadata:
                for item in args.metadata:
                    if "=" in item:
                        kvstring = item.split("=")
                        result_json[kvstring[0].strip()] = kvstring[1].strip()
                    else:
                        raise ValueError(
                            "Invalid metadata format. Please use KEY=VALUE format."
                        )

            # Traffic
            result_json["request_rate"] = (
                args.request_rate if args.request_rate < float("inf") else "inf")
            result_json["burstiness"] = args.burstiness
            result_json["max_concurrency"] = max_concurrency
            

            # Merge with benchmark result
            result_json = { **benchmark_result,**result_json}

            # Save to file
            base_model_id = model_id.split("/")[-1]
            max_concurrency_str = (f"-concurrency{max_concurrency}"
                                if max_concurrency is not None else "")
            file_name = f"{backend}-{args.request_rate}qps{max_concurrency_str}-{base_model_id}-{current_dt}.json"  #noqa
            if args.result_filename:
                file_name = args.result_filename
            if args.result_dir:
                file_name = os.path.join(args.result_dir, file_name)
            with open(file_name, "w", encoding='utf-8') as outfile:
                json.dump(result_json, outfile)
            # Add your load testing logic here




@dataclass
class BenchmarkMetrics:
    completed: int
    total_input: int
    total_output: int
    request_throughput: float
    request_goodput: float
    output_throughput: float
    total_token_throughput: float
    mean_input_token_len: int
    median_input_token_len: int
    std_input_token_len: int
    percentiles_input_token_len: List[Tuple[float, int]]
    mean_output_token_len: int
    median_output_token_len: int
    std_output_token_len: int
    percentiles_output_token_len: List[Tuple[float, int]]
    mean_fs_token_len: int
    median_fs_token_len: int
    std_fs_token_len: int
    percentiles_fs_token_len: List[Tuple[float, int]]
    percentiles_input_token_len: List[Tuple[float, int]]
    mean_ttft_ms: float
    median_ttft_ms: float
    std_ttft_ms: float
    percentiles_ttft_ms: List[Tuple[float, float]]
    mean_ttfs_ms: float
    median_ttfs_ms: float
    std_ttfs_ms: float
    percentiles_ttfs_ms: List[Tuple[float, float]]
    mean_tpot_ms: float
    median_tpot_ms: float
    std_tpot_ms: float
    percentiles_tpot_ms: List[Tuple[float, float]]
    mean_itl_ms: float
    median_itl_ms: float
    std_itl_ms: float
    percentiles_itl_ms: List[Tuple[float, float]]
    # E2EL stands for end-to-end latency per request.
    # It is the time taken on the client side from sending
    # a request to receiving a complete response.
    mean_e2el_ms: float
    median_e2el_ms: float
    std_e2el_ms: float
    percentiles_e2el_ms: List[Tuple[float, float]]


def sample_mmmu_pro_vision_requests(
    dataset,
    num_requests: int,
    tokenizer,
    fixed_output_len: Optional[int] = None,
) -> List[Tuple[str, str, int, Optional[Dict[str, Collection[str]]]]]:
    sampled_requests: List[Tuple[str, int, int, Dict[str,
                                                     Collection[str]]]] = []
    for data in dataset:
        if len(sampled_requests) == num_requests:
            break

        # MMMU-Pro vision direct prompt
        # Ref: https://github.com/MMMU-Benchmark/MMMU/blob/6ce42f4d8f70c1841c67867152648974415b5cac/mmmu-pro/prompts.yaml#L5
        prompt = (
            "Answer with the option letter from the given choices directly. "
            "The last line of your response should be of the following "
            "format: 'Answer: $LETTER' (without quotes) where LETTER is one of "
            "options.")

        prompt_token_ids = tokenizer(prompt).input_ids
        if fixed_output_len is None:
            # Default max output len is set to 128
            print("--hf-output-len is not provided. Using default value 128.")
            fixed_output_len = 128

        prompt_len = len(prompt_token_ids)
        output_len = fixed_output_len

        assert isinstance(
            data["image"],
            Image), ("Input image format must be `PIL.Image.Image`, "
                     f"given {type(data['image'])}.")
        image: Image = data["image"]
        image = image.convert("RGB")
        image_data = io.BytesIO()
        image.save(image_data, format='JPEG')
        image_base64 = base64.b64encode(image_data.getvalue()).decode("utf-8")
        mm_content = {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_base64}"
            },
        }

        sampled_requests.append((prompt, prompt_len, output_len, mm_content))

    return sampled_requests


def sample_anc_requests_openai_chat(
    dataset_path: str,
    num_requests: int,
    fixed_output_len: int,
) -> List[Tuple[str, int, int, Dict]]:
    supported_formats = ['.jsonl']
    _, file_extension = os.path.splitext(dataset_path)
    if not file_extension.lower() in supported_formats:
        raise ValueError(f"Unsupported dataset format: {dataset_path}. Supported Format: {supported_formats}")
    if file_extension == '.jsonl':
        # Initialize dataset and processor
        dataset = JsonlDataset(dataset_path)

        selected_ids = random.choices(range(len(dataset)), k=num_requests)
        print(f'selected_ids: {selected_ids}')
        processed_data = []
        for id in selected_ids:

            messages = dataset[id]['messages']
            if messages[-1]['role'] == 'assistant':
                messages.pop()
                
            processed_data.append([messages, None, fixed_output_len, None])

    return processed_data

def sample_anc_requests(
    dataset_path: str,
    num_requests: int,
    tokenizer,
    processor_class: Processor = None,
    fixed_output_len: Optional[int] = None,
    multi_turn: bool = False,
) -> List[Tuple[str, int, int, Dict]]:
    supported_formats = ['.jsonl']
    _, file_extension = os.path.splitext(dataset_path)
    if not file_extension.lower() in supported_formats:
        raise ValueError(f"Unsupported dataset format: {dataset_path}. Supported Format: {supported_formats}")
    
    if file_extension == '.jsonl':
        # Initialize dataset and processor
        dataset = JsonlDataset(dataset_path)
        processor = processor_class() if processor_class else MultiDialogProcessor()
        
        # Process and organize conversations
        conversation_groups = {}
        
        for idx in range(len(dataset)):
            item = dataset[idx]
            if idx==0:
                print(f'item: {item}')
            
            if isinstance(item, dict):
                if 'messages' in item:
                    messages = item['messages']
                else:
                    raise ValueError(f"Unsupported dataset format: {dataset_path}")
            else:
                messages = item
            
            transformed = processor.transform(messages)
            for data in transformed:
                prompt = data.get("prompt")
                output_len = data.get("output_len", fixed_output_len)
                conversation_id = data.get("conversation_id")
                turn_index = data.get("turn_index", 0)

                prompt_token_ids = tokenizer(prompt).input_ids
                prompt_len = len(prompt_token_ids)
                
                # Group by conversation ID
                if conversation_id not in conversation_groups:
                    conversation_groups[conversation_id] = []
                    
                # Store with metadata
                conversation_groups[conversation_id].append({
                    "prompt": prompt,
                    "prompt_len": prompt_len,
                    "output_len": output_len,
                    "turn_index": turn_index,
                    "conversation_id": conversation_id
                })
        
        # Sort each conversation by turn index
        for conv_id in conversation_groups:
            conversation_groups[conv_id].sort(key=lambda x: x["turn_index"])
        
        # Select a subset of conversations if needed
        if multi_turn:
            # we will send each prmopt in multi-turn conversations in order. num_requests is the total number of conversations
            conv_ids = list(conversation_groups.keys())
            selected_ids = random.choices(conv_ids, k=num_requests)
            conversation_groups = {conv_id: conversation_groups[conv_id] 
                                  for conv_id in selected_ids}
        
        # Flatten for processing but keep metadata

            processed_data = flatten_data(conversation_groups)

        else:
            # we will randomly pickup a single prompt in a random conversations, num_requests is the total number of prompts
            processed_data = flatten_data(conversation_groups, only_use_last_turn=True)
            selected_ids = random.choices(range(len(processed_data)), k=num_requests)
            processed_data = [processed_data[i] for i in selected_ids]
    
    print(f'total number of prompts: {len(processed_data)}')
    
    return processed_data

def flatten_data(conversation_groups, only_use_last_turn: bool = False):
    processed_data = []
    for conv_id, turns in conversation_groups.items():
        if only_use_last_turn:
            turns = turns[-1:]
        for turn in turns:
            processed_data.append((
                        turn["prompt"],
                        turn["prompt_len"],
                        turn["output_len"],
                        None
                    ))
    return processed_data

def sample_hf_requests(
    dataset_path: str,
    dataset_subset: str,
    dataset_split: str,
    num_requests: int,
    tokenizer,
    random_seed: int,
    fixed_output_len: Optional[int] = None,
) -> List[Tuple[str, str, int, Optional[Dict[str, Collection[str]]]]]:

    # Special case for MMMU-Pro vision dataset
    if dataset_path == 'MMMU/MMMU_Pro' and dataset_subset == 'vision':
        assert dataset_split == "test"
        dataset = load_dataset(dataset_path,
                               name=dataset_subset,
                               split=dataset_split,
                               streaming=True)
        assert "image" in dataset.features, (
            "MMMU/MMMU_Pro vision dataset must have 'image' column.")
        filter_func = lambda x: isinstance(x["image"], Image)
        dataset = dataset.shuffle(seed=random_seed).filter(filter_func)
        return sample_mmmu_pro_vision_requests(dataset, num_requests,
                                               tokenizer, fixed_output_len)

    dataset = load_dataset(dataset_path,
                           name=dataset_subset,
                           split=dataset_split,
                           streaming=True)
    assert "conversations" in dataset.features, (
        "HF Dataset must have 'conversations' column.")
    filter_func = lambda x: len(x["conversations"]) >= 2
    filtered_dataset = dataset.shuffle(seed=random_seed).filter(filter_func)
    sampled_requests: List[Tuple[str, int, int, Dict[str,
                                                     Collection[str]]]] = []
    for data in filtered_dataset:
        if len(sampled_requests) == num_requests:
            break

        # Tokenize the prompts and completions.
        prompt = data["conversations"][0]["value"]
        prompt_token_ids = tokenizer(prompt).input_ids
        completion = data["conversations"][1]["value"]
        completion_token_ids = tokenizer(completion).input_ids
        prompt_len = len(prompt_token_ids)
        output_len = len(completion_token_ids
                         ) if fixed_output_len is None else fixed_output_len
        if fixed_output_len is None and (prompt_len < 4 or output_len < 4):
            # Prune too short sequences.
            continue
        if fixed_output_len is None and \
            (prompt_len > 1024 or prompt_len + output_len > 2048):
            # Prune too long sequences.
            continue

        if "image" in data and isinstance(data["image"], Image):
            image: Image = data["image"]
            image = image.convert("RGB")
            image_data = io.BytesIO()
            image.save(image_data, format='JPEG')
            image_base64 = base64.b64encode(
                image_data.getvalue()).decode("utf-8")
            mm_content = {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_base64}"
                },
            }
        elif "image" in data and isinstance(data["image"], str):
            if (data["image"].startswith("http://") or \
                data["image"].startswith("file://")):
                image_url = data["image"]
            else:
                image_url = f"file://{data['image']}"

            mm_content = {
                "type": "image_url",
                "image_url": {
                    "url": image_url
                },
            }
        else:
            mm_content = None

        sampled_requests.append((prompt, prompt_len, output_len, mm_content))

    return sampled_requests


def sample_random_requests(
    prefix_len: int,
    input_len: int,
    output_len: int,
    num_prompts: int,
    range_ratio: float,
    tokenizer,
) -> List[Tuple[str, int, int]]:
    prefix_token_ids = np.random.randint(0,
                                         tokenizer.vocab_size,
                                         size=prefix_len).tolist()

    input_lens = np.random.randint(
        int(input_len * range_ratio),
        input_len + 1,
        size=num_prompts,
    )
    output_lens = np.random.randint(
        int(output_len * range_ratio),
        output_len + 1,
        size=num_prompts,
    )
    offsets = np.random.randint(0, tokenizer.vocab_size, size=num_prompts)
    input_requests = []
    for i in range(num_prompts):
        input_ids = prefix_token_ids + [(offsets[i] + i + j) % tokenizer.vocab_size for j in range(input_lens[i])] 
        # input_ids =[i for i in range(input_lens[i])]
        input_requests.append((input_ids, int(prefix_len + input_lens[i]),
                               int(output_lens[i]), None))

    return input_requests


async def get_request(
    input_requests: List[Tuple[str, int, int]],
    request_rate: float,
    burstiness: float = 1.0,
) -> AsyncGenerator[Tuple[str, int, int], None]:
    """
    Asynchronously generates requests at a specified rate 
    with OPTIONAL burstiness.
    
    Args:
        input_requests: 
            A list of input requests, each represented as a tuple.
        request_rate: 
            The rate at which requests are generated (requests/s).
        burstiness (optional): 
            The burstiness factor of the request generation. 
            Only takes effect when request_rate is not inf.
            Default value is 1, which follows a Poisson process.
            Otherwise, the request intervals follow a gamma distribution.
            A lower burstiness value (0 < burstiness < 1) results 
            in more bursty requests, while a higher burstiness value 
            (burstiness > 1) results in a more uniform arrival of requests.
    """
    input_requests = iter(input_requests)

    # Calculate scale parameter theta to maintain the desired request_rate.
    assert burstiness > 0, (
        f"A positive burstiness factor is expected, but given {burstiness}.")
    theta = 1.0 / (request_rate * burstiness)

    for request in input_requests:
        yield request

        if request_rate == float("inf"):
            # If the request rate is infinity, then we don't need to wait.
            continue

        # Sample the request interval from the gamma distribution.
        # If burstiness is 1, it follows exponential distribution.
        interval = np.random.gamma(shape=burstiness, scale=theta)
        # The next request will be sent after the interval.
        await asyncio.sleep(interval)


def calculate_metrics(
    input_requests: List[Tuple[str, int, int]],
    outputs: List[RequestFuncOutput],
    dur_s: float,
    tokenizer,
    selected_percentile_metrics: List[str],
    selected_percentiles: List[float],
    gootput_config_dict: Dict[str, float],
) -> Tuple[BenchmarkMetrics, List[int]]:
    input_lens: List[int] = []
    actual_output_lens: List[int] = []
    actual_input_lens: List[int] = []
    actual_first_sentence_lens: List[int] = []
    total_input = 0
    completed = 0
    good_completed = 0
    itls: List[float] = []
    tpots: List[float] = []
    all_tpots: List[float] = []
    ttfts: List[float] = []
    ttfss: List[float] = []
    e2els: List[float] = []
    for i in range(len(outputs)):
        if outputs[i].success:
            # We use the tokenizer to count the number of output tokens for all
            # serving backends instead of looking at len(outputs[i].itl) since
            # multiple output tokens may be bundled together
            # Note : this may inflate the output token count slightly
            if outputs[i].input_token_len:
                actual_input_lens.append(outputs[i].input_token_len) # currently only available for openai completions  
            else:
                actual_input_lens.append(input_requests[i][1])
            input_len = outputs[i].input_token_len if outputs[i].input_token_len else input_requests[i][1]
            if outputs[i].output_token_len:
                output_len = outputs[i].output_token_len
            else:
                print(f'warning, output_token_len is not found for {input_requests[i][0]}, will use tokenizer to count the number of output tokens')
                output_len = len(
                    tokenizer(outputs[i].generated_text,
                          add_special_tokens=False).input_ids)
            
            actual_input_lens.append(input_len)
            actual_output_lens.append(output_len)
            
             
            first_sentence_len = len(
                tokenizer(outputs[i].first_sentence_text,
                          add_special_tokens=False).input_ids)
            actual_first_sentence_lens.append(first_sentence_len)
            
            # TODO: figure out why sometimes input_len is None: for anc data, soemtimes outputs[i].input_token_len is still None
            total_input += input_len if input_len else 0
            tpot = 0
            if output_len > 1:
                tpot = (outputs[i].latency - outputs[i].ttft) / (output_len -
                                                                 1)
                tpots.append(tpot)
            # Note: if output_len <= 1, we regard tpot as 0 for goodput
            all_tpots.append(tpot)
            itls += outputs[i].itl
            ttfts.append(outputs[i].ttft)
            ttfss.append(outputs[i].ttfs)
            e2els.append(outputs[i].latency)
            completed += 1
        else:
            input_lens.append(0)
            actual_output_lens.append(0)
            actual_first_sentence_lens.append(0)

    if gootput_config_dict:
        valid_metrics = []
        slo_values = []

        if "ttft" in gootput_config_dict:
            valid_metrics.append(ttfts)
            slo_values.append(gootput_config_dict["ttft"] /
                              MILLISECONDS_TO_SECONDS_CONVERSION)
        if "ttfs" in gootput_config_dict:
            valid_metrics.append(ttfss)
            slo_values.append(gootput_config_dict["ttfs"] /
                              MILLISECONDS_TO_SECONDS_CONVERSION)
        if "tpot" in gootput_config_dict:
            valid_metrics.append(all_tpots)
            slo_values.append(gootput_config_dict["tpot"] /
                              MILLISECONDS_TO_SECONDS_CONVERSION)
        if "e2el" in gootput_config_dict:
            valid_metrics.append(e2els)
            slo_values.append(gootput_config_dict["e2el"] /
                              MILLISECONDS_TO_SECONDS_CONVERSION)

        for req_metric in zip(*valid_metrics):
            is_good_req = all([s >= r for s, r in zip(slo_values, req_metric)])
            if is_good_req:
                good_completed += 1

    if completed == 0:
        warnings.warn(
            "All requests failed. This is likely due to a misconfiguration "
            "on the benchmark arguments.",
            stacklevel=2)
    metrics = BenchmarkMetrics(
        completed=completed,
        total_input=total_input,
        total_output=sum(actual_output_lens),
        request_throughput=completed / dur_s,
        request_goodput=good_completed / dur_s,
        output_throughput=sum(actual_output_lens) / dur_s,
        total_token_throughput=(total_input + sum(actual_output_lens)) / dur_s,
        mean_input_token_len=np.mean(actual_input_lens or 0),
        median_input_token_len=np.median(actual_input_lens or 0),
        std_input_token_len=np.std(actual_input_lens or 0),
        percentiles_input_token_len=[(p, np.percentile(actual_input_lens or 0, p))
                             for p in selected_percentiles], 
        mean_output_token_len=np.mean(actual_output_lens or 0),
        median_output_token_len=np.median(actual_output_lens or 0),
        std_output_token_len=np.std(actual_output_lens or 0),
        percentiles_output_token_len=[(p, np.percentile(actual_output_lens or 0, p))
                             for p in selected_percentiles], 
        mean_fs_token_len=np.mean(actual_first_sentence_lens or 0),
        median_fs_token_len=np.median(actual_first_sentence_lens or 0),
        std_fs_token_len=np.std(actual_first_sentence_lens or 0),
        percentiles_fs_token_len=[(p, np.percentile(actual_first_sentence_lens or 0, p))
                             for p in selected_percentiles], 
        mean_ttft_ms=np.mean(ttfts or 0) *
        1000,  # ttfts is empty if streaming is not supported by backend
        std_ttft_ms=np.std(ttfts or 0) * 1000,
        median_ttft_ms=np.median(ttfts or 0) * 1000,
        percentiles_ttft_ms=[(p, np.percentile(ttfts or 0, p) * 1000)
                             for p in selected_percentiles],
        mean_ttfs_ms=np.mean(ttfss or 0) *
        1000,  # ttfss is empty if streaming is not supported by backend
        std_ttfs_ms=np.std(ttfss or 0) * 1000,
        median_ttfs_ms=np.median(ttfss or 0) * 1000,
        percentiles_ttfs_ms=[(p, np.percentile(ttfss or 0, p) * 1000)
                             for p in selected_percentiles],
        mean_tpot_ms=np.mean(tpots or 0) * 1000,
        std_tpot_ms=np.std(tpots or 0) * 1000,
        median_tpot_ms=np.median(tpots or 0) * 1000,
        percentiles_tpot_ms=[(p, np.percentile(tpots or 0, p) * 1000)
                             for p in selected_percentiles],
        mean_itl_ms=np.mean(itls or 0) * 1000,
        std_itl_ms=np.std(itls or 0) * 1000,
        median_itl_ms=np.median(itls or 0) * 1000,
        percentiles_itl_ms=[(p, np.percentile(itls or 0, p) * 1000)
                            for p in selected_percentiles],
        mean_e2el_ms=np.mean(e2els or 0) * 1000,
        std_e2el_ms=np.std(e2els or 0) * 1000,
        median_e2el_ms=np.median(e2els or 0) * 1000,
        percentiles_e2el_ms=[(p, np.percentile(e2els or 0, p) * 1000)
                             for p in selected_percentiles],
    )

    return metrics, actual_output_lens, actual_first_sentence_lens, actual_input_lens


async def benchmark(
    backend: str,
    api_url: str,
    base_url: str,
    model_id: str,
    tokenizer,
    input_requests: List[Tuple[str, int, int, Dict]],
    logprobs: Optional[int],
    best_of: int,
    request_rate: float,
    burstiness: float,
    disable_tqdm: bool,
    profile: bool,
    selected_percentile_metrics: List[str],
    selected_percentiles: List[str],
    ignore_eos: bool,
    gootput_config_dict: Dict[str, float],
    max_concurrency: Optional[int],
    num_warmup_requests: int = 1,
):
    if backend in ASYNC_REQUEST_FUNCS:
        request_func = ASYNC_REQUEST_FUNCS[backend]
    else:
        raise ValueError(f"Unknown backend: {backend}")

    # Test run with first input
    print("Starting initial single prompt test run...")
    test_prompt, test_prompt_len, test_output_len, test_mm_content = (
        input_requests[0])
    if backend != "openai-chat" and test_mm_content is not None:
        # multi-modal benchmark is only available on OpenAI Chat backend.
        raise ValueError(
            "Multi-modal content is only supported on 'openai-chat' backend.")
    test_input = RequestFuncInput(
        model=model_id,
        prompt=test_prompt,
        api_url=api_url,
        prompt_len=test_prompt_len,
        output_len=test_output_len,
        logprobs=logprobs,
        best_of=best_of,
        multi_modal_content=test_mm_content,
        ignore_eos=ignore_eos,
    )
    # test_output = await request_func(request_func_input=test_input)
    # if not test_output.success:
    #     raise ValueError(
    #         "Initial test run failed - Please make sure benchmark arguments "
    #         f"are correctly specified. Error: {test_output.error}")
    # else:
    #     print("Initial test run completed. Starting main benchmark run...")

    if profile:
        print("Starting profiler...")
        profile_input = RequestFuncInput(model=model_id,
                                         prompt=test_prompt,
                                         api_url=base_url + "/start_profile",
                                         prompt_len=test_prompt_len,
                                         output_len=test_output_len,
                                         logprobs=logprobs,
                                         best_of=best_of,
                                         multi_modal_content=test_mm_content,
                                         ignore_eos=ignore_eos)
        profile_output = await request_func(request_func_input=profile_input)
        if profile_output.success:
            print("Profiler started")


    conversation_groups = {}
    for request in input_requests:
        prompt, prompt_len, output_len, metadata = request
        if metadata and "conversation_id" in metadata:
            conv_id = metadata["conversation_id"]
            if conv_id not in conversation_groups:
                conversation_groups[conv_id] = []
            conversation_groups[conv_id].append(request)
        else:
            # For non-conversation requests, treat as separate conversations
            conv_id = f"single_{time.time()}_{random.randint(0, 1000000)}"
            conversation_groups[conv_id] = [request]

    # Sort each conversation's requests by turn index
    for conv_id in conversation_groups:
        conversation_groups[conv_id].sort(
            key=lambda req: req[3].get("turn_index", 0) if req[3] else 0
        )
    # Create a semaphore for max concurrency
    semaphore = asyncio.Semaphore(max_concurrency) if max_concurrency else None

    # Function to process a single conversation
    async def process_conversation(conversation_requests, pbar=None):
        outputs = []
        for prompt, prompt_len, output_len, metadata in conversation_requests:
            request_func_input = RequestFuncInput(
                model=model_id,
                prompt=prompt,
                api_url=api_url,
                prompt_len=prompt_len,
                output_len=output_len,
                logprobs=logprobs,
                best_of=best_of,
                multi_modal_content=metadata.get("multi_modal_content") if metadata else None,
                ignore_eos=ignore_eos,
            )
            
            # Use semaphore if provided
            if semaphore:
                async with semaphore:
                    output = await request_func(request_func_input=request_func_input, 
                                               pbar=pbar)
            else:
                output = await request_func(request_func_input=request_func_input,
                                           pbar=pbar)
            outputs.append(output)
            await asyncio.sleep(0.1)
            return outputs, conversation_requests
    
    if burstiness == 1.0:
        distribution = "Poisson process"
    else:
        distribution = "Gamma distribution"

    print(f"Traffic request rate: {request_rate}")
    print(f"Burstiness factor: {burstiness} ({distribution})")
    print(f"Maximum request concurrency: {max_concurrency}")

    # Group requests by conversation ID
    conversation_ids = list(conversation_groups.keys())
    
    # Generate tasks based on request rate
    if num_warmup_requests > 0:
        warmup_tasks = []
        print(f"Processing {num_warmup_requests} warm up requests")
        warmup_ids = random.choices(conversation_ids, k=num_warmup_requests)
        for conv_id in warmup_ids:
            conversation = conversation_groups[conv_id]
            warmup_tasks.append(asyncio.create_task(process_conversation(conversation)))
        await asyncio.gather(*warmup_tasks)
   
   
   
    print(f"Processing {len(input_requests) } requests")
    benchmark_start_time = time.perf_counter()
    pbar = None if disable_tqdm else tqdm(total=len(input_requests))
    
    tasks = []
    # Create tasks at the specified rate

    if request_rate == float("inf"):
        # Start all conversations at once
        for conv_id in conversation_ids:
            conversation = conversation_groups[conv_id]
            tasks.append(asyncio.create_task(process_conversation(conversation, pbar)))
    else:
        # Start conversations at specified rate
        async def launch_conversations():
            for i, conv_id in enumerate(conversation_ids):
                conversation = conversation_groups[conv_id]
                tasks.append(asyncio.create_task(process_conversation(conversation, pbar)))
                
                if i < len(conversation_ids) - 1:  # Don't wait after the last one
                    # Sample interval based on request rate and burstiness
                    if burstiness == 1.0:
                        # Poisson process - exponential intervals
                        interval = np.random.exponential(1.0 / request_rate)
                    else:
                        # Gamma distribution for controlled burstiness
                        theta = 1.0 / (request_rate * burstiness)
                        interval = np.random.gamma(shape=burstiness, scale=theta)
                    
                    await asyncio.sleep(interval)
        
        await launch_conversations()
    
    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks)

    # Flatten the results for metrics calculation
    all_outputs = []
    all_requests = []
    for outputs, requests in results:
        all_outputs.extend(outputs)
        all_requests.extend(requests)
    
    if pbar:
        pbar.close()
    
    benchmark_duration = time.perf_counter() - benchmark_start_time
    
    # Calculate metrics (ensure the order matches between requests and outputs)
    metrics, actual_output_lens, first_sentence_lens, actual_input_lens = calculate_metrics(
        input_requests=all_requests,
        outputs=all_outputs,
        dur_s=benchmark_duration,
        tokenizer=tokenizer,
        selected_percentile_metrics=selected_percentile_metrics,
        selected_percentiles=selected_percentiles,
        gootput_config_dict=gootput_config_dict,
    )
    
    print("{s:{c}^{n}}".format(s=' Serving Benchmark Result ', n=50, c='='))
    print("{:<40} {:<10}".format("Successful requests:", metrics.completed))
    print("{:<40} {:<10.2f}".format("Benchmark duration (s):",
                                    benchmark_duration))
    print("{:<40} {:<10}".format("Total input tokens:", metrics.total_input))
    print("{:<40} {:<10}".format("Total generated tokens:",
                                 metrics.total_output))
    print("{:<40} {:<10.2f}".format("Request throughput (req/s):",
                                    metrics.request_throughput))
    if gootput_config_dict:
        print("{:<40} {:<10.2f}".format("Request goodput (req/s):",
                                        metrics.request_goodput))
    print("{:<40} {:<10.2f}".format("Output token throughput (tok/s):",
                                    metrics.output_throughput))
    print("{:<40} {:<10.2f}".format("Total Token throughput (tok/s):",
                                    metrics.total_token_throughput))

    result = {
        "duration": benchmark_duration,
        "completed": metrics.completed,
        "total_input_tokens": metrics.total_input,
        "total_output_tokens": metrics.total_output,
        "request_throughput": metrics.request_throughput,
        "request_goodput:":
        metrics.request_goodput if gootput_config_dict else None,
        "output_throughput": metrics.output_throughput,
        "total_token_throughput": metrics.total_token_throughput,
        "input_lens": actual_input_lens,
        "output_lens": actual_output_lens,
        "first_sentence_lens": first_sentence_lens,
        "ttfts": [output.ttft for output in all_outputs],
        "ttfss": [output.ttfs for output in all_outputs],
        # "itls": [output.itl for output in all_outputs],
        "generated_texts": [output.generated_text for output in all_outputs],
        "first_sentence_texts": [output.first_sentence_text for output in all_outputs],
        "e2els": [output.latency for output in all_outputs],
        "errors": [output.error for output in all_outputs],
    }

    def process_one_metric(
        # E.g., "ttft"
        metric_attribute_name: str,
        # E.g., "TTFT"
        metric_name: str,
        # E.g., "Time to First Token"
        metric_header: str,
        # E.g., "ms"
        metric_unit: str,
    ):
        # This function prints and adds statistics of the specified
        # metric.
        if metric_attribute_name not in selected_percentile_metrics:
            return
        print("{s:{c}^{n}}".format(s=metric_header, n=50, c='-'))
        print("{:<40} {:<10.2f}".format(
            f"Mean {metric_name} ({metric_unit}):",
            getattr(metrics, f"mean_{metric_attribute_name}_{metric_unit}")))
        print("{:<40} {:<10.2f}".format(
            f"Median {metric_name} ({metric_unit}):",
            getattr(metrics, f"median_{metric_attribute_name}_{metric_unit}")))
        result[f"mean_{metric_attribute_name}_{metric_unit}"] = getattr(
            metrics, f"mean_{metric_attribute_name}_{metric_unit}")
        result[f"median_{metric_attribute_name}_{metric_unit}"] = getattr(
            metrics, f"median_{metric_attribute_name}_{metric_unit}")
        result[f"std_{metric_attribute_name}_{metric_unit}"] = getattr(
            metrics, f"std_{metric_attribute_name}_{metric_unit}")
        for p, value in getattr(metrics,
                                f"percentiles_{metric_attribute_name}_{metric_unit}"):
            p_word = str(int(p)) if int(p) == p else str(p)
            print("{:<40} {:<10.2f}".format(f"P{p_word} {metric_name} ({metric_unit}):",
                                            value))
            result[f"p{p_word}_{metric_attribute_name}_{metric_unit}"] = value

    process_one_metric("input_token", "Input Tokens", "Stats for Input Tokens Len", "len")
    process_one_metric("output_token", "Output Tokens", "Stats for Output Tokens Len", "len")
    process_one_metric("fs_token", "First Sentence Tokens", "Stats for First Sentence Tokens Len", "len")
    process_one_metric("ttfs", "TTFS", "Time to First Sentence", "ms")
    process_one_metric("ttft", "TTFT", "Time to First Token", "ms")
    process_one_metric("tpot", "TPOT",
                       "Time per Output Token (excl. 1st token)", "ms")
    process_one_metric("itl", "ITL", "Inter-token Latency", "ms")
    process_one_metric("e2el", "E2EL", "End-to-end Latency", "ms")

    print("=" * 50)

    return result


def check_goodput_args(args):
    # Check and parse goodput arguments
    gootput_config_dict = {}
    VALID_NAMES = ["ttft", "ttfs", "tpot", "e2el"]
    if args.goodput:
        gootput_config_dict = parse_goodput(args.goodput)
        for slo_name, slo_val in gootput_config_dict.items():
            if slo_name not in VALID_NAMES:
                raise ValueError(
                    f"Invalid metric name found, {slo_name}: {slo_val}. "
                    "The service level objective name should be one of "
                    f"{str(VALID_NAMES)}. ")
            if slo_val < 0:
                raise ValueError(
                    f"Invalid value found, {slo_name}: {slo_val}. "
                    "The service level objective value should be "
                    "non-negative.")
    return gootput_config_dict


def parse_goodput(slo_pairs):
    gootput_config_dict = {}
    try:
        for slo_pair in slo_pairs:
            slo_name, slo_val = slo_pair.split(":")
            gootput_config_dict[slo_name] = float(slo_val)
    except ValueError as err:
        raise argparse.ArgumentTypeError(
            "Invalid format found for service level objectives. "
            "Specify service level objectives for goodput as \"KEY:VALUE\" "
            "pairs, where the key is a metric name, and the value is a "
            "number in milliseconds.") from err
    return gootput_config_dict


