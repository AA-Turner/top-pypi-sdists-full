from __future__ import annotations

from typing import Any, Dict, Tuple, Optional

import os
import json
import logging

from ..imports import *
from .manager import *

logger = logging.getLogger(__name__)


# ───────────────────────────── Registry (DB + filesystem) ─────────────────────────────




# ──────────────────────────────── Text ingestion ────────────────────────────────


def get_text(
    *args,
    text: Optional[str] = None,
    url: Optional[str] = None,
    file_path: Optional[str] = None,
    audio_path: Optional[str] = None,
    video_url: Optional[str] = None,
    video_path: Optional[str] = None,
    video_id: Optional[str] = None,
    data_url: Optional[str] = None,
    **kwargs,
) -> Optional[str]:
    """
    Unified entrypoint:

    1. Explicit text
    2. Audio / video → Whisper
    3. URL / file ingestion → soup / file read + registry
    4. Fallback to DB
    """
    # 1) Explicit text
    if text is not None:
        if video_id:
            db_upsert(video_id, {"text": text})
        if isinstance(text, list):
            text = " ".join(str(t) for t in text if t is not None)
        elif text is None:
            text = ""

        return text

    # 2) Audio/video → whisper
    if audio_path or video_url or video_path:
        text = get_whisper_text(
            *args,
            audio_path=audio_path,
            video_url=video_url,
            video_path=video_path,
            **kwargs,
        )
        if video_id and text:
            db_upsert(video_id, {"whisper": {"text": text}})
        if isinstance(text, list):
            text = " ".join(str(t) for t in text if t is not None)
        elif text is None:
            text = ""

        return text

    # 3) URL / file ingestion
    if url or file_path:
        if url:
            file_path = save_url_html(
                url=url, documents_root=DEFAULT_DOCUMENTS_ROOT
            )
        

        dirname = os.path.dirname(file_path)
        basename = os.path.basename(file_path)
        filename, ext = os.path.splitext(basename)

        # Prefer live fetch from URL, fallback to local file
     
        text = read_file_as_text(file_path) if is_file(file_path) else get_soup_text(url)
        if text is None:
            text = ""
        write_to_file(contents=text,file_path=file_path)
       
        # Save a simple JSON blob in the documents root
        save_file = os.path.join(dirname, "info.json")
        safe_dump_to_file(data={filename: filename,'file_path':file_path}, file_path=save_file)
        
        # Mirror in registry as cache
        info = get_infoRegistry().add_file(
            file_path=file_path,
            url=url,
            save_file=save_file,
            video_id=video_id,
            data_url=data_url,
        )

        # DB as single source of truth
        if video_id and text:
            db_upsert(video_id, {"info": info, "text": text})

        if text and info.get("text_path"):
            write_to_file(info["text_path"], text)
        if isinstance(text, list):
            text = " ".join(str(t) for t in text if t is not None)
        elif text is None:
            text = ""

        return text

    # 4) Last chance → DB only
    if video_id:
        rec = db_get(video_id)
        if rec and getattr(rec, "info", None):
            return rec.info.get("text")

    return None


def get_soup_text(url: str) -> str:
    soup = get_soup(url)
    return soup.text


# ─────────────────────── Video info helpers (yt-dlp, paths) ───────────────────────


def get_video_info_spec(
    video_url: Optional[str] = None,
    video_path: Optional[str] = None,
    key: Optional[str] = None,
    download: Optional[bool] = None,
    force_refresh: bool = False,
):
    """
    Convenience wrapper around infoRegistry.get_video_info + VideoDownloader.

    Returns:
        - If key is provided: info[key] or None
        - Else: full info dict (or {})
    """
    if (not video_path and not video_url) or (
        video_path and not is_file(video_path) and not video_url
    ):
        return None

    if video_path and not video_url:
        video_id = generate_video_id(video_path)
    else:
        video_url = get_corrected_url(video_url)
        video_id = get_video_id(video_url)

    registry = infoRegistry()
    info = (
        registry.get_video_info(
            url=video_url,
            video_id=video_id,
            video_path=video_path,
            force_refresh=force_refresh,
        )
        or {}
    )
    video_info = info.get("info") or {}

    # If we don't have a local path, optionally trigger a download manager
    if video_url and (not video_path or (video_path and not is_file(video_path))):
        video_mgr = VideoDownloader(
            url=video_url,
            download_video=True if download else False,
        )
        extra_info = get_info_from_mgr(video_mgr) or {}
        video_info.update(extra_info)

    if video_info or (
        video_path and is_file(video_path) and is_media_type(video_path, categories=["video"])
    ):
        if key:
            return video_info.get(key)
    return video_info


