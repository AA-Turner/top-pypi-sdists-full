"""`probe source|dataset|checkpoint|provenance` (plan data-catalog C5, C8, C11)
and the CLI's catalog-era refusals: a 402 over the hosted-data cap (C8i) and a
loose-file write after the freeze (C6's 410).

The commands run against `tests.catalog_fake.CatalogFake` through a real
Client, so what is asserted is what reaches the wire. Test map: C5 CLI
(dataset/source/checkpoint/provenance commands; `--from` step), F22 (`--from`
files under the producer's project, else refuses), C11b client half
(`dataset download` via the files list and the existing download batch),
C8 client paths.
"""

from __future__ import annotations

import importlib
import json
import re

import pytest
from typer.testing import CliRunner

from probe import errors
from probe.sdk import catalog
from tests.catalog_fake import CatalogFake
from tests.conftest import make_client, open_run

cli_main = importlib.import_module("probe.cli.main")


@pytest.fixture(autouse=True)
def _fresh():
    catalog._warned.clear()


@pytest.fixture
def fake(monkeypatch) -> CatalogFake:
    fake = CatalogFake()
    monkeypatch.setattr(cli_main, "_client", lambda **_kw: make_client(fake))
    return fake


@pytest.fixture
def run_id(fake) -> str:
    client = make_client(fake)
    run = open_run(client, experiment="e", name="dedup-v2", heartbeat=False, capture_outputs=False)
    client.close()
    return run.id


def _cli(*args: str):
    return CliRunner().invoke(cli_main.app, list(args), catch_exceptions=False)


def _plain(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"\x1b\[[0-9;]*m", "", text))


def _folder(root, files):
    for rel, data in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_bytes(data)
    return root


def test_source_add_prints_the_ref_and_key(fake):
    first = _cli("source", "add", "https://huggingface.co/datasets/allenai/c4", "--revision", "1588ec4",
                 "--license", "ODC-BY")
    assert first.exit_code == 0, first.output
    ref = next(iter(fake.sources.values()))["ref"]
    assert first.output.strip() == f"{ref}  hf:datasets/allenai/c4@1588ec4  (new)"
    again = _cli("source", "add", "https://huggingface.co/datasets/allenai/c4", "--revision", "1588ec4")
    assert again.output.strip().endswith("(existing)")
    listed = _cli("source", "list")
    assert "hf:datasets/allenai/c4@1588ec4" in listed.output and "ODC-BY" in listed.output


def test_dataset_add_from_a_run_registers_its_file(fake, run_id, tmp_path):
    src = _cli("source", "add", "https://huggingface.co/datasets/allenai/c4")
    source_ref = src.output.split()[0]
    data = _folder(tmp_path / "c4-clean", {"a.jsonl": b"{}\n" * 3, "b.jsonl": b"{}\n"})
    result = _cli("dataset", "add", str(data), "--name", "c4-clean", "--run", run_id, "--source", source_ref,
                  "--note", "dropped 1,204 seqs", "--no-preview")
    assert result.exit_code == 0, result.output
    assert result.output.startswith("dataset:c4-clean@1  ") and "identity bytes  from run dedup-v2" in result.output
    body = fake.registrations[0]
    assert body["sources"] == [source_ref] and body["change"] == {"note": "dropped 1,204 seqs"}
    assert body["run_file"]["run_id"] == run_id and body["run_file"]["meta"]["files"] == 2


def test_dataset_add_with_no_run_is_a_reference(fake, tmp_path):
    result = _cli("dataset", "add", "s3://lab/pdb/2026-09", "--name", "pdb-motif")
    assert result.exit_code == 0, result.output
    assert fake.registrations[0]["reference"]["identity"] == "pointer"
    assert set(fake.registrations[0]) == {"name", "reference"}


