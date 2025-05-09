# coding: utf-8

"""
    Seeq REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 66.18.1-v202505080754-CD
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from pprint import pformat
from six import iteritems
import re


class SupportRequestInputV1(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
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
        'attachment': 'AttachmentInputV1',
        'attachment_for_jira': 'JiraAttachment',
        'description': 'str',
        'email': 'str',
        'frequency': 'str',
        'name': 'str',
        'severity': 'str',
        'steps_to_reproduce': 'str',
        'summary': 'str'
    }

    attribute_map = {
        'attachment': 'attachment',
        'attachment_for_jira': 'attachmentForJira',
        'description': 'description',
        'email': 'email',
        'frequency': 'frequency',
        'name': 'name',
        'severity': 'severity',
        'steps_to_reproduce': 'stepsToReproduce',
        'summary': 'summary'
    }

    def __init__(self, attachment=None, attachment_for_jira=None, description=None, email=None, frequency=None, name=None, severity=None, steps_to_reproduce=None, summary=None):
        """
        SupportRequestInputV1 - a model defined in Swagger
        """

        self._attachment = None
        self._attachment_for_jira = None
        self._description = None
        self._email = None
        self._frequency = None
        self._name = None
        self._severity = None
        self._steps_to_reproduce = None
        self._summary = None

        if attachment is not None:
          self.attachment = attachment
        if attachment_for_jira is not None:
          self.attachment_for_jira = attachment_for_jira
        if description is not None:
          self.description = description
        if email is not None:
          self.email = email
        if frequency is not None:
          self.frequency = frequency
        if name is not None:
          self.name = name
        if severity is not None:
          self.severity = severity
        if steps_to_reproduce is not None:
          self.steps_to_reproduce = steps_to_reproduce
        if summary is not None:
          self.summary = summary

    @property
    def attachment(self):
        """
        Gets the attachment of this SupportRequestInputV1.

        :return: The attachment of this SupportRequestInputV1.
        :rtype: AttachmentInputV1
        """
        return self._attachment

    @attachment.setter
    def attachment(self, attachment):
        """
        Sets the attachment of this SupportRequestInputV1.

        :param attachment: The attachment of this SupportRequestInputV1.
        :type: AttachmentInputV1
        """

        self._attachment = attachment

    @property
    def attachment_for_jira(self):
        """
        Gets the attachment_for_jira of this SupportRequestInputV1.

        :return: The attachment_for_jira of this SupportRequestInputV1.
        :rtype: JiraAttachment
        """
        return self._attachment_for_jira

    @attachment_for_jira.setter
    def attachment_for_jira(self, attachment_for_jira):
        """
        Sets the attachment_for_jira of this SupportRequestInputV1.

        :param attachment_for_jira: The attachment_for_jira of this SupportRequestInputV1.
        :type: JiraAttachment
        """

        self._attachment_for_jira = attachment_for_jira

    @property
    def description(self):
        """
        Gets the description of this SupportRequestInputV1.
        Additional details that can help the Support Team understand the problem or request

        :return: The description of this SupportRequestInputV1.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this SupportRequestInputV1.
        Additional details that can help the Support Team understand the problem or request

        :param description: The description of this SupportRequestInputV1.
        :type: str
        """
        if description is None:
            raise ValueError("Invalid value for `description`, must not be `None`")

        self._description = description

    @property
    def email(self):
        """
        Gets the email of this SupportRequestInputV1.
        The email address of the sender

        :return: The email of this SupportRequestInputV1.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """
        Sets the email of this SupportRequestInputV1.
        The email address of the sender

        :param email: The email of this SupportRequestInputV1.
        :type: str
        """
        if email is None:
            raise ValueError("Invalid value for `email`, must not be `None`")

        self._email = email

    @property
    def frequency(self):
        """
        Gets the frequency of this SupportRequestInputV1.
        The observed frequency of the problem

        :return: The frequency of this SupportRequestInputV1.
        :rtype: str
        """
        return self._frequency

    @frequency.setter
    def frequency(self, frequency):
        """
        Sets the frequency of this SupportRequestInputV1.
        The observed frequency of the problem

        :param frequency: The frequency of this SupportRequestInputV1.
        :type: str
        """
        if frequency is None:
            raise ValueError("Invalid value for `frequency`, must not be `None`")
        allowed_values = ["NotApplicable", "Once", "EveryTime", "Infrequently"]
        if frequency not in allowed_values:
            raise ValueError(
                "Invalid value for `frequency` ({0}), must be one of {1}"
                .format(frequency, allowed_values)
            )

        self._frequency = frequency

    @property
    def name(self):
        """
        Gets the name of this SupportRequestInputV1.
        The name of the sender

        :return: The name of this SupportRequestInputV1.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this SupportRequestInputV1.
        The name of the sender

        :param name: The name of this SupportRequestInputV1.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def severity(self):
        """
        Gets the severity of this SupportRequestInputV1.
        The severity level, S4 is the lowest and most common and S1 is the highest and for system down events

        :return: The severity of this SupportRequestInputV1.
        :rtype: str
        """
        return self._severity

    @severity.setter
    def severity(self, severity):
        """
        Sets the severity of this SupportRequestInputV1.
        The severity level, S4 is the lowest and most common and S1 is the highest and for system down events

        :param severity: The severity of this SupportRequestInputV1.
        :type: str
        """
        if severity is None:
            raise ValueError("Invalid value for `severity`, must not be `None`")
        allowed_values = ["S4", "S3", "S2", "S1"]
        if severity not in allowed_values:
            raise ValueError(
                "Invalid value for `severity` ({0}), must be one of {1}"
                .format(severity, allowed_values)
            )

        self._severity = severity

    @property
    def steps_to_reproduce(self):
        """
        Gets the steps_to_reproduce of this SupportRequestInputV1.
        The steps to reproduce the problem

        :return: The steps_to_reproduce of this SupportRequestInputV1.
        :rtype: str
        """
        return self._steps_to_reproduce

    @steps_to_reproduce.setter
    def steps_to_reproduce(self, steps_to_reproduce):
        """
        Sets the steps_to_reproduce of this SupportRequestInputV1.
        The steps to reproduce the problem

        :param steps_to_reproduce: The steps_to_reproduce of this SupportRequestInputV1.
        :type: str
        """

        self._steps_to_reproduce = steps_to_reproduce

    @property
    def summary(self):
        """
        Gets the summary of this SupportRequestInputV1.
        A one-line description of the problem or feature request

        :return: The summary of this SupportRequestInputV1.
        :rtype: str
        """
        return self._summary

    @summary.setter
    def summary(self, summary):
        """
        Sets the summary of this SupportRequestInputV1.
        A one-line description of the problem or feature request

        :param summary: The summary of this SupportRequestInputV1.
        :type: str
        """
        if summary is None:
            raise ValueError("Invalid value for `summary`, must not be `None`")

        self._summary = summary

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
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
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, SupportRequestInputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
