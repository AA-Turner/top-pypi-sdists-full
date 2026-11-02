"""Harbor's users as the numeric identities the sandbox protocol accepts."""

import re
from collections.abc import Sequence
from typing import ClassVar

from labqoat.sandbox.sandbox import Sandbox
from labqoat.sandbox.sandbox_file_not_found_error import SandboxFileNotFoundError


class SandboxUsers:
    """Resolve a user name or number against the sandbox's own account file, once per user.

    Harbor names users as a task image does (``agent``, ``root``, ``1000``); the sandbox host takes only
    ``uid`` or ``uid:gid``. As with a container runtime, a user the image knows runs with its primary group,
    and a number the image does not know is passed through unchanged.
    """

    ACCOUNTS: ClassVar[str] = "/etc/passwd"

    def __init__(self, sandbox: Sandbox) -> None:
        """Remember resolved users for one sandbox without reading anything yet."""
        self._sandbox = sandbox
        self._resolved: dict[str, str] = {}

    async def resolve(self, user: str | int | None) -> str | None:
        """Return ``uid:gid`` for a user the image knows, an unknown number as given, and nothing for no user."""
        if user is None:
            return None
        name = str(user)
        if re.fullmatch(r"[0-9]+:[0-9]+", name):
            return name
        if name not in self._resolved:
            self._resolved[name] = self._identity(name, await self._accounts())
        return self._resolved[name]

    async def _accounts(self) -> list[list[str]]:
        """Read the well-formed rows of the account file; an image without one knows no users."""
        try:
            content = await self._sandbox.read_file_async(self.ACCOUNTS)
        except SandboxFileNotFoundError:
            return []
        rows = (line.split(":") for line in content.decode(errors="replace").splitlines())
        return [row for row in rows if len(row) >= 4 and all(re.fullmatch(r"[0-9]+", number) for number in row[2:4])]

    @staticmethod
    def _identity(user: str, accounts: Sequence[Sequence[str]]) -> str:
        """Match a number against account uids and anything else against account names."""
        numeric = re.fullmatch(r"[0-9]+", user) is not None
        account = next((row for row in accounts if row[2 if numeric else 0] == user), None)
        if account is not None:
            return f"{account[2]}:{account[3]}"
        if numeric:
            return user
        raise ValueError(f"User {user!r} has no account in the sandbox image")
