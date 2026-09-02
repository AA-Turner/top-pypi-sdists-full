"""Amazon Nova Sonic speech-to-speech adapter (Bedrock bidirectional stream).

Realtime S2S can't be expressed as a single POST — it needs a stateful handshake
(sessionStart → promptStart → SYSTEM text → USER audio → contentEnd) with server-side
VAD deciding end-of-turn. This adapter drives that handshake and exposes the same
``@task`` interface as the HTTP transport, so attacks treat it identically.

Optional deps (``aws-sdk-bedrock-runtime``, ``awscrt``, ``smithy-aws-core``) are imported
dynamically. Auth is AWS IAM/SigV4 via the credential chain — no API key.
"""

import base64
import contextlib
import importlib
import importlib.util
import os
import typing as t

from dreadnode.core.task import Task, task
from dreadnode.generators.message import ContentAudioInput, ContentText, Message

_NOVA_DEPS = ("aws_sdk_bedrock_runtime", "awscrt", "smithy_aws_core")


def _require_nova_deps() -> None:
    """Fail fast if the Nova Sonic streaming deps are missing.

    The streaming deps ship with the **core** install, but only build on Python
    >=3.12 (they carry a version marker), so on 3.11 they are absent. Checked at
    target-construction time so an unsupported Python version stops the run up
    front instead of surfacing as a mid-stream error finding.
    """
    import sys

    for mod in _NOVA_DEPS:
        if importlib.util.find_spec(mod) is None:
            raise RuntimeError(
                "Nova Sonic speech-to-speech requires Python >=3.12 (the AWS Bedrock "
                f"bidirectional-streaming dependencies are not available on Python "
                f"{sys.version_info.major}.{sys.version_info.minor}). Missing module: {mod}."
            )


def _ensure_aws_credentials(region: str) -> None:
    """Resolve AWS credentials up front and seed the environment for Nova Sonic.

    The Bedrock bidirectional stream authenticates from the environment. If no
    credentials are present it does **not** error — it hangs — so we resolve them
    ourselves first via the standard AWS credential chain (env vars, then the shared
    ``~/.aws`` config / SSO profile, then IAM role / instance metadata) and export
    them, so a local ``aws sso login`` / profile is picked up just like an explicit
    ``AWS_ACCESS_KEY_ID`` would be. If nothing resolves, raise a clear error instead
    of letting the stream hang.
    """
    os.environ.setdefault("AWS_DEFAULT_REGION", region)
    if os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"):
        return
    creds = None
    resolve_error: Exception | None = None
    try:
        botocore_session = importlib.import_module("botocore.session")
        creds = botocore_session.Session().get_credentials()
    except Exception as exc:
        resolve_error = exc
    if creds is None:
        raise RuntimeError(
            "Nova Sonic requires AWS credentials, but none were found. Set "
            "AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY (+ AWS_SESSION_TOKEN), or "
            "configure a profile / SSO login (e.g. `aws sso login` + AWS_PROFILE). "
            f"Region: {region}."
        ) from resolve_error
    frozen = creds.get_frozen_credentials()
    os.environ["AWS_ACCESS_KEY_ID"] = frozen.access_key
    os.environ["AWS_SECRET_ACCESS_KEY"] = frozen.secret_key
    if frozen.token:
        os.environ["AWS_SESSION_TOKEN"] = frozen.token


def nova_sonic_target(
    *,
    region: str = "us-east-1",
    model_id: str = "amazon.nova-sonic-v1:0",
    voice: str = "matthew",
    system_prompt: str = "You are a helpful voice assistant.",
    name: str = "nova_sonic",
    **_: t.Any,
) -> Task[..., Message]:
    """A ``@task`` target for Amazon Nova Sonic speech-to-speech.

    Expects the input message to carry **audio** (16 kHz mono 16-bit PCM, or a WAV that
    decodes to it). Streams it to Nova Sonic and returns a :class:`Message` with the
    model's spoken reply (audio) and its transcript (text).

    Prerequisites: Python >=3.12 (the streaming dependencies ship with the core install
    but carry that version marker), AWS credentials (env vars / profile / role), and Nova
    Sonic model access in the region.
    """
    # Fail fast at construction so a missing dependency doesn't register a doomed
    # assessment that only errors mid-stream.
    _require_nova_deps()

    async def target(message: Message) -> Message:
        pcm = _first_audio_pcm(message)
        text, audio = await _roundtrip(
            pcm, region=region, model_id=model_id, voice=voice, system_prompt=system_prompt
        )
        parts: list[t.Any] = []
        if text:
            parts.append(ContentText(text=text))
        if audio:
            parts.append(ContentAudioInput.from_bytes(_pcm_to_wav(audio, 24000), format="wav"))
        return Message(role="assistant", content=parts or [ContentText(text="")])

    return task(target, name=name)


def _first_audio_pcm(message: Message) -> bytes:
    """Extract 16 kHz mono PCM bytes from the first audio part (accepts raw PCM or WAV)."""
    import io
    import wave

    for part in getattr(message, "content_parts", None) or []:
        if getattr(part, "type", None) == "input_audio":
            raw = part.to_bytes()
            if raw[:4] == b"RIFF":  # WAV → extract PCM frames
                with wave.open(io.BytesIO(raw), "rb") as w:
                    return w.readframes(w.getnframes())
            return raw
    raise ValueError("nova_sonic_target requires an audio part in the input message")


def _pcm_to_wav(pcm: bytes, rate: int) -> bytes:
    import io
    import wave

    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(pcm)
    return buf.getvalue()


