from collections import defaultdict

from .base import WBCoreViewConfig


class FieldsViewConfig(WBCoreViewConfig):
    metadata_key = "fields"
    config_class_attribute = "fields_config_class"

    def get_metadata(self) -> dict:
        fields = defaultdict(dict)
        if (serializer_class := getattr(self.view, "get_serializer", None)) and (serializer := serializer_class()):
            related_key_fields = []
            for field_name, field in serializer.fields.items():
                field_key, field_representation = field.get_representation(self.request, field_name)
                # we need to get the representation of the related field last so that the key update properly (priority to the related field values)
                if "related_key" in field_representation:
                    related_key_fields.append((field_key, field_representation))
                fields[field_key].update(field_representation)
            for field_key, field_representation in related_key_fields:
                fields[field_key].update(field_representation)
        return fields
