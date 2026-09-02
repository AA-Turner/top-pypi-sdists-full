"""Versioned CAPS constants for the checkpoint engine (S3 contract §1).

Every value here is a code constant, not an env var — changing one is a code push
and (for the format-bearing ones) a version bump. The single legitimate env var is
``CHECKPOINT_KMS_KEY_ENV`` below, whose *name* is a constant and whose *value* is
supplied per-environment (a value, never a toggle).
"""

from __future__ import annotations

from typing import Final

# ── Format / shape versions ──────────────────────────────────────────────
MANIFEST_VERSION: Final[int] = 1
ARCHIVE_FORMAT: Final[str] = "tar+zstd:v1"
PROFILE_FORMAT_VERSION: Final[int] = 1

# ── Bulk content cipher ──────────────────────────────────────────────────
CONTENT_CIPHER: Final[str] = "AES-256-GCM"
GCM_NONCE_BYTES: Final[int] = 12
GCM_TAG_BYTES: Final[int] = 16
DEK_BYTES: Final[int] = 32

# ── Key wrapping ─────────────────────────────────────────────────────────
KEY_VERSION: Final[str] = "1"  # a string: KMS encryption-context values are strings
ENCRYPTION_PURPOSE: Final[str] = "browser_profile_checkpoint"
WRAP_ALG_KMS: Final[str] = "kms-symmetric-gcm:v1"
WRAP_ALG_LOCAL_DEV: Final[str] = "local-dev-fernet:v1"
CHECKPOINT_KMS_KEY_ENV: Final[str] = "MATRX_BROWSER_PROFILE_KMS_KEY_ID"

# ── Archive codec ────────────────────────────────────────────────────────
ZSTD_LEVEL: Final[int] = 10  # OPEN(archive-codec) — pinned after WS-3 capacity report
ARCHIVE_CHUNK_BYTES: Final[int] = 8 * 1024 * 1024  # 8 MiB streaming chunk

# ── Closure proof ────────────────────────────────────────────────────────
CLOSE_GRACE_SECONDS: Final[int] = 15

# ── Fallback / retention ─────────────────────────────────────────────────
MAX_FALLBACK_CANDIDATES: Final[int] = 5
RETENTION_DAYS: Final[int] = 30  # D-20: 30-day checkpoint retention

# ── Supported sets (read-side validation) ────────────────────────────────
SUPPORTED_MANIFEST_VERSIONS: Final[frozenset[int]] = frozenset({1})
SUPPORTED_ARCHIVE_FORMATS: Final[frozenset[str]] = frozenset({ARCHIVE_FORMAT})

# ── Profile archive contents (part of PROFILE_FORMAT_VERSION) ─────────────
# Always excluded — large, regenerable, and carrying page content the audit
# policy never sanctioned. Prefix match against archive-root-relative paths.
ARCHIVE_EXCLUDE_PREFIXES: Final[tuple[str, ...]] = (
    "Crashpad/",
    "GrShaderCache/",
    "ShaderCache/",
    "GPUCache/",
    "Code Cache/",
    "Default/Code Cache/",
    "Default/GPUCache/",
    "Default/Service Worker/CacheStorage/",
    "Default/Service Worker/ScriptCache/",
    "component_crx_cache/",
    "Default/optimization_guide",
    "Default/Cache/",
)
# Exact singleton / lock names excluded regardless of location.
ARCHIVE_EXCLUDE_NAMES: Final[frozenset[str]] = frozenset(
    {"SingletonLock", "SingletonCookie", "SingletonSocket"}
)
# Suffixes excluded regardless of location.
ARCHIVE_EXCLUDE_SUFFIXES: Final[tuple[str, ...]] = (".lock",)

# Members whose presence a verification archive-probe (V4) asserts.
EXPECTED_ARCHIVE_MEMBERS: Final[tuple[str, ...]] = ("Default", "Local State")

# ── Cookie encryption scheme (D-5) ───────────────────────────────────────
# The observed Chromium cookie scheme, recorded in the manifest and refused on a
# cross-scheme restore. ``v10`` = basic store (published constant key, portable);
# ``v11`` = keyring key living OUTSIDE the profile dir (NOT portable).
COOKIE_SCHEME_BASIC: Final[str] = "v10"
COOKIE_SCHEME_KEYRING: Final[str] = "v11"
SUPPORTED_COOKIE_SCHEMES: Final[frozenset[str]] = frozenset(
    {COOKIE_SCHEME_BASIC, COOKIE_SCHEME_KEYRING}
)
