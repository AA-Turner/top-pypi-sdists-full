"""Deterministic project resource and generated Python names."""

import keyword
import re


class ProjectNames:
    """Keep schema aliases and resource directories explicit and safe for source generation."""

    pattern = r"[a-z0-9][a-z0-9-]{0,63}"

    @classmethod
    def project(cls, value: object, source: str) -> str:
        """Require a server-accepted project name and say where a rejected one came from."""
        if not isinstance(value, str) or re.fullmatch(cls.pattern, value) is None:
            raise ValueError(
                f"Invalid project name {value!r} from {source}: use 1-64 lowercase letters, digits and hyphens, "
                "starting with a letter or digit"
            )
        return value

    @staticmethod
    def alias(value: str) -> str:
        """Require one unambiguous snake-case Python module name for a pinned schema alias."""
        if re.fullmatch(r"[a-z][a-z0-9]*(_[a-z][a-z0-9]*)*", value) is None or keyword.iskeyword(value):
            raise ValueError("Dataset aliases must be lowercase snake-case Python identifiers")
        return value
