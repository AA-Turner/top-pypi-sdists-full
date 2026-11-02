"""The boxes this router fronts: the boxes file and its links.

boxes file (JSON, 0600 — it holds box keys), `HUGPY_ROUTER_BOXES` or
<config dir>/router/boxes.json:

    {"boxes": [{"name": "ae", "url": "http://127.0.0.1:40717", "key": "hpk_box_…",
                "store": "/var/lib/hugpy-wrapper/fitevict.sqlite3", "pool": ""}]}

`store` is accepted for 0.0.1 files and ignored: every link uses the wrapper's API.
"""
from __future__ import annotations

import json
import os
from typing import Dict, List, Optional

from hugpy_core.router.imports import functions as F
from hugpy_core.router.links.box import BoxLink


def load(path: Optional[str] = None) -> List[dict]:
    path = path or F.boxes_path()
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        return []
    boxes = data.get("boxes") if isinstance(data, dict) else None
    return [b for b in (boxes or []) if isinstance(b, dict) and b.get("name") and b.get("url")]


def save(boxes: List[dict], path: Optional[str] = None) -> str:
    path = path or F.boxes_path()
    os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
    tmp = f"{path}.tmp-{os.getpid()}"
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump({"boxes": boxes}, fh, indent=1)
    os.replace(tmp, path)
    return path


class Registry:
    def __init__(self, boxes: List[dict]):
        self.on_change: list = []             # shared by every link, present or added later
        self.links: Dict[str, BoxLink] = {}
        for b in boxes:
            self.add(BoxLink(b["name"], b["url"], b.get("key"), b.get("pool") or "", b.get("store"),
                             bool(b.get("blocked")), bool(b.get("wildcard"))))

    def add(self, link: BoxLink) -> BoxLink:
        link.on_change = self.on_change
        self.links[link.name] = link
        return link

    def start(self, session) -> None:
        for link in self.links.values():
            link.start(session)

    async def stop(self) -> None:
        for link in self.links.values():
            await link.stop()

    def boxes(self):
        return [link.box() for link in self.links.values()]

    def link(self, name: str) -> Optional[BoxLink]:
        return self.links.get(name)
