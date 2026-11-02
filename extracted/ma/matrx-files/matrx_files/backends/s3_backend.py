"""S3 storage backend.

Auto-configures from environment variables (or a matrx_utils settings object):

    AWS_ACCESS_KEY_ID       — optional static credential
    AWS_SECRET_ACCESS_KEY   — optional static credential
    AWS_REGION              — optional, defaults to "us-east-1"
    AWS_S3_DEFAULT_BUCKET   — optional default bucket when none is supplied in
                              the URI (s3://path/key vs s3://bucket/path/key)
    AWS_S3_OBJECT_ACL       — optional. If unset or empty, **no** ``ACL`` is sent
                              on upload (required for Object Ownership *Bucket
                              owner enforced* / ACLs disabled). Set to e.g.
                              ``private`` or ``public-read`` only for legacy
                              buckets that still use object ACLs.

Path convention expected by this backend:
    "bucket-name/path/to/object.ext"

If AWS_S3_DEFAULT_BUCKET is set you may omit the bucket segment:
    "path/to/object.ext"  →  "{default_bucket}/path/to/object.ext"
"""

from __future__ import annotations

import io
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .base_backend import ObjectInfo, StorageBackend
from ..content_headers import ObjectHeaders, resolve_object_headers

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.type_defs import CompletedPartTypeDef

    from ..ephemeral_objects import EphemeralObjectPolicy


_MULTIPART_THRESHOLD: int = 8 * 1024 * 1024  # 8 MB


