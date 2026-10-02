"""Extensive search examples for mode='vid_file'.

Endpoint: POST /search_frontui   (infra/search_api_ui/routers/frontui_search.py)
SDK path:  client.searches.search_video(...)

# Usage:
  export VMODAL_API_KEY=ak_xxx

  python search_ex.py ex1_text
  python search_ex.py ex2_date_range
  python search_ex.py ex3_stream_filter
  python search_ex.py ex4_sources
  python search_ex.py ex5_metadata_context
  python search_ex.py ex6_pagination
  python search_ex.py ex7_image_url
  python search_ex.py ex8_version
  python search_ex.py ex9_video_group
  python search_ex.py ex10_json_field
  python search_ex.py ex11_newsalien2_image
  python search_ex.py ex_all
"""
from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
import os, sys, json
import fire
import logging
from vmodal import SyncClient

logging.basicConfig(level=logging.INFO, format="%(message)s")
log_info = logging.info


def _client() -> SyncClient:
    return SyncClient.from_env()


def _rows(res):
    rows = getattr(res, "hits", None)
    if rows is None:
        rows = getattr(res, "data", None)
    return list(rows or [])


def _field(row, name: str, default: Any = "?") -> Any:
    if isinstance(row, dict):
        return row.get(name, default)
    return getattr(row, name, default)


def _print(label: str, res) -> None:
    log_info(f"[{label}] cnt_actual={res.cnt_actual}")
    for i, h in enumerate(_rows(res)[:3]):
        score = _field(h, "score")
        try:
            score = f"{float(score):.4f}"
        except (TypeError, ValueError):
            score = str(score)
        ts = _field(h, "ts_unix")
        src = _field(h, "stream_name", None) or _field(h, "stream", None) or _field(h, "source_path")
        log_info(f"  hit[{i}] score={score}  ts={ts}  stream={src}")


# ── Backend field reference (frontui_search.py:SearchRequest_frontui) ─────────
#
#  query_text        str            "" — primary text query
#  query_metadata    Optional[str]  None — Box-2 context keywords (plain string)
#  image_query       Optional[str]  None — base64 data URI or https image URL
#  query_json_field  Dict[str,str]  {} — cat5_json sub-field FTS, e.g. {"brand":"nike"}
#  query_text_lang   "auto"|"en"|"ja"  "auto" — hint for translation
#  search_sources    List[Literal["ocr","asr","image","object"]]  ["ocr","asr","image"]
#  search_combine_mode  "union"|"intersect"|"weighted"  "union"
#  start_date        Optional[str]  None — "YYYY-MM-DD HH:MM:SS"
#  end_date          Optional[str]  None — "YYYY-MM-DD HH:MM:SS"
#  offset            int            0
#  limit             int            50
#  text_emb_score_min   float  0.90 — cosine similarity floor for text embeddings
#  image_emb_score_min  float  1.5  — L2-ish floor for image embeddings
#  group_name        str       "agroup" — collection name
#  stream_name       str       "astream" — sub-collection; "astream" = all streams
#  mode              "vid_file"|"vid_stream_day"|"img_file"  "vid_file"
#  video_group       Optional[str]  None — shorthand "{mode}-{group_name}" combo
#  version_lancedb   int       0 — index version (0 = latest)
#  version_emb       Optional[int]  None — embedding parquet version
#  tracking_id       Optional[str]  None — client request tracking id


# ── 1. Basic text search ───────────────────────────────────────────────────────
def ex1_text(
    query: str = "company earnings report",
    group: str = "news1",
    limit: int = 10,
):
    """Text search across all modalities (ocr + asr + image)."""
    c = _client()
    res = c.searches.search_video(
        query_text=query,
        mode="vid_file",
        group_name=group,
        stream_name="astream",           # "astream" = no stream filter (all streams)
        search_sources=["ocr", "asr", "image"],
        search_combine_mode="union",     # union: any modality match = hit
        limit=limit,
        text_emb_score_min=0.90,
        version_lancedb=0,               # 0 = latest index version
    )
    _print("ex1_text", res)
    return res


