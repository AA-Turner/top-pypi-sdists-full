"""Machinery behind `@ray_ui`: resolving what to proxy, and tearing it down.

The decorator itself lives in `__init__.py`. Nothing here imports metaflow-ray:
that extension ships separately, so `@ray_ui` finds it by decorator name and
duplicates the handful of constants it needs.
"""

import atexit
import os
import re
import signal
import sys

from metaflow.exception import MetaflowException

# The name `metaflow_ray`'s RayDecorator registers itself under.
RAY_DECORATOR_NAME = "metaflow_ray"

# Mirrors `metaflow_extensions.ray.plugins.constants.DEFAULT_DASHBOARD_PORT`.
# Duplicated so importing this module does not require metaflow-ray to be
# importable on the client side.
DEFAULT_DASHBOARD_PORT = 8265

# Set on every task of a jobset-backed parallel step to the in-cluster FQDN of
# the control pod, i.e. `<jobset>-c-0-0.<jobset>.<namespace>.svc.cluster.local`.
CONTROL_ADDR_ENV_VAR = "MF_MASTER_ADDR"

# Metaflow gives the control task of a parallel step node index 0.
CONTROL_NODE_INDEX = 0

# `BasicAppValidations.name` in the apps config: lowercase alphanumerics and
# hyphens only, at most 150 characters.
APP_NAME_MAX_LENGTH = 150

# The range `BasicAppValidations.port` accepts. Checked here too so that a bad
# `@ray_ui(port=...)` fails when the flow is loaded rather than at deploy time.
MIN_PORT = 1
MAX_PORT = 65535


class RayUIException(MetaflowException):
    headline = "@ray_ui error"


def _log(message):
    print("[@ray_ui] %s" % message, file=sys.stderr)


def _as_bool(value):
    # Decorator attributes reach the task as strings when the step is scheduled
    # remotely, so `bool("False")` is a real hazard here.
    if isinstance(value, str):
        return value.strip().lower() in ("true", "1", "yes", "y")
    return bool(value)


def _sanitize_app_name(raw):
    name = re.sub(r"[^a-z0-9]+", "-", raw.lower())
    name = re.sub(r"-{2,}", "-", name).strip("-")
    return name[:APP_NAME_MAX_LENGTH].strip("-")


def _ray_decorator(decorators):
    """Return the `@metaflow_ray` decorator among `decorators`, or None.

    Metaflow hands every step decorator the full list of decorators on its step
    in `step_init`, so this is a lookup by name rather than an import of an
    extension that may not be installed.
    """
    for deco in decorators or []:
        if getattr(deco, "name", None) == RAY_DECORATOR_NAME:
            return deco
    return None


def _node_index(current):
    parallel = current.get("parallel")
    return getattr(parallel, "node_index", None) if parallel else None


def _requested_port(step_name, requested_port):
    """`@ray_ui(port=...)` as an int, or None if it was not set."""
    if requested_port is None:
        return None
    try:
        port = int(requested_port)
    except (TypeError, ValueError):
        port = None
    if port is None or not (MIN_PORT <= port <= MAX_PORT):
        raise RayUIException(
            "@ray_ui(port=%r) on step `%s` is not a valid port. It must be a "
            "whole number between %d and %d."
            % (requested_port, step_name, MIN_PORT, MAX_PORT)
        )
    return port


def _resolve_port(step_name, ray_deco, requested_port):
    attributes = getattr(ray_deco, "attributes", None) or {}
    dashboard_enabled = _as_bool(attributes.get("enable_dashboard"))
    try:
        dashboard_port = int(attributes.get("dashboard_port") or DEFAULT_DASHBOARD_PORT)
    except (TypeError, ValueError):
        dashboard_port = DEFAULT_DASHBOARD_PORT

    requested_port = _requested_port(step_name, requested_port)
    port = dashboard_port if requested_port is None else requested_port

    if port == dashboard_port and not dashboard_enabled:
        raise RayUIException(
            "There is no Ray dashboard to serve on step `%s`: @metaflow_ray was "
            "given enable_dashboard=False (the default). Use "
            "@metaflow_ray(enable_dashboard=True), or point @ray_ui at a "
            "different port with @ray_ui(port=...)." % step_name
        )
    if port != dashboard_port:
        _log(
            "proxying port %d, which is not the Ray dashboard port (%d) of this "
            "step -- nothing will answer there unless you are serving something "
            "else on it." % (port, dashboard_port)
        )
    return port


