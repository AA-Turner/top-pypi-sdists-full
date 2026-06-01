"""Merge and process Zensical search.json files.

Usage examples:
    # Merge multiple files, minify, compress with gzip and brotli
    python -m atlasdocs.postprocess.search.add_twiki_search a.json b.json --output search.json --gz --br

    # Single file, collapse h3+ into h2 parents, no minify
    python -m atlasdocs.postprocess.search.add_twiki_search search.json --output out.json --no-minify

    # Merge files but keep all heading levels separate
    python -m atlasdocs.postprocess.search.add_twiki_search a.json b.json --merge-level 0

    # Collapse everything into h1 only
    python -m atlasdocs.postprocess.search.add_twiki_search search.json --merge-level 1

    # Always include a TWiki index with a tag applied to all its items
    python -m atlasdocs.postprocess.search.add_twiki_search search.json --extra data/twiki_search_index.json --extra-tag twiki
"""

import argparse
import gzip
import json
import os
import re
import sys
import tomllib
from collections import OrderedDict
from datetime import date

try:
    import brotli
    _BROTLI = True
except ImportError:
    _BROTLI = False


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Merge and/or process Zensical search.json files."
    )
    parser.add_argument("files", nargs="+", help="One or more search.json files")
    parser.add_argument("--output", default="search.json", help="Output file (default: search.json)")

    # File merging
    parser.add_argument(
        "--no-merge", action="store_true",
        help="Skip merging multiple files — process only the first file"
    )

    # Level merging
    parser.add_argument(
        "--merge-level", type=int, default=2, metavar="N",
        help=(
            "Collapse items at level > N by appending their text to the nearest "
            "ancestor at level ≤ N. Use 0 to disable. (default: 2)"
        )
    )

    # Output format
    parser.add_argument(
        "--no-minify", action="store_true",
        help="Write pretty-printed JSON (default: minified)"
    )
    parser.add_argument("--gz", action="store_true", help="Also write a .gz compressed copy")
    parser.add_argument("--br", action="store_true", help="Also write a .br (brotli) compressed copy")

    # Extra sources from config file
    parser.add_argument(
        "--search-config", metavar="FILE", default="search.toml",
        help="TOML config listing extra search indexes to merge in (default: search.toml)"
    )

    return parser.parse_args()


# ── Deduplication key ─────────────────────────────────────────────────────────

def get_unique_key(item):
    loc = item.get("location")
    if loc:
        return str(loc)
    path = item.get("path")
    if isinstance(path, list) and path:
        return str(path[0])
    if isinstance(path, str):
        return path
    return None


# ── Level merging ─────────────────────────────────────────────────────────────

def apply_level_merge(items, max_level):
    """Collapse items whose level > max_level into the nearest ancestor at level ≤ max_level.

    Args:
        items: list of search item dicts (mutated in place)
        max_level: maximum heading level to keep as a separate item (0 = keep all)

    Returns:
        Filtered list with deep-level items removed (text appended to parents).
    """
    if max_level == 0:
        return items

    result = []
    # Stack of items kept so far, used to find the nearest ancestor
    parent_stack = []

    for item in items:
        level = item.get("level", 1)

        if level <= max_level:
            result.append(item)
            # Trim stack to items at a level strictly less than current
            parent_stack = [p for p in parent_stack if p.get("level", 1) < level]
            parent_stack.append(item)
        else:
            # Find nearest kept ancestor
            parent = None
            for candidate in reversed(parent_stack):
                if candidate.get("level", 1) <= max_level:
                    parent = candidate
                    break
            if parent is not None:
                extra = item.get("text", "").strip()
                if extra:
                    existing = parent.get("text", "").strip()
                    parent["text"] = (existing + " " + extra).strip() if existing else extra
            # Item is not added to result

    return result


# ── File I/O ──────────────────────────────────────────────────────────────────

def load_search_config(config_path):
    """Load search.toml and return list of {file, tag} dicts."""
    if not os.path.exists(config_path):
        return []
    try:
        with open(config_path, "rb") as f:
            data = tomllib.load(f)
        return data.get("source", [])
    except Exception as e:
        print(f"Warning: could not read {config_path}: {e}", file=sys.stderr)
        return []


