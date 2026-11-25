"""Cloud objects a run reads and writes (GCS, S3, gcsfs, s3fs), told to the recorder as object observations.

The read recorder sees files on this machine; a job that reads its inputs from
``gs://`` and publishes results there left nothing to link (grades-back-to-jobs
E4/E8). These hooks record each object a library call moved, as the contract's
OBJECT OBSERVATION: the URI (``gs://<bucket>/<key>``, ``s3://<bucket>/<key>``),
the storage endpoint (``storage.googleapis.com``, ``s3.amazonaws.com``, or an
emulator / MinIO / R2 ``host[:port]``, plus ``@<machine>`` when it is loopback) and ``obj1:<identity>`` -- the GCS
generation, else the S3 ``VersionId`` (versioned bucket) or ``ETag``. The
server links a read to the run that wrote that exact (uri, host, identity).

Every hook records AFTER the call succeeded, from that call's own response: no
extra request, no download, no hashing. A response without an identity records
nothing (no link beats a wrong link). Hooked:

* botocore ``BaseClient._make_api_call`` and aiobotocore's (s3fs): the one call
  every S3 client, resource and transfer-manager path goes through, so a client
  made before ``probe.init()`` is seen too. ``GetObject`` is a read;
  ``PutObject``, ``CompleteMultipartUpload`` and ``CopyObject`` are writes.
  ``HeadObject`` (a size check) is not a read.
* google-cloud-storage's media layer (``Download.consume``,
  ``ChunkedDownload.consume_next_chunk``, ``*Upload.transmit``,
  ``ResumableUpload.transmit_next_chunk``): every ``Blob.download_*`` /
  ``upload_from_*`` and ``Blob.open`` goes through them, and each response says
  its generation (``x-goog-generation``, or the uploaded object's resource).
* gcsfs ``GCSFileSystem._request`` and ``_get_file_request``: its two HTTP calls.

A wrapper returns exactly what the library returned and lets through exactly
what it raised; a failure while recording is swallowed, with one warning per
process. INSTALLED LAZILY through `c_readers`' finder (`make_patches`): nothing here
imports a library. STDLIB ONLY: the same source runs in ``probe exec``'s child
hook (`child_site.CHILD_SITE_CODE`), where Probe may not be importable.
"""

from __future__ import annotations

import functools
import io
import json
import re
import socket
import sys
from urllib.parse import unquote, urlsplit

#: The fingerprint scheme of an object observation (the contract's).
OBJECT_PREFIX = "obj1:"
#: The server stores a fingerprint of at most this many characters.
MAX_FINGERPRINT_CHARS = 256
GCS_HOST = "storage.googleapis.com"
AWS_S3_HOST = "s3.amazonaws.com"
#: S3 operations that move an object's bytes: True for a read.
_S3_OPERATIONS = {
    "GetObject": True,
    "PutObject": False,
    "CompleteMultipartUpload": False,
    "CopyObject": False,
}
#: A GCS JSON-API object path: ``[/download]/storage/v1/b/<bucket>/o/<name>``.
_GCS_OBJECT_PATH = re.compile(r"(/download)?/storage/v1/b/([^/]+)/o/(.+)$")
_PRINTABLE = re.compile(r"[!-~]+")
#: An uploaded object's resource is a small JSON object; a larger body is not one.
_MAX_RESOURCE_BYTES = 1 << 20

#: library -> its coverage line ("hooked <lib>" / "unhooked <lib> <ver>"), in this process.
_STATUS: dict[str, str] = {}


def get_coverage_line() -> str | None:
    """``hooked <libs>; unhooked <lib> <ver>`` for what this process hooked, or None."""
    return join_coverage(_STATUS.values())


def join_coverage(lines) -> str | None:
    """Status lines (from any process of the run) as one coverage line, or None."""
    hooked = sorted({line[len("hooked ") :] for line in lines if line.startswith("hooked ")})
    unhooked = sorted({line for line in lines if line.startswith("unhooked ")})
    parts = (["hooked " + ", ".join(hooked)] if hooked else []) + unhooked
    return "; ".join(parts) or None


