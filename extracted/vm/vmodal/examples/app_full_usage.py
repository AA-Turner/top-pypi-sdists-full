"""Application-style usage of the Python SDK.

This file shows the SDK calls you would wire into a real application service:
configuration, health/auth checks, collection discovery, search, signed image URL
creation, single-image download, and bulk image retrieval.

Usage:
  pip install vmodal
  export VMODAL_API_KEY=ak_xxx
  python examples/app_full_usage.py run
  python examples/app_full_usage.py search
  python examples/app_full_usage.py image_from_hit
  python examples/app_full_usage.py image_from_url --url_pre_signed "$URL"
  python examples/app_full_usage.py upload_video --filepath_local /path/to/video.mp4 --collection_name newsalien2
  python examples/app_full_usage.py video_e2e_process --collection_name sdk_dummy_video
  python examples/app_full_usage.py create_index_dry_run

Fixture defaults:
  VMODAL_API_KEY is read by SyncClient.from_env(); identity is derived from it.
  mode="vid_file", group_name="newsalien2", stream_name="astream".
  search_sources=["image"] avoids missing OCR/ASR LanceDB text tables.
"""
from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
import os,sys
import base64
import time
import shutil
import subprocess
import tempfile
import logging
from pathlib import Path
import fire
from vmodal import SyncClient
from vmodal.errors import ApiError

logging.basicConfig(level=logging.INFO, format="%(message)s")
log_info = logging.info
log_warning = logging.warning

DIR_IMAGE_OUT = os.path.join(tempfile.gettempdir(), "vmodal_examples")


@dataclass
class AppConfig:
    mode: str = "vid_file"
    group_name: str = "newsalien2"
    stream_name: str = "astream"
    modality: str = "vid_img"
    query: str = "alien"
    limit: int = 10
    dirout: str = DIR_IMAGE_OUT


def str_env(name: str, default: str = "") -> str:
    return str(os.environ.get(name, default) or "").strip()


def str_live_group(prefix: str = "sdk_live_app") -> str:
    return f"{prefix}_{int(time.time() * 1000)}"


def str_ts_13digits(value: Any) -> str:
    raw = str(value or "").strip()
    if not raw:
        return ""
    digits = "".join([c for c in raw if c.isdigit()])
    if len(digits) >= 13:
        return digits[:13]
    if len(digits) == 10:
        return str(int(digits) * 1000)
    return digits.zfill(13)


def obj_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    raw = str(value or "").strip().lower()
    return raw not in {"0", "false", "no", "off", ""}


def obj_allow_api_error(fn: Any, allow_status: List[int]) -> Dict[str, Any]:
    try:
        return fn()
    except ApiError as exc:
        code = int(getattr(exc, "status_code", 0) or 0)
        if code not in allow_status:
            raise
        return {
            "status": "skipped",
            "status_code": code,
            "body": getattr(exc, "body", None),
        }


def app_client() -> SyncClient:
    return SyncClient.from_env()


def os_image_path(name: str = "image.webp") -> str:
    name = os.path.basename(str(name or "image.webp"))
    return os.path.join(DIR_IMAGE_OUT, name)


def os_dummy_mp4_path(name: str = "dummy_video.mp4") -> str:
    name = os.path.basename(str(name or "dummy_video.mp4"))
    if not name.lower().endswith(".mp4"):
        name = name + ".mp4"
    return os.path.join(DIR_IMAGE_OUT, name)


def os_make_dummy_mp4(path: str = "") -> str:
    path = path or os_dummy_mp4_path()
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            ffmpeg,
            "-y",
            "-f", "lavfi",
            "-i", "testsrc=size=160x90:rate=1:duration=2",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            path,
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return path
    # Fallback for SDK/API upload plumbing when ffmpeg is unavailable.
    data = (
        b"\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp42isom"
        b"\x00\x00\x00\x08free"
        b"\x00\x00\x00\x10mdatdummy-video"
    )
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_bytes(data)
    return path


def obj_dict(obj: Any) -> Dict[str, Any]:
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if isinstance(obj, dict):
        return obj
    return dict(getattr(obj, "__dict__", {}) or {})


