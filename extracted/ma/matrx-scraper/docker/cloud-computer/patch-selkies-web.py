"""Turn the stock Selkies web client into the Cloud Computer screen page.

Run once at image build:
python patch-selkies-web.py <selkies-web dir> <stream-client dir> <selkies_gstreamer package dir>.
Every upstream file is checked against the exact bytes this patch was written
for (Selkies 1.6.2 portable); a different upstream fails the build instead of
shipping a half-patched page. Patched upstream files (MPL-2.0) are listed in
streaming/deploy/LICENSE-NOTE-selkies.md; their sources are this script plus
the upstream release.
"""
from __future__ import annotations

import hashlib
import shutil
import sys
from pathlib import Path

UPSTREAM_SHA256 = {
    "index.html": "e7961149233c0fd95f9ca9681c39dbaeac9d259736b2f96b105abb374da57f32",
    "app.js": "3ca67d4b5cc7dfed88470a61501231d2002708b12743048b39743a8a75118c3a",
    "signalling.js": "17829db232fc118ab9cac1b4463372bdcdd842e7bfa32f6140a7883639ef762d",
}
#: The Selkies Python package (``lib/python3.12/site-packages/selkies_gstreamer``).
PACKAGE_UPSTREAM_SHA256 = {
    "__main__.py": "714b3b2204d486ec26af882150c8631412d9d92091d14a2d4594f2d12f750843",
    "signalling_web.py": "ee9a448ab1746d18f8aeb2388fb23f829868c563d0f652a3d217b4843d646791",
}
VERSION = "6"

# Upstream waits for the browser's peer with ``time.sleep(2)`` inside an async
# error handler, once per media peer (video 0, audio 2). That loop is the same
# one that serves the screen page, its assets, every signalling handshake and
# HELLO, so until a viewer registered it was blocked ~4 s of every 4 s: live
# 2026-10-17 the page took 15 s to load and connect and another 4 s to register
# (FIX-CONNECT-2026-10-17). Wait without blocking, and start the session within
# 50 ms of the peer registering instead of on the next 4 s tick.
WAIT_FOR_PEER = """    async def _matrx_wait_for_peer(peer):
        while str(peer) not in server.peers:
            await asyncio.sleep(0.05)

    # Handle errors from the signalling server
"""


def _peer_wait(name: str) -> tuple[str, str]:
    old = (
        "           # Waiting for peer to connect, retry in 2 seconds.\n"
        "           time.sleep(2)\n"
        f"           await {name}.setup_call()\n"
    )
    new = (
        "           # Matrx: wait for the browser's peer without blocking the loop.\n"
        f"           await _matrx_wait_for_peer({name}.peer_id)\n"
        f"           await {name}.setup_call()\n"
    )
    return old, new


# Upstream's RTC-file callback only pokes the RUNNING video webrtcbin: it never
# updates ``app.turn_servers``, which every NEW session builds its pipeline
# from. A warm machine therefore opened every later session with the TURN
# credentials it started with; they expire after 120 s, so a viewer who closed
# the Computer and came back more than two minutes later got no relay route
# and sat on "Connecting..." for ever (live 2026-10-17, machine 681bba: relay
# offered only while the startup credentials were under 120 s old). And each
# rewrite ``add-turn-server``-ed one more entry into the live agent until
# libnice refused more than 8. Replace the lists on both apps (the next session
# uses the newest credentials) and never append to a live agent.
UPSTREAM_MON_RTC_CONFIG = """    # Callback method to update TURN servers of a running pipeline.
    def mon_rtc_config(stun_servers, turn_servers, rtc_config):
        if app.webrtcbin:
            logger.info("updating STUN server")
            app.webrtcbin.set_property("stun-server", stun_servers[0])
            for i, turn_server in enumerate(turn_servers):
                logger.info("updating TURN server")
                if i == 0:
                    app.webrtcbin.set_property("turn-server", turn_server)
                else:
                    app.webrtcbin.emit("add-turn-server", turn_server)
        server.set_rtc_config(rtc_config)
"""
MATRX_MON_RTC_CONFIG = """    # Matrx: the next session's pipeline is built from these lists; replace them.
    def mon_rtc_config(stun_servers, turn_servers, rtc_config):
        for _matrx_app in (app, audio_app):
            _matrx_app.stun_servers = list(stun_servers)
            _matrx_app.turn_servers = list(turn_servers)
        logger.info("RTC config replaced: %d STUN, %d TURN for the next session", len(stun_servers), len(turn_servers))
        server.set_rtc_config(rtc_config)
"""

