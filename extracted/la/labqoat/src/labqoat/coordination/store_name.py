"""Names of dicts and queues."""

import re
from typing import ClassVar


class StoreName:
    """A name the service accepts: 1 to 64 letters, digits, dots, underscores or hyphens, starting with one."""

    PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}")

    @staticmethod
    def check(name: str) -> str:
        """Refuse a name the service would refuse, before anything is sent."""
        if not isinstance(name, str) or StoreName.PATTERN.fullmatch(name) is None:
            raise ValueError(
                "A dict or queue name has 1 to 64 letters, digits, dots, underscores or hyphens and starts with a "
                f"letter or digit; got {name!r}"
            )
        return name
