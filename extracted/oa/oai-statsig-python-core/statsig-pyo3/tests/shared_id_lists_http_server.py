"""Local, synthetic HTTP service shared by ID-list tests and memory benchmarks.

No SDK is imported here. Keep this process separate from SDK worker cgroups
when measuring memory so fixture serving costs cannot look like SDK savings.
"""

import argparse
import base64
from collections import defaultdict, deque
import gzip
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import threading
import time
from urllib.parse import unquote, urlsplit


def member_key(user_id):
    return base64.b64encode(hashlib.sha256(user_id.encode()).digest()).decode()[:8]


def changeset(add_users=(), remove_users=()):
    return "".join(f"+{member_key(user)}\n" for user in add_users) + "".join(
        f"-{member_key(user)}\n" for user in remove_users
    )


def _specs(names):
    gates, configs, conditions = {}, {}, {}
    for index, name in enumerate(names):
        condition = f"member-{index}"
        rule = {"name": condition, "id": condition, "salt": condition,
                "conditions": [condition], "passPercentage": 100,
                "returnValue": True, "idType": "userID"}
        gate = {"type": "feature_gate", "entity": "feature_gate", "salt": condition,
                "enabled": True, "defaultValue": False, "idType": "userID",
                "version": 1, "rules": [rule]}
        config = {**gate, "type": "dynamic_config", "entity": "dynamic_config",
                  "defaultValue": {"member": False},
                  "rules": [{**rule, "returnValue": {"member": True}}]}
        gates[name], configs[name] = gate, config
        if index == 0:
            gates["membership"], configs["membership"] = gate, config
        conditions[condition] = {"type": "unit_id", "operator": "in_segment_list",
                                 "targetValue": name, "idType": "userID"}
    return {"time": 1_800_000_100_001, "has_updates": True,
            "feature_gates": gates, "dynamic_configs": configs, "layer_configs": {},
            "experiment_to_layer": {}, "condition_map": conditions}


def resource_snapshot():
    """Optional Linux accounting; the ordinary fixture stays usable on macOS."""
    rollup = Path('/proc/self/smaps_rollup')
    if not rollup.exists():
        return None
    memory = {}
    for line in rollup.read_text().splitlines():
        fields = line.split()
        if len(fields) == 3 and fields[2] == 'kB':
            memory[fields[0].rstrip(':')] = int(fields[1]) * 1024
    result = {'pid': os.getpid(), 'process_memory': memory}
    cgroup = Path('/sys/fs/cgroup')
    for name in ['memory.current', 'memory.peak', 'memory.max']:
        path = cgroup / name
        if path.exists(): result[name] = path.read_text().strip()
    for name in ['memory.stat', 'cpu.stat']:
        path = cgroup / name
        if path.exists(): result[name] = {key:int(value) for key,value in
                                         (line.split() for line in path.read_text().splitlines())}
    return result


