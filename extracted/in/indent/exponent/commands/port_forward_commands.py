import asyncio
import json
import logging
import socket
import uuid
from dataclasses import dataclass

import click
import websockets.asyncio.client
from aiortc import (
    RTCConfiguration,
    RTCIceCandidate,
    RTCIceServer,
    RTCPeerConnection,
    RTCSessionDescription,
)
from aiortc.sdp import candidate_from_sdp

from exponent.commands.common import redirect_to_login, run_until_complete
from exponent.commands.settings import use_settings
from exponent.commands.types import exponent_cli_group
from exponent.core.config import Settings

logger = logging.getLogger(__name__)

BUFFER_SIZE = 16384
DEFAULT_STUN_SERVERS = [
    RTCIceServer(urls=["stun:stun.cloudflare.com:3478"]),
]


def _parse_ice_candidate(candidate_data: dict[str, object]) -> RTCIceCandidate | None:
    candidate_str = str(candidate_data.get("candidate", ""))
    if not candidate_str:
        return None
    candidate = candidate_from_sdp(candidate_str)
    candidate.sdpMid = candidate_data.get("sdpMid")  # type: ignore[assignment]
    candidate.sdpMLineIndex = candidate_data.get("sdpMLineIndex")  # type: ignore[assignment]
    return candidate


@dataclass
class PortSpec:
    local_port: int
    remote_port: int | None
    remote_unix_socket: str | None

    def dc_label(self) -> str:
        if self.remote_unix_socket:
            return f"unix:{self.remote_unix_socket}"
        return f"tcp:{self.remote_port}"


def _validate_port(port: int) -> None:
    if port < 1 or port > 65535:
        raise ValueError(f"port {port} out of range (1-65535)")


def parse_port_spec(spec: str) -> PortSpec:
    if ":" in spec:
        local_str, remote = spec.split(":", 1)
        local_port = int(local_str)
        _validate_port(local_port)
        if remote.startswith("/") or remote.startswith("."):
            return PortSpec(local_port=local_port, remote_port=None, remote_unix_socket=remote)
        else:
            remote_port = int(remote)
            _validate_port(remote_port)
            return PortSpec(local_port=local_port, remote_port=remote_port, remote_unix_socket=None)
    else:
        port = int(spec)
        _validate_port(port)
        return PortSpec(local_port=port, remote_port=port, remote_unix_socket=None)


