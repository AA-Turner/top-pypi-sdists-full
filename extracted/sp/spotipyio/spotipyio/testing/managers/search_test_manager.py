from typing import Dict, Type

from spotipyio.testing.components import SearchItemTestComponent
from spotipyio.testing.infra import BaseTestManager, BaseTestComponent


class SearchTestManager(BaseTestManager):
    def __init__(self, search_item: SearchItemTestComponent):
        super().__init__()
        self.search_item = search_item

    @staticmethod
    def _components() -> Dict[str, Type[BaseTestComponent]]:
        return {
            "search_item": SearchItemTestComponent,
        }
