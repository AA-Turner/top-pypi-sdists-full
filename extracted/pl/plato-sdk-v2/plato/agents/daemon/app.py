"""Compose the daemon aiohttp application from its services."""

from __future__ import annotations

from pathlib import Path

from aiohttp import web

from plato.agents.daemon.auth import build_auth_middleware
from plato.agents.daemon.http_util import error_middleware
from plato.agents.daemon.jobs.manager import AgentJobManager
from plato.agents.daemon.services import env as env_service
from plato.agents.daemon.services import exec_ as exec_service
from plato.agents.daemon.services import files as files_service
from plato.agents.daemon.services import git as git_service
from plato.agents.daemon.services import health
from plato.agents.daemon.services import job as job_service
from plato.agents.daemon.services import pool as pool_service
from plato.agents.daemon.state import DaemonContext
from plato.rpc.protocol import MAX_BODY_BYTES

CTX_KEY: web.AppKey[DaemonContext] = web.AppKey("ctx", DaemonContext)


def build_app(
    *,
    state_dir: str | Path,
    token: str,
    env_file: str | Path | None = None,
    hosts_file: str | Path | None = None,
    tmp_globs: tuple[str, ...] | None = None,
    cgroup_setup_glob: str | None = None,
) -> web.Application:
    """Build the daemon app. Services self-register their routes and
    capabilities onto the shared ``DaemonContext``. Each later build step adds
    one ``mod.register(app, ctx)`` line.

    ``env_file``/``hosts_file`` override the env service's target paths (tests
    point these at a tmp dir; production uses /etc/environment and /etc/hosts).
    """
    ctx = DaemonContext(state_dir=Path(state_dir), token=token)
    ctx.ensure_dirs()

    app = web.Application(
        client_max_size=MAX_BODY_BYTES,
        middlewares=[error_middleware, build_auth_middleware(ctx)],
    )
    app[CTX_KEY] = ctx

    health.register(app, ctx)
    exec_service.register(app, ctx)
    files_service.register(app, ctx)
    env_kwargs = {}
    if env_file is not None:
        env_kwargs["env_path"] = Path(env_file)
    if hosts_file is not None:
        env_kwargs["hosts_path"] = Path(hosts_file)
    env_service.register(app, ctx, **env_kwargs)

    # One AgentJobManager shared by the job service (start/status/wait/signal) and
    # the pool service (reset prunes finished-job state between tenants).
    job_manager = AgentJobManager(ctx.jobs_dir)

    pool_kwargs = dict(env_kwargs)
    if tmp_globs is not None:
        pool_kwargs["tmp_globs"] = tmp_globs
    if cgroup_setup_glob is not None:
        pool_kwargs["cgroup_setup_glob"] = cgroup_setup_glob
    pool_service.register(app, ctx, job_manager=job_manager, **pool_kwargs)

    job_service.register(app, ctx, manager=job_manager)
    git_service.register(app, ctx)

    # Re-adopt jobs left running by a previous daemon on startup. This MUST run
    # under the event loop, not in build_app: recover() spawns poll tasks via
    # asyncio.create_task, which raises "no running event loop" if called
    # before web.run_app starts the loop. on_startup runs with the loop live
    # and before the server accepts requests, so a reconnecting world sees the
    # re-adopted job state.
    async def _recover_jobs(_app: web.Application) -> None:
        job_manager.recover()

    app.on_startup.append(_recover_jobs)

    return app
