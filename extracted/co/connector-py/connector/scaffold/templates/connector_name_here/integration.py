import httpx
from connector.error import HTTPHandler
from connector.integration import DescriptionData, Integration, OAuthCredential, StandardCapabilityName

from {name} import capabilities_read, capabilities_write
from {name}.__about__ import __version__
from {name}.enums import entitlement_types, resource_types
from {name}.settings import {pascal}Settings

integration = Integration(
    app_id="{hyphenated_name}",
    version=__version__,
    auth=OAuthCredential,
    exception_handlers=[
        (httpx.HTTPStatusError, HTTPHandler, None),
    ],
    description_data=DescriptionData(
        logo_url="", app_vendor_domain="", user_friendly_name="{pascal}", description="", categories=[]
    ),
    settings_model={pascal}Settings,
    resource_types=resource_types,
    entitlement_types=entitlement_types,
)

integration.register_capabilities(
    {{
        # Read capabilities
        StandardCapabilityName.VALIDATE_CREDENTIALS: capabilities_read.validate_credentials,
        # StandardCapabilityName.LIST_ACCOUNTS: capabilities_read.list_accounts,
        # StandardCapabilityName.LIST_RESOURCES: capabilities_read.list_resources,
        # StandardCapabilityName.LIST_ENTITLEMENTS: capabilities_read.list_entitlements,
        # StandardCapabilityName.FIND_ENTITLEMENT_ASSOCIATIONS: capabilities_read.find_entitlement_associations,
        # StandardCapabilityName.GET_LAST_ACTIVITY: capabilities_read.get_last_activity,
        # StandardCapabilityName.LIST_CUSTOM_ATTRIBUTES_SCHEMA: capabilities_read.list_custom_attributes_schema,
        # Write capabilities
        # StandardCapabilityName.ASSIGN_ENTITLEMENT: capabilities_write.assign_entitlement,
        # StandardCapabilityName.UNASSIGN_ENTITLEMENT: capabilities_write.unassign_entitlement,
        # StandardCapabilityName.CREATE_ACCOUNT: capabilities_write.create_account,
        # StandardCapabilityName.ACTIVATE_ACCOUNT: capabilities_write.activate_account,
        # StandardCapabilityName.DEACTIVATE_ACCOUNT: capabilities_write.deactivate_account,
        # StandardCapabilityName.DELETE_ACCOUNT: capabilities_write.delete_account,
        # StandardCapabilityName.TRANSFER_DATA: capabilities_write.transfer_data,
        # StandardCapabilityName.DOWNGRADE_LICENSE: capabilities_write.downgrade_license,
        # StandardCapabilityName.RELEASE_RESOURCES: capabilities_write.release_resources,
    }}
)