# The signalling socket is NOT the session (2026-10-17, FIX-RELEASE-SURVIVAL).
# The viewer's signalling socket rides an aidream gateway task; every release
# drains that task and cuts the socket, while the picture itself is peer to
# peer. Upstream's hub answered any viewer socket close by closing the app
# peer's socket too (cleanup_session), which stops the pipeline: the screen
# went black every ~30 minutes. Now a viewer link that is LOST (any close but
# a viewer's own 1000/1001/1005) keeps its session parked; the same viewer's
# page re-opens signalling with ``matrx_resume`` in its HELLO and is put back
# in that session with nothing restarted. A fresh page (no resume) ends a
# parked session exactly the upstream way; a resume with nothing parked is
# refused (``ERROR matrx-no-session``) so the page resets the upstream way. A
# still-open old link (its gateway task still going away) is superseded.
HUB_INIT_OLD = "        self.sessions = dict()\n"
HUB_INIT_NEW = "        self.sessions = dict()\n        self._matrx_parked = dict()\n"
HUB_METHODS = """    ############### Matrx: a lost viewer link keeps its session ###############

    _MATRX_CLEAN_CLOSES = (1000, 1001, 1005)

    async def _matrx_hello(self, ws, uid, meta):
        resume = isinstance(meta, dict) and bool(meta.pop("matrx_resume", None))
        if not resume:
            if uid in self._matrx_parked:
                await self._matrx_end_parked(uid)
            return
        entry = self.peers.get(uid)
        if entry is not None and entry[2] == 'session' and uid in self.sessions:
            # The old link is still closing (its gateway task is going away).
            old = entry[0]
            del self.peers[uid]
            self._matrx_parked[uid] = self.sessions.pop(uid)
            logger.info("Matrx: peer {} re-opened signalling; old link superseded".format(uid))
            await old.close(code=4003, reason='superseded')
        if uid not in self._matrx_parked:
            await ws.send('ERROR matrx-no-session')
            await ws.close(code=4002, reason='no session to resume')
            raise Exception("Matrx: no session to resume for {!r}".format(uid))

    def _matrx_take_parked(self, uid):
        other = self._matrx_parked.pop(uid, None)
        if other is None or other not in self.peers or self.sessions.get(other) != uid:
            return None
        self.sessions[uid] = other
        logger.info("Matrx: peer {} resumed its session with {}".format(uid, other))
        return 'session'

    async def _matrx_end_parked(self, uid):
        other = self._matrx_parked.pop(uid)
        logger.info("Matrx: peer {} came back as a new page; ending its session with {}".format(uid, other))
        if self.sessions.get(other) == uid:
            del self.sessions[other]
        if other in self.peers:
            wso = self.peers.pop(other)[0]
            await wso.close()

    async def _matrx_remove_peer(self, uid, ws):
        entry = self.peers.get(uid)
        if entry is None or entry[0] is not ws:
            return  # already removed with its partner, or superseded by a newer link
        other = self.sessions.get(uid)
        code = getattr(ws, 'close_code', None)
        if (other is not None and other in self.peers and self.sessions.get(other) == uid
                and code is not None and code not in self._MATRX_CLEAN_CLOSES):
            del self.peers[uid]
            del self.sessions[uid]
            self._matrx_parked[uid] = other
            logger.info("Matrx: peer {} link lost (code {}); session with {} kept for its return".format(uid, code, other))
            return
        for parked, partner in list(self._matrx_parked.items()):
            if partner == uid:
                del self._matrx_parked[parked]
        await self.remove_peer(uid)

    ############### Handler functions ###############
"""
HUB_EDITS = [
    (HUB_INIT_OLD, HUB_INIT_NEW),
    ("    ############### Handler functions ###############\n", HUB_METHODS),
    (
        "        raddr = ws.remote_address\n        peer_status = None\n        self.peers[uid] = [ws, raddr, peer_status, meta]\n",
        "        raddr = ws.remote_address\n        peer_status = self._matrx_take_parked(uid)\n        self.peers[uid] = [ws, raddr, peer_status, meta]\n",
    ),
    (
        "                    other_id = self.sessions[uid]\n                    wso, oaddr, status, _ = self.peers[other_id]\n",
        "                    other_id = self.sessions[uid]\n"
        "                    if other_id not in self.peers:\n"
        "                        logger.info(\"Matrx: {} is re-opening signalling; dropped {} -> {}\".format(other_id, uid, other_id))\n"
        "                        continue\n"
        "                    wso, oaddr, status, _ = self.peers[other_id]\n",
    ),
    (
        "        if not uid or uid in self.peers or uid.split() != [uid]: # no whitespace\n"
        "            await ws.close(code=1002, reason='invalid peer uid')\n"
        "            raise Exception(\"Invalid uid {!r} from {!r}\".format(uid, raddr))\n"
        "        meta = None\n"
        "        if metab64str:\n"
        "            meta = json.loads(base64.b64decode(metab64str))\n",
        "        meta = None\n"
        "        if metab64str:\n"
        "            meta = json.loads(base64.b64decode(metab64str))\n"
        "        await self._matrx_hello(ws, uid, meta)\n"
        "        if not uid or uid in self.peers or uid.split() != [uid]: # no whitespace\n"
        "            await ws.close(code=1002, reason='invalid peer uid')\n"
        "            raise Exception(\"Invalid uid {!r} from {!r}\".format(uid, raddr))\n",
    ),
    ("                await self.remove_peer(peer_id)\n", "                await self._matrx_remove_peer(peer_id, ws)\n"),
]

