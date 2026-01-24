from __future__ import annotations

import io
import os
import time
from pathlib import Path

import httpx
from rich.align import Align
from rich.console import Group
from rich.prompt import Confirm
from rich.status import Status

import coiled
from coiled.cli.curl import sync_request
from coiled.exceptions import CoiledException


def wait_until_complete(cluster_id, wait_for_output=True, wait_for_input=False):
    done = False
    attachments = None
    timeout_at = time.monotonic() + 30
    while not done and time.monotonic() < timeout_at:
        attachments = FilestoreManager.get_cluster_attachments(cluster_id)
        if not attachments:
            return None

        done = all(
            a["complete"] for a in attachments if ((wait_for_output and a["output"]) or (wait_for_input and a["input"]))
        )
        if not done:
            time.sleep(2)
    return attachments


def list_files_ui(fs, name_includes=None):
    blobs = FilestoreManager.get_download_list_with_urls(fs["id"])

    if name_includes:
        blobs = [blob for blob in blobs if name_includes in blob["relative_path"]]

    for blob in blobs:
        print(blob["relative_path"])


def download_from_filestore_with_ui(fs, into=".", name_includes=None):
    if fs:
        # TODO (possible enhancement) if "has files" flag is set then make sure we do see files to download?
        blobs = FilestoreManager.get_download_list_with_urls(fs["id"])

        if name_includes:
            blobs = [blob for blob in blobs if name_includes in blob["relative_path"]]

        total_bytes = sum(blob["size"] for blob in blobs)

        size_label = "Bytes"
        size_scale = 1

        if total_bytes > 10_000_000:
            size_label = "Mb"
            size_scale = 1_000_000
        elif total_bytes > 10_000:
            size_label = "Kb"
            size_scale = 1_000

        def progress_title(f=None):
            return Group(
                Align.left(Status(f"Downloading from cloud storage: [green]{fs['name']}[green]", spinner="dots")),
                Align.left(f"Local directory: [green]{into}[/green]"),
                Align.left(f"Currently downloading: [blue]{f or ''}[/blue]"),
            )

        with coiled.utils.SimpleRichProgressPanel.from_defaults(title=progress_title()) as progress:
            done_files = 0
            done_bytes = 0

            progress.update_progress([
                {"label": "Files", "total": len(blobs), "completed": done_files},
                {
                    "label": size_label,
                    "total": total_bytes / size_scale if size_scale > 1 else total_bytes,
                    "completed": done_bytes / size_scale if size_scale > 1 else done_bytes,
                },
            ])

            for blob in blobs:
                progress.update_title(progress_title(blob["key"]))

                FilestoreManager.download_from_signed_url(
                    local_path=os.path.join(into, blob["relative_path"]),
                    url=blob["url"],
                )

                done_files += 1
                done_bytes += blob["size"]

                progress.update_progress([
                    {"label": "Files", "total": len(blobs), "completed": done_files},
                    {
                        "label": size_label,
                        "total": total_bytes / size_scale if size_scale > 1 else total_bytes,
                        "completed": done_bytes / size_scale if size_scale > 1 else done_bytes,
                    },
                ])

            progress.update_title(
                Group(
                    Align.left(f"Downloaded from cloud storage: [green]{fs['name']}[green]"),
                    Align.left(f"Local directory: [green]{into}[/green]"),
                )
            )