class IdListHTTPFixture:
    def __init__(self, initial_lists=None, counts=None, host="127.0.0.1", port=0):
        self.lock = threading.RLock()
        self.files = {}
        self.manifest = {}
        self.counters = defaultdict(lambda: defaultdict(int))
        self.recent_requests = deque(maxlen=2000)
        self.failures = {}
        self.generation = 0
        self.server = ThreadingHTTPServer((host, port), self._handler())
        self.server.daemon_threads = True
        self.host = host
        self.port = self.server.server_address[1]
        self.thread = None
        if counts is not None:
            if not isinstance(counts, dict):
                counts = {"members" if index == 0 else f"list-{index}": count
                          for index, count in enumerate(counts)}
            # Files use the SDK's actual user-ID hash encoding. A temporary
            # bytearray avoids a Python object per membership in the fixture.
            for name, count in counts.items():
                body = bytearray()
                for index in range(count):
                    body.extend(f"+{member_key(f'user-{index}')}\n".encode())
                self._install(name, bytes(body), f"{name}-initial", 1)
        else:
            initial_lists = initial_lists or {"members": ["alice", "steady"]}
            for name, users in initial_lists.items():
                self._install(name, changeset(users).encode(), f"{name}-initial", 1)
        self.initial_files = self.files.copy()
        self.initial_manifest = {name: metadata.copy() for name, metadata in self.manifest.items()}
        self.specs = _specs(list(self.manifest))

    def url(self, path):
        host = "127.0.0.1" if self.host == "0.0.0.0" else self.host
        return f"http://{host}:{self.port}{path}"

    def _install(self, name, body, file_id, creation_time):
        self.files[file_id] = body
        self.manifest[name] = {"name": name, "url": self.url(f"/files/{file_id}"),
                               "size": len(body), "creationTime": creation_time,
                               "fileID": file_id}

    def state(self):
        with self.lock:
            return {"generation": self.generation,
                    "manifest": {name: value.copy() for name, value in self.manifest.items()},
                    "files": {key: len(value) for key, value in self.files.items()},
                    "counters": {worker: dict(values) for worker, values in self.counters.items()},
                    "recent_requests": list(self.recent_requests), "failures": self.failures.copy(),
                    "resources": resource_snapshot()}

    def control(self, command):
        with self.lock:
            op = command["op"]
            if op == "reset_counters":
                self.counters.clear()
                self.recent_requests.clear()
            elif op == "reset":
                self.files = self.initial_files.copy()
                self.manifest = {name: value.copy() for name, value in self.initial_manifest.items()}
                self.generation = 0
                self.failures = {}
                self.counters.clear()
                self.recent_requests.clear()
            elif op == "set_failures":
                self.failures = {key: value for key, value in command.items() if key != "op"}
            elif op == "set_manifest":
                if "names" in command:
                    self.manifest = {name: self.manifest[name] for name in command["names"]}
                else:
                    self.manifest = {name: value.copy() for name, value in command["manifest"].items()}
                self.generation += 1
            elif op in {"append", "replace"}:
                updates = command.get("updates", {command.get("list", "members"): command})
                for name, update in updates.items():
                    if isinstance(update, str):
                        update = {"body": update}
                    body = update.get("body")
                    if body is None:
                        body = changeset(update.get("users", update.get("add_users", [])),
                                         update.get("remove_users", []))
                    body = body.encode()
                    if op == "append":
                        metadata = self.manifest[name]
                        file_id = metadata["fileID"]
                        self.files[file_id] += body
                        metadata["size"] = len(self.files[file_id])
                    else:
                        generation = self.generation + 2
                        self._install(name, body, update.get("file_id", f"{name}-generation-{generation}"),
                                      update.get("creation_time", generation))
                self.generation += 1
            else:
                raise ValueError(f"Unknown control operation: {op}")
            return self.state()

    def _handler(self):
        fixture = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, *_):
                pass

            def do_GET(self):
                self.handle_request()

            def do_POST(self):
                self.handle_request()

            def handle_request(self):
                path = urlsplit(self.path).path
                request_body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
                if path == "/control/state":
                    self.respond(200, json.dumps(fixture.state()).encode(), "application/json")
                    return
                if path == "/control":
                    try:
                        result = fixture.control(json.loads(request_body))
                    except (ValueError, KeyError, TypeError) as error:
                        self.respond(400, json.dumps({"error": str(error)}).encode(), "application/json")
                        return
                    self.respond(200, json.dumps(result).encode(), "application/json")
                    return
                worker = self.headers.get("x-request-service", "unknown")
                with fixture.lock:
                    delay = fixture.failures.get("delay_ms", 0) / 1000
                if delay:
                    time.sleep(delay)
                extra = {}
                with fixture.lock:
                    record = {"worker": worker, "path": path}
                    if path.startswith("/v2/download_config_specs"):
                        status, body, kind = 200, json.dumps(fixture.specs).encode(), "specs"
                    elif path == "/v1/get_id_lists":
                        status = fixture.failures.get("manifest_status", 200)
                        body, kind = json.dumps(fixture.manifest).encode(), "manifest"
                    elif path.startswith("/files/"):
                        file_id = unquote(path.removeprefix("/files/"))
                        status = fixture.failures.get("file_status", {}).get(
                            file_id, fixture.failures.get("all_files_status", 206))
                        kind = "file"
                        if file_id not in fixture.files:
                            status, body = 404, b"unknown file"
                        else:
                            data = fixture.files[file_id]
                            requested = self.headers.get("Range", "bytes=0-")
                            start = int(requested.removeprefix("bytes=").split("-", 1)[0])
                            end = min(int(self.headers.get("statsig-id-list-file-size", len(data))), len(data))
                            record.update(file_id=file_id, start=start, end=end)
                            if start >= end:
                                status, body = 416, b"empty or invalid range"
                            else:
                                body = memoryview(data)[start:end]
                                extra["Content-Range"] = f"bytes {start}-{end - 1}/{end}"
                    elif path == "/v1/log_event":
                        encoding = self.headers.get("Content-Encoding")
                        if encoding == "gzip":
                            request_body = gzip.decompress(request_body)
                        elif encoding == "zstd":
                            import zstandard

                            request_body = zstandard.ZstdDecompressor().decompress(request_body)
                        payload = json.loads(request_body)
                        record["events"] = [
                            {"name": event["eventName"],
                             "user_id": event.get("user", {}).get("userID")}
                            for event in payload["events"]
                        ]
                        status, body, kind = 200, b'{"success":true}', "events"
                    else:
                        status, body, kind = 404, b"unknown path", "unknown"
                    fixture.counters[worker][f"{kind}_requests"] += 1
                    fixture.counters[worker][f"{kind}_bytes"] += len(body)
                    fixture.counters[worker][f"status_{status}"] += 1
                    record.update(status=status, bytes=len(body))
                    fixture.recent_requests.append(record)
                self.respond(status, body, "text/plain" if kind == "file" else "application/json", extra)

            def respond(self, status, body, content_type, extra=None):
                self.send_response(status)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(body)))
                for key, value in (extra or {}).items():
                    self.send_header(key, value)
                self.end_headers()
                try:
                    self.wfile.write(body)
                except (BrokenPipeError, ConnectionResetError):
                    # A killed SDK reader can close an in-flight test response.
                    pass

        return Handler

    def start(self):
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        return self

    def close(self):
        if self.thread is not None:
            self.server.shutdown()
            self.thread.join()
        self.server.server_close()

    def __enter__(self):
        return self.start()

    def __exit__(self, *_):
        self.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--counts", type=Path)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    counts = list(map(int, args.counts.read_text().split())) if args.counts else None
    with IdListHTTPFixture(counts=counts, host=args.host, port=args.port) as fixture:
        print(json.dumps({"ready": True, "url": fixture.url(""), "pid": os.getpid(),
                          "lists": len(fixture.manifest)}), flush=True)
        threading.Event().wait()


if __name__ == "__main__":
    main()
