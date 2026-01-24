import logging


class SeqSplitConfig:
    """Configuration class for sequence splitting behavior.
    
    Attributes:
        allow_split: Boolean flag to enable/disable sequence splitting
        split_threshold: Minimum sequence length that triggers splitting
        freeze_batch_interval: Number of batches to wait before unfreezing split sequences
    """
    def __init__(
        self,
        allow_split=False,
        split_threshold=None,
        freeze_batch_interval=None
    ):
        self.allow_split = allow_split
        self.split_threshold = split_threshold
        self.freeze_batch_interval = freeze_batch_interval


# AncComposerBuffer uses get_token_length_fn to get the token length of each sample.
# Set get_token_length_fn properly to make sample composing correct.
class AncComposerBuffer:
    """Buffer class that manages token sequences and their composition.
    
    This class handles the storage, splitting, and retrieval of token sequences while
    maintaining proper token length tracking and batch management.
    
    Attributes:
        buffer: List of tuples containing (token_length, item)
        total_token_length: Running sum of all token lengths in buffer
        get_token_length_fn: Function to calculate token length of an item
        split_fn: Function to split sequences that are too long
        delete_idx: Set of indices marked for deletion
        freeze_splits_buffer: Buffer for split sequences that are temporarily frozen
        unfrozen_splits_buffer: Buffer for split sequences ready to be processed
    """
    def __init__(
        self,
        get_token_length_fn=None,
        split_fn=None,
        freeze_batch_interval=None,
        enable_logging=True,
        # get_from_split_chunks_prob=0.6,
    ):
        self.buffer = []
        self.total_token_length = 0
        self.get_token_length_fn = get_token_length_fn
        self.split_fn = split_fn
        self.delete_idx = set()
        self.cur_idx = 0
        # if freeze_batch_interval is None, we do not care the split chunks existing in the same minibatch
        # otherwise, we need to hold the remained splitted chunks for a while to make sure
        # split chunks trained in different mini batches
        self.freeze_batch_interval = freeze_batch_interval
        self.enable_split_freeze = freeze_batch_interval is not None
        self.batch_count = 0
        self.freeze_splits_buffer = []
        self.unfrozen_splits_buffer = []
        self.enable_logging = enable_logging
        # self.random_state = None
        # self.get_from_split_chunks_prob = get_from_split_chunks_prob

    def put(self, item):
        """Add an item to the buffer and return total token length.
        
        Args:
            item: The sequence item to add to the buffer
        Returns:
            int: Updated total token length in buffer
        """
        if item is not None:
            token_length = self._get_token_length(item)
            self.buffer.append((token_length, item))
            self.total_token_length += token_length
        return self.total_token_length

    def get(self, target_length, first_call=False):
        """Retrieve first sample that fits within target length.
        
        Args:
            target_length: Maximum allowed token length
            first_call: Whether this is the first retrieval attempt for current batch
        Returns:
            tuple: (token_length, item) or None if no suitable item found
        """
        # try to get from split chunks first
        if first_call and self.split_fn is not None and self.enable_split_freeze:
            # when first_call is True, the target_length should be equal to context window size
            split_chunk = self.try_to_get_from_split_chunks(target_length)
            if split_chunk is not None:
                return split_chunk
        for i in range(len(self.buffer)):
            idx = (i + self.cur_idx) % len(self.buffer)
            if idx in self.delete_idx:
                continue
            if self.buffer[idx][0] <= target_length:
                self.delete_idx.add(idx)
                self.total_token_length -= self.buffer[idx][0]
                self.cur_idx = (idx + 1) % len(self.buffer)
                return self.buffer[idx]
        return None

    def _get_token_length(self, item):
        """Helper function to get token length of an item.
        
        Args:
            item: The item to get token length of
        Returns:
            int: Token length of the item, default to 1 if get_token_length_fn is not provided
        """
        if self.get_token_length_fn is not None:
            return self.get_token_length_fn(item)
        else:
            return 1

    # try to get target_length from unfrozen split chunks
    def try_to_get_from_split_chunks(self, target_length):
        """Try to get a split chunk that fits within target length.
        
        Args:
            target_length: The target length to get
        Returns:
            Tuple: (target_length, split_chunk_of_item) or None if no suitable split chunk found
        """
        if len(self.unfrozen_splits_buffer) == 0:
            return
        # if self.random_state is None:
        #     self.random_state = random.Random(self.batch_count)
        # if self.random_state.random() > self.get_from_split_chunks_prob:
        #     return
        split_chunk = self.unfrozen_splits_buffer.pop(0)
        if split_chunk[0] <= target_length:
            return split_chunk
        else:
            if self.enable_logging:
                print(
                    f"[Composer] chunked item with size {split_chunk[0]} "
                    f"will be split one more time to get {target_length}"
                )
            # the split is still too large, needs to further split it
            to_return, remain = self.split_fn(split_chunk[1], target_length)
            remain_length = self._get_token_length(remain)
            assert self._get_token_length(to_return) == target_length
            self.freeze_splits_buffer.append((remain_length, remain, self.batch_count))
            return (target_length, to_return)
    
    def get_with_split(self, target_length, ignore_split_freezing=False):
        """Split a long sequence to fit target length requirement.
        
        Finds the longest sequence in buffer and splits it to create a sequence
        of exactly target_length tokens.
        
        Args:
            target_length: Desired length of the returned sequence
            ignore_split_freezing: Whether to bypass freeze mechanism for splits
        Returns:
            tuple: (target_length, split_chunk_of_item) or None if splitting not possible
        """
        if self.total_token_length == 0:
            return None
        if self.split_fn is None:
            return None
        max_length_idx = -1
        max_length = target_length
        for i, item in enumerate(self.buffer):
            if i in self.delete_idx:
                continue
            if item[0] > max_length:
                max_length = item[0]
                max_length_idx = i
        if max_length_idx == -1:
            return None
        assert max_length > target_length, (
            f"Invalid buffer {[i[0] for i in self.buffer]} with target_length {target_length}"
        )
        assert self.buffer[max_length_idx][0] == max_length
        to_return, remain = self.split_fn(self.buffer[max_length_idx][1], target_length)
        remain_length = self._get_token_length(remain)
        assert self._get_token_length(to_return) == target_length
        
        if not self.enable_split_freeze or ignore_split_freezing:
            self.buffer[max_length_idx] = (remain_length, remain)
            self.total_token_length = (
                self.total_token_length - max_length + remain_length
            )
            self.cur_idx = max_length_idx
        else:
            self.freeze_splits_buffer.append((remain_length, remain, self.batch_count))
            self.total_token_length -= max_length
            self.delete_idx.add(max_length_idx)
        return (target_length, to_return)
    
    def get_all(self):
        """Retrieve all items from the buffer.
        
        Returns:
            list: List of all items in the buffer
        """
        res = self.buffer
        self.buffer = []
        self.total_token_length = 0
        self.delete_idx = set()
        self.cur_ids = 0
        return res
    
    def unfrozen_splits(self):
        """Unfreeze split chunks.
        
        Adds split chunks from freeze_splits_buffer to unfrozen_splits_buffer.
        """
        to_freeze = [(i[0], i[1]) for i in self.freeze_splits_buffer if self.batch_count - i[2] > self.freeze_batch_interval]
        self.unfrozen_splits_buffer += to_freeze
        self.freeze_splits_buffer = [i for i in self.freeze_splits_buffer if self.batch_count - i[2] <= self.freeze_batch_interval]
        if self.enable_logging:
            print(
                f"[Composer] item count in unfrozen_splits_buffer: "
                f"{len(self.unfrozen_splits_buffer)}"
            )
            print(
                f"[Composer] token count in unfrozen_splits_buffer: "
                f"{sum(i[0] for i in self.unfrozen_splits_buffer)}"
            )

    def flush(self):
        """Flush the buffer.
        
        Removes deleted items and updates the buffer.
        It is usually called when finish getting one micro batch of data.
        """
        buffer = [self.buffer[i] for i in range(len(self.buffer)) if i not in self.delete_idx]
        self.buffer = buffer
        self.delete_idx = set()
        #print(f"=====self.total_token_length: {self.total_token_length}, {[i[0] for i in self.unfrozen_splits_buffer]}, {[(i[0], i[2]) for i in self.freeze_splits_buffer]}, {self.batch_count}, {self.freeze_batch_interval}")
        assert sum([i[0] for i in self.buffer]) == self.total_token_length
        if self.enable_split_freeze:
            self.batch_count += 1
            # if self.batch_count == self.freeze_batch_interval:
            #     self.batch_count = 0
            self.unfrozen_splits()
        #print(f"=====self.total_token_length: {self.total_token_length}, {[i[0] for i in self.unfrozen_splits_buffer]}, {[(i[0], i[2]) for i in self.freeze_splits_buffer]}, {self.batch_count}, {self.freeze_batch_interval}")

    def combine_buffers(self):
        """Combine buffers.
        
        Adds split chunks from unfrozen_splits_buffer and freeze_splits_buffer to the main buffer.
        It is usually called when running to the end of the dataset
        """
        self.buffer += self.unfrozen_splits_buffer + [(i[0], i[1]) for i in self.freeze_splits_buffer]
        self.unfrozen_splits_buffer = []
        self.freeze_splits_buffer = []
        self.total_token_length = sum([i[0] for i in self.buffer])

    def _get_ckpt(self):
        states = {}
        states['buffer'] = self.buffer
        states['total_token_length'] = self.total_token_length
        states['unfrozen_splits_buffer'] = self.unfrozen_splits_buffer
        states['freeze_splits_buffer'] = self.freeze_splits_buffer
        states['delete_idx'] = self.delete_idx
        states['cur_idx'] = self.cur_idx
        states['batch_count'] = self.batch_count
        # states['random_state'] = self.random_state
        return states

    def _set_ckpt(self, state):
        self.buffer = state['buffer']
        self.total_token_length = state['total_token_length']
        self.unfrozen_splits_buffer = state['unfrozen_splits_buffer']
        self.freeze_splits_buffer = state['freeze_splits_buffer']
        self.delete_idx = state['delete_idx']
        self.cur_idx = state['cur_idx']
        self.batch_count = state['batch_count']
        # self.random_state = state['random_state']

