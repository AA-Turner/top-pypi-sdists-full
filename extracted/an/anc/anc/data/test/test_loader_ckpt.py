from anc.data.processors.llm_processor import PretrainProcessor
from anc.data.anc_dataloader import AncDataLoader
from anc.data.anc_composer import SeqSplitConfig
from anc.data.anc_dataset import AncDataset
from anc.data.anc_sampler import AncSampler
import os
import time
import torch


def run(data_paths, save_ckpt=True):
    """Test the checkpoint functionality of AncDataLoader
    
    This function tests two scenarios:
    1. Loading data without checkpoint (save_ckpt=False). The loaded data act as the baseline.
    2. Loading data with checkpoint, save and restore (save_ckpt=True), 
       and compare the loaded data with the baseline.
    
    Args:
        data_paths: List of paths to parquet files
        save_ckpt: Boolean flag to enable/disable saving checkpoint
    
    Returns:
        List of loaded data batches
    """
    # Initialize tokenizer configuration
    special_token_ids = [128011, 128012]
    pad_to_max_seq_len = True
    seq_split_config = SeqSplitConfig(True, 128, 64)
    
    # Create processor for tokenization and sequence processing
    processor = PretrainProcessor(
        hf_model_name="/mnt/project/llm/ckpt/tokenizer/ocean_tokenizer_based_on_llama3",
        max_seq_len=8192,
        add_bos=True,
        batch_size=1,
        micro_batch_size=1,
        special_token_ids=special_token_ids,
        pad_to_max_seq_len=pad_to_max_seq_len,
        seq_split_config=seq_split_config,
    )
    
    # DataLoader configuration
    nw = 2  # Number of workers
    ckpt_interval = 10 if save_ckpt else None  # Save checkpoint every 10 batches if enabled
    
    # Initialize first dataloader
    ld = AncDataLoader(
        paths=data_paths,
        batch_size=64,
        num_workers=nw,
        rank=0,
        world=1,
        processor=processor,
        data_type="parquet",
        enable_compose=True,
        pin_memory=True,
        is_train=True,
        shuffle=True,
        drop_last=False,
        repeat=False,
        max_steps=-1,
        prefetch_factor=2,
        enable_logging=False,
        ckpt_interval=ckpt_interval,
    )

    # First pass: Load data and optionally save checkpoint
    cnt = 0
    data = []
    ckpt = None
    stop_cnt = 78  # Maximum number of batches to process
    ckpt_cnt = 0

    for i in ld:
        cnt += 1
        data.append(i)
        if save_ckpt and cnt % ckpt_interval == 0:
            ckpt = ld.get_checkpoint()
            ckpt_cnt = cnt
        if cnt >= stop_cnt:
            break

    # If no checkpoint was saved, return the data
    if not ckpt:
        return data
        
    # Second pass: Create new dataloader and restore from checkpoint
    ld = AncDataLoader(
        paths=data_paths,
        batch_size=64,
        num_workers=nw,
        rank=0,
        world=1,
        processor=processor,
        data_type="parquet",
        enable_compose=True,
        pin_memory=True,
        is_train=True,
        shuffle=True,
        drop_last=False,
        repeat=False,
        max_steps=-1,
        prefetch_factor=2,
        enable_logging=False,
        data_borrow=False,
        ckpt_interval=None,
        chunk_granularity=100,
    )
    
    # Keep data up to checkpoint and continue loading from there
    data = data[:ckpt_cnt]
    ld.set_checkpoint(ckpt)
    for i in ld:
        ckpt_cnt += 1
        data.append(i)
        if ckpt_cnt >= stop_cnt:
            break

    return data


def _check_helper(i, j):
    """Recursively compare two data structures (lists, dicts, tensors, or basic types)
    
    Args:
        i, j: Two items to compare
    
    Raises:
        AssertionError: If items are not identical
    """
    if isinstance(i, list):
        for ii, jj in zip(i, j):
            _check_helper(ii, jj)
    elif isinstance(i, dict):
        for k in i:
            _check_helper(i[k], j[k])
    elif isinstance(i, torch.Tensor):
        assert torch.equal(i, j)
    else:
        assert i == j


def check_identical(d0, d1):
    """Compare two datasets for exact equality
    
    Args:
        d0, d1: Two datasets to compare
    
    Raises:
        AssertionError: If datasets are not identical
        
    Prints:
        Error message indicating which key mismatched in which item if comparison fails
    """
    assert len(d0) == len(d1)
    for i in range(len(d0)):
        for k in d0[i]:
            assert k in d1[i]
            try:
                _check_helper(d0[i], d1[i])
            except:
                print(f"key {k} mismatch of {i}th item")


if __name__ == "__main__":
    import random
    data_paths = [f"/mnt/project/llm/data/pretrain/test/d01_test/final/part-{i:05}-effb730d-5a52-4fd2-a545-cd2ffb648b8f-c000.snappy.parquet" for i in range(198)]
    data_paths = [i for i in data_paths if os.path.exists(i)]
    random.shuffle(data_paths)
    data0 = run(data_paths[:1], False)
    data1 = run(data_paths[:1], True)
    check_identical(data0, data1)