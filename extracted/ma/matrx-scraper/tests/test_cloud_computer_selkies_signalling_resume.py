"""A release must not cut an open Computer screen (2026-10-17, FIX-RELEASE-SURVIVAL).

The viewer's Selkies signalling socket rides an aidream gateway task; every
release drains that task and cuts the socket, while the picture is peer to
peer. Upstream's hub answered the viewer's socket closing by closing the app
peer's socket too (``cleanup_session``), which stops the pipeline: the screen
went black about every 30 minutes. Live 2026-10-17 run 2: the gateway task was
deregistered at 00:27:01 and the session ended when the socket closed at 00:29:02.

This runs Selkies 1.6.2's hub methods verbatim (``signalling_web.py``: the
session cleanup, peer handler, HELLO exchange and connection handler), then the
same text through the patcher's real edits, against in-memory sockets. The same
scenarios were also run against the real file and websockets 12.0 inside the
Cloud Computer image (FIX-RELEASE-SURVIVAL-2026-10-17.md).
"""
from __future__ import annotations

import asyncio
import base64
import importlib.util
import json
import logging
from pathlib import Path
from types import SimpleNamespace

import pytest

PATCHER = Path(__file__).resolve().parents[1] / "docker" / "cloud-computer" / "patch-selkies-web.py"

