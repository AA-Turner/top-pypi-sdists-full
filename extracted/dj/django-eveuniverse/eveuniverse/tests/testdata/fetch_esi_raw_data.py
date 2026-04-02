import json
from pathlib import Path

import requests

from eveuniverse.app_settings import EVEUNIVERSE_REQUESTS_DEFAULT_TIMEOUT

TYPE_IDS = [
    34,
    35,
    36,
    37,
    38,
    39,
    40,
    3380,
    21947,
    21949,
    21951,
    21953,
    21955,
    21957,
    21959,
    21961,
    21967,
]

print("Fetching ESI raw data...")

# fetching types from ESI
esi_data = {"categories": {}, "groups": {}, "types": {}}
category_ids = set()
group_ids = set()
print("Fetching types...")
for type_id in TYPE_IDS:
    r = requests.get(
        f"https://esi.evetech.net/latest/universe/types/{type_id}/",
        timeout=EVEUNIVERSE_REQUESTS_DEFAULT_TIMEOUT,
    )
    r.raise_for_status()
    info = r.json()
    esi_data["types"][type_id] = info
    group_ids.add(info["group_id"])

print("Fetching groups...")
for group_id in group_ids:
    r = requests.get(
        f"https://esi.evetech.net/latest/universe/groups/{group_id}/",
        timeout=EVEUNIVERSE_REQUESTS_DEFAULT_TIMEOUT,
    )
    r.raise_for_status()
    info = r.json()
    esi_data["groups"][group_id] = info
    category_ids.add(info["category_id"])

print("Fetching categories...")
for category_id in category_ids:
    r = requests.get(
        f"https://esi.evetech.net/latest/universe/categories/{category_id}/",
        timeout=EVEUNIVERSE_REQUESTS_DEFAULT_TIMEOUT,
    )
    r.raise_for_status()
    info = r.json()
    esi_data["categories"][category_id] = info

# writing raw data
esi_data_path = Path(__file__).parent / "esi_raw_data.json"
with esi_data_path.open("w", encoding="utf-8") as fp:
    json.dump(esi_data, fp, indent=4, sort_keys=True)

print("DONE")
