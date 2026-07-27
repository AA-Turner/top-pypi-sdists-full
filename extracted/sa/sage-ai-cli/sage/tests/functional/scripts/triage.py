import json
import pathlib
import subprocess
import os

HTML = pathlib.Path("report.html")
JSON = pathlib.Path(".report.json")
if not JSON.is_file():
    print("No .report.json found, skipping triage.")
    exit(0)

data = json.loads(JSON.read_text())
failures = [node for node in data["tests"] if node["outcome"] == "failed"]

print(f"Found {len(failures)} failures out of {data['summary'].get('total', 0)} tests.")

# We won't actually create GitHub issues in an automated fashion here to avoid spamming the user's repo,
# but we will print a triage summary report.
for f in failures[:10]:
    title = f["nodeid"]
    print(f"Failure: {title}")
    # In a real environment we would invoke: `gh issue create ...`