class AncComposer:
    """Main composer class that handles sequence composition and batch creation.
    
    This class coordinates the buffer management, sequence splitting, and batch
    formation according to specified constraints.
    
    Attributes:
        max_seq_len: Maximum allowed sequence length
        allow_split: Whether to allow splitting of long sequences
        ratio: Controls buffer size relative to max_seq_len
        split_threshold: Minimum length that triggers sequence splitting
    """
    def __init__(
        self,
        max_seq_len,
        get_token_length_fn=None,
        ratio=2.0,
        seq_split_config=None,
        split_fn=None,
        enable_logging=True,
    ):
        self.max_seq_len = max_seq_len
        self.allow_split = seq_split_config.allow_split if seq_split_config is not None else False
        freeze_batch_interval = seq_split_config.freeze_batch_interval if seq_split_config is not None else None
        if self.allow_split:
            assert split_fn is not None, "Need to provide split_fn to enable allow_split"
        self.split_fn = split_fn if self.allow_split else None
        self.buffer = AncComposerBuffer(
            get_token_length_fn,
            self.split_fn,
            freeze_batch_interval,
            enable_logging,
        )
        # ratio here controls how many samples would be collected in the buffer
        # it might be difficult to compose enough samples to reach the max_seq_len when buffer size is small
        self.ratio = ratio
        self.split_threshold = seq_split_config.split_threshold if seq_split_config is not None else max_seq_len
        if self.split_threshold is None:
            self.split_threshold = max_seq_len
        self.enable_logging = enable_logging
        self.remain = []

    # function to return one micro batch
    def get_items(self, is_last_call=False, ignore_split_freezing=False):
        """Retrieve one micro batch (max_seq_len of tokens) from the buffer.
        
        Args:
            is_last_call: Whether this is the final call (triggers buffer cleanup)
            ignore_split_freezing: Whether to bypass freeze mechanism for splits
        Returns:
            list: List of items in the micro batch, the sum of the token length of the items should be equal to or less than max_seq_len
        """
        items = []
        if is_last_call:
            items = self.buffer.get_all()
            items = [i[1] for i in items if i is not None]
            return items
        cur_seq_length = self.max_seq_len
        first_call = True
        while True:
            item = self.buffer.get(cur_seq_length, first_call)
            first_call = False
            if item is None:
                break
            assert len(item) == 2
            items.append(item[1])
            cur_seq_length = cur_seq_length - item[0]
            if cur_seq_length == 0:
                break
        if cur_seq_length >= self.split_threshold and self.allow_split:
            item = self.buffer.get_with_split(cur_seq_length, ignore_split_freezing)
            if item is not None:
                assert item[0] == cur_seq_length
                items.append(item[1])
        self.buffer.flush()
        return items

    def apply(self, sample, is_last_call=False):
        """Process a single sample and generate batches if buffer is full enough.
        
        Args:
            sample: Input item to process
            is_last_call: Whether this is the final call (triggers buffer cleanup)
        Returns:
            list: List of batched items or None if no batches were created
        """
        total_token_length = self.buffer.put(sample)
        res = []
        while total_token_length >= self.max_seq_len * self.ratio:
            items = self.get_items()
            res.append(items)
            total_token_length = self.buffer.put(None)
        if is_last_call:
            self.buffer.combine_buffers()
            total_token_length = self.buffer.put(None)
            while total_token_length >= self.max_seq_len:
                items = self.get_items(ignore_split_freezing=True)
                res.append(items)
                total_token_length = self.buffer.put(None)
            if total_token_length > 0:
                items = self.get_items(is_last_call=True)
                res.append(items)
        return res if len(res) > 0 else None
    
    def __call__(self, samples, is_last_call=False):
        """Entrypoint of the composer.
        
        Args:
            samples: List of samples to process
            is_last_call: Whether this is the final call (triggers buffer cleanup)
        Returns:
            list: List of batched items or None if no batches were created
        """
        if self.remain:
            yield from self.remain
            self.remain = []
        for sample in samples:
            if sample is None:
                continue
            res = self.apply(sample)
            if res is None:
                continue
            for i, item in enumerate(res):
                self.remain = res[i+1:]
                yield item
            # yield from res
        assert len(self.remain) == 0
        if is_last_call:
            res = self.apply(None, True)
            if res is not None:
                yield from res

    def _get_ckpt(self):
        states = {}
        states['buffer'] = self.buffer._get_ckpt()
        states['remain'] = self.remain
        return states
    
    def _set_ckpt(self, state):
        self.buffer._set_ckpt(state['buffer'])
        if 'remain' in state:
            self.remain = state['remain']


