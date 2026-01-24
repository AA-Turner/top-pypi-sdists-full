import numpy as np
from functools import partial
from nemo.collections.nlp.data.language_modeling.megatron.indexed_dataset import IndexedCachedDataset
from nemo.collections.nlp.data.language_modeling.megatron.indexed_dataset import make_dataset as nemo_make_dataset
from nemo.collections.nlp.data.language_modeling.megatron.gpt_dataset import GPTDataset as NeMoGPTDataset
from nemo.collections.nlp.data.language_modeling.megatron.gpt_dataset import _build_doc_idx
from nemo.collections.nlp.data.language_modeling.megatron.gpt_dataset import build_dataset as nemo_build_dataset


def make_dataset(path, impl, skip_warmup=False, impl_kwargs={}, delay_data_mmap=False):
    if impl == 'sequential_cached':
        return SequentialIndexedCachedDataset(path)
    return nemo_make_dataset(path, impl, skip_warmup, impl_kwargs, delay_data_mmap)


def build_dataset(cfg, trainer, data_prefix, data_impl, num_samples, seq_length, seed, skip_warmup, tokenizer, name):
    import nemo.collections.nlp.data.language_modeling.megatron.gpt_dataset as nemo_gpt_dataset
    nemo_gpt_dataset.make_indexed_dataset = make_dataset
    return nemo_build_dataset(cfg, trainer, data_prefix, data_impl, num_samples, seq_length, seed, skip_warmup, tokenizer, name)


def _customized_build_doc_idx(indexed_dataset, documents, num_epochs, np_rng, separate_last_epoch, shuffle=True):
    sub_documents = []
    cur_ds_idx = -1
    for doc_id in documents:
        ds_idx = indexed_dataset._get_ds_idx_based_on_doc_idx(doc_id)
        if ds_idx != cur_ds_idx:
            sub_documents.append([])
            cur_ds_idx = ds_idx
        sub_documents[-1].append(doc_id)
    doc_idx_list = []
    for docs in sub_documents:
        for epoch in range(num_epochs):
            doc_idx_list.append(_build_doc_idx(docs, 1, np_rng, False, shuffle=shuffle))
    return np.concatenate(doc_idx_list)


def _costomized_build_shuffle_idx(num_samples, total_size, np_rng):
    # we will not shuffle the sample idx here
    # so just return np arange
    dtype_ = np.uint32
    if total_size >= (np.iinfo(np.uint32).max - 1):
        dtype_ = np.int64
    return np.arange(start=0, stop=total_size, step=1, dtype=dtype_)


class GPTDataset(NeMoGPTDataset):
    def __init__(
        self, 
        cfg,
        trainer, 
        tokenizer, 
        name, 
        data_prefix, 
        documents, 
        indexed_dataset, 
        num_samples, 
        seq_length, 
        seed, 
        drop_last=True,
    ):
        if isinstance(indexed_dataset, SequentialIndexedCachedDataset):
            # hack the _build_doc_idx and _build_shuffle_idx function here 
            # to make it right for SequentialIndexedCachedDataset
            import nemo.collections.nlp.data.language_modeling.megatron.gpt_dataset as nemo_gpt_dataset
            official_build_doc_idx = nemo_gpt_dataset._build_doc_idx
            official_build_shuffle_idx = nemo_gpt_dataset._build_shuffle_idx
            nemo_gpt_dataset._build_doc_idx = partial(_customized_build_doc_idx, indexed_dataset)
            nemo_gpt_dataset._build_shuffle_idx = _costomized_build_shuffle_idx
        super().__init__(
            cfg,
            trainer, 
            tokenizer, 
            name, 
            data_prefix, 
            documents, 
            indexed_dataset, 
            num_samples, 
            seq_length, 
            seed, 
            drop_last
        )
        if isinstance(indexed_dataset, SequentialIndexedCachedDataset):
            # set the hacked functions back
            nemo_gpt_dataset._build_doc_idx = official_build_doc_idx
            nemo_gpt_dataset._build_shuffle_idx = official_build_shuffle_idx


class SequentialIndexedCachedDataset(IndexedCachedDataset):
    def __init__(self, paths, cache_all=False):
        self.paths = paths
        self.inner_datasets = [IndexedCachedDataset(path) for path in paths]
        self.ds_num = len(paths)
        self.sizes = []
        sizes = [ds.sizes for ds in self.inner_datasets]
        self.sizes = np.concatenate(sizes)
        lens = [len(ds) for ds in self.inner_datasets]
        self._len = sum(lens)
        self._len_accumulate = []
        cur_len = 0
        for i in range(self.ds_num):
            self._len_accumulate.append(cur_len)
            cur_len += len(self.inner_datasets[i])
        self._len_accumulate.append(cur_len)
        self.cur_ds_idx = 0
        self.cache_all = cache_all

    def __del__(self):
        for ds in self.inner_datasets:
            del ds

    # TODO: need to implement logic to do prefetch in sub thread
    def prefetch(self, ds_idx, indices):
        if ds_idx >= self.ds_num:
            logging.warn(f"ds_idx {ds_idx} exceeds the number of inner datasets {self.ds_num}, will loop back")
            ds_idx %= self.ds_num
        indices_for_inner_ds = [i - self._len_accumulate[ds_idx] for i in indices]
        self.inner_datasets[ds_idx].prefetch(indices_for_inner_ds)

    def evict_sub_ds_cache(self, ds_idx):
        ds_idx = ds_idx % self.ds_num
        self.inner_datasets[ds_idx].cache = None
        self.inner_datasets[ds_idx].cache_idx = {}

    def _get_ds_idx_based_on_doc_idx(self, doc_idx):
        for i in range(self.ds_num):
            ds_idx = (i + self.cur_ds_idx) % self.ds_num
            if self._len_accumulate[ds] <= doc_idx < self._len_accumulate[ds_idx + 1]:
                self.cur_ds_idx = ds_idx
                return ds_idx
        raise IndexError(f'index {doc_idx} out of range {self._len_accumulate[-1]}')

    def __getitem__(self, idx):
        if isinstance(idx, int):
            ds_idx = self._get_ds_idx_based_on_doc_idx(idx)
            if not self.cache_all:
                # evict the previous ds cache
                self.evict_sub_ds_cache(ds_idx - 1)
            ds_doc_idx = idx - self._len_accumulate[ds_idx]
            return self.inner_datasets[ds_idx][ds_doc_idx]
        elif isinstance(idx, slice):
            sents = []
            for i in range(*idx.indices(len(self))):
                sents.append(self[i])
            return sents
