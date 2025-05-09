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


class CloudDataBucketPresignedUploadInfo(object):
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
        'file_uri': 'str',
        'upload_url': 'str',
        'upload_scheme': 'CloudDataBucketPresignedUploadScheme',
        'file_exists': 'bool',
        'bucket_name': 'str',
        'bucket_path': 'str'
    }

    attribute_map = {
        'file_uri': 'file_uri',
        'upload_url': 'upload_url',
        'upload_scheme': 'upload_scheme',
        'file_exists': 'file_exists',
        'bucket_name': 'bucket_name',
        'bucket_path': 'bucket_path'
    }

    def __init__(self, file_uri=None, upload_url=None, upload_scheme=None, file_exists=None, bucket_name=None, bucket_path=None, local_vars_configuration=None):  # noqa: E501
        """CloudDataBucketPresignedUploadInfo - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._file_uri = None
        self._upload_url = None
        self._upload_scheme = None
        self._file_exists = None
        self._bucket_name = None
        self._bucket_path = None
        self.discriminator = None

        self.file_uri = file_uri
        self.upload_url = upload_url
        self.upload_scheme = upload_scheme
        self.file_exists = file_exists
        self.bucket_name = bucket_name
        self.bucket_path = bucket_path

    @property
    def file_uri(self):
        """Gets the file_uri of this CloudDataBucketPresignedUploadInfo.  # noqa: E501

        The fully-qualified path to the file in the cloud data bucket (e.g. 's3://anyscale-production-data-cld-123/org_id/cloud_id/runtime_env_packages/job_id.zip').  # noqa: E501

        :return: The file_uri of this CloudDataBucketPresignedUploadInfo.  # noqa: E501
        :rtype: str
        """
        return self._file_uri

    @file_uri.setter
    def file_uri(self, file_uri):
        """Sets the file_uri of this CloudDataBucketPresignedUploadInfo.

        The fully-qualified path to the file in the cloud data bucket (e.g. 's3://anyscale-production-data-cld-123/org_id/cloud_id/runtime_env_packages/job_id.zip').  # noqa: E501

        :param file_uri: The file_uri of this CloudDataBucketPresignedUploadInfo.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and file_uri is None:  # noqa: E501
            raise ValueError("Invalid value for `file_uri`, must not be `None`")  # noqa: E501

        self._file_uri = file_uri

    @property
    def upload_url(self):
        """Gets the upload_url of this CloudDataBucketPresignedUploadInfo.  # noqa: E501

        The presigned URL to use for uploading the file to the cloud data bucket.  # noqa: E501

        :return: The upload_url of this CloudDataBucketPresignedUploadInfo.  # noqa: E501
        :rtype: str
        """
        return self._upload_url

    @upload_url.setter
    def upload_url(self, upload_url):
        """Sets the upload_url of this CloudDataBucketPresignedUploadInfo.

        The presigned URL to use for uploading the file to the cloud data bucket.  # noqa: E501

        :param upload_url: The upload_url of this CloudDataBucketPresignedUploadInfo.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and upload_url is None:  # noqa: E501
            raise ValueError("Invalid value for `upload_url`, must not be `None`")  # noqa: E501

        self._upload_url = upload_url

    @property
    def upload_scheme(self):
        """Gets the upload_scheme of this CloudDataBucketPresignedUploadInfo.  # noqa: E501

        The scheme of the upload URL for uploading the file to the cloud data bucket.  # noqa: E501

        :return: The upload_scheme of this CloudDataBucketPresignedUploadInfo.  # noqa: E501
        :rtype: CloudDataBucketPresignedUploadScheme
        """
        return self._upload_scheme

    @upload_scheme.setter
    def upload_scheme(self, upload_scheme):
        """Sets the upload_scheme of this CloudDataBucketPresignedUploadInfo.

        The scheme of the upload URL for uploading the file to the cloud data bucket.  # noqa: E501

        :param upload_scheme: The upload_scheme of this CloudDataBucketPresignedUploadInfo.  # noqa: E501
        :type: CloudDataBucketPresignedUploadScheme
        """
        if self.local_vars_configuration.client_side_validation and upload_scheme is None:  # noqa: E501
            raise ValueError("Invalid value for `upload_scheme`, must not be `None`")  # noqa: E501

        self._upload_scheme = upload_scheme

    @property
    def file_exists(self):
        """Gets the file_exists of this CloudDataBucketPresignedUploadInfo.  # noqa: E501

        Whether or not an object under the returned URI already exists.  # noqa: E501

        :return: The file_exists of this CloudDataBucketPresignedUploadInfo.  # noqa: E501
        :rtype: bool
        """
        return self._file_exists

    @file_exists.setter
    def file_exists(self, file_exists):
        """Sets the file_exists of this CloudDataBucketPresignedUploadInfo.

        Whether or not an object under the returned URI already exists.  # noqa: E501

        :param file_exists: The file_exists of this CloudDataBucketPresignedUploadInfo.  # noqa: E501
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and file_exists is None:  # noqa: E501
            raise ValueError("Invalid value for `file_exists`, must not be `None`")  # noqa: E501

        self._file_exists = file_exists

    @property
    def bucket_name(self):
        """Gets the bucket_name of this CloudDataBucketPresignedUploadInfo.  # noqa: E501

        The name of the cloud data bucket where the file will be uploaded (e.g. 'anyscale-production-data-cld-123').  # noqa: E501

        :return: The bucket_name of this CloudDataBucketPresignedUploadInfo.  # noqa: E501
        :rtype: str
        """
        return self._bucket_name

    @bucket_name.setter
    def bucket_name(self, bucket_name):
        """Sets the bucket_name of this CloudDataBucketPresignedUploadInfo.

        The name of the cloud data bucket where the file will be uploaded (e.g. 'anyscale-production-data-cld-123').  # noqa: E501

        :param bucket_name: The bucket_name of this CloudDataBucketPresignedUploadInfo.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and bucket_name is None:  # noqa: E501
            raise ValueError("Invalid value for `bucket_name`, must not be `None`")  # noqa: E501

        self._bucket_name = bucket_name

    @property
    def bucket_path(self):
        """Gets the bucket_path of this CloudDataBucketPresignedUploadInfo.  # noqa: E501

        The path to the file in the cloud data bucket (e.g. 'org_id/cloud_id/runtime_env_packages/job_id.zip').  # noqa: E501

        :return: The bucket_path of this CloudDataBucketPresignedUploadInfo.  # noqa: E501
        :rtype: str
        """
        return self._bucket_path

    @bucket_path.setter
    def bucket_path(self, bucket_path):
        """Sets the bucket_path of this CloudDataBucketPresignedUploadInfo.

        The path to the file in the cloud data bucket (e.g. 'org_id/cloud_id/runtime_env_packages/job_id.zip').  # noqa: E501

        :param bucket_path: The bucket_path of this CloudDataBucketPresignedUploadInfo.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and bucket_path is None:  # noqa: E501
            raise ValueError("Invalid value for `bucket_path`, must not be `None`")  # noqa: E501

        self._bucket_path = bucket_path

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
        if not isinstance(other, CloudDataBucketPresignedUploadInfo):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CloudDataBucketPresignedUploadInfo):
            return True

        return self.to_dict() != other.to_dict()
