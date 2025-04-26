r'''
# `snowflake_resource_monitor`

Refer to the Terraform Registry for docs: [`snowflake_resource_monitor`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor).
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


class ResourceMonitor(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.resourceMonitor.ResourceMonitor",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor snowflake_resource_monitor}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        credit_quota: typing.Optional[jsii.Number] = None,
        end_timestamp: typing.Optional[builtins.str] = None,
        frequency: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        notify_triggers: typing.Optional[typing.Sequence[jsii.Number]] = None,
        notify_users: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_timestamp: typing.Optional[builtins.str] = None,
        suspend_immediate_trigger: typing.Optional[jsii.Number] = None,
        suspend_trigger: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor snowflake_resource_monitor} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Identifier for the resource monitor; must be unique for your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#name ResourceMonitor#name}
        :param credit_quota: The number of credits allocated to the resource monitor per frequency interval. When total usage for all warehouses assigned to the monitor reaches this number for the current frequency interval, the resource monitor is considered to be at 100% of quota. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#credit_quota ResourceMonitor#credit_quota}
        :param end_timestamp: The date and time when the resource monitor suspends the assigned warehouses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#end_timestamp ResourceMonitor#end_timestamp}
        :param frequency: The frequency interval at which the credit usage resets to 0. Valid values are (case-insensitive): ``MONTHLY`` | ``DAILY`` | ``WEEKLY`` | ``YEARLY`` | ``NEVER``. If you set a ``frequency`` for a resource monitor, you must also set ``start_timestamp``. If you specify ``NEVER`` for the frequency, the credit usage for the warehouse does not reset. After removing this field from the config, the previously set value will be preserved on the Snowflake side, not the default value. That's due to Snowflake limitation and the lack of unset functionality for this parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#frequency ResourceMonitor#frequency}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#id ResourceMonitor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notify_triggers: Specifies a list of percentages of the credit quota. After reaching any of the values the users passed in the notify_users field will be notified (to receive the notification they should have notifications enabled). Values over 100 are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#notify_triggers ResourceMonitor#notify_triggers}
        :param notify_users: Specifies the list of users (their identifiers) to receive email notifications on resource monitors. For more information about this resource, see `docs <./user>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#notify_users ResourceMonitor#notify_users}
        :param start_timestamp: The date and time when the resource monitor starts monitoring credit usage for the assigned warehouses. If you set a ``start_timestamp`` for a resource monitor, you must also set ``frequency``. After removing this field from the config, the previously set value will be preserved on the Snowflake side, not the default value. That's due to Snowflake limitation and the lack of unset functionality for this parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#start_timestamp ResourceMonitor#start_timestamp}
        :param suspend_immediate_trigger: Represents a numeric value specified as a percentage of the credit quota. Values over 100 are supported. After reaching this value, all assigned warehouses immediately cancel any currently running queries or statements. In addition, this action sends a notification to all users who have enabled notifications for themselves. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#suspend_immediate_trigger ResourceMonitor#suspend_immediate_trigger}
        :param suspend_trigger: Represents a numeric value specified as a percentage of the credit quota. Values over 100 are supported. After reaching this value, all assigned warehouses while allowing currently running queries to complete will be suspended. No new queries can be executed by the warehouses until the credit quota for the resource monitor is increased. In addition, this action sends a notification to all users who have enabled notifications for themselves. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#suspend_trigger ResourceMonitor#suspend_trigger}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b43a9f295b51125a0dc341a3552580e5e5ddea1e35a3201e8b54a8ca99f95b21)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ResourceMonitorConfig(
            name=name,
            credit_quota=credit_quota,
            end_timestamp=end_timestamp,
            frequency=frequency,
            id=id,
            notify_triggers=notify_triggers,
            notify_users=notify_users,
            start_timestamp=start_timestamp,
            suspend_immediate_trigger=suspend_immediate_trigger,
            suspend_trigger=suspend_trigger,
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
        '''Generates CDKTF code for importing a ResourceMonitor resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ResourceMonitor to import.
        :param import_from_id: The id of the existing ResourceMonitor that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ResourceMonitor to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ac9f9f7b342306213d834c3bec854cfb26029b5439a1a7369a1f69f8ce54cb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetCreditQuota")
    def reset_credit_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreditQuota", []))

    @jsii.member(jsii_name="resetEndTimestamp")
    def reset_end_timestamp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndTimestamp", []))

    @jsii.member(jsii_name="resetFrequency")
    def reset_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrequency", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNotifyTriggers")
    def reset_notify_triggers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotifyTriggers", []))

    @jsii.member(jsii_name="resetNotifyUsers")
    def reset_notify_users(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotifyUsers", []))

    @jsii.member(jsii_name="resetStartTimestamp")
    def reset_start_timestamp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTimestamp", []))

    @jsii.member(jsii_name="resetSuspendImmediateTrigger")
    def reset_suspend_immediate_trigger(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuspendImmediateTrigger", []))

    @jsii.member(jsii_name="resetSuspendTrigger")
    def reset_suspend_trigger(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuspendTrigger", []))

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
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "ResourceMonitorShowOutputList":
        return typing.cast("ResourceMonitorShowOutputList", jsii.get(self, "showOutput"))

    @builtins.property
    @jsii.member(jsii_name="creditQuotaInput")
    def credit_quota_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "creditQuotaInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimestampInput")
    def end_timestamp_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimestampInput"))

    @builtins.property
    @jsii.member(jsii_name="frequencyInput")
    def frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="notifyTriggersInput")
    def notify_triggers_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "notifyTriggersInput"))

    @builtins.property
    @jsii.member(jsii_name="notifyUsersInput")
    def notify_users_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notifyUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimestampInput")
    def start_timestamp_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimestampInput"))

    @builtins.property
    @jsii.member(jsii_name="suspendImmediateTriggerInput")
    def suspend_immediate_trigger_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "suspendImmediateTriggerInput"))

    @builtins.property
    @jsii.member(jsii_name="suspendTriggerInput")
    def suspend_trigger_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "suspendTriggerInput"))

    @builtins.property
    @jsii.member(jsii_name="creditQuota")
    def credit_quota(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "creditQuota"))

    @credit_quota.setter
    def credit_quota(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96602caff2c16f75fbba74de405c9c77824284c81393b6f5f5f0bd94ff45eb2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "creditQuota", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endTimestamp")
    def end_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTimestamp"))

    @end_timestamp.setter
    def end_timestamp(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3d7deb08041c42bce10f40e8038f28d35285a8bb382453400460d82e154451b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTimestamp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequency"))

    @frequency.setter
    def frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__894cd8cacad81cb91f6065b680e30ed3fd543495844a290d7e48e437bb9e33e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9021990c2b184ed0e466635c380fd5a3c070de8dfabcc0b7aea239761b88aa25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24041f919aedf240169256de40993fa94cd711ddc7717db3b69846ccdeacbc5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notifyTriggers")
    def notify_triggers(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "notifyTriggers"))

    @notify_triggers.setter
    def notify_triggers(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d335b3aacc03c9c38bda997dbddd1fabd0d813654d995556ba749cd16d265704)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifyTriggers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notifyUsers")
    def notify_users(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notifyUsers"))

    @notify_users.setter
    def notify_users(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bfaa7d35d7c8a7c7429628e363ed1bef8587571e67236057805a18f0b5cf6d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifyUsers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTimestamp")
    def start_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTimestamp"))

    @start_timestamp.setter
    def start_timestamp(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__638ac1a05fbd330d55c7d6bee7e08ddb584718264bf2cf67d407684acca021ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTimestamp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suspendImmediateTrigger")
    def suspend_immediate_trigger(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "suspendImmediateTrigger"))

    @suspend_immediate_trigger.setter
    def suspend_immediate_trigger(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba2cd17ae14b1bc8055e0c64a036f7e5f64ec56b456658f715cb78a1534a5ed7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspendImmediateTrigger", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suspendTrigger")
    def suspend_trigger(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "suspendTrigger"))

    @suspend_trigger.setter
    def suspend_trigger(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4368be39ac9dc9595e4501cadf1781e002027363a968efbf717125766f3ffb2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspendTrigger", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.resourceMonitor.ResourceMonitorConfig",
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
        "credit_quota": "creditQuota",
        "end_timestamp": "endTimestamp",
        "frequency": "frequency",
        "id": "id",
        "notify_triggers": "notifyTriggers",
        "notify_users": "notifyUsers",
        "start_timestamp": "startTimestamp",
        "suspend_immediate_trigger": "suspendImmediateTrigger",
        "suspend_trigger": "suspendTrigger",
    },
)
class ResourceMonitorConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        credit_quota: typing.Optional[jsii.Number] = None,
        end_timestamp: typing.Optional[builtins.str] = None,
        frequency: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        notify_triggers: typing.Optional[typing.Sequence[jsii.Number]] = None,
        notify_users: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_timestamp: typing.Optional[builtins.str] = None,
        suspend_immediate_trigger: typing.Optional[jsii.Number] = None,
        suspend_trigger: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Identifier for the resource monitor; must be unique for your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#name ResourceMonitor#name}
        :param credit_quota: The number of credits allocated to the resource monitor per frequency interval. When total usage for all warehouses assigned to the monitor reaches this number for the current frequency interval, the resource monitor is considered to be at 100% of quota. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#credit_quota ResourceMonitor#credit_quota}
        :param end_timestamp: The date and time when the resource monitor suspends the assigned warehouses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#end_timestamp ResourceMonitor#end_timestamp}
        :param frequency: The frequency interval at which the credit usage resets to 0. Valid values are (case-insensitive): ``MONTHLY`` | ``DAILY`` | ``WEEKLY`` | ``YEARLY`` | ``NEVER``. If you set a ``frequency`` for a resource monitor, you must also set ``start_timestamp``. If you specify ``NEVER`` for the frequency, the credit usage for the warehouse does not reset. After removing this field from the config, the previously set value will be preserved on the Snowflake side, not the default value. That's due to Snowflake limitation and the lack of unset functionality for this parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#frequency ResourceMonitor#frequency}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#id ResourceMonitor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notify_triggers: Specifies a list of percentages of the credit quota. After reaching any of the values the users passed in the notify_users field will be notified (to receive the notification they should have notifications enabled). Values over 100 are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#notify_triggers ResourceMonitor#notify_triggers}
        :param notify_users: Specifies the list of users (their identifiers) to receive email notifications on resource monitors. For more information about this resource, see `docs <./user>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#notify_users ResourceMonitor#notify_users}
        :param start_timestamp: The date and time when the resource monitor starts monitoring credit usage for the assigned warehouses. If you set a ``start_timestamp`` for a resource monitor, you must also set ``frequency``. After removing this field from the config, the previously set value will be preserved on the Snowflake side, not the default value. That's due to Snowflake limitation and the lack of unset functionality for this parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#start_timestamp ResourceMonitor#start_timestamp}
        :param suspend_immediate_trigger: Represents a numeric value specified as a percentage of the credit quota. Values over 100 are supported. After reaching this value, all assigned warehouses immediately cancel any currently running queries or statements. In addition, this action sends a notification to all users who have enabled notifications for themselves. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#suspend_immediate_trigger ResourceMonitor#suspend_immediate_trigger}
        :param suspend_trigger: Represents a numeric value specified as a percentage of the credit quota. Values over 100 are supported. After reaching this value, all assigned warehouses while allowing currently running queries to complete will be suspended. No new queries can be executed by the warehouses until the credit quota for the resource monitor is increased. In addition, this action sends a notification to all users who have enabled notifications for themselves. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#suspend_trigger ResourceMonitor#suspend_trigger}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85b439086a68ba68e8f0eae072b448ebc95a349a034db77c7cc5c6d98df78a7c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument credit_quota", value=credit_quota, expected_type=type_hints["credit_quota"])
            check_type(argname="argument end_timestamp", value=end_timestamp, expected_type=type_hints["end_timestamp"])
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument notify_triggers", value=notify_triggers, expected_type=type_hints["notify_triggers"])
            check_type(argname="argument notify_users", value=notify_users, expected_type=type_hints["notify_users"])
            check_type(argname="argument start_timestamp", value=start_timestamp, expected_type=type_hints["start_timestamp"])
            check_type(argname="argument suspend_immediate_trigger", value=suspend_immediate_trigger, expected_type=type_hints["suspend_immediate_trigger"])
            check_type(argname="argument suspend_trigger", value=suspend_trigger, expected_type=type_hints["suspend_trigger"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
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
        if credit_quota is not None:
            self._values["credit_quota"] = credit_quota
        if end_timestamp is not None:
            self._values["end_timestamp"] = end_timestamp
        if frequency is not None:
            self._values["frequency"] = frequency
        if id is not None:
            self._values["id"] = id
        if notify_triggers is not None:
            self._values["notify_triggers"] = notify_triggers
        if notify_users is not None:
            self._values["notify_users"] = notify_users
        if start_timestamp is not None:
            self._values["start_timestamp"] = start_timestamp
        if suspend_immediate_trigger is not None:
            self._values["suspend_immediate_trigger"] = suspend_immediate_trigger
        if suspend_trigger is not None:
            self._values["suspend_trigger"] = suspend_trigger

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
        '''Identifier for the resource monitor;

        must be unique for your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#name ResourceMonitor#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def credit_quota(self) -> typing.Optional[jsii.Number]:
        '''The number of credits allocated to the resource monitor per frequency interval.

        When total usage for all warehouses assigned to the monitor reaches this number for the current frequency interval, the resource monitor is considered to be at 100% of quota.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#credit_quota ResourceMonitor#credit_quota}
        '''
        result = self._values.get("credit_quota")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def end_timestamp(self) -> typing.Optional[builtins.str]:
        '''The date and time when the resource monitor suspends the assigned warehouses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#end_timestamp ResourceMonitor#end_timestamp}
        '''
        result = self._values.get("end_timestamp")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def frequency(self) -> typing.Optional[builtins.str]:
        '''The frequency interval at which the credit usage resets to 0.

        Valid values are (case-insensitive): ``MONTHLY`` | ``DAILY`` | ``WEEKLY`` | ``YEARLY`` | ``NEVER``. If you set a ``frequency`` for a resource monitor, you must also set ``start_timestamp``. If you specify ``NEVER`` for the frequency, the credit usage for the warehouse does not reset. After removing this field from the config, the previously set value will be preserved on the Snowflake side, not the default value. That's due to Snowflake limitation and the lack of unset functionality for this parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#frequency ResourceMonitor#frequency}
        '''
        result = self._values.get("frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#id ResourceMonitor#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notify_triggers(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Specifies a list of percentages of the credit quota.

        After reaching any of the values the users passed in the notify_users field will be notified (to receive the notification they should have notifications enabled). Values over 100 are supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#notify_triggers ResourceMonitor#notify_triggers}
        '''
        result = self._values.get("notify_triggers")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def notify_users(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the list of users (their identifiers) to receive email notifications on resource monitors.

        For more information about this resource, see `docs <./user>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#notify_users ResourceMonitor#notify_users}
        '''
        result = self._values.get("notify_users")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def start_timestamp(self) -> typing.Optional[builtins.str]:
        '''The date and time when the resource monitor starts monitoring credit usage for the assigned warehouses.

        If you set a ``start_timestamp`` for a resource monitor, you must also set ``frequency``.  After removing this field from the config, the previously set value will be preserved on the Snowflake side, not the default value. That's due to Snowflake limitation and the lack of unset functionality for this parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#start_timestamp ResourceMonitor#start_timestamp}
        '''
        result = self._values.get("start_timestamp")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suspend_immediate_trigger(self) -> typing.Optional[jsii.Number]:
        '''Represents a numeric value specified as a percentage of the credit quota.

        Values over 100 are supported. After reaching this value, all assigned warehouses immediately cancel any currently running queries or statements. In addition, this action sends a notification to all users who have enabled notifications for themselves.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#suspend_immediate_trigger ResourceMonitor#suspend_immediate_trigger}
        '''
        result = self._values.get("suspend_immediate_trigger")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def suspend_trigger(self) -> typing.Optional[jsii.Number]:
        '''Represents a numeric value specified as a percentage of the credit quota.

        Values over 100 are supported. After reaching this value, all assigned warehouses while allowing currently running queries to complete will be suspended. No new queries can be executed by the warehouses until the credit quota for the resource monitor is increased. In addition, this action sends a notification to all users who have enabled notifications for themselves.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/resource_monitor#suspend_trigger ResourceMonitor#suspend_trigger}
        '''
        result = self._values.get("suspend_trigger")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceMonitorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.resourceMonitor.ResourceMonitorShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class ResourceMonitorShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceMonitorShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ResourceMonitorShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.resourceMonitor.ResourceMonitorShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e93ee7c6a96fd4496b4f9462ebbd1b0f2dd87c2ded421cafcbc752dc5fd2ffa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ResourceMonitorShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f13f9e03375e1cda236a6c91ff79333a8b594df847e0a787c8345571e27b557)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ResourceMonitorShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ceda50f2471bb0c1db0754e83d156571a89105d8025d1985ff2ad0a07b540e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20862d16e75274819062201ab3441bb0d42d55f95c41eb9a4fd1ecfb03e2552a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19262a56a0a15a89f31c1ba463ea0ba24100be5b55db3e03838ec42c0ee12833)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ResourceMonitorShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.resourceMonitor.ResourceMonitorShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45da65a2abafbbac953be6245f95a1a4d271b22b6c78c62ab95c57456f17fd17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @builtins.property
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="creditQuota")
    def credit_quota(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "creditQuota"))

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequency"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @builtins.property
    @jsii.member(jsii_name="remainingCredits")
    def remaining_credits(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "remainingCredits"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="suspendAt")
    def suspend_at(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "suspendAt"))

    @builtins.property
    @jsii.member(jsii_name="suspendImmediateAt")
    def suspend_immediate_at(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "suspendImmediateAt"))

    @builtins.property
    @jsii.member(jsii_name="usedCredits")
    def used_credits(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "usedCredits"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ResourceMonitorShowOutput]:
        return typing.cast(typing.Optional[ResourceMonitorShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ResourceMonitorShowOutput]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2188c11cfffc64d2518a825b4ec33a7bbd2fecd64682e027ad0ab069b0d6d5d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ResourceMonitor",
    "ResourceMonitorConfig",
    "ResourceMonitorShowOutput",
    "ResourceMonitorShowOutputList",
    "ResourceMonitorShowOutputOutputReference",
]

publication.publish()

def _typecheckingstub__b43a9f295b51125a0dc341a3552580e5e5ddea1e35a3201e8b54a8ca99f95b21(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    credit_quota: typing.Optional[jsii.Number] = None,
    end_timestamp: typing.Optional[builtins.str] = None,
    frequency: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    notify_triggers: typing.Optional[typing.Sequence[jsii.Number]] = None,
    notify_users: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_timestamp: typing.Optional[builtins.str] = None,
    suspend_immediate_trigger: typing.Optional[jsii.Number] = None,
    suspend_trigger: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__26ac9f9f7b342306213d834c3bec854cfb26029b5439a1a7369a1f69f8ce54cb(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96602caff2c16f75fbba74de405c9c77824284c81393b6f5f5f0bd94ff45eb2f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3d7deb08041c42bce10f40e8038f28d35285a8bb382453400460d82e154451b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__894cd8cacad81cb91f6065b680e30ed3fd543495844a290d7e48e437bb9e33e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9021990c2b184ed0e466635c380fd5a3c070de8dfabcc0b7aea239761b88aa25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24041f919aedf240169256de40993fa94cd711ddc7717db3b69846ccdeacbc5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d335b3aacc03c9c38bda997dbddd1fabd0d813654d995556ba749cd16d265704(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bfaa7d35d7c8a7c7429628e363ed1bef8587571e67236057805a18f0b5cf6d1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__638ac1a05fbd330d55c7d6bee7e08ddb584718264bf2cf67d407684acca021ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba2cd17ae14b1bc8055e0c64a036f7e5f64ec56b456658f715cb78a1534a5ed7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4368be39ac9dc9595e4501cadf1781e002027363a968efbf717125766f3ffb2d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b439086a68ba68e8f0eae072b448ebc95a349a034db77c7cc5c6d98df78a7c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    credit_quota: typing.Optional[jsii.Number] = None,
    end_timestamp: typing.Optional[builtins.str] = None,
    frequency: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    notify_triggers: typing.Optional[typing.Sequence[jsii.Number]] = None,
    notify_users: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_timestamp: typing.Optional[builtins.str] = None,
    suspend_immediate_trigger: typing.Optional[jsii.Number] = None,
    suspend_trigger: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e93ee7c6a96fd4496b4f9462ebbd1b0f2dd87c2ded421cafcbc752dc5fd2ffa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f13f9e03375e1cda236a6c91ff79333a8b594df847e0a787c8345571e27b557(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ceda50f2471bb0c1db0754e83d156571a89105d8025d1985ff2ad0a07b540e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20862d16e75274819062201ab3441bb0d42d55f95c41eb9a4fd1ecfb03e2552a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19262a56a0a15a89f31c1ba463ea0ba24100be5b55db3e03838ec42c0ee12833(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45da65a2abafbbac953be6245f95a1a4d271b22b6c78c62ab95c57456f17fd17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2188c11cfffc64d2518a825b4ec33a7bbd2fecd64682e027ad0ab069b0d6d5d1(
    value: typing.Optional[ResourceMonitorShowOutput],
) -> None:
    """Type checking stubs"""
    pass
