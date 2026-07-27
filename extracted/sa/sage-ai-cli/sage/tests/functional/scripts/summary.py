import json
import pathlib
import csv

JSON = pathlib.Path(".report.json")
if not JSON.is_file():
    print("No .report.json found, skipping summary.")
    exit(0)

data = json.loads(JSON.read_text())

rows = []
for t in data["tests"]:
    rows.append({
        "id": t["nodeid"],
        "outcome": t["outcome"],
        "duration": t["setup"].get("duration", 0) + t["call"].get("duration", 0) if "call" in t else 0,
    })

csv_file = "summary.csv"
with open(csv_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["id", "outcome", "duration"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Summary written to {csv_file}")
