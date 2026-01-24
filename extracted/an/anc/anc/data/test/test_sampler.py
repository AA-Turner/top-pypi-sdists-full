import random
import os
from anc.data.anc_sampler import AncSampler, RangesHolder, CustomizedRange


class SimpleDataset:
    def __init__(self, sub_ds_count, sub_ds_size):
        self.sub_ds_count = sub_ds_count
        self.sub_ds_size = sub_ds_size

    def get_sub_lengths(self):
        return [self.sub_ds_size] * self.sub_ds_count

    def __len__(self):
        return self.sub_ds_count * self.sub_ds_size


class SimpleDataset2:
    def __init__(self, ds_count, sub_ds_count, sub_ds_size):
        self.ds_count = ds_count
        self.sub_ds_count = sub_ds_count
        self.sub_ds_size = sub_ds_size
    def get_sub_lengths(self):
        return [[self.sub_ds_size] * self.sub_ds_count for _ in range(self.ds_count)]
    def __len__(self):
        return self.sub_ds_count * self.sub_ds_size * self.ds_count


'''def check_sampler_indices(shuffle, batch_size, resume_step):
    # create a fake dataset with 3 files and each file contains 100 elements
    sub_ds_size = 40
    sub_ds_count = 3
    ds = SimpleDataset(sub_ds_count, sub_ds_size)
    world = 4
    rank = 0
    num_workers = 2
    drop_last = False
    num_per_rank = (sub_ds_size * sub_ds_count + (world - 1) * int(not drop_last)) // world
    # with the above parameters (if shuffle = False), the data idxs that rank 0 would generate are [0, 30), totally 30 elements
    # since batch size = 4, the batch number would be 8, with last batch only containing 2 elements
    # thus worker 0 of rank 0 would generate [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    #      worker 1 of rank 0 would generate [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
    sampler = AncSampler(ds, batch_size, world, rank, num_workers, shuffle=False, drop_last=drop_last, resume_step=resume_step)
    assert len(sampler) == (num_per_rank + batch_size - 1) // batch_size
    indices = []
    for item in sampler:
        cur_index, is_last_batch = item
        if not is_last_batch:
            # cur_index would be [] if resume_step % num_workers != 0
            assert len(cur_index) == batch_size or len(cur_index) == 0
        #if is_last_batch:
            # each worker's last batch would set is_last_batch to True
            # so we have num_workers is_last_batch
        #    assert sampler.step >= len(sampler) - num_workers
        indices += cur_index
    print(indices)
    #if not shuffle and resume_step == 0:
    #    assert indices[:16] == [0, 1, 2, 3, 16, 17, 18, 19, 4, 5, 6, 7, 20, 21, 22, 23]
    #    assert indices[-6:] == [12, 13, 14, 15, 28, 29]
    return indices
'''
def check_sampler_indices(shuffle, batch_size, resume_step):
    # create a fake dataset with 3 files and each file contains 100 elements
    sub_ds_size = 40
    sub_ds_count = 3
    ds = SimpleDataset(sub_ds_count, sub_ds_size)
    world = 4
    rank = 0
    num_workers = 2
    drop_last = False
    num_per_rank = (sub_ds_size * sub_ds_count + (world - 1) * int(not drop_last)) // world
    indices_of_all_workers = {}
    for i in range(num_workers):
        # with the above parameters (if shuffle = False), the data idxs that rank 0 would generate are [0, 30), totally 30 elements
        # since batch size = 4, the batch number would be 8, with last batch only containing 2 elements
        # thus worker 0 of rank 0 would generate [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        #      worker 1 of rank 0 would generate [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
        os.environ['WID_FOR_DEBUG'] = str(i)
        worker_resume_step = resume_step // num_workers
        remain = resume_step % num_workers
        if i < remain:
            worker_resume_step += 1
        sampler = AncSampler(ds, batch_size, world, rank, num_workers, shuffle=False, drop_last=drop_last, resume_step=worker_resume_step)
        assert len(sampler) == (num_per_rank + batch_size - 1) // batch_size
        indices = []
        for item in sampler:
            cur_index, is_last_batch = item
            if not is_last_batch:
                # cur_index would be [] if resume_step % num_workers != 0
                assert len(cur_index) == batch_size or len(cur_index) == 0
            # if is_last_batch:
            #     # each worker's last batch would set is_last_batch to True
            #     # so we have num_workers is_last_batch
            #     assert sampler.step >= len(sampler) - num_workers
            # indices += cur_index
            indices.append(cur_index)
        indices_of_all_workers[i] = indices
    indices = []
    while True:
        for i in range(num_workers):
            if indices_of_all_workers[i]:
                indices += indices_of_all_workers[i].pop(0)
        if all(len(indices_of_all_workers[i]) == 0 for i in range(num_workers)):
            break
    if not shuffle and resume_step == 0:
        assert indices[:16] == [0, 1, 2, 3, 16, 17, 18, 19, 4, 5, 6, 7, 20, 21, 22, 23]
        assert indices[-6:] == [12, 13, 14, 15, 28, 29]
    return indices