def test_a_step_by_hand_is_a_finished_run_under_the_producers_project(fake, run_id, tmp_path):
    v1 = _folder(tmp_path / "v1", {"a.jsonl": b"{}\n" * 4})
    _cli("dataset", "add", str(v1), "--name", "c4", "--run", run_id, "--no-preview")
    fake.datasets["c4"]["versions"][0]["producer"]["project"] = "project-e"
    v2 = _folder(tmp_path / "v2", {"a.jsonl": b"{}\n" * 3})
    result = _cli("dataset", "add", str(v2), "--name", "c4", "--from", "dataset:c4@1", "--step", "dedup by hand",
                  "--note", "dropped a duplicate")
    assert result.exit_code == 0, result.output
    assert "recording the step under project project-e" in result.output
    step = next(r for r in fake.base.runs.values() if r.get("name") == "dedup by hand")
    assert step["status"] == "completed" and (step.get("metadata") or {}).get("recorded_after") is True
    assert {"run_id": step["id"], "target": fake._target("dataset:c4@1"), "roles": ["other"], "share": None,
            "provenance": "human"} in fake.uses
    assert fake.registrations[-1]["run_file"]["run_id"] == step["id"]
    assert result.output.splitlines()[-1].startswith("dataset:c4@2  ")


def test_a_step_by_hand_with_no_project_to_file_it_under_is_refused(fake, tmp_path):
    v1 = _folder(tmp_path / "v1", {"a.jsonl": b"{}\n"})
    _cli("dataset", "add", str(v1), "--name", "loose")  # a reference: no producer run
    v2 = _folder(tmp_path / "v2", {"a.jsonl": b"{}\n{}\n"})
    result = CliRunner().invoke(cli_main.app, ["dataset", "add", str(v2), "--name", "loose", "--from", "dataset:loose@1"])
    assert result.exit_code == 1
    assert "--project P" in _plain(result.output) and len(fake.registrations) == 1