async def _roundtrip(
    pcm: bytes, *, region: str, model_id: str, voice: str, system_prompt: str
) -> tuple[str, bytes]:
    """Run one Nova Sonic S2S turn; return (transcript, reply_pcm_24k). Validated live."""
    import asyncio
    import json
    import uuid

    # Resolve credentials before opening the stream so a missing/expired login fails
    # fast with a clear error instead of hanging on the Bedrock handshake.
    _ensure_aws_credentials(region)

    try:
        bedrock = importlib.import_module("aws_sdk_bedrock_runtime.client")
        models = importlib.import_module("aws_sdk_bedrock_runtime.models")
        config_mod = importlib.import_module("aws_sdk_bedrock_runtime.config")
        smithy_env = importlib.import_module("smithy_aws_core.identity.environment")
    except ModuleNotFoundError as e:
        raise RuntimeError(
            "Nova Sonic speech-to-speech needs the optional streaming dependencies. "
            'Install them with:  pip install "dreadnode[nova-sonic]"  (requires Python '
            f">=3.12). Missing module: {e.name}."
        ) from e

    prompt_id, sys_id, audio_id = (str(uuid.uuid4()) for _ in range(3))
    text_out: list[str] = []
    audio_out = bytearray()
    role = {"v": None}
    done = asyncio.Event()

    client = bedrock.BedrockRuntimeClient(
        config=config_mod.Config(
            endpoint_uri=f"https://bedrock-runtime.{region}.amazonaws.com",
            region=region,
            aws_credentials_identity_resolver=smithy_env.EnvironmentCredentialsResolver(),
        )
    )
    stream = await client.invoke_model_with_bidirectional_stream(
        bedrock.InvokeModelWithBidirectionalStreamOperationInput(model_id=model_id)
    )

    async def send(d: dict) -> None:
        await stream.input_stream.send(
            models.InvokeModelWithBidirectionalStreamInputChunk(
                value=models.BidirectionalInputPayloadPart(bytes_=json.dumps(d).encode("utf-8"))
            )
        )

    async def process() -> None:
        while not done.is_set():
            output = await stream.await_output()
            result = await output[1].receive()
            # `result` is a union of chunk + error types; only the chunk variant
            # carries `.value.bytes_`. Access defensively so the type checker
            # doesn't flag the error variants (which have no such attribute).
            value = getattr(result, "value", None)
            payload = getattr(value, "bytes_", None)
            if not payload:
                continue
            ev = json.loads(payload.decode("utf-8")).get("event", {})
            if "contentStart" in ev:
                role["v"] = ev["contentStart"].get("role")
            elif "textOutput" in ev and role["v"] == "ASSISTANT":
                text_out.append(ev["textOutput"].get("content", ""))
            elif "audioOutput" in ev:
                audio_out.extend(base64.b64decode(ev["audioOutput"]["content"]))
            elif (
                "contentEnd" in ev and role["v"] == "ASSISTANT" and audio_out
            ) or "completionEnd" in ev:
                done.set()

    await send(
        {
            "event": {
                "sessionStart": {
                    "inferenceConfiguration": {"maxTokens": 1024, "topP": 0.9, "temperature": 0.7}
                }
            }
        }
    )
    await send(
        {
            "event": {
                "promptStart": {
                    "promptName": prompt_id,
                    "textOutputConfiguration": {"mediaType": "text/plain"},
                    "audioOutputConfiguration": {
                        "mediaType": "audio/lpcm",
                        "sampleRateHertz": 24000,
                        "sampleSizeBits": 16,
                        "channelCount": 1,
                        "voiceId": voice,
                        "encoding": "base64",
                        "audioType": "SPEECH",
                    },
                }
            }
        }
    )
    await send(
        {
            "event": {
                "contentStart": {
                    "promptName": prompt_id,
                    "contentName": sys_id,
                    "type": "TEXT",
                    "interactive": False,
                    "role": "SYSTEM",
                    "textInputConfiguration": {"mediaType": "text/plain"},
                }
            }
        }
    )
    await send(
        {
            "event": {
                "textInput": {
                    "promptName": prompt_id,
                    "contentName": sys_id,
                    "content": system_prompt,
                }
            }
        }
    )
    await send({"event": {"contentEnd": {"promptName": prompt_id, "contentName": sys_id}}})

    processor = asyncio.create_task(process())

    await send(
        {
            "event": {
                "contentStart": {
                    "promptName": prompt_id,
                    "contentName": audio_id,
                    "type": "AUDIO",
                    "interactive": True,
                    "role": "USER",
                    "audioInputConfiguration": {
                        "mediaType": "audio/lpcm",
                        "sampleRateHertz": 16000,
                        "sampleSizeBits": 16,
                        "channelCount": 1,
                        "audioType": "SPEECH",
                        "encoding": "base64",
                    },
                }
            }
        }
    )
    payload = pcm + b"\x00" * (16000 * 2)  # +1s silence → VAD end-of-turn
    for i in range(0, len(payload), 2048):
        await send(
            {
                "event": {
                    "audioInput": {
                        "promptName": prompt_id,
                        "contentName": audio_id,
                        "content": base64.b64encode(payload[i : i + 2048]).decode("utf-8"),
                    }
                }
            }
        )
        await asyncio.sleep(0.01)  # real-time pacing
    await send({"event": {"contentEnd": {"promptName": prompt_id, "contentName": audio_id}}})

    with contextlib.suppress(TimeoutError):
        await asyncio.wait_for(done.wait(), timeout=30)
    await send({"event": {"promptEnd": {"promptName": prompt_id}}})
    await send({"event": {"sessionEnd": {}}})
    await stream.input_stream.close()
    if not processor.done():
        processor.cancel()
    return " ".join(text_out).strip(), bytes(audio_out)