def obj_get(obj: Any, names: List[str], default: Any = "") -> Any:
    data = obj_dict(obj)
    for name in names:
        val = data.get(name, getattr(obj, name, None))
        if val not in (None, "", []):
            return val
    return default


def image_record_from_hit(
    hit: Any,
    cfg: AppConfig,
    filename: str = "",
    ts_unix_13digits: str = "",
) -> Dict[str, Any]:
    fname = filename or obj_get(hit, ["filename", "filename_sanitized", "video_filename", "video", "source_path", "path"], "")
    fname = os.path.basename(str(fname or ""))
    ts = str_ts_13digits(ts_unix_13digits or obj_get(hit, ["ts_unix_13digits", "ts_unix", "timestamp_ms"], ""))
    rec: Dict[str, Any] = {
        "mode": cfg.mode,
        "group_name": cfg.group_name,
        "modality": cfg.modality,
        "stream_name": str(obj_get(hit, ["stream_name"], cfg.stream_name) or cfg.stream_name),
        "filename": fname,
    }
    if ts:
        rec["ts_unix_13digits"] = ts
    return rec


def health() -> Dict[str, Any]:
    c = app_client()
    res = c.health()
    data = obj_dict(res)
    log_info(f"health status={data.get('status', '')}")
    return data


def auth_check() -> bool:
    c = app_client()
    ok = c.auth_check()
    log_info(f"auth_check={ok}")
    return ok


def list_groups(mode: str = "vid_file") -> Dict[str, Any]:
    c = app_client()
    res = c.collections.list_groups(mode=mode)
    data = obj_dict(res)
    log_info(f"groups total={data.get('total', len(data.get('data', [])))}")
    return data


def upload_asset(
    path: str,
    group_name: str,
    mode: str = "img_file",
    stream_name: str = "astream",
    modality: str = "img_raw",
) -> Dict[str, Any]:
    c = app_client()
    res = c.collections.video_upload(
        filepath_local=path,
        collection_name=group_name,
        sub_collection_name=stream_name,
        mode=mode,
        modality=modality,
    )
    data = obj_dict(res)
    log_info(f"uploaded file={path} group={group_name}")
    return data


def upload_video(
    filepath_local: str,
    collection_name: str = "newsalien2",
    sub_collection_name: str = "astream",
) -> Dict[str, Any]:
    c = app_client()
    res = c.collections.video_upload(
        filepath_local=filepath_local,
        collection_name=collection_name,
        sub_collection_name=sub_collection_name,
        mode="vid_file",
        modality="vid_raw",
    )
    data = obj_dict(res)
    log_info(f"uploaded video filename={data.get('filename', '')} size={data.get('size_bytes', 0)}")
    return data


def upload_dummy_video(
    collection_name: str = "sdk_dummy_video",
    sub_collection_name: str = "astream",
    filename: str = "dummy_video.mp4",
) -> Dict[str, Any]:
    path = os_make_dummy_mp4(os_dummy_mp4_path(filename))
    upload = upload_video(
        filepath_local=path,
        collection_name=collection_name,
        sub_collection_name=sub_collection_name,
    )
    return {"dummy_path": path, "upload": upload}


def upload_video_folder(
    folderpath_local: str,
    collection_name: str = "newsalien2",
    sub_collection_name: str = "astream",
) -> Dict[str, Any]:
    c = app_client()
    res = c.collections.video_upload_bulk(
        folderpath_local=folderpath_local,
        collection_name=collection_name,
        sub_collection_name=sub_collection_name,
        mode="vid_file",
        modality="vid_raw",
    )
    data = obj_dict(res)
    log_info(f"uploaded videos total={data.get('total', 0)}")
    return data


def upload_metadata_jsonl(
    path: str,
    group_name: str = "newsalien2",
    stream_name: str = "astream",
    write_mode: str = "append",
) -> Dict[str, Any]:
    c = app_client()
    res = c.collections.upload_metadata_jsonl(
        path=path,
        mode="vid_file",
        group_name=group_name,
        stream_name=stream_name,
        write_mode=write_mode,
        allow_overlap=False,
    )
    data = obj_dict(res)
    log_info(f"uploaded metadata path={path}")
    return data


