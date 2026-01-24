import magic
from django.apps import apps
from django.conf import settings
from django.utils.module_loading import import_string
from import_export.formats.base_formats import CSV
from import_export.results import RowResult
from import_export.signals import post_import


def default_import_parse(import_source):
    resource_path = import_source.resource_kwargs["resource_path"]
    resource_kwargs = import_source.resource_kwargs["resource_kwargs"]
    resource_class = import_string(resource_path)
    resource = resource_class(**resource_kwargs)
    input_format = CSV(encoding="utf-8-sig")

    file_stream = import_source.file.read()
    if input_format.CONTENT_TYPE == magic.from_buffer(file_stream, mime=True):
        dataset = input_format.create_dataset(file_stream)

        model = apps.get_model(import_source.parser_handler.handler)
        result = resource.import_data(
            dataset,
            dry_run=False,
            file_name=import_source.file.name,
            user=import_source.creator,
            rollback_on_validation_errors=True,
            raise_errors=settings.DEBUG,
        )
        import_source.file.close()
        post_import.send(sender=None, model=model)
        success_message = """
        {} import finished:
        * new {}
        * updated {}
        * skipped {}
        * failed {}
        * deleted {}
        * invalid {}
        """.format(
            model._meta.verbose_name_plural,
            result.totals[RowResult.IMPORT_TYPE_NEW],
            result.totals[RowResult.IMPORT_TYPE_UPDATE],
            result.totals[RowResult.IMPORT_TYPE_SKIP],
            result.totals[RowResult.IMPORT_TYPE_ERROR],
            result.totals[RowResult.IMPORT_TYPE_DELETE],
            result.totals[RowResult.IMPORT_TYPE_INVALID],
        )
        import_source.log = success_message
        import_source.save()
