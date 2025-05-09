# coding: utf-8

"""
    external/v1/auth_service.proto

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: version not set
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git

    NOTE
    ----
    standard swagger-codegen-cli for this python client has been modified
    by custom templates. The purpose of these templates is to include
    typing information in the API and Model code. Please refer to the
    main grid repository for more info
"""

import pprint
import re  # noqa: F401

from typing import TYPE_CHECKING

import six

if TYPE_CHECKING:
    from datetime import datetime
    from lightning_cloud.openapi.models import *

class V1ListClustersResponse(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'clusters': 'list[Externalv1Cluster]',
        'default_cluster': 'str'
    }

    attribute_map = {
        'clusters': 'clusters',
        'default_cluster': 'defaultCluster'
    }

    def __init__(self, clusters: 'list[Externalv1Cluster]' =None, default_cluster: 'str' =None):  # noqa: E501
        """V1ListClustersResponse - a model defined in Swagger"""  # noqa: E501
        self._clusters = None
        self._default_cluster = None
        self.discriminator = None
        if clusters is not None:
            self.clusters = clusters
        if default_cluster is not None:
            self.default_cluster = default_cluster

    @property
    def clusters(self) -> 'list[Externalv1Cluster]':
        """Gets the clusters of this V1ListClustersResponse.  # noqa: E501


        :return: The clusters of this V1ListClustersResponse.  # noqa: E501
        :rtype: list[Externalv1Cluster]
        """
        return self._clusters

    @clusters.setter
    def clusters(self, clusters: 'list[Externalv1Cluster]'):
        """Sets the clusters of this V1ListClustersResponse.


        :param clusters: The clusters of this V1ListClustersResponse.  # noqa: E501
        :type: list[Externalv1Cluster]
        """

        self._clusters = clusters

    @property
    def default_cluster(self) -> 'str':
        """Gets the default_cluster of this V1ListClustersResponse.  # noqa: E501


        :return: The default_cluster of this V1ListClustersResponse.  # noqa: E501
        :rtype: str
        """
        return self._default_cluster

    @default_cluster.setter
    def default_cluster(self, default_cluster: 'str'):
        """Sets the default_cluster of this V1ListClustersResponse.


        :param default_cluster: The default_cluster of this V1ListClustersResponse.  # noqa: E501
        :type: str
        """

        self._default_cluster = default_cluster

    def to_dict(self) -> dict:
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(V1ListClustersResponse, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1ListClustersResponse') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1ListClustersResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1ListClustersResponse') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