PACKAGE_EDITS = {
    "signalling_web.py": HUB_EDITS,
    "__main__.py": [
        ("    # Handle errors from the signalling server\n", WAIT_FOR_PEER),
        _peer_wait("signalling"),
        _peer_wait("audio_signalling"),
        (UPSTREAM_MON_RTC_CONFIG, MATRX_MON_RTC_CONFIG),
    ],
}

EDITS = {
    "index.html": [
        ("</head>", f'  <link href="matrx-stream.css?v={VERSION}" rel="stylesheet" />\n</head>'),
        (
            '<script src="app.js?ts=1723709107"></script>',
            '<script src="app.js?ts=1723709107"></script>\n'
            f'<script src="matrx-stream.js?v={VERSION}"></script>',
        ),
    ],
    "app.js": [
        # The stock service worker caches the page under a fixed version, so a
        # patched page could be served stale; the screen page runs without it.
        (
            "navigator.serviceWorker.register('./sw.js?ts=1723709107');",
            "navigator.serviceWorker.getRegistrations().then((rs) => rs.forEach((r) => r.unregister()));",
        ),
    ],
    "signalling.js": [
        # After three failed reconnects Selkies navigated the page to the site
        # root (stream.aimatrx.com/), leaving the person on a dead page. Keep
        # retrying in place; the embedding app shows "reconnecting".
        (
            'window.location.replace(window.location.href.replace(window.location.pathname, "/"));',
            "this.retry_count = 0; this.connect();",
        ),
        # A page whose picture is still live re-opens signalling as a RESUME
        # (matrx-stream.js sets matrx_resume); the hub puts it back in its
        # session instead of starting a new one.
        (
            '            "scale": window.devicePixelRatio\n        };\n',
            '            "scale": window.devicePixelRatio\n        };\n'
            "        if (this.matrx_resume) meta.matrx_resume = 1;\n",
        ),
    ],
}


def patch_text(name: str, text: str, edits: list[tuple[str, str]]) -> str:
    for old, new in edits:
        if text.count(old) != 1:
            raise SystemExit(f"{name}: expected exactly one {old[:60]!r}")
        text = text.replace(old, new)
    return text


def _check(root: Path, digests: dict[str, str]) -> None:
    for name, digest in digests.items():
        actual = hashlib.sha256((root / name).read_bytes()).hexdigest()
        if actual != digest:
            raise SystemExit(f"upstream {name} changed ({actual}); re-check the Selkies patch")


def _apply(root: Path, edits: dict[str, list[tuple[str, str]]]) -> None:
    for name, file_edits in edits.items():
        path = root / name
        path.write_text(patch_text(name, path.read_text(encoding="utf-8"), file_edits), encoding="utf-8")


def main(web: Path, client: Path, package: Path) -> None:
    _check(web, UPSTREAM_SHA256)
    _check(package, PACKAGE_UPSTREAM_SHA256)
    _apply(web, EDITS)
    _apply(package, PACKAGE_EDITS)
    # A stale bytecode cache must never run in place of the patched source.
    for stale in (package / "__pycache__").glob("__main__.*.pyc"):
        stale.unlink()
    for name in ("matrx-stream.js", "matrx-stream.css"):
        shutil.copyfile(client / name, web / name)
        (web / name).chmod(0o644)
    print("selkies web client patched for the Cloud Computer screen page")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
