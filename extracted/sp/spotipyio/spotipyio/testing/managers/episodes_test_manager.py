from typing import Dict, Type

from spotipyio.testing.components import EpisodesInfoTestComponent
from spotipyio.testing.infra import BaseTestManager, BaseTestComponent


class EpisodesTestManager(BaseTestManager):
    def __init__(self, info: EpisodesInfoTestComponent):
        super().__init__()
        self.info = info

    @staticmethod
    def _components() -> Dict[str, Type[BaseTestComponent]]:
        return {
            "info": EpisodesInfoTestComponent,
        }
