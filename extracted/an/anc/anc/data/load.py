import os
from typing import Callable, Any, Optional
from functools import wraps

from anc.api.connection import Connection
from anc.conf.remote import remote_server

training_dataset_base_default_path = "/mnt/weka/dvc_data"

def is_rank_zero() -> bool:
    node_rank = int(os.getenv("RANK", "0"))
    if node_rank == 0:
        local_rank = int(os.getenv("LOCAL_RANK", "0"))
        return local_rank == 0
    return False

def rank_zero_only(fn: Callable[..., Any]) -> Callable[..., Optional[Any]]:
    @wraps(fn)
    def wrapped_fn(*args: Any, **kwargs: Any) -> Optional[Any]:
        if is_rank_zero():
            return fn(*args, **kwargs)
        return None
    return wrapped_fn

class Dataload:
    def __init__(self, cfg):
        self._cfg = cfg
        self.dataset_name = None
        self.dataset_version = None
        self.dataset_files = None
        self.dataset_concat_sampling_probabilities = None
        if self._cfg:
            self.dataset_name = self._cfg.data.train_ds.customized_dataset.name
            self.dataset_files = self._cfg.data.train_ds.customized_dataset.files
            self.dataset_version = self._cfg.data.train_ds.customized_dataset.version
            self.dataset_concat_sampling_probabilities = self._cfg.data.train_ds.customized_dataset.concat_sampling_probabilities
    
    def _replace_cfg_data_train_ds_file_names(self, dest_path):
        if not self.dataset_files:
            return
        # reset origin dataset in cfg
        if self._cfg.data.train_ds.file_names is None:
            self._cfg.data.train_ds.file_names = []

        for file in self.dataset_files:
            self._cfg.data.train_ds.file_names.append(dest_path+"/"+file)
            
        if self.dataset_concat_sampling_probabilities:
            if self._cfg.data.train_ds.concat_sampling_probabilities is None:
                self._cfg.data.train_ds.concat_sampling_probabilities = []
            self._cfg.data.train_ds.concat_sampling_probabilities.extend(self.dataset_concat_sampling_probabilities)    

        return self._cfg

    @rank_zero_only
    def download_dataset(self, dataset_name, dataset_version, dest_path):
        # download dataset
        conn = Connection(url=remote_server)
        data = {
            "dataset_name": dataset_name,
            "version": dataset_version,
            "dest_path": dest_path
        }
        try:
            response = conn.post("/get", json=data, stream=True)
            for chunk in response.iter_lines(decode_unicode=True):
                if chunk:
                    print(chunk)
        except Exception as e:
            raise(f"Dataloader error occurred: {e}")
        print("- dataset downloaded.")

    def setup_dataset(self):
        if self.dataset_name is None or self.dataset_version is None:
            print("warning: no customized dataset/version found. Skip data setup ...")
            return
        training_dataset_base_path = os.getenv("training_dataset_base_path", training_dataset_base_default_path)
        dest_path = training_dataset_base_path + '/' + self.dataset_name + "_" + self.dataset_version
        os.makedirs(dest_path, exist_ok=True)
        # We will create a path under training_dataset_base_default_path, e.g. /mnt/weka/dvc_data/train_v1.0
        # when we finished download, we expected that the /mnt/weka/dvc_data/train_v1.0/train will be created.
        # download dataset
        self.download_dataset(self.dataset_name, self.dataset_version, dest_path)
        final_dest_path = dest_path + "/" + self.dataset_name
        updated_cfg = self._replace_cfg_data_train_ds_file_names(final_dest_path)