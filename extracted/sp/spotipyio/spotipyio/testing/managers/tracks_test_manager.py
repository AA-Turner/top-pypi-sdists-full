from typing import Dict, Type

from spotipyio.testing.components import TracksInfoTestComponent, TracksAudioFeaturesTestComponent
from spotipyio.testing.infra import BaseTestManager, BaseTestComponent


class TracksTestManager(BaseTestManager):
    def __init__(self, audio_features: TracksAudioFeaturesTestComponent, info: TracksInfoTestComponent):
        super().__init__()
        self.audio_features = audio_features
        self.info = info

    @staticmethod
    def _components() -> Dict[str, Type[BaseTestComponent]]:
        return {
            "audio_features": TracksAudioFeaturesTestComponent,
            "info": TracksInfoTestComponent,
        }
