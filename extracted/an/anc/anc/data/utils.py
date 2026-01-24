from pyarrow.parquet import ParquetFile
import tarfile
import os
import inspect


class DataNotReady:
    def __init__(self):
        pass


def line_print(*args, **kwargs):
    frame = inspect.currentframe().f_back
    filename = os.path.basename(frame.f_code.co_filename)
    lineno = frame.f_lineno
    print(f"[{filename}:{lineno}]", *args, **kwargs)


def convert_parquet_to_wds(parquet_path, wds_folder):
    import webdataset
    _, parquet_file_name = os.path.split(parquet_path)
    wds_file_name = os.path.join(wds_folder, parquet_file_name.split(".")[0])
    parquet_file = ParquetFile(parquet_path)
    num_row_groups = parquet_file.num_row_groups
    with wds.TarWriter(f"{wds_file_name}.tar") as tar:
        for rid in range(num_row_groups):
            rg = parquet_file.read_row_group(rid)
            group_data = rg.to_pandas()
            rows = group_data.to_dict('records')
            for i, row in enumerate(rows):
                print(rid, i)
                tar.write(row)
    parquet_file.close()


class TarFileReader:
    def __init__(self, path, columns=None):
        self.tar_file = tarfile.open(path)
        self.names = self.tar_file.getnames()
        if columns is None:
            columns_all = {i.rsplit(".", 1)[-1] for i in self.names}
            columns = list(columns_all)
        self.columns = columns

    def __getitem__(self, key):
        targets = [f"{key}.{column}" for column in self.columns]
        tarinfos = [self.tar_file.getmember(name) for name in targets]
        tarinfos.sort(key=lambda x: x.offset)
        data = {}
        for tarinfo in tarinfos:
            cur_data = self.tar_file.extractfile(tarinfo).read()
            data[tarinfo.name[len(key)+1:]] = cur_data
        return data
    def close(self):
        self.tar_file.close()


def test_parquet(parquet_path):
    t1 = time.time()
    parquet_file = ParquetFile(parquet_path)
    num_row_groups = parquet_file.num_row_groups
    for rid in range(num_row_groups):
        rg = parquet_file.read_row_group(rid)
        group_data = rg.to_pandas()
        rows = group_data.to_dict('records')
    parquet_file.close()
    print(f"parquet test time: {time.time() - t1}s")


def test_tar(tar_file, shuffle=False):
    t1 = time.time()
    r = TarFileReader(tar_file)
    keys = [i.split(".")[0] for i in r.names if i.endswith(".wav")]
    if shuffle:
        random.shuffle(keys)
    for k in keys:
        d = r[k]
    r.close()
    print(f"tar test time: {time.time() - t1}s")