# Selkies 1.6.2 signalling_web.py, WebRTCSimpleServer: the constructor's peer
# tables, then cleanup_session through hello_peer verbatim, then run()'s
# nested ``handler`` verbatim inside a factory.
UPSTREAM_INIT = """class Hub:
    def __init__(self):
        self.peers = dict()
        self.sessions = dict()
        self.rooms = dict()

    async def recv_msg_ping(self, ws, raddr):
        return await ws.recv()

"""
UPSTREAM_HUB = '''
    async def cleanup_session(self, uid):
        if uid in self.sessions:
            other_id = self.sessions[uid]
            del self.sessions[uid]
            logger.info("Cleaned up {} session".format(uid))
            if other_id in self.sessions:
                del self.sessions[other_id]
                logger.info("Also cleaned up {} session".format(other_id))
                # If there was a session with this peer, also
                # close the connection to reset its state.
                if other_id in self.peers:
                    logger.info("Closing connection to {}".format(other_id))
                    wso, oaddr, _, _ = self.peers[other_id]
                    del self.peers[other_id]
                    await wso.close()

    async def cleanup_room(self, uid, room_id):
        room_peers = self.rooms[room_id]
        if uid not in room_peers:
            return
        room_peers.remove(uid)
        for pid in room_peers:
            wsp, paddr, _, _ = self.peers[pid]
            msg = 'ROOM_PEER_LEFT {}'.format(uid)
            logger.info('room {}: {} -> {}: {}'.format(room_id, uid, pid, msg))
            await wsp.send(msg)

    async def remove_peer(self, uid):
        await self.cleanup_session(uid)
        if uid in self.peers:
            ws, raddr, status, _ = self.peers[uid]
            if status and status != 'session':
                await self.cleanup_room(uid, status)
            del self.peers[uid]
            await ws.close()
            logger.info("Disconnected from peer {!r} at {!r}".format(uid, raddr))

    ############### Handler functions ###############

    async def connection_handler(self, ws, uid, meta=None):
        raddr = ws.remote_address
        peer_status = None
        self.peers[uid] = [ws, raddr, peer_status, meta]
        logger.info("Registered peer {!r} at {!r} with meta: {}".format(uid, raddr, meta))
        while True:
            # Receive command, wait forever if necessary
            msg = await self.recv_msg_ping(ws, raddr)
            # Update current status
            peer_status = self.peers[uid][2]
            # We are in a session or a room, messages must be relayed
            if peer_status is not None:
                # We're in a session, route message to connected peer
                if peer_status == 'session':
                    other_id = self.sessions[uid]
                    wso, oaddr, status, _ = self.peers[other_id]
                    assert(status == 'session')
                    logger.info("{} -> {}: {}".format(uid, other_id, msg))
                    await wso.send(msg)
                # We're in a room, accept room-specific commands
                elif peer_status:
                    # ROOM_PEER_MSG peer_id MSG
                    if msg.startswith('ROOM_PEER_MSG'):
                        _, other_id, msg = msg.split(maxsplit=2)
                        if other_id not in self.peers:
                            await ws.send('ERROR peer {!r} not found'
                                          ''.format(other_id))
                            continue
                        wso, oaddr, status, _ = self.peers[other_id]
                        if status != room_id:
                            await ws.send('ERROR peer {!r} is not in the room'
                                          ''.format(other_id))
                            continue
                        msg = 'ROOM_PEER_MSG {} {}'.format(uid, msg)
                        logger.info('room {}: {} -> {}: {}'.format(room_id, uid, other_id, msg))
                        await wso.send(msg)
                    elif msg == 'ROOM_PEER_LIST':
                        room_id = self.peers[peer_id][2]
                        room_peers = ' '.join([pid for pid in self.rooms[room_id] if pid != peer_id])
                        msg = 'ROOM_PEER_LIST {}'.format(room_peers)
                        logger.info('room {}: -> {}: {}'.format(room_id, uid, msg))
                        await ws.send(msg)
                    else:
                        await ws.send('ERROR invalid msg, already in room')
                        continue
                else:
                    raise AssertionError('Unknown peer status {!r}'.format(peer_status))
            # Requested a session with a specific peer
            elif msg.startswith('SESSION'):
                logger.info("{!r} command {!r}".format(uid, msg))
                _, callee_id = msg.split(maxsplit=1)
                if callee_id not in self.peers:
                    await ws.send('ERROR peer {!r} not found'.format(callee_id))
                    continue
                if peer_status is not None:
                    await ws.send('ERROR peer {!r} busy'.format(callee_id))
                    continue
                meta = self.peers[callee_id][3]
                if meta:
                    meta64 = base64.b64encode(bytes(json.dumps(meta).encode())).decode("ascii")
                else:
                    meta64 = ""
                await ws.send('SESSION_OK {}'.format(meta64))
                wsc = self.peers[callee_id][0]
                logger.info('Session from {!r} ({!r}) to {!r} ({!r})'
                      ''.format(uid, raddr, callee_id, wsc.remote_address))
                # Register session
                self.peers[uid][2] = peer_status = 'session'
                self.sessions[uid] = callee_id
                self.peers[callee_id][2] = 'session'
                self.sessions[callee_id] = uid
            # Requested joining or creation of a room
            elif msg.startswith('ROOM'):
                logger.info('{!r} command {!r}'.format(uid, msg))
                _, room_id = msg.split(maxsplit=1)
                # Room name cannot be 'session', empty, or contain whitespace
                if room_id == 'session' or room_id.split() != [room_id]:
                    await ws.send('ERROR invalid room id {!r}'.format(room_id))
                    continue
                if room_id in self.rooms:
                    if uid in self.rooms[room_id]:
                        raise AssertionError('How did we accept a ROOM command '
                                             'despite already being in a room?')
                else:
                    # Create room if required
                    self.rooms[room_id] = set()
                room_peers = ' '.join([pid for pid in self.rooms[room_id]])
                await ws.send('ROOM_OK {}'.format(room_peers))
                # Enter room
                self.peers[uid][2] = peer_status = room_id
                self.rooms[room_id].add(uid)
                for pid in self.rooms[room_id]:
                    if pid == uid:
                        continue
                    wsp, paddr, _, _ = self.peers[pid]
                    msg = 'ROOM_PEER_JOINED {}'.format(uid)
                    logger.info('room {}: {} -> {}: {}'.format(room_id, uid, pid, msg))
                    await wsp.send(msg)
            else:
                logger.info('Ignoring unknown message {!r} from {!r}'.format(msg, uid))

    async def hello_peer(self, ws):
        \'\'\'
        Exchange hello, register peer
        \'\'\'
        raddr = ws.remote_address
        hello = await ws.recv()
        toks = hello.split(maxsplit=2)
        metab64str = None
        if len(toks) > 2:
            hello, uid, metab64str = toks
        else:
            hello, uid = toks
        if hello != 'HELLO':
            await ws.close(code=1002, reason='invalid protocol')
            raise Exception("Invalid hello from {!r}".format(raddr))
        if not uid or uid in self.peers or uid.split() != [uid]: # no whitespace
            await ws.close(code=1002, reason='invalid peer uid')
            raise Exception("Invalid uid {!r} from {!r}".format(uid, raddr))
        meta = None
        if metab64str:
            meta = json.loads(base64.b64decode(metab64str))
        # Send back a HELLO
        await ws.send('HELLO')
        return uid, meta

    def make_handler(self):
        async def handler(ws, path):
            \'\'\'
            All incoming messages are handled here. @path is unused.
            \'\'\'
            raddr = ws.remote_address
            logger.info("Connected to {!r}".format(raddr))
            peer_id, meta = await self.hello_peer(ws)
            try:
                await self.connection_handler(ws, peer_id, meta)
            except websockets.ConnectionClosed:
                logger.info("Connection to peer {!r} closed, exiting handler".format(raddr))
            finally:
                await self.remove_peer(peer_id)
        return handler
'''


CLOSED = object()


class ConnectionClosed(Exception):
    pass


class Socket:
    """One signalling socket as the hub sees it (websockets' legacy protocol)."""

    def __init__(self, name: str, *messages: str) -> None:
        self.remote_address = (name, 0)
        self.inbox: asyncio.Queue = asyncio.Queue()
        self.sent: list[str] = []
        self.close_code: int | None = None
        for message in messages:
            self.inbox.put_nowait(message)

    async def recv(self) -> str:
        item = await self.inbox.get()
        if item is CLOSED:
            raise ConnectionClosed()
        return item

    async def send(self, message: str) -> None:
        if self.close_code is not None:
            raise ConnectionClosed()
        self.sent.append(message)

    async def close(self, code: int = 1000, reason: str = "") -> None:
        self.end(code)

    def end(self, code: int) -> None:
        """The far side went away: 1006 = the link died, 1000 = closed on purpose."""
        if self.close_code is None:
            self.close_code = code
            self.inbox.put_nowait(CLOSED)


