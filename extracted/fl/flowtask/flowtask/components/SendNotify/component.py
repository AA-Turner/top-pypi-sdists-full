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
from ..flow import FlowComponent
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
        print(
            f"Notification with status {result!s} to {recipient.account!s}"
        )
        logging.info(f"Notification with status {result!s} to {recipient.account!s}")
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
        # using mailing list:
        if hasattr(self, "list"):
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
        account = {**self.credentials}

        try:
            self.notify = Notify(self.via, loop=self._loop, **account)
            self.notify.sent = self.status_sent
        except Exception as err:
            raise ComponentError(f"Error Creating Notification App: {err}") from err
        try:
            result = await self.notify.send(
                recipient=self._recipients,
                attachments=self.list_attachment,
                **self.message,
            )
            logging.debug(f"Notification Status: {result}")
            self.add_metric("Notification", self.message)
        except Exception as err:
            raise ComponentError(f"SendNotify Error: {err}") from err
        if self.log_table and self.via == 'zoom':
            await self._flush_zoom_log()
        if self.data is None:
            return True
        return self._result
