#!/usr/bin/env python3
"""Prove the locked textcharts tracker runtime using scratch databases only."""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import subprocess
import tempfile
from importlib import resources
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "_project" / "scripts"
WRAPPER = SCRIPTS / "todo"
WHEEL = SCRIPTS / "vendor" / "todo_db-0.3.2-py3-none-any.whl"
PROJECT_ID = "textcharts"
REPOSITORY = "https://github.com/joeharris76/textcharts.git"
WHEEL_SHA256 = "ddc8c56a8b9f11c550d8f3b81df568c6d111cc79c076cbc4bf7c03fd68a95fa4"


def run_todo(
    *args: str,
    db: Path,
    actor: str | None = None,
    cwd: Path | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.pop("TODO_DB_URL", None)
    env.pop("TODO_DB_AUTH_TOKEN", None)
    env.pop("TODO_DB_RO_AUTH_TOKEN", None)
    env["TODO_DB_PATH"] = str(db)
    command = [str(WRAPPER)]
    if actor:
        command.extend(("--actor", actor))
    command.extend(args)
    result = subprocess.run(
        command,
        cwd=cwd or ROOT,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        raise AssertionError(
            f"todo command failed ({result.returncode}): {' '.join(command)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def create_schema_v3(db: Path) -> None:
    migration_root = resources.files("todo_db.migrations")
    connection = sqlite3.connect(db)
    try:
        for version in range(1, 4):
            matches = sorted(migration_root.glob(f"{version:03d}_*.sql"))
            assert len(matches) == 1, f"missing migration {version}"
            migration = matches[0]
            sql = migration.read_text(encoding="utf-8")
            connection.executescript(sql)
            name = migration.name.partition("_")[2].removesuffix(".sql")
            checksum = hashlib.sha256(sql.encode()).hexdigest()
            connection.execute(
                "INSERT INTO schema_migrations(version, name, checksum, applied_at, tool_version) "
                "VALUES (?, ?, ?, ?, ?)",
                (version, name, checksum, "2026-01-01T00:00:00Z", "0.1.0"),
            )
        connection.execute(
            "INSERT INTO project_identity(singleton, project_id, repository) VALUES (1, ?, ?)",
            (PROJECT_ID, REPOSITORY),
        )
        connection.commit()
    finally:
        connection.close()


def query_one(db: Path, sql: str, parameters: tuple[object, ...] = ()) -> tuple[object, ...]:
    connection = sqlite3.connect(db)
    try:
        row = connection.execute(sql, parameters).fetchone()
        assert row is not None
        return row
    finally:
        connection.close()


def assert_source_is_portable() -> None:
    tracked_runtime = (
        WRAPPER,
        SCRIPTS / "pyproject.toml",
        SCRIPTS / "uv.lock",
        ROOT / "skill-sync.yaml",
        ROOT / ".gitignore",
    )
    forbidden = (
        "/Users/" + "joe/Developer/todo-db",
        ".." + "/todo-db",
        "TODO_DB_AUTH_TOKEN=",
        "TODO_DB_RO_AUTH_TOKEN=",
    )
    for path in tracked_runtime:
        text = path.read_text(encoding="utf-8")
        for pattern in forbidden:
            assert pattern not in text, f"{path.relative_to(ROOT)} contains forbidden runtime text {pattern!r}"
    assert ".todo-db/" in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()


def assert_yaml_mapping(db: Path) -> str:
    result = run_todo(
        "import-yaml",
        "--todo-dir",
        str(ROOT / "_project" / "TODO"),
        "--done-dir",
        str(ROOT / "_project" / "DONE"),
        db=db,
    )
    report = json.loads(result.stdout)
    candidates = [
        path
        for tree in (ROOT / "_project" / "TODO", ROOT / "_project" / "DONE")
        for path in tree.rglob("*.yaml")
        if "_indexes" not in path.parts
    ]
    imported = set(report["imported"])
    skipped = report["skipped"]
    assert len(imported) + len(skipped) == len(candidates), (
        f"YAML mapping incomplete: {len(candidates)} candidates, {len(imported)} imported, {len(skipped)} skipped"
    )
    assert not skipped, f"legacy YAML items skipped: {skipped}"
    connection = sqlite3.connect(db)
    try:
        stored = {row[0] for row in connection.execute("SELECT id FROM items")}
        claimable = connection.execute("SELECT id FROM items WHERE state != 'done' ORDER BY id LIMIT 1").fetchone()
    finally:
        connection.close()
    assert stored == imported, "database item IDs differ from the importer mapping"
    assert claimable is not None, "YAML import produced no claimable item"
    return str(claimable[0])


def main() -> None:
    assert hashlib.sha256(WHEEL.read_bytes()).hexdigest() == WHEEL_SHA256
    assert_source_is_portable()
    version = subprocess.run(
        ["uv", "run", "--project", str(SCRIPTS), "--locked", "--", "todo-db", "--version"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert version.stdout.strip() == "todo-db 0.3.2"

    with tempfile.TemporaryDirectory(prefix="textcharts-todo-runtime-") as temporary:
        scratch = Path(temporary)
        nested = scratch / "nested" / "working-directory"
        nested.mkdir(parents=True)

        migrated_db = scratch / "schema-v3.sqlite"
        create_schema_v3(migrated_db)
        run_todo("migrate", db=migrated_db, cwd=nested)
        run_todo("stats", db=migrated_db, cwd=nested)
        assert query_one(migrated_db, "SELECT max(version) FROM schema_migrations") == (5,)
        assert query_one(migrated_db, "SELECT project_id, repository FROM project_identity") == (
            PROJECT_ID,
            REPOSITORY,
        )

        source_db = scratch / "source.sqlite"
        item_id = assert_yaml_mapping(source_db)
        run_todo("claim", item_id, db=source_db, actor="Alice")
        rejected = run_todo("release", item_id, db=source_db, actor="Bob", check=False)
        assert rejected.returncode == 2, f"non-holder release returned {rejected.returncode}"
        assert query_one(source_db, "SELECT claimed_by FROM items WHERE id = ?", (item_id,)) == ("Alice",)
        run_todo("release", item_id, db=source_db, actor="Alice")
        run_todo("audit", "verify", db=source_db)

        first_export = scratch / "source.json"
        second_export = scratch / "restored.json"
        run_todo("export", "--output", str(first_export), db=source_db)
        restored_db = scratch / "restored.sqlite"
        run_todo("restore", "--input", str(first_export), "--replace", db=restored_db)
        run_todo("audit", "verify", db=restored_db)
        run_todo("export", "--output", str(second_export), db=restored_db)
        assert first_export.read_bytes() == second_export.read_bytes(), "export/restore changed canonical bytes"

        overridden = run_todo("--project-id", "wrong", "stats", db=source_db, check=False)
        assert overridden.returncode == 2, "wrapper accepted a project identity override"

    print("locked textcharts todo-db runtime verified")


if __name__ == "__main__":
    main()
