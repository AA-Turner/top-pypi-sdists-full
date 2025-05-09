# coding: utf-8

"""
    Aron API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from openapi_client.configuration import Configuration


class ClientconfigFrontendConfigResponse(object):
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
        'cluster_create_enabled': 'bool',
        'google_client_id': 'str',
        'google_recaptcha_site_key': 'str',
        'model_enabled': 'bool',
        'serverless_service_enabled': 'bool',
        'signup_enabled': 'bool',
        'vessl_storage_enabled': 'bool'
    }

    attribute_map = {
        'cluster_create_enabled': 'cluster_create_enabled',
        'google_client_id': 'google_client_id',
        'google_recaptcha_site_key': 'google_recaptcha_site_key',
        'model_enabled': 'model_enabled',
        'serverless_service_enabled': 'serverless_service_enabled',
        'signup_enabled': 'signup_enabled',
        'vessl_storage_enabled': 'vessl_storage_enabled'
    }

    def __init__(self, cluster_create_enabled=None, google_client_id=None, google_recaptcha_site_key=None, model_enabled=None, serverless_service_enabled=None, signup_enabled=None, vessl_storage_enabled=None, local_vars_configuration=None):  # noqa: E501
        """ClientconfigFrontendConfigResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._cluster_create_enabled = None
        self._google_client_id = None
        self._google_recaptcha_site_key = None
        self._model_enabled = None
        self._serverless_service_enabled = None
        self._signup_enabled = None
        self._vessl_storage_enabled = None
        self.discriminator = None

        self.cluster_create_enabled = cluster_create_enabled
        self.google_client_id = google_client_id
        self.google_recaptcha_site_key = google_recaptcha_site_key
        self.model_enabled = model_enabled
        self.serverless_service_enabled = serverless_service_enabled
        self.signup_enabled = signup_enabled
        self.vessl_storage_enabled = vessl_storage_enabled

    @property
    def cluster_create_enabled(self):
        """Gets the cluster_create_enabled of this ClientconfigFrontendConfigResponse.  # noqa: E501


        :return: The cluster_create_enabled of this ClientconfigFrontendConfigResponse.  # noqa: E501
        :rtype: bool
        """
        return self._cluster_create_enabled

    @cluster_create_enabled.setter
    def cluster_create_enabled(self, cluster_create_enabled):
        """Sets the cluster_create_enabled of this ClientconfigFrontendConfigResponse.


        :param cluster_create_enabled: The cluster_create_enabled of this ClientconfigFrontendConfigResponse.  # noqa: E501
        :type cluster_create_enabled: bool
        """
        if self.local_vars_configuration.client_side_validation and cluster_create_enabled is None:  # noqa: E501
            raise ValueError("Invalid value for `cluster_create_enabled`, must not be `None`")  # noqa: E501

        self._cluster_create_enabled = cluster_create_enabled

    @property
    def google_client_id(self):
        """Gets the google_client_id of this ClientconfigFrontendConfigResponse.  # noqa: E501


        :return: The google_client_id of this ClientconfigFrontendConfigResponse.  # noqa: E501
        :rtype: str
        """
        return self._google_client_id

    @google_client_id.setter
    def google_client_id(self, google_client_id):
        """Sets the google_client_id of this ClientconfigFrontendConfigResponse.


        :param google_client_id: The google_client_id of this ClientconfigFrontendConfigResponse.  # noqa: E501
        :type google_client_id: str
        """
        if self.local_vars_configuration.client_side_validation and google_client_id is None:  # noqa: E501
            raise ValueError("Invalid value for `google_client_id`, must not be `None`")  # noqa: E501

        self._google_client_id = google_client_id

    @property
    def google_recaptcha_site_key(self):
        """Gets the google_recaptcha_site_key of this ClientconfigFrontendConfigResponse.  # noqa: E501


        :return: The google_recaptcha_site_key of this ClientconfigFrontendConfigResponse.  # noqa: E501
        :rtype: str
        """
        return self._google_recaptcha_site_key

    @google_recaptcha_site_key.setter
    def google_recaptcha_site_key(self, google_recaptcha_site_key):
        """Sets the google_recaptcha_site_key of this ClientconfigFrontendConfigResponse.


        :param google_recaptcha_site_key: The google_recaptcha_site_key of this ClientconfigFrontendConfigResponse.  # noqa: E501
        :type google_recaptcha_site_key: str
        """
        if self.local_vars_configuration.client_side_validation and google_recaptcha_site_key is None:  # noqa: E501
            raise ValueError("Invalid value for `google_recaptcha_site_key`, must not be `None`")  # noqa: E501

        self._google_recaptcha_site_key = google_recaptcha_site_key

    @property
    def model_enabled(self):
        """Gets the model_enabled of this ClientconfigFrontendConfigResponse.  # noqa: E501


        :return: The model_enabled of this ClientconfigFrontendConfigResponse.  # noqa: E501
        :rtype: bool
        """
        return self._model_enabled

    @model_enabled.setter
    def model_enabled(self, model_enabled):
        """Sets the model_enabled of this ClientconfigFrontendConfigResponse.


        :param model_enabled: The model_enabled of this ClientconfigFrontendConfigResponse.  # noqa: E501
        :type model_enabled: bool
        """
        if self.local_vars_configuration.client_side_validation and model_enabled is None:  # noqa: E501
            raise ValueError("Invalid value for `model_enabled`, must not be `None`")  # noqa: E501

        self._model_enabled = model_enabled

    @property
    def serverless_service_enabled(self):
        """Gets the serverless_service_enabled of this ClientconfigFrontendConfigResponse.  # noqa: E501


        :return: The serverless_service_enabled of this ClientconfigFrontendConfigResponse.  # noqa: E501
        :rtype: bool
        """
        return self._serverless_service_enabled

    @serverless_service_enabled.setter
    def serverless_service_enabled(self, serverless_service_enabled):
        """Sets the serverless_service_enabled of this ClientconfigFrontendConfigResponse.


        :param serverless_service_enabled: The serverless_service_enabled of this ClientconfigFrontendConfigResponse.  # noqa: E501
        :type serverless_service_enabled: bool
        """
        if self.local_vars_configuration.client_side_validation and serverless_service_enabled is None:  # noqa: E501
            raise ValueError("Invalid value for `serverless_service_enabled`, must not be `None`")  # noqa: E501

        self._serverless_service_enabled = serverless_service_enabled

    @property
    def signup_enabled(self):
        """Gets the signup_enabled of this ClientconfigFrontendConfigResponse.  # noqa: E501


        :return: The signup_enabled of this ClientconfigFrontendConfigResponse.  # noqa: E501
        :rtype: bool
        """
        return self._signup_enabled

    @signup_enabled.setter
    def signup_enabled(self, signup_enabled):
        """Sets the signup_enabled of this ClientconfigFrontendConfigResponse.


        :param signup_enabled: The signup_enabled of this ClientconfigFrontendConfigResponse.  # noqa: E501
        :type signup_enabled: bool
        """
        if self.local_vars_configuration.client_side_validation and signup_enabled is None:  # noqa: E501
            raise ValueError("Invalid value for `signup_enabled`, must not be `None`")  # noqa: E501

        self._signup_enabled = signup_enabled

    @property
    def vessl_storage_enabled(self):
        """Gets the vessl_storage_enabled of this ClientconfigFrontendConfigResponse.  # noqa: E501


        :return: The vessl_storage_enabled of this ClientconfigFrontendConfigResponse.  # noqa: E501
        :rtype: bool
        """
        return self._vessl_storage_enabled

    @vessl_storage_enabled.setter
    def vessl_storage_enabled(self, vessl_storage_enabled):
        """Sets the vessl_storage_enabled of this ClientconfigFrontendConfigResponse.


        :param vessl_storage_enabled: The vessl_storage_enabled of this ClientconfigFrontendConfigResponse.  # noqa: E501
        :type vessl_storage_enabled: bool
        """
        if self.local_vars_configuration.client_side_validation and vessl_storage_enabled is None:  # noqa: E501
            raise ValueError("Invalid value for `vessl_storage_enabled`, must not be `None`")  # noqa: E501

        self._vessl_storage_enabled = vessl_storage_enabled

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
        if not isinstance(other, ClientconfigFrontendConfigResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ClientconfigFrontendConfigResponse):
            return True

        return self.to_dict() != other.to_dict()
