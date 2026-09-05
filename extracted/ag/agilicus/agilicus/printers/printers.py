from .. import context
from agilicus.agilicus_api import (
    Printer,
    PrinterSpec,
    PrinterClientConfig,
    PrinterWindowsConfig,
    K8sSlug,
)

from ..input_helpers import build_updated_model_validate, strip_none
from ..input_helpers import update_org_from_input_or_ctx
from ..output.table import (
    spec_column,
    status_column,
    format_table,
    metadata_column,
)
from ..pagination import normalize_page_args
from ..resource_helpers import map_resource_published, standard_page_fields

page_fields = standard_page_fields


def list_printers(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs = strip_none(kwargs)
    kwargs = normalize_page_args(kwargs)
    query_results = apiclient.app_services_api.list_printers(**kwargs)
    return query_results.printers


def add_printer(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs = strip_none(kwargs)

    driver_name = kwargs.pop("driver_name", None)
    if driver_name:
        # The ORM exposes a top-level driver_name on the printer spec; the
        # client_config.windows_config.driver_name is used for launcher-side
        # configuration. Set both so the overview's driver column is populated.
        kwargs["driver_name"] = driver_name
        kwargs["client_config"] = PrinterClientConfig(
            windows_config=PrinterWindowsConfig(driver_name=driver_name),
            _configuration=context.get_api_config(),
        )

    spec = PrinterSpec(
        **kwargs,
        _configuration=context.get_api_config(),
    )
    model = Printer(
        spec=spec,
        _configuration=context.get_api_config(),
    )

    return apiclient.app_services_api.create_printer(model).to_dict()


def _get_printer(ctx, apiclient, printer_id, **kwargs):
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs = strip_none(kwargs)
    return apiclient.app_services_api.get_printer(printer_id, **kwargs)


def show_printer(ctx, printer_id, **kwargs):
    kwargs = strip_none(kwargs)
    apiclient = context.get_apiclient_from_ctx(ctx)
    return _get_printer(ctx, apiclient, printer_id, **kwargs).to_dict()


def delete_printer(ctx, printer_id, **kwargs):
    kwargs = strip_none(kwargs)
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    return apiclient.app_services_api.delete_printer(printer_id, **kwargs)


def update_printer(ctx, printer_id, published=None, name_slug=None, **kwargs):
    kwargs = strip_none(kwargs)
    apiclient = context.get_apiclient_from_ctx(ctx)
    get_args = {}
    update_org_from_input_or_ctx(get_args, ctx, **kwargs)
    mapping = _get_printer(ctx, apiclient, printer_id, **get_args)

    if name_slug is not None:
        kwargs["name_slug"] = K8sSlug(name_slug)

    # Keep the top-level driver_name and the launcher client_config in sync.
    driver_name = kwargs.pop("driver_name", None)

    # PrinterSpec is a strict model: the round-trip through
    # build_updated_model_validate fails when client_config is present in the
    # spec as an explicit null, but works fine when the key is absent. Only
    # materialize a config when it is actually needed - either because we are
    # updating driver_name, or because the server returned an explicit null
    # that must be preserved through the round-trip. This avoids sending a
    # spurious "client_config": {} on unrelated updates of driver-less
    # printers.
    if mapping.spec.client_config is None and (
        driver_name is not None or "client_config" in mapping.spec.to_dict()
    ):
        mapping.spec.client_config = PrinterClientConfig(
            _configuration=context.get_api_config()
        )

    mapping.spec = build_updated_model_validate(PrinterSpec, mapping.spec, kwargs)
    if driver_name is not None:
        mapping.spec.driver_name = driver_name
        # Mutate the existing windows_config so unrelated fields such as
        # location, comment, or is_default survive the update.
        windows_config = mapping.spec.client_config.windows_config
        if windows_config is None:
            windows_config = PrinterWindowsConfig(
                _configuration=context.get_api_config()
            )
            mapping.spec.client_config.windows_config = windows_config
        windows_config.driver_name = driver_name

    mapping = map_resource_published(mapping, published)
    return apiclient.app_services_api.replace_printer(
        printer_id, printer=mapping
    ).to_dict()


def format_printers_as_text(ctx, printers):
    columns = [
        metadata_column("id"),
        spec_column("org_id"),
        spec_column("name"),
        spec_column("printer_name"),
        spec_column("hostname"),
        spec_column("port"),
        spec_column("connector_id"),
        status_column(
            in_name=["per_host_printer_uri", "printer_uri"], out_name="printer_uri"
        ),
    ]

    return format_table(ctx, printers, columns)