PATH_MAX_LEN = 70
TEXT_MAX_LEN = 5000
_HTML_TAG_RE = re.compile(r"<[^>]+>")
_MD_BOLD_RE = re.compile(r"\*\*([^*]*)\*\*")


def _strip_html(text: str) -> str:
    return _HTML_TAG_RE.sub("", text).strip()


def _clean_text(text: str) -> str:
    text = _HTML_TAG_RE.sub("", text)
    text = _MD_BOLD_RE.sub(r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:TEXT_MAX_LEN]


def _process_path(path: list) -> list:
    """Strip HTML, split path segments on '|' or ':', truncate each to PATH_MAX_LEN chars."""
    result = []
    for segment in path:
        segment = _strip_html(str(segment))
        if "|" in segment:
            parts = segment.split("|", 1)
        elif ":" in segment:
            parts = segment.split(":", 1)
        else:
            parts = [segment]
        for p in parts:
            p = p.strip()
            if p:
                result.append(p[:PATH_MAX_LEN])
    return result


def normalize_item(item):
    """Normalize a search item:
    - Split each path string at '|' or ':' and truncate to PATH_MAX_LEN (always).
    - Strip tags to only ★ GITLAB or ★ TWIKI.
    """
    item["path"] = _process_path(item.get("path") or [])
    item["tags"] = [t for t in (item.get("tags") or []) if t.startswith("★")]
    return item


def _extract_last_edit_date(item: dict):
    """Parse the YYYY-MM-DD last-edit date from an item's path field, or None."""
    for segment in (item.get("path") or []):
        m = re.search(r"Last edit.*?(\d{4}-\d{2}-\d{2})", str(segment))
        if m:
            try:
                return date.fromisoformat(m.group(1))
            except ValueError:
                pass
    return None


def filter_by_age(items: list, max_years: int) -> tuple[list, int]:
    """Drop items whose last-edit date is older than max_years years.

    Items with no parseable date are kept (assume still current).
    Returns (kept_items, dropped_count).
    """
    if max_years <= 0:
        return items, 0
    cutoff = date.today().replace(year=date.today().year - max_years)
    kept, dropped = [], 0
    for item in items:
        edit_date = _extract_last_edit_date(item)
        if edit_date is not None and edit_date < cutoff:
            dropped += 1
        else:
            kept.append(item)
    return kept, dropped


def _gitlab_namespace(location: str) -> str | None:
    """Extract the namespace (first path segment) from a gitlab.cern.ch URL."""
    m = re.match(r"https://gitlab\.cern\.ch/([^/]+)", location or "")
    return m.group(1) if m else None


def filter_by_gitlab_scope(items: list, allowed_scopes: list[str]) -> tuple[list, int]:
    """Keep only ★ GITLAB items whose location namespace matches an allowed scope.

    Scope matching rules (against https://gitlab.cern.ch/<namespace>/...):
      - Trailing '*'  → prefix match  e.g. 'atlas-phys*' matches 'atlas-physics', 'atlas-phys'
      - No '*'        → exact match   e.g. 'atlas' matches only the 'atlas' namespace

    Non-★ GITLAB items pass through unchanged.
    Items with no parseable gitlab.cern.ch location pass through unchanged.
    Returns (kept_items, dropped_count).
    """
    if not allowed_scopes:
        return items, 0
    kept, dropped = [], 0
    for item in items:
        tags = item.get("tags") or []
        if "★ GITLAB" not in tags:
            kept.append(item)
            continue
        ns = _gitlab_namespace(item.get("location", ""))
        if ns is None:
            kept.append(item)
            continue
        matched = False
        for scope in allowed_scopes:
            if scope.endswith("*"):
                if ns.startswith(scope[:-1]):
                    matched = True
                    break
            else:
                if ns == scope:
                    matched = True
                    break
        if matched:
            kept.append(item)
        else:
            dropped += 1
    return kept, dropped


