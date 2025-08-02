# arpakit

import json
import logging
import os
import shutil
from typing import Any, Optional, Self

from arpakitlib.ar_type_util import raise_for_type

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class JSONDbFile:

    def __init__(self, *, filepath: str, use_memory: bool = True, beautify_json: bool = True, **kwargs):
        self._logger = logging.getLogger(self.__class__.__name__)
        raise_for_type(filepath, str)
        filepath = os.path.abspath(filepath.strip())
        if not filepath:
            raise ValueError("not filepath")

        self.filepath = filepath
        self.use_memory = use_memory
        self.beautify_json = beautify_json
        self.saved_json_data: Optional[dict[str, Any]] = None

    def __str__(self) -> str:
        return f"JSONDbFile ({self.filepath}) ({self.count_records()})"

    def __repr__(self) -> str:
        return f"JSONDbFile ({self.filepath}) ({self.count_records()})"

    def __len__(self) -> int:
        return self.count_records()

    @property
    def filename(self) -> str:
        return os.path.split(self.filepath)[1]

    @property
    def dirpath(self) -> str:
        return os.path.split(self.filepath)[0]

    def write_json_data(self, json_data: dict[str, Any]):
        raise_for_type(json_data, dict)

        if self.dirpath and not os.path.exists(self.dirpath):
            os.makedirs(self.dirpath, exist_ok=True)

        with open(self.filepath, mode="w", encoding="utf-8") as f:
            f.write(json.dumps(json_data, ensure_ascii=False, indent=2 if self.beautify_json else None))

        if self.use_memory is True:
            self.saved_json_data = json_data

    def read_json_data(self) -> dict[str, Any]:
        if self.use_memory is True and self.saved_json_data is not None:
            return self.saved_json_data

        if not self.check_exists():
            self.write_json_data({})

        with open(self.filepath, mode="r", encoding="utf-8") as f:
            text_from_file = f.read()
        json_data = json.loads(text_from_file)

        if self.use_memory is True:
            self.saved_json_data = json_data

        return json_data

    def init(self):
        if not self.check_exists():
            self.write_json_data({})

    def reinit(self):
        self.drop()
        self.init()

    def refresh_saved_json_data(self):
        if self.use_memory is True:
            self.saved_json_data = self.read_json_data()

    def get_records(self) -> list[(str, dict[str, Any])]:
        return [(record_id, record) for record_id, record in self.read_json_data().items()]

    def get_record_ids(self) -> list[str]:
        return [record_id for record_id in self.read_json_data().keys()]

    def check_exists(self) -> bool:
        return os.path.exists(self.filepath)

    def check_record_id_exists(self, record_id: str) -> bool:
        return self.get_record(record_id=record_id) is not None

    def count_records(self) -> int:
        return len(self.read_json_data().keys())

    def get_record(self, record_id: str) -> Optional[dict[str, Any]]:
        raise_for_type(record_id, str)
        json_data = self.read_json_data()
        return json_data[record_id] if record_id in json_data.keys() else None

    def generate_record_id(self) -> str:
        record_ids = set(self.get_record_ids())
        res = len(record_ids)
        while str(res) in record_ids:
            res += 1
        return str(res)

    def create_record(
            self,
            record: dict[str, Any],
            record_id: Optional[str] = None,
    ) -> (str, dict[str, Any]):
        if record_id is None:
            record_id = self.generate_record_id()
        raise_for_type(record_id, str)

        json_data = self.read_json_data()
        if record_id in json_data.keys():
            raise KeyError(f"record with record_id={record_id} already exists")

        json_data[record_id] = record
        self.write_json_data(json_data=json_data)

        return record_id, record

    def update_record(
            self,
            *,
            record_id: str,
            record: dict[str, Any]
    ) -> dict[str, Any]:
        raise_for_type(record_id, str)
        raise_for_type(record, dict)

        json_data = self.read_json_data()
        if record_id not in json_data.keys():
            raise ValueError(f"record with record_id='{record_id}' not exists")

        json_data[record_id] = record
        self.write_json_data(json_data)

        return record

    def rm_record(self, record_id: str):
        json_data = self.read_json_data()
        if record_id not in json_data.keys():
            return
        del json_data[record_id]
        self.write_json_data(json_data)

    def rm_records(self, record_ids: list[str]):
        json_data = self.read_json_data()
        for record_id, record in json_data.items():
            if record_id not in record_ids:
                continue
            del json_data[record_id]
        self.write_json_data(json_data)

    def rm_all_records(self):
        self.write_json_data({})

    def copy(self, to_filepath: str):
        self.init()
        shutil.copy(self.filepath, to_filepath)
        return JSONDbFile(filepath=to_filepath, use_memory=self.use_memory, beautify_json=self.beautify_json)

    def drop(self):
        if self.check_exists():
            os.remove(self.filepath)


class BaseJSONDb:

    def __init__(self, json_db_files: list[JSONDbFile] | None = None, **kwargs):
        self._logger = logging.getLogger(self.__class__.__name__)
        if json_db_files is None:
            json_db_files = []
        self.json_db_files: list[JSONDbFile] = json_db_files

    def __str__(self) -> str:
        return f"JSONDbFiles ({len(self.json_db_files)})"

    def __repr__(self) -> str:
        return f"JSONDbFiles ({len(self.json_db_files)})"

    def __len__(self) -> int:
        return len(self.json_db_files)

    def create_json_db_file(
            self, filepath: str, use_memory: bool = False, beautify_json: bool = False, **kwargs
    ) -> JSONDbFile:
        json_db_file = JSONDbFile(filepath=filepath, use_memory=use_memory, beautify_json=beautify_json)
        self.json_db_files.append(json_db_file)
        return json_db_file

    def add_json_db_file(self, json_db_file: JSONDbFile):
        self.json_db_files.append(json_db_file)

    def init(self):
        for file in self.json_db_files:
            file.init()

    def reinit(self):
        for file in self.json_db_files:
            file.reinit()

    def drop(self):
        for file in self.json_db_files:
            file.drop()

    def rm_all_records(self):
        for json_db_file in self.json_db_files:
            json_db_file.rm_all_records()

    def copy_files_to_dir(self, to_dirpath: str) -> Self:
        json_db = BaseJSONDb()
        for json_db_file in self.json_db_files:
            filepath = os.path.join(to_dirpath, json_db_file.filename)
            json_db_file.copy(filepath)
            json_db.create_json_db_file(
                filepath=filepath, use_memory=json_db_file.use_memory, beautify_json=json_db_file.beautify_json
            )
        return json_db


def __example():
    pass


if __name__ == '__main__':
    __example()
