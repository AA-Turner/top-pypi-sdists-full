"""Small, reproducible inputs for real worker task calls from the fit station."""
from __future__ import annotations

import base64
import io
import json
import struct
import time
import urllib.error
import urllib.request
import wave
import zlib


TASK_PATHS = {
    "text-generation": "/v1/chat/completions",
    "image-text-to-text": "/v1/chat/completions",
    "embed": "/v1/embeddings",
    "feature-extraction": "/v1/embeddings",
    "asr": "/v1/audio/transcriptions",
    "automatic-speech-recognition": "/v1/audio/transcriptions",
    "summarization": "/v1/summarize",
    "image-generation": "/v1/images/generations",
    "text-to-image": "/v1/images/generations",
    "text-to-audio": "/v1/audio/speech",
    "text-to-speech": "/v1/audio/speech",
    "text-to-video": "/v1/videos/generations",
    "image-to-video": "/v1/videos/generations",
}


def _png() -> str:
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
    raw = b"".join(b"\x00" + b"\xff\x00\x00" * 16 for _ in range(16))
    data = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 16, 16, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))
    return base64.b64encode(data).decode("ascii")


def _wav() -> str:
    out = io.BytesIO()
    with wave.open(out, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)
        wav.writeframes(b"\x00\x00" * 8000)
    return base64.b64encode(out.getvalue()).decode("ascii")


def fixture(task: str, model: str, knobs: dict | None = None) -> dict:
    body: dict = {"model": model}
    if knobs:
        body["knobs"] = knobs
    if task == "text-generation":
        body.update(messages=[{"role": "user", "content": "/no_think Reply with exactly: test passed"}],
                    max_tokens=96, chat_template_kwargs={"enable_thinking": False})
    elif task == "image-text-to-text":
        body.update(messages=[{"role": "user", "content": [
            {"type": "text", "text": "What color is this image? Answer briefly."},
            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + _png()}},
        ]}], max_tokens=32)
    elif task in ("embed", "feature-extraction"):
        body["input"] = "Hugpy fit station task test."
    elif task in ("asr", "automatic-speech-recognition"):
        body.update(file_b64=_wav(), response_format="json")
    elif task == "summarization":
        body.update(input="The council approved a new park on Tuesday. Construction begins next spring.", max_length=40)
    elif task in ("image-generation", "text-to-image"):
        body.update(prompt="A plain red square on a white background", size="256x256", n=1, num_inference_steps=1)
    elif task in ("text-to-audio", "text-to-speech"):
        body.update(input="Hugpy task test.", voice="default")
    elif task == "text-to-video":
        body.update(prompt="A red square on a white background", num_frames=4, width=256, height=256)
    elif task == "image-to-video":
        body.update(prompt="The red square moves right", image_b64=_png(), num_frames=4, width=256, height=256)
    else:
        raise ValueError(f"No station task method for {task}")
    return body


def run(worker: dict, task: str, model: str, lease_id: str, knobs: dict | None = None) -> tuple[dict, int]:
    if task not in TASK_PATHS:
        raise ValueError(f"No station task method for {task}")
    body = fixture(task, model, knobs)
    url = worker["url"].rstrip("/") + TASK_PATHS[task]
    headers = {"Content-Type": "application/json", "Accept": "application/json",
               "Authorization": "Bearer " + worker["key"], "X-Hugpy-Station-Lease": lease_id,
               "X-Task": task}
    request = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    began = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=300) as reply:
            raw = reply.read()
            content_type = reply.headers.get("Content-Type", "")
            status = reply.status
    except urllib.error.HTTPError as exc:
        raw = exc.read(10000)
        content_type = exc.headers.get("Content-Type", "")
        status = exc.code
    elapsed = round(time.monotonic() - began, 3)
    result = {"task": task, "model_key": model, "endpoint": TASK_PATHS[task],
              "status": status, "seconds": elapsed, "ok": 200 <= status < 300}
    if "json" not in content_type:
        result.update(content_type=content_type, output_bytes=len(raw))
        result["ok"] = result["ok"] and bool(raw) and (content_type.startswith("audio/") or content_type.startswith("video/") or content_type.startswith("image/"))
        if not result["ok"]:
            result["error"] = "Worker returned no usable media output"
        return result, status
    try:
        data = json.loads(raw)
    except (UnicodeDecodeError, ValueError):
        result["ok"] = False
        result["error"] = "Worker returned invalid JSON"
        return result, status
    if not result["ok"]:
        result["error"] = data.get("error", data) if isinstance(data, dict) else data
        return result, status
    if not isinstance(data, dict):
        result["ok"] = False
        result["error"] = "Worker returned an unexpected response"
        return result, status
    choices = data.get("choices")
    choice = choices[0] if isinstance(choices, list) and choices and isinstance(choices[0], dict) else {}
    message = choice.get("message") if isinstance(choice.get("message"), dict) else {}
    if "choices" in data:
        result["text"] = str(message.get("content") or "")[:1000]
        result["reasoning_only"] = not result["text"] and bool(message.get("reasoning_content"))
        result["finish_reason"] = choice.get("finish_reason")
    elif "summaries" in data:
        result["text"] = str((data.get("summaries") or [""])[0])[:1000]
    elif "text" in data:
        result["text"] = str(data["text"])[:1000]
    elif "data" in data:
        result["outputs"] = len(data.get("data") or [])
        first = (data.get("data") or [{}])[0]
        if isinstance(first, dict):
            if "embedding" in first:
                result["embedding_dimensions"] = len(first["embedding"])
            if "b64_json" in first:
                result["image_base64_bytes"] = len(first["b64_json"])
    result["timings"] = data.get("timings")
    result["usage"] = data.get("usage")
    result["request_id"] = (data.get("hugpy") or {}).get("request_id")
    if task in ("text-generation", "image-text-to-text", "summarization") and not result.get("text", "").strip():
        result.update(ok=False, error="No user-visible text was returned")
    elif task in ("embed", "feature-extraction") and not result.get("embedding_dimensions"):
        result.update(ok=False, error="No nonempty embedding was returned")
    elif task in ("asr", "automatic-speech-recognition"):
        result["ok"] = isinstance(data.get("text"), str) and result["ok"]
        result["fixture_note"] = "Silent audio checks execution only; any nonempty transcript is a hallucination, not a transcription-quality pass"
    elif task in ("text-to-image", "image-generation") and not result.get("image_base64_bytes"):
        result.update(ok=False, error="No generated image bytes were returned")
    elif task in ("text-to-audio", "text-to-speech", "text-to-video", "image-to-video"):
        artifacts = data.get("artifacts") or data.get("data") or []
        result["ok"] = result["ok"] and bool(artifacts)
        result["outputs"] = len(artifacts)
        if not result["ok"]:
            result["error"] = "No generated media artifact was returned"
    if result.get("reasoning_only"):
        result["ok"] = False
        result["error"] = "Only reasoning tokens were returned; no user-visible answer"
    return result, status
