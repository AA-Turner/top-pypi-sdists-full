import os
import sys
from io import StringIO
from typing import Optional, TextIO, List, NamedTuple

import pytest
import requests
from dict_compare import compare_dicts
from jsonasobj import loads as jao_loads
from pyjsg.jsglib.loader import loads as jsg_loads, is_valid

from ShExJSG import ShExJ
from tests import shexTestRepository

# If not empty, validate this single file
shexTestJson: str = None
# shexTestJson = "https://raw.githubusercontent.com/shexSpec/shexTest/2.0/schemas/" \
#                "1refbnode_with_spanning_PN_CHARS_BASE1.json"

STOP_ON_ERROR = False
VERBOSE = False

skip = ['coverage.json', 'manifest.json', 'representationTests.json']


class ExampleTestFile(NamedTuple):
    fullpath: str
    filename: str


def compare_json(j1: str, j2: str, log: TextIO) -> bool:
    d1 = jao_loads(j1)
    d2 = jao_loads(j2)
    return compare_dicts(d1._as_dict, d2._as_dict, file=log)


def validate_shexj_json(json_str: str, input_fname: str) -> bool:
    logger = StringIO()
    shex_obj = jsg_loads(json_str, ShExJ)
    if not is_valid(shex_obj, logger):
        print(f"File: {input_fname} - ")
        print(logger.getvalue())
        return False
    elif not compare_json(json_str, shex_obj._as_json, logger):
        print(f"File: {input_fname} - ")
        print(logger.getvalue())
        print(shex_obj._as_json_dumps())
        return False
    return True


def validate_file(file: ExampleTestFile) -> tuple[bool, bool]:
    """Returns (passed, skipped)."""
    if file.filename in skip:
        return True, True
    if VERBOSE:
        print(f"Testing {file.fullpath}")
    if ':' in file.fullpath:
        resp = requests.get(file.fullpath)
        if not resp.ok:
            print(f"Error {resp.status_code}: {resp.reason}")
            return False, False
        file_text = resp.text
    else:
        with open(file.fullpath, 'rb') as f:
            file_text = f.read().decode()
    return validate_shexj_json(file_text, file.fullpath), False


def download_github_file(github_url: str) -> Optional[str]:
    print(f"Downloading {github_url}")
    resp = requests.get(github_url)
    if resp.ok:
        resp = requests.get(resp.json()['download_url'])
        if resp.ok:
            return resp.text
    print(f"Error {resp.status_code}: {resp.reason}")
    return None


def enumerate_http_files(url) -> List[ExampleTestFile]:
    resp = requests.get(url)
    if resp.ok:
        for f in resp.json():
            yield ExampleTestFile(f['download_url'], f['name'])
    else:
        print(f"Error {resp.status_code}: {resp.reason}", file=sys.stderr)


def enumerate_directory(dir_) -> List[ExampleTestFile]:
    for fname in os.listdir(dir_):
        fpath = os.path.join(dir_, fname)
        if os.path.isfile(fpath):
            yield ExampleTestFile(fpath, fname)


def get_test_files() -> List[ExampleTestFile]:
    if shexTestJson:
        return [ExampleTestFile(shexTestJson, shexTestJson.rsplit('/')[1])]
    if ':' in shexTestRepository:
        return list(enumerate_http_files(shexTestRepository))
    return list(enumerate_directory(shexTestRepository))


def pytest_generate_tests(metafunc):
    if "shex_file" in metafunc.fixturenames:
        files = [f for f in get_test_files() if f.filename.endswith('.json')]
        metafunc.parametrize("shex_file", files, ids=[f.filename for f in files])


def test_shex_schema(shex_file: ExampleTestFile):
    """Download the contents of the shexTestRepository and make sure that they can all be correctly loaded as
    ShExJSG images.
    """
    passed, skipped = validate_file(shex_file)
    if skipped:
        pytest.skip(f"Skipping {shex_file.filename}")
    assert passed, f"Validation failed for {shex_file.fullpath}"
