"""
Two-layer client for pulling models from the Anaconda AI catalog via OBP.

Layer 1 — AnacondaModelClient: talks to the OBP catalog proxy. No disk I/O.
Layer 2 — AnacondaModel: one model on disk. Owns its file(s) and lifecycle.

Everything — single-file gguf quants and multi-file safetensor collections —
comes through the same ``.model()`` API; filters pick what lands on disk.

Usage:
    client = AnacondaModelClient()
    model = client.model("Qwen/Qwen2.5-0.5B",
                         filename="Qwen_Qwen2.5-0.5B-q4_k_m.gguf",
                         root_dir="/tmp/models")
    model.pull()
    print(model.path)   # /tmp/models/Qwen2.5-0.5B/Qwen_Qwen2.5-0.5B-q4_k_m.gguf

    model = client.model("Qwen/Qwen2.5-0.5B", format="safetensors",
                         root_dir="/tmp/models")
    model.pull()
    print(model.path)   # /tmp/models/Qwen2.5-0.5B/  (HuggingFace-layout dir)
    model.delete()
"""

import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import time

import requests

from .exceptions import ModelAccessDenied

CHUNK_SIZE = 8 * 1024 * 1024  # 8 MB
MAX_STREAM_RETRIES = 5  # retries after interruptions without new progress
# Transient client errors that a retry with a fresh signed URL can fix.
RETRYABLE_4XX = frozenset({408, 425, 429})
RETRY_BACKOFF_BASE = 2.0  # seconds; doubles per consecutive retryable error
RETRY_BACKOFF_CAP = 32.0  # upper bound for any single backoff sleep


def _log(source, msg):
    """Write a prefixed log line to stderr."""
    sys.stderr.write("[%s] %s\n" % (source, msg))
    sys.stderr.flush()


def _retry_after_seconds(response, cap):
    """
    Extract a bounded retry delay from a ``Retry-After`` header.

    Supports both the delay-seconds and HTTP-date forms. Returns ``None``
    when the header is absent or unparseable, otherwise a non-negative
    number of seconds capped at ``cap``.
    """
    value = response.headers.get("retry-after") if response is not None else None
    if not value:
        return None
    try:
        delay = float(value)
    except ValueError:
        from datetime import datetime, timezone
        from email.utils import parsedate_to_datetime

        try:
            then = parsedate_to_datetime(value)
            delay = (then - datetime.now(timezone.utc)).total_seconds()
        except (TypeError, ValueError, OverflowError):
            return None
    if delay <= 0:
        return None
    return min(delay, cap)


# ======================================================================
# Layer 1 — Catalog client (API only, no disk I/O)
# ======================================================================


