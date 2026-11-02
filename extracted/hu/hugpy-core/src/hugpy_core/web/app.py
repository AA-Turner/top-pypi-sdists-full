"""hugpy_core router app: abstract_flask app over the routes module."""
from __future__ import annotations

import argparse
import logging
import os
from contextlib import contextmanager
from pathlib import Path

from abstract_flask import get_Flask_app

from hugpy_core import routes

logger = logging.getLogger("hugpy_core")


@contextmanager
def _audit_log_directory():
    """Place abstract_flask's relative audit file in the staged logs directory."""
    requested = os.environ.get("HUGPY_LOG_DIR")
    if not requested:
        source_package = Path(__file__).resolve().parents[3]
        if (source_package / "pyproject.toml").is_file():
            requested = str(source_package / "logs")
    if not requested:
        yield
        return
    directory = Path(requested).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    previous = Path.cwd()
    try:
        os.chdir(directory)
        yield
    finally:
        os.chdir(previous)


def build_app(*, start_runtime=True):
    # The Settings page can select a declared central drive. Restore that
    # choice before routes and the transfer catalog read the model root.
    from pathlib import Path
    saved_root = Path("/var/lib/hugpy-core/central-models-home")
    try:
        path = saved_root.read_text(encoding="utf-8").strip()
        if path and Path(path).is_dir():
            import os
            os.environ["HUGPY_CENTRAL_MODELS_HOME"] = path
    except OSError:
        pass
    with _audit_log_directory():
        # Optional Media/Video blueprints are mounted explicitly by routes.
        # Keep automatic arm discovery off to avoid duplicate registrations.
        app = get_Flask_app(name="hugpy_core", routes=routes,
                            dual_prefix="/api", arms_group=None)
    from hugpy_core.web.api_access import initialize_api_access
    if start_runtime:
        initialize_api_access()
    if start_runtime:
        from hugpy_core.testfire.storage_cycle import recover_allocations
        recover_allocations()
        from hugpy_core.grading.lifecycle import recover
        recover()
    from hugpy_core.models.modeldb import forget_unpinned_assignments
    # Do not begin serving with stale transient allocations if the reset fails.
    forgotten = forget_unpinned_assignments() if start_runtime else 0
    if forgotten:
        logger.info("forgot %d unpinned worker allocations on API reload", forgotten)
    from hugpy_core.calllog.call_record import attach
    attach(app)
    # The console's Station tab: the real `hugpy-harness tui` over a websocket PTY.
    from hugpy_core.web import station_term
    station_term.attach(app)
    from hugpy_core.relay.internal import configure
    configure(app)
    from hugpy_engine.config.models.models_config import set_core_sources
    from hugpy_core.web.routes import catalog_rows as core_catalog_rows
    from hugpy_core.config.settings import task_bindings as core_task_bindings
    set_core_sources(catalog=core_catalog_rows, bindings=core_task_bindings)
    # The deployed Flask entry point calls build_app() directly, so the brain
    # listener must start here as well as in the CLI entry point.
    from hugpy_core.brain import brain
    if start_runtime:
        brain.ensure()
    # Resource events must refresh pair_live even when no browser is open.
    from hugpy_core.registry import live
    if start_runtime:
        live._ensure()
    # Run every hugpy.arm_prepare entry point: a merged arm's in-process startup
    # (state dirs, sqlite job bus, runner pools, planner hooks). Guarded and
    # logged — a missing or failing arm never stops core. See CORE-MERGE-PLAN §7B.
    from importlib.metadata import entry_points as _entry_points
    from hugpy_core.relay.hosted import configure_arms
    configure_arms(app)
    for _ep in _entry_points(group="hugpy.arm_prepare") if start_runtime else ():
        try:
            _facts = _ep.load()()
            logger.info("arm_prepare %s: %s", _ep.name, _facts)
        except Exception:  # noqa: BLE001 — a failing arm is a fact, not a crash
            logger.exception("arm_prepare %s failed", _ep.name)
    from hugpy_core.web import ui
    from hugpy_core.web import arm_proxy
    from hugpy_core.web import guest_access
    from hugpy_core.web.worker_aliases import WorkerAliases
    # WSGI chain: the console static app (ui.wrap) first, then each hugpy.arm_ui
    # wrapper (so an arm's SPA is served before ConsoleApp sees its path),
    # inside arm_proxy for external addons and under the guest-access gate.
    # Successfully mounted addon UIs override their obsolete service descriptors.
    # Preserve Flask's public application interface while applying middleware
    # to its original dispatcher. Capturing this bound method first prevents
    # the middleware chain from recursively calling itself through app().
    wsgi = ui.wrap(app.wsgi_app)
    embedded_arms = set()
    for _ep in _entry_points(group="hugpy.arm_ui"):
        try:
            wrapped = _ep.load()(wsgi)
            if not callable(wrapped):
                raise TypeError("arm UI hook must return a WSGI application")
            if wrapped is not wsgi:
                embedded_arms.add(_ep.name)
            wsgi = wrapped
            logger.info("arm_ui %s: wrapped the WSGI chain", _ep.name)
        except Exception:  # noqa: BLE001 — a failing arm UI never stops core
            logger.exception("arm_ui %s failed", _ep.name)
    app.wsgi_app = WorkerAliases(guest_access.wrap(
        arm_proxy.wrap(wsgi, app, embedded_arms=embedded_arms), app))
    if start_runtime:
        from hugpy_core.relay import inference_requests
        inference_requests.start(app)
    return app


def main(argv=None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    ap = argparse.ArgumentParser(prog="hugpy_core")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=7020)
    a = ap.parse_args(argv)
    logger.info("hugpy_core router on %s:%s", a.host, a.port)
    from werkzeug.serving import make_server

    from hugpy_core.registry import registry
    # bind (listening) BEFORE telling the workers core is back: a worker that
    # re-registers the instant it hears the notify must find the socket open
    server = make_server(a.host, a.port, build_app(), threaded=True)
    from hugpy_core import schema
    try:
        schema.ensure()                           # core creates its own tables
        from hugpy_core.models.identity import reconcile
        import psycopg
        from hugpy_core.imports.functions import core_dsn
        with psycopg.connect(core_dsn()) as identity_conn:
            result = reconcile(identity_conn)
        logger.info("model identity reconciliation: %s", result)
    except Exception:  # noqa: BLE001 — a DB away never stops core starting
        logger.exception("schema ensure failed")
    from hugpy_core import intake
    intake.start()                                # every box's telemetry, via the router, into the DB
    from hugpy_core.registry import central_store
    from hugpy_storage.catalog_source import set_catalog_source
    central_store.seed_if_empty()                 # the one seed walk of the central drive
    set_catalog_source(central_store.CentralCatalog())   # transfers resolve from the DB
    from hugpy_core.models import modelrows
    modelrows._ensure()     # drive changes resync the box's catalog even with no console open
    from hugpy_core.calllog import call_record
    from hugpy_core.grading import review
    try:
        orphans = call_record.close_orphans(review._PROCESS_STARTED)
        if orphans:
            logger.info("closed %d call row(s) left pending by an earlier core process", orphans)
    except Exception:  # noqa: BLE001 — the call log being away never stops core starting
        logger.exception("closing orphaned call rows failed")
    from hugpy_core.registry import facts_listener
    facts_listener.ensure()  # a measurement row in hugpy_wrapper re-plans its worker (event, not heartbeat)
    from hugpy_core.brain import brain
    brain.ensure()           # a residents.load_error change is evaluated by the brain (event)
    registry.announce_started()
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