def test_resume():
    batch_size = 4
    from_beginning_indices = check_sampler_indices(shuffle=False, batch_size=batch_size, resume_step=0)
    check_sampler_indices(shuffle=True, batch_size=batch_size, resume_step=0)
    resume_step = 4
    resumed_indices = check_sampler_indices(shuffle=False, batch_size=batch_size, resume_step=resume_step)
    #print(resumed_indices)
    assert resumed_indices == from_beginning_indices[batch_size * resume_step:]


def test_get_indices_with_ratio():
    # Test setup
    ds = SimpleDataset(1, 10)  # Single dataset with 10 elements
    sampler = AncSampler(ds, batch_size=2, shuffle=False)
    base_indices = list(range(10))  # [0,1,2,3,4,5,6,7,8,9]
    
    # Test case 1: Integer ratio without shuffle
    result = sampler._get_indices_with_ratio(base_indices, 2.0)
    assert len(result) == 2, "Should have 2 copies of indices"
    assert result[0] == base_indices, "First copy should match original"
    assert result[1] == base_indices, "Second copy should match original"
    
    # Test case 2: Fractional ratio without shuffle
    result = sampler._get_indices_with_ratio(base_indices, 1.5)
    assert len(result) == 2, "Should have 2 lists (1 full + 1 partial)"
    assert result[0] == base_indices, "First copy should be complete"
    assert len(result[1]) == 5, "Second copy should be half length"
    assert result[1] == base_indices[:5], "Partial copy should be first half"
    
    # Test case 3: With chunk granularity
    sampler.chunk_granularity = 3
    result = sampler._get_indices_with_ratio(base_indices, 1.0)
    assert len(result) == 4, "Should split into 4 chunks of size 3 (last chunk size 1)"
    assert result[0] == [0,1,2], "First chunk"
    assert result[1] == [3,4,5], "Second chunk"
    assert result[2] == [6,7,8], "Third chunk"
    assert result[3] == [9], "Last chunk"

    # Test case 4: With shuffle
    sampler.shuffle = True
    sampler.chunk_granularity = -1
    random.seed(42)  # For reproducibility
    result = sampler._get_indices_with_ratio(base_indices, 1.0)
    assert len(result) == 1, "Should have 1 shuffled copy"
    assert len(result[0]) == len(base_indices), "Should contain all indices"
    assert result[0] != base_indices, "Should be shuffled"
    assert sorted(result[0]) == base_indices, "Should contain same elements"


def test_mem_save_mode(shuffle=False):
    sub_ds_size = 40
    sub_ds_count = 3
    ds_count = 3
    ds = SimpleDataset2(ds_count, sub_ds_count, sub_ds_size)
    world = 8
    num_workers = 2
    drop_last = False
    batch_size = 4
    indices = []
    for rank in range(world):
        for i in range(num_workers):
            os.environ['WID_FOR_DEBUG'] = str(i)
            sampler = AncSampler(ds, batch_size, world, rank, num_workers, shuffle=shuffle, drop_last=drop_last, mem_save_mode=True)
            for item in sampler:
                cur_index, is_last_batch = item
                indices += cur_index
    print(len(indices), len(set(indices)), ds_count * sub_ds_count * sub_ds_size)
    #assert len(indices) == ds_count * sub_ds_count * sub_ds_size
    return indices


def test_range_holder():
    holder = RangesHolder([CustomizedRange(0, 10), CustomizedRange(10, 25), CustomizedRange(25, 30)])
    assert len(holder) == 30
    sliced_holder = holder.slice(0, 30)
    assert sliced_holder.to_list() == list(range(30))
    sliced_holder = holder.slice(5, 12)
    assert sliced_holder.to_list() == list(range(5, 17))

def test_get_start_idx():
    ranges = []
    accu_length = 0
    for i in range(100):
        range_size = random.randint(10, 100)
        ranges.append(CustomizedRange(accu_length, accu_length+range_size))
        accu_length += range_size
    holder = RangesHolder(ranges)
    for i in range(100):
        start = random.randint(0, accu_length - 1)
        length = random.randint(1, 100)
        length = min(length, accu_length - start)
        start_range_id, start_range_offset, end_range_id, end_range_offset = holder.get_start_and_end_ranges(start, length)
        assert holder.accu_lengths[start_range_id] <= start, f"{holder.accu_lengths[start_range_id]} vs {start}"
        assert holder.accu_lengths[end_range_id + 1] > start + length >= holder.accu_lengths[end_range_id], f"{start}, {length}, {start_range_id}, {holder.accu_lengths}, {end_range_id} {end_range_offset}, {holder.accu_lengths[end_range_id + 1]} vs {start + length} vs {holder.accu_lengths[end_range_id]}"

if __name__ == "__main__":
    test_resume()
    test_get_indices_with_ratio()
    test_mem_save_mode(True)
    test_range_holder()
    test_get_start_idx()
