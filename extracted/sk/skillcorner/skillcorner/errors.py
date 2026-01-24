import re
from dataclasses import asdict, dataclass


@dataclass
class SkillcornerRuntimeError(RuntimeError):
    """Base Skillcorner runtime error."""

    def __str__(self) -> str:
        return str(self.dump())

    def dump(self) -> dict:
        message = re.sub(r'\s+', ' ', self.__doc__ or '').strip()
        return {'message': message} | asdict(self)


@dataclass
class InfinitePaginationError(SkillcornerRuntimeError):
    """
    Triggered when the current page has already been requested during the pagination loop,
    resulting in the client being trapped in an infinite loop.
    """

    url_stack: list[str]
