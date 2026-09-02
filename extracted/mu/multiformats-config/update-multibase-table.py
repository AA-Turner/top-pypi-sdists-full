"""
    Pulls the current multibase table from the [multibase spec](https://github.com/multiformats/multibase)
"""

import csv
import io
import json
import pprint
import textwrap
from numpy import character

# not a dependency for the `multiformats` library
import requests

from multiformats import multibase
from multiformats_config.multibase import build_multibase_tables


# Fetches and validates the new multibase table from the multibase spec GitHub repo:
multibase_table_url = "https://github.com/multiformats/multibase/raw/master/multibase.csv"
print("Fetching multibase table from:")
print(multibase_table_url)
print()

new_bytes = requests.get(multibase_table_url).content
new_text = new_bytes.decode("utf-8")
print("Building new multibase table...")
reader = csv.DictReader(io.StringIO(new_text))
rows = [{k.strip(): v.strip() for k, v in row.items()} for row in reader]
for r, row in enumerate(rows):
    if sorted(row.keys()) != ['Unicode', 'character', 'description', 'encoding', 'status']:
        raise ValueError(
            f"Unexpected columns in row {r}: {sorted(row.keys())}"
        )
    if not row["Unicode"].startswith("U+"):
        raise ValueError(
            f"In row {r}, expected row['Unicode'] to start with 'U+', found {row['Unicode']}."
        )
    code = "\x00" if (row_code:=row["character"]) == "NUL" else row_code
    if code != chr(int(row["Unicode"][2:], 16)):
        raise ValueError(
            f"In row {r}, expected row['character'] to be "
            f"{chr(int(row['Unicode'][2:], 16))!r}, found {code!r}."
        )
encodings = [
    multibase.Multibase(
        name="identity" if row_code == "NUL" else row["encoding"],
        code="\x00" if row_code == "NUL" else row_code,
        status=row["status"],
        description=row["description"]
    )
    for row in rows
    if (row_code:=row["character"]) == "NUL" or row["encoding"] != "none"
]
new_table, _ = build_multibase_tables(encodings)

# Loads and validates the current multibase table:
print("Building current multibase table...")
with open("multiformats_config/multibase-table.csv", "r", encoding="utf8") as f:
    current_text = f.read()
reader = csv.DictReader(io.StringIO(current_text))
rows = [{k.strip(): v.strip() for k, v in row.items()} for row in reader]
for r, row in enumerate(rows):
    if sorted(row.keys()) != ['Unicode', 'character', 'description', 'encoding', 'status']:
        raise ValueError(
            f"Unexpected columns in row {r}: {sorted(row.keys())}"
        )
    if not row["Unicode"].startswith("U+"):
        raise ValueError(
            f"In row {r}, expected row['Unicode'] to start with 'U+', found {row['Unicode']}."
        )
    code = "\x00" if (row_code:=row["character"]) == "NUL" else row_code
    if code != chr(int(row["Unicode"][2:], 16)):
        raise ValueError(
            f"In row {r}, expected row['character'] to be "
            f"{chr(int(row['Unicode'][2:], 16))!r}, found {code!r}."
        )
encodings = [
    multibase.Multibase(
        name="identity" if row_code == "NUL" else row["encoding"],
        code="\x00" if row_code == "NUL" else row_code,
        status=row["status"],
        description=row["description"]
    )
    for row in rows
    if (row_code:=row["character"]) == "NUL" or row["encoding"] != "none"
]
current_table, _ = build_multibase_tables(encodings)

print()

# Displays added encodings, if any:
added = {
    code: m
    for code, m in new_table.items()
    if code not in current_table
}
if added:
    print(f"Added {len(added)} new encodings:")
    for m in sorted(added.values(), key=lambda m: m.code):
        print(textwrap.indent(pprint.pformat(m.to_json()), "  "))
else:
    print("Added no new encodings.")

# Displays removed encodings, if any:
removed = {
    code: m
    for code, m in current_table.items()
    if code not in new_table
}
if removed:
    print(f"Removed {len(added)} existing encodings:")
    for m in sorted(removed.values(), key=lambda m: m.code):
        print(textwrap.indent(pprint.pformat(m.to_json()), "  "))
else:
    print("Removed no existing encodings.")

# Displays changed encodings, if any:
changed = {
    code: (m, new_table[code])
    for code, m in current_table.items()
    if code in new_table and new_table[code] != m
}

if changed:
    print(f"Changed {len(added)} existing encodings:")
    for m_old, m_new in sorted(changed.values(), key=lambda pair: pair[0].code):
        print(f"  Changes in protocol {repr(m_old.code)}:")
        for attr in ("name", "status", "description"):
            old_val, new_val = (getattr(m_old, attr), getattr(m_new, attr))
            if old_val != new_val:
                print(f"    {attr}: {repr(old_val)} -> {repr(new_val)}")
else:
    print("Changed no existing encodings.")

print()

# If the table has changed, prompts for update:
if added or removed or changed:
    answer = input("Would you like to update the multibase table? (y/n) ")
    if answer.lower().startswith("y"):
        with open("multiformats_config/multibase-table.csv", "w", encoding="utf8") as f:
            f.write(new_text)
        with open("multiformats_config/multibase-table.json", "w", encoding="utf8") as f:
            table = [new_table[code].to_json() for code in sorted(new_table.keys())]
            json.dump(table, f, indent=4)
else:
    print("Nothing to update, exiting.")
