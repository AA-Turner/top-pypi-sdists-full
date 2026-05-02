import asyncio
from collections.abc import Callable
import re
import fnmatch
from pathlib import Path, PurePath
import imaplib
import aiofiles
from ..conf import IMAP_RETRY_SELECT, FILES_PATH
from ..utils.mail import MailMessage
from ..exceptions import ComponentError, FileNotFound
from .DownloadFrom import DownloadFromBase
from ..interfaces.IMAPClient import IMAPClient


class DownloadFromIMAP(IMAPClient, DownloadFromBase):
    """
    DownloadFromIMAP.

        Overview

            Download emails from an IMAP mailbox using the functionality from DownloadFrom.

            :widths: auto

            | credentials       |   Yes    | Credentials to access the IMAP mailbox.                                                                 |
            | mailbox           |   Yes    | The IMAP mailbox name (default: "INBOX").                                                               |
            | search_terms      |   Yes    | Dictionary containing search criteria in IMAP format.                                                   |
            | attachments       |   Yes    | Dictionary specifying download configuration for attachments:                                           |
            |                   |          |   - directory (str): Path to save downloaded attachments.                                               |
            |                   |          |   - filename (str, optional): Filename pattern for selection (fnmatch).                                 |
            |                   |          |   - pattern (str, optional): Regular expression pattern for selection.                                  |
            |                   |          |   - expected_mime (str, optional): Expected MIME type filter.                                           |
            |                   |          |   - rename (str, optional): Template string for renaming attachments (uses "{filename}").               |
            |                   |          |   - download_existing (bool, optional): Skip existing files (default: True).                            |
            |                   |          |   - create_destination (bool, optional): Create download directory if it doesn't exist (default: True). |
            | download_existing |    no    | Flag indicating whether to skip downloading existing files.                                             |
            | results           |   Yes    | Dictionary containing download results:                                                                 |
            |                   |          |   - attachments: List of downloaded attachment file paths.                                              |
            |                   |          |   - messages: List of `MailMessage` objects representing downloaded emails.                             |
            | use_ssl           |   Yes    | Boolean for indicate if we need to use the TLS protocol                                                 |

            Save the downloaded files on the new destination.


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          DownloadFromIMAP:
          credentials:
          host: email_host
          port: email_port
          user: email_host_user
          password: email_host_password
          use_ssl: true
          search_terms:
          'ON': '{search_today}'
          SUBJECT: Custom Punch with Pay Codes - Excel
          FROM: eet_application@adp.com
          overwrite: true
          attachments:
          directory: /home/ubuntu/symbits/bose/files/worked_hours/
          masks:
          '{search_today}':
          - today
          - mask: '%d-%b-%Y'
        ```
    """
    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ) -> None:
        self.attachments = {"directory": None}
        self.search_terms = None
        super().__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

    async def start(self, **kwargs):  # pylint: disable=W0613
        if hasattr(self, "attachments"):
            # attachment directory
            if "directory" not in self.attachments:
                self.attachments["directory"] = FILES_PATH.joinpath(
                    self._program, "files", "download"
                )
            else:
                self.attachments["directory"] = Path(
                    self.attachments["directory"]
                ).resolve()
            try:
                directory = self.attachments["directory"]
                if not directory.exists():
                    if self.create_destination is True:
                        directory.mkdir(parents=True, exist_ok=True)
                    else:
                        raise ComponentError(
                            f"DownloadFromIMAP: Error creating directory: {directory}"
                        )
            except Exception as err:
                self._logger.error(
                    f"IMAP: Error creating directory: {err}"
                )
                raise ComponentError(
                    f"IMAP: Error creating directory: {err}"
                ) from err
            # masking elements:
            if hasattr(self, "masks"):
                for mask, replace in self._mask.items():
                    for key, val in self.attachments.items():
                        value = str(val).replace(mask, str(replace))
                        if isinstance(val, PurePath):
                            self.attachments[key] = Path(value)
                        else:
                            self.attachments[key] = value
        await super(DownloadFromIMAP, self).start(**kwargs)
        return True

    def _quote_imap_value(self, value: str) -> str:
        """
        Properly quote IMAP search values that contain special characters.

        IMAP special characters include: ( ) { } % * " \
        Values containing spaces or these characters must be quoted.
        """
        # Check if value needs quoting (contains spaces or special IMAP chars)
        special_chars = ['(', ')', '{', '}', '%', '*', '"', '\\', ' ']
        needs_quoting = any(char in value for char in special_chars)

        if needs_quoting:
            # Escape any internal double quotes and backslashes
            escaped_value = value.replace('\\', '\\\\').replace('"', '\\"')
            # Wrap in double quotes
            return f'"{escaped_value}"'

        return value

    async def run(self):
        self._result = None
        filter_criteria = []
        msgs = [""]
        messages = []
        files: list = []
        try:
            await self.open(self.host, self.port, self.credentials)
            if not self._client:
                raise ComponentError("IMAP Connection not Opened, exiting.")
        except Exception as err:
            self._logger.exception(err, stack_info=True)
            raise
        # getting search Terms
        self.search_terms = self.process_mask("search_terms")
        for term, value in self.search_terms.items():
            try:
                value = self.mask_replacement(value)
                # Quote the value if it contains special IMAP characters
                quoted_value = self._quote_imap_value(value)
                # For imaplib.search(), we need to pass criteria as separate arguments
                # We add the term and quoted value as separate items
                filter_criteria.append(term)
                filter_criteria.append(quoted_value)
                self._logger.debug(f"Added search criterion: {term} = {quoted_value}")
            except (ValueError, KeyError):
                pass
        self._logger.debug(f"FILTER CRITERIA: {filter_criteria}")
        self.add_metric("SEARCH", filter_criteria)

        try:
            # getting the Mailbox
            self._client.select(self.mailbox)
        except Exception as err:
            if "User is authenticated but not connected." in str(err):
                tries = 0
                while tries < IMAP_RETRY_SELECT:
                    self._client.logout()
                    await asyncio.sleep(10)
                    try:
                        await self.open(self.host, self.port, self.credentials)
                        if not self._client:
                            raise ComponentError(
                                "IMAP Connection not Opened, exiting."
                            ) from err
                        self._client.select(self.mailbox)
                        break
                    except Exception as exc:
                        self._logger.exception(exc, stack_info=True)
                        if tries < (IMAP_RETRY_SELECT - 1):
                            tries += 1
                            continue
                        else:
                            raise RuntimeError(
                                f"IMAP: Error opening Mailbox {self.mailbox}: {exc}"
                            ) from exc
        try:
            result, msgs = self._client.search(None, *filter_criteria)
            if result == "NO" or result == "BAD":
                self._logger.error(msgs[0])
                raise ComponentError(
                    message=f"Error on Search: {msgs[0]}",
                    status=500
                )
        except imaplib.IMAP4.abort as err:
            raise ComponentError(f"IMAP Illegal Search: {err}") from err
        except Exception as err:
            self._logger.exception(err, stack_info=True)
            raise ComponentError(f"IMAP Error: {err}") from err
        msgs = msgs[0].split()
        i = 0
        if not msgs:
            raise FileNotFound("DownloadFromIMAP: File(s) doesn't exists")
        if not isinstance(msgs, list):
            raise ComponentError(f"DownloadFromIMAP: Invalid Email Response: {msgs}")
        if "expected_mime" in self.attachments:
            expected_mime = self.attachments["expected_mime"]
            if expected_mime:
                validate_mime = True
            else:
                validate_mime = False
        else:
            expected_mime = None
            validate_mime = False
        for emailid in msgs:
            i += 1
            resp, data = self._client.fetch(emailid.decode("utf-8"), "(RFC822)")
            if resp == "OK":  # mail was retrieved
                msg = MailMessage(
                    self.attachments["directory"],
                    data[0][1].decode("utf-8"),
                    data[1],
                    validate_mime=validate_mime,
                )
                messages.append(msg)
                for attachment in msg.attachments:
                    if expected_mime is not None:
                        # checking only for valid MIME types:
                        if expected_mime != attachment["content_type"]:
                            continue
                    if "filename" in self.attachments:
                        fname = self.attachments[
                            "filename"
                        ]  # we only need to save selected files
                        if not fnmatch.fnmatch(attachment["filename"], fname):
                            continue
                        else:
                            if "rename" in self.attachments:
                                filename = self.attachments["rename"]
                                filename = filename.replace(
                                    "{filename}", Path(attachment["filename"]).stem
                                )
                                self._logger.debug(f"NEW FILENAME IS {filename}")
                                file_path = self.attachments["directory"].joinpath(
                                    filename
                                )
                            else:
                                file_path = self.attachments["directory"].joinpath(
                                    attachment["filename"]
                                )
                    elif (
                        "pattern" in self.attachments
                    ):  # only save files that match the pattern
                        fpattern = self.attachments["pattern"]
                        if bool(re.match(fpattern, attachment["filename"])):
                            file_path = self.attachments["directory"].joinpath(
                                attachment["filename"]
                            )
                        else:
                            continue
                    else:
                        # I need to save everything
                        if "rename" in self.attachments:
                            filename = self.attachments["rename"]
                            if hasattr(self, "masks"):
                                filename = self.mask_replacement(filename)
                                # for mask, replace in self._mask.items():
                                #     filename = filename.replace(mask, replace)
                            filename = filename.replace(
                                "{filename}", Path(attachment["filename"]).stem
                            )
                            file_path = self.attachments["directory"].joinpath(filename)
                        else:
                            file_path = self.attachments["directory"].joinpath(
                                attachment["filename"]
                            )
                    # saving the filename in the attachment
                    attachment["filename"] = file_path
                    if "download_existing" in self.attachments:
                        if (
                            file_path.exists()
                            and self.attachments["download_existing"] is False
                        ):
                            # we don't need to download again
                            self._logger.info(f"File Exists {file_path!s}, skipping")
                            continue
                    if file_path.exists() and self.overwrite is False:
                        # TODO: before to save a new renamed file,
                        #  we need to check if we have it (checksum)
                        file_name = file_path.name
                        # dir_name = file_path.absolute()
                        ext = file_path.suffix
                        # calculated new filepath
                        file_path = self.attachments["directory"].joinpath(
                            f"{file_name}_{i}{ext}"
                        )
                        if file_path.exists():
                            # TODO: more efficient way (while) to check if file exists
                            files.append(file_path)
                            continue
                    await self.save_attachment(file_path, attachment["attachment"])
                    # saving this file in the list of files:
                    files.append(file_path)
            else:
                raise ComponentError(f"File was not fetch: {resp}")
        # saving the result:
        self.add_metric("ATTACHMENTS", files)
        self.add_metric("NUM_ATTACHMENTS", len(files))
        self.add_metric('NUM_MESSAGES', len(messages))
        self._result = {"messages": messages, "files": files}
        return self._result

    async def save_attachment(self, file_path, content):
        try:
            self._logger.info(f"IMAP: Saving attachment file: {file_path}")
            async with aiofiles.open(file_path, mode="wb") as fp:
                await fp.write(content)
        except Exception as err:
            raise ComponentError(f"File {file_path} was not saved: {err}") from err