def upload_google_drive_folder(
    google_drive_url: str,
    group_name: str = "newsalien2",
    stream_name: str = "astream",
) -> Dict[str, Any]:
    c = app_client()
    res = c.collections.upload_google_drive_folder(
        google_drive_url=google_drive_url,
        group_name=group_name,
        mode="vid_file",
        stream_name=stream_name,
    )
    data = obj_dict(res)
    log_info(f"submitted google drive folder group={group_name}")
    return data


def update_asset_description(
    filename_sanitized: str,
    description: str,
    group_name: str = "newsalien2",
    stream_name: str = "astream",
    tag: Optional[List[str]] = None,
) -> Dict[str, Any]:
    c = app_client()
    res = c.collections.update_description(
        group_name=group_name,
        mode="vid_file",
        stream_name=stream_name,
        filename_sanitized=filename_sanitized,
        description=description,
        tag=tag or [],
    )
    data = obj_dict(res)
    log_info(f"updated description filename={filename_sanitized}")
    return data


def add_assets(
    collection_id: str,
    asset_ids: List[str],
    group_name: str = "newsalien2",
    stream_name: str = "astream",
) -> Dict[str, Any]:
    c = app_client()
    res = c.collections.add_assets(
        collection_id=collection_id,
        asset_ids=asset_ids,
        mode="vid_file",
        group_name=group_name,
        stream_name=stream_name,
    )
    data = obj_dict(res)
    log_info(f"added assets count={len(asset_ids)} collection_id={collection_id}")
    return data


def delete_collection_dry_run(group_name: str = "newsalien2", mode: str = "vid_file") -> Dict[str, Any]:
    c = app_client()
    res = c.collections.delete(group_name=group_name, mode=mode, scope="all", dry_run=True, confirm=False)
    data = obj_dict(res)
    log_info(f"delete dry_run group={group_name}")
    return data


def delete_collection_confirm(group_name: str, mode: str = "vid_file") -> Dict[str, Any]:
    c = app_client()
    res = c.collections.delete(group_name=group_name, mode=mode, scope="all", dry_run=False, confirm=True)
    data = obj_dict(res)
    log_info(f"delete confirm group={group_name}")
    return data


def search(
    query: str = "alien",
    group_name: str = "newsalien2",
    stream_name: str = "astream",
    limit: int = 10,
) -> Dict[str, Any]:
    c = app_client()
    res = c.searches.search_video(
        query_text=query,
        mode="vid_file",
        group_name=group_name,
        stream_name=stream_name,
        search_sources=["image"],
        search_combine_mode="union",
        limit=limit,
        image_emb_score_min=1.5,
        tracking_id="app_full_usage_search",
    )
    data = obj_dict(res)
    hits = data.get("data", [])
    log_info(f"search cnt_actual={data.get('cnt_actual', 0)} returned={len(hits)}")
    return data


def video_search_examples(
    group_name: str = "sdk_dummy_video",
    stream_name: str = "astream",
    limit: int = 5,
) -> Dict[str, Any]:
    out = {
        "image_only": search(
            query="dummy video",
            group_name=group_name,
            stream_name=stream_name,
            limit=limit,
        ),
        "image_only_page2": obj_dict(app_client().searches.search_video(
            query_text="dummy video",
            mode="vid_file",
            group_name=group_name,
            stream_name=stream_name,
            search_sources=["image"],
            search_combine_mode="union",
            offset=limit,
            limit=limit,
            image_emb_score_min=1.5,
            tracking_id="app_full_usage_video_search_page2",
        )),
        "video_group": obj_dict(app_client().searches.search_video(
            query_text="dummy video",
            video_group=f"vid_file-{group_name}",
            stream_name=stream_name,
            search_sources=["image"],
            search_combine_mode="union",
            limit=limit,
            image_emb_score_min=1.5,
            tracking_id="app_full_usage_video_group_search",
        )),
    }
    return out


