# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Durable, encrypted OAuth-state backend for the hosted Cloud MCP image.

The Cloud MCP Cloud Run image runs PyAirbyte's generic `airbyte-mcp-http`
entrypoint. On the interactive OIDC path, PyAirbyte's `OIDCProxy` holds OAuth
state (dynamic client registrations, upstream Keycloak refresh tokens, and JTI
mappings) in an in-process store by default, so that state is lost on every
restart and is not shared across replicas — each Cloud Run cold start, new
revision, or scale event would silently drop interactive users' sessions.

PyAirbyte stays backend-agnostic: it exposes a factory hook
(`AIRBYTE_MCP_OIDC_CLIENT_STORAGE_FACTORY="module:callable"`) and calls the named
callable with the OIDC client secret as `encryption_source_material`, expecting
an `AsyncKeyValue` store back. This module is that callable for the Cloud MCP
deployment: it lives here in the deployment repo (not in public PyAirbyte) and
builds a Fernet-encrypted Cloud Firestore store, mirroring the Ops MCP
`_oidc_storage.py` construction.

Firestore is reached over Google APIs with IAM auth (the Cloud Run runtime
service account via Application Default Credentials), so there is no password or
AUTH secret and no VPC to operate. `FirestoreStore` uses the key verbatim as the
document ID, which is invalid for OAuth keys that contain `/` or other reserved
characters, so keys are routed through `fastmcp_extensions.NormalizedKeysWrapper`
with the default `HashKeyNormalizer` (sha256 -> url-safe base64). Values are
encrypted at rest with `FernetEncryptionWrapper`, keyed off
`encryption_source_material` (the OIDC client secret this image already holds)
plus a fixed salt. The material is never logged.

Connection env (read at construction time):
    AIRBYTE_MCP_FIRESTORE_PROJECT: GCP project id. Optional; when unset it is
        inferred from Application Default Credentials / the runtime environment.
    AIRBYTE_MCP_FIRESTORE_DATABASE: Firestore database id. Optional; defaults to
        Firestore's `(default)` database.
"""

from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

from fastmcp_extensions import HashKeyNormalizer, NormalizedKeysWrapper
from key_value.aio.stores.firestore import FirestoreStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper

if TYPE_CHECKING:
    from key_value.aio.protocols.key_value import AsyncKeyValue

logger = logging.getLogger(__name__)

# Firestore connection settings, supplied by the deployment (Pulumi).
FIRESTORE_PROJECT_ENV = "AIRBYTE_MCP_FIRESTORE_PROJECT"
FIRESTORE_DATABASE_ENV = "AIRBYTE_MCP_FIRESTORE_DATABASE"

# Distinct keyspace + key-derivation namespace so Cloud MCP OAuth state never
# collides with Ops MCP state (which uses the `ops-mcp-oauth` collection/salt).
OAUTH_STATE_COLLECTION = "cloud-mcp-oauth"
ENCRYPTION_SALT = "cloud-mcp-oauth-storage"


def _env(name: str) -> str | None:
    """Return the stripped value of `name`, treating whitespace-only as unset."""
    return os.environ.get(name, "").strip() or None


def build_store(*, encryption_source_material: str) -> AsyncKeyValue:
    """Build the Fernet-encrypted Firestore OAuth-state store for Cloud MCP.

    Implements PyAirbyte's `AIRBYTE_MCP_OIDC_CLIENT_STORAGE_FACTORY` contract:
    invoked with the OIDC client secret as `encryption_source_material`, it
    returns an `AsyncKeyValue`. The secret is used only to derive the at-rest
    encryption key and is never logged.
    """
    if not encryption_source_material:
        raise ValueError(
            "Cloud MCP OIDC storage factory requires encryption source material "
            "(the OIDC client secret) to encrypt OAuth state at rest."
        )
    project = _env(FIRESTORE_PROJECT_ENV)
    database = _env(FIRESTORE_DATABASE_ENV)
    logger.info(
        "Cloud MCP OIDC OAuth-state storage: Firestore (project=%s, database=%s).",
        project or "<inferred>",
        database or "(default)",
    )
    store = FirestoreStore(
        project=project,
        database=database,
        default_collection=OAUTH_STATE_COLLECTION,
    )
    safe_store = NormalizedKeysWrapper(key_value=store, normalizer=HashKeyNormalizer())
    return FernetEncryptionWrapper(
        key_value=safe_store,
        source_material=encryption_source_material,
        salt=ENCRYPTION_SALT,
    )
