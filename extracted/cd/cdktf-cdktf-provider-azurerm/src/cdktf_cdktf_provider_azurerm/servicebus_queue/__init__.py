r'''
# `azurerm_servicebus_queue`

Refer to the Terraform Registry for docs: [`azurerm_servicebus_queue`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue).
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


class ServicebusQueue(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.servicebusQueue.ServicebusQueue",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue azurerm_servicebus_queue}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        namespace_id: builtins.str,
        auto_delete_on_idle: typing.Optional[builtins.str] = None,
        batched_operations_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dead_lettering_on_message_expiration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_message_ttl: typing.Optional[builtins.str] = None,
        duplicate_detection_history_time_window: typing.Optional[builtins.str] = None,
        express_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forward_dead_lettered_messages_to: typing.Optional[builtins.str] = None,
        forward_to: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lock_duration: typing.Optional[builtins.str] = None,
        max_delivery_count: typing.Optional[jsii.Number] = None,
        max_message_size_in_kilobytes: typing.Optional[jsii.Number] = None,
        max_size_in_megabytes: typing.Optional[jsii.Number] = None,
        partitioning_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        requires_duplicate_detection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        requires_session: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ServicebusQueueTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue azurerm_servicebus_queue} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#name ServicebusQueue#name}.
        :param namespace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#namespace_id ServicebusQueue#namespace_id}.
        :param auto_delete_on_idle: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#auto_delete_on_idle ServicebusQueue#auto_delete_on_idle}.
        :param batched_operations_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#batched_operations_enabled ServicebusQueue#batched_operations_enabled}.
        :param dead_lettering_on_message_expiration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#dead_lettering_on_message_expiration ServicebusQueue#dead_lettering_on_message_expiration}.
        :param default_message_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#default_message_ttl ServicebusQueue#default_message_ttl}.
        :param duplicate_detection_history_time_window: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#duplicate_detection_history_time_window ServicebusQueue#duplicate_detection_history_time_window}.
        :param express_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#express_enabled ServicebusQueue#express_enabled}.
        :param forward_dead_lettered_messages_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#forward_dead_lettered_messages_to ServicebusQueue#forward_dead_lettered_messages_to}.
        :param forward_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#forward_to ServicebusQueue#forward_to}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#id ServicebusQueue#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lock_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#lock_duration ServicebusQueue#lock_duration}.
        :param max_delivery_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#max_delivery_count ServicebusQueue#max_delivery_count}.
        :param max_message_size_in_kilobytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#max_message_size_in_kilobytes ServicebusQueue#max_message_size_in_kilobytes}.
        :param max_size_in_megabytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#max_size_in_megabytes ServicebusQueue#max_size_in_megabytes}.
        :param partitioning_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#partitioning_enabled ServicebusQueue#partitioning_enabled}.
        :param requires_duplicate_detection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#requires_duplicate_detection ServicebusQueue#requires_duplicate_detection}.
        :param requires_session: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#requires_session ServicebusQueue#requires_session}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#status ServicebusQueue#status}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#timeouts ServicebusQueue#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19d2b52d829e94f3ce6e598a32eac575da0ac68998512830b727e12b8b1d81b7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ServicebusQueueConfig(
            name=name,
            namespace_id=namespace_id,
            auto_delete_on_idle=auto_delete_on_idle,
            batched_operations_enabled=batched_operations_enabled,
            dead_lettering_on_message_expiration=dead_lettering_on_message_expiration,
            default_message_ttl=default_message_ttl,
            duplicate_detection_history_time_window=duplicate_detection_history_time_window,
            express_enabled=express_enabled,
            forward_dead_lettered_messages_to=forward_dead_lettered_messages_to,
            forward_to=forward_to,
            id=id,
            lock_duration=lock_duration,
            max_delivery_count=max_delivery_count,
            max_message_size_in_kilobytes=max_message_size_in_kilobytes,
            max_size_in_megabytes=max_size_in_megabytes,
            partitioning_enabled=partitioning_enabled,
            requires_duplicate_detection=requires_duplicate_detection,
            requires_session=requires_session,
            status=status,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a ServicebusQueue resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ServicebusQueue to import.
        :param import_from_id: The id of the existing ServicebusQueue that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ServicebusQueue to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae35c78d2550eba4182fcfc2e954ade6db20778a6ccccfc9c84fbc850ebe1348)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#create ServicebusQueue#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#delete ServicebusQueue#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#read ServicebusQueue#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#update ServicebusQueue#update}.
        '''
        value = ServicebusQueueTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAutoDeleteOnIdle")
    def reset_auto_delete_on_idle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoDeleteOnIdle", []))

    @jsii.member(jsii_name="resetBatchedOperationsEnabled")
    def reset_batched_operations_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchedOperationsEnabled", []))

    @jsii.member(jsii_name="resetDeadLetteringOnMessageExpiration")
    def reset_dead_lettering_on_message_expiration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeadLetteringOnMessageExpiration", []))

    @jsii.member(jsii_name="resetDefaultMessageTtl")
    def reset_default_message_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultMessageTtl", []))

    @jsii.member(jsii_name="resetDuplicateDetectionHistoryTimeWindow")
    def reset_duplicate_detection_history_time_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDuplicateDetectionHistoryTimeWindow", []))

    @jsii.member(jsii_name="resetExpressEnabled")
    def reset_express_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpressEnabled", []))

    @jsii.member(jsii_name="resetForwardDeadLetteredMessagesTo")
    def reset_forward_dead_lettered_messages_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardDeadLetteredMessagesTo", []))

    @jsii.member(jsii_name="resetForwardTo")
    def reset_forward_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardTo", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLockDuration")
    def reset_lock_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLockDuration", []))

    @jsii.member(jsii_name="resetMaxDeliveryCount")
    def reset_max_delivery_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxDeliveryCount", []))

    @jsii.member(jsii_name="resetMaxMessageSizeInKilobytes")
    def reset_max_message_size_in_kilobytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxMessageSizeInKilobytes", []))

    @jsii.member(jsii_name="resetMaxSizeInMegabytes")
    def reset_max_size_in_megabytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxSizeInMegabytes", []))

    @jsii.member(jsii_name="resetPartitioningEnabled")
    def reset_partitioning_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartitioningEnabled", []))

    @jsii.member(jsii_name="resetRequiresDuplicateDetection")
    def reset_requires_duplicate_detection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiresDuplicateDetection", []))

    @jsii.member(jsii_name="resetRequiresSession")
    def reset_requires_session(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiresSession", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ServicebusQueueTimeoutsOutputReference":
        return typing.cast("ServicebusQueueTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="autoDeleteOnIdleInput")
    def auto_delete_on_idle_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoDeleteOnIdleInput"))

    @builtins.property
    @jsii.member(jsii_name="batchedOperationsEnabledInput")
    def batched_operations_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "batchedOperationsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="deadLetteringOnMessageExpirationInput")
    def dead_lettering_on_message_expiration_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deadLetteringOnMessageExpirationInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultMessageTtlInput")
    def default_message_ttl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultMessageTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="duplicateDetectionHistoryTimeWindowInput")
    def duplicate_detection_history_time_window_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "duplicateDetectionHistoryTimeWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="expressEnabledInput")
    def express_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "expressEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardDeadLetteredMessagesToInput")
    def forward_dead_lettered_messages_to_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forwardDeadLetteredMessagesToInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardToInput")
    def forward_to_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forwardToInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="lockDurationInput")
    def lock_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lockDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxDeliveryCountInput")
    def max_delivery_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxDeliveryCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxMessageSizeInKilobytesInput")
    def max_message_size_in_kilobytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxMessageSizeInKilobytesInput"))

    @builtins.property
    @jsii.member(jsii_name="maxSizeInMegabytesInput")
    def max_size_in_megabytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxSizeInMegabytesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceIdInput")
    def namespace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="partitioningEnabledInput")
    def partitioning_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "partitioningEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="requiresDuplicateDetectionInput")
    def requires_duplicate_detection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requiresDuplicateDetectionInput"))

    @builtins.property
    @jsii.member(jsii_name="requiresSessionInput")
    def requires_session_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requiresSessionInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ServicebusQueueTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ServicebusQueueTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDeleteOnIdle")
    def auto_delete_on_idle(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoDeleteOnIdle"))

    @auto_delete_on_idle.setter
    def auto_delete_on_idle(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98e3af3613d5c2d6b8190d0c29977001bc362b976c8e6adf597f68544f826a99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDeleteOnIdle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="batchedOperationsEnabled")
    def batched_operations_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "batchedOperationsEnabled"))

    @batched_operations_enabled.setter
    def batched_operations_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76c1960215bc643e0ad579ae78e947a7161415f264c88e5870e5aaef3ba4a92f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchedOperationsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deadLetteringOnMessageExpiration")
    def dead_lettering_on_message_expiration(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deadLetteringOnMessageExpiration"))

    @dead_lettering_on_message_expiration.setter
    def dead_lettering_on_message_expiration(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93f3edaba1557dbbaec360b2841125d34a67d936eb1a217dbdb7aab4d342cac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deadLetteringOnMessageExpiration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultMessageTtl")
    def default_message_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultMessageTtl"))

    @default_message_ttl.setter
    def default_message_ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1130f85a9ad08c41266b4957ece44cea3a4f8e5d763d172a634a19dd504beb69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultMessageTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="duplicateDetectionHistoryTimeWindow")
    def duplicate_detection_history_time_window(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duplicateDetectionHistoryTimeWindow"))

    @duplicate_detection_history_time_window.setter
    def duplicate_detection_history_time_window(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1a0c14809f452845ab59f9b9914746b801709c32d9df1758081d3f7d8d2a57e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duplicateDetectionHistoryTimeWindow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expressEnabled")
    def express_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "expressEnabled"))

    @express_enabled.setter
    def express_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df38f1a2a3edebc7e1f72adb7109dacf2a0e2cb51783ecd117b554c3a0a00408)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expressEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardDeadLetteredMessagesTo")
    def forward_dead_lettered_messages_to(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardDeadLetteredMessagesTo"))

    @forward_dead_lettered_messages_to.setter
    def forward_dead_lettered_messages_to(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaf7fcb40ca17a43443341e1e584e7bdf263cbda73bafcf7d8f98e3f979a4319)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardDeadLetteredMessagesTo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardTo")
    def forward_to(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardTo"))

    @forward_to.setter
    def forward_to(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be0e425673ea512cc30f6a67501ae50e481735f78c579b5e13f033cb2b27cda5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardTo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7476beb842e11fc1b68a9c6a0e3589197c6ed07833f9585a8954c950f28de553)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lockDuration")
    def lock_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lockDuration"))

    @lock_duration.setter
    def lock_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c19f18a59ac3ef66caf9162a76761dba90b2f99ac388d93d048f6d14fa17960)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lockDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDeliveryCount")
    def max_delivery_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDeliveryCount"))

    @max_delivery_count.setter
    def max_delivery_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d56358c9bf9915b3f5e9f0a96bda44956da47650ccfa7899e8844bec9ead25d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDeliveryCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxMessageSizeInKilobytes")
    def max_message_size_in_kilobytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxMessageSizeInKilobytes"))

    @max_message_size_in_kilobytes.setter
    def max_message_size_in_kilobytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15fece5145820d22ad73ba6c964a9d0935d1fca7d903729523930c47edcd14cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxMessageSizeInKilobytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxSizeInMegabytes")
    def max_size_in_megabytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxSizeInMegabytes"))

    @max_size_in_megabytes.setter
    def max_size_in_megabytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9da14dc28d3526764ef9a41dc34e94780645db01d821c27f6a3041ed14f01a21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSizeInMegabytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__340342478b064c8ea62e43d4dba3aec382fefc8c1cb6f6b2ea88f29cbbb24d73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespaceId"))

    @namespace_id.setter
    def namespace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__031457ee4124fe2a01b5728b429bef4fea2d22d1dd8ec9b49eb2526264913fc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partitioningEnabled")
    def partitioning_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "partitioningEnabled"))

    @partitioning_enabled.setter
    def partitioning_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a8cc9c7e189ff6df870fae209de7057ce6c426042a1d5194c16e0416e78a57c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitioningEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requiresDuplicateDetection")
    def requires_duplicate_detection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requiresDuplicateDetection"))

    @requires_duplicate_detection.setter
    def requires_duplicate_detection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c15cfef60c2ff3b9e889f23fa2b66db5e312df0a20cffbf8b170e0ba7e00aa28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requiresDuplicateDetection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requiresSession")
    def requires_session(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requiresSession"))

    @requires_session.setter
    def requires_session(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85eb0ccfa3e4d5b0b84fa2177b008b205894d29676a0b17248c2770abd0beb45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requiresSession", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e93cd15b0076c341207cc1b6ece0c82f97e64f08e9ed1b34cf7f2ebb7c3c566d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.servicebusQueue.ServicebusQueueConfig",
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
        "namespace_id": "namespaceId",
        "auto_delete_on_idle": "autoDeleteOnIdle",
        "batched_operations_enabled": "batchedOperationsEnabled",
        "dead_lettering_on_message_expiration": "deadLetteringOnMessageExpiration",
        "default_message_ttl": "defaultMessageTtl",
        "duplicate_detection_history_time_window": "duplicateDetectionHistoryTimeWindow",
        "express_enabled": "expressEnabled",
        "forward_dead_lettered_messages_to": "forwardDeadLetteredMessagesTo",
        "forward_to": "forwardTo",
        "id": "id",
        "lock_duration": "lockDuration",
        "max_delivery_count": "maxDeliveryCount",
        "max_message_size_in_kilobytes": "maxMessageSizeInKilobytes",
        "max_size_in_megabytes": "maxSizeInMegabytes",
        "partitioning_enabled": "partitioningEnabled",
        "requires_duplicate_detection": "requiresDuplicateDetection",
        "requires_session": "requiresSession",
        "status": "status",
        "timeouts": "timeouts",
    },
)
class ServicebusQueueConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        namespace_id: builtins.str,
        auto_delete_on_idle: typing.Optional[builtins.str] = None,
        batched_operations_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dead_lettering_on_message_expiration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_message_ttl: typing.Optional[builtins.str] = None,
        duplicate_detection_history_time_window: typing.Optional[builtins.str] = None,
        express_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forward_dead_lettered_messages_to: typing.Optional[builtins.str] = None,
        forward_to: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lock_duration: typing.Optional[builtins.str] = None,
        max_delivery_count: typing.Optional[jsii.Number] = None,
        max_message_size_in_kilobytes: typing.Optional[jsii.Number] = None,
        max_size_in_megabytes: typing.Optional[jsii.Number] = None,
        partitioning_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        requires_duplicate_detection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        requires_session: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ServicebusQueueTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#name ServicebusQueue#name}.
        :param namespace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#namespace_id ServicebusQueue#namespace_id}.
        :param auto_delete_on_idle: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#auto_delete_on_idle ServicebusQueue#auto_delete_on_idle}.
        :param batched_operations_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#batched_operations_enabled ServicebusQueue#batched_operations_enabled}.
        :param dead_lettering_on_message_expiration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#dead_lettering_on_message_expiration ServicebusQueue#dead_lettering_on_message_expiration}.
        :param default_message_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#default_message_ttl ServicebusQueue#default_message_ttl}.
        :param duplicate_detection_history_time_window: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#duplicate_detection_history_time_window ServicebusQueue#duplicate_detection_history_time_window}.
        :param express_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#express_enabled ServicebusQueue#express_enabled}.
        :param forward_dead_lettered_messages_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#forward_dead_lettered_messages_to ServicebusQueue#forward_dead_lettered_messages_to}.
        :param forward_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#forward_to ServicebusQueue#forward_to}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#id ServicebusQueue#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lock_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#lock_duration ServicebusQueue#lock_duration}.
        :param max_delivery_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#max_delivery_count ServicebusQueue#max_delivery_count}.
        :param max_message_size_in_kilobytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#max_message_size_in_kilobytes ServicebusQueue#max_message_size_in_kilobytes}.
        :param max_size_in_megabytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#max_size_in_megabytes ServicebusQueue#max_size_in_megabytes}.
        :param partitioning_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#partitioning_enabled ServicebusQueue#partitioning_enabled}.
        :param requires_duplicate_detection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#requires_duplicate_detection ServicebusQueue#requires_duplicate_detection}.
        :param requires_session: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#requires_session ServicebusQueue#requires_session}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#status ServicebusQueue#status}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#timeouts ServicebusQueue#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ServicebusQueueTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb0604ab69183d1aac24468193296b06a74560cf57ec13b14b9e8cd82abe54a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace_id", value=namespace_id, expected_type=type_hints["namespace_id"])
            check_type(argname="argument auto_delete_on_idle", value=auto_delete_on_idle, expected_type=type_hints["auto_delete_on_idle"])
            check_type(argname="argument batched_operations_enabled", value=batched_operations_enabled, expected_type=type_hints["batched_operations_enabled"])
            check_type(argname="argument dead_lettering_on_message_expiration", value=dead_lettering_on_message_expiration, expected_type=type_hints["dead_lettering_on_message_expiration"])
            check_type(argname="argument default_message_ttl", value=default_message_ttl, expected_type=type_hints["default_message_ttl"])
            check_type(argname="argument duplicate_detection_history_time_window", value=duplicate_detection_history_time_window, expected_type=type_hints["duplicate_detection_history_time_window"])
            check_type(argname="argument express_enabled", value=express_enabled, expected_type=type_hints["express_enabled"])
            check_type(argname="argument forward_dead_lettered_messages_to", value=forward_dead_lettered_messages_to, expected_type=type_hints["forward_dead_lettered_messages_to"])
            check_type(argname="argument forward_to", value=forward_to, expected_type=type_hints["forward_to"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lock_duration", value=lock_duration, expected_type=type_hints["lock_duration"])
            check_type(argname="argument max_delivery_count", value=max_delivery_count, expected_type=type_hints["max_delivery_count"])
            check_type(argname="argument max_message_size_in_kilobytes", value=max_message_size_in_kilobytes, expected_type=type_hints["max_message_size_in_kilobytes"])
            check_type(argname="argument max_size_in_megabytes", value=max_size_in_megabytes, expected_type=type_hints["max_size_in_megabytes"])
            check_type(argname="argument partitioning_enabled", value=partitioning_enabled, expected_type=type_hints["partitioning_enabled"])
            check_type(argname="argument requires_duplicate_detection", value=requires_duplicate_detection, expected_type=type_hints["requires_duplicate_detection"])
            check_type(argname="argument requires_session", value=requires_session, expected_type=type_hints["requires_session"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "namespace_id": namespace_id,
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
        if auto_delete_on_idle is not None:
            self._values["auto_delete_on_idle"] = auto_delete_on_idle
        if batched_operations_enabled is not None:
            self._values["batched_operations_enabled"] = batched_operations_enabled
        if dead_lettering_on_message_expiration is not None:
            self._values["dead_lettering_on_message_expiration"] = dead_lettering_on_message_expiration
        if default_message_ttl is not None:
            self._values["default_message_ttl"] = default_message_ttl
        if duplicate_detection_history_time_window is not None:
            self._values["duplicate_detection_history_time_window"] = duplicate_detection_history_time_window
        if express_enabled is not None:
            self._values["express_enabled"] = express_enabled
        if forward_dead_lettered_messages_to is not None:
            self._values["forward_dead_lettered_messages_to"] = forward_dead_lettered_messages_to
        if forward_to is not None:
            self._values["forward_to"] = forward_to
        if id is not None:
            self._values["id"] = id
        if lock_duration is not None:
            self._values["lock_duration"] = lock_duration
        if max_delivery_count is not None:
            self._values["max_delivery_count"] = max_delivery_count
        if max_message_size_in_kilobytes is not None:
            self._values["max_message_size_in_kilobytes"] = max_message_size_in_kilobytes
        if max_size_in_megabytes is not None:
            self._values["max_size_in_megabytes"] = max_size_in_megabytes
        if partitioning_enabled is not None:
            self._values["partitioning_enabled"] = partitioning_enabled
        if requires_duplicate_detection is not None:
            self._values["requires_duplicate_detection"] = requires_duplicate_detection
        if requires_session is not None:
            self._values["requires_session"] = requires_session
        if status is not None:
            self._values["status"] = status
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#name ServicebusQueue#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#namespace_id ServicebusQueue#namespace_id}.'''
        result = self._values.get("namespace_id")
        assert result is not None, "Required property 'namespace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_delete_on_idle(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#auto_delete_on_idle ServicebusQueue#auto_delete_on_idle}.'''
        result = self._values.get("auto_delete_on_idle")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def batched_operations_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#batched_operations_enabled ServicebusQueue#batched_operations_enabled}.'''
        result = self._values.get("batched_operations_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dead_lettering_on_message_expiration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#dead_lettering_on_message_expiration ServicebusQueue#dead_lettering_on_message_expiration}.'''
        result = self._values.get("dead_lettering_on_message_expiration")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def default_message_ttl(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#default_message_ttl ServicebusQueue#default_message_ttl}.'''
        result = self._values.get("default_message_ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def duplicate_detection_history_time_window(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#duplicate_detection_history_time_window ServicebusQueue#duplicate_detection_history_time_window}.'''
        result = self._values.get("duplicate_detection_history_time_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def express_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#express_enabled ServicebusQueue#express_enabled}.'''
        result = self._values.get("express_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def forward_dead_lettered_messages_to(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#forward_dead_lettered_messages_to ServicebusQueue#forward_dead_lettered_messages_to}.'''
        result = self._values.get("forward_dead_lettered_messages_to")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def forward_to(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#forward_to ServicebusQueue#forward_to}.'''
        result = self._values.get("forward_to")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#id ServicebusQueue#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lock_duration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#lock_duration ServicebusQueue#lock_duration}.'''
        result = self._values.get("lock_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_delivery_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#max_delivery_count ServicebusQueue#max_delivery_count}.'''
        result = self._values.get("max_delivery_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_message_size_in_kilobytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#max_message_size_in_kilobytes ServicebusQueue#max_message_size_in_kilobytes}.'''
        result = self._values.get("max_message_size_in_kilobytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_size_in_megabytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#max_size_in_megabytes ServicebusQueue#max_size_in_megabytes}.'''
        result = self._values.get("max_size_in_megabytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def partitioning_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#partitioning_enabled ServicebusQueue#partitioning_enabled}.'''
        result = self._values.get("partitioning_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def requires_duplicate_detection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#requires_duplicate_detection ServicebusQueue#requires_duplicate_detection}.'''
        result = self._values.get("requires_duplicate_detection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def requires_session(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#requires_session ServicebusQueue#requires_session}.'''
        result = self._values.get("requires_session")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#status ServicebusQueue#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ServicebusQueueTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#timeouts ServicebusQueue#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ServicebusQueueTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServicebusQueueConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.servicebusQueue.ServicebusQueueTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ServicebusQueueTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#create ServicebusQueue#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#delete ServicebusQueue#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#read ServicebusQueue#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#update ServicebusQueue#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51579fcfb08ef43fc4f87a287b0f6ac35b4043f3ca86c47448eed616416d31bb)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#create ServicebusQueue#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#delete ServicebusQueue#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#read ServicebusQueue#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_queue#update ServicebusQueue#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServicebusQueueTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServicebusQueueTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.servicebusQueue.ServicebusQueueTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecda01d5cc6a5079e96fa4eccabb005554e386f567f38a76f529743a028355f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e710307878a00826651a2c125fe84b761389f62a25a1b7e51da493af4b47e6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b90546aba41893edfb2aadc931d4de1fb4ba8b0a384632a7cc40104ba38d9483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3febe8c4c3a6b3386496ae5b046eb54704589ca446d56254fae89157ddf8419)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b88d8f3f92d5afe0997ccd337d7166e5198eaeee0f807ae50035811cd5c35b37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServicebusQueueTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServicebusQueueTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServicebusQueueTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b5660ee7f88141280108bc1cb3a7d24e70b3f5047e829f81de8b8ed2c9123c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ServicebusQueue",
    "ServicebusQueueConfig",
    "ServicebusQueueTimeouts",
    "ServicebusQueueTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__19d2b52d829e94f3ce6e598a32eac575da0ac68998512830b727e12b8b1d81b7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    namespace_id: builtins.str,
    auto_delete_on_idle: typing.Optional[builtins.str] = None,
    batched_operations_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dead_lettering_on_message_expiration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_message_ttl: typing.Optional[builtins.str] = None,
    duplicate_detection_history_time_window: typing.Optional[builtins.str] = None,
    express_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forward_dead_lettered_messages_to: typing.Optional[builtins.str] = None,
    forward_to: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    lock_duration: typing.Optional[builtins.str] = None,
    max_delivery_count: typing.Optional[jsii.Number] = None,
    max_message_size_in_kilobytes: typing.Optional[jsii.Number] = None,
    max_size_in_megabytes: typing.Optional[jsii.Number] = None,
    partitioning_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    requires_duplicate_detection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    requires_session: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ServicebusQueueTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ae35c78d2550eba4182fcfc2e954ade6db20778a6ccccfc9c84fbc850ebe1348(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e3af3613d5c2d6b8190d0c29977001bc362b976c8e6adf597f68544f826a99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76c1960215bc643e0ad579ae78e947a7161415f264c88e5870e5aaef3ba4a92f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f3edaba1557dbbaec360b2841125d34a67d936eb1a217dbdb7aab4d342cac3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1130f85a9ad08c41266b4957ece44cea3a4f8e5d763d172a634a19dd504beb69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1a0c14809f452845ab59f9b9914746b801709c32d9df1758081d3f7d8d2a57e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df38f1a2a3edebc7e1f72adb7109dacf2a0e2cb51783ecd117b554c3a0a00408(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf7fcb40ca17a43443341e1e584e7bdf263cbda73bafcf7d8f98e3f979a4319(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be0e425673ea512cc30f6a67501ae50e481735f78c579b5e13f033cb2b27cda5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7476beb842e11fc1b68a9c6a0e3589197c6ed07833f9585a8954c950f28de553(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c19f18a59ac3ef66caf9162a76761dba90b2f99ac388d93d048f6d14fa17960(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d56358c9bf9915b3f5e9f0a96bda44956da47650ccfa7899e8844bec9ead25d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15fece5145820d22ad73ba6c964a9d0935d1fca7d903729523930c47edcd14cb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9da14dc28d3526764ef9a41dc34e94780645db01d821c27f6a3041ed14f01a21(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__340342478b064c8ea62e43d4dba3aec382fefc8c1cb6f6b2ea88f29cbbb24d73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__031457ee4124fe2a01b5728b429bef4fea2d22d1dd8ec9b49eb2526264913fc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a8cc9c7e189ff6df870fae209de7057ce6c426042a1d5194c16e0416e78a57c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c15cfef60c2ff3b9e889f23fa2b66db5e312df0a20cffbf8b170e0ba7e00aa28(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85eb0ccfa3e4d5b0b84fa2177b008b205894d29676a0b17248c2770abd0beb45(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e93cd15b0076c341207cc1b6ece0c82f97e64f08e9ed1b34cf7f2ebb7c3c566d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb0604ab69183d1aac24468193296b06a74560cf57ec13b14b9e8cd82abe54a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    namespace_id: builtins.str,
    auto_delete_on_idle: typing.Optional[builtins.str] = None,
    batched_operations_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dead_lettering_on_message_expiration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_message_ttl: typing.Optional[builtins.str] = None,
    duplicate_detection_history_time_window: typing.Optional[builtins.str] = None,
    express_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forward_dead_lettered_messages_to: typing.Optional[builtins.str] = None,
    forward_to: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    lock_duration: typing.Optional[builtins.str] = None,
    max_delivery_count: typing.Optional[jsii.Number] = None,
    max_message_size_in_kilobytes: typing.Optional[jsii.Number] = None,
    max_size_in_megabytes: typing.Optional[jsii.Number] = None,
    partitioning_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    requires_duplicate_detection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    requires_session: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ServicebusQueueTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51579fcfb08ef43fc4f87a287b0f6ac35b4043f3ca86c47448eed616416d31bb(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecda01d5cc6a5079e96fa4eccabb005554e386f567f38a76f529743a028355f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e710307878a00826651a2c125fe84b761389f62a25a1b7e51da493af4b47e6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90546aba41893edfb2aadc931d4de1fb4ba8b0a384632a7cc40104ba38d9483(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3febe8c4c3a6b3386496ae5b046eb54704589ca446d56254fae89157ddf8419(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88d8f3f92d5afe0997ccd337d7166e5198eaeee0f807ae50035811cd5c35b37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b5660ee7f88141280108bc1cb3a7d24e70b3f5047e829f81de8b8ed2c9123c5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServicebusQueueTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
