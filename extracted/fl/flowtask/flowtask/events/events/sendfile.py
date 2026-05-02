from typing import Union
from collections.abc import Callable, Iterable
import asyncio
from pathlib import Path
from notify.models import Actor
from notify import Notify
from ...exceptions import FileNotFound, ActionError
from .interfaces import ClientInterface
from .abstract import AbstractEvent


def expand_path(filename: Union[str, Path]) -> Iterable[Path]:
    if isinstance(filename, str):
        p = Path(filename)
    else:
        p = filename
    return list(Path(p.parent).expanduser().glob(p.name))


class SendFile(ClientInterface, AbstractEvent):
    def __init__(self, *args, **kwargs):
        self.list_attachment: list = []
        self.notify: Callable = None
        super(SendFile, self).__init__(*args, **kwargs)

    async def __call__(self, *args, **kwargs):
        # determine the recipients:
        # TODO: add support for mailing lists
        try:
            self._recipients = [Actor(**user) for user in self.recipients]
        except Exception as err:
            raise RuntimeError(f"Error formatting Recipients: {err}") from err
        if not self._recipients:
            raise RuntimeError("SendNotify: Invalid Number of Recipients.")

        # File Attachment:
        # TODO: multiple attachments
        if hasattr(self, "directory"):
            d = self.mask_replacement(
                self.directory  # pylint: disable=access-member-before-definition
            )
            p = Path(d)  # pylint: disable=E0203
            if p.exists() and p.is_dir():
                self.directory = p
            else:
                self._logger.error(f"Path doesn't exists: {self.directory}")
        else:
            self.directory = None

        if hasattr(self, "filename"):
            file = self.mask_replacement(self.filename)
            files = []
            if self.directory:
                fs = self.directory.joinpath(file)
                files = expand_path(fs)
            else:
                files = expand_path(file)
            for file in files:
                if file.exists():
                    self.list_attachment.append(file)
                else:
                    raise FileNotFound(f"File doesn't exists: {file}")

        # Mask transform of message
        for key, value in self.message.items():
            self.message[key] = self.mask_replacement(value)

        try:
            await self.open()
            async with self.notify as mail:
                try:
                    result = await mail.send(
                        recipient=self._recipients,
                        attachments=self.list_attachment,
                        **self.message,
                    )
                    self._logger.debug(f"Notification Status: {result}")
                except Exception as err:
                    raise ActionError(f"SendNotify Error: {err}") from err
                return None
        finally:
            await self.close()

    async def close(self):
        """close.
        Closing the connection.
        """
        if self.notify:
            try:
                await self.notify.close()
            except Exception as err:
                print(err)

    async def open(self):
        """open.
        Starts (open) a connection to an external resource.
        """
        try:
            self.notify = Notify(
                "email", loop=asyncio.get_event_loop(), **self.credentials
            )
        except Exception as err:
            raise ActionError(f"Error Creating Notification App: {err}") from err
        return self
