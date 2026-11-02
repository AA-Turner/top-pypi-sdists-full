#!/usr/bin/env python3
"""Interactive demo: build a linkchart of people and their related entities.

Walks you through picking a workspace, searching for a few people by name,
pulling in everything directly related to them (their phones, cars, and any
other neighbours the ontology defines), and saving it all as a linkchart in
the chosen workspace. It exercises the SDK's ``create_linkchart`` end to end,
which now stores linkcharts as ``os_file`` entities whose attachment body
holds the ``application/octostar-linkchart-settings+json`` graph.

Run it with::

    export OS_JWT='...'
    export OS_API_ENDPOINT='https://api-pr-746.main.octostar.com/'
    uv run python octostar_python_client/examples/create_linkchart_demo.py

``OS_ONTOLOGY`` is read from the environment if set, otherwise you'll be
prompted for it. Use ``--help`` to see the available flags.
"""

import argparse
import logging
import os
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any, cast

# This example lives alongside the SDK rather than depending on an installed
# package, so put the SDK's import root on sys.path before importing octostar.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from octostar.client import Client, make_client  # noqa: E402
from octostar.utils.ontology import fetch_ontology_data, query_ontology  # noqa: E402
from octostar.utils.workspace.linkcharts import create_linkchart  # noqa: E402

logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("create_linkchart_demo")

NEIGHBOUR_LIMIT = 50  # per person, per relationship — keeps the chart readable


# ── SQL helpers ───────────────────────────────────────────────────────────


def sql_literal(value: object) -> str:
    """Render a Python value as a Timbr/SQL literal (quotes escaped)."""
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (int, float)):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"


def run_query(client: Client, sql: str) -> list[dict]:
    """Run a SELECT and always return a list (never None), logging failures."""
    try:
        rows = query_ontology.sync(sql, client=client)
    except Exception as exc:
        logger.warning("Query failed (%s): %s", exc, sql)
        return []
    return rows or []


# ── Interactive selection ───────────────────────────────────────────────────


def prompt(message: str) -> str:
    return input(message).strip()


def choose(options: list, render: Callable[[Any], str], header: str):
    """Show a numbered menu and return the picked option (or None to skip)."""
    if not options:
        return None
    print(f"\n{header}")
    for idx, opt in enumerate(options, start=1):
        print(f"  {idx}. {render(opt)}")
    while True:
        raw = prompt("Pick a number (or blank to skip): ")
        if not raw:
            return None
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        print("  ! Please enter a valid number from the list.")


# ── Steps ─────────────────────────────────────────────────────────────────


def pick_workspace(client: Client) -> dict:
    """Search workspaces by name fragment and let the user pick one."""
    while True:
        term = prompt("\nWorkspace name to search for: ")
        if not term:
            print("  ! A search term is required.")
            continue
        sql = (
            "SELECT `entity_id`, `entity_label` FROM `timbr`.`os_workspace` "
            f"WHERE LOWER(`entity_label`) LIKE LOWER('%{term}%') "
            "ORDER BY `entity_label` LIMIT 25"
        )
        workspaces = run_query(client, sql)
        if not workspaces:
            print(f"  No workspaces matched '{term}'. Try again.")
            continue
        chosen = choose(
            workspaces,
            lambda w: f"{w.get('entity_label')}  ({w.get('entity_id')})",
            "Matching workspaces:",
        )
        if chosen:
            return chosen


def resolve_person_concept(ontology: dict, requested: str) -> str:
    """Confirm the person concept exists; otherwise help the user pick one."""
    concepts = ontology.get("concepts", {})
    if requested in concepts:
        return requested
    print(f"\nConcept '{requested}' not found in this ontology.")
    hints = sorted(
        name
        for name in concepts
        if any(h in name.lower() for h in ("person", "people", "individual", "human"))
    )
    if hints:
        picked = choose(hints, lambda c: c, "Person-like concepts available:")
        if picked:
            return picked
    manual = prompt("Enter the concept name to search people in: ")
    return manual or requested


def search_people(client: Client, concept: str, name: str, limit: int) -> list[dict]:
    sql = (
        f"SELECT `entity_id`, `entity_label`, `entity_type` FROM `timbr`.`{concept}` "
        f"WHERE LOWER(`entity_label`) LIKE LOWER('%{name}%') "
        f"ORDER BY `entity_label` LIMIT {limit}"
    )
    return run_query(client, sql)


