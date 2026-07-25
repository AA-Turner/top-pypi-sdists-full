# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Durable, encrypted backend for the interactive `OIDCProxy`'s OAuth state.

The interactive login path (`OIDCProxy`, active once the OIDC client credentials
are supplied) holds the upstream Keycloak refresh tokens, JTI mappings, and the
dynamic client registrations of MCP clients. `OIDCProxy` defaults to an
in-process store, so all of that state is lost on restart and is not shared
across replicas — every Cloud Run cold start, new revision, or scale event would
silently drop every interactive user's session and force a fresh browser login.

This module resolves an optional durable, shared, encrypted store from env so
that state survives restarts and spans replicas. It builds a
`key_value.aio.stores.firestore.FirestoreStore` (Cloud Firestore in Native mode)
wrapped in a `key_value.aio.wrappers.encryption.FernetEncryptionWrapper` so
tokens are encrypted at rest. Firestore is a serverless, fully-managed key-value
store reached over Google APIs with IAM auth — the Cloud Run runtime service
account authenticates via Application Default Credentials, so there is no
password/AUTH secret and no VPC to operate. The generic `fastmcp_extensions`
library stays backend-agnostic — it accepts the constructed store via
`OIDCAuthConfig(..., client_storage=...)`; this module owns the Airbyte-specific
env wiring and the Firestore/Fernet construction.

`FirestoreStore` uses the key verbatim as the document ID, which fails for keys
containing `/` (a URL `client_id` from the CIMD flow, or a standard-base64
token) — the store raises `InvalidArgument: ... lacks a collection id` before
any OAuth logic runs. To make any string key storable, the store is wrapped in
`fastmcp_extensions.NormalizedKeysWrapper` with the default
`HashKeyNormalizer` (sha256 → url-safe base64, `k-` prefix): every key becomes a
fixed-length, always-legal document ID. The wrapper is applied innermost
(`Firestore ← NormalizedKeys ← Fernet`), so values stay encrypted at rest and
only the document-id keyspace changes.

Selection is controlled by `AIRBYTE_MCP_OIDC_STORAGE`:
- `memory` (default): return `None` so `OIDCProxy` keeps its in-process store.
  Fine for stdio and single-instance local dev.
- `firestore`: construct the Fernet-wrapped Firestore store from the
  `AIRBYTE_MCP_FIRESTORE_*` settings below.

Firestore connection env (only read when `AIRBYTE_MCP_OIDC_STORAGE=firestore`):
    AIRBYTE_MCP_FIRESTORE_PROJECT: GCP project id. Optional; when unset it is
        inferred from Application Default Credentials / the runtime environment.
    AIRBYTE_MCP_FIRESTORE_DATABASE: Firestore database id. Optional; defaults to
        Firestore's `(default)` database.

The Fernet encryption key is derived from `encryption_source_material` (the fixed
OIDC client secret this server already holds) plus a fixed salt, so no separate
encryption secret needs to be provisioned. The material is never logged.
"""

from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

from fastmcp_extensions import HashKeyNormalizer, NormalizedKeysWrapper
from key_value.aio.stores.firestore import FirestoreStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper

if TYPE_CHECKING:
    from collections.abc import Mapping

    from key_value.aio.protocols.key_value import AsyncKeyValue

logger = logging.getLogger(__name__)

# Selects the OAuth-state backend for the interactive `OIDCProxy`.
OIDC_STORAGE_ENV = "AIRBYTE_MCP_OIDC_STORAGE"
STORAGE_MEMORY = "memory"
STORAGE_FIRESTORE = "firestore"

# Firestore connection settings, read only when `OIDC_STORAGE_ENV == "firestore"`.
FIRESTORE_PROJECT_ENV = "AIRBYTE_MCP_FIRESTORE_PROJECT"
FIRESTORE_DATABASE_ENV = "AIRBYTE_MCP_FIRESTORE_DATABASE"

# Namespacing for the OAuth-state keys and the encryption key derivation. Kept
# stable so restarts and replicas resolve the same keyspace and can decrypt
# previously written entries.
OAUTH_STATE_COLLECTION = "ops-mcp-oauth"
ENCRYPTION_SALT = "ops-mcp-oauth-storage"


def _get(env: Mapping[str, str], name: str) -> str:
    """Return the stripped value of `name`, treating whitespace-only as unset."""
    return env.get(name, "").strip()


def resolve_oidc_client_storage(
    *,
    encryption_source_material: str,
    env: Mapping[str, str] | None = None,
) -> AsyncKeyValue | None:
    """Resolve the durable OAuth-state store for `OIDCProxy`, or `None`.

    Returns `None` when `AIRBYTE_MCP_OIDC_STORAGE` is unset or `memory`, so
    `OIDCProxy` keeps its default in-process store. When `firestore`, returns a
    `FernetEncryptionWrapper`-wrapped `FirestoreStore` built from the
    `AIRBYTE_MCP_FIRESTORE_*` settings, with the encryption key derived from
    `encryption_source_material` (never logged). The store authenticates to
    Firestore with Application Default Credentials (the runtime service account),
    so no password or key material is passed or stored.

    Callers pass the store to `fastmcp_extensions.OIDCAuthConfig`'s
    `client_storage` argument, keeping that library backend-agnostic.
    """
    source = env if env is not None else os.environ
    mode = (_get(source, OIDC_STORAGE_ENV) or STORAGE_MEMORY).lower()

    if mode == STORAGE_MEMORY:
        logger.info(
            "Using in-memory OIDC OAuth-state storage; interactive sessions will "
            "not survive restarts or span replicas (set %s=%s for durability).",
            OIDC_STORAGE_ENV,
            STORAGE_FIRESTORE,
        )
        return None

    if mode != STORAGE_FIRESTORE:
        raise ValueError(
            f"{OIDC_STORAGE_ENV} must be '{STORAGE_MEMORY}' or '{STORAGE_FIRESTORE}', "
            f"got '{mode}'."
        )

    if not encryption_source_material:
        raise ValueError(
            f"{OIDC_STORAGE_ENV}={STORAGE_FIRESTORE} requires encryption source "
            "material (the OIDC client secret) to encrypt tokens at rest."
        )

    project = _get(source, FIRESTORE_PROJECT_ENV) or None
    database = _get(source, FIRESTORE_DATABASE_ENV) or None
    logger.info(
        "Using Firestore for OIDC OAuth-state storage (project=%s, database=%s).",
        project or "<inferred>",
        database or "(default)",
    )
    store = FirestoreStore(
        project=project,
        database=database,
        default_collection=OAUTH_STATE_COLLECTION,
    )
    # Normalize keys into legal, fixed-length Firestore document IDs before they
    # reach the store. `OIDCProxy` keys its client store by `client_id`, which
    # for the CIMD flow (e.g. Goose Desktop) is a URL whose `/` chars are illegal
    # in a Firestore document ID and otherwise crash `/authorize`.
    safe_store = NormalizedKeysWrapper(key_value=store, normalizer=HashKeyNormalizer())
    return FernetEncryptionWrapper(
        key_value=safe_store,
        source_material=encryption_source_material,
        salt=ENCRYPTION_SALT,
    )
