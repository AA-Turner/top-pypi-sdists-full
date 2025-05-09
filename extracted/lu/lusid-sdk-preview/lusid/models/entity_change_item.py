# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 1.1.226
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


class EntityChangeItem(object):
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
        'as_at_modified': 'datetime',
        'user_id_modified': 'str',
        'request_id_modified': 'str',
        'as_at_version_number': 'int',
        'action': 'str',
        'action_description': 'str',
        'attribute_name': 'str',
        'previous_value': 'object',
        'new_value': 'object',
        'effective_from': 'datetime',
        'effective_until': 'datetime',
        'detail': 'dict(str, str)'
    }

    attribute_map = {
        'as_at_modified': 'asAtModified',
        'user_id_modified': 'userIdModified',
        'request_id_modified': 'requestIdModified',
        'as_at_version_number': 'asAtVersionNumber',
        'action': 'action',
        'action_description': 'actionDescription',
        'attribute_name': 'attributeName',
        'previous_value': 'previousValue',
        'new_value': 'newValue',
        'effective_from': 'effectiveFrom',
        'effective_until': 'effectiveUntil',
        'detail': 'detail'
    }

    required_map = {
        'as_at_modified': 'required',
        'user_id_modified': 'required',
        'request_id_modified': 'required',
        'as_at_version_number': 'required',
        'action': 'required',
        'action_description': 'required',
        'attribute_name': 'optional',
        'previous_value': 'optional',
        'new_value': 'optional',
        'effective_from': 'optional',
        'effective_until': 'optional',
        'detail': 'optional'
    }

    def __init__(self, as_at_modified=None, user_id_modified=None, request_id_modified=None, as_at_version_number=None, action=None, action_description=None, attribute_name=None, previous_value=None, new_value=None, effective_from=None, effective_until=None, detail=None, local_vars_configuration=None):  # noqa: E501
        """EntityChangeItem - a model defined in OpenAPI"
        
        :param as_at_modified:  The date/time of the change. (required)
        :type as_at_modified: datetime
        :param user_id_modified:  The unique identifier of the user that made the change. (required)
        :type user_id_modified: str
        :param request_id_modified:  The unique identifier of the request that the changes were part of. (required)
        :type request_id_modified: str
        :param as_at_version_number:  The version number for the entity (the entity was created at version 1). This may refer to the version number of a changed related entity, not a change for the entity itself. (required)
        :type as_at_version_number: int
        :param action:  The action performed on the entity. (required)
        :type action: str
        :param action_description:  Description of the action performed on the entity. (required)
        :type action_description: str
        :param attribute_name:  The name of the field or property that has been changed.
        :type attribute_name: str
        :param previous_value:  The value of the attribute prior to the change.
        :type previous_value: object
        :param new_value:  The value of the attribute following the change.
        :type new_value: object
        :param effective_from:  The effective datetime from which the field's new value is valid.
        :type effective_from: datetime
        :param effective_until:  The effective datetime until which the field's new value is valid.
        :type effective_until: datetime
        :param detail:  Information about the particular instance of the ChangeItem (supplied information depends on the type of Action).
        :type detail: dict(str, str)

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._as_at_modified = None
        self._user_id_modified = None
        self._request_id_modified = None
        self._as_at_version_number = None
        self._action = None
        self._action_description = None
        self._attribute_name = None
        self._previous_value = None
        self._new_value = None
        self._effective_from = None
        self._effective_until = None
        self._detail = None
        self.discriminator = None

        self.as_at_modified = as_at_modified
        self.user_id_modified = user_id_modified
        self.request_id_modified = request_id_modified
        self.as_at_version_number = as_at_version_number
        self.action = action
        self.action_description = action_description
        self.attribute_name = attribute_name
        self.previous_value = previous_value
        self.new_value = new_value
        self.effective_from = effective_from
        self.effective_until = effective_until
        self.detail = detail

    @property
    def as_at_modified(self):
        """Gets the as_at_modified of this EntityChangeItem.  # noqa: E501

        The date/time of the change.  # noqa: E501

        :return: The as_at_modified of this EntityChangeItem.  # noqa: E501
        :rtype: datetime
        """
        return self._as_at_modified

    @as_at_modified.setter
    def as_at_modified(self, as_at_modified):
        """Sets the as_at_modified of this EntityChangeItem.

        The date/time of the change.  # noqa: E501

        :param as_at_modified: The as_at_modified of this EntityChangeItem.  # noqa: E501
        :type as_at_modified: datetime
        """
        if self.local_vars_configuration.client_side_validation and as_at_modified is None:  # noqa: E501
            raise ValueError("Invalid value for `as_at_modified`, must not be `None`")  # noqa: E501

        self._as_at_modified = as_at_modified

    @property
    def user_id_modified(self):
        """Gets the user_id_modified of this EntityChangeItem.  # noqa: E501

        The unique identifier of the user that made the change.  # noqa: E501

        :return: The user_id_modified of this EntityChangeItem.  # noqa: E501
        :rtype: str
        """
        return self._user_id_modified

    @user_id_modified.setter
    def user_id_modified(self, user_id_modified):
        """Sets the user_id_modified of this EntityChangeItem.

        The unique identifier of the user that made the change.  # noqa: E501

        :param user_id_modified: The user_id_modified of this EntityChangeItem.  # noqa: E501
        :type user_id_modified: str
        """
        if self.local_vars_configuration.client_side_validation and user_id_modified is None:  # noqa: E501
            raise ValueError("Invalid value for `user_id_modified`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                user_id_modified is not None and len(user_id_modified) < 1):
            raise ValueError("Invalid value for `user_id_modified`, length must be greater than or equal to `1`")  # noqa: E501

        self._user_id_modified = user_id_modified

    @property
    def request_id_modified(self):
        """Gets the request_id_modified of this EntityChangeItem.  # noqa: E501

        The unique identifier of the request that the changes were part of.  # noqa: E501

        :return: The request_id_modified of this EntityChangeItem.  # noqa: E501
        :rtype: str
        """
        return self._request_id_modified

    @request_id_modified.setter
    def request_id_modified(self, request_id_modified):
        """Sets the request_id_modified of this EntityChangeItem.

        The unique identifier of the request that the changes were part of.  # noqa: E501

        :param request_id_modified: The request_id_modified of this EntityChangeItem.  # noqa: E501
        :type request_id_modified: str
        """
        if self.local_vars_configuration.client_side_validation and request_id_modified is None:  # noqa: E501
            raise ValueError("Invalid value for `request_id_modified`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                request_id_modified is not None and len(request_id_modified) < 1):
            raise ValueError("Invalid value for `request_id_modified`, length must be greater than or equal to `1`")  # noqa: E501

        self._request_id_modified = request_id_modified

    @property
    def as_at_version_number(self):
        """Gets the as_at_version_number of this EntityChangeItem.  # noqa: E501

        The version number for the entity (the entity was created at version 1). This may refer to the version number of a changed related entity, not a change for the entity itself.  # noqa: E501

        :return: The as_at_version_number of this EntityChangeItem.  # noqa: E501
        :rtype: int
        """
        return self._as_at_version_number

    @as_at_version_number.setter
    def as_at_version_number(self, as_at_version_number):
        """Sets the as_at_version_number of this EntityChangeItem.

        The version number for the entity (the entity was created at version 1). This may refer to the version number of a changed related entity, not a change for the entity itself.  # noqa: E501

        :param as_at_version_number: The as_at_version_number of this EntityChangeItem.  # noqa: E501
        :type as_at_version_number: int
        """
        if self.local_vars_configuration.client_side_validation and as_at_version_number is None:  # noqa: E501
            raise ValueError("Invalid value for `as_at_version_number`, must not be `None`")  # noqa: E501

        self._as_at_version_number = as_at_version_number

    @property
    def action(self):
        """Gets the action of this EntityChangeItem.  # noqa: E501

        The action performed on the entity.  # noqa: E501

        :return: The action of this EntityChangeItem.  # noqa: E501
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """Sets the action of this EntityChangeItem.

        The action performed on the entity.  # noqa: E501

        :param action: The action of this EntityChangeItem.  # noqa: E501
        :type action: str
        """
        if self.local_vars_configuration.client_side_validation and action is None:  # noqa: E501
            raise ValueError("Invalid value for `action`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                action is not None and len(action) < 1):
            raise ValueError("Invalid value for `action`, length must be greater than or equal to `1`")  # noqa: E501

        self._action = action

    @property
    def action_description(self):
        """Gets the action_description of this EntityChangeItem.  # noqa: E501

        Description of the action performed on the entity.  # noqa: E501

        :return: The action_description of this EntityChangeItem.  # noqa: E501
        :rtype: str
        """
        return self._action_description

    @action_description.setter
    def action_description(self, action_description):
        """Sets the action_description of this EntityChangeItem.

        Description of the action performed on the entity.  # noqa: E501

        :param action_description: The action_description of this EntityChangeItem.  # noqa: E501
        :type action_description: str
        """
        if self.local_vars_configuration.client_side_validation and action_description is None:  # noqa: E501
            raise ValueError("Invalid value for `action_description`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                action_description is not None and len(action_description) < 1):
            raise ValueError("Invalid value for `action_description`, length must be greater than or equal to `1`")  # noqa: E501

        self._action_description = action_description

    @property
    def attribute_name(self):
        """Gets the attribute_name of this EntityChangeItem.  # noqa: E501

        The name of the field or property that has been changed.  # noqa: E501

        :return: The attribute_name of this EntityChangeItem.  # noqa: E501
        :rtype: str
        """
        return self._attribute_name

    @attribute_name.setter
    def attribute_name(self, attribute_name):
        """Sets the attribute_name of this EntityChangeItem.

        The name of the field or property that has been changed.  # noqa: E501

        :param attribute_name: The attribute_name of this EntityChangeItem.  # noqa: E501
        :type attribute_name: str
        """

        self._attribute_name = attribute_name

    @property
    def previous_value(self):
        """Gets the previous_value of this EntityChangeItem.  # noqa: E501

        The value of the attribute prior to the change.  # noqa: E501

        :return: The previous_value of this EntityChangeItem.  # noqa: E501
        :rtype: object
        """
        return self._previous_value

    @previous_value.setter
    def previous_value(self, previous_value):
        """Sets the previous_value of this EntityChangeItem.

        The value of the attribute prior to the change.  # noqa: E501

        :param previous_value: The previous_value of this EntityChangeItem.  # noqa: E501
        :type previous_value: object
        """

        self._previous_value = previous_value

    @property
    def new_value(self):
        """Gets the new_value of this EntityChangeItem.  # noqa: E501

        The value of the attribute following the change.  # noqa: E501

        :return: The new_value of this EntityChangeItem.  # noqa: E501
        :rtype: object
        """
        return self._new_value

    @new_value.setter
    def new_value(self, new_value):
        """Sets the new_value of this EntityChangeItem.

        The value of the attribute following the change.  # noqa: E501

        :param new_value: The new_value of this EntityChangeItem.  # noqa: E501
        :type new_value: object
        """

        self._new_value = new_value

    @property
    def effective_from(self):
        """Gets the effective_from of this EntityChangeItem.  # noqa: E501

        The effective datetime from which the field's new value is valid.  # noqa: E501

        :return: The effective_from of this EntityChangeItem.  # noqa: E501
        :rtype: datetime
        """
        return self._effective_from

    @effective_from.setter
    def effective_from(self, effective_from):
        """Sets the effective_from of this EntityChangeItem.

        The effective datetime from which the field's new value is valid.  # noqa: E501

        :param effective_from: The effective_from of this EntityChangeItem.  # noqa: E501
        :type effective_from: datetime
        """

        self._effective_from = effective_from

    @property
    def effective_until(self):
        """Gets the effective_until of this EntityChangeItem.  # noqa: E501

        The effective datetime until which the field's new value is valid.  # noqa: E501

        :return: The effective_until of this EntityChangeItem.  # noqa: E501
        :rtype: datetime
        """
        return self._effective_until

    @effective_until.setter
    def effective_until(self, effective_until):
        """Sets the effective_until of this EntityChangeItem.

        The effective datetime until which the field's new value is valid.  # noqa: E501

        :param effective_until: The effective_until of this EntityChangeItem.  # noqa: E501
        :type effective_until: datetime
        """

        self._effective_until = effective_until

    @property
    def detail(self):
        """Gets the detail of this EntityChangeItem.  # noqa: E501

        Information about the particular instance of the ChangeItem (supplied information depends on the type of Action).  # noqa: E501

        :return: The detail of this EntityChangeItem.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._detail

    @detail.setter
    def detail(self, detail):
        """Sets the detail of this EntityChangeItem.

        Information about the particular instance of the ChangeItem (supplied information depends on the type of Action).  # noqa: E501

        :param detail: The detail of this EntityChangeItem.  # noqa: E501
        :type detail: dict(str, str)
        """

        self._detail = detail

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
        if not isinstance(other, EntityChangeItem):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, EntityChangeItem):
            return True

        return self.to_dict() != other.to_dict()
