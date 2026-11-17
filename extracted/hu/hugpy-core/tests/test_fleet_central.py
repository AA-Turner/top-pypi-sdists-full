"""One central made of every host's central drive: a model held by two hosts is one model with two holders, and a
copy is relayed from its holder under a token for that one copy (operator 2026-11-14)."""
import json
import threading
import urllib.error
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from werkzeug.serving import make_server

from hugpy_core.registry import fleet_central, registrations
from hugpy_core.web import worker_link


def test_the_same_model_on_two_centrals_is_one_model_with_two_holders(monkeypatch):
    now = datetime.now(timezone.utc)
    row = dict(bytes=10, engine="llama-server", files=1, seen_at=now)
    monkeypatch.setattr(fleet_central, "_all_rows", lambda: [
        dict(row, holder="ae", key="org/m", variation="m.gguf", content_id="c1", basis="sha256"),
        dict(row, holder="a-brain", key="mirror/m", variation="m.gguf", content_id="c1", basis="sha256"),  # same bytes
        dict(row, holder="ae", key="org/x", variation="x.gguf", content_id=None, basis="size"),
        dict(row, holder="computron", key="org/x", variation="x.gguf", content_id=None, basis="size"),
        dict(row, holder="computron", key="org/x", variation="x.gguf", bytes=11, content_id=None, basis="size"),
        dict(row, holder="freshbox", key="org/m", variation="m.gguf", content_id=None, basis="size"),   # not proved yet
        dict(row, holder="gone", key="org/m", variation="m.gguf", content_id="c1", basis="sha256"),      # disconnected
        dict(row, holder="a-brain", key="cache/pip/http-v2/0/0", variation="ab12", bytes=499, engine=None,
             content_id=None, basis="size")])
    monkeypatch.setattr(fleet_central, "_connected", lambda: {"ae", "a-brain", "computron", "freshbox"})
    catalog = fleet_central.catalog()
    assert all(m["key"] != "cache/pip/http-v2/0/0" for m in catalog)                # no engine, no task: left out
    assert any(m["key"] == "cache/pip/http-v2/0/0" for m in fleet_central.catalog(include_unservable=True))
    merged = {(m["key"], m["bytes"]): sorted(h["holder"] for h in m["holders"]) for m in catalog}
    assert merged == {("org/m", 10): ["a-brain", "ae", "freshbox"], ("org/x", 10): ["ae", "computron"],
                      ("org/x", 11): ["computron"]}
    m = next(m for m in catalog if m["key"] == "org/m")
    assert {h["holder"]: h["verified"] for h in m["holders"]} == {"ae": True, "a-brain": True, "freshbox": False}


