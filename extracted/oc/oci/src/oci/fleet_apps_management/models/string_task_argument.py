# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20250228

from .task_argument import TaskArgument
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class StringTaskArgument(TaskArgument):
    """
    A string variable that holds a value
    """

    def __init__(self, **kwargs):
        """
        Initializes a new StringTaskArgument object with values from keyword arguments. The default value of the :py:attr:`~oci.fleet_apps_management.models.StringTaskArgument.kind` attribute
        of this class is ``STRING`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param kind:
            The value to assign to the kind property of this StringTaskArgument.
            Allowed values for this property are: "STRING", "FILE"
        :type kind: str

        :param name:
            The value to assign to the name property of this StringTaskArgument.
        :type name: str

        :param value:
            The value to assign to the value property of this StringTaskArgument.
        :type value: str

        """
        self.swagger_types = {
            'kind': 'str',
            'name': 'str',
            'value': 'str'
        }
        self.attribute_map = {
            'kind': 'kind',
            'name': 'name',
            'value': 'value'
        }
        self._kind = None
        self._name = None
        self._value = None
        self._kind = 'STRING'

    @property
    def value(self):
        """
        Gets the value of this StringTaskArgument.
        The task input


        :return: The value of this StringTaskArgument.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this StringTaskArgument.
        The task input


        :param value: The value of this StringTaskArgument.
        :type: str
        """
        self._value = value

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