def load_extra(path, tag, normalize=False):
    """Load an extra search.json, normalize paths (always), strip tags (if normalize=True), and apply tag."""
    data = load_file(path)
    if data is None or not isinstance(data, dict) or "items" not in data:
        print(f"Warning: {path} missing 'items' — skipping", file=sys.stderr)
        return []
    items = data["items"]
    for item in items:
        item["path"] = _process_path(item.get("path") or [])
        if item.get("title"):
            item["title"] = _strip_html(item["title"])
        if item.get("text"):
            item["text"] = _clean_text(item["text"])
    if normalize:
        for item in items:
            item["tags"] = [t for t in (item.get("tags") or []) if t.startswith("★")]
    if tag:
        for item in items:
            existing = item.get("tags") or []
            if tag not in existing:
                item["tags"] = existing + [tag]
    return items


def load_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading {path}: {e}", file=sys.stderr)
        return None


def write_json(path, data, minify):
    with open(path, "w", encoding="utf-8") as f:
        if minify:
            json.dump(data, f, separators=(",", ":"))
        else:
            json.dump(data, f, indent=2)


def write_gz(path):
    with open(path, "rb") as f:
        content = f.read()
    with gzip.open(path + ".gz", "wb") as f:
        f.write(content)
    print(f"  → {path}.gz")


def write_br(path):
    if not _BROTLI:
        print("Warning: brotli not installed — skipping .br output", file=sys.stderr)
        return
    with open(path, "rb") as f:
        content = f.read()
    with open(path + ".br", "wb") as f:
        f.write(brotli.compress(content))
    print(f"  → {path}.br")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    args = parse_args()

    # Resolve which files to process
    files_to_process = args.files[:1] if args.no_merge else args.files

    # Load and merge
    unique_items = OrderedDict()
    config = None

    for idx, path in enumerate(files_to_process):
        data = load_file(path)
        if data is None:
            continue
        if not isinstance(data, dict) or "items" not in data:
            print(f"Warning: {path} missing 'items' — skipping", file=sys.stderr)
            continue
        if idx == 0:
            config = data.get("config", {})
        for item in data["items"]:
            key = get_unique_key(item)
            if key and key not in unique_items:
                unique_items[key] = item

    if not unique_items and config is None:
        print("No valid data found.", file=sys.stderr)
        sys.exit(1)

    items = list(unique_items.values())
    for item in items:
        item["path"] = _process_path(item.get("path") or [])

    # Merge extra sources from search.toml
    for src in load_search_config(args.search_config):
        src_file = src.get("file", "")
        src_tag = src.get("tag", "")
        if not src_file:
            continue
        extra_items = load_extra(src_file, src_tag, normalize=src.get("normalize", False))

        # Filter: maximum age since last edit (default 5 years)
        max_years = src.get("maximum_years_since_last_edit", 5)
        extra_items, age_dropped = filter_by_age(extra_items, max_years)
        if age_dropped:
            print(f"  Age filter (>{max_years}y): dropped {age_dropped} items")

        # Filter: restrict ★ GITLAB items to allowed namespace scopes
        scope_raw = src.get("gitlab_allowed_scope", [])
        allowed_scopes = [scope_raw] if isinstance(scope_raw, str) else list(scope_raw)
        extra_items, scope_dropped = filter_by_gitlab_scope(extra_items, allowed_scopes)
        if scope_dropped:
            print(f"  Scope filter ({allowed_scopes}): dropped {scope_dropped} GitLab items")

        extra_added = 0
        for item in extra_items:
            key = get_unique_key(item)
            if key and key not in unique_items:
                unique_items[key] = item
                items.append(item)
                extra_added += 1
        print(f"Extra ({src_file}): added {extra_added} items (tag={src_tag!r})")

    # Apply level merging
    if args.merge_level > 0:
        before = len(items)
        items = apply_level_merge(items, args.merge_level)
        print(f"Level merge (≤{args.merge_level}): {before} → {len(items)} items")

    merged = {"config": config or {}, "items": items}

    # Write output
    write_json(args.output, merged, not args.no_minify)
    print(f"Written: {args.output} ({len(items)} items)")

    if args.gz:
        write_gz(args.output)
    if args.br:
        write_br(args.output)


if __name__ == "__main__":
    main()
