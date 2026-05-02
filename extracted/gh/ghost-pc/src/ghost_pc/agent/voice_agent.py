"""Voice agent for GhostPC — Gemini Live API integration.

Uses ADK's run_live() with LiveRequestQueue for bidirectional audio streaming.

Architecture:
  Microphone → VoiceController (wake word) → VoiceSession (Gemini Live)
  Gemini Live → Tool calls (desktop actions) + Audio responses → Speakers

Two-tier tool strategy:
  - Voice agent uses high-level FunctionTools that work with run_live()
    (open_application, run_terminal, switch_to_window, read_clipboard, etc.)
  - ComputerUseToolset does NOT work with run_live() — visual/pixel tasks
    are delegated to the main text agent via delegate_visual_task()

Audio formats:
  Input:  16kHz, 16-bit signed, mono PCM (from microphone)
  Output: 24kHz, 16-bit signed, mono PCM (from Gemini Live)
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import Any

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

logger = logging.getLogger(__name__)

# Gemini model with native audio streaming support
VOICE_MODEL = "gemini-2.5-flash-native-audio-preview-12-2025"

VOICE_INSTRUCTION = """\
You are GhostPC, a voice-controlled AI assistant for a Windows desktop computer.
The user is speaking to you through their microphone.

## How to Respond
- Respond naturally with speech — keep it short and conversational.
- After performing an action, briefly describe what you did.
- If a task involves looking at the screen or clicking specific visual elements,
  use delegate_visual_task to hand it off to the vision agent.

## Your Tools
You have direct access to high-level desktop tools:
- open_application, run_terminal, switch_to_window, get_open_windows
- read_clipboard, write_clipboard, list_files, find_files, read_text_file
- manage_window, set_volume, get_system_info, send_desktop_notification
- set_reminder, task_complete

## Visual Tasks (Delegation)
For anything requiring screen vision or pixel-level clicking:
- Use delegate_visual_task("click the blue button") — the vision agent handles it.
- This covers: clicking UI elements, reading on-screen text, drag-and-drop, etc.