def _bind_socket(family: socket.AddressFamily, addr: str, port: int) -> socket.socket:
    sock = socket.socket(family, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if family == socket.AF_INET6:
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
    sock.setblocking(False)
    sock.bind((addr, port))
    sock.listen(128)
    return sock


def bind_listeners(specs: list[PortSpec]) -> list[tuple[PortSpec, socket.socket]]:
    listeners: list[tuple[PortSpec, socket.socket]] = []
    for spec in specs:
        listeners.append((spec, _bind_socket(socket.AF_INET, "127.0.0.1", spec.local_port)))
        try:
            listeners.append((spec, _bind_socket(socket.AF_INET6, "::1", spec.local_port)))
        except OSError:
            logger.debug("IPv6 not available for port %d, skipping", spec.local_port)
    return listeners


async def _signaling_handshake(
    ws_url: str,
    api_key: str,
    pc: RTCPeerConnection,
    first_spec: PortSpec,
) -> None:
    ws = await websockets.asyncio.client.connect(ws_url, open_timeout=10)
    try:
        await ws.send(json.dumps({"type": "auth", "data": {"api_key": api_key}}))
        resp = json.loads(await ws.recv())
        if resp.get("type") != "auth_success":
            raise click.ClickException(f"Signaling auth failed: {resp.get('reason', 'unknown')}")

        offer = await pc.createOffer()
        await pc.setLocalDescription(offer)
        while pc.iceGatheringState != "complete":
            await asyncio.sleep(0.05)

        local_desc = pc.localDescription
        assert local_desc is not None

        session_id = str(uuid.uuid4())
        offer_msg: dict[str, object] = {
            "type": "offer",
            "session_id": session_id,
            "payload": json.dumps({"type": "offer", "sdp": local_desc.sdp}),
        }
        if first_spec.remote_port is not None:
            offer_msg["target_port"] = first_spec.remote_port
        if first_spec.remote_unix_socket is not None:
            offer_msg["target_unix_socket"] = first_spec.remote_unix_socket
        await ws.send(json.dumps(offer_msg))

        ice_connected = asyncio.Event()
        got_answer = False

        def _check_ice_state() -> None:
            state = pc.iceConnectionState
            logger.debug("ICE connection state: %s", state)
            if state in ("connected", "completed"):
                ice_connected.set()
            elif state == "failed":
                ice_connected.set()

        pc.on("iceconnectionstatechange", _check_ice_state)
        _check_ice_state()

        async def _read_signaling() -> None:
            nonlocal got_answer
            async for raw in ws:
                msg = json.loads(raw)
                msg_type = msg.get("type")

                if msg_type == "session_ok":
                    continue

                if msg_type == "signal":
                    kind = msg.get("kind")
                    payload = str(msg.get("payload", ""))

                    if kind == "ANSWER":
                        answer_data = json.loads(payload)
                        await pc.setRemoteDescription(
                            RTCSessionDescription(sdp=str(answer_data.get("sdp", "")), type="answer")
                        )
                        got_answer = True
                        click.echo("  Received answer, waiting for ICE...")

                    elif kind == "ICE_CANDIDATE":
                        candidate = _parse_ice_candidate(json.loads(payload))
                        if candidate:
                            await pc.addIceCandidate(candidate)

                elif msg_type == "error":
                    raise click.ClickException(f"Signaling error: {msg.get('error', 'unknown')}")

                elif msg_type == "ping":
                    await ws.send(json.dumps({"type": "pong"}))

            if not got_answer:
                raise click.ClickException("Signaling WebSocket closed before answer received")

        read_task = asyncio.create_task(_read_signaling())
        done, _pending = await asyncio.wait(
            [read_task, asyncio.create_task(ice_connected.wait())],
            timeout=30.0,
            return_when=asyncio.FIRST_COMPLETED,
        )

        read_task.cancel()
        try:
            await read_task
        except asyncio.CancelledError:
            pass  # Expected: we just cancelled read_task above

        if not done:
            if got_answer:
                raise click.ClickException(f"Timed out waiting for ICE connection (state: {pc.iceConnectionState})")
            raise click.ClickException("Timed out waiting for signaling answer from sandbox")

        for task in done:
            exc = task.exception()
            if exc is not None:
                raise exc

        if pc.iceConnectionState == "failed":
            raise click.ClickException("ICE connection failed")
    finally:
        await ws.close()


async def _fetch_ice_servers(ws_url: str, api_key: str) -> list[RTCIceServer]:
    ws = await websockets.asyncio.client.connect(ws_url, open_timeout=10)
    try:
        await ws.send(json.dumps({"type": "auth", "data": {"api_key": api_key}}))
        resp = json.loads(await ws.recv())
        if resp.get("type") != "auth_success":
            raise click.ClickException(f"Signaling auth failed: {resp.get('reason', 'unknown')}")

        ice_servers: list[RTCIceServer] = []
        for cfg in resp.get("ice_servers") or []:
            ice_servers.append(
                RTCIceServer(
                    urls=cfg["urls"],
                    username=cfg.get("username", ""),
                    credential=cfg.get("credential", ""),
                )
            )
        if not ice_servers:
            return list(DEFAULT_STUN_SERVERS)
        return ice_servers
    finally:
        await ws.close()


async def _bridge_connection(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    pc: RTCPeerConnection,
    spec: PortSpec,
) -> None:
    peer_addr = writer.get_extra_info("peername")
    target_label = spec.remote_unix_socket or str(spec.remote_port)
    click.echo(f"New connection on :{spec.local_port} from {peer_addr} -> {target_label}")

    dc = pc.createDataChannel(spec.dc_label(), ordered=True, protocol="bridge-v1")
    done = asyncio.Event()
    dc_open = asyncio.Event()
    bridge_ready = asyncio.Event()
    remote_error: str | None = None

    @dc.on("open")
    def on_open() -> None:
        dc_open.set()

    @dc.on("close")
    def on_close() -> None:
        done.set()

    @dc.on("message")
    def on_message(data: bytes | str) -> None:
        nonlocal remote_error
        if isinstance(data, str):
            data = data.encode()
        if not bridge_ready.is_set():
            if len(data) == 0:
                return
            if data[0] == 0x00:
                bridge_ready.set()
            elif data[0] == 0x01:
                remote_error = data[1:].decode(errors="replace")
                done.set()
            return

        try:
            writer.write(data)
        except Exception:
            done.set()

    try:
        await asyncio.wait_for(dc_open.wait(), timeout=10.0)
    except TimeoutError:
        click.echo(f"Timed out waiting for data channel open on :{spec.local_port}", err=True)
        dc.close()
        writer.close()
        return

    async def tcp_to_dc() -> None:
        try:
            while not done.is_set():
                data = await reader.read(BUFFER_SIZE)
                if not data:
                    break
                dc.send(data)
        except Exception:
            logger.debug("tcp_to_dc error on :%d", spec.local_port, exc_info=True)
        finally:
            done.set()

    tcp_task = asyncio.create_task(tcp_to_dc())
    await done.wait()
    tcp_task.cancel()
    try:
        await tcp_task
    except asyncio.CancelledError:
        pass  # Expected: we just cancelled the task above

    dc.close()
    writer.close()
    try:
        await writer.wait_closed()
    except OSError:
        logger.debug("Error closing writer on :%d", spec.local_port, exc_info=True)

    if remote_error:
        click.echo(f"Connection refused on :{spec.local_port} -> {target_label}: {remote_error}", err=True)
    else:
        click.echo(f"Connection closed on :{spec.local_port} from {peer_addr}")


async def port_forward_async(
    chat_uuid: str,
    specs: list[PortSpec],
    ws_url: str,
    api_key: str,
) -> None:
    listeners = bind_listeners(specs)
    for spec in specs:
        if spec.remote_unix_socket:
            click.echo(f"Forwarding 127.0.0.1:{spec.local_port} -> {spec.remote_unix_socket}")
        else:
            click.echo(f"Forwarding 127.0.0.1:{spec.local_port} -> :{spec.remote_port}")

    click.echo(f"\nConnecting to sandbox {chat_uuid}...")
    ice_servers = await _fetch_ice_servers(ws_url, api_key)

    config = RTCConfiguration(iceServers=ice_servers)
    pc = RTCPeerConnection(configuration=config)
    pc.createDataChannel("_sctp", negotiated=True, id=0)

    stop = asyncio.Event()

    def on_connection_state_change() -> None:
        state = pc.connectionState
        if state in ("failed", "closed"):
            click.echo(f"WebRTC connection {state}, shutting down.", err=True)
            stop.set()

    pc.on("connectionstatechange", on_connection_state_change)

    click.echo("  Establishing WebRTC session...")
    await _signaling_handshake(ws_url, api_key, pc, specs[0])
    click.echo("Connected. Press Ctrl+C to stop.\n")

    servers: list[asyncio.AbstractServer] = []
    for spec, sock in listeners:

        async def on_connect(
            reader: asyncio.StreamReader,
            writer: asyncio.StreamWriter,
            _pc: RTCPeerConnection = pc,
            _spec: PortSpec = spec,
        ) -> None:
            try:
                await _bridge_connection(reader, writer, _pc, _spec)
            except Exception:
                logger.exception("error handling connection on :%d", _spec.local_port)

        server = await asyncio.start_server(on_connect, sock=sock)
        servers.append(server)

    try:
        await stop.wait()
    except asyncio.CancelledError:
        logger.debug("port-forward shutting down")
    finally:
        for server in servers:
            server.close()
        for server in servers:
            await server.wait_closed()
        await pc.close()


@exponent_cli_group()
def port_forward_cli() -> None:
    pass


@port_forward_cli.command("port-forward")
@click.argument("chat_uuid")
@click.argument("ports", nargs=-1, required=True)
@use_settings
def port_forward(settings: Settings, chat_uuid: str, ports: tuple[str, ...]) -> None:
    """Forward local ports to a sandbox via WebRTC.

    CHAT_UUID is the chat/sandbox identifier.

    PORTS are port specs in the form:
      3002          - forward local 3002 to remote 3002
      8000:8080     - forward local 8000 to remote 8080
      2222:/tmp/s   - forward local 2222 to a remote unix socket
    """
    if not settings.api_key:
        redirect_to_login(settings)
        return

    specs: list[PortSpec] = []
    for p in ports:
        try:
            specs.append(parse_port_spec(p))
        except ValueError:
            raise click.BadParameter(f"Invalid port spec: {p}")

    ws_base = settings.get_base_ws_url()
    ws_url = f"{ws_base}/api/ws/webrtc/{chat_uuid}"

    run_until_complete(port_forward_async(chat_uuid, specs, ws_url, settings.api_key))
