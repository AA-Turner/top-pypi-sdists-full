from typing import Union

from ..extensions import UnknownType
from ..models.barcode_form_field import BarcodeFormField
from ..models.date_selection_form_field import DateSelectionFormField
from ..models.entity_link_form_field import EntityLinkFormField
from ..models.free_form_text_form_field import FreeFormTextFormField
from ..models.nested_form_field import NestedFormField
from ..models.string_select_form_field import StringSelectFormField

BaseFormField = Union[
    BarcodeFormField,
    DateSelectionFormField,
    EntityLinkFormField,
    NestedFormField,
    FreeFormTextFormField,
    StringSelectFormField,
    UnknownType,
]
