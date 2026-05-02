"""
FTP Client.

Overview

This class provides functionalities for asynchronous operations with an FTP server, including establishing connections,
checking directory existence, changing working directories, and downloading files.

"""
from typing import List, Dict
from collections.abc import Callable
import aioftp
from ..exceptions import ComponentError
from .client import ClientInterface


"""
FOR FTP over SSL

from ftplib import FTP_TLS

ftps = FTP_TLS(timeout=10)
ftps.set_debuglevel(2)
ftps.context.set_ciphers('DEFAULT@SECLEVEL=1')

ftps.connect(host, port)

ftps.login('user', 'password')
# enable TLS
ftps.auth()
ftps.prot_p()
ftps.retrlines('LIST')
"""


class FTPClient(ClientInterface):
    block_size = 8192
    algorithms: List = [
        "ssh-rsa",
        "ssh-dss",
        "sk-ssh-ed25519-cert-v01@openssh.com",
        "sk-ecdsa-sha2-nistp256-cert-v01@openssh.com",
        "ssh-ed25519-cert-v01@openssh.com",
        "ssh-ed448-cert-v01@openssh.com",
        "ecdsa-sha2-nistp521-cert-v01@openssh.com",
        "ecdsa-sha2-nistp384-cert-v01@openssh.com",
        "ecdsa-sha2-nistp256-cert-v01@openssh.com",
        "ecdsa-sha2-1.3.132.0.10-cert-v01@openssh.com",
        "ssh-rsa-cert-v01@openssh.com",
        "ssh-dss-cert-v01@openssh.com",
        "sk-ssh-ed25519@openssh.com",
        "sk-ecdsa-sha2-nistp256@openssh.com",
        "ssh-ed25519",
        "ssh-ed448",
        "ecdsa-sha2-nistp521",
        "ecdsa-sha2-nistp384",
        "ecdsa-sha2-nistp256",
        "ecdsa-sha2-1.3.132.0.10",
        "rsa-sha2-256",
        "rsa-sha2-512",
    ]

    async def close(self):
        """Close Method."""
        try:
            await self._connection.quit()
        except Exception as err:
            print(f"Error on FTP disconnection, reason: {err!s}")

    async def init_connection(
        self, host, port, credentials: Dict, ssl: Callable = None
    ):
        """
        init an FTP connection
        """
        args = {
            "socket_timeout": 120,
            "path_timeout": 30,
            "encoding": "utf-8",
            "ssl": ssl,
        }
        connection = None
        try:
            connection = aioftp.Client(**args)
            await connection.connect(host, port)
        except ValueError as err:
            raise ComponentError(f"{err!s}") from err
        except OSError as err:
            raise ComponentError(f"FTP connection failed: {err!s}") from err
        except Exception as err:
            raise ComponentError(f"FTP Exception: {err!s}") from err
        try:
            await connection.login(*credentials.values())
            return connection
        except aioftp.StatusCodeError as err:
            raise ComponentError(f"FTP connection Error: {err!s}") from err
        except Exception as err:
            raise ComponentError(f"FTP Exception: {err!s}") from err

    def err_handler(self, err):
        print(f"FTP Error: reason: {err.reason}, error: {err}")
        return False

    async def directory_exists(self, directory: str):
        return await self._connection.exists(directory)

    async def change_directory(self, directory: str):
        await self._connection.change_directory(directory)

    async def open(self):
        pass

    async def download_file(self, file: str, destination: str, rewrite: bool = False):
        """download_file

        Download a File from FTP based on Path.
        Args:
            file (str): file to be downloaded
            destination (str): path to destination
            rewrite (bool): file if exists, will be overwrite
        TODO: Support for write_into and Renaming Files.
        """
        try:
            await self._connection.download(
                file,
                destination=destination,
                write_into=rewrite,
                block_size=self.block_size,
            )
        except Exception as err:
            raise ComponentError(f"FTP Download Exception: {err!s}") from err
