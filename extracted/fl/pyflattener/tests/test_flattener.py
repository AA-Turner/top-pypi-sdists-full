import json
from pyflattener import Flattener, clean_xmltodict_result, do_flatten, unflatten
import pytest
from deepdiff import DeepDiff
import os
file_path = os.path.dirname(os.path.abspath(__file__))


DATACHECK_FILE = "data.json"  # File to check data against
DATASAVE_FILE = "data2.json"  # File to save data to (should be the same as above unless testing)

SAVE_NEW_DATA = False
# If true, Don't check for data in memory since it doesn't exist (used for new params, skips assertions)
# If making and saving new data, make sure to uncomment last line of this file
# If False, run as normal


with open(os.path.join(file_path, DATACHECK_FILE), "r") as fp:
    data_to_check = json.load(fp)

data_to_flatten = [
    ("combine_ints", [{"a": 1, "b": 4, "c": 7}, {"a": 2, "b": 5, "c": 8}, {"a": 3, "b": 6, "c": 9}]),
    ("nested_dicts.json", json.load(open(os.path.join(file_path, "nested_dicts.json"), "r"))),
    ("list_dicts.json", json.load(open(os.path.join(file_path, "list_dicts.json"), "r"))),
    ("single_list", [1, 2, 3]),
    ("key_collision", {"asdf": [1, 2], "test": [{"asdf": "val1"}, {"asdf": "val2"}]})
]

indexes = {name[0]: index for index, name in enumerate(data_to_flatten)}

outputs = {}
# Careful not to overparametrize, the number of tests will explode exponentially
p_keycount = ["data_name", ["nested_dicts.json"]]
p_test_data = ["test_data", data_to_flatten]
p_prefix = ["prefix", [None, "a_d_gfs", " "]]
p_stringify = ["stringify", [None, True, False]]
p_shallow = ["shallow", [None, True, False]]
p_autoparse_dts = ["autoparse_dts", [True, False]]
p_oldest_dt_allowed = ["oldest_dt", ["2005", None]]
p_special_dt_fmts = ["special_dt_fmts", [["YYYY-mm-dd"]]]
p_keep_simple_lists = ["simple_lists", [True, False]]


def dict_key_count(d, c=0):
    if isinstance(d, list):
        return len(d)

    for k, v in d.items():
        if isinstance(v, dict):
            c = c + dict_key_count(v)
        else:
            c = c + 1
    return c


# @pytest.mark.parametrize(*p_keycount)
# @pytest.mark.parametrize(*p_prefix)
# @pytest.mark.parametrize(*p_stringify)
# @pytest.mark.parametrize("shallow", [None, False])  # Removed "True" since shallow flattening removes keys
# def test_nested_dicts(data_name, prefix, stringify, shallow):
#     if not SAVE_NEW_DATA:
#         # Make sure that we didn't lose any keys in the nested_dicts test
#         fl = Flattener(prefix=prefix, stringify_lists=stringify, shallow_flatten=shallow)
#
#         flat = dict_key_count(fl.flatten(data_to_flatten[indexes[data_name]][1]))
#         check = dict_key_count(data_to_flatten[indexes[data_name]][1])
#         assert flat == check


@pytest.mark.parametrize(*p_test_data)
@pytest.mark.parametrize(*p_prefix)
@pytest.mark.parametrize(*p_stringify)
@pytest.mark.parametrize(*p_shallow)
@pytest.mark.parametrize(*p_autoparse_dts)
@pytest.mark.parametrize(*p_oldest_dt_allowed)
@pytest.mark.parametrize(*p_special_dt_fmts)
@pytest.mark.parametrize(*p_keep_simple_lists)
def test_datas(test_data, prefix, stringify, shallow, autoparse_dts, oldest_dt, special_dt_fmts, simple_lists):
    name = test_data[0] + "_" + "_".join([str(prefix), str(stringify), str(shallow), str(autoparse_dts), str(oldest_dt),
                                          str(special_dt_fmts), str(simple_lists)])

    fl = Flattener(prefix=prefix, stringify_lists=stringify, shallow_flatten=shallow, autoparse_dt_strs=autoparse_dts,
                   oldest_dt_allowed=oldest_dt, keep_simple_lists=simple_lists, special_dt_formats=special_dt_fmts)

    flat = fl.flatten(test_data[1])

    outputs[name] = flat
    if not SAVE_NEW_DATA:
        check = data_to_check[name]
        # It's okay if the lists are out of order, as long as they contain the same stuff (Python 2 & 3 compatibility fix)
        if isinstance(flat, list) and isinstance(check, list) and not isinstance(flat[0], dict) and not isinstance(
                check[0], dict):
            assert set(flat) == set(data_to_check[name])
        else:
            assert flat == data_to_check[name]


@pytest.mark.parametrize("data", [json.load(open(os.path.join(file_path, "xmltodict.json"), "r"))])
def test_clean_xmltodict(data):
    clean_xmltodict_result(data)
    # TODO Add more tests if needed


tests = json.load(open(os.path.join(file_path, 'flattener_individual_test_cases.json')))

@pytest.mark.parametrize('input_vars,expected_output', [(x['inputs'], x['expected_output']) for x in tests])
def test_parser(input_vars, expected_output):
    # Added to combat the default True value
    if "add_raw_json" not in input_vars:
        input_vars["add_raw_json"] = False

    flat = do_flatten(**input_vars)
    if isinstance(flat, list):
        flat = [x.todict() for x in flat]
    else:
        flat = flat.todict()
    assert str(DeepDiff(expected_output, flat, ignore_order=True)) == '{}'


def test_basictype_lists():
    fl = Flattener()
    data = fl.flatten({"a": [1, 2, 3], "b": ["d", "e", "f"], "c": [1, "g", 3]})
    assert data == {"a": [1, 2, 3], "b": ["d", "e", "f"], "c": "1,g,3"}


def test_ignore_dts():
    assert Flattener(ignore_dt_formats=["\d\-\d\d"]).flatten({"a": "5-22-19"})["a"] == "5-22-19"
    assert Flattener(autoparse_dt_strs=True, ignore_dt_formats=[]).flatten({"a": "5-22-19"})["a"] != "5-22-19"


def test_nestedlist_fix():
    # Test to test specific edgecases of flattening nested data
    data = {
        "key1": "value1",
        "key2": 2,
        "key3": {
            "subkey1": [
                {"a": 1},
                {"a": 1}
            ],
            "subkey2": [
                {"b": [2]},
                {"b": [2]}
            ],
            "subkey3": [
                {"c": [3]},
                {"c": []}
            ],
            "subkey4": [
                {"c": []},
                {"c": []}
            ],
            "subkey5": [
                {"d": [4]},
                {"d": 4}
            ]
        }
    }

    Flattener().flatten(data)


with open(os.path.join(file_path, 'unflatten_individual_test_cases.json'), 'r') as f:
    unflatten_tests = json.load(f)

@pytest.mark.parametrize('inputs,expected_output', [(x['inputs'], x['expected_output']) for x in unflatten_tests])
def test_unflatten(inputs, expected_output):
    nested = unflatten(**inputs)
    assert str(DeepDiff(expected_output, nested, ignore_order=True)) == '{}'


def save_outputs():
    with open(os.path.join(file_path, DATASAVE_FILE), "w") as f:
        json.dump(outputs, f)


@pytest.fixture(scope="session", autouse=True)
def test_main():
    tw = 2
    yield None

    # save_outputs()  # ONLY SAVE OUTPUTS IF TESTS PASS, OVERWRITES, Make sure to uncomment if SAVE_NEW_DATA == True
