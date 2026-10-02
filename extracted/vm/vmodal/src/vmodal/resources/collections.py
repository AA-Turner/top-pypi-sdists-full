from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
import os,sys
import asyncio
import random
import uuid
from pathlib import Path
import mimetypes
import fire
from pydantic import ValidationError
from vmodal.errors import ApiError, FeatureDisabled, ValidationFailed
from vmodal.models import (
    GroupsResponse,
    ExternalUploadSignedUrlResponse,
    MultipartCreateResponse,
    MultipartSignResponse,
    MultipartStatusResponse,
    MultipartCompleteResponse,
    VideoUploadResponse,
    VideoUploadBulkResponse,
    FolderUploadResponse,
    GoogleDriveFolderUploadResponse,
    MetadataParquetUploadResponse,
    CollectionDescriptionUpdateResponse,
    DeleteCollectionRequest,
    DeleteCollectionResponse,
    CollectionAddAssetsRequest,
    CollectionAddAssetsResponse,
)
from vmodal.routes import (
    ENDPOINTS,
    _EXTERNAL_UPLOAD_DONE,
    _EXTERNAL_UPLOAD_GET_SIGNED_URL,
    _EXTERNAL_UPLOAD_MULTIPART_CREATE,
    _EXTERNAL_UPLOAD_MULTIPART_SIGN_PARTS,
    _EXTERNAL_UPLOAD_MULTIPART_STATUS,
    _EXTERNAL_UPLOAD_MULTIPART_COMPLETE,
    _EXTERNAL_UPLOAD_MULTIPART_ABORT,
    full,
)
from vmodal.utils import (
    OsPartStream,
    os_file_stat,
    os_file_stat_same,
    os_file_range_md5,
    os_upload_checkpoint_path,
    os_upload_checkpoint_load,
    os_upload_checkpoint_save,
    os_upload_checkpoint_delete,
    os_upload_lock_acquire,
    os_upload_lock_release,
)


def _file_part(file_or_path: Any, fallback: str = "upload.bin") -> Tuple[str, bytes, str]:
    if hasattr(file_or_path, "read"):
        data = file_or_path.read()
        name = os.path.basename(getattr(file_or_path, "name", "") or fallback)
    else:
        path = os.fspath(file_or_path)
        data = Path(path).read_bytes()
        name = os.path.basename(path)
    ctype = mimetypes.guess_type(name)[0] or "application/octet-stream"
    return name, data, ctype


