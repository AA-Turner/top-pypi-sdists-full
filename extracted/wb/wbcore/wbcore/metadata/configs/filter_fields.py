from contextlib import suppress

from wbcore.filters import DjangoFilterBackend

from .base import WBCoreViewConfig


class FilterFieldsViewConfig(WBCoreViewConfig):
    metadata_key = "filter_fields"
    config_class_attribute = "filter_fields_config_class"

    def get_metadata(self):
        filter_fields = dict()

        with suppress(StopIteration):
            backend = next(
                filter(lambda b: issubclass(b, DjangoFilterBackend), getattr(self.view, "filter_backends", []))
            )
            if filterset_class := backend().get_filterset_class(self.view, self.view.queryset):  # type: ignore
                filterset = filterset_class()
                filters = filterset.get_filters()
                hidden_fields = []
                # TODO: This should be the responsibility of the filterset_class to return also the df_fields
                if filterset_class_meta := getattr(filterset_class, "Meta", None):
                    hidden_fields.extend(getattr(filterset_class_meta, "hidden_fields", []))
                    filters.update(getattr(filterset_class_meta, "df_fields", {}))
                for name, field in filters.items():
                    field.parent = filterset
                    if res := field.get_representation(self.request, name, self.view):
                        representation, lookup_expr = res
                        if name in hidden_fields:
                            lookup_expr["hidden"] = True
                        if field.key in filter_fields:
                            filter_fields[field.key]["lookup_expr"].append(lookup_expr)
                        else:
                            filter_fields[field.key] = representation
                            filter_fields[field.key]["lookup_expr"] = [lookup_expr]
                            filter_fields[field.key]["label"] = field.label

        return filter_fields
