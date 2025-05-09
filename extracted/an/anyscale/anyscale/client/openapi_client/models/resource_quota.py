# coding: utf-8

"""
    Managed Ray API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from openapi_client.configuration import Configuration


class ResourceQuota(object):
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
        'name': 'str',
        'cloud_id': 'str',
        'project_id': 'str',
        'user_id': 'str',
        'quota': 'Quota',
        'notification_channel': 'CreateNotificationChannelRecord',
        'is_soft_quota': 'bool',
        'id': 'str',
        'is_enabled': 'bool',
        'created_at': 'datetime',
        'deleted_at': 'datetime',
        'creator': 'MiniUser',
        'cloud': 'MiniCloud'
    }

    attribute_map = {
        'name': 'name',
        'cloud_id': 'cloud_id',
        'project_id': 'project_id',
        'user_id': 'user_id',
        'quota': 'quota',
        'notification_channel': 'notification_channel',
        'is_soft_quota': 'is_soft_quota',
        'id': 'id',
        'is_enabled': 'is_enabled',
        'created_at': 'created_at',
        'deleted_at': 'deleted_at',
        'creator': 'creator',
        'cloud': 'cloud'
    }

    def __init__(self, name=None, cloud_id=None, project_id=None, user_id=None, quota=None, notification_channel=None, is_soft_quota=False, id=None, is_enabled=True, created_at=None, deleted_at=None, creator=None, cloud=None, local_vars_configuration=None):  # noqa: E501
        """ResourceQuota - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._cloud_id = None
        self._project_id = None
        self._user_id = None
        self._quota = None
        self._notification_channel = None
        self._is_soft_quota = None
        self._id = None
        self._is_enabled = None
        self._created_at = None
        self._deleted_at = None
        self._creator = None
        self._cloud = None
        self.discriminator = None

        self.name = name
        self.cloud_id = cloud_id
        if project_id is not None:
            self.project_id = project_id
        if user_id is not None:
            self.user_id = user_id
        self.quota = quota
        if notification_channel is not None:
            self.notification_channel = notification_channel
        if is_soft_quota is not None:
            self.is_soft_quota = is_soft_quota
        self.id = id
        if is_enabled is not None:
            self.is_enabled = is_enabled
        self.created_at = created_at
        if deleted_at is not None:
            self.deleted_at = deleted_at
        self.creator = creator
        self.cloud = cloud

    @property
    def name(self):
        """Gets the name of this ResourceQuota.  # noqa: E501

        The name of this resource quota.  # noqa: E501

        :return: The name of this ResourceQuota.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ResourceQuota.

        The name of this resource quota.  # noqa: E501

        :param name: The name of this ResourceQuota.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def cloud_id(self):
        """Gets the cloud_id of this ResourceQuota.  # noqa: E501

        The ID of the cloud that this resource quota applies to.  # noqa: E501

        :return: The cloud_id of this ResourceQuota.  # noqa: E501
        :rtype: str
        """
        return self._cloud_id

    @cloud_id.setter
    def cloud_id(self, cloud_id):
        """Sets the cloud_id of this ResourceQuota.

        The ID of the cloud that this resource quota applies to.  # noqa: E501

        :param cloud_id: The cloud_id of this ResourceQuota.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and cloud_id is None:  # noqa: E501
            raise ValueError("Invalid value for `cloud_id`, must not be `None`")  # noqa: E501

        self._cloud_id = cloud_id

    @property
    def project_id(self):
        """Gets the project_id of this ResourceQuota.  # noqa: E501

        The ID of the project that this resource quota applies to.  # noqa: E501

        :return: The project_id of this ResourceQuota.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this ResourceQuota.

        The ID of the project that this resource quota applies to.  # noqa: E501

        :param project_id: The project_id of this ResourceQuota.  # noqa: E501
        :type: str
        """

        self._project_id = project_id

    @property
    def user_id(self):
        """Gets the user_id of this ResourceQuota.  # noqa: E501

        The ID of the user that this resource quota applies to.  # noqa: E501

        :return: The user_id of this ResourceQuota.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this ResourceQuota.

        The ID of the user that this resource quota applies to.  # noqa: E501

        :param user_id: The user_id of this ResourceQuota.  # noqa: E501
        :type: str
        """

        self._user_id = user_id

    @property
    def quota(self):
        """Gets the quota of this ResourceQuota.  # noqa: E501

        The quota limit.  # noqa: E501

        :return: The quota of this ResourceQuota.  # noqa: E501
        :rtype: Quota
        """
        return self._quota

    @quota.setter
    def quota(self, quota):
        """Sets the quota of this ResourceQuota.

        The quota limit.  # noqa: E501

        :param quota: The quota of this ResourceQuota.  # noqa: E501
        :type: Quota
        """
        if self.local_vars_configuration.client_side_validation and quota is None:  # noqa: E501
            raise ValueError("Invalid value for `quota`, must not be `None`")  # noqa: E501

        self._quota = quota

    @property
    def notification_channel(self):
        """Gets the notification_channel of this ResourceQuota.  # noqa: E501

        The notification channel that this resource quota sends notification to.  # noqa: E501

        :return: The notification_channel of this ResourceQuota.  # noqa: E501
        :rtype: CreateNotificationChannelRecord
        """
        return self._notification_channel

    @notification_channel.setter
    def notification_channel(self, notification_channel):
        """Sets the notification_channel of this ResourceQuota.

        The notification channel that this resource quota sends notification to.  # noqa: E501

        :param notification_channel: The notification_channel of this ResourceQuota.  # noqa: E501
        :type: CreateNotificationChannelRecord
        """

        self._notification_channel = notification_channel

    @property
    def is_soft_quota(self):
        """Gets the is_soft_quota of this ResourceQuota.  # noqa: E501

        Whether this resource quota is a soft quota. If the quota is a soft quota, the user will not be blocked from launching instances when the quota is exceeded.   # noqa: E501

        :return: The is_soft_quota of this ResourceQuota.  # noqa: E501
        :rtype: bool
        """
        return self._is_soft_quota

    @is_soft_quota.setter
    def is_soft_quota(self, is_soft_quota):
        """Sets the is_soft_quota of this ResourceQuota.

        Whether this resource quota is a soft quota. If the quota is a soft quota, the user will not be blocked from launching instances when the quota is exceeded.   # noqa: E501

        :param is_soft_quota: The is_soft_quota of this ResourceQuota.  # noqa: E501
        :type: bool
        """

        self._is_soft_quota = is_soft_quota

    @property
    def id(self):
        """Gets the id of this ResourceQuota.  # noqa: E501

        The ID of this resource quota.  # noqa: E501

        :return: The id of this ResourceQuota.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ResourceQuota.

        The ID of this resource quota.  # noqa: E501

        :param id: The id of this ResourceQuota.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def is_enabled(self):
        """Gets the is_enabled of this ResourceQuota.  # noqa: E501

        Whether this resource quota is enabled.  # noqa: E501

        :return: The is_enabled of this ResourceQuota.  # noqa: E501
        :rtype: bool
        """
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, is_enabled):
        """Sets the is_enabled of this ResourceQuota.

        Whether this resource quota is enabled.  # noqa: E501

        :param is_enabled: The is_enabled of this ResourceQuota.  # noqa: E501
        :type: bool
        """

        self._is_enabled = is_enabled

    @property
    def created_at(self):
        """Gets the created_at of this ResourceQuota.  # noqa: E501

        The timestamp when this resource quota was created.  # noqa: E501

        :return: The created_at of this ResourceQuota.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ResourceQuota.

        The timestamp when this resource quota was created.  # noqa: E501

        :param created_at: The created_at of this ResourceQuota.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_at is None:  # noqa: E501
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    @property
    def deleted_at(self):
        """Gets the deleted_at of this ResourceQuota.  # noqa: E501

        The timestamp when this resource quota was deleted.  # noqa: E501

        :return: The deleted_at of this ResourceQuota.  # noqa: E501
        :rtype: datetime
        """
        return self._deleted_at

    @deleted_at.setter
    def deleted_at(self, deleted_at):
        """Sets the deleted_at of this ResourceQuota.

        The timestamp when this resource quota was deleted.  # noqa: E501

        :param deleted_at: The deleted_at of this ResourceQuota.  # noqa: E501
        :type: datetime
        """

        self._deleted_at = deleted_at

    @property
    def creator(self):
        """Gets the creator of this ResourceQuota.  # noqa: E501

        The user that created this resource quota.  # noqa: E501

        :return: The creator of this ResourceQuota.  # noqa: E501
        :rtype: MiniUser
        """
        return self._creator

    @creator.setter
    def creator(self, creator):
        """Sets the creator of this ResourceQuota.

        The user that created this resource quota.  # noqa: E501

        :param creator: The creator of this ResourceQuota.  # noqa: E501
        :type: MiniUser
        """
        if self.local_vars_configuration.client_side_validation and creator is None:  # noqa: E501
            raise ValueError("Invalid value for `creator`, must not be `None`")  # noqa: E501

        self._creator = creator

    @property
    def cloud(self):
        """Gets the cloud of this ResourceQuota.  # noqa: E501

        The cloud that this resource quota applies to.  # noqa: E501

        :return: The cloud of this ResourceQuota.  # noqa: E501
        :rtype: MiniCloud
        """
        return self._cloud

    @cloud.setter
    def cloud(self, cloud):
        """Sets the cloud of this ResourceQuota.

        The cloud that this resource quota applies to.  # noqa: E501

        :param cloud: The cloud of this ResourceQuota.  # noqa: E501
        :type: MiniCloud
        """
        if self.local_vars_configuration.client_side_validation and cloud is None:  # noqa: E501
            raise ValueError("Invalid value for `cloud`, must not be `None`")  # noqa: E501

        self._cloud = cloud

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
        if not isinstance(other, ResourceQuota):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ResourceQuota):
            return True

        return self.to_dict() != other.to_dict()