class CollectionsResource:
    def __init__(self, http):
        self.http = http

    async def list_groups(self, mode: Optional[str] = None) -> GroupsResponse:
        params = {}
        if mode is not None:
            params["mode"] = mode
        body = await self.http.request("GET", full(ENDPOINTS.groups), params=params)
        return GroupsResponse.model_validate(body)

    async def _signed_upload_put(self, url: str, method: str, filepath_local: str, ctype: str) -> int:
        import httpx

        if not str(url or "").strip():
            raise ApiError("signed upload URL is empty")

        async def iter_file():
            with open(filepath_local, "rb") as fh:
                while True:
                    chunk = fh.read(1024 * 1024)
                    if not chunk:
                        break
                    yield chunk

        try:
            async with httpx.AsyncClient(timeout=self.http.cfg.timeout) as client:
                res = await client.request(
                    str(method or "PUT").upper(),
                    url,
                    content=iter_file(),
                    headers={"Content-Type": ctype, "Content-Length": str(os.path.getsize(filepath_local))},
                )
        except Exception as exc:
            raise ApiError("signed upload transport error", body=str(exc)) from exc
        if not (200 <= int(res.status_code) < 300):
            raise ApiError("signed upload failed", status_code=int(res.status_code), body=res.text)
        return int(res.status_code)

    async def _signed_upload_done(
        self,
        key: str,
        mode: str,
        collection_name: str,
        sub_collection_name: str,
        modality: str,
        filename: str,
    ) -> Dict[str, Any]:
        return await self.http.request(
            "POST",
            full(_EXTERNAL_UPLOAD_DONE),
            params={
                "key": key,
                "mode": mode,
                "group_name": collection_name,
                "stream_name": sub_collection_name,
                "modality": modality,
                "filename": filename,
            },
        )

    async def _multipart_status(self, checkpoint: Dict[str, Any]) -> MultipartStatusResponse:
        body = await self.http.request(
            "GET",
            full(_EXTERNAL_UPLOAD_MULTIPART_STATUS),
            params={
                "request_id": checkpoint["request_id"],
                "upload_id": checkpoint["upload_id"],
                "key": checkpoint["key"],
            },
        )
        return MultipartStatusResponse.model_validate(body)

    async def _multipart_sign(
        self,
        checkpoint: Dict[str, Any],
        part_numbers: List[int],
        ttl: int,
    ) -> MultipartSignResponse:
        body = await self.http.request(
            "POST",
            full(_EXTERNAL_UPLOAD_MULTIPART_SIGN_PARTS),
            json={
                "request_id": checkpoint["request_id"],
                "upload_id": checkpoint["upload_id"],
                "key": checkpoint["key"],
                "part_numbers": part_numbers,
                "ttl": int(ttl),
            },
        )
        return MultipartSignResponse.model_validate(body)

    async def _multipart_abort(self, checkpoint: Dict[str, Any]) -> None:
        if not checkpoint.get("upload_id"):
            return
        await self.http.request(
            "POST",
            full(_EXTERNAL_UPLOAD_MULTIPART_ABORT),
            json={
                "request_id": checkpoint["request_id"],
                "upload_id": checkpoint["upload_id"],
                "key": checkpoint["key"],
            },
        )

    async def _multipart_put_one(
        self,
        checkpoint: Dict[str, Any],
        checkpoint_path: str,
        signed: Any,
        filepath_local: str,
        part_size: int,
        ttl: int,
        max_part_attempts: int,
        part_timeout_seconds: float,
    ) -> Tuple[int, str, int, int]:
        import httpx

        number = int(signed.part_number)
        offset = (number - 1) * int(checkpoint["part_size_bytes"])
        url = signed.url
        method = signed.method
        base_headers = dict(signed.headers or {})
        for name in list(base_headers):
            if name.lower() in {"authorization", "x-user-id", "x-tenant-id", "x-user-email"}:
                base_headers.pop(name, None)
        retry_codes = {408, 429, 500, 502, 503, 504}
        for attempt in range(1, max_part_attempts + 1):
            stream = OsPartStream(filepath_local, offset, part_size)
            headers = dict(base_headers)
            headers["Content-Length"] = str(part_size)
            try:
                timeout = httpx.Timeout(float(part_timeout_seconds))
                async with httpx.AsyncClient(timeout=timeout) as client:
                    res = await client.request(str(method or "PUT").upper(), url, content=stream, headers=headers)
                etag = str(res.headers.get("ETag") or "").strip().strip('"')
                if 200 <= int(res.status_code) < 300 and etag and etag.lower() == stream.str_md5().lower():
                    return number, etag, part_size, attempt
                if int(res.status_code) == 403 and attempt < max_part_attempts:
                    refreshed = await self._multipart_sign(checkpoint, [number], ttl)
                    if len(refreshed.parts) != 1:
                        raise ApiError("multipart URL refresh returned no part", body={"part_number": number})
                    url = refreshed.parts[0].url
                    method = refreshed.parts[0].method
                    base_headers = dict(refreshed.parts[0].headers or {})
                    for name in list(base_headers):
                        if name.lower() in {"authorization", "x-user-id", "x-tenant-id", "x-user-email"}:
                            base_headers.pop(name, None)
                elif int(res.status_code) not in retry_codes:
                    raise ApiError(
                        "multipart part upload failed",
                        status_code=int(res.status_code),
                        body={
                            "request_id": checkpoint["request_id"],
                            "upload_id": checkpoint["upload_id"],
                            "part_number": number,
                            "attempt_count": attempt,
                        },
                    )
                retry_after = str(res.headers.get("Retry-After") or "").strip()
                delay = min(60.0, float(retry_after)) if retry_after.replace(".", "", 1).isdigit() else 0.0
            except ApiError:
                raise
            except (httpx.TransportError, OSError) as exc:
                delay = 0.0
                if stream.read_bytes == part_size:
                    try:
                        status_now = await self._multipart_status(checkpoint)
                        found = next((p for p in status_now.parts if p.part_number == number), None)
                        if found and found.size_bytes == part_size and found.etag.lower() == stream.str_md5().lower():
                            return number, found.etag, part_size, attempt
                    except ApiError:
                        pass
                if attempt >= max_part_attempts:
                    raise ApiError(
                        "multipart part transport failed",
                        body={
                            "request_id": checkpoint["request_id"],
                            "upload_id": checkpoint["upload_id"],
                            "part_number": number,
                            "attempt_count": attempt,
                            "error": str(exc),
                        },
                    ) from exc
            if attempt < max_part_attempts:
                delay = delay or random.uniform(0.0, min(30.0, float(2 ** (attempt - 1))))
                await asyncio.sleep(delay)
        raise ApiError("multipart part attempts exhausted", body={"part_number": number})

    async def _multipart_upload(
        self,
        filepath_local: str,
        filename: str,
        ctype: str,
        file_stat: Dict[str, int],
        collection_name: str,
        sub_collection_name: str,
        mode: str,
        modality: str,
        ttl: int,
        part_size_bytes: int,
        max_concurrency: int,
        max_part_attempts: int,
        part_timeout_seconds: float,
        resume: bool,
    ) -> VideoUploadResponse:
        user_id = str(self.http.cfg.user_id or "").strip()
        checkpoint_path = os_upload_checkpoint_path(user_id, filepath_local)
        lock = os_upload_lock_acquire(checkpoint_path)
        contract = {
            "mode": mode,
            "group_name": collection_name,
            "stream_name": sub_collection_name,
            "modality": modality,
            "filename": filename,
            "content_type": ctype,
            "size_bytes": file_stat["size"],
            "part_size_bytes": int(part_size_bytes),
        }
        try:
            checkpoint = os_upload_checkpoint_load(checkpoint_path)
            resumed = bool(checkpoint and resume)
            if checkpoint and not resume:
                await self._multipart_abort(checkpoint)
                os_upload_checkpoint_delete(checkpoint_path)
                checkpoint = None
            if checkpoint and (
                os.path.abspath(str(checkpoint.get("path") or "")) != filepath_local
                or int(checkpoint.get("part_size_bytes", 0)) != int(part_size_bytes)
                or not os_file_stat_same(dict(checkpoint.get("file_stat") or {}), file_stat)
                or {
                    key: value
                    for key, value in dict(checkpoint.get("create_body") or {}).items()
                    if key != "request_id"
                } != contract
            ):
                await self._multipart_abort(checkpoint)
                os_upload_checkpoint_delete(checkpoint_path)
                raise ValidationFailed("local file changed since multipart upload started", status_code=422)
            if checkpoint is None:
                request_id = str(uuid.uuid4())
                create_body = {"request_id": request_id, **contract}
                body = await self.http.request(
                    "POST",
                    full(_EXTERNAL_UPLOAD_MULTIPART_CREATE),
                    json=create_body,
                )
                created = MultipartCreateResponse.model_validate(body)
                if created.part_size_bytes != int(part_size_bytes) or created.part_count != max(
                    1, (file_stat["size"] + int(part_size_bytes) - 1) // int(part_size_bytes)
                ):
                    raise ApiError("multipart create response does not match local upload contract")
                checkpoint = {
                    "version": 1,
                    "request_id": created.request_id,
                    "upload_id": created.upload_id,
                    "key": created.key,
                    "path": filepath_local,
                    "file_stat": file_stat,
                    "part_size_bytes": created.part_size_bytes,
                    "part_count": created.part_count,
                    "parts": {},
                    "state": "uploading",
                    "create_body": create_body,
                }
                os_upload_checkpoint_save(checkpoint_path, checkpoint)

            try:
                status_now = await self._multipart_status(checkpoint)
            except ApiError as exc:
                if int(exc.status_code or 0) != 404:
                    raise
                recovered_body = await self.http.request(
                    "POST",
                    full(_EXTERNAL_UPLOAD_MULTIPART_CREATE),
                    json=checkpoint["create_body"],
                )
                recovered = MultipartCreateResponse.model_validate(recovered_body)
                if recovered.upload_id != checkpoint["upload_id"] or recovered.key != checkpoint["key"]:
                    raise ApiError(
                        "multipart upload session could not be recovered",
                        body={"request_id": checkpoint["request_id"], "upload_id": checkpoint["upload_id"]},
                    )
                status_now = await self._multipart_status(checkpoint)
            if status_now.status == "completed":
                checkpoint["state"] = "r2_completed"
                checkpoint["etag"] = status_now.etag
                os_upload_checkpoint_save(checkpoint_path, checkpoint)
            else:
                if len({part.part_number for part in status_now.parts}) != len(status_now.parts):
                    raise ApiError("multipart status returned duplicate parts")
                authoritative = {}
                for part in status_now.parts:
                    offset = (part.part_number - 1) * int(checkpoint["part_size_bytes"])
                    expected_size = min(int(checkpoint["part_size_bytes"]), file_stat["size"] - offset)
                    expected_etag = ""
                    if 1 <= part.part_number <= int(checkpoint["part_count"]) and expected_size > 0:
                        expected_etag = os_file_range_md5(filepath_local, offset, expected_size)
                    if part.size_bytes == expected_size and part.etag.lower() == expected_etag.lower():
                        authoritative[str(part.part_number)] = {
                            "etag": part.etag,
                            "size_bytes": part.size_bytes,
                        }
                checkpoint["parts"] = authoritative
                os_upload_checkpoint_save(checkpoint_path, checkpoint)
                missing = [
                    number
                    for number in range(1, int(checkpoint["part_count"]) + 1)
                    if str(number) not in authoritative
                ]
                attempts = 0
                batch_size = min(32, max_concurrency * 2)
                for start in range(0, len(missing), batch_size):
                    numbers = missing[start : start + batch_size]
                    signed_batch = await self._multipart_sign(checkpoint, numbers, ttl)
                    signed_by_number = {part.part_number: part for part in signed_batch.parts}
                    if set(signed_by_number) != set(numbers):
                        raise ApiError("multipart sign response did not match requested parts")
                    semaphore = asyncio.Semaphore(max_concurrency)

                    async def put_one(number: int):
                        async with semaphore:
                            offset = (number - 1) * int(checkpoint["part_size_bytes"])
                            size = min(int(checkpoint["part_size_bytes"]), file_stat["size"] - offset)
                            result = await self._multipart_put_one(
                                checkpoint,
                                checkpoint_path,
                                signed_by_number[number],
                                filepath_local,
                                size,
                                ttl,
                                max_part_attempts,
                                part_timeout_seconds,
                            )
                            part_number, etag, uploaded_size, count = result
                            checkpoint["parts"][str(part_number)] = {
                                "etag": etag,
                                "size_bytes": uploaded_size,
                            }
                            os_upload_checkpoint_save(checkpoint_path, checkpoint)
                            return result

                    results = await asyncio.gather(*(put_one(number) for number in numbers))
                    for number, etag, size, count in results:
                        attempts += count

                if not os_file_stat_same(file_stat, os_file_stat(filepath_local)):
                    await self._multipart_abort(checkpoint)
                    os_upload_checkpoint_delete(checkpoint_path)
                    raise ValidationFailed("local file changed during multipart upload", status_code=422)
                status_now = await self._multipart_status(checkpoint)
                parts = sorted(status_now.parts, key=lambda part: part.part_number)
                if len(parts) != int(checkpoint["part_count"]):
                    raise ApiError("multipart status is missing uploaded parts")
                for part in parts[:-1]:
                    if part.size_bytes != int(checkpoint["part_size_bytes"]):
                        raise ApiError("multipart status returned an invalid part size")
                final_size = file_stat["size"] - (len(parts) - 1) * int(checkpoint["part_size_bytes"])
                if not parts or parts[-1].size_bytes != final_size:
                    raise ApiError("multipart status returned an invalid final part size")
                complete_body = await self.http.request(
                    "POST",
                    full(_EXTERNAL_UPLOAD_MULTIPART_COMPLETE),
                    json={
                        "request_id": checkpoint["request_id"],
                        "upload_id": checkpoint["upload_id"],
                        "key": checkpoint["key"],
                        "size_bytes": file_stat["size"],
                        "parts": [
                            {"part_number": part.part_number, "etag": part.etag}
                            for part in parts
                        ],
                    },
                )
                completed = MultipartCompleteResponse.model_validate(complete_body)
                checkpoint["state"] = "r2_completed"
                checkpoint["etag"] = completed.etag
                os_upload_checkpoint_save(checkpoint_path, checkpoint)

            done = await self._signed_upload_done(
                key=checkpoint["key"],
                mode=mode,
                collection_name=collection_name,
                sub_collection_name=sub_collection_name,
                modality=modality,
                filename=filename,
            )
            part_count = int(checkpoint["part_count"])
            result = VideoUploadResponse(
                filepath_local=filepath_local,
                filename=filename,
                size_bytes=file_stat["size"],
                status_code=200,
                uploaded=True,
                upload_strategy="multipart",
                upload_id=checkpoint["upload_id"],
                key=checkpoint["key"],
                etag=str(checkpoint.get("etag") or ""),
                part_size_bytes=int(checkpoint["part_size_bytes"]),
                part_count=part_count,
                parts_uploaded=part_count,
                resumed=resumed,
                attempt_count=locals().get("attempts", 0),
                upload_done=done,
                dest_path=done.get("dest_path", "") if isinstance(done, dict) else "",
            )
            os_upload_checkpoint_delete(checkpoint_path)
            return result
        finally:
            os_upload_lock_release(lock)

    async def video_upload(
        self,
        filepath_local: str,
        collection_name: str,
        sub_collection_name: str,
        mode: str = "vid_file",
        modality: str = "vid_raw",
        ttl: int = 12600,
        *,
        multipart: Optional[bool] = None,
        multipart_threshold_bytes: int = 100 * 1024 * 1024,
        part_size_bytes: int = 64 * 1024 * 1024,
        max_concurrency: int = 4,
        max_part_attempts: int = 5,
        part_timeout_seconds: float = 300,
        resume: bool = True,
    ) -> VideoUploadResponse:
        """Stream one local media file through a signed object-store upload.

        Use ``mode="img_file", modality="img_raw"`` for images. The legacy
        multipart ``upload_file()`` method was removed because it loaded the
        complete file into memory.
        """
        path = os.path.abspath(os.fspath(filepath_local))
        if not os.path.isfile(path):
            raise ValidationFailed("filepath_local must be an existing file", status_code=422, details=path)
        if int(multipart_threshold_bytes) <= 0:
            raise ValidationFailed("multipart_threshold_bytes must be positive", status_code=422)
        if int(part_size_bytes) < 5 * 1024 * 1024:
            raise ValidationFailed("part_size_bytes must be at least 5 MiB", status_code=422)
        if not 1 <= int(max_concurrency) <= 16:
            raise ValidationFailed("max_concurrency must be in 1..16", status_code=422)
        if not 1 <= int(max_part_attempts) <= 10:
            raise ValidationFailed("max_part_attempts must be in 1..10", status_code=422)
        if float(part_timeout_seconds) <= 0:
            raise ValidationFailed("part_timeout_seconds must be positive", status_code=422)
        file_stat = os_file_stat(path)
        part_count = max(1, (file_stat["size"] + int(part_size_bytes) - 1) // int(part_size_bytes))
        if part_count > 10000:
            raise ValidationFailed("part_size_bytes would create more than 10,000 parts", status_code=422)
        filename = os.path.basename(path)
        ctype = mimetypes.guess_type(filename)[0] or "video/mp4"
        use_multipart = bool(multipart) if multipart is not None else file_stat["size"] >= int(multipart_threshold_bytes)
        if use_multipart:
            return await self._multipart_upload(
                filepath_local=path,
                filename=filename,
                ctype=ctype,
                file_stat=file_stat,
                collection_name=collection_name,
                sub_collection_name=sub_collection_name,
                mode=mode,
                modality=modality,
                ttl=ttl,
                part_size_bytes=int(part_size_bytes),
                max_concurrency=int(max_concurrency),
                max_part_attempts=int(max_part_attempts),
                part_timeout_seconds=float(part_timeout_seconds),
                resume=bool(resume),
            )
        body = await self.http.request(
            "POST",
            full(_EXTERNAL_UPLOAD_GET_SIGNED_URL),
            params={
                "mode": mode,
                "group_name": collection_name,
                "stream_name": sub_collection_name,
                "modality": modality,
                "filename": filename,
                "ttl": int(ttl),
            },
        )
        signed = ExternalUploadSignedUrlResponse.model_validate(body)
        status_code = await self._signed_upload_put(signed.url, signed.method, path, ctype)
        done = await self._signed_upload_done(
            key=signed.key,
            mode=mode,
            collection_name=collection_name,
            sub_collection_name=sub_collection_name,
            modality=modality,
            filename=filename,
        )
        out = signed.model_dump()
        out.update(
            {
                "filepath_local": path,
                "filename": filename,
                "size_bytes": os.path.getsize(path),
                "status_code": status_code,
                "uploaded": True,
                "upload_strategy": "single",
                "part_count": 1,
                "parts_uploaded": 1,
                "attempt_count": 1,
                "upload_done": done,
                "dest_path": done.get("dest_path", "") if isinstance(done, dict) else "",
            }
        )
        return VideoUploadResponse.model_validate(out)

    async def video_upload_bulk(
        self,
        folderpath_local: str,
        collection_name: str,
        sub_collection_name: str,
        mode: str = "vid_file",
        modality: str = "vid_raw",
        ttl: int = 12600,
    ) -> VideoUploadBulkResponse:
        folder = os.path.abspath(os.fspath(folderpath_local))
        if not os.path.isdir(folder):
            raise ValidationFailed("folderpath_local must be an existing folder", status_code=422, details=folder)
        files = []
        for name in sorted(os.listdir(folder)):
            path = os.path.join(folder, name)
            if os.path.isfile(path) and name.lower().endswith(".mp4"):
                files.append(path)
        data = []
        for path in files:
            item = await self.video_upload(
                filepath_local=path,
                collection_name=collection_name,
                sub_collection_name=sub_collection_name,
                mode=mode,
                modality=modality,
                ttl=ttl,
            )
            data.append(item)
        return VideoUploadBulkResponse(data=data, total=len(data))

    async def upload_folder(
        self,
        paths: Optional[List[Any]] = None,
        files: Optional[List[Any]] = None,
        group_name: str = "",
        mode: str = "img_file",
        stream_name: str = "astream",
        overwrite: bool = False,
    ) -> FolderUploadResponse:
        # Disabled: cannot scan remote PC/laptop folders.
        raise FeatureDisabled("folder upload is disabled on server (cannot scan remote PC/laptop)")
        # items = files if files is not None else paths
        # items = list(items or [])
        # parts = []
        # for item in items:
        #     name, data, ctype = _file_part(item, "upload.bin")
        #     parts.append(("files", (name, data, ctype)))
        # body = await self.http.request(
        #     "POST",
        #     full(ENDPOINTS.upload_folder),
        #     data={
        #         "mode": mode,
        #         "group_name": group_name,
        #         "stream_name": stream_name,
        #         "overwrite": str(bool(overwrite)).lower(),
        #     },
        #     files=parts,
        # )
        # return FolderUploadResponse.model_validate(body)

    async def upload_google_drive_folder(self, google_drive_url: str, group_name: str, mode: str = "vid_file", stream_name: str = "astream") -> GoogleDriveFolderUploadResponse:
        body = await self.http.request(
            "POST",
            full(ENDPOINTS.upload_google_drive_folder),
            data={
                "google_drive_url": google_drive_url,
                "mode": mode,
                "group_name": group_name,
                "stream_name": stream_name,
            },
        )
        return GoogleDriveFolderUploadResponse.model_validate(body)

    async def upload_metadata_jsonl(
        self,
        path: Any = None,
        file: Any = None,
        mode: str = "img_file",
        group_name: str = "",
        stream_name: str = "",
        write_mode: str = "append",
        allow_overlap: bool = False,
    ) -> MetadataParquetUploadResponse:
        """Upload a metadata JSONL file.

        mode='img_file' expects the strict img_file schema. mode='vid_file'
        accepts a friendly flat JSONL — only ``video`` (the video filename) is
        required; ``title``/``description``/``duration`` map to direct columns
        and every other key (``dtime``/``tags``/``location``/``lat``/``lon``/...)
        is packed into the row's ``info_json`` blob (no new schema columns).
        """
        item = file if file is not None else path
        name, data, ctype = _file_part(item, "metadata.jsonl")
        form = {
            "user_id": str(self.http.cfg.user_id or "").strip(),
            "mode": mode,
            "group_name": group_name,
            "stream_name": stream_name,
            "write_mode": write_mode,
            "allow_overlap": str(bool(allow_overlap)).lower(),
        }
        parts = [("file", (name, data, ctype))]
        try:
            body = await self.http.request(
                "POST",
                full(ENDPOINTS.upload_metadata_jsonl),
                data=form,
                files=parts,
            )
        except ApiError as exc:
            if int(getattr(exc, "status_code", 0) or 0) != 404:
                raise
            # Fallback for old servers without apionly_routes external surface.
            # Real handler: frontui_collection.py POST /api/internal/v1/collection/upload/metadata.
            body = await self.http.request(
                "POST",
                ENDPOINTS.upload_metadata_item_parquet_internal,
                data=form,
                files=parts,
            )
        return MetadataParquetUploadResponse.model_validate(body)

    async def add_assets(
        self,
        collection_id: str,
        asset_ids: List[str],
        mode: str,
        group_name: str,
        stream_name: str = "astream",
        **kw,
    ) -> CollectionAddAssetsResponse:
        data = dict(kw)
        data.pop("user_id", None)
        data.update(
            {
                "collection_id": collection_id,
                "asset_ids": asset_ids,
                "mode": mode,
                "group_name": group_name,
                "stream_name": stream_name,
            }
        )
        try:
            req = CollectionAddAssetsRequest.model_validate(data)
        except ValidationError as exc:
            raise ValidationFailed("validation failed", status_code=422, details=exc.errors()) from exc
        body = await self.http.request(
            "POST",
            full(ENDPOINTS.collection_add_assets.format(collection_id=collection_id)),
            json=req.model_dump(exclude_none=True),
        )
        return CollectionAddAssetsResponse.model_validate(body)

    async def update_description(
        self,
        group_name: str,
        mode: str,
        stream_name: str,
        filename_sanitized: str,
        description: Optional[str] = None,
        tag: Optional[List[str]] = None,
    ) -> CollectionDescriptionUpdateResponse:
        form: Dict[str, Any] = {
            "group_name": group_name,
            "mode": mode,
            "stream_name": stream_name,
            "filename_sanitized": filename_sanitized,
        }
        if description is not None:
            form["description"] = description
        if tag is not None:
            form["tag"] = [str(x) for x in tag]
        body = await self.http.request(
            "POST",
            full(ENDPOINTS.collection_description_update),
            data=form,
        )
        return CollectionDescriptionUpdateResponse.model_validate(body)

    async def delete(
        self,
        group_name: str,
        mode: str,
        scope: str = "all",
        dry_run: bool = False,
        confirm: bool = False,
        **kw,
    ) -> DeleteCollectionResponse:
        data = dict(kw)
        data.pop("user_id", None)
        data.update(
            {
                "group_name": group_name,
                "mode": mode,
                "scope": scope,
                "dry_run": dry_run,
                "confirm": confirm,
            }
        )
        try:
            req = DeleteCollectionRequest.model_validate(data)
        except ValidationError as exc:
            raise ValidationFailed("validation failed", status_code=422, details=exc.errors()) from exc
        body = await self.http.request("DELETE", full(ENDPOINTS.collection_delete), json=req.model_dump(exclude_none=True))
        return DeleteCollectionResponse.model_validate(body)

    async def create(self, **kw):
        raise FeatureDisabled("no server endpoint; upload creates collection implicitly")

    async def edit(self, **kw):
        raise FeatureDisabled("no server endpoint; upload creates collection implicitly")

    async def auto_index_get(self, **kw):
        raise FeatureDisabled("collection auto_index is disabled on server")

    async def auto_index_set(self, **kw):
        raise FeatureDisabled("collection auto_index is disabled on server")

if __name__ == "__main__":
    fire.Fire()
