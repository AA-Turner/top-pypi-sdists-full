import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from pprint import pprint
from typing import List, Optional, Tuple, Union

import yaml

from .database import Database


@dataclass
class Archive:
    """Archive Object"""

    date: datetime
    payload: str
    key: str
    field_1: Optional[Union[str, dict]]
    field_2: Optional[Union[str, dict]]

    def to_json(self) -> dict:
        """Converts class to json"""
        return {"key": self.key, "date": self.date, "payload": self.payload}


class Runtime:
    """Runtime Object"""

    source_data: dict = {}
    target_data: dict = {}
    archives: List = []
    source: Union[str, Path] = ""
    target: Optional[Union[str, Path]] = None
    database: Optional[Database] = None
    database_information: Optional[Tuple[str, dict]] = None

    def __init__(
        self, source: str, target: Optional[str] = None, database: bool = False
    ):
        """Init function

        :param source: Source target host or target file
        :param target: Optional, output file
        """
        self.source = Path(source)
        self.target = target
        self.source_data = {}
        self.target_data = {}
        self.archives = []

        if database:
            with open(Path(target)) as f:
                secrets = yaml.load(f)
            self.database_information = (source, secrets)

        else:
            if self.source.exists():
                with open(self.source, "r") as source_file:
                    self.source_data = json.load(source_file)

            if not self.target and not self.source.exists():
                self.target = self.source

            if not self.target:
                today = datetime.today()
                file_name = f"{today.day}-{today.month}-{today.hour}-{today.minute}-{today.second}.json"
                self.target = Path(f"{self.source.parent}/{file_name}")

            self.target = Path(self.target)

    def archive(
        self,
        location: str,
        payload: str,
        field_1: Optional[dict] = None,
        field_2: Optional[dict] = None,
        sql: Optional[str] = None,
    ) -> None:
        """Archives the file"""

        arch = Archive(
            str(datetime.now()),
            payload,
            hashlib.md5(payload.encode("utf-8")).hexdigest(),
            field_1,
            field_2,
        )
        self.archives.append(arch)

        if self.database_information:
            if not sql:
                raise ValueError("Missing sql statement")
            if "INSERT" not in sql:
                raise ValueError("Missing 'INSERT' statement")

            h, s = self.database_information
            with Database(s, h) as db:
                with db.engine.connect() as con:
                    con.execute(sql, payload)

        else:
            location = Path(location)
            with open(location, "w") as archive_output:
                json.dump(arch.to_json(), archive_output)

    def print_archive(self, target: int = 0) -> None:
        """Prints the target"""
        pprint(self.archives[-target:], indent=4)

    def save(self) -> None:
        """Saves the runtime file"""
        with open(self.target, "w") as target_file:
            write_dictionary = (
                {**self.source_data, **self.target_data}
                if self.source_data
                else self.target_data
            )
            json.dump(write_dictionary, target_file, indent=4)

    def __enter__(self):
        """Entry context, loads the file"""
        return self

    def __exit__(self, type, value, traceback) -> None:
        """Exit context, saves target_data"""
        self.save()
