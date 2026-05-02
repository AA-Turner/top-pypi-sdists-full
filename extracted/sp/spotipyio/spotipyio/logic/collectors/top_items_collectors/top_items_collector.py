from spotipyio.logic.consts.spotify_consts import TIME_RANGE, LIMIT
from spotipyio.logic.contract import ISpotifyComponent
from spotipyio.models import ItemsType, TimeRange


class TopItemsCollector(ISpotifyComponent):
    async def run(self, items_type: ItemsType, time_range: TimeRange, limit: int = 50) -> dict:
        """
        Get the current user's top artists or tracks based on calculated affinity.

        Args:
            items_type (ItemsType):
                The type of entity to return.
                Valid values:
                    - ItemsType.ARTISTS
                    - ItemsType.TRACKS
            time_range (TimeRange):
                Over what time frame the affinities are computed.
                Valid values:
                    - TimeRange.LONG_TERM: Approximately 1 year of data.
                    - TimeRange.MEDIUM_TERM: Approximately the last 6 months (default).
                    - TimeRange.SHORT_TERM: Approximately the last 4 weeks.
            limit (int):
                The maximum number of items to return. Default is 50.
                    - Minimum: 1
                    - Maximum: 50

        Returns:
            dict: A dictionary containing the user's top artists or tracks.

        Raises:
            ClientResponseError

        Examples:
        ```
        from spotipyio import SpotifySession, SpotifyClient
        from spotipyio.auth import ClientCredentials, SpotifyGrantType
        from spotipyio.models import ItemsType, TimeRange
        import asyncio

        async def fetch_current_user_top_artists(access_code: str):
            credentials = ClientCredentials(
                grant_type=SpotifyGrantType.AUTHORIZATION_CODE,
                access_code=access_code
            )

            async with SpotifySession(credentials=credentials) as session:
                async with SpotifyClient(session=session) as client:
                    top_items = await client.current_user.top_items.run(
                        items_type=ItemsType.ARTISTS,
                        time_range=TimeRange.SHORT_TERM
                    )

            print(top_items)

        if __name__ == '__main__':
            loop = asyncio.get_event_loop()
            loop.run_until_complete(fetch_current_user_top_artists("<your-access-code>"))
        ```
        """
        url = self._url_format.format(items_type=items_type.value)
        params = {TIME_RANGE: time_range.value, LIMIT: limit}

        return await self._session.get(url=url, params=params)

    @property
    def _url_format(self) -> str:
        return f"{self._base_url}/me/top/{{items_type}}"
