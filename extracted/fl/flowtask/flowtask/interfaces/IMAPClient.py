"""
IMAP/POP Client.

Class for operations with IMAP Mailboxes.

"""
import socket
import asyncio
import ssl
from collections.abc import Callable
import imaplib
from ..exceptions import ComponentError
from .client import ClientInterface
from .azureauth import AzureAuth
from ..conf import IMAP_RETRY_AUTH, IMAP_RETRY_AUTH_BACKOFF


class IMAPClient(ClientInterface):
    """
    IMAPClient

    Overview

        The IMAPClient class provides operations for interacting with IMAP mailboxes.
        It supports both SSL and non-SSL
        connections and uses XOAUTH2 authentication by default.

    .. table:: Properties
    :widths: auto

        +------------------+----------+------------------------------------------------------------------------------------------+
        | Name             | Required | Description                                                                              |
        +------------------+----------+------------------------------------------------------------------------------------------+
        | use_ssl          |   No     | Boolean flag to specify whether to use SSL, defaults to True.                            |
        +------------------+----------+------------------------------------------------------------------------------------------+
        | mailbox          |   No     | The mailbox to access, defaults to "Inbox".                                              |
        +------------------+----------+------------------------------------------------------------------------------------------+
        | overwrite        |   No     | Boolean flag to specify whether to overwrite existing configurations, defaults to False. |
        +------------------+----------+------------------------------------------------------------------------------------------+

    Return

        The methods in this class manage the connection to the IMAP server and perform authentication and closure of
        the connection.

    """  # noqa

    _credentials: dict = {"user": str, "password": str}
    authmech: str = "XOAUTH2"
    use_ssl = True

    def __init__(
        self, *args, host: str = None, port: str = None, **kwargs
    ) -> None:
        self._connected: bool = False
        self._client: Callable = None
        self.use_ssl: bool = kwargs.pop("use_ssl", True)
        self.mailbox: str = kwargs.pop('mailbox', "Inbox")
        self.overwrite: bool = kwargs.pop('overwrite', False)
        self._sslcontext = ssl.create_default_context()
        self._sslcontext.minimum_version = ssl.TLSVersion.TLSv1_2
        self._sslcontext.check_hostname = False
        self._sslcontext.verify_mode = ssl.CERT_NONE
        self._client: Callable = None
        self._timeout = kwargs.get('timeout', 20)
        super(IMAPClient, self).__init__(*args, host=host, port=port, **kwargs)
        if "use_ssl" in self.credentials:
            self.use_ssl = self.credentials["use_ssl"]
            del self.credentials["use_ssl"]

    async def open(self, host: str, port: int, credentials: dict, **kwargs):
        try:
            if self.use_ssl:
                self._client = imaplib.IMAP4_SSL(
                    host, port, timeout=10, ssl_context=self._sslcontext
                )
            else:
                self._client = imaplib.IMAP4(host, port, timeout=10)
        except socket.error as e:
            raise ComponentError(f"Socket Error: {e}") from e
        except ValueError as ex:
            print("IMAP err", ex)
            raise RuntimeError(f"IMAP Invalid parameters or credentials: {ex}") from ex
        except Exception as ex:
            print("IMAP err", ex)
            self._logger.error(
                f"Error connecting to server: {ex}"
            )
            raise ComponentError(
                f"Error connecting to server: {ex}"
            ) from ex
        # start the connection
        try:
            # disable debug:
            self._client.debug = 0
        except Exception:
            pass
        try:
            await asyncio.sleep(0.5)
            self._client.timeout = 20
            if self.authmech is not None:
                last_exc = None
                for attempt in range(IMAP_RETRY_AUTH):
                    try:
                        # build an Auth token via Azure and authenticate
                        azure = AzureAuth()  # default values
                        result, msg = self._client.authenticate(
                            self.authmech,
                            lambda x: azure.binary_token(
                                credentials["user"], credentials["password"]
                            ),
                        )
                        print("RESULT ", result, msg)
                        if result == "OK":
                            self._connected = True
                            return self._connected
                        raise ComponentError(
                            f"IMAP: Wrong response from Server {msg}"
                        )
                    except Exception as err:
                        last_exc = err
                        self._logger.warning(
                            "IMAP: AzureAuth authenticate failed (attempt %s/%s): %s",
                            attempt + 1,
                            IMAP_RETRY_AUTH,
                            err,
                        )
                        if attempt < (IMAP_RETRY_AUTH - 1):
                            await asyncio.sleep(IMAP_RETRY_AUTH_BACKOFF * (attempt + 1))
                            continue
                        break
                raise ComponentError(
                    f"IMAP: AzureAuth failed after {IMAP_RETRY_AUTH} attempts: {last_exc}"
                ) from last_exc
            else:
                # using default authentication
                r = self._client.login(credentials["user"], credentials["password"])
                if r.result != "NO":
                    self._connected = True
                    return self._connected
                else:
                    raise ComponentError(f"IMAP: Wrong response from Server {r.result}")
        except AttributeError as err:
            raise ComponentError(
                f"Login Forbidden, wrong username or password: {err}"
            ) from err
        except Exception as err:
            raise ComponentError(f"Error connecting to server: {err}") from err

    async def close(self, timeout: int = 5):
        try:
            if self._client:
                self._client.close()
                self._client.logout()
                self._connected = False
        except imaplib.IMAP4.abort as err:
            self._logger.warning(err)
