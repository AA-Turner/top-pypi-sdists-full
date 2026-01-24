import os
import io
import json
import mmap
import argparse
from typing import List, Tuple, Optional
from concurrent.futures import ProcessPoolExecutor, as_completed
from collections import defaultdict

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

from transformers import AutoTokenizer

def make_line_aligned_chunks(path: str, chunk_bytes: int) -> List[Tuple[int, int]]:
    file_path = []
    # for single file
    if not os.path.isdir(path):
        file_path.append(path)
    else: 
        # for directory
        for entry in sorted(os.scandir(path), key=lambda e: e.name):
            if entry.is_file():
                file_path.append(entry.path)
    
    #file_to_range = defaultdict(list)
    chunks = defaultdict(list)
    for one_file in file_path:
        size = os.path.getsize(one_file)
        with open(one_file, "rb") as f:
            start = 0
            while start < size:
                end = min(start + chunk_bytes, size)
                if end < size:
                    f.seek(end)
                    f.readline()
                    end = f.tell()
                    if end <= start:  # 极端情况下保护（比如没读到换行）
                        end = min(start + chunk_bytes, size)
                #chunks.append((start, end))
                chunks[one_file].append((start, end))
                start = end
    return chunks

def iter_lines_mmap(path: str, start: int, end: int, encoding="utf-8"):
    with open(path, "rb") as f, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
        mm.seek(start)
        while mm.tell() < end:
            bline = mm.readline()
            if not bline:
                break
            pos = mm.tell()
            if pos > end:
                break
            yield bline.decode(encoding, errors="ignore").rstrip("\n")

def extract_text_from_jsonl_line(line: str) -> Optional[str]:
    try:
        obj = json.loads(line)
    except Exception:
        return None, 0

    invalid_count = 0
    if 'text' in obj:
        return obj['text'], 0
    elif 'messages' in obj:
        if not all(turn['role'] and turn['content'] and type(turn['role']) is str and type(turn['content']) is str for turn in obj['messages']):
            return None, 1
        text = ' '.join([f"{msg.get('role', '')} {msg.get('content', '')}" for msg in obj['messages']])
    else:
        print("invalid line:", line[:20] + "...")
        return None, 1

    return text, invalid_count

def count_tokens_batch(tokenizer, texts, add_special_tokens=False) -> int:
    if not texts:
        return 0
    enc = tokenizer(
        texts,
        add_special_tokens=add_special_tokens,
        return_attention_mask=False,
        return_token_type_ids=False,
    )
    return sum(len(ids) for ids in enc["input_ids"])

def worker_count_slice(
    path: str,
    start: int,
    end: int,
    tokenizer_path: str,
    batch_size: int,
    add_special_tokens: bool,
    rayon_threads: int,
    encoding: str,
) -> int:
    if rayon_threads > 0:
        os.environ["RAYON_NUM_THREADS"] = str(rayon_threads)

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, use_fast=True)

    total = 0
    buf = []
    invalid_sample_count = 0
    for line in iter_lines_mmap(path, start, end, encoding=encoding):
        text, invalid = extract_text_from_jsonl_line(line)
        invalid_sample_count += invalid
        if not text:
            continue
        buf.append(text)
        if len(buf) >= batch_size:
            total += count_tokens_batch(tokenizer, buf, add_special_tokens)
            buf.clear()
    if buf:
        total += count_tokens_batch(tokenizer, buf, add_special_tokens)
        buf.clear()
    return total, invalid_sample_count

def count_tokens_jsonl_mmap_mp(
    path: str,
    tokenizer_path: str,
    workers: int = max(1, (os.cpu_count() or 8) // 2),
    chunk_bytes: int = 1 << 30,  # 1 GiB
    batch_size: int = 2048,
    add_special_tokens: bool = False,
    rayon_threads_per_proc: Optional[int] = None,
    encoding: str = "utf-8",
) -> int:
    chunks = make_line_aligned_chunks(path, chunk_bytes)
    chunk_num = sum(len(v) for v in chunks.values())
    print(f"Split to {chunk_num} chunks")
    if not chunks:
        return 0, 0
    workers = min(workers, chunk_num)

    cpu = os.cpu_count() or 8
    if rayon_threads_per_proc is None:
        rayon_threads_per_proc = max(1, cpu // max(1, workers))
    total_invalid_sample_count = 0
    total_tokens_count = 0
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = []
        for file_path, chunk_list in chunks.items():
            for s, e in chunk_list:
                futs.append(
                    ex.submit(
                        worker_count_slice,
                        file_path, 
                        s, 
                        e,
                        tokenizer_path,
                        batch_size,
                        add_special_tokens,
                        rayon_threads_per_proc,
                        encoding,
                    )
                )
        for fut in as_completed(futs):
            tokens_count, invalid_sample_count = fut.result()
            total_tokens_count += tokens_count
            total_invalid_sample_count += invalid_sample_count
    return total_tokens_count, total_invalid_sample_count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True, help="Path to the JSONL file")
    ap.add_argument("--tokenizer_path", required=True, help="Path/name to load with AutoTokenizer")
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 8)//2))
    ap.add_argument("--chunk_bytes", type=int, default=1<<30, help="Bytes per chunk (default: 1 GiB)")
    ap.add_argument("--batch_size", type=int, default=2048, help="Batch size for tokenization")
    ap.add_argument("--add_special_tokens", action="store_true", help="Include special tokens when counting")
    ap.add_argument("--rayon_threads_per_proc", type=int, default=None, help="Number of Rust (rayon) threads per process")
    ap.add_argument("--encoding", default="utf-8")
    ap.add_argument("--force", action='store_true', help="force re calculate iterations")
    ap.add_argument("--dataset_role", type=str, default="eval", choices=["train", "eval"])
    args = ap.parse_args()

    dataset_role_dir = os.path.join(args.path, args.dataset_role)
    if not os.path.isdir(dataset_role_dir):
        raise FileNotFoundError(f"Dataset directory {dataset_role_dir} does not exist")

    json_file = os.path.join(dataset_role_dir, "token_count.json")
    catched_data = {}
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            catched_data = json.load(f)
        
    if (
        args.tokenizer_path in catched_data 
        and catched_data[args.tokenizer_path] != 0 
        and not args.force
    ):
        print(f"Token count for tokenizer {args.tokenizer_path} already exists: {catched_data[args.tokenizer_path]}")
        return

    total, total_invalid_count = count_tokens_jsonl_mmap_mp(
        path=dataset_role_dir,
        tokenizer_path=args.tokenizer_path,
        workers=args.workers,
        chunk_bytes=args.chunk_bytes,
        batch_size=args.batch_size,
        add_special_tokens=args.add_special_tokens,
        rayon_threads_per_proc=args.rayon_threads_per_proc,
        encoding=args.encoding,
    )
    print(f"total token is {total} but has {total_invalid_count} invalid samples")

    catched_data[args.tokenizer_path] = total
    catched_data["invalid_sample_count"] = total_invalid_count
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(catched_data, f, ensure_ascii=False, indent=2)

#python3 utils.py --path /mnt/project/llm/data/posttrain/foundation/v1.4_exp5 --dataset_role train --tokenizer_path /mnt/project/minghao/ckpts/CPT_72b/model_name=0__val_loss=1.88_step=103299_consumed_samples=16114800.0/nemo_to_hf
if __name__ == "__main__":
    import time
    t0 = time.time()
    main()
    elapsed_min = (time.time() - t0) / 60
    print(f"总耗时 {elapsed_min:.1f} 分钟")