def image_url(
    filename: str,
    ts_unix_13digits: str = "",
    group_name: str = "newsalien2",
    stream_name: str = "astream",
) -> Dict[str, Any]:
    c = app_client()
    res = c.images.get_url(
        mode="vid_file",
        group_name=group_name,
        modality="vid_img",
        stream_name=stream_name,
        filename=filename,
        ts_unix_13digits=ts_unix_13digits or None,
    )
    data = obj_dict(res)
    log_info(f"image_url found={data.get('found', False)}")
    return data


def image_from_url(
    url_pre_signed: str,
    output_path: str = "",
) -> Dict[str, Any]:
    c = app_client()
    img = c.images.get_image_from_url(url_pre_signed=url_pre_signed)
    output_path = output_path or os_image_path("image.webp")
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_bytes(img)
    out = {"output_path": output_path, "size_bytes": len(img)}
    log_info(f"image saved path={output_path} size_bytes={len(img)}")
    return out


def image_bulk_from_urls(urls: Optional[List[str]] = None) -> Dict[str, Any]:
    c = app_client()
    res = c.images.get_image_bulk_from_urls(urls=list(urls or []))
    data = obj_dict(res)
    log_info(f"bulk images records={len(data.get('records', []))}")
    return data


def image_from_hit(
    query: str = "alien",
    filename: str = "",
    ts_unix_13digits: str = "",
    output_path: str = "",
) -> Dict[str, Any]:
    cfg = AppConfig(query=query)
    found = search(query=cfg.query, group_name=cfg.group_name, stream_name=cfg.stream_name, limit=cfg.limit)
    hits = found.get("data", [])
    if not hits and not filename:
        raise ValueError("search returned no hits; pass filename and ts_unix_13digits explicitly")
    hit = hits[0] if hits else {}
    rec = image_record_from_hit(hit, cfg, filename=filename, ts_unix_13digits=ts_unix_13digits)
    if not rec.get("filename"):
        raise ValueError("cannot derive image filename from hit; pass filename explicitly")
    url_res = app_client().images.get_url(**rec)
    url_data = obj_dict(url_res)
    if not url_data.get("found") or not url_data.get("url_pre_signed"):
        raise ValueError(f"image URL not found for record: {rec}")
    output_path = output_path or os_image_path("hit_image.webp")
    img_res = image_from_url(url_data["url_pre_signed"], output_path=output_path)
    return {"search": found, "image_record": rec, "image_url": url_data, "image_file": img_res}


def image_bulk_from_search(query: str = "alien", limit: int = 3) -> Dict[str, Any]:
    cfg = AppConfig(query=query, limit=limit)
    found = search(query=cfg.query, group_name=cfg.group_name, stream_name=cfg.stream_name, limit=cfg.limit)
    records = [image_record_from_hit(hit, cfg) for hit in found.get("data", [])]
    records = [rec for rec in records if rec.get("filename")]
    if not records:
        raise ValueError("search returned no hits with image coordinates")
    url_res = app_client().images.get_url_bulk(records=records)
    url_data = obj_dict(url_res)
    urls = [r.get("url_pre_signed", "") for r in url_data.get("records", []) if r.get("url_pre_signed")]
    bulk_data = image_bulk_from_urls(urls=urls)
    return {"search": found, "image_records": records, "image_urls": url_data, "images": bulk_data}


def save_bulk_images(
    urls: Optional[List[str]] = None,
    dirout: str = "",
) -> Dict[str, Any]:
    dirout = dirout or os.path.join(DIR_IMAGE_OUT, "bulk")
    data = image_bulk_from_urls(urls=urls)
    Path(dirout).mkdir(parents=True, exist_ok=True)
    saved = []
    for i, rec in enumerate(data.get("records", [])):
        if not rec.get("found") or not rec.get("content_base64"):
            continue
        raw = base64.b64decode(rec["content_base64"])
        mime = str(rec.get("mime", "image/webp"))
        ext = "jpg" if "jpeg" in mime else "png" if "png" in mime else "webp"
        path = os.path.join(dirout, f"image_{i:03d}.{ext}")
        Path(path).write_bytes(raw)
        saved.append({"path": path, "size_bytes": len(raw)})
    log_info(f"bulk images saved={len(saved)}")
    return {"records": data.get("records", []), "saved": saved}


