from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
import os,sys
import json
import fire
from vmodal.sync import SyncClient


def _dump(x: Any) -> Any:
    if hasattr(x, "model_dump"):
        return x.model_dump()
    return x


class CliApp:
    def __init__(self, base_url: str = "", user_id: str = "", tenant_id: str = "", email: str = "", token: str = "", timeout: float = 30, mode: str = ""):
        kw = {}
        if base_url:
            kw["base_url"] = base_url
        if user_id:
            kw["user_id"] = user_id
        if tenant_id:
            kw["tenant_id"] = tenant_id
        if email:
            kw["email"] = email
        if token:
            kw["token"] = token
        if timeout:
            kw["timeout"] = timeout
        if mode:
            kw["mode"] = mode
        self.client = SyncClient.from_env(**kw)

    def health(self):
        return _dump(self.client.health())

    def auth_check(self, user_id: str = ""):
        return self.client.auth_check(user_id=user_id)

    def auth_me(self):
        return _dump(self.client.auth.me())

    def search_video(self, **kw):
        return _dump(self.client.searches.search_video(**kw))

    def list_groups(self, mode: str = ""):
        return _dump(self.client.collections.list_groups(mode=mode or None))

    def video_upload(
        self,
        filepath_local: str,
        collection_name: str,
        sub_collection_name: str,
        mode: str = "vid_file",
        modality: str = "vid_raw",
        ttl: int = 12600,
        multipart: Optional[bool] = None,
        multipart_threshold_bytes: int = 100 * 1024 * 1024,
        part_size_bytes: int = 64 * 1024 * 1024,
        max_concurrency: int = 4,
        max_part_attempts: int = 5,
        part_timeout_seconds: float = 300,
        resume: bool = True,
    ):
        return _dump(self.client.collections.video_upload(
            filepath_local=filepath_local,
            collection_name=collection_name,
            sub_collection_name=sub_collection_name,
            mode=mode,
            modality=modality,
            ttl=ttl,
            multipart=multipart,
            multipart_threshold_bytes=multipart_threshold_bytes,
            part_size_bytes=part_size_bytes,
            max_concurrency=max_concurrency,
            max_part_attempts=max_part_attempts,
            part_timeout_seconds=part_timeout_seconds,
            resume=resume,
        ))

    def video_upload_bulk(self, folderpath_local: str, collection_name: str, sub_collection_name: str, mode: str = "vid_file"):
        return _dump(self.client.collections.video_upload_bulk(folderpath_local=folderpath_local, collection_name=collection_name, sub_collection_name=sub_collection_name, mode=mode))

    # Disabled: cannot scan remote PC/laptop folders.
    # def upload_folder(self, paths: str, group_name: str, mode: str = "img_file", stream_name: str = "astream", overwrite: bool = False):
    #     items = [x.strip() for x in str(paths).split(",") if x.strip()]
    #     return _dump(self.client.collections.upload_folder(paths=items, group_name=group_name, mode=mode, stream_name=stream_name, overwrite=overwrite))

    def upload_google_drive_folder(self, google_drive_url: str, group_name: str, mode: str = "vid_file", stream_name: str = "astream"):
        return _dump(self.client.collections.upload_google_drive_folder(google_drive_url=google_drive_url, group_name=group_name, mode=mode, stream_name=stream_name))

    def upload_metadata_jsonl(self, path: str, mode: str = "img_file", group_name: str = "", stream_name: str = "", write_mode: str = "append", allow_overlap: bool = False):
        return _dump(self.client.collections.upload_metadata_jsonl(path=path, mode=mode, group_name=group_name, stream_name=stream_name, write_mode=write_mode, allow_overlap=allow_overlap))

    def update_description(self, group_name: str, mode: str, stream_name: str, filename_sanitized: str, description: str = "", tag_json: str = ""):
        tag = json.loads(tag_json or "[]") if tag_json else None
        return _dump(
            self.client.collections.update_description(
                group_name=group_name,
                mode=mode,
                stream_name=stream_name,
                filename_sanitized=filename_sanitized,
                description=description or None,
                tag=tag,
            )
        )

    def add_assets(
        self,
        collection_id: str,
        asset_ids_json: str = "",
        assets_json: str = "",
        mode: str = "img_file",
        group_name: str = "",
        stream_name: str = "astream",
    ):
        asset_ids = json.loads(asset_ids_json or assets_json or "[]")
        return _dump(
            self.client.collections.add_assets(
                collection_id=collection_id,
                asset_ids=asset_ids,
                mode=mode,
                group_name=group_name or collection_id,
                stream_name=stream_name,
            )
        )

    def delete_collection(
        self,
        group_name: str,
        mode: str,
        scope: str = "all",
        dry_run: bool = False,
        confirm: bool = False,
    ):
        return _dump(
            self.client.collections.delete(
                group_name=group_name,
                mode=mode,
                scope=scope,
                dry_run=dry_run,
                confirm=confirm,
            )
        )

    def jobs_list(self, status: str = "", mode: str = "", group_name: str = "", limit: int = 200):
        return _dump(self.client.indexes.jobs_list(status=status or None, mode=mode or None, group_name=group_name or None, limit=limit))

    def create_index(self, mode: str, group_name: str, index_type: str = "", version: str = "new_version", insert_mode: str = "append", dry_run: bool = False):
        return _dump(self.client.indexes.create_index(mode=mode, group_name=group_name, index_type=index_type or None, version=version, insert_mode=insert_mode, dry_run=dry_run))

    def index_status(self, job_id: str):
        return _dump(self.client.indexes.index_status(job_id=job_id))

    def delete_index(self, mode: str, group_name: str, version: str, modality: str = "", dry_run: bool = False, confirm: bool = False):
        return _dump(self.client.indexes.delete_index(mode=mode, group_name=group_name, version=version, modality=modality or None, dry_run=dry_run, confirm=confirm))

    def user_stats(self):
        return _dump(self.client.admin.user_stats())

    def admin_usage(self, date: str = ""):
        return _dump(self.client.admin.usage(date=date))

    def admin_cache_stats(self):
        return _dump(self.client.admin.cache_stats())

    def r2_credentials(self, dir_prefix: str = ""):
        return _dump(self.client.r2.get_credentials(dir_prefix=dir_prefix))

    def r2_presign_upload_file(self, mode: str, group_name: str, stream_name: str, modality: str, filename: str, expires_in: int = 86400):
        return _dump(
            self.client.r2.presign_upload_file(
                mode=mode,
                group_name=group_name,
                stream_name=stream_name,
                modality=modality,
                filename=filename,
                expires_in=expires_in,
            )
        )

    def r2_presign_upload_folder_video(self, mode: str, group_name: str, stream_name: str, filenames: str, expires_in: int = 86400):
        items = [x.strip() for x in str(filenames or "").split(",") if x.strip()]
        return _dump(
            self.client.r2.presign_upload_folder_video(
                mode=mode,
                group_name=group_name,
                stream_name=stream_name,
                filenames=items,
                expires_in=expires_in,
            )
        )

    def image_get_url(self, mode: str, group_name: str, modality: str, filename: str, stream_name: str = "astream", ts_unix_13digits: str = "", userid: str = ""):
        return _dump(self.client.images.get_url(mode=mode, group_name=group_name, modality=modality, stream_name=stream_name, filename=filename, ts_unix_13digits=ts_unix_13digits or None, userid=userid or None))

    def image_get_url_bulk(self, records_json: str, userid: str = ""):
        return _dump(self.client.images.get_url_bulk(records=json.loads(records_json or "[]"), userid=userid or None))

    def image_get_from_url(self, url_pre_signed: str, userid: str = ""):
        return self.client.images.get_image_from_url(url_pre_signed=url_pre_signed, userid=userid or None)

    def image_get_bulk_from_urls(self, urls_json: str, userid: str = ""):
        return _dump(self.client.images.get_image_bulk_from_urls(urls=json.loads(urls_json or "[]"), userid=userid or None))


def main():
    fire.Fire(CliApp)


if __name__ == "__main__":
    main()
