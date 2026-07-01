#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "typer",
#     "httpx",
#     "polars",
# ]
# ///
from __future__ import annotations

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Generator, Iterable, Literal

import httpx
import polars as pl

ENDPOINT_WIKIDATA_SPARQL = "https://query.wikidata.org/sparql"
PATH_BASE = Path(__file__).parent / "wikidata"
FP_QUANTITIES_RQ = PATH_BASE / "quantities.sparql"
FP_QUANTITIES_JSON = PATH_BASE / "quantities.json"
FP_QUANTITIES_PQ = PATH_BASE / "quantities.parquet"
FP_QUANTITIES_MD = PATH_BASE / "quantities.md"

logger = logging.getLogger(__name__)


def fetch(
    query: str,
    *,
    fmt: Literal["json", "xml"],
    endpoint_url: str = ENDPOINT_WIKIDATA_SPARQL,
) -> bytes:
    response = httpx.post(
        endpoint_url, data={"query": query, "format": fmt}, timeout=120.0
    )
    response.raise_for_status()
    return response.content


def fetch_json(
    fp_rq: Path = FP_QUANTITIES_RQ,
    fp_json: Path = FP_QUANTITIES_JSON,
) -> None:
    """Execute a SPARQL query from a file and save the raw response as JSON."""
    if fp_json.exists():
        logger.info(f"file already exists, skipping fetch: {fp_json}")
        return
    query = fp_rq.read_text()
    res = fetch(query, fmt="json")
    with open(fp_json, "wb") as f:
        f.write(res)


#
# parquet
#

RE_CLAUSE = r"(?P<a>\d+)[-.](?P<b>\d+)(\.(?P<c>[\d\w]+))?"


def to_int(s: str | None) -> int | None:
    if s is None:
        return None
    try:
        return int(s)
    except ValueError:
        if len(s) != 1:
            logger.warning(f"expected char of length 1, but got {s}")
            return None
        val = ord(s.lower()) - ord("a")
        if val < 0 or val > 25:
            logger.warning(f"expected [a-z], but got {s}")
            return None
        return val


def parse_isoiec_items(
    isoiec_items: Iterable[str],
) -> Generator[dict[str, Any], None, None]:
    for isoiec_item in isoiec_items:
        if not isoiec_item:
            continue
        t_string, clause = items(isoiec_item, separator="|||")
        dt = datetime.strptime(t_string, "%Y-%m-%dT%H:%M:%SZ")
        if not (match := re.match(RE_CLAUSE, clause)):
            clause_order = None
        else:
            clause_order = (
                (to_int(match.group("a")) or 0) * 10000
                + (to_int(match.group("b")) or 0) * 100
                + (to_int(match.group("c")) or 0)
            )

        yield {"dt": dt, "clause": clause, "clause_order": clause_order}


def shorten_uri(uri: str) -> str:
    code = uri.removeprefix("http://www.wikidata.org/entity/")
    if code[0] in ("Q", "P"):
        return code
    return uri


def parse_uri(value: dict[str, str] | None) -> str | None:
    if not value:
        return None
    if (t := value["type"]) != "uri":
        raise ValueError(f"expected uri type, got {t}")
    return shorten_uri(value["value"])


def parse_literal(value: dict[str, str] | None) -> str | None:
    if not value:
        return None
    if (t := value["type"]) != "literal":
        raise ValueError(f"expected literal type, got {t}")
    return value["value"]


def items(
    lit: str | None, *, separator: str = "@@@"
) -> Generator[str, None, None]:
    if not lit:
        return
    for item in lit.split(separator):
        yield item


def parse_latex(mathml: str) -> str:
    anno = mathml.split('<annotation encoding="application/x-tex">', 1)[-1]
    anno = anno.split("</annotation>", 1)[0]
    if anno.startswith(r"{\displaystyle "):
        anno = anno.removeprefix(r"{\displaystyle ").removesuffix(r"}")
    return anno


