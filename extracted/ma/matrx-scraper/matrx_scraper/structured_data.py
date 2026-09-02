"""Complete structured-data extraction for captured web pages."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from selectolax.parser import HTMLParser

try:
    import extruct

    _EXTRUCT_AVAILABLE = True
except ImportError:
    _EXTRUCT_AVAILABLE = False

_MAX_BLOCKS = 200


@dataclass
class StructuredDataBlock:
    source: str  # "json-ld" | "microdata" | "rdfa" | "microformat"
    types: list[str]
    data: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {"source": self.source, "types": self.types, "data": self.data}


@dataclass
class StructuredDataExtraction:
    schema_types: list[str]
    schema_org: dict[str, Any]
    json_ld: list[Any]
    json_ld_raw: list[str]
    microdata: list[dict[str, Any]]
    rdfa: list[dict[str, Any]]
    microformats: list[dict[str, Any]]
    blocks: list[StructuredDataBlock]
    parse_errors: list[dict[str, Any]]
    blocks_truncated: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_types": self.schema_types,
            "schema_org": self.schema_org,
            "json_ld": self.json_ld,
            "json_ld_raw": self.json_ld_raw,
            "microdata": self.microdata,
            "rdfa": self.rdfa,
            "microformats": self.microformats,
            "blocks": [block.to_dict() for block in self.blocks],
            "blocks_truncated": self.blocks_truncated,
            "parse_errors": self.parse_errors,
        }


def _types_of(node: dict[str, Any]) -> list[str]:
    t = node.get("@type")
    if isinstance(t, str):
        return [t]
    if isinstance(t, list):
        return [x for x in t if isinstance(x, str)]
    # extruct's microdata items carry a schema.org URL in "type", not "@type"
    microdata_type = node.get("type")
    if isinstance(microdata_type, str):
        return [microdata_type.rstrip("/").rsplit("/", 1)[-1]]
    if isinstance(microdata_type, list):
        return [str(x).rstrip("/").rsplit("/", 1)[-1] for x in microdata_type if x]
    return []


def _walk_types(node: Any, output: list[str]) -> None:
    if isinstance(node, dict):
        output.extend(_types_of(node))
        for value in node.values():
            _walk_types(value, output)
    elif isinstance(node, list):
        for item in node:
            _walk_types(item, output)


def _record_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def extract_structured_payload(html: str, url: str) -> StructuredDataExtraction:
    """Extract every raw and normalized structured-data signal on a page."""
    if not html or not url:
        return StructuredDataExtraction([], {}, [], [], [], [], [], [], [])

    json_ld: list[Any] = []
    json_ld_raw: list[str] = []
    parse_errors: list[dict[str, Any]] = []
    try:
        tree = HTMLParser(html)
        scripts = tree.css('script[type="application/ld+json"]')
    except Exception as exc:
        return StructuredDataExtraction(
            [],
            {},
            [],
            [],
            [],
            [],
            [],
            [],
            [{"source": "html", "message": f"{type(exc).__name__}: {exc}"}],
        )

    for index, script in enumerate(scripts):
        raw = (script.text(deep=True) or "").strip()
        if not raw:
            continue
        json_ld_raw.append(raw)
        try:
            json_ld.append(json.loads(raw))
        except (TypeError, ValueError) as exc:
            parse_errors.append(
                {
                    "source": "json-ld",
                    "index": index,
                    "message": f"{type(exc).__name__}: {exc}",
                }
            )

    extracted: dict[str, Any] = {}
    if _EXTRUCT_AVAILABLE:
        try:
            extracted = extruct.extract(
                html,
                base_url=url,
                syntaxes=["microdata", "rdfa", "microformat"],
            )
        except Exception as exc:
            parse_errors.append(
                {
                    "source": "extruct",
                    "message": f"{type(exc).__name__}: {exc}",
                }
            )

    microdata = _record_list(extracted.get("microdata"))
    rdfa = _record_list(extracted.get("rdfa"))
    microformats = _record_list(extracted.get("microformat"))
    blocks: list[StructuredDataBlock] = []
    blocks_truncated = False

    def append_block(block: StructuredDataBlock) -> None:
        nonlocal blocks_truncated
        if len(blocks) >= _MAX_BLOCKS:
            blocks_truncated = True
            return
        blocks.append(block)

    for item in json_ld:
        nodes: list[Any]
        if isinstance(item, dict) and isinstance(item.get("@graph"), list):
            nodes = item["@graph"]
        elif isinstance(item, list):
            nodes = item
        else:
            nodes = [item]
        for node in nodes:
            if not isinstance(node, dict):
                continue
            types = _types_of(node)
            append_block(StructuredDataBlock(source="json-ld", types=types, data=node))

    for source, items in (
        ("microdata", microdata),
        ("rdfa", rdfa),
        ("microformat", microformats),
    ):
        for item in items:
            append_block(StructuredDataBlock(source=source, types=_types_of(item), data=item))

    schema_types: list[str] = []
    for value in [*json_ld, *microdata, *rdfa, *microformats]:
        _walk_types(value, schema_types)
    seen: set[str] = set()
    schema_types = [
        value for value in schema_types if value and not (value in seen or seen.add(value))
    ]
    representative: dict[str, Any] = {}
    for value in json_ld:
        if isinstance(value, dict):
            representative = value
            break
        if isinstance(value, list):
            representative = {"@graph": value}
            break
    return StructuredDataExtraction(
        schema_types=schema_types,
        schema_org=representative,
        json_ld=json_ld,
        json_ld_raw=json_ld_raw,
        microdata=microdata,
        rdfa=rdfa,
        microformats=microformats,
        blocks=blocks,
        parse_errors=parse_errors,
        blocks_truncated=blocks_truncated,
    )


def extract_structured_data(html: str, url: str) -> list[StructuredDataBlock]:
    """Extract every flattened structured-data block on a page."""
    return extract_structured_payload(html, url).blocks


__all__ = [
    "StructuredDataBlock",
    "StructuredDataExtraction",
    "extract_structured_data",
    "extract_structured_payload",
]
