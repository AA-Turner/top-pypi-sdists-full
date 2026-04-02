import json
from pathlib import Path

import requests

print("Generating SDE data...")

# fetch type materials from SDE bridge
r = requests.get("https://sde.eve-o.tech/latest/invTypeMaterials.json")
r.raise_for_status()
data_all = r.json()

# fetch type IDs from current test data
esi_data_path = Path(__file__).parent / "esi_data.json"
with esi_data_path.open("r", encoding="utf-8") as fp:
    esi_data = json.load(fp)

# extract needed items only
existing_type_ids = set(
    map(int, esi_data["Universe"]["get_universe_types_type_id"].keys())
)
data_excerpt = [row for row in data_all if row["typeID"] in existing_type_ids]
sde_data = {"type_materials": data_excerpt}

# write sde data
sde_data_path = Path(__file__).parent / "sde_data.json"
with sde_data_path.open("w", encoding="utf-8") as fp:
    json.dump(sde_data, fp, indent=4, sort_keys=True)

# check data consistency
missing_type_ids = []
material_type_ids = {row["materialTypeID"] for row in data_excerpt}
for type_id in material_type_ids:
    if type_id not in existing_type_ids:
        missing_type_ids.append(type_id)

print(f"ERROR: Missing type IDs {', '.join(map(str, sorted(material_type_ids)))}")
print("DONE")
