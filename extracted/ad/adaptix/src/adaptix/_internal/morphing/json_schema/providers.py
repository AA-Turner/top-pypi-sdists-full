from ...provider.essential import CannotProvide, Mediator
from ...provider.located_request import LocatedRequestMethodsProvider
from ...provider.methods_provider import method_handler
from ...utils import Omitted, SingletonMeta
from ..provider_template import JSONSchemaProvider
from .definitions import JSONSchema, LocalRefSource
from .patch import JSONSchemaPatch
from .request_cls import InlineJSONSchemaRequest, JSONSchemaRequest, RefSourceRequest


class ConstantInlineJSONSchemaProvider(LocatedRequestMethodsProvider):
    def __init__(self, *, inline: bool):
        self._inline = inline

    @method_handler
    def provide_inline_json_schema(self, mediator: Mediator, request: InlineJSONSchemaRequest) -> bool:
        return self._inline


class BuiltinInlineJSONSchemaProvider(LocatedRequestMethodsProvider):
    @method_handler
    def provide_inline_json_schema(self, mediator: Mediator, request: InlineJSONSchemaRequest) -> bool:
        return request.json_schema.properties == Omitted() and request.json_schema.prefix_items == Omitted()


class JSONSchemaRefProvider(LocatedRequestMethodsProvider):
    @method_handler
    def provide_ref_source(self, mediator: Mediator, request: RefSourceRequest) -> LocalRefSource:
        return LocalRefSource(
            value=None,
            json_schema=request.json_schema,
            loc_stack=request.loc_stack,
        )


class ConstantJSONSchemaRefProvider(LocatedRequestMethodsProvider):
    def __init__(self, ref: str):
        self._ref = ref

    @method_handler
    def provide_ref_source(self, mediator: Mediator, request: RefSourceRequest) -> LocalRefSource:
        return LocalRefSource(
            value=self._ref,
            json_schema=request.json_schema,
            loc_stack=request.loc_stack,
        )


class KeepJSONSchema(metaclass=SingletonMeta):
    pass


class EraseJSONSchema(metaclass=SingletonMeta):
    pass


JSONSchemaOverride = JSONSchema | KeepJSONSchema | EraseJSONSchema | JSONSchemaPatch


class JSONSchemaOverrideProvider(JSONSchemaProvider):
    def __init__(self, override: JSONSchemaOverride):
        self._override = override

    def provide_json_schema(self, mediator: Mediator, request: JSONSchemaRequest) -> JSONSchema:
        if isinstance(self._override, JSONSchema):
            return self._override
        if isinstance(self._override, JSONSchemaPatch):
            json_schema = mediator.provide_from_next()
            for patcher in self._override.get_patchers():
                json_schema = patcher(json_schema)
            return json_schema
        if self._override == KeepJSONSchema():
            return mediator.provide_from_next()
        if self._override == EraseJSONSchema():
            raise CannotProvide(
                "JSON Schema is erased",
                is_terminal=True,
                is_demonstrative=True,
            )
        raise ValueError