# ── 2. Date-range filter ───────────────────────────────────────────────────────
def ex2_date_range(
    query: str = "product launch",
    group: str = "news1",
    start: str = "2024-01-01 00:00:00",   # backend format: "YYYY-MM-DD HH:MM:SS"
    end:   str = "2024-06-30 23:59:59",
):
    """Search within a datetime window."""
    c = _client()
    res = c.searches.search_video(
        query_text=query,
        mode="vid_file",
        group_name=group,
        stream_name="astream",
        search_sources=["asr", "ocr"],
        start_date=start,
        end_date=end,
        limit=20,
        text_emb_score_min=0.88,
    )
    _print("ex2_date_range", res)
    return res


# ── 3. Sub-collection / stream filter ─────────────────────────────────────────
def ex3_stream_filter(
    query: str = "interview CEO",
    group: str = "news1",
    stream: str = "cnn_2024",           # exact stream_name value from LanceDB
):
    """Pin search to a single stream (sub-collection)."""
    c = _client()
    res = c.searches.search_video(
        query_text=query,
        mode="vid_file",
        group_name=group,
        stream_name=stream,              # exact match; "astream" = all
        search_sources=["asr"],          # speech-only
        limit=15,
        text_emb_score_min=0.85,
    )
    _print("ex3_stream_filter", res)
    return res


# ── 4. Choose modalities (search_sources) ─────────────────────────────────────
def ex4_sources(
    query: str = "price chart graph",
    group: str = "finance1",
):
    """Compare image-only vs text-only vs all-sources vs object-detection."""
    c = _client()

    for label, sources, extra in [
        ("image-only",   ["image"],                {"image_emb_score_min": 1.3}),
        ("ocr-only",     ["ocr"],                  {"text_emb_score_min": 0.88}),
        ("asr-only",     ["asr"],                  {"text_emb_score_min": 0.88}),
        ("object-only",  ["object"],               {"text_emb_score_min": 0.85}),
        ("all-union",    ["ocr","asr","image"],     {"text_emb_score_min": 0.90, "image_emb_score_min": 1.5}),
        ("all-intersect",["ocr","asr"],             {"text_emb_score_min": 0.88, "search_combine_mode": "intersect"}),
    ]:
        res = c.searches.search_video(
            query_text=query,
            mode="vid_file",
            group_name=group,
            stream_name="astream",
            search_sources=sources,
            limit=5,
            **extra,
        )
        log_info(f"[ex4 {label}] cnt_actual={res.cnt_actual}")


# ── 5. Metadata context / query_metadata (Box-2) ─────────────────────────────
def ex5_metadata_context(
    query: str = "earnings",
    group: str = "news1",
):
    """
    query_metadata = Box-2 context string from the frontend.
    Backend post-filters vid_file metadata (title/description/info_json) on hits.
    NOTE: backend expects a plain string, not a dict.
    """
    c = _client()
    res = c.searches.search_video(
        query_text=query,
        query_metadata="finance Q1 2024",  # plain keyword string (Box-2)
        mode="vid_file",
        group_name=group,
        stream_name="astream",
        search_sources=["ocr", "asr", "image"],
        limit=10,
        text_emb_score_min=0.90,
    )
    _print("ex5_metadata_context", res)
    return res


# ── 6. Pagination ─────────────────────────────────────────────────────────────
def ex6_pagination(
    query: str = "market analysis",
    group: str = "news1",
    pages: int = 3,
    page_size: int = 10,
):
    """Iterate multiple pages using offset + limit."""
    c = _client()
    all_hits = []
    for page in range(pages):
        res = c.searches.search_video(
            query_text=query,
            mode="vid_file",
            group_name=group,
            stream_name="astream",
            search_sources=["ocr", "asr", "image"],
            offset=page * page_size,
            limit=page_size,
            text_emb_score_min=0.90,
        )
        rows = _rows(res)
        log_info(f"[ex6 page={page}] returned={len(rows)} cnt_actual={res.cnt_actual}")
        all_hits.extend(rows)
        if len(rows) < page_size:
            break   # last page
    log_info(f"[ex6_pagination] total fetched={len(all_hits)}")
    return all_hits