# -- what an observation is -------------------------------------------------------------


def make_uri(scheme: str, bucket, key) -> str | None:
    """The one URI normalizer: ``gs://`` (also for ``gcs://``) or ``s3://`` (also for
    ``s3a://``, ``s3n://``), the key byte-exact and never a query string."""
    scheme = {"gcs": "gs", "s3a": "s3", "s3n": "s3"}.get(scheme, scheme)
    if not (isinstance(bucket, str) and isinstance(key, str) and bucket and key):
        return None
    if "/" in bucket or ":" in bucket:  # an access-point ARN, not a bucket name
        return None
    return f"{scheme}://{bucket}/{key}"


def _get_netloc(url) -> str:
    """``host[:port]`` of a URL, lowercased, without credentials."""
    try:
        return urlsplit(str(url)).netloc.rpartition("@")[2].lower()
    except ValueError:
        return ""


def _is_loopback(name: str) -> bool:
    """A name only this machine answers on: ``localhost``, ``*.localhost``, 127/8, ``::1``,
    the unspecified addresses, and IPv4-mapped loopback. ``ipaddress`` is imported here, not
    at the top: most ``probe exec`` children never touch an object store."""
    import ipaddress

    name = name.removesuffix(".")
    if name == "localhost" or name.endswith(".localhost"):
        return True
    try:
        ip = ipaddress.ip_address(name)
    except ValueError:
        return False
    mapped = getattr(ip, "ipv4_mapped", None)
    return ip.is_loopback or ip.is_unspecified or bool(mapped and mapped.is_loopback)


@functools.lru_cache(maxsize=1)
def _get_machine_name() -> str:
    """This machine's name, capped so ``host:port@name`` stays under the server's 255 bytes."""
    try:
        name = socket.gethostname()
    except Exception:  # noqa: BLE001 - an audit hook or OSError must not drop the row
        name = ""
    return (name or "host").lower()[:200]


def get_endpoint_host(url, *, is_gcs: bool) -> str:
    """The contract's ``host``: any Google API host is GCS itself, any ``*.amazonaws.com``
    is AWS S3; another endpoint (an emulator, MinIO, R2) is its ``host[:port]``. A loopback
    endpoint names a server on THIS machine, so it carries the machine's name
    (``localhost:9000@<machine>``): two machines' local MinIOs are different stores."""
    netloc = _get_netloc(url)
    name = netloc.rsplit(":", 1)[0] if netloc.count(":") == 1 else netloc
    if is_gcs and (name == "googleapis.com" or name.endswith(".googleapis.com")):
        return GCS_HOST
    if not is_gcs and (name == "amazonaws.com" or name.endswith(".amazonaws.com")):
        return AWS_S3_HOST
    try:
        hostname = urlsplit(str(url)).hostname or ""
    except ValueError:
        hostname = ""
    if netloc and _is_loopback(hostname):
        return f"{netloc}@{_get_machine_name()}"
    return netloc


def make_fingerprint(identity) -> str | None:
    """``obj1:<identity>``, or None when there is no identity fit to match on."""
    if isinstance(identity, int) and not isinstance(identity, bool):
        identity = str(identity)
    if not isinstance(identity, str):
        return None
    identity = identity.strip('"')
    fingerprint = OBJECT_PREFIX + identity
    if (
        not identity
        or len(fingerprint) > MAX_FINGERPRINT_CHARS
        or not _PRINTABLE.fullmatch(identity)
    ):
        return None
    return fingerprint


#: The largest size the server stores (a signed 64-bit integer): a larger one, from a
#: buggy or hostile endpoint, would refuse the whole batch it is in.
_MAX_SIZE = (1 << 63) - 1


def _to_size(value) -> int | None:
    try:
        size = int(value)
    except (TypeError, ValueError):
        return None
    return size if 0 <= size <= _MAX_SIZE else None


