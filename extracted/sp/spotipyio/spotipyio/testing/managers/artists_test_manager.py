from typing import Dict, Type

from spotipyio.testing.components import ArtistsInfoTestComponent, ArtistsTopTracksTestComponent
from spotipyio.testing.infra import BaseTestManager, BaseTestComponent


class ArtistsTestManager(BaseTestManager):
    def __init__(self, info: ArtistsInfoTestComponent, top_tracks: ArtistsTopTracksTestComponent):
        super().__init__()
        self.info = info
        self.top_tracks = top_tracks

    @staticmethod
    def _components() -> Dict[str, Type[BaseTestComponent]]:
        return {"info": ArtistsInfoTestComponent, "top_tracks": ArtistsTopTracksTestComponent}
