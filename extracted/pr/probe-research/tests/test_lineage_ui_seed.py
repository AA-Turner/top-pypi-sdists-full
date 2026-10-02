"""Contract tests for the additive run-lineage UI fixture seed."""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SEED_PATH = REPO_ROOT / "scripts" / "seed_lineage_ui.py"


def _load_seed_module():
    spec = importlib.util.spec_from_file_location("probe_lineage_ui_seed", SEED_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


seed = _load_seed_module()


@dataclass
class _Page:
    items: list[dict]
    next_cursor: str | None = None


class _FakeRun:
    def __init__(self, client: "_FakeClient", row: dict):
        self.client = client
        self.data = row
        self.id = str(row["id"])

    def finish(self, status="completed", *, summary=None, **_kwargs):
        self.data["status"] = status
        self.data["summary"] = summary or {}
        return self.data


class _FakeClient:
    def __init__(
        self,
        *,
        project: dict | None = None,
        experiment: dict | None = None,
        page_size: int = 200,
    ):
        self.project = project
        self.experiment = experiment
        self.rows: list[dict] = []
        self.create_calls = 0
        self.experiment_create_calls = 0
        self.page_size = page_size

    def resolve_project(self, slug):
        assert slug == seed.PROJECT_SLUG
        return self.project

    def resolve_experiment(self, slug):
        assert slug == seed.EXPERIMENT_SLUG
        return self.experiment

    def create_experiment(self, slug, name, **kwargs):
        self.experiment_create_calls += 1
        self.experiment = {
            "id": "experiment-1",
            "slug": slug,
            "name": name,
            "question": kwargs["question"],
            "project_id": kwargs["project_id"],
            "description": kwargs["description"],
            "tags": kwargs["tags"],
        }
        return self.experiment

    def list_runs(self, *, experiment_id, limit, cursor=None):
        assert experiment_id == str(self.experiment["id"])
        assert limit == 200
        start = int(cursor or 0)
        stop = min(start + self.page_size, len(self.rows))
        next_cursor = str(stop) if stop < len(self.rows) else None
        return _Page(list(self.rows[start:stop]), next_cursor)

    def create_run(self, experiment_id, name, **kwargs):
        self.create_calls += 1
        row = {
            "id": f"run-{self.create_calls}",
            "slug": kwargs["slug"],
            "project_id": str(self.project["id"]),
            "experiment_id": experiment_id,
            "name": name,
            "status": "created",
            "source": kwargs["source"],
            "external_id": kwargs["external_id"],
            "parent_run_id": kwargs["parent_run_id"],
            "parent_relation": kwargs["parent_relation"],
            "metadata": kwargs["metadata"],
        }
        self.rows.append(row)
        return _FakeRun(self, row)

    def get_run(self, run_id):
        return next(dict(row) for row in self.rows if row["id"] == run_id)

    def run_lineage(self, run_id):
        descendants = []
        frontier = [run_id]
        depth = 1
        while frontier:
            level = [row for row in self.rows if row["parent_run_id"] in frontier]
            if not level:
                break
            descendants.extend({**row, "depth": depth} for row in level)
            frontier = [str(row["id"]) for row in level]
            depth += 1
        return {"run_id": run_id, "ancestors": [], "descendants": descendants}


def _project(*, synthetic=True, fixture_contract=None):
    return {
        "id": "project-1",
        "slug": seed.PROJECT_SLUG,
        "metadata": {
            "synthetic": synthetic,
            "fixture_contract": fixture_contract or seed.PROJECT_FIXTURE_CONTRACT,
        },
    }


def _experiment(*, project_id="project-1", owned=True):
    return {
        "id": "experiment-1",
        "slug": seed.EXPERIMENT_SLUG,
        "project_id": project_id,
        "tags": [
            "synthetic-data",
            "lineage-ui",
            *([seed.EXPERIMENT_OWNERSHIP_TAG] if owned else []),
        ],
    }


def test_fixture_shape_covers_siblings_plural_singular_middle_and_leaf_states():
    depths = seed.planned_depths()

    assert seed.FIXTURE_CONTRACT == "probe.lineage-ui-tree/2"
    assert seed.EXTERNAL_ID_PREFIX == "lineage-ui-tree-v2"
    assert all(node.slug.startswith("lineage-ui-v2-") for node in seed.RUN_NODES)
    assert depths == {
        "root": 0,
        "branch-a": 1,
        "branch-b": 1,
        "branch-c": 1,
        "branch-a-child": 2,
        "branch-a-leaf": 3,
        "branch-b-leaf": 2,
    }
    assert [node.key for node in seed.RUN_NODES if node.parent_key == "root"] == [
        "branch-a",
        "branch-b",
        "branch-c",
    ]
    assert seed.planned_descendant_counts() == {
        "root": 6,
        "branch-a": 2,
        "branch-b": 1,
        "branch-c": 0,
        "branch-a-child": 1,
        "branch-a-leaf": 0,
        "branch-b-leaf": 0,
    }
    summary = seed.dry_run_summary()
    assert summary["runs_by_depth"] == {0: 1, 1: 3, 2: 2, 3: 1}
    assert summary["direct_child_descendant_counts"] == {
        "branch-a": 2,
        "branch-b": 1,
        "branch-c": 0,
    }
    assert summary["experiment_slug"] == seed.EXPERIMENT_SLUG


@pytest.mark.parametrize(
    "project",
    [
        None,
        _project(synthetic=False),
        _project(fixture_contract="somebody-elses-fixture"),
    ],
)
def test_seed_refuses_a_missing_or_foreign_project_before_writing(project):
    client = _FakeClient(project=project)

    with pytest.raises(RuntimeError):
        seed.seed(client)

    assert client.create_calls == 0
    assert client.experiment_create_calls == 0
    assert client.rows == []


@pytest.mark.parametrize(
    "experiment",
    [
        _experiment(project_id="another-project"),
        _experiment(owned=False),
    ],
)
def test_seed_refuses_a_foreign_experiment_before_writing_runs(experiment):
    client = _FakeClient(project=_project(), experiment=experiment)

    with pytest.raises(RuntimeError, match="experiment slug"):
        seed.seed(client)

    assert client.create_calls == 0
    assert client.experiment_create_calls == 0
    assert client.rows == []


def test_seed_writes_exact_parentage_then_reuses_every_row():
    client = _FakeClient(project=_project())

    first = seed.seed(client)
    second = seed.seed(client)

    assert first["created"] == 7
    assert first["reused"] == 0
    assert second["created"] == 0
    assert second["reused"] == 7
    assert client.create_calls == 7
    assert client.experiment_create_calls == 1
    assert len(client.rows) == 7

    by_external_id = {row["external_id"]: row for row in client.rows}
    root = by_external_id[f"{seed.EXTERNAL_ID_PREFIX}:root"]
    branch_a = by_external_id[f"{seed.EXTERNAL_ID_PREFIX}:branch-a"]
    branch_a_child = by_external_id[f"{seed.EXTERNAL_ID_PREFIX}:branch-a-child"]
    branch_b = by_external_id[f"{seed.EXTERNAL_ID_PREFIX}:branch-b"]
    branch_b_leaf = by_external_id[f"{seed.EXTERNAL_ID_PREFIX}:branch-b-leaf"]
    assert {row["external_id"] for row in client.rows if row["parent_run_id"] == root["id"]} == {
        f"{seed.EXTERNAL_ID_PREFIX}:branch-a",
        f"{seed.EXTERNAL_ID_PREFIX}:branch-b",
        f"{seed.EXTERNAL_ID_PREFIX}:branch-c",
    }
    assert branch_a["parent_relation"] == "branch"
    assert branch_a_child["parent_run_id"] == branch_a["id"]
    assert branch_b_leaf["parent_run_id"] == branch_b["id"]
    assert all(row["experiment_id"] == first["experiment_id"] for row in client.rows)
    assert all(row["status"] == "completed" for row in client.rows)
    assert first["experiment_path"] == f"/experiments/{first['experiment_id']}"
    assert first["experiment_runs_path"] == (
        f"/experiments/{first['experiment_id']}?tab=runs"
    )
    assert set(first["run_paths"]) == {node.key for node in seed.RUN_NODES}
    assert first["run_paths"]["root"] == first["root_run_path"]


def test_seed_follows_every_page_before_deciding_what_exists():
    client = _FakeClient(project=_project(), page_size=2)

    seed.seed(client)
    second = seed.seed(client)

    assert second["created"] == 0
    assert second["reused"] == 7
    assert client.create_calls == 7


def test_seed_refuses_duplicate_fixture_identity_across_pages():
    client = _FakeClient(project=_project(), page_size=2)
    seed.seed(client)
    client.rows.append(dict(client.rows[0]))

    with pytest.raises(RuntimeError, match="duplicate lineage UI fixture external id"):
        seed.seed(client)

    assert client.create_calls == 7


def test_seed_refuses_an_unexpected_prefixed_fixture_row():
    client = _FakeClient(project=_project())
    seed.seed(client)
    client.rows.append(
        {
            **client.rows[0],
            "id": "stale-run",
            "external_id": f"{seed.EXTERNAL_ID_PREFIX}:stale",
        }
    )

    with pytest.raises(RuntimeError, match="unexpected lineage UI fixture external ids"):
        seed.seed(client)

    assert client.create_calls == 7


def test_seed_resumes_an_interrupted_prefix_without_rewriting_it():
    client = _FakeClient(project=_project())
    seed.seed(client)
    retained = list(client.rows[:4])
    client.rows = list(retained)

    resumed = seed.seed(client)

    assert resumed["created"] == 3
    assert resumed["reused"] == 4
    assert client.rows[:4] == retained


def test_seed_refuses_a_bad_lineage_readback():
    client = _FakeClient(project=_project())
    client.run_lineage = lambda _run_id: {
        "run_id": "wrong",
        "ancestors": [],
        "descendants": [],
    }

    with pytest.raises(RuntimeError, match="lineage UI fixture readback mismatch"):
        seed.seed(client)


def test_seed_refuses_an_unexpected_descendant_under_the_fixture_root():
    client = _FakeClient(project=_project())
    seed.seed(client)
    root = next(row for row in client.rows if row["external_id"].endswith(":root"))
    client.rows.append(
        {
            **root,
            "id": "foreign-child",
            "slug": "foreign-child",
            "source": "api",
            "external_id": "foreign-child",
            "parent_run_id": root["id"],
            "parent_relation": "branch",
        }
    )

    with pytest.raises(RuntimeError, match="lineage UI fixture readback mismatch"):
        seed.seed(client)


def test_seed_refuses_drift_in_an_existing_parent_pointer():
    client = _FakeClient(project=_project())
    seed.seed(client)
    branch_a = next(
        row for row in client.rows if row["external_id"] == f"{seed.EXTERNAL_ID_PREFIX}:branch-a"
    )
    branch_a["parent_run_id"] = "wrong-parent"

    with pytest.raises(RuntimeError, match="incompatible"):
        seed.seed(client)

    assert client.create_calls == 7