def test_a_copy_is_relayed_from_its_holder_under_its_own_token(tmp_path, monkeypatch):
    monkeypatch.setenv("HUGPY_CORE_STATE_DIR", str(tmp_path))
    data = bytes(range(256)) * 64

    class Holder(BaseHTTPRequestHandler):
        def do_GET(self):
            q = {k: v[0] for k, v in parse_qs(urlparse(self.path).query).items()}
            ok = urlparse(self.path).path == "/v1/central/file" and q["offer"] == "ofr_1" and q["rel"] == "m.gguf"
            body = data[int(q["offset"]): int(q["offset"]) + int(q["length"])] if ok else b"{}"
            self.send_response(200 if ok else 404)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    holder = HTTPServer(("127.0.0.1", 0), Holder)
    threading.Thread(target=holder.serve_forever, daemon=True).start()
    saved = {"ae": {"name": "ae", "url": f"http://127.0.0.1:{holder.server_port}", "key": "k"}}
    monkeypatch.setattr(registrations, "get", saved.get)
    door = worker_link.wrap(lambda environ, start: (start("404 Not Found", []), [b""])[1])
    core = make_server("127.0.0.1", 0, door, threaded=True)
    threading.Thread(target=core.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{core.port}/fleet-link/relay"

    def get(token, rel="m.gguf", offset=100, length=50, auth=None):
        req = urllib.request.Request(f"{base}/{token}/file?rel={rel}&offset={offset}&length={length}",
                                     headers={"Authorization": "Bearer " + (auth or token)})
        try:
            with urllib.request.urlopen(req, timeout=10) as reply:
                return reply.status, reply.read()
        except urllib.error.HTTPError as exc:
            return exc.code, exc.read()
    try:
        token = fleet_central.mint("ae", "org/m", "m.gguf", "a-brain", offer="ofr_1")
        assert get(token) == (200, data[100:150])
        assert get(token, rel="other.gguf")[0] == 404                              # only the files the holder lists
        other = fleet_central.mint("ae", "org/other", "o.gguf", "a-brain", offer="ofr_2")
        assert get(other)[0] == 404                                # the holder serves only the offer the token names
        assert get(token, auth="hcr1.forged.sig")[0] == 401
        assert get(token[:-4] + "0000")[0] == 401                                  # signed by this Core
        assert fleet_central.verify(fleet_central.mint("ae", "org/m", "m.gguf", "a-brain", ttl=-1)) is None
    finally:
        core.shutdown()
        holder.shutdown()
        holder.server_close()


def test_the_destination_is_sent_the_copy_only_once_holders_confirmed_it(tmp_path, monkeypatch):
    """Core asks the holders first (a proved copy, a host it reaches directly, first): one that declines is passed
    over, one whose files differ is not used (its offer closed); the destination gets the request ready, with every
    confirmed holder to pull from, each under a token bound to that holder's offer."""
    from hugpy_core.registry import transport
    monkeypatch.setenv("HUGPY_CORE_STATE_DIR", str(tmp_path))
    monkeypatch.setenv("HUGPY_SELF_BASE", "https://core.example")
    workers = {n: {"name": n, "url": f"http://10.0.0.{i}:15102"} for i, n in enumerate(("ae", "b", "c", "d"))}
    workers["a-brain"] = {"name": "a-brain", "url": "http://127.0.0.1:7020/_link/a-brain", "link": True}
    monkeypatch.setattr(registrations, "get", workers.get)
    monkeypatch.setattr(fleet_central, "holders", lambda key, variation: [
        dict(holder=n, content_id="c1") for n in ("ae", "b", "c", "d")])
    monkeypatch.setattr(fleet_central, "_live_copy", lambda *a: None)
    rows = []
    monkeypatch.setattr(fleet_central, "_insert_copy", lambda *a: rows.append(a) or 7)
    files = [dict(rel="m.gguf", bytes=10, sha256="s", weights=True)]
    sent, job = [], {}

    def request(worker, path, body=None, **kw):
        sent.append((worker["name"], path))
        if path == "/v1/central/offer":
            if worker["name"] == "ae":
                raise RuntimeError("Worker HTTP 403: this host does not share its central drive")
            other = ([dict(files[0], sha256="different")] if worker["name"] == "c" else
                     [dict(files[0], sha256=None)] if worker["name"] == "d" else files)   # d: not proved yet
            return dict(offer=f"ofr_{worker['name']}", confirmed_at=1.0, files=other)
        if path == "/v1/central/offer/close":
            return {"closed": True}
        job.update(body)
        return dict(state="copying")
    monkeypatch.setattr(transport, "request", request)
    done = fleet_central.fetch("a-brain", "org/m", "m.gguf")
    assert done["state"] == "sent" and done["copy"] == 7 and done["holders"] == ["b", "d"]
    assert [d.split(":")[0] for d in done["declined"]] == ["ae", "c"]
    assert ("c", "/v1/central/offer/close") in sent                                   # the odd one's offer closed
    assert sent[-1] == ("a-brain", "/v1/central/fetch") and job["copy"] == 7 and job["files"] == files
    assert [fleet_central.verify(s["token"])["o"] for s in job["sources"]] == ["ofr_b", "ofr_d"]
    assert all(s["url"].startswith("https://core.example/fleet-link/relay/") for s in job["sources"])
    assert rows[0][3] == [dict(holder="b", offer="ofr_b"), dict(holder="d", offer="ofr_d")]


def test_a_call_for_a_model_only_another_hosts_central_holds_is_served_once_copied(monkeypatch):
    """The call's worker is the one routing ranks first; one that refuses the copy passes to the next; the call is
    served once the copy is whole there, and told to retry (503) when it is still copying."""
    now = datetime.now(timezone.utc)
    monkeypatch.setattr(fleet_central, "_all_rows", lambda: [
        dict(holder="ae", key="org/m", variation="big.gguf", bytes=90, engine="llama-server", files=1,
             content_id="c2", basis="sha256", seen_at=now),
        dict(holder="ae", key="org/m", variation="small.gguf", bytes=10, engine="llama-server", files=1,
             content_id="c1", basis="sha256", seen_at=now)])
    monkeypatch.setattr(fleet_central, "_connected", lambda: {"ae", "w1", "w2"})
    assert fleet_central.resolve("org/m") == ("org/m", "small.gguf")       # a bare key: its proved, smallest
    assert fleet_central.resolve("org/m::big.gguf") == ("org/m", "big.gguf")
    assert fleet_central.resolve("other/x") is None
    monkeypatch.setattr(registrations, "get", lambda n: {"name": n})
    asked = []

    def fetch(dest, key, variation, reason="operator"):
        asked.append(dest)
        if dest == "w1":
            raise OSError("Worker HTTP 507: the central drive has 0.5 GiB free")
        return dict(state="sent", bytes=10)
    monkeypatch.setattr(fleet_central, "fetch", fetch)
    monkeypatch.setattr(fleet_central, "wait", lambda *a: dict(state="done", served=True))
    workers = [dict(name="w2", rank=2), dict(name="w1", rank=1)]
    got = fleet_central.provide("org/m", workers, rank=lambda w: w["rank"])
    assert got["name"] == "w2" and asked == ["w1", "w2"]
    monkeypatch.setattr(fleet_central, "wait", lambda *a: dict(state="copying", done_bytes=4, timed_out=True))
    import pytest
    with pytest.raises(fleet_central.CopyPending):
        fleet_central.provide("org/m", [dict(name="w2")])
    assert fleet_central.provide("other/x", workers) is None                # no central holds it: routing as before
    monkeypatch.setattr(fleet_central, "fetch", lambda *a, **k: dict(state="present"))
    monkeypatch.setattr(fleet_central, "wait", lambda *a: (_ for _ in ()).throw(AssertionError("waited")))
    assert fleet_central.provide("org/m", [dict(name="w2")])["name"] == "w2"   # it holds it: no wait


def test_a_console_row_says_where_every_copy_is_and_what_the_model_is(monkeypatch):
    """The fleet models database fills the model list's columns: where (host:drive roles, '?' unproved), the
    smallest proved quant as its size, and Discovery's task, framework, context (operator 2026-11-15)."""
    from hugpy_core.web.routes import _fleet_fields
    now = datetime.now(timezone.utc)
    row = dict(engine="llama-server", files=1, seen_at=now, task="text-generation", arch="qwen3", layers=48,
               ctx_train=262144, expert_count=None, expert_used_count=None)
    monkeypatch.setattr(fleet_central, "_all_rows", lambda: [
        dict(row, holder="ae", key="org/m", variation="m-Q8.gguf", bytes=80, content_id="c8", basis="sha256",
             source_role="central", locations=[dict(role="central"), dict(role="immutable")]),
        dict(row, holder="a-brain", key="org/m", variation="m-Q4.gguf", bytes=40, content_id=None, basis="size",
             source_role="worker", locations=[dict(role="worker")])])
    monkeypatch.setattr(fleet_central, "_connected", lambda: {"ae", "a-brain"})
    f = _fleet_fields(fleet_central.by_key()["org/m"])
    assert f["fleet_where"] == ["a-brain:worker?", "ae:central+immutable"]
    assert f["framework"] == "gguf" and f["model_max_length"] == 262144 and f["arch"] == "qwen3"
    assert f["effective_gguf"] == "m-Q8.gguf" and f["size_bytes"] == 80           # the proved one first
    assert [v["variation"] for v in f["fleet_variations"]] == ["m-Q8.gguf", "m-Q4.gguf"]


def test_video_models_are_what_they_can_render_and_available_only_on_a_connected_host(monkeypatch):
    """Video chooses by capability (2026-11-15): a model's tasks are what its declared pipeline renders, not its
    catalog tag, and it is available only when a connected host holds it."""
    from contextlib import contextmanager
    from hugpy_core.relay import inference_catalog
    now = datetime.now(timezone.utc)
    row = dict(files=1, seen_at=now, content_id=None, basis="size", source_role="central", locations=[],
               task="text-to-video", arch=None, layers=None, ctx_train=None, expert_count=None,
               expert_used_count=None, class_names=[], bytes=10, engine="videogen", variation="*")
    monkeypatch.setattr(fleet_central, "_all_rows", lambda: [
        dict(row, holder="ae", key="org/i2v", capabilities=["i2v"]),
        dict(row, holder="ae", key="org/vace", capabilities=["extend", "reference", "t2v", "v2v"]),
        dict(row, holder="gone", key="org/away", capabilities=["t2v"])])
    monkeypatch.setattr(fleet_central, "_connected", lambda: {"ae"})
    table = [dict(model_key="org/i2v::*", primary_task="text-to-video", metadata={}, framework="diffusers"),
             dict(model_key="org/away", primary_task="text-to-video", metadata={}, framework="diffusers")]

    class Conn:
        def execute(self, *a):
            return self

        def fetchall(self):
            return table

    monkeypatch.setattr(inference_catalog, "_conn", contextmanager(lambda: (yield Conn())))
    models = inference_catalog.video_models()
    assert models["org/i2v::*"].tasks == ("image-to-video",) and models["org/i2v::*"].extra["available"] is True
    assert models["org/vace"].tasks == ("text-to-video", "video-to-video")
    assert models["org/away"].extra["available"] is False            # held only by a host that is not connected


def test_pickers_offer_what_can_serve_a_call_with_the_inputs_it_needs(monkeypatch):
    """Browser pickers (2026-11-16): a model's tasks and required inputs come from the engine and pipeline that
    serve it, not its catalog tag; a pipeline's sub-folders and key::* twins are not offered; availability says
    whether an online worker serves it now and which connected hosts hold it."""
    from contextlib import contextmanager
    from hugpy_core.relay import inference_catalog
    from hugpy_core.web import routes
    now = datetime.now(timezone.utc)
    row = dict(files=1, seen_at=now, content_id=None, basis="size", source_role="central", locations=[],
               task="text-to-image", arch=None, layers=None, ctx_train=None, expert_count=None,
               expert_used_count=None, bytes=10, variation="*", capabilities=[], holder="ae")
    monkeypatch.setattr(fleet_central, "_all_rows", lambda: [
        dict(row, key="org/edit", engine="imagegen", class_names=["QwenImageEditPlusPipeline"]),
        dict(row, key="org/encoder", engine="llama-server", class_names=[], variation="enc-q4.gguf"),
        dict(row, key="org/Wan-I2V", engine="videogen", class_names=["WanModel"], task="text-to-video"),
        dict(row, key="org/flux", engine="imagegen", class_names=["Flux2Pipeline"], holder="brain")])
    monkeypatch.setattr(fleet_central, "_connected", lambda: {"ae", "brain"})
    table = [dict(model_key=k, primary_task=t, metadata={}, framework=None) for k, t in (
        ("org/edit", "text-to-image"), ("org/edit::*", "text-to-image"), ("org/edit/text_encoder", "text-generation"),
        ("org/encoder", "text-to-image"), ("org/Wan-I2V", "text-to-video"), ("org/flux", "text-to-image"))]

    class Conn:
        def execute(self, *a):
            return self

        def fetchall(self):
            return table

    monkeypatch.setattr(inference_catalog, "_conn", contextmanager(lambda: (yield Conn())))
    monkeypatch.setattr(routes, "model_rows", lambda: [
        dict(id=k, available=True, workers=["ae"]) for k in ("org/edit", "org/encoder", "org/Wan-I2V")])
    rows = {r["id"]: r for r in inference_catalog.picker_models()}
    assert set(rows) == {"org/edit", "org/encoder", "org/Wan-I2V", "org/flux"}
    assert rows["org/edit"]["tasks"] == ["image-to-image"] and rows["org/edit"]["needs"] == ["image", "text"]
    assert rows["org/encoder"]["tasks"] == ["text-generation"]             # a chat unit, never an image model
    assert rows["org/Wan-I2V"]["tasks"] == ["image-to-video"] and rows["org/Wan-I2V"]["needs"] == ["image"]
    assert rows["org/flux"]["needs"] == ["text"] and rows["org/flux"]["available"] is False
    assert rows["org/flux"]["held_by"] == ["brain"] and rows["org/edit"]["hosts"] == ["ae"]
