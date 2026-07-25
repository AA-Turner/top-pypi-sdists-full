# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for the interactive `OIDCProxy` OAuth-state storage resolver.

These cover what this module owns: the `AIRBYTE_MCP_OIDC_STORAGE` mode
selection, the guard rails that reject an unknown mode / missing encryption
material, and the Fernet-wrapped, key-normalized `FirestoreStore` returned in
`firestore` mode (including that the `AIRBYTE_MCP_FIRESTORE_*` settings reach the
client, and that the key-normalizing wrapper keeps illegal document IDs — URL
`client_id`s from the CIMD flow — from reaching Firestore).

`FirestoreStore` resolves Google credentials when it is constructed, so the
`_stub_adc` fixture points Application Default Credentials at anonymous
credentials — the client is built (no network call is made until a request) but
never needs real cloud credentials.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import google.auth
import pytest
from fastmcp_extensions import HashKeyNormalizer, NormalizedKeysWrapper
from google.auth.credentials import AnonymousCredentials
from key_value.aio.stores.firestore import FirestoreStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper

from airbyte_ops_mcp.mcp import _oidc_storage as storage

if TYPE_CHECKING:
    from collections.abc import Iterator

_SECRET = "test-oidc-client-secret"


@pytest.fixture(autouse=True)
def _stub_adc(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Point Application Default Credentials at anonymous credentials.

    Lets `FirestoreStore` construct its client without real GCP credentials; no
    network call happens until a request is issued, which these tests never do.
    """
    monkeypatch.setattr(
        google.auth,
        "default",
        lambda *args, **kwargs: (AnonymousCredentials(), "stub-project"),
    )
    yield


@pytest.mark.parametrize(
    "mode",
    [
        pytest.param(None, id="unset"),
        pytest.param("memory", id="memory"),
        pytest.param("MEMORY", id="uppercase"),
        pytest.param("  memory  ", id="whitespace_padded"),
    ],
)
def test_resolve_returns_none_for_memory_mode(mode: str | None) -> None:
    env = {} if mode is None else {storage.OIDC_STORAGE_ENV: mode}
    assert (
        storage.resolve_oidc_client_storage(encryption_source_material=_SECRET, env=env)
        is None
    )


def test_resolve_rejects_unknown_mode() -> None:
    with pytest.raises(ValueError, match="must be 'memory' or 'firestore'"):
        storage.resolve_oidc_client_storage(
            encryption_source_material=_SECRET,
            env={storage.OIDC_STORAGE_ENV: "redis"},
        )


def test_resolve_firestore_requires_encryption_material() -> None:
    with pytest.raises(ValueError, match="encryption source"):
        storage.resolve_oidc_client_storage(
            encryption_source_material="",
            env={storage.OIDC_STORAGE_ENV: "firestore"},
        )


def test_resolve_firestore_returns_fernet_wrapped_normalized_store() -> None:
    # The wrapper chain is `Fernet ← NormalizedKeys ← Firestore`: values are
    # encrypted at rest (outermost) and every key is normalized to a legal
    # document ID before it reaches Firestore (innermost).
    store = storage.resolve_oidc_client_storage(
        encryption_source_material=_SECRET,
        env={storage.OIDC_STORAGE_ENV: "firestore"},
    )
    assert isinstance(store, FernetEncryptionWrapper)
    normalized = store.key_value
    assert isinstance(normalized, NormalizedKeysWrapper)
    assert isinstance(normalized.normalizer, HashKeyNormalizer)
    assert isinstance(normalized.key_value, FirestoreStore)


@pytest.mark.parametrize(
    "raw_key",
    [
        pytest.param("https://goose-docs.ai/oauth/client-metadata.json", id="cimd_url"),
        pytest.param("a/b/c", id="slashes"),
        pytest.param("tok+en/with=std-base64", id="std_base64"),
    ],
)
def test_normalizer_yields_legal_firestore_ids(raw_key: str) -> None:
    # A URL `client_id` (Goose Desktop's CIMD flow) or a standard-base64 token
    # contains `/`, which is illegal in a Firestore document ID and crashes
    # `/authorize`. The normalizer must map any such key to a `/`-free id.
    store = storage.resolve_oidc_client_storage(
        encryption_source_material=_SECRET,
        env={storage.OIDC_STORAGE_ENV: "firestore"},
    )
    assert isinstance(store, FernetEncryptionWrapper)
    normalized = store.key_value
    assert isinstance(normalized, NormalizedKeysWrapper)
    document_id = normalized.normalizer.normalize(raw_key)
    assert "/" not in document_id
    assert document_id != raw_key


@pytest.mark.parametrize(
    "env,expected_database",
    [
        pytest.param(
            {storage.OIDC_STORAGE_ENV: "firestore"},
            None,
            id="default_database",
        ),
        pytest.param(
            {
                storage.OIDC_STORAGE_ENV: "firestore",
                storage.FIRESTORE_DATABASE_ENV: "ops-mcp-oauth",
            },
            "ops-mcp-oauth",
            id="explicit_database",
        ),
    ],
)
def test_resolve_firestore_passes_settings_to_client(
    env: dict[str, str], expected_database: str | None
) -> None:
    # Assert on the values the resolver forwards into the `FirestoreStore`
    # constructor (`project`/`database`) rather than the google client
    # internals. When `database` is unset the resolver forwards `None`, and
    # google-cloud-firestore applies its own `(default)` — that defaulting is
    # google's behavior, not what this resolver owns.
    env = {**env, storage.FIRESTORE_PROJECT_ENV: "my-project"}
    store = storage.resolve_oidc_client_storage(
        encryption_source_material=_SECRET, env=env
    )
    assert isinstance(store, FernetEncryptionWrapper)
    normalized = store.key_value
    assert isinstance(normalized, NormalizedKeysWrapper)
    inner = normalized.key_value
    assert isinstance(inner, FirestoreStore)
    assert inner._project == "my-project"
    assert inner._database == expected_database
    assert inner.default_collection == storage.OAUTH_STATE_COLLECTION
