from typing import Union

from ..extensions import UnknownType
from ..models.barcode_scan_form_instance_provider import BarcodeScanFormInstanceProvider
from ..models.entity_search_instance_provider import EntitySearchInstanceProvider
from ..models.new_blank_form_instance_provider import NewBlankFormInstanceProvider

InstanceProvider = Union[
    BarcodeScanFormInstanceProvider, NewBlankFormInstanceProvider, EntitySearchInstanceProvider, UnknownType
]
