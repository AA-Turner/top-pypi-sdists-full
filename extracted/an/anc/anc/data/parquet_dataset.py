from pyarrow.parquet import ParquetFile
import multiprocessing.dummy as mt
import os
import copy
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import numpy as np
import logging

def get_parquet_files_metadata(filepaths, num_threads=None):
    logging.info(f"Getting parquet files metadata for {len(filepaths)} files")
    def _get_parquet_rows(filepath):
        pf = ParquetFile(filepath)
        num_rows = pf.metadata.num_rows
        row_group_rows = [pf.metadata.row_group(i).num_rows for i in range(pf.num_row_groups)]
        pf.close()
        return num_rows, row_group_rows

    num_rows = []
    row_group_rows = []
    with ThreadPoolExecutor(max_workers=num_threads) as pool:
        results = list(tqdm(pool.map(_get_parquet_rows, filepaths), total=len(filepaths), desc="get parquet file metadata"))
        num_rows = [result[0] for result in results]
        row_group_rows = [result[1] for result in results]

    return {
        'num_rows': num_rows,
        'row_group_rows': row_group_rows,
    }


def search_sorted(a, v, hint):
    # fast path
    assert 0 <= hint < len(a)
    if hint == 0 and v < a[0]:
        return 0
    elif a[hint-1] <= v < a[hint]:
        return hint
    # slow path
    indice = np.searchsorted(a, v, side='right').tolist()
    assert 0 <= indice < len(a)
    return indice


class ParquetDataset:
    r'''
    Given a path of parquet file, return target data by index
    Note: This class only implements an efficient way to return sample by index
        The index order is controlled by sampler, not here.

    Args:
        filepath (str or tuple of str): file from which to load the data. If is tuple of str, each 
            each str represents a single parquet file, and corresponding rows across those files together
            form a sample
        columns (list of str, optional), columns to load (default: ``None`` means load all columns)
    '''
    def __init__(self, filepath, columns=None):

        self.filepath = filepath
        if isinstance(filepath, tuple) or isinstance(filepath, list):
            self.parquet_file = [ParquetFile(path) for path in filepath if os.path.exists(path)]
        else:
            self.parquet_file = [ParquetFile(filepath),]

        self.columns = []
        if columns is not None:
            if isinstance(columns[0], str):
                columns = [columns]

            assert len(columns) == len(self.parquet_file), f"columns length {len(columns)} should be the same as the number of parquet files {len(self.parquet_file)}"
            
            for idx, pf in enumerate(self.parquet_file):
                columns_from_file = set(pf.schema.names)
                columns_feed_in = columns[idx]
                # make sure the columns feed in is a subset of the columns in the file
                self.columns.append([col for col in columns_feed_in if col in columns_from_file])
        else:
            self.columns = [None] * len(self.parquet_file)

        self.num_row_groups = self.parquet_file[0].num_row_groups
        self.row_groups = list(range(self.num_row_groups))
        self.row_group_rows = [self.parquet_file[0].metadata.row_group(i).num_rows for i in self.row_groups]

        self.row_group_rows_accumulate = np.cumsum(self.row_group_rows).tolist()
        self.cur_row_group = 0

        self.num_rows = self.parquet_file[0].metadata.num_rows
        self.cache = {}
        # ensure that the metadata of the group files is same
        for i in range(1, len(self.parquet_file)):
            assert self.num_row_groups == self.parquet_file[i].num_row_groups
            assert self.row_group_rows == [self.parquet_file[i].metadata.row_group(rid).num_rows for rid in self.row_groups]
    
    def _read_row_group(self, row_group):
        rows = []
        for idx, pf in enumerate(self.parquet_file):
            row_group_data = pf.read_row_group(row_group, columns=self.columns[idx])
            group_data = row_group_data.to_pandas()
            cur_rows = group_data.to_dict('records')
            if len(rows) == 0:
                rows = cur_rows
            else:
                assert len(rows) == len(cur_rows), "row group of each file should be the same"
                for i in range(len(rows)):
                    rows[i].update(cur_rows[i])
        return rows

    def __iter__(self):
        for row_group in self.row_groups:
            rows = self._read_row_group(row_group)
            yield from rows
    
    def _get_row_group_idx_from_ridx(self, ridx):
        if self.row_group_rows_accumulate[self.cur_row_group] <= ridx < self.row_group_rows_accumulate[self.cur_row_group + 1]:
            return self.cur_row_group
        for i in self.row_groups:
            cur_gidx = (self.cur_row_group + i) % self.num_row_groups
            if self.row_group_rows_accumulate[cur_gidx] <= ridx < self.row_group_rows_accumulate[cur_gidx + 1]:
                self.cur_row_group = cur_gidx
                return self.cur_row_group
        return -1
    
    def _clean_cache(self):
        # TODO: maybe a better way to find out which row groups to delete
        gidx_to_delete = [i for i in self.cache]
        for i in gidx_to_delete:
            del self.cache[i]
    
    def __getitem__(self, idx):
        assert 0 <= idx < self.num_rows, f"idx shoud be in [0, {self.num_rows}) but get {idx}"
        cur_row_group = search_sorted(self.row_group_rows_accumulate, idx, self.cur_row_group)
        assert cur_row_group >= 0, f"invalid row group {cur_row_group} for idx {idx}"
        self.cur_row_group = cur_row_group
        if cur_row_group not in self.cache:
            cur_rows = self._read_row_group(cur_row_group)
            self._clean_cache()
            self.cache[cur_row_group] = cur_rows
        else:
            cur_rows = self.cache[cur_row_group]
        offset = idx if cur_row_group == 0 else idx - self.row_group_rows_accumulate[cur_row_group-1]
        sample = cur_rows[offset]
        if 'row_idx' not in sample:
            sample['row_idx'] = idx
        return copy.deepcopy(sample)
    
    def __len__(self):
        return self.num_rows

    def close(self):
        del self.cache
        for pf in self.parquet_file:
            pf.close()
    
    def get_sub_lengths(self):
        return self.row_group_rows


