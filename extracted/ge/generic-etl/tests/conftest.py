import json
import shutil
import pathlib
from unittest.mock import MagicMock

import pytest

CONTENT = {"foo": "bar"}
CSV_DATA_ONE = [
    "index,name,area",
    "0,test1,rw",
    "1,test2,mb",
    "2,test3,x",
    "3,test4,y",
    "4,test5,z",
]
CSV_DATA_TWO = [
    "index,name,area",
    "0,test1,bb",
    "1,test2,cc",
    "21,test3,rw",
    "32,test4,mb",
    "55,test5,x",
]


@pytest.fixture
def generate_paths(tmp_path: pathlib.Path):
    def _generate(create: bool = False):
        source = tmp_path / "source.json"
        target = tmp_path / "target.json"

        if create:
            source.parent.mkdir(exist_ok=True)
            source.write_text(json.dumps(CONTENT))

        yield source
        yield target

        shutil.rmtree(source, ignore_errors=True)

    return _generate


@pytest.fixture
def generate_intersection(tmp_path: pathlib.Path):
    def _generate():
        source = tmp_path / "csv1.csv"
        target = tmp_path / "csv2.csv"

        source.parent.mkdir(exist_ok=True)
        target.parent.mkdir(exist_ok=True)

        # create some data!
        source.write_text("\n".join(CSV_DATA_ONE))
        target.write_text("\n".join(CSV_DATA_TWO))

        yield source
        yield target
        yield tmp_path

        shutil.rmtree(source, ignore_errors=True)
        shutil.rmtree(target, ignore_errors=True)

    return _generate
