"""indent-ssh-helper: tunnels SSH over a WebRTC data channel."""

import asyncio
import json
import os
import sys
import uuid
from pathlib import Path

import websockets
from aiortc import RTCConfiguration, RTCIceServer, RTCPeerConnection, RTCSessionDescription
from aiortc.sdp import candidate_from_sdp


def _log(msg: str, **fields: object) -> None:
    parts = [msg] + [f"{k}={v}" for k, v in fields.items()]
    sys.stderr.write(" ".join(parts) + "\n")
    sys.stderr.flush()


def _read_api_key() -> str:
    key = os.environ.get("INDENT_API_KEY")
    if key:
        return key

    config_path = Path.home() / ".config" / "indent" / "config.json"
    try:
        config = json.loads(config_path.read_text())
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"cannot read {config_path}: {e} (set INDENT_API_KEY env var as an alternative)")

    env = os.environ.get("INDENT_ENV")
    if env:
        extra = config.get("extra_exponent_api_keys", {})
        if env in extra:
            return extra[env]
        raise SystemExit(f"INDENT_ENV={env!r} but no matching key in extra_exponent_api_keys in {config_path}")

    api_key = config.get("exponent_api_key")
    if not api_key:
        raise SystemExit(f"exponent_api_key not found in {config_path}")
    return api_key


async def _run(chat_uuid: str, api_key: str, ws_url: str) -> None:
    _log("connecting", chat_uuid=chat_uuid, ws_url=ws_url)

    async with websockets.connect(ws_url, open_timeout=10) as ws:
        await ws.send(json.dumps({"type": "auth", "data": {"api_key": api_key}}))
        auth = json.loads(await ws.recv())
        if auth.get("type") != "auth_success":
            raise SystemExit(f"auth failed: {auth.get('reason')}")
        _log("authenticated", role=auth.get("role"))

        ice_configs = auth.get("ice_servers", [])
        ice_servers = []
        for c in ice_configs:
            ice_servers.append(
                RTCIceServer(
                    urls=c.get("urls", []),
                    username=c.get("username", ""),
                    credential=c.get("credential", ""),
                )
            )

        pc = RTCPeerConnection(RTCConfiguration(iceServers=ice_servers))

        done = asyncio.Event()
        loop = asyncio.get_running_loop()
        background_tasks: set[asyncio.Task] = set()

        @pc.on("connectionstatechange")
        async def on_state() -> None:
            _log("peer connection state", state=pc.connectionState)
            if pc.connectionState in ("failed", "closed"):
                done.set()

        # Negotiated SCTP channel (must match remote side)
        pc.createDataChannel("_sctp", negotiated=True, id=0)

        ssh_dc = pc.createDataChannel("ssh", ordered=True)

        @ssh_dc.on("open")
        def on_open() -> None:
            _log("ssh data channel open")

            async def pump_stdin() -> None:
                reader = asyncio.StreamReader()
                await loop.connect_read_pipe(lambda: asyncio.StreamReaderProtocol(reader), sys.stdin.buffer)
                try:
                    while True:
                        chunk = await reader.read(16384)
                        if not chunk:
                            break
                        ssh_dc.send(chunk)
                except Exception:
                    pass
                done.set()

            task = loop.create_task(pump_stdin())
            background_tasks.add(task)
            task.add_done_callback(background_tasks.discard)

        @ssh_dc.on("message")
        def on_message(msg: bytes | str) -> None:
            data = msg if isinstance(msg, bytes) else msg.encode()
            try:
                sys.stdout.buffer.write(data)
                sys.stdout.buffer.flush()
            except BrokenPipeError:
                done.set()

        @ssh_dc.on("close")
        def on_close() -> None:
            _log("ssh data channel closed")
            done.set()

        offer = await pc.createOffer()
        await pc.setLocalDescription(offer)

        local_desc = pc.localDescription
        offer_payload = json.dumps({"type": "offer", "sdp": local_desc.sdp})
        session_id = str(uuid.uuid4())

        await ws.send(
            json.dumps(
                {
                    "type": "offer",
                    "session_id": session_id,
                    "target_port": 22,
                    "payload": offer_payload,
                }
            )
        )
        _log("offer sent", session_id=session_id)

        async def handle_signaling() -> None:
            try:
                async for raw in ws:
                    msg = json.loads(raw)
                    match msg.get("type"):
                        case "session_ok":
                            _log("session accepted", session_id=msg.get("session_id"))
                        case "signal":
                            kind = msg.get("kind")
                            payload = json.loads(msg.get("payload", "{}"))
                            if kind == "ANSWER":
                                answer = RTCSessionDescription(sdp=payload["sdp"], type="answer")
                                await pc.setRemoteDescription(answer)
                                _log("remote description set (answer)")
                            elif kind == "ICE_CANDIDATE":
                                candidate_str = payload.get("candidate", "")
                                if candidate_str:
                                    candidate = candidate_from_sdp(candidate_str)
                                    candidate.sdpMid = payload.get("sdpMid", "0")
                                    candidate.sdpMLineIndex = payload.get("sdpMLineIndex", 0)
                                    await pc.addIceCandidate(candidate)
                        case "error":
                            _log("signaling error", error=msg.get("error"), session_id=msg.get("session_id"))
                            done.set()
                            return
                        case "ping":
                            await ws.send(json.dumps({"type": "pong"}))
            except websockets.ConnectionClosed:
                pass
            done.set()

        signaling_task = asyncio.ensure_future(handle_signaling())

        try:
            await done.wait()
        except asyncio.CancelledError:
            pass
        finally:
            _log("exiting")
            signaling_task.cancel()
            try:
                await signaling_task
            except (asyncio.CancelledError, Exception):
                pass
            await pc.close()


def main() -> None:
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: indent-ssh-helper <uuid>.indent\n")
        sys.exit(1)

    host = sys.argv[1]
    chat_uuid = host.removesuffix(".indent")
    try:
        uuid.UUID(chat_uuid)
    except ValueError:
        sys.stderr.write(f'Error: "{chat_uuid}" is not a valid chat UUID\n')
        sys.exit(1)

    api_key = _read_api_key()

    ws_url = os.environ.get("INDENT_WS_URL")
    if not ws_url:
        ws_url = f"wss://ws-api.indent.com/api/ws/webrtc/{chat_uuid}"
    else:
        ws_url = f"{ws_url.rstrip('/')}/webrtc/{chat_uuid}"

    try:
        asyncio.run(_run(chat_uuid, api_key, ws_url))
    except KeyboardInterrupt:
        pass
