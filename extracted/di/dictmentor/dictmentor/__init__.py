"""Package dictmentor."""

from . import extensions
from .base import DictMentor
from .types import Version

DictMentor = Mentor = DictMentor  # type: ignore
ext = extensions  # pylint: disable=invalid-name


def version() -> Version:
    """Return the version of the package."""
    return '0.2.2'