class AnacondaModelClient:
    """
    Talks to the Anaconda AI model catalog via the OBP platform.

    Browse/detail calls go to the OBP API server (utqiagvik).
    Download calls go directly to keywest (the programmatic runtime service).

    Reads configuration from environment variables:
        - OBP_API_SERVER: the API server hostname (e.g. "api.my-cluster.obp.outerbounds.com")
        - OBP_INTEGRATIONS_URL: keywest integrations endpoint (e.g. "https://host/integrations")
        - OBP_PERIMETER: the perimeter name
        - METAFLOW_SERVICE_HEADERS: JSON dict of auth headers (contains x-api-key)
    """

    def _resolve_from_conf_or_env(self, key):
        from metaflow_extensions.outerbounds.remote_config import init_config

        conf = init_config()
        if key in conf:
            return conf[key]
        return os.environ.get(key, "")

    def __init__(self):
        self._api_server = self._resolve_from_conf_or_env("OBP_API_SERVER")
        self._integrations_url = self._resolve_from_conf_or_env(
            "OBP_INTEGRATIONS_URL",
        )
        self._perimeter = self._resolve_from_conf_or_env("OBP_PERIMETER")
        headers_json = self._resolve_from_conf_or_env("METAFLOW_SERVICE_HEADERS")
        key_val = self._resolve_from_conf_or_env("METAFLOW_SERVICE_AUTH_KEY")

        if not self._api_server:
            if self._integrations_url.endswith("/integrations"):
                self._api_server = self._integrations_url[: -len("/integrations")]
            else:
                raise RuntimeError(
                    "@anaconda_models: OBP_API_SERVER not found in environment. "
                    "This decorator requires an OBP platform environment."
                )
        if not self._integrations_url:
            # Derive integrations URL from API server if not explicitly set
            server = self._api_server
            if not server.startswith("https://") and not server.startswith("http://"):
                server = "https://%s" % server
            self._integrations_url = "%s/integrations" % server.rstrip("/")

        if not self._perimeter:
            raise RuntimeError(
                "@anaconda_models: OBP_PERIMETER not found in environment."
            )

        if not headers_json:
            if not key_val:
                raise RuntimeError(
                    "@anaconda_models: METAFLOW_SERVICE_HEADERS not found in environment."
                )
            headers_json = json.dumps({"x-api-key": key_val})
        self._session = requests.Session()
        self._session.headers.update(json.loads(headers_json))

    @property
    def _base_url(self):
        server = self._api_server
        if server.startswith("https://") or server.startswith("http://"):
            return "%s/v1/perimeters/%s/catalog" % (server.rstrip("/"), self._perimeter)
        return "https://%s/v1/perimeters/%s/catalog" % (server, self._perimeter)

    def list_models(self, limit=20, **filters):
        """
        List models from the catalog.

        Parameters
        ----------
        limit : int
            Max models to return.
        **filters
            Query params: name, search, source_name, model_type, quant_method, etc.

        Returns
        -------
        list[dict]
        """
        params = {"limit": limit}
        params.update(filters)
        return self._get("/models", params=params)["result"]["data"] or []

    def get_model(self, model_name):
        """
        Look up a single model by name.

        Raises
        ------
        LookupError
            If the model is not found.
        """
        models = self.list_models(name=model_name, limit=5) or []
        if models:
            if len(models) == 1:
                return models[0]
            raise LookupError(
                f"Found multiple matches for {model_name}: {[_hfname(m) for m in models]}"
            )
        else:
            # Lookup potential name matches
            possible_matches = self.list_models(search=model_name, limit=5)
            if possible_matches:
                raise LookupError(
                    f"Model {model_name} not found. Closest matches: {[_hfname(m) for m in possible_matches]}"
                )
            raise LookupError(f"Model {model_name} not found.")

    def resolve(self, model_name, **filters):
        """
        Resolve a model and pick the smallest published file matching `filters`.

        A filter is just a field on a catalog file dict that must equal the
        given value; all filters must match. With no filters, every single
        file is a candidate (collections are only picked when a filter
        selects them). Among the matches, the smallest published file wins
        (falling back to the smallest overall if none are published).

        Both single files (gguf quants) and multi-file safetensor collections
        live in the same ``quantized_files[]`` array, so the same filters
        reach both — e.g. ``format="safetensors"`` resolves the collection.

        Parameters
        ----------
        model_name : str
            Exact name in the catalog.
        **filters
            Field constraints on the file, e.g. ``quant_method="q4_k_m"``,
            ``format="gguf"``, ``format="safetensors"``. Omit for the smallest published
            single file. One filter is special: ``collection_uuid`` bypasses
            the catalog file listing entirely and resolves the collection
            straight from its manifest (workaround for catalog data gaps).

        Returns
        -------
        (dict, dict)
            ``(model_dict, file_dict)``.

        Raises
        ------
        LookupError
            If the model has no files, or none match `filters`.

        Examples
        --------
        >>> client.resolve("Qwen2.5-0.5B")                       # smallest
        >>> client.resolve("Qwen2.5-0.5B", quant_method="q4_k_m")
        >>> client.resolve("Qwen2.5-0.5B", format="safetensors")
        """
        collection_uuid = filters.pop("collection_uuid", None)

        model = self.get_model(model_name)
        model_uuid = model.get("model_uuid")

        if collection_uuid:
            _log(
                "client",
                "Using explicit collection_uuid=%r for model %r "
                "(bypassing quantized_files — catalog data issue workaround)."
                % (collection_uuid, model_name),
            )
            manifest = self.get_collection_manifest(
                model_uuid, collection_uuid, model_name=model_name
            )
            return model, self._collection_dict_from_manifest(manifest, model_uuid)

        files = model.get("quantized_files", [])
        matches = [f for f in files if all(f.get(k) == v for k, v in filters.items())]
        if not filters:
            # No filters: only single files are candidates, preserving the
            # "smallest published file" default.
            matches = [f for f in matches if not f.get("is_collection")]
        if not matches:
            # The catalog sometimes doesn't surface safetensor collections in
            # quantized_files[]. If the filters were asking for one, probe the
            # manifest endpoint before giving up.
            if filters.get("format") == "safetensors" or filters.get("is_collection"):
                _log(
                    "client",
                    "Model %r has no safetensor collection in quantized_files "
                    "(quantized_files count: %d). Probing v1 manifest endpoint "
                    "as fallback (catalog data issue)." % (model_name, len(files)),
                )
                manifest = self._probe_collection_manifest(
                    model_uuid, model_name=model_name
                )
                if manifest is not None:
                    collection_dict = self._collection_dict_from_manifest(
                        manifest, model_uuid
                    )
                    _log(
                        "client",
                        "Fallback resolved collection %r (%d files, %d MB) "
                        "via manifest endpoint."
                        % (
                            collection_dict["file_uuid"],
                            collection_dict["file_count"] or 0,
                            (collection_dict["total_size_bytes"] or 0) >> 20,
                        ),
                    )
                    return model, collection_dict
            raise LookupError(
                "No file for %r matches %s. Available: %s"
                % (
                    model_name,
                    filters or "(any)",
                    [
                        {
                            "format": f.get("format"),
                            "quant_method": f.get("quant_method"),
                            "filename": f.get("filename"),
                            "collection_type": f.get("collection_type"),
                            "is_collection": f.get("is_collection", False),
                        }
                        for f in files
                    ],
                )
            )
        published = [f for f in matches if f.get("published")] or matches
        return model, min(
            published,
            key=lambda f: f.get("size_bytes")
            or f.get("total_size_bytes")
            or float("inf"),
        )

    def get_download_url(self, model_uuid, file_uuid, model_name=None):
        """
        Get a signed download URL for a file via keywest (programmatic runtime).

        Parameters
        ----------
        model_uuid : str
            The model's UUID.
        file_uuid : str
            UUID of the specific file within the model.
        model_name : str, optional
            The model name. Required by the server for access control validation.

        Returns
        -------
        str
            The pre-signed R2 download URL.
        """
        url = "%s/model-catalog/download" % self._integrations_url.rstrip("/")
        r = self._session.post(
            url,
            json={
                "perimeter_name": self._perimeter,
                "model_name": model_name or "",
                "model_uuid": model_uuid,
                "file_uuid": file_uuid,
            },
            timeout=30,
        )
        if r.status_code == 403:
            body = (
                r.json()
                if r.headers.get("content-type", "").startswith("application/json")
                else {}
            )
            model_name_parsed, reason = self._parse_403(body)
            raise ModelAccessDenied(model_name=model_name_parsed, reason=reason)
        r.raise_for_status()
        return r.json()["download_url"]

    def get_test_scores(self, model_uuid, file_uuid):
        """
        Fetch evaluation test scores for a specific quantized file.

        Returns
        -------
        list[dict]
            Each dict has test_name, test_value (0-100), quant, etc.
            Returns [] on any error.
        """
        try:
            path = "/models/%s/test-scores" % model_uuid
            data = self._get(path)
            return data.get("data", [])
        except Exception as e:
            _log("client", "test-scores fetch failed (non-fatal): %s" % e)
            return []

    def model(self, model_name, root_dir=None, **filters):
        """
        Create an AnacondaModel — a handle to one model on disk. This is
        the single entry point for everything in the catalog: gguf quants,
        safetensor collections, etc. Filters pick what lands on disk.

        Resolves catalog metadata immediately. Does not download yet.

        Parameters
        ----------
        model_name : str
            Huggingface-style model name in the catalog (e.g. meta-llama/Llama-3.2-1B-Instruct).
        root_dir : str, optional
            Root directory for the download.  A subdirectory per model
            is created underneath.  Defaults to a new temp directory.
        **filters
            Field constraints used to pick the file, e.g.
            ``quant_method="q4_k_m"``, ``format="gguf"`` or
            ``format="safetensors"`` (resolves the multi-file collection).
            See :meth:`resolve`. If omitted, the smallest published single
            file is chosen.

        Returns
        -------
        AnacondaModel
        """
        model_dict, model_reconstruction_dict = self.resolve(model_name, **filters)
        return AnacondaModel(
            self, model_dict, model_reconstruction_dict, root_dir=root_dir
        )

    # ------------------------------------------------------------------
    # Safetensor collection plumbing (used by resolve() and pull())
    # ------------------------------------------------------------------

    def _collection_dict_from_manifest(self, manifest, model_uuid):
        """Shape a manifest response into a collection_dict."""
        return {
            "file_uuid": manifest.get("file_uuid"),
            "model_uuid": manifest.get("model_uuid") or model_uuid,
            "format": manifest.get("format", "safetensors"),
            "collection_type": manifest.get("collection_type", "original"),
            "file_count": manifest.get("file_count"),
            "total_size_bytes": manifest.get("total_size_bytes"),
            "is_collection": True,
            "published": True,
        }

    def _probe_collection_manifest(self, model_uuid, model_name=None):
        """Try candidate UUIDs until one returns a non-empty manifest, or None."""
        for coll_uuid in self._candidate_collection_uuids(model_uuid):
            try:
                manifest = self.get_collection_manifest(
                    model_uuid, coll_uuid, model_name=model_name
                )
                if manifest.get("files"):
                    return manifest
            except ModelAccessDenied:
                raise
            except Exception as e:
                _log(
                    "client",
                    "Manifest probe for collection %s failed (non-fatal): %s"
                    % (coll_uuid, e),
                )
                continue
        return None

    def _candidate_collection_uuids(self, model_uuid):
        """Yield collection UUIDs to probe. Tries /files endpoint first, then model_uuid itself."""
        seen = set()
        try:
            data = self._get("/models/%s/files" % model_uuid)
            for entry in data.get("data", {}).get("collections", []):
                uid = entry.get("file_uuid") or entry.get("uuid")
                if uid and uid not in seen:
                    seen.add(uid)
                    yield uid
        except ModelAccessDenied:
            raise
        except Exception as e:
            _log(
                "client",
                "Listing collection candidates for %s failed (non-fatal): %s"
                % (model_uuid, e),
            )
        if model_uuid and model_uuid not in seen:
            seen.add(model_uuid)
            yield model_uuid

    def get_collection_manifest(self, model_uuid, collection_uuid, model_name=None):
        """
        Fetch a collection's download manifest via keywest.

        Parameters
        ----------
        model_uuid : str
            The model's UUID.
        collection_uuid : str
            The collection's UUID.
        model_name : str, optional
            The model name (used for server-side access control validation).

        Returns
        -------
        dict
            Manifest with file_count, total_size_bytes, and files[].
        """
        url = "%s/model-catalog/collection-download" % self._integrations_url.rstrip(
            "/"
        )
        r = self._session.post(
            url,
            json={
                "perimeter_name": self._perimeter,
                "model_name": model_name or "",
                "model_uuid": model_uuid,
                "collection_uuid": collection_uuid,
            },
            timeout=30,
        )
        if r.status_code == 403:
            body = (
                r.json()
                if r.headers.get("content-type", "").startswith("application/json")
                else {}
            )
            model_name_parsed, reason = self._parse_403(body)
            raise ModelAccessDenied(model_name=model_name_parsed, reason=reason)
        r.raise_for_status()
        return r.json()

    def get_collection_file_url(
        self, model_uuid, collection_uuid, filename, model_name=None
    ):
        """
        Get a signed download URL for a single file within a collection via keywest.

        Parameters
        ----------
        model_uuid : str
            The model's UUID.
        collection_uuid : str
            The collection's UUID.
        filename : str
            The filename within the collection.
        model_name : str, optional
            The model name (used for server-side access control validation).

        Returns
        -------
        str
            The pre-authenticated signed download URL.
        """
        _validate_manifest_filename(filename)
        url = "%s/model-catalog/collection-file" % self._integrations_url.rstrip("/")
        r = self._session.post(
            url,
            json={
                "perimeter_name": self._perimeter,
                "model_name": model_name or "",
                "model_uuid": model_uuid,
                "collection_uuid": collection_uuid,
                "filename": filename,
            },
            timeout=30,
        )
        if r.status_code == 403:
            body = (
                r.json()
                if r.headers.get("content-type", "").startswith("application/json")
                else {}
            )
            model_name_parsed, reason = self._parse_403(body)
            raise ModelAccessDenied(model_name=model_name_parsed, reason=reason)
        r.raise_for_status()
        return r.json()["download_url"]

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_403(body):
        """Extract model_name and reason from a 403 response body."""
        error_msg = body.get("error", "Access denied by policy")
        model_name = body.get("model_name", "")
        if not model_name:
            match = re.search(r"Model '([^']+)'", error_msg)
            model_name = match.group(1) if match else "unknown"
        return model_name, error_msg

    def _get(self, path, params=None, api_version=None):
        headers = {"X-Anaconda-Api-Version": api_version} if api_version else None
        r = self._session.get(
            self._base_url + path, params=params, headers=headers, timeout=30
        )
        if r.status_code == 403:
            body = (
                r.json()
                if r.headers.get("content-type", "").startswith("application/json")
                else {}
            )
            model_name, reason = self._parse_403(body)
            raise ModelAccessDenied(model_name=model_name, reason=reason)
        r.raise_for_status()
        return r.json()

    def _post(self, path, json_body=None):
        r = self._session.post(self._base_url + path, json=json_body, timeout=30)
        if r.status_code == 403:
            body = (
                r.json()
                if r.headers.get("content-type", "").startswith("application/json")
                else {}
            )
            model_name, reason = self._parse_403(body)
            raise ModelAccessDenied(model_name=model_name, reason=reason)
        r.raise_for_status()
        return r.json()

    def _stream_to_file(self, get_url, dest, expected_size=None, expected_sha256=None):
        """
        Download to ``dest`` (atomic via a ``.part`` file), tolerating
        expired signed URLs and interrupted streams.

        ``get_url`` is invoked once per HTTP request so every attempt —
        including Range resumes — gets a fresh signed URL. A plain URL
        string is also accepted for backwards compatibility.

        The initial request downloads the whole file. Interrupted streams
        are resumed with an open-ended Range request from the bytes written,
        with at most ``MAX_STREAM_RETRIES`` retries between advances past the
        furthest byte written (i.e. as long as newer data chunks keep
        arriving, we can retry forever). Partial responses are validated
        before appending, including servers returning 200 with Content-Range.
        A resumed 200 without Content-Range restarts from byte 0. The final
        size must match ``expected_size`` or the size reported by the server,
        when available. Oversized or zero-size responses raise ``IOError``.
        Free disk space is checked against the expected size up front when
        known, otherwise once when the server first reports a size. Other
        4xx errors raise immediately; retriable errors (server errors
        and 408/425/429) are retried with short exponential backoff,
        honoring a ``Retry-After`` header when present. On terminal
        failure the ``.part`` file is removed.

        When ``expected_sha256`` is given, the digest is computed
        incrementally from the bytes as they are written to the ``.part``
        file (reset alongside the byte counter on a restart from byte 0),
        so no second pass over the finished file is needed. A mismatch
        raises ``IOError`` before the ``.part`` file is renamed into place.

        Returns
        -------
        int
            Number of bytes written to ``dest``.
        """
        if expected_size is not None and expected_size <= 0:
            # Zero-size model artifacts indicate corrupt catalog data
            raise IOError(
                "Download of %s was requested with an expected size of %d bytes"
                % (dest, expected_size)
            )
        if not callable(get_url):
            fixed_url = get_url

            def get_url():
                return fixed_url

        tmp = dest + ".part"
        downloaded = 0
        furthest_downloaded = 0
        short_streams = 0
        total = expected_size
        last_pct = -1
        space_checked = False
        hasher = hashlib.sha256() if expected_sha256 else None
        if expected_size is not None:
            _check_free_space(dest, expected_size)
            space_checked = True

        try:
            while True:
                start = downloaded
                headers = {}
                if start:
                    headers["Range"] = "bytes=%d-" % start

                error = None
                try:
                    with self._session.get(
                        get_url(), stream=True, timeout=(30, 120), headers=headers
                    ) as r:
                        content_range = r.headers.get("content-range")
                        # The catalog download server honors Range but returns 200,
                        # not 206. Trust validated range metadata, not status alone.
                        partial = r.status_code == 206 or content_range is not None
                        if r.status_code == 200 and start and not partial:
                            # Server ignored the Range header; restart from scratch.
                            _log(
                                "download",
                                "got 200 for a ranged request; restarting from byte 0",
                            )
                            downloaded = 0
                            if hasher is not None:
                                hasher = hashlib.sha256()
                            last_pct = -1
                        r.raise_for_status()
                        if r.status_code not in (200, 206):
                            raise IOError(
                                "Unexpected download status: %s" % r.status_code
                            )
                        content_length = r.headers.get("content-length")
                        declared = (
                            int(content_length) if content_length is not None else None
                        )

                        if partial:
                            # This server uses '*' for the total and may omit the
                            # end (bytes N-/*). Recover that end from Content-Length.
                            match = re.fullmatch(
                                r"bytes (\d+)-(\d*)/(\d+|\*)", content_range or ""
                            )
                            if not match:
                                raise IOError(
                                    "Invalid Content-Range: %r" % content_range
                                )
                            range_start = int(match[1])
                            range_end = (
                                int(match[2])
                                if match[2]
                                else (
                                    range_start + declared - 1
                                    if declared is not None
                                    else None
                                )
                            )
                            range_total = int(match[3]) if match[3] != "*" else None
                            if (
                                (r.status_code == 206 and not start)
                                or range_start != downloaded
                                or range_end is None
                                or range_end < range_start
                                or (
                                    range_total is not None and range_end >= range_total
                                )
                                or (total is not None and range_end >= total)
                                or (
                                    total is not None
                                    and range_total is not None
                                    and range_total != total
                                )
                                or (
                                    declared is not None
                                    and declared != range_end - range_start + 1
                                )
                            ):
                                raise IOError(
                                    "Unexpected Content-Range: %r" % content_range
                                )
                            if range_total is not None:
                                total = range_total
                            response_limit = range_end + 1
                        elif total is None and declared is not None:
                            total = declared

                        if not partial:
                            response_limit = declared if declared is not None else total

                        # Check free space once, as soon as the total size is
                        # known — either from the caller or from the server.
                        if total is not None and not space_checked:
                            space_checked = True
                            _check_free_space(dest, total)

                        if total == 0:
                            # Treat zero-size body as corrupt catalog/server data
                            raise IOError(
                                "Download of %s: server reported a zero-byte file"
                                % dest
                            )

                        if (
                            total is not None
                            and response_limit is not None
                            and response_limit > total
                        ):
                            raise IOError(
                                "Download of %s exceeds expected size of %d bytes"
                                % (dest, total)
                            )

                        with open(tmp, "wb" if downloaded == 0 else "ab") as f:
                            for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
                                if not chunk:
                                    continue
                                if (
                                    response_limit is not None
                                    and downloaded + len(chunk) > response_limit
                                ):
                                    raise IOError(
                                        "Download of %s exceeds expected size of "
                                        "%d bytes" % (dest, response_limit)
                                    )
                                f.write(chunk)
                                if hasher is not None:
                                    hasher.update(chunk)
                                downloaded += len(chunk)
                                if downloaded > furthest_downloaded:
                                    furthest_downloaded = downloaded
                                    short_streams = 0
                                if total:
                                    pct = int(downloaded * 100 / total)
                                    if pct >= last_pct + 5:
                                        _log(
                                            "download",
                                            "%d / %d MB (%d%%)"
                                            % (downloaded >> 20, total >> 20, pct),
                                        )
                                        last_pct = pct
                except requests.HTTPError as e:
                    status = e.response.status_code if e.response is not None else 0
                    if status < 500 and status not in RETRYABLE_4XX:
                        # A fresh signed URL was just used; most 4xx errors will
                        # not fix themselves on retry.
                        raise
                    error = e
                    # The server may be throttling or restarting: back off
                    # before retrying instead of exhausting the retry budget
                    # with immediate attempts. A Retry-After header wins when
                    # present; otherwise back off exponentially.
                    delay = _retry_after_seconds(e.response, RETRY_BACKOFF_CAP)
                    if not delay:
                        delay = min(
                            RETRY_BACKOFF_CAP,
                            RETRY_BACKOFF_BASE * (2**short_streams),
                        )
                    _log("download", "got %d; retrying in %.1fs" % (status, delay))
                    time.sleep(delay)
                except requests.RequestException as e:
                    # Includes ChunkedEncodingError (short read), ConnectionError,
                    # and Timeout.
                    error = e

                if total is not None:
                    if downloaded == total:
                        break
                elif error is None and (not partial or downloaded == response_limit):
                    break

                # The server can cap a response even for an open-ended range.
                # A fully received partial response is progress, not a failed
                # stream.
                if error is None and partial and downloaded == response_limit:
                    continue

                short_streams += 1
                if short_streams > MAX_STREAM_RETRIES:
                    raise IOError(
                        "Download of %s was interrupted %d times without new "
                        "progress; gave up after "
                        "%d of %s bytes. Last error: %s"
                        % (
                            dest,
                            short_streams,
                            downloaded,
                            total if total is not None else "unknown",
                            error,
                        )
                    )
                _log(
                    "download",
                    "short stream after %d bytes (%s); retry %d/%d since last "
                    "new progress from byte %d "
                    "with a fresh signed URL"
                    % (
                        downloaded,
                        error,
                        short_streams,
                        MAX_STREAM_RETRIES,
                        downloaded,
                    ),
                )

            if total is not None and downloaded != total:
                raise IOError(
                    "Download of %s is incomplete: got %d bytes, expected %d"
                    % (dest, downloaded, total)
                )
            if hasher is not None:
                actual = hasher.hexdigest()
                if actual != expected_sha256:
                    raise IOError(
                        "SHA256 mismatch for %s: expected %s, got %s"
                        % (dest, expected_sha256, actual)
                    )
                _log("download", "sha256 verified: %s..." % actual[:16])
            os.replace(tmp, dest)
        finally:
            # Clean up the .part file on any terminal failure. On success it
            # has already been renamed to dest, so this is a no-op.
            if os.path.exists(tmp):
                os.remove(tmp)
        return downloaded


