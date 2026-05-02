"""Voice — text-to-speech via the user's fleet TTS services.

Submits an audio_generation task to the PastaWater broker (or brain in
direct mode), polls for the result, downloads the audio file, and plays
it locally via the system's audio player.

Supported TTS models on the fleet:
  - audio-chatterbox  (Chatterbox TTS, voice cloning)
  - audio-fish        (Fish Speech 1.5)
  - audio-qwen-tts    (Qwen3 TTS)
  - audio-dia         (Dia 1.6B)

The model can call this via the speak_text tool. Users can toggle
continuous voice mode with /voice on, which auto-speaks every
assistant response.

Audio playback chain (first one available wins):
  ffplay → mpv → aplay → afplay → paplay → play (sox)
"""

import os
import shutil
import subprocess
import tempfile
import time
from typing import Optional

import requests


# Default TTS model — falls through to whichever audio service is running
DEFAULT_TTS_MODELS = ["audio-chatterbox", "audio-fish", "audio-qwen-tts", "audio-dia"]

PLAYBACK_COMMANDS = [
    ("ffplay", ["-nodisp", "-autoexit", "-loglevel", "quiet"]),
    ("mpv",    ["--no-video", "--really-quiet"]),
    ("aplay",  ["-q"]),
    ("afplay", []),
    ("paplay", []),
    ("play",   ["-q"]),  # sox
]


def get_playback_command() -> Optional[tuple[str, list]]:
    """Find the first available audio playback command."""
    for cmd, args in PLAYBACK_COMMANDS:
        if shutil.which(cmd):
            return cmd, args
    return None


def play_audio_file(path: str) -> tuple[bool, str]:
    """Play an audio file. Returns (ok, message)."""
    if not os.path.exists(path):
        return False, f"audio file not found: {path}"
    cmd_info = get_playback_command()
    if not cmd_info:
        return False, "no audio player found (install ffplay, mpv, aplay, afplay, paplay, or sox)"
    cmd, args = cmd_info
    try:
        # Run synchronously so the function blocks until playback ends
        result = subprocess.run(
            [cmd, *args, path],
            capture_output=True,
            timeout=300,
        )
        if result.returncode != 0:
            return False, f"{cmd} failed: {result.stderr.decode('utf-8', 'replace')[:200]}"
        return True, f"played via {cmd}"
    except subprocess.TimeoutExpired:
        return False, "playback timed out after 5 minutes"
    except Exception as e:
        return False, f"playback failed: {e}"


def speak_text(text: str, client, voice_model: str = "", timeout: float = 120.0) -> str:
    """Send text to fleet TTS, download the audio, and play it locally.

    client: an LLMClient instance from llm_client.py (cloud or brain mode).
    voice_model: TTS model to use, e.g. 'audio-chatterbox'. Empty = auto.

    Returns a status string for the agent's tool result.
    """
    text = (text or "").strip()
    if not text:
        return "Error: speak_text needs non-empty text"
    if len(text) > 4000:
        text = text[:4000]

    if not client:
        return "Error: no LLM client available for TTS"

    # Direct brain mode — audio task goes to the brain's PubSub via broker URL
    # Cloud mode — audio task goes to broker /generate/async endpoint
    if client.direct_mode:
        # In direct mode, the brain doesn't expose a playground endpoint.
        # We can't do TTS without the broker. Bail with a friendly message.
        return "Error: speak_text requires PastaWater cloud mode (broker not available in direct brain mode)"

    # Resolve TTS model — try the configured one, else auto-detect from fleet
    model = voice_model or _detect_tts_model(client)
    if not model:
        return "Error: no TTS service running on the fleet. Start one on a slot via GPU Setup (audio-chatterbox, audio-fish, audio-qwen-tts, or audio-dia)."

    # Submit task
    payload = {
        "model": model,
        "slot": client.slot,
        "text": text,
    }
    try:
        resp = client.session.post(
            f"{client.api_url}/api/v1/playground/generate/async",
            json=payload,
            timeout=20,
        )
    except Exception as e:
        return f"Error: failed to submit TTS task — {e}"

    if resp.status_code not in (200, 202):
        return f"Error: TTS submit failed ({resp.status_code}): {resp.text[:200]}"

    data = resp.json()
    if not data.get("success"):
        return f"Error: {data.get('error', 'unknown TTS error')}"

    task_id = data.get("task_id")
    if not task_id:
        return "Error: TTS submit returned no task_id"

    # Poll for completion
    deadline = time.time() + timeout
    audio_url = None
    while time.time() < deadline:
        try:
            poll = client.session.get(
                f"{client.api_url}/api/v1/playground/tasks/{task_id}",
                timeout=10,
            )
        except Exception:
            time.sleep(1.0)
            continue
        if poll.status_code != 200:
            time.sleep(1.0)
            continue
        pdata = poll.json()
        status = pdata.get("status")
        if status == "completed":
            result = pdata.get("result", {}) or {}
            # Result keys vary by service — try common ones
            audio_url = (
                result.get("audio_url")
                or result.get("url")
                or result.get("file_url")
                or result.get("output_url")
            )
            break
        if status == "failed":
            return f"Error: TTS failed — {pdata.get('error', 'unknown')}"
        time.sleep(1.0)

    if not audio_url:
        return "Error: TTS task timed out"

    # Download the audio
    try:
        audio_resp = requests.get(audio_url, timeout=60)
    except Exception as e:
        return f"Error: failed to download audio — {e}"
    if audio_resp.status_code != 200:
        return f"Error: audio download returned {audio_resp.status_code}"

    # Save and play
    suffix = ".wav"
    if ".mp3" in audio_url.lower():
        suffix = ".mp3"
    elif ".ogg" in audio_url.lower():
        suffix = ".ogg"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
        f.write(audio_resp.content)
        audio_path = f.name

    ok, msg = play_audio_file(audio_path)
    try:
        os.unlink(audio_path)
    except Exception:
        pass

    if ok:
        return f"Spoke {len(text)} chars via {model} ({msg})"
    return f"Generated audio but {msg}. URL: {audio_url}"


def _detect_tts_model(client) -> str:
    """Look at the fleet's running services and return the first TTS model found."""
    try:
        devices = client.list_devices()
    except Exception:
        return ""

    # Need to call slots endpoint with running_services
    try:
        resp = client.session.get(f"{client.api_url}/api/user/byog/slots", timeout=10)
        if resp.status_code != 200:
            return ""
        data = resp.json()
        for slot in data.get("slots", []):
            if not slot.get("online"):
                continue
            running = slot.get("running_services", [])
            for svc in running:
                if svc.startswith("audio-") or svc.startswith("tts"):
                    # Map known service names to playground model IDs
                    if "chatterbox" in svc:
                        return "audio-chatterbox"
                    if "fish" in svc:
                        return "audio-fish"
                    if "qwen" in svc:
                        return "audio-qwen-tts"
                    if "dia" in svc:
                        return "audio-dia"
    except Exception:
        return ""

    return ""
