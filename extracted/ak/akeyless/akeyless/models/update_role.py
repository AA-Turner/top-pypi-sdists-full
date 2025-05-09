# coding: utf-8

"""
    Akeyless API

    The purpose of this application is to provide access to Akeyless API.  # noqa: E501

    The version of the OpenAPI document: 3.0
    Contact: support@akeyless.io
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from akeyless.configuration import Configuration


class UpdateRole(object):
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
    """
    openapi_types = {
        'analytics_access': 'str',
        'audit_access': 'str',
        'delete_protection': 'str',
        'description': 'str',
        'event_center_access': 'str',
        'event_forwarder_access': 'str',
        'gw_analytics_access': 'str',
        'json': 'bool',
        'name': 'str',
        'new_comment': 'str',
        'new_name': 'str',
        'sra_reports_access': 'str',
        'token': 'str',
        'uid_token': 'str',
        'usage_reports_access': 'str'
    }

    attribute_map = {
        'analytics_access': 'analytics-access',
        'audit_access': 'audit-access',
        'delete_protection': 'delete_protection',
        'description': 'description',
        'event_center_access': 'event-center-access',
        'event_forwarder_access': 'event-forwarder-access',
        'gw_analytics_access': 'gw-analytics-access',
        'json': 'json',
        'name': 'name',
        'new_comment': 'new-comment',
        'new_name': 'new-name',
        'sra_reports_access': 'sra-reports-access',
        'token': 'token',
        'uid_token': 'uid-token',
        'usage_reports_access': 'usage-reports-access'
    }

    def __init__(self, analytics_access=None, audit_access=None, delete_protection=None, description='default_comment', event_center_access=None, event_forwarder_access=None, gw_analytics_access=None, json=False, name=None, new_comment='default_comment', new_name=None, sra_reports_access=None, token=None, uid_token=None, usage_reports_access=None, local_vars_configuration=None):  # noqa: E501
        """UpdateRole - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._analytics_access = None
        self._audit_access = None
        self._delete_protection = None
        self._description = None
        self._event_center_access = None
        self._event_forwarder_access = None
        self._gw_analytics_access = None
        self._json = None
        self._name = None
        self._new_comment = None
        self._new_name = None
        self._sra_reports_access = None
        self._token = None
        self._uid_token = None
        self._usage_reports_access = None
        self.discriminator = None

        if analytics_access is not None:
            self.analytics_access = analytics_access
        if audit_access is not None:
            self.audit_access = audit_access
        if delete_protection is not None:
            self.delete_protection = delete_protection
        if description is not None:
            self.description = description
        if event_center_access is not None:
            self.event_center_access = event_center_access
        if event_forwarder_access is not None:
            self.event_forwarder_access = event_forwarder_access
        if gw_analytics_access is not None:
            self.gw_analytics_access = gw_analytics_access
        if json is not None:
            self.json = json
        self.name = name
        if new_comment is not None:
            self.new_comment = new_comment
        if new_name is not None:
            self.new_name = new_name
        if sra_reports_access is not None:
            self.sra_reports_access = sra_reports_access
        if token is not None:
            self.token = token
        if uid_token is not None:
            self.uid_token = uid_token
        if usage_reports_access is not None:
            self.usage_reports_access = usage_reports_access

    @property
    def analytics_access(self):
        """Gets the analytics_access of this UpdateRole.  # noqa: E501

        Allow this role to view analytics. Currently only 'none', 'own', 'all' values are supported, allowing associated auth methods to view reports produced by the same auth methods.  # noqa: E501

        :return: The analytics_access of this UpdateRole.  # noqa: E501
        :rtype: str
        """
        return self._analytics_access

    @analytics_access.setter
    def analytics_access(self, analytics_access):
        """Sets the analytics_access of this UpdateRole.

        Allow this role to view analytics. Currently only 'none', 'own', 'all' values are supported, allowing associated auth methods to view reports produced by the same auth methods.  # noqa: E501

        :param analytics_access: The analytics_access of this UpdateRole.  # noqa: E501
        :type: str
        """

        self._analytics_access = analytics_access

    @property
    def audit_access(self):
        """Gets the audit_access of this UpdateRole.  # noqa: E501

        Allow this role to view audit logs. Currently only 'none', 'own' and 'all' values are supported, allowing associated auth methods to view audit logs produced by the same auth methods.  # noqa: E501

        :return: The audit_access of this UpdateRole.  # noqa: E501
        :rtype: str
        """
        return self._audit_access

    @audit_access.setter
    def audit_access(self, audit_access):
        """Sets the audit_access of this UpdateRole.

        Allow this role to view audit logs. Currently only 'none', 'own' and 'all' values are supported, allowing associated auth methods to view audit logs produced by the same auth methods.  # noqa: E501

        :param audit_access: The audit_access of this UpdateRole.  # noqa: E501
        :type: str
        """

        self._audit_access = audit_access

    @property
    def delete_protection(self):
        """Gets the delete_protection of this UpdateRole.  # noqa: E501

        Protection from accidental deletion of this object [true/false]  # noqa: E501

        :return: The delete_protection of this UpdateRole.  # noqa: E501
        :rtype: str
        """
        return self._delete_protection

    @delete_protection.setter
    def delete_protection(self, delete_protection):
        """Sets the delete_protection of this UpdateRole.

        Protection from accidental deletion of this object [true/false]  # noqa: E501

        :param delete_protection: The delete_protection of this UpdateRole.  # noqa: E501
        :type: str
        """

        self._delete_protection = delete_protection

    @property
    def description(self):
        """Gets the description of this UpdateRole.  # noqa: E501

        Description of the object  # noqa: E501

        :return: The description of this UpdateRole.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this UpdateRole.

        Description of the object  # noqa: E501

        :param description: The description of this UpdateRole.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def event_center_access(self):
        """Gets the event_center_access of this UpdateRole.  # noqa: E501

        Allow this role to view Event Center. Currently only 'none', 'own' and 'all' values are supported  # noqa: E501

        :return: The event_center_access of this UpdateRole.  # noqa: E501
        :rtype: str
        """
        return self._event_center_access

    @event_center_access.setter
    def event_center_access(self, event_center_access):
        """Sets the event_center_access of this UpdateRole.

        Allow this role to view Event Center. Currently only 'none', 'own' and 'all' values are supported  # noqa: E501

        :param event_center_access: The event_center_access of this UpdateRole.  # noqa: E501
        :type: str
        """

        self._event_center_access = event_center_access

    @property
    def event_forwarder_access(self):
        """Gets the event_forwarder_access of this UpdateRole.  # noqa: E501

        Allow this role to manage Event Forwarders. Currently only 'none' and 'all' values are supported.  # noqa: E501

        :return: The event_forwarder_access of this UpdateRole.  # noqa: E501
        :rtype: str
        """
        return self._event_forwarder_access

    @event_forwarder_access.setter
    def event_forwarder_access(self, event_forwarder_access):
        """Sets the event_forwarder_access of this UpdateRole.

        Allow this role to manage Event Forwarders. Currently only 'none' and 'all' values are supported.  # noqa: E501

        :param event_forwarder_access: The event_forwarder_access of this UpdateRole.  # noqa: E501
        :type: str
        """

        self._event_forwarder_access = event_forwarder_access

    @property
    def gw_analytics_access(self):
        """Gets the gw_analytics_access of this UpdateRole.  # noqa: E501

        Allow this role to view gw analytics. Currently only 'none', 'own', 'all' values are supported, allowing associated auth methods to view reports produced by the same auth methods.  # noqa: E501

        :return: The gw_analytics_access of this UpdateRole.  # noqa: E501
        :rtype: str
        """
        return self._gw_analytics_access

    @gw_analytics_access.setter
    def gw_analytics_access(self, gw_analytics_access):
        """Sets the gw_analytics_access of this UpdateRole.

        Allow this role to view gw analytics. Currently only 'none', 'own', 'all' values are supported, allowing associated auth methods to view reports produced by the same auth methods.  # noqa: E501

        :param gw_analytics_access: The gw_analytics_access of this UpdateRole.  # noqa: E501
        :type: str
        """

        self._gw_analytics_access = gw_analytics_access

    @property
    def json(self):
        """Gets the json of this UpdateRole.  # noqa: E501

        Set output format to JSON  # noqa: E501

        :return: The json of this UpdateRole.  # noqa: E501
        :rtype: bool
        """
        return self._json

    @json.setter
    def json(self, json):
        """Sets the json of this UpdateRole.

        Set output format to JSON  # noqa: E501

        :param json: The json of this UpdateRole.  # noqa: E501
        :type: bool
        """

        self._json = json

    @property
    def name(self):
        """Gets the name of this UpdateRole.  # noqa: E501

        Role name  # noqa: E501

        :return: The name of this UpdateRole.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UpdateRole.

        Role name  # noqa: E501

        :param name: The name of this UpdateRole.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def new_comment(self):
        """Gets the new_comment of this UpdateRole.  # noqa: E501

        Deprecated - use description  # noqa: E501

        :return: The new_comment of this UpdateRole.  # noqa: E501
        :rtype: str
        """
        return self._new_comment

    @new_comment.setter
    def new_comment(self, new_comment):
        """Sets the new_comment of this UpdateRole.

        Deprecated - use description  # noqa: E501

        :param new_comment: The new_comment of this UpdateRole.  # noqa: E501
        :type: str
        """

        self._new_comment = new_comment

    @property
    def new_name(self):
        """Gets the new_name of this UpdateRole.  # noqa: E501

        New Role name  # noqa: E501

        :return: The new_name of this UpdateRole.  # noqa: E501
        :rtype: str
        """
        return self._new_name

    @new_name.setter
    def new_name(self, new_name):
        """Sets the new_name of this UpdateRole.

        New Role name  # noqa: E501

        :param new_name: The new_name of this UpdateRole.  # noqa: E501
        :type: str
        """

        self._new_name = new_name

    @property
    def sra_reports_access(self):
        """Gets the sra_reports_access of this UpdateRole.  # noqa: E501

        Allow this role to view SRA Clusters. Currently only 'none', 'own', 'all' values are supported.  # noqa: E501

        :return: The sra_reports_access of this UpdateRole.  # noqa: E501
        :rtype: str
        """
        return self._sra_reports_access

    @sra_reports_access.setter
    def sra_reports_access(self, sra_reports_access):
        """Sets the sra_reports_access of this UpdateRole.

        Allow this role to view SRA Clusters. Currently only 'none', 'own', 'all' values are supported.  # noqa: E501

        :param sra_reports_access: The sra_reports_access of this UpdateRole.  # noqa: E501
        :type: str
        """

        self._sra_reports_access = sra_reports_access

    @property
    def token(self):
        """Gets the token of this UpdateRole.  # noqa: E501

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :return: The token of this UpdateRole.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this UpdateRole.

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :param token: The token of this UpdateRole.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def uid_token(self):
        """Gets the uid_token of this UpdateRole.  # noqa: E501

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :return: The uid_token of this UpdateRole.  # noqa: E501
        :rtype: str
        """
        return self._uid_token

    @uid_token.setter
    def uid_token(self, uid_token):
        """Sets the uid_token of this UpdateRole.

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :param uid_token: The uid_token of this UpdateRole.  # noqa: E501
        :type: str
        """

        self._uid_token = uid_token

    @property
    def usage_reports_access(self):
        """Gets the usage_reports_access of this UpdateRole.  # noqa: E501

        Allow this role to view Usage Report. Currently only 'none' and 'all' values are supported.  # noqa: E501

        :return: The usage_reports_access of this UpdateRole.  # noqa: E501
        :rtype: str
        """
        return self._usage_reports_access

    @usage_reports_access.setter
    def usage_reports_access(self, usage_reports_access):
        """Sets the usage_reports_access of this UpdateRole.

        Allow this role to view Usage Report. Currently only 'none' and 'all' values are supported.  # noqa: E501

        :param usage_reports_access: The usage_reports_access of this UpdateRole.  # noqa: E501
        :type: str
        """

        self._usage_reports_access = usage_reports_access

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, UpdateRole):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpdateRole):
            return True

        return self.to_dict() != other.to_dict()
