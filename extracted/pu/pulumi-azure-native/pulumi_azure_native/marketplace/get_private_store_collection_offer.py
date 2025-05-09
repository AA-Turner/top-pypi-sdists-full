# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import builtins
import copy
import warnings
import sys
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
if sys.version_info >= (3, 11):
    from typing import NotRequired, TypedDict, TypeAlias
else:
    from typing_extensions import NotRequired, TypedDict, TypeAlias
from .. import _utilities
from . import outputs

__all__ = [
    'GetPrivateStoreCollectionOfferResult',
    'AwaitableGetPrivateStoreCollectionOfferResult',
    'get_private_store_collection_offer',
    'get_private_store_collection_offer_output',
]

@pulumi.output_type
class GetPrivateStoreCollectionOfferResult:
    """
    The privateStore offer data structure.
    """
    def __init__(__self__, azure_api_version=None, created_at=None, e_tag=None, icon_file_uris=None, id=None, modified_at=None, name=None, offer_display_name=None, plans=None, private_store_id=None, publisher_display_name=None, specific_plan_ids_limitation=None, system_data=None, type=None, unique_offer_id=None, update_suppressed_due_idempotence=None):
        if azure_api_version and not isinstance(azure_api_version, str):
            raise TypeError("Expected argument 'azure_api_version' to be a str")
        pulumi.set(__self__, "azure_api_version", azure_api_version)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if e_tag and not isinstance(e_tag, str):
            raise TypeError("Expected argument 'e_tag' to be a str")
        pulumi.set(__self__, "e_tag", e_tag)
        if icon_file_uris and not isinstance(icon_file_uris, dict):
            raise TypeError("Expected argument 'icon_file_uris' to be a dict")
        pulumi.set(__self__, "icon_file_uris", icon_file_uris)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if modified_at and not isinstance(modified_at, str):
            raise TypeError("Expected argument 'modified_at' to be a str")
        pulumi.set(__self__, "modified_at", modified_at)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if offer_display_name and not isinstance(offer_display_name, str):
            raise TypeError("Expected argument 'offer_display_name' to be a str")
        pulumi.set(__self__, "offer_display_name", offer_display_name)
        if plans and not isinstance(plans, list):
            raise TypeError("Expected argument 'plans' to be a list")
        pulumi.set(__self__, "plans", plans)
        if private_store_id and not isinstance(private_store_id, str):
            raise TypeError("Expected argument 'private_store_id' to be a str")
        pulumi.set(__self__, "private_store_id", private_store_id)
        if publisher_display_name and not isinstance(publisher_display_name, str):
            raise TypeError("Expected argument 'publisher_display_name' to be a str")
        pulumi.set(__self__, "publisher_display_name", publisher_display_name)
        if specific_plan_ids_limitation and not isinstance(specific_plan_ids_limitation, list):
            raise TypeError("Expected argument 'specific_plan_ids_limitation' to be a list")
        pulumi.set(__self__, "specific_plan_ids_limitation", specific_plan_ids_limitation)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if unique_offer_id and not isinstance(unique_offer_id, str):
            raise TypeError("Expected argument 'unique_offer_id' to be a str")
        pulumi.set(__self__, "unique_offer_id", unique_offer_id)
        if update_suppressed_due_idempotence and not isinstance(update_suppressed_due_idempotence, bool):
            raise TypeError("Expected argument 'update_suppressed_due_idempotence' to be a bool")
        pulumi.set(__self__, "update_suppressed_due_idempotence", update_suppressed_due_idempotence)

    @property
    @pulumi.getter(name="azureApiVersion")
    def azure_api_version(self) -> builtins.str:
        """
        The Azure API version of the resource.
        """
        return pulumi.get(self, "azure_api_version")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> builtins.str:
        """
        Private store offer creation date
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="eTag")
    def e_tag(self) -> Optional[builtins.str]:
        """
        Identifier for purposes of race condition
        """
        return pulumi.get(self, "e_tag")

    @property
    @pulumi.getter(name="iconFileUris")
    def icon_file_uris(self) -> Optional[Mapping[str, builtins.str]]:
        """
        Icon File Uris
        """
        return pulumi.get(self, "icon_file_uris")

    @property
    @pulumi.getter
    def id(self) -> builtins.str:
        """
        The resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="modifiedAt")
    def modified_at(self) -> builtins.str:
        """
        Private store offer modification date
        """
        return pulumi.get(self, "modified_at")

    @property
    @pulumi.getter
    def name(self) -> builtins.str:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="offerDisplayName")
    def offer_display_name(self) -> builtins.str:
        """
        It will be displayed prominently in the marketplace
        """
        return pulumi.get(self, "offer_display_name")

    @property
    @pulumi.getter
    def plans(self) -> Optional[Sequence['outputs.PlanResponse']]:
        """
        Offer plans
        """
        return pulumi.get(self, "plans")

    @property
    @pulumi.getter(name="privateStoreId")
    def private_store_id(self) -> builtins.str:
        """
        Private store unique id
        """
        return pulumi.get(self, "private_store_id")

    @property
    @pulumi.getter(name="publisherDisplayName")
    def publisher_display_name(self) -> builtins.str:
        """
        Publisher name that will be displayed prominently in the marketplace
        """
        return pulumi.get(self, "publisher_display_name")

    @property
    @pulumi.getter(name="specificPlanIdsLimitation")
    def specific_plan_ids_limitation(self) -> Optional[Sequence[builtins.str]]:
        """
        Plan ids limitation for this offer
        """
        return pulumi.get(self, "specific_plan_ids_limitation")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> builtins.str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="uniqueOfferId")
    def unique_offer_id(self) -> builtins.str:
        """
        Offers unique id
        """
        return pulumi.get(self, "unique_offer_id")

    @property
    @pulumi.getter(name="updateSuppressedDueIdempotence")
    def update_suppressed_due_idempotence(self) -> Optional[builtins.bool]:
        """
        Indicating whether the offer was not updated to db (true = not updated). If the allow list is identical to the existed one in db, the offer would not be updated.
        """
        return pulumi.get(self, "update_suppressed_due_idempotence")


