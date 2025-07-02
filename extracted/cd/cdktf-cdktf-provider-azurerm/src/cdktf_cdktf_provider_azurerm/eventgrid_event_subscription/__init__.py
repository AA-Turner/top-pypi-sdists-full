r'''
# `azurerm_eventgrid_event_subscription`

Refer to the Terraform Registry for docs: [`azurerm_eventgrid_event_subscription`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class EventgridEventSubscription(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscription",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription azurerm_eventgrid_event_subscription}.'''

    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        scope: builtins.str,
        advanced_filter: typing.Optional[typing.Union["EventgridEventSubscriptionAdvancedFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        advanced_filtering_on_arrays_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        azure_function_endpoint: typing.Optional[typing.Union["EventgridEventSubscriptionAzureFunctionEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
        dead_letter_identity: typing.Optional[typing.Union["EventgridEventSubscriptionDeadLetterIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        delivery_identity: typing.Optional[typing.Union["EventgridEventSubscriptionDeliveryIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        delivery_property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionDeliveryProperty", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_delivery_schema: typing.Optional[builtins.str] = None,
        eventhub_endpoint_id: typing.Optional[builtins.str] = None,
        expiration_time_utc: typing.Optional[builtins.str] = None,
        hybrid_connection_endpoint_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        included_event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        retry_policy: typing.Optional[typing.Union["EventgridEventSubscriptionRetryPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        service_bus_queue_endpoint_id: typing.Optional[builtins.str] = None,
        service_bus_topic_endpoint_id: typing.Optional[builtins.str] = None,
        storage_blob_dead_letter_destination: typing.Optional[typing.Union["EventgridEventSubscriptionStorageBlobDeadLetterDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_queue_endpoint: typing.Optional[typing.Union["EventgridEventSubscriptionStorageQueueEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
        subject_filter: typing.Optional[typing.Union["EventgridEventSubscriptionSubjectFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["EventgridEventSubscriptionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        webhook_endpoint: typing.Optional[typing.Union["EventgridEventSubscriptionWebhookEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription azurerm_eventgrid_event_subscription} Resource.

        :param scope_: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#name EventgridEventSubscription#name}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#scope EventgridEventSubscription#scope}.
        :param advanced_filter: advanced_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#advanced_filter EventgridEventSubscription#advanced_filter}
        :param advanced_filtering_on_arrays_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#advanced_filtering_on_arrays_enabled EventgridEventSubscription#advanced_filtering_on_arrays_enabled}.
        :param azure_function_endpoint: azure_function_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#azure_function_endpoint EventgridEventSubscription#azure_function_endpoint}
        :param dead_letter_identity: dead_letter_identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#dead_letter_identity EventgridEventSubscription#dead_letter_identity}
        :param delivery_identity: delivery_identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#delivery_identity EventgridEventSubscription#delivery_identity}
        :param delivery_property: delivery_property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#delivery_property EventgridEventSubscription#delivery_property}
        :param event_delivery_schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#event_delivery_schema EventgridEventSubscription#event_delivery_schema}.
        :param eventhub_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#eventhub_endpoint_id EventgridEventSubscription#eventhub_endpoint_id}.
        :param expiration_time_utc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#expiration_time_utc EventgridEventSubscription#expiration_time_utc}.
        :param hybrid_connection_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#hybrid_connection_endpoint_id EventgridEventSubscription#hybrid_connection_endpoint_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#id EventgridEventSubscription#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param included_event_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#included_event_types EventgridEventSubscription#included_event_types}.
        :param labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#labels EventgridEventSubscription#labels}.
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#retry_policy EventgridEventSubscription#retry_policy}
        :param service_bus_queue_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#service_bus_queue_endpoint_id EventgridEventSubscription#service_bus_queue_endpoint_id}.
        :param service_bus_topic_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#service_bus_topic_endpoint_id EventgridEventSubscription#service_bus_topic_endpoint_id}.
        :param storage_blob_dead_letter_destination: storage_blob_dead_letter_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#storage_blob_dead_letter_destination EventgridEventSubscription#storage_blob_dead_letter_destination}
        :param storage_queue_endpoint: storage_queue_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#storage_queue_endpoint EventgridEventSubscription#storage_queue_endpoint}
        :param subject_filter: subject_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#subject_filter EventgridEventSubscription#subject_filter}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#timeouts EventgridEventSubscription#timeouts}
        :param webhook_endpoint: webhook_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#webhook_endpoint EventgridEventSubscription#webhook_endpoint}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7aed6640d0aa77216d19be72bc922c6e99455d6c594c47dd2d5af9bd5b5c77c)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EventgridEventSubscriptionConfig(
            name=name,
            scope=scope,
            advanced_filter=advanced_filter,
            advanced_filtering_on_arrays_enabled=advanced_filtering_on_arrays_enabled,
            azure_function_endpoint=azure_function_endpoint,
            dead_letter_identity=dead_letter_identity,
            delivery_identity=delivery_identity,
            delivery_property=delivery_property,
            event_delivery_schema=event_delivery_schema,
            eventhub_endpoint_id=eventhub_endpoint_id,
            expiration_time_utc=expiration_time_utc,
            hybrid_connection_endpoint_id=hybrid_connection_endpoint_id,
            id=id,
            included_event_types=included_event_types,
            labels=labels,
            retry_policy=retry_policy,
            service_bus_queue_endpoint_id=service_bus_queue_endpoint_id,
            service_bus_topic_endpoint_id=service_bus_topic_endpoint_id,
            storage_blob_dead_letter_destination=storage_blob_dead_letter_destination,
            storage_queue_endpoint=storage_queue_endpoint,
            subject_filter=subject_filter,
            timeouts=timeouts,
            webhook_endpoint=webhook_endpoint,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope_, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a EventgridEventSubscription resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EventgridEventSubscription to import.
        :param import_from_id: The id of the existing EventgridEventSubscription that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EventgridEventSubscription to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__892caa621263ef81dec47a820d168016fc37c43775d3465e41cd05925115e323)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdvancedFilter")
    def put_advanced_filter(
        self,
        *,
        bool_equals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterBoolEquals", typing.Dict[builtins.str, typing.Any]]]]] = None,
        is_not_null: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterIsNotNull", typing.Dict[builtins.str, typing.Any]]]]] = None,
        is_null_or_undefined: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterIsNullOrUndefined", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_greater_than: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterNumberGreaterThan", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_greater_than_or_equals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterNumberIn", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_in_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterNumberInRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_less_than: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterNumberLessThan", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_less_than_or_equals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEquals", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_not_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterNumberNotIn", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_not_in_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterNumberNotInRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_begins_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringBeginsWith", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_contains: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringContains", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_ends_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringEndsWith", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringIn", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_not_begins_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringNotBeginsWith", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_not_contains: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringNotContains", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_not_ends_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringNotEndsWith", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_not_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringNotIn", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param bool_equals: bool_equals block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#bool_equals EventgridEventSubscription#bool_equals}
        :param is_not_null: is_not_null block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#is_not_null EventgridEventSubscription#is_not_null}
        :param is_null_or_undefined: is_null_or_undefined block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#is_null_or_undefined EventgridEventSubscription#is_null_or_undefined}
        :param number_greater_than: number_greater_than block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_greater_than EventgridEventSubscription#number_greater_than}
        :param number_greater_than_or_equals: number_greater_than_or_equals block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_greater_than_or_equals EventgridEventSubscription#number_greater_than_or_equals}
        :param number_in: number_in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_in EventgridEventSubscription#number_in}
        :param number_in_range: number_in_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_in_range EventgridEventSubscription#number_in_range}
        :param number_less_than: number_less_than block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_less_than EventgridEventSubscription#number_less_than}
        :param number_less_than_or_equals: number_less_than_or_equals block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_less_than_or_equals EventgridEventSubscription#number_less_than_or_equals}
        :param number_not_in: number_not_in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_not_in EventgridEventSubscription#number_not_in}
        :param number_not_in_range: number_not_in_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_not_in_range EventgridEventSubscription#number_not_in_range}
        :param string_begins_with: string_begins_with block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_begins_with EventgridEventSubscription#string_begins_with}
        :param string_contains: string_contains block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_contains EventgridEventSubscription#string_contains}
        :param string_ends_with: string_ends_with block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_ends_with EventgridEventSubscription#string_ends_with}
        :param string_in: string_in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_in EventgridEventSubscription#string_in}
        :param string_not_begins_with: string_not_begins_with block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_not_begins_with EventgridEventSubscription#string_not_begins_with}
        :param string_not_contains: string_not_contains block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_not_contains EventgridEventSubscription#string_not_contains}
        :param string_not_ends_with: string_not_ends_with block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_not_ends_with EventgridEventSubscription#string_not_ends_with}
        :param string_not_in: string_not_in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_not_in EventgridEventSubscription#string_not_in}
        '''
        value = EventgridEventSubscriptionAdvancedFilter(
            bool_equals=bool_equals,
            is_not_null=is_not_null,
            is_null_or_undefined=is_null_or_undefined,
            number_greater_than=number_greater_than,
            number_greater_than_or_equals=number_greater_than_or_equals,
            number_in=number_in,
            number_in_range=number_in_range,
            number_less_than=number_less_than,
            number_less_than_or_equals=number_less_than_or_equals,
            number_not_in=number_not_in,
            number_not_in_range=number_not_in_range,
            string_begins_with=string_begins_with,
            string_contains=string_contains,
            string_ends_with=string_ends_with,
            string_in=string_in,
            string_not_begins_with=string_not_begins_with,
            string_not_contains=string_not_contains,
            string_not_ends_with=string_not_ends_with,
            string_not_in=string_not_in,
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedFilter", [value]))

    @jsii.member(jsii_name="putAzureFunctionEndpoint")
    def put_azure_function_endpoint(
        self,
        *,
        function_id: builtins.str,
        max_events_per_batch: typing.Optional[jsii.Number] = None,
        preferred_batch_size_in_kilobytes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param function_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#function_id EventgridEventSubscription#function_id}.
        :param max_events_per_batch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#max_events_per_batch EventgridEventSubscription#max_events_per_batch}.
        :param preferred_batch_size_in_kilobytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#preferred_batch_size_in_kilobytes EventgridEventSubscription#preferred_batch_size_in_kilobytes}.
        '''
        value = EventgridEventSubscriptionAzureFunctionEndpoint(
            function_id=function_id,
            max_events_per_batch=max_events_per_batch,
            preferred_batch_size_in_kilobytes=preferred_batch_size_in_kilobytes,
        )

        return typing.cast(None, jsii.invoke(self, "putAzureFunctionEndpoint", [value]))

    @jsii.member(jsii_name="putDeadLetterIdentity")
    def put_dead_letter_identity(
        self,
        *,
        type: builtins.str,
        user_assigned_identity: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#type EventgridEventSubscription#type}.
        :param user_assigned_identity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#user_assigned_identity EventgridEventSubscription#user_assigned_identity}.
        '''
        value = EventgridEventSubscriptionDeadLetterIdentity(
            type=type, user_assigned_identity=user_assigned_identity
        )

        return typing.cast(None, jsii.invoke(self, "putDeadLetterIdentity", [value]))

    @jsii.member(jsii_name="putDeliveryIdentity")
    def put_delivery_identity(
        self,
        *,
        type: builtins.str,
        user_assigned_identity: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#type EventgridEventSubscription#type}.
        :param user_assigned_identity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#user_assigned_identity EventgridEventSubscription#user_assigned_identity}.
        '''
        value = EventgridEventSubscriptionDeliveryIdentity(
            type=type, user_assigned_identity=user_assigned_identity
        )

        return typing.cast(None, jsii.invoke(self, "putDeliveryIdentity", [value]))

    @jsii.member(jsii_name="putDeliveryProperty")
    def put_delivery_property(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionDeliveryProperty", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da9f12332b443ff91d281be5faa3a961c8ccb73d7b3c9ce65a7910be539bd262)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDeliveryProperty", [value]))

    @jsii.member(jsii_name="putRetryPolicy")
    def put_retry_policy(
        self,
        *,
        event_time_to_live: jsii.Number,
        max_delivery_attempts: jsii.Number,
    ) -> None:
        '''
        :param event_time_to_live: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#event_time_to_live EventgridEventSubscription#event_time_to_live}.
        :param max_delivery_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#max_delivery_attempts EventgridEventSubscription#max_delivery_attempts}.
        '''
        value = EventgridEventSubscriptionRetryPolicy(
            event_time_to_live=event_time_to_live,
            max_delivery_attempts=max_delivery_attempts,
        )

        return typing.cast(None, jsii.invoke(self, "putRetryPolicy", [value]))

    @jsii.member(jsii_name="putStorageBlobDeadLetterDestination")
    def put_storage_blob_dead_letter_destination(
        self,
        *,
        storage_account_id: builtins.str,
        storage_blob_container_name: builtins.str,
    ) -> None:
        '''
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#storage_account_id EventgridEventSubscription#storage_account_id}.
        :param storage_blob_container_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#storage_blob_container_name EventgridEventSubscription#storage_blob_container_name}.
        '''
        value = EventgridEventSubscriptionStorageBlobDeadLetterDestination(
            storage_account_id=storage_account_id,
            storage_blob_container_name=storage_blob_container_name,
        )

        return typing.cast(None, jsii.invoke(self, "putStorageBlobDeadLetterDestination", [value]))

    @jsii.member(jsii_name="putStorageQueueEndpoint")
    def put_storage_queue_endpoint(
        self,
        *,
        queue_name: builtins.str,
        storage_account_id: builtins.str,
        queue_message_time_to_live_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param queue_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#queue_name EventgridEventSubscription#queue_name}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#storage_account_id EventgridEventSubscription#storage_account_id}.
        :param queue_message_time_to_live_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#queue_message_time_to_live_in_seconds EventgridEventSubscription#queue_message_time_to_live_in_seconds}.
        '''
        value = EventgridEventSubscriptionStorageQueueEndpoint(
            queue_name=queue_name,
            storage_account_id=storage_account_id,
            queue_message_time_to_live_in_seconds=queue_message_time_to_live_in_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putStorageQueueEndpoint", [value]))

    @jsii.member(jsii_name="putSubjectFilter")
    def put_subject_filter(
        self,
        *,
        case_sensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subject_begins_with: typing.Optional[builtins.str] = None,
        subject_ends_with: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param case_sensitive: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#case_sensitive EventgridEventSubscription#case_sensitive}.
        :param subject_begins_with: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#subject_begins_with EventgridEventSubscription#subject_begins_with}.
        :param subject_ends_with: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#subject_ends_with EventgridEventSubscription#subject_ends_with}.
        '''
        value = EventgridEventSubscriptionSubjectFilter(
            case_sensitive=case_sensitive,
            subject_begins_with=subject_begins_with,
            subject_ends_with=subject_ends_with,
        )

        return typing.cast(None, jsii.invoke(self, "putSubjectFilter", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#create EventgridEventSubscription#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#delete EventgridEventSubscription#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#read EventgridEventSubscription#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#update EventgridEventSubscription#update}.
        '''
        value = EventgridEventSubscriptionTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWebhookEndpoint")
    def put_webhook_endpoint(
        self,
        *,
        url: builtins.str,
        active_directory_app_id_or_uri: typing.Optional[builtins.str] = None,
        active_directory_tenant_id: typing.Optional[builtins.str] = None,
        max_events_per_batch: typing.Optional[jsii.Number] = None,
        preferred_batch_size_in_kilobytes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#url EventgridEventSubscription#url}.
        :param active_directory_app_id_or_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#active_directory_app_id_or_uri EventgridEventSubscription#active_directory_app_id_or_uri}.
        :param active_directory_tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#active_directory_tenant_id EventgridEventSubscription#active_directory_tenant_id}.
        :param max_events_per_batch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#max_events_per_batch EventgridEventSubscription#max_events_per_batch}.
        :param preferred_batch_size_in_kilobytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#preferred_batch_size_in_kilobytes EventgridEventSubscription#preferred_batch_size_in_kilobytes}.
        '''
        value = EventgridEventSubscriptionWebhookEndpoint(
            url=url,
            active_directory_app_id_or_uri=active_directory_app_id_or_uri,
            active_directory_tenant_id=active_directory_tenant_id,
            max_events_per_batch=max_events_per_batch,
            preferred_batch_size_in_kilobytes=preferred_batch_size_in_kilobytes,
        )

        return typing.cast(None, jsii.invoke(self, "putWebhookEndpoint", [value]))

    @jsii.member(jsii_name="resetAdvancedFilter")
    def reset_advanced_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedFilter", []))

    @jsii.member(jsii_name="resetAdvancedFilteringOnArraysEnabled")
    def reset_advanced_filtering_on_arrays_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedFilteringOnArraysEnabled", []))

    @jsii.member(jsii_name="resetAzureFunctionEndpoint")
    def reset_azure_function_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureFunctionEndpoint", []))

    @jsii.member(jsii_name="resetDeadLetterIdentity")
    def reset_dead_letter_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeadLetterIdentity", []))

    @jsii.member(jsii_name="resetDeliveryIdentity")
    def reset_delivery_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeliveryIdentity", []))

    @jsii.member(jsii_name="resetDeliveryProperty")
    def reset_delivery_property(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeliveryProperty", []))

    @jsii.member(jsii_name="resetEventDeliverySchema")
    def reset_event_delivery_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventDeliverySchema", []))

    @jsii.member(jsii_name="resetEventhubEndpointId")
    def reset_eventhub_endpoint_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventhubEndpointId", []))

    @jsii.member(jsii_name="resetExpirationTimeUtc")
    def reset_expiration_time_utc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpirationTimeUtc", []))

    @jsii.member(jsii_name="resetHybridConnectionEndpointId")
    def reset_hybrid_connection_endpoint_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHybridConnectionEndpointId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIncludedEventTypes")
    def reset_included_event_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedEventTypes", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetRetryPolicy")
    def reset_retry_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryPolicy", []))

    @jsii.member(jsii_name="resetServiceBusQueueEndpointId")
    def reset_service_bus_queue_endpoint_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceBusQueueEndpointId", []))

    @jsii.member(jsii_name="resetServiceBusTopicEndpointId")
    def reset_service_bus_topic_endpoint_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceBusTopicEndpointId", []))

    @jsii.member(jsii_name="resetStorageBlobDeadLetterDestination")
    def reset_storage_blob_dead_letter_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageBlobDeadLetterDestination", []))

    @jsii.member(jsii_name="resetStorageQueueEndpoint")
    def reset_storage_queue_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageQueueEndpoint", []))

    @jsii.member(jsii_name="resetSubjectFilter")
    def reset_subject_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectFilter", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWebhookEndpoint")
    def reset_webhook_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebhookEndpoint", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="advancedFilter")
    def advanced_filter(
        self,
    ) -> "EventgridEventSubscriptionAdvancedFilterOutputReference":
        return typing.cast("EventgridEventSubscriptionAdvancedFilterOutputReference", jsii.get(self, "advancedFilter"))

    @builtins.property
    @jsii.member(jsii_name="azureFunctionEndpoint")
    def azure_function_endpoint(
        self,
    ) -> "EventgridEventSubscriptionAzureFunctionEndpointOutputReference":
        return typing.cast("EventgridEventSubscriptionAzureFunctionEndpointOutputReference", jsii.get(self, "azureFunctionEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="deadLetterIdentity")
    def dead_letter_identity(
        self,
    ) -> "EventgridEventSubscriptionDeadLetterIdentityOutputReference":
        return typing.cast("EventgridEventSubscriptionDeadLetterIdentityOutputReference", jsii.get(self, "deadLetterIdentity"))

    @builtins.property
    @jsii.member(jsii_name="deliveryIdentity")
    def delivery_identity(
        self,
    ) -> "EventgridEventSubscriptionDeliveryIdentityOutputReference":
        return typing.cast("EventgridEventSubscriptionDeliveryIdentityOutputReference", jsii.get(self, "deliveryIdentity"))

    @builtins.property
    @jsii.member(jsii_name="deliveryProperty")
    def delivery_property(self) -> "EventgridEventSubscriptionDeliveryPropertyList":
        return typing.cast("EventgridEventSubscriptionDeliveryPropertyList", jsii.get(self, "deliveryProperty"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicy")
    def retry_policy(self) -> "EventgridEventSubscriptionRetryPolicyOutputReference":
        return typing.cast("EventgridEventSubscriptionRetryPolicyOutputReference", jsii.get(self, "retryPolicy"))

    @builtins.property
    @jsii.member(jsii_name="storageBlobDeadLetterDestination")
    def storage_blob_dead_letter_destination(
        self,
    ) -> "EventgridEventSubscriptionStorageBlobDeadLetterDestinationOutputReference":
        return typing.cast("EventgridEventSubscriptionStorageBlobDeadLetterDestinationOutputReference", jsii.get(self, "storageBlobDeadLetterDestination"))

    @builtins.property
    @jsii.member(jsii_name="storageQueueEndpoint")
    def storage_queue_endpoint(
        self,
    ) -> "EventgridEventSubscriptionStorageQueueEndpointOutputReference":
        return typing.cast("EventgridEventSubscriptionStorageQueueEndpointOutputReference", jsii.get(self, "storageQueueEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="subjectFilter")
    def subject_filter(
        self,
    ) -> "EventgridEventSubscriptionSubjectFilterOutputReference":
        return typing.cast("EventgridEventSubscriptionSubjectFilterOutputReference", jsii.get(self, "subjectFilter"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "EventgridEventSubscriptionTimeoutsOutputReference":
        return typing.cast("EventgridEventSubscriptionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="webhookEndpoint")
    def webhook_endpoint(
        self,
    ) -> "EventgridEventSubscriptionWebhookEndpointOutputReference":
        return typing.cast("EventgridEventSubscriptionWebhookEndpointOutputReference", jsii.get(self, "webhookEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="advancedFilteringOnArraysEnabledInput")
    def advanced_filtering_on_arrays_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "advancedFilteringOnArraysEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="advancedFilterInput")
    def advanced_filter_input(
        self,
    ) -> typing.Optional["EventgridEventSubscriptionAdvancedFilter"]:
        return typing.cast(typing.Optional["EventgridEventSubscriptionAdvancedFilter"], jsii.get(self, "advancedFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="azureFunctionEndpointInput")
    def azure_function_endpoint_input(
        self,
    ) -> typing.Optional["EventgridEventSubscriptionAzureFunctionEndpoint"]:
        return typing.cast(typing.Optional["EventgridEventSubscriptionAzureFunctionEndpoint"], jsii.get(self, "azureFunctionEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="deadLetterIdentityInput")
    def dead_letter_identity_input(
        self,
    ) -> typing.Optional["EventgridEventSubscriptionDeadLetterIdentity"]:
        return typing.cast(typing.Optional["EventgridEventSubscriptionDeadLetterIdentity"], jsii.get(self, "deadLetterIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="deliveryIdentityInput")
    def delivery_identity_input(
        self,
    ) -> typing.Optional["EventgridEventSubscriptionDeliveryIdentity"]:
        return typing.cast(typing.Optional["EventgridEventSubscriptionDeliveryIdentity"], jsii.get(self, "deliveryIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="deliveryPropertyInput")
    def delivery_property_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionDeliveryProperty"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionDeliveryProperty"]]], jsii.get(self, "deliveryPropertyInput"))

    @builtins.property
    @jsii.member(jsii_name="eventDeliverySchemaInput")
    def event_delivery_schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventDeliverySchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="eventhubEndpointIdInput")
    def eventhub_endpoint_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventhubEndpointIdInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationTimeUtcInput")
    def expiration_time_utc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expirationTimeUtcInput"))

    @builtins.property
    @jsii.member(jsii_name="hybridConnectionEndpointIdInput")
    def hybrid_connection_endpoint_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hybridConnectionEndpointIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includedEventTypesInput")
    def included_event_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedEventTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicyInput")
    def retry_policy_input(
        self,
    ) -> typing.Optional["EventgridEventSubscriptionRetryPolicy"]:
        return typing.cast(typing.Optional["EventgridEventSubscriptionRetryPolicy"], jsii.get(self, "retryPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceBusQueueEndpointIdInput")
    def service_bus_queue_endpoint_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceBusQueueEndpointIdInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceBusTopicEndpointIdInput")
    def service_bus_topic_endpoint_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceBusTopicEndpointIdInput"))

    @builtins.property
    @jsii.member(jsii_name="storageBlobDeadLetterDestinationInput")
    def storage_blob_dead_letter_destination_input(
        self,
    ) -> typing.Optional["EventgridEventSubscriptionStorageBlobDeadLetterDestination"]:
        return typing.cast(typing.Optional["EventgridEventSubscriptionStorageBlobDeadLetterDestination"], jsii.get(self, "storageBlobDeadLetterDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="storageQueueEndpointInput")
    def storage_queue_endpoint_input(
        self,
    ) -> typing.Optional["EventgridEventSubscriptionStorageQueueEndpoint"]:
        return typing.cast(typing.Optional["EventgridEventSubscriptionStorageQueueEndpoint"], jsii.get(self, "storageQueueEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectFilterInput")
    def subject_filter_input(
        self,
    ) -> typing.Optional["EventgridEventSubscriptionSubjectFilter"]:
        return typing.cast(typing.Optional["EventgridEventSubscriptionSubjectFilter"], jsii.get(self, "subjectFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EventgridEventSubscriptionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EventgridEventSubscriptionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookEndpointInput")
    def webhook_endpoint_input(
        self,
    ) -> typing.Optional["EventgridEventSubscriptionWebhookEndpoint"]:
        return typing.cast(typing.Optional["EventgridEventSubscriptionWebhookEndpoint"], jsii.get(self, "webhookEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="advancedFilteringOnArraysEnabled")
    def advanced_filtering_on_arrays_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "advancedFilteringOnArraysEnabled"))

    @advanced_filtering_on_arrays_enabled.setter
    def advanced_filtering_on_arrays_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3cc70103e6bb2c61ccbd0bf78629859dfe9534f069f81d80e73f34fb37cd03b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advancedFilteringOnArraysEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventDeliverySchema")
    def event_delivery_schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventDeliverySchema"))

    @event_delivery_schema.setter
    def event_delivery_schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__431ef82fd2bccb53874c7f8e980337ac1689ce5ec78d38fc3844c3a4f204f33d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventDeliverySchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventhubEndpointId")
    def eventhub_endpoint_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventhubEndpointId"))

    @eventhub_endpoint_id.setter
    def eventhub_endpoint_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cd314db06ff2bf61371d53713d343cf433c5702cd2af41b70f46c9b9891e753)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventhubEndpointId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expirationTimeUtc")
    def expiration_time_utc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expirationTimeUtc"))

    @expiration_time_utc.setter
    def expiration_time_utc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__648a13ec239b044661a70293b6c164ad05ed58744446d52ad89fc43d58eaab5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationTimeUtc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hybridConnectionEndpointId")
    def hybrid_connection_endpoint_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hybridConnectionEndpointId"))

    @hybrid_connection_endpoint_id.setter
    def hybrid_connection_endpoint_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92de951aea097129bee12569c50304e536675866ed81ac0b5333d7fee59da021)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hybridConnectionEndpointId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e61184ff44da30d6958a4b1ca1840cff5b36a41f9a0da222e06a48748a05699)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedEventTypes")
    def included_event_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedEventTypes"))

    @included_event_types.setter
    def included_event_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4eebd904f59fc158eb2ad4a9630186a5f9dae52ce7068cf6391400f80b54975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedEventTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a13ecfb456b1fbb4adb9ff2b802826710afc09fc367fe3bebc1ef0596d18145)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b887d074fd6fa8658a829037c3794e416744b519c04ab0f1a443f73551546fd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59c23699006615417d9e3ac070e053e94c85455d2d95902a63a9510ebe08f8d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceBusQueueEndpointId")
    def service_bus_queue_endpoint_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceBusQueueEndpointId"))

    @service_bus_queue_endpoint_id.setter
    def service_bus_queue_endpoint_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26971cdad9581d6d31f17f73bd597fe94b19b90ae131c8fb11a576edb2e6c619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceBusQueueEndpointId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceBusTopicEndpointId")
    def service_bus_topic_endpoint_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceBusTopicEndpointId"))

    @service_bus_topic_endpoint_id.setter
    def service_bus_topic_endpoint_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db56240d8b1f781353dcfdabd2fdc14233fad248bea93103b23998b7515c656a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceBusTopicEndpointId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilter",
    jsii_struct_bases=[],
    name_mapping={
        "bool_equals": "boolEquals",
        "is_not_null": "isNotNull",
        "is_null_or_undefined": "isNullOrUndefined",
        "number_greater_than": "numberGreaterThan",
        "number_greater_than_or_equals": "numberGreaterThanOrEquals",
        "number_in": "numberIn",
        "number_in_range": "numberInRange",
        "number_less_than": "numberLessThan",
        "number_less_than_or_equals": "numberLessThanOrEquals",
        "number_not_in": "numberNotIn",
        "number_not_in_range": "numberNotInRange",
        "string_begins_with": "stringBeginsWith",
        "string_contains": "stringContains",
        "string_ends_with": "stringEndsWith",
        "string_in": "stringIn",
        "string_not_begins_with": "stringNotBeginsWith",
        "string_not_contains": "stringNotContains",
        "string_not_ends_with": "stringNotEndsWith",
        "string_not_in": "stringNotIn",
    },
)
class EventgridEventSubscriptionAdvancedFilter:
    def __init__(
        self,
        *,
        bool_equals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterBoolEquals", typing.Dict[builtins.str, typing.Any]]]]] = None,
        is_not_null: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterIsNotNull", typing.Dict[builtins.str, typing.Any]]]]] = None,
        is_null_or_undefined: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterIsNullOrUndefined", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_greater_than: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterNumberGreaterThan", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_greater_than_or_equals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterNumberIn", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_in_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterNumberInRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_less_than: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterNumberLessThan", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_less_than_or_equals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEquals", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_not_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterNumberNotIn", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_not_in_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterNumberNotInRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_begins_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringBeginsWith", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_contains: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringContains", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_ends_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringEndsWith", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringIn", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_not_begins_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringNotBeginsWith", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_not_contains: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringNotContains", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_not_ends_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringNotEndsWith", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_not_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringNotIn", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param bool_equals: bool_equals block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#bool_equals EventgridEventSubscription#bool_equals}
        :param is_not_null: is_not_null block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#is_not_null EventgridEventSubscription#is_not_null}
        :param is_null_or_undefined: is_null_or_undefined block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#is_null_or_undefined EventgridEventSubscription#is_null_or_undefined}
        :param number_greater_than: number_greater_than block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_greater_than EventgridEventSubscription#number_greater_than}
        :param number_greater_than_or_equals: number_greater_than_or_equals block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_greater_than_or_equals EventgridEventSubscription#number_greater_than_or_equals}
        :param number_in: number_in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_in EventgridEventSubscription#number_in}
        :param number_in_range: number_in_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_in_range EventgridEventSubscription#number_in_range}
        :param number_less_than: number_less_than block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_less_than EventgridEventSubscription#number_less_than}
        :param number_less_than_or_equals: number_less_than_or_equals block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_less_than_or_equals EventgridEventSubscription#number_less_than_or_equals}
        :param number_not_in: number_not_in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_not_in EventgridEventSubscription#number_not_in}
        :param number_not_in_range: number_not_in_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_not_in_range EventgridEventSubscription#number_not_in_range}
        :param string_begins_with: string_begins_with block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_begins_with EventgridEventSubscription#string_begins_with}
        :param string_contains: string_contains block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_contains EventgridEventSubscription#string_contains}
        :param string_ends_with: string_ends_with block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_ends_with EventgridEventSubscription#string_ends_with}
        :param string_in: string_in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_in EventgridEventSubscription#string_in}
        :param string_not_begins_with: string_not_begins_with block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_not_begins_with EventgridEventSubscription#string_not_begins_with}
        :param string_not_contains: string_not_contains block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_not_contains EventgridEventSubscription#string_not_contains}
        :param string_not_ends_with: string_not_ends_with block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_not_ends_with EventgridEventSubscription#string_not_ends_with}
        :param string_not_in: string_not_in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_not_in EventgridEventSubscription#string_not_in}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__431d69c0e88b9b96ce58d7ea91825d68900446d993489b02c0198d2cf02f6df7)
            check_type(argname="argument bool_equals", value=bool_equals, expected_type=type_hints["bool_equals"])
            check_type(argname="argument is_not_null", value=is_not_null, expected_type=type_hints["is_not_null"])
            check_type(argname="argument is_null_or_undefined", value=is_null_or_undefined, expected_type=type_hints["is_null_or_undefined"])
            check_type(argname="argument number_greater_than", value=number_greater_than, expected_type=type_hints["number_greater_than"])
            check_type(argname="argument number_greater_than_or_equals", value=number_greater_than_or_equals, expected_type=type_hints["number_greater_than_or_equals"])
            check_type(argname="argument number_in", value=number_in, expected_type=type_hints["number_in"])
            check_type(argname="argument number_in_range", value=number_in_range, expected_type=type_hints["number_in_range"])
            check_type(argname="argument number_less_than", value=number_less_than, expected_type=type_hints["number_less_than"])
            check_type(argname="argument number_less_than_or_equals", value=number_less_than_or_equals, expected_type=type_hints["number_less_than_or_equals"])
            check_type(argname="argument number_not_in", value=number_not_in, expected_type=type_hints["number_not_in"])
            check_type(argname="argument number_not_in_range", value=number_not_in_range, expected_type=type_hints["number_not_in_range"])
            check_type(argname="argument string_begins_with", value=string_begins_with, expected_type=type_hints["string_begins_with"])
            check_type(argname="argument string_contains", value=string_contains, expected_type=type_hints["string_contains"])
            check_type(argname="argument string_ends_with", value=string_ends_with, expected_type=type_hints["string_ends_with"])
            check_type(argname="argument string_in", value=string_in, expected_type=type_hints["string_in"])
            check_type(argname="argument string_not_begins_with", value=string_not_begins_with, expected_type=type_hints["string_not_begins_with"])
            check_type(argname="argument string_not_contains", value=string_not_contains, expected_type=type_hints["string_not_contains"])
            check_type(argname="argument string_not_ends_with", value=string_not_ends_with, expected_type=type_hints["string_not_ends_with"])
            check_type(argname="argument string_not_in", value=string_not_in, expected_type=type_hints["string_not_in"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bool_equals is not None:
            self._values["bool_equals"] = bool_equals
        if is_not_null is not None:
            self._values["is_not_null"] = is_not_null
        if is_null_or_undefined is not None:
            self._values["is_null_or_undefined"] = is_null_or_undefined
        if number_greater_than is not None:
            self._values["number_greater_than"] = number_greater_than
        if number_greater_than_or_equals is not None:
            self._values["number_greater_than_or_equals"] = number_greater_than_or_equals
        if number_in is not None:
            self._values["number_in"] = number_in
        if number_in_range is not None:
            self._values["number_in_range"] = number_in_range
        if number_less_than is not None:
            self._values["number_less_than"] = number_less_than
        if number_less_than_or_equals is not None:
            self._values["number_less_than_or_equals"] = number_less_than_or_equals
        if number_not_in is not None:
            self._values["number_not_in"] = number_not_in
        if number_not_in_range is not None:
            self._values["number_not_in_range"] = number_not_in_range
        if string_begins_with is not None:
            self._values["string_begins_with"] = string_begins_with
        if string_contains is not None:
            self._values["string_contains"] = string_contains
        if string_ends_with is not None:
            self._values["string_ends_with"] = string_ends_with
        if string_in is not None:
            self._values["string_in"] = string_in
        if string_not_begins_with is not None:
            self._values["string_not_begins_with"] = string_not_begins_with
        if string_not_contains is not None:
            self._values["string_not_contains"] = string_not_contains
        if string_not_ends_with is not None:
            self._values["string_not_ends_with"] = string_not_ends_with
        if string_not_in is not None:
            self._values["string_not_in"] = string_not_in

    @builtins.property
    def bool_equals(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterBoolEquals"]]]:
        '''bool_equals block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#bool_equals EventgridEventSubscription#bool_equals}
        '''
        result = self._values.get("bool_equals")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterBoolEquals"]]], result)

    @builtins.property
    def is_not_null(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterIsNotNull"]]]:
        '''is_not_null block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#is_not_null EventgridEventSubscription#is_not_null}
        '''
        result = self._values.get("is_not_null")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterIsNotNull"]]], result)

    @builtins.property
    def is_null_or_undefined(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterIsNullOrUndefined"]]]:
        '''is_null_or_undefined block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#is_null_or_undefined EventgridEventSubscription#is_null_or_undefined}
        '''
        result = self._values.get("is_null_or_undefined")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterIsNullOrUndefined"]]], result)

    @builtins.property
    def number_greater_than(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterNumberGreaterThan"]]]:
        '''number_greater_than block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_greater_than EventgridEventSubscription#number_greater_than}
        '''
        result = self._values.get("number_greater_than")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterNumberGreaterThan"]]], result)

    @builtins.property
    def number_greater_than_or_equals(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals"]]]:
        '''number_greater_than_or_equals block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_greater_than_or_equals EventgridEventSubscription#number_greater_than_or_equals}
        '''
        result = self._values.get("number_greater_than_or_equals")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals"]]], result)

    @builtins.property
    def number_in(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterNumberIn"]]]:
        '''number_in block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_in EventgridEventSubscription#number_in}
        '''
        result = self._values.get("number_in")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterNumberIn"]]], result)

    @builtins.property
    def number_in_range(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterNumberInRange"]]]:
        '''number_in_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_in_range EventgridEventSubscription#number_in_range}
        '''
        result = self._values.get("number_in_range")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterNumberInRange"]]], result)

    @builtins.property
    def number_less_than(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterNumberLessThan"]]]:
        '''number_less_than block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_less_than EventgridEventSubscription#number_less_than}
        '''
        result = self._values.get("number_less_than")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterNumberLessThan"]]], result)

    @builtins.property
    def number_less_than_or_equals(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEquals"]]]:
        '''number_less_than_or_equals block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_less_than_or_equals EventgridEventSubscription#number_less_than_or_equals}
        '''
        result = self._values.get("number_less_than_or_equals")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEquals"]]], result)

    @builtins.property
    def number_not_in(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterNumberNotIn"]]]:
        '''number_not_in block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_not_in EventgridEventSubscription#number_not_in}
        '''
        result = self._values.get("number_not_in")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterNumberNotIn"]]], result)

    @builtins.property
    def number_not_in_range(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterNumberNotInRange"]]]:
        '''number_not_in_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#number_not_in_range EventgridEventSubscription#number_not_in_range}
        '''
        result = self._values.get("number_not_in_range")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterNumberNotInRange"]]], result)

    @builtins.property
    def string_begins_with(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringBeginsWith"]]]:
        '''string_begins_with block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_begins_with EventgridEventSubscription#string_begins_with}
        '''
        result = self._values.get("string_begins_with")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringBeginsWith"]]], result)

    @builtins.property
    def string_contains(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringContains"]]]:
        '''string_contains block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_contains EventgridEventSubscription#string_contains}
        '''
        result = self._values.get("string_contains")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringContains"]]], result)

    @builtins.property
    def string_ends_with(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringEndsWith"]]]:
        '''string_ends_with block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_ends_with EventgridEventSubscription#string_ends_with}
        '''
        result = self._values.get("string_ends_with")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringEndsWith"]]], result)

    @builtins.property
    def string_in(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringIn"]]]:
        '''string_in block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_in EventgridEventSubscription#string_in}
        '''
        result = self._values.get("string_in")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringIn"]]], result)

    @builtins.property
    def string_not_begins_with(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringNotBeginsWith"]]]:
        '''string_not_begins_with block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_not_begins_with EventgridEventSubscription#string_not_begins_with}
        '''
        result = self._values.get("string_not_begins_with")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringNotBeginsWith"]]], result)

    @builtins.property
    def string_not_contains(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringNotContains"]]]:
        '''string_not_contains block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_not_contains EventgridEventSubscription#string_not_contains}
        '''
        result = self._values.get("string_not_contains")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringNotContains"]]], result)

    @builtins.property
    def string_not_ends_with(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringNotEndsWith"]]]:
        '''string_not_ends_with block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_not_ends_with EventgridEventSubscription#string_not_ends_with}
        '''
        result = self._values.get("string_not_ends_with")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringNotEndsWith"]]], result)

    @builtins.property
    def string_not_in(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringNotIn"]]]:
        '''string_not_in block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#string_not_in EventgridEventSubscription#string_not_in}
        '''
        result = self._values.get("string_not_in")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringNotIn"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionAdvancedFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterBoolEquals",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class EventgridEventSubscriptionAdvancedFilterBoolEquals:
    def __init__(
        self,
        *,
        key: builtins.str,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#value EventgridEventSubscription#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4da15a7e262e2999c8690a7f023dfc0d46755554473d7c2b64532a0ab9751050)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#value EventgridEventSubscription#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionAdvancedFilterBoolEquals(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionAdvancedFilterBoolEqualsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterBoolEqualsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a94bb0d7a9a4e64778f27a46fa8392b5325b9153e85775a5b0d355cc936b2b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridEventSubscriptionAdvancedFilterBoolEqualsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3050ba53beef469d52edf446a2ce70d377099457763f903e45b0a3aac18de8fd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridEventSubscriptionAdvancedFilterBoolEqualsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe481f6e9e6e28fd13ec8305e2781e8ddc8d99fd58324b8717a26359bd3e7cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a3097f7b06ea05314db991a084089845353496db62c816c9bc79649a505008d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1d4c3531e1c86c8efacd1bbc0fbc7775eebea6be703b3bd67478b6d83fe538e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterBoolEquals]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterBoolEquals]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterBoolEquals]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ec82eb31dd0d5897b78beecf69ee1b63c705a5187ad29e8bfd1f3bd47061000)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridEventSubscriptionAdvancedFilterBoolEqualsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterBoolEqualsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa55018b0505f2feb6c72147c3e320f48932ce47e04b080b8990c66cca2ee62d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__020e4e1525e4e3586151ceb8c7cd835a83c0535c2913838a70e3e4dbe73c85aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "value"))

    @value.setter
    def value(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__818ab963ff99c875b425f3fceceb46a212c75bcff360f24285ae4a3619dc1a80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterBoolEquals]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterBoolEquals]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterBoolEquals]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b2d506f8d8567951431aee3d6e23e77f348666ea6864adf19d5903c82c6b40b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterIsNotNull",
    jsii_struct_bases=[],
    name_mapping={"key": "key"},
)
class EventgridEventSubscriptionAdvancedFilterIsNotNull:
    def __init__(self, *, key: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cfcfc23a0f30dc0ce4390ad6a2073881ef50a66c7958c38ab7a0af6f36489ca)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionAdvancedFilterIsNotNull(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionAdvancedFilterIsNotNullList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterIsNotNullList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c2d502fbd47e13eacad6e9c675731b6bf4891641031c767a4677444209d1be5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridEventSubscriptionAdvancedFilterIsNotNullOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b538c9c80b5c40a66edea1c53437b3ef41190b553173d8dc8fc987979c2d8ce)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridEventSubscriptionAdvancedFilterIsNotNullOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd74bd226392add353779b7696d3485368dd7280afac6d3f02001a40e17aeedb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__939269d23c447f798275f175318c6b49cc6579e44c3eb2053ec2a5613eccae6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e70695e1e40d50ba8d293bd8465a4379a907459134cbd28011bcbf0c6e534326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterIsNotNull]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterIsNotNull]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterIsNotNull]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e503a74b9447e0e8ca68df3b610fef673fa80c5ce293852f3ecbe64da86d25a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridEventSubscriptionAdvancedFilterIsNotNullOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterIsNotNullOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__721447961dc9ae88796361291b3b331f9dc6f3c9dd4cc4750ea2b72703f36c84)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__657d69d6d67806e50e0186619c00f190253bfac9ae7bf407a88f34fc6777f818)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterIsNotNull]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterIsNotNull]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterIsNotNull]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ae144b8fb0ff69936057842357e7f1cabf743b76a6e9bca2b64d4dec67651a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterIsNullOrUndefined",
    jsii_struct_bases=[],
    name_mapping={"key": "key"},
)
class EventgridEventSubscriptionAdvancedFilterIsNullOrUndefined:
    def __init__(self, *, key: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7df5eedbc6d32686c152f577ac9637bb2bb373942e68d9f4253af61c5c48f27e)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionAdvancedFilterIsNullOrUndefined(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionAdvancedFilterIsNullOrUndefinedList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterIsNullOrUndefinedList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dc25756cb704c74256b9aeb1e776dfefde7c9559429315a986e826365bbd40b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridEventSubscriptionAdvancedFilterIsNullOrUndefinedOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94ec83a78eec1763292d0edce171438320dba912406e9fd8a336cc1bec0c381d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridEventSubscriptionAdvancedFilterIsNullOrUndefinedOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60cc3fd4540a8adbeabf326796374579dde2960f362fdd0ab89accee0996b254)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a656c96c3db5c8603c9e2835c94e751964f503d1f1dc99a27de017f36f8f587)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a5ccc3a947408b5e5c8071319e6285199e2f700f836837b3cd03a1d0e71ef22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterIsNullOrUndefined]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterIsNullOrUndefined]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterIsNullOrUndefined]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69753bd8c8780c7ab5645c077bd60bcd4dcb4c28810648d6f8fe5a5a83590db0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridEventSubscriptionAdvancedFilterIsNullOrUndefinedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterIsNullOrUndefinedOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ee5759994cd793ec719ca0529d209da320fbf95f8989afaac70ce3e94c90db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b2bcb526f2b9d5c09d3d5dd7c93f10a7415d800ef4a9ca820f95e186c14ff2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterIsNullOrUndefined]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterIsNullOrUndefined]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterIsNullOrUndefined]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60829e3c5f6f1e8392030de704a1941e2cb99515edc256d86f1e352c095a32a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberGreaterThan",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class EventgridEventSubscriptionAdvancedFilterNumberGreaterThan:
    def __init__(self, *, key: builtins.str, value: jsii.Number) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#value EventgridEventSubscription#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dbedeec84e94c2ae5f670611c7619abcaa6530e94c45d013a29755f8ffc3a5f)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#value EventgridEventSubscription#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionAdvancedFilterNumberGreaterThan(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionAdvancedFilterNumberGreaterThanList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberGreaterThanList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02410fd26fa091bb5206894d83c067b165cf41af6aa6d0955b20881670a36fce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed930506e8c1f065394bded6c724f46b16b12e9815f1d49b74ae61d56346752a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae95ac98d740520da622c65d91072fb37ea666ae1ba38176aa32f5ded597125)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e494aea5dac9d785c5a8c75890ef9fca5cdc1cda96531f6f426bfe9d6209c6a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__affce53707611a450e7360a8ed7d50527ca13c29295c1aec364eb40615391e24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberGreaterThan]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberGreaterThan]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberGreaterThan]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bd4ac3ade13fc8848cc44f3dcd995b7bde37346060bf73f7158d8af5156661b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals:
    def __init__(self, *, key: builtins.str, value: jsii.Number) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#value EventgridEventSubscription#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eecab5b4cda48763258fed19b01c26d6d8bd844c86f34173fdcdd861b004717b)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#value EventgridEventSubscription#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEqualsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEqualsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca37400fb1c8f257c51d78c010217e6afd6c89ff3dd43ca5f83aeb954d410bc5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEqualsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4711e8b0d199206e42e0b9463ad6c8ee4ad54f2bdf35d0af94c335b4cf583146)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEqualsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f4fc6599416baa4819d9f9c2cdc285b2e066fcc22dd7ce68c1e8d1e3ce0357a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02b84f813efc1146f04fcb91488f7f07e3af70086cf76f4f3a212dd6767445d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a7709f9ae2b6e7c23c3015e6726d7df74f2d2043ff109ed9a756a23ec52174a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74d25171256cddec4ef2d64aeb5a7561976b83918422abafd2671bb5292c0efe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEqualsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEqualsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__460d6a8418b629beb082adfd08e80b33f3d4a99f9ba902525d35a952ae7e26b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf1112704e7e4577ca90d0a63b72e3a7c3f94210a8a98bf3e4f8652796ddd738)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23c02c985bdbda4af702fb63cd7c381fd5175a722d0462b680bb28e68f3d24dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6341a1a9ba2c19abb4fa8b0af75e438e82fe50525cd44d10c9d14c928b625577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7f4e7a9ab162a64da0611685db5531dd3fdbb7eb87850e54a70be29775eb43b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__755e8334d918ceb8d74b0e162dadce511193ceaf31b9e0ef5e1ef339f31c8272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c39ea30d6d57c53205382f0200c8ec63f23436dfdcd7b61a8b353c4adc6b569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberGreaterThan]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberGreaterThan]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberGreaterThan]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__256f30e49dfcec3a26b74f0122d3c8e3f277ba105495d9c2eb6e90ad282bbfae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberIn",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridEventSubscriptionAdvancedFilterNumberIn:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[jsii.Number],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcbba0678a72ee969c091bfcc9bc3b6978d17efe168243d0df5d6f7c95bb55fd)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionAdvancedFilterNumberIn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionAdvancedFilterNumberInList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberInList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80626e9997021a596c8cb368b3a505b6b0cdcc277b5fcf1642f1837e910f9b4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridEventSubscriptionAdvancedFilterNumberInOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f20a1cc675eb2d3cd08ee33aae103b5fff349a60b6b60ccdc8caca4d5290914)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridEventSubscriptionAdvancedFilterNumberInOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cde5c5d07f93b8d9f4950937c88b8d4576562a33eae96fefd8d2ca2794ea7daa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d7ea3e4ca9d1b8642208dfa79fedb9820bf9b5ba1565d6d5d2f9f3d6120acf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2e0a4cd705242a9ed95214d36eb86463a5d9febb950b0dffdb1aaf27ce2120b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberIn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberIn]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberIn]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c19a7bf266070e68da8d85f941c8dc769c6a5ee1faf394892256a671359f4bde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridEventSubscriptionAdvancedFilterNumberInOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberInOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__708c8cec42f959985f8004ef77df718a84e9d09e9b7c6182aef91abd89b06181)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4c7a9946f1ca67fc4335d1be9ba96860ee059a389ca94b963e1cdc2ee6c115f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff333271d7b5f070d6367c6765fa3f7c2e65c5632e011a7bf3e656c7dce924bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberIn]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberIn]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberIn]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d154481a393880eed50a14b4dae023472678a3995ae7bfe702cf8a8b4566066)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberInRange",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridEventSubscriptionAdvancedFilterNumberInRange:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Sequence[jsii.Number]]],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2479ae8910d3a85fcb2166c2489f1fecbd5f1e5456bab22c6bc68c78b03cdf15)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[jsii.Number]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[jsii.Number]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionAdvancedFilterNumberInRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionAdvancedFilterNumberInRangeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberInRangeList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a0b903e2712dd0ed90664a67a549782cc6690df96ef96140768338e0940d431)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridEventSubscriptionAdvancedFilterNumberInRangeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6911f5df52ec3ba30a70336b459f0e2b91b218a20eafe9a412fcbf20b0b6de34)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridEventSubscriptionAdvancedFilterNumberInRangeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb096a98352e653265bfbf43065756b35e3458f16b416e3758b489e1646fe1c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bed856539508c27f3f4d895668fd56833fdff0fc3f84b4bfc77bfe6e58f40aac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eb03beba4480ed126c2d0424bba74a7d869a7910c0bf4edf5f70df07d2991b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberInRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberInRange]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberInRange]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae497095794dfb6e35554601dd1b45c2695c6a29e7523d35a6113ff2cb7adfff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridEventSubscriptionAdvancedFilterNumberInRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberInRangeOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__638e1312219d674fbcb8ea0ef28da6f96ae33e25f61c862fdcf2cc7748d3d249)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[jsii.Number]]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[jsii.Number]]]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb2685224ff83cd6d1fef200e0dc3fb35cd96a5c170973c948113559ef6215a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[jsii.Number]]]:
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[jsii.Number]]], jsii.get(self, "values"))

    @values.setter
    def values(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[jsii.Number]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b4fe4bbf8e30e614b0e0c0e2136270d79ef0c9a4f2db358d9f6857a378ef3c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberInRange]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberInRange]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberInRange]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d2da1eb3c7d0b3d64ac22931b22051313466dd0ca0060f0d01308e6a2629a3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberLessThan",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class EventgridEventSubscriptionAdvancedFilterNumberLessThan:
    def __init__(self, *, key: builtins.str, value: jsii.Number) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#value EventgridEventSubscription#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__503ab840f7fa1312f3fd7f6cc1ae72a3659a7addc51af1e536a8410cae1a5968)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#value EventgridEventSubscription#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionAdvancedFilterNumberLessThan(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionAdvancedFilterNumberLessThanList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberLessThanList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ae6568602cc8f9489bc4328f78cfeb2745895423f68ed21b05c102746284b96)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridEventSubscriptionAdvancedFilterNumberLessThanOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf31c7f246aae45c8647409b2474258a93099255686829363c4f4002b44bdffb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridEventSubscriptionAdvancedFilterNumberLessThanOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87e28555af6e4cfd63a0651a809d74670a49edd9d1c2491a6aab8921b554c752)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a29869e4f772d9748de4fa5fa0012de435489039362dacf4504506ed8b55a37e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__603d79f40537bfa819e7f1c55931302d067d1285c0dd1bad97c191a4f27584b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberLessThan]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberLessThan]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberLessThan]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47ce3eac4cb255a966c950e5bdc656176f1c12edae8f069738dcb6a2aacea86d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEquals",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEquals:
    def __init__(self, *, key: builtins.str, value: jsii.Number) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#value EventgridEventSubscription#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56f1b915f1c2728e42f1a88ed27cad83cf35617a0821ff35f145dd4563dd6387)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#value EventgridEventSubscription#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEquals(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEqualsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEqualsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33c7c12541dcce4702d1bba4c1e73156c7380997027a9d34f29572bae8dc4ff8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEqualsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e45706b4f0d99617f7cc4a332a8136ff979123015e08b14bbd8387b8062bfbc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEqualsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19c7e873e70cca82936e1b524d317cae1b403ca4bcbd94f2c085193c2812be99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f700475d0726b7f312fd4b93f912b8aad9fec17dda066b333daa0f61818bd4b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c60f7b124d579a1f4b1fcd5d616765870414df19fd2d526c7ccc715bbfbd9a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEquals]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEquals]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEquals]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e8a05d81a321a8cc472317fd582a9b62ea21b210f12f69a196ccee688d7b5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEqualsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEqualsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc26a548a7f5a1009ceda3338acbcf7c21e0cdbf37b6a35aea4b587a2e5a6746)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3416ffcdd74cb334067de3c36e071281017f9e75491e4697c33a3506bd7800d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0d579aa2492ccf761ef685ae051b37d4372c2ee1cddb90f02c8679a14beb1f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEquals]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEquals]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEquals]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72a9b2463e8340bccfc855ca074a28e94738a695216c119e46c18caafe4e1c41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridEventSubscriptionAdvancedFilterNumberLessThanOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberLessThanOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0034db4f8d9c10e851855d5915135264bf89ca64678e85055affa9c383b1f38)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd228d2032a9835a2cccc70c86027a37ed9c419f8cf0e95fa59a44831c26adb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbe3d244af40d72630277e46a4666f7b598cf2c4bf8e9ca56a2e89eb5192e631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberLessThan]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberLessThan]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberLessThan]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61efad9f72e13509f1f7c9c522146ff261b7dce82417eb5bf3784a0aa4fb7f15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberNotIn",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridEventSubscriptionAdvancedFilterNumberNotIn:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[jsii.Number],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33a9f4507616ee158fc5f165be03a8705493c01ba8e869141ff597fbb33b42d4)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionAdvancedFilterNumberNotIn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionAdvancedFilterNumberNotInList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberNotInList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c541c4ca6de79dd7767117405ae4d111431c92c58a95658813f72d1ac6eb523)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridEventSubscriptionAdvancedFilterNumberNotInOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f825dc3d213917cf7e26801546e83acc773693649820fcd8c1e8dbc09e8d98a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridEventSubscriptionAdvancedFilterNumberNotInOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b78adffd3c56a0f29ffbda905513183ceff1ddfa367addc511843326a99d49db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97fdb81151181505ca6e3f4e0f798ef6f2812c80b5fd9d9fbd6829ad8e10c3e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75c388c48a441fde7e8a1b4bc587b25a2e6da0b4b58e88458376854ea3fee6ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberNotIn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberNotIn]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberNotIn]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0cf6651b59c1676441f11372efc2815c0620d2e832a2d8e378cec0fdf90149d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridEventSubscriptionAdvancedFilterNumberNotInOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberNotInOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc6768109068dd69f6b76c8df1c0bdbcab9f332a563c3dece2931253a3f5f6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d270a7983f97c9f0d5843b58b7499675108a75917030b48b6e31fac8037d0681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1fb6cc8913bb64cdebf201e64e56f8af0fc819d5102130f8b719eefaea19238)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberNotIn]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberNotIn]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberNotIn]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e851271668f55c1bcd7d134c3e02490dfa82375492a20d9f07d4f7b4d4c84bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberNotInRange",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridEventSubscriptionAdvancedFilterNumberNotInRange:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Sequence[jsii.Number]]],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c89a75ec5efed0b0910ebdc576e91836dfcaa7827eb8f74d2d55deaf16e15c6e)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[jsii.Number]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[jsii.Number]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionAdvancedFilterNumberNotInRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionAdvancedFilterNumberNotInRangeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberNotInRangeList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e1a71a66da79b9bb1c8139489ed899e28c7b899cc764f48bcae0215cf037a6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridEventSubscriptionAdvancedFilterNumberNotInRangeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b78b0d8541ac2c9ad6f6e2aa9095854a691d8992ba0a8e8c7770bcfa76edaaa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridEventSubscriptionAdvancedFilterNumberNotInRangeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7c4d6d3d332c4a156c1581395be9890f5f2c26c8f9a39e2848c3a053158b03d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8051c4fbec150605ae0483ba09ef85fcabd8099fb13de7abc389d1beac6704f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11841900d04f285a58d5335d7263ce1f55226accab9adbdd26d8701b81cb8212)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberNotInRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberNotInRange]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberNotInRange]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5858470658e67873e1af05e7905b8754a0d6519e9fcc501c62d76c831c68a8da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridEventSubscriptionAdvancedFilterNumberNotInRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterNumberNotInRangeOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9135bafa13e3d1f9688a674f9e1e9979cd2dd4e7610b7257f97053f4fbb61f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[jsii.Number]]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[jsii.Number]]]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ee317d9bac135acd8f3100485b3db2e25c91166daebba31ca3ea1bf543372fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[jsii.Number]]]:
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[jsii.Number]]], jsii.get(self, "values"))

    @values.setter
    def values(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[jsii.Number]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ba7a414b7f8878b07bcb63b8f6b4ad8ef3976b7d0215be625bf5e6a42c70ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberNotInRange]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberNotInRange]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberNotInRange]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6781d1d80f7e5384a44b3739b2b6ac313e835514a8965ee0b8aa1e880a7fd1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridEventSubscriptionAdvancedFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e97ed9238cc5f13bef466bf54dd6e66e52c191dbd76da759badfb25599ca8607)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBoolEquals")
    def put_bool_equals(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterBoolEquals, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adcb93413d337a98ef584f09a8e2ec9a377e4fc9982a083ef932b3cfb8960bb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBoolEquals", [value]))

    @jsii.member(jsii_name="putIsNotNull")
    def put_is_not_null(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterIsNotNull, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b10ce5a0e206cd8af09b636b2b7aa8e57b482c7e6ad463c8f9ae67ad6508bf2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIsNotNull", [value]))

    @jsii.member(jsii_name="putIsNullOrUndefined")
    def put_is_null_or_undefined(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterIsNullOrUndefined, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__188794b1520fcf9dc07f11b87e41423c7fd856d198c23962641a71c100049c88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIsNullOrUndefined", [value]))

    @jsii.member(jsii_name="putNumberGreaterThan")
    def put_number_greater_than(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberGreaterThan, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dd1a487c61cff41cbc1115631a9fed3ea042aae9a1580b569610dab237d599b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNumberGreaterThan", [value]))

    @jsii.member(jsii_name="putNumberGreaterThanOrEquals")
    def put_number_greater_than_or_equals(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab3baa1c3ed42ec48833ee00441e79e4829df7308f1721fc3b51f42593890b16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNumberGreaterThanOrEquals", [value]))

    @jsii.member(jsii_name="putNumberIn")
    def put_number_in(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberIn, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__339f68e9b4b97af4b1402d2c7f248eae09dfe60ece2ceaed1e21a32defdf0337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNumberIn", [value]))

    @jsii.member(jsii_name="putNumberInRange")
    def put_number_in_range(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberInRange, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90a3dfb8768e70dc8bf92ba9bc028e9cb477dc03330ee2de0b6483466e42d49d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNumberInRange", [value]))

    @jsii.member(jsii_name="putNumberLessThan")
    def put_number_less_than(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberLessThan, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49d6b85448aec6054403fc2123735e54317a782ffe92d29367381ee07973c5ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNumberLessThan", [value]))

    @jsii.member(jsii_name="putNumberLessThanOrEquals")
    def put_number_less_than_or_equals(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEquals, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c725a1b112e6b8500d3e3aae0288445970fb0588a7f9a4ede931610cfe76964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNumberLessThanOrEquals", [value]))

    @jsii.member(jsii_name="putNumberNotIn")
    def put_number_not_in(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberNotIn, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f9192b7000c777d204750fc17bc87b046caffd22d581c96b5f219137284f97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNumberNotIn", [value]))

    @jsii.member(jsii_name="putNumberNotInRange")
    def put_number_not_in_range(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberNotInRange, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a19d18f928266d4360e0fb767979dbb7c662322763f31c26a0bdbf3bc8217355)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNumberNotInRange", [value]))

    @jsii.member(jsii_name="putStringBeginsWith")
    def put_string_begins_with(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringBeginsWith", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc1bd3069fb9a96efcf4ebc6e786b43983699bd07f1bbb3edfc9ac98eafb99ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStringBeginsWith", [value]))

    @jsii.member(jsii_name="putStringContains")
    def put_string_contains(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringContains", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6966edf88d8156533de14a8bfed9b136e32460a88a48476b8999aeeecc1625c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStringContains", [value]))

    @jsii.member(jsii_name="putStringEndsWith")
    def put_string_ends_with(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringEndsWith", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c6911b9e142f63dd4d9426e2f4fe75102f87147ddbc2b0589960ec25199f81d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStringEndsWith", [value]))

    @jsii.member(jsii_name="putStringIn")
    def put_string_in(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringIn", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc9c49df403953b181c9fad714d4aa22848ca9b802ccdf96dfc33711f8023b62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStringIn", [value]))

    @jsii.member(jsii_name="putStringNotBeginsWith")
    def put_string_not_begins_with(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringNotBeginsWith", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62055bfced2c9312412e2e70679077b3ff09a3f06fe9bd76932f2166cccc9486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStringNotBeginsWith", [value]))

    @jsii.member(jsii_name="putStringNotContains")
    def put_string_not_contains(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringNotContains", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__824e2a348d9b46c43569a26a1f8229983e492c6afb3c10d60e9fbacdbe85bcc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStringNotContains", [value]))

    @jsii.member(jsii_name="putStringNotEndsWith")
    def put_string_not_ends_with(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringNotEndsWith", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63bd9d1002f1d5c54bee7c472f1079e772e5184713caa2f878b555c19ee47b75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStringNotEndsWith", [value]))

    @jsii.member(jsii_name="putStringNotIn")
    def put_string_not_in(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionAdvancedFilterStringNotIn", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d9cded5ab33d6656033fa92643b3b3528b36179ca787d2c8a5b6c98569fc802)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStringNotIn", [value]))

    @jsii.member(jsii_name="resetBoolEquals")
    def reset_bool_equals(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBoolEquals", []))

    @jsii.member(jsii_name="resetIsNotNull")
    def reset_is_not_null(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsNotNull", []))

    @jsii.member(jsii_name="resetIsNullOrUndefined")
    def reset_is_null_or_undefined(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsNullOrUndefined", []))

    @jsii.member(jsii_name="resetNumberGreaterThan")
    def reset_number_greater_than(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumberGreaterThan", []))

    @jsii.member(jsii_name="resetNumberGreaterThanOrEquals")
    def reset_number_greater_than_or_equals(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumberGreaterThanOrEquals", []))

    @jsii.member(jsii_name="resetNumberIn")
    def reset_number_in(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumberIn", []))

    @jsii.member(jsii_name="resetNumberInRange")
    def reset_number_in_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumberInRange", []))

    @jsii.member(jsii_name="resetNumberLessThan")
    def reset_number_less_than(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumberLessThan", []))

    @jsii.member(jsii_name="resetNumberLessThanOrEquals")
    def reset_number_less_than_or_equals(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumberLessThanOrEquals", []))

    @jsii.member(jsii_name="resetNumberNotIn")
    def reset_number_not_in(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumberNotIn", []))

    @jsii.member(jsii_name="resetNumberNotInRange")
    def reset_number_not_in_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumberNotInRange", []))

    @jsii.member(jsii_name="resetStringBeginsWith")
    def reset_string_begins_with(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringBeginsWith", []))

    @jsii.member(jsii_name="resetStringContains")
    def reset_string_contains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringContains", []))

    @jsii.member(jsii_name="resetStringEndsWith")
    def reset_string_ends_with(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringEndsWith", []))

    @jsii.member(jsii_name="resetStringIn")
    def reset_string_in(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringIn", []))

    @jsii.member(jsii_name="resetStringNotBeginsWith")
    def reset_string_not_begins_with(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringNotBeginsWith", []))

    @jsii.member(jsii_name="resetStringNotContains")
    def reset_string_not_contains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringNotContains", []))

    @jsii.member(jsii_name="resetStringNotEndsWith")
    def reset_string_not_ends_with(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringNotEndsWith", []))

    @jsii.member(jsii_name="resetStringNotIn")
    def reset_string_not_in(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringNotIn", []))

    @builtins.property
    @jsii.member(jsii_name="boolEquals")
    def bool_equals(self) -> EventgridEventSubscriptionAdvancedFilterBoolEqualsList:
        return typing.cast(EventgridEventSubscriptionAdvancedFilterBoolEqualsList, jsii.get(self, "boolEquals"))

    @builtins.property
    @jsii.member(jsii_name="isNotNull")
    def is_not_null(self) -> EventgridEventSubscriptionAdvancedFilterIsNotNullList:
        return typing.cast(EventgridEventSubscriptionAdvancedFilterIsNotNullList, jsii.get(self, "isNotNull"))

    @builtins.property
    @jsii.member(jsii_name="isNullOrUndefined")
    def is_null_or_undefined(
        self,
    ) -> EventgridEventSubscriptionAdvancedFilterIsNullOrUndefinedList:
        return typing.cast(EventgridEventSubscriptionAdvancedFilterIsNullOrUndefinedList, jsii.get(self, "isNullOrUndefined"))

    @builtins.property
    @jsii.member(jsii_name="numberGreaterThan")
    def number_greater_than(
        self,
    ) -> EventgridEventSubscriptionAdvancedFilterNumberGreaterThanList:
        return typing.cast(EventgridEventSubscriptionAdvancedFilterNumberGreaterThanList, jsii.get(self, "numberGreaterThan"))

    @builtins.property
    @jsii.member(jsii_name="numberGreaterThanOrEquals")
    def number_greater_than_or_equals(
        self,
    ) -> EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEqualsList:
        return typing.cast(EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEqualsList, jsii.get(self, "numberGreaterThanOrEquals"))

    @builtins.property
    @jsii.member(jsii_name="numberIn")
    def number_in(self) -> EventgridEventSubscriptionAdvancedFilterNumberInList:
        return typing.cast(EventgridEventSubscriptionAdvancedFilterNumberInList, jsii.get(self, "numberIn"))

    @builtins.property
    @jsii.member(jsii_name="numberInRange")
    def number_in_range(
        self,
    ) -> EventgridEventSubscriptionAdvancedFilterNumberInRangeList:
        return typing.cast(EventgridEventSubscriptionAdvancedFilterNumberInRangeList, jsii.get(self, "numberInRange"))

    @builtins.property
    @jsii.member(jsii_name="numberLessThan")
    def number_less_than(
        self,
    ) -> EventgridEventSubscriptionAdvancedFilterNumberLessThanList:
        return typing.cast(EventgridEventSubscriptionAdvancedFilterNumberLessThanList, jsii.get(self, "numberLessThan"))

    @builtins.property
    @jsii.member(jsii_name="numberLessThanOrEquals")
    def number_less_than_or_equals(
        self,
    ) -> EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEqualsList:
        return typing.cast(EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEqualsList, jsii.get(self, "numberLessThanOrEquals"))

    @builtins.property
    @jsii.member(jsii_name="numberNotIn")
    def number_not_in(self) -> EventgridEventSubscriptionAdvancedFilterNumberNotInList:
        return typing.cast(EventgridEventSubscriptionAdvancedFilterNumberNotInList, jsii.get(self, "numberNotIn"))

    @builtins.property
    @jsii.member(jsii_name="numberNotInRange")
    def number_not_in_range(
        self,
    ) -> EventgridEventSubscriptionAdvancedFilterNumberNotInRangeList:
        return typing.cast(EventgridEventSubscriptionAdvancedFilterNumberNotInRangeList, jsii.get(self, "numberNotInRange"))

    @builtins.property
    @jsii.member(jsii_name="stringBeginsWith")
    def string_begins_with(
        self,
    ) -> "EventgridEventSubscriptionAdvancedFilterStringBeginsWithList":
        return typing.cast("EventgridEventSubscriptionAdvancedFilterStringBeginsWithList", jsii.get(self, "stringBeginsWith"))

    @builtins.property
    @jsii.member(jsii_name="stringContains")
    def string_contains(
        self,
    ) -> "EventgridEventSubscriptionAdvancedFilterStringContainsList":
        return typing.cast("EventgridEventSubscriptionAdvancedFilterStringContainsList", jsii.get(self, "stringContains"))

    @builtins.property
    @jsii.member(jsii_name="stringEndsWith")
    def string_ends_with(
        self,
    ) -> "EventgridEventSubscriptionAdvancedFilterStringEndsWithList":
        return typing.cast("EventgridEventSubscriptionAdvancedFilterStringEndsWithList", jsii.get(self, "stringEndsWith"))

    @builtins.property
    @jsii.member(jsii_name="stringIn")
    def string_in(self) -> "EventgridEventSubscriptionAdvancedFilterStringInList":
        return typing.cast("EventgridEventSubscriptionAdvancedFilterStringInList", jsii.get(self, "stringIn"))

    @builtins.property
    @jsii.member(jsii_name="stringNotBeginsWith")
    def string_not_begins_with(
        self,
    ) -> "EventgridEventSubscriptionAdvancedFilterStringNotBeginsWithList":
        return typing.cast("EventgridEventSubscriptionAdvancedFilterStringNotBeginsWithList", jsii.get(self, "stringNotBeginsWith"))

    @builtins.property
    @jsii.member(jsii_name="stringNotContains")
    def string_not_contains(
        self,
    ) -> "EventgridEventSubscriptionAdvancedFilterStringNotContainsList":
        return typing.cast("EventgridEventSubscriptionAdvancedFilterStringNotContainsList", jsii.get(self, "stringNotContains"))

    @builtins.property
    @jsii.member(jsii_name="stringNotEndsWith")
    def string_not_ends_with(
        self,
    ) -> "EventgridEventSubscriptionAdvancedFilterStringNotEndsWithList":
        return typing.cast("EventgridEventSubscriptionAdvancedFilterStringNotEndsWithList", jsii.get(self, "stringNotEndsWith"))

    @builtins.property
    @jsii.member(jsii_name="stringNotIn")
    def string_not_in(
        self,
    ) -> "EventgridEventSubscriptionAdvancedFilterStringNotInList":
        return typing.cast("EventgridEventSubscriptionAdvancedFilterStringNotInList", jsii.get(self, "stringNotIn"))

    @builtins.property
    @jsii.member(jsii_name="boolEqualsInput")
    def bool_equals_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterBoolEquals]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterBoolEquals]]], jsii.get(self, "boolEqualsInput"))

    @builtins.property
    @jsii.member(jsii_name="isNotNullInput")
    def is_not_null_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterIsNotNull]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterIsNotNull]]], jsii.get(self, "isNotNullInput"))

    @builtins.property
    @jsii.member(jsii_name="isNullOrUndefinedInput")
    def is_null_or_undefined_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterIsNullOrUndefined]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterIsNullOrUndefined]]], jsii.get(self, "isNullOrUndefinedInput"))

    @builtins.property
    @jsii.member(jsii_name="numberGreaterThanInput")
    def number_greater_than_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberGreaterThan]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberGreaterThan]]], jsii.get(self, "numberGreaterThanInput"))

    @builtins.property
    @jsii.member(jsii_name="numberGreaterThanOrEqualsInput")
    def number_greater_than_or_equals_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals]]], jsii.get(self, "numberGreaterThanOrEqualsInput"))

    @builtins.property
    @jsii.member(jsii_name="numberInInput")
    def number_in_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberIn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberIn]]], jsii.get(self, "numberInInput"))

    @builtins.property
    @jsii.member(jsii_name="numberInRangeInput")
    def number_in_range_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberInRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberInRange]]], jsii.get(self, "numberInRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="numberLessThanInput")
    def number_less_than_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberLessThan]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberLessThan]]], jsii.get(self, "numberLessThanInput"))

    @builtins.property
    @jsii.member(jsii_name="numberLessThanOrEqualsInput")
    def number_less_than_or_equals_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEquals]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEquals]]], jsii.get(self, "numberLessThanOrEqualsInput"))

    @builtins.property
    @jsii.member(jsii_name="numberNotInInput")
    def number_not_in_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberNotIn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberNotIn]]], jsii.get(self, "numberNotInInput"))

    @builtins.property
    @jsii.member(jsii_name="numberNotInRangeInput")
    def number_not_in_range_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberNotInRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberNotInRange]]], jsii.get(self, "numberNotInRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="stringBeginsWithInput")
    def string_begins_with_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringBeginsWith"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringBeginsWith"]]], jsii.get(self, "stringBeginsWithInput"))

    @builtins.property
    @jsii.member(jsii_name="stringContainsInput")
    def string_contains_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringContains"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringContains"]]], jsii.get(self, "stringContainsInput"))

    @builtins.property
    @jsii.member(jsii_name="stringEndsWithInput")
    def string_ends_with_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringEndsWith"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringEndsWith"]]], jsii.get(self, "stringEndsWithInput"))

    @builtins.property
    @jsii.member(jsii_name="stringInInput")
    def string_in_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringIn"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringIn"]]], jsii.get(self, "stringInInput"))

    @builtins.property
    @jsii.member(jsii_name="stringNotBeginsWithInput")
    def string_not_begins_with_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringNotBeginsWith"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringNotBeginsWith"]]], jsii.get(self, "stringNotBeginsWithInput"))

    @builtins.property
    @jsii.member(jsii_name="stringNotContainsInput")
    def string_not_contains_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringNotContains"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringNotContains"]]], jsii.get(self, "stringNotContainsInput"))

    @builtins.property
    @jsii.member(jsii_name="stringNotEndsWithInput")
    def string_not_ends_with_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringNotEndsWith"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringNotEndsWith"]]], jsii.get(self, "stringNotEndsWithInput"))

    @builtins.property
    @jsii.member(jsii_name="stringNotInInput")
    def string_not_in_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringNotIn"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionAdvancedFilterStringNotIn"]]], jsii.get(self, "stringNotInInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventgridEventSubscriptionAdvancedFilter]:
        return typing.cast(typing.Optional[EventgridEventSubscriptionAdvancedFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventgridEventSubscriptionAdvancedFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fda554c47e1d28edf0d5ceb9bccbcfaa7a5a63f2b02c1dacdd9a1b397347c44a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringBeginsWith",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridEventSubscriptionAdvancedFilterStringBeginsWith:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc1ad89ffd19d0d35a80ffdef45ef6461de00573d0dc54deac2cd50fcbb85c0)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionAdvancedFilterStringBeginsWith(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionAdvancedFilterStringBeginsWithList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringBeginsWithList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81af93f7e9cba205a95562d9031c893b526c35035d006b2082b1fa4e4d588dd8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridEventSubscriptionAdvancedFilterStringBeginsWithOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__915ebe4022824f70d52e9e83788e8556e74dde2fe03c93df53c0b54f40c4a8a5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridEventSubscriptionAdvancedFilterStringBeginsWithOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__211f97251551af56f0b262708e3d163795a3b9eb642c01cf0786cc9f36f07c29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b753484410562966b003fb0f99fd192cc6e058141b9b76cf8a14baff37999c25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825b58c264290f6e842479a8ba71e4e6558c6bfa3479d929ff38470bd0b365f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringBeginsWith]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringBeginsWith]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringBeginsWith]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__943a9c28ccbfe624aa4137c94ea0a3bb39a20d3a3a8cc5ad5fb53a78e39d0446)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridEventSubscriptionAdvancedFilterStringBeginsWithOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringBeginsWithOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__372a90d8e1e74a95d7a56b65dfa04febbe6134bbb93f0f47733a696979e980b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__425c74cfdb9d6b22b22d88bd2b4bf3f3e6ea46cd83777d8e627fa1a2334dbd80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da319c39f19d717e6e0ae051f860766f600583d4ca3fb18fef6ff6ed9061d3da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringBeginsWith]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringBeginsWith]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringBeginsWith]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363ff8a5891b94b1051b74ec0e5c3e23149bdec0e10312648b3cff4c64c61c44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringContains",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridEventSubscriptionAdvancedFilterStringContains:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2af2264eee13610c78d7608226bf1568d9cae3920c780b0d9fc1acebc86fc09)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionAdvancedFilterStringContains(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionAdvancedFilterStringContainsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringContainsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9423b6c1b6753984e441e703a01108e9bbdead687ac3915759ad94b357b83c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridEventSubscriptionAdvancedFilterStringContainsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9786299a030126a5ec1b38ca382ffa393d414ce0fc92726ed290f67ed9e6fbf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridEventSubscriptionAdvancedFilterStringContainsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ab29f9cf001c643d4be8948d10ddbfb475830e190bcac4a2422ec3d43d08c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fee457c2cb978519360fca2d597cf492145fdce10d1a1d87cba6a2efb44cd976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a331cea75ee43e1b04050c3a45ef4755c9590909b90452689d95221f8ee262)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringContains]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringContains]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringContains]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__935a6abfc4800fc124d5f18efec512b5f7be81c751c9f09be664dede806b8e50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridEventSubscriptionAdvancedFilterStringContainsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringContainsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48d71f867ca12c9fa3f75cfbab78081acd1c20b567dc1e29d8101def3ce0f028)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f7a191387d5ebea1eaa3b285efe7da9564d3ba9e0349ad7a5e5ef851ebccc5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4ab44e088328e9920ff35def45c6a10ead10b0a947926f3e855b8f503757ac5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringContains]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringContains]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringContains]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fffb0d24ab9ae0cbdb522440b513e997ad72b87ca1b6a095513509328f8ed52d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringEndsWith",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridEventSubscriptionAdvancedFilterStringEndsWith:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb63af44fd36df30980fbf32d143dac0181c5c2bf14ae697fbb9ab20da1118c1)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionAdvancedFilterStringEndsWith(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionAdvancedFilterStringEndsWithList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringEndsWithList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc562b5be17d2362eb998d51793a97ed8585efc32ba86a0a050e0571eda89767)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridEventSubscriptionAdvancedFilterStringEndsWithOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3409adc5f6d99e0d066a1b118930a3184038d5ebc7ac8451e426c53ae285be67)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridEventSubscriptionAdvancedFilterStringEndsWithOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2f9d1e3a7cd2a6d29f0f7c1fa051d0d3a15afb628dd51bb8d7000c97b1f2a39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__127446ce9c99c28a8caa140da3155a2c78e2bd8487073627b972548a0c96d425)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5afb406746be096ea3ce5685e559faed4dfda6d8340c5f7b7a4fc2fe4e1fdb68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringEndsWith]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringEndsWith]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringEndsWith]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e19561d446d2deeade477502c4a1b66e308178c366ec24476f3594fecc310fbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridEventSubscriptionAdvancedFilterStringEndsWithOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringEndsWithOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd292665ec87edf21f53a1a3d4e9f12c806120f0c1c50798d48123b236f3e45d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c3fc751039d17a3b00d5041ceda4cbaa54cb71e75b79d3faa35db43593e2760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23f9afa165300e479e0f783e77ad6664d3e9e71c533e83b6c4d3eef18d3e6f54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringEndsWith]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringEndsWith]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringEndsWith]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15af2f407f0527718a04f8c9bfac33f5de59f5f5d8eb842a7a3b257f4f2e5a3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringIn",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridEventSubscriptionAdvancedFilterStringIn:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3279aa899b4924fadb4ccebff04acae2f318a1ea9f5e5081be2c2f40049f25d7)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionAdvancedFilterStringIn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionAdvancedFilterStringInList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringInList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c88c8a88f392ad82db5c26e39c3ae3d7366191bdb94eb4a7f39c9f8c799328f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridEventSubscriptionAdvancedFilterStringInOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee1b8a714ca1154bd00a88ad0989faf53c9b2733b9501f4d2ed596a988735c11)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridEventSubscriptionAdvancedFilterStringInOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e16f57ca063429afb1e789d9648dd92f97765643bee8257b4bcb1e09a2fedc9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38e90de75e53d586c6f69ff8eb0213f7bf20e4d6739e2f56b165ba7fb765b591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33d916ab57fc80cc61c5ba533b7f53087b4ba4747ff987bcb2eb77ee1bb40b5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringIn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringIn]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringIn]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39dc703c7fa740491e6148c743b50ea52de167b2a96e8e4ca078bca80176ae4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridEventSubscriptionAdvancedFilterStringInOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringInOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48db09010ff34d3c1d1b1fd0b3bbf2193f8ac76da52926a94c7323fe0e5455b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c16077163021bd53e0ca1fff74a5c0f80bb098fdcfad767294fe8060b48ecc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e3a266c2589078409f50d9d184484e7be39bbc641bedd94f859f1ca4eae5877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringIn]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringIn]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringIn]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__342f9ab45635fcd65640a56da5c04e86bb60db72f522f048d4b6ef7e6adeb6af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringNotBeginsWith",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridEventSubscriptionAdvancedFilterStringNotBeginsWith:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c284089bbadade25f45881d13e6438ed57e02f52c485a61922ff0b881e9ea3d9)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionAdvancedFilterStringNotBeginsWith(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionAdvancedFilterStringNotBeginsWithList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringNotBeginsWithList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b27b24bc209c2ae5e63cdcf3cf955ffed02cee98ea7b4ac2852b7ab93254e5d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridEventSubscriptionAdvancedFilterStringNotBeginsWithOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae8e8c64c86031b72aa5691ee3bbe76f66084e4b4f07fcafa2197f561aede4f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridEventSubscriptionAdvancedFilterStringNotBeginsWithOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32ef3ace72d259cde5fad98261e103c254e5e72f5a689d796f27b85ee4c459a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__237e180c45e2b5c17f5e77695c4086c68c130c74581b4f1c78bc457698eebb87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df277f07bf9f39912ead031f1036fab40271753475f6301a098bfefa16cf843f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringNotBeginsWith]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringNotBeginsWith]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringNotBeginsWith]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2c3feb700b1e07daa8dfc95c3ab19effe0e0f5dac86b02cb984d3736d587f24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridEventSubscriptionAdvancedFilterStringNotBeginsWithOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringNotBeginsWithOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10ed8216926375d163bdfe1a2174eceb4f5305c74d296d5f8979ca7e552120f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9f9d5f5286395d5b245a0c189c047937e395de0d190e1e9213e58d50d226b62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08825c489c0944488b46b1eb3f5cd55345e47a127c2c7c607ae32556b81fca48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringNotBeginsWith]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringNotBeginsWith]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringNotBeginsWith]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c36658ec8ab42158bd9736faa6d01db8dab4c7e3b26e4568c12b4b5de61ed04a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringNotContains",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridEventSubscriptionAdvancedFilterStringNotContains:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76f5c73fa5312665085acb16d8e2d8d2fb827f3a00663ed2af4282b988d09670)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionAdvancedFilterStringNotContains(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionAdvancedFilterStringNotContainsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringNotContainsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f8822e4f0d04127b2a9733bae423ad7ef304aeec1257ff9ff2d3cdf373743a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridEventSubscriptionAdvancedFilterStringNotContainsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7de299bc2e47ffb9c9e896cc973650a5abb0c0d93a23ad16df9fe33503f3e4c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridEventSubscriptionAdvancedFilterStringNotContainsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e474cea12dd55668cbb253935d5f5246f5fa340bdf26d4581f5f6100a806d65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cb9786125d667b0073bfec785efb980413f8df3790cd87e4e591ad34d0c4a39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f1821bfd6a23a6ab07317be8a719100487faba26fd4a5c5176bac74849a98b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringNotContains]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringNotContains]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringNotContains]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1429eaec94b8b2d13d569546ad74e698175a8f598cc51acfd89dd49f25aeb6a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridEventSubscriptionAdvancedFilterStringNotContainsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringNotContainsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0117e1ac141f5de7831607da67c1652ac40de09647110bbaa61e95fc1ddda797)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2fec4985ea270969ea19b6d0f9923afdf13a9d89b2c4dddbd7f327e1db07fb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ba948ea02b516b57d67c76cbab20cb3e70c9ca3cecb9ac7623e12e0e30b5744)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringNotContains]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringNotContains]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringNotContains]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c87abe195509a6fca567c0bff8d578658851d4f19c3b8e590248ef1ede8c6cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringNotEndsWith",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridEventSubscriptionAdvancedFilterStringNotEndsWith:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abfa5fed7cff01c08958f01aa95b0298342511bfb89ccc1410a030e75be1706e)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionAdvancedFilterStringNotEndsWith(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionAdvancedFilterStringNotEndsWithList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringNotEndsWithList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3195ce9f17b5ac70fa2ebbc951132fd5de1400bfa02a9164ad04b0bf330024be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridEventSubscriptionAdvancedFilterStringNotEndsWithOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dec21ab271538f54627ee5251d125e20a6d272dd473f0369d80f3e2da3c947d1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridEventSubscriptionAdvancedFilterStringNotEndsWithOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cacb5a78a28e2648abe6ef76a0ec9056e2b397eb14c559ddeaa781f4066c1156)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4680acddc79da1ea948ab44b89eca9c34fef452b46d1f6e9cd0b480abd625d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__274ba763b2890000583b6618c20d85b8546e9bdfeae3813aedf213ad11175685)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringNotEndsWith]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringNotEndsWith]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringNotEndsWith]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__332808cd1fcac732009496f2723891ca6ee8a47aa14ea7db6b2a7b2055ae2c13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridEventSubscriptionAdvancedFilterStringNotEndsWithOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringNotEndsWithOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aa85ada45e6286ec8a91e21188b7a88b83b426a765c211a7fa1246737b1ee7d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e684d7e26cb5ac1800662c0f4a8b6d0be8e2a144a29ebd02f30d07875662245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c42a3b8794a63145a584cfb764844371e764abfef4633b35889f629c34f207e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringNotEndsWith]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringNotEndsWith]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringNotEndsWith]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cb554901ed09544ea87995f6032ca334ef705ab132d6dc5bd5d9fa0a6ef2446)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringNotIn",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridEventSubscriptionAdvancedFilterStringNotIn:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad3b7d551d53f90f435d07161103df510dbe49e0640153f889e27a8a10982ac0)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#key EventgridEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#values EventgridEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionAdvancedFilterStringNotIn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionAdvancedFilterStringNotInList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringNotInList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d6d78ce4723c18008deddffd12f06a6989e94c4accb658c6c9c9cb66a1c812f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridEventSubscriptionAdvancedFilterStringNotInOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ec4b293641012a2c7e7dab520f108a1a50fc7bdf2790f31e2837ee75d484fc8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridEventSubscriptionAdvancedFilterStringNotInOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52d67a9dd483b541a15b4efa6ac52eb4db1856d6126e051a827275ac29904835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ace5e70a0df87a3f500dc9b2e703386b371bb3770830679cd27d0198c628152)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6807d2420c2b01ff114a783930eef90e467209737c3a446b7ecaa5db54dca611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringNotIn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringNotIn]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringNotIn]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f36a373b81d6af707311e812cc41a80fdf66f7c7c303462daa9d821366bc5d50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridEventSubscriptionAdvancedFilterStringNotInOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAdvancedFilterStringNotInOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29951b0b1fefe6a31c6c820182b23e93e11a23df55b83c00a5eb6ed75cc7177d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__179fdb57462b47c345874e7aaad02c2d872efc87919413d57099da1e7af3eb3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae80fcc3e05b40a3d78d6012f916d66a3367fce16f2bd3f07c8187faebcfe7a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringNotIn]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringNotIn]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringNotIn]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1786d14f0d167a6df0c04b02eccb97e4bdea14fbfcd8e3047fd162d8f5f7c645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAzureFunctionEndpoint",
    jsii_struct_bases=[],
    name_mapping={
        "function_id": "functionId",
        "max_events_per_batch": "maxEventsPerBatch",
        "preferred_batch_size_in_kilobytes": "preferredBatchSizeInKilobytes",
    },
)
class EventgridEventSubscriptionAzureFunctionEndpoint:
    def __init__(
        self,
        *,
        function_id: builtins.str,
        max_events_per_batch: typing.Optional[jsii.Number] = None,
        preferred_batch_size_in_kilobytes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param function_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#function_id EventgridEventSubscription#function_id}.
        :param max_events_per_batch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#max_events_per_batch EventgridEventSubscription#max_events_per_batch}.
        :param preferred_batch_size_in_kilobytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#preferred_batch_size_in_kilobytes EventgridEventSubscription#preferred_batch_size_in_kilobytes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6032229fda6725491236fd4a611f19439a951fd60b97ec81f94b6ac6f5b916db)
            check_type(argname="argument function_id", value=function_id, expected_type=type_hints["function_id"])
            check_type(argname="argument max_events_per_batch", value=max_events_per_batch, expected_type=type_hints["max_events_per_batch"])
            check_type(argname="argument preferred_batch_size_in_kilobytes", value=preferred_batch_size_in_kilobytes, expected_type=type_hints["preferred_batch_size_in_kilobytes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_id": function_id,
        }
        if max_events_per_batch is not None:
            self._values["max_events_per_batch"] = max_events_per_batch
        if preferred_batch_size_in_kilobytes is not None:
            self._values["preferred_batch_size_in_kilobytes"] = preferred_batch_size_in_kilobytes

    @builtins.property
    def function_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#function_id EventgridEventSubscription#function_id}.'''
        result = self._values.get("function_id")
        assert result is not None, "Required property 'function_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_events_per_batch(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#max_events_per_batch EventgridEventSubscription#max_events_per_batch}.'''
        result = self._values.get("max_events_per_batch")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preferred_batch_size_in_kilobytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#preferred_batch_size_in_kilobytes EventgridEventSubscription#preferred_batch_size_in_kilobytes}.'''
        result = self._values.get("preferred_batch_size_in_kilobytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionAzureFunctionEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionAzureFunctionEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionAzureFunctionEndpointOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d643d5ba58126287dc0e83085ae436da65c7aaebf07bd32f4b592427803881e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxEventsPerBatch")
    def reset_max_events_per_batch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxEventsPerBatch", []))

    @jsii.member(jsii_name="resetPreferredBatchSizeInKilobytes")
    def reset_preferred_batch_size_in_kilobytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreferredBatchSizeInKilobytes", []))

    @builtins.property
    @jsii.member(jsii_name="functionIdInput")
    def function_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="maxEventsPerBatchInput")
    def max_events_per_batch_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxEventsPerBatchInput"))

    @builtins.property
    @jsii.member(jsii_name="preferredBatchSizeInKilobytesInput")
    def preferred_batch_size_in_kilobytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "preferredBatchSizeInKilobytesInput"))

    @builtins.property
    @jsii.member(jsii_name="functionId")
    def function_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionId"))

    @function_id.setter
    def function_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f566d474116a67e4ff1db5963c630c0682c91e50fa28dd8724239f96b0beda9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxEventsPerBatch")
    def max_events_per_batch(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxEventsPerBatch"))

    @max_events_per_batch.setter
    def max_events_per_batch(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6466d4afa9fbdea506c5c11832266e2c996441765c319059048139314b0c5a1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxEventsPerBatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preferredBatchSizeInKilobytes")
    def preferred_batch_size_in_kilobytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "preferredBatchSizeInKilobytes"))

    @preferred_batch_size_in_kilobytes.setter
    def preferred_batch_size_in_kilobytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80be9615d4160e7a65fe5d43c0403d9007a23c562277069efd7837ff9b20abf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredBatchSizeInKilobytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventgridEventSubscriptionAzureFunctionEndpoint]:
        return typing.cast(typing.Optional[EventgridEventSubscriptionAzureFunctionEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventgridEventSubscriptionAzureFunctionEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4868872486341e3fad3349fc940733d04997ca1d0d73a12f9495c14cdb4df8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "scope": "scope",
        "advanced_filter": "advancedFilter",
        "advanced_filtering_on_arrays_enabled": "advancedFilteringOnArraysEnabled",
        "azure_function_endpoint": "azureFunctionEndpoint",
        "dead_letter_identity": "deadLetterIdentity",
        "delivery_identity": "deliveryIdentity",
        "delivery_property": "deliveryProperty",
        "event_delivery_schema": "eventDeliverySchema",
        "eventhub_endpoint_id": "eventhubEndpointId",
        "expiration_time_utc": "expirationTimeUtc",
        "hybrid_connection_endpoint_id": "hybridConnectionEndpointId",
        "id": "id",
        "included_event_types": "includedEventTypes",
        "labels": "labels",
        "retry_policy": "retryPolicy",
        "service_bus_queue_endpoint_id": "serviceBusQueueEndpointId",
        "service_bus_topic_endpoint_id": "serviceBusTopicEndpointId",
        "storage_blob_dead_letter_destination": "storageBlobDeadLetterDestination",
        "storage_queue_endpoint": "storageQueueEndpoint",
        "subject_filter": "subjectFilter",
        "timeouts": "timeouts",
        "webhook_endpoint": "webhookEndpoint",
    },
)
class EventgridEventSubscriptionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        name: builtins.str,
        scope: builtins.str,
        advanced_filter: typing.Optional[typing.Union[EventgridEventSubscriptionAdvancedFilter, typing.Dict[builtins.str, typing.Any]]] = None,
        advanced_filtering_on_arrays_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        azure_function_endpoint: typing.Optional[typing.Union[EventgridEventSubscriptionAzureFunctionEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
        dead_letter_identity: typing.Optional[typing.Union["EventgridEventSubscriptionDeadLetterIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        delivery_identity: typing.Optional[typing.Union["EventgridEventSubscriptionDeliveryIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        delivery_property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridEventSubscriptionDeliveryProperty", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_delivery_schema: typing.Optional[builtins.str] = None,
        eventhub_endpoint_id: typing.Optional[builtins.str] = None,
        expiration_time_utc: typing.Optional[builtins.str] = None,
        hybrid_connection_endpoint_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        included_event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        retry_policy: typing.Optional[typing.Union["EventgridEventSubscriptionRetryPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        service_bus_queue_endpoint_id: typing.Optional[builtins.str] = None,
        service_bus_topic_endpoint_id: typing.Optional[builtins.str] = None,
        storage_blob_dead_letter_destination: typing.Optional[typing.Union["EventgridEventSubscriptionStorageBlobDeadLetterDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_queue_endpoint: typing.Optional[typing.Union["EventgridEventSubscriptionStorageQueueEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
        subject_filter: typing.Optional[typing.Union["EventgridEventSubscriptionSubjectFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["EventgridEventSubscriptionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        webhook_endpoint: typing.Optional[typing.Union["EventgridEventSubscriptionWebhookEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#name EventgridEventSubscription#name}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#scope EventgridEventSubscription#scope}.
        :param advanced_filter: advanced_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#advanced_filter EventgridEventSubscription#advanced_filter}
        :param advanced_filtering_on_arrays_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#advanced_filtering_on_arrays_enabled EventgridEventSubscription#advanced_filtering_on_arrays_enabled}.
        :param azure_function_endpoint: azure_function_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#azure_function_endpoint EventgridEventSubscription#azure_function_endpoint}
        :param dead_letter_identity: dead_letter_identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#dead_letter_identity EventgridEventSubscription#dead_letter_identity}
        :param delivery_identity: delivery_identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#delivery_identity EventgridEventSubscription#delivery_identity}
        :param delivery_property: delivery_property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#delivery_property EventgridEventSubscription#delivery_property}
        :param event_delivery_schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#event_delivery_schema EventgridEventSubscription#event_delivery_schema}.
        :param eventhub_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#eventhub_endpoint_id EventgridEventSubscription#eventhub_endpoint_id}.
        :param expiration_time_utc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#expiration_time_utc EventgridEventSubscription#expiration_time_utc}.
        :param hybrid_connection_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#hybrid_connection_endpoint_id EventgridEventSubscription#hybrid_connection_endpoint_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#id EventgridEventSubscription#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param included_event_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#included_event_types EventgridEventSubscription#included_event_types}.
        :param labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#labels EventgridEventSubscription#labels}.
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#retry_policy EventgridEventSubscription#retry_policy}
        :param service_bus_queue_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#service_bus_queue_endpoint_id EventgridEventSubscription#service_bus_queue_endpoint_id}.
        :param service_bus_topic_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#service_bus_topic_endpoint_id EventgridEventSubscription#service_bus_topic_endpoint_id}.
        :param storage_blob_dead_letter_destination: storage_blob_dead_letter_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#storage_blob_dead_letter_destination EventgridEventSubscription#storage_blob_dead_letter_destination}
        :param storage_queue_endpoint: storage_queue_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#storage_queue_endpoint EventgridEventSubscription#storage_queue_endpoint}
        :param subject_filter: subject_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#subject_filter EventgridEventSubscription#subject_filter}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#timeouts EventgridEventSubscription#timeouts}
        :param webhook_endpoint: webhook_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#webhook_endpoint EventgridEventSubscription#webhook_endpoint}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(advanced_filter, dict):
            advanced_filter = EventgridEventSubscriptionAdvancedFilter(**advanced_filter)
        if isinstance(azure_function_endpoint, dict):
            azure_function_endpoint = EventgridEventSubscriptionAzureFunctionEndpoint(**azure_function_endpoint)
        if isinstance(dead_letter_identity, dict):
            dead_letter_identity = EventgridEventSubscriptionDeadLetterIdentity(**dead_letter_identity)
        if isinstance(delivery_identity, dict):
            delivery_identity = EventgridEventSubscriptionDeliveryIdentity(**delivery_identity)
        if isinstance(retry_policy, dict):
            retry_policy = EventgridEventSubscriptionRetryPolicy(**retry_policy)
        if isinstance(storage_blob_dead_letter_destination, dict):
            storage_blob_dead_letter_destination = EventgridEventSubscriptionStorageBlobDeadLetterDestination(**storage_blob_dead_letter_destination)
        if isinstance(storage_queue_endpoint, dict):
            storage_queue_endpoint = EventgridEventSubscriptionStorageQueueEndpoint(**storage_queue_endpoint)
        if isinstance(subject_filter, dict):
            subject_filter = EventgridEventSubscriptionSubjectFilter(**subject_filter)
        if isinstance(timeouts, dict):
            timeouts = EventgridEventSubscriptionTimeouts(**timeouts)
        if isinstance(webhook_endpoint, dict):
            webhook_endpoint = EventgridEventSubscriptionWebhookEndpoint(**webhook_endpoint)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a47c10c5cbbe163c0703b533052397a56ed3281e450faee112782c72f549b5ee)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument advanced_filter", value=advanced_filter, expected_type=type_hints["advanced_filter"])
            check_type(argname="argument advanced_filtering_on_arrays_enabled", value=advanced_filtering_on_arrays_enabled, expected_type=type_hints["advanced_filtering_on_arrays_enabled"])
            check_type(argname="argument azure_function_endpoint", value=azure_function_endpoint, expected_type=type_hints["azure_function_endpoint"])
            check_type(argname="argument dead_letter_identity", value=dead_letter_identity, expected_type=type_hints["dead_letter_identity"])
            check_type(argname="argument delivery_identity", value=delivery_identity, expected_type=type_hints["delivery_identity"])
            check_type(argname="argument delivery_property", value=delivery_property, expected_type=type_hints["delivery_property"])
            check_type(argname="argument event_delivery_schema", value=event_delivery_schema, expected_type=type_hints["event_delivery_schema"])
            check_type(argname="argument eventhub_endpoint_id", value=eventhub_endpoint_id, expected_type=type_hints["eventhub_endpoint_id"])
            check_type(argname="argument expiration_time_utc", value=expiration_time_utc, expected_type=type_hints["expiration_time_utc"])
            check_type(argname="argument hybrid_connection_endpoint_id", value=hybrid_connection_endpoint_id, expected_type=type_hints["hybrid_connection_endpoint_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument included_event_types", value=included_event_types, expected_type=type_hints["included_event_types"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument retry_policy", value=retry_policy, expected_type=type_hints["retry_policy"])
            check_type(argname="argument service_bus_queue_endpoint_id", value=service_bus_queue_endpoint_id, expected_type=type_hints["service_bus_queue_endpoint_id"])
            check_type(argname="argument service_bus_topic_endpoint_id", value=service_bus_topic_endpoint_id, expected_type=type_hints["service_bus_topic_endpoint_id"])
            check_type(argname="argument storage_blob_dead_letter_destination", value=storage_blob_dead_letter_destination, expected_type=type_hints["storage_blob_dead_letter_destination"])
            check_type(argname="argument storage_queue_endpoint", value=storage_queue_endpoint, expected_type=type_hints["storage_queue_endpoint"])
            check_type(argname="argument subject_filter", value=subject_filter, expected_type=type_hints["subject_filter"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument webhook_endpoint", value=webhook_endpoint, expected_type=type_hints["webhook_endpoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "scope": scope,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if advanced_filter is not None:
            self._values["advanced_filter"] = advanced_filter
        if advanced_filtering_on_arrays_enabled is not None:
            self._values["advanced_filtering_on_arrays_enabled"] = advanced_filtering_on_arrays_enabled
        if azure_function_endpoint is not None:
            self._values["azure_function_endpoint"] = azure_function_endpoint
        if dead_letter_identity is not None:
            self._values["dead_letter_identity"] = dead_letter_identity
        if delivery_identity is not None:
            self._values["delivery_identity"] = delivery_identity
        if delivery_property is not None:
            self._values["delivery_property"] = delivery_property
        if event_delivery_schema is not None:
            self._values["event_delivery_schema"] = event_delivery_schema
        if eventhub_endpoint_id is not None:
            self._values["eventhub_endpoint_id"] = eventhub_endpoint_id
        if expiration_time_utc is not None:
            self._values["expiration_time_utc"] = expiration_time_utc
        if hybrid_connection_endpoint_id is not None:
            self._values["hybrid_connection_endpoint_id"] = hybrid_connection_endpoint_id
        if id is not None:
            self._values["id"] = id
        if included_event_types is not None:
            self._values["included_event_types"] = included_event_types
        if labels is not None:
            self._values["labels"] = labels
        if retry_policy is not None:
            self._values["retry_policy"] = retry_policy
        if service_bus_queue_endpoint_id is not None:
            self._values["service_bus_queue_endpoint_id"] = service_bus_queue_endpoint_id
        if service_bus_topic_endpoint_id is not None:
            self._values["service_bus_topic_endpoint_id"] = service_bus_topic_endpoint_id
        if storage_blob_dead_letter_destination is not None:
            self._values["storage_blob_dead_letter_destination"] = storage_blob_dead_letter_destination
        if storage_queue_endpoint is not None:
            self._values["storage_queue_endpoint"] = storage_queue_endpoint
        if subject_filter is not None:
            self._values["subject_filter"] = subject_filter
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if webhook_endpoint is not None:
            self._values["webhook_endpoint"] = webhook_endpoint

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#name EventgridEventSubscription#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#scope EventgridEventSubscription#scope}.'''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def advanced_filter(
        self,
    ) -> typing.Optional[EventgridEventSubscriptionAdvancedFilter]:
        '''advanced_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#advanced_filter EventgridEventSubscription#advanced_filter}
        '''
        result = self._values.get("advanced_filter")
        return typing.cast(typing.Optional[EventgridEventSubscriptionAdvancedFilter], result)

    @builtins.property
    def advanced_filtering_on_arrays_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#advanced_filtering_on_arrays_enabled EventgridEventSubscription#advanced_filtering_on_arrays_enabled}.'''
        result = self._values.get("advanced_filtering_on_arrays_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def azure_function_endpoint(
        self,
    ) -> typing.Optional[EventgridEventSubscriptionAzureFunctionEndpoint]:
        '''azure_function_endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#azure_function_endpoint EventgridEventSubscription#azure_function_endpoint}
        '''
        result = self._values.get("azure_function_endpoint")
        return typing.cast(typing.Optional[EventgridEventSubscriptionAzureFunctionEndpoint], result)

    @builtins.property
    def dead_letter_identity(
        self,
    ) -> typing.Optional["EventgridEventSubscriptionDeadLetterIdentity"]:
        '''dead_letter_identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#dead_letter_identity EventgridEventSubscription#dead_letter_identity}
        '''
        result = self._values.get("dead_letter_identity")
        return typing.cast(typing.Optional["EventgridEventSubscriptionDeadLetterIdentity"], result)

    @builtins.property
    def delivery_identity(
        self,
    ) -> typing.Optional["EventgridEventSubscriptionDeliveryIdentity"]:
        '''delivery_identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#delivery_identity EventgridEventSubscription#delivery_identity}
        '''
        result = self._values.get("delivery_identity")
        return typing.cast(typing.Optional["EventgridEventSubscriptionDeliveryIdentity"], result)

    @builtins.property
    def delivery_property(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionDeliveryProperty"]]]:
        '''delivery_property block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#delivery_property EventgridEventSubscription#delivery_property}
        '''
        result = self._values.get("delivery_property")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridEventSubscriptionDeliveryProperty"]]], result)

    @builtins.property
    def event_delivery_schema(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#event_delivery_schema EventgridEventSubscription#event_delivery_schema}.'''
        result = self._values.get("event_delivery_schema")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eventhub_endpoint_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#eventhub_endpoint_id EventgridEventSubscription#eventhub_endpoint_id}.'''
        result = self._values.get("eventhub_endpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expiration_time_utc(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#expiration_time_utc EventgridEventSubscription#expiration_time_utc}.'''
        result = self._values.get("expiration_time_utc")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hybrid_connection_endpoint_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#hybrid_connection_endpoint_id EventgridEventSubscription#hybrid_connection_endpoint_id}.'''
        result = self._values.get("hybrid_connection_endpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#id EventgridEventSubscription#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def included_event_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#included_event_types EventgridEventSubscription#included_event_types}.'''
        result = self._values.get("included_event_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#labels EventgridEventSubscription#labels}.'''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def retry_policy(self) -> typing.Optional["EventgridEventSubscriptionRetryPolicy"]:
        '''retry_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#retry_policy EventgridEventSubscription#retry_policy}
        '''
        result = self._values.get("retry_policy")
        return typing.cast(typing.Optional["EventgridEventSubscriptionRetryPolicy"], result)

    @builtins.property
    def service_bus_queue_endpoint_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#service_bus_queue_endpoint_id EventgridEventSubscription#service_bus_queue_endpoint_id}.'''
        result = self._values.get("service_bus_queue_endpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_bus_topic_endpoint_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#service_bus_topic_endpoint_id EventgridEventSubscription#service_bus_topic_endpoint_id}.'''
        result = self._values.get("service_bus_topic_endpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_blob_dead_letter_destination(
        self,
    ) -> typing.Optional["EventgridEventSubscriptionStorageBlobDeadLetterDestination"]:
        '''storage_blob_dead_letter_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#storage_blob_dead_letter_destination EventgridEventSubscription#storage_blob_dead_letter_destination}
        '''
        result = self._values.get("storage_blob_dead_letter_destination")
        return typing.cast(typing.Optional["EventgridEventSubscriptionStorageBlobDeadLetterDestination"], result)

    @builtins.property
    def storage_queue_endpoint(
        self,
    ) -> typing.Optional["EventgridEventSubscriptionStorageQueueEndpoint"]:
        '''storage_queue_endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#storage_queue_endpoint EventgridEventSubscription#storage_queue_endpoint}
        '''
        result = self._values.get("storage_queue_endpoint")
        return typing.cast(typing.Optional["EventgridEventSubscriptionStorageQueueEndpoint"], result)

    @builtins.property
    def subject_filter(
        self,
    ) -> typing.Optional["EventgridEventSubscriptionSubjectFilter"]:
        '''subject_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#subject_filter EventgridEventSubscription#subject_filter}
        '''
        result = self._values.get("subject_filter")
        return typing.cast(typing.Optional["EventgridEventSubscriptionSubjectFilter"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["EventgridEventSubscriptionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#timeouts EventgridEventSubscription#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["EventgridEventSubscriptionTimeouts"], result)

    @builtins.property
    def webhook_endpoint(
        self,
    ) -> typing.Optional["EventgridEventSubscriptionWebhookEndpoint"]:
        '''webhook_endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#webhook_endpoint EventgridEventSubscription#webhook_endpoint}
        '''
        result = self._values.get("webhook_endpoint")
        return typing.cast(typing.Optional["EventgridEventSubscriptionWebhookEndpoint"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionDeadLetterIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "user_assigned_identity": "userAssignedIdentity"},
)
class EventgridEventSubscriptionDeadLetterIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        user_assigned_identity: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#type EventgridEventSubscription#type}.
        :param user_assigned_identity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#user_assigned_identity EventgridEventSubscription#user_assigned_identity}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__505f88d1f8177b3af223a700ca2180de5534e263d75d74ed71ce44986e4607bc)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument user_assigned_identity", value=user_assigned_identity, expected_type=type_hints["user_assigned_identity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if user_assigned_identity is not None:
            self._values["user_assigned_identity"] = user_assigned_identity

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#type EventgridEventSubscription#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_assigned_identity(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#user_assigned_identity EventgridEventSubscription#user_assigned_identity}.'''
        result = self._values.get("user_assigned_identity")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionDeadLetterIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionDeadLetterIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionDeadLetterIdentityOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4b9ad7a88a1b4568397cc06ff0cd703e7dc5eb08bedf2d8c1a89cc86e960ef5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUserAssignedIdentity")
    def reset_user_assigned_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserAssignedIdentity", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentityInput")
    def user_assigned_identity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userAssignedIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22a5df8a9c6fa9f9a9c40f1bb259f8c53d916925dc1543225cfda14685d42274)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentity")
    def user_assigned_identity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAssignedIdentity"))

    @user_assigned_identity.setter
    def user_assigned_identity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d5fac2a9e45d475485f2b6c1406c8759bcadc35797941abfbf791a7f3d33ae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAssignedIdentity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventgridEventSubscriptionDeadLetterIdentity]:
        return typing.cast(typing.Optional[EventgridEventSubscriptionDeadLetterIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventgridEventSubscriptionDeadLetterIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95e434b20e4631c2ed72fe0e23772dac7a4b3aa89e8430245ce9a8a29d2a0c41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionDeliveryIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "user_assigned_identity": "userAssignedIdentity"},
)
class EventgridEventSubscriptionDeliveryIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        user_assigned_identity: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#type EventgridEventSubscription#type}.
        :param user_assigned_identity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#user_assigned_identity EventgridEventSubscription#user_assigned_identity}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d2d00d51633b594e9a6f1b7bb3d63e4c39a6d0a51455f23dbffbacbf9385ee6)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument user_assigned_identity", value=user_assigned_identity, expected_type=type_hints["user_assigned_identity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if user_assigned_identity is not None:
            self._values["user_assigned_identity"] = user_assigned_identity

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#type EventgridEventSubscription#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_assigned_identity(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#user_assigned_identity EventgridEventSubscription#user_assigned_identity}.'''
        result = self._values.get("user_assigned_identity")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionDeliveryIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionDeliveryIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionDeliveryIdentityOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7538b2c3ca46b5b3f4bd84c273201bafe6dcc644f60f8497619b892a855eca8b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUserAssignedIdentity")
    def reset_user_assigned_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserAssignedIdentity", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentityInput")
    def user_assigned_identity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userAssignedIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41e0c3836772afeb6856ff24ce6b2d42667777c42c9dc1ceffb2325db1ef2878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentity")
    def user_assigned_identity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAssignedIdentity"))

    @user_assigned_identity.setter
    def user_assigned_identity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__795c047d0e676696bc70a91b74749342331b4b77d7c2ef68e1aff62810365394)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAssignedIdentity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventgridEventSubscriptionDeliveryIdentity]:
        return typing.cast(typing.Optional[EventgridEventSubscriptionDeliveryIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventgridEventSubscriptionDeliveryIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fffaae8ba3642b29ca6a240bfa10d94cb954d4953caae9765c1cd885f1e7fc2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionDeliveryProperty",
    jsii_struct_bases=[],
    name_mapping={
        "header_name": "headerName",
        "type": "type",
        "secret": "secret",
        "source_field": "sourceField",
        "value": "value",
    },
)
class EventgridEventSubscriptionDeliveryProperty:
    def __init__(
        self,
        *,
        header_name: builtins.str,
        type: builtins.str,
        secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_field: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#header_name EventgridEventSubscription#header_name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#type EventgridEventSubscription#type}.
        :param secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#secret EventgridEventSubscription#secret}.
        :param source_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#source_field EventgridEventSubscription#source_field}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#value EventgridEventSubscription#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b0e5902fefa563a2d252ecc837656cd2db3af423c264bb5681e5e9e6607f305)
            check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument source_field", value=source_field, expected_type=type_hints["source_field"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header_name": header_name,
            "type": type,
        }
        if secret is not None:
            self._values["secret"] = secret
        if source_field is not None:
            self._values["source_field"] = source_field
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def header_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#header_name EventgridEventSubscription#header_name}.'''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#type EventgridEventSubscription#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#secret EventgridEventSubscription#secret}.'''
        result = self._values.get("secret")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def source_field(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#source_field EventgridEventSubscription#source_field}.'''
        result = self._values.get("source_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#value EventgridEventSubscription#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionDeliveryProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionDeliveryPropertyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionDeliveryPropertyList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23d395f2e85c9b0e9a9ca72445a4b270623ae4cf0b5c9d9076e6505adb208d52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridEventSubscriptionDeliveryPropertyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4637db758c1a54c963f962d4b355528d31a9040165f80e5b11ba43ef6fe46d97)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridEventSubscriptionDeliveryPropertyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bf28c3c433b6851acc1cd1bf54cedb334405ba0d20f06ee5b4cae3f881d8c32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24450b57c4760e9ebbee54b006259a411be15b5c5bc8275fa2f11d7f97d61389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20a38c533270824ba06e115f2febc7223711fc627050be1c46b145d87e54ca56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionDeliveryProperty]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionDeliveryProperty]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionDeliveryProperty]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fecb6d5537d9b46397224bfb00dae7b3ed8bf724af8e5064bd9a32f40194cec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridEventSubscriptionDeliveryPropertyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionDeliveryPropertyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cef29c033faeab8486133d68f794c9d20e3f18e6abcaa264057111c26ba2a160)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSecret")
    def reset_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecret", []))

    @jsii.member(jsii_name="resetSourceField")
    def reset_source_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceField", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="headerNameInput")
    def header_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFieldInput")
    def source_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="headerName")
    def header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerName"))

    @header_name.setter
    def header_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b3d5f3e16e9c4b7bbdd6d65afb9300731484308f55a1f7f8d183d89be123cdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "secret"))

    @secret.setter
    def secret(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53f6bc75e34dea9d23291b67403848b229ecd002228f7cb3a1a6b655fcaae64f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceField")
    def source_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceField"))

    @source_field.setter
    def source_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2f69a815932128971d348c474867aad2fc980da8e60a7151c1cb1af2ddf2543)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b22266edb0f69bb177bdd45981f63a902fbf0ab7ab6b7e8918cf3dc58d1e3a4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c40c4a00160bc69f43d81c8c5df4740994400722987f91c2c6f06619a2a52ea3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionDeliveryProperty]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionDeliveryProperty]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionDeliveryProperty]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1d3778f1b2e4c68b4d02fa48cd55bacdbc2ed3e47c9c104d4c3b963c5420560)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionRetryPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "event_time_to_live": "eventTimeToLive",
        "max_delivery_attempts": "maxDeliveryAttempts",
    },
)
class EventgridEventSubscriptionRetryPolicy:
    def __init__(
        self,
        *,
        event_time_to_live: jsii.Number,
        max_delivery_attempts: jsii.Number,
    ) -> None:
        '''
        :param event_time_to_live: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#event_time_to_live EventgridEventSubscription#event_time_to_live}.
        :param max_delivery_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#max_delivery_attempts EventgridEventSubscription#max_delivery_attempts}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17304d3161cd9dba3da93e0821b9ad18306e7e56ea35337d522a37510d34afe0)
            check_type(argname="argument event_time_to_live", value=event_time_to_live, expected_type=type_hints["event_time_to_live"])
            check_type(argname="argument max_delivery_attempts", value=max_delivery_attempts, expected_type=type_hints["max_delivery_attempts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_time_to_live": event_time_to_live,
            "max_delivery_attempts": max_delivery_attempts,
        }

    @builtins.property
    def event_time_to_live(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#event_time_to_live EventgridEventSubscription#event_time_to_live}.'''
        result = self._values.get("event_time_to_live")
        assert result is not None, "Required property 'event_time_to_live' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def max_delivery_attempts(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#max_delivery_attempts EventgridEventSubscription#max_delivery_attempts}.'''
        result = self._values.get("max_delivery_attempts")
        assert result is not None, "Required property 'max_delivery_attempts' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionRetryPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionRetryPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionRetryPolicyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cc181ee6b7bae300d380ecb9cf9908fcfcd5c94a543b454c2d92d38f8914583)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="eventTimeToLiveInput")
    def event_time_to_live_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "eventTimeToLiveInput"))

    @builtins.property
    @jsii.member(jsii_name="maxDeliveryAttemptsInput")
    def max_delivery_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxDeliveryAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="eventTimeToLive")
    def event_time_to_live(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "eventTimeToLive"))

    @event_time_to_live.setter
    def event_time_to_live(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03faf4f793e4aaa2bd313b136e9332d2d091ba41a3261c8ca4656fa2de892642)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventTimeToLive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDeliveryAttempts")
    def max_delivery_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDeliveryAttempts"))

    @max_delivery_attempts.setter
    def max_delivery_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd529ac08146910cc73bfb18385348c7ab3f0377898efd42fc62b1e500ed5db1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDeliveryAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EventgridEventSubscriptionRetryPolicy]:
        return typing.cast(typing.Optional[EventgridEventSubscriptionRetryPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventgridEventSubscriptionRetryPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d52e3e46e349c8067058884d50adbb6cb85a32025b4e01925380bd84a0ea986)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionStorageBlobDeadLetterDestination",
    jsii_struct_bases=[],
    name_mapping={
        "storage_account_id": "storageAccountId",
        "storage_blob_container_name": "storageBlobContainerName",
    },
)
class EventgridEventSubscriptionStorageBlobDeadLetterDestination:
    def __init__(
        self,
        *,
        storage_account_id: builtins.str,
        storage_blob_container_name: builtins.str,
    ) -> None:
        '''
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#storage_account_id EventgridEventSubscription#storage_account_id}.
        :param storage_blob_container_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#storage_blob_container_name EventgridEventSubscription#storage_blob_container_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16483da8ee1bafe800d108ab40023447af20e116475878b33486f0d151787512)
            check_type(argname="argument storage_account_id", value=storage_account_id, expected_type=type_hints["storage_account_id"])
            check_type(argname="argument storage_blob_container_name", value=storage_blob_container_name, expected_type=type_hints["storage_blob_container_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "storage_account_id": storage_account_id,
            "storage_blob_container_name": storage_blob_container_name,
        }

    @builtins.property
    def storage_account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#storage_account_id EventgridEventSubscription#storage_account_id}.'''
        result = self._values.get("storage_account_id")
        assert result is not None, "Required property 'storage_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_blob_container_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#storage_blob_container_name EventgridEventSubscription#storage_blob_container_name}.'''
        result = self._values.get("storage_blob_container_name")
        assert result is not None, "Required property 'storage_blob_container_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionStorageBlobDeadLetterDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionStorageBlobDeadLetterDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionStorageBlobDeadLetterDestinationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86d0bee0254d19166ee9ef249b56d0037159ac0770d535eb94f656ec7912ed4e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="storageAccountIdInput")
    def storage_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="storageBlobContainerNameInput")
    def storage_blob_container_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageBlobContainerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountId")
    def storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountId"))

    @storage_account_id.setter
    def storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a6528be3b8b23356e102ba0e669abcf779bdd0dbdae67fa2912eff250d4857d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageBlobContainerName")
    def storage_blob_container_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageBlobContainerName"))

    @storage_blob_container_name.setter
    def storage_blob_container_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa61eeb0f161a42a6d3d4d275826728fd9a97716e17d148157b4c6440f25a644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageBlobContainerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventgridEventSubscriptionStorageBlobDeadLetterDestination]:
        return typing.cast(typing.Optional[EventgridEventSubscriptionStorageBlobDeadLetterDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventgridEventSubscriptionStorageBlobDeadLetterDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d30c5a4ebb4799863a66839ce474cab30a4b7866acdc4337e9eaa29fc2331f41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionStorageQueueEndpoint",
    jsii_struct_bases=[],
    name_mapping={
        "queue_name": "queueName",
        "storage_account_id": "storageAccountId",
        "queue_message_time_to_live_in_seconds": "queueMessageTimeToLiveInSeconds",
    },
)
class EventgridEventSubscriptionStorageQueueEndpoint:
    def __init__(
        self,
        *,
        queue_name: builtins.str,
        storage_account_id: builtins.str,
        queue_message_time_to_live_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param queue_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#queue_name EventgridEventSubscription#queue_name}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#storage_account_id EventgridEventSubscription#storage_account_id}.
        :param queue_message_time_to_live_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#queue_message_time_to_live_in_seconds EventgridEventSubscription#queue_message_time_to_live_in_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08dfd9584acdfa5a71777f8cae4a67897b755d82b3a43f45ab8fbc827984fe4e)
            check_type(argname="argument queue_name", value=queue_name, expected_type=type_hints["queue_name"])
            check_type(argname="argument storage_account_id", value=storage_account_id, expected_type=type_hints["storage_account_id"])
            check_type(argname="argument queue_message_time_to_live_in_seconds", value=queue_message_time_to_live_in_seconds, expected_type=type_hints["queue_message_time_to_live_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "queue_name": queue_name,
            "storage_account_id": storage_account_id,
        }
        if queue_message_time_to_live_in_seconds is not None:
            self._values["queue_message_time_to_live_in_seconds"] = queue_message_time_to_live_in_seconds

    @builtins.property
    def queue_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#queue_name EventgridEventSubscription#queue_name}.'''
        result = self._values.get("queue_name")
        assert result is not None, "Required property 'queue_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#storage_account_id EventgridEventSubscription#storage_account_id}.'''
        result = self._values.get("storage_account_id")
        assert result is not None, "Required property 'storage_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def queue_message_time_to_live_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#queue_message_time_to_live_in_seconds EventgridEventSubscription#queue_message_time_to_live_in_seconds}.'''
        result = self._values.get("queue_message_time_to_live_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionStorageQueueEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionStorageQueueEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionStorageQueueEndpointOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5790fcc18274f3ccf81d779d636696566f1950ef44308d49a69ab6226a36427)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetQueueMessageTimeToLiveInSeconds")
    def reset_queue_message_time_to_live_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueueMessageTimeToLiveInSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="queueMessageTimeToLiveInSecondsInput")
    def queue_message_time_to_live_in_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "queueMessageTimeToLiveInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="queueNameInput")
    def queue_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queueNameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountIdInput")
    def storage_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="queueMessageTimeToLiveInSeconds")
    def queue_message_time_to_live_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queueMessageTimeToLiveInSeconds"))

    @queue_message_time_to_live_in_seconds.setter
    def queue_message_time_to_live_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54fb26ecfab33479dba94c72dc05f8cc775a4618b703abf6d3ecfe29991b02fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueMessageTimeToLiveInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queueName"))

    @queue_name.setter
    def queue_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b3f4a595ba8056c1e3cef1d75400d8dd40f6441c2f840349a473044169a3e18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountId")
    def storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountId"))

    @storage_account_id.setter
    def storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cc4a19680d7503fd2abe4948921e4fde9355704eb6b3b29034581125300d3b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventgridEventSubscriptionStorageQueueEndpoint]:
        return typing.cast(typing.Optional[EventgridEventSubscriptionStorageQueueEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventgridEventSubscriptionStorageQueueEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe170e67648cc2de1d2614e32181b4ee9e42457c1095bcffc488325c20989393)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionSubjectFilter",
    jsii_struct_bases=[],
    name_mapping={
        "case_sensitive": "caseSensitive",
        "subject_begins_with": "subjectBeginsWith",
        "subject_ends_with": "subjectEndsWith",
    },
)
class EventgridEventSubscriptionSubjectFilter:
    def __init__(
        self,
        *,
        case_sensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subject_begins_with: typing.Optional[builtins.str] = None,
        subject_ends_with: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param case_sensitive: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#case_sensitive EventgridEventSubscription#case_sensitive}.
        :param subject_begins_with: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#subject_begins_with EventgridEventSubscription#subject_begins_with}.
        :param subject_ends_with: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#subject_ends_with EventgridEventSubscription#subject_ends_with}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc2e10a280055d54d4aba9583bfe2f32057fe1f09e48f95afa51da8a36a9bf6b)
            check_type(argname="argument case_sensitive", value=case_sensitive, expected_type=type_hints["case_sensitive"])
            check_type(argname="argument subject_begins_with", value=subject_begins_with, expected_type=type_hints["subject_begins_with"])
            check_type(argname="argument subject_ends_with", value=subject_ends_with, expected_type=type_hints["subject_ends_with"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if case_sensitive is not None:
            self._values["case_sensitive"] = case_sensitive
        if subject_begins_with is not None:
            self._values["subject_begins_with"] = subject_begins_with
        if subject_ends_with is not None:
            self._values["subject_ends_with"] = subject_ends_with

    @builtins.property
    def case_sensitive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#case_sensitive EventgridEventSubscription#case_sensitive}.'''
        result = self._values.get("case_sensitive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def subject_begins_with(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#subject_begins_with EventgridEventSubscription#subject_begins_with}.'''
        result = self._values.get("subject_begins_with")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_ends_with(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#subject_ends_with EventgridEventSubscription#subject_ends_with}.'''
        result = self._values.get("subject_ends_with")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionSubjectFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionSubjectFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionSubjectFilterOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f19847a004083c65ff1be9dd0745431a4c711c9c00cd19f3827f4a458358e04)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCaseSensitive")
    def reset_case_sensitive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaseSensitive", []))

    @jsii.member(jsii_name="resetSubjectBeginsWith")
    def reset_subject_begins_with(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectBeginsWith", []))

    @jsii.member(jsii_name="resetSubjectEndsWith")
    def reset_subject_ends_with(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectEndsWith", []))

    @builtins.property
    @jsii.member(jsii_name="caseSensitiveInput")
    def case_sensitive_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "caseSensitiveInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectBeginsWithInput")
    def subject_begins_with_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectBeginsWithInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectEndsWithInput")
    def subject_ends_with_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectEndsWithInput"))

    @builtins.property
    @jsii.member(jsii_name="caseSensitive")
    def case_sensitive(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "caseSensitive"))

    @case_sensitive.setter
    def case_sensitive(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8faa62454829ff7dfc939420647d0c040515ab9d716d574ffa0d79d1b2024257)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caseSensitive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subjectBeginsWith")
    def subject_begins_with(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectBeginsWith"))

    @subject_begins_with.setter
    def subject_begins_with(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc46f83ee80555f0388074bd3e031703b1f0981fc5f699b4f67b2c9dd14266fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectBeginsWith", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subjectEndsWith")
    def subject_ends_with(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectEndsWith"))

    @subject_ends_with.setter
    def subject_ends_with(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be2e095be12a66bfb7518dfb2487bedb65884533a143a325fdb15c55f21324e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectEndsWith", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventgridEventSubscriptionSubjectFilter]:
        return typing.cast(typing.Optional[EventgridEventSubscriptionSubjectFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventgridEventSubscriptionSubjectFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__453d631be394f719b5e3b5e712dc048a190db308fae195dbf13cde35f0b7b4f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class EventgridEventSubscriptionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#create EventgridEventSubscription#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#delete EventgridEventSubscription#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#read EventgridEventSubscription#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#update EventgridEventSubscription#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1885ea55e459bf192a4b8c1941ec4a175788ef949c3f83024427bd8fb37814aa)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#create EventgridEventSubscription#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#delete EventgridEventSubscription#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#read EventgridEventSubscription#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#update EventgridEventSubscription#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__348ba6a9814af0ea9c279c3cc6a32e4d4ef4dd81f53208008c472d4a8795d200)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__418390961faab8ec0597e2655c94c124233bae1bec84adc70722dcea91b9aa66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__364ccf4babb7d84286b1afdca360fdafda187072a90a1b854c40a907776fd137)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a7e2004ac1b1cd5b8449711ddee58044656b6c8b6aa207ca89d9ad8516256e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1a9b13cfc2c9aa6fc0595aba892c110be274aff6673a3c3801bae02eb058235)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7556aff4d7903a4c66fab770f28393086015b195a0861dd4324fb4c57c7e5f6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionWebhookEndpoint",
    jsii_struct_bases=[],
    name_mapping={
        "url": "url",
        "active_directory_app_id_or_uri": "activeDirectoryAppIdOrUri",
        "active_directory_tenant_id": "activeDirectoryTenantId",
        "max_events_per_batch": "maxEventsPerBatch",
        "preferred_batch_size_in_kilobytes": "preferredBatchSizeInKilobytes",
    },
)
class EventgridEventSubscriptionWebhookEndpoint:
    def __init__(
        self,
        *,
        url: builtins.str,
        active_directory_app_id_or_uri: typing.Optional[builtins.str] = None,
        active_directory_tenant_id: typing.Optional[builtins.str] = None,
        max_events_per_batch: typing.Optional[jsii.Number] = None,
        preferred_batch_size_in_kilobytes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#url EventgridEventSubscription#url}.
        :param active_directory_app_id_or_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#active_directory_app_id_or_uri EventgridEventSubscription#active_directory_app_id_or_uri}.
        :param active_directory_tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#active_directory_tenant_id EventgridEventSubscription#active_directory_tenant_id}.
        :param max_events_per_batch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#max_events_per_batch EventgridEventSubscription#max_events_per_batch}.
        :param preferred_batch_size_in_kilobytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#preferred_batch_size_in_kilobytes EventgridEventSubscription#preferred_batch_size_in_kilobytes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65e2e3d6c1e4ecdc1d40c723957606e84454efb2505602704b448946e8f99f0b)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument active_directory_app_id_or_uri", value=active_directory_app_id_or_uri, expected_type=type_hints["active_directory_app_id_or_uri"])
            check_type(argname="argument active_directory_tenant_id", value=active_directory_tenant_id, expected_type=type_hints["active_directory_tenant_id"])
            check_type(argname="argument max_events_per_batch", value=max_events_per_batch, expected_type=type_hints["max_events_per_batch"])
            check_type(argname="argument preferred_batch_size_in_kilobytes", value=preferred_batch_size_in_kilobytes, expected_type=type_hints["preferred_batch_size_in_kilobytes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if active_directory_app_id_or_uri is not None:
            self._values["active_directory_app_id_or_uri"] = active_directory_app_id_or_uri
        if active_directory_tenant_id is not None:
            self._values["active_directory_tenant_id"] = active_directory_tenant_id
        if max_events_per_batch is not None:
            self._values["max_events_per_batch"] = max_events_per_batch
        if preferred_batch_size_in_kilobytes is not None:
            self._values["preferred_batch_size_in_kilobytes"] = preferred_batch_size_in_kilobytes

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#url EventgridEventSubscription#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def active_directory_app_id_or_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#active_directory_app_id_or_uri EventgridEventSubscription#active_directory_app_id_or_uri}.'''
        result = self._values.get("active_directory_app_id_or_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def active_directory_tenant_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#active_directory_tenant_id EventgridEventSubscription#active_directory_tenant_id}.'''
        result = self._values.get("active_directory_tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_events_per_batch(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#max_events_per_batch EventgridEventSubscription#max_events_per_batch}.'''
        result = self._values.get("max_events_per_batch")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preferred_batch_size_in_kilobytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_event_subscription#preferred_batch_size_in_kilobytes EventgridEventSubscription#preferred_batch_size_in_kilobytes}.'''
        result = self._values.get("preferred_batch_size_in_kilobytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridEventSubscriptionWebhookEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridEventSubscriptionWebhookEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridEventSubscription.EventgridEventSubscriptionWebhookEndpointOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__046e3ccfedba392de97e487357bdd15d1176d605ed0e48c1c5eab49b545bdf85)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetActiveDirectoryAppIdOrUri")
    def reset_active_directory_app_id_or_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveDirectoryAppIdOrUri", []))

    @jsii.member(jsii_name="resetActiveDirectoryTenantId")
    def reset_active_directory_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveDirectoryTenantId", []))

    @jsii.member(jsii_name="resetMaxEventsPerBatch")
    def reset_max_events_per_batch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxEventsPerBatch", []))

    @jsii.member(jsii_name="resetPreferredBatchSizeInKilobytes")
    def reset_preferred_batch_size_in_kilobytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreferredBatchSizeInKilobytes", []))

    @builtins.property
    @jsii.member(jsii_name="baseUrl")
    def base_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseUrl"))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryAppIdOrUriInput")
    def active_directory_app_id_or_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "activeDirectoryAppIdOrUriInput"))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryTenantIdInput")
    def active_directory_tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "activeDirectoryTenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="maxEventsPerBatchInput")
    def max_events_per_batch_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxEventsPerBatchInput"))

    @builtins.property
    @jsii.member(jsii_name="preferredBatchSizeInKilobytesInput")
    def preferred_batch_size_in_kilobytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "preferredBatchSizeInKilobytesInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryAppIdOrUri")
    def active_directory_app_id_or_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "activeDirectoryAppIdOrUri"))

    @active_directory_app_id_or_uri.setter
    def active_directory_app_id_or_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cae53e620f033a0a4f6ba294a4508b94fb354b7d6c4f5fa8ea3fc646aa5fec3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activeDirectoryAppIdOrUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryTenantId")
    def active_directory_tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "activeDirectoryTenantId"))

    @active_directory_tenant_id.setter
    def active_directory_tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f10e2dc33c7e5593024ace05cb5121f7983b0e4e5fde59792cd6509144d9c1bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activeDirectoryTenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxEventsPerBatch")
    def max_events_per_batch(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxEventsPerBatch"))

    @max_events_per_batch.setter
    def max_events_per_batch(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2814710f56e10728da3a130e3aa5560976f0c35b6123f4d5d9fabcbd284a9aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxEventsPerBatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preferredBatchSizeInKilobytes")
    def preferred_batch_size_in_kilobytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "preferredBatchSizeInKilobytes"))

    @preferred_batch_size_in_kilobytes.setter
    def preferred_batch_size_in_kilobytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0b98abc97c2b224232102e9af21d9ddaabc8912e2e038f4453587ba70a342a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredBatchSizeInKilobytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ed5fd1fcbd0c55752984b4cc4c130652cb7ebdeb5eee40273eca747726d3d4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventgridEventSubscriptionWebhookEndpoint]:
        return typing.cast(typing.Optional[EventgridEventSubscriptionWebhookEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventgridEventSubscriptionWebhookEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a54e5ede82e3f4dfdaa0d8d5218dd95acaee8a25310032ed2dfc9f608ba11d2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "EventgridEventSubscription",
    "EventgridEventSubscriptionAdvancedFilter",
    "EventgridEventSubscriptionAdvancedFilterBoolEquals",
    "EventgridEventSubscriptionAdvancedFilterBoolEqualsList",
    "EventgridEventSubscriptionAdvancedFilterBoolEqualsOutputReference",
    "EventgridEventSubscriptionAdvancedFilterIsNotNull",
    "EventgridEventSubscriptionAdvancedFilterIsNotNullList",
    "EventgridEventSubscriptionAdvancedFilterIsNotNullOutputReference",
    "EventgridEventSubscriptionAdvancedFilterIsNullOrUndefined",
    "EventgridEventSubscriptionAdvancedFilterIsNullOrUndefinedList",
    "EventgridEventSubscriptionAdvancedFilterIsNullOrUndefinedOutputReference",
    "EventgridEventSubscriptionAdvancedFilterNumberGreaterThan",
    "EventgridEventSubscriptionAdvancedFilterNumberGreaterThanList",
    "EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals",
    "EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEqualsList",
    "EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEqualsOutputReference",
    "EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOutputReference",
    "EventgridEventSubscriptionAdvancedFilterNumberIn",
    "EventgridEventSubscriptionAdvancedFilterNumberInList",
    "EventgridEventSubscriptionAdvancedFilterNumberInOutputReference",
    "EventgridEventSubscriptionAdvancedFilterNumberInRange",
    "EventgridEventSubscriptionAdvancedFilterNumberInRangeList",
    "EventgridEventSubscriptionAdvancedFilterNumberInRangeOutputReference",
    "EventgridEventSubscriptionAdvancedFilterNumberLessThan",
    "EventgridEventSubscriptionAdvancedFilterNumberLessThanList",
    "EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEquals",
    "EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEqualsList",
    "EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEqualsOutputReference",
    "EventgridEventSubscriptionAdvancedFilterNumberLessThanOutputReference",
    "EventgridEventSubscriptionAdvancedFilterNumberNotIn",
    "EventgridEventSubscriptionAdvancedFilterNumberNotInList",
    "EventgridEventSubscriptionAdvancedFilterNumberNotInOutputReference",
    "EventgridEventSubscriptionAdvancedFilterNumberNotInRange",
    "EventgridEventSubscriptionAdvancedFilterNumberNotInRangeList",
    "EventgridEventSubscriptionAdvancedFilterNumberNotInRangeOutputReference",
    "EventgridEventSubscriptionAdvancedFilterOutputReference",
    "EventgridEventSubscriptionAdvancedFilterStringBeginsWith",
    "EventgridEventSubscriptionAdvancedFilterStringBeginsWithList",
    "EventgridEventSubscriptionAdvancedFilterStringBeginsWithOutputReference",
    "EventgridEventSubscriptionAdvancedFilterStringContains",
    "EventgridEventSubscriptionAdvancedFilterStringContainsList",
    "EventgridEventSubscriptionAdvancedFilterStringContainsOutputReference",
    "EventgridEventSubscriptionAdvancedFilterStringEndsWith",
    "EventgridEventSubscriptionAdvancedFilterStringEndsWithList",
    "EventgridEventSubscriptionAdvancedFilterStringEndsWithOutputReference",
    "EventgridEventSubscriptionAdvancedFilterStringIn",
    "EventgridEventSubscriptionAdvancedFilterStringInList",
    "EventgridEventSubscriptionAdvancedFilterStringInOutputReference",
    "EventgridEventSubscriptionAdvancedFilterStringNotBeginsWith",
    "EventgridEventSubscriptionAdvancedFilterStringNotBeginsWithList",
    "EventgridEventSubscriptionAdvancedFilterStringNotBeginsWithOutputReference",
    "EventgridEventSubscriptionAdvancedFilterStringNotContains",
    "EventgridEventSubscriptionAdvancedFilterStringNotContainsList",
    "EventgridEventSubscriptionAdvancedFilterStringNotContainsOutputReference",
    "EventgridEventSubscriptionAdvancedFilterStringNotEndsWith",
    "EventgridEventSubscriptionAdvancedFilterStringNotEndsWithList",
    "EventgridEventSubscriptionAdvancedFilterStringNotEndsWithOutputReference",
    "EventgridEventSubscriptionAdvancedFilterStringNotIn",
    "EventgridEventSubscriptionAdvancedFilterStringNotInList",
    "EventgridEventSubscriptionAdvancedFilterStringNotInOutputReference",
    "EventgridEventSubscriptionAzureFunctionEndpoint",
    "EventgridEventSubscriptionAzureFunctionEndpointOutputReference",
    "EventgridEventSubscriptionConfig",
    "EventgridEventSubscriptionDeadLetterIdentity",
    "EventgridEventSubscriptionDeadLetterIdentityOutputReference",
    "EventgridEventSubscriptionDeliveryIdentity",
    "EventgridEventSubscriptionDeliveryIdentityOutputReference",
    "EventgridEventSubscriptionDeliveryProperty",
    "EventgridEventSubscriptionDeliveryPropertyList",
    "EventgridEventSubscriptionDeliveryPropertyOutputReference",
    "EventgridEventSubscriptionRetryPolicy",
    "EventgridEventSubscriptionRetryPolicyOutputReference",
    "EventgridEventSubscriptionStorageBlobDeadLetterDestination",
    "EventgridEventSubscriptionStorageBlobDeadLetterDestinationOutputReference",
    "EventgridEventSubscriptionStorageQueueEndpoint",
    "EventgridEventSubscriptionStorageQueueEndpointOutputReference",
    "EventgridEventSubscriptionSubjectFilter",
    "EventgridEventSubscriptionSubjectFilterOutputReference",
    "EventgridEventSubscriptionTimeouts",
    "EventgridEventSubscriptionTimeoutsOutputReference",
    "EventgridEventSubscriptionWebhookEndpoint",
    "EventgridEventSubscriptionWebhookEndpointOutputReference",
]

publication.publish()

def _typecheckingstub__e7aed6640d0aa77216d19be72bc922c6e99455d6c594c47dd2d5af9bd5b5c77c(
    scope_: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    scope: builtins.str,
    advanced_filter: typing.Optional[typing.Union[EventgridEventSubscriptionAdvancedFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    advanced_filtering_on_arrays_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    azure_function_endpoint: typing.Optional[typing.Union[EventgridEventSubscriptionAzureFunctionEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
    dead_letter_identity: typing.Optional[typing.Union[EventgridEventSubscriptionDeadLetterIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    delivery_identity: typing.Optional[typing.Union[EventgridEventSubscriptionDeliveryIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    delivery_property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionDeliveryProperty, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_delivery_schema: typing.Optional[builtins.str] = None,
    eventhub_endpoint_id: typing.Optional[builtins.str] = None,
    expiration_time_utc: typing.Optional[builtins.str] = None,
    hybrid_connection_endpoint_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    included_event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    retry_policy: typing.Optional[typing.Union[EventgridEventSubscriptionRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    service_bus_queue_endpoint_id: typing.Optional[builtins.str] = None,
    service_bus_topic_endpoint_id: typing.Optional[builtins.str] = None,
    storage_blob_dead_letter_destination: typing.Optional[typing.Union[EventgridEventSubscriptionStorageBlobDeadLetterDestination, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_queue_endpoint: typing.Optional[typing.Union[EventgridEventSubscriptionStorageQueueEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
    subject_filter: typing.Optional[typing.Union[EventgridEventSubscriptionSubjectFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[EventgridEventSubscriptionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    webhook_endpoint: typing.Optional[typing.Union[EventgridEventSubscriptionWebhookEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__892caa621263ef81dec47a820d168016fc37c43775d3465e41cd05925115e323(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da9f12332b443ff91d281be5faa3a961c8ccb73d7b3c9ce65a7910be539bd262(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionDeliveryProperty, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3cc70103e6bb2c61ccbd0bf78629859dfe9534f069f81d80e73f34fb37cd03b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__431ef82fd2bccb53874c7f8e980337ac1689ce5ec78d38fc3844c3a4f204f33d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd314db06ff2bf61371d53713d343cf433c5702cd2af41b70f46c9b9891e753(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__648a13ec239b044661a70293b6c164ad05ed58744446d52ad89fc43d58eaab5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92de951aea097129bee12569c50304e536675866ed81ac0b5333d7fee59da021(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e61184ff44da30d6958a4b1ca1840cff5b36a41f9a0da222e06a48748a05699(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4eebd904f59fc158eb2ad4a9630186a5f9dae52ce7068cf6391400f80b54975(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a13ecfb456b1fbb4adb9ff2b802826710afc09fc367fe3bebc1ef0596d18145(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b887d074fd6fa8658a829037c3794e416744b519c04ab0f1a443f73551546fd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c23699006615417d9e3ac070e053e94c85455d2d95902a63a9510ebe08f8d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26971cdad9581d6d31f17f73bd597fe94b19b90ae131c8fb11a576edb2e6c619(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db56240d8b1f781353dcfdabd2fdc14233fad248bea93103b23998b7515c656a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__431d69c0e88b9b96ce58d7ea91825d68900446d993489b02c0198d2cf02f6df7(
    *,
    bool_equals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterBoolEquals, typing.Dict[builtins.str, typing.Any]]]]] = None,
    is_not_null: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterIsNotNull, typing.Dict[builtins.str, typing.Any]]]]] = None,
    is_null_or_undefined: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterIsNullOrUndefined, typing.Dict[builtins.str, typing.Any]]]]] = None,
    number_greater_than: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberGreaterThan, typing.Dict[builtins.str, typing.Any]]]]] = None,
    number_greater_than_or_equals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals, typing.Dict[builtins.str, typing.Any]]]]] = None,
    number_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberIn, typing.Dict[builtins.str, typing.Any]]]]] = None,
    number_in_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberInRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
    number_less_than: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberLessThan, typing.Dict[builtins.str, typing.Any]]]]] = None,
    number_less_than_or_equals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEquals, typing.Dict[builtins.str, typing.Any]]]]] = None,
    number_not_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberNotIn, typing.Dict[builtins.str, typing.Any]]]]] = None,
    number_not_in_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberNotInRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
    string_begins_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterStringBeginsWith, typing.Dict[builtins.str, typing.Any]]]]] = None,
    string_contains: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterStringContains, typing.Dict[builtins.str, typing.Any]]]]] = None,
    string_ends_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterStringEndsWith, typing.Dict[builtins.str, typing.Any]]]]] = None,
    string_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterStringIn, typing.Dict[builtins.str, typing.Any]]]]] = None,
    string_not_begins_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterStringNotBeginsWith, typing.Dict[builtins.str, typing.Any]]]]] = None,
    string_not_contains: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterStringNotContains, typing.Dict[builtins.str, typing.Any]]]]] = None,
    string_not_ends_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterStringNotEndsWith, typing.Dict[builtins.str, typing.Any]]]]] = None,
    string_not_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterStringNotIn, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4da15a7e262e2999c8690a7f023dfc0d46755554473d7c2b64532a0ab9751050(
    *,
    key: builtins.str,
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a94bb0d7a9a4e64778f27a46fa8392b5325b9153e85775a5b0d355cc936b2b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3050ba53beef469d52edf446a2ce70d377099457763f903e45b0a3aac18de8fd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe481f6e9e6e28fd13ec8305e2781e8ddc8d99fd58324b8717a26359bd3e7cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a3097f7b06ea05314db991a084089845353496db62c816c9bc79649a505008d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d4c3531e1c86c8efacd1bbc0fbc7775eebea6be703b3bd67478b6d83fe538e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec82eb31dd0d5897b78beecf69ee1b63c705a5187ad29e8bfd1f3bd47061000(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterBoolEquals]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa55018b0505f2feb6c72147c3e320f48932ce47e04b080b8990c66cca2ee62d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020e4e1525e4e3586151ceb8c7cd835a83c0535c2913838a70e3e4dbe73c85aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__818ab963ff99c875b425f3fceceb46a212c75bcff360f24285ae4a3619dc1a80(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b2d506f8d8567951431aee3d6e23e77f348666ea6864adf19d5903c82c6b40b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterBoolEquals]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cfcfc23a0f30dc0ce4390ad6a2073881ef50a66c7958c38ab7a0af6f36489ca(
    *,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2d502fbd47e13eacad6e9c675731b6bf4891641031c767a4677444209d1be5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b538c9c80b5c40a66edea1c53437b3ef41190b553173d8dc8fc987979c2d8ce(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd74bd226392add353779b7696d3485368dd7280afac6d3f02001a40e17aeedb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__939269d23c447f798275f175318c6b49cc6579e44c3eb2053ec2a5613eccae6c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e70695e1e40d50ba8d293bd8465a4379a907459134cbd28011bcbf0c6e534326(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e503a74b9447e0e8ca68df3b610fef673fa80c5ce293852f3ecbe64da86d25a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterIsNotNull]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__721447961dc9ae88796361291b3b331f9dc6f3c9dd4cc4750ea2b72703f36c84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__657d69d6d67806e50e0186619c00f190253bfac9ae7bf407a88f34fc6777f818(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ae144b8fb0ff69936057842357e7f1cabf743b76a6e9bca2b64d4dec67651a7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterIsNotNull]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7df5eedbc6d32686c152f577ac9637bb2bb373942e68d9f4253af61c5c48f27e(
    *,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dc25756cb704c74256b9aeb1e776dfefde7c9559429315a986e826365bbd40b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ec83a78eec1763292d0edce171438320dba912406e9fd8a336cc1bec0c381d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60cc3fd4540a8adbeabf326796374579dde2960f362fdd0ab89accee0996b254(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a656c96c3db5c8603c9e2835c94e751964f503d1f1dc99a27de017f36f8f587(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a5ccc3a947408b5e5c8071319e6285199e2f700f836837b3cd03a1d0e71ef22(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69753bd8c8780c7ab5645c077bd60bcd4dcb4c28810648d6f8fe5a5a83590db0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterIsNullOrUndefined]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ee5759994cd793ec719ca0529d209da320fbf95f8989afaac70ce3e94c90db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b2bcb526f2b9d5c09d3d5dd7c93f10a7415d800ef4a9ca820f95e186c14ff2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60829e3c5f6f1e8392030de704a1941e2cb99515edc256d86f1e352c095a32a9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterIsNullOrUndefined]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dbedeec84e94c2ae5f670611c7619abcaa6530e94c45d013a29755f8ffc3a5f(
    *,
    key: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02410fd26fa091bb5206894d83c067b165cf41af6aa6d0955b20881670a36fce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed930506e8c1f065394bded6c724f46b16b12e9815f1d49b74ae61d56346752a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae95ac98d740520da622c65d91072fb37ea666ae1ba38176aa32f5ded597125(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e494aea5dac9d785c5a8c75890ef9fca5cdc1cda96531f6f426bfe9d6209c6a5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__affce53707611a450e7360a8ed7d50527ca13c29295c1aec364eb40615391e24(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bd4ac3ade13fc8848cc44f3dcd995b7bde37346060bf73f7158d8af5156661b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberGreaterThan]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eecab5b4cda48763258fed19b01c26d6d8bd844c86f34173fdcdd861b004717b(
    *,
    key: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca37400fb1c8f257c51d78c010217e6afd6c89ff3dd43ca5f83aeb954d410bc5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4711e8b0d199206e42e0b9463ad6c8ee4ad54f2bdf35d0af94c335b4cf583146(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f4fc6599416baa4819d9f9c2cdc285b2e066fcc22dd7ce68c1e8d1e3ce0357a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02b84f813efc1146f04fcb91488f7f07e3af70086cf76f4f3a212dd6767445d8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7709f9ae2b6e7c23c3015e6726d7df74f2d2043ff109ed9a756a23ec52174a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74d25171256cddec4ef2d64aeb5a7561976b83918422abafd2671bb5292c0efe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__460d6a8418b629beb082adfd08e80b33f3d4a99f9ba902525d35a952ae7e26b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf1112704e7e4577ca90d0a63b72e3a7c3f94210a8a98bf3e4f8652796ddd738(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23c02c985bdbda4af702fb63cd7c381fd5175a722d0462b680bb28e68f3d24dd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6341a1a9ba2c19abb4fa8b0af75e438e82fe50525cd44d10c9d14c928b625577(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7f4e7a9ab162a64da0611685db5531dd3fdbb7eb87850e54a70be29775eb43b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755e8334d918ceb8d74b0e162dadce511193ceaf31b9e0ef5e1ef339f31c8272(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c39ea30d6d57c53205382f0200c8ec63f23436dfdcd7b61a8b353c4adc6b569(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__256f30e49dfcec3a26b74f0122d3c8e3f277ba105495d9c2eb6e90ad282bbfae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberGreaterThan]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcbba0678a72ee969c091bfcc9bc3b6978d17efe168243d0df5d6f7c95bb55fd(
    *,
    key: builtins.str,
    values: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80626e9997021a596c8cb368b3a505b6b0cdcc277b5fcf1642f1837e910f9b4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f20a1cc675eb2d3cd08ee33aae103b5fff349a60b6b60ccdc8caca4d5290914(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cde5c5d07f93b8d9f4950937c88b8d4576562a33eae96fefd8d2ca2794ea7daa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d7ea3e4ca9d1b8642208dfa79fedb9820bf9b5ba1565d6d5d2f9f3d6120acf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2e0a4cd705242a9ed95214d36eb86463a5d9febb950b0dffdb1aaf27ce2120b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19a7bf266070e68da8d85f941c8dc769c6a5ee1faf394892256a671359f4bde(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberIn]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__708c8cec42f959985f8004ef77df718a84e9d09e9b7c6182aef91abd89b06181(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4c7a9946f1ca67fc4335d1be9ba96860ee059a389ca94b963e1cdc2ee6c115f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff333271d7b5f070d6367c6765fa3f7c2e65c5632e011a7bf3e656c7dce924bd(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d154481a393880eed50a14b4dae023472678a3995ae7bfe702cf8a8b4566066(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberIn]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2479ae8910d3a85fcb2166c2489f1fecbd5f1e5456bab22c6bc68c78b03cdf15(
    *,
    key: builtins.str,
    values: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Sequence[jsii.Number]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a0b903e2712dd0ed90664a67a549782cc6690df96ef96140768338e0940d431(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6911f5df52ec3ba30a70336b459f0e2b91b218a20eafe9a412fcbf20b0b6de34(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb096a98352e653265bfbf43065756b35e3458f16b416e3758b489e1646fe1c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed856539508c27f3f4d895668fd56833fdff0fc3f84b4bfc77bfe6e58f40aac(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb03beba4480ed126c2d0424bba74a7d869a7910c0bf4edf5f70df07d2991b1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae497095794dfb6e35554601dd1b45c2695c6a29e7523d35a6113ff2cb7adfff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberInRange]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__638e1312219d674fbcb8ea0ef28da6f96ae33e25f61c862fdcf2cc7748d3d249(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb2685224ff83cd6d1fef200e0dc3fb35cd96a5c170973c948113559ef6215a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b4fe4bbf8e30e614b0e0c0e2136270d79ef0c9a4f2db358d9f6857a378ef3c2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[jsii.Number]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d2da1eb3c7d0b3d64ac22931b22051313466dd0ca0060f0d01308e6a2629a3a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberInRange]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__503ab840f7fa1312f3fd7f6cc1ae72a3659a7addc51af1e536a8410cae1a5968(
    *,
    key: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ae6568602cc8f9489bc4328f78cfeb2745895423f68ed21b05c102746284b96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf31c7f246aae45c8647409b2474258a93099255686829363c4f4002b44bdffb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e28555af6e4cfd63a0651a809d74670a49edd9d1c2491a6aab8921b554c752(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a29869e4f772d9748de4fa5fa0012de435489039362dacf4504506ed8b55a37e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__603d79f40537bfa819e7f1c55931302d067d1285c0dd1bad97c191a4f27584b2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ce3eac4cb255a966c950e5bdc656176f1c12edae8f069738dcb6a2aacea86d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberLessThan]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56f1b915f1c2728e42f1a88ed27cad83cf35617a0821ff35f145dd4563dd6387(
    *,
    key: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c7c12541dcce4702d1bba4c1e73156c7380997027a9d34f29572bae8dc4ff8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e45706b4f0d99617f7cc4a332a8136ff979123015e08b14bbd8387b8062bfbc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c7e873e70cca82936e1b524d317cae1b403ca4bcbd94f2c085193c2812be99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f700475d0726b7f312fd4b93f912b8aad9fec17dda066b333daa0f61818bd4b9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c60f7b124d579a1f4b1fcd5d616765870414df19fd2d526c7ccc715bbfbd9a2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e8a05d81a321a8cc472317fd582a9b62ea21b210f12f69a196ccee688d7b5d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEquals]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc26a548a7f5a1009ceda3338acbcf7c21e0cdbf37b6a35aea4b587a2e5a6746(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3416ffcdd74cb334067de3c36e071281017f9e75491e4697c33a3506bd7800d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0d579aa2492ccf761ef685ae051b37d4372c2ee1cddb90f02c8679a14beb1f1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72a9b2463e8340bccfc855ca074a28e94738a695216c119e46c18caafe4e1c41(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEquals]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0034db4f8d9c10e851855d5915135264bf89ca64678e85055affa9c383b1f38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd228d2032a9835a2cccc70c86027a37ed9c419f8cf0e95fa59a44831c26adb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe3d244af40d72630277e46a4666f7b598cf2c4bf8e9ca56a2e89eb5192e631(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61efad9f72e13509f1f7c9c522146ff261b7dce82417eb5bf3784a0aa4fb7f15(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberLessThan]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a9f4507616ee158fc5f165be03a8705493c01ba8e869141ff597fbb33b42d4(
    *,
    key: builtins.str,
    values: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c541c4ca6de79dd7767117405ae4d111431c92c58a95658813f72d1ac6eb523(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f825dc3d213917cf7e26801546e83acc773693649820fcd8c1e8dbc09e8d98a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b78adffd3c56a0f29ffbda905513183ceff1ddfa367addc511843326a99d49db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97fdb81151181505ca6e3f4e0f798ef6f2812c80b5fd9d9fbd6829ad8e10c3e3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c388c48a441fde7e8a1b4bc587b25a2e6da0b4b58e88458376854ea3fee6ec(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0cf6651b59c1676441f11372efc2815c0620d2e832a2d8e378cec0fdf90149d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberNotIn]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc6768109068dd69f6b76c8df1c0bdbcab9f332a563c3dece2931253a3f5f6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d270a7983f97c9f0d5843b58b7499675108a75917030b48b6e31fac8037d0681(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1fb6cc8913bb64cdebf201e64e56f8af0fc819d5102130f8b719eefaea19238(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e851271668f55c1bcd7d134c3e02490dfa82375492a20d9f07d4f7b4d4c84bd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberNotIn]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c89a75ec5efed0b0910ebdc576e91836dfcaa7827eb8f74d2d55deaf16e15c6e(
    *,
    key: builtins.str,
    values: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Sequence[jsii.Number]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e1a71a66da79b9bb1c8139489ed899e28c7b899cc764f48bcae0215cf037a6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b78b0d8541ac2c9ad6f6e2aa9095854a691d8992ba0a8e8c7770bcfa76edaaa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7c4d6d3d332c4a156c1581395be9890f5f2c26c8f9a39e2848c3a053158b03d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8051c4fbec150605ae0483ba09ef85fcabd8099fb13de7abc389d1beac6704f1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11841900d04f285a58d5335d7263ce1f55226accab9adbdd26d8701b81cb8212(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5858470658e67873e1af05e7905b8754a0d6519e9fcc501c62d76c831c68a8da(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterNumberNotInRange]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9135bafa13e3d1f9688a674f9e1e9979cd2dd4e7610b7257f97053f4fbb61f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee317d9bac135acd8f3100485b3db2e25c91166daebba31ca3ea1bf543372fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ba7a414b7f8878b07bcb63b8f6b4ad8ef3976b7d0215be625bf5e6a42c70ff(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[jsii.Number]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6781d1d80f7e5384a44b3739b2b6ac313e835514a8965ee0b8aa1e880a7fd1d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterNumberNotInRange]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e97ed9238cc5f13bef466bf54dd6e66e52c191dbd76da759badfb25599ca8607(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adcb93413d337a98ef584f09a8e2ec9a377e4fc9982a083ef932b3cfb8960bb9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterBoolEquals, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b10ce5a0e206cd8af09b636b2b7aa8e57b482c7e6ad463c8f9ae67ad6508bf2a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterIsNotNull, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__188794b1520fcf9dc07f11b87e41423c7fd856d198c23962641a71c100049c88(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterIsNullOrUndefined, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dd1a487c61cff41cbc1115631a9fed3ea042aae9a1580b569610dab237d599b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberGreaterThan, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab3baa1c3ed42ec48833ee00441e79e4829df7308f1721fc3b51f42593890b16(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__339f68e9b4b97af4b1402d2c7f248eae09dfe60ece2ceaed1e21a32defdf0337(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberIn, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90a3dfb8768e70dc8bf92ba9bc028e9cb477dc03330ee2de0b6483466e42d49d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberInRange, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d6b85448aec6054403fc2123735e54317a782ffe92d29367381ee07973c5ef(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberLessThan, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c725a1b112e6b8500d3e3aae0288445970fb0588a7f9a4ede931610cfe76964(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberLessThanOrEquals, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f9192b7000c777d204750fc17bc87b046caffd22d581c96b5f219137284f97(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberNotIn, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19d18f928266d4360e0fb767979dbb7c662322763f31c26a0bdbf3bc8217355(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterNumberNotInRange, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc1bd3069fb9a96efcf4ebc6e786b43983699bd07f1bbb3edfc9ac98eafb99ff(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterStringBeginsWith, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6966edf88d8156533de14a8bfed9b136e32460a88a48476b8999aeeecc1625c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterStringContains, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c6911b9e142f63dd4d9426e2f4fe75102f87147ddbc2b0589960ec25199f81d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterStringEndsWith, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc9c49df403953b181c9fad714d4aa22848ca9b802ccdf96dfc33711f8023b62(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterStringIn, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62055bfced2c9312412e2e70679077b3ff09a3f06fe9bd76932f2166cccc9486(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterStringNotBeginsWith, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__824e2a348d9b46c43569a26a1f8229983e492c6afb3c10d60e9fbacdbe85bcc8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterStringNotContains, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63bd9d1002f1d5c54bee7c472f1079e772e5184713caa2f878b555c19ee47b75(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterStringNotEndsWith, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d9cded5ab33d6656033fa92643b3b3528b36179ca787d2c8a5b6c98569fc802(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionAdvancedFilterStringNotIn, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fda554c47e1d28edf0d5ceb9bccbcfaa7a5a63f2b02c1dacdd9a1b397347c44a(
    value: typing.Optional[EventgridEventSubscriptionAdvancedFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc1ad89ffd19d0d35a80ffdef45ef6461de00573d0dc54deac2cd50fcbb85c0(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81af93f7e9cba205a95562d9031c893b526c35035d006b2082b1fa4e4d588dd8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__915ebe4022824f70d52e9e83788e8556e74dde2fe03c93df53c0b54f40c4a8a5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211f97251551af56f0b262708e3d163795a3b9eb642c01cf0786cc9f36f07c29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b753484410562966b003fb0f99fd192cc6e058141b9b76cf8a14baff37999c25(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825b58c264290f6e842479a8ba71e4e6558c6bfa3479d929ff38470bd0b365f7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__943a9c28ccbfe624aa4137c94ea0a3bb39a20d3a3a8cc5ad5fb53a78e39d0446(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringBeginsWith]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__372a90d8e1e74a95d7a56b65dfa04febbe6134bbb93f0f47733a696979e980b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__425c74cfdb9d6b22b22d88bd2b4bf3f3e6ea46cd83777d8e627fa1a2334dbd80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da319c39f19d717e6e0ae051f860766f600583d4ca3fb18fef6ff6ed9061d3da(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363ff8a5891b94b1051b74ec0e5c3e23149bdec0e10312648b3cff4c64c61c44(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringBeginsWith]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2af2264eee13610c78d7608226bf1568d9cae3920c780b0d9fc1acebc86fc09(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9423b6c1b6753984e441e703a01108e9bbdead687ac3915759ad94b357b83c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9786299a030126a5ec1b38ca382ffa393d414ce0fc92726ed290f67ed9e6fbf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ab29f9cf001c643d4be8948d10ddbfb475830e190bcac4a2422ec3d43d08c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fee457c2cb978519360fca2d597cf492145fdce10d1a1d87cba6a2efb44cd976(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a331cea75ee43e1b04050c3a45ef4755c9590909b90452689d95221f8ee262(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__935a6abfc4800fc124d5f18efec512b5f7be81c751c9f09be664dede806b8e50(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringContains]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d71f867ca12c9fa3f75cfbab78081acd1c20b567dc1e29d8101def3ce0f028(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f7a191387d5ebea1eaa3b285efe7da9564d3ba9e0349ad7a5e5ef851ebccc5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4ab44e088328e9920ff35def45c6a10ead10b0a947926f3e855b8f503757ac5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fffb0d24ab9ae0cbdb522440b513e997ad72b87ca1b6a095513509328f8ed52d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringContains]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb63af44fd36df30980fbf32d143dac0181c5c2bf14ae697fbb9ab20da1118c1(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc562b5be17d2362eb998d51793a97ed8585efc32ba86a0a050e0571eda89767(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3409adc5f6d99e0d066a1b118930a3184038d5ebc7ac8451e426c53ae285be67(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2f9d1e3a7cd2a6d29f0f7c1fa051d0d3a15afb628dd51bb8d7000c97b1f2a39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__127446ce9c99c28a8caa140da3155a2c78e2bd8487073627b972548a0c96d425(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5afb406746be096ea3ce5685e559faed4dfda6d8340c5f7b7a4fc2fe4e1fdb68(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e19561d446d2deeade477502c4a1b66e308178c366ec24476f3594fecc310fbd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringEndsWith]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd292665ec87edf21f53a1a3d4e9f12c806120f0c1c50798d48123b236f3e45d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c3fc751039d17a3b00d5041ceda4cbaa54cb71e75b79d3faa35db43593e2760(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23f9afa165300e479e0f783e77ad6664d3e9e71c533e83b6c4d3eef18d3e6f54(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15af2f407f0527718a04f8c9bfac33f5de59f5f5d8eb842a7a3b257f4f2e5a3c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringEndsWith]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3279aa899b4924fadb4ccebff04acae2f318a1ea9f5e5081be2c2f40049f25d7(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c88c8a88f392ad82db5c26e39c3ae3d7366191bdb94eb4a7f39c9f8c799328f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee1b8a714ca1154bd00a88ad0989faf53c9b2733b9501f4d2ed596a988735c11(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e16f57ca063429afb1e789d9648dd92f97765643bee8257b4bcb1e09a2fedc9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e90de75e53d586c6f69ff8eb0213f7bf20e4d6739e2f56b165ba7fb765b591(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33d916ab57fc80cc61c5ba533b7f53087b4ba4747ff987bcb2eb77ee1bb40b5d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39dc703c7fa740491e6148c743b50ea52de167b2a96e8e4ca078bca80176ae4c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringIn]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48db09010ff34d3c1d1b1fd0b3bbf2193f8ac76da52926a94c7323fe0e5455b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c16077163021bd53e0ca1fff74a5c0f80bb098fdcfad767294fe8060b48ecc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e3a266c2589078409f50d9d184484e7be39bbc641bedd94f859f1ca4eae5877(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__342f9ab45635fcd65640a56da5c04e86bb60db72f522f048d4b6ef7e6adeb6af(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringIn]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c284089bbadade25f45881d13e6438ed57e02f52c485a61922ff0b881e9ea3d9(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b27b24bc209c2ae5e63cdcf3cf955ffed02cee98ea7b4ac2852b7ab93254e5d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8e8c64c86031b72aa5691ee3bbe76f66084e4b4f07fcafa2197f561aede4f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32ef3ace72d259cde5fad98261e103c254e5e72f5a689d796f27b85ee4c459a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__237e180c45e2b5c17f5e77695c4086c68c130c74581b4f1c78bc457698eebb87(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df277f07bf9f39912ead031f1036fab40271753475f6301a098bfefa16cf843f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2c3feb700b1e07daa8dfc95c3ab19effe0e0f5dac86b02cb984d3736d587f24(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringNotBeginsWith]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10ed8216926375d163bdfe1a2174eceb4f5305c74d296d5f8979ca7e552120f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9f9d5f5286395d5b245a0c189c047937e395de0d190e1e9213e58d50d226b62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08825c489c0944488b46b1eb3f5cd55345e47a127c2c7c607ae32556b81fca48(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c36658ec8ab42158bd9736faa6d01db8dab4c7e3b26e4568c12b4b5de61ed04a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringNotBeginsWith]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f5c73fa5312665085acb16d8e2d8d2fb827f3a00663ed2af4282b988d09670(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f8822e4f0d04127b2a9733bae423ad7ef304aeec1257ff9ff2d3cdf373743a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7de299bc2e47ffb9c9e896cc973650a5abb0c0d93a23ad16df9fe33503f3e4c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e474cea12dd55668cbb253935d5f5246f5fa340bdf26d4581f5f6100a806d65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb9786125d667b0073bfec785efb980413f8df3790cd87e4e591ad34d0c4a39(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f1821bfd6a23a6ab07317be8a719100487faba26fd4a5c5176bac74849a98b5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1429eaec94b8b2d13d569546ad74e698175a8f598cc51acfd89dd49f25aeb6a9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringNotContains]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0117e1ac141f5de7831607da67c1652ac40de09647110bbaa61e95fc1ddda797(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2fec4985ea270969ea19b6d0f9923afdf13a9d89b2c4dddbd7f327e1db07fb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba948ea02b516b57d67c76cbab20cb3e70c9ca3cecb9ac7623e12e0e30b5744(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c87abe195509a6fca567c0bff8d578658851d4f19c3b8e590248ef1ede8c6cf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringNotContains]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abfa5fed7cff01c08958f01aa95b0298342511bfb89ccc1410a030e75be1706e(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3195ce9f17b5ac70fa2ebbc951132fd5de1400bfa02a9164ad04b0bf330024be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec21ab271538f54627ee5251d125e20a6d272dd473f0369d80f3e2da3c947d1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cacb5a78a28e2648abe6ef76a0ec9056e2b397eb14c559ddeaa781f4066c1156(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4680acddc79da1ea948ab44b89eca9c34fef452b46d1f6e9cd0b480abd625d3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__274ba763b2890000583b6618c20d85b8546e9bdfeae3813aedf213ad11175685(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__332808cd1fcac732009496f2723891ca6ee8a47aa14ea7db6b2a7b2055ae2c13(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringNotEndsWith]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa85ada45e6286ec8a91e21188b7a88b83b426a765c211a7fa1246737b1ee7d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e684d7e26cb5ac1800662c0f4a8b6d0be8e2a144a29ebd02f30d07875662245(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c42a3b8794a63145a584cfb764844371e764abfef4633b35889f629c34f207e6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cb554901ed09544ea87995f6032ca334ef705ab132d6dc5bd5d9fa0a6ef2446(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringNotEndsWith]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad3b7d551d53f90f435d07161103df510dbe49e0640153f889e27a8a10982ac0(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d6d78ce4723c18008deddffd12f06a6989e94c4accb658c6c9c9cb66a1c812f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec4b293641012a2c7e7dab520f108a1a50fc7bdf2790f31e2837ee75d484fc8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52d67a9dd483b541a15b4efa6ac52eb4db1856d6126e051a827275ac29904835(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ace5e70a0df87a3f500dc9b2e703386b371bb3770830679cd27d0198c628152(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6807d2420c2b01ff114a783930eef90e467209737c3a446b7ecaa5db54dca611(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f36a373b81d6af707311e812cc41a80fdf66f7c7c303462daa9d821366bc5d50(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionAdvancedFilterStringNotIn]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29951b0b1fefe6a31c6c820182b23e93e11a23df55b83c00a5eb6ed75cc7177d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__179fdb57462b47c345874e7aaad02c2d872efc87919413d57099da1e7af3eb3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae80fcc3e05b40a3d78d6012f916d66a3367fce16f2bd3f07c8187faebcfe7a3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1786d14f0d167a6df0c04b02eccb97e4bdea14fbfcd8e3047fd162d8f5f7c645(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionAdvancedFilterStringNotIn]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6032229fda6725491236fd4a611f19439a951fd60b97ec81f94b6ac6f5b916db(
    *,
    function_id: builtins.str,
    max_events_per_batch: typing.Optional[jsii.Number] = None,
    preferred_batch_size_in_kilobytes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d643d5ba58126287dc0e83085ae436da65c7aaebf07bd32f4b592427803881e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f566d474116a67e4ff1db5963c630c0682c91e50fa28dd8724239f96b0beda9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6466d4afa9fbdea506c5c11832266e2c996441765c319059048139314b0c5a1b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80be9615d4160e7a65fe5d43c0403d9007a23c562277069efd7837ff9b20abf5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4868872486341e3fad3349fc940733d04997ca1d0d73a12f9495c14cdb4df8a(
    value: typing.Optional[EventgridEventSubscriptionAzureFunctionEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a47c10c5cbbe163c0703b533052397a56ed3281e450faee112782c72f549b5ee(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    scope: builtins.str,
    advanced_filter: typing.Optional[typing.Union[EventgridEventSubscriptionAdvancedFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    advanced_filtering_on_arrays_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    azure_function_endpoint: typing.Optional[typing.Union[EventgridEventSubscriptionAzureFunctionEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
    dead_letter_identity: typing.Optional[typing.Union[EventgridEventSubscriptionDeadLetterIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    delivery_identity: typing.Optional[typing.Union[EventgridEventSubscriptionDeliveryIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    delivery_property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridEventSubscriptionDeliveryProperty, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_delivery_schema: typing.Optional[builtins.str] = None,
    eventhub_endpoint_id: typing.Optional[builtins.str] = None,
    expiration_time_utc: typing.Optional[builtins.str] = None,
    hybrid_connection_endpoint_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    included_event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    retry_policy: typing.Optional[typing.Union[EventgridEventSubscriptionRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    service_bus_queue_endpoint_id: typing.Optional[builtins.str] = None,
    service_bus_topic_endpoint_id: typing.Optional[builtins.str] = None,
    storage_blob_dead_letter_destination: typing.Optional[typing.Union[EventgridEventSubscriptionStorageBlobDeadLetterDestination, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_queue_endpoint: typing.Optional[typing.Union[EventgridEventSubscriptionStorageQueueEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
    subject_filter: typing.Optional[typing.Union[EventgridEventSubscriptionSubjectFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[EventgridEventSubscriptionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    webhook_endpoint: typing.Optional[typing.Union[EventgridEventSubscriptionWebhookEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__505f88d1f8177b3af223a700ca2180de5534e263d75d74ed71ce44986e4607bc(
    *,
    type: builtins.str,
    user_assigned_identity: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b9ad7a88a1b4568397cc06ff0cd703e7dc5eb08bedf2d8c1a89cc86e960ef5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a5df8a9c6fa9f9a9c40f1bb259f8c53d916925dc1543225cfda14685d42274(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5fac2a9e45d475485f2b6c1406c8759bcadc35797941abfbf791a7f3d33ae0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e434b20e4631c2ed72fe0e23772dac7a4b3aa89e8430245ce9a8a29d2a0c41(
    value: typing.Optional[EventgridEventSubscriptionDeadLetterIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d2d00d51633b594e9a6f1b7bb3d63e4c39a6d0a51455f23dbffbacbf9385ee6(
    *,
    type: builtins.str,
    user_assigned_identity: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7538b2c3ca46b5b3f4bd84c273201bafe6dcc644f60f8497619b892a855eca8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e0c3836772afeb6856ff24ce6b2d42667777c42c9dc1ceffb2325db1ef2878(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__795c047d0e676696bc70a91b74749342331b4b77d7c2ef68e1aff62810365394(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fffaae8ba3642b29ca6a240bfa10d94cb954d4953caae9765c1cd885f1e7fc2b(
    value: typing.Optional[EventgridEventSubscriptionDeliveryIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0e5902fefa563a2d252ecc837656cd2db3af423c264bb5681e5e9e6607f305(
    *,
    header_name: builtins.str,
    type: builtins.str,
    secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source_field: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23d395f2e85c9b0e9a9ca72445a4b270623ae4cf0b5c9d9076e6505adb208d52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4637db758c1a54c963f962d4b355528d31a9040165f80e5b11ba43ef6fe46d97(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bf28c3c433b6851acc1cd1bf54cedb334405ba0d20f06ee5b4cae3f881d8c32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24450b57c4760e9ebbee54b006259a411be15b5c5bc8275fa2f11d7f97d61389(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a38c533270824ba06e115f2febc7223711fc627050be1c46b145d87e54ca56(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fecb6d5537d9b46397224bfb00dae7b3ed8bf724af8e5064bd9a32f40194cec5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridEventSubscriptionDeliveryProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef29c033faeab8486133d68f794c9d20e3f18e6abcaa264057111c26ba2a160(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b3d5f3e16e9c4b7bbdd6d65afb9300731484308f55a1f7f8d183d89be123cdc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f6bc75e34dea9d23291b67403848b229ecd002228f7cb3a1a6b655fcaae64f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2f69a815932128971d348c474867aad2fc980da8e60a7151c1cb1af2ddf2543(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b22266edb0f69bb177bdd45981f63a902fbf0ab7ab6b7e8918cf3dc58d1e3a4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c40c4a00160bc69f43d81c8c5df4740994400722987f91c2c6f06619a2a52ea3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d3778f1b2e4c68b4d02fa48cd55bacdbc2ed3e47c9c104d4c3b963c5420560(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionDeliveryProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17304d3161cd9dba3da93e0821b9ad18306e7e56ea35337d522a37510d34afe0(
    *,
    event_time_to_live: jsii.Number,
    max_delivery_attempts: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc181ee6b7bae300d380ecb9cf9908fcfcd5c94a543b454c2d92d38f8914583(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03faf4f793e4aaa2bd313b136e9332d2d091ba41a3261c8ca4656fa2de892642(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd529ac08146910cc73bfb18385348c7ab3f0377898efd42fc62b1e500ed5db1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d52e3e46e349c8067058884d50adbb6cb85a32025b4e01925380bd84a0ea986(
    value: typing.Optional[EventgridEventSubscriptionRetryPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16483da8ee1bafe800d108ab40023447af20e116475878b33486f0d151787512(
    *,
    storage_account_id: builtins.str,
    storage_blob_container_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d0bee0254d19166ee9ef249b56d0037159ac0770d535eb94f656ec7912ed4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a6528be3b8b23356e102ba0e669abcf779bdd0dbdae67fa2912eff250d4857d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa61eeb0f161a42a6d3d4d275826728fd9a97716e17d148157b4c6440f25a644(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30c5a4ebb4799863a66839ce474cab30a4b7866acdc4337e9eaa29fc2331f41(
    value: typing.Optional[EventgridEventSubscriptionStorageBlobDeadLetterDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08dfd9584acdfa5a71777f8cae4a67897b755d82b3a43f45ab8fbc827984fe4e(
    *,
    queue_name: builtins.str,
    storage_account_id: builtins.str,
    queue_message_time_to_live_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5790fcc18274f3ccf81d779d636696566f1950ef44308d49a69ab6226a36427(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54fb26ecfab33479dba94c72dc05f8cc775a4618b703abf6d3ecfe29991b02fd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b3f4a595ba8056c1e3cef1d75400d8dd40f6441c2f840349a473044169a3e18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc4a19680d7503fd2abe4948921e4fde9355704eb6b3b29034581125300d3b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe170e67648cc2de1d2614e32181b4ee9e42457c1095bcffc488325c20989393(
    value: typing.Optional[EventgridEventSubscriptionStorageQueueEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc2e10a280055d54d4aba9583bfe2f32057fe1f09e48f95afa51da8a36a9bf6b(
    *,
    case_sensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subject_begins_with: typing.Optional[builtins.str] = None,
    subject_ends_with: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f19847a004083c65ff1be9dd0745431a4c711c9c00cd19f3827f4a458358e04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8faa62454829ff7dfc939420647d0c040515ab9d716d574ffa0d79d1b2024257(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc46f83ee80555f0388074bd3e031703b1f0981fc5f699b4f67b2c9dd14266fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be2e095be12a66bfb7518dfb2487bedb65884533a143a325fdb15c55f21324e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__453d631be394f719b5e3b5e712dc048a190db308fae195dbf13cde35f0b7b4f0(
    value: typing.Optional[EventgridEventSubscriptionSubjectFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1885ea55e459bf192a4b8c1941ec4a175788ef949c3f83024427bd8fb37814aa(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__348ba6a9814af0ea9c279c3cc6a32e4d4ef4dd81f53208008c472d4a8795d200(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__418390961faab8ec0597e2655c94c124233bae1bec84adc70722dcea91b9aa66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__364ccf4babb7d84286b1afdca360fdafda187072a90a1b854c40a907776fd137(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a7e2004ac1b1cd5b8449711ddee58044656b6c8b6aa207ca89d9ad8516256e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a9b13cfc2c9aa6fc0595aba892c110be274aff6673a3c3801bae02eb058235(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7556aff4d7903a4c66fab770f28393086015b195a0861dd4324fb4c57c7e5f6b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridEventSubscriptionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65e2e3d6c1e4ecdc1d40c723957606e84454efb2505602704b448946e8f99f0b(
    *,
    url: builtins.str,
    active_directory_app_id_or_uri: typing.Optional[builtins.str] = None,
    active_directory_tenant_id: typing.Optional[builtins.str] = None,
    max_events_per_batch: typing.Optional[jsii.Number] = None,
    preferred_batch_size_in_kilobytes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__046e3ccfedba392de97e487357bdd15d1176d605ed0e48c1c5eab49b545bdf85(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cae53e620f033a0a4f6ba294a4508b94fb354b7d6c4f5fa8ea3fc646aa5fec3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10e2dc33c7e5593024ace05cb5121f7983b0e4e5fde59792cd6509144d9c1bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2814710f56e10728da3a130e3aa5560976f0c35b6123f4d5d9fabcbd284a9aa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0b98abc97c2b224232102e9af21d9ddaabc8912e2e038f4453587ba70a342a7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed5fd1fcbd0c55752984b4cc4c130652cb7ebdeb5eee40273eca747726d3d4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54e5ede82e3f4dfdaa0d8d5218dd95acaee8a25310032ed2dfc9f608ba11d2a(
    value: typing.Optional[EventgridEventSubscriptionWebhookEndpoint],
) -> None:
    """Type checking stubs"""
    pass
