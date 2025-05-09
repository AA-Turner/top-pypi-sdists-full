# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BillViewVendorChild(Model):
    """BillViewVendorChild.

    :param vendor_id: The vendor identifier
    :type vendor_id: int
    :param vendor_code: The vendor code
    :type vendor_code: str
    :param vendor_info: The vendor info
    :type vendor_info: str
    :param address:
    :type address: ~energycap.sdk.models.BillViewAddressChild
    """

    _attribute_map = {
        'vendor_id': {'key': 'vendorId', 'type': 'int'},
        'vendor_code': {'key': 'vendorCode', 'type': 'str'},
        'vendor_info': {'key': 'vendorInfo', 'type': 'str'},
        'address': {'key': 'address', 'type': 'BillViewAddressChild'},
    }

    def __init__(self, *, vendor_id: int=None, vendor_code: str=None, vendor_info: str=None, address=None, **kwargs) -> None:
        super(BillViewVendorChild, self).__init__(**kwargs)
        self.vendor_id = vendor_id
        self.vendor_code = vendor_code
        self.vendor_info = vendor_info
        self.address = address
