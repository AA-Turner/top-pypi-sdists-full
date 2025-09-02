import datetime
import html
from typing import Any, Dict, Optional

from aiohttp import ClientSession

from .baseApi import BaseAPI
from .const import _LOGGER, ENDPOINT_WARNING_DETAIL, ReadOnlyClass
from .label_matcher import LabelMatcher


class Warning(BaseAPI, metaclass=ReadOnlyClass):
    """Class to reflect a warning."""

    def __init__(self, data: Dict[str, Any], session: ClientSession = None):
        """Initialize."""
        super().__init__(session)

        self.id: str = data["payload"]["id"]
        self.headline: str = data["payload"]["data"]["headline"]
        self.severity: str = data["payload"]["data"]["severity"]
        self.description: str = ""
        self.sender: str = ""
        self.affected_areas: list[str] = []
        self.recommended_actions: list[str] = []
        self.web: str = ""
        self.sent: str = data["sent"]
        self.start: Optional[str] = data.get("effective", data.get("onset", None))
        self.expires: Optional[str] = data.get("expires", None)

        self.raw: Dict[str, Any] = data

    def isValid(self) -> bool:
        """Test if warning is valid."""
        if self.expires is not None:
            currDate: datetime = datetime.datetime.now().timestamp()
            expiresDate = datetime.datetime.fromisoformat(self.expires).timestamp()
            return currDate < expiresDate
        return True

    async def getDetails(self, matcher: LabelMatcher = None):
        """Get the details of a warning."""
        _LOGGER.debug(f"Fetch details for {self.id}")

        url: str = ENDPOINT_WARNING_DETAIL + self.id + ".json"
        data = await self._makeRequest(url)

        infos = data["info"][0]

        self.description = html.unescape(infos.get("description", ""))

        if "senderName" in infos:
            self.sender = infos.get("senderName", "")

        if "web" in infos:
            self.web = infos.get("web", "")

        for area in infos.get("area", []):
            self.affected_areas.append(area["areaDesc"])

        recommended_actions_raw: list[str] = []

        for parameter in infos.get("parameter", {}):
            if parameter["valueName"] == "instructionCode":
                recommended_actions_raw = parameter["value"].split(" ")

        if "instruction" in infos:
            self.recommended_actions = [
                infos.get("instruction", "").replace("<br/>", " ")
            ]

        if matcher is not None and len(self.recommended_actions) == 0:
            for code in recommended_actions_raw:
                self.recommended_actions.append(matcher.match(code))

    def __repr__(self) -> str:
        return (
            f"{self.id} ({self.sent}): [{self.sender}, {self.start} - "
            f"{self.expires} ({self.sent})] {self.headline}, {self.description} - {self.web}"
        )
