"""Contract tests for the additive RL UI seed dataset."""

from __future__ import annotations

import gzip
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

from probe.connectors.harbor import parse_trial
from probe.connectors.harbor_export import consume_export_request
from probe.connectors.sandbox_state import BEGIN_BYTES, BUNDLE_DIRNAME
from tests.conftest import open_run

REPO_ROOT = Path(__file__).resolve().parents[2]
SEED_PATH = REPO_ROOT / "scripts" / "seed_rl_ui.py"


def _load_seed_module():
    spec = importlib.util.spec_from_file_location("probe_rl_ui_seed", SEED_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


seed = _load_seed_module()


def test_seed_matrix_keeps_two_prompt_groups_across_both_steps():
    specs = seed.sample_specs()

    assert len(specs) == 8
    assert Counter(spec.step for spec in specs) == {100: 4, 101: 4}
    assert Counter(spec.group.id for spec in specs) == {
        "prompt-code-refactor": 4,
        "prompt-incident-debug": 4,
    }
    assert Counter((spec.step, spec.group.id) for spec in specs) == {
        (100, "prompt-code-refactor"): 2,
        (100, "prompt-incident-debug"): 2,
        (101, "prompt-code-refactor"): 2,
        (101, "prompt-incident-debug"): 2,
    }
    prompts = {
        group.id: {spec.group.prompt for spec in specs if spec.group.id == group.id}
        for group in seed.PROMPT_GROUPS
    }
    assert all(len(values) == 1 for values in prompts.values())


def test_seed_prepares_producer_shaped_complete_exports(tmp_path):
    prepared = seed.prepare_seed(tmp_path)

    assert len(prepared) == 8
    assert all(item.export.durable_collection_complete for item in prepared)
    assert sum(
        (item.trial_dir / "artifacts" / BUNDLE_DIRNAME / BEGIN_BYTES).is_file()
        for item in prepared
    ) == 2

    for item in prepared:
        parsed = parse_trial(item.trial_dir)
        assert parsed.trajectory_format == "ATIF-v1.7"
        descriptor = json.loads(item.export.request_path.read_text())
        assert descriptor["arguments"]["expand"] is True
        assert descriptor["correlation"]["group_id"] == item.spec.group.id
        assert descriptor["correlation"]["sample_id"] == item.spec.sample_id

        meta = json.loads(
            (item.trial_dir / "artifacts" / BUNDLE_DIRNAME / "meta.json").read_text()
        )
        assert meta["schema"] == "probe.sandbox-state/1"
        assert meta["status"] == {"begin": "ok", "end": "ok"}
        assert meta["scan"]["hash_mode"] == "sha256"
        # This comes from production build_meta(), not the legacy backend-only
        # fixture shape that injected top-level manifest_fields.
        assert "manifest_fields" not in meta
        assert meta["base_state"] == {
            "ref": item.spec.group.id,
            "captured_here": (item.spec.step == seed.STEPS[0] and item.spec.sibling == 0),
        }
        assert meta["begin_bytes"]["ref"] == item.spec.group.id
        with gzip.open(
            item.trial_dir / "artifacts" / BUNDLE_DIRNAME / "begin-manifest.jsonl.gz",
            "rt",
        ) as manifest_file:
            assert all("h" in json.loads(line) for line in manifest_file if line.strip())


def test_seed_v2_identity_is_additive_to_the_existing_fixture():
    assert seed.RUN_EXTERNAL_ID == "rl-ui-happy-path-v2"
    assert all(spec.trial_name.startswith("rl-ui-v2__") for spec in seed.sample_specs())
    assert all(spec.external_key.startswith("miles:rl-ui-v2:") for spec in seed.sample_specs())


def test_seed_runs_all_eight_samples_through_the_real_connector(client, app, tmp_path):
    client.fail_open = False
    prepared = seed.prepare_seed(tmp_path)
    run = open_run(client, experiment="e", name="rl-ui-seed")

    for item in prepared:
        completed = consume_export_request(client, item.export.request_path, run_id=run.id)
        assert completed["status"] == "completed"

    manifests = client.list_run_artifacts(run.id, kind="harbor_trial")
    rewards = app.metric_points_posted[run.id]
    spans = app.spans[run.id]

    assert len(manifests) == 8
    assert len(rewards) == 8
    assert Counter(row["step_index"] for row in rewards) == {100: 4, 101: 4}
    assert Counter(row["labels"]["group"] for row in rewards) == {
        "prompt-code-refactor": 4,
        "prompt-incident-debug": 4,
    }
    assert sum(span["span_type"] == "rollout" for span in spans) == 8
    assert sum(span["span_type"] == "turn" for span in spans) >= 24
    assert sum(span["span_type"] == "tool_call" for span in spans) >= 8
    assert sum(
        span["span_type"] == "turn" and span["attributes"].get("subagent") is True
        for span in spans
    ) >= 2
