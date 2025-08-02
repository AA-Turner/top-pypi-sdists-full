# arpakit

import logging
from datetime import datetime
from typing import Optional, Any

import pytz
from pydantic import BaseModel

from arpakitlib.ar_json_db_util import JSONDbFile
from arpakitlib.ar_type_util import raise_for_type

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class CacheBlock(BaseModel):
    key: str
    data: Any
    last_update_dt: datetime


class CacheFile:

    def __init__(self, *, json_db_file: JSONDbFile):
        self.json_db_file = json_db_file
        self._logger = logging.getLogger(self.__class__.__name__)

    def __len__(self) -> int:
        return self.json_db_file.count_records()

    def __str__(self) -> str:
        return f"CacheFile ({self.json_db_file.filepath}) ({self.json_db_file.count_records()})"

    def __repr__(self) -> str:
        return f"CacheFile ({self.json_db_file.filepath}) ({self.json_db_file.count_records()})"

    def create_block(
            self,
            *,
            key: str,
            data: Any,
            last_update_dt: Optional[datetime] = None
    ) -> CacheBlock:
        raise_for_type(key, str)

        if last_update_dt is None:
            last_update_dt = datetime.now(tz=pytz.UTC)
        raise_for_type(last_update_dt, datetime)
        last_update_dt = last_update_dt.astimezone(tz=pytz.UTC)

        _, record = self.json_db_file.create_record(
            record_id=key,
            record={
                "data": data,
                "last_update_dt": last_update_dt.isoformat()
            }
        )

        return CacheBlock(
            key=key,
            data=record["data"],
            last_update_dt=datetime.fromisoformat(record["last_update_dt"])
        )

    def get_block(self, key: str) -> Optional[CacheBlock]:
        raise_for_type(key, str)

        record = self.json_db_file.get_record(record_id=key)
        if record is None:
            return None

        return CacheBlock(
            key=key,
            data=record["data"],
            last_update_dt=datetime.fromisoformat(record["last_update_dt"])
        )

    def get_blocks(self) -> list[CacheBlock]:
        return [
            CacheBlock(
                key=record_id,
                data=record["data"],
                last_update_dt=datetime.fromisoformat(record["last_update_dt"])
            )
            for record_id, record in self.json_db_file.get_records()
        ]

    def update_block(
            self,
            *,
            key: str,
            data: Optional[dict[str, Any]] = None,
            last_update_dt: Optional[datetime] = None
    ) -> CacheBlock:
        raise_for_type(key, str)
        record = self.json_db_file.get_record(record_id=key)
        if record is None:
            raise ValueError(f"block (key='{key}') not exists")

        if data is not None:
            raise_for_type(data, dict)
            record["data"] = data

        if last_update_dt is not None:
            raise_for_type(last_update_dt, datetime)
            last_update_dt = last_update_dt.astimezone(tz=pytz.UTC)
            record["last_update_dt"] = last_update_dt.isoformat()

        self.json_db_file.update_record(record_id=key, record=record)

        return self.get_block(key=key)

    def remove_block(self, key: str):
        raise_for_type(key, str)
        self.json_db_file.rm_record(record_id=key)

    def remove_blocks(self):
        self.json_db_file.rm_all_records()


def __example():
    pass


if __name__ == '__main__':
    __example()
