# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class VendorResponse(Model):
    """VendorResponse.

    :param vendor_id: The vendor identifier
    :type vendor_id: int
    :param vendor_code: The vendor code
    :type vendor_code: str
    :param vendor_info: The vendor info
    :type vendor_info: str
    :param address:
    :type address: ~energycap.sdk.models.AddressChild
    :param edi_code: The vendor's edi code
    :type edi_code: str
    :param pay_days: The pay days
    :type pay_days: int
    :param created_by:
    :type created_by: ~energycap.sdk.models.UserChild
    :param created_date: The date and time the vendor was created
    :type created_date: datetime
    :param modified_by:
    :type modified_by: ~energycap.sdk.models.UserChild
    :param modified_date: The date and time of the most recent modification
    :type modified_date: datetime
    :param website: The vendor's website
    :type website: str
    :param rates: The vendor's rates
    :type rates: list[~energycap.sdk.models.RateChildResponse]
    :param vendor_description: A description of the vendor
    :type vendor_description: str
    """

    _attribute_map = {
        'vendor_id': {'key': 'vendorId', 'type': 'int'},
        'vendor_code': {'key': 'vendorCode', 'type': 'str'},
        'vendor_info': {'key': 'vendorInfo', 'type': 'str'},
        'address': {'key': 'address', 'type': 'AddressChild'},
        'edi_code': {'key': 'ediCode', 'type': 'str'},
        'pay_days': {'key': 'payDays', 'type': 'int'},
        'created_by': {'key': 'createdBy', 'type': 'UserChild'},
        'created_date': {'key': 'createdDate', 'type': 'iso-8601'},
        'modified_by': {'key': 'modifiedBy', 'type': 'UserChild'},
        'modified_date': {'key': 'modifiedDate', 'type': 'iso-8601'},
        'website': {'key': 'website', 'type': 'str'},
        'rates': {'key': 'rates', 'type': '[RateChildResponse]'},
        'vendor_description': {'key': 'vendorDescription', 'type': 'str'},
    }

    def __init__(self, *, vendor_id: int=None, vendor_code: str=None, vendor_info: str=None, address=None, edi_code: str=None, pay_days: int=None, created_by=None, created_date=None, modified_by=None, modified_date=None, website: str=None, rates=None, vendor_description: str=None, **kwargs) -> None:
        super(VendorResponse, self).__init__(**kwargs)
        self.vendor_id = vendor_id
        self.vendor_code = vendor_code
        self.vendor_info = vendor_info
        self.address = address
        self.edi_code = edi_code
        self.pay_days = pay_days
        self.created_by = created_by
        self.created_date = created_date
        self.modified_by = modified_by
        self.modified_date = modified_date
        self.website = website
        self.rates = rates
        self.vendor_description = vendor_description
