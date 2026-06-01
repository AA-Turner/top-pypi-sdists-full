from __future__ import annotations

import csv
import io
import os
import re
import tomllib
from collections import defaultdict
from datetime import datetime
from pathlib import Path


# ── Configuration ──────────────────────────────────────────────────────────────

# URL type classification (checked in order — first match wins)
URL_TYPES: list[tuple[str, str]] = [
    ("twiki.cern.ch",    "Twiki"),
    ("indico.cern.ch",   "Indico"),
    ("gitlab.cern.ch",   "GitLab"),
    (".docs.cern.ch",    "Docs"),
    ("its.cern.ch/jira", "Jira"),
]

# Maximum display length for a URL cell before truncation
URL_DISPLAY_MAX_LEN = 55

# Files excluded from link scanning regardless of directory config
SCAN_EXCLUDE_FILES = {"directory.md", "migrationstatus.md", "overview.md", "links.md"}

# Top-level docs subdirectories skipped entirely during scanning
SCAN_EXCLUDE_DIRS = {"category", "jira", "glance", "archive", "assets", "images", "img", "diagrams", "files", "attachments", "directory"}

# Frontmatter written into every generated migrationstatus.md
PAGE_ICON = "lucide/link"
PAGE_BOOST = 0
PAGE_TAGS = ["★ MIGRATION"]
PAGE_HIDE = ["toc"]

# Content shown when no matching links are found in the directory
PAGE_NO_LINKS_MESSAGE = (
    ":lucide-circle-check: **No external links found!**\n\n"
    "This directory contains no external links."
)

# Tip admonition shown at the top of every migration status page
PAGE_TIP = (
    "How to use this page\"\n"
    "    - Hover over a link to see which pages use it (tooltip)\n"
    "    - The \"Usage Count\" column shows how many pages reference this link\n"
    "    - Focus on high-usage links first for maximum migration impact"
)


# ── Fetch ──────────────────────────────────────────────────────────────────────

