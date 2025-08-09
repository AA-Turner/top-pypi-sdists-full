import asyncio
import logging
import sys
from csv import writer as csv_writer
from logging import basicConfig
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from coiled.scan import scan_prefix
from coiled.software_utils import COILED_LOCAL_PACKAGE_PREFIX, get_index_urls
from coiled.utils import IGNORE_PYTHON_DIRS, recurse_importable_python_files


@click.group()
def package_sync():
    basicConfig(level=logging.INFO)


@package_sync.command()
@click.option("--csv", is_flag=True, default=False, help="Output as CSV")
@click.option("--verbose", "-v", is_flag=True, default=False, help="Output files that will end up in wheels")
def scan(csv: bool, verbose: bool):
    result = asyncio.run(scan_prefix())
    table = Table(title="Packages")
    table.add_column("Package Name", style="cyan", no_wrap=True)
    table.add_column("Conda Name", style="cyan", no_wrap=True)
    table.add_column("Version", style="magenta")
    table.add_column("Source", style="magenta")
    table.add_column("Requested", style="cyan", no_wrap=True)
    table.add_column("Channel", style="magenta", overflow="fold")
    table.add_column("Channel URL", style="magenta", overflow="fold")
    table.add_column("Wheel target", style="green", overflow="fold")
    table.add_column("Path", overflow="fold")
    if verbose:
        table.add_column("Python modules", overflow="fold")
    rows = []
    for pkg in result:
        row = [
            pkg["name"],
            pkg["conda_name"],
            pkg["version"],
            pkg["source"],
            "✅" if pkg["requested"] else "",
            pkg["channel"] or "",
            pkg["channel_url"] or "",
            pkg["wheel_target"] or "",
            str(pkg["path"]) if pkg["path"] else "",
        ]
        if verbose:
            if pkg["name"].startswith(COILED_LOCAL_PACKAGE_PREFIX) and pkg["path"]:
                modules = []
                for path in recurse_importable_python_files(pkg["path"]):
                    parent_names = {parent.name for parent in path.parents}
                    if not parent_names.intersection(IGNORE_PYTHON_DIRS) and str(path) not in (
                        "__init__.py",
                        "__main__.py",
                    ):
                        modules.append(str(path))
                row.append("\n".join(modules))
            else:
                row.append("")

        rows.append(row)

    rows = sorted(rows, key=lambda x: (x[3], x[0].lower()))

    if csv:
        writer = csv_writer(sys.stdout, lineterminator="\n")
        writer.writerow([c.header for c in table.columns])
        writer.writerows(rows)
    else:
        for row in rows:
            table.add_row(*row)
        console = Console()
        console.print(table)


@package_sync.command()
@click.option("--csv", is_flag=True, default=False, help="Output as CSV")
def debug(csv: bool):
    table = Table(title="Debug")
    table.add_column("Path", no_wrap=True, overflow="fold")
    rows = []
    for path in sys.path:
        p = Path(path)
        if p.is_dir():
            for file in p.iterdir():
                rows.append([str(file)])
        else:
            rows.append([str(p)])
    rows = sorted(rows)
    if csv:
        writer = csv_writer(sys.stdout, lineterminator="\n")
        writer.writerow([c.header for c in table.columns])
        writer.writerows(rows)
    else:
        for row in rows:
            table.add_row(*row)
        console = Console()
        console.print(table)


@package_sync.command()
@click.option("--csv", is_flag=True, default=False, help="Output as CSV")
def indexes(csv: bool):
    table = Table(title="PyPI Indexes")
    table.add_column("URL", no_wrap=True, overflow="fold")
    rows = sorted([[url] for url in get_index_urls()])
    if csv:
        writer = csv_writer(sys.stdout, lineterminator="\n")
        writer.writerow([c.header for c in table.columns])
        writer.writerows(rows)
    else:
        for row in rows:
            table.add_row(*row)
        console = Console()
        console.print(table)
