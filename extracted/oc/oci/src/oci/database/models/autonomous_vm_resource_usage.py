# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20160918


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AutonomousVmResourceUsage(object):
    """
    Autonomous VM usage statistics.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AutonomousVmResourceUsage object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this AutonomousVmResourceUsage.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this AutonomousVmResourceUsage.
        :type display_name: str

        :param used_cpus:
            The value to assign to the used_cpus property of this AutonomousVmResourceUsage.
        :type used_cpus: float

        :param available_cpus:
            The value to assign to the available_cpus property of this AutonomousVmResourceUsage.
        :type available_cpus: float

        :param reclaimable_cpus:
            The value to assign to the reclaimable_cpus property of this AutonomousVmResourceUsage.
        :type reclaimable_cpus: float

        :param provisioned_cpus:
            The value to assign to the provisioned_cpus property of this AutonomousVmResourceUsage.
        :type provisioned_cpus: float

        :param reserved_cpus:
            The value to assign to the reserved_cpus property of this AutonomousVmResourceUsage.
        :type reserved_cpus: float

        :param autonomous_container_database_usage:
            The value to assign to the autonomous_container_database_usage property of this AutonomousVmResourceUsage.
        :type autonomous_container_database_usage: list[oci.database.models.AvmAcdResourceStats]

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'used_cpus': 'float',
            'available_cpus': 'float',
            'reclaimable_cpus': 'float',
            'provisioned_cpus': 'float',
            'reserved_cpus': 'float',
            'autonomous_container_database_usage': 'list[AvmAcdResourceStats]'
        }
        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'used_cpus': 'usedCpus',
            'available_cpus': 'availableCpus',
            'reclaimable_cpus': 'reclaimableCpus',
            'provisioned_cpus': 'provisionedCpus',
            'reserved_cpus': 'reservedCpus',
            'autonomous_container_database_usage': 'autonomousContainerDatabaseUsage'
        }
        self._id = None
        self._display_name = None
        self._used_cpus = None
        self._available_cpus = None
        self._reclaimable_cpus = None
        self._provisioned_cpus = None
        self._reserved_cpus = None
        self._autonomous_container_database_usage = None

    @property
    def id(self):
        """
        Gets the id of this AutonomousVmResourceUsage.
        The `OCID`__ of the Autonomous VM Cluster.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this AutonomousVmResourceUsage.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this AutonomousVmResourceUsage.
        The `OCID`__ of the Autonomous VM Cluster.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this AutonomousVmResourceUsage.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this AutonomousVmResourceUsage.
        The user-friendly name for the Autonomous VM cluster. The name does not need to be unique.


        :return: The display_name of this AutonomousVmResourceUsage.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this AutonomousVmResourceUsage.
        The user-friendly name for the Autonomous VM cluster. The name does not need to be unique.


        :param display_name: The display_name of this AutonomousVmResourceUsage.
        :type: str
        """
        self._display_name = display_name

    @property
    def used_cpus(self):
        """
        Gets the used_cpus of this AutonomousVmResourceUsage.
        The number of CPU cores alloted to the Autonomous Container Databases in an Cloud Autonomous VM cluster.


        :return: The used_cpus of this AutonomousVmResourceUsage.
        :rtype: float
        """
        return self._used_cpus

    @used_cpus.setter
    def used_cpus(self, used_cpus):
        """
        Sets the used_cpus of this AutonomousVmResourceUsage.
        The number of CPU cores alloted to the Autonomous Container Databases in an Cloud Autonomous VM cluster.


        :param used_cpus: The used_cpus of this AutonomousVmResourceUsage.
        :type: float
        """
        self._used_cpus = used_cpus

    @property
    def available_cpus(self):
        """
        Gets the available_cpus of this AutonomousVmResourceUsage.
        The number of CPU cores available.


        :return: The available_cpus of this AutonomousVmResourceUsage.
        :rtype: float
        """
        return self._available_cpus

    @available_cpus.setter
    def available_cpus(self, available_cpus):
        """
        Sets the available_cpus of this AutonomousVmResourceUsage.
        The number of CPU cores available.


        :param available_cpus: The available_cpus of this AutonomousVmResourceUsage.
        :type: float
        """
        self._available_cpus = available_cpus

    @property
    def reclaimable_cpus(self):
        """
        Gets the reclaimable_cpus of this AutonomousVmResourceUsage.
        CPU cores that continue to be included in the count of OCPUs available to the
        Autonomous Container Database even after one of its Autonomous Database is
        terminated or scaled down. You can release them to the available OCPUs at its
        parent AVMC level by restarting the Autonomous Container Database.


        :return: The reclaimable_cpus of this AutonomousVmResourceUsage.
        :rtype: float
        """
        return self._reclaimable_cpus

    @reclaimable_cpus.setter
    def reclaimable_cpus(self, reclaimable_cpus):
        """
        Sets the reclaimable_cpus of this AutonomousVmResourceUsage.
        CPU cores that continue to be included in the count of OCPUs available to the
        Autonomous Container Database even after one of its Autonomous Database is
        terminated or scaled down. You can release them to the available OCPUs at its
        parent AVMC level by restarting the Autonomous Container Database.


        :param reclaimable_cpus: The reclaimable_cpus of this AutonomousVmResourceUsage.
        :type: float
        """
        self._reclaimable_cpus = reclaimable_cpus

    @property
    def provisioned_cpus(self):
        """
        Gets the provisioned_cpus of this AutonomousVmResourceUsage.
        The number of CPUs provisioned in an Autonomous VM Cluster.


        :return: The provisioned_cpus of this AutonomousVmResourceUsage.
        :rtype: float
        """
        return self._provisioned_cpus

    @provisioned_cpus.setter
    def provisioned_cpus(self, provisioned_cpus):
        """
        Sets the provisioned_cpus of this AutonomousVmResourceUsage.
        The number of CPUs provisioned in an Autonomous VM Cluster.


        :param provisioned_cpus: The provisioned_cpus of this AutonomousVmResourceUsage.
        :type: float
        """
        self._provisioned_cpus = provisioned_cpus

    @property
    def reserved_cpus(self):
        """
        Gets the reserved_cpus of this AutonomousVmResourceUsage.
        The number of CPUs reserved in an Autonomous VM Cluster.


        :return: The reserved_cpus of this AutonomousVmResourceUsage.
        :rtype: float
        """
        return self._reserved_cpus

    @reserved_cpus.setter
    def reserved_cpus(self, reserved_cpus):
        """
        Sets the reserved_cpus of this AutonomousVmResourceUsage.
        The number of CPUs reserved in an Autonomous VM Cluster.


        :param reserved_cpus: The reserved_cpus of this AutonomousVmResourceUsage.
        :type: float
        """
        self._reserved_cpus = reserved_cpus

    @property
    def autonomous_container_database_usage(self):
        """
        Gets the autonomous_container_database_usage of this AutonomousVmResourceUsage.
        Associated Autonomous Container Database Usages.


        :return: The autonomous_container_database_usage of this AutonomousVmResourceUsage.
        :rtype: list[oci.database.models.AvmAcdResourceStats]
        """
        return self._autonomous_container_database_usage

    @autonomous_container_database_usage.setter
    def autonomous_container_database_usage(self, autonomous_container_database_usage):
        """
        Sets the autonomous_container_database_usage of this AutonomousVmResourceUsage.
        Associated Autonomous Container Database Usages.


        :param autonomous_container_database_usage: The autonomous_container_database_usage of this AutonomousVmResourceUsage.
        :type: list[oci.database.models.AvmAcdResourceStats]
        """
        self._autonomous_container_database_usage = autonomous_container_database_usage

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