def get_schema_paths(
    *args,
    video_url: Optional[str] = None,
    video_path: Optional[str] = None,
    video_info: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    if video_info and isinstance(video_info, dict) and video_info.get("schema_paths"):
        return video_info.get("schema_paths")
    return get_video_info_spec(
        video_url=video_url,
        video_path=video_path,
        key="schema_paths",
    )


# ───────────────────────────── Whisper path helpers ─────────────────────────────


def get_whisper_video_info(
    *args,
    video_url: Optional[str] = None,
    video_path: Optional[str] = None,
    video_info: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """
    Return a video_info dict suitable for whisper usage.
    Delegates to get_video_info (imported from .manager).
    """
    if video_info and isinstance(video_info, dict) and video_info.get("video_path"):
        video_path = video_info.get("video_path")
    video_info = get_video_info(  # noqa: F405 - expected from .manager
        video_url=video_url,
        video_path=video_path,
        download=True,
    )
    return video_info


def extract_audio_from_video(
    video_path: str,
    audio_path: Optional[str] = None,
):
    """Extract audio from a video file using moviepy."""
    if audio_path is None:
        video_directory = os.path.dirname(video_path)
        audio_path = video_directory
    if os.path.isdir(audio_path):
        audio_path = os.path.join(audio_path, "audio.wav")
    try:
        logger.info(f"Extracting audio from {video_path} to {audio_path}")
        video = mp.VideoFileClip(video_path)  # noqa: F405 - mp from imports
        video.audio.write_audiofile(audio_path)
        video.close()
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file {audio_path} was not created.")
        logger.info(f"Audio extracted successfully: {audio_path}")
        return audio_path
    except Exception as e:
        logger.error(f"Error extracting audio from {video_path}: {e}")
        return None


def get_whisper_audio_path(
    *args,
    audio_path: Optional[str] = None,
    video_url: Optional[str] = None,
    video_path: Optional[str] = None,
    video_info: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """
    Ensure we have an audio_path for whisper (from existing file or extracted from video).
    """
    if audio_path and os.path.isfile(audio_path):
        return audio_path

    video_info = (
        get_whisper_video_info(
            video_url=video_url,
            video_path=video_path,
            video_info=video_info,
        )
        or {}
    )

    video_path = video_path or video_info.get("video_path")
    audio_path = audio_path or video_info.get("audio_path")

    extract_audio_from_video(video_path=video_path, audio_path=audio_path)
    return audio_path


def get_whisper_video_path(
    *args,
    video_url: Optional[str] = None,
    video_path: Optional[str] = None,
    **kwargs,
):
    return get_video_info_spec(
        video_url=video_url,
        video_path=video_path,
        download=True,
        key="video_path",
    )


def get_metadata_path(
    *args,
    video_url: Optional[str] = None,
    video_path: Optional[str] = None,
    **kwargs,
):
    return get_video_info_spec(
        video_url=video_url,
        video_path=video_path,
        download=True,
        key="metadata_path",
    )


def get_whisper_path(
    *args,
    video_url: Optional[str] = None,
    video_path: Optional[str] = None,
    **kwargs,
):
    return get_video_info_spec(
        video_url=video_url,
        video_path=video_path,
        download=True,
        key="whisper_path",
    )


def get_whisper_audio_paths(
    video_url: Optional[str] = None,
    video_path: Optional[str] = None,
    force_refresh: bool = False,
):
    """
    Convenience helper → get or derive audio_path for the video.
    """
    if (not video_path and not video_url) or (
        video_path and not is_file(video_path) and not video_url
    ):
        return None

    if video_path and not video_url:
        video_id = generate_video_id(video_path)
    else:
        video_url = get_corrected_url(video_url)
        video_id = get_video_id(video_url)

    registry = infoRegistry()
    info = (
        registry.get_video_info(
            url=video_url,
            video_id=video_id,
            video_path=video_path,
            force_refresh=force_refresh,
        )
        or {}
    )
    video_info = info.get("info") or {}

    if video_url and (not video_path or (video_path and not is_file(video_path))):
        video_mgr = VideoDownloader(
            url=video_url,
            download_video=True,
        )
        extra_info = get_info_from_mgr(video_mgr) or {}
        video_info.update(extra_info)

    # If registry already knows an audio_path and it's real, just use it
    if video_info.get("audio_path") and is_file(video_info["audio_path"]):
        return video_info["audio_path"]

    # Otherwise derive it via whisper helpers
    if video_path and is_file(video_path) and is_media_type(
        video_path, categories=["video"]
    ):
        return get_whisper_audio_path(
            audio_path=None,
            video_url=video_url,
            video_path=video_path,
            video_info=video_info,
        )

    return None


# ───────────────────────────── JSON-safe helpers ─────────────────────────────


def _safe_read_from_json(
    file_path: Optional[str],
    remove_if_corrupt: bool = True,
    default: Optional[dict] = None,
) -> dict:
    """
    Read JSON safely. If the file is corrupt, optionally remove it and return default.
    """
    if not file_path or not os.path.isfile(file_path):
        return default if default is not None else {}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Corrupt JSON detected at {file_path}: {e}")
        if remove_if_corrupt:
            try:
                os.remove(file_path)
                logger.warning(f"Removed corrupt JSON file: {file_path}")
            except Exception as rm_err:
                logger.error(f"Failed to remove corrupt JSON {file_path}: {rm_err}")
        return default if default is not None else {}


def try_get_read(file_path: Optional[str]):
    """
    Raw read helper → returns dict (or {}) on success, False on unexpected error.
    """
    try:
        return _safe_read_from_json(file_path)
    except Exception:
        return False


def try_get_data(file_path: Optional[str]):
    """
    Wrapper used by whisper result code:
      - Guarantees file exists with at least {} JSON.
      - Returns the dict loaded from file.
    """
    data = try_get_read(file_path)
    if not file_path or not is_file(file_path) or not data:
        safe_dump_to_json(data={}, file_path=file_path)
        return {}
    return data


# ───────────────────────────── Whisper result wrappers ─────────────────────────────


def get_whisper_result(
    *args,
    audio_path: Optional[str] = None,
    video_url: Optional[str] = None,
    video_path: Optional[str] = None,
    **kwargs,
):
    """
    Idempotent whisper runner:

    - If whisper_path JSON exists and is valid → load + return
    - Else → compute via run_whisper_func + persist JSON
    """
    whisper_path = get_whisper_path(
        video_url=video_url,
        video_path=video_path,
    )
    data = try_get_data(whisper_path)
    if not data:
        audio_path = get_whisper_audio_path(
            audio_path=audio_path,
            video_url=video_url,
            video_path=video_path,
        )
        whisper_result = run_whisper_func(
            whisper_transcribe,
            *args,
            audio_path=audio_path,
            **kwargs,
        )

        safe_dump_to_file(
            data=whisper_result,
            file_path=whisper_path,
        )
        return whisper_result
    return data


def get_whisper_text(
    *args,
    audio_path: Optional[str] = None,
    video_url: Optional[str] = None,
    video_path: Optional[str] = None,
    **kwargs,
) -> Optional[str]:
    result = get_whisper_result(
        *args,
        audio_path=audio_path,
        video_url=video_url,
        video_path=video_path,
        **kwargs,
    ) or {}
    return result.get("text")


def get_whisper_segments(
    *args,
    audio_path: Optional[str] = None,
    video_url: Optional[str] = None,
    video_path: Optional[str] = None,
    **kwargs,
):
    result = get_whisper_result(
        *args,
        audio_path=audio_path,
        video_url=video_url,
        video_path=video_path,
        **kwargs,
    ) or {}
    return result.get("segments")


# ───────────────────────────── Request arg parsing ─────────────────────────────


def get_args_kwargs(req) -> Tuple[list, Dict[str, Any]]:
    """
    Extracts positional args and keyword args from a JSON request.

    Client should send:
        {
            "args": [arg1, arg2, ...],
            "kw1": "val1",
            "kw2": "val2"
        }

    Returns:
        tuple: (args_list, kwargs_dict)
    """
    data = req.get_json(force=True) or {}
    args = data.pop("args", [])
    if not isinstance(args, (list, tuple)):
        raise ValueError(f"Expected 'args' to be list/tuple, got {type(args)}")
    return list(args), data
