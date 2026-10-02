"""Create a 10-frame color video, upload it, index it, and verify color search.

Usage:
  pip install vmodal
  export VMODAL_API_KEY=ak_xxx
  python examples/index_example.py run
"""
from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
import os,sys
import fire
import re
import shutil
import subprocess
import tempfile
import time
import logging

from vmodal import SyncClient

logging.basicConfig(level=logging.INFO, format="%(message)s")
log_info = logging.info


MODE = "vid_file"
STREAM = "astream"
INDEX_TYPE = "vid_img_emb"
MODALITY_INDEX = "vid_img_emb"
MODALITY_RAW = "vid_raw"
OK_STATUS = {"success", "succeeded", "done", "completed", "ok"}
FAIL_STATUS = {"failed", "failure", "error", "cancelled", "canceled", "dead_letter"}
FRAME_COLOR_TS = {
    "red": {"0000000000000"},
    "blue": {"0000000002000"},
}


def os_video_path() -> str:
    return os.path.join(tempfile.gettempdir(), "vmodal_examples", "vid_10frames.mp4")


def os_create_color_video(path: str = "") -> str:
    path = path or os_video_path()
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg is required to create the sample mp4")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    red = "160+mod(X*3+Y*2,96)"
    green = "160+mod(X*2+Y*3,96)"
    blue = "160+mod(X+Y*4,96)"
    low1 = "mod(X*5+Y*3+N*17,56)"
    low2 = "mod(X*2+Y*7+N*13,56)"
    expr = (
        "geq="
        f"r='if(eq(N,0),{red},if(eq(N,2),{low1},if(eq(N,4),{red},if(eq(N,6),{red},if(eq(N,8),{red},{low2})))))':"
        f"g='if(eq(N,1),{green},if(eq(N,3),{green},if(eq(N,5),{green},if(eq(N,6),{green},if(eq(N,8),{green},{low1})))))':"
        f"b='if(eq(N,2),{blue},if(eq(N,4),{blue},if(eq(N,5),{blue},if(eq(N,6),{blue},if(eq(N,9),{blue},{low2})))))',"
        "format=yuv420p"
    )
    cmd = [
        ffmpeg,
        "-y",
        "-v", "error",
        "-f", "lavfi",
        "-i", "nullsrc=s=160x120:r=1:d=10",
        "-vf", expr,
        "-frames:v", "10",
        "-r", "1",
        path,
    ]
    subprocess.run(cmd, check=True)
    log_info("created video path=%s" % path)
    return path


def str_live_group(prefix: str = "sdk_color_idx") -> str:
    group = os.environ.get("SDK_INDEX_EXAMPLE_GROUP", "").strip()
    if group:
        return group
    tail = str(int(time.time() * 1000))[-8:]
    return f"{prefix}_{tail}".lower()


def app_client() -> SyncClient:
    return SyncClient.from_env()


def obj_dict(obj: Any) -> Dict[str, Any]:
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if isinstance(obj, dict):
        return dict(obj)
    return dict(getattr(obj, "__dict__", {}) or {})


def str_status(obj: Any) -> str:
    return str(obj_dict(obj).get("status") or "").strip().lower()


def str_ts13(item: Any) -> str:
    data = obj_dict(item)
    raw = str(data.get("ts_unix") or "").strip()
    if raw:
        digits = "".join(ch for ch in raw if ch.isdigit())
        if digits:
            return digits.zfill(13)[-13:]
    vals = re.findall(r"\d{13}", " ".join(str(v) for v in data.values()))
    return vals[-1] if vals else ""


def int_version_lancedb(status_obj: Any) -> int:
    data = obj_dict(status_obj)
    result = data.get("result") if isinstance(data.get("result"), dict) else {}
    vals = [
        data.get("version_lancedb"),
        data.get("version"),
        result.get("version_lancedb"),
        result.get("version"),
    ]
    for val in vals:
        txt = str(val or "").strip().lower().lstrip("v")
        if txt.isdigit():
            return int(txt)
    return 0


