import os
import asyncio
from datetime import datetime, timezone
from typing import Dict, List
from collections.abc import Callable, Iterable
from pathlib import Path
from navconfig.logging import logging
from notify import Notify
from notify.models import Actor
from ...exceptions import ComponentError, FileNotFound
from ...interfaces.flow import FlowComponent
from ...interfaces import DBSupport


def expand_path(filename: str) -> Iterable[Path]:
    p = Path(filename)
    return Path(p.parent).expanduser().glob(p.name)


class SendNotify(DBSupport, FlowComponent):
    """
    SendNotify

        Overview

            The SendNotify class is a component for sending notifications to a list of recipients via various
            channels (e.g., email) using the Notify component. It supports adding attachments, templating messages
            with masked variables, and utilizing custom credentials for authentication.

        :widths: auto

            | via            |   Yes    | The method for sending the notification, e.g., "email".                          |
            | account        |   Yes    | A dictionary with server credentials, including `host`, `port`,                  |
            |                |          | `username`, and `password`.                                                      |
            | recipients     |   Yes    | List of dictionaries with target user details for notification.                  |
            | list           |   No     | Optional mailing list name for retrieving recipients from the database.          |
            | attachments    |   No     | List of file paths for attachments to include in the notification.               |
            | message        |   Yes    | Dictionary with the notification message content, supporting template variables. |
            | scenario_id    |   No     | Business scenario identifier logged alongside the notification.                  |
            | log_table      |   No     | If true, persists each sent notification to the provider log table.             |

        Returns

            This component returns the input data after sending the notification. Metrics are recorded for each
            successful send, with details on recipients and the message content. If any specified attachment file
            is missing, a `FileNotFound` exception is raised. If there are errors in setting up or sending the
            notification, a `ComponentError` is raised with descriptive messages.


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          SendNotify:
          via: zoom
          scenario_id: LC_WELCOME
          log_table: true
          recipients:
          - name: "{first_name}"
            account:
              number: "{phone_e164}"
          message:
            message: "{message_content}"
        ```
    """
    _version = "1.0.0"

    _credentials: dict = {
        "hostname": str,
        "port": int,
        "username": str,
        "password": str,
    }

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self.attachments: List = []
        self.list_attachment: List = []
        self.notify: Callable = None
        self.recipients: List = []
        self._recipients: List = []
        self.via: str = "email"
        self.message: Dict = {}
        self.scenario_id: str = kwargs.pop('scenario_id', None)
        self.log_table: bool = kwargs.pop('log_table', False)
        self._pending_logs: List = []
        # Teams channel target (used when via == 'teams' to post to a channel
        # instead of a direct message): team_id/channel_id accept either a literal
        # id or an env var name (resolved via get_env_value in start()).
        self.team_id = kwargs.pop('team_id', None)
        self.channel_id = kwargs.pop('channel_id', None)
        self.chat_id = kwargs.pop('chat_id', None)
        self.webhook = kwargs.pop('webhook', None)
        # Group direct message: post to a group chat created among `recipients`
        # (Actors by email) with an optional topic.
        self.group = kwargs.pop('group', False)
        self.topic = kwargs.pop('topic', None)
        self.channel_name = kwargs.pop('channel_name', 'General')
        self.as_user = kwargs.pop('as_user', True)
        self._team_id = None
        # Teams auth overrides: each accepts a literal value or an env var name
        # (resolved via get_env_value in run()). When omitted, the Teams provider
        # falls back to its MS_TEAMS_* / O365_* env defaults.
        self.client_id = kwargs.pop('client_id', None)
        self.client_secret = kwargs.pop('client_secret', None)
        self.tenant_id = kwargs.pop('tenant_id', None)
        self.username = kwargs.pop('username', None)
        self.password = kwargs.pop('password', None)
        # renaming account to credentials in kwargs:
        if "account" in kwargs:
            kwargs["credentials"] = kwargs.pop("account")
        super(SendNotify, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

    def status_sent(self, recipient, message, result, *args, **kwargs):
        # TeamsChannel/TeamsChat recipients have no `.account`; fall back safely.
        target = getattr(recipient, 'account', None) or getattr(recipient, 'name', None) or recipient
        print(
            f"Notification with status {result!s} to {target!s}"
        )
        logging.info(f"Notification with status {result!s} to {target!s}")
        status = {"recipient": recipient, "result": result}
        self.add_metric("Sent", status)
        if self.log_table and isinstance(result, dict) and result.get('message_id'):
            raw_dt = result.get('date_time')
            try:
                sent_at = datetime.fromisoformat(raw_dt.replace('Z', '+00:00'))
            except (AttributeError, ValueError):
                sent_at = datetime.now(timezone.utc)
            self._pending_logs.append({
                'message_id':      result.get('message_id'),
                'session_id':      result.get('session_id'),
                'sent_at':         sent_at,
                'recipient_name':  recipient.name,
                'recipient_address': str(
                    getattr(recipient.account, 'number', None)
                    or getattr(recipient.account, 'address', None)
                    or recipient.account
                ),
                'message_content': str(message),
                'associate_id':    self._variables.get('associate_id'),
                'token':           self._variables.get('token'),
            })

    def _build_teams_card(self, spec: dict):
        """Build a notify ``TeamsCard`` from a YAML card spec.

        Spec keys (all optional except summary):
            summary: short header / toast text (rendered as the title line).
            title, text: extra TextBlocks above the body.
            facts: list of {title, value} → a FactSet section.
            body: list of raw Adaptive Card elements (full styling control),
                  appended after title/summary/text/facts.
            version: Adaptive Card version (default 1.5).

        Placeholders ({sender_name}, etc.) are already resolved in start().
        """
        from notify.models import TeamsCard
        card = TeamsCard(
            summary=spec.get('summary', spec.get('title', 'Notification')),
            title=spec.get('title'),
            text=spec.get('text'),
            version=spec.get('version', '1.5'),
        )
        if spec.get('facts'):
            section = card.addSection()
            section.addFacts(facts=spec['facts'])
        if spec.get('body'):
            card.body_objects.extend(spec['body'])
        # actions: buttons (Action.Submit / Action.OpenUrl …) at the card footer.
        for action in spec.get('actions', []):
            card.addAction(
                type=action.get('type', 'Action.Submit'),
                title=action.get('title', ''),
                data=action.get('data', {}),
                url=action.get('url', ''),
            )
        return card

    async def _flush_zoom_log(self) -> None:
        """Persist pending Zoom SMS log entries to navigator.zoom_log."""
        if not self._pending_logs:
            return
        from .models.zoom import ZoomLog
        for entry in self._pending_logs:
            try:
                log = ZoomLog(
                    program_slug=self._program,
                    scenario_id=self.scenario_id,
                    task_id=getattr(self, '_task_id', None),
                    **entry
                )
                await log.save()
            except Exception as err:
                self._logger.warning(f"SendNotify: failed to write ZoomLog entry: {err}")
        self._pending_logs.clear()

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        await super().start(**kwargs)
        self.processing_credentials()
        # TODO: generate file from dataset (dataframe)
        # Teams: the provider routes by recipient type, so we build the matching
        # recipient — TeamsWebhook (webhook URL, no auth), TeamsChat (chat_id),
        # TeamsChannel (team_id + channel_id), or fall back to Actor(s) for DMs.
        if self.via == 'teams' and self.webhook:
            from notify.models import TeamsWebhook
            uri = self.get_env_value(self.webhook, default=self.webhook)
            self._recipients = [TeamsWebhook(uri=uri)]
        elif self.via == 'teams' and self.chat_id:
            from notify.models import TeamsChat
            chat_id = self.get_env_value(self.chat_id, default=self.chat_id)
            self._team_id = self.get_env_value(self.team_id, default=self.team_id) or ''
            self._recipients = [
                TeamsChat(
                    name=self.channel_name,
                    chat_id=chat_id,
                    team_id=self._team_id,
                )
            ]
        elif self.via == 'teams' and self.channel_id:
            from notify.models import TeamsChannel
            self._team_id = self.get_env_value(self.team_id, default=self.team_id)
            channel_id = self.get_env_value(self.channel_id, default=self.channel_id)
            self._recipients = [
                TeamsChannel(
                    name=self.channel_name,
                    team_id=self._team_id,
                    channel_id=channel_id,
                )
            ]
        # using mailing list:
        elif hasattr(self, "list"):
            # getting the mailing list:
            lst = self.list
            sql = f"SELECT * FROM troc.get_mailing_list('{lst!s}')"
            try:
                connection = self.get_connection()
                async with await connection.connection() as conn:
                    result, error = await conn.query(sql)
                    if error:
                        raise ComponentError(
                            f"CreateReport: Error on Recipients: {error!s}."
                        )
                    for r in result:
                        actor = Actor(**dict(r))
                        self._recipients.append(actor)
            except Exception as err:
                logging.exception(err)
        else:
            # determine the recipients:
            try:
                resolved = self.resolve_variables_recursively(self.recipients)
                self._recipients = [Actor(**user) for user in resolved]
            except Exception as err:
                raise ComponentError(f"Error formatting Recipients: {err}") from err
        if not self._recipients:
            raise ComponentError("SendNotify: Invalid Number of Recipients.")
        self.message = self.resolve_variables_recursively(self.message)
        if hasattr(self, "masks"):
            for _, attach in enumerate(self.attachments):
                attachment = self.mask_replacement(attach)
                # resolve filenames:
                files = expand_path(attachment)
                for file in files:
                    self.list_attachment.append(file)
            # Mask transform of message
            for key, value in self.message.items():
                self.message[key] = self.mask_replacement(value)
                self._logger.notice(
                    f"Variable: {key} = {self.message[key]}"
                )
        # Verify if file exists
        for file in self.list_attachment:
            if not file.exists():
                raise FileNotFound(
                    f"File doesn't exists: {file}"
                )
        return True

    async def close(self):
        if self.notify:
            try:
                await self.notify.close()
            except Exception as err:
                print(err)

    async def run(self):
        """
        Running the Notification over all recipients.
        """
        self._result = self.data  # by-pass override data (pass-through)
        if self.data is not None:
            if isinstance(self.data, list):
                self.message['filenames'] = self.data
            elif isinstance(self.data, dict):
                self.message.update(self.data)

        # create the notify component
        account = {**(self.credentials or {})}
        if self.via == 'teams':
            # Teams auth/credentials default from MS_TEAMS_* env in the provider;
            # channel posting needs delegated access (as_user) and the team_id.
            account.setdefault('as_user', self.as_user)
            if self._team_id:
                account.setdefault('team_id', self._team_id)
            # Optional per-task auth overrides — resolve env var names to values
            # and pass them to the provider (only when provided in the YAML).
            for key, val in (
                ('client_id', self.client_id),
                ('client_secret', self.client_secret),
                ('tenant_id', self.tenant_id),
                ('username', self.username),
                ('password', self.password),
            ):
                if val:
                    account[key] = self.get_env_value(val, default=val)
            # Message can be an Adaptive Card (message.card) or plain text.
            card_spec = self.message.get('card') if isinstance(self.message, dict) else None
            if card_spec:
                self.message = {'message': self._build_teams_card(card_spec)}
            else:
                text = self.message.get('message', '') if isinstance(self.message, dict) else str(self.message)
                if self.webhook:
                    # Webhooks render a plain string into a MessageCard themselves.
                    self.message = {'message': str(text)}
                else:
                    # Chat/channel endpoints need an HTML body; a bare string is
                    # rendered as a MessageCard they reject ("Missing body content").
                    self.message = {
                        'message': {'body': {'content': str(text).replace('\n', '<br>')}}
                    }

        try:
            self.notify = Notify(self.via, loop=self._loop, **account)
            self.notify.sent = self.status_sent
        except Exception as err:
            raise ComponentError(f"Error Creating Notification App: {err}") from err
        if self.via == 'teams' and not self.webhook:
            # The Teams provider builds its MS Graph client in connect(); send()
            # does not call it (the event-based usage relies on `async with`).
            # Webhooks are a plain HTTP POST and need no Graph auth.
            await self.notify.connect()
        try:
            if self.via == 'teams' and self.group:
                # Group direct message: creates/reuses a group chat among the
                # recipient Actors and posts there. Uses a dedicated provider
                # method (not send()), so it bypasses per-recipient fan-out.
                # TODO: send_group_direct_message does NOT render TeamsCard objects
                #       (it passes the message straight to send_message_to_chat, which
                #       str()-ifies non-dict messages). Until the provider renders
                #       cards on this path, group mode only sends plain text/HTML
                #       bodies correctly — cards will not display as adaptive cards.
                result = await self.notify.send_group_direct_message(
                    recipients=self._recipients,
                    message=self.message.get('message'),
                    topic=self.topic,
                )
            else:
                result = await self.notify.send(
                    recipient=self._recipients,
                    attachments=self.list_attachment,
                    **self.message,
                )
            logging.debug(f"Notification Status: {result}")
            self.add_metric("Notification", self.message)
        except Exception as err:
            raise ComponentError(f"SendNotify Error: {err}") from err
        # Failure-safety: the notify layer swallows per-recipient send errors and
        # returns an empty result. For Teams (used in per-row forward + mark groups),
        # raise so a failed send stops the group BEFORE the row is marked as sent.
        if self.via == 'teams' and not result:
            raise ComponentError(
                "SendNotify: Teams send failed (no message returned) — see provider log above."
            )
        if self.log_table and self.via == 'zoom':
            await self._flush_zoom_log()
        if self.data is None:
            return True
        return self._result
