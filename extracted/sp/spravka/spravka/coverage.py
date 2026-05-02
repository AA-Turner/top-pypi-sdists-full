import os
import yaml
import importlib
import sys
import pprint

BASE_DIR = os.getcwd()
sys.path.append(BASE_DIR)
CONFIG_PATH = os.path.join(BASE_DIR, "spravka.yml")

with open(CONFIG_PATH, 'r') as stream:
    data_loaded = yaml.safe_load(stream)

coverage_obj = {}
coverage_list = []
coverage_sum = {
    "coverage": 0,
    "missing_count": 0,
    "needed_count": 0,
}


def coverage():
    for item_dir in data_loaded.get('dir'):
        for item_module in data_loaded.get('dir').get(item_dir):
            mdl = import_by_path(item_dir, item_module)
            function_list = [i for i in dir(mdl) if (i[:2] + i[-2:]) != '____']
            module_path = get_path_module(item_dir, item_module)
            empty = False
            if os.path.getsize(module_path) == 0:
                empty = True
            coverage_obj_id = f"{os.path.join(item_dir, item_module)}.py"
            coverage_obj[coverage_obj_id] = {
                "coverage": 0.0,
                "missing": [],
                "missing_count": 0,
                "empty": empty,
                "module_doc": bool(mdl.__doc__),
                "needed_count": 1
            }
            coverage_sum["needed_count"] += (1 + len(function_list))
            for i in function_list:
                if vars(mdl).get(i).__globals__.get('__name__') != f'{item_dir}.{item_module}':
                    continue
                if not vars(mdl).get(i).__doc__:
                    coverage_obj[coverage_obj_id]["missing"].append(i)
                    coverage_obj[coverage_obj_id]["missing_count"] += 1
                    coverage_sum["missing_count"] += 1
                coverage_obj[coverage_obj_id]["needed_count"] += 1

            if not mdl.__doc__:
                coverage_obj[coverage_obj_id]["missing_count"] += 1
                coverage_sum["missing_count"] += 1
            coverage_obj[coverage_obj_id]["coverage"] = (100 / coverage_obj[coverage_obj_id]["needed_count"]) * (
                    coverage_obj[coverage_obj_id]["needed_count"] - coverage_obj[coverage_obj_id]["missing_count"])
            coverage_list.append(f'{item_dir}.{item_module}')
    coverage_sum["coverage"] = coverage_sum["missing_count"] * 100 / coverage_sum["needed_count"]

    pprint.pprint(coverage_obj)
    pprint.pprint(coverage_sum)

    return coverage_obj, coverage_sum


def import_by_path(item_dir, item_module):
    mdl = importlib.import_module(f".{item_module}", item_dir)
    return mdl


def get_path_module(pkg, mdl):
    packege_path = os.path.join(os.getcwd(), pkg)
    module_path = os.path.join(packege_path, f'{mdl}.py')
    return module_path