# ── 7. Image URL / base64 query ───────────────────────────────────────────────
def ex7_image_url(
    image_url: str = "https://example.com/frame.jpg",
    group: str = "news1",
):
    """
    Search by image: pass an https URL or base64 data URI as image_query.
    query_text must be empty when no text is provided (validator: text OR image required).
    """
    c = _client()
    res = c.searches.search_video(
        query_text="",                   # empty: image_query satisfies the either-or validator
        image_query=image_url,           # https URL or "data:image/jpeg;base64,..."
        mode="vid_file",
        group_name=group,
        stream_name="astream",
        search_sources=["image"],        # image source required for image queries
        image_emb_score_min=1.3,         # lower = more results; default 1.5 is strict
        limit=10,
    )
    _print("ex7_image_url", res)
    return res


# ── 8. Specific LanceDB index version ────────────────────────────────────────
def ex8_version(
    query: str = "sports highlight",
    group: str = "sports1",
    version: int = 2,
):
    """Pin to a specific LanceDB index version; version_lancedb=0 = latest."""
    c = _client()
    res = c.searches.search_video(
        query_text=query,
        mode="vid_file",
        group_name=group,
        stream_name="astream",
        search_sources=["ocr", "asr", "image"],
        version_lancedb=version,
        limit=10,
        text_emb_score_min=0.90,
    )
    _print("ex8_version", res)
    return res


# ── 9. video_group shorthand ──────────────────────────────────────────────────
def ex9_video_group(
    query: str = "technology conference",
    video_group: str = "vid_file-news1",  # "{mode}-{group_name}" format
):
    """
    video_group overrides mode + group_name when provided.
    Backend parses "vid_file-news1" → mode="vid_file", group_name="news1".
    """
    c = _client()
    res = c.searches.search_video(
        query_text=query,
        video_group=video_group,         # shorthand overrides mode + group_name
        stream_name="astream",
        search_sources=["ocr", "asr", "image"],
        limit=10,
        text_emb_score_min=0.90,
        tracking_id="ex9_demo_001",      # optional client-side request tracing
    )
    _print("ex9_video_group", res)
    return res


# ── 10. cat5_json sub-field FTS filter ────────────────────────────────────────
def ex10_json_field(
    query: str = "product review",
    group: str = "ecommerce1",
):
    """
    query_json_field filters on cat5_json sub-fields via FTS.
    Keys are JSON field paths; values are Lucene-style expressions.
    """
    c = _client()
    res = c.searches.search_video(
        query_text=query,
        query_json_field={
            "brand":       "nike OR adidas",
            "attrs.color": "red AND leather",
        },
        mode="vid_file",
        group_name=group,
        stream_name="astream",
        search_sources=["ocr"],
        limit=10,
        text_emb_score_min=0.88,
    )
    _print("ex10_json_field", res)
    return res


# ── 11. newsalien2 fixture image-only search ─────────────────────────────────
def ex11_newsalien2_image(
    query: str = "alien",
    limit: int = 10,
):
    """
    Search the newsalien2 vid_file fixture using image embeddings only.
    VMODAL_API_KEY is read by SyncClient.from_env(); identity is derived from it.
    """
    c = _client()
    res = c.searches.search_video(
        query_text=query,
        mode="vid_file",
        group_name="newsalien2",
        stream_name="astream",
        search_sources=["image"],
        search_combine_mode="union",
        limit=limit,
        image_emb_score_min=1.5,
        tracking_id="ex11_newsalien2_image",
    )
    _print("ex11_newsalien2_image", res)
    return res


# ── run all ───────────────────────────────────────────────────────────────────
def ex_all():
    ex1_text()
    ex2_date_range()
    ex3_stream_filter()
    ex4_sources()
    ex5_metadata_context()
    ex6_pagination()
    ex8_version()


if __name__ == "__main__":
    fire.Fire()
