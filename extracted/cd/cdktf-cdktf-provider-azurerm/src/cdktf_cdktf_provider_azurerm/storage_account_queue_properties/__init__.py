r'''
# `azurerm_storage_account_queue_properties`

Refer to the Terraform Registry for docs: [`azurerm_storage_account_queue_properties`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties).
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


class StorageAccountQueuePropertiesA(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccountQueueProperties.StorageAccountQueuePropertiesA",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties azurerm_storage_account_queue_properties}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        storage_account_id: builtins.str,
        cors_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageAccountQueuePropertiesCorsRuleA", typing.Dict[builtins.str, typing.Any]]]]] = None,
        hour_metrics: typing.Optional[typing.Union["StorageAccountQueuePropertiesHourMetricsA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union["StorageAccountQueuePropertiesLoggingA", typing.Dict[builtins.str, typing.Any]]] = None,
        minute_metrics: typing.Optional[typing.Union["StorageAccountQueuePropertiesMinuteMetricsA", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["StorageAccountQueuePropertiesTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties azurerm_storage_account_queue_properties} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#storage_account_id StorageAccountQueuePropertiesA#storage_account_id}.
        :param cors_rule: cors_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#cors_rule StorageAccountQueuePropertiesA#cors_rule}
        :param hour_metrics: hour_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#hour_metrics StorageAccountQueuePropertiesA#hour_metrics}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#id StorageAccountQueuePropertiesA#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging: logging block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#logging StorageAccountQueuePropertiesA#logging}
        :param minute_metrics: minute_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#minute_metrics StorageAccountQueuePropertiesA#minute_metrics}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#timeouts StorageAccountQueuePropertiesA#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c789426185c078ce3b68e216ed9b4edf8405f32684e7a1deca96c1ebfc157c0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = StorageAccountQueuePropertiesAConfig(
            storage_account_id=storage_account_id,
            cors_rule=cors_rule,
            hour_metrics=hour_metrics,
            id=id,
            logging=logging,
            minute_metrics=minute_metrics,
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
        '''Generates CDKTF code for importing a StorageAccountQueuePropertiesA resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the StorageAccountQueuePropertiesA to import.
        :param import_from_id: The id of the existing StorageAccountQueuePropertiesA that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the StorageAccountQueuePropertiesA to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4782d828af83cf51bf3594c21acfce2678225df06f80cfea8f611b6943835750)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCorsRule")
    def put_cors_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageAccountQueuePropertiesCorsRuleA", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d046a7676b6a4d5a644ce5797a8c120faf94cbbd37c466ebd0e3dba3ae5da59e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCorsRule", [value]))

    @jsii.member(jsii_name="putHourMetrics")
    def put_hour_metrics(
        self,
        *,
        version: builtins.str,
        include_apis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retention_policy_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#version StorageAccountQueuePropertiesA#version}.
        :param include_apis: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#include_apis StorageAccountQueuePropertiesA#include_apis}.
        :param retention_policy_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#retention_policy_days StorageAccountQueuePropertiesA#retention_policy_days}.
        '''
        value = StorageAccountQueuePropertiesHourMetricsA(
            version=version,
            include_apis=include_apis,
            retention_policy_days=retention_policy_days,
        )

        return typing.cast(None, jsii.invoke(self, "putHourMetrics", [value]))

    @jsii.member(jsii_name="putLogging")
    def put_logging(
        self,
        *,
        delete: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        read: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        version: builtins.str,
        write: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        retention_policy_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#delete StorageAccountQueuePropertiesA#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#read StorageAccountQueuePropertiesA#read}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#version StorageAccountQueuePropertiesA#version}.
        :param write: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#write StorageAccountQueuePropertiesA#write}.
        :param retention_policy_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#retention_policy_days StorageAccountQueuePropertiesA#retention_policy_days}.
        '''
        value = StorageAccountQueuePropertiesLoggingA(
            delete=delete,
            read=read,
            version=version,
            write=write,
            retention_policy_days=retention_policy_days,
        )

        return typing.cast(None, jsii.invoke(self, "putLogging", [value]))

    @jsii.member(jsii_name="putMinuteMetrics")
    def put_minute_metrics(
        self,
        *,
        version: builtins.str,
        include_apis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retention_policy_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#version StorageAccountQueuePropertiesA#version}.
        :param include_apis: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#include_apis StorageAccountQueuePropertiesA#include_apis}.
        :param retention_policy_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#retention_policy_days StorageAccountQueuePropertiesA#retention_policy_days}.
        '''
        value = StorageAccountQueuePropertiesMinuteMetricsA(
            version=version,
            include_apis=include_apis,
            retention_policy_days=retention_policy_days,
        )

        return typing.cast(None, jsii.invoke(self, "putMinuteMetrics", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#create StorageAccountQueuePropertiesA#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#delete StorageAccountQueuePropertiesA#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#read StorageAccountQueuePropertiesA#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#update StorageAccountQueuePropertiesA#update}.
        '''
        value = StorageAccountQueuePropertiesTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCorsRule")
    def reset_cors_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCorsRule", []))

    @jsii.member(jsii_name="resetHourMetrics")
    def reset_hour_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHourMetrics", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogging")
    def reset_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogging", []))

    @jsii.member(jsii_name="resetMinuteMetrics")
    def reset_minute_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinuteMetrics", []))

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
    @jsii.member(jsii_name="corsRule")
    def cors_rule(self) -> "StorageAccountQueuePropertiesCorsRuleAList":
        return typing.cast("StorageAccountQueuePropertiesCorsRuleAList", jsii.get(self, "corsRule"))

    @builtins.property
    @jsii.member(jsii_name="hourMetrics")
    def hour_metrics(
        self,
    ) -> "StorageAccountQueuePropertiesHourMetricsAOutputReference":
        return typing.cast("StorageAccountQueuePropertiesHourMetricsAOutputReference", jsii.get(self, "hourMetrics"))

    @builtins.property
    @jsii.member(jsii_name="logging")
    def logging(self) -> "StorageAccountQueuePropertiesLoggingAOutputReference":
        return typing.cast("StorageAccountQueuePropertiesLoggingAOutputReference", jsii.get(self, "logging"))

    @builtins.property
    @jsii.member(jsii_name="minuteMetrics")
    def minute_metrics(
        self,
    ) -> "StorageAccountQueuePropertiesMinuteMetricsAOutputReference":
        return typing.cast("StorageAccountQueuePropertiesMinuteMetricsAOutputReference", jsii.get(self, "minuteMetrics"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "StorageAccountQueuePropertiesTimeoutsOutputReference":
        return typing.cast("StorageAccountQueuePropertiesTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="corsRuleInput")
    def cors_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageAccountQueuePropertiesCorsRuleA"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageAccountQueuePropertiesCorsRuleA"]]], jsii.get(self, "corsRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="hourMetricsInput")
    def hour_metrics_input(
        self,
    ) -> typing.Optional["StorageAccountQueuePropertiesHourMetricsA"]:
        return typing.cast(typing.Optional["StorageAccountQueuePropertiesHourMetricsA"], jsii.get(self, "hourMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingInput")
    def logging_input(self) -> typing.Optional["StorageAccountQueuePropertiesLoggingA"]:
        return typing.cast(typing.Optional["StorageAccountQueuePropertiesLoggingA"], jsii.get(self, "loggingInput"))

    @builtins.property
    @jsii.member(jsii_name="minuteMetricsInput")
    def minute_metrics_input(
        self,
    ) -> typing.Optional["StorageAccountQueuePropertiesMinuteMetricsA"]:
        return typing.cast(typing.Optional["StorageAccountQueuePropertiesMinuteMetricsA"], jsii.get(self, "minuteMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountIdInput")
    def storage_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StorageAccountQueuePropertiesTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StorageAccountQueuePropertiesTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__548959894698f2c5bd83b5afada67474abd7d3513e0c1eaccb53d6e56e84ff37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountId")
    def storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountId"))

    @storage_account_id.setter
    def storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cf0b8d486b34bd736ee3f5f440908a52fe4e48ae77e72d4613927bd74d5835a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccountQueueProperties.StorageAccountQueuePropertiesAConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "storage_account_id": "storageAccountId",
        "cors_rule": "corsRule",
        "hour_metrics": "hourMetrics",
        "id": "id",
        "logging": "logging",
        "minute_metrics": "minuteMetrics",
        "timeouts": "timeouts",
    },
)
class StorageAccountQueuePropertiesAConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        storage_account_id: builtins.str,
        cors_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageAccountQueuePropertiesCorsRuleA", typing.Dict[builtins.str, typing.Any]]]]] = None,
        hour_metrics: typing.Optional[typing.Union["StorageAccountQueuePropertiesHourMetricsA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union["StorageAccountQueuePropertiesLoggingA", typing.Dict[builtins.str, typing.Any]]] = None,
        minute_metrics: typing.Optional[typing.Union["StorageAccountQueuePropertiesMinuteMetricsA", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["StorageAccountQueuePropertiesTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#storage_account_id StorageAccountQueuePropertiesA#storage_account_id}.
        :param cors_rule: cors_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#cors_rule StorageAccountQueuePropertiesA#cors_rule}
        :param hour_metrics: hour_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#hour_metrics StorageAccountQueuePropertiesA#hour_metrics}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#id StorageAccountQueuePropertiesA#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging: logging block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#logging StorageAccountQueuePropertiesA#logging}
        :param minute_metrics: minute_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#minute_metrics StorageAccountQueuePropertiesA#minute_metrics}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#timeouts StorageAccountQueuePropertiesA#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(hour_metrics, dict):
            hour_metrics = StorageAccountQueuePropertiesHourMetricsA(**hour_metrics)
        if isinstance(logging, dict):
            logging = StorageAccountQueuePropertiesLoggingA(**logging)
        if isinstance(minute_metrics, dict):
            minute_metrics = StorageAccountQueuePropertiesMinuteMetricsA(**minute_metrics)
        if isinstance(timeouts, dict):
            timeouts = StorageAccountQueuePropertiesTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f4a73571b98f1bc3c51e0c7108c398d9a2a909c6e31b7789e0adc540026c4be)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument storage_account_id", value=storage_account_id, expected_type=type_hints["storage_account_id"])
            check_type(argname="argument cors_rule", value=cors_rule, expected_type=type_hints["cors_rule"])
            check_type(argname="argument hour_metrics", value=hour_metrics, expected_type=type_hints["hour_metrics"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument minute_metrics", value=minute_metrics, expected_type=type_hints["minute_metrics"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "storage_account_id": storage_account_id,
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
        if cors_rule is not None:
            self._values["cors_rule"] = cors_rule
        if hour_metrics is not None:
            self._values["hour_metrics"] = hour_metrics
        if id is not None:
            self._values["id"] = id
        if logging is not None:
            self._values["logging"] = logging
        if minute_metrics is not None:
            self._values["minute_metrics"] = minute_metrics
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
    def storage_account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#storage_account_id StorageAccountQueuePropertiesA#storage_account_id}.'''
        result = self._values.get("storage_account_id")
        assert result is not None, "Required property 'storage_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cors_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageAccountQueuePropertiesCorsRuleA"]]]:
        '''cors_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#cors_rule StorageAccountQueuePropertiesA#cors_rule}
        '''
        result = self._values.get("cors_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageAccountQueuePropertiesCorsRuleA"]]], result)

    @builtins.property
    def hour_metrics(
        self,
    ) -> typing.Optional["StorageAccountQueuePropertiesHourMetricsA"]:
        '''hour_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#hour_metrics StorageAccountQueuePropertiesA#hour_metrics}
        '''
        result = self._values.get("hour_metrics")
        return typing.cast(typing.Optional["StorageAccountQueuePropertiesHourMetricsA"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#id StorageAccountQueuePropertiesA#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging(self) -> typing.Optional["StorageAccountQueuePropertiesLoggingA"]:
        '''logging block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#logging StorageAccountQueuePropertiesA#logging}
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional["StorageAccountQueuePropertiesLoggingA"], result)

    @builtins.property
    def minute_metrics(
        self,
    ) -> typing.Optional["StorageAccountQueuePropertiesMinuteMetricsA"]:
        '''minute_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#minute_metrics StorageAccountQueuePropertiesA#minute_metrics}
        '''
        result = self._values.get("minute_metrics")
        return typing.cast(typing.Optional["StorageAccountQueuePropertiesMinuteMetricsA"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["StorageAccountQueuePropertiesTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#timeouts StorageAccountQueuePropertiesA#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["StorageAccountQueuePropertiesTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountQueuePropertiesAConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccountQueueProperties.StorageAccountQueuePropertiesCorsRuleA",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_headers": "allowedHeaders",
        "allowed_methods": "allowedMethods",
        "allowed_origins": "allowedOrigins",
        "exposed_headers": "exposedHeaders",
        "max_age_in_seconds": "maxAgeInSeconds",
    },
)
class StorageAccountQueuePropertiesCorsRuleA:
    def __init__(
        self,
        *,
        allowed_headers: typing.Sequence[builtins.str],
        allowed_methods: typing.Sequence[builtins.str],
        allowed_origins: typing.Sequence[builtins.str],
        exposed_headers: typing.Sequence[builtins.str],
        max_age_in_seconds: jsii.Number,
    ) -> None:
        '''
        :param allowed_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#allowed_headers StorageAccountQueuePropertiesA#allowed_headers}.
        :param allowed_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#allowed_methods StorageAccountQueuePropertiesA#allowed_methods}.
        :param allowed_origins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#allowed_origins StorageAccountQueuePropertiesA#allowed_origins}.
        :param exposed_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#exposed_headers StorageAccountQueuePropertiesA#exposed_headers}.
        :param max_age_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#max_age_in_seconds StorageAccountQueuePropertiesA#max_age_in_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7590131fc6b93090967894e7de7a08fa29bfc1bdc61a16f3f37994170348c0e1)
            check_type(argname="argument allowed_headers", value=allowed_headers, expected_type=type_hints["allowed_headers"])
            check_type(argname="argument allowed_methods", value=allowed_methods, expected_type=type_hints["allowed_methods"])
            check_type(argname="argument allowed_origins", value=allowed_origins, expected_type=type_hints["allowed_origins"])
            check_type(argname="argument exposed_headers", value=exposed_headers, expected_type=type_hints["exposed_headers"])
            check_type(argname="argument max_age_in_seconds", value=max_age_in_seconds, expected_type=type_hints["max_age_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_headers": allowed_headers,
            "allowed_methods": allowed_methods,
            "allowed_origins": allowed_origins,
            "exposed_headers": exposed_headers,
            "max_age_in_seconds": max_age_in_seconds,
        }

    @builtins.property
    def allowed_headers(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#allowed_headers StorageAccountQueuePropertiesA#allowed_headers}.'''
        result = self._values.get("allowed_headers")
        assert result is not None, "Required property 'allowed_headers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def allowed_methods(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#allowed_methods StorageAccountQueuePropertiesA#allowed_methods}.'''
        result = self._values.get("allowed_methods")
        assert result is not None, "Required property 'allowed_methods' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def allowed_origins(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#allowed_origins StorageAccountQueuePropertiesA#allowed_origins}.'''
        result = self._values.get("allowed_origins")
        assert result is not None, "Required property 'allowed_origins' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def exposed_headers(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#exposed_headers StorageAccountQueuePropertiesA#exposed_headers}.'''
        result = self._values.get("exposed_headers")
        assert result is not None, "Required property 'exposed_headers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def max_age_in_seconds(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#max_age_in_seconds StorageAccountQueuePropertiesA#max_age_in_seconds}.'''
        result = self._values.get("max_age_in_seconds")
        assert result is not None, "Required property 'max_age_in_seconds' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountQueuePropertiesCorsRuleA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountQueuePropertiesCorsRuleAList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccountQueueProperties.StorageAccountQueuePropertiesCorsRuleAList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d29c91430da0daf11c220721027ca742c0e765c3f7f7e0f08032a4f66f49c11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StorageAccountQueuePropertiesCorsRuleAOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c33ba4a6b1874a44b70241c2d42e72bc5e8e155b2099804b5048e1b3a4806492)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StorageAccountQueuePropertiesCorsRuleAOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89f1ec965eebfdbba1f1958ff55bdfca2475067f5698dba3c76251f9bca85933)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bda36a768f09de577e0a6a0a37bba2a7e7249d49ce3ac1c0dfd9367db9cc4155)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63cb78db3d79816451b42da8db569eefbc5d6d28bfad2ff7861f1f070bb65061)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountQueuePropertiesCorsRuleA]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountQueuePropertiesCorsRuleA]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountQueuePropertiesCorsRuleA]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f47d16cc6d13118f339aae08b7134674f584231e84816852a2760ff309717d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageAccountQueuePropertiesCorsRuleAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccountQueueProperties.StorageAccountQueuePropertiesCorsRuleAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53557e6ec29788efe36259dda913cff58d1848b7807e20a00f64f0549cf2636d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allowedHeadersInput")
    def allowed_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedMethodsInput")
    def allowed_methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedOriginsInput")
    def allowed_origins_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedOriginsInput"))

    @builtins.property
    @jsii.member(jsii_name="exposedHeadersInput")
    def exposed_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exposedHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAgeInSecondsInput")
    def max_age_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAgeInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedHeaders")
    def allowed_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedHeaders"))

    @allowed_headers.setter
    def allowed_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77082018b58b73b6ca386c05d630985a6c3613680e8b3c1512490bbd827f9b2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedMethods")
    def allowed_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedMethods"))

    @allowed_methods.setter
    def allowed_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceea2e8abd2c3cf0f622860fa703d872b0d65dbfa9a35bd63fc9bb70b730e0af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedOrigins")
    def allowed_origins(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedOrigins"))

    @allowed_origins.setter
    def allowed_origins(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e0c5e1f2fcc2a1f5e5eb18432c773e97e2dd46fe6142d95a25aeb3c30e4c32c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedOrigins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exposedHeaders")
    def exposed_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exposedHeaders"))

    @exposed_headers.setter
    def exposed_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e60ce02321a59a8d6380ab541f9eb2dab2f1361a026e471698e1676a2617eed3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exposedHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAgeInSeconds")
    def max_age_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAgeInSeconds"))

    @max_age_in_seconds.setter
    def max_age_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38c58a5a19d6c8dc6d665d7013a10e17efbbd93cd448028372517ddb6de81a41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAgeInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountQueuePropertiesCorsRuleA]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountQueuePropertiesCorsRuleA]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountQueuePropertiesCorsRuleA]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__688d173a2f16c9dda492d6707b69e007a37bb3f78b40a9a3bcd9adbcff6d4d36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccountQueueProperties.StorageAccountQueuePropertiesHourMetricsA",
    jsii_struct_bases=[],
    name_mapping={
        "version": "version",
        "include_apis": "includeApis",
        "retention_policy_days": "retentionPolicyDays",
    },
)
class StorageAccountQueuePropertiesHourMetricsA:
    def __init__(
        self,
        *,
        version: builtins.str,
        include_apis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retention_policy_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#version StorageAccountQueuePropertiesA#version}.
        :param include_apis: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#include_apis StorageAccountQueuePropertiesA#include_apis}.
        :param retention_policy_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#retention_policy_days StorageAccountQueuePropertiesA#retention_policy_days}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40762850fb274b004a7d5d295d7446ff991ce4cb2652e39c55b2f4bc5c73f411)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument include_apis", value=include_apis, expected_type=type_hints["include_apis"])
            check_type(argname="argument retention_policy_days", value=retention_policy_days, expected_type=type_hints["retention_policy_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "version": version,
        }
        if include_apis is not None:
            self._values["include_apis"] = include_apis
        if retention_policy_days is not None:
            self._values["retention_policy_days"] = retention_policy_days

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#version StorageAccountQueuePropertiesA#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include_apis(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#include_apis StorageAccountQueuePropertiesA#include_apis}.'''
        result = self._values.get("include_apis")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def retention_policy_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#retention_policy_days StorageAccountQueuePropertiesA#retention_policy_days}.'''
        result = self._values.get("retention_policy_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountQueuePropertiesHourMetricsA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountQueuePropertiesHourMetricsAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccountQueueProperties.StorageAccountQueuePropertiesHourMetricsAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbd9912a08e19275a91dd2c281528572385b17c9a430d826c28f89711f875c9a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIncludeApis")
    def reset_include_apis(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeApis", []))

    @jsii.member(jsii_name="resetRetentionPolicyDays")
    def reset_retention_policy_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPolicyDays", []))

    @builtins.property
    @jsii.member(jsii_name="includeApisInput")
    def include_apis_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeApisInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyDaysInput")
    def retention_policy_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionPolicyDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="includeApis")
    def include_apis(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeApis"))

    @include_apis.setter
    def include_apis(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f2a029883bd83c9ed14a291f6d4fd92e8a08b25b0632d0747bb451a99875feb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeApis", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyDays")
    def retention_policy_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionPolicyDays"))

    @retention_policy_days.setter
    def retention_policy_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cd2ee15dbe66d1fe39331567fa2477da50dac6a586ac5a17cf67a540ecf8687)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPolicyDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0504126191edfb8797cdd055cbc1e7607429c3f1cb27a6815f8a415fbc6ea4c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageAccountQueuePropertiesHourMetricsA]:
        return typing.cast(typing.Optional[StorageAccountQueuePropertiesHourMetricsA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageAccountQueuePropertiesHourMetricsA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de1bacc5d2ddcb0ed5dfad03324820cb34ac2d31094612c396b1a2420cbce067)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccountQueueProperties.StorageAccountQueuePropertiesLoggingA",
    jsii_struct_bases=[],
    name_mapping={
        "delete": "delete",
        "read": "read",
        "version": "version",
        "write": "write",
        "retention_policy_days": "retentionPolicyDays",
    },
)
class StorageAccountQueuePropertiesLoggingA:
    def __init__(
        self,
        *,
        delete: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        read: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        version: builtins.str,
        write: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        retention_policy_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#delete StorageAccountQueuePropertiesA#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#read StorageAccountQueuePropertiesA#read}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#version StorageAccountQueuePropertiesA#version}.
        :param write: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#write StorageAccountQueuePropertiesA#write}.
        :param retention_policy_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#retention_policy_days StorageAccountQueuePropertiesA#retention_policy_days}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3d4868fc3df72012e156674f76d6138b4585465f81c628e6ba2ece84171f2c9)
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument write", value=write, expected_type=type_hints["write"])
            check_type(argname="argument retention_policy_days", value=retention_policy_days, expected_type=type_hints["retention_policy_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "delete": delete,
            "read": read,
            "version": version,
            "write": write,
        }
        if retention_policy_days is not None:
            self._values["retention_policy_days"] = retention_policy_days

    @builtins.property
    def delete(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#delete StorageAccountQueuePropertiesA#delete}.'''
        result = self._values.get("delete")
        assert result is not None, "Required property 'delete' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def read(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#read StorageAccountQueuePropertiesA#read}.'''
        result = self._values.get("read")
        assert result is not None, "Required property 'read' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#version StorageAccountQueuePropertiesA#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def write(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#write StorageAccountQueuePropertiesA#write}.'''
        result = self._values.get("write")
        assert result is not None, "Required property 'write' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def retention_policy_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#retention_policy_days StorageAccountQueuePropertiesA#retention_policy_days}.'''
        result = self._values.get("retention_policy_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountQueuePropertiesLoggingA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountQueuePropertiesLoggingAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccountQueueProperties.StorageAccountQueuePropertiesLoggingAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92edcfad09c32552aa8b702ffef052efd2169593cfc75e83f6ad680c39b44f6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRetentionPolicyDays")
    def reset_retention_policy_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPolicyDays", []))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyDaysInput")
    def retention_policy_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionPolicyDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="writeInput")
    def write_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "writeInput"))

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "delete"))

    @delete.setter
    def delete(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8a2e5cb0984b56ff42ae744d8655224f1edfc7a5f3f9702affd7b57c95eca0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "read"))

    @read.setter
    def read(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7b739e520602e8868ceeb07d1ff6dc14013391a7c660bdda627cbc5a194c578)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyDays")
    def retention_policy_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionPolicyDays"))

    @retention_policy_days.setter
    def retention_policy_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3496ae1c742db8503a0ea50f5577bf37528e8fdd68a93e32b30c02b20cb0a9ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPolicyDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b69fe774085dc646ede6ccf2353c0e0fce1ff5a10618fe9a65b9cd430eb8d519)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="write")
    def write(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "write"))

    @write.setter
    def write(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71aa5c118af48aeabe9a56e40a38aa483e08c8b2f2b0bd3fd0c6b85b475a6b37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "write", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageAccountQueuePropertiesLoggingA]:
        return typing.cast(typing.Optional[StorageAccountQueuePropertiesLoggingA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageAccountQueuePropertiesLoggingA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3405424e02ca99f00dadc10099e90d2139e62f394568f0a5d4e2e819f4f2087)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccountQueueProperties.StorageAccountQueuePropertiesMinuteMetricsA",
    jsii_struct_bases=[],
    name_mapping={
        "version": "version",
        "include_apis": "includeApis",
        "retention_policy_days": "retentionPolicyDays",
    },
)
class StorageAccountQueuePropertiesMinuteMetricsA:
    def __init__(
        self,
        *,
        version: builtins.str,
        include_apis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retention_policy_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#version StorageAccountQueuePropertiesA#version}.
        :param include_apis: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#include_apis StorageAccountQueuePropertiesA#include_apis}.
        :param retention_policy_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#retention_policy_days StorageAccountQueuePropertiesA#retention_policy_days}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c71b585a19e4bf3f3323cb0315070940df3da34054aac1d7345962eadd740c)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument include_apis", value=include_apis, expected_type=type_hints["include_apis"])
            check_type(argname="argument retention_policy_days", value=retention_policy_days, expected_type=type_hints["retention_policy_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "version": version,
        }
        if include_apis is not None:
            self._values["include_apis"] = include_apis
        if retention_policy_days is not None:
            self._values["retention_policy_days"] = retention_policy_days

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#version StorageAccountQueuePropertiesA#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include_apis(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#include_apis StorageAccountQueuePropertiesA#include_apis}.'''
        result = self._values.get("include_apis")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def retention_policy_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#retention_policy_days StorageAccountQueuePropertiesA#retention_policy_days}.'''
        result = self._values.get("retention_policy_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountQueuePropertiesMinuteMetricsA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountQueuePropertiesMinuteMetricsAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccountQueueProperties.StorageAccountQueuePropertiesMinuteMetricsAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e6849b8e1ae75037422839f3ff385bfb520e8bbd73700ae6a4346186f6fa386)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIncludeApis")
    def reset_include_apis(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeApis", []))

    @jsii.member(jsii_name="resetRetentionPolicyDays")
    def reset_retention_policy_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPolicyDays", []))

    @builtins.property
    @jsii.member(jsii_name="includeApisInput")
    def include_apis_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeApisInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyDaysInput")
    def retention_policy_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionPolicyDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="includeApis")
    def include_apis(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeApis"))

    @include_apis.setter
    def include_apis(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e658daa943a48e9e2fa8b0fe6e995cb096647176398fc74891d866ba6aa55104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeApis", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyDays")
    def retention_policy_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionPolicyDays"))

    @retention_policy_days.setter
    def retention_policy_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41bf183b57880aa0b92b7980977865afcbfb60422d6be2b85c042f58d795944b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPolicyDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c244aad79e9e97bccb4396a6b5b46eb9277548aeaddf1036fd1e5fa63b4ad46c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageAccountQueuePropertiesMinuteMetricsA]:
        return typing.cast(typing.Optional[StorageAccountQueuePropertiesMinuteMetricsA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageAccountQueuePropertiesMinuteMetricsA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3715d394707cd2f4285858afc1a4128f110d2e1ae16b2607daf9969374424b19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccountQueueProperties.StorageAccountQueuePropertiesTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class StorageAccountQueuePropertiesTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#create StorageAccountQueuePropertiesA#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#delete StorageAccountQueuePropertiesA#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#read StorageAccountQueuePropertiesA#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#update StorageAccountQueuePropertiesA#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec1cb070665da2cceabe00e74c5e98cb700ecd21165bd41b271c3ea9d68bb42a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#create StorageAccountQueuePropertiesA#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#delete StorageAccountQueuePropertiesA#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#read StorageAccountQueuePropertiesA#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account_queue_properties#update StorageAccountQueuePropertiesA#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountQueuePropertiesTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountQueuePropertiesTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccountQueueProperties.StorageAccountQueuePropertiesTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a9809c3f0c3a68ab77d84bb2a12292e7522e9deb48b334f46a0241f98f6bfa6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f24b71ed93315cfe68137148c1f1fbf65c66454c991f157e6c757684bbf0e233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6810141443626a4b6bf0a2019a8715a0d419cec56a1c6810f0fe24f8ebbaee2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0760a527627fbf23dc4a3be5025081c8929c2084765e624e776f89dfdf8198e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37594910c65036a4957e9698a5064e490662297ffe3d6f697af520310dd5fef3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountQueuePropertiesTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountQueuePropertiesTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountQueuePropertiesTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51abbfed8141f081ec13d75b9cdf3cc9dcc4e4a5ef840d29b966b3fb4bd9bd35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "StorageAccountQueuePropertiesA",
    "StorageAccountQueuePropertiesAConfig",
    "StorageAccountQueuePropertiesCorsRuleA",
    "StorageAccountQueuePropertiesCorsRuleAList",
    "StorageAccountQueuePropertiesCorsRuleAOutputReference",
    "StorageAccountQueuePropertiesHourMetricsA",
    "StorageAccountQueuePropertiesHourMetricsAOutputReference",
    "StorageAccountQueuePropertiesLoggingA",
    "StorageAccountQueuePropertiesLoggingAOutputReference",
    "StorageAccountQueuePropertiesMinuteMetricsA",
    "StorageAccountQueuePropertiesMinuteMetricsAOutputReference",
    "StorageAccountQueuePropertiesTimeouts",
    "StorageAccountQueuePropertiesTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__2c789426185c078ce3b68e216ed9b4edf8405f32684e7a1deca96c1ebfc157c0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    storage_account_id: builtins.str,
    cors_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageAccountQueuePropertiesCorsRuleA, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hour_metrics: typing.Optional[typing.Union[StorageAccountQueuePropertiesHourMetricsA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[StorageAccountQueuePropertiesLoggingA, typing.Dict[builtins.str, typing.Any]]] = None,
    minute_metrics: typing.Optional[typing.Union[StorageAccountQueuePropertiesMinuteMetricsA, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[StorageAccountQueuePropertiesTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4782d828af83cf51bf3594c21acfce2678225df06f80cfea8f611b6943835750(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d046a7676b6a4d5a644ce5797a8c120faf94cbbd37c466ebd0e3dba3ae5da59e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageAccountQueuePropertiesCorsRuleA, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__548959894698f2c5bd83b5afada67474abd7d3513e0c1eaccb53d6e56e84ff37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf0b8d486b34bd736ee3f5f440908a52fe4e48ae77e72d4613927bd74d5835a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f4a73571b98f1bc3c51e0c7108c398d9a2a909c6e31b7789e0adc540026c4be(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    storage_account_id: builtins.str,
    cors_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageAccountQueuePropertiesCorsRuleA, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hour_metrics: typing.Optional[typing.Union[StorageAccountQueuePropertiesHourMetricsA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[StorageAccountQueuePropertiesLoggingA, typing.Dict[builtins.str, typing.Any]]] = None,
    minute_metrics: typing.Optional[typing.Union[StorageAccountQueuePropertiesMinuteMetricsA, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[StorageAccountQueuePropertiesTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7590131fc6b93090967894e7de7a08fa29bfc1bdc61a16f3f37994170348c0e1(
    *,
    allowed_headers: typing.Sequence[builtins.str],
    allowed_methods: typing.Sequence[builtins.str],
    allowed_origins: typing.Sequence[builtins.str],
    exposed_headers: typing.Sequence[builtins.str],
    max_age_in_seconds: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d29c91430da0daf11c220721027ca742c0e765c3f7f7e0f08032a4f66f49c11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33ba4a6b1874a44b70241c2d42e72bc5e8e155b2099804b5048e1b3a4806492(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f1ec965eebfdbba1f1958ff55bdfca2475067f5698dba3c76251f9bca85933(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda36a768f09de577e0a6a0a37bba2a7e7249d49ce3ac1c0dfd9367db9cc4155(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63cb78db3d79816451b42da8db569eefbc5d6d28bfad2ff7861f1f070bb65061(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f47d16cc6d13118f339aae08b7134674f584231e84816852a2760ff309717d1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountQueuePropertiesCorsRuleA]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53557e6ec29788efe36259dda913cff58d1848b7807e20a00f64f0549cf2636d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77082018b58b73b6ca386c05d630985a6c3613680e8b3c1512490bbd827f9b2c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceea2e8abd2c3cf0f622860fa703d872b0d65dbfa9a35bd63fc9bb70b730e0af(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e0c5e1f2fcc2a1f5e5eb18432c773e97e2dd46fe6142d95a25aeb3c30e4c32c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e60ce02321a59a8d6380ab541f9eb2dab2f1361a026e471698e1676a2617eed3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38c58a5a19d6c8dc6d665d7013a10e17efbbd93cd448028372517ddb6de81a41(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__688d173a2f16c9dda492d6707b69e007a37bb3f78b40a9a3bcd9adbcff6d4d36(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountQueuePropertiesCorsRuleA]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40762850fb274b004a7d5d295d7446ff991ce4cb2652e39c55b2f4bc5c73f411(
    *,
    version: builtins.str,
    include_apis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retention_policy_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbd9912a08e19275a91dd2c281528572385b17c9a430d826c28f89711f875c9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f2a029883bd83c9ed14a291f6d4fd92e8a08b25b0632d0747bb451a99875feb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd2ee15dbe66d1fe39331567fa2477da50dac6a586ac5a17cf67a540ecf8687(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0504126191edfb8797cdd055cbc1e7607429c3f1cb27a6815f8a415fbc6ea4c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de1bacc5d2ddcb0ed5dfad03324820cb34ac2d31094612c396b1a2420cbce067(
    value: typing.Optional[StorageAccountQueuePropertiesHourMetricsA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3d4868fc3df72012e156674f76d6138b4585465f81c628e6ba2ece84171f2c9(
    *,
    delete: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    read: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    version: builtins.str,
    write: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    retention_policy_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92edcfad09c32552aa8b702ffef052efd2169593cfc75e83f6ad680c39b44f6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a2e5cb0984b56ff42ae744d8655224f1edfc7a5f3f9702affd7b57c95eca0d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b739e520602e8868ceeb07d1ff6dc14013391a7c660bdda627cbc5a194c578(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3496ae1c742db8503a0ea50f5577bf37528e8fdd68a93e32b30c02b20cb0a9ea(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69fe774085dc646ede6ccf2353c0e0fce1ff5a10618fe9a65b9cd430eb8d519(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71aa5c118af48aeabe9a56e40a38aa483e08c8b2f2b0bd3fd0c6b85b475a6b37(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3405424e02ca99f00dadc10099e90d2139e62f394568f0a5d4e2e819f4f2087(
    value: typing.Optional[StorageAccountQueuePropertiesLoggingA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c71b585a19e4bf3f3323cb0315070940df3da34054aac1d7345962eadd740c(
    *,
    version: builtins.str,
    include_apis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retention_policy_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e6849b8e1ae75037422839f3ff385bfb520e8bbd73700ae6a4346186f6fa386(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e658daa943a48e9e2fa8b0fe6e995cb096647176398fc74891d866ba6aa55104(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41bf183b57880aa0b92b7980977865afcbfb60422d6be2b85c042f58d795944b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c244aad79e9e97bccb4396a6b5b46eb9277548aeaddf1036fd1e5fa63b4ad46c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3715d394707cd2f4285858afc1a4128f110d2e1ae16b2607daf9969374424b19(
    value: typing.Optional[StorageAccountQueuePropertiesMinuteMetricsA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1cb070665da2cceabe00e74c5e98cb700ecd21165bd41b271c3ea9d68bb42a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9809c3f0c3a68ab77d84bb2a12292e7522e9deb48b334f46a0241f98f6bfa6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f24b71ed93315cfe68137148c1f1fbf65c66454c991f157e6c757684bbf0e233(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6810141443626a4b6bf0a2019a8715a0d419cec56a1c6810f0fe24f8ebbaee2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0760a527627fbf23dc4a3be5025081c8929c2084765e624e776f89dfdf8198e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37594910c65036a4957e9698a5064e490662297ffe3d6f697af520310dd5fef3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51abbfed8141f081ec13d75b9cdf3cc9dcc4e4a5ef840d29b966b3fb4bd9bd35(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountQueuePropertiesTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
