r'''
# `azurerm_eventgrid_system_topic_event_subscription`

Refer to the Terraform Registry for docs: [`azurerm_eventgrid_system_topic_event_subscription`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription).
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


class EventgridSystemTopicEventSubscription(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscription",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription azurerm_eventgrid_system_topic_event_subscription}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        resource_group_name: builtins.str,
        system_topic: builtins.str,
        advanced_filter: typing.Optional[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        advanced_filtering_on_arrays_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        azure_function_endpoint: typing.Optional[typing.Union["EventgridSystemTopicEventSubscriptionAzureFunctionEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
        dead_letter_identity: typing.Optional[typing.Union["EventgridSystemTopicEventSubscriptionDeadLetterIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        delivery_identity: typing.Optional[typing.Union["EventgridSystemTopicEventSubscriptionDeliveryIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        delivery_property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionDeliveryProperty", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_delivery_schema: typing.Optional[builtins.str] = None,
        eventhub_endpoint_id: typing.Optional[builtins.str] = None,
        expiration_time_utc: typing.Optional[builtins.str] = None,
        hybrid_connection_endpoint_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        included_event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        retry_policy: typing.Optional[typing.Union["EventgridSystemTopicEventSubscriptionRetryPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        service_bus_queue_endpoint_id: typing.Optional[builtins.str] = None,
        service_bus_topic_endpoint_id: typing.Optional[builtins.str] = None,
        storage_blob_dead_letter_destination: typing.Optional[typing.Union["EventgridSystemTopicEventSubscriptionStorageBlobDeadLetterDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_queue_endpoint: typing.Optional[typing.Union["EventgridSystemTopicEventSubscriptionStorageQueueEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
        subject_filter: typing.Optional[typing.Union["EventgridSystemTopicEventSubscriptionSubjectFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["EventgridSystemTopicEventSubscriptionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        webhook_endpoint: typing.Optional[typing.Union["EventgridSystemTopicEventSubscriptionWebhookEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription azurerm_eventgrid_system_topic_event_subscription} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#name EventgridSystemTopicEventSubscription#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#resource_group_name EventgridSystemTopicEventSubscription#resource_group_name}.
        :param system_topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#system_topic EventgridSystemTopicEventSubscription#system_topic}.
        :param advanced_filter: advanced_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#advanced_filter EventgridSystemTopicEventSubscription#advanced_filter}
        :param advanced_filtering_on_arrays_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#advanced_filtering_on_arrays_enabled EventgridSystemTopicEventSubscription#advanced_filtering_on_arrays_enabled}.
        :param azure_function_endpoint: azure_function_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#azure_function_endpoint EventgridSystemTopicEventSubscription#azure_function_endpoint}
        :param dead_letter_identity: dead_letter_identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#dead_letter_identity EventgridSystemTopicEventSubscription#dead_letter_identity}
        :param delivery_identity: delivery_identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#delivery_identity EventgridSystemTopicEventSubscription#delivery_identity}
        :param delivery_property: delivery_property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#delivery_property EventgridSystemTopicEventSubscription#delivery_property}
        :param event_delivery_schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#event_delivery_schema EventgridSystemTopicEventSubscription#event_delivery_schema}.
        :param eventhub_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#eventhub_endpoint_id EventgridSystemTopicEventSubscription#eventhub_endpoint_id}.
        :param expiration_time_utc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#expiration_time_utc EventgridSystemTopicEventSubscription#expiration_time_utc}.
        :param hybrid_connection_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#hybrid_connection_endpoint_id EventgridSystemTopicEventSubscription#hybrid_connection_endpoint_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#id EventgridSystemTopicEventSubscription#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param included_event_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#included_event_types EventgridSystemTopicEventSubscription#included_event_types}.
        :param labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#labels EventgridSystemTopicEventSubscription#labels}.
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#retry_policy EventgridSystemTopicEventSubscription#retry_policy}
        :param service_bus_queue_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#service_bus_queue_endpoint_id EventgridSystemTopicEventSubscription#service_bus_queue_endpoint_id}.
        :param service_bus_topic_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#service_bus_topic_endpoint_id EventgridSystemTopicEventSubscription#service_bus_topic_endpoint_id}.
        :param storage_blob_dead_letter_destination: storage_blob_dead_letter_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#storage_blob_dead_letter_destination EventgridSystemTopicEventSubscription#storage_blob_dead_letter_destination}
        :param storage_queue_endpoint: storage_queue_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#storage_queue_endpoint EventgridSystemTopicEventSubscription#storage_queue_endpoint}
        :param subject_filter: subject_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#subject_filter EventgridSystemTopicEventSubscription#subject_filter}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#timeouts EventgridSystemTopicEventSubscription#timeouts}
        :param webhook_endpoint: webhook_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#webhook_endpoint EventgridSystemTopicEventSubscription#webhook_endpoint}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e6ffabd576d2ded52f9219fdef6e3ca88e08e3386546bcef81696eae047cc13)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EventgridSystemTopicEventSubscriptionConfig(
            name=name,
            resource_group_name=resource_group_name,
            system_topic=system_topic,
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

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a EventgridSystemTopicEventSubscription resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EventgridSystemTopicEventSubscription to import.
        :param import_from_id: The id of the existing EventgridSystemTopicEventSubscription that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EventgridSystemTopicEventSubscription to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c60643124b3510a8899a2fce8d27c03135ec136c2b893196c717e5bb13ea2ae)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdvancedFilter")
    def put_advanced_filter(
        self,
        *,
        bool_equals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEquals", typing.Dict[builtins.str, typing.Any]]]]] = None,
        is_not_null: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNull", typing.Dict[builtins.str, typing.Any]]]]] = None,
        is_null_or_undefined: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefined", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_greater_than: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThan", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_greater_than_or_equals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberIn", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_in_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_less_than: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThan", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_less_than_or_equals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEquals", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_not_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotIn", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_not_in_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_begins_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWith", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_contains: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringContains", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_ends_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWith", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringIn", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_not_begins_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWith", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_not_contains: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContains", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_not_ends_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWith", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_not_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotIn", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param bool_equals: bool_equals block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#bool_equals EventgridSystemTopicEventSubscription#bool_equals}
        :param is_not_null: is_not_null block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#is_not_null EventgridSystemTopicEventSubscription#is_not_null}
        :param is_null_or_undefined: is_null_or_undefined block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#is_null_or_undefined EventgridSystemTopicEventSubscription#is_null_or_undefined}
        :param number_greater_than: number_greater_than block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_greater_than EventgridSystemTopicEventSubscription#number_greater_than}
        :param number_greater_than_or_equals: number_greater_than_or_equals block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_greater_than_or_equals EventgridSystemTopicEventSubscription#number_greater_than_or_equals}
        :param number_in: number_in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_in EventgridSystemTopicEventSubscription#number_in}
        :param number_in_range: number_in_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_in_range EventgridSystemTopicEventSubscription#number_in_range}
        :param number_less_than: number_less_than block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_less_than EventgridSystemTopicEventSubscription#number_less_than}
        :param number_less_than_or_equals: number_less_than_or_equals block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_less_than_or_equals EventgridSystemTopicEventSubscription#number_less_than_or_equals}
        :param number_not_in: number_not_in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_not_in EventgridSystemTopicEventSubscription#number_not_in}
        :param number_not_in_range: number_not_in_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_not_in_range EventgridSystemTopicEventSubscription#number_not_in_range}
        :param string_begins_with: string_begins_with block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_begins_with EventgridSystemTopicEventSubscription#string_begins_with}
        :param string_contains: string_contains block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_contains EventgridSystemTopicEventSubscription#string_contains}
        :param string_ends_with: string_ends_with block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_ends_with EventgridSystemTopicEventSubscription#string_ends_with}
        :param string_in: string_in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_in EventgridSystemTopicEventSubscription#string_in}
        :param string_not_begins_with: string_not_begins_with block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_not_begins_with EventgridSystemTopicEventSubscription#string_not_begins_with}
        :param string_not_contains: string_not_contains block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_not_contains EventgridSystemTopicEventSubscription#string_not_contains}
        :param string_not_ends_with: string_not_ends_with block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_not_ends_with EventgridSystemTopicEventSubscription#string_not_ends_with}
        :param string_not_in: string_not_in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_not_in EventgridSystemTopicEventSubscription#string_not_in}
        '''
        value = EventgridSystemTopicEventSubscriptionAdvancedFilter(
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
        :param function_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#function_id EventgridSystemTopicEventSubscription#function_id}.
        :param max_events_per_batch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#max_events_per_batch EventgridSystemTopicEventSubscription#max_events_per_batch}.
        :param preferred_batch_size_in_kilobytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#preferred_batch_size_in_kilobytes EventgridSystemTopicEventSubscription#preferred_batch_size_in_kilobytes}.
        '''
        value = EventgridSystemTopicEventSubscriptionAzureFunctionEndpoint(
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
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#type EventgridSystemTopicEventSubscription#type}.
        :param user_assigned_identity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#user_assigned_identity EventgridSystemTopicEventSubscription#user_assigned_identity}.
        '''
        value = EventgridSystemTopicEventSubscriptionDeadLetterIdentity(
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
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#type EventgridSystemTopicEventSubscription#type}.
        :param user_assigned_identity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#user_assigned_identity EventgridSystemTopicEventSubscription#user_assigned_identity}.
        '''
        value = EventgridSystemTopicEventSubscriptionDeliveryIdentity(
            type=type, user_assigned_identity=user_assigned_identity
        )

        return typing.cast(None, jsii.invoke(self, "putDeliveryIdentity", [value]))

    @jsii.member(jsii_name="putDeliveryProperty")
    def put_delivery_property(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionDeliveryProperty", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0608e1a2c9de636a7c03ad6766166c4701f6051d32e808cd0a332b1d30062b3a)
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
        :param event_time_to_live: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#event_time_to_live EventgridSystemTopicEventSubscription#event_time_to_live}.
        :param max_delivery_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#max_delivery_attempts EventgridSystemTopicEventSubscription#max_delivery_attempts}.
        '''
        value = EventgridSystemTopicEventSubscriptionRetryPolicy(
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
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#storage_account_id EventgridSystemTopicEventSubscription#storage_account_id}.
        :param storage_blob_container_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#storage_blob_container_name EventgridSystemTopicEventSubscription#storage_blob_container_name}.
        '''
        value = EventgridSystemTopicEventSubscriptionStorageBlobDeadLetterDestination(
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
        :param queue_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#queue_name EventgridSystemTopicEventSubscription#queue_name}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#storage_account_id EventgridSystemTopicEventSubscription#storage_account_id}.
        :param queue_message_time_to_live_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#queue_message_time_to_live_in_seconds EventgridSystemTopicEventSubscription#queue_message_time_to_live_in_seconds}.
        '''
        value = EventgridSystemTopicEventSubscriptionStorageQueueEndpoint(
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
        :param case_sensitive: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#case_sensitive EventgridSystemTopicEventSubscription#case_sensitive}.
        :param subject_begins_with: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#subject_begins_with EventgridSystemTopicEventSubscription#subject_begins_with}.
        :param subject_ends_with: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#subject_ends_with EventgridSystemTopicEventSubscription#subject_ends_with}.
        '''
        value = EventgridSystemTopicEventSubscriptionSubjectFilter(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#create EventgridSystemTopicEventSubscription#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#delete EventgridSystemTopicEventSubscription#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#read EventgridSystemTopicEventSubscription#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#update EventgridSystemTopicEventSubscription#update}.
        '''
        value = EventgridSystemTopicEventSubscriptionTimeouts(
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
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#url EventgridSystemTopicEventSubscription#url}.
        :param active_directory_app_id_or_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#active_directory_app_id_or_uri EventgridSystemTopicEventSubscription#active_directory_app_id_or_uri}.
        :param active_directory_tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#active_directory_tenant_id EventgridSystemTopicEventSubscription#active_directory_tenant_id}.
        :param max_events_per_batch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#max_events_per_batch EventgridSystemTopicEventSubscription#max_events_per_batch}.
        :param preferred_batch_size_in_kilobytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#preferred_batch_size_in_kilobytes EventgridSystemTopicEventSubscription#preferred_batch_size_in_kilobytes}.
        '''
        value = EventgridSystemTopicEventSubscriptionWebhookEndpoint(
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
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterOutputReference":
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterOutputReference", jsii.get(self, "advancedFilter"))

    @builtins.property
    @jsii.member(jsii_name="azureFunctionEndpoint")
    def azure_function_endpoint(
        self,
    ) -> "EventgridSystemTopicEventSubscriptionAzureFunctionEndpointOutputReference":
        return typing.cast("EventgridSystemTopicEventSubscriptionAzureFunctionEndpointOutputReference", jsii.get(self, "azureFunctionEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="deadLetterIdentity")
    def dead_letter_identity(
        self,
    ) -> "EventgridSystemTopicEventSubscriptionDeadLetterIdentityOutputReference":
        return typing.cast("EventgridSystemTopicEventSubscriptionDeadLetterIdentityOutputReference", jsii.get(self, "deadLetterIdentity"))

    @builtins.property
    @jsii.member(jsii_name="deliveryIdentity")
    def delivery_identity(
        self,
    ) -> "EventgridSystemTopicEventSubscriptionDeliveryIdentityOutputReference":
        return typing.cast("EventgridSystemTopicEventSubscriptionDeliveryIdentityOutputReference", jsii.get(self, "deliveryIdentity"))

    @builtins.property
    @jsii.member(jsii_name="deliveryProperty")
    def delivery_property(
        self,
    ) -> "EventgridSystemTopicEventSubscriptionDeliveryPropertyList":
        return typing.cast("EventgridSystemTopicEventSubscriptionDeliveryPropertyList", jsii.get(self, "deliveryProperty"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicy")
    def retry_policy(
        self,
    ) -> "EventgridSystemTopicEventSubscriptionRetryPolicyOutputReference":
        return typing.cast("EventgridSystemTopicEventSubscriptionRetryPolicyOutputReference", jsii.get(self, "retryPolicy"))

    @builtins.property
    @jsii.member(jsii_name="storageBlobDeadLetterDestination")
    def storage_blob_dead_letter_destination(
        self,
    ) -> "EventgridSystemTopicEventSubscriptionStorageBlobDeadLetterDestinationOutputReference":
        return typing.cast("EventgridSystemTopicEventSubscriptionStorageBlobDeadLetterDestinationOutputReference", jsii.get(self, "storageBlobDeadLetterDestination"))

    @builtins.property
    @jsii.member(jsii_name="storageQueueEndpoint")
    def storage_queue_endpoint(
        self,
    ) -> "EventgridSystemTopicEventSubscriptionStorageQueueEndpointOutputReference":
        return typing.cast("EventgridSystemTopicEventSubscriptionStorageQueueEndpointOutputReference", jsii.get(self, "storageQueueEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="subjectFilter")
    def subject_filter(
        self,
    ) -> "EventgridSystemTopicEventSubscriptionSubjectFilterOutputReference":
        return typing.cast("EventgridSystemTopicEventSubscriptionSubjectFilterOutputReference", jsii.get(self, "subjectFilter"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "EventgridSystemTopicEventSubscriptionTimeoutsOutputReference":
        return typing.cast("EventgridSystemTopicEventSubscriptionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="webhookEndpoint")
    def webhook_endpoint(
        self,
    ) -> "EventgridSystemTopicEventSubscriptionWebhookEndpointOutputReference":
        return typing.cast("EventgridSystemTopicEventSubscriptionWebhookEndpointOutputReference", jsii.get(self, "webhookEndpoint"))

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
    ) -> typing.Optional["EventgridSystemTopicEventSubscriptionAdvancedFilter"]:
        return typing.cast(typing.Optional["EventgridSystemTopicEventSubscriptionAdvancedFilter"], jsii.get(self, "advancedFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="azureFunctionEndpointInput")
    def azure_function_endpoint_input(
        self,
    ) -> typing.Optional["EventgridSystemTopicEventSubscriptionAzureFunctionEndpoint"]:
        return typing.cast(typing.Optional["EventgridSystemTopicEventSubscriptionAzureFunctionEndpoint"], jsii.get(self, "azureFunctionEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="deadLetterIdentityInput")
    def dead_letter_identity_input(
        self,
    ) -> typing.Optional["EventgridSystemTopicEventSubscriptionDeadLetterIdentity"]:
        return typing.cast(typing.Optional["EventgridSystemTopicEventSubscriptionDeadLetterIdentity"], jsii.get(self, "deadLetterIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="deliveryIdentityInput")
    def delivery_identity_input(
        self,
    ) -> typing.Optional["EventgridSystemTopicEventSubscriptionDeliveryIdentity"]:
        return typing.cast(typing.Optional["EventgridSystemTopicEventSubscriptionDeliveryIdentity"], jsii.get(self, "deliveryIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="deliveryPropertyInput")
    def delivery_property_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionDeliveryProperty"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionDeliveryProperty"]]], jsii.get(self, "deliveryPropertyInput"))

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
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicyInput")
    def retry_policy_input(
        self,
    ) -> typing.Optional["EventgridSystemTopicEventSubscriptionRetryPolicy"]:
        return typing.cast(typing.Optional["EventgridSystemTopicEventSubscriptionRetryPolicy"], jsii.get(self, "retryPolicyInput"))

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
    ) -> typing.Optional["EventgridSystemTopicEventSubscriptionStorageBlobDeadLetterDestination"]:
        return typing.cast(typing.Optional["EventgridSystemTopicEventSubscriptionStorageBlobDeadLetterDestination"], jsii.get(self, "storageBlobDeadLetterDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="storageQueueEndpointInput")
    def storage_queue_endpoint_input(
        self,
    ) -> typing.Optional["EventgridSystemTopicEventSubscriptionStorageQueueEndpoint"]:
        return typing.cast(typing.Optional["EventgridSystemTopicEventSubscriptionStorageQueueEndpoint"], jsii.get(self, "storageQueueEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectFilterInput")
    def subject_filter_input(
        self,
    ) -> typing.Optional["EventgridSystemTopicEventSubscriptionSubjectFilter"]:
        return typing.cast(typing.Optional["EventgridSystemTopicEventSubscriptionSubjectFilter"], jsii.get(self, "subjectFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="systemTopicInput")
    def system_topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "systemTopicInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EventgridSystemTopicEventSubscriptionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EventgridSystemTopicEventSubscriptionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookEndpointInput")
    def webhook_endpoint_input(
        self,
    ) -> typing.Optional["EventgridSystemTopicEventSubscriptionWebhookEndpoint"]:
        return typing.cast(typing.Optional["EventgridSystemTopicEventSubscriptionWebhookEndpoint"], jsii.get(self, "webhookEndpointInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b95b01e5097d8a6eda30534043e3bf5a2586227cd207db114ab56c3cb7e67092)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advancedFilteringOnArraysEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventDeliverySchema")
    def event_delivery_schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventDeliverySchema"))

    @event_delivery_schema.setter
    def event_delivery_schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2925dd135350c06531f75656e2a34d8140637b53ef1ca768ef558733b89b887)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventDeliverySchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventhubEndpointId")
    def eventhub_endpoint_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventhubEndpointId"))

    @eventhub_endpoint_id.setter
    def eventhub_endpoint_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35e611da522d2485b349eba2c1038c7e5ae7c1089da3f3ca61ed32d3645bde24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventhubEndpointId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expirationTimeUtc")
    def expiration_time_utc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expirationTimeUtc"))

    @expiration_time_utc.setter
    def expiration_time_utc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eb0a29736eb41e9cf05b386c0ae6624d4fd2c13902e980b5eab87a2a786cc86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationTimeUtc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hybridConnectionEndpointId")
    def hybrid_connection_endpoint_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hybridConnectionEndpointId"))

    @hybrid_connection_endpoint_id.setter
    def hybrid_connection_endpoint_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c391451d291cae233a1e86765d5a8544b9f234e6970321ba1194f16c312d54c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hybridConnectionEndpointId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29435038a527fb3d696905e8bf00835a563ac3eb33bd4c82841febba7aade637)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedEventTypes")
    def included_event_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedEventTypes"))

    @included_event_types.setter
    def included_event_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09fef22854a19ecf4771887d003643a2dc28b1c2c87230c6c2a82556fe4cc766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedEventTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e47c59e3b7f95ea959f5d7738ded82e371beca65b6d686d53b20d6a6bca40ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80ed412d549f086055a2f13066c4e651a3c2d5cc208be75f3bf1a511d5091426)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ba02be5ae428911cb4d7acf7661bb5b3cf5bbf3d48bd8972e108f473a295bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceBusQueueEndpointId")
    def service_bus_queue_endpoint_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceBusQueueEndpointId"))

    @service_bus_queue_endpoint_id.setter
    def service_bus_queue_endpoint_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__012d97c3b6bc8a5109e6964f8b9275a51b5548a6319f183f6d4659e2ed23eced)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceBusQueueEndpointId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceBusTopicEndpointId")
    def service_bus_topic_endpoint_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceBusTopicEndpointId"))

    @service_bus_topic_endpoint_id.setter
    def service_bus_topic_endpoint_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86a41048d1503555d3eae5c7d966617c5e119b0a8a1fd4717b736e44774ca4e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceBusTopicEndpointId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemTopic")
    def system_topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "systemTopic"))

    @system_topic.setter
    def system_topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3329bc4ad695ae108366649b44a3c7b0180b262bf45885bf211051193771fadd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemTopic", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilter",
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
class EventgridSystemTopicEventSubscriptionAdvancedFilter:
    def __init__(
        self,
        *,
        bool_equals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEquals", typing.Dict[builtins.str, typing.Any]]]]] = None,
        is_not_null: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNull", typing.Dict[builtins.str, typing.Any]]]]] = None,
        is_null_or_undefined: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefined", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_greater_than: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThan", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_greater_than_or_equals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberIn", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_in_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_less_than: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThan", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_less_than_or_equals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEquals", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_not_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotIn", typing.Dict[builtins.str, typing.Any]]]]] = None,
        number_not_in_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_begins_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWith", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_contains: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringContains", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_ends_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWith", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringIn", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_not_begins_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWith", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_not_contains: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContains", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_not_ends_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWith", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_not_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotIn", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param bool_equals: bool_equals block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#bool_equals EventgridSystemTopicEventSubscription#bool_equals}
        :param is_not_null: is_not_null block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#is_not_null EventgridSystemTopicEventSubscription#is_not_null}
        :param is_null_or_undefined: is_null_or_undefined block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#is_null_or_undefined EventgridSystemTopicEventSubscription#is_null_or_undefined}
        :param number_greater_than: number_greater_than block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_greater_than EventgridSystemTopicEventSubscription#number_greater_than}
        :param number_greater_than_or_equals: number_greater_than_or_equals block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_greater_than_or_equals EventgridSystemTopicEventSubscription#number_greater_than_or_equals}
        :param number_in: number_in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_in EventgridSystemTopicEventSubscription#number_in}
        :param number_in_range: number_in_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_in_range EventgridSystemTopicEventSubscription#number_in_range}
        :param number_less_than: number_less_than block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_less_than EventgridSystemTopicEventSubscription#number_less_than}
        :param number_less_than_or_equals: number_less_than_or_equals block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_less_than_or_equals EventgridSystemTopicEventSubscription#number_less_than_or_equals}
        :param number_not_in: number_not_in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_not_in EventgridSystemTopicEventSubscription#number_not_in}
        :param number_not_in_range: number_not_in_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_not_in_range EventgridSystemTopicEventSubscription#number_not_in_range}
        :param string_begins_with: string_begins_with block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_begins_with EventgridSystemTopicEventSubscription#string_begins_with}
        :param string_contains: string_contains block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_contains EventgridSystemTopicEventSubscription#string_contains}
        :param string_ends_with: string_ends_with block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_ends_with EventgridSystemTopicEventSubscription#string_ends_with}
        :param string_in: string_in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_in EventgridSystemTopicEventSubscription#string_in}
        :param string_not_begins_with: string_not_begins_with block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_not_begins_with EventgridSystemTopicEventSubscription#string_not_begins_with}
        :param string_not_contains: string_not_contains block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_not_contains EventgridSystemTopicEventSubscription#string_not_contains}
        :param string_not_ends_with: string_not_ends_with block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_not_ends_with EventgridSystemTopicEventSubscription#string_not_ends_with}
        :param string_not_in: string_not_in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_not_in EventgridSystemTopicEventSubscription#string_not_in}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f91dd6616109a0cf828cd71946693f50c986d00ae0fd8261ebe304350f8927ae)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEquals"]]]:
        '''bool_equals block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#bool_equals EventgridSystemTopicEventSubscription#bool_equals}
        '''
        result = self._values.get("bool_equals")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEquals"]]], result)

    @builtins.property
    def is_not_null(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNull"]]]:
        '''is_not_null block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#is_not_null EventgridSystemTopicEventSubscription#is_not_null}
        '''
        result = self._values.get("is_not_null")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNull"]]], result)

    @builtins.property
    def is_null_or_undefined(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefined"]]]:
        '''is_null_or_undefined block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#is_null_or_undefined EventgridSystemTopicEventSubscription#is_null_or_undefined}
        '''
        result = self._values.get("is_null_or_undefined")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefined"]]], result)

    @builtins.property
    def number_greater_than(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThan"]]]:
        '''number_greater_than block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_greater_than EventgridSystemTopicEventSubscription#number_greater_than}
        '''
        result = self._values.get("number_greater_than")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThan"]]], result)

    @builtins.property
    def number_greater_than_or_equals(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals"]]]:
        '''number_greater_than_or_equals block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_greater_than_or_equals EventgridSystemTopicEventSubscription#number_greater_than_or_equals}
        '''
        result = self._values.get("number_greater_than_or_equals")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals"]]], result)

    @builtins.property
    def number_in(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberIn"]]]:
        '''number_in block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_in EventgridSystemTopicEventSubscription#number_in}
        '''
        result = self._values.get("number_in")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberIn"]]], result)

    @builtins.property
    def number_in_range(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRange"]]]:
        '''number_in_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_in_range EventgridSystemTopicEventSubscription#number_in_range}
        '''
        result = self._values.get("number_in_range")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRange"]]], result)

    @builtins.property
    def number_less_than(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThan"]]]:
        '''number_less_than block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_less_than EventgridSystemTopicEventSubscription#number_less_than}
        '''
        result = self._values.get("number_less_than")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThan"]]], result)

    @builtins.property
    def number_less_than_or_equals(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEquals"]]]:
        '''number_less_than_or_equals block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_less_than_or_equals EventgridSystemTopicEventSubscription#number_less_than_or_equals}
        '''
        result = self._values.get("number_less_than_or_equals")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEquals"]]], result)

    @builtins.property
    def number_not_in(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotIn"]]]:
        '''number_not_in block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_not_in EventgridSystemTopicEventSubscription#number_not_in}
        '''
        result = self._values.get("number_not_in")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotIn"]]], result)

    @builtins.property
    def number_not_in_range(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRange"]]]:
        '''number_not_in_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#number_not_in_range EventgridSystemTopicEventSubscription#number_not_in_range}
        '''
        result = self._values.get("number_not_in_range")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRange"]]], result)

    @builtins.property
    def string_begins_with(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWith"]]]:
        '''string_begins_with block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_begins_with EventgridSystemTopicEventSubscription#string_begins_with}
        '''
        result = self._values.get("string_begins_with")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWith"]]], result)

    @builtins.property
    def string_contains(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringContains"]]]:
        '''string_contains block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_contains EventgridSystemTopicEventSubscription#string_contains}
        '''
        result = self._values.get("string_contains")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringContains"]]], result)

    @builtins.property
    def string_ends_with(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWith"]]]:
        '''string_ends_with block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_ends_with EventgridSystemTopicEventSubscription#string_ends_with}
        '''
        result = self._values.get("string_ends_with")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWith"]]], result)

    @builtins.property
    def string_in(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringIn"]]]:
        '''string_in block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_in EventgridSystemTopicEventSubscription#string_in}
        '''
        result = self._values.get("string_in")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringIn"]]], result)

    @builtins.property
    def string_not_begins_with(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWith"]]]:
        '''string_not_begins_with block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_not_begins_with EventgridSystemTopicEventSubscription#string_not_begins_with}
        '''
        result = self._values.get("string_not_begins_with")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWith"]]], result)

    @builtins.property
    def string_not_contains(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContains"]]]:
        '''string_not_contains block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_not_contains EventgridSystemTopicEventSubscription#string_not_contains}
        '''
        result = self._values.get("string_not_contains")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContains"]]], result)

    @builtins.property
    def string_not_ends_with(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWith"]]]:
        '''string_not_ends_with block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_not_ends_with EventgridSystemTopicEventSubscription#string_not_ends_with}
        '''
        result = self._values.get("string_not_ends_with")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWith"]]], result)

    @builtins.property
    def string_not_in(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotIn"]]]:
        '''string_not_in block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#string_not_in EventgridSystemTopicEventSubscription#string_not_in}
        '''
        result = self._values.get("string_not_in")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotIn"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionAdvancedFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEquals",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEquals:
    def __init__(
        self,
        *,
        key: builtins.str,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#value EventgridSystemTopicEventSubscription#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__266f4c19761e471cb6fb499a82f02b44c03d26c1910a43c54a2727d339565e93)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#value EventgridSystemTopicEventSubscription#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEquals(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEqualsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEqualsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fedb9198c21a1758f9d2de2d1da4b09caf2b76650691ac38afefe6cb4e98dad1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEqualsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caaabc0f679a876a26dc30281066d676ddf5cbddeba6b65858e069590746eb02)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEqualsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d5ff7198c72346e5593c73328a12de328c11e51330b3e46f93c1672e06131fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e615d57e0d025bb60121cc06f9524b0ccc7fd399039da2f5ad2f9f680e6c33f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe660966c2402c7561c34bbfb789a5c10b614401524529715e780952804e3edd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEquals]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEquals]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEquals]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c478452c5725b4973ac80d3b3d334da235f88719fd728e5f95363363acdcf0c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEqualsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEqualsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fd0c44deb22f84e6a049f351175a3237d8667f08bbc11e067c997792b2a4e57)
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
            type_hints = typing.get_type_hints(_typecheckingstub__430594b669800584d695e001b2e6fe8d5f4c8ec96c730e1d8afe531ff7f4e5e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fb8dc7835044cb6e3ec8ddf100ab9f48113dead04edc517087d16d0b5073fcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEquals]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEquals]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEquals]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ece7d849f1838417c100868277aa398764df046e2e479ce95a992467fd05d5b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNull",
    jsii_struct_bases=[],
    name_mapping={"key": "key"},
)
class EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNull:
    def __init__(self, *, key: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f83e93d6af701c72a779d4f25b8f9c31b40778366b3888ece6e39a68c1269e64)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNull(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNullList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNullList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__379c8a84bdaafd78c19e7dd7dba5d9744654a0a390a0c056718c439287be19b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNullOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aebf937cac743193af3a11ce47191ba5e806243c9c549d0d94820f1170d3ae3f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNullOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baba89ecedd9b6cdbb2a69d4531d301ff6126d09a87584d0a5b1c7182285cb2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d01edae4bd6046578d0a9f80a2a8212827bdd770b1a5e0d2e6d10c1f2c4392c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e55601992c5e4bfb43501475817bd0bb0ea44fcc9da1bf9873e7b049c7152c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNull]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNull]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNull]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa3a90c42845743a628add08c2fc623952d23279597ebcc0699bd43b1ca40e52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNullOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNullOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b4270af462eae91e86ffb1aabd417b29a16a5eb9fec11fe3b4e4e5f4c6dda33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c903d85b8c583eba849aa02fd389efb7a672f412adbf1241b270b83a9e788e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNull]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNull]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNull]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87f61dc9e989b08ab1fefe2f12c6f876aa2549abc2b7ee05b55d9de8b5cd6bd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefined",
    jsii_struct_bases=[],
    name_mapping={"key": "key"},
)
class EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefined:
    def __init__(self, *, key: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0588f6527f9ad0206c0c608d7d184d90189efca9d8f5519c6913ac7b60eb4797)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefined(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefinedList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefinedList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__584ee6e4b2ce979c285c991d906d1ce6fbb17c54ade6fede696337c0a988963b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefinedOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c876b8a5486c2cd3a4f80b051336c0dc4c21a069d6b66066d3f217aa21b46a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefinedOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa260bec788588c2aefba2ae796b84d339ccd1bf9d27150b1aa42a93c0f0d36b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0b60fea2a5d4e269919eecb45f0673d1c60359404c6940e196722021e192b76)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6cc9e7a313d135a00a78a88751202a7d51ff0b133aff726ab886d713d3ffd7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefined]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefined]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefined]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab7cf73351111658a7ce51bf9e7b14e012146bd4e376d65af87614a4944f7cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefinedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefinedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32c377833305e992947e0b60ed67b1c3f55cb1d6de5650f55cb94e3563b20cbf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__00211dbce8ef492c9e4af97f7ff175552fe120f328d0aab5251ac48402e4b2d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefined]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefined]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefined]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__504cd8cfe1ef60df4b9eecace9c309765850edb73f918ef8da67c0f7aeea7538)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThan",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThan:
    def __init__(self, *, key: builtins.str, value: jsii.Number) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#value EventgridSystemTopicEventSubscription#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__212dc7ec49ab32047b94d1b1bd5b0c28ac469211866a76f527cd1894a1b04c56)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#value EventgridSystemTopicEventSubscription#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThan(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8744cc1cc1bb43411ff3978519e9e9da98ba446e84f61d42149bffbe5941cdb0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f6ed3ff19082e00be4d91fb4d4d3180eb256a9ce88a8370c83cb1338c572949)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a87fa37ccc4bd4f091254cdf507126a0212198e847c52bc207338f77e20ea70a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c6d9ab63bb8b920f89efdf3426cbc75ece82cd3208be6352e8d81e90df3a06f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__03ee6b8be9af8aca81b746774b5e923e7843aa8ed81082e7d29d46ac5dfe1767)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThan]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThan]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThan]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363597ebd4d1a523055c5dbe4c9571678d6db4eb3fe528bfb601acecb6915e97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals:
    def __init__(self, *, key: builtins.str, value: jsii.Number) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#value EventgridSystemTopicEventSubscription#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53d8e9f3fb6f3fd59859fdd008493961f17c4c9b4388eb621955116da9fd893b)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#value EventgridSystemTopicEventSubscription#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEqualsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEqualsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ee39d11d3f7ce3789dfee893837742d7c8c69e84366914548347ba6bfc0da95)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEqualsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c4f1618a84dd695565352b6adbf41c9b28c13aaf62fc255a9b1085928e5fda2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEqualsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bce324803f4293e0f11e92c2fc84062e201bc452093621bfda00bf85fc7454f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__88c1826284c66c0ac359a2953549fa235a7eabc9ef1228676ff64123409285fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2ca4b263b354fa97565157ddcea17fb1854b90516627d6e81d6cdd3d857cd0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59a67684f263d9e6e9c7eed1dd8e7b80eb04e51cea3feb7d06f05563b489ceda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEqualsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEqualsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0013ee048e4880ad892f9df739b9ca52d7aa4e126cbb596773f5908c5dc77e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__33d94e040e615d2a8e84e35ccf2248cb32833f77f2d029186c0c8e80893c7deb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1857df325880ce0ab3e160d5ebda6b6895b970b7138e62c687d476a0921fbeb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f80818536f9b790627147cc4bc5889cf11d9a202d6f69272841723513a227358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bded1fbd87950082ac53a6bcb55e1fcb4e5495e350b9485985b1dc58b4467943)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8eb7784857701a43a7dc4fc41cb85e63064bc602cf7186699f3c4bd7206bf3cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5ab0e6db63035a923169e6f1ff65221b9115201cb8130fafae877bfa60c06b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThan]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThan]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThan]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__328494fcc5ea43bc8321e1b4f9f4042257dfa89f71f0ba746907e0eaadcec06d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberIn",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberIn:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[jsii.Number],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38590be1cad9fdf3eddefe8d7fd4817c8ee56e9049fd639f256a9f0608678fa9)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberIn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09c59508ecd65f416e09e930ca12303e0756ca00a7f6f847f8357c22e39fdd79)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d26048f7e7a89e0df8a0c1fc56d4ccc72c73b84fb49db72830d1ebef9da292b0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ad4b2030e2ae4666e48069e6e909e04bd4fd7c64d569e09ddeb1c4272af151)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02efa689dbd5a2d32917aede151b53f2322ab4b235975bacfb2a0b6874f27ca0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__313e274aa0972cfce4b6caf069bfe59007fd12dfe4cb70ffca0ddecd6437c606)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberIn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberIn]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberIn]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37f1bde5d6043a4e78f962a96601c3fa3b6e2f02bf5c6625ad439272f481cbc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__082276f2d90f7ca687e2c74e18f4d1bc9a7904928e49df4d03416464317dd0fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45a8e93268b80ff192a58ec91c0e43de0e38d3126b19ab874c78cb79a6fa517b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f3f1d16cb2fa5cd536aa5ce67ac372eaae07a5ff710eb8788ea407ace9d8581)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberIn]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberIn]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberIn]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4c24f76c55f5c033c97be52fe2d52ced74b4ad2ff389833e46c0e7815ed303f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRange",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRange:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Sequence[jsii.Number]]],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c8f51541c6f3ba8de2aecb9cc637a1e53538baa6f1edea94dff163c747dd880)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[jsii.Number]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[jsii.Number]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRangeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRangeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a55f450162087e375db2a4f7f5cbf4fe6be5df1283465ae60d3ac67fcba7c696)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRangeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9638b24bb219586b5c9557d846f63c0347c06928e1f28395ca96bbca7593dcd9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRangeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__850b2b9ce598437ccec8a5a4c7078c7a45db44b7dd745385a29e2f0131873c3e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0d97504b0294fe9acac6ebd164f40c6de3f700b2e4d17827528db9e1a73cb3e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc7567597735c37588eaa773ff674a26cbe668f6989352f89773ec7b934b9742)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRange]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRange]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1cad6656ed151b093290ff2430c588a3cc4b3b5122e6a23316afec9fa9ecfcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25ece7b805e8228c31645d5437597d883ffa9426ba6213284765859829cb77b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1411d22d468e58c53b68e23728a4f30ef97a08fcd7f4f80d30f1d185785f3d5e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f99b3465eccb18171c02e6900c4ccf4ff0fe7a649933a1cd6e72b251471d2092)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRange]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRange]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRange]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e951a571dee5ee2d99f61a892da231cdd9c18149135c418478460171a4e7df0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThan",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThan:
    def __init__(self, *, key: builtins.str, value: jsii.Number) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#value EventgridSystemTopicEventSubscription#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bd4da26fc901d5e3d7937a5a549e82520c7e52e687c6618a8009fd193d215b9)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#value EventgridSystemTopicEventSubscription#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThan(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be775d6dec6a7c0f58137ad9d13dd6412391719b4c35ad1439fa3dd6bbf93022)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__978a700ab210563ce598429d91fb268578b4704bb69e93e5482524cad1c44785)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2701f56283fc45fdba7a198ef86d66af040499d152c5d681477dbbeaec0508d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da8b956f472da56d40cbf5f656c169fe712e714ce3ab5302ba8651f089b1a9e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad4d1d1c7360d937115e8eea4e59069b8a4d41b507ff1c7de026b8a811574606)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThan]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThan]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThan]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c593920d8cb9789604a38b0dafe91352983416fcc658238bf6dea1b5d06a7ce1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEquals",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEquals:
    def __init__(self, *, key: builtins.str, value: jsii.Number) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#value EventgridSystemTopicEventSubscription#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__722ccb489da02bd00e33c2dbd0ac4fe684138ab767078b7cf5320e87122d3eb3)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#value EventgridSystemTopicEventSubscription#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEquals(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEqualsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEqualsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c2a021b023cf766cf4a0279b04f477c082fc42eb076d197d79c44861ad0c0a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEqualsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__236b005a1823cf644dcf7d7edbb2f095020f45d94423bef44ccc2e1782430f94)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEqualsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c89966a5eb992c66a44d31c94c96fdd407c1cd16ea672d9164d0bc6eaf5da3ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3276b50071d96a2a6ceb7462475ba12525d0c782b2b24255a6e8edebb36df554)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8997fe862b4a83a5ca2e6d9b777210588ab8e7ce2dd397e5de42ea786f11d0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEquals]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEquals]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEquals]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f23e54257799e829f7908f54b85e18b597a2dca453425007ec9401b8571c5379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEqualsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEqualsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c03ffc252a39db678e3547031e5c19e97f5077ad60c5943c3ca2b46c899433d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7f1129785b714fcc7f12e5a7ea741188f73415a0678ae1e38a397b2ea8aaadf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6176ad862810180fec13d28e15dd9797ea76ded11fec70a7110c392079645933)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEquals]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEquals]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEquals]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5e51aad42aee50e325e633067c38ecda8374c39303a0cfa2041b89ce00ec7a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e897305d63deef854d2e64775ccf70c8c37f4bd2d6ddc7edd7dca71c4f955f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83b3e92c0a4aec18fa58d014afd50213189243af369c05b8ae538a499674b8bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa3daa33beecb2e5037e971a52764c03c2e52570f0667e53498f803b60f36ec2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThan]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThan]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThan]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bd6777d9e1485c0de0473ad1697d05f7a05116933499a9d2989062406e0a8c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotIn",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotIn:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[jsii.Number],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__600610e7a69f7571d91c55c2a1897fe4814345c63a64bc61d557c50b0ba2e0cf)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotIn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e212411557dcc056a31789c13a5c41a1247b04dce040a55d94e543538d66d09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e1ec3a302a3b2fcac2bc23e85cbd79112fdf4775e3c739b7a2d753d0a84239f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99634073feb39bdc3a88c53c29ee8da5e10ce2e4f89a87ad066869d170f47384)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47ff107f5b5256e71c5f95976ef069dd34f6ca41cfb96ba2137746d791e1e875)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef23511c7374c92f3a467c722a82933b93e1d372955f4886a5eb82071f26d950)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotIn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotIn]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotIn]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62c17be27a8f13192429eae36d8ef382da179afc09d8ffe98d15a32aeccc445b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c6aea348a5a1a774c0e0096a2199e5516cec3b05e27f2a950fecb4374536fa2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44a42741710376f645c8e40499420680b72fa4108c6689ca1d3973f14279ecb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb12fe3c2848c4f01b71fec127ebf974a6f4a9690071b79ce74148c52784b58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotIn]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotIn]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotIn]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daa338eaf09c3aac860bb2aebaef135829810226aa068fb8c6507241112e209f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRange",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRange:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Sequence[jsii.Number]]],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70e1f55b525b5cedfcbe35f0fe31650178e0b88e2073d002cc0a96fd2a06aee6)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[jsii.Number]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[jsii.Number]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRangeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRangeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98d68f2b578dfd252a0c49ff1cd93bc26de3d239029faf46fd5fba85da98131e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRangeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6aa9722fefe9217626e084198fc82861a399f500c85a9553ebc3445d992ee80)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRangeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc4102568fc731087ae83fe84e12fa77e7de414ee29ca32f204509747305602f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85ff8ad82e7dad951cf4bb6a1b7e6d15464638d229f5ece1fa738dda68431696)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59b9bb18edfcafed4d91717eecb48d1fbe12b31780b55a6783e50de8fc028bb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRange]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRange]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c545604fa5ff93812efb0774c19749534a5cef8bdfeb9923d22bda77d559078)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f3cb5fc36d2b8ca046fb57848ff7454ff25efb101e91fa9493fd9880c222ec4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4829e43640a3b4d5a129dee3edc1f4c8ac46205070acb6a40df2fd4697a80c9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6b93ec8f40074e49325f4da5072c0da4b980a5c217d205e245b6bd19f50850d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRange]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRange]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRange]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d5a4004762bac8d0f2db0b62b2d944a4bf2022fb04352569456c33aa0c81994)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridSystemTopicEventSubscriptionAdvancedFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ecff7b72995c07bb2906528c5c358d483cd57ba87f6ba1d5dcae450299e40a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBoolEquals")
    def put_bool_equals(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEquals, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b715a06467857bb862cc8a47b1ac93129d439d25d115ab79a5c8b5040589482)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBoolEquals", [value]))

    @jsii.member(jsii_name="putIsNotNull")
    def put_is_not_null(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNull, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__639d630b20075dadceeedd19e2e0707b215aac1cb874da31fd821ffcd912ad59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIsNotNull", [value]))

    @jsii.member(jsii_name="putIsNullOrUndefined")
    def put_is_null_or_undefined(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefined, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c397241610d10bddb1ac05d628a19e516aae679ad83d162b91b4c80fb2ac0aec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIsNullOrUndefined", [value]))

    @jsii.member(jsii_name="putNumberGreaterThan")
    def put_number_greater_than(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThan, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72b726f5f1249631f6281489ebf1bc0ba0b5e1c10ede04299da1e0c2875ffb8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNumberGreaterThan", [value]))

    @jsii.member(jsii_name="putNumberGreaterThanOrEquals")
    def put_number_greater_than_or_equals(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e0b9d4da64435ca3ee978040675a9e1864783b8b5634fa1cee5646e846f808)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNumberGreaterThanOrEquals", [value]))

    @jsii.member(jsii_name="putNumberIn")
    def put_number_in(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberIn, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f1eb05703a8199d114d9fb4fb96220856887270e168a56e8834df8d72acf5c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNumberIn", [value]))

    @jsii.member(jsii_name="putNumberInRange")
    def put_number_in_range(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRange, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03dc2a10553633546ff0a55231f0c61acf727ef1487a6d421a141546b141b782)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNumberInRange", [value]))

    @jsii.member(jsii_name="putNumberLessThan")
    def put_number_less_than(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThan, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3579506d2aab13280afbe3ce7864271f6cc2a983dbd7fb7e4980a346773a162f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNumberLessThan", [value]))

    @jsii.member(jsii_name="putNumberLessThanOrEquals")
    def put_number_less_than_or_equals(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEquals, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52decfcffe75ff5a96d0b3ea3a048a03042dbc2021b7e65b00936df34dbe7ebd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNumberLessThanOrEquals", [value]))

    @jsii.member(jsii_name="putNumberNotIn")
    def put_number_not_in(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotIn, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f361164e21a1297a7b52f4d7dff99386a08df535e63fde051babbea28fca17c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNumberNotIn", [value]))

    @jsii.member(jsii_name="putNumberNotInRange")
    def put_number_not_in_range(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRange, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2127dec11416b74d47c80847606962d4260a8787d5e8e8a1f23d837cce73b01e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNumberNotInRange", [value]))

    @jsii.member(jsii_name="putStringBeginsWith")
    def put_string_begins_with(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWith", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49070197c00bdd12095b66a2f2f94361f2ae2181c5dc0063a3f817407f38d56a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStringBeginsWith", [value]))

    @jsii.member(jsii_name="putStringContains")
    def put_string_contains(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringContains", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f86bb92e1a0419eb73eca9f304084a2c462cf789a3d4092f1c2d97e1c9ae2009)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStringContains", [value]))

    @jsii.member(jsii_name="putStringEndsWith")
    def put_string_ends_with(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWith", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a947487879976ea460abeea969d7a05e58375ee74efc810aceb0a541ddfd248f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStringEndsWith", [value]))

    @jsii.member(jsii_name="putStringIn")
    def put_string_in(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringIn", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbfe8ae547d35a62b4ada32707ffbc0bcf534581ddfa654c0e14f31a381a1cf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStringIn", [value]))

    @jsii.member(jsii_name="putStringNotBeginsWith")
    def put_string_not_begins_with(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWith", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__312a1243bd180df4e9014272c3d630104f0fd89dc4ba34133c4e1d305a7098e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStringNotBeginsWith", [value]))

    @jsii.member(jsii_name="putStringNotContains")
    def put_string_not_contains(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContains", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a7b1381adebb0a1fea6e6679d61cb5608c4aec48d371eb15c2f238721cb23d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStringNotContains", [value]))

    @jsii.member(jsii_name="putStringNotEndsWith")
    def put_string_not_ends_with(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWith", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3446fa15a0b84f47062b169d837598c33ceafebe9e4236f475aa631c8f25cf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStringNotEndsWith", [value]))

    @jsii.member(jsii_name="putStringNotIn")
    def put_string_not_in(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotIn", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__211204455d0a6b619de9792fd0ed8155ff931cb6fe7237e506ec6562fdf69e7f)
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
    def bool_equals(
        self,
    ) -> EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEqualsList:
        return typing.cast(EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEqualsList, jsii.get(self, "boolEquals"))

    @builtins.property
    @jsii.member(jsii_name="isNotNull")
    def is_not_null(
        self,
    ) -> EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNullList:
        return typing.cast(EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNullList, jsii.get(self, "isNotNull"))

    @builtins.property
    @jsii.member(jsii_name="isNullOrUndefined")
    def is_null_or_undefined(
        self,
    ) -> EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefinedList:
        return typing.cast(EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefinedList, jsii.get(self, "isNullOrUndefined"))

    @builtins.property
    @jsii.member(jsii_name="numberGreaterThan")
    def number_greater_than(
        self,
    ) -> EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanList:
        return typing.cast(EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanList, jsii.get(self, "numberGreaterThan"))

    @builtins.property
    @jsii.member(jsii_name="numberGreaterThanOrEquals")
    def number_greater_than_or_equals(
        self,
    ) -> EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEqualsList:
        return typing.cast(EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEqualsList, jsii.get(self, "numberGreaterThanOrEquals"))

    @builtins.property
    @jsii.member(jsii_name="numberIn")
    def number_in(
        self,
    ) -> EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInList:
        return typing.cast(EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInList, jsii.get(self, "numberIn"))

    @builtins.property
    @jsii.member(jsii_name="numberInRange")
    def number_in_range(
        self,
    ) -> EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRangeList:
        return typing.cast(EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRangeList, jsii.get(self, "numberInRange"))

    @builtins.property
    @jsii.member(jsii_name="numberLessThan")
    def number_less_than(
        self,
    ) -> EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanList:
        return typing.cast(EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanList, jsii.get(self, "numberLessThan"))

    @builtins.property
    @jsii.member(jsii_name="numberLessThanOrEquals")
    def number_less_than_or_equals(
        self,
    ) -> EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEqualsList:
        return typing.cast(EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEqualsList, jsii.get(self, "numberLessThanOrEquals"))

    @builtins.property
    @jsii.member(jsii_name="numberNotIn")
    def number_not_in(
        self,
    ) -> EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInList:
        return typing.cast(EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInList, jsii.get(self, "numberNotIn"))

    @builtins.property
    @jsii.member(jsii_name="numberNotInRange")
    def number_not_in_range(
        self,
    ) -> EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRangeList:
        return typing.cast(EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRangeList, jsii.get(self, "numberNotInRange"))

    @builtins.property
    @jsii.member(jsii_name="stringBeginsWith")
    def string_begins_with(
        self,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWithList":
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWithList", jsii.get(self, "stringBeginsWith"))

    @builtins.property
    @jsii.member(jsii_name="stringContains")
    def string_contains(
        self,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterStringContainsList":
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterStringContainsList", jsii.get(self, "stringContains"))

    @builtins.property
    @jsii.member(jsii_name="stringEndsWith")
    def string_ends_with(
        self,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWithList":
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWithList", jsii.get(self, "stringEndsWith"))

    @builtins.property
    @jsii.member(jsii_name="stringIn")
    def string_in(
        self,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterStringInList":
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterStringInList", jsii.get(self, "stringIn"))

    @builtins.property
    @jsii.member(jsii_name="stringNotBeginsWith")
    def string_not_begins_with(
        self,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWithList":
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWithList", jsii.get(self, "stringNotBeginsWith"))

    @builtins.property
    @jsii.member(jsii_name="stringNotContains")
    def string_not_contains(
        self,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContainsList":
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContainsList", jsii.get(self, "stringNotContains"))

    @builtins.property
    @jsii.member(jsii_name="stringNotEndsWith")
    def string_not_ends_with(
        self,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWithList":
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWithList", jsii.get(self, "stringNotEndsWith"))

    @builtins.property
    @jsii.member(jsii_name="stringNotIn")
    def string_not_in(
        self,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotInList":
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotInList", jsii.get(self, "stringNotIn"))

    @builtins.property
    @jsii.member(jsii_name="boolEqualsInput")
    def bool_equals_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEquals]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEquals]]], jsii.get(self, "boolEqualsInput"))

    @builtins.property
    @jsii.member(jsii_name="isNotNullInput")
    def is_not_null_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNull]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNull]]], jsii.get(self, "isNotNullInput"))

    @builtins.property
    @jsii.member(jsii_name="isNullOrUndefinedInput")
    def is_null_or_undefined_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefined]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefined]]], jsii.get(self, "isNullOrUndefinedInput"))

    @builtins.property
    @jsii.member(jsii_name="numberGreaterThanInput")
    def number_greater_than_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThan]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThan]]], jsii.get(self, "numberGreaterThanInput"))

    @builtins.property
    @jsii.member(jsii_name="numberGreaterThanOrEqualsInput")
    def number_greater_than_or_equals_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals]]], jsii.get(self, "numberGreaterThanOrEqualsInput"))

    @builtins.property
    @jsii.member(jsii_name="numberInInput")
    def number_in_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberIn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberIn]]], jsii.get(self, "numberInInput"))

    @builtins.property
    @jsii.member(jsii_name="numberInRangeInput")
    def number_in_range_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRange]]], jsii.get(self, "numberInRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="numberLessThanInput")
    def number_less_than_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThan]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThan]]], jsii.get(self, "numberLessThanInput"))

    @builtins.property
    @jsii.member(jsii_name="numberLessThanOrEqualsInput")
    def number_less_than_or_equals_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEquals]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEquals]]], jsii.get(self, "numberLessThanOrEqualsInput"))

    @builtins.property
    @jsii.member(jsii_name="numberNotInInput")
    def number_not_in_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotIn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotIn]]], jsii.get(self, "numberNotInInput"))

    @builtins.property
    @jsii.member(jsii_name="numberNotInRangeInput")
    def number_not_in_range_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRange]]], jsii.get(self, "numberNotInRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="stringBeginsWithInput")
    def string_begins_with_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWith"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWith"]]], jsii.get(self, "stringBeginsWithInput"))

    @builtins.property
    @jsii.member(jsii_name="stringContainsInput")
    def string_contains_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringContains"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringContains"]]], jsii.get(self, "stringContainsInput"))

    @builtins.property
    @jsii.member(jsii_name="stringEndsWithInput")
    def string_ends_with_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWith"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWith"]]], jsii.get(self, "stringEndsWithInput"))

    @builtins.property
    @jsii.member(jsii_name="stringInInput")
    def string_in_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringIn"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringIn"]]], jsii.get(self, "stringInInput"))

    @builtins.property
    @jsii.member(jsii_name="stringNotBeginsWithInput")
    def string_not_begins_with_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWith"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWith"]]], jsii.get(self, "stringNotBeginsWithInput"))

    @builtins.property
    @jsii.member(jsii_name="stringNotContainsInput")
    def string_not_contains_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContains"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContains"]]], jsii.get(self, "stringNotContainsInput"))

    @builtins.property
    @jsii.member(jsii_name="stringNotEndsWithInput")
    def string_not_ends_with_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWith"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWith"]]], jsii.get(self, "stringNotEndsWithInput"))

    @builtins.property
    @jsii.member(jsii_name="stringNotInInput")
    def string_not_in_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotIn"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotIn"]]], jsii.get(self, "stringNotInInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventgridSystemTopicEventSubscriptionAdvancedFilter]:
        return typing.cast(typing.Optional[EventgridSystemTopicEventSubscriptionAdvancedFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventgridSystemTopicEventSubscriptionAdvancedFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56d8931fa26094f8c3863913c3ff68304f41597c5166fe8ee3c9073aa7a2d825)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWith",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWith:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dca2870aca0df9a382226541ba9bd3a82f241b15bae8e7073d37f82e4b2e0238)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWith(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWithList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWithList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fd35f508b234bfafdbcc0fc2ad21fea507dfaed83c578e74db9aef655f0f5a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWithOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a96b6d1a8e1554e67ecbae662324176aebccf0261e6ecbe2cab95327ead00d82)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWithOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f82d3f86c58683ca81b97d808ac703bcef84b3d074335fa4c02a7748d91da1f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__211ada65e72aacf667e31017c6234edf6a13c94a0b1430c8a7045c12086167b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__99dacf2f891463ef9257463635d899da9189742915d866cb82b0e8aaa594034a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWith]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWith]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWith]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__582db5588ae608d97938944d5eec4a902f086523f958e59058032ee7fdba91ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWithOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWithOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3104f1da4b39338dd06b53fc661d53b1c2340e796febfff5f05bc1664d5ee8e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3eaa5470c4a5bfa5701c47d96065ecae8b9bba6057b563962930c9e9ae3bc49a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7854eafaaeadeb77abdb1019ecb720bcb5368692e6c0ff36d133f95c7195a76a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWith]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWith]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWith]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ada9dd37ac50a84bf0886c887436e8b3ca09929609e56420c6a3201516612ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringContains",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridSystemTopicEventSubscriptionAdvancedFilterStringContains:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f8d74379d2af9dc423498cc1f580503580a7fa1c731bf824bce4ed1b072ffca)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionAdvancedFilterStringContains(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionAdvancedFilterStringContainsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringContainsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50a808b956a4dd92a642ceda45c34592fe48237f0f0f2d1255a680dc52f203f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterStringContainsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__471374f337810b5f28feab56d23146ef67d8fc1f56edacd18685a73cebb909b1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterStringContainsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e12deba80aa35775b08c2b35e27d2fcc7336ae7a1cc72e03dbdca73dcccf9fac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__578c1675080b3c771ad3c1f1462f7b9ffd125808ea33b552c83141a26ab2729e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8c424597198538691a5ed67a8fe3c16ac553317b817ddb4b08df5c6d6018188)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringContains]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringContains]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringContains]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d8be9e350935d3d507297269b46bf50def6187208980bd9b854383ba943254b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridSystemTopicEventSubscriptionAdvancedFilterStringContainsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringContainsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__074be7d761bb6fccbdfecbf637dbfd3b6ab2a6bf81de4b1af071342d5b1da078)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7caea28fd124df581ffcb991674b7908e174cf8754440bc536e44cc8871c0de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397805a8b28245daae039a6b3cb61c4e5e07d0ba0af412bb039836cf0541359c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringContains]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringContains]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringContains]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b100575cb7d2c745f41a49216253b57de77cc02e25f4496838aa28de24d990)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWith",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWith:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5249c56975e1bc798ca97bc93a0a4f2f72ceb19a1d0f6b0c0285e962527c8255)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWith(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWithList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWithList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d99effc5319d07b728447bf5f7c0b5d0731155fa0edafea5256a8403aa720fd9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWithOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7837c9981981bc440e7acae9da373a16b495ddd69a2c5fbf0bc9290ed1fff84c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWithOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff816bdd87db1be27b0fd82db47214e178e97a4d860da9280642ee95a05a892)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa8748ae1969b7df31e13ecf358dffe730adacc9e334ff1ea365423334090457)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6492239d63a0977b5a3f39931ffd0e78bab5de7f06c6e1dae47bde541ce11ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWith]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWith]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWith]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__742426f957ea789c83470aea9b1e52ed4f62d5562f572ebd87c4806b9d577d1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWithOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWithOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__406fdab4aedc08eca1939064aba3e83ff4a30881dc4a6e4b77b5706f2c00afea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__897cba12f2887ae62dd6d69048b66f0a06350ba8a44a93959f53f6151766871a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb7db7207b21454f2434441eb9a78d40945ae44ed6e887401fb8af15279b0ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWith]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWith]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWith]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38b483f187155db70d38ff89836fe71aeb0ac7c7e56e4b870e2cd25e51a00eca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringIn",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridSystemTopicEventSubscriptionAdvancedFilterStringIn:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c3845311e2fb42753a073a7084f0218e5ebd89a0b8d331ce4521772870ebd04)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionAdvancedFilterStringIn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionAdvancedFilterStringInList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringInList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96e439804bd1b7ce015c2c497d5cd457d5ba2612c6c3eb75928f828204c2d21b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterStringInOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84c0f9704cb503a08e70a6c2e20b25068320fa39f66cd40f6c62072a30ffe6d2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterStringInOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deefa8daa91b9c6d6ffe6c16ad88f176b9bf861cb8e766a2808e304e3c81fd14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a6ddc0dfd76df3fe81183c71cc42223046d1121581a76ea91996f267ff79dea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__faf6c379007d5fd72db7721768a461683e9dae41de39dbbbaa2a01dee663006f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringIn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringIn]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringIn]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d3e3fad9f39633c7740f78db85810ef774e1b57d5550535d9019bb45949bf39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridSystemTopicEventSubscriptionAdvancedFilterStringInOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringInOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4004d3771984812132800e64caaead647c371172704184372a06365783c3a169)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a30fde84f9f33253eaa7c5e518aac2f0e3ff16b072236fb052c267acecdb81c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c2e10dbdf74603294f9d507727af360e1240f1750e4feb93f9713af88f02094)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringIn]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringIn]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringIn]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4863ec9a3d19770ce29fd2e90901c67509e4d1833fa4116cc208c407d03692e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWith",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWith:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee5462c3e4c4c65105dcfde6e672fed1a5abdf166d719885023040623229f11c)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWith(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWithList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWithList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e34ad57a422031a77315fb9f7c9e36234780a5d1b754ae09abf1bb176d94f65c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWithOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1b6cecc7621334b6312372d10310a4cd071a0ad28faed6fd46aefb5ac5c9405)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWithOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c19db116baf1a94d668c294a2c70231c1eaf6a45d1eb76fb6aee671a1ff2b21)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c60faf25e54318350754de7ad4eb426959699e7c47be1ae0dde8e2196cc39034)
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
            type_hints = typing.get_type_hints(_typecheckingstub__970b3b178e0dab819f794eaffaf7b53a86f1516f33dc3f1daca576d68e519c23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWith]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWith]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWith]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80b17fb67dbcef7d73398719de162e7dafb9ae8788dd793aed5e238b6522b18f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWithOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWithOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__104b7b0d4ca410ab1679c3374a34e5e00935e6c027af49fe6e54790538bbc6ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab7818ecb82eb8b472e46e464db45af156dc05279027505b31ce8ce90f06930c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ece0d5361b20f8f9fc3cf4f31d560b99f7193fb44f83fdadbd8885a314f2fc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWith]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWith]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWith]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c2547582b9eed78a067433137f04a92ac2ff330ad45b3c8326b4e80657840d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContains",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContains:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8418d897e4273f7cf5824ff913a2f300c5e0eaebaf5d426c3d7564e67fde1a93)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContains(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContainsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContainsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed799fb72f536534aef375098a1ca7de6d95f9e7656e9ecc6cc8b4646cf02553)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContainsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c4edae0e53cca5402033b7b6e751795dbf430e630aa2d97e06a4c8504bafd79)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContainsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef3bd6f44e8b2d0920c4ebf0534ab1db0c2a0674a9051d9feb4bb9899a323455)
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
            type_hints = typing.get_type_hints(_typecheckingstub__42252bdad5a34de2eabdc2379c867f9d26535cc90529e9924bf03956a55bcb32)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f05103922761e591f1652ac49a7f4f253b9309b2bc75eba797ca027693496eaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContains]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContains]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContains]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7ae42acc8e681680d6cdfdfeee30d246120bd467453be92292f375ed810409)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContainsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContainsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb815e9184b32ef91dc41d2d4c323f26f31c6b5bbc6ade9c8fbab431cff16a51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6c5efdb4a1073aba8c276e128938557053f08b8eb45c79cde9d70f6ad5c62f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b870d9979b2f70728919dad2356e1e663fad7782fbb58ffc1633a332107a2243)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContains]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContains]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContains]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0906b332bf42b53301e6d5474c503f0cfdbb135eb74c681ec6532b45dea4b3b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWith",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWith:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c2a648113e8cc36a998d9acb29a1149059f575178f11b5015724b174cb16a0b)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWith(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWithList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWithList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a2e8580266a9b191d0b345b4e3b87f8410241636e4a334aea0c0fe6a9e30bf3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWithOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__684f915fcf26aed6677c89585405ee442fa320d5b2a68d2443ea62a3aa3ff173)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWithOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f18e3de0c71b388d047b4cdb8825e721f24cad91835f9d0c217e9621e618412f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__88ed65916e7a53c858bbef72039d85c155357e70f9266831603f7f879f75d2fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d283166b573a695e0c2b1a691e34cc57882958844e2c4444cbe34de616b8be2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWith]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWith]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWith]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__037270d4a6e20e2058078bdc3b5b0dfe6275fa4d4ecfc0e283bfff5dfaea5519)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWithOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWithOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__243352a411312c3334892ee2e56103048227bb0c7273d85937e78321e182997e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d881bcc5201bce20112693afe6d1406d7d4ca1c652ad9a4e5433cb73a49dc67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e7d6b291836395912e2457fd16a558fb5ae798a102e17bd07d999b913dba862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWith]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWith]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWith]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78050692cbe4ca7103b7fb308e7625b5c8e41d1e0bcfb9085ff69d985378d9e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotIn",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotIn:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d4c5a32625ee2b2a1213e8405344a77bdb985fa2633e09181a02ce2c2c29d0e)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#key EventgridSystemTopicEventSubscription#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#values EventgridSystemTopicEventSubscription#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotIn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotInList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotInList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e606972c17612a52285172dcba360894a3d2d5873f2194e83e2d4b6549fc2371)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotInOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d7474b8eee71426e22fbe23178dfda8f2a30d121c6f5cf966e32e9b899f5f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotInOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__267664b31002ab3abe04e04dc6957ecd418a4d851ce7b27eec9a4fbe079b570a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3dbe0fe6cd97926a43ed8c6f778b270b4c35a4d4a7bbddca6ac022ce859e3898)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8c30e96109be1cfaf01526378b93abb8e49df0c51b36cadd317d94cc35e3f40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotIn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotIn]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotIn]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43990881aa381ff1b77458e3855a4c53b2c68ca49a0c166b97293c98ca3dd338)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotInOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotInOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fb9af9da6a4f23a588043de32daf233d0bb671472fd198f5ff8c3e5ee8a102e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e058186337aad10dcf201bde432b8ba53b007f772b28ed6c575a1cbd74cbcb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__094d039466663bac8b7c1c0069a539dd98cdda20dcf79206590793a7b2156057)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotIn]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotIn]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotIn]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a57fd8af2475f6f2483c356ee83d9708a7fdf7144b8af3b40887ea8409c5e0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAzureFunctionEndpoint",
    jsii_struct_bases=[],
    name_mapping={
        "function_id": "functionId",
        "max_events_per_batch": "maxEventsPerBatch",
        "preferred_batch_size_in_kilobytes": "preferredBatchSizeInKilobytes",
    },
)
class EventgridSystemTopicEventSubscriptionAzureFunctionEndpoint:
    def __init__(
        self,
        *,
        function_id: builtins.str,
        max_events_per_batch: typing.Optional[jsii.Number] = None,
        preferred_batch_size_in_kilobytes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param function_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#function_id EventgridSystemTopicEventSubscription#function_id}.
        :param max_events_per_batch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#max_events_per_batch EventgridSystemTopicEventSubscription#max_events_per_batch}.
        :param preferred_batch_size_in_kilobytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#preferred_batch_size_in_kilobytes EventgridSystemTopicEventSubscription#preferred_batch_size_in_kilobytes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecdfd564b60c7d61d07607a1e715bee6918d2de7bc3c44ae34a11501335494d2)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#function_id EventgridSystemTopicEventSubscription#function_id}.'''
        result = self._values.get("function_id")
        assert result is not None, "Required property 'function_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_events_per_batch(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#max_events_per_batch EventgridSystemTopicEventSubscription#max_events_per_batch}.'''
        result = self._values.get("max_events_per_batch")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preferred_batch_size_in_kilobytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#preferred_batch_size_in_kilobytes EventgridSystemTopicEventSubscription#preferred_batch_size_in_kilobytes}.'''
        result = self._values.get("preferred_batch_size_in_kilobytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionAzureFunctionEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionAzureFunctionEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionAzureFunctionEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cd3966f14ec6acd4cbf517c4ff4b3b2f04af70611c2c14aaad03eb7e1b3666a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__044d7f5355b4bc30c24c6ca0b125764cd573094c80e50ca697cb025fccd20c34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxEventsPerBatch")
    def max_events_per_batch(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxEventsPerBatch"))

    @max_events_per_batch.setter
    def max_events_per_batch(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d79b93ac0a3d8a4a58e879d030b2e90e1fd26eb4fe1ee892f06923d5c4f033de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxEventsPerBatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preferredBatchSizeInKilobytes")
    def preferred_batch_size_in_kilobytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "preferredBatchSizeInKilobytes"))

    @preferred_batch_size_in_kilobytes.setter
    def preferred_batch_size_in_kilobytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a83a0c766ee569c26632e8406a1034b403df3e982cd8a26af24501505cc86e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredBatchSizeInKilobytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventgridSystemTopicEventSubscriptionAzureFunctionEndpoint]:
        return typing.cast(typing.Optional[EventgridSystemTopicEventSubscriptionAzureFunctionEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventgridSystemTopicEventSubscriptionAzureFunctionEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe75eb005ac60ef5339d43be9be3116a7b895c7ac7bf7b1167fad5fdea901a40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionConfig",
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
        "resource_group_name": "resourceGroupName",
        "system_topic": "systemTopic",
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
class EventgridSystemTopicEventSubscriptionConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        resource_group_name: builtins.str,
        system_topic: builtins.str,
        advanced_filter: typing.Optional[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilter, typing.Dict[builtins.str, typing.Any]]] = None,
        advanced_filtering_on_arrays_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        azure_function_endpoint: typing.Optional[typing.Union[EventgridSystemTopicEventSubscriptionAzureFunctionEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
        dead_letter_identity: typing.Optional[typing.Union["EventgridSystemTopicEventSubscriptionDeadLetterIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        delivery_identity: typing.Optional[typing.Union["EventgridSystemTopicEventSubscriptionDeliveryIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        delivery_property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventgridSystemTopicEventSubscriptionDeliveryProperty", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_delivery_schema: typing.Optional[builtins.str] = None,
        eventhub_endpoint_id: typing.Optional[builtins.str] = None,
        expiration_time_utc: typing.Optional[builtins.str] = None,
        hybrid_connection_endpoint_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        included_event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        retry_policy: typing.Optional[typing.Union["EventgridSystemTopicEventSubscriptionRetryPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        service_bus_queue_endpoint_id: typing.Optional[builtins.str] = None,
        service_bus_topic_endpoint_id: typing.Optional[builtins.str] = None,
        storage_blob_dead_letter_destination: typing.Optional[typing.Union["EventgridSystemTopicEventSubscriptionStorageBlobDeadLetterDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_queue_endpoint: typing.Optional[typing.Union["EventgridSystemTopicEventSubscriptionStorageQueueEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
        subject_filter: typing.Optional[typing.Union["EventgridSystemTopicEventSubscriptionSubjectFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["EventgridSystemTopicEventSubscriptionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        webhook_endpoint: typing.Optional[typing.Union["EventgridSystemTopicEventSubscriptionWebhookEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#name EventgridSystemTopicEventSubscription#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#resource_group_name EventgridSystemTopicEventSubscription#resource_group_name}.
        :param system_topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#system_topic EventgridSystemTopicEventSubscription#system_topic}.
        :param advanced_filter: advanced_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#advanced_filter EventgridSystemTopicEventSubscription#advanced_filter}
        :param advanced_filtering_on_arrays_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#advanced_filtering_on_arrays_enabled EventgridSystemTopicEventSubscription#advanced_filtering_on_arrays_enabled}.
        :param azure_function_endpoint: azure_function_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#azure_function_endpoint EventgridSystemTopicEventSubscription#azure_function_endpoint}
        :param dead_letter_identity: dead_letter_identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#dead_letter_identity EventgridSystemTopicEventSubscription#dead_letter_identity}
        :param delivery_identity: delivery_identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#delivery_identity EventgridSystemTopicEventSubscription#delivery_identity}
        :param delivery_property: delivery_property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#delivery_property EventgridSystemTopicEventSubscription#delivery_property}
        :param event_delivery_schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#event_delivery_schema EventgridSystemTopicEventSubscription#event_delivery_schema}.
        :param eventhub_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#eventhub_endpoint_id EventgridSystemTopicEventSubscription#eventhub_endpoint_id}.
        :param expiration_time_utc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#expiration_time_utc EventgridSystemTopicEventSubscription#expiration_time_utc}.
        :param hybrid_connection_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#hybrid_connection_endpoint_id EventgridSystemTopicEventSubscription#hybrid_connection_endpoint_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#id EventgridSystemTopicEventSubscription#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param included_event_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#included_event_types EventgridSystemTopicEventSubscription#included_event_types}.
        :param labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#labels EventgridSystemTopicEventSubscription#labels}.
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#retry_policy EventgridSystemTopicEventSubscription#retry_policy}
        :param service_bus_queue_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#service_bus_queue_endpoint_id EventgridSystemTopicEventSubscription#service_bus_queue_endpoint_id}.
        :param service_bus_topic_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#service_bus_topic_endpoint_id EventgridSystemTopicEventSubscription#service_bus_topic_endpoint_id}.
        :param storage_blob_dead_letter_destination: storage_blob_dead_letter_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#storage_blob_dead_letter_destination EventgridSystemTopicEventSubscription#storage_blob_dead_letter_destination}
        :param storage_queue_endpoint: storage_queue_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#storage_queue_endpoint EventgridSystemTopicEventSubscription#storage_queue_endpoint}
        :param subject_filter: subject_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#subject_filter EventgridSystemTopicEventSubscription#subject_filter}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#timeouts EventgridSystemTopicEventSubscription#timeouts}
        :param webhook_endpoint: webhook_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#webhook_endpoint EventgridSystemTopicEventSubscription#webhook_endpoint}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(advanced_filter, dict):
            advanced_filter = EventgridSystemTopicEventSubscriptionAdvancedFilter(**advanced_filter)
        if isinstance(azure_function_endpoint, dict):
            azure_function_endpoint = EventgridSystemTopicEventSubscriptionAzureFunctionEndpoint(**azure_function_endpoint)
        if isinstance(dead_letter_identity, dict):
            dead_letter_identity = EventgridSystemTopicEventSubscriptionDeadLetterIdentity(**dead_letter_identity)
        if isinstance(delivery_identity, dict):
            delivery_identity = EventgridSystemTopicEventSubscriptionDeliveryIdentity(**delivery_identity)
        if isinstance(retry_policy, dict):
            retry_policy = EventgridSystemTopicEventSubscriptionRetryPolicy(**retry_policy)
        if isinstance(storage_blob_dead_letter_destination, dict):
            storage_blob_dead_letter_destination = EventgridSystemTopicEventSubscriptionStorageBlobDeadLetterDestination(**storage_blob_dead_letter_destination)
        if isinstance(storage_queue_endpoint, dict):
            storage_queue_endpoint = EventgridSystemTopicEventSubscriptionStorageQueueEndpoint(**storage_queue_endpoint)
        if isinstance(subject_filter, dict):
            subject_filter = EventgridSystemTopicEventSubscriptionSubjectFilter(**subject_filter)
        if isinstance(timeouts, dict):
            timeouts = EventgridSystemTopicEventSubscriptionTimeouts(**timeouts)
        if isinstance(webhook_endpoint, dict):
            webhook_endpoint = EventgridSystemTopicEventSubscriptionWebhookEndpoint(**webhook_endpoint)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5c740739baf128eaff9a416c7a23e3eb57fc0f612b91aebabfa29d59580db55)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument system_topic", value=system_topic, expected_type=type_hints["system_topic"])
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
            "resource_group_name": resource_group_name,
            "system_topic": system_topic,
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#name EventgridSystemTopicEventSubscription#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#resource_group_name EventgridSystemTopicEventSubscription#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def system_topic(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#system_topic EventgridSystemTopicEventSubscription#system_topic}.'''
        result = self._values.get("system_topic")
        assert result is not None, "Required property 'system_topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def advanced_filter(
        self,
    ) -> typing.Optional[EventgridSystemTopicEventSubscriptionAdvancedFilter]:
        '''advanced_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#advanced_filter EventgridSystemTopicEventSubscription#advanced_filter}
        '''
        result = self._values.get("advanced_filter")
        return typing.cast(typing.Optional[EventgridSystemTopicEventSubscriptionAdvancedFilter], result)

    @builtins.property
    def advanced_filtering_on_arrays_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#advanced_filtering_on_arrays_enabled EventgridSystemTopicEventSubscription#advanced_filtering_on_arrays_enabled}.'''
        result = self._values.get("advanced_filtering_on_arrays_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def azure_function_endpoint(
        self,
    ) -> typing.Optional[EventgridSystemTopicEventSubscriptionAzureFunctionEndpoint]:
        '''azure_function_endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#azure_function_endpoint EventgridSystemTopicEventSubscription#azure_function_endpoint}
        '''
        result = self._values.get("azure_function_endpoint")
        return typing.cast(typing.Optional[EventgridSystemTopicEventSubscriptionAzureFunctionEndpoint], result)

    @builtins.property
    def dead_letter_identity(
        self,
    ) -> typing.Optional["EventgridSystemTopicEventSubscriptionDeadLetterIdentity"]:
        '''dead_letter_identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#dead_letter_identity EventgridSystemTopicEventSubscription#dead_letter_identity}
        '''
        result = self._values.get("dead_letter_identity")
        return typing.cast(typing.Optional["EventgridSystemTopicEventSubscriptionDeadLetterIdentity"], result)

    @builtins.property
    def delivery_identity(
        self,
    ) -> typing.Optional["EventgridSystemTopicEventSubscriptionDeliveryIdentity"]:
        '''delivery_identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#delivery_identity EventgridSystemTopicEventSubscription#delivery_identity}
        '''
        result = self._values.get("delivery_identity")
        return typing.cast(typing.Optional["EventgridSystemTopicEventSubscriptionDeliveryIdentity"], result)

    @builtins.property
    def delivery_property(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionDeliveryProperty"]]]:
        '''delivery_property block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#delivery_property EventgridSystemTopicEventSubscription#delivery_property}
        '''
        result = self._values.get("delivery_property")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventgridSystemTopicEventSubscriptionDeliveryProperty"]]], result)

    @builtins.property
    def event_delivery_schema(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#event_delivery_schema EventgridSystemTopicEventSubscription#event_delivery_schema}.'''
        result = self._values.get("event_delivery_schema")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eventhub_endpoint_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#eventhub_endpoint_id EventgridSystemTopicEventSubscription#eventhub_endpoint_id}.'''
        result = self._values.get("eventhub_endpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expiration_time_utc(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#expiration_time_utc EventgridSystemTopicEventSubscription#expiration_time_utc}.'''
        result = self._values.get("expiration_time_utc")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hybrid_connection_endpoint_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#hybrid_connection_endpoint_id EventgridSystemTopicEventSubscription#hybrid_connection_endpoint_id}.'''
        result = self._values.get("hybrid_connection_endpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#id EventgridSystemTopicEventSubscription#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def included_event_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#included_event_types EventgridSystemTopicEventSubscription#included_event_types}.'''
        result = self._values.get("included_event_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#labels EventgridSystemTopicEventSubscription#labels}.'''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def retry_policy(
        self,
    ) -> typing.Optional["EventgridSystemTopicEventSubscriptionRetryPolicy"]:
        '''retry_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#retry_policy EventgridSystemTopicEventSubscription#retry_policy}
        '''
        result = self._values.get("retry_policy")
        return typing.cast(typing.Optional["EventgridSystemTopicEventSubscriptionRetryPolicy"], result)

    @builtins.property
    def service_bus_queue_endpoint_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#service_bus_queue_endpoint_id EventgridSystemTopicEventSubscription#service_bus_queue_endpoint_id}.'''
        result = self._values.get("service_bus_queue_endpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_bus_topic_endpoint_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#service_bus_topic_endpoint_id EventgridSystemTopicEventSubscription#service_bus_topic_endpoint_id}.'''
        result = self._values.get("service_bus_topic_endpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_blob_dead_letter_destination(
        self,
    ) -> typing.Optional["EventgridSystemTopicEventSubscriptionStorageBlobDeadLetterDestination"]:
        '''storage_blob_dead_letter_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#storage_blob_dead_letter_destination EventgridSystemTopicEventSubscription#storage_blob_dead_letter_destination}
        '''
        result = self._values.get("storage_blob_dead_letter_destination")
        return typing.cast(typing.Optional["EventgridSystemTopicEventSubscriptionStorageBlobDeadLetterDestination"], result)

    @builtins.property
    def storage_queue_endpoint(
        self,
    ) -> typing.Optional["EventgridSystemTopicEventSubscriptionStorageQueueEndpoint"]:
        '''storage_queue_endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#storage_queue_endpoint EventgridSystemTopicEventSubscription#storage_queue_endpoint}
        '''
        result = self._values.get("storage_queue_endpoint")
        return typing.cast(typing.Optional["EventgridSystemTopicEventSubscriptionStorageQueueEndpoint"], result)

    @builtins.property
    def subject_filter(
        self,
    ) -> typing.Optional["EventgridSystemTopicEventSubscriptionSubjectFilter"]:
        '''subject_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#subject_filter EventgridSystemTopicEventSubscription#subject_filter}
        '''
        result = self._values.get("subject_filter")
        return typing.cast(typing.Optional["EventgridSystemTopicEventSubscriptionSubjectFilter"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["EventgridSystemTopicEventSubscriptionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#timeouts EventgridSystemTopicEventSubscription#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["EventgridSystemTopicEventSubscriptionTimeouts"], result)

    @builtins.property
    def webhook_endpoint(
        self,
    ) -> typing.Optional["EventgridSystemTopicEventSubscriptionWebhookEndpoint"]:
        '''webhook_endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#webhook_endpoint EventgridSystemTopicEventSubscription#webhook_endpoint}
        '''
        result = self._values.get("webhook_endpoint")
        return typing.cast(typing.Optional["EventgridSystemTopicEventSubscriptionWebhookEndpoint"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionDeadLetterIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "user_assigned_identity": "userAssignedIdentity"},
)
class EventgridSystemTopicEventSubscriptionDeadLetterIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        user_assigned_identity: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#type EventgridSystemTopicEventSubscription#type}.
        :param user_assigned_identity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#user_assigned_identity EventgridSystemTopicEventSubscription#user_assigned_identity}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d06371d41b0699c64aff84d52f099c3dc3b3ec3491d439549f47bddde924962)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument user_assigned_identity", value=user_assigned_identity, expected_type=type_hints["user_assigned_identity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if user_assigned_identity is not None:
            self._values["user_assigned_identity"] = user_assigned_identity

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#type EventgridSystemTopicEventSubscription#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_assigned_identity(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#user_assigned_identity EventgridSystemTopicEventSubscription#user_assigned_identity}.'''
        result = self._values.get("user_assigned_identity")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionDeadLetterIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionDeadLetterIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionDeadLetterIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e82a14a1a7f4f4fbef1b2746478a0c2a63562f0bb78fd90392bc3092b3da9e9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c1fd547e5dfbf11b4f13cdc909fa5b0398a25d09079463f41019a7d086081c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentity")
    def user_assigned_identity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAssignedIdentity"))

    @user_assigned_identity.setter
    def user_assigned_identity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bac3221e03b89e40b20eff48f2787810a89f7febe16827e40ce32a2f2d48e4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAssignedIdentity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventgridSystemTopicEventSubscriptionDeadLetterIdentity]:
        return typing.cast(typing.Optional[EventgridSystemTopicEventSubscriptionDeadLetterIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventgridSystemTopicEventSubscriptionDeadLetterIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2f8b3d1ad39307fa1877fed3ef7278e3ebdbede904077260d045170c81e6eca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionDeliveryIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "user_assigned_identity": "userAssignedIdentity"},
)
class EventgridSystemTopicEventSubscriptionDeliveryIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        user_assigned_identity: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#type EventgridSystemTopicEventSubscription#type}.
        :param user_assigned_identity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#user_assigned_identity EventgridSystemTopicEventSubscription#user_assigned_identity}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3a47045fe8f4e82be426f8c341c41dedcbf53558cfcabb36a9092d363b63a52)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument user_assigned_identity", value=user_assigned_identity, expected_type=type_hints["user_assigned_identity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if user_assigned_identity is not None:
            self._values["user_assigned_identity"] = user_assigned_identity

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#type EventgridSystemTopicEventSubscription#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_assigned_identity(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#user_assigned_identity EventgridSystemTopicEventSubscription#user_assigned_identity}.'''
        result = self._values.get("user_assigned_identity")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionDeliveryIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionDeliveryIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionDeliveryIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3242437936873ebba0258bb9caf97e6ff63e7eae9a3d1bc24999dc4290678892)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30e977710d69715de75ee4ed2405d33fb00744c1e7897d029a23b053aea18682)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentity")
    def user_assigned_identity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAssignedIdentity"))

    @user_assigned_identity.setter
    def user_assigned_identity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__532131c3b8d7921763abf4b0b5337d360b1481a64da5f094705e88f461fed1b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAssignedIdentity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventgridSystemTopicEventSubscriptionDeliveryIdentity]:
        return typing.cast(typing.Optional[EventgridSystemTopicEventSubscriptionDeliveryIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventgridSystemTopicEventSubscriptionDeliveryIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f7b5962a45a0adf0c6dc2dac8681c5840f59ae715e0b100de2a1802ffa45a7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionDeliveryProperty",
    jsii_struct_bases=[],
    name_mapping={
        "header_name": "headerName",
        "type": "type",
        "secret": "secret",
        "source_field": "sourceField",
        "value": "value",
    },
)
class EventgridSystemTopicEventSubscriptionDeliveryProperty:
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
        :param header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#header_name EventgridSystemTopicEventSubscription#header_name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#type EventgridSystemTopicEventSubscription#type}.
        :param secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#secret EventgridSystemTopicEventSubscription#secret}.
        :param source_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#source_field EventgridSystemTopicEventSubscription#source_field}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#value EventgridSystemTopicEventSubscription#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4157dcf76b500d7618db2908dc5fd80fbeb2e6459c834621024e7014a448f9d9)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#header_name EventgridSystemTopicEventSubscription#header_name}.'''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#type EventgridSystemTopicEventSubscription#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#secret EventgridSystemTopicEventSubscription#secret}.'''
        result = self._values.get("secret")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def source_field(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#source_field EventgridSystemTopicEventSubscription#source_field}.'''
        result = self._values.get("source_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#value EventgridSystemTopicEventSubscription#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionDeliveryProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionDeliveryPropertyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionDeliveryPropertyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a64644e47e8a3bdb4e9daefa59e3d0615c95166631b6bf8fd7100cafa13cfdcf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventgridSystemTopicEventSubscriptionDeliveryPropertyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ee96028c8147ae49ab661e9a487aa6ba1782a1a399b57ab7a01dd88bcb786bc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventgridSystemTopicEventSubscriptionDeliveryPropertyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2dfae8f73304a5ff031235083e1b6611bebca1143249cc94764423248759caa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__295487e28920e0ff8fa7093ab6059db81718181a0f17c776d06080b70fa046f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66c2d55a52024237fe94c7a72b5ebcdccf0922edfad749e239b0faeea9b033ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionDeliveryProperty]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionDeliveryProperty]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionDeliveryProperty]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7008d9a5192d48f04b096dbb653e890a4c9f41d2920f71ff43996eff3166af4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventgridSystemTopicEventSubscriptionDeliveryPropertyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionDeliveryPropertyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__593e42b9e5319f7bf05cf56803b5e32f1ca05fa0ddc53e55ba824e196a7f7553)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c5767220c7e379660b7f52495c673a37cbc8848c15c5b70cebd4c20973e29e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4843945f5c039cc94d89628c7bed69adc2ab304bae29c6adcc641a6924e0ac04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceField")
    def source_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceField"))

    @source_field.setter
    def source_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a56326d5807478ccefb2d02fe55cd7b11a401a79c82adfabf420425e78ba77f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6570b34d51a18a9484a339f0d40f0e8d3be128e748d9cfa5bad23c19e9cf6971)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f56351b6a10f017e7274437ba19b9e9e30cbf425dd1008d008575933bb01dea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionDeliveryProperty]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionDeliveryProperty]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionDeliveryProperty]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d176acd1b5f649f281fede5798012eef3ff61be385da95f9961453b2cfe7853)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionRetryPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "event_time_to_live": "eventTimeToLive",
        "max_delivery_attempts": "maxDeliveryAttempts",
    },
)
class EventgridSystemTopicEventSubscriptionRetryPolicy:
    def __init__(
        self,
        *,
        event_time_to_live: jsii.Number,
        max_delivery_attempts: jsii.Number,
    ) -> None:
        '''
        :param event_time_to_live: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#event_time_to_live EventgridSystemTopicEventSubscription#event_time_to_live}.
        :param max_delivery_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#max_delivery_attempts EventgridSystemTopicEventSubscription#max_delivery_attempts}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c3b86828fd82ff4c3e8643c0043e1395a49bd5a2a198385837f78d511ab741)
            check_type(argname="argument event_time_to_live", value=event_time_to_live, expected_type=type_hints["event_time_to_live"])
            check_type(argname="argument max_delivery_attempts", value=max_delivery_attempts, expected_type=type_hints["max_delivery_attempts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_time_to_live": event_time_to_live,
            "max_delivery_attempts": max_delivery_attempts,
        }

    @builtins.property
    def event_time_to_live(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#event_time_to_live EventgridSystemTopicEventSubscription#event_time_to_live}.'''
        result = self._values.get("event_time_to_live")
        assert result is not None, "Required property 'event_time_to_live' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def max_delivery_attempts(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#max_delivery_attempts EventgridSystemTopicEventSubscription#max_delivery_attempts}.'''
        result = self._values.get("max_delivery_attempts")
        assert result is not None, "Required property 'max_delivery_attempts' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionRetryPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionRetryPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionRetryPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cadce26e4145057b35fffc7c6d54132a702f01f0b5f10b7df0122ec11c8e0a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cad76cb1d84180baf1e95759fc4eadddb92b45ebb690d3e69e9d213765077462)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventTimeToLive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDeliveryAttempts")
    def max_delivery_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDeliveryAttempts"))

    @max_delivery_attempts.setter
    def max_delivery_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f249b6177a81fe65bd01883ea8fa199bf6b394ea68251130411e84bbed4a5a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDeliveryAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventgridSystemTopicEventSubscriptionRetryPolicy]:
        return typing.cast(typing.Optional[EventgridSystemTopicEventSubscriptionRetryPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventgridSystemTopicEventSubscriptionRetryPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c07fa2b9663a22fbcfb277a980173651c6de1edb772278ca9c62e314f1b4890)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionStorageBlobDeadLetterDestination",
    jsii_struct_bases=[],
    name_mapping={
        "storage_account_id": "storageAccountId",
        "storage_blob_container_name": "storageBlobContainerName",
    },
)
class EventgridSystemTopicEventSubscriptionStorageBlobDeadLetterDestination:
    def __init__(
        self,
        *,
        storage_account_id: builtins.str,
        storage_blob_container_name: builtins.str,
    ) -> None:
        '''
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#storage_account_id EventgridSystemTopicEventSubscription#storage_account_id}.
        :param storage_blob_container_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#storage_blob_container_name EventgridSystemTopicEventSubscription#storage_blob_container_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2cec756508e7ba546bd05c2d300603eb12b744dfc8d4b2906e8c955d2402320)
            check_type(argname="argument storage_account_id", value=storage_account_id, expected_type=type_hints["storage_account_id"])
            check_type(argname="argument storage_blob_container_name", value=storage_blob_container_name, expected_type=type_hints["storage_blob_container_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "storage_account_id": storage_account_id,
            "storage_blob_container_name": storage_blob_container_name,
        }

    @builtins.property
    def storage_account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#storage_account_id EventgridSystemTopicEventSubscription#storage_account_id}.'''
        result = self._values.get("storage_account_id")
        assert result is not None, "Required property 'storage_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_blob_container_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#storage_blob_container_name EventgridSystemTopicEventSubscription#storage_blob_container_name}.'''
        result = self._values.get("storage_blob_container_name")
        assert result is not None, "Required property 'storage_blob_container_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionStorageBlobDeadLetterDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionStorageBlobDeadLetterDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionStorageBlobDeadLetterDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2b95b42686e25b22e502774c48a2f47a48ded23dd78884a44ba477869f79312)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e63778e7acb8de96c31e10013b8e03dc7daf7c9d3a25a4bcc0e3417c8d609757)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageBlobContainerName")
    def storage_blob_container_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageBlobContainerName"))

    @storage_blob_container_name.setter
    def storage_blob_container_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88d620a6c162fdc76455182306608136c3634588a129ceb19c90be54102688fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageBlobContainerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventgridSystemTopicEventSubscriptionStorageBlobDeadLetterDestination]:
        return typing.cast(typing.Optional[EventgridSystemTopicEventSubscriptionStorageBlobDeadLetterDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventgridSystemTopicEventSubscriptionStorageBlobDeadLetterDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c85dfafee7623e51140acdbc9add53facd3241cfbe47cf6782cda2861706e759)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionStorageQueueEndpoint",
    jsii_struct_bases=[],
    name_mapping={
        "queue_name": "queueName",
        "storage_account_id": "storageAccountId",
        "queue_message_time_to_live_in_seconds": "queueMessageTimeToLiveInSeconds",
    },
)
class EventgridSystemTopicEventSubscriptionStorageQueueEndpoint:
    def __init__(
        self,
        *,
        queue_name: builtins.str,
        storage_account_id: builtins.str,
        queue_message_time_to_live_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param queue_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#queue_name EventgridSystemTopicEventSubscription#queue_name}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#storage_account_id EventgridSystemTopicEventSubscription#storage_account_id}.
        :param queue_message_time_to_live_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#queue_message_time_to_live_in_seconds EventgridSystemTopicEventSubscription#queue_message_time_to_live_in_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfc6cc376ee4925d0ed63fa388d2ffe375c2dffc0672d56d48db8826bf418517)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#queue_name EventgridSystemTopicEventSubscription#queue_name}.'''
        result = self._values.get("queue_name")
        assert result is not None, "Required property 'queue_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#storage_account_id EventgridSystemTopicEventSubscription#storage_account_id}.'''
        result = self._values.get("storage_account_id")
        assert result is not None, "Required property 'storage_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def queue_message_time_to_live_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#queue_message_time_to_live_in_seconds EventgridSystemTopicEventSubscription#queue_message_time_to_live_in_seconds}.'''
        result = self._values.get("queue_message_time_to_live_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionStorageQueueEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionStorageQueueEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionStorageQueueEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe66cdee71ee32c75365c43bd96719feb969968bb766c53b80216198bc1963d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__822c560fd5dcded3754e71a40b942b87278706beb7dbc75df6be90568cfcafce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueMessageTimeToLiveInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queueName"))

    @queue_name.setter
    def queue_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fa22dfd3bb2372183b0fffe74264373b8135b7d6c7c522b69feca2e41e58fe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountId")
    def storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountId"))

    @storage_account_id.setter
    def storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__902beb152bbb293ee74e1f56491678bf855f9762c8c116007f3fb25b0417827d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventgridSystemTopicEventSubscriptionStorageQueueEndpoint]:
        return typing.cast(typing.Optional[EventgridSystemTopicEventSubscriptionStorageQueueEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventgridSystemTopicEventSubscriptionStorageQueueEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aa016321dacba5a2ed6a215d5bf670442d165f62fc09215754301fb7b8adee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionSubjectFilter",
    jsii_struct_bases=[],
    name_mapping={
        "case_sensitive": "caseSensitive",
        "subject_begins_with": "subjectBeginsWith",
        "subject_ends_with": "subjectEndsWith",
    },
)
class EventgridSystemTopicEventSubscriptionSubjectFilter:
    def __init__(
        self,
        *,
        case_sensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subject_begins_with: typing.Optional[builtins.str] = None,
        subject_ends_with: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param case_sensitive: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#case_sensitive EventgridSystemTopicEventSubscription#case_sensitive}.
        :param subject_begins_with: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#subject_begins_with EventgridSystemTopicEventSubscription#subject_begins_with}.
        :param subject_ends_with: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#subject_ends_with EventgridSystemTopicEventSubscription#subject_ends_with}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99ad77a46fa6e4e3911002a9c330779e249a05d42326d144167d7f3b0aa44fc3)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#case_sensitive EventgridSystemTopicEventSubscription#case_sensitive}.'''
        result = self._values.get("case_sensitive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def subject_begins_with(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#subject_begins_with EventgridSystemTopicEventSubscription#subject_begins_with}.'''
        result = self._values.get("subject_begins_with")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_ends_with(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#subject_ends_with EventgridSystemTopicEventSubscription#subject_ends_with}.'''
        result = self._values.get("subject_ends_with")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionSubjectFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionSubjectFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionSubjectFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5412b9206cd8622611fcdbee4e0b06d97a830ae5bc8e662b748641ec65b3177)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3944b089a13d7ab9878683f8afb5a05ddbd6856739f44daa4461260341fc043a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caseSensitive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subjectBeginsWith")
    def subject_begins_with(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectBeginsWith"))

    @subject_begins_with.setter
    def subject_begins_with(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54c76db048d3cb350522b5fb9aba2406e1166b393e9719a5bbe455e595ec37d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectBeginsWith", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subjectEndsWith")
    def subject_ends_with(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectEndsWith"))

    @subject_ends_with.setter
    def subject_ends_with(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a277a173a2165f463488ba70404cbdba7119815897133ce65d7a178265af317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectEndsWith", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventgridSystemTopicEventSubscriptionSubjectFilter]:
        return typing.cast(typing.Optional[EventgridSystemTopicEventSubscriptionSubjectFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventgridSystemTopicEventSubscriptionSubjectFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4a617ef1f29f76f344070283dba813c450ebb84befda02326ab45fb02541bb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class EventgridSystemTopicEventSubscriptionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#create EventgridSystemTopicEventSubscription#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#delete EventgridSystemTopicEventSubscription#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#read EventgridSystemTopicEventSubscription#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#update EventgridSystemTopicEventSubscription#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c30c474881e22e16821324cfbe46cb122f37ecf0b3183637d535ad29017e46d5)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#create EventgridSystemTopicEventSubscription#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#delete EventgridSystemTopicEventSubscription#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#read EventgridSystemTopicEventSubscription#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#update EventgridSystemTopicEventSubscription#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd620df7c0ceaf20aa9c31c8eb7d68e8be1f5d6ca1d2894774818a4b5c5f545c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f6474e999fd9faf8c889a59265a1b5a5e5244d0980aee05e4207e7fcaed7d60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0064eec71d8bb533777bef1841600c0474fd8a4c5145633ec71c930246f09887)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__714ee24c38be09ede23de912d842caaca4dc29986c202d77124982c492785c1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc81df98951c9647c0dd74a991dcb5623e9f9b8d2b7a9ab336aefc3b4288352)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e5d8edf4b2455e91fb3dba66ea91d8717fa8f4bb9a48645eeeac2cac7d7c669)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionWebhookEndpoint",
    jsii_struct_bases=[],
    name_mapping={
        "url": "url",
        "active_directory_app_id_or_uri": "activeDirectoryAppIdOrUri",
        "active_directory_tenant_id": "activeDirectoryTenantId",
        "max_events_per_batch": "maxEventsPerBatch",
        "preferred_batch_size_in_kilobytes": "preferredBatchSizeInKilobytes",
    },
)
class EventgridSystemTopicEventSubscriptionWebhookEndpoint:
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
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#url EventgridSystemTopicEventSubscription#url}.
        :param active_directory_app_id_or_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#active_directory_app_id_or_uri EventgridSystemTopicEventSubscription#active_directory_app_id_or_uri}.
        :param active_directory_tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#active_directory_tenant_id EventgridSystemTopicEventSubscription#active_directory_tenant_id}.
        :param max_events_per_batch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#max_events_per_batch EventgridSystemTopicEventSubscription#max_events_per_batch}.
        :param preferred_batch_size_in_kilobytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#preferred_batch_size_in_kilobytes EventgridSystemTopicEventSubscription#preferred_batch_size_in_kilobytes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddd4f17eee7c5c5075345702f2e2955d57ab198b3fc03f033cf76a5db9bfcc34)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#url EventgridSystemTopicEventSubscription#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def active_directory_app_id_or_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#active_directory_app_id_or_uri EventgridSystemTopicEventSubscription#active_directory_app_id_or_uri}.'''
        result = self._values.get("active_directory_app_id_or_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def active_directory_tenant_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#active_directory_tenant_id EventgridSystemTopicEventSubscription#active_directory_tenant_id}.'''
        result = self._values.get("active_directory_tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_events_per_batch(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#max_events_per_batch EventgridSystemTopicEventSubscription#max_events_per_batch}.'''
        result = self._values.get("max_events_per_batch")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preferred_batch_size_in_kilobytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/eventgrid_system_topic_event_subscription#preferred_batch_size_in_kilobytes EventgridSystemTopicEventSubscription#preferred_batch_size_in_kilobytes}.'''
        result = self._values.get("preferred_batch_size_in_kilobytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventgridSystemTopicEventSubscriptionWebhookEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventgridSystemTopicEventSubscriptionWebhookEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.eventgridSystemTopicEventSubscription.EventgridSystemTopicEventSubscriptionWebhookEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__988e3123005334c2f7fffd576ee73313606ce39184ebc2e3aaef45b0f1c58568)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a370a8b37e8d37ecd807b28552fb145e4d411023ef7aea194cada4497df9e3f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activeDirectoryAppIdOrUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryTenantId")
    def active_directory_tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "activeDirectoryTenantId"))

    @active_directory_tenant_id.setter
    def active_directory_tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fae208efea6c28e2d292815d589d4cb85b972bb16b7a18448f3ad925dac1f48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activeDirectoryTenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxEventsPerBatch")
    def max_events_per_batch(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxEventsPerBatch"))

    @max_events_per_batch.setter
    def max_events_per_batch(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce3d9a501708945240b43c6ca2c2ea8c335c2f661f3753ed0d02eceb05664304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxEventsPerBatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preferredBatchSizeInKilobytes")
    def preferred_batch_size_in_kilobytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "preferredBatchSizeInKilobytes"))

    @preferred_batch_size_in_kilobytes.setter
    def preferred_batch_size_in_kilobytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a766c332b5f3c74120548eabb5c734467545fd675786f9ea80b6bf318e8a7770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredBatchSizeInKilobytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__230689708a52947bdd439ccdb9e8c322c8b026bc8d8d23a153caaa9a5bac420a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventgridSystemTopicEventSubscriptionWebhookEndpoint]:
        return typing.cast(typing.Optional[EventgridSystemTopicEventSubscriptionWebhookEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventgridSystemTopicEventSubscriptionWebhookEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__893b6ed9cdb6943abcbfd5e1c6fc7c1a2f0943de221da09092e4910e6a58d270)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "EventgridSystemTopicEventSubscription",
    "EventgridSystemTopicEventSubscriptionAdvancedFilter",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEquals",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEqualsList",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEqualsOutputReference",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNull",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNullList",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNullOutputReference",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefined",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefinedList",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefinedOutputReference",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThan",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanList",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEqualsList",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEqualsOutputReference",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOutputReference",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberIn",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInList",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInOutputReference",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRange",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRangeList",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRangeOutputReference",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThan",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanList",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEquals",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEqualsList",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEqualsOutputReference",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOutputReference",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotIn",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInList",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInOutputReference",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRange",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRangeList",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRangeOutputReference",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterOutputReference",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWith",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWithList",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWithOutputReference",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringContains",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringContainsList",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringContainsOutputReference",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWith",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWithList",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWithOutputReference",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringIn",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringInList",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringInOutputReference",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWith",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWithList",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWithOutputReference",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContains",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContainsList",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContainsOutputReference",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWith",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWithList",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWithOutputReference",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotIn",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotInList",
    "EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotInOutputReference",
    "EventgridSystemTopicEventSubscriptionAzureFunctionEndpoint",
    "EventgridSystemTopicEventSubscriptionAzureFunctionEndpointOutputReference",
    "EventgridSystemTopicEventSubscriptionConfig",
    "EventgridSystemTopicEventSubscriptionDeadLetterIdentity",
    "EventgridSystemTopicEventSubscriptionDeadLetterIdentityOutputReference",
    "EventgridSystemTopicEventSubscriptionDeliveryIdentity",
    "EventgridSystemTopicEventSubscriptionDeliveryIdentityOutputReference",
    "EventgridSystemTopicEventSubscriptionDeliveryProperty",
    "EventgridSystemTopicEventSubscriptionDeliveryPropertyList",
    "EventgridSystemTopicEventSubscriptionDeliveryPropertyOutputReference",
    "EventgridSystemTopicEventSubscriptionRetryPolicy",
    "EventgridSystemTopicEventSubscriptionRetryPolicyOutputReference",
    "EventgridSystemTopicEventSubscriptionStorageBlobDeadLetterDestination",
    "EventgridSystemTopicEventSubscriptionStorageBlobDeadLetterDestinationOutputReference",
    "EventgridSystemTopicEventSubscriptionStorageQueueEndpoint",
    "EventgridSystemTopicEventSubscriptionStorageQueueEndpointOutputReference",
    "EventgridSystemTopicEventSubscriptionSubjectFilter",
    "EventgridSystemTopicEventSubscriptionSubjectFilterOutputReference",
    "EventgridSystemTopicEventSubscriptionTimeouts",
    "EventgridSystemTopicEventSubscriptionTimeoutsOutputReference",
    "EventgridSystemTopicEventSubscriptionWebhookEndpoint",
    "EventgridSystemTopicEventSubscriptionWebhookEndpointOutputReference",
]

publication.publish()

def _typecheckingstub__6e6ffabd576d2ded52f9219fdef6e3ca88e08e3386546bcef81696eae047cc13(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    resource_group_name: builtins.str,
    system_topic: builtins.str,
    advanced_filter: typing.Optional[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    advanced_filtering_on_arrays_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    azure_function_endpoint: typing.Optional[typing.Union[EventgridSystemTopicEventSubscriptionAzureFunctionEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
    dead_letter_identity: typing.Optional[typing.Union[EventgridSystemTopicEventSubscriptionDeadLetterIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    delivery_identity: typing.Optional[typing.Union[EventgridSystemTopicEventSubscriptionDeliveryIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    delivery_property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionDeliveryProperty, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_delivery_schema: typing.Optional[builtins.str] = None,
    eventhub_endpoint_id: typing.Optional[builtins.str] = None,
    expiration_time_utc: typing.Optional[builtins.str] = None,
    hybrid_connection_endpoint_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    included_event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    retry_policy: typing.Optional[typing.Union[EventgridSystemTopicEventSubscriptionRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    service_bus_queue_endpoint_id: typing.Optional[builtins.str] = None,
    service_bus_topic_endpoint_id: typing.Optional[builtins.str] = None,
    storage_blob_dead_letter_destination: typing.Optional[typing.Union[EventgridSystemTopicEventSubscriptionStorageBlobDeadLetterDestination, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_queue_endpoint: typing.Optional[typing.Union[EventgridSystemTopicEventSubscriptionStorageQueueEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
    subject_filter: typing.Optional[typing.Union[EventgridSystemTopicEventSubscriptionSubjectFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[EventgridSystemTopicEventSubscriptionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    webhook_endpoint: typing.Optional[typing.Union[EventgridSystemTopicEventSubscriptionWebhookEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3c60643124b3510a8899a2fce8d27c03135ec136c2b893196c717e5bb13ea2ae(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0608e1a2c9de636a7c03ad6766166c4701f6051d32e808cd0a332b1d30062b3a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionDeliveryProperty, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b95b01e5097d8a6eda30534043e3bf5a2586227cd207db114ab56c3cb7e67092(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2925dd135350c06531f75656e2a34d8140637b53ef1ca768ef558733b89b887(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35e611da522d2485b349eba2c1038c7e5ae7c1089da3f3ca61ed32d3645bde24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb0a29736eb41e9cf05b386c0ae6624d4fd2c13902e980b5eab87a2a786cc86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c391451d291cae233a1e86765d5a8544b9f234e6970321ba1194f16c312d54c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29435038a527fb3d696905e8bf00835a563ac3eb33bd4c82841febba7aade637(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09fef22854a19ecf4771887d003643a2dc28b1c2c87230c6c2a82556fe4cc766(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e47c59e3b7f95ea959f5d7738ded82e371beca65b6d686d53b20d6a6bca40ce(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80ed412d549f086055a2f13066c4e651a3c2d5cc208be75f3bf1a511d5091426(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ba02be5ae428911cb4d7acf7661bb5b3cf5bbf3d48bd8972e108f473a295bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__012d97c3b6bc8a5109e6964f8b9275a51b5548a6319f183f6d4659e2ed23eced(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86a41048d1503555d3eae5c7d966617c5e119b0a8a1fd4717b736e44774ca4e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3329bc4ad695ae108366649b44a3c7b0180b262bf45885bf211051193771fadd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f91dd6616109a0cf828cd71946693f50c986d00ae0fd8261ebe304350f8927ae(
    *,
    bool_equals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEquals, typing.Dict[builtins.str, typing.Any]]]]] = None,
    is_not_null: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNull, typing.Dict[builtins.str, typing.Any]]]]] = None,
    is_null_or_undefined: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefined, typing.Dict[builtins.str, typing.Any]]]]] = None,
    number_greater_than: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThan, typing.Dict[builtins.str, typing.Any]]]]] = None,
    number_greater_than_or_equals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals, typing.Dict[builtins.str, typing.Any]]]]] = None,
    number_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberIn, typing.Dict[builtins.str, typing.Any]]]]] = None,
    number_in_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
    number_less_than: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThan, typing.Dict[builtins.str, typing.Any]]]]] = None,
    number_less_than_or_equals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEquals, typing.Dict[builtins.str, typing.Any]]]]] = None,
    number_not_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotIn, typing.Dict[builtins.str, typing.Any]]]]] = None,
    number_not_in_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
    string_begins_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWith, typing.Dict[builtins.str, typing.Any]]]]] = None,
    string_contains: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterStringContains, typing.Dict[builtins.str, typing.Any]]]]] = None,
    string_ends_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWith, typing.Dict[builtins.str, typing.Any]]]]] = None,
    string_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterStringIn, typing.Dict[builtins.str, typing.Any]]]]] = None,
    string_not_begins_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWith, typing.Dict[builtins.str, typing.Any]]]]] = None,
    string_not_contains: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContains, typing.Dict[builtins.str, typing.Any]]]]] = None,
    string_not_ends_with: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWith, typing.Dict[builtins.str, typing.Any]]]]] = None,
    string_not_in: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotIn, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__266f4c19761e471cb6fb499a82f02b44c03d26c1910a43c54a2727d339565e93(
    *,
    key: builtins.str,
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fedb9198c21a1758f9d2de2d1da4b09caf2b76650691ac38afefe6cb4e98dad1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caaabc0f679a876a26dc30281066d676ddf5cbddeba6b65858e069590746eb02(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d5ff7198c72346e5593c73328a12de328c11e51330b3e46f93c1672e06131fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e615d57e0d025bb60121cc06f9524b0ccc7fd399039da2f5ad2f9f680e6c33f1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe660966c2402c7561c34bbfb789a5c10b614401524529715e780952804e3edd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c478452c5725b4973ac80d3b3d334da235f88719fd728e5f95363363acdcf0c6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEquals]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd0c44deb22f84e6a049f351175a3237d8667f08bbc11e067c997792b2a4e57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__430594b669800584d695e001b2e6fe8d5f4c8ec96c730e1d8afe531ff7f4e5e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb8dc7835044cb6e3ec8ddf100ab9f48113dead04edc517087d16d0b5073fcf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ece7d849f1838417c100868277aa398764df046e2e479ce95a992467fd05d5b8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEquals]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f83e93d6af701c72a779d4f25b8f9c31b40778366b3888ece6e39a68c1269e64(
    *,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__379c8a84bdaafd78c19e7dd7dba5d9744654a0a390a0c056718c439287be19b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aebf937cac743193af3a11ce47191ba5e806243c9c549d0d94820f1170d3ae3f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baba89ecedd9b6cdbb2a69d4531d301ff6126d09a87584d0a5b1c7182285cb2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d01edae4bd6046578d0a9f80a2a8212827bdd770b1a5e0d2e6d10c1f2c4392c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e55601992c5e4bfb43501475817bd0bb0ea44fcc9da1bf9873e7b049c7152c4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3a90c42845743a628add08c2fc623952d23279597ebcc0699bd43b1ca40e52(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNull]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b4270af462eae91e86ffb1aabd417b29a16a5eb9fec11fe3b4e4e5f4c6dda33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c903d85b8c583eba849aa02fd389efb7a672f412adbf1241b270b83a9e788e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f61dc9e989b08ab1fefe2f12c6f876aa2549abc2b7ee05b55d9de8b5cd6bd3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNull]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0588f6527f9ad0206c0c608d7d184d90189efca9d8f5519c6913ac7b60eb4797(
    *,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__584ee6e4b2ce979c285c991d906d1ce6fbb17c54ade6fede696337c0a988963b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c876b8a5486c2cd3a4f80b051336c0dc4c21a069d6b66066d3f217aa21b46a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa260bec788588c2aefba2ae796b84d339ccd1bf9d27150b1aa42a93c0f0d36b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0b60fea2a5d4e269919eecb45f0673d1c60359404c6940e196722021e192b76(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6cc9e7a313d135a00a78a88751202a7d51ff0b133aff726ab886d713d3ffd7e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab7cf73351111658a7ce51bf9e7b14e012146bd4e376d65af87614a4944f7cd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefined]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32c377833305e992947e0b60ed67b1c3f55cb1d6de5650f55cb94e3563b20cbf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00211dbce8ef492c9e4af97f7ff175552fe120f328d0aab5251ac48402e4b2d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__504cd8cfe1ef60df4b9eecace9c309765850edb73f918ef8da67c0f7aeea7538(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefined]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__212dc7ec49ab32047b94d1b1bd5b0c28ac469211866a76f527cd1894a1b04c56(
    *,
    key: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8744cc1cc1bb43411ff3978519e9e9da98ba446e84f61d42149bffbe5941cdb0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6ed3ff19082e00be4d91fb4d4d3180eb256a9ce88a8370c83cb1338c572949(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87fa37ccc4bd4f091254cdf507126a0212198e847c52bc207338f77e20ea70a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c6d9ab63bb8b920f89efdf3426cbc75ece82cd3208be6352e8d81e90df3a06f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ee6b8be9af8aca81b746774b5e923e7843aa8ed81082e7d29d46ac5dfe1767(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363597ebd4d1a523055c5dbe4c9571678d6db4eb3fe528bfb601acecb6915e97(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThan]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53d8e9f3fb6f3fd59859fdd008493961f17c4c9b4388eb621955116da9fd893b(
    *,
    key: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee39d11d3f7ce3789dfee893837742d7c8c69e84366914548347ba6bfc0da95(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c4f1618a84dd695565352b6adbf41c9b28c13aaf62fc255a9b1085928e5fda2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bce324803f4293e0f11e92c2fc84062e201bc452093621bfda00bf85fc7454f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c1826284c66c0ac359a2953549fa235a7eabc9ef1228676ff64123409285fa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2ca4b263b354fa97565157ddcea17fb1854b90516627d6e81d6cdd3d857cd0e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a67684f263d9e6e9c7eed1dd8e7b80eb04e51cea3feb7d06f05563b489ceda(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0013ee048e4880ad892f9df739b9ca52d7aa4e126cbb596773f5908c5dc77e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33d94e040e615d2a8e84e35ccf2248cb32833f77f2d029186c0c8e80893c7deb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1857df325880ce0ab3e160d5ebda6b6895b970b7138e62c687d476a0921fbeb1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f80818536f9b790627147cc4bc5889cf11d9a202d6f69272841723513a227358(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bded1fbd87950082ac53a6bcb55e1fcb4e5495e350b9485985b1dc58b4467943(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb7784857701a43a7dc4fc41cb85e63064bc602cf7186699f3c4bd7206bf3cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5ab0e6db63035a923169e6f1ff65221b9115201cb8130fafae877bfa60c06b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__328494fcc5ea43bc8321e1b4f9f4042257dfa89f71f0ba746907e0eaadcec06d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThan]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38590be1cad9fdf3eddefe8d7fd4817c8ee56e9049fd639f256a9f0608678fa9(
    *,
    key: builtins.str,
    values: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09c59508ecd65f416e09e930ca12303e0756ca00a7f6f847f8357c22e39fdd79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d26048f7e7a89e0df8a0c1fc56d4ccc72c73b84fb49db72830d1ebef9da292b0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ad4b2030e2ae4666e48069e6e909e04bd4fd7c64d569e09ddeb1c4272af151(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02efa689dbd5a2d32917aede151b53f2322ab4b235975bacfb2a0b6874f27ca0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__313e274aa0972cfce4b6caf069bfe59007fd12dfe4cb70ffca0ddecd6437c606(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f1bde5d6043a4e78f962a96601c3fa3b6e2f02bf5c6625ad439272f481cbc9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberIn]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__082276f2d90f7ca687e2c74e18f4d1bc9a7904928e49df4d03416464317dd0fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a8e93268b80ff192a58ec91c0e43de0e38d3126b19ab874c78cb79a6fa517b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f3f1d16cb2fa5cd536aa5ce67ac372eaae07a5ff710eb8788ea407ace9d8581(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4c24f76c55f5c033c97be52fe2d52ced74b4ad2ff389833e46c0e7815ed303f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberIn]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c8f51541c6f3ba8de2aecb9cc637a1e53538baa6f1edea94dff163c747dd880(
    *,
    key: builtins.str,
    values: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Sequence[jsii.Number]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a55f450162087e375db2a4f7f5cbf4fe6be5df1283465ae60d3ac67fcba7c696(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9638b24bb219586b5c9557d846f63c0347c06928e1f28395ca96bbca7593dcd9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__850b2b9ce598437ccec8a5a4c7078c7a45db44b7dd745385a29e2f0131873c3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d97504b0294fe9acac6ebd164f40c6de3f700b2e4d17827528db9e1a73cb3e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc7567597735c37588eaa773ff674a26cbe668f6989352f89773ec7b934b9742(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1cad6656ed151b093290ff2430c588a3cc4b3b5122e6a23316afec9fa9ecfcc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRange]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ece7b805e8228c31645d5437597d883ffa9426ba6213284765859829cb77b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1411d22d468e58c53b68e23728a4f30ef97a08fcd7f4f80d30f1d185785f3d5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f99b3465eccb18171c02e6900c4ccf4ff0fe7a649933a1cd6e72b251471d2092(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[jsii.Number]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e951a571dee5ee2d99f61a892da231cdd9c18149135c418478460171a4e7df0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRange]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd4da26fc901d5e3d7937a5a549e82520c7e52e687c6618a8009fd193d215b9(
    *,
    key: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be775d6dec6a7c0f58137ad9d13dd6412391719b4c35ad1439fa3dd6bbf93022(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__978a700ab210563ce598429d91fb268578b4704bb69e93e5482524cad1c44785(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2701f56283fc45fdba7a198ef86d66af040499d152c5d681477dbbeaec0508d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da8b956f472da56d40cbf5f656c169fe712e714ce3ab5302ba8651f089b1a9e6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad4d1d1c7360d937115e8eea4e59069b8a4d41b507ff1c7de026b8a811574606(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c593920d8cb9789604a38b0dafe91352983416fcc658238bf6dea1b5d06a7ce1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThan]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__722ccb489da02bd00e33c2dbd0ac4fe684138ab767078b7cf5320e87122d3eb3(
    *,
    key: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c2a021b023cf766cf4a0279b04f477c082fc42eb076d197d79c44861ad0c0a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__236b005a1823cf644dcf7d7edbb2f095020f45d94423bef44ccc2e1782430f94(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c89966a5eb992c66a44d31c94c96fdd407c1cd16ea672d9164d0bc6eaf5da3ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3276b50071d96a2a6ceb7462475ba12525d0c782b2b24255a6e8edebb36df554(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8997fe862b4a83a5ca2e6d9b777210588ab8e7ce2dd397e5de42ea786f11d0a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f23e54257799e829f7908f54b85e18b597a2dca453425007ec9401b8571c5379(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEquals]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c03ffc252a39db678e3547031e5c19e97f5077ad60c5943c3ca2b46c899433d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7f1129785b714fcc7f12e5a7ea741188f73415a0678ae1e38a397b2ea8aaadf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6176ad862810180fec13d28e15dd9797ea76ded11fec70a7110c392079645933(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5e51aad42aee50e325e633067c38ecda8374c39303a0cfa2041b89ce00ec7a7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEquals]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e897305d63deef854d2e64775ccf70c8c37f4bd2d6ddc7edd7dca71c4f955f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b3e92c0a4aec18fa58d014afd50213189243af369c05b8ae538a499674b8bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa3daa33beecb2e5037e971a52764c03c2e52570f0667e53498f803b60f36ec2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bd6777d9e1485c0de0473ad1697d05f7a05116933499a9d2989062406e0a8c8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThan]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__600610e7a69f7571d91c55c2a1897fe4814345c63a64bc61d557c50b0ba2e0cf(
    *,
    key: builtins.str,
    values: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e212411557dcc056a31789c13a5c41a1247b04dce040a55d94e543538d66d09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1ec3a302a3b2fcac2bc23e85cbd79112fdf4775e3c739b7a2d753d0a84239f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99634073feb39bdc3a88c53c29ee8da5e10ce2e4f89a87ad066869d170f47384(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ff107f5b5256e71c5f95976ef069dd34f6ca41cfb96ba2137746d791e1e875(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef23511c7374c92f3a467c722a82933b93e1d372955f4886a5eb82071f26d950(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c17be27a8f13192429eae36d8ef382da179afc09d8ffe98d15a32aeccc445b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotIn]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6aea348a5a1a774c0e0096a2199e5516cec3b05e27f2a950fecb4374536fa2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a42741710376f645c8e40499420680b72fa4108c6689ca1d3973f14279ecb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb12fe3c2848c4f01b71fec127ebf974a6f4a9690071b79ce74148c52784b58(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daa338eaf09c3aac860bb2aebaef135829810226aa068fb8c6507241112e209f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotIn]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e1f55b525b5cedfcbe35f0fe31650178e0b88e2073d002cc0a96fd2a06aee6(
    *,
    key: builtins.str,
    values: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Sequence[jsii.Number]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d68f2b578dfd252a0c49ff1cd93bc26de3d239029faf46fd5fba85da98131e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6aa9722fefe9217626e084198fc82861a399f500c85a9553ebc3445d992ee80(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4102568fc731087ae83fe84e12fa77e7de414ee29ca32f204509747305602f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85ff8ad82e7dad951cf4bb6a1b7e6d15464638d229f5ece1fa738dda68431696(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59b9bb18edfcafed4d91717eecb48d1fbe12b31780b55a6783e50de8fc028bb6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c545604fa5ff93812efb0774c19749534a5cef8bdfeb9923d22bda77d559078(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRange]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3cb5fc36d2b8ca046fb57848ff7454ff25efb101e91fa9493fd9880c222ec4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4829e43640a3b4d5a129dee3edc1f4c8ac46205070acb6a40df2fd4697a80c9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6b93ec8f40074e49325f4da5072c0da4b980a5c217d205e245b6bd19f50850d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[jsii.Number]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d5a4004762bac8d0f2db0b62b2d944a4bf2022fb04352569456c33aa0c81994(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRange]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ecff7b72995c07bb2906528c5c358d483cd57ba87f6ba1d5dcae450299e40a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b715a06467857bb862cc8a47b1ac93129d439d25d115ab79a5c8b5040589482(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterBoolEquals, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__639d630b20075dadceeedd19e2e0707b215aac1cb874da31fd821ffcd912ad59(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterIsNotNull, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c397241610d10bddb1ac05d628a19e516aae679ad83d162b91b4c80fb2ac0aec(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterIsNullOrUndefined, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72b726f5f1249631f6281489ebf1bc0ba0b5e1c10ede04299da1e0c2875ffb8f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThan, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e0b9d4da64435ca3ee978040675a9e1864783b8b5634fa1cee5646e846f808(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberGreaterThanOrEquals, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f1eb05703a8199d114d9fb4fb96220856887270e168a56e8834df8d72acf5c1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberIn, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03dc2a10553633546ff0a55231f0c61acf727ef1487a6d421a141546b141b782(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberInRange, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3579506d2aab13280afbe3ce7864271f6cc2a983dbd7fb7e4980a346773a162f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThan, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52decfcffe75ff5a96d0b3ea3a048a03042dbc2021b7e65b00936df34dbe7ebd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberLessThanOrEquals, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f361164e21a1297a7b52f4d7dff99386a08df535e63fde051babbea28fca17c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotIn, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2127dec11416b74d47c80847606962d4260a8787d5e8e8a1f23d837cce73b01e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterNumberNotInRange, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49070197c00bdd12095b66a2f2f94361f2ae2181c5dc0063a3f817407f38d56a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWith, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f86bb92e1a0419eb73eca9f304084a2c462cf789a3d4092f1c2d97e1c9ae2009(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterStringContains, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a947487879976ea460abeea969d7a05e58375ee74efc810aceb0a541ddfd248f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWith, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbfe8ae547d35a62b4ada32707ffbc0bcf534581ddfa654c0e14f31a381a1cf9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterStringIn, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__312a1243bd180df4e9014272c3d630104f0fd89dc4ba34133c4e1d305a7098e6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWith, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a7b1381adebb0a1fea6e6679d61cb5608c4aec48d371eb15c2f238721cb23d7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContains, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3446fa15a0b84f47062b169d837598c33ceafebe9e4236f475aa631c8f25cf1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWith, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211204455d0a6b619de9792fd0ed8155ff931cb6fe7237e506ec6562fdf69e7f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotIn, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56d8931fa26094f8c3863913c3ff68304f41597c5166fe8ee3c9073aa7a2d825(
    value: typing.Optional[EventgridSystemTopicEventSubscriptionAdvancedFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca2870aca0df9a382226541ba9bd3a82f241b15bae8e7073d37f82e4b2e0238(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fd35f508b234bfafdbcc0fc2ad21fea507dfaed83c578e74db9aef655f0f5a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a96b6d1a8e1554e67ecbae662324176aebccf0261e6ecbe2cab95327ead00d82(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f82d3f86c58683ca81b97d808ac703bcef84b3d074335fa4c02a7748d91da1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211ada65e72aacf667e31017c6234edf6a13c94a0b1430c8a7045c12086167b7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99dacf2f891463ef9257463635d899da9189742915d866cb82b0e8aaa594034a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__582db5588ae608d97938944d5eec4a902f086523f958e59058032ee7fdba91ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWith]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3104f1da4b39338dd06b53fc661d53b1c2340e796febfff5f05bc1664d5ee8e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eaa5470c4a5bfa5701c47d96065ecae8b9bba6057b563962930c9e9ae3bc49a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7854eafaaeadeb77abdb1019ecb720bcb5368692e6c0ff36d133f95c7195a76a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ada9dd37ac50a84bf0886c887436e8b3ca09929609e56420c6a3201516612ae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringBeginsWith]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f8d74379d2af9dc423498cc1f580503580a7fa1c731bf824bce4ed1b072ffca(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a808b956a4dd92a642ceda45c34592fe48237f0f0f2d1255a680dc52f203f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__471374f337810b5f28feab56d23146ef67d8fc1f56edacd18685a73cebb909b1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e12deba80aa35775b08c2b35e27d2fcc7336ae7a1cc72e03dbdca73dcccf9fac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__578c1675080b3c771ad3c1f1462f7b9ffd125808ea33b552c83141a26ab2729e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8c424597198538691a5ed67a8fe3c16ac553317b817ddb4b08df5c6d6018188(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d8be9e350935d3d507297269b46bf50def6187208980bd9b854383ba943254b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringContains]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__074be7d761bb6fccbdfecbf637dbfd3b6ab2a6bf81de4b1af071342d5b1da078(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7caea28fd124df581ffcb991674b7908e174cf8754440bc536e44cc8871c0de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397805a8b28245daae039a6b3cb61c4e5e07d0ba0af412bb039836cf0541359c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b100575cb7d2c745f41a49216253b57de77cc02e25f4496838aa28de24d990(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringContains]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5249c56975e1bc798ca97bc93a0a4f2f72ceb19a1d0f6b0c0285e962527c8255(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d99effc5319d07b728447bf5f7c0b5d0731155fa0edafea5256a8403aa720fd9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7837c9981981bc440e7acae9da373a16b495ddd69a2c5fbf0bc9290ed1fff84c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff816bdd87db1be27b0fd82db47214e178e97a4d860da9280642ee95a05a892(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa8748ae1969b7df31e13ecf358dffe730adacc9e334ff1ea365423334090457(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6492239d63a0977b5a3f39931ffd0e78bab5de7f06c6e1dae47bde541ce11ef(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__742426f957ea789c83470aea9b1e52ed4f62d5562f572ebd87c4806b9d577d1e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWith]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__406fdab4aedc08eca1939064aba3e83ff4a30881dc4a6e4b77b5706f2c00afea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__897cba12f2887ae62dd6d69048b66f0a06350ba8a44a93959f53f6151766871a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb7db7207b21454f2434441eb9a78d40945ae44ed6e887401fb8af15279b0ef(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38b483f187155db70d38ff89836fe71aeb0ac7c7e56e4b870e2cd25e51a00eca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringEndsWith]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c3845311e2fb42753a073a7084f0218e5ebd89a0b8d331ce4521772870ebd04(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e439804bd1b7ce015c2c497d5cd457d5ba2612c6c3eb75928f828204c2d21b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84c0f9704cb503a08e70a6c2e20b25068320fa39f66cd40f6c62072a30ffe6d2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deefa8daa91b9c6d6ffe6c16ad88f176b9bf861cb8e766a2808e304e3c81fd14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a6ddc0dfd76df3fe81183c71cc42223046d1121581a76ea91996f267ff79dea(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faf6c379007d5fd72db7721768a461683e9dae41de39dbbbaa2a01dee663006f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d3e3fad9f39633c7740f78db85810ef774e1b57d5550535d9019bb45949bf39(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringIn]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4004d3771984812132800e64caaead647c371172704184372a06365783c3a169(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a30fde84f9f33253eaa7c5e518aac2f0e3ff16b072236fb052c267acecdb81c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c2e10dbdf74603294f9d507727af360e1240f1750e4feb93f9713af88f02094(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4863ec9a3d19770ce29fd2e90901c67509e4d1833fa4116cc208c407d03692e7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringIn]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee5462c3e4c4c65105dcfde6e672fed1a5abdf166d719885023040623229f11c(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34ad57a422031a77315fb9f7c9e36234780a5d1b754ae09abf1bb176d94f65c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b6cecc7621334b6312372d10310a4cd071a0ad28faed6fd46aefb5ac5c9405(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c19db116baf1a94d668c294a2c70231c1eaf6a45d1eb76fb6aee671a1ff2b21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c60faf25e54318350754de7ad4eb426959699e7c47be1ae0dde8e2196cc39034(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__970b3b178e0dab819f794eaffaf7b53a86f1516f33dc3f1daca576d68e519c23(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80b17fb67dbcef7d73398719de162e7dafb9ae8788dd793aed5e238b6522b18f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWith]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__104b7b0d4ca410ab1679c3374a34e5e00935e6c027af49fe6e54790538bbc6ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab7818ecb82eb8b472e46e464db45af156dc05279027505b31ce8ce90f06930c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ece0d5361b20f8f9fc3cf4f31d560b99f7193fb44f83fdadbd8885a314f2fc4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2547582b9eed78a067433137f04a92ac2ff330ad45b3c8326b4e80657840d0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotBeginsWith]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8418d897e4273f7cf5824ff913a2f300c5e0eaebaf5d426c3d7564e67fde1a93(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed799fb72f536534aef375098a1ca7de6d95f9e7656e9ecc6cc8b4646cf02553(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4edae0e53cca5402033b7b6e751795dbf430e630aa2d97e06a4c8504bafd79(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef3bd6f44e8b2d0920c4ebf0534ab1db0c2a0674a9051d9feb4bb9899a323455(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42252bdad5a34de2eabdc2379c867f9d26535cc90529e9924bf03956a55bcb32(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f05103922761e591f1652ac49a7f4f253b9309b2bc75eba797ca027693496eaa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7ae42acc8e681680d6cdfdfeee30d246120bd467453be92292f375ed810409(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContains]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb815e9184b32ef91dc41d2d4c323f26f31c6b5bbc6ade9c8fbab431cff16a51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6c5efdb4a1073aba8c276e128938557053f08b8eb45c79cde9d70f6ad5c62f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b870d9979b2f70728919dad2356e1e663fad7782fbb58ffc1633a332107a2243(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0906b332bf42b53301e6d5474c503f0cfdbb135eb74c681ec6532b45dea4b3b0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotContains]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c2a648113e8cc36a998d9acb29a1149059f575178f11b5015724b174cb16a0b(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2e8580266a9b191d0b345b4e3b87f8410241636e4a334aea0c0fe6a9e30bf3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__684f915fcf26aed6677c89585405ee442fa320d5b2a68d2443ea62a3aa3ff173(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f18e3de0c71b388d047b4cdb8825e721f24cad91835f9d0c217e9621e618412f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88ed65916e7a53c858bbef72039d85c155357e70f9266831603f7f879f75d2fb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d283166b573a695e0c2b1a691e34cc57882958844e2c4444cbe34de616b8be2f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__037270d4a6e20e2058078bdc3b5b0dfe6275fa4d4ecfc0e283bfff5dfaea5519(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWith]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__243352a411312c3334892ee2e56103048227bb0c7273d85937e78321e182997e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d881bcc5201bce20112693afe6d1406d7d4ca1c652ad9a4e5433cb73a49dc67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e7d6b291836395912e2457fd16a558fb5ae798a102e17bd07d999b913dba862(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78050692cbe4ca7103b7fb308e7625b5c8e41d1e0bcfb9085ff69d985378d9e1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotEndsWith]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d4c5a32625ee2b2a1213e8405344a77bdb985fa2633e09181a02ce2c2c29d0e(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e606972c17612a52285172dcba360894a3d2d5873f2194e83e2d4b6549fc2371(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d7474b8eee71426e22fbe23178dfda8f2a30d121c6f5cf966e32e9b899f5f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267664b31002ab3abe04e04dc6957ecd418a4d851ce7b27eec9a4fbe079b570a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dbe0fe6cd97926a43ed8c6f778b270b4c35a4d4a7bbddca6ac022ce859e3898(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8c30e96109be1cfaf01526378b93abb8e49df0c51b36cadd317d94cc35e3f40(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43990881aa381ff1b77458e3855a4c53b2c68ca49a0c166b97293c98ca3dd338(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotIn]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb9af9da6a4f23a588043de32daf233d0bb671472fd198f5ff8c3e5ee8a102e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e058186337aad10dcf201bde432b8ba53b007f772b28ed6c575a1cbd74cbcb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__094d039466663bac8b7c1c0069a539dd98cdda20dcf79206590793a7b2156057(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a57fd8af2475f6f2483c356ee83d9708a7fdf7144b8af3b40887ea8409c5e0a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionAdvancedFilterStringNotIn]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecdfd564b60c7d61d07607a1e715bee6918d2de7bc3c44ae34a11501335494d2(
    *,
    function_id: builtins.str,
    max_events_per_batch: typing.Optional[jsii.Number] = None,
    preferred_batch_size_in_kilobytes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd3966f14ec6acd4cbf517c4ff4b3b2f04af70611c2c14aaad03eb7e1b3666a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__044d7f5355b4bc30c24c6ca0b125764cd573094c80e50ca697cb025fccd20c34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d79b93ac0a3d8a4a58e879d030b2e90e1fd26eb4fe1ee892f06923d5c4f033de(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a83a0c766ee569c26632e8406a1034b403df3e982cd8a26af24501505cc86e8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe75eb005ac60ef5339d43be9be3116a7b895c7ac7bf7b1167fad5fdea901a40(
    value: typing.Optional[EventgridSystemTopicEventSubscriptionAzureFunctionEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c740739baf128eaff9a416c7a23e3eb57fc0f612b91aebabfa29d59580db55(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    resource_group_name: builtins.str,
    system_topic: builtins.str,
    advanced_filter: typing.Optional[typing.Union[EventgridSystemTopicEventSubscriptionAdvancedFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    advanced_filtering_on_arrays_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    azure_function_endpoint: typing.Optional[typing.Union[EventgridSystemTopicEventSubscriptionAzureFunctionEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
    dead_letter_identity: typing.Optional[typing.Union[EventgridSystemTopicEventSubscriptionDeadLetterIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    delivery_identity: typing.Optional[typing.Union[EventgridSystemTopicEventSubscriptionDeliveryIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    delivery_property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventgridSystemTopicEventSubscriptionDeliveryProperty, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_delivery_schema: typing.Optional[builtins.str] = None,
    eventhub_endpoint_id: typing.Optional[builtins.str] = None,
    expiration_time_utc: typing.Optional[builtins.str] = None,
    hybrid_connection_endpoint_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    included_event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    retry_policy: typing.Optional[typing.Union[EventgridSystemTopicEventSubscriptionRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    service_bus_queue_endpoint_id: typing.Optional[builtins.str] = None,
    service_bus_topic_endpoint_id: typing.Optional[builtins.str] = None,
    storage_blob_dead_letter_destination: typing.Optional[typing.Union[EventgridSystemTopicEventSubscriptionStorageBlobDeadLetterDestination, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_queue_endpoint: typing.Optional[typing.Union[EventgridSystemTopicEventSubscriptionStorageQueueEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
    subject_filter: typing.Optional[typing.Union[EventgridSystemTopicEventSubscriptionSubjectFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[EventgridSystemTopicEventSubscriptionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    webhook_endpoint: typing.Optional[typing.Union[EventgridSystemTopicEventSubscriptionWebhookEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d06371d41b0699c64aff84d52f099c3dc3b3ec3491d439549f47bddde924962(
    *,
    type: builtins.str,
    user_assigned_identity: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e82a14a1a7f4f4fbef1b2746478a0c2a63562f0bb78fd90392bc3092b3da9e9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c1fd547e5dfbf11b4f13cdc909fa5b0398a25d09079463f41019a7d086081c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bac3221e03b89e40b20eff48f2787810a89f7febe16827e40ce32a2f2d48e4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f8b3d1ad39307fa1877fed3ef7278e3ebdbede904077260d045170c81e6eca(
    value: typing.Optional[EventgridSystemTopicEventSubscriptionDeadLetterIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3a47045fe8f4e82be426f8c341c41dedcbf53558cfcabb36a9092d363b63a52(
    *,
    type: builtins.str,
    user_assigned_identity: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3242437936873ebba0258bb9caf97e6ff63e7eae9a3d1bc24999dc4290678892(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e977710d69715de75ee4ed2405d33fb00744c1e7897d029a23b053aea18682(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__532131c3b8d7921763abf4b0b5337d360b1481a64da5f094705e88f461fed1b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f7b5962a45a0adf0c6dc2dac8681c5840f59ae715e0b100de2a1802ffa45a7e(
    value: typing.Optional[EventgridSystemTopicEventSubscriptionDeliveryIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4157dcf76b500d7618db2908dc5fd80fbeb2e6459c834621024e7014a448f9d9(
    *,
    header_name: builtins.str,
    type: builtins.str,
    secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source_field: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a64644e47e8a3bdb4e9daefa59e3d0615c95166631b6bf8fd7100cafa13cfdcf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee96028c8147ae49ab661e9a487aa6ba1782a1a399b57ab7a01dd88bcb786bc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2dfae8f73304a5ff031235083e1b6611bebca1143249cc94764423248759caa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__295487e28920e0ff8fa7093ab6059db81718181a0f17c776d06080b70fa046f8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66c2d55a52024237fe94c7a72b5ebcdccf0922edfad749e239b0faeea9b033ac(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7008d9a5192d48f04b096dbb653e890a4c9f41d2920f71ff43996eff3166af4b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventgridSystemTopicEventSubscriptionDeliveryProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__593e42b9e5319f7bf05cf56803b5e32f1ca05fa0ddc53e55ba824e196a7f7553(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5767220c7e379660b7f52495c673a37cbc8848c15c5b70cebd4c20973e29e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4843945f5c039cc94d89628c7bed69adc2ab304bae29c6adcc641a6924e0ac04(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a56326d5807478ccefb2d02fe55cd7b11a401a79c82adfabf420425e78ba77f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6570b34d51a18a9484a339f0d40f0e8d3be128e748d9cfa5bad23c19e9cf6971(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f56351b6a10f017e7274437ba19b9e9e30cbf425dd1008d008575933bb01dea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d176acd1b5f649f281fede5798012eef3ff61be385da95f9961453b2cfe7853(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionDeliveryProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c3b86828fd82ff4c3e8643c0043e1395a49bd5a2a198385837f78d511ab741(
    *,
    event_time_to_live: jsii.Number,
    max_delivery_attempts: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cadce26e4145057b35fffc7c6d54132a702f01f0b5f10b7df0122ec11c8e0a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cad76cb1d84180baf1e95759fc4eadddb92b45ebb690d3e69e9d213765077462(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f249b6177a81fe65bd01883ea8fa199bf6b394ea68251130411e84bbed4a5a5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c07fa2b9663a22fbcfb277a980173651c6de1edb772278ca9c62e314f1b4890(
    value: typing.Optional[EventgridSystemTopicEventSubscriptionRetryPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2cec756508e7ba546bd05c2d300603eb12b744dfc8d4b2906e8c955d2402320(
    *,
    storage_account_id: builtins.str,
    storage_blob_container_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2b95b42686e25b22e502774c48a2f47a48ded23dd78884a44ba477869f79312(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63778e7acb8de96c31e10013b8e03dc7daf7c9d3a25a4bcc0e3417c8d609757(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88d620a6c162fdc76455182306608136c3634588a129ceb19c90be54102688fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c85dfafee7623e51140acdbc9add53facd3241cfbe47cf6782cda2861706e759(
    value: typing.Optional[EventgridSystemTopicEventSubscriptionStorageBlobDeadLetterDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfc6cc376ee4925d0ed63fa388d2ffe375c2dffc0672d56d48db8826bf418517(
    *,
    queue_name: builtins.str,
    storage_account_id: builtins.str,
    queue_message_time_to_live_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe66cdee71ee32c75365c43bd96719feb969968bb766c53b80216198bc1963d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__822c560fd5dcded3754e71a40b942b87278706beb7dbc75df6be90568cfcafce(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa22dfd3bb2372183b0fffe74264373b8135b7d6c7c522b69feca2e41e58fe7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__902beb152bbb293ee74e1f56491678bf855f9762c8c116007f3fb25b0417827d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa016321dacba5a2ed6a215d5bf670442d165f62fc09215754301fb7b8adee7(
    value: typing.Optional[EventgridSystemTopicEventSubscriptionStorageQueueEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ad77a46fa6e4e3911002a9c330779e249a05d42326d144167d7f3b0aa44fc3(
    *,
    case_sensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subject_begins_with: typing.Optional[builtins.str] = None,
    subject_ends_with: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5412b9206cd8622611fcdbee4e0b06d97a830ae5bc8e662b748641ec65b3177(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3944b089a13d7ab9878683f8afb5a05ddbd6856739f44daa4461260341fc043a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c76db048d3cb350522b5fb9aba2406e1166b393e9719a5bbe455e595ec37d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a277a173a2165f463488ba70404cbdba7119815897133ce65d7a178265af317(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a617ef1f29f76f344070283dba813c450ebb84befda02326ab45fb02541bb5(
    value: typing.Optional[EventgridSystemTopicEventSubscriptionSubjectFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c30c474881e22e16821324cfbe46cb122f37ecf0b3183637d535ad29017e46d5(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd620df7c0ceaf20aa9c31c8eb7d68e8be1f5d6ca1d2894774818a4b5c5f545c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f6474e999fd9faf8c889a59265a1b5a5e5244d0980aee05e4207e7fcaed7d60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0064eec71d8bb533777bef1841600c0474fd8a4c5145633ec71c930246f09887(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714ee24c38be09ede23de912d842caaca4dc29986c202d77124982c492785c1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc81df98951c9647c0dd74a991dcb5623e9f9b8d2b7a9ab336aefc3b4288352(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5d8edf4b2455e91fb3dba66ea91d8717fa8f4bb9a48645eeeac2cac7d7c669(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventgridSystemTopicEventSubscriptionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd4f17eee7c5c5075345702f2e2955d57ab198b3fc03f033cf76a5db9bfcc34(
    *,
    url: builtins.str,
    active_directory_app_id_or_uri: typing.Optional[builtins.str] = None,
    active_directory_tenant_id: typing.Optional[builtins.str] = None,
    max_events_per_batch: typing.Optional[jsii.Number] = None,
    preferred_batch_size_in_kilobytes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__988e3123005334c2f7fffd576ee73313606ce39184ebc2e3aaef45b0f1c58568(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a370a8b37e8d37ecd807b28552fb145e4d411023ef7aea194cada4497df9e3f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fae208efea6c28e2d292815d589d4cb85b972bb16b7a18448f3ad925dac1f48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce3d9a501708945240b43c6ca2c2ea8c335c2f661f3753ed0d02eceb05664304(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a766c332b5f3c74120548eabb5c734467545fd675786f9ea80b6bf318e8a7770(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230689708a52947bdd439ccdb9e8c322c8b026bc8d8d23a153caaa9a5bac420a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__893b6ed9cdb6943abcbfd5e1c6fc7c1a2f0943de221da09092e4910e6a58d270(
    value: typing.Optional[EventgridSystemTopicEventSubscriptionWebhookEndpoint],
) -> None:
    """Type checking stubs"""
    pass