class S3Backend(StorageBackend):
    def __init__(self) -> None:
        self._client: S3Client | None = None
        self._default_bucket: str = ""
        self._region: str = "us-east-1"
        self._configured: bool = False
        self._init_from_settings()

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def _init_from_settings(self) -> None:
        try:
            from matrx_utils.conf import settings

            self._region = self._safe_get(settings, "AWS_REGION") or "us-east-1"
            self._default_bucket = self._safe_get(settings, "AWS_S3_DEFAULT_BUCKET") or ""
            # boto3's default provider chain supplies ECS task-role,
            # web-identity, shared-profile, and instance-role credentials.
            # Actual access is proved by assert_bucket_accessible().
            self._configured = bool(self._default_bucket)
        except Exception:
            return

    @staticmethod
    def _safe_get(settings_obj: object, name: str) -> str:
        try:
            val: object = getattr(settings_obj, name, None)
            return val if isinstance(val, str) and val.strip() else ""
        except Exception:
            return ""

    def _resolve_write_acl(self, acl: str | None) -> str | None:
        """Canned ACL for PutObject, or None to omit (modern private buckets).

        When *acl* is ``None``, the default comes from ``AWS_S3_OBJECT_ACL``;
        if that is also unset/empty, returns ``None`` so boto3 does not send an
        ``ACL`` key (required when the bucket has ACLs disabled).
        """
        if acl is not None:
            return acl.strip() if acl.strip() else None
        from matrx_utils.conf import settings

        v = self._safe_get(settings, "AWS_S3_OBJECT_ACL")
        return v.strip() if v.strip() else None

    def _get_client(self) -> S3Client:
        """Return the boto3 S3 client, creating it on first call."""
        if self._client is None:
            import boto3
            from matrx_utils.conf import settings

            key_id = self._safe_get(settings, "AWS_ACCESS_KEY_ID")
            secret = self._safe_get(settings, "AWS_SECRET_ACCESS_KEY")
            client_kwargs: dict[str, str] = {"region_name": self._region}
            if key_id and secret:
                client_kwargs.update(
                    aws_access_key_id=key_id,
                    aws_secret_access_key=secret,
                )
            self._client = boto3.client("s3", **client_kwargs)  # type: ignore[assignment]
        return self._client  # type: ignore[return-value]

    def is_configured(self) -> bool:
        return self._configured

    def assert_bucket_accessible(self, bucket: str | None = None) -> None:
        """Fail loudly unless credentials can access the configured bucket."""

        target = (bucket or self._default_bucket).strip()
        if not target:
            raise RuntimeError("AWS_S3_DEFAULT_BUCKET is not configured")
        self._get_client().head_bucket(Bucket=target)

    async def assert_bucket_accessible_async(self, bucket: str | None = None) -> None:
        import asyncio

        await asyncio.to_thread(self.assert_bucket_accessible, bucket)

    # ------------------------------------------------------------------
    # Path helpers
    # ------------------------------------------------------------------

    def _parse_path(self, path: str) -> tuple[str, str]:
        """Split 'bucket/key/path' → ('bucket', 'key/path').

        If the path does not contain a '/' the entire string is treated as
        the key and the default bucket is used.
        """
        if "/" in path:
            bucket, _, key = path.partition("/")
            if not key:
                raise ValueError(f"S3 path '{path}' has no key component after the bucket.")
            return bucket, key
        if self._default_bucket:
            return self._default_bucket, path
        raise ValueError(
            f"Cannot resolve S3 path '{path}': no bucket specified and "
            "AWS_S3_DEFAULT_BUCKET is not set."
        )

    # ------------------------------------------------------------------
    # Core CRUD
    # ------------------------------------------------------------------

    def read(self, path: str) -> bytes:
        self._require_configured()
        bucket, key = self._parse_path(path)
        response: Any = self._get_client().get_object(Bucket=bucket, Key=key)
        body: bytes = response["Body"].read()
        return body

    def write(
        self,
        path: str,
        content: bytes | str,
        acl: str | None = None,
        content_type: str | None = None,
    ) -> bool:
        return self._write_object(
            path,
            content,
            acl=acl,
            content_type=content_type,
            tagging=None,
        )

    def write_ephemeral(
        self,
        path: str,
        content: bytes | str,
        *,
        policy: EphemeralObjectPolicy,
        content_type: str | None = None,
    ) -> bool:
        """Write scratch bytes with the policy tag in the same S3 request.

        The supplied policy is the complete managed tag set. Rewriting an
        existing key therefore replaces an obsolete lifecycle classification
        instead of merging it and accidentally matching multiple expiry rules.
        """
        from ..ephemeral_objects import require_registered_ephemeral_object_policy

        require_registered_ephemeral_object_policy(policy)
        return self._write_object(
            path,
            content,
            acl=None,
            content_type=content_type,
            tagging=policy.s3_tagging_query,
        )

    def _write_object(
        self,
        path: str,
        content: bytes | str,
        *,
        acl: str | None,
        content_type: str | None,
        tagging: str | None,
    ) -> bool:
        self._require_configured()
        bucket, key = self._parse_path(path)
        client: S3Client = self._get_client()

        raw: bytes = content.encode() if isinstance(content, str) else content
        eff_acl = self._resolve_write_acl(acl)
        # SSOT: stamp Content-Type + Content-Disposition onto the object so a
        # bare public CDN URL renders correctly. The key is often extensionless
        # (canonical <owner>/<file_id>), so the caller's content_type is the
        # authoritative source; the key-extension guess is only the fallback.
        headers = resolve_object_headers(mime_type=content_type, file_name=key)

        if len(raw) >= _MULTIPART_THRESHOLD:
            self._multipart_upload(
                client,
                bucket,
                key,
                raw,
                eff_acl,
                headers,
                tagging=tagging,
            )
        else:
            put_kw: dict[str, Any] = {
                "Bucket": bucket,
                "Key": key,
                "Body": raw,
                "ContentType": headers.content_type,
                "ContentDisposition": headers.content_disposition,
            }
            if eff_acl:
                put_kw["ACL"] = eff_acl
            if tagging:
                put_kw["Tagging"] = tagging
            client.put_object(**put_kw)  # type: ignore[arg-type]
        return True

    def _multipart_upload(
        self,
        client: S3Client,
        bucket: str,
        key: str,
        content: bytes,
        acl: str | None,
        headers: ObjectHeaders | None = None,
        *,
        tagging: str | None = None,
    ) -> None:
        if headers is None:
            headers = resolve_object_headers(mime_type=None, file_name=key)
        mpu_kw: dict[str, Any] = {
            "Bucket": bucket,
            "Key": key,
            "ContentType": headers.content_type,
            "ContentDisposition": headers.content_disposition,
        }
        if acl:
            mpu_kw["ACL"] = acl
        if tagging:
            mpu_kw["Tagging"] = tagging
        mpu: Any = client.create_multipart_upload(**mpu_kw)  # type: ignore[arg-type]
        upload_id: str = mpu["UploadId"]
        parts: list[CompletedPartTypeDef] = []
        chunk_size: int = _MULTIPART_THRESHOLD
        try:
            for i, offset in enumerate(range(0, len(content), chunk_size), start=1):
                chunk: bytes = content[offset : offset + chunk_size]
                part: Any = client.upload_part(
                    Bucket=bucket,
                    Key=key,
                    PartNumber=i,
                    UploadId=upload_id,
                    Body=chunk,
                )
                parts.append({"PartNumber": i, "ETag": part["ETag"]})
            client.complete_multipart_upload(
                Bucket=bucket,
                Key=key,
                UploadId=upload_id,
                MultipartUpload={"Parts": parts},
            )
        except Exception:
            client.abort_multipart_upload(Bucket=bucket, Key=key, UploadId=upload_id)
            raise

    def append(self, path: str, content: bytes | str) -> bool:
        self._require_configured()
        try:
            existing: bytes = self.read(path)
        except Exception:
            existing = b""

        raw: bytes = content.encode() if isinstance(content, str) else content
        return self.write(path, existing + raw)

    def delete(self, path: str) -> bool:
        self._require_configured()
        bucket, key = self._parse_path(path)
        self._get_client().delete_object(Bucket=bucket, Key=key)
        return True

    def delete_many(self, paths: list[str]) -> tuple[int, list[tuple[str, str]]]:
        """Batch-delete via S3 DeleteObjects (1000 keys per call, the API max).

        Returns ``(deleted_count, [(path, error), ...])`` where each error path is
        **the path this method was GIVEN** — same contract as the base
        implementation, so a caller can match errors against its own input. (An
        earlier version returned a re-derived ``s3://…`` URI, which silently
        disagreed with the base class and broke callers' error accounting.)

        Bulk cleanup one key at a time is thousands of round-trips — a 13k-object
        reclaim goes from ~40 min to seconds. NOTHING raises: a bad path or a
        failed chunk is reported per-key, because a destructive bulk job that dies
        partway with no accounting of what it already deleted is worse than useless.
        """
        self._require_configured()
        client: S3Client = self._get_client()

        by_bucket: dict[str, list[tuple[str, str]]] = {}  # bucket -> [(key, original)]
        errors: list[tuple[str, str]] = []
        for p in paths:
            try:
                bucket, key = self._parse_path(p)
            except Exception as e:  # noqa: BLE001 — a malformed path must not abort the batch
                errors.append((p, f"unparseable path: {e}"))
                continue
            by_bucket.setdefault(bucket, []).append((key, p))

        deleted = 0
        for bucket, entries in by_bucket.items():
            for i in range(0, len(entries), 1000):  # DeleteObjects hard-caps at 1000
                chunk = entries[i : i + 1000]
                by_key = {k: orig for k, orig in chunk}
                try:
                    resp = client.delete_objects(
                        Bucket=bucket,
                        Delete={"Objects": [{"Key": k} for k, _ in chunk], "Quiet": True},
                    )
                except Exception as e:  # noqa: BLE001 — throttle/5xx must not lose the count
                    errors.extend((orig, str(e)) for _, orig in chunk)
                    continue
                failed = resp.get("Errors", []) or []
                deleted += len(chunk) - len(failed)
                for err in failed:
                    key = err.get("Key") or ""
                    errors.append((by_key.get(key, key), err.get("Message", "unknown")))
        return deleted, errors

    async def delete_many_async(self, paths: list[str]) -> tuple[int, list[tuple[str, str]]]:
        import asyncio

        return await asyncio.get_event_loop().run_in_executor(None, self.delete_many, paths)

    # ------------------------------------------------------------------
    # URL generation
    # ------------------------------------------------------------------

    def get_url(
        self,
        path: str,
        expires_in: int = 3600,
        *,
        response_content_disposition: str | None = None,
        response_content_type: str | None = None,
    ) -> str:
        """Return a presigned GET URL for *path*.

        When ``response_content_disposition`` or ``response_content_type`` is
        provided, S3 echoes the value back in the response headers without
        any re-upload. This is how the platform mints two distinct URLs
        for the same object — one with ``inline`` (browser renders it)
        and one with ``attachment`` (browser downloads it).
        """
        self._require_configured()
        bucket, key = self._parse_path(path)
        params: dict[str, Any] = {"Bucket": bucket, "Key": key}
        if response_content_disposition:
            params["ResponseContentDisposition"] = response_content_disposition
        if response_content_type:
            params["ResponseContentType"] = response_content_type
        url: str = self._get_client().generate_presigned_url(
            "get_object",
            Params=params,
            ExpiresIn=expires_in,
        )
        return url

    def make_public_url(self, path: str) -> str:
        """Return the permanent public URL (only works for public-read objects)."""
        bucket, key = self._parse_path(path)
        return f"https://{bucket}.s3.{self._region}.amazonaws.com/{key}"

    def get_presigned_put_url(
        self,
        path: str,
        *,
        expires_in: int = 900,
        content_type: str | None = None,
        max_size_bytes: int | None = None,
    ) -> dict[str, Any]:
        """Return a presigned PUT URL the browser can upload to directly.

        Returns ``{"url": "...", "headers": {"Content-Type": "...", ...}}``.

        Use cases:
            - Files larger than the FastAPI worker can buffer (>100 MB).
            - Direct browser → S3 to skip the API host's bandwidth.

        After the browser PUTs successfully, it must call back to the
        backend with the path so we can register the metadata in cld_files.
        """
        self._require_configured()
        bucket, key = self._parse_path(path)
        params: dict[str, Any] = {"Bucket": bucket, "Key": key}
        if content_type:
            params["ContentType"] = content_type
        url: str = self._get_client().generate_presigned_url(
            "put_object",
            Params=params,
            ExpiresIn=expires_in,
        )
        headers: dict[str, str] = {}
        if content_type:
            headers["Content-Type"] = content_type
        return {
            "url": url,
            "headers": headers,
            "expires_in": expires_in,
            "max_size_bytes": max_size_bytes,
        }

    def get_presigned_post(
        self,
        path: str,
        *,
        expires_in: int = 900,
        content_type: str | None = None,
        max_size_bytes: int | None = None,
    ) -> dict[str, Any]:
        """Return a presigned POST policy for browser form-based uploads.

        More flexible than presigned PUT — supports per-field policy
        constraints (size cap, content-type prefix, etc.). The browser
        builds a multipart/form-data POST against ``url`` with the returned
        ``fields`` plus the file as the ``file`` field.
        """
        self._require_configured()
        bucket, key = self._parse_path(path)
        conditions: list = []
        fields: dict[str, str] = {}
        if content_type:
            conditions.append(["starts-with", "$Content-Type", content_type.split("/")[0] + "/"])
            fields["Content-Type"] = content_type
        if max_size_bytes is not None:
            conditions.append(["content-length-range", 0, int(max_size_bytes)])
        post: dict[str, Any] = self._get_client().generate_presigned_post(
            Bucket=bucket,
            Key=key,
            Fields=fields if fields else None,
            Conditions=conditions if conditions else None,
            ExpiresIn=expires_in,
        )
        # Returns {"url": "...", "fields": {...}}
        return {**post, "expires_in": expires_in, "max_size_bytes": max_size_bytes}

    # ------------------------------------------------------------------
    # Listing
    # ------------------------------------------------------------------

    def _split_list_prefix(self, prefix: str) -> tuple[str, str]:
        if "/" in prefix:
            bucket, _, key_prefix = prefix.partition("/")
            return bucket, key_prefix
        if self._default_bucket:
            return self._default_bucket, prefix
        raise ValueError(
            f"Cannot list S3 files for prefix '{prefix}': "
            "no bucket specified and AWS_S3_DEFAULT_BUCKET is not set."
        )

    def list_files(self, prefix: str = "") -> list[str]:
        return [o.path for o in self.list_objects(prefix)]

    def list_objects(self, prefix: str = "") -> list[ObjectInfo]:
        """Paginated listing carrying Size + LastModified + ETag.

        LastModified is what makes a destructive reconcile safe: the write
        path PUTs bytes before the DB row lands, so a young unreferenced
        object is an in-flight upload, not an orphan.
        """
        self._require_configured()
        client: S3Client = self._get_client()
        bucket, key_prefix = self._split_list_prefix(prefix)

        paginator: Any = client.get_paginator("list_objects_v2")
        results: list[ObjectInfo] = []
        for page in paginator.paginate(Bucket=bucket, Prefix=key_prefix):
            for obj in page.get("Contents", []):
                results.append(
                    ObjectInfo(
                        path=f"{bucket}/{obj['Key']}",
                        size=obj.get("Size"),
                        last_modified=obj.get("LastModified"),
                        etag=(obj.get("ETag") or "").strip('"') or None,
                    )
                )
        return results

    # ------------------------------------------------------------------
    # Copy / move helpers (convenience, not in ABC)
    # ------------------------------------------------------------------

    def copy(self, src_path: str, dst_path: str) -> bool:
        """Server-side copy within S3 — no data transfer to/from client."""
        self._require_configured()
        src_bucket, src_key = self._parse_path(src_path)
        dst_bucket, dst_key = self._parse_path(dst_path)
        self._get_client().copy_object(
            CopySource={"Bucket": src_bucket, "Key": src_key},
            Bucket=dst_bucket,
            Key=dst_key,
        )
        return True

    def restamp_headers(
        self,
        path: str,
        *,
        content_type: str,
        content_disposition: str,
    ) -> bool:
        """Rewrite an existing object's Content-Type / Content-Disposition.

        Server-side ``CopyObject`` onto itself with ``MetadataDirective=REPLACE``
        — no bytes are transferred. Used by the header re-stamp backfill to heal
        objects written before the write path stamped these headers. Idempotent:
        re-running with the same headers is a no-op write.
        """
        self._require_configured()
        bucket, key = self._parse_path(path)
        copy_kw: dict[str, Any] = {
            "Bucket": bucket,
            "Key": key,
            "CopySource": {"Bucket": bucket, "Key": key},
            "MetadataDirective": "REPLACE",
            "ContentType": content_type,
            "ContentDisposition": content_disposition,
        }
        eff_acl = self._resolve_write_acl(None)
        if eff_acl:
            copy_kw["ACL"] = eff_acl
        self._get_client().copy_object(**copy_kw)  # type: ignore[arg-type]
        return True

    def get_metadata(self, path: str) -> dict[str, Any]:
        """Return object metadata (content-type, size, last-modified, etc.)."""
        self._require_configured()
        bucket, key = self._parse_path(path)
        response: Any = self._get_client().head_object(Bucket=bucket, Key=key)
        return {
            "content_type": response.get("ContentType", ""),
            "size": response.get("ContentLength", 0),
            "last_modified": str(response.get("LastModified", "")),
            "etag": response.get("ETag", "").strip('"'),
            "metadata": response.get("Metadata", {}),
        }

    def upload_file(
        self,
        local_path: str,
        s3_path: str,
        acl: str | None = None,
        content_type: str | None = None,
    ) -> bool:
        """Upload a local file to S3 using streaming (memory-efficient)."""
        self._require_configured()
        bucket, key = self._parse_path(s3_path)
        eff = self._resolve_write_acl(acl)
        headers = resolve_object_headers(mime_type=content_type, file_name=local_path or key)
        extra: dict[str, str] = {
            "ContentType": headers.content_type,
            "ContentDisposition": headers.content_disposition,
        }
        if eff:
            extra["ACL"] = eff
        self._get_client().upload_file(local_path, bucket, key, ExtraArgs=extra)
        return True

    def download_file(self, s3_path: str, local_path: str) -> bool:
        """Download an S3 object to a local file path."""
        self._require_configured()
        bucket, key = self._parse_path(s3_path)
        self._get_client().download_file(bucket, key, local_path)
        return True

    def download_to_path(self, path: str, local_path: str) -> int:
        """Stream an S3 object to disk without buffering it in Python memory."""
        self._require_configured()
        bucket, key = self._parse_path(path)
        client = self._get_client()
        client.download_file(bucket, key, local_path)
        return Path(local_path).stat().st_size

    def upload_fileobj(
        self,
        file_obj: io.IOBase,
        s3_path: str,
        acl: str | None = None,
        content_type: str | None = None,
    ) -> bool:
        """Upload a file-like object to S3."""
        self._require_configured()
        bucket, key = self._parse_path(s3_path)
        eff = self._resolve_write_acl(acl)
        headers = resolve_object_headers(mime_type=content_type, file_name=key)
        extra: dict[str, str] = {
            "ContentType": headers.content_type,
            "ContentDisposition": headers.content_disposition,
        }
        if eff:
            extra["ACL"] = eff
        self._get_client().upload_fileobj(file_obj, bucket, key, ExtraArgs=extra)
        return True

    # ------------------------------------------------------------------
    # Asynchronous API
    # ------------------------------------------------------------------
    # boto3 is synchronous and aioboto3 cannot be pinned alongside our
    # boto3 version. The correct non-blocking pattern for boto3 in async
    # applications is to run sync calls in a thread-pool executor — the
    # event loop is never blocked; I/O waits happen in worker threads.

    async def read_async(self, path: str) -> bytes:
        import asyncio

        return await asyncio.get_event_loop().run_in_executor(None, self.read, path)

    async def download_to_path_async(self, path: str, local_path: str) -> int:
        import asyncio

        fn = partial(self.download_to_path, path, local_path)
        return await asyncio.get_running_loop().run_in_executor(None, fn)

    async def write_async(
        self,
        path: str,
        content: bytes | str,
        acl: str | None = None,
        content_type: str | None = None,
    ) -> bool:
        import asyncio

        fn = partial(self.write, path, content, acl, content_type)
        return await asyncio.get_event_loop().run_in_executor(None, fn)

    async def write_ephemeral_async(
        self,
        path: str,
        content: bytes | str,
        *,
        policy: EphemeralObjectPolicy,
        content_type: str | None = None,
    ) -> bool:
        import asyncio

        fn = partial(
            self.write_ephemeral,
            path,
            content,
            policy=policy,
            content_type=content_type,
        )
        return await asyncio.get_running_loop().run_in_executor(None, fn)

    async def append_async(self, path: str, content: bytes | str) -> bool:
        import asyncio

        return await asyncio.get_event_loop().run_in_executor(None, self.append, path, content)

    async def delete_async(self, path: str) -> bool:
        import asyncio

        return await asyncio.get_event_loop().run_in_executor(None, self.delete, path)

    async def get_url_async(
        self,
        path: str,
        expires_in: int = 3600,
        *,
        response_content_disposition: str | None = None,
        response_content_type: str | None = None,
    ) -> str:
        import asyncio

        fn = partial(
            self.get_url,
            path,
            expires_in,
            response_content_disposition=response_content_disposition,
            response_content_type=response_content_type,
        )
        return await asyncio.get_event_loop().run_in_executor(None, fn)

    async def list_files_async(self, prefix: str = "") -> list[str]:
        import asyncio

        return await asyncio.get_event_loop().run_in_executor(None, self.list_files, prefix)

    async def list_objects_async(self, prefix: str = "") -> list[ObjectInfo]:
        import asyncio

        return await asyncio.get_event_loop().run_in_executor(None, self.list_objects, prefix)

    async def copy_async(self, src_path: str, dst_path: str) -> bool:
        import asyncio

        return await asyncio.get_event_loop().run_in_executor(None, self.copy, src_path, dst_path)

    async def restamp_headers_async(
        self,
        path: str,
        *,
        content_type: str,
        content_disposition: str,
    ) -> bool:
        import asyncio

        fn = partial(
            self.restamp_headers,
            path,
            content_type=content_type,
            content_disposition=content_disposition,
        )
        return await asyncio.get_event_loop().run_in_executor(None, fn)

    async def get_metadata_async(self, path: str) -> dict[str, Any]:
        import asyncio

        return await asyncio.get_event_loop().run_in_executor(None, self.get_metadata, path)
