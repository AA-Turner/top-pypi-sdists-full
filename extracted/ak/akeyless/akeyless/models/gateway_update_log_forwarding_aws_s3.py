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


class GatewayUpdateLogForwardingAwsS3(object):
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
        'access_id': 'str',
        'access_key': 'str',
        'auth_type': 'str',
        'bucket_name': 'str',
        'enable': 'str',
        'json': 'bool',
        'log_folder': 'str',
        'output_format': 'str',
        'pull_interval': 'str',
        'region': 'str',
        'role_arn': 'str',
        'token': 'str',
        'uid_token': 'str'
    }

    attribute_map = {
        'access_id': 'access-id',
        'access_key': 'access-key',
        'auth_type': 'auth-type',
        'bucket_name': 'bucket-name',
        'enable': 'enable',
        'json': 'json',
        'log_folder': 'log-folder',
        'output_format': 'output-format',
        'pull_interval': 'pull-interval',
        'region': 'region',
        'role_arn': 'role-arn',
        'token': 'token',
        'uid_token': 'uid-token'
    }

    def __init__(self, access_id=None, access_key=None, auth_type=None, bucket_name=None, enable='true', json=False, log_folder='use-existing', output_format='text', pull_interval='10', region=None, role_arn=None, token=None, uid_token=None, local_vars_configuration=None):  # noqa: E501
        """GatewayUpdateLogForwardingAwsS3 - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._access_id = None
        self._access_key = None
        self._auth_type = None
        self._bucket_name = None
        self._enable = None
        self._json = None
        self._log_folder = None
        self._output_format = None
        self._pull_interval = None
        self._region = None
        self._role_arn = None
        self._token = None
        self._uid_token = None
        self.discriminator = None

        if access_id is not None:
            self.access_id = access_id
        if access_key is not None:
            self.access_key = access_key
        if auth_type is not None:
            self.auth_type = auth_type
        if bucket_name is not None:
            self.bucket_name = bucket_name
        if enable is not None:
            self.enable = enable
        if json is not None:
            self.json = json
        if log_folder is not None:
            self.log_folder = log_folder
        if output_format is not None:
            self.output_format = output_format
        if pull_interval is not None:
            self.pull_interval = pull_interval
        if region is not None:
            self.region = region
        if role_arn is not None:
            self.role_arn = role_arn
        if token is not None:
            self.token = token
        if uid_token is not None:
            self.uid_token = uid_token

    @property
    def access_id(self):
        """Gets the access_id of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501

        AWS access id relevant for access_key auth-type  # noqa: E501

        :return: The access_id of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :rtype: str
        """
        return self._access_id

    @access_id.setter
    def access_id(self, access_id):
        """Sets the access_id of this GatewayUpdateLogForwardingAwsS3.

        AWS access id relevant for access_key auth-type  # noqa: E501

        :param access_id: The access_id of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :type: str
        """

        self._access_id = access_id

    @property
    def access_key(self):
        """Gets the access_key of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501

        AWS access key relevant for access_key auth-type  # noqa: E501

        :return: The access_key of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :rtype: str
        """
        return self._access_key

    @access_key.setter
    def access_key(self, access_key):
        """Sets the access_key of this GatewayUpdateLogForwardingAwsS3.

        AWS access key relevant for access_key auth-type  # noqa: E501

        :param access_key: The access_key of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :type: str
        """

        self._access_key = access_key

    @property
    def auth_type(self):
        """Gets the auth_type of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501

        AWS auth type [access_key/cloud_id/assume_role]  # noqa: E501

        :return: The auth_type of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :rtype: str
        """
        return self._auth_type

    @auth_type.setter
    def auth_type(self, auth_type):
        """Sets the auth_type of this GatewayUpdateLogForwardingAwsS3.

        AWS auth type [access_key/cloud_id/assume_role]  # noqa: E501

        :param auth_type: The auth_type of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :type: str
        """

        self._auth_type = auth_type

    @property
    def bucket_name(self):
        """Gets the bucket_name of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501

        AWS S3 bucket name  # noqa: E501

        :return: The bucket_name of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :rtype: str
        """
        return self._bucket_name

    @bucket_name.setter
    def bucket_name(self, bucket_name):
        """Sets the bucket_name of this GatewayUpdateLogForwardingAwsS3.

        AWS S3 bucket name  # noqa: E501

        :param bucket_name: The bucket_name of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :type: str
        """

        self._bucket_name = bucket_name

    @property
    def enable(self):
        """Gets the enable of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501

        Enable Log Forwarding [true/false]  # noqa: E501

        :return: The enable of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :rtype: str
        """
        return self._enable

    @enable.setter
    def enable(self, enable):
        """Sets the enable of this GatewayUpdateLogForwardingAwsS3.

        Enable Log Forwarding [true/false]  # noqa: E501

        :param enable: The enable of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :type: str
        """

        self._enable = enable

    @property
    def json(self):
        """Gets the json of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501

        Set output format to JSON  # noqa: E501

        :return: The json of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :rtype: bool
        """
        return self._json

    @json.setter
    def json(self, json):
        """Sets the json of this GatewayUpdateLogForwardingAwsS3.

        Set output format to JSON  # noqa: E501

        :param json: The json of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :type: bool
        """

        self._json = json

    @property
    def log_folder(self):
        """Gets the log_folder of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501

        AWS S3 destination folder for logs  # noqa: E501

        :return: The log_folder of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :rtype: str
        """
        return self._log_folder

    @log_folder.setter
    def log_folder(self, log_folder):
        """Sets the log_folder of this GatewayUpdateLogForwardingAwsS3.

        AWS S3 destination folder for logs  # noqa: E501

        :param log_folder: The log_folder of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :type: str
        """

        self._log_folder = log_folder

    @property
    def output_format(self):
        """Gets the output_format of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501

        Logs format [text/json]  # noqa: E501

        :return: The output_format of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :rtype: str
        """
        return self._output_format

    @output_format.setter
    def output_format(self, output_format):
        """Sets the output_format of this GatewayUpdateLogForwardingAwsS3.

        Logs format [text/json]  # noqa: E501

        :param output_format: The output_format of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :type: str
        """

        self._output_format = output_format

    @property
    def pull_interval(self):
        """Gets the pull_interval of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501

        Pull interval in seconds  # noqa: E501

        :return: The pull_interval of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :rtype: str
        """
        return self._pull_interval

    @pull_interval.setter
    def pull_interval(self, pull_interval):
        """Sets the pull_interval of this GatewayUpdateLogForwardingAwsS3.

        Pull interval in seconds  # noqa: E501

        :param pull_interval: The pull_interval of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :type: str
        """

        self._pull_interval = pull_interval

    @property
    def region(self):
        """Gets the region of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501

        AWS region  # noqa: E501

        :return: The region of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :rtype: str
        """
        return self._region

    @region.setter
    def region(self, region):
        """Sets the region of this GatewayUpdateLogForwardingAwsS3.

        AWS region  # noqa: E501

        :param region: The region of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :type: str
        """

        self._region = region

    @property
    def role_arn(self):
        """Gets the role_arn of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501

        AWS role arn relevant for assume_role auth-type  # noqa: E501

        :return: The role_arn of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :rtype: str
        """
        return self._role_arn

    @role_arn.setter
    def role_arn(self, role_arn):
        """Sets the role_arn of this GatewayUpdateLogForwardingAwsS3.

        AWS role arn relevant for assume_role auth-type  # noqa: E501

        :param role_arn: The role_arn of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :type: str
        """

        self._role_arn = role_arn

    @property
    def token(self):
        """Gets the token of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :return: The token of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this GatewayUpdateLogForwardingAwsS3.

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :param token: The token of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def uid_token(self):
        """Gets the uid_token of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :return: The uid_token of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :rtype: str
        """
        return self._uid_token

    @uid_token.setter
    def uid_token(self, uid_token):
        """Sets the uid_token of this GatewayUpdateLogForwardingAwsS3.

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :param uid_token: The uid_token of this GatewayUpdateLogForwardingAwsS3.  # noqa: E501
        :type: str
        """

        self._uid_token = uid_token

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
        if not isinstance(other, GatewayUpdateLogForwardingAwsS3):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GatewayUpdateLogForwardingAwsS3):
            return True

        return self.to_dict() != other.to_dict()
