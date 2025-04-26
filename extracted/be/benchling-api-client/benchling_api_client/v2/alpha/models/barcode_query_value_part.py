from typing import Union

from ..extensions import UnknownType
from ..models.form_barcode_value_reference import FormBarcodeValueReference
from ..models.form_field_value_reference import FormFieldValueReference
from ..models.form_raw_string_query_value_part import FormRawStringQueryValuePart

BarcodeQueryValuePart = Union[
    FormBarcodeValueReference, FormFieldValueReference, FormRawStringQueryValuePart, UnknownType
]
