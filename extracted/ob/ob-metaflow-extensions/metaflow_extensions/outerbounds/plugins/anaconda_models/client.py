"""
Two-layer client for pulling models from the Anaconda AI catalog.

Layer 1 — AnacondaModelClient: talks to the catalog API. No disk I/O.
Layer 2 — AnacondaModel: one model on disk. Owns its file and lifecycle.

Usage:
    client = AnacondaModelClient(api_key="...")
    model = client.model("Qwen2.5-0.5B", quant_method="q4_k_m",
                         root_dir="/tmp/models")
    model.pull()
    print(model.path)   # /tmp/models/Qwen2.5-0.5B/Qwen_Qwen2.5-0.5B-q4_k_m.gguf
    model.delete()
"""

import hashlib
import os
import sys
import tempfile

import requests


API_BASE = "https://anaconda.com/api/ai/model"
API_VERSION = "2"
CHUNK_SIZE = 8 * 1024 * 1024  # 8 MB


def _log(source, msg):
    """Write a prefixed log line to stderr."""
    sys.stderr.write("[%s] %s\n" % (source, msg))
    sys.stderr.flush()


# ======================================================================
# Layer 1 — Catalog client (API only, no disk I/O)
# ======================================================================


class AnacondaModelClient:
    """
    Talks to the Anaconda AI model catalog.

    Parameters
    ----------
    api_key : str
        Anaconda API bearer token.
    """

    def __init__(self, api_key):
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": "Bearer %s" % api_key,
                "X-Anaconda-Api-Version": API_VERSION,
            }
        )

    def list_models(self, limit=20, **filters):
        """
        List models from the catalog.

        Parameters
        ----------
        limit : int
            Max models to return.
        **filters
            Query params: name, search, model_type, quant_method, etc.

        Returns
        -------
        list[dict]
        """
        params = {"limit": limit}
        params.update(filters)
        return self._get("/models", params=params)["result"]["data"]

    def get_model(self, model_name):
        """
        Look up a single model by exact name.

        Raises
        ------
        LookupError
            If the model is not found.
        """
        models = self.list_models(name=model_name, limit=5)
        for m in models:
            if m["name"] == model_name:
                return m
        available = [m["name"] for m in models]
        raise LookupError(
            "Model %r not found. Closest matches: %s" % (model_name, available)
        )

    def resolve_quant(self, model_name, quant_method=None):
        """
        Resolve a model and pick a quantized file.

        Parameters
        ----------
        model_name : str
            Exact name in the catalog.
        quant_method : str, optional
            e.g. "q4_k_m". If omitted, picks smallest published GGUF.

        Returns
        -------
        (dict, dict)
            (model_dict, quant_dict)
        """
        model = self.get_model(model_name)
        qfiles = model.get("quantized_files", [])
        if not qfiles:
            raise LookupError("Model %r has no quantized files." % model_name)

        if quant_method:
            match = [q for q in qfiles if q.get("quant_method") == quant_method]
            if not match:
                available = [q.get("quant_method") for q in qfiles]
                raise LookupError(
                    "Quant %r not found for %r. Available: %s"
                    % (quant_method, model_name, available)
                )
            return model, match[0]

        published = [q for q in qfiles if q.get("published")] or qfiles
        chosen = min(published, key=lambda q: q.get("size_bytes") or float("inf"))
        return model, chosen

    def get_download_url(self, model_uuid, file_uuid):
        """
        Get a signed download URL for a file.

        Returns
        -------
        str
            The download URL.
        """
        path = "/models/%s/files/%s/download" % (model_uuid, file_uuid)
        data = self._get(path, params={"redirect": "false", "stream": "false"})
        return data["download_url"]

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
            path = "/models/%s/test-scores/%s" % (model_uuid, file_uuid)
            data = self._get(path)
            return data.get("data", [])
        except Exception as e:
            _log("client", "test-scores fetch failed (non-fatal): %s" % e)
            return []

    def get_license(self, model_uuid):
        """
        Fetch full license details for a model.

        Returns
        -------
        dict or None
            License dict with fields like commercial_use, fine_tuning_permitted,
            attribution_required, open_weights, etc. None on error.
        """
        try:
            path = "/license/%s" % model_uuid
            data = self._get(path)
            return data.get("data", data)
        except Exception as e:
            _log("client", "license fetch failed (non-fatal): %s" % e)
            return None

    def model(self, model_name, quant_method=None, root_dir=None):
        """
        Create an AnacondaModel — a handle to one model file on disk.

        Resolves catalog metadata immediately. Does not download yet.

        Parameters
        ----------
        model_name : str
            Exact name in the catalog.
        quant_method : str, optional
            e.g. "q4_k_m". If omitted, picks smallest published GGUF.
        root_dir : str, optional
            Root directory for the download.  A subdirectory per model
            is created underneath.  Defaults to a new temp directory.

        Returns
        -------
        AnacondaModel
        """
        model_dict, quant_dict = self.resolve_quant(model_name, quant_method)
        return AnacondaModel(self, model_dict, quant_dict, root_dir=root_dir)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _get(self, path, params=None):
        r = self._session.get(API_BASE + path, params=params, timeout=30)
        r.raise_for_status()
        return r.json()

    def _stream_to_file(self, url, dest, expected_size=None):
        """Download url to dest with chunked streaming."""
        tmp = dest + ".part"
        downloaded = 0
        last_pct = -1

        with self._session.get(url, stream=True, timeout=600) as r:
            r.raise_for_status()
            total = expected_size or int(r.headers.get("content-length", 0)) or None
            with open(tmp, "wb") as f:
                for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        pct = int(downloaded * 100 / total)
                        if pct >= last_pct + 10:
                            _log(
                                "download",
                                "%d / %d MB (%d%%)"
                                % (downloaded >> 20, total >> 20, pct),
                            )
                            last_pct = pct

        os.replace(tmp, dest)
        return downloaded


