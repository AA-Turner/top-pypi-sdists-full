import contextlib
import dataclasses
import logging
import os
import shutil
import subprocess
import threading
import time
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Callable, Iterator, List, Optional, Tuple, cast

import humanize
import reacton.core
import solara
import solara.lab
import solara.util
from dateutil import parser  # type: ignore
from solara import Result
from solara.alias import reacton
from solara.alias import rv as v
from solara.alias import sol
from solara.components.applayout import should_use_embed

import domino_code_assist.assistant.notebook
from domino_code_assist.settings import settings

from ..assistant import mixpanel
from ..domino_api import AppInfo, get_domino_api
from .app_checker import AppChecker
from .button_clipboard import ButtonClipboard
from .filesystem_watcher import FileSystemWatcher

run_sh_content_template = """#!/usr/bin/env bash
SOLARA_APP=domino_code_assist.app_entrypoint SOLARA_TELEMETRY_MIXPANEL_ENABLE=False SOLARA_THEME_VARIANT={theme_variant}\\
    SOLARA_THEME_LOADER={theme_loader} uvicorn solara.server.starlette:app\\
    --loop asyncio\\
    --host=0.0.0.0 --port=8888"""


logger = logging.getLogger("dca.deploy")

deploy_sync = solara.util.load_file_as_data_url(Path(__file__).parent / "deploy-sync.png", "image/png")

# these are changed from test tests
timeout_notebook_save: float = 60 * 3
timeout_filesystem_sync: float = 60 * 1
timeout_app_stop: int = 60
timeout_app_start: int = 60 * 5
delay_app_state: float = 10.0
delay_app_publish: float = 3.0
app_poll_delay: float = 1
server_log_update_deplay: float = 10.0
fresh_deploy_delta = timedelta(minutes=1)


class AppStatus(str, Enum):
    NON_EXISTENT = "Non existent"  # not a return value by the domino api, but used interally
    PENDING = "Pending"
    PREPARING = "Preparing"
    RUNNING = "Running"
    STOPPED = "Stopped"
    QUEUED = "Queued"
    FAILED = "Failed"
    SUCCEEDED = "Succeeded"
    ERROR = "Error"


APP_END_STATES = (AppStatus.NON_EXISTENT, AppStatus.STOPPED, AppStatus.FAILED, AppStatus.RUNNING, AppStatus.SUCCEEDED, AppStatus.ERROR)


class AppOperation(str, Enum):
    START = "Start"
    STOP = "Stop"


notebook_saved_error = solara.lab.Reactive(False)
notebook_save_request = solara.lab.Reactive(0)
deploy_step = solara.lab.Reactive("")


@dataclasses.dataclass
class LogMessage:
    message: str
    timestamp: datetime = dataclasses.field(default_factory=lambda: datetime.now())


deploy_log = solara.lab.Reactive(cast(Tuple[LogMessage, ...], ()))


@contextlib.contextmanager
def step(info: str):
    deploy_step.value = info
    try:
        log("## " + info)
        yield
    except Exception as e:
        # deploy_error.value = e
        log("faild step: " + info + " with error: " + str(e))
        raise


def log(message: str):
    msg = LogMessage(message)
    # useful when debugging with the tests to see this in stdout
    # print(msg.timestamp, msg.message, flush=True)
    deploy_log.value += (msg,)


