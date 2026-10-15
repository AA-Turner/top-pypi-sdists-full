"""Which Hub repos a Trainer starts from and reads (plan data-catalog R9, Q11;
`probe.integrations._hub`). Duck-typed, so no transformers or datasets is
needed; the callback that sends them is driven through a real Trainer in
`framework_integrations/test_hf_data_provenance.py`.

Test map C5 "HF": a Hub model -> an `init` source; a Hub dataset -> a `train`
source; a local path -> nothing (no wrong link).
"""

from __future__ import annotations

import types

import pytest

from probe.integrations import _hub


def _model(name, commit=None):
    config = types.SimpleNamespace(_name_or_path=name, _commit_hash=commit)
    return types.SimpleNamespace(config=config)


def _dataset(**fields):
    """An object whose class lives in the `datasets` package, as a real
    `datasets.Dataset` does."""
    cls = type("Dataset", (), {"__module__": "datasets.arrow_dataset"})
    obj = cls()
    info = types.SimpleNamespace(
        dataset_name=fields.pop("dataset_name", None),
        download_checksums=fields.pop("download_checksums", None),
    )
    obj.info = info
    for key, value in fields.items():
        setattr(obj, key, value)
    return obj


def test_a_hub_model_is_its_repo_with_the_commit():
    sha = "a" * 40
    got = _hub.base_model(_model("meta-llama/Llama-3.1-8B", sha))
    assert got == _hub.HubRef(uri="https://huggingface.co/meta-llama/Llama-3.1-8B", kind="model", revision=sha)
    assert _hub.base_model(_model("gpt2")).uri == "https://huggingface.co/gpt2"
    assert _hub.base_model(_model("gpt2", "not-a-sha")).revision is None


@pytest.mark.parametrize("name", ["/data/ckpt/step-4000", "./out", "~/models/x", "a--b/c", "a/b/c", "", None])
def test_a_local_or_odd_model_path_records_nothing(name):
    assert _hub.base_model(_model(name)) is None


def test_an_existing_local_folder_records_nothing(tmp_path, monkeypatch):
    (tmp_path / "org" / "model").mkdir(parents=True)
    monkeypatch.chdir(tmp_path)
    assert _hub.base_model(_model("org/model")) is None


def test_a_hub_dataset_from_its_download_urls_with_the_revision():
    ds = _dataset(download_checksums={"hf://datasets/allenai/c4@1588ec4/en/c4-train.00000.json.gz": {}},
                  _fingerprint="f00d")
    assert _hub.hub_dataset(ds) == _hub.HubRef("https://huggingface.co/datasets/allenai/c4", "dataset", "1588ec4")
    ds = _dataset(download_checksums={
        "https://huggingface.co/datasets/allenai/c4/resolve/abc123/en/x.json.gz": {}})
    assert _hub.hub_dataset(ds).revision == "abc123"


def test_a_hub_dataset_from_its_cache_folder_takes_the_fingerprint():
    ds = _dataset(cache_files=[{"filename": "/root/.cache/huggingface/datasets/allenai___c4/en/0.0.0/x/c4-train.arrow"}],
                  _fingerprint="9f86d081")
    assert _hub.hub_dataset(ds) == _hub.HubRef("https://huggingface.co/datasets/allenai/c4", "dataset", "9f86d081")


def test_local_files_and_other_objects_record_nothing():
    assert _hub.hub_dataset(_dataset(dataset_name="json", cache_files=[{"filename": "/tmp/json/default/x.arrow"}])) is None
    assert _hub.hub_dataset(types.SimpleNamespace(info=types.SimpleNamespace(dataset_name="c4"))) is None
    assert _hub.hub_dataset(None) is None


def test_a_named_hub_dataset_without_files_still_counts():
    assert _hub.hub_dataset(_dataset(dataset_name="squad", _fingerprint="ab")).uri == "https://huggingface.co/datasets/squad"


def test_the_dataset_behind_wrapped_dataloaders():
    ds = _dataset(dataset_name="squad")
    loader = types.SimpleNamespace(dataset=types.SimpleNamespace(dataset=ds))
    assert _hub.loader_dataset(loader) is ds


def test_a_real_datasets_object_from_local_data_records_nothing():
    datasets = pytest.importorskip("datasets")
    assert _hub.hub_dataset(datasets.Dataset.from_dict({"x": [1, 2]})) is None
