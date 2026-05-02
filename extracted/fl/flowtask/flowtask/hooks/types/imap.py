from typing import Union, Optional
import imaplib
import time
from functools import partial
import ssl
from ...exceptions import ComponentError
from ...interfaces.azureauth import AzureAuth
from .watch import BaseWatchdog, BaseWatcher
from ...interfaces import CacheSupport


class ImapWatcher(BaseWatcher):
    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        mailbox="INBOX",
        use_ssl: bool = True,
        interval: int = 320,
        authmech: str = None,
        search: Optional[Union[str, dict, list]] = None,
        **kwargs,
    ):
        super(ImapWatcher, self).__init__(**kwargs)
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.mailbox = mailbox
        self.interval = interval
        self.authmech = authmech
        self.use_ssl = use_ssl
        self.search = search
        self.args = kwargs
        self._expiration = kwargs.pop("expiration", None)

    def close_watcher(self):
        try:
            self.imap_server.logout()
        except OSError as exc:
            self._logger.error(f"Error closing IMAP Connection: {exc}")

    def connect(self, max_retries: int = 3, delay: int = 10):
        if self.use_ssl is True:
            sslcontext = ssl.create_default_context()
            server = partial(
                imaplib.IMAP4_SSL,
                self.host,
                self.port,
                timeout=10,
                ssl_context=sslcontext,
            )
        else:
            server = partial(imaplib.IMAP4, self.host, self.port, timeout=10)
        # azure auth:
        if isinstance(server, str):
            raise ComponentError(
                f"Failed to configure to IMAP Server: {server}"
            )
        azure = AzureAuth()  # default values
        for attempt in range(max_retries):
            try:
                self.imap_server = server()
                if self.authmech == "XOAUTH2":
                    self._logger.debug("IMAP Auth XOAUTH2")
                    try:
                        result, msg = self.imap_server.authenticate(
                            self.authmech,
                            lambda x: azure.binary_token(self.user, self.password),
                        )
                        if result != "OK":
                            raise ComponentError(
                                f"IMAP: Wrong response: {result} message={msg}"
                            )
                    except AttributeError as err:
                        raise ComponentError(
                            f"Login Forbidden, wrong username or password: {err}"
                        ) from err
                else:
                    self._logger.debug("IMAP Basic Login")
                    ## making the server login:
                    r = self.imap_server.login(self.user, self.password)
                    if r.result == "NO":
                        raise ComponentError(
                            f"Login Forbidden, Server Disconnected: {r}"
                        )
                ### Select Mailbox
                self.imap_server.select(self.mailbox, readonly=False)
                # If connection is successful, break out of the loop
                break
            except Exception as exc:
                server = f"{self.host}:{self.port}"
                if attempt == max_retries - 1:
                    raise ComponentError(
                        f"Could not connect to IMAP Server {self.host}:{self.port}: {exc}"
                    ) from exc
                # Otherwise, log the exception and wait before retrying
                self._logger.warning(
                    f"Attempt {attempt + 1} to connect to IMAP {server}: {exc}. Retrying in {delay} sec."
                )
                time.sleep(delay)

    def build_search_criteria(self, search_criteria):
        criteria = []
        for key, value in search_criteria.items():
            if value is None:
                criteria.append(key)
            else:
                criteria.append(f'({key} "{value}")')
        return " ".join(criteria)

    def process_email(self, email_id, **kwargs):
        self._logger.debug(f"Email {email_id} has processed.")
        self.parent.call_actions(**kwargs)

    def run(self, **kwargs):
        try:
            self.connect()
        except ComponentError as exc:
            self._logger.error(
                f"Error connecting to IMAP server: {exc}"
            )
            return
        while not self.stop_event.is_set():
            try:
                search_criteria = self.build_search_criteria(self.search)
                self._logger.debug(f"IMAP: Running Search: {search_criteria}")
                result, data = self.imap_server.search(None, search_criteria)
                if result == "OK":
                    # TODO:
                    emails = data[0].split()
                    unseen_emails = len(emails)
                    self._logger.notice(
                        f"Found {unseen_emails} emails in {self.mailbox}"
                    )
                    for email_id in emails:
                        # Fetch the email's structure
                        status, mail_data = self.imap_server.fetch(
                            email_id, "(BODYSTRUCTURE)"
                        )
                        if status == "OK":
                            with CacheSupport(every=self._expiration) as cache:
                                if cache.exists(email_id):
                                    continue
                                # check if email has attachments:
                                if (
                                    "has_attachments" in self.args and self.args["has_attachments"] is True
                                ):
                                    structure = mail_data[0]
                                    if isinstance(structure, bytes):
                                        structure = structure.decode("utf-8")
                                    # Check if the structure contains a filename parameter
                                    if '("attachment"' in structure:
                                        cache.setexp(email_id, value=structure)
                                        self.process_email(email_id, **kwargs)
                                else:
                                    structure = mail_data[0]
                                    cache.setexp(email_id, value=structure)
                                    self.process_email(email_id, **kwargs)
            except Exception as e:
                print(f"An error occurred while checking the mailbox: {e}")
                # Reconnect if an error occurs
                self.connect()
            # Wait for the interval, but allow the sleep to be interrupted by the signal
            try:
                for _ in range(self.interval):
                    if self.stop_event.is_set():
                        break
                    time.sleep(1)
            except KeyboardInterrupt:
                break


class IMAPWatchdog(BaseWatchdog):
    def processing_search(self, search_terms: dict):
        search = {}
        for key, value in search_terms.items():
            val = self.mask_replacement(value)
            search[key] = val
        return search

    def create_watcher(self, *args, **kwargs) -> BaseWatcher:
        credentials = kwargs.pop("credentials", {})
        self.mailbox = kwargs.pop("mailbox", "INBOX")
        interval = kwargs.pop("interval", 60)
        authmech = credentials.pop("authmech", None)
        self.mask_start(**kwargs)
        search = self.processing_search(kwargs.pop("search", {}))
        # TODO: processing with masks the Search criteria:
        self.credentials = self.set_credentials(credentials)
        return ImapWatcher(
            **self.credentials,
            mailbox=self.mailbox,
            interval=interval,
            authmech=authmech,
            search=search,
            **kwargs,
        )
