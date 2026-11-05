"""Data catalog verbs from training jobs: refs, server answers, identity, hosting, manifests, log_dataset.
One front door; names are served live, so a patch on a piece reaches every caller."""

from __future__ import annotations

import importlib

# Every piece loads here; names are served live below (see module docstring).
for _piece in (
    "probe.sdk.artifact.record_formats.lines",
    "probe.sdk.artifact.record_formats.parquet",
    "probe.sdk.catalog.hosting",
    "probe.sdk.catalog.identity",
    "probe.sdk.catalog.log_dataset",
    "probe.sdk.catalog.manifest",
    "probe.sdk.catalog.refs",
    "probe.sdk.catalog.server",
    "probe.sdk.catalog.catalog",
):
    importlib.import_module(_piece)
del _piece

# `log_dataset` is both a piece and its function: importing the piece bound the module, so rebind the function.
log_dataset = importlib.import_module("probe.sdk.catalog.log_dataset").log_dataset

#: Every name the front door serves -> the module that defines it.
_HOMES = {
    # probe.sdk.artifact.record_formats.lines
    "PREVIEW_MAX_RECORDS": "probe.sdk.artifact.record_formats.lines",
    "PREVIEW_MAX_BYTES": "probe.sdk.artifact.record_formats.lines",
    "_LINE_SUFFIXES": "probe.sdk.artifact.record_formats.lines",
    "_HEADER_SUFFIXES": "probe.sdk.artifact.record_formats.lines",
    "preview_sample": "probe.sdk.artifact.record_formats.lines",
    # probe.sdk.artifact.record_formats.parquet
    "_parquet_sample": "probe.sdk.artifact.record_formats.parquet",
    # probe.sdk.catalog.hosting
    "MANIFEST_SECONDS": "probe.sdk.catalog.hosting",
    "DOOR_SECONDS": "probe.sdk.catalog.hosting",
    "DOOR_ANSWERS_AT_LEAST": "probe.sdk.catalog.hosting",
    "DOOR_SPARE_CALLS": "probe.sdk.catalog.hosting",
    "HOSTED_VERIFY_SECONDS": "probe.sdk.catalog.hosting",
    "HOSTED_VERIFY_POLL_SECONDS": "probe.sdk.catalog.hosting",
    "HOSTED_PREFIX": "probe.sdk.catalog.hosting",
    "door_call_limit": "probe.sdk.catalog.hosting",
    "host": "probe.sdk.catalog.hosting",
    "_declared_size": "probe.sdk.catalog.hosting",
    "_upload_blob": "probe.sdk.catalog.hosting",
    "_upload_parts": "probe.sdk.catalog.hosting",
    "reopen_hosted": "probe.sdk.catalog.hosting",
    "_await_verified": "probe.sdk.catalog.hosting",
    # probe.sdk.catalog.identity
    "CHANGE_STAT_KEYS": "probe.sdk.catalog.identity",
    "HASH_DEADLINE_SECONDS": "probe.sdk.catalog.identity",
    "FULL_HASH_DEADLINE_SECONDS": "probe.sdk.catalog.identity",
    "HASH_GRACE_SECONDS": "probe.sdk.catalog.identity",
    "_SCHEME": "probe.sdk.catalog.identity",
    "pointer_hash": "probe.sdk.catalog.identity",
    "Prepared": "probe.sdk.catalog.identity",
    "_remote": "probe.sdk.catalog.identity",
    "prepare": "probe.sdk.catalog.identity",
    "_hash_local": "probe.sdk.catalog.identity",
    "_hash_off_thread": "probe.sdk.catalog.identity",
    "_fresh_budget": "probe.sdk.catalog.identity",
    "run_file_spec": "probe.sdk.catalog.identity",
    "reference_spec": "probe.sdk.catalog.identity",
    "_stat_count": "probe.sdk.catalog.identity",
    "change_stats": "probe.sdk.catalog.identity",
    "registration_body": "probe.sdk.catalog.identity",
    # probe.sdk.catalog.log_dataset
    "REGISTER_WAIT_SECONDS": "probe.sdk.catalog.log_dataset",
    "REGISTER_DEADLINE_SECONDS": "probe.sdk.catalog.log_dataset",
    "PREVIEW_PREFIX": "probe.sdk.catalog.log_dataset",
    "_previewable": "probe.sdk.catalog.log_dataset",
    "upload_preview": "probe.sdk.catalog.log_dataset",
    "_run_sender": "probe.sdk.catalog.log_dataset",
    "log_dataset": "probe.sdk.catalog.log_dataset",
    "_log_dataset": "probe.sdk.catalog.log_dataset",
    "_ship_manifest": "probe.sdk.catalog.log_dataset",
    "_queue_registration": "probe.sdk.catalog.log_dataset",
    "_record_run_file": "probe.sdk.catalog.log_dataset",
    "_register_bounded": "probe.sdk.catalog.log_dataset",
    # probe.sdk.catalog.manifest
    "MAX_MANIFEST_FILES": "probe.sdk.catalog.manifest",
    "MAX_WALK_ENTRIES": "probe.sdk.catalog.manifest",
    "MANIFEST_FORMAT": "probe.sdk.catalog.manifest",
    "ManifestFile": "probe.sdk.catalog.manifest",
    "Manifest": "probe.sdk.catalog.manifest",
    "_identify": "probe.sdk.catalog.manifest",
    "_hash_cache": "probe.sdk.catalog.manifest",
    "build_manifest": "probe.sdk.catalog.manifest",
    "_walk_manifest": "probe.sdk.catalog.manifest",
    "_add": "probe.sdk.catalog.manifest",
    "_shown_relpath": "probe.sdk.catalog.manifest",
    "_settle": "probe.sdk.catalog.manifest",
    # probe.sdk.catalog.refs
    "SHARE_TOLERANCE": "probe.sdk.catalog.refs",
    "NAME_PATTERN": "probe.sdk.catalog.refs",
    "_UUID": "probe.sdk.catalog.refs",
    "CatalogRefused": "probe.sdk.catalog.refs",
    "SourceRef": "probe.sdk.catalog.refs",
    "DatasetRef": "probe.sdk.catalog.refs",
    "ref_of": "probe.sdk.catalog.refs",
    "_DATASET_LATEST": "probe.sdk.catalog.refs",
    "_CHECKPOINT_STEP": "probe.sdk.catalog.refs",
    "_CHECKPOINT_MOVING": "probe.sdk.catalog.refs",
    "is_moving_ref": "probe.sdk.catalog.refs",
    "moving_ref_refusal": "probe.sdk.catalog.refs",
    "check_share": "probe.sdk.catalog.refs",
    "mixture_parts": "probe.sdk.catalog.refs",
    "composition_parts": "probe.sdk.catalog.refs",
    "check_name": "probe.sdk.catalog.refs",
    # probe.sdk.catalog.server
    "UNREACHABLE_TTL_SECONDS": "probe.sdk.catalog.server",
    "STATED": "probe.sdk.catalog.server",
    "HOSTED_DATA_LIMIT": "probe.sdk.catalog.server",
    "_warned": "probe.sdk.catalog.server",
    "_warned_lock": "probe.sdk.catalog.server",
    "_warn_once": "probe.sdk.catalog.server",
    "_say": "probe.sdk.catalog.server",
    "FIXED_REF_FORMS": "probe.sdk.catalog.server",
    "old_server": "probe.sdk.catalog.server",
    "hosted_limit_message": "probe.sdk.catalog.server",
    "bytes_figure": "probe.sdk.catalog.server",
    "describe": "probe.sdk.catalog.server",
    "_warn_failure": "probe.sdk.catalog.server",
    "catalog_available": "probe.sdk.catalog.server",
    "_NOT_QUEUED": "probe.sdk.catalog.server",
    "could_succeed_later": "probe.sdk.catalog.server",
    "_may_have_landed": "probe.sdk.catalog.server",
    "warn_not_queued": "probe.sdk.catalog.server",
    "human_bytes": "probe.sdk.catalog.server",
    # probe.sdk.catalog.catalog
    "REQUEST_SECONDS": "probe.sdk.catalog.catalog",
    "OBSERVED": "probe.sdk.catalog.catalog",
    "_role": "probe.sdk.catalog.catalog",
    "_send": "probe.sdk.catalog.catalog",
    "_ambient": "probe.sdk.catalog.catalog",
    "_ambient_lock": "probe.sdk.catalog.catalog",
    "_client_for": "probe.sdk.catalog.catalog",
    "CREDENTIAL_PARAMS": "probe.sdk.catalog.catalog",
    "NAME_ONLY_USERINFO_SCHEMES": "probe.sdk.catalog.catalog",
    "credential_in_uri": "probe.sdk.catalog.catalog",
    "_refuse_credential": "probe.sdk.catalog.catalog",
    "source_body": "probe.sdk.catalog.catalog",
    "source": "probe.sdk.catalog.catalog",
    "use": "probe.sdk.catalog.catalog",
    "use_mixture": "probe.sdk.catalog.catalog",
}


def __getattr__(name: str):
    home = _HOMES.get(name)
    if home is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return getattr(importlib.import_module(home), name)


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(_HOMES))