def upload_to_filestore_with_ui(fs, local_dir, file_buffers=None):
    # TODO (future enhancement) send write status
    #   this is tricky because status is stored on the "attachment" object, which might not exist yet
    #   because we want to be able to upload files before cluster has been created
    # FilestoreManager.post_fs_write_status(fs["id"], "start")

    def progress_title(f=None):
        return Group(
            Align.left(Status(f"Uploading to cloud storage: [green]{fs['name']}[green]", spinner="dots")),
            Align.left(f"Currently uploading: [blue]{f or ''}[/blue]"),
        )

    files = []
    total_bytes = None

    if fs:
        if local_dir:
            files_from_path, total_bytes = FilestoreManager.get_files_for_upload(local_dir)
            files.extend(files_from_path)
        if file_buffers:
            files.extend(file_buffers)

    if files:
        size_label = "Bytes"
        size_scale = 1

        if total_bytes and total_bytes > 10_000_000:
            size_label = "Mb"
            size_scale = 1_000_000
        elif total_bytes and total_bytes > 10_000:
            size_label = "Kb"
            size_scale = 1_000

        with coiled.utils.SimpleRichProgressPanel.from_defaults(title=progress_title()) as progress:
            done_files = 0
            done_bytes = 0

            progress.update_progress([
                {"label": "Files", "total": len(files), "completed": done_files},
                {
                    "label": size_label,
                    "total": total_bytes / size_scale if size_scale > 1 else total_bytes,
                    "completed": done_bytes / size_scale if size_scale > 1 else done_bytes,
                }
                if total_bytes
                else {},
            ])

            # files_for_upload is type list[dict] where each dict has "relative_path" key
            upload_info = FilestoreManager.get_signed_upload_urls(fs["id"], files_for_upload=files)

            upload_urls = upload_info.get("urls")
            existing_blobs = upload_info.get("existing")

            for file in files:
                relative_path = file.get("relative_path")
                local_path = file.get("local_path")
                buffer = file.get("buffer")
                if local_path:
                    size = file.get("size")
                    skip_upload = False
                    existing_blob_info = existing_blobs.get(relative_path)
                    if existing_blob_info:
                        modified = os.path.getmtime(local_path)
                        if size == existing_blob_info["size"] and modified < existing_blob_info["modified"]:
                            skip_upload = True

                    if not skip_upload:
                        progress.batch_title = progress_title(local_path)
                        progress.refresh()

                        FilestoreManager.upload_to_signed_url(local_path, upload_urls[relative_path])

                    done_bytes += size

                elif buffer:
                    FilestoreManager.upload_bytes_to_signed_url(buffer, upload_urls[relative_path])

                done_files += 1

                progress.update_progress([
                    {"label": "Files", "total": len(files), "completed": done_files},
                    {
                        "label": size_label,
                        "total": total_bytes / size_scale if size_scale > 1 else total_bytes,
                        "completed": done_bytes / size_scale if size_scale > 1 else done_bytes,
                    }
                    if total_bytes
                    else {},
                ])

            progress.update_title(Align.left(f"Uploaded to cloud storage: [green]{fs['name']}[green]"))

        # TODO (future enhancement) send write status
        # FilestoreManager.post_fs_write_status(fs["id"], "finish", {"complete": True, "file_count": len(files)})

        return len(files)


def upload_bytes_to_fs(fs, files):
    def progress_title(f=None):
        return Group(
            Align.left(Status(f"Uploading to cloud storage: [green]{fs['name']}[green]", spinner="dots")),
            Align.left(f"Currently uploading: [blue]{f or ''}[/blue]"),
        )

    if fs and files:
        with coiled.utils.SimpleRichProgressPanel.from_defaults(title=progress_title()) as progress:
            done_files = 0

            progress.update_progress([
                {"label": "Files", "total": len(files), "completed": done_files},
            ])

            upload_info = FilestoreManager.get_signed_upload_urls(fs["id"], files_for_upload=files)

            upload_urls = upload_info.get("urls")
            existing_blobs = upload_info.get("existing")

            for file in files:
                local_path = file.get("local_path")
                relative_path = file.get("relative_path")
                size = file.get("size")
                skip_upload = False
                existing_blob_info = existing_blobs.get(relative_path)
                if existing_blob_info:
                    modified = os.path.getmtime(local_path)
                    if size == existing_blob_info["size"] and modified < existing_blob_info["modified"]:
                        skip_upload = True

                if not skip_upload:
                    progress.batch_title = progress_title(local_path)
                    progress.refresh()

                    FilestoreManager.upload_to_signed_url(local_path, upload_urls[relative_path])

                done_files += 1

                progress.update_progress([
                    {"label": "Files", "total": len(files), "completed": done_files},
                ])

            progress.update_title(Align.left(f"Uploaded to cloud storage: [green]{fs['name']}[green]"))

        # TODO (future enhancement) send write status
        # FilestoreManager.post_fs_write_status(fs["id"], "finish", {"complete": True, "file_count": len(files)})

        return len(files)


