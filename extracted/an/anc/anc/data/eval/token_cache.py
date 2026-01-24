import json
import os
import argparse

from anc.data.parquet_dataset import ParquetDataset
from anc.data.jsonl_dataset import JsonlDataset

from transformers import AutoTokenizer
import concurrent.futures


def process_batch(ds_path, start_idx, end_idx, tokenizer_path, is_parquet):
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

    if is_parquet:
        ds = ParquetDataset(ds_path)
    else:
        ds = JsonlDataset(ds_path)

    tokens = 0
    for i in range(start_idx, end_idx):
        item = ds[i]
        if is_parquet:
            tokens += len(tokenizer.encode(item['content']))
        else:
            if 'text' in item:
                tokens += len(tokenizer.encode(item['text']))
                continue
            elif 'messages' not in item:
                continue
            text = ' '.join([f"{msg.get('role', '')} {msg.get('content', '')}" for msg in item['messages']])
            tokens += len(tokenizer.encode(text))
    return tokens

def get_token_count_unified(ds_path, tokenizer_path):
    try:
        if ds_path.endswith('.parquet'):
            ds = ParquetDataset(ds_path)
            print(f"Processing {ds_path} as parquet length: {len(ds)}")
            is_parquet = True
        elif ds_path.endswith('.jsonl'):
            ds = JsonlDataset(ds_path)
            print(f"Processing {ds_path} as jsonl length: {len(ds)}")
            is_parquet = False
        else:
            print(f"Unsupported file type: {ds_path}, just skip it")
            return 0

        total_items = len(ds)
        tokens = 0

        if total_items > 5000:
            batch_size = max(1000, total_items // 16)
            max_workers = min(16, (os.cpu_count() or 4))
            # void GIL issue, use ProcessPoolExecutor instead of ThreadPoolExecutor
            with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
                futures = []
                for i in range(0, total_items, batch_size):
                    start_idx = i
                    end_idx = min(i + batch_size, total_items)
                    print(f"Dispatching batch: {start_idx} - {end_idx}")
                    futures.append(executor.submit(
                        process_batch,
                        ds_path,
                        start_idx,
                        end_idx,
                        tokenizer_path,
                        is_parquet
                    ))

                for future in concurrent.futures.as_completed(futures):
                    tokens += future.result()
        else:
            tokens = process_batch(ds_path, 0, total_items, tokenizer_path, is_parquet)

        print(f"Processed {ds_path}: {tokens} tokens")
        return tokens

    except Exception as e:
        print(f"Error processing {ds_path}: {e}")
        return 0

def get_dataset_paths(path, dataset_role):
    dataset_paths = []
    # for only one dataset, the path is the dataset path
    if os.path.isdir(path) and dataset_role in os.listdir(path):
        dataset_paths.append(path)
        return dataset_paths

    # for all datasets, so add all subdirectories as dataset paths
    subdirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    for subdir in subdirs:
        subdir_path = os.path.join(path, subdir)
        dataset_paths.extend(get_dataset_paths(subdir_path, dataset_role))

    return dataset_paths


def count_tokens(dataset_dir, tokenizer_path, dataset_role, max_workers=6):
    role_dir = os.path.join(dataset_dir, dataset_role)

    if not os.path.exists(role_dir):
        print(f"Eval directory not found in {dataset_dir}")
        return 0

    files = []
    for file in os.listdir(role_dir):
        if file.endswith('.parquet') or file.endswith('.jsonl'):
            files.append(os.path.join(role_dir, file))

    if not files:
        print(f"No parquet or json files found in {role_dir}")
        return 0

    print(f"Found {len(files)} files in {role_dir}")

    total_tokens = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_path = {
            executor.submit(get_token_count_unified, path, tokenizer_path): path 
            for path in files
        }
        for future in concurrent.futures.as_completed(future_to_path):
            path = future_to_path[future]
            try:
                token_count = future.result()
                total_tokens += token_count
                print(f"Processed {path}: {token_count} tokens")
            except Exception as e:
                print(f"Error processing {path}: {e}")

    return total_tokens


# Process all eval dataset token count and dump to json file [offline use only].
#   a. If the key of tokenizer in json file, read the token count from the json file.
#   b. If the key of tokenizer not in json file, calculate the token count and dump to the json file.
#   c. For the eval dataset, the token count is the sum of all the token count of the parquet files in the eval folder. 
def process_all_datasets(dataset_list, tokenizer_path, dataset_role, force_recalc=False):
    results = {}

    for dataset_dir in dataset_list:
        dataset_name = os.path.basename(dataset_dir)
        print(f"\nProcessing dataset: {dataset_name}")
        
        dataset_role_dir = os.path.join(dataset_dir, dataset_role)
        if os.path.exists(dataset_role_dir) and not force_recalc:
            json_path = os.path.join(dataset_role_dir, "token_count.json")
            if os.path.exists(json_path):
                try:
                    with open(json_path, 'r') as f:
                        existing_data = json.load(f)
                    if tokenizer_path in existing_data:
                        token_count = existing_data[tokenizer_path]
                        if token_count == 0:
                            print(f"Warning: token count is 0 for {dataset_name}, will calculate it again")
                        else:
                            print(f"Using existing token count for {dataset_name}: {token_count}")
                            results[dataset_dir] = token_count
                            continue
                except Exception as e:
                    print(f"Error reading existing JSON: {e}")

        token_count = count_tokens(dataset_dir, tokenizer_path, dataset_role)
        results[dataset_dir] = token_count

        if os.path.exists(dataset_role_dir):
            json_path = os.path.join(dataset_role_dir, "token_count.json")

            existing_data = {}
            if os.path.exists(json_path):
                try:
                    with open(json_path, 'r') as f:
                        existing_data = json.load(f)
                    print(f"Found existing token count file at {json_path}")
                except json.JSONDecodeError:
                    print(f"Waring: reading existing JSON file {json_path}, will create new one")

            existing_data[tokenizer_path] = token_count
            
            with open(json_path, 'w') as f:
                json.dump(existing_data, f, indent=2)
            print(f"Updated token count at {json_path}")

    print("\n===== Token Count Summary =====")
    for dataset_dir, count in results.items():
        print(f"{os.path.basename(dataset_dir)}: {count} tokens")

    return results


# Online use.
def get_num_iterations_from_cache(file_dir, tokenizer_path, dataset_role):
    token_count = 0
    cached_dataset = 0
    dataset_paths = get_dataset_paths(file_dir, dataset_role)
    for dataset_path in dataset_paths:
        if os.path.exists(os.path.join(dataset_path, dataset_role, "token_count.json")):
            with open(os.path.join(dataset_path, dataset_role, "token_count.json"), 'r') as f:
                data = json.load(f)
                if tokenizer_path in data:
                    token_count += int(data.get(tokenizer_path, 0))
                    cached_dataset += 1
    return token_count, cached_dataset, len(dataset_paths)

# example:
# /mnt/project/llm/infra/playgroud/data contains train and eval
# -- /mnt/project/llm/infra/playgroud/data/eval
# -- /mnt/project/llm/infra/playgroud/data/train
#
# python3 token_cache_pretrain.py --dataset_role train  --file_dir /mnt/project/llm/data/posttrain/xug_v0/test --tokenizer_path /mnt/project/llm/ckpt/tokenizer/ocean_deepseek_v2

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process eval datasets and count tokens")
    parser.add_argument("--file_dir", type=str, 
                       default="/mnt/project/llm/infra/playgroud/data",
                       help="Dataset directory path")
    parser.add_argument("--tokenizer_path", type=str,
                       default="/mnt/project/llm/ckpt/tokenizer/ocean_deepseek_v2", 
                       help="Path to tokenizer")
    parser.add_argument("--max_workers", type=int, default=4,
                       help="Maximum number of worker threads")
    parser.add_argument("--global_batch_size", type=int, default=None,
                       help="Global batch size for iteration calculation")
    parser.add_argument("--seq_len", type=int, default=None,
                       help="Sequence length for iteration calculation")
    parser.add_argument("--dataset_role", type=str, default="eval", choices=["train", "eval"])
    parser.add_argument("--force", action='store_true', help="force re calculate iterations")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file_dir):
        raise FileNotFoundError(f"Dataset directory {args.file_dir} does not exist")
    
    dataset_paths = get_dataset_paths(args.file_dir, args.dataset_role)
    print(f"Found {len(dataset_paths)} dataset paths: {dataset_paths}")

    process_all_datasets(dataset_paths, args.tokenizer_path, args.dataset_role, args.force)