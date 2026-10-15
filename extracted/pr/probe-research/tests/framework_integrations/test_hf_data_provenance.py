"""ProbeCallback records where a fine-tune starts and what it reads (plan
data-catalog R9, Q11), through a REAL `Trainer.train`.

A tiny BERT built from a config, made to look loaded from the Hub
(`config._name_or_path` + `_commit_hash`), trained on a real `datasets.Dataset`
named as a Hub dataset. The run must use a `model` source as `init` (never
`base_model`, which the server's closed role list refuses) and the dataset
source as `train` and `eval`, ids and revisions only. A model from a local
folder records nothing, and `capture_reads=False` turns it all off.

Skipped without transformers and datasets (the default agent-ci job).
"""

from __future__ import annotations

import os

import pytest

if os.environ.get("PROBE_REQUIRE_INTEGRATIONS") == "1":
    import transformers  # noqa: F401 -- an ImportError here fails the job
else:
    pytest.importorskip("transformers")
    pytest.importorskip("accelerate")
datasets = pytest.importorskip("datasets")

import torch  # noqa: E402
from transformers import BertConfig, BertForSequenceClassification, Trainer, TrainingArguments  # noqa: E402

import probe.integrations.huggingface as hf  # noqa: E402
from probe.integrations.huggingface import ProbeCallback  # noqa: E402
from probe.sdk import catalog, fluent  # noqa: E402
from tests.catalog_fake import CatalogFake  # noqa: E402
from tests.conftest import make_client  # noqa: E402

SHA = "0123456789abcdef0123456789abcdef01234567"


def _model(name: str | None) -> BertForSequenceClassification:
    torch.manual_seed(0)
    model = BertForSequenceClassification(
        BertConfig(vocab_size=32, hidden_size=8, num_hidden_layers=1, num_attention_heads=2,
                   intermediate_size=16, max_position_embeddings=16)
    )
    if name is not None:
        model.config._name_or_path = name
        model.config._commit_hash = SHA
    return model


def _data(n: int):
    generator = torch.Generator().manual_seed(n)
    ds = datasets.Dataset.from_dict({
        "input_ids": torch.randint(0, 32, (n, 6), generator=generator).tolist(),
        "labels": torch.randint(0, 2, (n,), generator=generator).tolist(),
    })
    ds.info.dataset_name = "glue"
    return ds


@pytest.fixture(autouse=True)
def _clean():
    def reset():
        hf._CALLBACK_RUNS.clear()
        hf._LAUNCHER_RUNS.clear()
        hf._ADOPTED.clear()
        hf._UNFINISHED.clear()
        fluent._current.set(None)
        fluent._process_default = None
        catalog._warned.clear()

    reset()
    yield
    reset()


@pytest.fixture
def fake(app, tmp_path, monkeypatch) -> CatalogFake:
    fake = CatalogFake(app)
    monkeypatch.setenv("PROBE_EPHEMERAL", "0")
    # The recorder's switch is this capture's switch too (conftest pins it off).
    monkeypatch.setenv("PROBE_CAPTURE_READS", "1")
    monkeypatch.setattr(fluent, "Client", lambda *a, **kw: make_client(fake, tmp_spool=tmp_path / "spool"))
    app.seed_experiment("e1")
    return fake


def _train(tmp_path, model, **callback_kw):
    args = TrainingArguments(
        output_dir=str(tmp_path / "out"), max_steps=2, per_device_train_batch_size=4, logging_steps=1,
        eval_strategy="steps", eval_steps=2, save_strategy="no", report_to="none", use_cpu=True,
        disable_tqdm=True, seed=0,
    )
    trainer = Trainer(model=model, args=args, train_dataset=_data(8), eval_dataset=_data(4),
                      callbacks=[ProbeCallback(experiment="e1", **callback_kw)])
    trainer.train()


def test_the_base_model_and_hub_datasets_are_recorded(fake, tmp_path):
    _train(tmp_path, _model("google-bert/bert-base-uncased"))
    models = [s for s in fake.sources.values() if s["kind"] == "model"]
    assert [(m["uri"], m["revision"]) for m in models] == [("https://huggingface.co/google-bert/bert-base-uncased", SHA)]
    # Train and eval are different rows of "glue": two revisions (each its fingerprint).
    data = {s["ref"]: s for s in fake.sources.values() if s["kind"] == "dataset"}
    assert {s["uri"] for s in data.values()} == {"https://huggingface.co/datasets/glue"} and len(data) == 2
    assert all(s["revision"] for s in data.values())
    roles = {(u["target"]["ref"], tuple(u["roles"])) for u in fake.uses}
    assert (models[0]["ref"], ("init",)) in roles
    assert sorted(role for ref, (role,) in roles if ref in data) == ["eval", "train"]
    assert len(fake.uses) == 3


def test_a_local_model_records_no_source(fake, tmp_path):
    _train(tmp_path, _model(str(tmp_path)))
    assert all(s["kind"] != "model" for s in fake.sources.values())


def test_capture_reads_false_records_nothing(fake, tmp_path):
    _train(tmp_path, _model("google-bert/bert-base-uncased"), capture_reads=False)
    assert not fake.sources and not fake.uses


def test_an_old_server_never_stops_training(fake, tmp_path):
    fake.old_server = True
    _train(tmp_path, _model("google-bert/bert-base-uncased"))
    assert not fake.uses
