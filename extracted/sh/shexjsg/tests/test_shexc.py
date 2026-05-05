import os
import sys
from io import StringIO
from typing import NamedTuple, List, TextIO

import pytest
import requests
from dict_compare import compare_dicts
from jsonasobj import loads as jao_loads
from pyjsg.jsglib import loads as jsg_loads
from pyjsg.jsglib.loader import is_valid

from ShExJSG import ShExJ, ShExC
from tests import SHEXC_INSTALLED, shexTestRepository
from tests.utils.shape_decl_wrapper import rewrap_shape_decls

if SHEXC_INSTALLED:
    from pyshexc.parser_impl.generate_shexj import parse

# If not empty, validate this single file
testShexFile: str = ""

STOP_ON_ERROR = False
VERBOSE = False

NOT_SHEX_FILE = "Not a ShExJ file"
NESTED_AND = "e1 AND (e2 AND e3) vs. e1 AND e2 AND e3"
SEMACT_CHARS = "semAct escapes still need doing"
PATTERN_CHARS = "pattern escapes still need doing"
LITERAL_CHARS = "literal escapes need doing"
USES_IMPORTS = "Imports is a 2.1 feature"
INSANE_BNODE = "Insane BNODE Identifiers"

skip = {
    'coverage.json': NOT_SHEX_FILE,
    'manifest.json': NOT_SHEX_FILE,
    'representationTests.json': NOT_SHEX_FILE,
}

if testShexFile and not testShexFile.endswith(".json"):
    testShexFile += ".json"

for k in list(skip.keys()):
    if not k.endswith(".json"):
        skip[k + '.json'] = skip[k]
        del skip[k]


class ExampleTestFile(NamedTuple):
    fullpath: str
    filename: str


def compare_json(j1: str, j2: str, log: TextIO) -> bool:
    d1 = jao_loads(j1)
    d2 = jao_loads(j2)
    return compare_dicts(d1._as_dict, d2._as_dict, file=log)


def validate_shexc_json(json_str: str, input_fname: str) -> bool:
    logger = StringIO()
    shex_json: ShExJ.Schema = jsg_loads(json_str, ShExJ)
    if not is_valid(shex_json, logger):
        print(f"File: {input_fname} - ")
        print(logger.getvalue())
        return False
    shexc_str = str(ShExC(shex_json))
    output_shex_obj = parse(shexc_str)
    output_shex_obj = rewrap_shape_decls(output_shex_obj)
    if output_shex_obj is None:
        print(f"{input_fname}")
        for number, line in enumerate(shexc_str.split('\n')):
            print(f"{number + 1}: {line}")
        return False
    output_shex_obj["@context"] = "http://www.w3.org/ns/shex.jsonld"
    rval = compare_json(json_str, output_shex_obj._as_json_dumps(), logger)
    if not rval:
        print(shexc_str)
        print(logger.getvalue())
    return rval


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
    if testShexFile:
        return [ExampleTestFile(os.path.join(shexTestRepository, testShexFile), testShexFile)]
    if ':' in shexTestRepository:
        return list(enumerate_http_files(shexTestRepository))
    return list(enumerate_directory(shexTestRepository))


def validate_file(file: ExampleTestFile) -> tuple[bool, str | None]:
    """Returns (passed, skip_reason) where skip_reason is None if not skipped."""
    if file.filename in skip:
        return True, skip[file.filename]
    if VERBOSE:
        print(f"Testing {file.fullpath}")
    if ':' in file.fullpath:
        resp = requests.get(file.fullpath)
        if not resp.ok:
            print(f"Error {resp.status_code}: {resp.reason}")
            return False, None
        file_text = resp.text
    else:
        with open(file.fullpath) as f:
            file_text = f.read()
    return validate_shexc_json(file_text, file.fullpath), None


def pytest_generate_tests(metafunc):
    if "shex_file" in metafunc.fixturenames:
        files = [f for f in get_test_files() if f.filename.endswith('.json')]
        metafunc.parametrize("shex_file", files, ids=[f.filename for f in files])


@pytest.mark.skipif(not SHEXC_INSTALLED, reason="ShExC must be installed to run this test")
def test_shex_schema(shex_file: ExampleTestFile):
    """1) Convert the contents of the shexTest/schema's directory into ShExJSG
       2) Convert the ShExJSG into ShExC
       3) Parse the ShExC back into ShExJSG
       4) Compare the input and output JSG's
    """
    passed, skip_reason = validate_file(shex_file)
    if skip_reason:
        pytest.skip(skip_reason)
    assert passed, f"Validation failed for {shex_file.fullpath}"
