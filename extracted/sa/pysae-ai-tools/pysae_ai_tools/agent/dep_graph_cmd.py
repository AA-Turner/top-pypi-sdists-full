"""``pysae-ai-tools agent dep-graph`` — schedulable ticket dependency graph.

Reads the batch candidate pool (same JSON shape as ``agent candidates``) on stdin, fetches
each candidate's hard GitLab issue links, and emits the DAG (``ready`` / ``edges`` /
``deferred`` / ``cycles``) the parallel scheduler consumes. No LLM.
"""

import json
import sys

import typer

from .dep_graph import build_graph, ref
from .dep_graph_gitlab import fetch_links, is_satisfied


def main() -> None:
    """Emit the schedulable dependency graph for the candidates on stdin (JSON)."""
    try:
        candidates = json.loads(sys.stdin.read() or "[]")
    except json.JSONDecodeError as exc:
        typer.echo(f"invalid candidates JSON on stdin: {exc}", err=True)
        raise typer.Exit(code=1) from None
    refs = [ref(str(c["project_path"]), int(c["iid"])) for c in candidates]
    graph = build_graph(refs, fetch_links, is_satisfied)
    typer.echo(graph.model_dump_json())
