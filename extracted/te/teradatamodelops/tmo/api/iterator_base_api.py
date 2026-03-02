import abc

from tmo.api.api_iterator import ApiIterator
from tmo.api.base_api import BaseApi


class IteratorBaseApi(BaseApi):  # noqa
    __metaclass__ = abc.ABCMeta

    def __init__(self, tmo_client=None, iterator_projection=None, show_archived=True):
        super().__init__(tmo_client=tmo_client)

        self.iterator_projection = iterator_projection

        if show_archived:
            self.iterator_func = self.find_all
        else:
            self.iterator_func = self.find_by_archived

    def __iter__(self):
        return ApiIterator(
            api_func=self.iterator_func,
            entities=list(filter(str.strip, self.path.split("/")))[-1],
            projection=self.iterator_projection,
        )

    def __len__(self):
        return self.find_all()["page"]["totalElements"]