def concept_family(ontology: dict, concept: str) -> set[str]:
    """The concept plus its ancestors (relationships may be defined on parents)."""
    info = ontology.get("concepts", {}).get(concept, {})
    # fetch_ontology_data puts the concept itself at parents[0].
    return set(info.get("parents", [])) | {concept}


def relationships_for(ontology: dict, person_concepts: set[str]) -> list[dict]:
    """Find traversable relationships touching the person's concept family.

    Returns normalised descriptors with the direction already resolved so the
    person side is always the 'from' side:
        {label, from_concept, from_props, to_concept, to_props, is_mtm}
    """
    out: list[dict] = []
    seen: set[tuple] = set()
    for rel in ontology.get("relationships", []):
        src = rel.get("source_concept")
        tgt = rel.get("target_concept")
        name = rel.get("relationship_name") or ""
        src_props = [p for p in (rel.get("source_properties") or "").split(",") if p]
        tgt_props = [p for p in (rel.get("target_properties") or "").split(",") if p]
        if not src_props or not tgt_props:
            continue
        if src in person_concepts:  # forward: person -> target
            key = (name, src, tgt, "fwd")
            if key not in seen:
                seen.add(key)
                out.append(
                    {
                        "label": name,
                        "from_concept": src,
                        "from_props": src_props,
                        "to_concept": tgt,
                        "to_props": tgt_props,
                        "is_mtm": bool(rel.get("is_mtm")),
                    }
                )
        if tgt in person_concepts:  # reverse: person -> source
            key = (name, tgt, src, "rev")
            if key not in seen:
                seen.add(key)
                out.append(
                    {
                        "label": rel.get("inverse_name") or f"{name} (inverse)",
                        "from_concept": tgt,
                        "from_props": tgt_props,
                        "to_concept": src,
                        "to_props": src_props,
                        "is_mtm": bool(rel.get("is_mtm")),
                    }
                )
    return out


def traverse(client: Client, person: dict, rel: dict) -> list[dict]:
    """Return entities related to ``person`` through one relationship."""
    # Read the person's join-key values from the concept that defines the rel.
    key_sql = (
        f"SELECT {', '.join(f'`{p}`' for p in rel['from_props'])} "
        f"FROM `timbr`.`{rel['from_concept']}` "
        f"WHERE `entity_id` = {sql_literal(person['entity_id'])} LIMIT 1"
    )
    key_rows = run_query(client, key_sql)
    if not key_rows:
        return []
    values = [key_rows[0].get(p) for p in rel["from_props"]]
    if any(v is None for v in values):
        return []

    to_props = rel["to_props"]
    cols = ["`entity_id`", "`entity_label`", "`entity_type`"]
    tuple_cols = ", ".join(f"`{p}`" for p in to_props)
    tuple_vals = ", ".join(sql_literal(v) for v in values)
    where = f"({tuple_cols}) IN (({tuple_vals}))"
    sql = (
        f"SELECT {', '.join(cols)} FROM `timbr`.`{rel['to_concept']}` "
        f"WHERE {where} LIMIT {NEIGHBOUR_LIMIT}"
    )
    return run_query(client, sql)


def keep_neighbour(entity: dict, concept: str, filters: list[str]) -> bool:
    if not filters:
        return True
    haystack = f"{entity.get('entity_type') or concept}".lower()
    return any(f in haystack for f in filters)


# ── Graph assembly ──────────────────────────────────────────────────────────


def node_from(entity: dict, fallback_type: str | None) -> dict:
    return {
        "entity_id": entity["entity_id"],
        "entity_label": entity.get("entity_label") or entity["entity_id"],
        "entity_type": entity.get("entity_type") or fallback_type or "os_thing",
    }