def test_dataset_use_and_checkpoint_use(fake, run_id, tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_DAEMON_SESSION", "daemon-session-1")
    _cli("dataset", "add", str(_folder(tmp_path / "d", {"a.jsonl": b"{}\n"})), "--name", "val", "--run", run_id,
         "--no-preview")
    used = _cli("dataset", "use", "dataset:val@1", "--run", run_id, "--role", "validation", "--share", "1",
                "--reason", "the held-out split", "--evidence", "main:1200:0", "--evidence", "agent-7:88:2")
    assert used.exit_code == 0, used.output
    assert used.output.strip() == f"run {run_id} uses dataset:val@1 (validation)"
    # The server answers the row it resolved and the save as it holds it now:
    # the CLI prints THAT, not the step the ref named.
    fake.checkpoint_pins["checkpoint:sft-7b@step400"] = {"step": 400, "uri": "s3://ckpt/sft-7b/400"}
    ckpt = _cli("checkpoint", "use", "checkpoint:sft-7b@step400", "--run", run_id, "--role", "eval")
    assert ckpt.exit_code == 0, ckpt.output
    resolved = fake.uses[-1]["target"]["ref"]
    assert resolved.startswith("checkpoint:") and "@" not in resolved
    assert ckpt.output.strip() == f"run {run_id} uses {resolved} (step 400, s3://ckpt/sft-7b/400) (eval)"
    fake.checkpoint_pins["checkpoint:sft-7b@step100"] = None  # no `pinned` in the answer
    started = _cli("checkpoint", "use", "checkpoint:sft-7b@step100", "--run", run_id)
    assert started.output.strip() == f"run {run_id} uses {fake.uses[-1]['target']['ref']} (init)"
    assert [(u["roles"], u["provenance"]) for u in fake.uses] == [
        (["validation"], "human"), (["eval"], "human"), (["init"], "human")
    ]
    # Evidence is `{session, event}` per event id, as `probe edge add --evidence` sends it.
    assert fake.uses[0]["reason"] == "the held-out split"
    assert fake.uses[0]["evidence"] == [{"session": "daemon-session-1", "event": "main:1200:0"},
                                        {"session": "daemon-session-1", "event": "agent-7:88:2"}]
    assert "reason" not in fake.uses[1] and "evidence" not in fake.uses[1]


@pytest.mark.parametrize("group, ref", [("dataset", "dataset:val@1"), ("checkpoint", "checkpoint:sft-7b@step400")])
def test_evidence_with_no_session_or_no_event_id_is_a_usage_error(fake, run_id, monkeypatch, group, ref):
    """An event id names nothing the audit can open without its session (R7)."""
    monkeypatch.delenv("PROBE_DAEMON_SESSION", raising=False)
    monkeypatch.setattr(cli_main.agent_session, "session_id_from_env", lambda *a, **k: None)
    no_session = CliRunner().invoke(cli_main.app, [group, "use", ref, "--run", run_id, "--evidence", "main:6:0"])
    assert no_session.exit_code == 2 and "PROBE_DAEMON_SESSION" in _plain(no_session.output)
    monkeypatch.setenv("PROBE_DAEMON_SESSION", "daemon-session-1")
    not_an_id = CliRunner().invoke(cli_main.app, [group, "use", ref, "--run", run_id, "--evidence", "eval.py read it"])
    assert not_an_id.exit_code == 2 and "--evidence" in _plain(not_an_id.output)
    assert fake.uses == []


#: A ref the server resolves when the link is MADE (D16): from the CLI, after
#: the run used the data, so it could pin a newer version or save.
MOVING_REFS = [
    ("dataset", "dataset:val", "probe dataset show dataset:val"),
    ("dataset", "dataset:val@latest", "probe dataset show dataset:val"),
    ("checkpoint", "checkpoint:sft-7b@latest", "probe checkpoint list --run sft-7b"),
    ("checkpoint", "checkpoint:sft-7b@best", "probe checkpoint list --run sft-7b"),
    ("checkpoint", "checkpoint:sft-7b@best:val_loss", "probe checkpoint list --run sft-7b"),
    ("dataset", "source:hf:datasets/allenai/c4", "probe source list"),
]


@pytest.mark.parametrize(("group", "ref", "lister"), MOVING_REFS)
def test_a_moving_ref_is_refused_before_anything_is_sent(fake, run_id, group, ref, lister):
    result = CliRunner().invoke(cli_main.app, [group, "use", ref, "--run", run_id])
    assert result.exit_code == 1
    plain = _plain(result.output)
    assert ref in plain and lister in plain
    assert fake.uses == []


def test_a_step_from_a_moving_ref_is_refused_before_anything_is_recorded(fake, run_id, tmp_path):
    """`--from` records the step after it happened, often by the agent."""
    _cli("dataset", "add", str(_folder(tmp_path / "v1", {"a.jsonl": b"{}\n"})), "--name", "c4", "--run", run_id,
         "--no-preview")
    runs = len(fake.base.runs)
    result = CliRunner().invoke(cli_main.app, ["dataset", "add", str(_folder(tmp_path / "v2", {"a.jsonl": b"{}\n"})),
                                               "--name", "c4", "--from", "dataset:c4", "--step", "dedup"])
    assert result.exit_code == 1
    assert "probe dataset show dataset:c4" in _plain(result.output)
    assert (len(fake.base.runs), len(fake.registrations), fake.uses) == (runs, 1, [])


UUID = "3f0c6a1e-8b0d-4c4e-9a43-0f3a8f0e6c11"


@pytest.mark.parametrize(
    ("ref", "moving"),
    [
        *[(ref, True) for _group, ref, _lister in MOVING_REFS],
        (f"dataset:{UUID}", True),
        ("dataset:val@1", False), ("dataset:val@v2", False), (f"dataset:{UUID}@4", False),
        (f"source:{UUID}", False), ("source:hf:datasets/allenai/c4@1588ec4", False),
        (f"artifact_version:{UUID}", False), (f"artifact:{UUID}", False),
        ("checkpoint:sft-7b@step400", False), (f"checkpoint:{UUID}", False),
        # A form the client cannot read is left to the server to refuse.
        ("checkpoint:sft-7b@soon", False), ("nonsense", False),
    ],
)
def test_which_refs_move(ref, moving):
    assert catalog.is_moving_ref(ref) is moving


def test_dataset_list_is_a_table(fake, run_id, tmp_path):
    _cli("dataset", "add", str(_folder(tmp_path / "d", {"a.jsonl": b"{}\n" * 9})), "--name", "c4-clean",
         "--run", run_id, "--no-preview")
    out = _cli("dataset", "list").output.splitlines()
    assert out[0].split() == ["NAME", "LATEST", "IDENTITY", "SIZE", "MADE", "BY", "USED", "BY"]
    assert out[1].split()[:5] == ["c4-clean", "v1", "bytes", "27", "B"]
    assert "dedup-v2 (data-prep)" in out[1]
    assert json.loads(_cli("dataset", "list", "--json").output)["items"][0]["name"] == "c4-clean"


def test_dataset_download_writes_a_hosted_version_and_names_a_reference(fake, run_id, tmp_path):
    data = _folder(tmp_path / "d", {"a.jsonl": b'{"a":1}\n', "sub/b.jsonl": b'{"b":2}\n'})
    hosted = _cli("dataset", "add", str(data), "--name", "hosted", "--upload")
    assert hosted.exit_code == 0, hosted.output
    out = tmp_path / "out"
    got = _cli("dataset", "download", "dataset:hosted@1", "-o", str(out))
    assert got.exit_code == 0, got.output
    assert (out / "a.jsonl").read_bytes() == b'{"a":1}\n' and (out / "sub" / "b.jsonl").read_bytes() == b'{"b":2}\n'
    assert fake.calls("POST", "/v1/artifacts/download/batch")
    _cli("dataset", "add", str(_folder(tmp_path / "r", {"x.jsonl": b"{}\n"})), "--name", "kept", "--run", run_id,
         "--no-preview")
    where = _cli("dataset", "download", "dataset:kept", "-o", str(tmp_path / "out2"))
    assert where.exit_code == 0 and "is kept outside Probe" in where.output and "nothing to download" in where.output


def _stored_version(fake, run_id, tmp_path, name: str, data: bytes) -> dict:
    """A team dataset version over a file Probe stores: the run's uploaded
    file, pinned with `from_artifact_id` (the one-file `/files` path)."""
    from probe.sdk.anchors import Anchor

    path = tmp_path / f"{len(data)}-{name}.jsonl"
    path.write_bytes(data)
    client = make_client(fake)
    try:
        row = client.upload_file(Anchor.RUN, run_id, "train.jsonl", str(path))
        return client.register_dataset({"name": name, "from_artifact_id": row["id"]})
    finally:
        client.close()


def test_dataset_download_fetches_an_older_version_by_its_download(fake, run_id, tmp_path):
    """`/files` names the ENTRY for the live version only (`artifact_id`); an
    older version of a one-file dataset carries `download: {artifact_id,
    version}` instead, fetched through `POST /v1/artifacts/{id}/versions/{n}/download`."""
    v1 = _stored_version(fake, run_id, tmp_path, "weights-ds", b'{"v":1}\n')
    _stored_version(fake, run_id, tmp_path, "weights-ds", b'{"v":2,"more":true}\n')
    entry = v1["entry"]["id"]
    old = _cli("dataset", "download", "dataset:weights-ds@1", "-o", str(tmp_path / "old"))
    assert old.exit_code == 0, old.output
    assert (tmp_path / "old" / "train.jsonl").read_bytes() == b'{"v":1}\n'
    assert fake.calls("POST", f"/v1/artifacts/{entry}/versions/1/download")
    assert not fake.calls("POST", "/v1/artifacts/download/batch")
    live = _cli("dataset", "download", "dataset:weights-ds@2", "-o", str(tmp_path / "live"))
    assert live.exit_code == 0, live.output
    assert (tmp_path / "live" / "train.jsonl").read_bytes() == b'{"v":2,"more":true}\n'
    assert json.loads(fake.calls("POST", "/v1/artifacts/download/batch")[-1].content) == {"artifact_ids": [entry]}
    one = tmp_path / "one.jsonl"
    one.write_bytes(b"{}\n")
    _cli("dataset", "add", str(one), "--name", "kept-file", "--run", run_id, "--no-preview")
    where = _cli("dataset", "download", "dataset:kept-file", "-o", str(tmp_path / "out3"))
    assert where.exit_code == 0 and "is kept outside Probe" in where.output


def test_dataset_add_upload_asks_the_door_until_nothing_is_deferred(fake, run_id, tmp_path):
    """`--upload` loops the door (one line per round), names the producing run
    in `hosted`, and the version downloads page by page."""
    fake.door_max_uploads = 2
    fake.files_page = 2
    files = {f"part-{i}.jsonl": f'{{"i":{i}}}\n'.encode() for i in range(3)}
    data = _folder(tmp_path / "d", files)
    added = CliRunner().invoke(cli_main.app, ["dataset", "add", str(data), "--name", "rounds", "--upload",
                                              "--run", run_id], catch_exceptions=False)
    assert added.exit_code == 0, added.output
    assert len(fake.upload_asks) == 2 and len(fake.registrations) == 1
    assert fake.registrations[0]["hosted"] == {"manifest_hash": fake.upload_asks[0]["manifest_hash"], "run_id": run_id}
    assert "hosting round 1: 2 file(s) to send" in added.output and "hosting round 2: 1 file(s) to send" in added.output
    out = tmp_path / "out"
    got = _cli("dataset", "download", "dataset:rounds", "-o", str(out))
    assert got.exit_code == 0, got.output
    assert {p.name: p.read_bytes() for p in out.iterdir()} == files
    assert len(fake.calls("GET", "/v1/catalog/datasets/dataset:rounds/files")) == 2


def test_a_confirm_refused_for_bytes_over_the_reservation_names_the_file(fake, tmp_path):
    fake.reserve_less = True
    data = _folder(tmp_path / "d", {"shard-0.jsonl": b'{"a":1}\n'})
    got = CliRunner().invoke(cli_main.app, ["dataset", "add", str(data), "--name", "too-big", "--upload"])
    assert got.exit_code == 1 and not fake.registrations
    assert "shard-0.jsonl" in got.output and "larger than the size the hosting door reserved" in got.output


def test_upload_over_the_hosted_cap_explains_itself(fake, tmp_path):
    fake.hosted_cap = 1
    data = _folder(tmp_path / "d", {"a.jsonl": b"{}\n" * 20})
    code = cli_main.main(["dataset", "add", str(data), "--name", "big", "--upload"])
    assert code == 1 and not fake.registrations


def test_the_402_names_sizes_and_the_reference_way_out(capsys, monkeypatch):
    def refused(*_a, **_k):
        raise errors.error_for(402, {
            "message": "Your team's hosted data is at the free plan's cap.", "code": "limit_reached",
            "limit": "hosted_data_bytes", "current": 49, "maximum": 50, "plan": "free",
        })

    monkeypatch.setattr(cli_main, "_client", lambda **_kw: _Raising(refused))
    assert cli_main.main(["source", "list"]) == 1
    err = _plain(capsys.readouterr().err)
    assert "at 49 GB of 50 GB." in err and "leave out --upload" in err and "stays readable" in err


def test_an_unknown_limit_still_renders_plainly(capsys, monkeypatch):
    def refused(*_a, **_k):
        raise errors.error_for(402, {"message": "A future cap.", "limit": "future_thing", "current": 3, "maximum": 2})

    monkeypatch.setattr(cli_main, "_client", lambda **_kw: _Raising(refused))
    assert cli_main.main(["source", "list"]) == 1
    err = _plain(capsys.readouterr().err)
    assert "error: A future cap." in err and "at 3 of 2." in err and "--upload" not in err


def test_a_frozen_loose_file_write_names_where_files_go_now(capsys, monkeypatch, tmp_path):
    path = tmp_path / "notes.txt"
    path.write_text("x")

    def frozen(*_a, **_k):
        raise errors.ClientTooOldError("Workspace files are frozen. Upgrade to probe-research 0.251.0",
                                       status=410, min_version="0.251.0")

    monkeypatch.setattr(cli_main, "_client", lambda **_kw: _Raising(frozen))
    assert cli_main.main(["shared", "add", str(path)]) == 1
    err = _plain(capsys.readouterr().err)
    assert "read-only now" in err and "probe dataset add PATH --name NAME" in err and "Upgrade" not in err


def test_checkpoint_list_marks_rewound_saves(fake):
    fake.checkpoints = [
        {"ref": "checkpoint:1", "run": {"name": "sft-7b"}, "step": 4000, "best": {"monitor": "loss", "score": 0.1},
         "rewound": None, "stored": "reference", "location": {"host": "gpu-3", "local_path": "/ckpt/sft-7b/step-4000"},
         "size_bytes": 15_900_000_000},
        {"ref": "checkpoint:2", "run": {"name": "sft-7b"}, "step": 5000, "best": None, "rewound": {"to_step": 4000},
         "stored": "reference", "location": {"host": "gpu-3", "local_path": "/ckpt/sft-7b/step-5000"},
         "size_bytes": 15_900_000_000},
    ]
    out = _cli("checkpoint", "list", "--project", "odyssey-1b").output.splitlines()
    assert out[0].split() == ["RUN", "STEP", "BEST", "STORED", "WHERE", "SIZE"]
    assert out[1].split() == ["sft-7b", "4,000", "best", "loss", "reference", "gpu-3:/ckpt/sft-7b/step-4000", "15.9", "GB"]
    assert out[2].split()[:3] == ["sft-7b", "5,000", "rewound"]
    asked = fake.calls("GET", "/v1/catalog/checkpoints")[0]
    assert dict(asked.url.params) == {"project": "odyssey-1b", "limit": "100"}


def test_checkpoint_list_says_in_probe_for_bytes_probe_holds(fake):
    """Found by the prod smoke: a checkpoint stored in Probe printed its
    internal blob address (`r2://<bucket>/<tenant>/blobs/<sha>`) as WHERE. A
    reference keeps its host:path, else its uri."""
    blob = "r2://prbe-research/probe/blobs/" + "a" * 64
    fake.checkpoints = [
        {"ref": "checkpoint:1", "run": {"name": "sft-7b"}, "step": 10, "best": None, "rewound": None,
         "stored": "stored", "location": {"uri": blob, "local_path": "/ckpt/step-10.pt", "host": "gpu-3"},
         "size_bytes": 4096},
        {"ref": "checkpoint:2", "run": {"name": "sft-7b"}, "step": 20, "best": None, "rewound": None,
         "stored": "reference", "location": {"uri": "s3://lab/ckpt/step-20", "local_path": None, "host": None},
         "size_bytes": 4096},
    ]
    out = _cli("checkpoint", "list").output
    rows = out.splitlines()
    assert rows[1].split()[:5] == ["sft-7b", "10", "stored", "in", "Probe"]
    assert rows[2].split()[:4] == ["sft-7b", "20", "reference", "s3://lab/ckpt/step-20"]
    assert "r2://" not in out


def test_provenance_steps_names_a_run_the_server_labels(fake):
    """A server that sends the run's `label` (shipped before `name` joined the
    steps' run) still prints the run's name, never its ref."""
    fake.steps_answer = {
        "target": "dataset:c4-clean@1",
        "sources": [],
        "steps": [{"order": 1, "run": {"ref": "run:quiet-otter-12", "label": "dedup-v2"},
                   "outputs": ["dataset:c4-clean@1"]}],
    }
    out = _cli("provenance", "dataset:c4-clean@1", "--steps").output.splitlines()
    assert out[0].split()[:3] == ["1", "run", "dedup-v2"]


def test_provenance_steps_prints_the_methods_view(fake):
    fake.steps_answer = {
        "target": "checkpoint:sft-7b@best",
        "sources": [{"ref": "source:1", "canonical_key": "hf:datasets/allenai/c4", "revision": "1588ec4", "license": "ODC-BY"}],
        "steps": [
            {"order": 2, "run": {"name": "dedup-v2"}, "outputs": ["dataset:c4-clean@3"],
             "change": {"note": "dropped 1,204 seqs >90% identical to test"}},
            {"order": 1, "run": {"name": "download-c4"}, "outputs": ["dataset:c4-raw@1"]},
        ],
    }
    out = _cli("provenance", "checkpoint:sft-7b@best", "--steps").output.splitlines()
    assert out[0].split() == ["1", "source", "hf:datasets/allenai/c4@1588ec4", "(ODC-BY)"]
    assert out[1].split() == ["2", "run", "download-c4", "->", "dataset:c4-raw@1"]
    assert out[2].split()[:5] == ["3", "run", "dedup-v2", "->", "dataset:c4-clean@3"]
    assert out[2].endswith('"dropped 1,204 seqs >90% identical to test"')


def test_provenance_steps_prints_each_output_with_its_own_note(fake):
    """Found by the prod smoke: a step that made two versions printed the
    step's one `change` beside the first, which was the OTHER version's note.
    Each output now carries its own (`outputs_detail`); the step's `change`
    is null when it made more than one."""
    fake.steps_answer = {
        "target": "checkpoint:1",
        "sources": [],
        "steps": [
            {"order": 1, "run": {"name": "dedup"}, "change": None,
             "outputs": ["dataset:smoke-c4-clean@1", "dataset:smoke-hosted@1"],
             "outputs_detail": [
                 {"ref": "dataset:smoke-c4-clean@1", "change": {"note": "deduped"}},
                 {"ref": "dataset:smoke-hosted@1", "change": {"note": "hosted copy"}},
             ]},
            {"order": 2, "run": {"name": "validate"}, "check": True, "outputs": [], "outputs_detail": [],
             "change": {"note": "no test leakage"}},
            {"order": 3, "run": {"name": "sft"}, "outputs": ["checkpoint:1"],
             "outputs_detail": [{"ref": "checkpoint:1", "change": None}]},
        ],
    }
    out = _cli("provenance", "checkpoint:1", "--steps").output.splitlines()
    assert out[0].split()[:5] == ["1", "run", "dedup", "->", "dataset:smoke-c4-clean@1"]
    assert out[0].endswith('"deduped"')
    assert out[1].split()[:2] == ["->", "dataset:smoke-hosted@1"] and out[1].endswith('"hosted copy"')
    assert "  run  " not in out[1], "a second output is not another step"
    assert out[2].split()[:4] == ["2", "run", "validate", "->"] and out[2].endswith('"no test leakage"')
    assert out[3].split() == ["3", "run", "sft", "->", "checkpoint:1"]


def test_provenance_down_asks_downstream(fake):
    fake.provenance_answer = {
        "root": "s", "nodes": [{"id": "s", "type": "source", "ref": "source:1"}, {"id": "r", "type": "run", "label": "sft"}],
        "edges": [{"from": "r", "to": "s", "relation": "consumes", "roles": ["train"]}],
        "truncated": True, "truncated_reason": "500 nodes", "hidden": 2,
    }
    result = _cli("provenance", "source:1", "--down", "--depth", "3")
    assert result.exit_code == 0
    assert "run sft  --consumes train-->  source source:1" in result.output
    asked = fake.calls("GET", "/v1/provenance")[0]
    assert dict(asked.url.params) == {"ref": "source:1", "direction": "downstream", "depth": "3"}


class _Raising:
    """A client whose every catalog/upload call raises what it is given."""

    def __init__(self, fail):
        self._fail = fail

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def __getattr__(self, name):
        return self._fail


# -- review of #2791 (FIX FIRST): regressions --------------------------------------


def test_the_daemon_never_uploads_a_preview_sample(fake, run_id, tmp_path, monkeypatch):
    """F3: the daemon's precheck sends `dataset add` paths unscanned because
    their bytes never leave; a preview sample would be bytes."""
    monkeypatch.setenv("PROBE_DAEMON_SESSION", "s-1")
    data = _folder(tmp_path / "d", {"a.jsonl": b'{"secret": "x"}\n' * 5})
    result = _cli("dataset", "add", str(data), "--name", "by-daemon", "--run", run_id)
    assert result.exit_code == 0, result.output
    assert not [a for a in fake.base.artifacts.get(run_id, []) if a["name"].startswith(catalog.PREVIEW_PREFIX)]
    monkeypatch.delenv("PROBE_DAEMON_SESSION")
    _cli("dataset", "add", str(data), "--name", "by-hand", "--run", run_id)
    assert [a for a in fake.base.artifacts.get(run_id, []) if a["name"].startswith(catalog.PREVIEW_PREFIX)]


def test_source_list_reads_the_nested_counts(fake, run_id):
    """F4: the server nests `counts: {runs_using, datasets_derived}`."""
    ref = _cli("source", "add", "https://huggingface.co/datasets/allenai/c4").output.split()[0]
    _cli("dataset", "use", ref, "--run", run_id)
    row = next(line for line in _cli("source", "list").output.splitlines() if ref in line)
    assert "1 runs" in row


def test_a_failed_use_closes_the_hand_step_as_failed(fake, run_id, tmp_path):
    """F9: `--from` with a ref the server does not know: the step run it
    opened is closed `failed`, never left running."""
    data = _folder(tmp_path / "v2", {"a.jsonl": b"{}\n"})
    result = CliRunner().invoke(cli_main.app, ["dataset", "add", str(data), "--name", "x", "--from", "dataset:nope@1",
                                               "--project", "project-e", "--step", "by hand"])
    assert result.exit_code != 0
    step = next(r for r in fake.base.runs.values() if r.get("name") == "by hand")
    assert step["status"] == "failed"


def test_source_add_leaves_the_kind_to_the_server(fake):
    """F12."""
    _cli("source", "add", "https://huggingface.co/meta-llama/Llama-3.1-8B")
    assert "kind" not in json.loads(fake.calls("POST", "/v1/sources")[0].content)


def test_a_410_on_version_add_is_the_freeze_only_when_the_server_says_too_old(capsys, monkeypatch):
    """F14: a plain 410 (not the freeze's `client_too_old`, not the trash)
    on `artifact version-add` prints the server's own error."""
    def gone(*_a, **_k):
        raise errors.error_for(410, "this version was deleted")

    monkeypatch.setattr(cli_main, "_client", lambda **_kw: _Raising(gone))
    assert cli_main.main(["artifact", "version-add", "a-1", "--uri", "s3://b/k"]) == 1
    err = _plain(capsys.readouterr().err)
    assert "this version was deleted" in err and "read-only now" not in err

    def frozen(*_a, **_k):
        raise errors.ClientTooOldError("Shared files are frozen.", status=410, min_version="0.251.0")

    monkeypatch.setattr(cli_main, "_client", lambda **_kw: _Raising(frozen))
    assert cli_main.main(["artifact", "version-add", "a-1", "--uri", "s3://b/k"]) == 1
    assert "read-only now" in _plain(capsys.readouterr().err)
