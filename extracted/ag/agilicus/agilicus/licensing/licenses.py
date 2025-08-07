from .. import context

from agilicus import agilicus_api

from ..input_helpers import (
    build_updated_model,
    model_from_dict,
    update_org_from_input_or_ctx,
)
from ..input_helpers import strip_none
from ..output.table import (
    column,
    spec_column,
    format_table,
    metadata_column,
    object_subtable,
)

from .formatters import constraint_columns
from ..licensing.product_table_versions import list_product_table_versions


def list_licenses(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    params = strip_none(kwargs)
    query_results = apiclient.licensing_api.list_licenses(**params)
    return query_results.licenses


def add_license(
    ctx, product_table_version, product_name, constraints=None, vars=None, **kwargs
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    spec = agilicus_api.LicenseSpec(
        product_table_version=agilicus_api.ProductTableVersionString(
            product_table_version
        ),
        product_name=agilicus_api.LicensedProductName(product_name),
        **strip_none(kwargs),
    )
    if constraints:
        spec.license_constraints = build_constraints(constraints)
    if vars:
        spec.constraint_variables = build_vars(vars)

    model = agilicus_api.License(spec=spec)

    return apiclient.licensing_api.create_license(model)


def _add_constraint_defaults(**kwargs):
    if "priority" not in kwargs:
        kwargs["priority"] = 0
    return kwargs


def build_constraints(constraints):
    return [
        model_from_dict(
            agilicus_api.LicenseConstraint, _add_constraint_defaults(**constraint)
        )
        for constraint in constraints
    ]


def build_vars(vars):
    return agilicus_api.LicenseConstraintVariables._from_openapi_data(**vars)


def _get_license(ctx, apiclient, license_id, **kwargs):
    return apiclient.licensing_api.get_license(license_id, **kwargs)


def show_license(ctx, license_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return _get_license(ctx, apiclient, license_id, **kwargs)


def delete_license(ctx, license_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return apiclient.licensing_api.delete_license(license_id, **kwargs)


def update_license(
    ctx,
    license_id,
    constraints=None,
    vars=None,
    replace_constraints=None,
    replace_vars=None,
    **kwargs,
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    mapping = _get_license(ctx, apiclient, license_id)

    apply_constraint_and_vars(
        mapping.spec, constraints, vars, replace_constraints, replace_vars
    )

    # check_type=False works around nested types not deserializing correctly
    mapping.spec = build_updated_model(
        agilicus_api.LicenseSpec, mapping.spec, kwargs, check_type=False
    )

    return apiclient.licensing_api.replace_license(license_id, license=mapping)


def apply_constraint_and_vars(obj, constraints, vars, replace_constraints, replace_vars):
    if not constraints:
        constraints = {}
    if not vars:
        vars = {}

    if not replace_constraints:
        constraints = build_constraints(constraints) + (obj.license_constraints or [])
    else:
        constraints = build_constraints(constraints)

    if not replace_vars and obj.constraint_variables:
        vars = obj.constraint_variables.to_dict() | vars
    vars = build_vars(vars)

    obj.license_constraints = constraints
    obj.constraint_variables = vars


def format_licenses(ctx, resources):
    columns = [
        metadata_column("id"),
        spec_column("product_table_version"),
        spec_column("product_name"),
        *constraint_columns(10, column_func=spec_column),
    ]

    return format_table(ctx, resources, columns)


def list_license_details(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs = strip_none(kwargs)

    result = apiclient.licensing_api.list_license_details(**kwargs)
    return result.license_details


def format_license_details(ctx, resources):
    columns = [
        column("org_id"),
        column("license.metadata.id", "license"),
        column("license.spec.product_name", "product_name"),
        column("license.spec.product_table_version", "product_table_version"),
        *constraint_columns(10),
    ]

    return format_table(ctx, resources, columns)


def list_license_evaluation_contexts(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs = strip_none(kwargs)

    result = apiclient.licensing_api.list_license_evaluation_contexts(**kwargs)
    return result.license_evaluation_contexts


def format_license_evaluation_contexts(ctx, resources):
    usage_columns = [
        column("num_resources"),
        column("num_desktops"),
        column("num_applications"),
        column("num_networks"),
        column("num_ssh"),
        column("num_databases"),
        column("num_resource_groups"),
        column("num_fileshares"),
        column("num_launchers"),
        column("num_users"),
        column("num_groups"),
        column("num_orgs"),
        column("num_connectors"),
    ]
    columns = [
        column("org_id"),
        column("subscription_id"),
        object_subtable(
            ctx, "license_evaluation_input.subscription.usage", usage_columns, "usage"
        ),
    ]

    return format_table(ctx, resources, columns)


def get_licensed_product(product_label, product_table):
    if not product_label:
        return None

    product_tokens = product_label.split("-")

    if len(product_tokens) == 1:
        normalized_product_name = "Standard"
    elif len(product_tokens) >= 2:
        # everything but the last, which is the currency
        normalized_product_name = "-".join(product_tokens[:-1])

    for licensed_product in product_table["products"]:
        if (
            str(licensed_product["name"]).casefold()
            == normalized_product_name.casefold()
        ):
            return licensed_product["name"]
    return None


def add_license_to_billing_sub(ctx, bsub, product_name=None, product_table_version=None):
    if bsub.spec.license_id:
        raise Exception("subscription already has a license_id set!")

    product_table = list_product_table_versions(ctx, published=True, limit=1)
    product_version = product_table[0]

    if not product_table_version:
        product_table_version = product_version["spec"]["version"]

    product_table = product_version["spec"].get("product_table")
    if not product_name:
        if not bsub.status.product:
            raise Exception(f"no product for subscription {bsub.metadata.id}")

        product_name = get_licensed_product(
            bsub.status.product.spec.label, product_table
        )
        if not product_name:
            raise Exception(
                "could not find a suitable licensed for product label: "
                f"{bsub.status.product.spec.label}"
            )

    result = add_license(
        ctx,
        product_table_version=str(product_table_version),
        product_name=str(product_name),
    )
    bsub.spec.license_id = result.metadata.id