# ======================================================================
# Layer 2 — One model on disk
# ======================================================================


class AnacondaModel:
    """
    A single model file on disk.  Created via ``client.model(...)``.

    Holds the complete resolved state for one model, structured for
    easy consumption by a card or any other renderer.

    State available at construction (from catalog response):
        identity, provenance, license_info, all_quants, selected_quant

    State populated at pull time (extra API calls, never fatal):
        test_scores, download_status
    """

    def __init__(self, client, model_dict, quant_dict, root_dir=None):
        self._client = client
        self._model_dict = model_dict
        self._quant_dict = quant_dict

        self._root_dir = root_dir or tempfile.mkdtemp(prefix="anaconda_models_")
        self._owns_root = root_dir is None

        # Pre-compute the destination path
        model_dir = os.path.join(self._root_dir, _safe_dirname(model_dict["name"]))
        filename = _quant_filename(model_dict, quant_dict)
        self._dir = model_dir
        self._path = os.path.join(model_dir, filename)
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
            "base_model": model_dict.get("base_model"),
            "context_window_size": model_dict.get("context_window_size"),
            "knowledge_cut_off": model_dict.get("knowledge_cut_off"),
            "has_chat_template": model_dict.get("has_chat_template"),
            "supports_tool_calling": model_dict.get("supports_tool_calling"),
            "library_name": model_dict.get("library_name"),
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

        self.selected_quant = {
            "file_uuid": quant_dict.get("file_uuid"),
            "quant_method": quant_dict.get("quant_method"),
            "format": quant_dict.get("format"),
            "quant_engine": quant_dict.get("quant_engine"),
            "size_bytes": quant_dict.get("size_bytes"),
            "max_ram_usage": quant_dict.get("max_ram_usage"),
            "sha256": quant_dict.get("sha256"),
            "filename": quant_dict.get("filename"),
            "published": quant_dict.get("published"),
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
        self.download_status = None  # "downloaded", "skipped", or None

    # ------------------------------------------------------------------
    # Convenience properties (shortcuts into structured state)
    # ------------------------------------------------------------------

    @property
    def name(self):
        return self.identity["name"]

    @property
    def quant_method(self):
        return self.selected_quant["quant_method"]

    @property
    def size(self):
        return self.selected_quant["size_bytes"]

    @property
    def sha256(self):
        return self.selected_quant["sha256"]

    @property
    def model_uuid(self):
        return self.identity["model_uuid"]

    @property
    def file_uuid(self):
        return self.selected_quant["file_uuid"]

    @property
    def metadata(self):
        """Full model catalog dict (raw)."""
        return self._model_dict

    @property
    def quant_metadata(self):
        """Full quantized-file catalog dict (raw)."""
        return self._quant_dict

    @property
    def path(self):
        return self._path

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def pull(self, verify_sha256=True):
        """
        Download the model file to disk.

        Also fetches enrichment metadata (test scores, full license).
        Enrichment failures are logged but never raise.

        Returns
        -------
        str
            The local file path (same as .path).
        """
        tag = "model:%s" % self.name

        if self._is_present():
            _log(
                tag,
                "already on disk (%d bytes), skipping." % os.path.getsize(self._path),
            )
            self._pulled = True
            self.download_status = "skipped"
        else:
            url = self._client.get_download_url(self.model_uuid, self.file_uuid)
            os.makedirs(self._dir, exist_ok=True)

            _log(
                tag,
                "downloading %s (%d MB) ..."
                % (self.quant_method, (self.size or 0) >> 20),
            )
            self._client._stream_to_file(url, self._path, expected_size=self.size)

            if verify_sha256 and self.sha256:
                _verify_sha256(tag, self._path, self.sha256)

            self._pulled = True
            self.download_status = "downloaded"
            _log(tag, "saved to %s" % self._path)

        # Enrich: fetch test scores for this specific quant file.
        # Non-fatal — if it fails we just have an empty list.
        self.test_scores = self._client.get_test_scores(self.model_uuid, self.file_uuid)
        if self.test_scores:
            _log(tag, "loaded %d test scores" % len(self.test_scores))

        # Enrich: fetch full license if embedded license_details was sparse.
        if not self.license_info.get("commercial_use"):
            full_license = self._client.get_license(self.model_uuid)
            if full_license:
                for key in self.license_info:
                    if not self.license_info[key] and key in full_license:
                        self.license_info[key] = full_license[key]

        return self._path

    def delete(self):
        """Remove the downloaded file (and its model subdirectory if empty)."""
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
        if not os.path.exists(self._path):
            return False
        if self.size and os.path.getsize(self._path) != self.size:
            return False
        return True

    def __repr__(self):
        status = "pulled" if self._pulled or self._is_present() else "not pulled"
        return "AnacondaModel(%s, %s, %s)" % (self.name, self.quant_method, status)


# ======================================================================
# Helpers
# ======================================================================


def _safe_dirname(name):
    return name.replace("/", "_").replace("\\", "_").replace(" ", "_")


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
