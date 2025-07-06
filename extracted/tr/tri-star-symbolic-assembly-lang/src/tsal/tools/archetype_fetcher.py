import json
from pathlib import Path
from typing import List, Dict

try:
    import requests
except ModuleNotFoundError:  # pragma: no cover - fallback
    import urllib.request as _u

    class _Resp:
        def __init__(self, text: str, status: int = 200) -> None:
            self.text = text
            self.status_code = status

        def raise_for_status(self) -> None:
            if self.status_code >= 400:
                raise RuntimeError(f"status {self.status_code}")

    class requests:
        @staticmethod
        def get(url: str) -> _Resp:
            with _u.urlopen(url) as f:
                return _Resp(f.read().decode(), f.getcode())


def fetch_online_mesh(url: str) -> List[Dict]:
    """Fetch archetype mesh entries from ``url``."""
    resp = requests.get(url)
    resp.raise_for_status()
    return json.loads(resp.text)


def merge_mesh(mesh_path: Path, entries: List[Dict]) -> None:
    """Merge ``entries`` into JSON mesh at ``mesh_path`` by archetype name."""
    if mesh_path.exists():
        data = json.loads(mesh_path.read_text())
    else:
        data = []
    names = {e.get("name") for e in data}
    for e in entries:
        if e.get("name") not in names:
            data.append(e)
            names.add(e.get("name"))
    mesh_path.write_text(json.dumps(data, indent=2))
