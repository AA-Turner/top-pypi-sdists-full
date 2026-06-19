# Logging:
import socket
from navconfig.logging import logging

## Notify System
from notify import Notify
from notify.providers.email import Email
from notify.providers.slack import Slack
from notify.providers.teams import Teams
from notify.models import (
    Actor,
    Chat,
    Channel,
    TeamsCard,
    TeamsChannel
)
from ...conf import (
    SEND_NOTIFICATIONS,
    EVENT_CHAT_ID,
    EVENT_CHAT_BOT,
    NOTIFY_ON_ERROR,
    NOTIFY_ON_SUCCESS,
    NOTIFY_ON_FAILURE,
    NOTIFY_ON_WARNING,
    DEFAULT_RECIPIENT,
    EMAIL_USERNAME,
    EMAIL_PASSWORD,
    EMAIL_PORT,
    EMAIL_HOST,
    ENVIRONMENT,
    SLACK_DEFAULT_CHANNEL,
    SLACK_DEFAULT_CHANNEL_NAME,
    MS_TEAMS_DEFAULT_TEAMS_ID,
    MS_TEAMS_DEFAULT_CHANNEL_ID,
    MS_TEAMS_DEFAULT_CHANNEL_NAME,
    SHOW_VERSION
)
from ...utils.functions import check_empty
from .abstract import AbstractEvent
from ...version import __version__
from ...utils.msgraph_patch import patch_graph_host_os_header

# This module imports the Teams provider eagerly (and therefore msgraph-core),
# so sanitise the HostOs telemetry header at import time to avoid h11
# "Illegal header value" errors on trailing-space kernel versions.
patch_graph_host_os_header()


class NotifyEvent(AbstractEvent):
    """Using Notify to send notifications for task Execution."""

    _hostname: str = socket.gethostname()

    def __init__(self, *args, event: str = "done", **kwargs):
        super(NotifyEvent, self).__init__(*args, **kwargs)
        self._logger = logging.getLogger("FlowTask.Notify")
        self._event_ = event
        if event == "done":
            self.event = NOTIFY_ON_SUCCESS
        elif event == "warning":
            self.event = NOTIFY_ON_WARNING
        elif event == "error":
            self.event = NOTIFY_ON_ERROR
        elif event == "exception":
            self.event = NOTIFY_ON_FAILURE
        else:
            self.event = NOTIFY_ON_SUCCESS

    def getNotify(self, notify, **kwargs):
        if notify == "telegram":
            # defining the Default chat object:
            recipient = Chat(**{"chat_id": EVENT_CHAT_ID, "chat_name": "Navigator"})
            # send notifications to Telegram bot
            args = {"bot_token": EVENT_CHAT_BOT, **kwargs}
            ntf = Notify("telegram", **args)
        elif notify == "slack":
            recipient = Channel(
                channel_id=SLACK_DEFAULT_CHANNEL,
                channel_name=SLACK_DEFAULT_CHANNEL_NAME,
            )
            ntf = Slack()
        elif notify == "email":
            account = {
                "host": EMAIL_HOST,
                "port": EMAIL_PORT,
                "username": EMAIL_USERNAME,
                "password": EMAIL_PASSWORD,
                **kwargs,
            }
            recipient = Actor(**DEFAULT_RECIPIENT)
            ntf = Email(debug=True, **account)
        elif notify == 'teams':
            team_id = kwargs.pop("team_id", MS_TEAMS_DEFAULT_TEAMS_ID)
            recipient = TeamsChannel(
                name=MS_TEAMS_DEFAULT_CHANNEL_NAME,
                team_id=team_id,
                channel_id=MS_TEAMS_DEFAULT_CHANNEL_ID
            )
            ntf = Teams(
                as_user=True,
                team_id=team_id,
            )
        else:
            # Any other Notify Provider:
            recipient = Actor(**DEFAULT_RECIPIENT)
            ntf = Notify(notify, **kwargs)
        return [ntf, recipient]

    async def __call__(self, *args, **kwargs):
        if SEND_NOTIFICATIONS is False:
            return
        task = kwargs.pop("task", None)
        result = kwargs.pop("result", None)
        message = kwargs.pop("message", None)
        trace = kwargs.pop("stacktrace", None)
        error = kwargs.pop("error", None)
        program = task.getProgram()
        task_name = task.taskname
        component = kwargs.pop("component", None)
        host = self._hostname
        if error is not None:
            self.event = NOTIFY_ON_ERROR
            if program and task and component:
                message = f"🛑 :: {ENVIRONMENT} - {program}.{task_name}, Error on {component}: {error!s} (host: {host})"
            elif program and task:
                message = (
                    f"🛑 :: {ENVIRONMENT} - Error on {program}.{task_name}: {error!s} (host: {host})"
                )
            elif trace is not None:
                self.event = NOTIFY_ON_FAILURE
                message = f"🛑 :: {ENVIRONMENT} - {program}.{task_name}: {error!s} (host: {host})"
            else:
                message = f"🛑 :: {ENVIRONMENT} - {program}.{task_name}: {error!s} (host: {host})"
        elif self._event_ == "warning":
            message = f"⚠️ :: {ENVIRONMENT} - *{program}.{task_name}*: Warning {component}->{str(message)!s} (host: {host})"
        else:
            if message is not None and result is not None:
                # success event:
                self.event = NOTIFY_ON_SUCCESS
                message = f"✅ :: {ENVIRONMENT} - {program}.{task_name}: {message!s} (host: {host})"
            elif not check_empty(result):
                message = f"✅ :: {ENVIRONMENT} - {program}.{task_name}: {message!s} (host: {host})"
            else:
                message = f"⚠️ :: {ENVIRONMENT} - {program}.{task_name}: {message!s}, Empty Result. (host: {host})"

        if SHOW_VERSION:
            message = f"{message} - Version: {__version__}"
        ntf, recipients = self.getNotify(self.event, **kwargs)
        args = {"recipient": [recipients], "message": message}
        if self.event == 'teams':
            channel = recipients
            msg = TeamsCard(
                text=str(message),
                summary=f"Task Summary: {program}.{task_name}",
                title=f"Task {program}.{task_name}",
            )
            async with ntf as conn:
                return await conn.send(
                    recipient=channel,
                    message=msg
                )
        elif ntf.provider_type == "email":
            args["subject"] = message
        elif ntf.provider == "telegram":
            args["disable_notification"] = True
        else:
            args["subject"] = message
        async with ntf as t:
            result = await t.send(**args)
        return result
