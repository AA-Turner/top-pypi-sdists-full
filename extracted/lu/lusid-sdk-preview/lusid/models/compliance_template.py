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


class ComplianceTemplate(object):
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
        'id': 'ResourceId',
        'description': 'str',
        'tags': 'list[str]',
        'variations': 'list[ComplianceTemplateVariation]',
        'links': 'list[Link]'
    }

    attribute_map = {
        'id': 'id',
        'description': 'description',
        'tags': 'tags',
        'variations': 'variations',
        'links': 'links'
    }

    required_map = {
        'id': 'required',
        'description': 'required',
        'tags': 'optional',
        'variations': 'required',
        'links': 'optional'
    }

    def __init__(self, id=None, description=None, tags=None, variations=None, links=None, local_vars_configuration=None):  # noqa: E501
        """ComplianceTemplate - a model defined in OpenAPI"
        
        :param id:  (required)
        :type id: lusid.ResourceId
        :param description:  The description of the Compliance Template (required)
        :type description: str
        :param tags:  Tags for a Compliance Template
        :type tags: list[str]
        :param variations:  Variation details of a Compliance Template (required)
        :type variations: list[lusid.ComplianceTemplateVariation]
        :param links: 
        :type links: list[lusid.Link]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._description = None
        self._tags = None
        self._variations = None
        self._links = None
        self.discriminator = None

        self.id = id
        self.description = description
        self.tags = tags
        self.variations = variations
        self.links = links

    @property
    def id(self):
        """Gets the id of this ComplianceTemplate.  # noqa: E501


        :return: The id of this ComplianceTemplate.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ComplianceTemplate.


        :param id: The id of this ComplianceTemplate.  # noqa: E501
        :type id: lusid.ResourceId
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def description(self):
        """Gets the description of this ComplianceTemplate.  # noqa: E501

        The description of the Compliance Template  # noqa: E501

        :return: The description of this ComplianceTemplate.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ComplianceTemplate.

        The description of the Compliance Template  # noqa: E501

        :param description: The description of this ComplianceTemplate.  # noqa: E501
        :type description: str
        """
        if self.local_vars_configuration.client_side_validation and description is None:  # noqa: E501
            raise ValueError("Invalid value for `description`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) < 1):
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `1`")  # noqa: E501

        self._description = description

    @property
    def tags(self):
        """Gets the tags of this ComplianceTemplate.  # noqa: E501

        Tags for a Compliance Template  # noqa: E501

        :return: The tags of this ComplianceTemplate.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this ComplianceTemplate.

        Tags for a Compliance Template  # noqa: E501

        :param tags: The tags of this ComplianceTemplate.  # noqa: E501
        :type tags: list[str]
        """

        self._tags = tags

    @property
    def variations(self):
        """Gets the variations of this ComplianceTemplate.  # noqa: E501

        Variation details of a Compliance Template  # noqa: E501

        :return: The variations of this ComplianceTemplate.  # noqa: E501
        :rtype: list[lusid.ComplianceTemplateVariation]
        """
        return self._variations

    @variations.setter
    def variations(self, variations):
        """Sets the variations of this ComplianceTemplate.

        Variation details of a Compliance Template  # noqa: E501

        :param variations: The variations of this ComplianceTemplate.  # noqa: E501
        :type variations: list[lusid.ComplianceTemplateVariation]
        """
        if self.local_vars_configuration.client_side_validation and variations is None:  # noqa: E501
            raise ValueError("Invalid value for `variations`, must not be `None`")  # noqa: E501

        self._variations = variations

    @property
    def links(self):
        """Gets the links of this ComplianceTemplate.  # noqa: E501


        :return: The links of this ComplianceTemplate.  # noqa: E501
        :rtype: list[lusid.Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this ComplianceTemplate.


        :param links: The links of this ComplianceTemplate.  # noqa: E501
        :type links: list[lusid.Link]
        """

        self._links = links

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
        if not isinstance(other, ComplianceTemplate):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ComplianceTemplate):
            return True

        return self.to_dict() != other.to_dict()
