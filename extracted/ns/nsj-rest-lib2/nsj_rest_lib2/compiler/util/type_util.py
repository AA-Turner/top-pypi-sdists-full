from nsj_rest_lib2.compiler.edl_model.primitives import (
    MAPPING_PRIMITIVE_TYPES_TO_PYTHON,
    PrimitiveTypes,
)


class TypeUtil:
    @staticmethod
    def property_type_to_python_type(prop_type: PrimitiveTypes) -> str:
        """Mapeia tipos de propriedades do EDL para tipos Python."""

        return MAPPING_PRIMITIVE_TYPES_TO_PYTHON[prop_type]
