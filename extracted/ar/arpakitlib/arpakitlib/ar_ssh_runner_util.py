# arpakit

from __future__ import annotations

import asyncio
import logging
from datetime import timedelta
from typing import Optional, Any

import asyncssh
import paramiko
from pydantic import BaseModel

from arpakitlib.ar_json_util import transfer_data_to_json_str

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class SSHRunTimeouts:
    fast_command = timedelta(minutes=0, seconds=15).total_seconds()
    medium_command = timedelta(minutes=2, seconds=30).total_seconds()
    long_command = timedelta(minutes=5, seconds=0).total_seconds()


class SSHBaseErr(Exception):
    pass


class SSHCannotConnect(SSHBaseErr):
    pass


class SSHCannotRun(SSHBaseErr):
    pass


class SSHRunResHasErr(SSHBaseErr):

    def __init__(self, ssh_run_res: SSHRunRes):
        self.ssh_run_res = ssh_run_res

    def __repr__(self):
        return f"return_code={self.ssh_run_res.return_code}, stderr={self.ssh_run_res.err.strip()}"

    def __str__(self):
        return f"return_code={self.ssh_run_res.return_code}, stderr={self.ssh_run_res.err.strip()}"


class SSHRunRes(BaseModel):
    out: str
    err: str
    return_code: int | None = None

    def simple_dict(self) -> dict[str, Any]:
        return {
            "out": self.out,
            "err": self.err,
            "return_code": self.return_code,
            "has_bad_return_code": self.has_bad_return_code,
            "has_err": self.has_err
        }

    def simple_json(self) -> str:
        return transfer_data_to_json_str(
            self.simple_dict(),
            beautify=True,
            fast=False
        )

    def __repr__(self) -> str:
        return self.simple_json()

    def __str__(self) -> str:
        return self.simple_json()

    @property
    def has_bad_return_code(self) -> bool:
        if self.return_code is None:
            return False
        return self.return_code != 0

    @property
    def has_err(self) -> bool:
        if self.err:
            return True
        return False

    def raise_for_bad_return_code(self):
        if self.has_bad_return_code:
            raise SSHRunResHasErr(ssh_run_res=self)

    def raise_for_err(self):
        if self.has_err:
            raise SSHRunResHasErr(ssh_run_res=self)


class SSHRunner:

    def __init__(
            self,
            *,
            hostname: str,
            port: int = 22,
            username: str = "root",
            password: Optional[str] = None,
            base_timeout: int = timedelta(seconds=5).total_seconds()
    ):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password

        self.base_timeout = base_timeout

        self._logger = logging.getLogger(
            f"{logging.getLogger(self.__class__.__name__)} - {self.username}@{self.hostname}:{self.port}"
        )

        self.async_conn: Optional[asyncssh.SSHClientConnection] = None

        self.sync_client = paramiko.SSHClient()
        self.sync_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    """SYNC"""

    def sync_connect(self) -> SSHRunner:
        try:
            self.sync_client.connect(
                hostname=self.hostname,
                username=self.username,
                password=self.password,
                port=self.port,
                timeout=self.base_timeout,
                auth_timeout=self.base_timeout,
                banner_timeout=self.base_timeout,
                channel_timeout=self.base_timeout
            )
        except Exception as err:
            raise SSHCannotConnect(err)
        return self

    def sync_check_connection(self):
        self.sync_connect()

    def sync_is_conn_good(self) -> bool:
        try:
            self.sync_check_connection()
        except SSHCannotConnect:
            return False
        return True

    def sync_run(
            self,
            command: str,
            *,
            timeout: float | None = SSHRunTimeouts.medium_command,
            raise_for_bad_return_code: bool = True
    ) -> SSHRunRes:
        if timeout is None:
            timeout = self.base_timeout

        self._logger.info(command)

        self.sync_connect()

        try:
            stdin, stdout, stderr = self.sync_client.exec_command(
                command=command,
                timeout=timeout
            )
            return_code = stdout.channel.recv_exit_status()
            stdout = stdout.read().decode()
            stderr = stderr.read().decode()
        except Exception as err:
            raise SSHCannotRun(err)

        ssh_run_res = SSHRunRes(
            out=stdout,
            err=stderr,
            return_code=return_code
        )
        if raise_for_bad_return_code is True:
            ssh_run_res.raise_for_bad_return_code()

        return ssh_run_res

    def sync_close(self):
        self.sync_client.close()

    """ASYNC SYNC"""

    async def async_connect(self) -> SSHRunner:
        if self.async_conn is None:
            try:
                self.async_conn = await asyncssh.connect(
                    host=self.hostname,
                    username=self.username,
                    password=self.password,
                    port=self.port,
                    connect_timeout=self.base_timeout,
                    known_hosts=None
                )
            except Exception as err:
                raise SSHCannotConnect(err)
        return self

    async def async_check_connection(self):
        await self.async_connect()

    async def async_is_conn_good(self) -> bool:
        try:
            await self.async_check_connection()
        except SSHCannotConnect:
            return False
        return True

    async def async_run(
            self,
            command: str,
            *,
            timeout: float | None = SSHRunTimeouts.medium_command,
            raise_for_bad_return_code: bool = True
    ) -> SSHRunRes:
        if timeout is None:
            timeout = self.base_timeout

        self._logger.info(command)

        await self.async_connect()

        try:
            result: asyncssh.SSHCompletedProcess = await self.async_conn.run(
                command,
                check=False,
                timeout=timeout
            )
        except Exception as err:
            raise SSHCannotRun(err)

        ssh_run_res = SSHRunRes(
            out=result.stdout,
            err=result.stderr,
            return_code=result.returncode
        )
        if raise_for_bad_return_code is True:
            ssh_run_res.raise_for_bad_return_code()

        return ssh_run_res

    def async_close(self):
        if self.async_conn is not None:
            self.async_conn.close()
            self.async_conn = None


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
