"""Update versions.json for docs deployment."""

import json
import sys
from pathlib import Path


def main():
    path, new_tag = Path(sys.argv[1]), sys.argv[2]
    versions = json.loads(path.read_text()) if path.exists() else []
    # Remove existing entry for this tag and clear old latest flags
    versions = [v for v in versions if v["version"] != new_tag]
    for v in versions:
        v.pop("latest", None)
    # Add new version as latest
    repo_name = "textcharts"
    versions.insert(0, {"version": new_tag, "url": f"/{repo_name}/{new_tag}/", "latest": True})
    path.write_text(json.dumps(versions, indent=2) + "\n")


if __name__ == "__main__":
    main()
