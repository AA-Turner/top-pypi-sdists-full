"""A fake data-catalog server for the SDK and CLI tests (plan data-catalog, PR D).

It answers the catalog routes EXACTLY as the plan's Interfaces section spells
them -- paths, body keys, status codes -- and hands every other request to the
ordinary `FakeApp` (runs, artifacts, presigned uploads, downloads), so a test
drives the real `Client`/`Run` end to end. The server lanes (PRs A-C) build the
real routes to the same contract; a test here that a contract change breaks is
the signal to re-check both sides.

    POST   /v1/sources                      201 new | 200 existing
    GET    /v1/sources/{ref}
    POST   /v1/runs/{run}/uses              {target, roles, share?} | {mixture, role}
    PUT    /v1/catalog/manifests/{sha256}   gzip JSON, 204
    POST   /v1/catalog/datasets/uploads     {name, manifest_hash} -> {have, uploads, bytes_new, deferred} | 402
    POST   /v1/catalog/datasets             201 {entry, version, created_entry, created_version, recorded_step}
    GET    /v1/catalog/datasets[/{ref}[/files]]
    GET    /v1/catalog/checkpoints | /v1/catalog/sources | /v1/provenance
    POST   /v1/shared/files/{id}/confirm    a hosted blob: 409 unsent, or LARGER than the door reserved
    GET|POST /v1/shared/files/multipart/{upload_id}[/parts|/complete]   a hosted blob over the threshold
    POST   /v1/artifacts/{entry}/versions/{n}/download   {download_url} | 409 {reason: reference, ...}

The hosting door and the files list follow the server (`app/catalog/hosting.py`,
`app/catalog/dataset_reads.py`): a door call answers at most
``door_max_uploads`` blobs, ``door_max_multipart`` of them multipart, in
content-hash order, and says how many wait (``deferred``); a blob is hosted
(`have`, listed with an `artifact_id`) only once CONFIRMED, or for a multipart
one once its verifier answers `verified` (``verify_polls`` status reads after
`complete`). A one-file version lists itself: its `artifact_id` is the entry's
for the live version only, and `download: {artifact_id, version}` names any
stored version.

Switches: ``old_server`` (every catalog route is FastAPI's own 404),
``register_delay`` (seconds the registration takes), ``hosted_cap`` (bytes;
over it the upload door answers 402 `hosted_data_bytes`), ``multipart_over``
(blobs over this many bytes get a multipart upload instead of one PUT),
``reserve_less`` (the door reserves one byte less than a blob, so its confirm
answers 409 as the server does for an object larger than reserved),
``give_up_once`` (a failure reason: each blob's first multipart upload reads as
`failed` with it, as when Probe gave up on an upload left idle; the door then
opens a new one) and ``hosted_meanwhile`` (that upload's blob is hosted by
another upload by then). The generic Shared multipart create refuses a
`.probe/datasets/` name (422), as the server's name check does.
"""

from __future__ import annotations

import base64
import gzip
import hashlib
import json
import re
import time
import uuid
from typing import Any

import httpx

from tests.conftest import FakeApp

ROLES = {"train", "validation", "test", "eval", "init", "tokenizer", "other"}
NAME = re.compile(r"^[a-z0-9][a-z0-9._-]{0,127}$")

_USES = re.compile(r"^/v1/runs/([^/]+)/uses$")
_SOURCE = re.compile(r"^/v1/sources/(.+)$")
_MANIFEST = re.compile(r"^/v1/catalog/manifests/([0-9a-f]{64})$")
_DATASET_FILES = re.compile(r"^/v1/catalog/datasets/([^/]+)/files$")
_DATASET = re.compile(r"^/v1/catalog/datasets/([^/]+)$")
_HOSTED_PUT = re.compile(r"^/hosted/([0-9a-f]{64})$")
_SHARED_MULTIPART = re.compile(r"^/v1/shared/files/multipart/([^/]+)(/parts|/complete)?$")
_PART_PUT = re.compile(r"^/hosted-part/([^/]+)/(\d+)$")
_CONFIRM = re.compile(r"^/v1/(?:artifacts|shared/files)/([^/]+)/confirm$")
_VERSION_DOWNLOAD = re.compile(r"^/v1/artifacts/([^/]+)/versions/(\d+)/download$")
#: The server's page size for `GET /v1/catalog/datasets/{ref}/files` (default 200).
FILES_PAGE = 200
_CATALOG_PREFIXES = ("/v1/sources", "/v1/catalog/", "/v1/provenance")


