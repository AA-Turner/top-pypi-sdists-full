# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 1.1.257
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from lusid.configuration import Configuration


class MarketOptions(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'default_supplier': 'str',
        'default_instrument_code_type': 'str',
        'default_scope': 'str',
        'attempt_to_infer_missing_fx': 'bool',
        'calendar_scope': 'str',
        'convention_scope': 'str'
    }

    attribute_map = {
        'default_supplier': 'defaultSupplier',
        'default_instrument_code_type': 'defaultInstrumentCodeType',
        'default_scope': 'defaultScope',
        'attempt_to_infer_missing_fx': 'attemptToInferMissingFx',
        'calendar_scope': 'calendarScope',
        'convention_scope': 'conventionScope'
    }

    required_map = {
        'default_supplier': 'optional',
        'default_instrument_code_type': 'optional',
        'default_scope': 'required',
        'attempt_to_infer_missing_fx': 'optional',
        'calendar_scope': 'optional',
        'convention_scope': 'optional'
    }

    def __init__(self, default_supplier=None, default_instrument_code_type=None, default_scope=None, attempt_to_infer_missing_fx=None, calendar_scope=None, convention_scope=None, local_vars_configuration=None):  # noqa: E501
        """MarketOptions - a model defined in OpenAPI"
        
        :param default_supplier:  The default supplier of data. This controls which 'dialect' is used to find particular market data. e.g. one supplier might address data by RIC, another by PermId
        :type default_supplier: str
        :param default_instrument_code_type:  When instrument quotes are searched for, what identifier should be used by default
        :type default_instrument_code_type: str
        :param default_scope:  For default rules, which scope should data be searched for in (required)
        :type default_scope: str
        :param attempt_to_infer_missing_fx:  if true will calculate a missing Fx pair (e.g. THBJPY) from the inverse JPYTHB or from standardised pairs against USD, e.g. THBUSD and JPYUSD
        :type attempt_to_infer_missing_fx: bool
        :param calendar_scope:  The scope in which holiday calendars stored
        :type calendar_scope: str
        :param convention_scope:  The scope in which conventions stored
        :type convention_scope: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._default_supplier = None
        self._default_instrument_code_type = None
        self._default_scope = None
        self._attempt_to_infer_missing_fx = None
        self._calendar_scope = None
        self._convention_scope = None
        self.discriminator = None

        self.default_supplier = default_supplier
        self.default_instrument_code_type = default_instrument_code_type
        self.default_scope = default_scope
        if attempt_to_infer_missing_fx is not None:
            self.attempt_to_infer_missing_fx = attempt_to_infer_missing_fx
        self.calendar_scope = calendar_scope
        self.convention_scope = convention_scope

    @property
    def default_supplier(self):
        """Gets the default_supplier of this MarketOptions.  # noqa: E501

        The default supplier of data. This controls which 'dialect' is used to find particular market data. e.g. one supplier might address data by RIC, another by PermId  # noqa: E501

        :return: The default_supplier of this MarketOptions.  # noqa: E501
        :rtype: str
        """
        return self._default_supplier

    @default_supplier.setter
    def default_supplier(self, default_supplier):
        """Sets the default_supplier of this MarketOptions.

        The default supplier of data. This controls which 'dialect' is used to find particular market data. e.g. one supplier might address data by RIC, another by PermId  # noqa: E501

        :param default_supplier: The default_supplier of this MarketOptions.  # noqa: E501
        :type default_supplier: str
        """
        if (self.local_vars_configuration.client_side_validation and
                default_supplier is not None and len(default_supplier) > 32):
            raise ValueError("Invalid value for `default_supplier`, length must be less than or equal to `32`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                default_supplier is not None and len(default_supplier) < 0):
            raise ValueError("Invalid value for `default_supplier`, length must be greater than or equal to `0`")  # noqa: E501

        self._default_supplier = default_supplier

    @property
    def default_instrument_code_type(self):
        """Gets the default_instrument_code_type of this MarketOptions.  # noqa: E501

        When instrument quotes are searched for, what identifier should be used by default  # noqa: E501

        :return: The default_instrument_code_type of this MarketOptions.  # noqa: E501
        :rtype: str
        """
        return self._default_instrument_code_type

    @default_instrument_code_type.setter
    def default_instrument_code_type(self, default_instrument_code_type):
        """Sets the default_instrument_code_type of this MarketOptions.

        When instrument quotes are searched for, what identifier should be used by default  # noqa: E501

        :param default_instrument_code_type: The default_instrument_code_type of this MarketOptions.  # noqa: E501
        :type default_instrument_code_type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                default_instrument_code_type is not None and len(default_instrument_code_type) > 32):
            raise ValueError("Invalid value for `default_instrument_code_type`, length must be less than or equal to `32`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                default_instrument_code_type is not None and len(default_instrument_code_type) < 0):
            raise ValueError("Invalid value for `default_instrument_code_type`, length must be greater than or equal to `0`")  # noqa: E501

        self._default_instrument_code_type = default_instrument_code_type

    @property
    def default_scope(self):
        """Gets the default_scope of this MarketOptions.  # noqa: E501

        For default rules, which scope should data be searched for in  # noqa: E501

        :return: The default_scope of this MarketOptions.  # noqa: E501
        :rtype: str
        """
        return self._default_scope

    @default_scope.setter
    def default_scope(self, default_scope):
        """Sets the default_scope of this MarketOptions.

        For default rules, which scope should data be searched for in  # noqa: E501

        :param default_scope: The default_scope of this MarketOptions.  # noqa: E501
        :type default_scope: str
        """
        if self.local_vars_configuration.client_side_validation and default_scope is None:  # noqa: E501
            raise ValueError("Invalid value for `default_scope`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                default_scope is not None and len(default_scope) > 256):
            raise ValueError("Invalid value for `default_scope`, length must be less than or equal to `256`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                default_scope is not None and len(default_scope) < 1):
            raise ValueError("Invalid value for `default_scope`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                default_scope is not None and not re.search(r'^[a-zA-Z0-9\-_]+$', default_scope)):  # noqa: E501
            raise ValueError(r"Invalid value for `default_scope`, must be a follow pattern or equal to `/^[a-zA-Z0-9\-_]+$/`")  # noqa: E501

        self._default_scope = default_scope

    @property
    def attempt_to_infer_missing_fx(self):
        """Gets the attempt_to_infer_missing_fx of this MarketOptions.  # noqa: E501

        if true will calculate a missing Fx pair (e.g. THBJPY) from the inverse JPYTHB or from standardised pairs against USD, e.g. THBUSD and JPYUSD  # noqa: E501

        :return: The attempt_to_infer_missing_fx of this MarketOptions.  # noqa: E501
        :rtype: bool
        """
        return self._attempt_to_infer_missing_fx

    @attempt_to_infer_missing_fx.setter
    def attempt_to_infer_missing_fx(self, attempt_to_infer_missing_fx):
        """Sets the attempt_to_infer_missing_fx of this MarketOptions.

        if true will calculate a missing Fx pair (e.g. THBJPY) from the inverse JPYTHB or from standardised pairs against USD, e.g. THBUSD and JPYUSD  # noqa: E501

        :param attempt_to_infer_missing_fx: The attempt_to_infer_missing_fx of this MarketOptions.  # noqa: E501
        :type attempt_to_infer_missing_fx: bool
        """

        self._attempt_to_infer_missing_fx = attempt_to_infer_missing_fx

    @property
    def calendar_scope(self):
        """Gets the calendar_scope of this MarketOptions.  # noqa: E501

        The scope in which holiday calendars stored  # noqa: E501

        :return: The calendar_scope of this MarketOptions.  # noqa: E501
        :rtype: str
        """
        return self._calendar_scope

    @calendar_scope.setter
    def calendar_scope(self, calendar_scope):
        """Sets the calendar_scope of this MarketOptions.

        The scope in which holiday calendars stored  # noqa: E501

        :param calendar_scope: The calendar_scope of this MarketOptions.  # noqa: E501
        :type calendar_scope: str
        """
        if (self.local_vars_configuration.client_side_validation and
                calendar_scope is not None and len(calendar_scope) > 256):
            raise ValueError("Invalid value for `calendar_scope`, length must be less than or equal to `256`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                calendar_scope is not None and len(calendar_scope) < 1):
            raise ValueError("Invalid value for `calendar_scope`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                calendar_scope is not None and not re.search(r'^[a-zA-Z0-9\-_]+$', calendar_scope)):  # noqa: E501
            raise ValueError(r"Invalid value for `calendar_scope`, must be a follow pattern or equal to `/^[a-zA-Z0-9\-_]+$/`")  # noqa: E501

        self._calendar_scope = calendar_scope

    @property
    def convention_scope(self):
        """Gets the convention_scope of this MarketOptions.  # noqa: E501

        The scope in which conventions stored  # noqa: E501

        :return: The convention_scope of this MarketOptions.  # noqa: E501
        :rtype: str
        """
        return self._convention_scope

    @convention_scope.setter
    def convention_scope(self, convention_scope):
        """Sets the convention_scope of this MarketOptions.

        The scope in which conventions stored  # noqa: E501

        :param convention_scope: The convention_scope of this MarketOptions.  # noqa: E501
        :type convention_scope: str
        """
        if (self.local_vars_configuration.client_side_validation and
                convention_scope is not None and len(convention_scope) > 256):
            raise ValueError("Invalid value for `convention_scope`, length must be less than or equal to `256`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                convention_scope is not None and len(convention_scope) < 1):
            raise ValueError("Invalid value for `convention_scope`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                convention_scope is not None and not re.search(r'^[a-zA-Z0-9\-_]+$', convention_scope)):  # noqa: E501
            raise ValueError(r"Invalid value for `convention_scope`, must be a follow pattern or equal to `/^[a-zA-Z0-9\-_]+$/`")  # noqa: E501

        self._convention_scope = convention_scope

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, MarketOptions):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MarketOptions):
            return True

        return self.to_dict() != other.to_dict()
