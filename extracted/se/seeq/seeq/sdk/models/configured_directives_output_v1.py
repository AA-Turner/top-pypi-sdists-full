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


class ConfiguredDirectivesOutputV1(object):
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
        'installers': 'list[InstallerOutputV1]',
        'run_version': 'str',
        'stage_installer': 'str'
    }

    attribute_map = {
        'installers': 'installers',
        'run_version': 'runVersion',
        'stage_installer': 'stageInstaller'
    }

    def __init__(self, installers=None, run_version=None, stage_installer=None):
        """
        ConfiguredDirectivesOutputV1 - a model defined in Swagger
        """

        self._installers = None
        self._run_version = None
        self._stage_installer = None

        if installers is not None:
          self.installers = installers
        if run_version is not None:
          self.run_version = run_version
        if stage_installer is not None:
          self.stage_installer = stage_installer

    @property
    def installers(self):
        """
        Gets the installers of this ConfiguredDirectivesOutputV1.
        List of installers

        :return: The installers of this ConfiguredDirectivesOutputV1.
        :rtype: list[InstallerOutputV1]
        """
        return self._installers

    @installers.setter
    def installers(self, installers):
        """
        Sets the installers of this ConfiguredDirectivesOutputV1.
        List of installers

        :param installers: The installers of this ConfiguredDirectivesOutputV1.
        :type: list[InstallerOutputV1]
        """

        self._installers = installers

    @property
    def run_version(self):
        """
        Gets the run_version of this ConfiguredDirectivesOutputV1.
        Run Version

        :return: The run_version of this ConfiguredDirectivesOutputV1.
        :rtype: str
        """
        return self._run_version

    @run_version.setter
    def run_version(self, run_version):
        """
        Sets the run_version of this ConfiguredDirectivesOutputV1.
        Run Version

        :param run_version: The run_version of this ConfiguredDirectivesOutputV1.
        :type: str
        """

        self._run_version = run_version

    @property
    def stage_installer(self):
        """
        Gets the stage_installer of this ConfiguredDirectivesOutputV1.
        Staged Installer

        :return: The stage_installer of this ConfiguredDirectivesOutputV1.
        :rtype: str
        """
        return self._stage_installer

    @stage_installer.setter
    def stage_installer(self, stage_installer):
        """
        Sets the stage_installer of this ConfiguredDirectivesOutputV1.
        Staged Installer

        :param stage_installer: The stage_installer of this ConfiguredDirectivesOutputV1.
        :type: str
        """

        self._stage_installer = stage_installer

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
        if not isinstance(other, ConfiguredDirectivesOutputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
