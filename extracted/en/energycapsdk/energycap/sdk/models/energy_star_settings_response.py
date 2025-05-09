# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class EnergyStarSettingsResponse(Model):
    """EnergyStarSettingsResponse.

    :param pm_account_manager_full_name: Full name of Portfolio Account
     Manager
    :type pm_account_manager_full_name: str
    :param pm_account_manager_user_name: User name of Portfolio Account
     Manager
    :type pm_account_manager_user_name: str
    :param earliest_submission_period: The earliest period to submit
    :type earliest_submission_period: int
    :param unlinked_property_count: Number of Portfolio Manager properties
     that are not linked to any buildings in EnergyCAP
    :type unlinked_property_count: int
    :param linked_property_count: Number of Portfolio Manager properties that
     are linked to a building in EnergyCAP
    :type linked_property_count: int
    :param is_energy_star_available: True if this client is configured for
     ENERGY STAR and Portfolio manager is available. False indicates an issue.
     EnergyStarConfigurationErrorMessage will contain details
    :type is_energy_star_available: bool
    :param energy_star_configuration_error_message: If IsEnergystarAvailable
     is false, this reports the error
    :type energy_star_configuration_error_message: str
    :param is_energy_star_disabled: True if running offline mode or if ENERGY
     STAR has been disabled for this client, false otherwise
    :type is_energy_star_disabled: bool
    :param is_energy_star_configured: True if ENERGY STAR has been configured
    :type is_energy_star_configured: bool
    """

    _attribute_map = {
        'pm_account_manager_full_name': {'key': 'pmAccountManagerFullName', 'type': 'str'},
        'pm_account_manager_user_name': {'key': 'pmAccountManagerUserName', 'type': 'str'},
        'earliest_submission_period': {'key': 'earliestSubmissionPeriod', 'type': 'int'},
        'unlinked_property_count': {'key': 'unlinkedPropertyCount', 'type': 'int'},
        'linked_property_count': {'key': 'linkedPropertyCount', 'type': 'int'},
        'is_energy_star_available': {'key': 'isEnergyStarAvailable', 'type': 'bool'},
        'energy_star_configuration_error_message': {'key': 'energyStarConfigurationErrorMessage', 'type': 'str'},
        'is_energy_star_disabled': {'key': 'isEnergyStarDisabled', 'type': 'bool'},
        'is_energy_star_configured': {'key': 'isEnergyStarConfigured', 'type': 'bool'},
    }

    def __init__(self, **kwargs):
        super(EnergyStarSettingsResponse, self).__init__(**kwargs)
        self.pm_account_manager_full_name = kwargs.get('pm_account_manager_full_name', None)
        self.pm_account_manager_user_name = kwargs.get('pm_account_manager_user_name', None)
        self.earliest_submission_period = kwargs.get('earliest_submission_period', None)
        self.unlinked_property_count = kwargs.get('unlinked_property_count', None)
        self.linked_property_count = kwargs.get('linked_property_count', None)
        self.is_energy_star_available = kwargs.get('is_energy_star_available', None)
        self.energy_star_configuration_error_message = kwargs.get('energy_star_configuration_error_message', None)
        self.is_energy_star_disabled = kwargs.get('is_energy_star_disabled', None)
        self.is_energy_star_configured = kwargs.get('is_energy_star_configured', None)
