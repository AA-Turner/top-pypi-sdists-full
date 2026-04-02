import json
from pathlib import Path


def _load_sde_data() -> dict:
    esi_data_path = Path(__file__).parent / "sde_data.json"
    with esi_data_path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


sde_data = _load_sde_data()


def type_materials_cache_content():
    return cache_content(table="type_materials")


def cache_content(table):
    data_all = {}
    cached_data = sde_data[table]
    for row in cached_data:
        type_id = row["typeID"]
        if type_id not in data_all:
            data_all[type_id] = []
        data_all[type_id].append(row)
    return data_all