def validate_app():
    proc = subprocess.run(
        ["python", "-m", "domino_code_assist.app_entrypoint"], cwd=settings.domino_working_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return proc


def track_view_app():
    mixpanel.api.track_with_defaults(
        "interaction",
        {
            "section": "deploy",
            "type": "view app",
        },
    )


def deploy(notebook_saved: threading.Event, filesytem_synced: threading.Event, notebook_browser_path: str, theme_variant="light"):
    mixpanel.api.track_with_defaults(
        "interaction",
        {
            "section": "deploy",
            "type": "deploy start",
        },
    )
    with step("Generating app startup script"):
        log("Generating app startup script content using theme variant: " + theme_variant)
        run_sh_content = run_sh_content_template.format(
            theme_variant=theme_variant,
            theme_loader="plain",
        ).encode("utf8")
        log(f"Write app.sh to working dir: {settings.domino_working_dir}")
        root = Path(settings.domino_working_dir)
        path = root / "app.sh"

        with open(path, "wb") as f:
            f.write(run_sh_content)
        log("Generated app startup script")

    with step("Saving notebook"):
        log("Requesting notebook save")
        notebook_save_request.value += 1

        if not notebook_saved.wait(timeout=timeout_notebook_save):
            log(f"Notebook save timeout: waited {timeout_notebook_save} seconds, but got no response")
            raise TimeoutError("Could not save notebook")
        if notebook_saved_error.value:
            log("Notebook saved, but return an error")
            raise Exception("Could not save notebook")
        root = Path(settings.domino_working_dir)
        notebook_local_path = Path(os.getcwd()) / Path(notebook_browser_path).name
        log(f"Saved notebook to {notebook_local_path}")
        shutil.copy2(notebook_local_path, root / settings.domino_notebook_deploy_filename)
        log(f"Copied notebook for deployment to {root / settings.domino_notebook_deploy_filename}")

    with step("Validating app"):
        log(f"Running python -m domino_code_assist.app_entrypoint with working directory: {settings.domino_working_dir}")
        proc = validate_app()
        if proc.returncode != 0:
            raise Exception(proc.stderr.decode("utf-8").split("\n")[-2])
        log("Notebook ran without errors")

    with step("Syncing files"):
        # what if not file changes?
        log("Asking Domino API endpoint to sync Project Files")
        get_domino_api().sync("Auto sync from Domino Code Assist for deployment")

        if not filesytem_synced.wait(timeout=timeout_filesystem_sync):
            log(f"Did not get a confirmation that files were synced within {timeout_filesystem_sync} seconds")
            raise TimeoutError("Did not synchronize files")
        log("Files were synced")

    with step("Deploying new app... (this may take a while)"):
        log("Asking Domino API endpoint for app status")
        # what if we started a new project?
        status = get_domino_api().get_app_status() or AppStatus.NON_EXISTENT
        if status not in APP_END_STATES:
            log(f"App status {status} is not in {APP_END_STATES}")
            raise Exception(f"Unexpected initial state: {status} for app")
        log(f"Got initial app state: {status}")

        if status == AppStatus.RUNNING:
            log("Asking Domino API endpoint to stop app")
            get_domino_api().app_unpublish()

            for i in range(timeout_app_stop):
                status = get_domino_api().get_app_status() or AppStatus.NON_EXISTENT
                if status == AppStatus.STOPPED:
                    log("App stopped")
                    break
                log(f"App is in state {status}, waiting for it to stop")
                time.sleep(app_poll_delay)
            else:
                log(f"App did not stop within {timeout_app_stop} seconds")
                raise TimeoutError("Could not stop app")

        log("Asking Domino API endpoint to start app")
        # If we publish directly, maybe the app will not pick up the latest file changes
        # To be safe, we wait a bit
        time.sleep(delay_app_publish)
        get_domino_api().app_publish()
        for i in range(timeout_app_start):
            status = get_domino_api().get_app_status() or AppStatus.NON_EXISTENT
            if status == AppStatus.RUNNING:
                log("App started")
                mixpanel.api.track_with_defaults(
                    "interaction",
                    {
                        "section": "deploy",
                        "type": "deploy success",
                    },
                )
                return True
            elif status in APP_END_STATES:
                log(f"App is in state {status}, but expected it to be {AppStatus.RUNNING}")
                # raise Exception(f"Could not start app (status: {status})")
                return False
            log(f"App is in state {status}, waiting for it to start")
            time.sleep(app_poll_delay)
        else:
            log(f"App did not start within {timeout_app_start} seconds")
            raise TimeoutError(f"Could not start app (status: {status})")


@solara.component
def Advanced():
    deploy_log.use()
    # server_logs, set_server_logs = solara.use_state([""])

    def get_logs() -> Iterator[Optional[List[str]]]:
        while True:
            if get_domino_api().get_app_id() is not None:
                logs = get_domino_api().get_app_log()
                lines = [k["log"] for k in logs]
                yield lines
            else:
                yield None
            time.sleep(server_log_update_deplay)

    server_log_result: Result[List[str]] = solara.use_thread(get_logs)

    lines = [f"{k.timestamp}: {k.message}" for k in deploy_log.value]
    text = "\n".join(lines)

    with v.Tabs() as main:
        v.Tab(children=["DCA deploy logs"])
        v.Tab(children=["Domino server app logs"])
        with v.TabItem():
            solara.Preformatted(text).meta(ref="log")
        with v.TabItem():
            if server_log_result.error:
                solara.Error(repr(server_log_result.error))
            else:
                server_log = "\n".join(server_log_result.value or ["No app exists yet"])

                solara.Style(
                    """
                .dca-server-logs {
                    overflow: auto;
                }
                """
                )
                solara.Text("Logs update every 10 seconds")
                solara.Preformatted(server_log, attributes={"class": "dca-server-logs"}).meta(ref="server_logs")
                url = f"/launchpad-publisher/{settings.domino_project_owner}/{settings.domino_project_name}/publishApp"
                solara.HTML(unsafe_innerHTML=f'Watch the logs at <a href="{url}" target="_blank">The Domino interface</a>.')
    return main


def use_current_environment() -> Result[str]:
    def get_current_environment():
        current_id = get_domino_api().get_current_environment_id()
        environments = get_domino_api().get_useable_environments()["environments"]
        names = [k["name"] for k in environments if k["id"] == current_id]
        if len(names) == 1:
            return names[0]
        else:
            return "UNKNOWN"

    return solara.use_thread(get_current_environment)


def use_default_environment() -> Result[str]:
    def get_default_environment():
        env_info = get_domino_api().get_useable_environments()
        environments = env_info["environments"]
        default_id = env_info["currentlySelectedEnvironment"]["id"]
        names = [k["name"] for k in environments if k["id"] == default_id]
        if len(names) == 1:
            return names[0]
        else:
            return "UNKNOWN"

    return solara.use_thread(get_default_environment)


@reacton.component
def Deployer(app: Callable[[], reacton.core.Element]):
    successfull_once, set_successfull_once = solara.use_state(False)
    show_app_deployed_dialog, set_show_app_deployed_dialog = solara.use_state(False)
    open_advanced, set_open_advanced = solara.use_state(False)
    online, set_online = reacton.use_state(False)
    open_preview, set_open_preview = reacton.use_state(False)
    deploy_request, set_deploy_request = reacton.use_state(False)
    filesystem_watcher_connected, set_filesystem_watcher_connected = reacton.use_state(False)
    last_deploy, set_last_deploy = solara.use_state(cast(Optional[datetime], None))
    filesystem_sync_failed, set_filesystem_sync_failed = reacton.use_state(False)

    current_env: Result[str] = use_current_environment()
    default_env: Result[str] = use_default_environment()

    def update_last_deploy():
        if deploy_request and not show_app_deployed_dialog:
            # we closed the dialog
            set_last_deploy(datetime.now())

    solara.use_memo(update_last_deploy, [deploy_request, show_app_deployed_dialog])

    notebook_save_request.use()
    domino_code_assist.assistant.notebook.notebook_browser_path.use()
    deploy_step.use()

    # The reactive variables need to be reset when the component gets re-created
    # since the lifetime is tied to the Python runtime.
    def reset():
        deploy_step.value = ""
        notebook_saved_error.value = False
        deploy_log.value = ()

    solara.use_memo(reset, [])

    # We constantly poll the app status, since it may sometimes fail later on (after deployment is successful)
    # or a different process/UI may change the app state.

    def app_status_info_run(cancel: threading.Event) -> Iterator[Tuple[AppStatus, AppInfo]]:
        while True:
            try:
                status = get_domino_api().get_app_status() or AppStatus.NON_EXISTENT
                info = get_domino_api().get_app_info()
                yield status, info[0] if len(info) else None
            except Exception:
                logger.exception("Error getting app status or info")
            time.sleep(delay_app_state)

    app_state: Result[Tuple[AppStatus, AppInfo]] = sol.use_thread(app_status_info_run, dependencies=[])
    # split app_state into app_status and app_info
    app_status: Optional[AppStatus] = None
    app_info: Optional[AppInfo] = None
    if app_state.state == solara.ResultState.RUNNING and app_state.value is not None:
        assert app_state is not None
        app_status, app_info = app_state.value

    # We run the deploy in a thread, and communicate via the reactive variables,
    # the return value (True if successful, False otherwise) and two events (notebook_saved and filesystem_synced)
    def run_deploy():
        if deploy_request:
            return deploy(
                notebook_saved=notebook_saved,
                filesytem_synced=filesytem_synced,
                notebook_browser_path=domino_code_assist.assistant.notebook.notebook_browser_path.value,
            )

    # these all have the same dependencies, such that if we 'redo' a deploy, we reset all of it
    notebook_saved = solara.use_memo(threading.Event, dependencies=[deploy_request])
    filesytem_synced = solara.use_memo(threading.Event, dependencies=[deploy_request])
    deployed: Result[bool] = sol.use_thread(run_deploy, dependencies=[deploy_request])

    # We respond to the notebook save request using a side effect
    # which will then trigger an notebook_saved event.
    initial_notebook_saved_value = solara.use_memo(notebook_save_request.get, dependencies=[])

    def save_notebook():
        from domino_code_assist.assistant import notebook

        assert notebook.save_notebook

        def on_save(is_saved):
            notebook_saved_error.value = not is_saved
            notebook_saved.set()

        # we don't want to save the notebook on the first run
        if initial_notebook_saved_value != notebook_save_request.value:
            notebook.save_notebook(on_save)

    solara.use_effect(save_notebook, dependencies=[notebook_save_request.value])

    app_url = f"/modelproducts/{app_info['id']}" if app_info else ""
    disable_view = (deploy_request and not online) or (not deploy_request and app_status != AppStatus.RUNNING)
    should_use_embed.provide(False)
    with v.Sheet() as main:
        with v.Dialog(v_model=open_preview, on_v_model=set_open_preview, fullscreen=True, hide_overlay=True, persistent=True, no_click_animation=True):
            with v.Sheet(class_="overflow-y-auto overflow-x-auto"):
                with solara.AppLayout():
                    with solara.AppBar():
                        solara.Button(icon_name="mdi-close", on_click=lambda: set_open_preview(False), icon=True)
                    if open_preview:
                        app()
        with sol.Div(class_="d-flex justify-center"):

            def deploy_or_retry():
                # WARNING: in the future, if reacton batches updates, we may have to find another way
                # as toggling a boolean might not trigger a re-render
                if deployed.error:
                    set_deploy_request(False)
                    set_deploy_request(True)
                else:
                    if deploy_request:
                        set_deploy_request(False)
                    set_deploy_request(True)
                # make sure we start with the default valyue again
                set_online(False)

            loading = False
            if deploy_request:
                if deployed.state == solara.ResultState.RUNNING:
                    loading = True
                elif deployed.state == solara.ResultState.FINISHED and app_status == AppStatus.RUNNING and not deployed.error:
                    loading = not online
            else:
                loading = (not filesystem_watcher_connected) or app_status not in APP_END_STATES
            solara.Button(
                "Re-Deploy app" if successfull_once else "Deploy app",
                on_click=deploy_or_retry,
                color="primary",
                disabled=loading,
                class_="ma-1",
                icon_name="mdi-rocket",
            ).meta(ref="deploy")
            sol.Button(
                "View app",
                class_="ma-1",
                color="primary",
                icon_name="mdi-application",
                disabled=disable_view,
                href=app_url,
                target="_blank",
                on_click=track_view_app,
                outlined=True,
            ).meta(ref="view_app")
            ButtonClipboard(pathname=app_url, disabled=disable_view)
            solara.Button(
                "Preview app",
                icon_name="mdi-magnify",
                color="primary",
                on_click=lambda: set_open_preview(True),
                outlined=True,
                class_="ma-1",
            )
            v.Spacer()
            sol.Button(
                "Advanced",
                class_="ma-1",
                icon_name="mdi-cogs",
                on_click=lambda: set_open_advanced(True),
                text=True,
            ).meta(ref="advanced")
        with v.Dialog(v_model=open_advanced, on_v_model=set_open_advanced, width="800px"):
            with v.Card():
                with v.CardText(class_="pt-2"):
                    if open_advanced:
                        Advanced()
                with v.CardActions():
                    sol.Button("Close", icon_name="mdi-close", on_click=lambda: set_open_advanced(False)).meta(ref="close_advanced")

        message_type = "info"
        if app_state.state == solara.ResultState.ERROR:
            info_message = "Error getting app state"
            message_type = "error"
        elif app_status is None:
            info_message = "Getting app state..."
        else:
            info_message = f"App state: {app_status}"
            if deployed.state == solara.ResultState.ERROR:
                info_message = f"Error deploying app: {deployed.error}"
                message_type = "error"
            else:
                if app_status == AppStatus.RUNNING and deployed.state == solara.ResultState.FINISHED and filesystem_watcher_connected:
                    if app_info:
                        try:
                            last_deploy_msg = humanize.naturaltime(datetime.now(timezone.utc) - parser.parse(app_info["created"]))
                        except Exception as e:
                            last_deploy_msg = f"error: {type(e).__name__} - {str(e)}"
                        info_message = (
                            f"The app was deployed {last_deploy_msg}. "
                            'If you\'ve made changes since the last deployment, click the "DEPLOY APP" button to redeploy.'
                        )
                    else:
                        info_message = "No app deployed yet"
                elif deployed.state == solara.ResultState.RUNNING:
                    if deploy_request:
                        # we get the info from the deploy function via deploy_step
                        info_message = deploy_step.value
                        if not info_message:
                            info_message = "Deploying app..."
        if not filesystem_watcher_connected:
            info_message = "Waiting for file system watcher..."

        if deployed.value and deployed.state == solara.ResultState.FINISHED and app_status == AppStatus.RUNNING:
            if online:
                fresh_deploy = False
                if last_deploy is not None:
                    fresh_deploy = (datetime.now() - last_deploy) <= fresh_deploy_delta
                if fresh_deploy:
                    info_message = "App deployed"
                    message_type = "success"
                # else we keep the "The app was deployed ... ago message"
            else:
                info_message = "Waiting for app to get online"
        if deployed.value is False and deployed.state == solara.ResultState.FINISHED:
            info_message = "App not deployed, click the advanced button for more details."
            message_type = "error"
        v.ProgressLinear(indeterminate=True, style_="visibility: " + ("hidden" if not loading else "visible"), class_="ma-1")
        v.Alert(type=message_type, children=[info_message], text=True, outlined=True, dense=False, icon=True, class_="ma-1").meta(ref="info_message")

        # only if the deployment if not successful, we show a warning when the environment is different
        if current_env.state == solara.ResultState.FINISHED and default_env.state == solara.ResultState.FINISHED and current_env.value != default_env.value:
            with solara.Warning(
                f"The current workspace is using the {current_env.value!r} environment, but the app is deployed with the {default_env.value!r} environment. "
                "This may have caused your app to fail",
                classes=["ma-1"],
            ).meta(ref="environment_message").key("environment_message"):
                settings_urls = f"/u/{settings.domino_project_owner}/{settings.domino_project_name}/settings#execution"
                solara.Markdown(
                    f'<a href="{settings_urls}" target="_blank">Changing your default environment to {current_env.value!r}'
                    "in your settings may solve this problem.</a>"
                )

        if deployed.value is not False:
            # if deployed, we do not need the filesystem watcher anymore
            # the frontend knows the hosts, we don't
            server_path = f"/u/{settings.domino_project_owner}/{settings.domino_project_name}/interactiveSession/ws/{settings.domino_run_id}"

            def on_message(msg):
                if msg is None:
                    return
                type = msg.get("type")
                if type == "RunResourcesStatusChangedEvent":
                    status = msg.get("status", {})
                    repositories = status.get("repositories", [])
                    for repository in repositories:
                        name = repository.get("name", "")
                        if name == "Domino Files":
                            status = repository.get("status", "")
                            clean = status.get("Clean")
                            if clean == {}:
                                if not filesytem_synced.is_set():
                                    log("Filesystem is clean, no need to sync")
                                filesytem_synced.set()
                                return
                elif type == "RunFullFileSynchronizationEvent":
                    key = msg.get("key", "")
                    if key == "full.sync.succeeded":
                        if not filesytem_synced.is_set():
                            log("Filesystem is synced successfully")
                        filesytem_synced.set()
                        set_filesystem_sync_failed(False)
                        return
                elif type == "FailedFileSynchronizationEvent":
                    key = msg.get("key", "")
                    if key == "full.sync.failed":
                        log("Filesystem sync failed")
                        set_filesystem_sync_failed(True)
                        return

            FileSystemWatcher(
                server_path=server_path, on_connected=set_filesystem_watcher_connected, on_message=on_message, dev=bool(settings.domino_code_assist_dev)
            ).meta(ref="filesystem_watcher").key("filesystem_watcher")

        def on_online(value):
            log("App is online" if value else "App is offline")
            set_online(value)
            # should_show_app_deployed_dialog = deploy_request and online and app_status == AppStatus.RUNNING and deployed.state == solara.ResultState.FINISHED
            # we only show it once
            if value and deploy_request and not show_app_deployed_dialog and deployed.state == solara.ResultState.FINISHED:
                set_show_app_deployed_dialog(True)
                set_successfull_once(True)

            # solara.use_memo(update_popup, [deploy_request, online, app_status, deployed.state])

        if bool(deployed.value) or bool(app_info):
            AppChecker(
                url=app_info["openUrl"] if app_info else "",
                online=online,
                running=app_status == AppStatus.RUNNING,
                on_online=on_online,
                dev=bool(settings.domino_code_assist_dev),
            ).key("app_checker")

        # popup when deployment is succesfull
        with v.Dialog(v_model=show_app_deployed_dialog, on_v_model=lambda v: set_show_app_deployed_dialog(v), width="400px").meta(ref="popup").key("popup"):
            with v.Card():
                with v.CardText(class_="pt-2"):
                    sol.Info(sol.HTML(unsafe_innerHTML="<h2>Your app is deployed! 🎉<h2>"), icon=False, classes=["mt-4", "mb-0"])

                with v.CardActions(class_="mx-3"):
                    with sol.Div(class_="d-flex justify-center"):
                        sol.Button(
                            "View app",
                            color="primary",
                            class_="ma-1",
                            icon_name="mdi-application",
                            href=app_url,
                            target="_blank",
                            on_click=track_view_app,
                        )
                        ButtonClipboard(pathname=app_url)
                    sol.Button(
                        "Close",
                        icon_name="mdi-close",
                        on_click=lambda: set_show_app_deployed_dialog(False),
                        color="primary",
                        outlined=True,
                    )
        if filesystem_sync_failed:
            with solara.Error(
                "File system sync failed. Please try to sync again manually using the Domino interface, as shown in the image below.", classes=["ma-1"]
            ).meta(ref="sync_error").key("sync_error"):
                v.Img(src=deploy_sync, style_="height: 455px", contain=True, class_="ma-4").meta(ref="sync_image")

    return main