def _get_body_size(body) -> int | None:
    """A PutObject body's size, read only from a type Python, botocore or s3transfer
    made: a caller's own class could run its code on ``len()`` or ``getbuffer()``
    after the upload (move its cursor, take a lock), so its size stays unknown."""
    kind = type(body)
    if kind is io.BytesIO and not body.closed:
        # botocore turns a bytes or str Body into a BytesIO of it, in place.
        with body.getbuffer() as view:
            return view.nbytes
    if kind is str:
        return len(body.encode("utf-8"))
    if kind in (bytes, bytearray):
        return len(body)
    if kind.__module__.startswith("s3transfer.") and hasattr(kind, "__len__"):
        return _to_size(len(body))  # s3transfer's ReadFileChunk: its part's length
    return None


def _get_range_total(content_range) -> int | None:
    """The object's whole size from ``Content-Range: bytes a-b/total``."""
    if isinstance(content_range, str) and "/" in content_range:
        return _to_size(content_range.rsplit("/", 1)[1])
    return None


def build_s3_observation(client, operation: str, parameters, result) -> tuple | None:
    """(reading, uri, host, fingerprint, size) for one successful S3 call, or None."""
    reading = _S3_OPERATIONS.get(operation)
    if reading is None or not isinstance(parameters, dict) or not isinstance(result, dict):
        return None
    meta = client.meta
    if meta.service_model.service_name != "s3":
        return None
    uri = make_uri("s3", parameters.get("Bucket"), parameters.get("Key"))
    if uri is None:
        return None
    etag = result.get("ETag")
    if operation == "CopyObject":
        etag = (result.get("CopyObjectResult") or {}).get("ETag")
    version = result.get("VersionId")
    # "null" is the version of an object written while versioning was off or suspended.
    fingerprint = make_fingerprint(version if version and version != "null" else etag)
    if fingerprint is None:
        return None
    size = None
    if operation == "GetObject":
        size = _get_range_total(result.get("ContentRange"))
        if size is None and "Range" not in parameters and "PartNumber" not in parameters:
            size = _to_size(result.get("ContentLength"))
    elif operation == "PutObject":
        size = _to_size(parameters.get("ContentLength"))
        if size is None:
            size = _get_body_size(parameters.get("Body"))
    return reading, uri, get_endpoint_host(meta.endpoint_url, is_gcs=False), fingerprint, size


def build_gcs_observation(method, url, status, headers, body=None) -> tuple | None:
    """(reading, uri, host, fingerprint, size) for one GCS JSON-API response, or None:
    a media GET is a read (its ``x-goog-generation``); a finished upload's response is
    the written object's resource. ``body()`` gives an upload's response body."""
    method = str(method).upper()
    url = str(url)
    if method == "GET":
        if status not in (200, 206):
            return None
        parts = urlsplit(url)
        match = _GCS_OBJECT_PATH.search(parts.path)
        if match is None or (match.group(1) is None and "alt=media" not in parts.query):
            return None  # an object's metadata, not its bytes
        uri = make_uri("gs", unquote(match.group(2)), unquote(match.group(3)))
        fingerprint = make_fingerprint(_get_generation(headers.get("x-goog-generation")))
        if uri is None or fingerprint is None:
            return None
        size = _to_size(headers.get("x-goog-stored-content-length"))
        if size is None:
            size = _get_range_total(headers.get("content-range"))
        if size is None and status == 200 and not headers.get("content-encoding"):
            size = _to_size(headers.get("content-length"))
        return True, uri, get_endpoint_host(url, is_gcs=True), fingerprint, size
    parts = urlsplit(url)
    if method not in ("POST", "PUT") or status != 200 or "/upload/storage/" not in parts.path:
        return None
    if "uploadType=resumable" in parts.query and "upload_id=" not in parts.query:
        return None  # opens an upload session; its last chunk's response is the object
    resource = body() if body is not None else None
    if isinstance(resource, (bytes, bytearray)):
        if len(resource) > _MAX_RESOURCE_BYTES or not resource.lstrip().startswith(b"{"):
            return None
        resource = json.loads(resource)
    if not isinstance(resource, dict) or resource.get("kind") != "storage#object":
        return None
    uri = make_uri("gs", resource.get("bucket"), resource.get("name"))
    fingerprint = make_fingerprint(_get_generation(resource.get("generation")))
    if uri is None or fingerprint is None:
        return None
    return (
        False,
        uri,
        get_endpoint_host(url, is_gcs=True),
        fingerprint,
        _to_size(resource.get("size")),
    )


