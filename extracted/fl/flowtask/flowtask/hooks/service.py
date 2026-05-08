"""
Hook Management.

This module is responsible for handling the Hooks in Flowtask.
"""
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Union
from navconfig.logging import logging
from asyncdb import AsyncDB
from navigator.types import WebApp
from navigator.applications.base import BaseApplication
from navigator.views import ModelView
from ..exceptions import ConfigError, FlowTaskError
from ..conf import TASK_STORAGES, default_dsn
from .types.base import BaseTrigger
from .hook import Hook
from .models import HookObject


class HookHandler(ModelView):
    model = HookObject
    name = "Navigator Triggers"
    pk: str = "trigger_id"

    async def _set_created_by(self, value, column, data):
        return await self.get_userid(session=self._session)

    @ModelView.service_auth
    async def _post_data(self, *args, **kwargs):
        payload = await super()._post_data(*args, **kwargs)
        if not payload:
            raise ConfigError("Trigger: No payload provided.")
        payload["definition"] = payload.copy()
        # then, remove the components
        del payload["When"]
        del payload["Then"]
        # and renamed "id" to "trigger_id":
        payload["trigger_id"] = payload.pop("id")
        return payload

    @ModelView.service_auth
    async def _post_response(
        self, response, fields: list = None, headers: dict = None, status: int = 200
    ):
        if status == 201:
            # Hook was correctly created.
            # TODO: remove the previous when edited.
            try:
                hookservice = self.request.app["HookService"]
                hook = Hook(hook=response.definition)
                for trigger in hook.triggers:
                    hookservice.add_hook(trigger)
                message = "Hook %s added successfully."
                self.logger.info(message, response.trigger_id)
                response.status = message % response.trigger_id
            except Exception as exc:
                self.logger.error("Error adding hook: %s", exc)
        return self.json_response(response=response, status=status)