def index_jobs(group_name: str = "newsalien2", mode: str = "vid_file", limit: int = 20) -> Dict[str, Any]:
    c = app_client()
    res = c.indexes.jobs_list(mode=mode, group_name=group_name, limit=limit)
    data = obj_dict(res)
    log_info(f"index jobs total={data.get('total', len(data.get('data', [])))}")
    return data


def create_frame_index(
    group_name: str = "sdk_dummy_video",
    stream_name: str = "astream",
    embedding_model: Optional[str] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    c = app_client()
    res = c.indexes.create_index(
        mode="vid_file",
        group_name=group_name,
        stream_name=stream_name,
        index_type="vid_img_emb",
        modality="vid_img_emb",
        insert_mode="append",
        create_index=True,
        version="new_version",
        embedding_model=embedding_model,
        re_process=False,
        dry_run=dry_run,
    )
    data = obj_dict(res)
    log_info(f"frame index submitted job_id={data.get('job_id', '')} status={data.get('status', '')}")
    return data


def wait_for_index(
    job_id: str,
    timeout_sec: int = 900,
    poll_sec: int = 10,
) -> Dict[str, Any]:
    end_time = time.time() + int(timeout_sec)
    terminal = {"done", "completed", "complete", "success", "failed", "error", "cancelled", "canceled"}
    last: Dict[str, Any] = {}
    while True:
        last = index_status(job_id=job_id)
        status = str(last.get("status", "")).strip().lower()
        if status in terminal:
            return last
        if time.time() >= end_time:
            last["wait_timeout"] = True
            return last
        time.sleep(max(1, int(poll_sec)))


def create_index_dry_run(
    group_name: str = "newsalien2",
    modality: str = "image",
    stream_name: str = "astream",
) -> Dict[str, Any]:
    c = app_client()
    res = c.indexes.create_index(
        mode="vid_file",
        group_name=group_name,
        stream_name=stream_name,
        modality=modality,
        insert_mode="append",
        create_index=True,
        version="new_version",
        dry_run=True,
    )
    data = obj_dict(res)
    log_info(f"create index dry_run group={group_name} modality={modality}")
    return data


def index_status(job_id: str) -> Dict[str, Any]:
    c = app_client()
    res = c.indexes.index_status(job_id=job_id)
    data = obj_dict(res)
    log_info(f"index job_id={job_id} status={data.get('status', '')}")
    return data


def delete_index_dry_run(
    group_name: str = "newsalien2",
    version: str = "all",
    modality: str = "vid_img_emb",
) -> Dict[str, Any]:
    c = app_client()
    res = c.indexes.delete_index(
        mode="vid_file",
        group_name=group_name,
        version=version,
        modality=modality,
        dry_run=True,
        confirm=False,
    )
    data = obj_dict(res)
    log_info(f"delete index dry_run group={group_name} version={version}")
    return data


def video_e2e_process(
    collection_name: str = "sdk_dummy_video",
    sub_collection_name: str = "astream",
    filename: str = "dummy_video.mp4",
    embedding_model: Optional[str] = None,
    wait: bool = True,
    timeout_sec: int = 900,
    poll_sec: int = 10,
    dry_run_index: bool = False,
) -> Dict[str, Any]:
    upload = upload_dummy_video(
        collection_name=collection_name,
        sub_collection_name=sub_collection_name,
        filename=filename,
    )
    index = create_frame_index(
        group_name=collection_name,
        stream_name=sub_collection_name,
        embedding_model=embedding_model,
        dry_run=dry_run_index,
    )
    job_id = str(index.get("job_id", "") or "").strip()
    status: Dict[str, Any] = {}
    if wait and job_id:
        status = wait_for_index(job_id=job_id, timeout_sec=timeout_sec, poll_sec=poll_sec)
    searches = video_search_examples(group_name=collection_name, stream_name=sub_collection_name)
    return {
        "upload": upload,
        "index": index,
        "status": status,
        "searches": searches,
    }


def live_exhaustive_check(
    process_video: Union[bool, str] = True,
    timeout_sec: int = 900,
    poll_sec: int = 10,
) -> Dict[str, Any]:
    run_video = obj_bool(process_video)
    group_name = str_live_group()
    out: Dict[str, Any] = {"group_name": group_name}
    try:
        out["run"] = run()
        out["image_url_missing"] = image_url(
            filename="missing.mp4",
            ts_unix_13digits="0000000000000",
            group_name=group_name,
        )
        out["image_url_bulk_missing"] = obj_dict(app_client().images.get_url_bulk(records=[{
            "mode": "vid_file",
            "group_name": group_name,
            "modality": "vid_img",
            "stream_name": "astream",
            "filename": "missing.mp4",
            "ts_unix_13digits": "0000000000000",
        }]))
        out["upload_dummy_video"] = upload_dummy_video(collection_name=group_name)
        out["frame_index"] = create_frame_index(
            group_name=group_name,
            stream_name="astream",
            dry_run=not run_video,
        )
        job_id = str(out["frame_index"].get("job_id", "") or "").strip()
        if run_video and job_id:
            out["frame_index_status"] = wait_for_index(
                job_id=job_id,
                timeout_sec=timeout_sec,
                poll_sec=poll_sec,
            )
            status = str(out["frame_index_status"].get("status", "") or "").strip().lower()
            if out["frame_index_status"].get("wait_timeout"):
                raise TimeoutError(f"frame index job timed out: {out['frame_index_status']}")
            if status in {"failed", "error", "cancelled", "canceled"}:
                raise RuntimeError(f"frame index job failed: {out['frame_index_status']}")
        out["search_known_fixture"] = search()
        if run_video:
            out["search_uploaded_video"] = video_search_examples(group_name=group_name)
        out["delete_index_dry_run"] = obj_allow_api_error(
            lambda: delete_index_dry_run(group_name=group_name, modality="vid_img_emb"),
            [404],
        )
        out["delete_collection_dry_run"] = obj_allow_api_error(
            lambda: delete_collection_dry_run(group_name=group_name, mode="vid_file"),
            [404],
        )
        return out
    finally:
        try:
            delete_collection_confirm(group_name=group_name, mode="vid_file")
        except Exception as exc:
            log_warning(f"cleanup failed group={group_name}: {exc}")


def run() -> Dict[str, Any]:
    out = {
        "health": health(),
        "auth_check": auth_check(),
        "groups": list_groups(mode="vid_file"),
        "search": search(),
        "index_jobs": index_jobs(),
    }
    log_info("run complete; call image_from_hit or image_bulk_from_search to fetch image bytes")
    return out


if __name__ == "__main__":
    fire.Fire({
        "run": run,
        "health": health,
        "auth_check": auth_check,
        "list_groups": list_groups,
        "upload_asset": upload_asset,
        "upload_video": upload_video,
        "upload_dummy_video": upload_dummy_video,
        "upload_video_folder": upload_video_folder,
        "upload_metadata_jsonl": upload_metadata_jsonl,
        "upload_google_drive_folder": upload_google_drive_folder,
        "update_asset_description": update_asset_description,
        "add_assets": add_assets,
        "delete_collection_dry_run": delete_collection_dry_run,
        "delete_collection_confirm": delete_collection_confirm,
        "search": search,
        "video_search_examples": video_search_examples,
        "image_url": image_url,
        "image_from_url": image_from_url,
        "image_bulk_from_urls": image_bulk_from_urls,
        "image_from_hit": image_from_hit,
        "image_bulk_from_search": image_bulk_from_search,
        "save_bulk_images": save_bulk_images,
        "index_jobs": index_jobs,
        "create_frame_index": create_frame_index,
        "wait_for_index": wait_for_index,
        "create_index_dry_run": create_index_dry_run,
        "index_status": index_status,
        "delete_index_dry_run": delete_index_dry_run,
        "video_e2e_process": video_e2e_process,
        "live_exhaustive_check": live_exhaustive_check,
    })
