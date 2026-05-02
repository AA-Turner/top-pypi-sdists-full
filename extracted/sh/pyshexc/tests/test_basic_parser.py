from contextlib import redirect_stdout
from io import StringIO
from typing import Optional

import pytest
import requests
from ShExJSG import ShExJ
from dict_compare import compare_dicts, json_filtr
from jsonasobj import loads as jao_loads, as_json, as_dict
from pyjsg.jsglib.loader import loads as jsg_loads
from pyjsg.jsglib.logger import Logger

from pyshexc.parser_impl.generate_shexj import parse
from tests import schemas_base
from tests.utils.build_test_harness import ValidationTestConfig
from tests.utils.shape_decl_wrapper import rewrap_shape_decls

#
# Starting file name (full URL) (with or without ".shex" suffix)
START_AT = "2dot"

# False if you want to start somewhere in the middle
SINGLE_FILE = bool(START_AT)

issue_43 = 'Broken test case - see shexTest issue #43'

skip = {
    "start2RefS2.shex": issue_43
}


class MemLogger:
    def __init__(self, prefix: Optional[str] = None):
        self.prefix = prefix
        self.log = ""

    def write(self, txt):
        self.log += self.prefix + txt


def compare_json(shex_url: str, shex_json: str, log: Logger) -> bool:
    json_url = shex_url.rsplit(".", 1)[0] + ".json"
    if ':' in json_url:
        resp = requests.get(json_url)
        if not resp.ok:
            return False
        json_text = resp.text
    else:
        try:
            with open(json_url) as f:
                json_text = f.read()
        except FileNotFoundError:
            print(f"****> {json_url} not found. Comparison not done ***")
            return True
    d1 = jao_loads(json_text)
    d2 = jao_loads(shex_json)
    if not compare_dicts(as_dict(d1), as_dict(d2), d1name="expected", d2name="actual  ", file=log, filtr=json_filtr):
        print(as_json(d2))
        return False
    return True


def validate_shexc(shexc_str: str, input_fname: str) -> bool:
    shexj = parse(shexc_str)
    if shexj is None:
        return False
    shexj['@context'] = "http://www.w3.org/ns/shex.jsonld"
    shex_obj = jsg_loads(as_json(shexj), ShExJ)
    shex_obj = rewrap_shape_decls(shex_obj)
    log = StringIO()
    rval = True
    with redirect_stdout(log):
        if not shex_obj._is_valid():
            rval = False
        elif not compare_json(input_fname, as_json(shex_obj), log):
            rval = False
    if not rval:
        print("File: {} - ".format(input_fname))
        print(log.getvalue())
    return rval


def validate_file(download_url: str) -> bool:
    if ':' in download_url:
        resp = requests.get(download_url)
        if resp.ok:
            return validate_shexc(resp.text, download_url)
        else:
            print("Error {}: {}".format(resp.status_code, resp.reason))
            return False
    else:
        with open(download_url, 'rb') as f:
            return validate_shexc(f.read().decode(), download_url)


class BasicParserTestCase(ValidationTestConfig):
    pass


BasicParserTestCase.repo_url = schemas_base
BasicParserTestCase.file_suffix = ".shex"
BasicParserTestCase.start_at = START_AT
BasicParserTestCase.single_file = SINGLE_FILE
BasicParserTestCase.skip = skip
BasicParserTestCase.validation_function = validate_file
BasicParserTestCase.build_test_harness()


@pytest.mark.parametrize("download_url", BasicParserTestCase.build_test_harness())
def test_shexc_file(download_url: str) -> None:
    if download_url in skip:
        pytest.skip(skip[download_url])
    assert validate_file(download_url)