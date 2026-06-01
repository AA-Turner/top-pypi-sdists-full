from jambo.parser._type_parser import GenericTypeParser
from jambo.types.type_parser_options import TypeParserOptions

from typing_extensions import Unpack


class NullTypeParser(GenericTypeParser):
    mapped_type = type(None)

    json_schema_type = "type:null"

    def from_properties_impl(
        self, name, properties, **kwargs: Unpack[TypeParserOptions]
    ):
        mapped_properties = self.mappings_properties_builder(properties, **kwargs)
        mapped_properties["default"] = None

        return self.mapped_type, mapped_properties
