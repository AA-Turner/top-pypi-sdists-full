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


class InstrumentEventInstruction(object):
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
        'instrument_event_instruction_id': 'str',
        'portfolio_id': 'ResourceId',
        'instrument_event_id': 'str',
        'instruction_type': 'str',
        'election_key': 'str',
        'holding_id': 'int',
        'version': 'Version',
        'href': 'str',
        'links': 'list[Link]'
    }

    attribute_map = {
        'instrument_event_instruction_id': 'instrumentEventInstructionId',
        'portfolio_id': 'portfolioId',
        'instrument_event_id': 'instrumentEventId',
        'instruction_type': 'instructionType',
        'election_key': 'electionKey',
        'holding_id': 'holdingId',
        'version': 'version',
        'href': 'href',
        'links': 'links'
    }

    required_map = {
        'instrument_event_instruction_id': 'optional',
        'portfolio_id': 'optional',
        'instrument_event_id': 'optional',
        'instruction_type': 'optional',
        'election_key': 'optional',
        'holding_id': 'optional',
        'version': 'optional',
        'href': 'optional',
        'links': 'optional'
    }

    def __init__(self, instrument_event_instruction_id=None, portfolio_id=None, instrument_event_id=None, instruction_type=None, election_key=None, holding_id=None, version=None, href=None, links=None, local_vars_configuration=None):  # noqa: E501
        """InstrumentEventInstruction - a model defined in OpenAPI"
        
        :param instrument_event_instruction_id:  The unique identifier for this instruction
        :type instrument_event_instruction_id: str
        :param portfolio_id: 
        :type portfolio_id: lusid.ResourceId
        :param instrument_event_id:  The identifier of the instrument event being instructed
        :type instrument_event_id: str
        :param instruction_type:  The type of instruction (Ignore, ElectForPortfolio, ElectForHolding)
        :type instruction_type: str
        :param election_key:  For elected instructions, the key to be chosen
        :type election_key: str
        :param holding_id:  For holding instructions, the id of the holding for which the instruction will apply
        :type holding_id: int
        :param version: 
        :type version: lusid.Version
        :param href:  The uri for this version of this instruction
        :type href: str
        :param links: 
        :type links: list[lusid.Link]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._instrument_event_instruction_id = None
        self._portfolio_id = None
        self._instrument_event_id = None
        self._instruction_type = None
        self._election_key = None
        self._holding_id = None
        self._version = None
        self._href = None
        self._links = None
        self.discriminator = None

        self.instrument_event_instruction_id = instrument_event_instruction_id
        if portfolio_id is not None:
            self.portfolio_id = portfolio_id
        self.instrument_event_id = instrument_event_id
        self.instruction_type = instruction_type
        self.election_key = election_key
        self.holding_id = holding_id
        if version is not None:
            self.version = version
        self.href = href
        self.links = links

    @property
    def instrument_event_instruction_id(self):
        """Gets the instrument_event_instruction_id of this InstrumentEventInstruction.  # noqa: E501

        The unique identifier for this instruction  # noqa: E501

        :return: The instrument_event_instruction_id of this InstrumentEventInstruction.  # noqa: E501
        :rtype: str
        """
        return self._instrument_event_instruction_id

    @instrument_event_instruction_id.setter
    def instrument_event_instruction_id(self, instrument_event_instruction_id):
        """Sets the instrument_event_instruction_id of this InstrumentEventInstruction.

        The unique identifier for this instruction  # noqa: E501

        :param instrument_event_instruction_id: The instrument_event_instruction_id of this InstrumentEventInstruction.  # noqa: E501
        :type instrument_event_instruction_id: str
        """

        self._instrument_event_instruction_id = instrument_event_instruction_id

    @property
    def portfolio_id(self):
        """Gets the portfolio_id of this InstrumentEventInstruction.  # noqa: E501


        :return: The portfolio_id of this InstrumentEventInstruction.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._portfolio_id

    @portfolio_id.setter
    def portfolio_id(self, portfolio_id):
        """Sets the portfolio_id of this InstrumentEventInstruction.


        :param portfolio_id: The portfolio_id of this InstrumentEventInstruction.  # noqa: E501
        :type portfolio_id: lusid.ResourceId
        """

        self._portfolio_id = portfolio_id

    @property
    def instrument_event_id(self):
        """Gets the instrument_event_id of this InstrumentEventInstruction.  # noqa: E501

        The identifier of the instrument event being instructed  # noqa: E501

        :return: The instrument_event_id of this InstrumentEventInstruction.  # noqa: E501
        :rtype: str
        """
        return self._instrument_event_id

    @instrument_event_id.setter
    def instrument_event_id(self, instrument_event_id):
        """Sets the instrument_event_id of this InstrumentEventInstruction.

        The identifier of the instrument event being instructed  # noqa: E501

        :param instrument_event_id: The instrument_event_id of this InstrumentEventInstruction.  # noqa: E501
        :type instrument_event_id: str
        """

        self._instrument_event_id = instrument_event_id

    @property
    def instruction_type(self):
        """Gets the instruction_type of this InstrumentEventInstruction.  # noqa: E501

        The type of instruction (Ignore, ElectForPortfolio, ElectForHolding)  # noqa: E501

        :return: The instruction_type of this InstrumentEventInstruction.  # noqa: E501
        :rtype: str
        """
        return self._instruction_type

    @instruction_type.setter
    def instruction_type(self, instruction_type):
        """Sets the instruction_type of this InstrumentEventInstruction.

        The type of instruction (Ignore, ElectForPortfolio, ElectForHolding)  # noqa: E501

        :param instruction_type: The instruction_type of this InstrumentEventInstruction.  # noqa: E501
        :type instruction_type: str
        """

        self._instruction_type = instruction_type

    @property
    def election_key(self):
        """Gets the election_key of this InstrumentEventInstruction.  # noqa: E501

        For elected instructions, the key to be chosen  # noqa: E501

        :return: The election_key of this InstrumentEventInstruction.  # noqa: E501
        :rtype: str
        """
        return self._election_key

    @election_key.setter
    def election_key(self, election_key):
        """Sets the election_key of this InstrumentEventInstruction.

        For elected instructions, the key to be chosen  # noqa: E501

        :param election_key: The election_key of this InstrumentEventInstruction.  # noqa: E501
        :type election_key: str
        """

        self._election_key = election_key

    @property
    def holding_id(self):
        """Gets the holding_id of this InstrumentEventInstruction.  # noqa: E501

        For holding instructions, the id of the holding for which the instruction will apply  # noqa: E501

        :return: The holding_id of this InstrumentEventInstruction.  # noqa: E501
        :rtype: int
        """
        return self._holding_id

    @holding_id.setter
    def holding_id(self, holding_id):
        """Sets the holding_id of this InstrumentEventInstruction.

        For holding instructions, the id of the holding for which the instruction will apply  # noqa: E501

        :param holding_id: The holding_id of this InstrumentEventInstruction.  # noqa: E501
        :type holding_id: int
        """

        self._holding_id = holding_id

    @property
    def version(self):
        """Gets the version of this InstrumentEventInstruction.  # noqa: E501


        :return: The version of this InstrumentEventInstruction.  # noqa: E501
        :rtype: lusid.Version
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this InstrumentEventInstruction.


        :param version: The version of this InstrumentEventInstruction.  # noqa: E501
        :type version: lusid.Version
        """

        self._version = version

    @property
    def href(self):
        """Gets the href of this InstrumentEventInstruction.  # noqa: E501

        The uri for this version of this instruction  # noqa: E501

        :return: The href of this InstrumentEventInstruction.  # noqa: E501
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """Sets the href of this InstrumentEventInstruction.

        The uri for this version of this instruction  # noqa: E501

        :param href: The href of this InstrumentEventInstruction.  # noqa: E501
        :type href: str
        """

        self._href = href

    @property
    def links(self):
        """Gets the links of this InstrumentEventInstruction.  # noqa: E501


        :return: The links of this InstrumentEventInstruction.  # noqa: E501
        :rtype: list[lusid.Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this InstrumentEventInstruction.


        :param links: The links of this InstrumentEventInstruction.  # noqa: E501
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
        if not isinstance(other, InstrumentEventInstruction):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InstrumentEventInstruction):
            return True

        return self.to_dict() != other.to_dict()