## Voice Session
- The session stays open while you're talking.
- 30 seconds of silence returns to wake word listening.
- Say "that's all" or "goodbye" to end the session.
"""


# ── Voice-specific tools ─────────────────────────────────────────────────────


def build_voice_tools() -> list[Any]:
    """Build the tool list for the voice agent.

    Returns high-level FunctionTools that work with run_live().
    ComputerUseToolset is excluded — it requires a different model.
    """
    from ghost_pc.agent.tools import (
        find_files,
        get_open_windows,
        get_system_info,
        kill_process,
        list_files,
        list_processes,
        manage_window,
        open_application,
        read_clipboard,
        read_text_file,
        run_terminal,
        send_desktop_notification,
        set_reminder,
        set_volume,
        switch_to_window,
        task_complete,
        write_clipboard,
    )

    return [
        open_application,
        run_terminal,
        switch_to_window,
        get_open_windows,
        manage_window,
        read_clipboard,
        write_clipboard,
        list_files,
        find_files,
        read_text_file,
        set_volume,
        get_system_info,
        list_processes,
        kill_process,
        send_desktop_notification,
        set_reminder,
        task_complete,
        delegate_visual_task,
    ]


async def delegate_visual_task(description: str) -> dict:
    """Delegate a visual/pixel-level task to the main desktop agent.

    Use this when you need to click specific UI elements, read text from
    the screen, or perform any action that requires seeing the screen.
    The vision agent will handle it using computer vision.

    Args:
        description: What needs to be done visually (e.g., "click the Save button").
    """
    # This is a signaling tool — the orchestrator picks up the delegation
    # request and routes it through the main agent.
    return {
        "status": "delegated",
        "message": f"Visual task delegated: {description}",
        "description": description,
    }


def create_voice_agent(tools: list[Any] | None = None) -> Agent:
    """Create the voice-capable ADK agent.

    Args:
        tools: Optional tool list override. Defaults to build_voice_tools().
    """
    return Agent(
        name="ghost_pc_voice",
        model=VOICE_MODEL,
        description="Voice-controlled desktop agent with native audio I/O.",
        instruction=VOICE_INSTRUCTION,
        tools=tools or build_voice_tools(),
    )


class VoiceSession:
    """Manages a single voice interaction session with Gemini Live.

    Lifecycle:
      1. start() → creates Runner, LiveRequestQueue, begins run_live()
      2. send_audio() → streams PCM to Gemini via LiveRequestQueue
      3. Events from run_live() → audio responses, tool calls
      4. stop() → closes the session, returns to wake word listening
    """

    def __init__(
        self,
        agent: Agent,
        on_audio_response: Callable[[bytes], Awaitable[None]] | None = None,
        on_text_response: Callable[[str], Awaitable[None]] | None = None,
        on_speaking_start: Callable[[], None] | None = None,
        on_speaking_end: Callable[[], None] | None = None,
    ) -> None:
        self._agent = agent
        self._on_audio_response = on_audio_response
        self._on_text_response = on_text_response
        self._on_speaking_start = on_speaking_start
        self._on_speaking_end = on_speaking_end
        self._session_service = InMemorySessionService()
        self._runner: Runner | None = None
        self._active = False
        self._live_queue: Any = None
        self._event_task: asyncio.Task[None] | None = None
        self._session_id: str = ""

    async def start(self) -> None:
        """Start the Gemini Live audio session."""
        if self._active:
            return

        try:
            self._runner = Runner(
                agent=self._agent,
                app_name="ghost_pc_voice",
                session_service=self._session_service,
            )

            session = await self._session_service.create_session(
                app_name="ghost_pc_voice",
                user_id="voice_user",
            )
            self._session_id = session.id

            # Create LiveRequestQueue for bidirectional streaming
            from google.adk.agents.live_request_queue import LiveRequestQueue

            self._live_queue = LiveRequestQueue()
            self._active = True

            # Background task: consume events from run_live()
            self._event_task = asyncio.create_task(self._process_events())

            logger.info("Voice session started (session_id=%s)", self._session_id)

        except Exception as e:
            logger.error("Failed to start voice session: %s", e)
            self._active = False

    async def stop(self) -> None:
        """Stop the live voice session."""
        self._active = False

        # Close the live queue to signal run_live() to stop
        if self._live_queue:
            try:
                self._live_queue.close()
            except Exception:
                pass
            self._live_queue = None

        # Wait for event processing to finish
        if self._event_task:
            self._event_task.cancel()
            try:
                await self._event_task
            except asyncio.CancelledError:
                pass
            self._event_task = None

        if self._runner:
            await self._runner.close()
            self._runner = None

        logger.info("Voice session stopped")

    async def send_audio(self, audio_chunk: bytes) -> None:
        """Send a PCM audio chunk to the Gemini Live session.

        Args:
            audio_chunk: Raw PCM bytes (16kHz, 16-bit, mono).
        """
        if not self._active or not self._live_queue:
            return

        try:
            self._live_queue.send_realtime(
                types.Blob(data=audio_chunk, mime_type="audio/pcm;rate=16000")
            )
        except Exception as e:
            logger.debug("Failed to send audio chunk: %s", e)

    async def send_text(self, text: str) -> str:
        """Send a text message through the voice agent (fallback mode).

        Uses run_async instead of run_live for text-only interaction.

        Args:
            text: Text message to process.

        Returns:
            Agent's text response.
        """
        if not self._runner:
            return "Voice agent not started"

        user_content = types.Content(
            role="user",
            parts=[types.Part(text=text)],
        )

        final_text = ""
        try:
            async for event in self._runner.run_async(
                user_id="voice_user",
                session_id=self._session_id,
                new_message=user_content,
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            final_text = part.text
        except Exception as e:
            logger.error("Voice agent text error: %s", e)
            return f"Error: {e}"

        return final_text or "Done."

    async def _process_events(self) -> None:
        """Process events from run_live() — audio output + tool calls.

        This runs as a background task for the duration of the session.
        """
        if not self._runner or not self._live_queue:
            return

        try:
            from google.adk.agents.run_config import RunConfig

            run_config = RunConfig(
                response_modalities=["AUDIO"],
                output_audio_transcription=True,
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Zephyr")
                    )
                ),
            )

            async for event in self._runner.run_live(
                user_id="voice_user",
                session_id=self._session_id,
                live_request_queue=self._live_queue,
                run_config=run_config,
            ):
                if not self._active:
                    break

                if not event.content or not event.content.parts:
                    continue

                for part in event.content.parts:
                    # Audio response — play through speakers
                    if part.inline_data and part.inline_data.data:
                        if self._on_speaking_start:
                            self._on_speaking_start()
                        if self._on_audio_response:
                            await self._on_audio_response(part.inline_data.data)
                        if self._on_speaking_end:
                            self._on_speaking_end()

                    # Text transcription
                    if part.text:
                        if self._on_text_response:
                            await self._on_text_response(part.text)

        except asyncio.CancelledError:
            pass
        except Exception as e:
            if self._active:
                logger.error("Voice session event error: %s", e, exc_info=True)

    @property
    def is_active(self) -> bool:
        return self._active


# ── Utility functions (WhatsApp voice notes) ─────────────────────────────────


async def text_to_speech(text: str, output_path: str) -> bool:
    """Convert text to speech using Edge TTS.

    Args:
        text: Text to convert to speech.
        output_path: Path to save the audio file (.mp3).

    Returns:
        True if successful.
    """
    try:
        import edge_tts

        communicate = edge_tts.Communicate(text, "en-US-GuyNeural")
        await communicate.save(output_path)
        return True
    except ImportError:
        logger.debug("edge-tts not installed")
        return False
    except Exception as e:
        logger.error("TTS failed: %s", e)
        return False


async def speech_to_ogg(mp3_path: str, ogg_path: str) -> bool:
    """Convert MP3 to OGG Opus format for WhatsApp voice notes.

    Uses ffmpeg for format conversion.

    Args:
        mp3_path: Input MP3 file path.
        ogg_path: Output OGG Opus file path.

    Returns:
        True if successful.
    """
    try:
        proc = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-y",
            "-i",
            mp3_path,
            "-c:a",
            "libopus",
            "-b:a",
            "64k",
            "-vn",
            ogg_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.communicate()
        return proc.returncode == 0
    except Exception as e:
        logger.error("ffmpeg conversion failed: %s", e)
        return False
