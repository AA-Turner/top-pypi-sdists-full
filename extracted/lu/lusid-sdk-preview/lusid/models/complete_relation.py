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


class CompleteRelation(object):
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
        'href': 'str',
        'version': 'Version',
        'relation_definition_id': 'ResourceId',
        'source_entity_id': 'dict(str, str)',
        'target_entity_id': 'dict(str, str)',
        'outward_description': 'str',
        'inward_description': 'str',
        'effective_from': 'datetime'
    }

    attribute_map = {
        'href': 'href',
        'version': 'version',
        'relation_definition_id': 'relationDefinitionId',
        'source_entity_id': 'sourceEntityId',
        'target_entity_id': 'targetEntityId',
        'outward_description': 'outwardDescription',
        'inward_description': 'inwardDescription',
        'effective_from': 'effectiveFrom'
    }

    required_map = {
        'href': 'optional',
        'version': 'optional',
        'relation_definition_id': 'required',
        'source_entity_id': 'required',
        'target_entity_id': 'required',
        'outward_description': 'required',
        'inward_description': 'required',
        'effective_from': 'optional'
    }

    def __init__(self, href=None, version=None, relation_definition_id=None, source_entity_id=None, target_entity_id=None, outward_description=None, inward_description=None, effective_from=None, local_vars_configuration=None):  # noqa: E501
        """CompleteRelation - a model defined in OpenAPI"
        
        :param href: 
        :type href: str
        :param version: 
        :type version: lusid.Version
        :param relation_definition_id:  (required)
        :type relation_definition_id: lusid.ResourceId
        :param source_entity_id:  (required)
        :type source_entity_id: dict(str, str)
        :param target_entity_id:  (required)
        :type target_entity_id: dict(str, str)
        :param outward_description:  (required)
        :type outward_description: str
        :param inward_description:  (required)
        :type inward_description: str
        :param effective_from: 
        :type effective_from: datetime

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._href = None
        self._version = None
        self._relation_definition_id = None
        self._source_entity_id = None
        self._target_entity_id = None
        self._outward_description = None
        self._inward_description = None
        self._effective_from = None
        self.discriminator = None

        self.href = href
        if version is not None:
            self.version = version
        self.relation_definition_id = relation_definition_id
        self.source_entity_id = source_entity_id
        self.target_entity_id = target_entity_id
        self.outward_description = outward_description
        self.inward_description = inward_description
        if effective_from is not None:
            self.effective_from = effective_from

    @property
    def href(self):
        """Gets the href of this CompleteRelation.  # noqa: E501


        :return: The href of this CompleteRelation.  # noqa: E501
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """Sets the href of this CompleteRelation.


        :param href: The href of this CompleteRelation.  # noqa: E501
        :type href: str
        """

        self._href = href

    @property
    def version(self):
        """Gets the version of this CompleteRelation.  # noqa: E501


        :return: The version of this CompleteRelation.  # noqa: E501
        :rtype: lusid.Version
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this CompleteRelation.


        :param version: The version of this CompleteRelation.  # noqa: E501
        :type version: lusid.Version
        """

        self._version = version

    @property
    def relation_definition_id(self):
        """Gets the relation_definition_id of this CompleteRelation.  # noqa: E501


        :return: The relation_definition_id of this CompleteRelation.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._relation_definition_id

    @relation_definition_id.setter
    def relation_definition_id(self, relation_definition_id):
        """Sets the relation_definition_id of this CompleteRelation.


        :param relation_definition_id: The relation_definition_id of this CompleteRelation.  # noqa: E501
        :type relation_definition_id: lusid.ResourceId
        """
        if self.local_vars_configuration.client_side_validation and relation_definition_id is None:  # noqa: E501
            raise ValueError("Invalid value for `relation_definition_id`, must not be `None`")  # noqa: E501

        self._relation_definition_id = relation_definition_id

    @property
    def source_entity_id(self):
        """Gets the source_entity_id of this CompleteRelation.  # noqa: E501


        :return: The source_entity_id of this CompleteRelation.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._source_entity_id

    @source_entity_id.setter
    def source_entity_id(self, source_entity_id):
        """Sets the source_entity_id of this CompleteRelation.


        :param source_entity_id: The source_entity_id of this CompleteRelation.  # noqa: E501
        :type source_entity_id: dict(str, str)
        """
        if self.local_vars_configuration.client_side_validation and source_entity_id is None:  # noqa: E501
            raise ValueError("Invalid value for `source_entity_id`, must not be `None`")  # noqa: E501

        self._source_entity_id = source_entity_id

    @property
    def target_entity_id(self):
        """Gets the target_entity_id of this CompleteRelation.  # noqa: E501


        :return: The target_entity_id of this CompleteRelation.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._target_entity_id

    @target_entity_id.setter
    def target_entity_id(self, target_entity_id):
        """Sets the target_entity_id of this CompleteRelation.


        :param target_entity_id: The target_entity_id of this CompleteRelation.  # noqa: E501
        :type target_entity_id: dict(str, str)
        """
        if self.local_vars_configuration.client_side_validation and target_entity_id is None:  # noqa: E501
            raise ValueError("Invalid value for `target_entity_id`, must not be `None`")  # noqa: E501

        self._target_entity_id = target_entity_id

    @property
    def outward_description(self):
        """Gets the outward_description of this CompleteRelation.  # noqa: E501


        :return: The outward_description of this CompleteRelation.  # noqa: E501
        :rtype: str
        """
        return self._outward_description

    @outward_description.setter
    def outward_description(self, outward_description):
        """Sets the outward_description of this CompleteRelation.


        :param outward_description: The outward_description of this CompleteRelation.  # noqa: E501
        :type outward_description: str
        """
        if self.local_vars_configuration.client_side_validation and outward_description is None:  # noqa: E501
            raise ValueError("Invalid value for `outward_description`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                outward_description is not None and len(outward_description) < 1):
            raise ValueError("Invalid value for `outward_description`, length must be greater than or equal to `1`")  # noqa: E501

        self._outward_description = outward_description

    @property
    def inward_description(self):
        """Gets the inward_description of this CompleteRelation.  # noqa: E501


        :return: The inward_description of this CompleteRelation.  # noqa: E501
        :rtype: str
        """
        return self._inward_description

    @inward_description.setter
    def inward_description(self, inward_description):
        """Sets the inward_description of this CompleteRelation.


        :param inward_description: The inward_description of this CompleteRelation.  # noqa: E501
        :type inward_description: str
        """
        if self.local_vars_configuration.client_side_validation and inward_description is None:  # noqa: E501
            raise ValueError("Invalid value for `inward_description`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                inward_description is not None and len(inward_description) < 1):
            raise ValueError("Invalid value for `inward_description`, length must be greater than or equal to `1`")  # noqa: E501

        self._inward_description = inward_description

    @property
    def effective_from(self):
        """Gets the effective_from of this CompleteRelation.  # noqa: E501


        :return: The effective_from of this CompleteRelation.  # noqa: E501
        :rtype: datetime
        """
        return self._effective_from

    @effective_from.setter
    def effective_from(self, effective_from):
        """Sets the effective_from of this CompleteRelation.


        :param effective_from: The effective_from of this CompleteRelation.  # noqa: E501
        :type effective_from: datetime
        """

        self._effective_from = effective_from

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
        if not isinstance(other, CompleteRelation):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CompleteRelation):
            return True

        return self.to_dict() != other.to_dict()
