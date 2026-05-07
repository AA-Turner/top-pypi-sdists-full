import os
import signal
import time
from hashlib import sha256
from queue import Empty, Queue
from threading import Event

import click
import grpc

from .. import terminal
from ..channel import ServiceClient, pass_service_client
from ..typestubs import generate_type_stubs
from ..clients.capsule import (
    ListAppsRequest,
    ListAppsResponse,
    ServeAttachRequest,
    ServeStreamMessage,
    ServeSyncRequest,
    StartServeRequest,
    StartServeResponse,
)
from ..utils import (
    resolve_entry_point,
    collect_source_archive,
    build_image_spec,
    build_channel_specs,
    build_filesystem_mount_specs,
    build_integration_specs,
    build_schedule_specs,
    normalize_image,
)

SYNC_INTERVAL = 0.1
HEARTBEAT_INTERVAL = 5.0
GATEWAY_READY_TIMEOUT = 5.0
START_SERVE_TIMEOUT = 180.0
BUILD_LOG_PREFIX = "Image build: "

_WATCHED_EXTENSIONS = (
    ".py", ".tsx", ".ts", ".jsx", ".js",
    ".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico",
    ".css", ".json", ".yaml", ".yml", ".toml",
    ".html", ".md", ".txt",
)
_IGNORED_WATCH_DIRS = {".git", ".venv", "__pycache__", "node_modules"}


def _handle_status(spinner, status: str, build_logs_seen: bool) -> bool:
    if status.startswith(BUILD_LOG_PREFIX):
        if not build_logs_seen:
            terminal.header("Build logs")
            build_logs_seen = True
        terminal.detail(f"  │ {status[len(BUILD_LOG_PREFIX):]}", dim=True)
        spinner.update("Building image...")
        return build_logs_seen

    spinner.update(status)
    return build_logs_seen