class HookService:
    def __init__(
        self,
        app: Union[BaseApplication, WebApp],
        *,
        storage: str = "default",
    ):
        """Construct the service and register HookHandler.

        Does NOT install any aiohttp lifecycle callbacks. The application
        MUST call `setup()` before `app.freeze()` for hooks to be active.

        Args:
            app: aiohttp Application or BaseApplication wrapper.
            storage: key into TASK_STORAGES for the filesystem hook store.

        Raises:
            TypeError: If app is not a recognised application type.
            RuntimeError: If the storage key is invalid.
            ConfigError: If the storage has no path configured.
        """
        self._hooks: list[BaseTrigger] = []
        self._runtime_hooks: list[BaseTrigger] = []
        self._started: bool = False
        self._teardown_registered: bool = False
        self.logger = logging.getLogger(name="Flowtask.HookService")

        if isinstance(app, BaseApplication):
            self.app: WebApp = app.get_app()
        elif isinstance(app, WebApp):
            self.app = app
        else:
            raise TypeError(f"Invalid type for Application Setup: {app}:{type(app)}")

        try:
            self.taskstore = TASK_STORAGES[storage]
        except KeyError as exc:
            raise RuntimeError(f"Invalid Task Storage > {storage}") from exc
        if not self.taskstore.path:
            raise ConfigError(
                f"Current Task Storage {self.taskstore!r} is not Supported "
                "for saving Triggers/Hooks."
            )

        self.app["HookService"] = self
        HookHandler.configure(self.app, path="/api/v1/triggers/")
        # NOTE: lifecycle is no longer registered here. The application MUST
        # call `setup(app, loop=...)` from configure() before app.freeze().

    def setup(
        self,
        app: WebApp | None = None,
        *,
        loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        """Synchronous entrypoint — load hooks and wire signals before app.freeze().

        Drives the async loaders to completion before returning. If the
        supplied loop is not running, it uses `loop.run_until_complete`. If
        Navigator is already running that loop while calling configure(), the
        loaders are executed on a temporary setup loop in a worker thread while
        this method blocks. After this returns, every trigger's
        on_startup/on_shutdown is registered on `app.on_startup`/
        `app.on_shutdown` (via BaseTrigger.setup), and aiohttp will invoke
        them through its normal signal lifecycle.

        Must be called from `configure()` (pre-freeze). Raises RuntimeError
        if called after app.freeze() (signals are frozen).

        Args:
            app: aiohttp Application to wire. Falls back to self.app.
            loop: Event loop to drive async loaders. Prefers the running loop;
                  falls back to a new event loop. Pass loop=self.event_loop()
                  from the caller for the most reliable behaviour.

        Raises:
            RuntimeError: If no app is available.
        """
        target = app or self.app
        if target is None:
            raise RuntimeError("HookService.setup requires an aiohttp Application")
        if loop is None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
        self.logger.notice(":: Starting Hook Service ::")
        self._run_setup_loader(app=target, loop=loop)
        if not self._teardown_registered:
            target.on_shutdown.append(self._stop_hooks)
            self._teardown_registered = True
        self.logger.notice(
            "Hook Service Started (%d triggers wired).", len(self._hooks)
        )

    def _run_setup_loader(
        self,
        *,
        app: WebApp,
        loop: asyncio.AbstractEventLoop,
    ) -> None:
        """Run async hook loading from sync configure() code.

        Navigator calls handler.configure() from inside its async
        start_server() coroutine, so the application loop can already be
        running here. Calling run_until_complete on that loop raises
        RuntimeError; deferring hook loading to app.on_startup is too late
        because aiohttp freezes signal lists before startup callbacks run.
        """
        if loop.is_running():
            self.logger.debug(
                "HookService.setup received a running loop; using temporary "
                "setup loop to load hooks before app.freeze()."
            )
            self._run_setup_loader_in_thread(app)
            return
        loop.run_until_complete(self.start_hooks(app))

    def _run_setup_loader_in_thread(self, app: WebApp) -> None:
        """Run start_hooks on a temporary event loop and propagate failures."""
        with ThreadPoolExecutor(
            max_workers=1,
            thread_name_prefix="HookServiceSetup",
        ) as executor:
            future = executor.submit(self._run_setup_loader_on_new_loop, app)
            future.result()

    def _run_setup_loader_on_new_loop(self, app: WebApp) -> None:
        """Thread target for the running-loop setup fallback."""
        setup_loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(setup_loop)
            setup_loop.run_until_complete(self.start_hooks(app))
        finally:
            asyncio.set_event_loop(None)
            setup_loop.close()

    def add_hook(self, hook: BaseTrigger) -> None:
        """Register a trigger either pre-freeze (via setup) or post-freeze (at runtime).

        Called from two paths:
        - Pre-freeze from configure() / app.py: signals are still mutable, so
          ``hook.setup(app)`` is invoked to register the trigger's on_startup and
          on_shutdown callbacks on the aiohttp signal lists.
        - Post-freeze from the HTTP API (HookHandler._post_response): signals are
          frozen, so ``hook.start_runtime(app)`` is scheduled with
          ``asyncio.ensure_future`` instead.

        Args:
            hook: Already-instantiated trigger to register.
        """
        self._hooks.append(hook)
        try:
            hook.setup(self.app)
            self.logger.info("Trigger %s registered pre-freeze (signals wired).", hook)
        except RuntimeError:
            # Signals are frozen — use the runtime path.
            self._runtime_hooks.append(hook)
            self.logger.info(
                "Trigger %s registered post-freeze (start_runtime scheduled).", hook
            )
            asyncio.ensure_future(hook.start_runtime(self.app))

    add_trigger = add_hook

    async def _stop_hooks(self, app: WebApp) -> None:
        """Housekeeping-only teardown callback registered on app.on_shutdown.

        Boot-time triggers have their on_shutdown invoked by aiohttp through
        the signals registered in BaseTrigger.setup — do NOT re-invoke them
        here (double-fire would break e.g. PostgresTrigger which cancels an
        already-cancelled task).

        Runtime-added triggers (added via add_hook post-freeze) were never
        wired into the signal list, so invoke their on_shutdown directly.
        """
        for hook in self._runtime_hooks:
            on_shutdown = getattr(hook, "on_shutdown", None)
            if callable(on_shutdown):
                try:
                    await on_shutdown(app)
                except Exception:
                    self.logger.exception("Trigger %s on_shutdown failed", hook)
        self._runtime_hooks.clear()
        self._hooks.clear()
        self._started = False

    async def start_hooks(self, app: WebApp) -> None:
        """Load file-based and database-backed hooks."""
        await self.load_fs_hooks(app)
        await self.load_db_hooks(app)
        self._started = True

    async def load_fs_hooks(self, app: WebApp) -> None:
        """Load all Hooks from the Task Storage (Filesystem)."""
        self.logger.notice(":: Loading Hooks from Filesystem.")
        for program_dir in self.taskstore.path.iterdir():
            if not program_dir.is_dir():
                continue
            hooks_dir = program_dir.joinpath("hooks.d")
            if not hooks_dir.exists():
                continue
            for file_path in hooks_dir.rglob("*.*"):
                if file_path.suffix not in (".json", ".yaml", ".yml"):
                    continue
                try:
                    store = await self.taskstore.open_hook(file_path)
                except Exception as exc:
                    self.logger.warning(
                        "Unable to load Hook %r: Invalid Hook File, %s",
                        file_path,
                        exc,
                    )
                    continue
                try:
                    hook = Hook(hook=store)
                    if hook:
                        for trigger in hook.triggers:
                            trigger.setup(app)
                            self._hooks.append(trigger)
                except FlowTaskError:
                    pass

    async def load_db_hooks(self, app: WebApp) -> None:
        """Load all Hooks saved into the Database."""
        try:
            db = AsyncDB("pg", dsn=default_dsn)
            async with await db.connection() as conn:
                HookObject.Meta.connection = conn
                hooks = await HookObject.all()
                for hook in hooks:
                    definition = hook.definition
                    try:
                        hook_instance = Hook(hook=definition)
                        for trigger in hook_instance.triggers:
                            trigger.setup(app)
                            self._hooks.append(trigger)
                    except FlowTaskError:
                        pass
                    except Exception as exc:
                        self.logger.error("Error Loading Database Hooks: %s", exc)
        except Exception as exc:
            self.logger.error(
                "Error connecting to Database for Hook loading: %s. "
                "Continuing with filesystem hooks only.",
                exc,
            )
