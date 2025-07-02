r'''
# `azurerm_servicebus_subscription`

Refer to the Terraform Registry for docs: [`azurerm_servicebus_subscription`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription).
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


class ServicebusSubscription(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.servicebusSubscription.ServicebusSubscription",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription azurerm_servicebus_subscription}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        max_delivery_count: jsii.Number,
        name: builtins.str,
        topic_id: builtins.str,
        auto_delete_on_idle: typing.Optional[builtins.str] = None,
        batched_operations_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_scoped_subscription: typing.Optional[typing.Union["ServicebusSubscriptionClientScopedSubscription", typing.Dict[builtins.str, typing.Any]]] = None,
        client_scoped_subscription_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dead_lettering_on_filter_evaluation_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dead_lettering_on_message_expiration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_message_ttl: typing.Optional[builtins.str] = None,
        forward_dead_lettered_messages_to: typing.Optional[builtins.str] = None,
        forward_to: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lock_duration: typing.Optional[builtins.str] = None,
        requires_session: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ServicebusSubscriptionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription azurerm_servicebus_subscription} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param max_delivery_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#max_delivery_count ServicebusSubscription#max_delivery_count}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#name ServicebusSubscription#name}.
        :param topic_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#topic_id ServicebusSubscription#topic_id}.
        :param auto_delete_on_idle: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#auto_delete_on_idle ServicebusSubscription#auto_delete_on_idle}.
        :param batched_operations_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#batched_operations_enabled ServicebusSubscription#batched_operations_enabled}.
        :param client_scoped_subscription: client_scoped_subscription block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#client_scoped_subscription ServicebusSubscription#client_scoped_subscription}
        :param client_scoped_subscription_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#client_scoped_subscription_enabled ServicebusSubscription#client_scoped_subscription_enabled}.
        :param dead_lettering_on_filter_evaluation_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#dead_lettering_on_filter_evaluation_error ServicebusSubscription#dead_lettering_on_filter_evaluation_error}.
        :param dead_lettering_on_message_expiration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#dead_lettering_on_message_expiration ServicebusSubscription#dead_lettering_on_message_expiration}.
        :param default_message_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#default_message_ttl ServicebusSubscription#default_message_ttl}.
        :param forward_dead_lettered_messages_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#forward_dead_lettered_messages_to ServicebusSubscription#forward_dead_lettered_messages_to}.
        :param forward_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#forward_to ServicebusSubscription#forward_to}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#id ServicebusSubscription#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lock_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#lock_duration ServicebusSubscription#lock_duration}.
        :param requires_session: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#requires_session ServicebusSubscription#requires_session}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#status ServicebusSubscription#status}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#timeouts ServicebusSubscription#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a64fc2856ff506217a437fa18c9c7bacf640e199bd247cc0e03d0af46592bf40)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ServicebusSubscriptionConfig(
            max_delivery_count=max_delivery_count,
            name=name,
            topic_id=topic_id,
            auto_delete_on_idle=auto_delete_on_idle,
            batched_operations_enabled=batched_operations_enabled,
            client_scoped_subscription=client_scoped_subscription,
            client_scoped_subscription_enabled=client_scoped_subscription_enabled,
            dead_lettering_on_filter_evaluation_error=dead_lettering_on_filter_evaluation_error,
            dead_lettering_on_message_expiration=dead_lettering_on_message_expiration,
            default_message_ttl=default_message_ttl,
            forward_dead_lettered_messages_to=forward_dead_lettered_messages_to,
            forward_to=forward_to,
            id=id,
            lock_duration=lock_duration,
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
        '''Generates CDKTF code for importing a ServicebusSubscription resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ServicebusSubscription to import.
        :param import_from_id: The id of the existing ServicebusSubscription that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ServicebusSubscription to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d2b04142583223b4aa83233f3f0e2fd4e66c975b938c864a2ec5d1834953deb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putClientScopedSubscription")
    def put_client_scoped_subscription(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        is_client_scoped_subscription_shareable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#client_id ServicebusSubscription#client_id}.
        :param is_client_scoped_subscription_shareable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#is_client_scoped_subscription_shareable ServicebusSubscription#is_client_scoped_subscription_shareable}.
        '''
        value = ServicebusSubscriptionClientScopedSubscription(
            client_id=client_id,
            is_client_scoped_subscription_shareable=is_client_scoped_subscription_shareable,
        )

        return typing.cast(None, jsii.invoke(self, "putClientScopedSubscription", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#create ServicebusSubscription#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#delete ServicebusSubscription#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#read ServicebusSubscription#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#update ServicebusSubscription#update}.
        '''
        value = ServicebusSubscriptionTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAutoDeleteOnIdle")
    def reset_auto_delete_on_idle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoDeleteOnIdle", []))

    @jsii.member(jsii_name="resetBatchedOperationsEnabled")
    def reset_batched_operations_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchedOperationsEnabled", []))

    @jsii.member(jsii_name="resetClientScopedSubscription")
    def reset_client_scoped_subscription(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientScopedSubscription", []))

    @jsii.member(jsii_name="resetClientScopedSubscriptionEnabled")
    def reset_client_scoped_subscription_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientScopedSubscriptionEnabled", []))

    @jsii.member(jsii_name="resetDeadLetteringOnFilterEvaluationError")
    def reset_dead_lettering_on_filter_evaluation_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeadLetteringOnFilterEvaluationError", []))

    @jsii.member(jsii_name="resetDeadLetteringOnMessageExpiration")
    def reset_dead_lettering_on_message_expiration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeadLetteringOnMessageExpiration", []))

    @jsii.member(jsii_name="resetDefaultMessageTtl")
    def reset_default_message_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultMessageTtl", []))

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
    @jsii.member(jsii_name="clientScopedSubscription")
    def client_scoped_subscription(
        self,
    ) -> "ServicebusSubscriptionClientScopedSubscriptionOutputReference":
        return typing.cast("ServicebusSubscriptionClientScopedSubscriptionOutputReference", jsii.get(self, "clientScopedSubscription"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ServicebusSubscriptionTimeoutsOutputReference":
        return typing.cast("ServicebusSubscriptionTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    @jsii.member(jsii_name="clientScopedSubscriptionEnabledInput")
    def client_scoped_subscription_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "clientScopedSubscriptionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="clientScopedSubscriptionInput")
    def client_scoped_subscription_input(
        self,
    ) -> typing.Optional["ServicebusSubscriptionClientScopedSubscription"]:
        return typing.cast(typing.Optional["ServicebusSubscriptionClientScopedSubscription"], jsii.get(self, "clientScopedSubscriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="deadLetteringOnFilterEvaluationErrorInput")
    def dead_lettering_on_filter_evaluation_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deadLetteringOnFilterEvaluationErrorInput"))

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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ServicebusSubscriptionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ServicebusSubscriptionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="topicIdInput")
    def topic_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicIdInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDeleteOnIdle")
    def auto_delete_on_idle(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoDeleteOnIdle"))

    @auto_delete_on_idle.setter
    def auto_delete_on_idle(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__444483b2423c1655baf0c54ab74c69e8cf04954b588fec2485993359212631f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e48b98a44449bdfbb6f9d0029a3fef42744b20e402ae44db03edaffdde00ae2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchedOperationsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientScopedSubscriptionEnabled")
    def client_scoped_subscription_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "clientScopedSubscriptionEnabled"))

    @client_scoped_subscription_enabled.setter
    def client_scoped_subscription_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d44b5673868cbc207bbe1c74dea9c55f1d4395f3897dbfb2cc7ac7d4cc2df9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientScopedSubscriptionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deadLetteringOnFilterEvaluationError")
    def dead_lettering_on_filter_evaluation_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deadLetteringOnFilterEvaluationError"))

    @dead_lettering_on_filter_evaluation_error.setter
    def dead_lettering_on_filter_evaluation_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae467e00e164f9f5a95da34568e2a09bfedb8989546378fab70106169b317c98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deadLetteringOnFilterEvaluationError", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__0a4aac1b0e4389fa6312971397ab23447c7cd78e0f154385f171204cdeb13d7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deadLetteringOnMessageExpiration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultMessageTtl")
    def default_message_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultMessageTtl"))

    @default_message_ttl.setter
    def default_message_ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3841401869902e595a701120ace40944e324ee1c617f20cd599e12ad8fa1352f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultMessageTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardDeadLetteredMessagesTo")
    def forward_dead_lettered_messages_to(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardDeadLetteredMessagesTo"))

    @forward_dead_lettered_messages_to.setter
    def forward_dead_lettered_messages_to(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cd48f406a84ff7c273e887d3203c84ef71fa316a412a7d974db4521ab2fdb7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardDeadLetteredMessagesTo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardTo")
    def forward_to(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardTo"))

    @forward_to.setter
    def forward_to(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3f3b97a2e7661f3875b1e9162a6f669f01d4f1e7d2689276e473f20e2bb1ded)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardTo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e36b443084fe5ac36c589853f25c3c7ac894a60551168eb47ba6fc09fa31d6e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lockDuration")
    def lock_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lockDuration"))

    @lock_duration.setter
    def lock_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0113435f97836488b0e7472574a36862d890969e35699cdbb88322600aca7dc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lockDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDeliveryCount")
    def max_delivery_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDeliveryCount"))

    @max_delivery_count.setter
    def max_delivery_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__503625be283c3dfd8720ba1619cb3694e1a0b16f528df1540314ea30c238f2f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDeliveryCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1eaa7b6864b22ae75819889556ca7ca390d14dcd88d78ce2d53cafcc77b139d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__6c54c80c4b615721c3ff14282f8312908e891df9f8a3a3573e650f91ac283ec6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requiresSession", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1d889d06972394781d5a19e817a760c9cd8160d8006e21cd18e2db90176bf87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topicId")
    def topic_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topicId"))

    @topic_id.setter
    def topic_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fefedb629f508b729021c0fc5406fccf5df8448bd16af3915b02fdd5eda4609)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topicId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.servicebusSubscription.ServicebusSubscriptionClientScopedSubscription",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "is_client_scoped_subscription_shareable": "isClientScopedSubscriptionShareable",
    },
)
class ServicebusSubscriptionClientScopedSubscription:
    def __init__(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        is_client_scoped_subscription_shareable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#client_id ServicebusSubscription#client_id}.
        :param is_client_scoped_subscription_shareable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#is_client_scoped_subscription_shareable ServicebusSubscription#is_client_scoped_subscription_shareable}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ed633b1cfc644aa4023a4399e0af7a88545996a532a3a9fc7121c39812dfa1a)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument is_client_scoped_subscription_shareable", value=is_client_scoped_subscription_shareable, expected_type=type_hints["is_client_scoped_subscription_shareable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_id is not None:
            self._values["client_id"] = client_id
        if is_client_scoped_subscription_shareable is not None:
            self._values["is_client_scoped_subscription_shareable"] = is_client_scoped_subscription_shareable

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#client_id ServicebusSubscription#client_id}.'''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_client_scoped_subscription_shareable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#is_client_scoped_subscription_shareable ServicebusSubscription#is_client_scoped_subscription_shareable}.'''
        result = self._values.get("is_client_scoped_subscription_shareable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServicebusSubscriptionClientScopedSubscription(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServicebusSubscriptionClientScopedSubscriptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.servicebusSubscription.ServicebusSubscriptionClientScopedSubscriptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__872973b32867a7bf75cdef879eef2d743dcf7eff73360725659e2220084b8b76)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetIsClientScopedSubscriptionShareable")
    def reset_is_client_scoped_subscription_shareable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsClientScopedSubscriptionShareable", []))

    @builtins.property
    @jsii.member(jsii_name="isClientScopedSubscriptionDurable")
    def is_client_scoped_subscription_durable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isClientScopedSubscriptionDurable"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="isClientScopedSubscriptionShareableInput")
    def is_client_scoped_subscription_shareable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isClientScopedSubscriptionShareableInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12ef6fa849c1231b291aeb704d7bbcca3d13148502635dfc25ff2890e1dc7fd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isClientScopedSubscriptionShareable")
    def is_client_scoped_subscription_shareable(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isClientScopedSubscriptionShareable"))

    @is_client_scoped_subscription_shareable.setter
    def is_client_scoped_subscription_shareable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcaefa6ae96d6ef22dfc90161864a53c0919a79683ff93ad35c61684b8f5e89b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isClientScopedSubscriptionShareable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServicebusSubscriptionClientScopedSubscription]:
        return typing.cast(typing.Optional[ServicebusSubscriptionClientScopedSubscription], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServicebusSubscriptionClientScopedSubscription],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b87a2825973ddf6e3c051265845d954072a16cfcf2b8d3d346cea883e5f905bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.servicebusSubscription.ServicebusSubscriptionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "max_delivery_count": "maxDeliveryCount",
        "name": "name",
        "topic_id": "topicId",
        "auto_delete_on_idle": "autoDeleteOnIdle",
        "batched_operations_enabled": "batchedOperationsEnabled",
        "client_scoped_subscription": "clientScopedSubscription",
        "client_scoped_subscription_enabled": "clientScopedSubscriptionEnabled",
        "dead_lettering_on_filter_evaluation_error": "deadLetteringOnFilterEvaluationError",
        "dead_lettering_on_message_expiration": "deadLetteringOnMessageExpiration",
        "default_message_ttl": "defaultMessageTtl",
        "forward_dead_lettered_messages_to": "forwardDeadLetteredMessagesTo",
        "forward_to": "forwardTo",
        "id": "id",
        "lock_duration": "lockDuration",
        "requires_session": "requiresSession",
        "status": "status",
        "timeouts": "timeouts",
    },
)
class ServicebusSubscriptionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        max_delivery_count: jsii.Number,
        name: builtins.str,
        topic_id: builtins.str,
        auto_delete_on_idle: typing.Optional[builtins.str] = None,
        batched_operations_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_scoped_subscription: typing.Optional[typing.Union[ServicebusSubscriptionClientScopedSubscription, typing.Dict[builtins.str, typing.Any]]] = None,
        client_scoped_subscription_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dead_lettering_on_filter_evaluation_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dead_lettering_on_message_expiration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_message_ttl: typing.Optional[builtins.str] = None,
        forward_dead_lettered_messages_to: typing.Optional[builtins.str] = None,
        forward_to: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lock_duration: typing.Optional[builtins.str] = None,
        requires_session: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ServicebusSubscriptionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param max_delivery_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#max_delivery_count ServicebusSubscription#max_delivery_count}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#name ServicebusSubscription#name}.
        :param topic_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#topic_id ServicebusSubscription#topic_id}.
        :param auto_delete_on_idle: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#auto_delete_on_idle ServicebusSubscription#auto_delete_on_idle}.
        :param batched_operations_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#batched_operations_enabled ServicebusSubscription#batched_operations_enabled}.
        :param client_scoped_subscription: client_scoped_subscription block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#client_scoped_subscription ServicebusSubscription#client_scoped_subscription}
        :param client_scoped_subscription_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#client_scoped_subscription_enabled ServicebusSubscription#client_scoped_subscription_enabled}.
        :param dead_lettering_on_filter_evaluation_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#dead_lettering_on_filter_evaluation_error ServicebusSubscription#dead_lettering_on_filter_evaluation_error}.
        :param dead_lettering_on_message_expiration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#dead_lettering_on_message_expiration ServicebusSubscription#dead_lettering_on_message_expiration}.
        :param default_message_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#default_message_ttl ServicebusSubscription#default_message_ttl}.
        :param forward_dead_lettered_messages_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#forward_dead_lettered_messages_to ServicebusSubscription#forward_dead_lettered_messages_to}.
        :param forward_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#forward_to ServicebusSubscription#forward_to}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#id ServicebusSubscription#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lock_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#lock_duration ServicebusSubscription#lock_duration}.
        :param requires_session: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#requires_session ServicebusSubscription#requires_session}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#status ServicebusSubscription#status}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#timeouts ServicebusSubscription#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(client_scoped_subscription, dict):
            client_scoped_subscription = ServicebusSubscriptionClientScopedSubscription(**client_scoped_subscription)
        if isinstance(timeouts, dict):
            timeouts = ServicebusSubscriptionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8a14110a9d24c4a298720bfd08b310b283a042be5e0bce1b20e2ae66e0e9cfa)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument max_delivery_count", value=max_delivery_count, expected_type=type_hints["max_delivery_count"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument topic_id", value=topic_id, expected_type=type_hints["topic_id"])
            check_type(argname="argument auto_delete_on_idle", value=auto_delete_on_idle, expected_type=type_hints["auto_delete_on_idle"])
            check_type(argname="argument batched_operations_enabled", value=batched_operations_enabled, expected_type=type_hints["batched_operations_enabled"])
            check_type(argname="argument client_scoped_subscription", value=client_scoped_subscription, expected_type=type_hints["client_scoped_subscription"])
            check_type(argname="argument client_scoped_subscription_enabled", value=client_scoped_subscription_enabled, expected_type=type_hints["client_scoped_subscription_enabled"])
            check_type(argname="argument dead_lettering_on_filter_evaluation_error", value=dead_lettering_on_filter_evaluation_error, expected_type=type_hints["dead_lettering_on_filter_evaluation_error"])
            check_type(argname="argument dead_lettering_on_message_expiration", value=dead_lettering_on_message_expiration, expected_type=type_hints["dead_lettering_on_message_expiration"])
            check_type(argname="argument default_message_ttl", value=default_message_ttl, expected_type=type_hints["default_message_ttl"])
            check_type(argname="argument forward_dead_lettered_messages_to", value=forward_dead_lettered_messages_to, expected_type=type_hints["forward_dead_lettered_messages_to"])
            check_type(argname="argument forward_to", value=forward_to, expected_type=type_hints["forward_to"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lock_duration", value=lock_duration, expected_type=type_hints["lock_duration"])
            check_type(argname="argument requires_session", value=requires_session, expected_type=type_hints["requires_session"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_delivery_count": max_delivery_count,
            "name": name,
            "topic_id": topic_id,
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
        if client_scoped_subscription is not None:
            self._values["client_scoped_subscription"] = client_scoped_subscription
        if client_scoped_subscription_enabled is not None:
            self._values["client_scoped_subscription_enabled"] = client_scoped_subscription_enabled
        if dead_lettering_on_filter_evaluation_error is not None:
            self._values["dead_lettering_on_filter_evaluation_error"] = dead_lettering_on_filter_evaluation_error
        if dead_lettering_on_message_expiration is not None:
            self._values["dead_lettering_on_message_expiration"] = dead_lettering_on_message_expiration
        if default_message_ttl is not None:
            self._values["default_message_ttl"] = default_message_ttl
        if forward_dead_lettered_messages_to is not None:
            self._values["forward_dead_lettered_messages_to"] = forward_dead_lettered_messages_to
        if forward_to is not None:
            self._values["forward_to"] = forward_to
        if id is not None:
            self._values["id"] = id
        if lock_duration is not None:
            self._values["lock_duration"] = lock_duration
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
    def max_delivery_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#max_delivery_count ServicebusSubscription#max_delivery_count}.'''
        result = self._values.get("max_delivery_count")
        assert result is not None, "Required property 'max_delivery_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#name ServicebusSubscription#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#topic_id ServicebusSubscription#topic_id}.'''
        result = self._values.get("topic_id")
        assert result is not None, "Required property 'topic_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_delete_on_idle(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#auto_delete_on_idle ServicebusSubscription#auto_delete_on_idle}.'''
        result = self._values.get("auto_delete_on_idle")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def batched_operations_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#batched_operations_enabled ServicebusSubscription#batched_operations_enabled}.'''
        result = self._values.get("batched_operations_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_scoped_subscription(
        self,
    ) -> typing.Optional[ServicebusSubscriptionClientScopedSubscription]:
        '''client_scoped_subscription block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#client_scoped_subscription ServicebusSubscription#client_scoped_subscription}
        '''
        result = self._values.get("client_scoped_subscription")
        return typing.cast(typing.Optional[ServicebusSubscriptionClientScopedSubscription], result)

    @builtins.property
    def client_scoped_subscription_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#client_scoped_subscription_enabled ServicebusSubscription#client_scoped_subscription_enabled}.'''
        result = self._values.get("client_scoped_subscription_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dead_lettering_on_filter_evaluation_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#dead_lettering_on_filter_evaluation_error ServicebusSubscription#dead_lettering_on_filter_evaluation_error}.'''
        result = self._values.get("dead_lettering_on_filter_evaluation_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dead_lettering_on_message_expiration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#dead_lettering_on_message_expiration ServicebusSubscription#dead_lettering_on_message_expiration}.'''
        result = self._values.get("dead_lettering_on_message_expiration")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def default_message_ttl(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#default_message_ttl ServicebusSubscription#default_message_ttl}.'''
        result = self._values.get("default_message_ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def forward_dead_lettered_messages_to(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#forward_dead_lettered_messages_to ServicebusSubscription#forward_dead_lettered_messages_to}.'''
        result = self._values.get("forward_dead_lettered_messages_to")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def forward_to(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#forward_to ServicebusSubscription#forward_to}.'''
        result = self._values.get("forward_to")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#id ServicebusSubscription#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lock_duration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#lock_duration ServicebusSubscription#lock_duration}.'''
        result = self._values.get("lock_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def requires_session(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#requires_session ServicebusSubscription#requires_session}.'''
        result = self._values.get("requires_session")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#status ServicebusSubscription#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ServicebusSubscriptionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#timeouts ServicebusSubscription#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ServicebusSubscriptionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServicebusSubscriptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.servicebusSubscription.ServicebusSubscriptionTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ServicebusSubscriptionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#create ServicebusSubscription#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#delete ServicebusSubscription#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#read ServicebusSubscription#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#update ServicebusSubscription#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5294849270dcb1e4d8ad16e436f3c52573502b5dfb0d7acad5e0160b6a1d86f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#create ServicebusSubscription#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#delete ServicebusSubscription#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#read ServicebusSubscription#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/servicebus_subscription#update ServicebusSubscription#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServicebusSubscriptionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServicebusSubscriptionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.servicebusSubscription.ServicebusSubscriptionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2a41342da8f9a84ed385d9b0f71a6e8bc6cbcbd8536175570adeeddf373b4d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86ec5f6e4b688d0fac21a69ade43c8c0efdbaad6cdda22683f56ca07a72e3c18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47cabb9890b3ed4e5539ac61740026366a12b60259db9658fe2491cb32e0b1a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98cb5886ccb88dcc3546276a22008ba6407748ff13a140170526e9b62554b83c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76d62a37721ac8b630a99829642a726620acd626f5e55c89bfb717019be640a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServicebusSubscriptionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServicebusSubscriptionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServicebusSubscriptionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f5537aeeeb38db3b7173fc694538e1a68745477a473471453493473dfa3eea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ServicebusSubscription",
    "ServicebusSubscriptionClientScopedSubscription",
    "ServicebusSubscriptionClientScopedSubscriptionOutputReference",
    "ServicebusSubscriptionConfig",
    "ServicebusSubscriptionTimeouts",
    "ServicebusSubscriptionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a64fc2856ff506217a437fa18c9c7bacf640e199bd247cc0e03d0af46592bf40(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    max_delivery_count: jsii.Number,
    name: builtins.str,
    topic_id: builtins.str,
    auto_delete_on_idle: typing.Optional[builtins.str] = None,
    batched_operations_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_scoped_subscription: typing.Optional[typing.Union[ServicebusSubscriptionClientScopedSubscription, typing.Dict[builtins.str, typing.Any]]] = None,
    client_scoped_subscription_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dead_lettering_on_filter_evaluation_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dead_lettering_on_message_expiration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_message_ttl: typing.Optional[builtins.str] = None,
    forward_dead_lettered_messages_to: typing.Optional[builtins.str] = None,
    forward_to: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    lock_duration: typing.Optional[builtins.str] = None,
    requires_session: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ServicebusSubscriptionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__5d2b04142583223b4aa83233f3f0e2fd4e66c975b938c864a2ec5d1834953deb(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__444483b2423c1655baf0c54ab74c69e8cf04954b588fec2485993359212631f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e48b98a44449bdfbb6f9d0029a3fef42744b20e402ae44db03edaffdde00ae2b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d44b5673868cbc207bbe1c74dea9c55f1d4395f3897dbfb2cc7ac7d4cc2df9c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae467e00e164f9f5a95da34568e2a09bfedb8989546378fab70106169b317c98(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4aac1b0e4389fa6312971397ab23447c7cd78e0f154385f171204cdeb13d7b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3841401869902e595a701120ace40944e324ee1c617f20cd599e12ad8fa1352f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cd48f406a84ff7c273e887d3203c84ef71fa316a412a7d974db4521ab2fdb7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f3b97a2e7661f3875b1e9162a6f669f01d4f1e7d2689276e473f20e2bb1ded(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e36b443084fe5ac36c589853f25c3c7ac894a60551168eb47ba6fc09fa31d6e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0113435f97836488b0e7472574a36862d890969e35699cdbb88322600aca7dc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__503625be283c3dfd8720ba1619cb3694e1a0b16f528df1540314ea30c238f2f3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1eaa7b6864b22ae75819889556ca7ca390d14dcd88d78ce2d53cafcc77b139d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c54c80c4b615721c3ff14282f8312908e891df9f8a3a3573e650f91ac283ec6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1d889d06972394781d5a19e817a760c9cd8160d8006e21cd18e2db90176bf87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fefedb629f508b729021c0fc5406fccf5df8448bd16af3915b02fdd5eda4609(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed633b1cfc644aa4023a4399e0af7a88545996a532a3a9fc7121c39812dfa1a(
    *,
    client_id: typing.Optional[builtins.str] = None,
    is_client_scoped_subscription_shareable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__872973b32867a7bf75cdef879eef2d743dcf7eff73360725659e2220084b8b76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ef6fa849c1231b291aeb704d7bbcca3d13148502635dfc25ff2890e1dc7fd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcaefa6ae96d6ef22dfc90161864a53c0919a79683ff93ad35c61684b8f5e89b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b87a2825973ddf6e3c051265845d954072a16cfcf2b8d3d346cea883e5f905bc(
    value: typing.Optional[ServicebusSubscriptionClientScopedSubscription],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a14110a9d24c4a298720bfd08b310b283a042be5e0bce1b20e2ae66e0e9cfa(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    max_delivery_count: jsii.Number,
    name: builtins.str,
    topic_id: builtins.str,
    auto_delete_on_idle: typing.Optional[builtins.str] = None,
    batched_operations_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_scoped_subscription: typing.Optional[typing.Union[ServicebusSubscriptionClientScopedSubscription, typing.Dict[builtins.str, typing.Any]]] = None,
    client_scoped_subscription_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dead_lettering_on_filter_evaluation_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dead_lettering_on_message_expiration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_message_ttl: typing.Optional[builtins.str] = None,
    forward_dead_lettered_messages_to: typing.Optional[builtins.str] = None,
    forward_to: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    lock_duration: typing.Optional[builtins.str] = None,
    requires_session: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ServicebusSubscriptionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5294849270dcb1e4d8ad16e436f3c52573502b5dfb0d7acad5e0160b6a1d86f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2a41342da8f9a84ed385d9b0f71a6e8bc6cbcbd8536175570adeeddf373b4d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ec5f6e4b688d0fac21a69ade43c8c0efdbaad6cdda22683f56ca07a72e3c18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47cabb9890b3ed4e5539ac61740026366a12b60259db9658fe2491cb32e0b1a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98cb5886ccb88dcc3546276a22008ba6407748ff13a140170526e9b62554b83c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d62a37721ac8b630a99829642a726620acd626f5e55c89bfb717019be640a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f5537aeeeb38db3b7173fc694538e1a68745477a473471453493473dfa3eea1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServicebusSubscriptionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