@click.command("serve")
@click.argument("entry_point")
@click.option(
    "--channel",
    "channel_names",
    multiple=True,
    help="Bind channel(s) to this serve (repeatable). Use --force-channel to rebind already-bound channels.",
)
@click.option(
    "--force-channel", is_flag=True, help="Unbind channels from their current app before rebinding."
)
@pass_service_client
def serve(
    client: ServiceClient, entry_point: str, channel_names: tuple[str, ...], force_channel: bool
):
    """Serve an app with hot-reload.

    ENTRY_POINT is <file.py>:<Name>, e.g. app.py:DietCoach or app.py:app
    """
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer

    shutdown = Event()

    def _handle_signal(signum, frame):
        shutdown.set()

    signal.signal(signal.SIGTERM, _handle_signal)
    signal.signal(signal.SIGINT, _handle_signal)
    if hasattr(signal, "SIGHUP"):
        signal.signal(signal.SIGHUP, _handle_signal)

    class _SyncHandler(FileSystemEventHandler):
        def __init__(self, queue: Queue, root: str):
            super().__init__()
            self.queue = queue
            self.root = os.path.abspath(root)
            self._known_hashes: dict[str, str] = {}

        def _is_watched(self, path: str) -> bool:
            return any(path.endswith(ext) for ext in _WATCHED_EXTENSIONS)

        def _normalize(self, path: str) -> str:
            return os.path.abspath(path)

        def _is_ignored(self, path: str) -> bool:
            normalized = self._normalize(path)
            try:
                rel = os.path.relpath(normalized, self.root)
            except ValueError:
                return False
            return any(part in _IGNORED_WATCH_DIRS for part in rel.split(os.sep))

        @staticmethod
        def _digest(data: bytes) -> str:
            return sha256(data).hexdigest()

        def seed(self) -> None:
            for dirpath, dirnames, filenames in os.walk(self.root):
                dirnames[:] = [name for name in dirnames if name not in _IGNORED_WATCH_DIRS]
                for filename in filenames:
                    path = os.path.join(dirpath, filename)
                    if not self._is_watched(path):
                        continue
                    try:
                        with open(path, "rb") as f:
                            self._known_hashes[self._normalize(path)] = self._digest(f.read())
                    except OSError:
                        continue

        def _enqueue_if_changed(self, path: str) -> None:
            normalized = self._normalize(path)
            try:
                with open(normalized, "rb") as f:
                    data = f.read()
            except OSError:
                return

            # Watchdog can emit duplicate modify events even when file contents
            # are unchanged; only sync when the bytes actually differ.
            digest = self._digest(data)
            if self._known_hashes.get(normalized) == digest:
                return

            self._known_hashes[normalized] = digest
            self.queue.put((normalized, data, False))

        def on_created(self, event):
            if event.is_directory or self._is_ignored(event.src_path) or not self._is_watched(event.src_path):
                return
            self._enqueue_if_changed(event.src_path)

        def on_modified(self, event):
            self.on_created(event)

        def on_deleted(self, event):
            if event.is_directory or self._is_ignored(event.src_path) or not self._is_watched(event.src_path):
                return
            normalized = self._normalize(event.src_path)
            if self._known_hashes.pop(normalized, None) is None:
                return
            self.queue.put((normalized, b"", True))

    config = resolve_entry_point(entry_point)

    image = normalize_image(config["image"])
    channels = config.get("channels", [])
    secrets = config.get("secrets", [])
    keep_warm = config.get("keep_warm_seconds", 0)
    filesystems = config.get("filesystems", {})
    integrations = config.get("integrations", [])
    schedules = config.get("schedules", [])
    cpu = config.get("cpu", 0.25)
    memory = config.get("memory", 512)
    gpu = config.get("gpu")
    spec_channel_names = tuple(
        ch["name"] for ch in channels if ch.get("type") == "_resource" and ch.get("name")
    )
    all_channel_names = tuple(dict.fromkeys(spec_channel_names + channel_names))
    serve_channels = list(channels)
    existing_channel_names = set(spec_channel_names)
    for name in channel_names:
        if name not in existing_channel_names:
            serve_channels.append({"type": "_resource", "name": name})
            existing_channel_names.add(name)

    pages = config.get("pages", [])
    data_sources = config.get("data_sources", [])

    generate_type_stubs(pages)

    terminal.header("Serving", f"[bold]{config['app_name']}[/bold]")
    entry_label = config['class_name'] or config['app_name']
    terminal.detail(f"  entry:     {config['module']}:{entry_label}")
    compute = f"{cpu} vCPU / {memory} MiB"
    if gpu:
        compute += f" / {gpu} GPU"
    terminal.detail(f"  compute:   {compute}")

    if pages:
        terminal.detail(f"  pages:     {', '.join(p['name'] for p in pages)}")
    if data_sources:
        terminal.detail(f"  data:      {', '.join(data_sources)}")
    if secrets:
        terminal.detail(f"  secrets:   {', '.join(secrets)}")
    if keep_warm > 0:
        terminal.detail(f"  keep_warm: {keep_warm}s")
    if image.get("python_packages"):
        terminal.detail(f"  pip:       {', '.join(image['python_packages'])}")
    if image.get("apt_packages"):
        terminal.detail(f"  apt:       {', '.join(image['apt_packages'])}")
    if image.get("commands"):
        terminal.detail(f"  commands:  {len(image['commands'])}")

    terminal.header("Syncing files")
    archive = collect_source_archive()

    req = StartServeRequest(
        app_name=config["app_name"],
        image=build_image_spec(image, cpu=cpu, memory=memory, gpu=gpu),
        channels=build_channel_specs(serve_channels),
        entry_point=f"{config['module']}:{config['class_name'] or entry_point.rsplit(':', 1)[1]}",
        source_archive=archive,
        keep_warm_seconds=keep_warm,
        secrets=secrets,
        filesystems=build_filesystem_mount_specs(filesystems),
        integrations=build_integration_specs(integrations),
        schedules=build_schedule_specs(schedules),
    )

    with terminal.progress("Starting machine...") as spinner:
        t0 = time.monotonic()
        list_apps = client.channel.unary_unary(
            "/capsule.CapsuleService/ListApps",
            ListAppsRequest.SerializeToString,
            ListAppsResponse.FromString,
        )
        try:
            list_apps(ListAppsRequest(), timeout=GATEWAY_READY_TIMEOUT)
        except grpc.RpcError as err:
            if err.code() in (grpc.StatusCode.DEADLINE_EXCEEDED, grpc.StatusCode.UNAVAILABLE):
                terminal.error(
                    "Gateway gRPC tunnel is not responding. "
                    "If you're using local dev, restart `make start`."
                )
                raise SystemExit(1)
            raise

        start_serve = client.channel.unary_stream(
            "/capsule.CapsuleService/StartServe",
            StartServeRequest.SerializeToString,
            StartServeResponse.FromString,
        )
        res = None
        build_logs_seen = False
        try:
            for msg in start_serve(req, timeout=START_SERVE_TIMEOUT):
                if msg.ok or msg.err_msg:
                    res = msg
                    break
                if msg.status:
                    build_logs_seen = _handle_status(spinner, msg.status, build_logs_seen)
        except grpc.RpcError as err:
            if err.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                terminal.error(
                    "Timed out waiting for StartServe. "
                    "If you're using local dev, restart `make start`."
                )
                raise SystemExit(1)
            raise

        if res is None:
            terminal.error("Serve stream ended without a result.")
            raise SystemExit(1)

        elapsed = time.monotonic() - t0

    if not res.ok:
        terminal.error(f"Serve failed: {res.err_msg}")
        raise SystemExit(1)

    app_id = res.app_id
    instance_ref = res.instance_ref

    terminal.success(f"Ready in {elapsed:.1f}s")
    terminal.header(f"Serving {config['app_name']}")

    terminal.url(res.url or f"https://{res.hostname}.capsule.new")
    if all_channel_names:
        terminal.detail("  channels: " + ", ".join(all_channel_names))

    sync_dir = os.getcwd()
    sync_queue: Queue = Queue()
    handler = _SyncHandler(sync_queue, sync_dir)
    handler.seed()
    observer = Observer()
    observer.schedule(handler, sync_dir, recursive=True)
    observer.start()

    def _stop_remote_serve():
        def _stop_generator():
            yield ServeStreamMessage(
                attach=ServeAttachRequest(app_id=app_id, instance_ref=instance_ref)
            )
            yield ServeStreamMessage(sync=ServeSyncRequest(path="", data=b"", is_delete=True))

        try:
            stream = client.capsule.serve_stream(_stop_generator())
            for _ in stream:
                break
        except grpc.RpcError:
            pass

    def _stream_generator():
        yield ServeStreamMessage(
            attach=ServeAttachRequest(app_id=app_id, instance_ref=instance_ref)
        )
        last_heartbeat = time.monotonic()
        while True:
            if shutdown.is_set():
                return
            try:
                path, data, is_delete = sync_queue.get_nowait()
                rel = os.path.relpath(path, start=sync_dir)
                terminal.header("Reloading", rel)
                yield ServeStreamMessage(
                    sync=ServeSyncRequest(
                        path=rel,
                        data=data,
                        is_delete=is_delete,
                    )
                )
                sync_queue.task_done()
                last_heartbeat = time.monotonic()
            except Empty:
                now = time.monotonic()
                if now - last_heartbeat >= HEARTBEAT_INTERVAL:
                    yield ServeStreamMessage(
                        sync=ServeSyncRequest(path="", data=b"", is_delete=False)
                    )
                    last_heartbeat = now
                else:
                    time.sleep(SYNC_INTERVAL)

    terminal.header("Watching for changes...")
    try:
        while not shutdown.is_set():
            try:
                stream = client.capsule.serve_stream(_stream_generator())
                remote_done = False
                for resp in stream:
                    if shutdown.is_set():
                        break
                    if resp.output:
                        terminal.detail(resp.output, dim=False, end="")
                    if resp.done:
                        remote_done = True
                        break
                if shutdown.is_set():
                    break
                if remote_done:
                    terminal.warn("Serve stream closed by server.")
                    break
                terminal.warn("Serve stream disconnected. Reconnecting...")
            except grpc.RpcError as err:
                if shutdown.is_set():
                    break
                code = err.code()
                if code == grpc.StatusCode.CANCELLED:
                    terminal.warn("Serve stream cancelled. Reconnecting...")
                else:
                    terminal.warn(f"Serve stream lost ({code.name.lower()}). Reconnecting...")
            time.sleep(1)
    except KeyboardInterrupt:
        shutdown.set()
    finally:
        observer.stop()
        observer.join(timeout=1)

    if shutdown.is_set():
        terminal.header("Stopping serve")
    else:
        terminal.warn("Serve stream ended; leaving remote serve running.")

    if shutdown.is_set():
        _stop_remote_serve()
    client.close()
