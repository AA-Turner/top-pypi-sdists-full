"""Contract tests for the additive degraded RL UI seed dataset."""

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

from probe.connectors.harbor import parse_trial
from tests.conftest import open_run

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "scripts"
SEED_PATH = SCRIPTS / "seed_rl_failure_modes.py"


def _load_seed_module():
    sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location("probe_rl_failure_seed", SEED_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


seed = _load_seed_module()


def test_failure_seed_keeps_the_eight_cell_happy_path_matrix():
    specs = seed.failure_specs()

    assert len(specs) == 8
    assert Counter(spec.sample.step for spec in specs) == {100: 4, 101: 4}
    assert Counter(spec.sample.group.id for spec in specs) == {
        "prompt-code-refactor": 4,
        "prompt-incident-debug": 4,
    }
    assert len({spec.mode.id for spec in specs}) == 8
    assert sum(spec.mode.incomplete_collection for spec in specs) == 2


def test_prepare_failure_seed_separates_exportable_and_partial_capture(tmp_path):
    prepared = seed.prepare_seed(tmp_path)

    assert sum(item.export.durable_collection_complete for item in prepared) == 6
    assert Counter(
        parse_trial(item.export.staged_trial.trial_dir).trajectory_format for item in prepared
    ) == {
        "ATIF-v1.7": 6,
        "private-agent-log/v9": 1,
        None: 1,
    }
    for item in prepared:
        descriptor = json.loads(item.export.request_path.read_text())
        assert descriptor["correlation"]["failure_mode"] == item.spec.mode.id
        assert descriptor["correlation"]["context"]["fixture_contract"] == seed.FIXTURE_CONTRACT
        assert item.export.durable_collection_complete is not item.spec.mode.incomplete_collection


def test_failure_seed_identity_is_additive_to_happy_path():
    assert seed.RUN_EXTERNAL_ID == "rl-ui-failure-modes-v1"
    assert seed.RUN_EXTERNAL_ID != seed.happy.RUN_EXTERNAL_ID
    assert seed.EXPERIMENT_SLUG != seed.happy.EXPERIMENT_SLUG
    assert all(spec.trial_name.startswith("rl-ui-failure-v1__") for spec in seed.failure_specs())


def test_failure_seed_runs_every_sample_through_a_real_connector_path(client, app, tmp_path):
    client.fail_open = False
    prepared = seed.prepare_seed(tmp_path)
    run = open_run(client, experiment="e", name="rl-ui-failure-seed")

    for item in prepared:
        seed.publish_sample(client, run, item)

    manifests = client.list_run_artifacts(run.id, kind="harbor_trial")
    spans = app.spans[run.id]
    rewards = app.metric_points_posted[run.id]

    assert len(manifests) == 8
    assert Counter(span["status"] for span in spans if span["span_type"] == "rollout") == {
        "failed": 4,
        "completed": 4,
    }
    assert len(rewards) == 5
    assert Counter(row["value"] for row in rewards)[0.0] == 2
    assert sum(span["span_type"] == "marker" for span in spans) == 1
    assert sum(
        ((manifest["meta"].get("capture") or {}).get("collection") or {}).get("state")
        == "partial"
        for manifest in manifests
    ) == 2