def build_graph(client: Client, ontology: dict, people: list[dict], filters: list[str]):
    """Return (nodes, edges) for the people and their related entities."""
    nodes: dict[str, dict] = {}
    edges: list[dict] = []

    for person in people:
        nodes[person["entity_id"]] = node_from(person, person.get("entity_type"))
        person_concepts = concept_family(ontology, person["entity_type"])
        rels = relationships_for(ontology, person_concepts)
        if not rels:
            print(f"  · No relationships defined for {person.get('entity_label')}.")
        for rel in rels:
            if rel["is_mtm"]:
                logger.info(
                    "Skipping many-to-many relationship '%s' (not traversed by the simple join path).",
                    rel["label"],
                )
                continue
            related = traverse(client, person, rel)
            kept = [r for r in related if keep_neighbour(r, rel["to_concept"], filters)]
            if kept:
                label = person.get("entity_label")
                print(
                    f"  · {label} --[{rel['label']}]--> {len(kept)} {rel['to_concept']}"
                )
            for entity in kept:
                nodes.setdefault(
                    entity["entity_id"], node_from(entity, rel["to_concept"])
                )
                edges.append(
                    {
                        "from_node": person["entity_id"],
                        "to_node": entity["entity_id"],
                        "label": rel["label"],
                    }
                )
    return list(nodes.values()), edges


# ── Main ────────────────────────────────────────────────────────────────────


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ontology",
        default=os.environ.get("OS_ONTOLOGY"),
        help="Ontology name (defaults to $OS_ONTOLOGY, else you'll be prompted).",
    )
    parser.add_argument(
        "--person-concept",
        default="os_person",
        help="Concept to search people in (default: os_person).",
    )
    parser.add_argument(
        "--concepts",
        default="",
        help=(
            "Comma-separated substrings to filter neighbours by entity type "
            "(e.g. 'phone,car'). Empty = include every related entity."
        ),
    )
    parser.add_argument(
        "--search-limit",
        type=int,
        default=15,
        help="Max people returned per name search (default: 15).",
    )
    parser.add_argument(
        "--chart-name",
        default=None,
        help="Name for the linkchart (default: prompted).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    for required in ("OS_JWT", "OS_API_ENDPOINT"):
        if not os.environ.get(required):
            print(f"ERROR: please set the {required} environment variable.")
            return 1

    ontology = args.ontology or prompt("Ontology name: ")
    if not ontology:
        print("ERROR: an ontology name is required.")
        return 1

    api_endpoint = os.environ["OS_API_ENDPOINT"]
    # Pass the JWT explicitly as fixed_jwt so the client uses $OS_JWT directly
    # instead of polling the /etc/secrets/OS_JWT file (a 10s retry loop locally).
    client = make_client(
        fixed_jwt=os.environ["OS_JWT"],
        ontology_name=ontology,
        api_endpoint=api_endpoint,
    )
    print(f"Connected to {api_endpoint} (ontology: {ontology}).")

    ontology_data = fetch_ontology_data.sync(client=client)
    person_concept = resolve_person_concept(ontology_data, args.person_concept)

    workspace = pick_workspace(client)
    print(
        f"Using workspace: {workspace.get('entity_label')} ({workspace['entity_id']})"
    )

    # Collect people across one or more name searches.
    people: dict[str, dict] = {}
    print("\nSearch for people to add (enter a blank name when you're done).")
    while True:
        name = prompt("Person name: ")
        if not name:
            break
        matches = search_people(client, person_concept, name, args.search_limit)
        if not matches:
            print(f"  No '{person_concept}' matched '{name}'.")
            continue
        picked = choose(
            matches,
            lambda p: f"{p.get('entity_label')}  ({p.get('entity_id')})",
            f"People matching '{name}':",
        )
        if picked:
            people[picked["entity_id"]] = picked
            print(f"  + Added {picked.get('entity_label')}.")

    if not people:
        print("No people selected — nothing to chart. Exiting.")
        return 0

    filters = [f.strip().lower() for f in args.concepts.split(",") if f.strip()]
    print("\nPulling in related entities…")
    nodes, edges = build_graph(client, ontology_data, list(people.values()), filters)
    print(f"\nGraph ready: {len(nodes)} nodes, {len(edges)} edges.")

    chart_name = args.chart_name or prompt("Linkchart name: ") or "People & assets"
    result = create_linkchart.sync(
        os_workspace=workspace["entity_id"],
        name=chart_name,
        nodes=cast(Any, nodes),
        edges=cast(Any, edges),
        client=client,
    )
    chart_id = (
        result.get("os_entity_uid") or result.get("entity_id")
        if isinstance(result, dict)
        else result
    )
    print(f"\n✓ Created linkchart '{chart_name}' (id: {chart_id}).")
    chart_url = (
        f"https://home.main.octostar.com/octostar/?octostar_api_url={api_endpoint}"
    )
    print(f"Open it at: {chart_url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