def upload_video(c: SyncClient, video_path: str, group_name: str) -> Dict[str, Any]:
    res = c.collections.video_upload(
        filepath_local=video_path,
        collection_name=group_name,
        sub_collection_name=STREAM,
        mode=MODE,
        modality=MODALITY_RAW,
    )
    data = obj_dict(res)
    log_info("uploaded video group=%s filename=%s" % (group_name, data.get("filename", "")))
    return data


def start_indexation(c: SyncClient, group_name: str) -> Dict[str, Any]:
    res = c.indexes.create_index(
        mode=MODE,
        group_name=group_name,
        stream_name=STREAM,
        index_type=INDEX_TYPE,
        modality=MODALITY_INDEX,
        insert_mode="append",
        create_index=True,
        version="new_version",
        re_process=True,
        dry_run=False,
    )
    data = obj_dict(res)
    log_info("started indexation group=%s job_id=%s" % (group_name, data.get("job_id", "")))
    return data


def poll_indexation(c: SyncClient, job_id: str, timeout_sec: int = 1800, poll_sec: int = 10) -> Dict[str, Any]:
    end_time = time.time() + int(timeout_sec)
    last: Dict[str, Any] = {}
    while time.time() <= end_time:
        res = c.indexes.index_status(job_id=job_id)
        last = obj_dict(res)
        status = str_status(res)
        log_info("indexation status job_id=%s status=%s" % (job_id, status))
        if status in OK_STATUS:
            return last
        if status in FAIL_STATUS:
            raise AssertionError("indexation failed: %s" % last)
        time.sleep(max(1, int(poll_sec)))
    raise AssertionError("indexation timeout after %s sec: %s" % (timeout_sec, last))


def search_color(c: SyncClient, group_name: str, color: str, version_lancedb: int = 0) -> Dict[str, Any]:
    res = c.searches.search_video(
        query_text=color,
        mode=MODE,
        group_name=group_name,
        stream_name=STREAM,
        search_sources=["image"],
        search_combine_mode="union",
        limit=1,
        offset=0,
        text_emb_score_min=0.0,
        image_emb_score_min=0.0,
        version_lancedb=version_lancedb,
    )
    data = obj_dict(res)
    rows = list(data.get("data") or [])
    assert rows, "search returned no rows for color=%s response=%s" % (color, data)
    top = rows[0]
    ts13 = str_ts13(top)
    expected = FRAME_COLOR_TS[color]
    assert ts13 in expected, (
        "top-1 color mismatch color=%s expected_ts=%s actual_ts=%s top=%s"
        % (color, sorted(expected), ts13, obj_dict(top))
    )
    log_info("top-1 color ok color=%s ts=%s" % (color, ts13))
    return data


def run(
    group_name: str = "",
    timeout_sec: int = 1800,
    poll_sec: int = 10,
) -> Dict[str, Any]:
    video_path = os_create_color_video()
    group_name = group_name or str_live_group()
    c = app_client()

    upload = upload_video(c, video_path=video_path, group_name=group_name)
    job = start_indexation(c, group_name=group_name)
    job_id = str(job.get("job_id") or "").strip()
    assert job_id, "indexation did not return job_id: %s" % job

    status = poll_indexation(c, job_id=job_id, timeout_sec=timeout_sec, poll_sec=poll_sec)
    version_lancedb = int_version_lancedb(status)
    blue = search_color(c, group_name=group_name, color="blue", version_lancedb=version_lancedb)
    red = search_color(c, group_name=group_name, color="red", version_lancedb=version_lancedb)
    return {
        "video_path": video_path,
        "group_name": group_name,
        "upload": upload,
        "job": job,
        "status": status,
        "version_lancedb": version_lancedb,
        "search_blue": blue,
        "search_red": red,
    }


if __name__ == "__main__":
    fire.Fire()
