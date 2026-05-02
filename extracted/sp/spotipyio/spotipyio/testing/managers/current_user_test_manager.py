from typing import Type, Dict

from spotipyio.testing.components import TopItemsTestComponent, CurrentProfileTestComponent
from spotipyio.testing.infra import BaseTestManager, BaseTestComponent


class CurrentUserTestManager(BaseTestManager):
    def __init__(self, top_items: TopItemsTestComponent, profile: CurrentProfileTestComponent):
        super().__init__()
        self.top_items = top_items
        self.profile = profile

    @staticmethod
    def _components() -> Dict[str, Type[BaseTestComponent]]:
        return {
            "top_items": TopItemsTestComponent,
            "profile": CurrentProfileTestComponent,
        }