def _patcher():
    spec = importlib.util.spec_from_file_location("patch_selkies_web", PATCHER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _hub(patched: bool):
    source = UPSTREAM_INIT + UPSTREAM_HUB
    if patched:
        patcher = _patcher()
        source = patcher.patch_text("signalling_web.py", source, patcher.PACKAGE_EDITS["signalling_web.py"])
    namespace = {
        "asyncio": asyncio,
        "base64": base64,
        "json": json,
        "logger": logging.getLogger("selkies-hub-test"),
        "websockets": SimpleNamespace(ConnectionClosed=ConnectionClosed),
    }
    exec(compile(source, "signalling_web.py", "exec"), namespace)
    hub = namespace["Hub"]()
    return hub, hub.make_handler()


def _hello(uid: str, resume: bool = False) -> str:
    meta = {"res": "1440x900", "scale": 1}
    if resume:
        meta["matrx_resume"] = 1
    return f"HELLO {uid} {base64.b64encode(json.dumps(meta).encode()).decode()}"


async def _settle() -> None:
    for _ in range(20):
        await asyncio.sleep(0)


class Machine:
    """The hub with the app's video peer (0) in a session with the viewer (1)."""

    def __init__(self, patched: bool) -> None:
        self.hub, self.handler = _hub(patched)
        self.tasks: list[asyncio.Task] = []

    async def connect(self, socket: Socket) -> Socket:
        self.tasks.append(asyncio.create_task(self.handler(socket, "/signalling/")))
        await _settle()
        return socket

    async def session(self) -> tuple[Socket, Socket]:
        viewer = await self.connect(Socket("viewer", _hello("1")))
        app = await self.connect(Socket("app", "HELLO 0", "SESSION 1"))
        assert self.hub.sessions == {"0": "1", "1": "0"}
        return app, viewer

    async def relays(self, app: Socket, viewer: Socket) -> bool:
        app.inbox.put_nowait('{"ice": "app->viewer"}')
        await _settle()
        return '{"ice": "app->viewer"}' in viewer.sent

    async def close(self) -> None:
        for task in self.tasks:
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)


@pytest.mark.parametrize("code", [1006, 4001])
async def test_a_lost_viewer_link_keeps_the_session_and_the_page_resumes_into_it(code):
    machine = Machine(patched=True)
    app, viewer = await machine.session()
    viewer.end(code)  # 1006: the link died; 4001: the gateway says it was lost
    await _settle()
    assert app.close_code is None, "the app peer (and so the pipeline) must keep running"
    again = await machine.connect(Socket("viewer-again", _hello("1", resume=True)))
    assert again.sent == ["HELLO"]
    assert machine.hub.sessions == {"0": "1", "1": "0"}
    assert await machine.relays(app, again)
    await machine.close()


async def test_upstream_hub_ends_the_session_when_the_viewer_link_is_lost():
    """The defect, measured on the verbatim upstream text: proves the scenario discriminates."""
    machine = Machine(patched=False)
    app, viewer = await machine.session()
    viewer.end(1006)
    await _settle()
    assert app.close_code == 1000
    await machine.close()


async def test_the_viewers_own_close_still_ends_its_session():
    machine = Machine(patched=True)
    app, viewer = await machine.session()
    viewer.end(1000)
    await _settle()
    assert app.close_code == 1000
    assert machine.hub.sessions == {}
    await machine.close()


async def test_a_new_page_while_parked_ends_the_old_session_the_upstream_way():
    machine = Machine(patched=True)
    app, viewer = await machine.session()
    viewer.end(1006)
    await _settle()
    fresh = await machine.connect(Socket("new-page", _hello("1")))
    assert fresh.sent == ["HELLO"]
    assert app.close_code == 1000
    assert machine.hub.sessions == {} and machine.hub._matrx_parked == {}
    await machine.close()


async def test_a_resume_with_nothing_to_resume_is_refused_by_name():
    machine = Machine(patched=True)
    await machine.connect(Socket("app", "HELLO 0"))
    stray = await machine.connect(Socket("stray", _hello("1", resume=True)))
    assert stray.sent == ["ERROR matrx-no-session"]
    assert stray.close_code == 4002
    await machine.close()


async def test_a_resume_supersedes_an_old_link_that_is_still_closing():
    machine = Machine(patched=True)
    app, viewer = await machine.session()
    again = await machine.connect(Socket("viewer-again", _hello("1", resume=True)))
    assert viewer.close_code == 4003
    await _settle()
    assert again.sent == ["HELLO"]
    assert machine.hub.peers["1"][0] is again
    assert app.close_code is None
    assert await machine.relays(app, again)
    await machine.close()


async def test_app_messages_while_the_viewer_is_away_are_dropped_not_fatal():
    machine = Machine(patched=True)
    app, viewer = await machine.session()
    viewer.end(1006)
    await _settle()
    app.inbox.put_nowait('{"ice": "late"}')
    await _settle()
    assert app.close_code is None and "0" in machine.hub.peers
    await machine.close()
