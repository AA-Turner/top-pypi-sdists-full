from dataclasses import FrozenInstanceError, fields
from typing import Any, cast

import pytest

from agentic_devtools.cli.ci.canonical_dispatch_identity import CanonicalDispatchIdentity

HEAD_SHA = "a" * 40
WORK_DIGEST = "b" * 64


def _identity(**overrides: object) -> CanonicalDispatchIdentity:
    values: dict[str, object] = {
        "repo": "owner/name",
        "pull_request_id": 12,
        "head_sha": HEAD_SHA,
        "review_id": 0,
        "work_digest": WORK_DIGEST,
        "ordinal": 4,
    }
    values.update(overrides)
    return CanonicalDispatchIdentity(
        repo=cast(Any, values["repo"]),
        pull_request_id=cast(Any, values["pull_request_id"]),
        head_sha=cast(Any, values["head_sha"]),
        review_id=cast(Any, values["review_id"]),
        work_digest=cast(Any, values["work_digest"]),
        ordinal=cast(Any, values["ordinal"]),
    )


def test_has_exact_six_fields_in_canonical_order() -> None:
    assert [field.name for field in fields(CanonicalDispatchIdentity)] == [
        "repo",
        "pull_request_id",
        "head_sha",
        "review_id",
        "work_digest",
        "ordinal",
    ]


@pytest.mark.parametrize(
    "repo",
    [
        None,
        "owner",
        "owner/name/extra",
        "/name",
        "owner/",
        "Owner/name",
        "owner/Name",
        " owner/name",
        "owner/name ",
        "owner/name with space",
        "owner/name$",
        "owner/é",
        "./name",
        "../name",
        "owner/.",
        "owner/..",
    ],
)
def test_rejects_noncanonical_repositories(repo: object) -> None:
    with pytest.raises(ValueError, match="repo"):
        _identity(repo=repo)


@pytest.mark.parametrize("pull_request_id", [True, False, "12", 0, -1])
def test_rejects_invalid_pull_request_ids(pull_request_id: object) -> None:
    with pytest.raises(ValueError, match="pull_request_id"):
        _identity(pull_request_id=pull_request_id)


@pytest.mark.parametrize("review_id", [True, False, "0", -1])
def test_rejects_invalid_review_ids(review_id: object) -> None:
    with pytest.raises(ValueError, match="review_id"):
        _identity(review_id=review_id)


@pytest.mark.parametrize("ordinal", [True, False, "4", 0, -1])
def test_rejects_invalid_ordinals(ordinal: object) -> None:
    with pytest.raises(ValueError, match="ordinal"):
        _identity(ordinal=ordinal)


@pytest.mark.parametrize(
    "head_sha",
    [None, "A" * 40, "a" * 39, "a" * 41, "g" * 40],
)
def test_rejects_invalid_head_shas(head_sha: object) -> None:
    with pytest.raises(ValueError, match="head_sha"):
        _identity(head_sha=head_sha)


@pytest.mark.parametrize(
    "work_digest",
    [None, "B" * 64, "b" * 63, "b" * 65, "g" * 64],
)
def test_rejects_invalid_work_digests(work_digest: object) -> None:
    with pytest.raises(ValueError, match="work_digest"):
        _identity(work_digest=work_digest)


def test_accepts_canonical_values_and_formats_key() -> None:
    identity = _identity(repo="owner_1/name.repo-2", pull_request_id=12, review_id=0, ordinal=10)

    assert identity.key == f"owner_1/name.repo-2:12:{HEAD_SHA}:0:{WORK_DIGEST}:10"
    assert identity.retry_key == (
        "owner_1/name.repo-2",
        12,
        HEAD_SHA,
        0,
        WORK_DIGEST,
    )


def test_accepts_positive_review_id() -> None:
    assert _identity(review_id=23).review_id == 23


def test_retry_key_omits_ordinal_but_full_equality_includes_it() -> None:
    first = _identity(ordinal=4)
    retry = _identity(ordinal=5)

    assert first.retry_key == retry.retry_key
    assert first != retry
    assert first == _identity()


@pytest.mark.parametrize(
    "change",
    [
        {"repo": "other/name"},
        {"pull_request_id": 13},
        {"head_sha": "c" * 40},
        {"review_id": 1},
        {"work_digest": "d" * 64},
    ],
)
def test_retry_key_differs_when_a_nonordinal_field_changes(change: dict[str, object]) -> None:
    assert _identity().retry_key != _identity(**change).retry_key


def test_identity_is_frozen() -> None:
    identity = _identity()

    with pytest.raises(FrozenInstanceError):
        identity.ordinal = 5  # type: ignore[misc]
