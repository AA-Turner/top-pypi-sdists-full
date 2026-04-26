#!/usr/bin/env python
"""Render docs through the configured project-link profile."""

from __future__ import annotations

import argparse
from pathlib import Path

from anteroom.services.docs_project_links import prepare_docs_site


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mkdocs", default="mkdocs.yml")
    parser.add_argument("--print-path", action="store_true")
    args = parser.parse_args()

    rendered = prepare_docs_site(Path(args.mkdocs))
    print(rendered if args.print_path else rendered.parent)


if __name__ == "__main__":
    main()