class ParquetConcateDataset:
    r'''
    Given multiple parquet files as a whole dataset, return target data by index
    Note: This class only implements an efficient way to return sample by index.
        The index order is controlled by sampler, not here.

    Args:
        filepaths (list of str): files from which to load the data.
        columns (list of str, optional), columns to load (default: ``None`` means load all columns)
    '''
    def __init__(self, filepaths, **kwargs):
        self.filepaths = filepaths
        self.num_files = len(filepaths)
        self.columns = kwargs.get("columns", None)
        self.cur_ds_idx = 0
        self.cache = {}
        self.metadata = kwargs.get("metadata", None)

        logging.info(f"Creating ParquetConcateDataset with {self.num_files} files, metadata provided: {self.metadata is not None}")
        if self.metadata is not None:
            self.num_rows = sum(self.metadata['num_rows'])
            self.num_rows_accumulate = np.cumsum(self.metadata['num_rows']).tolist()
            self.rows_per_file = self.metadata['num_rows']
            self.rows_per_group = self.metadata['row_group_rows']
            return

        rows = []
        rows_per_group = []
        with mt.Pool(16) as p:
            sub_ds_info = p.map(self._get_sub_ds_length, self.filepaths)
        rows = [i[0] for i in sub_ds_info]
        rows_per_group = [i[1] for i in sub_ds_info]
        self.rows_per_file = rows
        self.rows_per_group = rows_per_group
        self.num_rows = sum(self.rows_per_file)
        self.num_rows_accumulate = np.cumsum(self.rows_per_file).tolist()

    def _get_sub_ds_length(self, path):
        ds = ParquetDataset(path)
        row = len(ds)
        row_groups = ds.get_sub_lengths()
        ds.close()
        return row, row_groups

    def __len__(self):
        return self.num_rows
    
    def _clean_cache(self):
        ds_idx_to_delete = [i for i in self.cache]
        for i in ds_idx_to_delete:
            self.cache[i].close()
            del self.cache[i]

    def __getitem__(self, idx):
        assert 0 <= idx < self.num_rows, f"idx shoud be in [0, {self.num_rows}) but get {idx}"
        cur_ds_idx = search_sorted(self.num_rows_accumulate, idx, self.cur_ds_idx)
        assert cur_ds_idx >= 0, f"invalid file idx {cur_ds_idx} for row idx {idx}"
        self.cur_ds_idx = cur_ds_idx
        if cur_ds_idx not in self.cache:
            cur_ds = ParquetDataset(self.filepaths[cur_ds_idx], self.columns)
            self._clean_cache()
            self.cache[cur_ds_idx] = cur_ds
        else:
            cur_ds = self.cache[cur_ds_idx]
        offset = idx if cur_ds_idx == 0 else idx - self.num_rows_accumulate[cur_ds_idx-1]
        data = cur_ds[offset]
        if 'filepath' not in data:
            data['filepath'] = self.filepaths[cur_ds_idx]
        return data
    
    def get_sub_lengths(self, level="row_group"):
        assert level in {"row_group", "file"}
        if level == "row_group":
            return self.rows_per_group
        else:
            return self.rows_per_file


if __name__ == "__main__":
    folder = "/mnt/personal/parquet_demo_data"
    fnames = [
        "01_0001.parquet",
        "02_0001.parquet",
        "03_0001.parquet",
        "04_0001.parquet",
        "05_0001.parquet",
        "06_0001.parquet",
        "07_0001.parquet"
    ]
    files = [f"{folder}/{fname}" for fname in fnames]
    ds = ParquetConcateDataset(files)
    assert [sum(i) for i in ds.rows_per_group] == ds.rows_per_file
    assert sum(ds.rows_per_file) == len(ds)
    for i in range(10):
        data = ds[i * 500]
        print(data['filepath'])