def clear_filestores_with_ui(filestores):
    seen = set()
    # see if user wants to delete files from cloud storage now that job is done and results are downloaded
    # TODO (possible feature enhancement)
    #   distinguish filestores created for this specific job from "named" filestores made explicitly?
    for fs in filestores:
        if fs["id"] in seen:
            continue
        seen.add(fs["id"])
        if Confirm.ask(f"Clear cloud storage for [green]{fs['name']}[/green]?", default=True):
            FilestoreManager.clear_fs(fs["id"])


class FilestoreManagerWithoutHttp:
    # code duplicated between coiled_agent.py and coiled client package
    http2 = False

    @staticmethod
    def make_req(api_path, post=False, data=None):
        raise NotImplementedError()

    @classmethod
    def get_filestore(cls, name=None):
        if name:
            return cls.make_req(f"/api/v2/filestore/name/{name}").get("filestores")

    @classmethod
    def get_or_create_filestores(cls, names, workspace, region):
        return cls.make_req(
            "/api/v2/filestore/list", post=True, data={"names": names, "workspace": workspace, "region": region}
        ).get("filestores")

    @classmethod
    def get_cluster_attachments(cls, cluster_id):
        return cls.make_req(f"/api/v2/filestore/cluster/{cluster_id}").get("attachments")

    @classmethod
    def get_vm_attachments(cls, vm_role=""):
        return cls.make_req(f"/api/v2/filestore/vm/{vm_role}").get("attachments")

    @classmethod
    def get_signed_upload_urls(cls, fs_id, files_for_upload):
        paths = [f["relative_path"] for f in files_for_upload]  # relative paths
        return cls.make_req(f"/api/v2/filestore/fs/{fs_id}/signed-urls/upload", post=True, data={"paths": paths})

    @classmethod
    def get_download_list_with_urls(cls, fs_id):
        return cls.make_req(f"/api/v2/filestore/fs/{fs_id}/download-with-urls").get("blobs_with_urls")

    @classmethod
    def attach_filestores_to_cluster(cls, cluster_id, attachments):
        return cls.make_req(
            "/api/v2/filestore/attach",
            post=True,
            data={
                "cluster_id": cluster_id,
                "attachments": attachments,
            },
        )

    @classmethod
    def post_fs_write_status(cls, fs_id, action: str, data: dict | None = None):
        # this endpoint uses cluster auth to determine the filestore
        cls.make_req(f"/api/v2/filestore/fs/{fs_id}/status/{action}", post=True, data=data)

    @classmethod
    def clear_fs(cls, fs_id):
        cls.make_req(f"/api/v2/filestore/fs/{fs_id}/clear", post=True)

    @staticmethod
    def get_files_for_upload(local_dir):
        files = []
        total_bytes = 0

        # if we're given a specific file path instead of directory, then mark that file for upload
        if os.path.isfile(local_dir):
            local_path = local_dir
            local_dir = os.path.dirname(local_path)
            relative_path = Path(os.path.relpath(local_path, local_dir)).as_posix()
            size = os.path.getsize(local_path)

            files.append({"local_path": local_path, "relative_path": relative_path, "size": size})
            total_bytes += size

            return files, total_bytes

        ignore_before_ts = 0
        if os.path.exists(os.path.join(local_dir, ".ignore-before")):
            ignore_before_ts = os.path.getmtime(os.path.join(local_dir, ".ignore-before"))

        for parent_dir, _, children in os.walk(local_dir):
            ignore_file_list = set()

            if ".ignore-list" in children:
                with open(os.path.join(parent_dir, ".ignore-list")) as f:
                    ignore_file_list = set(f.read().split("\n"))

            for child in children:
                local_path = os.path.join(parent_dir, child)

                # we use .ignore-before file so that if we're using a directory which already had files
                # (e.g., we're using same directory for inputs and outputs)
                # then we'll only upload new or modified files, not prior unmodified files
                if (
                    child.startswith(".ignore")
                    or child in ignore_file_list
                    or (ignore_before_ts and os.path.getmtime(local_path) < ignore_before_ts)
                ):
                    continue

                relative_path = Path(os.path.relpath(local_path, local_dir)).as_posix()
                size = os.path.getsize(local_path)

                files.append({"local_path": local_path, "relative_path": relative_path, "size": size})
                total_bytes += size
        return files, total_bytes

    @classmethod
    def upload_to_signed_url(cls, local_path: str, url: str):
        with open(local_path, "rb") as f:
            buffer = io.BytesIO(f.read())
            cls.upload_bytes_to_signed_url(buffer=buffer, url=url)

    @classmethod
    def upload_bytes_to_signed_url(cls, buffer: io.BytesIO, url: str):
        buffer.seek(0)
        num_bytes = len(buffer.getvalue())
        with httpx.Client(http2=cls.http2) as client:
            headers = {"Content-Type": "binary/octet-stream", "Content-Length": str(num_bytes)}
            if "blob.core.windows.net" in url:
                headers["x-ms-blob-type"] = "BlockBlob"
            # TODO error handling
            client.put(
                url,
                # content must be set to an iterable of bytes, rather than a
                # bytes object (like file.read()) because files >2GB need
                # to be sent in chunks to avoid an OverflowError in the
                # Python stdlib ssl module, and httpx will not chunk up a
                # bytes object automatically.
                content=buffer,
                timeout=60,
                headers=headers,
            )

    @classmethod
    def download_from_signed_url(cls, local_path, url, max_retries=3, verbose=False):
        # TODO (performance enhancement) check if file already exists, skip if match, warn if not
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        if verbose:
            print(f"Downloading file from signed URL: {url} to {local_path}")

        with httpx.Client(http2=cls.http2) as client:
            for attempt in range(max_retries):
                try:
                    with client.stream("GET", url, timeout=60) as response:
                        response.raise_for_status()
                        with open(local_path, "wb") as f:
                            for chunk in response.iter_bytes(chunk_size=8192):
                                f.write(chunk)
                    return  # Success, exit function
                except (httpx.RemoteProtocolError, httpx.ReadTimeout, httpx.ConnectError, httpx.HTTPStatusError) as e:
                    if attempt < max_retries - 1:
                        wait_time = 2**attempt  # Exponential backoff: 1s, 2s, 4s
                        if verbose:
                            print(
                                f"Download failed (attempt {attempt + 1}/{max_retries}): {e}. "
                                f"Retrying in {wait_time}s..."
                            )
                        time.sleep(wait_time)
                    else:
                        if verbose:
                            print(f"Download failed after {max_retries} attempts: {e}")
                        raise


class FilestoreManager(FilestoreManagerWithoutHttp):
    http2 = True

    @staticmethod
    def make_req(api_path, post=False, data=None):
        workspace = (data or {}).get("workspace")
        with coiled.Cloud(workspace=workspace) as cloud:
            url = f"{cloud.server}{api_path}"
            response = sync_request(
                cloud=cloud,
                url=url,
                method="post" if post else "get",
                json=True,
                data=data,
                json_output=True,
            )
            if isinstance(response, dict) and response.get("error"):
                raise CoiledException(f"\n\n{response['error']}")
            return response
