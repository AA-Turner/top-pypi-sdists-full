"""
Hook Management.

This module is responsible for handling the Hooks in Flowtask.
"""
import asyncio
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
        payload['definition'] = payload.copy()
        # then, remove the components
        del payload['When']
        del payload['Then']
        # and renamed "id" to "trigger_id":
        payload['trigger_id'] = payload.pop('id')
        return payload

    @ModelView.service_auth
    async def _post_response(
        self,
        response,
        fields: list = None,
        headers: dict = None,
        status: int = 200
    ):
        if status == 201:
            # Hook was correctly created.
            # TODO: remove the previous when edited.
            try:
                hookservice = self.request.app['HookService']
                hook = Hook(hook=response.definition)
                for trigger in hook.triggers:
                    tg = trigger()
                    print('TG > ', tg)
                    hookservice.add_hook(tg)
                    await tg.start()
                message = f"Hook {response.trigger_id} added successfully."
                self.logger.info(
                    message
                )
                response.status = message
            except Exception as exc:
                self.logger.error(
                    f"Error adding hook: {exc}"
                )
        return self.json_response(
            response=response,
            status=status
        )

class HookService:
    def __init__(self, event_loop: asyncio.AbstractEventLoop, app: BaseApplication, **kwargs):
        self._loop = event_loop
        self._hooks: list = []
        self._started: bool = False
        self.logger = logging.getLogger(name="Flowtask.HookService")
        self.app: WebApp = None
        # TaskStorage
        self._storage = kwargs.pop("storage", "default")
        # App
        if isinstance(app, BaseApplication):  # migrate to BaseApplication (on types)
            self.app = app.get_app()
        elif isinstance(app, WebApp):
            self.app = app  # register the app into the Extension
        else:
            raise TypeError(
                f"Invalid type for Application Setup: {app}:{type(app)}"
            )
        try:
            self.taskstore = TASK_STORAGES[self._storage]
        except KeyError as exc:
            raise RuntimeError(
                f"Invalid Task Storage > {self._storage}"
            ) from exc
        if not self.taskstore.path:
            raise ConfigError(
                f"Current Task Storage {self.taskstore!r} is not Supported for saving Triggers/Hooks."
            )

    def add_hook(self, hook: BaseTrigger):
        """
        Add the Hook, start it and calling the Setup.
        """
        self._hooks.append(hook)
        hook.setup(app=self.app)

    add_trigger = add_hook

    async def setup(self) -> None:
        """setup.

            Service Configuration.
        Args:
            app (aiohttp.web.Application): Web Application.
        """
        self.app['HookService'] = self
        # Start all hooks, and register the endpoint.
        await self.start_hooks(self.app)
        # register endpoint to add Triggers to HookService.
        HookHandler.configure(
            self.app,
            path='/api/v1/triggers/'
        )
        self.logger.notice('Hook Service Started.')

    async def start_hooks(self, app: WebApp) -> None:
        """start_hooks.

            Starts the Hook Service.
        """
        # First: loading the File-based Hooks
        await self.load_fs_hooks()
        # Second: loading the Database Hooks
        await self.load_db_hooks()
        # mark service as started.
        self._started = True

    async def load_fs_hooks(self) -> None:
        """load_fs_hooks.

        Load all Hooks from the Task Storage (Filesystem).
        """
        self.logger.notice(":: Loading Hooks from Filesystem.")
        for program_dir in self.taskstore.path.iterdir():
            if program_dir.is_dir():
                hooks_dir = program_dir.joinpath("hooks.d")
                for file_path in hooks_dir.rglob("*.*"):
                    # only work with supported extensions:
                    if file_path.suffix in ('.json', '.yaml', '.yml'):
                        try:
                            store = await self.taskstore.open_hook(file_path)
                        except Exception as exc:
                            self.logger.warning(
                                f"Unable to load Hook {file_path!r}: Invalid Hook File, {exc}"
                            )
                            continue
                        try:
                            hook = Hook(hook=store)
                            if hook:
                                for trigger in hook.triggers:
                                    self.add_hook(trigger)
                        except FlowTaskError:
                            pass

    async def load_db_hooks(self) -> None:
        """load_db_hooks.

        Load all Hooks saved into the Database.
        """
        db = AsyncDB('pg', dsn=default_dsn)
        async with await db.connection() as conn:
            HookObject.Meta.connection = conn
            hooks = await HookObject.all()
            for hook in hooks:
                definition = hook.definition
                try:
                    hook = Hook(hook=definition)
                    for trigger in hook.triggers:
                        self.add_hook(trigger)
                except FlowTaskError:
                    pass
                except Exception as exc:
                    self.logger.error(
                        f"Error Loading Database Hooks: {exc}"
                    )
