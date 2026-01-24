# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.utils.patch_utils import (
    build_and_apply_patch,
    wrap_and_watermark,
    register_module_patcher,
)


# TODO: PYT-3819 this patch is not currently being applied; uncomment the lines in
# patches/__init__.py to apply it
def build_graphene_schema_init_patch(orig_func, _):
    def schema_init_patch(wrapped, instance, args, kwargs):
        result = wrapped(*args, **kwargs)
        assert result is None

        schema = instance

        _ = discover_graphene_routes(schema.graphql_schema.query_type)
        _ = discover_graphene_routes(schema.graphql_schema.mutation_type)

        return result

    return wrap_and_watermark(orig_func, schema_init_patch)


def discover_graphene_routes(query_or_mutation_obj):
    # TODO: PYT-3819 This is just a placeholder to demonstrate some of the introspection
    # operations we can perform on a graphql-core query/mutation object. The actual
    # implementation here will need to change considerably for route discovery to work
    # correctly.
    if not query_or_mutation_obj:
        return {}

    routes = {}
    for name, field in query_or_mutation_obj.fields.items():
        routes[name] = {
            "type": field.type,
            "args": {k: v.type for k, v in field.args.items()},
            # NOTE: `resolve` might not work for special cases like __schema, __type, __typename
            "resolver": field.resolve,
        }

    return routes


def patch_graphene(graphene_module):
    build_and_apply_patch(
        graphene_module.Schema,
        "__init__",
        build_graphene_schema_init_patch,
    )


def register_patches():
    register_module_patcher(patch_graphene, "graphene")
