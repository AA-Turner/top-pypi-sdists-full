from spotipyio.logic.contract import ISpotifyComponent


class CurrentProfileCollector(ISpotifyComponent):
    async def run(self):
        return await self._session.get(url=self._url)

    @property
    def _url(self) -> str:
        return f"{self._base_url}/me"
