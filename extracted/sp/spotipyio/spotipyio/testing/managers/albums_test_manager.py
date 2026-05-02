from typing import Dict, Type

from spotipyio.testing.components import AlbumsInfoTestComponent
from spotipyio.testing.infra import BaseTestManager, BaseTestComponent


class AlbumsTestManager(BaseTestManager):
    def __init__(self, info: AlbumsInfoTestComponent):
        super().__init__()
        self.info = info

    @staticmethod
    def _components() -> Dict[str, Type[BaseTestComponent]]:
        return {
            "info": AlbumsInfoTestComponent,
        }
