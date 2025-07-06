from cnvrgv2.proxy import Proxy, HTTP
from cnvrgv2.context import Context
from cnvrgv2.utils.api_list_generator import api_list_generator
from cnvrgv2.modules.labels.label import Label
from cnvrgv2.utils.json_api_format import JAF


class DataownerLabelsClient:
    def __init__(self, dataowner):
        self.dataowner = dataowner
        self._context = Context(context=dataowner._context)
        self._proxy = Proxy(context=self._context)

    def list(self, sort="-id"):
        """
        List all labels in a specific project/dataset
        @param sort: key to sort the list by (-key -> DESC | key -> ASC)
        @raise: HttpError
        @return: Generator that yields label objects
        """
        def label_builder(item):
            attributes = item.attributes
            attributes['id'] = item.id
            return Label(self._context, name=item.attributes['name'], kind=item.attributes['kind'], attributes=item.attributes)

        return api_list_generator(
            context=self._context,
            route=self._route,
            object_builder=label_builder,
            identifier='name',
            data={'kind': self.kind},
        )

    def remove(self):
        """
        Remove label from a specific project/dataset
        """
        self._proxy.call_api(route=self._route, http_method=HTTP.DELETE)

    def add(self, label):
        """
        Add label to a specific project/dataset
        """
        attributes = {
            "slug": self.dataowner.slug,
            "labels": [label.name],
        }

        self._proxy.call_api(
            route=self._route,
            http_method=HTTP.POST,
            payload=JAF.serialize(type="label", attributes=attributes)
        )
