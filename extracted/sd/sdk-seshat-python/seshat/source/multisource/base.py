from typing import Dict

from seshat.data_class import SFrame
from seshat.source import Source


class MultiSource(Source):
    """
    MultiSource is a Source that will save multiple source results in one group sf.

    Attributes:
    -----------
    sources_map : Dict[str, Source]
        A dictionary mapping sf key to Source object. This dictionary is used to save
        source result as a child in final group sf.
    """

    def __init__(self, sources_map: Dict[str, Source], *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.sources_map = sources_map

    def fetch(self, *args, **kwargs) -> SFrame:
        sf = self.data_class().make_group()
        sf.children = {}
        for sf_key, source in self.sources_map.items():
            result = source()
            sf[sf_key] = result
        return sf

    def calculate_complexity(self):
        return sum(
            [source.calculate_complexity() for source in self.sources_map.values()]
        )
