from typing import Dict

from aiohttp import ClientSession

from .const import ReadOnlyClass, ENDPOINT_DE_LABELS
from .baseApi import BaseAPI


class LabelMatcher(BaseAPI, metaclass=ReadOnlyClass):
    """Class to fetch and match labels with their codes."""

    def __init__(self, session: ClientSession = None):
        """Initialize."""
        super().__init__(session)
        self.labels: Dict[str, str] = {}

    async def update(self) -> None:
        """Update the labels."""
        self.labels = await self._makeRequest(ENDPOINT_DE_LABELS)

    def match(self, code: str) -> str:
        """Match a code to a label."""
        return self.labels.get(code, code)
