"""data catalog reads: dataset/checkpoint/source listings and entries, ref checks."""

from __future__ import annotations
import re
import uuid
from typing import Any
from urllib.parse import quote

from ...sdk import errors
from ...shared.reads.search_contract import EnvelopeState, EntityType

#: The data catalog's ref kinds, each read through its own `/v1` route. The
#: server resolves every ref form (`app/catalog/refs.py`); the MCP sends the
#: ref it was given, prefix kept. Only a dataset ref is checked here first (see
#: `dataset_ref_problem`).
_CATALOG_DETAIL_ROUTES: dict[str, str] = {
    EntityType.DATASET.value: "/v1/catalog/datasets",
    EntityType.SOURCE.value: "/v1/sources",
    EntityType.CHECKPOINT.value: "/v1/catalog/checkpoints",
}

#: Set on a dataset entity whose ref named a version that does not exist: the
#: route's 404 `{message, state: "no_match", versions}`, kept as the ANSWER
#: (the dataset exists, that version does not) rather than raised as absence,
#: which reads as licence to register a new name.
CATALOG_NO_MATCH = "_no_match"

#: Not a `Capability` member: that enum is the verbose envelope's static map,
#: and every member must be reported there. This names the refusal only.
_CATALOG_CAPABILITY = "data_catalog"

#: The server's own name for the catalog in `GET /v1/server/features`
#: (`app/client_version/router.py`); the SDK gates its catalog verbs on it too.
CATALOG_FEATURE = "catalog"

# The `dataset:` grammar, mirrored from app/catalog/dataset_refs.py: an entry id
# (anything `uuid.UUID` parses, tried first, as the server does) or a name
# (lower-case letters, digits, `.`, `_`, `-`), then optionally `@<N>`, `@v<N>`
# or `@latest`.
_DATASET_NAME = re.compile(r"^[a-z0-9][a-z0-9._-]{0,127}$")
_DATASET_VERSION = re.compile(r"^v?[0-9]{1,9}$")
_DATASET_LATEST = "latest"


def dataset_ref_problem(value: str) -> str | None:
    """Why `dataset:<value>` is not a dataset ref, or None when it is one.

    Checked BEFORE any request, because the route cannot say it: its `{ref}`
    is one path segment, so a name with a `/` (`allenai/c4`, a Hub id) never
    reaches the dataset resolver and comes back as FastAPI's bare 404 -- which
    reads as "no such dataset", licence to register one."""
    key, at, selector = value.strip().partition("@")
    key = key.strip()
    if at and selector.strip().lower() != _DATASET_LATEST and not _DATASET_VERSION.fullmatch(
        selector.strip()
    ):
        return f"unknown dataset version {selector!r}: use @<N>, @v<N> or @latest"
    try:
        uuid.UUID(key)
        return None
    except ValueError:
        pass
    if not _DATASET_NAME.fullmatch(key):
        hint = (
            " An external dataset (a Hub id, a bucket, a URL) is a `source:` ref."
            if "/" in key
            else ""
        )
        return (
            f"{key!r} is not a dataset name: a dataset name is lower-case letters, "
            "digits, `.`, `_` and `-`, starting with a letter or digit, at most 128 "
            f"characters (or the dataset's id).{hint}"
        )
    return None


def catalog_path_ref(ref: str) -> str:
    """A catalog ref as ONE path segment: `:` and `@` stay readable, anything
    else (a `/` in a source's canonical key) is percent-encoded. The SDK's
    `catalog_path_ref` encodes the same way, so both clients reach one route."""
    return quote(str(ref).strip(), safe=":@")


class CatalogReadsMixin:
    """Part of ResearchOSSource: its methods run with `self` the ResearchOSSource; compose() folds them into ResearchOSSource."""

    # -- the data catalog (C4): datasets, checkpoints, sources ----------------

    def _catalog_get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        """One catalog read. A 404 from a server that does not declare
        `catalog` in `GET /v1/server/features` is refused as that: passed on,
        it reads as "no such dataset", which is licence to register a
        duplicate. From a server that does, a 404 is the answer and passes.

        Decided by the declaration, not by the 404's text: FastAPI's bare
        "Not Found" also answers a catalog server's route that a ref did not
        match. Asked only on a 404, and once per source (`supports_feature`
        caches it on this token's client)."""
        try:
            return self.client.transport.get(path, params=params)
        except errors.NotFoundError:
            if not self.client.supports_feature(CATALOG_FEATURE):
                raise errors.CapabilityUnavailable(
                    _CATALOG_CAPABILITY,
                    f"this Probe Research server does not serve GET {path} yet "
                    "(it predates the data catalog); nothing was looked up",
                ) from None
            raise

    def catalog_list(
        self, listing: str, *, cursor: str | None, limit: int, **filters: Any
    ) -> dict:
        """``GET /v1/catalog/{datasets|checkpoints|sources}``: one keyset page,
        `{items, next_cursor}` (checkpoints add `totals`). A filter left None is
        not sent; a boolean goes as `true`."""
        parameters: dict[str, Any] = {"limit": limit}
        if cursor:
            parameters["cursor"] = cursor
        for name, value in filters.items():
            if value is None:
                continue
            parameters[name] = str(value).lower() if isinstance(value, bool) else value
        return self._catalog_get(f"/v1/catalog/{listing}", parameters) or {}

    def catalog_entity(self, kind: str, ref: str) -> dict:
        """One dataset (entry and every version, newest first), source or
        checkpoint by any ref form its server resolves. A dataset version that
        does not exist answers `CATALOG_NO_MATCH` with the versions that do."""
        try:
            return self._catalog_get(f"{_CATALOG_DETAIL_ROUTES[kind]}/{catalog_path_ref(ref)}")
        except errors.NotFoundError as exc:
            detail = exc.detail
            if (
                kind == EntityType.DATASET.value
                and isinstance(detail, dict)
                and detail.get("state") == EnvelopeState.NO_MATCH
            ):
                return {
                    "ref": ref,
                    CATALOG_NO_MATCH: {
                        "message": detail.get("message"),
                        "versions": [v for v in detail.get("versions") or [] if isinstance(v, int)],
                    },
                }
            raise
