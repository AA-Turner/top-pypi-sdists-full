from cnvrgv2 import cnvrg
from cnvrgv2.config import error_messages, routes
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.modules.labels.label import Label
from cnvrgv2.modules.labels.utils import LabelColor, LabelKind, validate_labels_params
from cnvrgv2.proxy import HTTP, Proxy
from cnvrgv2.utils.api_list_generator import api_list_generator
from cnvrgv2.utils.json_api_format import JAF


class LabelsClient:
    def __init__(self, organization) -> None:
        if type(organization) is not cnvrg.Cnvrg:
            raise CnvrgArgumentsError(error_messages.ARGUMENT_BAD_TYPE.format(cnvrg.Cnvrg, type(organization)))

        self._context = Context(context=organization._context)
        scope = self._context.get_scope(SCOPE.ORGANIZATION)

        self._scope = scope
        self._proxy = Proxy(context=self._context)
        self._route = routes.LABELS_BASE.format(scope["organization"])

    def list(self, kind, filter=None):
        """
        List all Labels in a specific organization
        @param sort: key to sort the list by (-key -> DESC | key -> ASC)
        @raise: HttpError
        @return: Generator that yields labels objects
        """
        if not LabelKind.validate(kind):
            raise CnvrgArgumentsError(error_messages.LABEL_BAD_KIND)

        def label_builder(item):
            attributes = item.attributes
            attributes['id'] = item.id
            return Label(self._context, name=item.attributes['name'], kind=item.attributes['kind'], attributes=item.attributes)

        res = api_list_generator(
            context=self._context,
            route=self._route,
            object_builder=label_builder,
            identifier='name',
            filter=filter,
            data={'kind': kind},
        )

        return res

    def create(self, name, kind, color_name=LabelColor.BLUE):
        """
        Create a new label
        @param name: [String] The label name
        @param kind: [String] The kind of the tag, either 'projects' or 'datasets' are available.
        @param color_name: [String] The name of the color from the available colors list
        @raise CnvrgHttpError: if label already exists.
        @return: [Label object] The newly created label
        """
        validate_labels_params(name, kind, color_name)

        attributes = {
            "name": name,
            "kind": kind,
            "color_name": color_name,
        }
        response = self._proxy.call_api(
            route=self._route,
            http_method=HTTP.POST,
            payload=JAF.serialize(type="label", attributes=attributes)
        )

        name = response.attributes['name']
        kind = response.attributes['kind']
        return Label(self._context, name=name, kind=kind, attributes=response.attributes)

    def get(self, name, kind):
        """
        Retrieves a Label by the given name
        @param name: [String] The name of the label
        @return: Image object
        """
        validate_labels_params(name, kind)
        filter = {"operator": "AND", "conditions": [{"key": "name", "operator": "is", "value": name}]}
        generator = self.list(kind=kind, filter=filter)
        try:
            label = next(generator)
            return label
        except StopIteration:
            raise CnvrgArgumentsError(error_messages.LABEL_NOT_FOUND)