# ======================================================================
# Layer 2 — One model on disk
# ======================================================================


class AnacondaModel:
    """
    One model on disk.  Created via ``client.model(...)``.

    Backed by either a single file (gguf quants — ``.path`` is the file)
    or a multi-file safetensor collection (``.path`` is a HuggingFace-layout
    directory).  Either way, ``.path`` is what you hand to your loader.

    Holds the complete resolved state for one model, structured for
    easy consumption by a card or any other renderer.

    State available at construction (from catalog response):
        identity, provenance, license_info, all_quants, selected_model

    State populated at pull time (extra API calls, never fatal):
        test_scores, files, download_status
    """

    def __init__(self, client, model_dict, selected_model_info, root_dir=None):
        self._client = client
        self._model_dict = model_dict
        self._selected_model_info = selected_model_info

        self._root_dir = root_dir or tempfile.mkdtemp(prefix="anaconda_models_")
        self._owns_root = root_dir is None

        # Pre-compute the destination path. A collection occupies the whole
        # model directory; a single file lives inside it.
        model_dir = os.path.join(self._root_dir, _safe_dirname(model_dict["name"]))
        self._dir = model_dir
        self.is_collection = bool(selected_model_info.get("is_collection"))
        if self.is_collection:
            self._path = model_dir
        else:
            self._path = os.path.join(
                model_dir, _quant_filename(model_dict, selected_model_info)
            )
        self._pulled = False

        # -----------------------------------------------------------
        # Structured state — extracted once at construction from the
        # model_dict that the catalog already returned.
        # -----------------------------------------------------------

        self.identity = {
            "name": model_dict.get("name"),
            "description": model_dict.get("description"),
            "model_uuid": model_dict.get("model_uuid"),
            "num_parameters": model_dict.get("num_parameters"),
            "model_type": model_dict.get("model_type"),
            "trained_for": model_dict.get("trained_for"),
            "base_models": model_dict.get("base_models", []),
            "base_model": model_dict.get("base_model"),
            "context_window_size": model_dict.get("context_window_size")
            or selected_model_info.get("context_window_size"),
            "knowledge_cut_off": model_dict.get("knowledge_cut_off"),
            "has_chat_template": model_dict.get("has_chat_template"),
            "supports_tool_calling": model_dict.get("supports_tool_calling"),
            "library_name": model_dict.get("library_name"),
            "modality": model_dict.get("modality"),
        }

        self.provenance = {
            "source": model_dict.get("source", {}),
            "source_url": model_dict.get("source_url"),
            "git_repo_url": model_dict.get("git_repo_url"),
            "paper_url": model_dict.get("paper_url"),
            "info_url": model_dict.get("info_url"),
            "first_published": model_dict.get("first_published"),
            "languages": model_dict.get("languages", []),
            "datasets": model_dict.get("datasets", []),
            "country_of_origin": model_dict.get("country_of_origin"),
            "curation_source": model_dict.get("curation_source"),
            "tags": model_dict.get("tags", []),
        }

        # license_details is already embedded in the model response
        ld = model_dict.get("license_details") or {}
        self.license_info = {
            "license": model_dict.get("license"),
            "license_summary": model_dict.get("license_summary"),
            "name": ld.get("name"),
            "commercial_use": ld.get("commercial_use"),
            "fine_tuning_permitted": ld.get("fine_tuning_permitted"),
            "attribution_required": ld.get("attribution_required"),
            "open_weights": ld.get("open_weights"),
            "requires_acceptance": ld.get("requires_acceptance"),
            "data_privacy": ld.get("data_privacy"),
            "license_link": ld.get("license_link"),
        }

        self.selected_model = {
            "file_uuid": selected_model_info.get("file_uuid"),
            "quant_method": selected_model_info.get("quant_method"),
            "format": selected_model_info.get("format"),
            "quant_engine": selected_model_info.get("quant_engine"),
            "size_bytes": selected_model_info.get("size_bytes"),
            "max_ram_usage": selected_model_info.get("max_ram_usage"),
            "sha256": selected_model_info.get("sha256"),
            "filename": selected_model_info.get("filename"),
            "published": selected_model_info.get("published"),
            # Collection-only fields (None for single files)
            "is_collection": self.is_collection,
            "collection_type": selected_model_info.get("collection_type"),
            "file_count": selected_model_info.get("file_count"),
            "total_size_bytes": selected_model_info.get("total_size_bytes"),
        }

        self.all_quants = [
            {
                "file_uuid": q.get("file_uuid"),
                "quant_method": q.get("quant_method"),
                "format": q.get("format"),
                "size_bytes": q.get("size_bytes"),
                "max_ram_usage": q.get("max_ram_usage"),
                "published": q.get("published"),
            }
            for q in model_dict.get("quantized_files", [])
        ]

        # -----------------------------------------------------------
        # State populated at pull time (enrichment — never fatal)
        # -----------------------------------------------------------
        self.test_scores = []  # list of {test_name, test_value, ...}
        self.files = []  # list of {filename, size_bytes, sha256, status}
        self.download_status = None  # "downloaded", "skipped", or None

    # ------------------------------------------------------------------
    # Convenience properties (shortcuts into structured state)
    # ------------------------------------------------------------------

    @property
    def name(self):
        return self.identity["name"]

    @property
    def quant_method(self):
        return self.selected_model["quant_method"]

    @property
    def format(self):
        return self.selected_model["format"]

    @property
    def collection_type(self):
        """The collection's type, e.g. "original" (None for single files)."""
        return self.selected_model["collection_type"]

    @property
    def file_count(self):
        return self.selected_model["file_count"]

    @property
    def size(self):
        return self.selected_model["size_bytes"] or self.selected_model.get(
            "total_size_bytes"
        )

    @property
    def sha256(self):
        return self.selected_model["sha256"]

    @property
    def model_uuid(self):
        return self.identity["model_uuid"]

    @property
    def file_uuid(self):
        return self.selected_model["file_uuid"]

    @property
    def metadata(self):
        """Full model catalog dict (raw)."""
        return self._model_dict

    @property
    def path(self):
        """What you hand to the loader: a file for single files, a
        HuggingFace-layout directory for collections."""
        return self._path

    @property
    def dir(self):
        return self._dir

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def pull(self, verify_sha256=True):
        """
        Download the model to disk — the single file, or every file in the
        collection manifest for safetensor collections.

        Also fetches enrichment metadata (test scores).
        Enrichment failures are logged but never raise.

        Returns
        -------
        str
            The local path (same as .path).
        """
        tag = "model:%s" % self.name

        if self.is_collection:
            self._pull_collection(tag, verify_sha256)
        else:
            self._pull_single(tag, verify_sha256)

            # Enrich: fetch test scores for this specific quant file.
            # Non-fatal — if it fails we just have an empty list.
            self.test_scores = self._client.get_test_scores(
                self.model_uuid, self.file_uuid
            )
            if self.test_scores:
                _log(tag, "loaded %d test scores" % len(self.test_scores))

        return self._path

    def _pull_single(self, tag, verify_sha256):
        """Download the one file via keywest."""
        sha256 = self.sha256
        if self._is_present():
            if verify_sha256 and sha256:
                _verify_sha256(tag, self._path, sha256)
            _log(
                tag,
                "already on disk (%d bytes), skipping." % os.path.getsize(self._path),
            )
            self._pulled = True
            self.download_status = "skipped"
        else:
            url_fn = lambda: self._client.get_download_url(
                self.model_uuid,
                self.selected_model["file_uuid"],
                model_name=self.name,
            )
            os.makedirs(self._dir, exist_ok=True)

            _log(
                tag,
                "downloading %s (%d MB) ..."
                % (self.quant_method, (self.size or 0) >> 20),
            )
            self._client._stream_to_file(
                url_fn,
                self._path,
                expected_size=self.size,
                expected_sha256=sha256 if verify_sha256 else None,
            )

            self._pulled = True
            self.download_status = "downloaded"
            _log(tag, "saved to %s" % self._path)

        self.files = [
            {
                "filename": os.path.basename(self._path),
                "size_bytes": self.selected_model["size_bytes"],
                "sha256": sha256,
                "status": self.download_status,
            }
        ]

    def _pull_collection(self, tag, verify_sha256):
        """
        Download every file in the collection manifest into the model dir
        (HuggingFace layout).

        Resumable: files already present with the expected size are verified
        and skipped. Each downloaded file is verified against the manifest
        size + SHA256.
        """
        collection_uuid = self.selected_model["file_uuid"]
        manifest = self._client.get_collection_manifest(
            self.model_uuid, collection_uuid, model_name=self.name
        )
        entries = manifest.get("files", [])
        if not entries:
            raise LookupError("Collection %r manifest is empty (0 files)." % self.name)
        total_mb = (manifest.get("total_size_bytes") or 0) >> 20
        _log(tag, "manifest: %d files, %d MB" % (len(entries), total_mb))

        os.makedirs(self._dir, exist_ok=True)
        self.files = []
        n_downloaded = 0
        n_skipped = 0

        for entry in entries:
            filename = entry["filename"]
            _validate_manifest_filename(filename)
            size_bytes = entry.get("size_bytes")
            sha256 = entry.get("sha256")
            local_path = os.path.join(self._dir, filename)

            if os.path.exists(local_path) and (
                not size_bytes or os.path.getsize(local_path) == size_bytes
            ):
                if verify_sha256 and sha256:
                    _verify_sha256(tag, local_path, sha256)
                status = "skipped"
                n_skipped += 1
            else:
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                url_fn = lambda filename=filename: self._client.get_collection_file_url(
                    self.model_uuid,
                    collection_uuid,
                    filename,
                    model_name=self.name,
                )
                self._client._stream_to_file(
                    url_fn,
                    local_path,
                    expected_size=size_bytes,
                    expected_sha256=sha256 if verify_sha256 else None,
                )
                status = "downloaded"
                n_downloaded += 1

            self.files.append(
                {
                    "filename": filename,
                    "size_bytes": size_bytes,
                    "sha256": sha256,
                    "status": status,
                }
            )

        self._pulled = True
        self.download_status = (
            "skipped" if (n_skipped and not n_downloaded) else "downloaded"
        )
        _log(
            tag,
            "verified %d/%d files; dir ready at %s"
            % (len(self.files), len(self.files), self._dir),
        )

    def delete(self):
        """Remove the downloaded file(s) and the model subdirectory."""
        if self.is_collection:
            if os.path.isdir(self._dir):
                shutil.rmtree(self._dir, ignore_errors=True)
        else:
            if os.path.exists(self._path):
                os.remove(self._path)
            if os.path.isdir(self._dir) and not os.listdir(self._dir):
                os.rmdir(self._dir)
        if (
            self._owns_root
            and os.path.isdir(self._root_dir)
            and not os.listdir(self._root_dir)
        ):
            os.rmdir(self._root_dir)
        self._pulled = False
        self.download_status = None

    def _is_present(self):
        if self.is_collection:
            # Per-file presence is decided against the manifest at pull time.
            return self._pulled
        if not os.path.exists(self._path):
            return False
        if self.size and os.path.getsize(self._path) != self.size:
            return False
        return True

    def __getstate__(self):
        state = self.__dict__.copy()
        state["_client"] = None  # requests.Session is not picklable
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __repr__(self):
        status = "pulled" if self._pulled or self._is_present() else "not pulled"
        kind = (
            "%s collection (%s files)" % (self.format, self.file_count)
            if self.is_collection
            else self.quant_method
        )
        return "AnacondaModel(%s, %s, %s)" % (self.name, kind, status)


