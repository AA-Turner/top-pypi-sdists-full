"""Public usage policy; model choice never grants management capabilities."""
from __future__ import annotations
import re
from hugpy_core.config import model_preferences

CHAT_MODELS = (
    "Qwen3.5-0.8B",
    "flux2-klein-9b-uncensored-text-encoder",
    "Qwen3-Coder-Next-GGUF",
)
# Public choices are a separate contract from the operator's task bindings.
# In particular, an empty binding table must not select an arbitrary fleet model.
DEFAULTS = {
    "text-generation": CHAT_MODELS[0],
    "image-text-to-text": "Qwen2.5-VL-3B-Instruct",
    "text-to-image": "sd-turbo", "image-to-image": "sd-turbo",
    "automatic-speech-recognition": "whisper-tiny",
    "feature-extraction": "all-MiniLM-L6-v2",
    "sentence-similarity": "all-MiniLM-L6-v2",
    "keyword-extraction": CHAT_MODELS[0],
    "depth-estimation": "Depth-Anything-V2-Small-hf",
    "object-detection": "detr-resnet-50",
    "image-classification": "vit-base-patch16-224",
    "image-segmentation": "segformer-b0-finetuned-ade-512-512",
}
DOWNLOAD_MESSAGE = "Download Hugpy to use other models and own your data."
MEDIA_TASKS = {
    "transcribe": "automatic-speech-recognition", "summarize": "text-generation",
    "keywords": "keyword-extraction", "embed": "feature-extraction",
    "similarity": "sentence-similarity", "vision": "image-text-to-text",
    "imagine": "text-to-image", "depth": "depth-estimation",
    "detect": "object-detection", "classify": "image-classification",
    "segment": "image-segmentation",
}
LOCAL_OPERATIONS = {
    "/api/media/upload", "/api/uploads", "/api/media/extract",
    "/api/media/document_inspect", "/api/media/document_page", "/api/media/document_search",
    "/api/session/ping", "/api/session/end", "/api/session/file",
    "/api/media/session/ping", "/api/media/session/end", "/api/media/session/file",
    "/api/video/ingest", "/api/video/upload",
}
READ = {
    "/api/version", "/api/media/health", "/api/media/capabilities", "/api/media/manifest",
    "/api/prompt/tasks", "/v1/task-bindings", "/v1/models", "/api/models",
    "/api/models/database", "/api/fleet/workers", "/api/llm/workers", "/api/video/job", "/api/video/media",
}


def task_for(path, body):
    if path == "/v1/chat/completions":
        return "text-generation"
    if path == "/api/video/jobs/generate_image":
        return "image-to-image" if any(p.get("kind") == "image" for p in body.get("parts", []) if isinstance(p, dict)) else "text-to-image"
    if path.startswith("/api/media/"):
        return MEDIA_TASKS.get(path.rsplit("/", 1)[-1])
    if path == "/api/prompt":
        task = body.get("task", "text-generation")
        return task if task in model_preferences.read()["media"] else None
    return None


def permitted(path, method):
    if any(part in (".", "..") for part in path.split("/")) or any(c in path for c in ("%", "\\", "//")):
        return False
    path = path.rstrip("/")
    return ((method in ("GET", "HEAD") and (path in READ or re.fullmatch(r"/api/video/jobs/[A-Za-z0-9_-]+", path)))
            or (method == "POST" and (path in LOCAL_OPERATIONS or path in {
                "/v1/chat/completions", "/api/prompt", "/api/video/jobs/generate_image",
                *["/api/media/" + name for name in MEDIA_TASKS],
            })))


def pin_models(path, body, defaults):
    """Reject nested overrides, and pin omitted selections before dispatch.

    The operator's per-page, per-task public choices are authoritative. More
    permits other compatible catalog models only when explicitly enabled.
    """
    if not isinstance(body, dict):
        raise ValueError("Expected a JSON object.")
    task = task_for(path, body)
    if task is None:
        if path in LOCAL_OPERATIONS:
            return dict(body)
        raise ValueError(DOWNLOAD_MESSAGE)
    surface = "video" if path.startswith("/api/video/") else "media"
    choices = model_preferences.public_models(surface, task)
    default = choices[0] if choices else None
    allowed = set(choices)
    if not allowed:
        raise ValueError("No public default is configured for this operation.")
    chosen = body.get("model") or body.get("model_key") or body.get("model_id") or default
    if chosen not in allowed:
        raise ValueError(DOWNLOAD_MESSAGE)

    def inspect(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key in ("model", "model_key", "model_id") and item and item not in allowed:
                    raise ValueError(DOWNLOAD_MESSAGE)
                if key in ("worker", "worker_id", "endpoint", "base_url", "fallback", "fallback_model", "pool", "api_key", "authorization", "headers", "tools", "tool_choice") and item:
                    raise ValueError("Public requests use the configured service route.")
                inspect(item)
        elif isinstance(value, list):
            for item in value: inspect(item)
    inspect(body)
    result = dict(body)
    for key in ("model", "model_key", "model_id"):
        result.pop(key, None)
    result["model" if path == "/v1/chat/completions" or path.startswith("/api/media/") else "model_id" if path == "/api/video/jobs/generate_image" else "model_key"] = chosen
    if task == "text-generation":
        for key in ("max_tokens", "max_new_tokens"):
            if key in result:
                result[key] = max(1, min(2048, int(result[key])))
        result.setdefault("max_tokens" if path == "/v1/chat/completions" else "max_new_tokens", 1024)
    if path == "/api/video/jobs/generate_image" and any(p.get("kind") not in ("text", "image") for p in result.get("parts", []) if isinstance(p, dict)):
        raise ValueError("Public Video supports images; other operations are demos. " + DOWNLOAD_MESSAGE)
    return result