def _service_url(port):
    control_addr = os.environ.get(CONTROL_ADDR_ENV_VAR)
    if not control_addr:
        raise RayUIException(
            "$%s is not set, so the Ray control node has no in-cluster address "
            "to proxy to. @ray_ui needs the step to run on Kubernetes -- add "
            "@kubernetes to the step (or run with --with kubernetes)."
            % CONTROL_ADDR_ENV_VAR
        )
    return "%s:%d" % (control_addr, port)


def _deploy(app_name, service_url, auth, description, app_kwargs, deploy_kwargs):
    from metaflow.apps import AppDeployer

    kwargs = {
        "name": app_name,
        "capsule_type": "Proxy",
        "proxy": {"service_url": service_url},
        "auth": auth,
        "description": description,
        # A retried control task redeploys under the same app name; without this
        # the second attempt fails with AppUpgradeInProgressException.
        "force_upgrade": True,
    }
    kwargs.update(app_kwargs)
    return AppDeployer(**kwargs).deploy(**deploy_kwargs)


class _AppTeardown:
    """Deletes a deployed app once, on whichever exit path fires first.

    A bare `finally` only covers the step function returning or raising. A
    control task holding a Ray cluster open is at least as likely to be torn
    down from the outside -- a cancelled run, a Ctrl-C, a `@timeout` -- and
    Metaflow installs no SIGTERM/SIGINT handler of its own in the task process,
    so Python's default handling would kill the interpreter without unwinding
    `finally` at all. Signals and interpreter exit therefore get wired up too,
    and every path funnels through `run()`, which is idempotent.

    A SIGKILL still cannot be caught: `@kubernetes` parallel steps run in a
    jobset whose pods set `termination_grace_period_seconds=0`, so a deleted pod
    is SIGKILLed with no window to delete anything. Pair the step with
    `@app_deploy(cleanup_policy="delete")` on the flow to cover that case from
    the client side.
    """

    def __init__(self, app, app_name):
        self._app = app
        self._app_name = app_name
        self._done = False
        self._previous_handlers = {}

    def run(self, reason="step exit"):
        if self._done:
            return
        self._done = True
        try:
            self._app.delete()
            _log("deleted app `%s` (%s)." % (self._app_name, reason))
        except Exception as e:
            # The step's own outcome matters more than the teardown.
            _log("failed to delete app `%s` (%s): %s" % (self._app_name, reason, e))

    def install(self):
        atexit.register(self.run, "interpreter exit")
        for signum in (signal.SIGTERM, signal.SIGINT):
            try:
                self._previous_handlers[signum] = signal.getsignal(signum)
                signal.signal(signum, self._on_signal)
            except (ValueError, OSError, RuntimeError):
                # Handlers can only be installed from the main thread of the
                # main interpreter; fall back to atexit alone.
                self._previous_handlers.pop(signum, None)

    def uninstall(self):
        atexit.unregister(self.run)
        for signum, previous in self._previous_handlers.items():
            try:
                signal.signal(signum, previous)
            except (ValueError, OSError, RuntimeError):
                pass
        self._previous_handlers.clear()

    def _on_signal(self, signum, frame):
        try:
            name = signal.Signals(signum).name
        except ValueError:
            name = str(signum)
        self.run("received %s" % name)

        # Leave the task dying exactly as it would have without us: hand the
        # signal back to whatever was installed before.
        previous = self._previous_handlers.get(signum, signal.SIG_DFL)
        if callable(previous):
            return previous(signum, frame)
        if previous == signal.SIG_IGN:
            return
        signal.signal(signum, signal.SIG_DFL)
        os.kill(os.getpid(), signum)