def manifest_identity(files: list[dict]) -> str:
    """The client's identity rule (`probe.sdk.catalog.Manifest.identity`),
    recomputed from the body as a server would."""
    digest = hashlib.sha256()
    for f in sorted(files, key=lambda f: f["relpath"]):
        line = f"{f['relpath']}\t{f['size_bytes']}\t{f.get('content_hash') or f.get('fingerprint') or ''}\n"
        digest.update(line.encode("utf-8", "surrogatepass"))
    return digest.hexdigest()


def _json(status: int, body: Any = None) -> httpx.Response:
    return httpx.Response(status, json=body) if body is not None else httpx.Response(status)


class CatalogFake:
    def __init__(self, base: FakeApp | None = None) -> None:
        self.base = base or FakeApp()
        self.old_server = False
        self.register_delay = 0.0
        self.hosted_cap: int | None = None
        self.multipart_over: int | None = None
        #: The server's per-call door limits (`hosting.MAX_DOOR_UPLOADS`, `MAX_DOOR_MULTIPART`).
        self.door_max_uploads = 1000
        self.door_max_multipart = 500
        self.reserve_less = False
        self.give_up_once: str | None = None
        self.hosted_meanwhile = False
        self._given_up: set[str] = set()
        #: Status reads a completed multipart upload answers `verifying` before `verified`.
        self.verify_polls = 1
        #: `GET .../files` rows per page when the request names no `limit`.
        self.files_page = FILES_PAGE
        self.sources: dict[str, dict] = {}
        self.uses: list[dict] = []
        self.manifests: dict[str, dict] = {}
        self.manifest_puts: list[dict] = []
        self.registrations: list[dict] = []
        self.datasets: dict[str, dict] = {}
        #: content_hash -> hosted blob artifact id (staged by the door; pending until complete).
        self.hosted: dict[str, str] = {}
        #: content_hash -> the bytes the object store holds for it.
        self.hosted_bytes: dict[str, bytes] = {}
        #: Hosted blobs that are complete: confirmed, or verified after a multipart upload.
        self.hosted_complete: set[str] = set()
        #: content_hash -> the size the door reserved for it.
        self.declared: dict[str, int] = {}
        self.upload_asks: list[dict] = []
        self.confirms: list[str] = []
        self.multipart: dict[str, dict] = {}
        self.checkpoints: list[dict] = []
        self.provenance_answer: dict = {"root": None, "nodes": [], "edges": [], "truncated": False, "hidden": 0}
        self.steps_answer: dict = {"target": None, "sources": [], "steps": []}
        self.requests: list[httpx.Request] = []
        #: (method, path) -> whether a `deadline_scope` bounded the request.
        self.deadlines: list[tuple[str, str, bool]] = []
        #: Every catalog route raises a connect error (Probe unreachable).
        self.unreachable = False
        #: A status the manifest PUT answers instead of 204 (a blip: 503).
        self.manifest_status: int | None = None

    # -- plumbing -------------------------------------------------------------
    def __getattr__(self, name: str) -> Any:  # runs, artifacts, blobs ... of the base fake
        return getattr(self.base, name)

    def handler(self, request: httpx.Request) -> httpx.Response:
        from probe.sdk import transport as _transport

        self.requests.append(request)
        path = request.url.path
        method = request.method
        self.deadlines.append((method, path, _transport._request_deadline.get() is not None))
        if self.unreachable and (path.startswith(_CATALOG_PREFIXES) or path == "/v1/server/features"):
            raise httpx.ConnectError("Probe is unreachable", request=request)
        if request.url.host == "r2.test":
            answered = self._object_store(request, path, method)
            if answered is not None:
                return answered
        if path.startswith(_CATALOG_PREFIXES) or _USES.match(path):
            if self.old_server:
                return _json(404, {"detail": "Not Found"})
            return self._catalog(request, path, method)
        if path == "/v1/shared/files/multipart" and method == "POST":
            name = str(self._body(request).get("name") or "")
            if name.startswith(".probe/datasets/"):
                return _json(422, {"detail": "names under .probe/datasets/ are reserved for hosted catalog data"})
        m = _SHARED_MULTIPART.match(path)
        if m and m.group(1) in self.multipart:
            return self._multipart(m.group(1), m.group(2), method, request)
        m = _CONFIRM.match(path)
        if m and method == "POST" and m.group(1) in self.hosted.values():
            return self._confirm(m.group(1))
        m = _VERSION_DOWNLOAD.match(path)
        if m and method == "POST" and self._entry_by_id(m.group(1)) is not None:
            return self._version_download(m.group(1), int(m.group(2)))
        return self.base.handler(request)

    def _body(self, request: httpx.Request) -> dict:
        try:
            return json.loads(request.content) if request.content else {}
        except ValueError:
            return {}

    def calls(self, method: str, path_prefix: str) -> list[httpx.Request]:
        return [r for r in self.requests if r.method == method and r.url.path.startswith(path_prefix)]

    # -- routes ---------------------------------------------------------------
    def _catalog(self, request: httpx.Request, path: str, method: str) -> httpx.Response:
        body = self._body(request)
        if path == "/v1/sources" and method == "POST":
            return self._create_source(body)
        m = _SOURCE.match(path)
        if m and method == "GET":
            row = self._source(m.group(1))
            return _json(200, self._source_out(row)) if row else _json(404, {"detail": "unknown ref"})
        m = _USES.match(path)
        if m and method == "POST":
            return self._use(m.group(1), body)
        m = _MANIFEST.match(path)
        if m and method == "PUT":
            return self._put_manifest(m.group(1), request)
        if path == "/v1/catalog/datasets/uploads" and method == "POST":
            return self._uploads(body)
        if path == "/v1/catalog/datasets" and method == "POST":
            return self._register(body)
        if path == "/v1/catalog/datasets" and method == "GET":
            return self._list_datasets()
        m = _DATASET_FILES.match(path)
        if m and method == "GET":
            return self._files(m.group(1), request.url.params)
        m = _DATASET.match(path)
        if m and method == "GET":
            entry, version = self._resolve_dataset(m.group(1))
            if entry is None:
                return _json(404, {"detail": f"unknown ref {m.group(1)}"})
            return _json(200, {**entry["public"], "versions": entry["versions"]})
        if path == "/v1/catalog/checkpoints" and method == "GET":
            return _json(200, {"items": self.checkpoints, "totals": {"bytes": sum(c.get("size_bytes") or 0 for c in self.checkpoints)}, "next_cursor": None})
        if path == "/v1/catalog/sources" and method == "GET":
            return _json(200, {"items": [self._source_out(r) for r in self.sources.values()], "next_cursor": None})
        if path == "/v1/provenance" and method == "GET":
            if request.url.params.get("format") == "steps":
                return _json(200, self.steps_answer)
            return _json(200, self.provenance_answer)
        return _json(404, {"detail": "Not Found"})

    def _create_source(self, body: dict) -> httpx.Response:
        uri = str(body.get("uri") or "")
        if "@" in uri.split("://", 1)[-1].split("/", 1)[0] or "X-Amz-Signature" in uri:
            return _json(422, {"detail": "a source uri must not carry a credential"})
        key = uri
        for prefix, canon in (("https://huggingface.co/datasets/", "hf:datasets/"), ("https://huggingface.co/", "hf:")):
            if uri.startswith(prefix):
                key = canon + uri[len(prefix):].rstrip("/")
                break
        revision = body.get("revision") or ""
        for row in self.sources.values():
            if row["canonical_key"] == key and row["revision"] == revision:
                return _json(200, {**row, "created": False})
        sid = str(uuid.uuid4())
        # The server infers the kind when none is sent (PR A: a Hub model repo
        # is a `model`, everything else a `dataset`).
        inferred = "model" if uri.startswith("https://huggingface.co/") and "/datasets/" not in uri else "dataset"
        row = {
            "id": sid, "ref": f"source:{sid}", "canonical_key": key, "provider": "huggingface" if key.startswith("hf:") else "other",
            "kind": body.get("kind") or inferred, "revision": revision, "license": body.get("license"), "uri": uri,
        }
        self.sources[sid] = row
        return _json(201, {**row, "created": True})

    def _source_out(self, row: dict) -> dict:
        """PR A's `SourceOut` on a read: the counts nested under `counts`."""
        runs = len({u["run_id"] for u in self.uses if u["target"].get("ref") == row["ref"]})
        return {**row, "counts": {"runs_using": runs, "datasets_derived": 0}}

    def _source(self, ref: str) -> dict | None:
        bare = ref.removeprefix("source:")
        return self.sources.get(bare) or next((r for r in self.sources.values() if r["canonical_key"] == bare), None)

    def _resolve_dataset(self, ref: str) -> tuple[dict | None, dict | None]:
        bare = ref.removeprefix("dataset:")
        name, _, n = bare.partition("@")
        entry = self.datasets.get(name)
        if entry is None or not entry["versions"]:
            return entry, None
        if not n or n == "latest":
            return entry, entry["versions"][-1]
        want = int(n.removeprefix("v"))
        return entry, next((v for v in entry["versions"] if v["n"] == want), None)

    def _use(self, run_id: str, body: dict) -> httpx.Response:
        if run_id not in self.base.runs:
            return _json(404, {"detail": "unknown run"})
        if "mixture" in body:
            parts = body.get("mixture") or []
            total = sum(float(p.get("share") or 0) for p in parts)
            if not parts or abs(total - 1) > 0.01 or any(float(p.get("share") or 0) <= 0 for p in parts):
                return _json(422, {"detail": "shares must be > 0 and sum to 1"})
            if body.get("role") not in ROLES:
                return _json(422, {"detail": "bad role"})
            out = []
            for p in parts:
                target = self._target(p["target"])
                if target is None:
                    return _json(404, {"detail": f"unknown ref {p['target']}"})
                out.append(target)
            self.uses = [u for u in self.uses if not (u["run_id"] == run_id and body["role"] in u["roles"] and u.get("share") is not None)]
            items = []
            for p, target in zip(parts, out):
                self.uses.append({"run_id": run_id, "target": target, "roles": [body["role"]], "share": p["share"],
                                  "provenance": body.get("provenance")})
                items.append({"edge_id": str(uuid.uuid4()), "target": target, "roles": [body["role"]],
                              "share": p["share"], "created": True})
            # Server PR A's MixtureOut.
            return _json(200, {"role": body["role"], "items": items, "cleared": 0})
        roles = body.get("roles") or []
        if not roles or any(r not in ROLES for r in roles):
            return _json(422, {"detail": "bad role"})
        target = self._target(str(body.get("target") or ""))
        if target is None:
            return _json(404, {"detail": f"unknown ref {body.get('target')}"})
        self.uses.append({"run_id": run_id, "target": target, "roles": roles, "share": body.get("share"),
                          "provenance": body.get("provenance")})
        return _json(200, {"edge_id": str(uuid.uuid4()), "target": target, "roles": roles, "created": True})

    def _target(self, ref: str) -> dict | None:
        if ref.startswith("source:"):
            row = self._source(ref)
            return {"type": "source", "id": row["id"], "ref": row["ref"]} if row else None
        if ref.startswith("dataset:"):
            _entry, version = self._resolve_dataset(ref)
            return {"type": "artifact_version", "id": version["id"], "ref": version["ref"]} if version else None
        if ref.startswith("checkpoint:"):
            return {"type": "artifact", "id": str(uuid.uuid5(uuid.NAMESPACE_URL, ref)), "ref": ref}
        return None

    def _put_manifest(self, digest: str, request: httpx.Request) -> httpx.Response:
        if self.manifest_status is not None:
            return _json(self.manifest_status, {"detail": "not now"})
        if request.headers.get("content-encoding") != "gzip":
            return _json(422, {"detail": "a manifest is gzip JSON"})
        try:
            body = json.loads(gzip.decompress(request.content))
        except (OSError, ValueError):
            return _json(422, {"detail": "not gzip JSON"})
        files = body.get("files") or []
        if len(files) > 100_000 or manifest_identity(files) != digest:
            return _json(422, {"detail": "the manifest does not hash to its key"})
        self.manifests[digest] = body
        self.manifest_puts.append(body)
        return _json(204)

    def _uploads(self, body: dict) -> httpx.Response:
        """`app.catalog.hosting.host_uploads`: `have` over the whole manifest,
        then at most `door_max_uploads` of the rest (`door_max_multipart` of
        them multipart) in content-hash order, and `deferred` for the others.
        A blob staged by an earlier call keeps its row; a multipart upload
        still in flight is resumed."""
        self.upload_asks.append(body)
        digest = str(body.get("manifest_hash"))
        manifest = self.manifests.get(digest)
        if manifest is None:
            return _json(404, {"detail": {
                "message": f"no manifest {digest} in this team: PUT /v1/catalog/manifests/{digest} first",
                "code": "manifest_not_found",
            }})
        unhashed = sum(1 for f in manifest["files"] if not f.get("content_hash"))
        if unhashed:
            return _json(422, {"detail": {"message": f"{unhashed} file(s) of this manifest carry no sha256",
                                          "code": "manifest_partial", "unhashed": unhashed}})
        sizes: dict[str, int] = {}
        for f in manifest["files"]:
            sizes[f["content_hash"]] = max(sizes.get(f["content_hash"], 0), int(f["size_bytes"]))
        hashes = sorted(sizes)
        have = [h for h in hashes if h in self.hosted_complete]
        need = [h for h in hashes if h not in self.hosted_complete]
        chosen: list[str] = []
        big = 0
        for h in need:
            if len(chosen) >= self.door_max_uploads:
                break
            if self._is_big(sizes[h]):
                if big >= self.door_max_multipart:
                    continue
                big += 1
            chosen.append(h)
        new = [h for h in chosen if h not in self.hosted]
        if self.hosted_cap is not None and sum(sizes[h] for h in new) > self.hosted_cap:
            gib = 1 << 30
            return _json(402, {"detail": {
                "message": "Your team's hosted datasets and checkpoints are at the free plan's cap.",
                "code": "limit_reached", "limit": "hosted_data_bytes",
                "current": 49, "maximum": 50 * gib // gib, "plan": "free",
            }})
        uploads = []
        for h in chosen:
            if h not in self.hosted:
                self.hosted[h] = str(uuid.uuid4())
                self.declared[h] = sizes[h] - (1 if self.reserve_less else 0)
            aid = self.hosted[h]
            item: dict[str, Any] = {"content_hash": h, "artifact_id": aid, "size_bytes": self.declared[h],
                                    "url": None, "headers": {}, "confirm": None, "multipart": None}
            if self._is_big(sizes[h]):
                upload_id, up = self._active_upload(h, aid, sizes[h])
                item["multipart"] = {"upload_id": upload_id, "part_size": up["part_size"],
                                     "part_count": up["part_count"], "state": up["state"]}
            else:
                checksum = base64.b64encode(bytes.fromhex(h)).decode()
                item.update(url=f"http://r2.test/hosted/{h}", headers={"x-amz-checksum-sha256": checksum},
                            confirm=f"/v1/shared/files/{aid}/confirm")
            uploads.append(item)
        return _json(200, {"have": have, "uploads": uploads, "bytes_new": sum(u["size_bytes"] for u in uploads),
                           "deferred": len(need) - len(chosen)})

    def _is_big(self, size: int) -> bool:
        return self.multipart_over is not None and size > self.multipart_over

    def _active_upload(self, blob: str, aid: str, size: int) -> tuple[str, dict]:
        """The blob's multipart upload still `uploading`/`verifying` (resumed),
        else a new one."""
        for upload_id, up in self.multipart.items():
            if up["blob"] == blob and up["state"] in ("uploading", "verifying"):
                return upload_id, up
        upload_id = str(uuid.uuid4())
        part_size = max(1, int(self.multipart_over or 1))
        up = {"blob": blob, "artifact_id": aid, "part_size": part_size, "part_count": -(-size // part_size),
              "parts": {}, "state": "uploading", "size": size, "status_reads": 0}
        self.multipart[upload_id] = up
        return upload_id, up

    def _confirm(self, aid: str) -> httpx.Response:
        """`confirm_file_upload` for a hosted blob (`_confirm_pending_row`)."""
        blob = next(h for h, a in self.hosted.items() if a == aid)
        data = self.hosted_bytes.get(blob)
        if data is None:
            return _json(409, {"detail": {"message": "object not uploaded yet; upload before confirming"}})
        if len(data) > self.declared[blob]:
            return _json(409, {"detail": {"message": (
                "the uploaded object is larger than the size the hosting door reserved for it; "
                "upload the bytes the manifest describes")}})
        self.hosted_complete.add(blob)
        self.confirms.append(aid)
        return _json(200, {"id": aid, "status": "complete", "size_bytes": len(data)})

    def _object_store(self, request: httpx.Request, path: str, method: str) -> httpx.Response | None:
        m = _HOSTED_PUT.match(path)
        if m and method == "PUT":
            data = request.content
            # A checksum-pinned PUT: the store refuses bytes that do not match.
            pinned = request.headers.get("x-amz-checksum-sha256")
            if pinned != base64.b64encode(hashlib.sha256(data).digest()).decode() or \
                    hashlib.sha256(data).hexdigest() != m.group(1):
                return _json(400, {"detail": "BadDigest"})
            self.hosted_bytes[m.group(1)] = data
            return _json(200, {})
        m = _PART_PUT.match(path)
        if m and method == "PUT":
            self.multipart[m.group(1)]["parts"][int(m.group(2))] = request.content
            return _json(200, {})
        return None

    def _multipart(self, upload_id: str, tail: str | None, method: str, request: httpx.Request) -> httpx.Response:
        up = self.multipart[upload_id]
        numbers = range(1, up["part_count"] + 1)
        if tail is None and method == "GET":
            if self.give_up_once and up["state"] == "uploading" and up["blob"] not in self._given_up:
                # Probe's sweep aborted it (this machine went quiet past its idle limit).
                self._given_up.add(up["blob"])
                up.update(state="failed", failure_reason=self.give_up_once)
                if self.hosted_meanwhile:
                    self.hosted_complete.add(up["blob"])
            if up["state"] == "verifying":
                # The verifier: it hashes the assembled object, then confirms the blob.
                up["status_reads"] += 1
                if up["status_reads"] > self.verify_polls:
                    up["state"] = "verified"
                    self.hosted_complete.add(up["blob"])
            missing = [n for n in numbers if n not in up["parts"]] if up["state"] == "uploading" else []
            return _json(200, {"upload_id": upload_id, "artifact_id": up["artifact_id"], "state": up["state"],
                               "missing_parts": missing, "wrong_size_parts": [],
                               "failure_reason": up.get("failure_reason")})
        if tail == "/parts" and method == "POST":
            asked = self._body(request).get("part_numbers") or []
            parts = []
            for n in asked:
                size = min(up["part_size"], up["size"] - (n - 1) * up["part_size"])
                parts.append({"part_number": n, "url": f"http://r2.test/hosted-part/{upload_id}/{n}", "size": size})
            return _json(200, {"parts": parts})
        if tail == "/complete" and method == "POST":
            if up["state"] in ("verifying", "verified"):
                return _json(200, {"upload_id": upload_id, "state": up["state"]})
            data = b"".join(up["parts"][n] for n in numbers)
            if hashlib.sha256(data).hexdigest() != up["blob"]:
                return _json(409, {"detail": {"state": "failed"}})
            up["state"] = "verifying"
            self.hosted_bytes[up["blob"]] = data
            return _json(200, {"upload_id": upload_id, "state": "verifying"})
        return _json(404, {"detail": "Not Found"})

    def _register(self, body: dict) -> httpx.Response:
        if self.register_delay:
            time.sleep(self.register_delay)
        self.registrations.append(body)
        name = body.get("name")
        if not isinstance(name, str) or not NAME.match(name):
            return _json(422, {"detail": "bad name"})
        kinds = [k for k in ("from_artifact_id", "run_file", "reference", "hosted") if body.get(k)]
        if len(kinds) != 1:
            return _json(422, {"detail": "exactly one of from_artifact_id, run_file, reference, hosted"})
        for ref in body.get("sources") or []:
            if self._source(ref) is None:
                return _json(404, {"detail": f"unknown ref {ref}"})
        composition = []
        for part in body.get("composition") or []:
            _entry, version = self._resolve_dataset(part.get("target", ""))
            if version is None:
                return _json(422, {"detail": f"cannot read {part.get('target')}"})
            composition.append({"version_id": version["id"], "rows": part.get("rows"), "share": part.get("share")})
        spec = body[kinds[0]]
        producer_run = None
        blob = None
        origin = "reference"
        if kinds[0] == "hosted":
            # `hosting.hosted_bytes_of`: every blob of the manifest hosted AND complete.
            manifest = self.manifests.get(spec["manifest_hash"])
            if manifest is None:
                return _json(404, {"detail": {"message": "no such manifest", "code": "manifest_not_found"}})
            blobs = {f.get("content_hash") for f in manifest["files"]}
            missing = sum(1 for h in blobs if not h or h not in self.hosted_complete)
            if missing:
                return _json(409, {"detail": {
                    "message": f"{missing} file(s) of this manifest are not hosted and complete yet",
                    "code": "hosted_incomplete", "missing": missing,
                }})
            if spec.get("run_id") and spec["run_id"] not in self.base.runs:
                return _json(404, {"detail": "unknown run"})
            producer_run = spec.get("run_id")
            content_hash, identity, uri = spec["manifest_hash"], "bytes", f"manifest:sha256:{spec['manifest_hash']}"
            size = sum(int(f["size_bytes"]) for f in manifest["files"])
            origin = "uploaded"
        elif kinds[0] == "from_artifact_id":
            row = self.base._find_artifact(str(spec))
            if row is None or row.get("status") != "complete":
                return _json(404, {"detail": "artifact not found"})
            content_hash, uri, size = row.get("content_hash"), row.get("uri"), row.get("size_bytes")
            identity = "bytes" if not row.get("is_reference") else "pointer"
            if not row.get("is_reference"):
                origin = "promoted"
                blob = self.base.blobs.get(row["id"], self.base.blobs_by_hash.get(content_hash or "", b""))
            spec = {"meta": {"local_path": row.get("name")}}
        else:
            content_hash, identity, uri = spec["content_hash"], spec.get("identity"), spec.get("uri")
            size = spec.get("size_bytes")
            if kinds[0] == "run_file":
                run_id = spec["run_id"]
                if run_id not in self.base.runs:
                    return _json(404, {"detail": "unknown run"})
                rows = self.base.artifacts.setdefault(run_id, [])
                held = next((r for r in rows if r.get("name") == spec["name"] and r.get("content_hash") == content_hash), None)
                if held is None:
                    held = {"id": str(uuid.uuid4()), "run_id": run_id, "name": spec["name"], "kind": "dataset",
                            "uri": uri, "content_hash": content_hash, "size_bytes": size, "is_reference": True,
                            "status": "complete", "meta": spec.get("meta") or {}}
                    rows.append(held)
                producer_run = run_id
        created_entry = name not in self.datasets
        entry = self.datasets.setdefault(name, {
            "public": {"id": str(uuid.uuid4()), "ref": f"dataset:{name}", "name": name},
            "versions": [],
        })
        versions = entry["versions"]
        if versions and versions[-1]["content_hash"] == content_hash:
            version = versions[-1]
            return _json(201, {"entry": entry["public"], "version": version, "created_entry": False,
                               "created_version": False, "recorded_step": bool(producer_run)})
        n = len(versions) + 1
        version = {"id": str(uuid.uuid4()), "n": n, "ref": f"dataset:{name}@{n}", "content_hash": content_hash,
                   "identity": identity, "uri": uri, "size_bytes": size, "origin": origin,
                   "composition": composition, "change": body.get("change"),
                   "meta": spec.get("meta") if isinstance(spec, dict) else None,
                   "producer": {"run": {"ref": producer_run}, "project": "data-prep"} if producer_run else None}
        versions.append(version)
        if blob is not None:
            self.base.blobs[f"{entry['public']['id']}-v{n}"] = blob
        self._entry_row(entry, version, blob)
        return _json(201, {"entry": entry["public"], "version": {k: version[k] for k in ("id", "n", "ref", "content_hash", "identity")},
                           "created_entry": created_entry, "created_version": True, "recorded_step": bool(producer_run)})

    def _entry_row(self, entry: dict, live: dict, blob: bytes | None) -> None:
        """The team dataset's Shared row, as the base fake's download batch
        reads it: its uri and bytes are the LIVE version's."""
        rows = self.base.artifacts.setdefault("shared:catalog", [])
        row = next((r for r in rows if r["id"] == entry["public"]["id"]), None)
        if row is None:
            row = {"id": entry["public"]["id"], "name": entry["public"]["name"], "kind": "dataset"}
            rows.append(row)
        row.update(status="complete", is_reference=live["origin"] == "reference", uri=live["uri"],
                   content_hash=live["content_hash"], size_bytes=live["size_bytes"])
        if blob is not None:
            self.base.blobs[row["id"]] = blob
        else:
            self.base.blobs.pop(row["id"], None)

    def _entry_by_id(self, entry_id: str) -> dict | None:
        return next((e for e in self.datasets.values() if e["public"]["id"] == entry_id), None)

    def _version_download(self, entry_id: str, n: int) -> httpx.Response:
        """`versions_router.presign_artifact_version_download` on a team dataset."""
        entry = self._entry_by_id(entry_id)
        version = next((v for v in entry["versions"] if v["n"] == n), None) if entry else None
        if version is None:
            return _json(404, {"detail": "version not found"})
        if version["origin"] == "reference":
            meta = version.get("meta") or {}
            return _json(409, {"detail": {"reason": "reference", "uri": version["uri"],
                                          "local_path": meta.get("local_path"), "host": meta.get("host"),
                                          "content_hash": version["content_hash"], "version": n}})
        return _json(200, {"download_url": f"http://r2.test/get/{entry_id}-v{n}"})

    def _list_datasets(self) -> httpx.Response:
        items = []
        for name, entry in self.datasets.items():
            latest = entry["versions"][-1]
            used = sum(1 for u in self.uses if u["target"].get("ref", "").startswith(f"dataset:{name}@"))
            items.append({
                "ref": f"dataset:{name}", "name": name, "registered": True,
                "latest": {"n": latest["n"], "ref": latest["ref"], "content_hash": latest["content_hash"],
                           "identity": latest["identity"], "size_bytes": latest["size_bytes"], "created_at": None,
                           "producer": {"run": {"name": "dedup-v2"}, "project": {"name": "data-prep"}} if latest.get("producer") else None,
                           "locked": False},
                "versions": len(entry["versions"]), "used_by_runs": used, "sources": [],
            })
        return _json(200, {"items": items, "next_cursor": None})

    def _files(self, ref: str, params: Any) -> httpx.Response:
        """`dataset_reads.dataset_files`: a folder version lists its manifest
        rows by relpath, a page at a time, each with the team's complete hosted
        blob for its bytes (whatever the version is); a one-file version lists
        itself, downloadable by the entry for the live version (`artifact_id`)
        and by `download` for any stored one."""
        entry, version = self._resolve_dataset(ref)
        if version is None:
            return _json(404, {"detail": f"unknown ref {ref}"})
        manifest = self.manifests.get(version["content_hash"])
        if manifest is None:
            stored_id = download = None
            if version["origin"] != "reference":
                download = {"artifact_id": entry["public"]["id"], "version": version["n"]}
                if entry["versions"][-1]["n"] == version["n"]:
                    stored_id = entry["public"]["id"]
            meta = version.get("meta") or {}
            relpath = (meta.get("local_path") or "").rstrip("/").rsplit("/", 1)[-1] or entry["public"]["name"]
            return _json(200, {"ref": version["ref"], "manifest": None, "next_cursor": None, "items": [{
                "relpath": relpath, "artifact_id": stored_id, "size_bytes": version["size_bytes"],
                "rows": meta.get("rows"), "content_hash": version["content_hash"], "fingerprint": None,
                "preview_artifact_id": None, "download": download,
            }]})
        limit = int(params.get("limit") or self.files_page)
        rows = sorted(manifest["files"], key=lambda f: f["relpath"])
        cursor = params.get("cursor")
        if cursor:
            after = base64.urlsafe_b64decode(cursor.encode()).decode()
            rows = [f for f in rows if f["relpath"] > after]
        page = rows[:limit]
        items = []
        for f in page:
            blob = f.get("content_hash")
            aid = self.hosted.get(blob) if blob in self.hosted_complete else None
            if aid is not None:
                self._shared_row(aid, f)
            items.append({"relpath": f["relpath"], "artifact_id": aid, "size_bytes": f["size_bytes"],
                          "rows": f.get("rows"), "content_hash": blob, "fingerprint": f.get("fingerprint"),
                          "preview_artifact_id": None, "download": None})
        files = manifest["files"]
        header = {"content_hash": version["content_hash"], "files": len(files),
                  "bytes": sum(int(f["size_bytes"]) for f in files),
                  "rows": sum(f.get("rows") or 0 for f in files) if all(f.get("rows") is not None for f in files) else None,
                  "rows_complete": bool(manifest.get("rows_complete")), "partial": bool(manifest.get("partial"))}
        next_cursor = base64.urlsafe_b64encode(page[-1]["relpath"].encode()).decode() if len(page) == limit else None
        return _json(200, {"ref": version["ref"], "manifest": header, "items": items, "next_cursor": next_cursor})

    def _shared_row(self, aid: str, f: dict) -> None:
        """A hosted blob as the base fake's download batch reads it."""
        rows = self.base.artifacts.setdefault("shared:", [])
        if not any(r["id"] == aid for r in rows):
            rows.append({"id": aid, "name": f".probe/datasets/{f['content_hash']}", "status": "complete",
                         "is_reference": False, "content_hash": f["content_hash"]})
            self.base.blobs[aid] = self.hosted_bytes.get(f["content_hash"], b"")
