"""Yantrik Companion HTTP service — FastAPI app + entry point."""

from __future__ import annotations

import json
import logging
import os
import sys
import tempfile
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.responses import StreamingResponse

from yantrikdb.agent.background import BackgroundCognition
from yantrikdb.agent.companion import CompanionService
from yantrikdb.agent.config import CompanionConfig

log = logging.getLogger("yantrik.service")

# Shared state
_service: Optional[CompanionService] = None
_background: Optional[BackgroundCognition] = None
_voice = None  # VoiceProcessor, initialized in lifespan
_start_time: float = 0


# ── Request/Response Models ──


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    proactive_messages: list[dict] = []
    metadata: dict = {}


class StatusResponse(BaseModel):
    status: str
    uptime_seconds: float
    memory_count: int
    pending_urges: int
    last_think_triggers: int
    last_interaction_ago_seconds: float
    session_active: bool
    session_turns: int
    personality: Optional[dict] = None


# ── Lifespan ──


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _service, _background, _start_time

    config_path = app.state.config_path
    config = CompanionConfig.from_yaml(config_path) if config_path else CompanionConfig()

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, config.logging.level, logging.INFO),
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        handlers=[logging.StreamHandler()],
    )
    if config.logging.file:
        Path(config.logging.file).parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(config.logging.file)
        fh.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s"))
        logging.getLogger().addHandler(fh)

    # Initialize embedder (HTTP-based, uses llama-server /embedding endpoint)
    from yantrikdb.agent.embedder import LlamaEmbedder
    embed_url = config.yantrikdb.embedding_url or "http://localhost:8082"
    log.info("Connecting to embedding server at %s", embed_url)
    embedder = LlamaEmbedder(base_url=embed_url)
    # Quick health check
    try:
        test_emb = embedder.encode("test")
        log.info("Embedder ready (dim=%d from server)", len(test_emb))
    except Exception as e:
        log.warning("Embedding server not available: %s — recall disabled", e)
        embedder = None

    # Initialize YantrikDB
    from yantrikdb import YantrikDB
    log.info("Initializing YantrikDB at %s (dim=%d)", config.yantrikdb.db_path, config.yantrikdb.embedding_dim)
    Path(config.yantrikdb.db_path).parent.mkdir(parents=True, exist_ok=True)
    db = YantrikDB(config.yantrikdb.db_path, config.yantrikdb.embedding_dim, embedder=embedder)

    # Initialize companion service
    _service = CompanionService(db, config)
    _start_time = time.time()

    # Start background cognition
    _background = BackgroundCognition(_service)
    await _background.start()

    # Initialize voice processor
    global _voice
    from yantrikdb.agent.voice import VoiceProcessor
    _voice = VoiceProcessor()
    log.info("Voice processor ready (whisper + piper)")

    log.info("Yantrik Companion ready on %s:%d", config.server.host, config.server.port)
    yield

    # Shutdown
    if _background:
        await _background.stop()
    if _service:
        await _service.close()
    log.info("Yantrik Companion stopped")


# ── App ──

app = FastAPI(
    title="Yantrik Companion",
    description="Personal AI companion with cognitive memory",
    version="0.1.0",
    lifespan=lifespan,
)
app.state.config_path = None  # set by main()

# Static files for UI
_static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(_static_dir)), name="static")


# ── Routes ──


@app.get("/")
async def index():
    return FileResponse(str(_static_dir / "index.html"), media_type="text/html")


@app.get("/health")
async def health():
    return {"ok": True}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not _service:
        raise HTTPException(503, "Service not initialized")

    # Check for proactive messages to include
    proactive = _service.get_proactive_message()
    proactive_msgs = [proactive] if proactive else []

    try:
        result = await _service.handle_message(req.message)
    except Exception as e:
        log.error("Chat handler failed: %s", e, exc_info=True)
        raise HTTPException(500, f"Agent error: {e}")

    return ChatResponse(
        response=result.message,
        proactive_messages=proactive_msgs,
        metadata={
            "memories_recalled": result.memories_recalled,
            "urges_delivered": result.urges_delivered,
            "tool_calls": result.tool_calls_made,
        },
    )


