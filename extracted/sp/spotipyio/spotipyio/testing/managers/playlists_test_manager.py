from typing import Type, Dict

from spotipyio.testing.components import (
    PlaylistsCreatorTestComponent,
    PlaylistsInfoTestComponent,
    PlaylistItemsAdderTestComponent,
    PlaylistsItemsRemoverTestComponent,
    PlaylistsCoverUpdaterTestComponent,
    PlaylistItemsReplacerTestComponent,
)
from spotipyio.testing.components.playlists import PlaylistItemsReorderTestComponent
from spotipyio.testing.infra import BaseTestManager, BaseTestComponent


class PlaylistsTestManager(BaseTestManager):
    def __init__(
        self,
        add_items: PlaylistItemsAdderTestComponent,
        create: PlaylistsCreatorTestComponent,
        info: PlaylistsInfoTestComponent,
        remove_items: PlaylistsItemsRemoverTestComponent,
        reorder_items: PlaylistItemsReorderTestComponent,
        replace_items: PlaylistItemsReplacerTestComponent,
        update_cover: PlaylistsCoverUpdaterTestComponent,
    ):
        super().__init__()
        self.add_items = add_items
        self.create = create
        self.info = info
        self.remove_items = remove_items
        self.reorder_items = reorder_items
        self.replace_items = replace_items
        self.update_cover = update_cover

    @staticmethod
    def _components() -> Dict[str, Type[BaseTestComponent]]:
        return {
            "add_items": PlaylistItemsAdderTestComponent,
            "create": PlaylistsCreatorTestComponent,
            "info": PlaylistsInfoTestComponent,
            "remove_items": PlaylistsItemsRemoverTestComponent,
            "reorder_items": PlaylistItemsReorderTestComponent,
            "replace_items": PlaylistItemsReplacerTestComponent,
            "update_cover": PlaylistsCoverUpdaterTestComponent,
        }
