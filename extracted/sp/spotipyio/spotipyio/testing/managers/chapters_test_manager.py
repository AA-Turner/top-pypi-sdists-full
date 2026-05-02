from typing import Dict, Type

from spotipyio.testing.components import ChaptersInfoTestComponent
from spotipyio.testing.infra import BaseTestManager, BaseTestComponent


class ChaptersTestManager(BaseTestManager):
    def __init__(self, info: ChaptersInfoTestComponent):
        super().__init__()
        self.info = info

    @staticmethod
    def _components() -> Dict[str, Type[BaseTestComponent]]:
        return {
            "info": ChaptersInfoTestComponent,
        }