class AwaitableGetPrivateStoreCollectionOfferResult(GetPrivateStoreCollectionOfferResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPrivateStoreCollectionOfferResult(
            azure_api_version=self.azure_api_version,
            created_at=self.created_at,
            e_tag=self.e_tag,
            icon_file_uris=self.icon_file_uris,
            id=self.id,
            modified_at=self.modified_at,
            name=self.name,
            offer_display_name=self.offer_display_name,
            plans=self.plans,
            private_store_id=self.private_store_id,
            publisher_display_name=self.publisher_display_name,
            specific_plan_ids_limitation=self.specific_plan_ids_limitation,
            system_data=self.system_data,
            type=self.type,
            unique_offer_id=self.unique_offer_id,
            update_suppressed_due_idempotence=self.update_suppressed_due_idempotence)


def get_private_store_collection_offer(collection_id: Optional[builtins.str] = None,
                                       offer_id: Optional[builtins.str] = None,
                                       private_store_id: Optional[builtins.str] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPrivateStoreCollectionOfferResult:
    """
    Gets information about a specific offer.

    Uses Azure REST API version 2023-01-01.

    Other available API versions: 2025-01-01. These can be accessed by generating a local SDK package using the CLI command `pulumi package add azure-native marketplace [ApiVersion]`. See the [version guide](../../../version-guide/#accessing-any-api-version-via-local-packages) for details.


    :param builtins.str collection_id: The collection ID
    :param builtins.str offer_id: The offer ID to update or delete
    :param builtins.str private_store_id: The store ID - must use the tenant ID
    """
    __args__ = dict()
    __args__['collectionId'] = collection_id
    __args__['offerId'] = offer_id
    __args__['privateStoreId'] = private_store_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:marketplace:getPrivateStoreCollectionOffer', __args__, opts=opts, typ=GetPrivateStoreCollectionOfferResult).value

    return AwaitableGetPrivateStoreCollectionOfferResult(
        azure_api_version=pulumi.get(__ret__, 'azure_api_version'),
        created_at=pulumi.get(__ret__, 'created_at'),
        e_tag=pulumi.get(__ret__, 'e_tag'),
        icon_file_uris=pulumi.get(__ret__, 'icon_file_uris'),
        id=pulumi.get(__ret__, 'id'),
        modified_at=pulumi.get(__ret__, 'modified_at'),
        name=pulumi.get(__ret__, 'name'),
        offer_display_name=pulumi.get(__ret__, 'offer_display_name'),
        plans=pulumi.get(__ret__, 'plans'),
        private_store_id=pulumi.get(__ret__, 'private_store_id'),
        publisher_display_name=pulumi.get(__ret__, 'publisher_display_name'),
        specific_plan_ids_limitation=pulumi.get(__ret__, 'specific_plan_ids_limitation'),
        system_data=pulumi.get(__ret__, 'system_data'),
        type=pulumi.get(__ret__, 'type'),
        unique_offer_id=pulumi.get(__ret__, 'unique_offer_id'),
        update_suppressed_due_idempotence=pulumi.get(__ret__, 'update_suppressed_due_idempotence'))
def get_private_store_collection_offer_output(collection_id: Optional[pulumi.Input[builtins.str]] = None,
                                              offer_id: Optional[pulumi.Input[builtins.str]] = None,
                                              private_store_id: Optional[pulumi.Input[builtins.str]] = None,
                                              opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetPrivateStoreCollectionOfferResult]:
    """
    Gets information about a specific offer.

    Uses Azure REST API version 2023-01-01.

    Other available API versions: 2025-01-01. These can be accessed by generating a local SDK package using the CLI command `pulumi package add azure-native marketplace [ApiVersion]`. See the [version guide](../../../version-guide/#accessing-any-api-version-via-local-packages) for details.


    :param builtins.str collection_id: The collection ID
    :param builtins.str offer_id: The offer ID to update or delete
    :param builtins.str private_store_id: The store ID - must use the tenant ID
    """
    __args__ = dict()
    __args__['collectionId'] = collection_id
    __args__['offerId'] = offer_id
    __args__['privateStoreId'] = private_store_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure-native:marketplace:getPrivateStoreCollectionOffer', __args__, opts=opts, typ=GetPrivateStoreCollectionOfferResult)
    return __ret__.apply(lambda __response__: GetPrivateStoreCollectionOfferResult(
        azure_api_version=pulumi.get(__response__, 'azure_api_version'),
        created_at=pulumi.get(__response__, 'created_at'),
        e_tag=pulumi.get(__response__, 'e_tag'),
        icon_file_uris=pulumi.get(__response__, 'icon_file_uris'),
        id=pulumi.get(__response__, 'id'),
        modified_at=pulumi.get(__response__, 'modified_at'),
        name=pulumi.get(__response__, 'name'),
        offer_display_name=pulumi.get(__response__, 'offer_display_name'),
        plans=pulumi.get(__response__, 'plans'),
        private_store_id=pulumi.get(__response__, 'private_store_id'),
        publisher_display_name=pulumi.get(__response__, 'publisher_display_name'),
        specific_plan_ids_limitation=pulumi.get(__response__, 'specific_plan_ids_limitation'),
        system_data=pulumi.get(__response__, 'system_data'),
        type=pulumi.get(__response__, 'type'),
        unique_offer_id=pulumi.get(__response__, 'unique_offer_id'),
        update_suppressed_due_idempotence=pulumi.get(__response__, 'update_suppressed_due_idempotence')))
