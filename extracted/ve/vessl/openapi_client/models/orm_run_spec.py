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


class OrmRunSpec(object):
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
        'cluster_id': 'int',
        'created_dt': 'datetime',
        'description': 'str',
        'edges': 'OrmRunSpecEdges',
        'id': 'int',
        'image_id': 'int',
        'immutable_slug': 'str',
        'organization_id': 'int',
        'resource_spec_preset_id': 'int',
        'spec': 'dict[str, object]',
        'title': 'str',
        'type': 'str',
        'updated_dt': 'datetime',
        'yaml': 'str'
    }

    attribute_map = {
        'cluster_id': 'cluster_id',
        'created_dt': 'created_dt',
        'description': 'description',
        'edges': 'edges',
        'id': 'id',
        'image_id': 'image_id',
        'immutable_slug': 'immutable_slug',
        'organization_id': 'organization_id',
        'resource_spec_preset_id': 'resource_spec_preset_id',
        'spec': 'spec',
        'title': 'title',
        'type': 'type',
        'updated_dt': 'updated_dt',
        'yaml': 'yaml'
    }

    def __init__(self, cluster_id=None, created_dt=None, description=None, edges=None, id=None, image_id=None, immutable_slug=None, organization_id=None, resource_spec_preset_id=None, spec=None, title=None, type=None, updated_dt=None, yaml=None, local_vars_configuration=None):  # noqa: E501
        """OrmRunSpec - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._cluster_id = None
        self._created_dt = None
        self._description = None
        self._edges = None
        self._id = None
        self._image_id = None
        self._immutable_slug = None
        self._organization_id = None
        self._resource_spec_preset_id = None
        self._spec = None
        self._title = None
        self._type = None
        self._updated_dt = None
        self._yaml = None
        self.discriminator = None

        if cluster_id is not None:
            self.cluster_id = cluster_id
        if created_dt is not None:
            self.created_dt = created_dt
        if description is not None:
            self.description = description
        if edges is not None:
            self.edges = edges
        if id is not None:
            self.id = id
        if image_id is not None:
            self.image_id = image_id
        if immutable_slug is not None:
            self.immutable_slug = immutable_slug
        if organization_id is not None:
            self.organization_id = organization_id
        self.resource_spec_preset_id = resource_spec_preset_id
        if spec is not None:
            self.spec = spec
        if title is not None:
            self.title = title
        if type is not None:
            self.type = type
        if updated_dt is not None:
            self.updated_dt = updated_dt
        self.yaml = yaml

    @property
    def cluster_id(self):
        """Gets the cluster_id of this OrmRunSpec.  # noqa: E501


        :return: The cluster_id of this OrmRunSpec.  # noqa: E501
        :rtype: int
        """
        return self._cluster_id

    @cluster_id.setter
    def cluster_id(self, cluster_id):
        """Sets the cluster_id of this OrmRunSpec.


        :param cluster_id: The cluster_id of this OrmRunSpec.  # noqa: E501
        :type cluster_id: int
        """

        self._cluster_id = cluster_id

    @property
    def created_dt(self):
        """Gets the created_dt of this OrmRunSpec.  # noqa: E501


        :return: The created_dt of this OrmRunSpec.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this OrmRunSpec.


        :param created_dt: The created_dt of this OrmRunSpec.  # noqa: E501
        :type created_dt: datetime
        """

        self._created_dt = created_dt

    @property
    def description(self):
        """Gets the description of this OrmRunSpec.  # noqa: E501


        :return: The description of this OrmRunSpec.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this OrmRunSpec.


        :param description: The description of this OrmRunSpec.  # noqa: E501
        :type description: str
        """

        self._description = description

    @property
    def edges(self):
        """Gets the edges of this OrmRunSpec.  # noqa: E501


        :return: The edges of this OrmRunSpec.  # noqa: E501
        :rtype: OrmRunSpecEdges
        """
        return self._edges

    @edges.setter
    def edges(self, edges):
        """Sets the edges of this OrmRunSpec.


        :param edges: The edges of this OrmRunSpec.  # noqa: E501
        :type edges: OrmRunSpecEdges
        """

        self._edges = edges

    @property
    def id(self):
        """Gets the id of this OrmRunSpec.  # noqa: E501


        :return: The id of this OrmRunSpec.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this OrmRunSpec.


        :param id: The id of this OrmRunSpec.  # noqa: E501
        :type id: int
        """

        self._id = id

    @property
    def image_id(self):
        """Gets the image_id of this OrmRunSpec.  # noqa: E501


        :return: The image_id of this OrmRunSpec.  # noqa: E501
        :rtype: int
        """
        return self._image_id

    @image_id.setter
    def image_id(self, image_id):
        """Sets the image_id of this OrmRunSpec.


        :param image_id: The image_id of this OrmRunSpec.  # noqa: E501
        :type image_id: int
        """

        self._image_id = image_id

    @property
    def immutable_slug(self):
        """Gets the immutable_slug of this OrmRunSpec.  # noqa: E501


        :return: The immutable_slug of this OrmRunSpec.  # noqa: E501
        :rtype: str
        """
        return self._immutable_slug

    @immutable_slug.setter
    def immutable_slug(self, immutable_slug):
        """Sets the immutable_slug of this OrmRunSpec.


        :param immutable_slug: The immutable_slug of this OrmRunSpec.  # noqa: E501
        :type immutable_slug: str
        """

        self._immutable_slug = immutable_slug

    @property
    def organization_id(self):
        """Gets the organization_id of this OrmRunSpec.  # noqa: E501


        :return: The organization_id of this OrmRunSpec.  # noqa: E501
        :rtype: int
        """
        return self._organization_id

    @organization_id.setter
    def organization_id(self, organization_id):
        """Sets the organization_id of this OrmRunSpec.


        :param organization_id: The organization_id of this OrmRunSpec.  # noqa: E501
        :type organization_id: int
        """

        self._organization_id = organization_id

    @property
    def resource_spec_preset_id(self):
        """Gets the resource_spec_preset_id of this OrmRunSpec.  # noqa: E501


        :return: The resource_spec_preset_id of this OrmRunSpec.  # noqa: E501
        :rtype: int
        """
        return self._resource_spec_preset_id

    @resource_spec_preset_id.setter
    def resource_spec_preset_id(self, resource_spec_preset_id):
        """Sets the resource_spec_preset_id of this OrmRunSpec.


        :param resource_spec_preset_id: The resource_spec_preset_id of this OrmRunSpec.  # noqa: E501
        :type resource_spec_preset_id: int
        """

        self._resource_spec_preset_id = resource_spec_preset_id

    @property
    def spec(self):
        """Gets the spec of this OrmRunSpec.  # noqa: E501


        :return: The spec of this OrmRunSpec.  # noqa: E501
        :rtype: dict[str, object]
        """
        return self._spec

    @spec.setter
    def spec(self, spec):
        """Sets the spec of this OrmRunSpec.


        :param spec: The spec of this OrmRunSpec.  # noqa: E501
        :type spec: dict[str, object]
        """

        self._spec = spec

    @property
    def title(self):
        """Gets the title of this OrmRunSpec.  # noqa: E501


        :return: The title of this OrmRunSpec.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this OrmRunSpec.


        :param title: The title of this OrmRunSpec.  # noqa: E501
        :type title: str
        """

        self._title = title

    @property
    def type(self):
        """Gets the type of this OrmRunSpec.  # noqa: E501


        :return: The type of this OrmRunSpec.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this OrmRunSpec.


        :param type: The type of this OrmRunSpec.  # noqa: E501
        :type type: str
        """

        self._type = type

    @property
    def updated_dt(self):
        """Gets the updated_dt of this OrmRunSpec.  # noqa: E501


        :return: The updated_dt of this OrmRunSpec.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_dt

    @updated_dt.setter
    def updated_dt(self, updated_dt):
        """Sets the updated_dt of this OrmRunSpec.


        :param updated_dt: The updated_dt of this OrmRunSpec.  # noqa: E501
        :type updated_dt: datetime
        """

        self._updated_dt = updated_dt

    @property
    def yaml(self):
        """Gets the yaml of this OrmRunSpec.  # noqa: E501


        :return: The yaml of this OrmRunSpec.  # noqa: E501
        :rtype: str
        """
        return self._yaml

    @yaml.setter
    def yaml(self, yaml):
        """Sets the yaml of this OrmRunSpec.


        :param yaml: The yaml of this OrmRunSpec.  # noqa: E501
        :type yaml: str
        """

        self._yaml = yaml

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
        if not isinstance(other, OrmRunSpec):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrmRunSpec):
            return True

        return self.to_dict() != other.to_dict()
