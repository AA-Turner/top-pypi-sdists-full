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


class AddressKeyOptionDefinition(object):
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
        'name': 'str',
        'type': 'str',
        'description': 'str',
        'optional': 'bool',
        'allowed_value_set': 'list[str]',
        'default_value': 'str'
    }

    attribute_map = {
        'name': 'name',
        'type': 'type',
        'description': 'description',
        'optional': 'optional',
        'allowed_value_set': 'allowedValueSet',
        'default_value': 'defaultValue'
    }

    required_map = {
        'name': 'required',
        'type': 'required',
        'description': 'required',
        'optional': 'required',
        'allowed_value_set': 'optional',
        'default_value': 'optional'
    }

    def __init__(self, name=None, type=None, description=None, optional=None, allowed_value_set=None, default_value=None, local_vars_configuration=None):  # noqa: E501
        """AddressKeyOptionDefinition - a model defined in OpenAPI"
        
        :param name:  The name of the option (required)
        :type name: str
        :param type:  The type of the option (required)
        :type type: str
        :param description:  The description of the option (required)
        :type description: str
        :param optional:  Is this option required or optional? (required)
        :type optional: bool
        :param allowed_value_set:  If the option is a string or enum, the allowed set of values it can take.
        :type allowed_value_set: list[str]
        :param default_value:  If the option is not required, what is the default value?
        :type default_value: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._type = None
        self._description = None
        self._optional = None
        self._allowed_value_set = None
        self._default_value = None
        self.discriminator = None

        self.name = name
        self.type = type
        self.description = description
        self.optional = optional
        self.allowed_value_set = allowed_value_set
        self.default_value = default_value

    @property
    def name(self):
        """Gets the name of this AddressKeyOptionDefinition.  # noqa: E501

        The name of the option  # noqa: E501

        :return: The name of this AddressKeyOptionDefinition.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this AddressKeyOptionDefinition.

        The name of the option  # noqa: E501

        :param name: The name of this AddressKeyOptionDefinition.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 1):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501

        self._name = name

    @property
    def type(self):
        """Gets the type of this AddressKeyOptionDefinition.  # noqa: E501

        The type of the option  # noqa: E501

        :return: The type of this AddressKeyOptionDefinition.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this AddressKeyOptionDefinition.

        The type of the option  # noqa: E501

        :param type: The type of this AddressKeyOptionDefinition.  # noqa: E501
        :type type: str
        """
        if self.local_vars_configuration.client_side_validation and type is None:  # noqa: E501
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                type is not None and len(type) < 1):
            raise ValueError("Invalid value for `type`, length must be greater than or equal to `1`")  # noqa: E501

        self._type = type

    @property
    def description(self):
        """Gets the description of this AddressKeyOptionDefinition.  # noqa: E501

        The description of the option  # noqa: E501

        :return: The description of this AddressKeyOptionDefinition.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this AddressKeyOptionDefinition.

        The description of the option  # noqa: E501

        :param description: The description of this AddressKeyOptionDefinition.  # noqa: E501
        :type description: str
        """
        if self.local_vars_configuration.client_side_validation and description is None:  # noqa: E501
            raise ValueError("Invalid value for `description`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) < 1):
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `1`")  # noqa: E501

        self._description = description

    @property
    def optional(self):
        """Gets the optional of this AddressKeyOptionDefinition.  # noqa: E501

        Is this option required or optional?  # noqa: E501

        :return: The optional of this AddressKeyOptionDefinition.  # noqa: E501
        :rtype: bool
        """
        return self._optional

    @optional.setter
    def optional(self, optional):
        """Sets the optional of this AddressKeyOptionDefinition.

        Is this option required or optional?  # noqa: E501

        :param optional: The optional of this AddressKeyOptionDefinition.  # noqa: E501
        :type optional: bool
        """
        if self.local_vars_configuration.client_side_validation and optional is None:  # noqa: E501
            raise ValueError("Invalid value for `optional`, must not be `None`")  # noqa: E501

        self._optional = optional

    @property
    def allowed_value_set(self):
        """Gets the allowed_value_set of this AddressKeyOptionDefinition.  # noqa: E501

        If the option is a string or enum, the allowed set of values it can take.  # noqa: E501

        :return: The allowed_value_set of this AddressKeyOptionDefinition.  # noqa: E501
        :rtype: list[str]
        """
        return self._allowed_value_set

    @allowed_value_set.setter
    def allowed_value_set(self, allowed_value_set):
        """Sets the allowed_value_set of this AddressKeyOptionDefinition.

        If the option is a string or enum, the allowed set of values it can take.  # noqa: E501

        :param allowed_value_set: The allowed_value_set of this AddressKeyOptionDefinition.  # noqa: E501
        :type allowed_value_set: list[str]
        """

        self._allowed_value_set = allowed_value_set

    @property
    def default_value(self):
        """Gets the default_value of this AddressKeyOptionDefinition.  # noqa: E501

        If the option is not required, what is the default value?  # noqa: E501

        :return: The default_value of this AddressKeyOptionDefinition.  # noqa: E501
        :rtype: str
        """
        return self._default_value

    @default_value.setter
    def default_value(self, default_value):
        """Sets the default_value of this AddressKeyOptionDefinition.

        If the option is not required, what is the default value?  # noqa: E501

        :param default_value: The default_value of this AddressKeyOptionDefinition.  # noqa: E501
        :type default_value: str
        """

        self._default_value = default_value

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
        if not isinstance(other, AddressKeyOptionDefinition):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AddressKeyOptionDefinition):
            return True

        return self.to_dict() != other.to_dict()