def _get_generation(value) -> str | None:
    """A GCS generation: a positive integer (as text), else None."""
    text = str(value) if isinstance(value, (str, int)) and not isinstance(value, bool) else ""
    return text if text.isdigit() and int(text) > 0 else None


def _make_json_reader(response):
    """A ``requests`` upload response's body: the object resource."""
    return lambda: response.json()


# -- the hooks ---------------------------------------------------------------------------


def _get_caller():
    """The frame that called a wrapper (two up from here), or None: no Python frame
    called it, or an audit hook refused the lookup. Never raises into the call."""
    try:
        return sys._getframe(2)
    except Exception:  # noqa: BLE001 -- recording never breaks the caller
        return None


class _Hooks:
    """One recorder's object hooks. ``note_object(reading, uri, host, fingerprint, size,
    frame)`` is the recorder's; ``active()`` whether anything records now; ``warn(msg)``
    says, once per process, that recording failed; ``report(line)`` hears each
    library's coverage line (the child hook spools them)."""

    def __init__(self, note_object, active, warn, report) -> None:
        self.note_object = note_object
        self.active = active
        self.warn = warn
        self.report = report
        self.token = object()
        self.has_warned = False

    def observe(self, observe, args, kwargs, result, frame) -> None:
        try:
            if not self.active():
                return
            observation = observe(args, kwargs, result)
            if observation is not None:
                self.note_object(*observation, frame)
        except Exception as exc:  # noqa: BLE001 -- recording never breaks the caller
            if not self.has_warned:
                self.has_warned = True
                try:
                    self.warn(f"probe: an object read or write was not recorded: {exc!r}")
                except Exception:  # noqa: BLE001
                    pass

    def wrap(self, original, observe):
        """``original``'s wrapper: the call first, then ``observe(args, kwargs, result)``."""
        # Here, not at the top: every `probe exec` child runs this file, and most hook nothing.
        import inspect

        hooks = self
        if inspect.iscoroutinefunction(original):

            @functools.wraps(original)
            async def run_wrapped(*args, **kwargs):
                frame = _get_caller()
                result = await original(*args, **kwargs)
                hooks.observe(observe, args, kwargs, result, frame)
                return result

        else:

            @functools.wraps(original)
            def run_wrapped(*args, **kwargs):
                frame = _get_caller()
                result = original(*args, **kwargs)
                hooks.observe(observe, args, kwargs, result, frame)
                return result

        run_wrapped.__probe_object_hook__ = self.token
        return run_wrapped

    def wrap_methods(self, lib: str, module, targets) -> None:
        """Wrap each ``(class name, method, observe)`` of ``module``; one that is
        missing leaves the library ``unhooked`` (a renamed method records nothing)."""
        is_hooked = True
        for cls_name, method, observe in targets:
            cls = getattr(module, cls_name, None)
            original = getattr(cls, method, None) if isinstance(cls, type) else None
            if not callable(original):
                is_hooked = False
                continue
            if getattr(original, "__probe_object_hook__", None) is self.token:
                continue  # inherited from a class already wrapped
            try:
                setattr(cls, method, self.wrap(original, observe))
            except (AttributeError, TypeError):
                is_hooked = False
        self.set_status(lib, is_hooked)

    def set_status(self, lib: str, is_hooked: bool) -> None:
        line = f"hooked {lib}"
        if not is_hooked or _STATUS.get(lib, line) != line:
            line = f"unhooked {lib} {_get_version(lib)}"
        if _STATUS.get(lib) == line:
            return
        _STATUS[lib] = line
        if self.report is not None:
            try:
                self.report(line)
            except Exception:  # noqa: BLE001
                pass

    # -- per library -----------------------------------------------------------------

    def patch_botocore(self, module) -> None:
        def call(args, kwargs, result):
            # (self, operation_name, api_params)
            return build_s3_observation(args[0], args[1], args[2], result)

        self.wrap_methods("botocore", module, (("BaseClient", "_make_api_call", call),))

    def patch_aiobotocore(self, module) -> None:
        def call(args, kwargs, result):
            return build_s3_observation(args[0], args[1], args[2], result)

        self.wrap_methods("aiobotocore", module, (("AioBaseClient", "_make_api_call", call),))

    def make_download_patch(self, lib: str):
        def download(args, kwargs, result):
            # (self, transport, ...) -> the response; `media_url` is what it fetched.
            return build_gcs_observation(
                "GET", args[0].media_url, result.status_code, result.headers
            )

        def patch(module) -> None:
            self.wrap_methods(
                lib,
                module,
                (
                    ("Download", "consume", download),
                    ("RawDownload", "consume", download),
                    ("ChunkedDownload", "consume_next_chunk", download),
                    ("RawChunkedDownload", "consume_next_chunk", download),
                ),
            )

        return patch

    def make_upload_patch(self, lib: str):
        def upload(args, kwargs, result):
            # (self, transport, ...) -> the response; only a finished upload is 200. A
            # resumable upload's chunks go to its session URL (`resumable_url`).
            media = args[0]
            url = getattr(media, "resumable_url", None) or media.upload_url
            return build_gcs_observation(
                "PUT", url, result.status_code, result.headers, _make_json_reader(result)
            )

        def patch(module) -> None:
            self.wrap_methods(
                lib,
                module,
                (
                    ("SimpleUpload", "transmit", upload),
                    ("MultipartUpload", "transmit", upload),
                    ("ResumableUpload", "transmit_next_chunk", upload),
                ),
            )

        return patch

    def patch_gcsfs(self, module) -> None:
        def request(args, kwargs, result):
            # _request(self, method, path, ...) -> (status, headers, request_info, contents)
            status, headers, info, contents = result
            method = args[1] if len(args) > 1 else kwargs.get("method")
            return build_gcs_observation(method, info.url, status, headers, lambda: contents)

        def get_file(args, kwargs, result):
            # _get_file_request(self, rpath, lpath, ...) -> (status, headers, request_info, data)
            status, headers, info, _ = result
            return build_gcs_observation("GET", info.url, status, headers)

        self.wrap_methods(
            "gcsfs",
            module,
            (
                ("GCSFileSystem", "_request", request),
                ("GCSFileSystem", "_get_file_request", get_file),
            ),
        )

    def get_patches(self) -> dict:
        """module name -> what to patch once it is imported."""
        return {
            "botocore.client": self.patch_botocore,
            "aiobotocore.client": self.patch_aiobotocore,
            "google.cloud.storage._media.requests.download": self.make_download_patch(
                "google-cloud-storage"
            ),
            "google.cloud.storage._media.requests.upload": self.make_upload_patch(
                "google-cloud-storage"
            ),
            # google-cloud-storage before 3.0 moves its bytes through google-resumable-media.
            "google.resumable_media.requests.download": self.make_download_patch(
                "google-resumable-media"
            ),
            "google.resumable_media.requests.upload": self.make_upload_patch(
                "google-resumable-media"
            ),
            "gcsfs.core": self.patch_gcsfs,
        }


def _get_version(lib: str) -> str:
    try:
        from importlib.metadata import version

        return version(lib)
    except Exception:  # noqa: BLE001
        return "?"


def _write_stderr(message: str) -> None:
    sys.stderr.write(message + "\n")


def make_patches(note_object, active=lambda: True, warn=_write_stderr, report=None) -> dict:
    """The object hooks for one recorder, as `c_readers.install`'s ``extra`` patches
    (module name -> patch). See `_Hooks` for the callbacks."""
    return _Hooks(note_object, active, warn, report).get_patches()
