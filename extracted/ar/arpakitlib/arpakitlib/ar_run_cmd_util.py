# arpakit

from __future__ import annotations

import subprocess

from pydantic import BaseModel

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class RunCmdResHasErr(Exception):
    pass


class RunCmdRes(BaseModel):
    out: str
    err: str
    return_code: int

    @property
    def has_bad_return_code(self) -> bool:
        return self.return_code != 0

    def raise_for_bad_return_code(self):
        if self.has_bad_return_code is True:
            raise RunCmdResHasErr(f"return_code={self.return_code}, err={self.err}")
        return


def run_cmd(command: str, raise_for_bad_return_code: bool = False) -> RunCmdRes:
    subprocess_res = subprocess.run(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=False)

    res = RunCmdRes(
        out=subprocess_res.stdout.decode(),
        err=subprocess_res.stderr.decode(),
        return_code=subprocess_res.returncode
    )
    if raise_for_bad_return_code is True:
        res.raise_for_bad_return_code()

    return res


def __example():
    pass


if __name__ == '__main__':
    __example()
