from typing import Type, Dict

from spotipyio.logic.collectors import TracksCollector, AudioFeaturesCollector
from spotipyio.logic.contract import BaseManager, ISpotifyComponent


class TracksManager(BaseManager):
    def __init__(self, info: TracksCollector, audio_features: AudioFeaturesCollector):
        super().__init__()
        self.info = info
        self.audio_features = audio_features

    @staticmethod
    def _components() -> Dict[str, Type[ISpotifyComponent]]:
        return {"info": TracksCollector, "audio_features": AudioFeaturesCollector}