# ======================================================================
# Helpers
# ======================================================================


def _safe_dirname(name):
    return name.replace("/", "_").replace("\\", "_").replace(" ", "_")


def _check_free_space(dest, needed):
    """Raise IOError if the filesystem holding ``dest`` lacks ``needed`` bytes."""
    target_dir = os.path.dirname(os.path.abspath(dest))
    free = shutil.disk_usage(target_dir).free
    if free < needed:
        raise IOError(
            "Insufficient disk space for %s: need %d bytes (%d MB), "
            "but only %d bytes (%d MB) are free"
            % (dest, needed, needed >> 20, free, free >> 20)
        )


def _quant_filename(model_dict, quant_dict):
    fmt = quant_dict.get("format", "gguf")
    if quant_dict.get("filename"):
        base = quant_dict["filename"]
        if not base.endswith(".%s" % fmt):
            base = "%s.%s" % (base, fmt)
        return base
    name = _safe_dirname(model_dict["name"])
    method = quant_dict.get("quant_method", "unknown")
    return "%s-%s.%s" % (name, method, fmt)


def _verify_sha256(tag, path, expected):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            h.update(chunk)
    actual = h.hexdigest()
    if actual != expected:
        raise IOError(
            "SHA256 mismatch for %s: expected %s, got %s" % (path, expected, actual)
        )
    _log(tag, "sha256 verified: %s..." % actual[:16])


def _validate_manifest_filename(filename):
    normalized = filename.replace("\\", "/")
    if normalized.startswith("/"):
        raise ValueError("Unsafe collection filename (absolute path): %r" % filename)
    if ".." in normalized.split("/"):
        raise ValueError("Unsafe collection filename (path traversal): %r" % filename)


def _hfname(model):
    source = model.get("source", {}).get("name", "<NO SOURCE>")
    name = model.get("name", "<NO NAME>")
    return f"{source}/{name}"
