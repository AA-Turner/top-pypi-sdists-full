from typing import Type, Dict

from spotipyio.logic.contract import BaseManager, ISpotifyComponent
from spotipyio.logic.collectors import ArtistsCollector, ArtistsTopTracksCollector


class ArtistsManager(BaseManager):
    def __init__(self, info: ArtistsCollector, top_tracks: ArtistsTopTracksCollector):
        super().__init__()
        self.info = info
        self.top_tracks = top_tracks

    @staticmethod
    def _components() -> Dict[str, Type[ISpotifyComponent]]:
        return {"info": ArtistsCollector, "top_tracks": ArtistsTopTracksCollector}
