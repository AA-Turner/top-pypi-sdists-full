from typing import Type, Dict

from spotipyio.logic.contract import BaseManager, ISpotifyComponent
from spotipyio.logic.collectors import CurrentProfileCollector, TopItemsCollector


class CurrentUserManager(BaseManager):
    def __init__(self, top_items: TopItemsCollector, profile: CurrentProfileCollector):
        super().__init__()
        self.top_items = top_items
        self.profile = profile

    @staticmethod
    def _components() -> Dict[str, Type[ISpotifyComponent]]:
        return {"top_items": TopItemsCollector, "profile": CurrentProfileCollector}