def get_page_title(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return Path(file_path).stem.replace("-", " ").replace("_", " ").title()

    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            for line in content[3:end].splitlines():
                if line.lower().startswith("title:"):
                    value = line.split(":", 1)[1].strip().strip("\"'")
                    if value:
                        return value

    for line in content.splitlines():
        if line.startswith("# "):
            return line[2:].strip()

    return Path(file_path).stem.replace("-", " ").replace("_", " ").title()


def extract_links_from_file(file_path: str) -> list[dict[str, str]]:
    links = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
        return links

    for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", content):
        text, url = match.groups()
        url = url.strip()
        if url and (url.startswith("http://") or url.startswith("https://")):
            links.append({"text": text, "url": url})

    return links


def get_url_type(url: str) -> str:
    lower = url.lower()
    for pattern, label in URL_TYPES:
        if pattern in lower:
            return label
    return "Other"


# ── Prepare ────────────────────────────────────────────────────────────────────

def create_migration_status(docs_root: str = "docs") -> None:
    directories = []
    for root, dirs, files in os.walk(docs_root):
        if "directory.toml" in files:
            print(f"Found directory.toml in {root}")
            directories.append(root)

    renderer = DefaultMigrationRenderer()

    for dir_path in directories:
        directory_config = {}
        try:
            with open(os.path.join(dir_path, "directory.toml"), "rb") as f:
                directory_config = tomllib.load(f)
        except Exception as e:
            print(f"Error loading config from {dir_path}: {e}")

        if not directory_config.get("migrationsummary", True):
            continue

        content, csv_content = renderer.render(Path(dir_path), scan_root=Path(docs_root))

        out_dir = Path(dir_path) / "directory"
        out_dir.mkdir(parents=True, exist_ok=True)

        output_path = out_dir / "links.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        if csv_content:
            with open(out_dir / "links.csv", "w", encoding="utf-8", newline="") as f:
                f.write(csv_content)

        link_count = content.count("\n| ") - 1
        print(f"Created links.md in {dir_path} with {link_count} unique external links")


# ── Postprocess ────────────────────────────────────────────────────────────────

class DefaultMigrationRenderer:
    def render(self, folder: Path, scan_root: Path | None = None) -> str:
        scan_path = str(scan_root) if scan_root is not None else str(folder)
        output_dir = folder

        directory_config = {}
        try:
            with open(folder / "directory.toml", "rb") as f:
                directory_config = tomllib.load(f)
        except Exception as e:
            print(f"Error loading config from {folder / 'directory.toml'}: {e}")

        pagetitle = directory_config.get("title", "Directory")
        exclude = directory_config.get("exclude", [])

        md_files = []
        for root, dirs, files in os.walk(scan_path):
            dirs[:] = [d for d in dirs if d not in SCAN_EXCLUDE_DIRS]
            for f in files:
                if f.endswith(".md") and f not in SCAN_EXCLUDE_FILES:
                    rel_from_scan = os.path.relpath(os.path.join(root, f), scan_path)
                    if any(rel_from_scan.startswith(excl) or rel_from_scan == excl for excl in exclude):
                        continue
                    md_files.append(rel_from_scan)

        hide_block = "".join(f"    - {h}\n" for h in PAGE_HIDE)
        tags_block = "".join(f"    - {t}\n" for t in PAGE_TAGS)

        if not md_files:
            frontmatter = (
                f"---\ntitle: Sources Summary - {pagetitle}\nicon: {PAGE_ICON}\n"
                f"hide:\n{hide_block}tags:\n{tags_block}boost: {PAGE_BOOST}\n"
                f"pagestatus: script\ndategenerated: {datetime.now().strftime('%Y-%m-%d')}\n---\n\n"
            )
            return frontmatter + PAGE_NO_LINKS_MESSAGE + "\n", ""

        link_usage: dict[str, list] = defaultdict(list)
        for md_file in md_files:
            abs_md = os.path.join(scan_path, md_file)
            page_name = md_file.replace(".md", "").replace("\\", "/")
            page_title = get_page_title(abs_md)
            for link in extract_links_from_file(abs_md):
                link_usage[link["url"]].append({"page": page_name, "title": page_title, "text": link["text"]})

        if not link_usage:
            print(f"No external links found in {scan_path}")
            frontmatter = (
                f"---\ntitle: Sources Summary - {pagetitle}\nicon: {PAGE_ICON}\n"
                f"hide:\n{hide_block}tags:\n{tags_block}boost: {PAGE_BOOST}\n"
                f"pagestatus: script\ndategenerated: {datetime.now().strftime('%Y-%m-%d')}\n---\n\n"
            )
            return frontmatter + PAGE_NO_LINKS_MESSAGE + "\n", ""

        def page_link(usage: dict) -> str:
            page = usage["page"].replace("\\", "/")
            label = usage.get("title") or page
            if page.endswith("/index"):
                page = page[:-6]
            elif page == "index":
                page = ""
            href = "/" + page if page else "/"
            return f"[{label}]({href})"

        table_rows = []
        for i, (url, usages) in enumerate(sorted(link_usage.items()), 1):
            pages_links = "<br>".join(
                page_link(u) for u in usages
            )

            url_display = url.replace("https://", "").replace("http://", "")
            url_display_clean = url_display.split("#")[0].split("?")[0]
            if len(url_display_clean) > URL_DISPLAY_MAX_LEN:
                url_display_clean = "..." + url_display_clean[-(URL_DISPLAY_MAX_LEN - 3):]
            url_display_clean = url_display_clean.replace("|", "\\|")

            has_query = "?" in url
            url_link = f"[{url_display_clean}{'*' if has_query else ''}]({url})"

            url_type = get_url_type(url)
            table_rows.append(f"| {i} | {url_type} | {url_link} | {len(usages)} | {pages_links} |")

        total_unique_links = len(link_usage)
        total_usages = sum(len(usages) for usages in link_usage.values())

        frontmatter = (
            f"---\n"
            f"title: Sources Summary - {pagetitle}\n"
            f"icon: {PAGE_ICON}\n"
            f"hide:\n{hide_block}"
            f"tags:\n{tags_block}"
            f"boost: {PAGE_BOOST}\n"
            f"pagestatus: script\n"
            f"csv_download: links.csv\n"
            f"dategenerated: {datetime.now().strftime('%Y-%m-%d')}\n"
            f"---\n\n"
        )

        # Build CSV content
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["#", "Type", "URL", "Usage Count", "Pages"])
        for i, (url, usages) in enumerate(sorted(link_usage.items()), 1):
            pages_str = "; ".join(u.get("title") or u["page"] for u in usages)
            writer.writerow([i, get_url_type(url), url, len(usages), pages_str])
        csv_content = buf.getvalue()

        md_content = (
            frontmatter
            + f"This folder contains **{total_unique_links} unique external links** with **{total_usages} total usages** across {len(md_files)} pages.\n\n"
            + f"!!! tip \"{PAGE_TIP}\n\n"
            + f"<div class=\"dense-table\" markdown>\n\n"
            + f"|:lucide-hash: # | Type | :lucide-external-link: URL | :lucide-list-ordered: Usage Count | :lucide-file-text: Pages |\n"
            + f"|:---|:---|:-------------------|:------------------------|:---------------------|\n"
            + "\n".join(table_rows)
            + "\n</div>\n\n"
        )
        return md_content, csv_content


def main() -> None:
    import sys
    hub_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    create_migration_status(docs_root=str(hub_dir / "docs"))


if __name__ == "__main__":
    main()
