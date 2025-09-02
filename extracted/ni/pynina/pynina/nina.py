from typing import Dict, Any

from aiohttp import ClientSession

from .const import (
    ReadOnlyClass,
    ENDPOINT_REGIONAL_CODE,
    ENDPOINT_NINA_BASE,
    CITY_STATES_CODE,
    COUNTIES,
    _LOGGER,
)
from .baseApi import BaseAPI
from .warning import Warning
from .label_matcher import LabelMatcher


class Nina(BaseAPI, metaclass=ReadOnlyClass):
    """Main class to interact with the NINA API"""

    def __init__(self, session: ClientSession = None):
        """Initialize."""
        super().__init__(session)
        self.warnings: Dict[str, list[Any]] = {}
        self.regions: list = []
        self.matcher: LabelMatcher = LabelMatcher(session)

    def addRegion(self, regionCode: str):
        """Add a region to monitor."""
        if regionCode not in self.regions:
            self.regions.append(regionCode)

    async def update(self):
        """Update the warnings."""
        if not len(self.matcher.labels):
            await self.matcher.update()

        self.warnings.clear()

        for regionCode in self.regions:
            _LOGGER.debug(f"Update region: {regionCode}")
            url: str = ENDPOINT_NINA_BASE + regionCode + ".json"
            data = await self._makeRequest(url)

            self.warnings[regionCode] = []

            for warn in data:
                warning: Warning = Warning(warn)
                await warning.getDetails(self.matcher)
                self.warnings[regionCode].append(warning)

    async def getAllRegionalCodes(self) -> Dict[str, str]:
        """Fetch all regional codes."""
        _LOGGER.debug("Get all regional codes")
        rawCodeData: Dict[str, Any] = await self._makeRequest(ENDPOINT_REGIONAL_CODE)

        regionalCodes: Dict[str, str] = {}
        for dataBlock in rawCodeData["daten"]:
            id: str = dataBlock[0]
            name: str = dataBlock[1]

            if id[:5] in COUNTIES:
                name = f"{name} ({COUNTIES[id[:5]]})"

            if id[:2] not in CITY_STATES_CODE:
                id = id[: len(id) - 7] + "0000000"
                regionalCodes[name] = id

            if id[:2] in CITY_STATES_CODE and id[:2] + "0" * 10 == id:
                regionalCodes[name] = id

        return regionalCodes