@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    if not _service:
        raise HTTPException(503, "Service not initialized")

    async def generate():
        try:
            async for token in _service.handle_message_stream(req.message):
                yield f"data: {json.dumps({'token': token})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            log.error("Stream handler failed: %s", e, exc_info=True)
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/status", response_model=StatusResponse)
async def status():
    if not _service:
        raise HTTPException(503, "Service not initialized")

    stats = _service.db.stats()
    now = time.time()

    # Include personality snapshot
    personality = None
    try:
        profile = _service.db.get_personality()
        personality = profile
    except Exception:
        pass

    return StatusResponse(
        status="running",
        uptime_seconds=round(now - _start_time, 1),
        memory_count=stats.get("active_memories", 0),
        pending_urges=_service.urge_queue.count_pending(),
        last_think_triggers=len(_service._pending_triggers),
        last_interaction_ago_seconds=round(now - _service.last_interaction_ts, 1),
        session_active=_service.session_turn_count > 0,
        session_turns=_service.session_turn_count,
        personality=personality,
    )


@app.get("/urges")
async def get_urges():
    if not _service:
        raise HTTPException(503, "Service not initialized")
    return {"urges": _service.urge_queue.get_pending()}


@app.post("/urges/{urge_id}/suppress")
async def suppress_urge(urge_id: str):
    if not _service:
        raise HTTPException(503, "Service not initialized")
    ok = _service.urge_queue.suppress(urge_id)
    if not ok:
        raise HTTPException(404, "Urge not found or already resolved")
    return {"suppressed": True}


@app.get("/personality")
async def get_personality():
    if not _service:
        raise HTTPException(503, "Service not initialized")
    try:
        profile = _service.db.get_personality()
        return profile
    except Exception as e:
        log.error("get_personality failed: %s", e, exc_info=True)
        raise HTTPException(500, f"Personality error: {e}")


@app.get("/history")
async def get_history(limit: int = 20):
    if not _service:
        raise HTTPException(503, "Service not initialized")
    history = _service.conversation_history[-limit:]
    return {"turns": history, "session_turns": _service.session_turn_count}


# ── Voice Endpoints ──


@app.post("/voice/stt")
async def speech_to_text(audio: UploadFile = File(...)):
    """Transcribe uploaded audio to text."""
    if not _voice:
        raise HTTPException(503, "Voice processor not available")

    suffix = ".webm" if "webm" in (audio.content_type or "") else ".wav"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
        f.write(await audio.read())
        tmp_path = f.name

    try:
        text = await _voice.transcribe(tmp_path)
        return {"text": text}
    except Exception as e:
        log.error("STT failed: %s", e, exc_info=True)
        raise HTTPException(500, f"Transcription failed: {e}")
    finally:
        os.unlink(tmp_path)
        wav_path = tmp_path + ".wav"
        if os.path.exists(wav_path):
            os.unlink(wav_path)


@app.post("/voice/tts")
async def text_to_speech(req: ChatRequest):
    """Synthesize text to speech. Returns WAV audio."""
    if not _voice:
        raise HTTPException(503, "Voice processor not available")

    try:
        wav_path = await _voice.synthesize(req.message)
        return FileResponse(
            wav_path,
            media_type="audio/wav",
            background=None,
        )
    except Exception as e:
        log.error("TTS failed: %s", e, exc_info=True)
        raise HTTPException(500, f"Speech synthesis failed: {e}")


# ── Entry Point ──


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Yantrik Companion Service")
    parser.add_argument("--config", "-c", type=str, help="Path to config YAML")
    parser.add_argument("--host", type=str, default=None)
    parser.add_argument("--port", type=int, default=None)
    args = parser.parse_args()

    if args.config:
        config = CompanionConfig.from_yaml(args.config)
    else:
        config = CompanionConfig()

    host = args.host or config.server.host
    port = args.port or config.server.port

    app.state.config_path = args.config

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level=config.logging.level.lower(),
    )


if __name__ == "__main__":
    main()
