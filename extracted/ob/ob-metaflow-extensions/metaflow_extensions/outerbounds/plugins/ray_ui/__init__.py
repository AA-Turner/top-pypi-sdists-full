import functools

from metaflow.decorators import StepDecorator

from .ray_ui import (
    CONTROL_NODE_INDEX,
    RayUIException,
    _AppTeardown,
    _deploy,
    _log,
    _node_index,
    _ray_decorator,
    _resolve_port,
    _sanitize_app_name,
    _service_url,
)

__all__ = ["RayUIDecorator", "RayUIException"]


class RayUIDecorator(StepDecorator):
    """
    Serve a `@metaflow_ray` step's Ray dashboard through an Outerbounds Proxy app.

    The app is deployed on the control task just before the step body runs -- by
    which point `@metaflow_ray` has already started the Ray processes -- and torn
    down when the task finishes, since the pod it proxies dies with the step.
    Worker tasks are left untouched.

    The step must also carry `@metaflow_ray`; `@ray_ui` raises otherwise.

    User code call
    --------------
    @ray_ui(
        port=8265,
        ...
    )

    Parameters
    ----------
    name : str, optional
        App name. Defaults to `ray-ui-<flow>-<step>-<run id>`, which keeps
        concurrent runs from redeploying over each other.
    port : int, optional
        Port on the control node to proxy. Defaults to the step's
        `@metaflow_ray(dashboard_port=...)`, i.e. 8265.
    public : bool, default False
        Whether the app is reachable without authentication.
    cleanup : bool, default True
        Delete the app when the task finishes -- on a normal return, on an
        exception, on SIGTERM/SIGINT, or at interpreter exit. Set to False to
        leave it behind (it will point at a dead pod). A SIGKILLed task cannot
        clean up after itself, so pair the step with
        `@app_deploy(cleanup_policy="delete")` on the flow to cover that case.
    description : str, optional
        App description. Defaults to naming the task pathspec.
    readiness_condition : str, optional
        Forwarded to `AppDeployer.deploy()` when set.
    max_wait_time : int, optional
        Forwarded to `AppDeployer.deploy()` when set.
    app_kwargs : dict, optional
        Forwarded to `AppDeployer()`, and overrides anything set above.
    """

    name = "ray_ui"
    defaults = {
        "name": None,
        "port": None,
        "public": False,
        "cleanup": True,
        "description": None,
        "readiness_condition": None,
        "max_wait_time": None,
        "app_kwargs": {},
    }

    def step_init(
        self, flow, graph, step_name, decorators, environment, flow_datastore, logger
    ):
        # Whether there is a dashboard to serve, and on which port, follows from
        # the two decorators alone. Settling it here fails a misconfigured step
        # when the flow is loaded rather than once the task is already running.
        ray_deco = _ray_decorator(decorators)
        if ray_deco is None:
            raise RayUIException(
                "@ray_ui only works on a step that also has @metaflow_ray, and "
                "step `%s` does not have it. @ray_ui exposes the Ray dashboard "
                "of a Ray cluster that @metaflow_ray starts." % step_name
            )
        self._port = _resolve_port(step_name, ray_deco, self.attributes["port"])

    def task_decorate(
        self, step_func, flow, graph, retry_count, max_user_code_retries, ubf_context
    ):
        @functools.wraps(step_func)
        def ray_ui_wrapper():
            from metaflow import current

            node_index = _node_index(current)
            if node_index != CONTROL_NODE_INDEX:
                # Under @metaflow_ray only the control task runs the step body
                # at all, so this is belt-and-braces: never deploy from a worker.
                _log(
                    "skipping deployment on node %s -- the Ray dashboard only "
                    "runs on the control node." % node_index
                )
                return step_func()

            service_url = _service_url(self._port)
            app_name = self.attributes["name"] or _sanitize_app_name(
                "ray-ui-%s-%s-%s"
                % (current.flow_name, current.step_name, current.run_id)
            )

            _log("deploying app `%s` ..." % (app_name))
            app = _deploy(
                app_name,
                service_url,
                {"type": "Browser", "public": self.attributes["public"]},
                self.attributes["description"]
                or "Ray dashboard for %s" % current.pathspec,
                self.attributes["app_kwargs"] or {},
                {
                    k: v
                    for k, v in (
                        ("readiness_condition", self.attributes["readiness_condition"]),
                        ("max_wait_time", self.attributes["max_wait_time"]),
                    )
                    if v is not None
                },
            )
            _log("Ray dashboard is available at %s" % app.public_url)

            # Lets the step body reach the deployment, e.g. current.ray_ui.public_url.
            try:
                current._update_env({"ray_ui": app})
            except Exception as e:
                _log("could not expose the app on `current`: %s" % e)

            teardown = (
                _AppTeardown(app, app_name) if self.attributes["cleanup"] else None
            )
            if teardown is not None:
                teardown.install()
            try:
                return step_func()
            finally:
                if teardown is not None:
                    teardown.run()
                    teardown.uninstall()

        return ray_ui_wrapper