def parse_symbol_in_formula(sym: str | None) -> dict[str, str] | None:
    if not sym:
        return None
    if len(i := tuple(items(sym, separator="|||"))) != 3:
        logger.warning(
            f"expected 3 items in symbol_in_formula, got {len(i)}: {sym}"
        )
        return None
    mathml, label, uri = i
    return {
        "latex": parse_latex(mathml),
        "label": label,
        "entity": shorten_uri(uri),
    }


def parse_response_quantities(
    bindings: Iterable[dict[str, Any]],
) -> Generator[dict[str, Any], None, None]:
    for binding in bindings:
        # one binding can be referenced by multiple ISO/IEC 80000 editions
        yield {
            "entity": parse_uri(binding.get("quantity")),
            "isoiec_items": sorted(
                parse_isoiec_items(
                    items(parse_literal(binding.get("isoiec_items")))
                ),
                key=lambda x: x["dt"],
                reverse=True,
            ),
            "label": parse_literal(binding.get("label")),
            "desc": parse_literal(binding.get("desc")),
            "symbols": tuple(
                parse_latex(mathml)
                for mathml in items(parse_literal(binding.get("symbols")))
            ),
            "dims": tuple(
                parse_latex(mathml)
                for mathml in items(parse_literal(binding.get("dims")))
            ),
            "units": tuple(
                parse_latex(mathml)
                for mathml in items(parse_literal(binding.get("units")))
            ),
            "wolfram_ids": tuple(
                items(parse_literal(binding.get("wolfram_ids")))
            ),
            "qudt_ids": tuple(items(parse_literal(binding.get("qudt_ids")))),
            "defining_formulas": tuple(
                parse_latex(mathml)
                for mathml in items(
                    parse_literal(binding.get("defining_formulas"))
                )
            ),
            "symbols_in_formula": tuple(
                parse_symbol_in_formula(sym)
                for sym in items(
                    parse_literal(binding.get("symbols_in_formula"))
                )
            ),
        }


def quantities_to_parquet(
    fp_json: Path = FP_QUANTITIES_JSON, fp_parquet: Path = FP_QUANTITIES_PQ
) -> None:
    """Organise the raw quantities JSON response in a parquet file."""
    response = json.loads(fp_json.read_text())
    bindings = response["results"]["bindings"]
    df = pl.DataFrame(parse_response_quantities(bindings))
    df.write_parquet(fp_parquet)
    logger.info(f"wrote {len(df)} rows to {fp_parquet}")


def md_lines(row: dict[str, Any]) -> Generator[str, None, None]:
    clause = ", ".join(
        f"`{item['dt'].year}::{item['clause']}`" for item in row["isoiec_items"]
    )
    clause = f"{clause} = " if clause else ""
    yield f"**{clause}`{row['entity']}`: {row['label']}**"
    if desc := row["desc"]:
        yield f'- description: "{desc}"'
    if dims := row["dims"]:
        yield f"- dimension: ${', '.join(dims)}$"
    if sym := row["symbols"]:
        yield f"- symbol: ${', '.join(sym)}$"
    if de := row["defining_formulas"]:
        yield f"- formula: ${', '.join(de)}$"
        for sym in row["symbols_in_formula"]:
            yield f"  - ${sym['latex']}$ = {sym['label']}"


def quantities_to_md(
    fp_parquet: Path = FP_QUANTITIES_PQ,
    fp_md: Path = FP_QUANTITIES_MD,
) -> None:
    """Organise the quantities parquet file in a human-readable markdown file."""
    df = (
        pl.scan_parquet(fp_parquet)
        .filter(pl.col("isoiec_items").list.len() > 0)
        .sort(pl.col("isoiec_items").list.first().struct.field("clause_order"))
        .collect()
    )
    with open(fp_md, "w") as f:
        for row in df.iter_rows(named=True):
            for line in md_lines(row):
                f.write(line + "\n")
            f.write("\n")
    logger.info(f"wrote {len(df)} entries to {fp_md}")


try:
    import typer

    app = typer.Typer(no_args_is_help=True)
    app.command()(fetch_json)
    app.command()(quantities_to_parquet)
    app.command()(quantities_to_md)
except ImportError:

    def app() -> None:
        fetch_json()
        quantities_to_parquet()
        quantities_to_md()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app()