if __name__ == "__main__":
    import random
    from functools import partial
    def create_fake_data(min_token_length, max_seq_length, max_token_length):
        i  = 0
        while True:
            if random.random() <= 0.2:
                data = random.randint(max_seq_length, max_token_length)
            else:
                data = random.randint(min_token_length, max_seq_length)
            yield {'doc_id': i, "tokens": data}
            i += 1
    
    def fake_split_fn(item, split_length, prefix_len):
        to_return = {}
        remain = {}
        to_return['doc_id'] = item['doc_id']
        remain['doc_id'] = item['doc_id']
        to_return['tokens'] = split_length
        assert split_length > prefix_len
        remain['tokens'] = item['tokens'] + prefix_len - split_length
        return to_return, remain
    
    def fake_get_token_length_fn(item):
        return item['tokens']
    
    max_seq_length = 8192  # 8K
    freeze_batch_interval = 64
    split_threshold = 128
    prefix_len = 32
    min_token_length = prefix_len + 32
    max_token_length = 2 ** 15  # 32K
    batch_limit = 100

    
    split_config = SeqSplitConfig(
        allow_split=True,
        split_threshold=split_threshold,
        freeze_batch_interval=freeze_batch_interval,
    )
    
    composer = AncComposer(
        max_seq_length,
        get_token_length_fn=fake_get_token_length_fn,
        seq_split_config=split_config,
        split_fn=partial(fake_split_fn, prefix_len=prefix_len),
    )

    data_generator = create_fake_data(min_token_length, max_seq_length, max_token_length)
    micro_batch_count = 0
    batch_doc_id = []
    token_lengths = []
    batch_count = 0
    for data in data_generator:
        res = composer([data])
        for micro_batch in res:
            micro_batch_count += 1
            doc_ids = [i['doc_id'] for i in micro_batch]
            token_length = sum([i['tokens'] for i in micro_batch])
            token_lengths.append(token_length)
            assert max_seq_length - split_threshold < token_length <= max_seq_length
            batch_doc_id += doc_ids
            if micro_batch_count == freeze_batch_interval:
                assert len(batch_doc_id) == len(set(batch_doc_id))
                print(token_lengths, batch_doc_id)
                micro_batch_count = 0
                batch_doc_id = []
                batch_count += 1
                token_lengths = []
        if batch_count >= batch_limit:
            break
