r'''
# `snowflake_warehouse`

Refer to the Terraform Registry for docs: [`snowflake_warehouse`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse).
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


class Warehouse(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.warehouse.Warehouse",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse snowflake_warehouse}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        auto_resume: typing.Optional[builtins.str] = None,
        auto_suspend: typing.Optional[jsii.Number] = None,
        comment: typing.Optional[builtins.str] = None,
        enable_query_acceleration: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        initially_suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_cluster_count: typing.Optional[jsii.Number] = None,
        max_concurrency_level: typing.Optional[jsii.Number] = None,
        min_cluster_count: typing.Optional[jsii.Number] = None,
        query_acceleration_max_scale_factor: typing.Optional[jsii.Number] = None,
        resource_monitor: typing.Optional[builtins.str] = None,
        scaling_policy: typing.Optional[builtins.str] = None,
        statement_queued_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        statement_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        warehouse_size: typing.Optional[builtins.str] = None,
        warehouse_type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse snowflake_warehouse} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Identifier for the virtual warehouse; must be unique for your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#name Warehouse#name}
        :param auto_resume: Specifies whether to automatically resume a warehouse when a SQL statement (e.g. query) is submitted to it. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#auto_resume Warehouse#auto_resume}
        :param auto_suspend: Specifies the number of seconds of inactivity after which a warehouse is automatically suspended. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#auto_suspend Warehouse#auto_suspend}
        :param comment: Specifies a comment for the warehouse. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#comment Warehouse#comment}
        :param enable_query_acceleration: Specifies whether to enable the query acceleration service for queries that rely on this warehouse for compute resources. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#enable_query_acceleration Warehouse#enable_query_acceleration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#id Warehouse#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initially_suspended: Specifies whether the warehouse is created initially in the ‘Suspended’ state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#initially_suspended Warehouse#initially_suspended}
        :param max_cluster_count: Specifies the maximum number of server clusters for the warehouse. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#max_cluster_count Warehouse#max_cluster_count}
        :param max_concurrency_level: Object parameter that specifies the concurrency level for SQL statements (i.e. queries and DML) executed by a warehouse. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#max_concurrency_level Warehouse#max_concurrency_level}
        :param min_cluster_count: Specifies the minimum number of server clusters for the warehouse (only applies to multi-cluster warehouses). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#min_cluster_count Warehouse#min_cluster_count}
        :param query_acceleration_max_scale_factor: Specifies the maximum scale factor for leasing compute resources for query acceleration. The scale factor is used as a multiplier based on warehouse size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#query_acceleration_max_scale_factor Warehouse#query_acceleration_max_scale_factor}
        :param resource_monitor: Specifies the name of a resource monitor that is explicitly assigned to the warehouse. For more information about this resource, see `docs <./resource_monitor>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#resource_monitor Warehouse#resource_monitor}
        :param scaling_policy: Specifies the policy for automatically starting and shutting down clusters in a multi-cluster warehouse running in Auto-scale mode. Valid values are (case-insensitive): ``STANDARD`` | ``ECONOMY``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#scaling_policy Warehouse#scaling_policy}
        :param statement_queued_timeout_in_seconds: Object parameter that specifies the time, in seconds, a SQL statement (query, DDL, DML, etc.) can be queued on a warehouse before it is canceled by the system. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#statement_queued_timeout_in_seconds Warehouse#statement_queued_timeout_in_seconds}
        :param statement_timeout_in_seconds: Specifies the time, in seconds, after which a running SQL statement (query, DDL, DML, etc.) is canceled by the system. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#statement_timeout_in_seconds Warehouse#statement_timeout_in_seconds}
        :param warehouse_size: Specifies the size of the virtual warehouse. Valid values are (case-insensitive): ``XSMALL`` | ``X-SMALL`` | ``SMALL`` | ``MEDIUM`` | ``LARGE`` | ``XLARGE`` | ``X-LARGE`` | ``XXLARGE`` | ``X2LARGE`` | ``2X-LARGE`` | ``XXXLARGE`` | ``X3LARGE`` | ``3X-LARGE`` | ``X4LARGE`` | ``4X-LARGE`` | ``X5LARGE`` | ``5X-LARGE`` | ``X6LARGE`` | ``6X-LARGE``. Consult `warehouse documentation <https://docs.snowflake.com/en/sql-reference/sql/create-warehouse#optional-properties-objectproperties>`_ for the details. Note: removing the size from config will result in the resource recreation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#warehouse_size Warehouse#warehouse_size}
        :param warehouse_type: Specifies warehouse type. Valid values are (case-insensitive): ``STANDARD`` | ``SNOWPARK-OPTIMIZED``. Warehouse needs to be suspended to change its type. Provider will handle automatic suspension and resumption if needed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#warehouse_type Warehouse#warehouse_type}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7a545b9470ddbc13f6797573fe9db4caad9ea0ec20a416254e98f74ad315894)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = WarehouseConfig(
            name=name,
            auto_resume=auto_resume,
            auto_suspend=auto_suspend,
            comment=comment,
            enable_query_acceleration=enable_query_acceleration,
            id=id,
            initially_suspended=initially_suspended,
            max_cluster_count=max_cluster_count,
            max_concurrency_level=max_concurrency_level,
            min_cluster_count=min_cluster_count,
            query_acceleration_max_scale_factor=query_acceleration_max_scale_factor,
            resource_monitor=resource_monitor,
            scaling_policy=scaling_policy,
            statement_queued_timeout_in_seconds=statement_queued_timeout_in_seconds,
            statement_timeout_in_seconds=statement_timeout_in_seconds,
            warehouse_size=warehouse_size,
            warehouse_type=warehouse_type,
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
        '''Generates CDKTF code for importing a Warehouse resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Warehouse to import.
        :param import_from_id: The id of the existing Warehouse that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Warehouse to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572da37f5bf450cb7fe3f011f5e0e5d584f32856d369188d26ecdd2bed0c8cea)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAutoResume")
    def reset_auto_resume(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoResume", []))

    @jsii.member(jsii_name="resetAutoSuspend")
    def reset_auto_suspend(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoSuspend", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetEnableQueryAcceleration")
    def reset_enable_query_acceleration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableQueryAcceleration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInitiallySuspended")
    def reset_initially_suspended(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitiallySuspended", []))

    @jsii.member(jsii_name="resetMaxClusterCount")
    def reset_max_cluster_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxClusterCount", []))

    @jsii.member(jsii_name="resetMaxConcurrencyLevel")
    def reset_max_concurrency_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConcurrencyLevel", []))

    @jsii.member(jsii_name="resetMinClusterCount")
    def reset_min_cluster_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinClusterCount", []))

    @jsii.member(jsii_name="resetQueryAccelerationMaxScaleFactor")
    def reset_query_acceleration_max_scale_factor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryAccelerationMaxScaleFactor", []))

    @jsii.member(jsii_name="resetResourceMonitor")
    def reset_resource_monitor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceMonitor", []))

    @jsii.member(jsii_name="resetScalingPolicy")
    def reset_scaling_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScalingPolicy", []))

    @jsii.member(jsii_name="resetStatementQueuedTimeoutInSeconds")
    def reset_statement_queued_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatementQueuedTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetStatementTimeoutInSeconds")
    def reset_statement_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatementTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetWarehouseSize")
    def reset_warehouse_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWarehouseSize", []))

    @jsii.member(jsii_name="resetWarehouseType")
    def reset_warehouse_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWarehouseType", []))

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
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> "WarehouseParametersList":
        return typing.cast("WarehouseParametersList", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "WarehouseShowOutputList":
        return typing.cast("WarehouseShowOutputList", jsii.get(self, "showOutput"))

    @builtins.property
    @jsii.member(jsii_name="autoResumeInput")
    def auto_resume_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoResumeInput"))

    @builtins.property
    @jsii.member(jsii_name="autoSuspendInput")
    def auto_suspend_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "autoSuspendInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="enableQueryAccelerationInput")
    def enable_query_acceleration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enableQueryAccelerationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="initiallySuspendedInput")
    def initially_suspended_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "initiallySuspendedInput"))

    @builtins.property
    @jsii.member(jsii_name="maxClusterCountInput")
    def max_cluster_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxClusterCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrencyLevelInput")
    def max_concurrency_level_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConcurrencyLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="minClusterCountInput")
    def min_cluster_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minClusterCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="queryAccelerationMaxScaleFactorInput")
    def query_acceleration_max_scale_factor_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "queryAccelerationMaxScaleFactorInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceMonitorInput")
    def resource_monitor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceMonitorInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingPolicyInput")
    def scaling_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="statementQueuedTimeoutInSecondsInput")
    def statement_queued_timeout_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "statementQueuedTimeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="statementTimeoutInSecondsInput")
    def statement_timeout_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "statementTimeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="warehouseSizeInput")
    def warehouse_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "warehouseSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="warehouseTypeInput")
    def warehouse_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "warehouseTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="autoResume")
    def auto_resume(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoResume"))

    @auto_resume.setter
    def auto_resume(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59e363e0e719321b9f36ba95f42412180d8c83bca4f70f5f58bf54d11faaca1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoResume", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoSuspend")
    def auto_suspend(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autoSuspend"))

    @auto_suspend.setter
    def auto_suspend(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e33c40876b47a58a42eafec0c16bfa190228c08a23a39eea9350f0f083d61dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoSuspend", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4c985a73dcb01e461dd3d79db0b1b2b150d1b6ad292921dd0553f38596bff56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableQueryAcceleration")
    def enable_query_acceleration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enableQueryAcceleration"))

    @enable_query_acceleration.setter
    def enable_query_acceleration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17a9dd2dcf21eba130519e20959255cf814826077dc1a2486f912d9091569c61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableQueryAcceleration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46603b6d33e982986e0b443f6a5696f6a33454cc6e0aa6678817badd8cd756ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initiallySuspended")
    def initially_suspended(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "initiallySuspended"))

    @initially_suspended.setter
    def initially_suspended(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09d176a43f31805f67ca01f79890fb1058791b57d84f2115996086f337ed2e1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initiallySuspended", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxClusterCount")
    def max_cluster_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxClusterCount"))

    @max_cluster_count.setter
    def max_cluster_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba9c5ca5c139d131448b0430ff14223b8e4d4bb0a0fd5b55adffbbe7796824f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxClusterCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxConcurrencyLevel")
    def max_concurrency_level(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrencyLevel"))

    @max_concurrency_level.setter
    def max_concurrency_level(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec1a76dc728c5c13221da328191e3e3c34cc72784972ed2e3fc82897c41a05e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrencyLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minClusterCount")
    def min_cluster_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minClusterCount"))

    @min_cluster_count.setter
    def min_cluster_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b96edb769e4b81e3cd326f1bc18a50dd3c4dac86feefc24a81934fafe5f777a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minClusterCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7077b71c10d32de0bc3d3c8d12117d655ce00aa136fc82b6a7c73b6d0ec8599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryAccelerationMaxScaleFactor")
    def query_acceleration_max_scale_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queryAccelerationMaxScaleFactor"))

    @query_acceleration_max_scale_factor.setter
    def query_acceleration_max_scale_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f96be4446754d4205d1e9d99a2c4abcb4828cb58dbd27f26e599e94fb3c26020)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryAccelerationMaxScaleFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceMonitor")
    def resource_monitor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceMonitor"))

    @resource_monitor.setter
    def resource_monitor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8e4b5fc94f6dc0de4811839fa018a79668ca9d8203c01cfb6f125c1c11eb185)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceMonitor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scalingPolicy")
    def scaling_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingPolicy"))

    @scaling_policy.setter
    def scaling_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da84474f179556752719c65f7b2440f46eb949691133a2f9714d5686438334d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statementQueuedTimeoutInSeconds")
    def statement_queued_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statementQueuedTimeoutInSeconds"))

    @statement_queued_timeout_in_seconds.setter
    def statement_queued_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3a106de57372b520a40ffb364b03b9b17f28f3178d2a39b83f02ec994035f8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statementQueuedTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statementTimeoutInSeconds")
    def statement_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statementTimeoutInSeconds"))

    @statement_timeout_in_seconds.setter
    def statement_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__142317704b4892b91eab76a9f614fe8251c78e43a9ab129e89de9d627f23595b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statementTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="warehouseSize")
    def warehouse_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "warehouseSize"))

    @warehouse_size.setter
    def warehouse_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb682cffa8639019a3d246df698597f1933be487556ff7d66681abdaec17a65a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "warehouseSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="warehouseType")
    def warehouse_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "warehouseType"))

    @warehouse_type.setter
    def warehouse_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e2ec6ca1e83f9784c4d21dfe7ac241ada21747ef3247184dfea371249ab7f05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "warehouseType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.warehouse.WarehouseConfig",
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
        "auto_resume": "autoResume",
        "auto_suspend": "autoSuspend",
        "comment": "comment",
        "enable_query_acceleration": "enableQueryAcceleration",
        "id": "id",
        "initially_suspended": "initiallySuspended",
        "max_cluster_count": "maxClusterCount",
        "max_concurrency_level": "maxConcurrencyLevel",
        "min_cluster_count": "minClusterCount",
        "query_acceleration_max_scale_factor": "queryAccelerationMaxScaleFactor",
        "resource_monitor": "resourceMonitor",
        "scaling_policy": "scalingPolicy",
        "statement_queued_timeout_in_seconds": "statementQueuedTimeoutInSeconds",
        "statement_timeout_in_seconds": "statementTimeoutInSeconds",
        "warehouse_size": "warehouseSize",
        "warehouse_type": "warehouseType",
    },
)
class WarehouseConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        auto_resume: typing.Optional[builtins.str] = None,
        auto_suspend: typing.Optional[jsii.Number] = None,
        comment: typing.Optional[builtins.str] = None,
        enable_query_acceleration: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        initially_suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_cluster_count: typing.Optional[jsii.Number] = None,
        max_concurrency_level: typing.Optional[jsii.Number] = None,
        min_cluster_count: typing.Optional[jsii.Number] = None,
        query_acceleration_max_scale_factor: typing.Optional[jsii.Number] = None,
        resource_monitor: typing.Optional[builtins.str] = None,
        scaling_policy: typing.Optional[builtins.str] = None,
        statement_queued_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        statement_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        warehouse_size: typing.Optional[builtins.str] = None,
        warehouse_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Identifier for the virtual warehouse; must be unique for your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#name Warehouse#name}
        :param auto_resume: Specifies whether to automatically resume a warehouse when a SQL statement (e.g. query) is submitted to it. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#auto_resume Warehouse#auto_resume}
        :param auto_suspend: Specifies the number of seconds of inactivity after which a warehouse is automatically suspended. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#auto_suspend Warehouse#auto_suspend}
        :param comment: Specifies a comment for the warehouse. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#comment Warehouse#comment}
        :param enable_query_acceleration: Specifies whether to enable the query acceleration service for queries that rely on this warehouse for compute resources. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#enable_query_acceleration Warehouse#enable_query_acceleration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#id Warehouse#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initially_suspended: Specifies whether the warehouse is created initially in the ‘Suspended’ state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#initially_suspended Warehouse#initially_suspended}
        :param max_cluster_count: Specifies the maximum number of server clusters for the warehouse. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#max_cluster_count Warehouse#max_cluster_count}
        :param max_concurrency_level: Object parameter that specifies the concurrency level for SQL statements (i.e. queries and DML) executed by a warehouse. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#max_concurrency_level Warehouse#max_concurrency_level}
        :param min_cluster_count: Specifies the minimum number of server clusters for the warehouse (only applies to multi-cluster warehouses). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#min_cluster_count Warehouse#min_cluster_count}
        :param query_acceleration_max_scale_factor: Specifies the maximum scale factor for leasing compute resources for query acceleration. The scale factor is used as a multiplier based on warehouse size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#query_acceleration_max_scale_factor Warehouse#query_acceleration_max_scale_factor}
        :param resource_monitor: Specifies the name of a resource monitor that is explicitly assigned to the warehouse. For more information about this resource, see `docs <./resource_monitor>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#resource_monitor Warehouse#resource_monitor}
        :param scaling_policy: Specifies the policy for automatically starting and shutting down clusters in a multi-cluster warehouse running in Auto-scale mode. Valid values are (case-insensitive): ``STANDARD`` | ``ECONOMY``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#scaling_policy Warehouse#scaling_policy}
        :param statement_queued_timeout_in_seconds: Object parameter that specifies the time, in seconds, a SQL statement (query, DDL, DML, etc.) can be queued on a warehouse before it is canceled by the system. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#statement_queued_timeout_in_seconds Warehouse#statement_queued_timeout_in_seconds}
        :param statement_timeout_in_seconds: Specifies the time, in seconds, after which a running SQL statement (query, DDL, DML, etc.) is canceled by the system. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#statement_timeout_in_seconds Warehouse#statement_timeout_in_seconds}
        :param warehouse_size: Specifies the size of the virtual warehouse. Valid values are (case-insensitive): ``XSMALL`` | ``X-SMALL`` | ``SMALL`` | ``MEDIUM`` | ``LARGE`` | ``XLARGE`` | ``X-LARGE`` | ``XXLARGE`` | ``X2LARGE`` | ``2X-LARGE`` | ``XXXLARGE`` | ``X3LARGE`` | ``3X-LARGE`` | ``X4LARGE`` | ``4X-LARGE`` | ``X5LARGE`` | ``5X-LARGE`` | ``X6LARGE`` | ``6X-LARGE``. Consult `warehouse documentation <https://docs.snowflake.com/en/sql-reference/sql/create-warehouse#optional-properties-objectproperties>`_ for the details. Note: removing the size from config will result in the resource recreation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#warehouse_size Warehouse#warehouse_size}
        :param warehouse_type: Specifies warehouse type. Valid values are (case-insensitive): ``STANDARD`` | ``SNOWPARK-OPTIMIZED``. Warehouse needs to be suspended to change its type. Provider will handle automatic suspension and resumption if needed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#warehouse_type Warehouse#warehouse_type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64f374449bfcb04875c974ead721be8454c4c46c8a3a696b4e9fd7fbc3003d99)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument auto_resume", value=auto_resume, expected_type=type_hints["auto_resume"])
            check_type(argname="argument auto_suspend", value=auto_suspend, expected_type=type_hints["auto_suspend"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument enable_query_acceleration", value=enable_query_acceleration, expected_type=type_hints["enable_query_acceleration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument initially_suspended", value=initially_suspended, expected_type=type_hints["initially_suspended"])
            check_type(argname="argument max_cluster_count", value=max_cluster_count, expected_type=type_hints["max_cluster_count"])
            check_type(argname="argument max_concurrency_level", value=max_concurrency_level, expected_type=type_hints["max_concurrency_level"])
            check_type(argname="argument min_cluster_count", value=min_cluster_count, expected_type=type_hints["min_cluster_count"])
            check_type(argname="argument query_acceleration_max_scale_factor", value=query_acceleration_max_scale_factor, expected_type=type_hints["query_acceleration_max_scale_factor"])
            check_type(argname="argument resource_monitor", value=resource_monitor, expected_type=type_hints["resource_monitor"])
            check_type(argname="argument scaling_policy", value=scaling_policy, expected_type=type_hints["scaling_policy"])
            check_type(argname="argument statement_queued_timeout_in_seconds", value=statement_queued_timeout_in_seconds, expected_type=type_hints["statement_queued_timeout_in_seconds"])
            check_type(argname="argument statement_timeout_in_seconds", value=statement_timeout_in_seconds, expected_type=type_hints["statement_timeout_in_seconds"])
            check_type(argname="argument warehouse_size", value=warehouse_size, expected_type=type_hints["warehouse_size"])
            check_type(argname="argument warehouse_type", value=warehouse_type, expected_type=type_hints["warehouse_type"])
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
        if auto_resume is not None:
            self._values["auto_resume"] = auto_resume
        if auto_suspend is not None:
            self._values["auto_suspend"] = auto_suspend
        if comment is not None:
            self._values["comment"] = comment
        if enable_query_acceleration is not None:
            self._values["enable_query_acceleration"] = enable_query_acceleration
        if id is not None:
            self._values["id"] = id
        if initially_suspended is not None:
            self._values["initially_suspended"] = initially_suspended
        if max_cluster_count is not None:
            self._values["max_cluster_count"] = max_cluster_count
        if max_concurrency_level is not None:
            self._values["max_concurrency_level"] = max_concurrency_level
        if min_cluster_count is not None:
            self._values["min_cluster_count"] = min_cluster_count
        if query_acceleration_max_scale_factor is not None:
            self._values["query_acceleration_max_scale_factor"] = query_acceleration_max_scale_factor
        if resource_monitor is not None:
            self._values["resource_monitor"] = resource_monitor
        if scaling_policy is not None:
            self._values["scaling_policy"] = scaling_policy
        if statement_queued_timeout_in_seconds is not None:
            self._values["statement_queued_timeout_in_seconds"] = statement_queued_timeout_in_seconds
        if statement_timeout_in_seconds is not None:
            self._values["statement_timeout_in_seconds"] = statement_timeout_in_seconds
        if warehouse_size is not None:
            self._values["warehouse_size"] = warehouse_size
        if warehouse_type is not None:
            self._values["warehouse_type"] = warehouse_type

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
        '''Identifier for the virtual warehouse;

        must be unique for your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#name Warehouse#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_resume(self) -> typing.Optional[builtins.str]:
        '''Specifies whether to automatically resume a warehouse when a SQL statement (e.g. query) is submitted to it. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#auto_resume Warehouse#auto_resume}
        '''
        result = self._values.get("auto_resume")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_suspend(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of seconds of inactivity after which a warehouse is automatically suspended.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#auto_suspend Warehouse#auto_suspend}
        '''
        result = self._values.get("auto_suspend")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the warehouse.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#comment Warehouse#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_query_acceleration(self) -> typing.Optional[builtins.str]:
        '''Specifies whether to enable the query acceleration service for queries that rely on this warehouse for compute resources.

        Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#enable_query_acceleration Warehouse#enable_query_acceleration}
        '''
        result = self._values.get("enable_query_acceleration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#id Warehouse#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initially_suspended(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the warehouse is created initially in the ‘Suspended’ state.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#initially_suspended Warehouse#initially_suspended}
        '''
        result = self._values.get("initially_suspended")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_cluster_count(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum number of server clusters for the warehouse.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#max_cluster_count Warehouse#max_cluster_count}
        '''
        result = self._values.get("max_cluster_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_concurrency_level(self) -> typing.Optional[jsii.Number]:
        '''Object parameter that specifies the concurrency level for SQL statements (i.e. queries and DML) executed by a warehouse.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#max_concurrency_level Warehouse#max_concurrency_level}
        '''
        result = self._values.get("max_concurrency_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_cluster_count(self) -> typing.Optional[jsii.Number]:
        '''Specifies the minimum number of server clusters for the warehouse (only applies to multi-cluster warehouses).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#min_cluster_count Warehouse#min_cluster_count}
        '''
        result = self._values.get("min_cluster_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def query_acceleration_max_scale_factor(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum scale factor for leasing compute resources for query acceleration.

        The scale factor is used as a multiplier based on warehouse size.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#query_acceleration_max_scale_factor Warehouse#query_acceleration_max_scale_factor}
        '''
        result = self._values.get("query_acceleration_max_scale_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_monitor(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of a resource monitor that is explicitly assigned to the warehouse.

        For more information about this resource, see `docs <./resource_monitor>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#resource_monitor Warehouse#resource_monitor}
        '''
        result = self._values.get("resource_monitor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies the policy for automatically starting and shutting down clusters in a multi-cluster warehouse running in Auto-scale mode.

        Valid values are (case-insensitive): ``STANDARD`` | ``ECONOMY``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#scaling_policy Warehouse#scaling_policy}
        '''
        result = self._values.get("scaling_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statement_queued_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Object parameter that specifies the time, in seconds, a SQL statement (query, DDL, DML, etc.) can be queued on a warehouse before it is canceled by the system.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#statement_queued_timeout_in_seconds Warehouse#statement_queued_timeout_in_seconds}
        '''
        result = self._values.get("statement_queued_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def statement_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Specifies the time, in seconds, after which a running SQL statement (query, DDL, DML, etc.) is canceled by the system.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#statement_timeout_in_seconds Warehouse#statement_timeout_in_seconds}
        '''
        result = self._values.get("statement_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def warehouse_size(self) -> typing.Optional[builtins.str]:
        '''Specifies the size of the virtual warehouse.

        Valid values are (case-insensitive): ``XSMALL`` | ``X-SMALL`` | ``SMALL`` | ``MEDIUM`` | ``LARGE`` | ``XLARGE`` | ``X-LARGE`` | ``XXLARGE`` | ``X2LARGE`` | ``2X-LARGE`` | ``XXXLARGE`` | ``X3LARGE`` | ``3X-LARGE`` | ``X4LARGE`` | ``4X-LARGE`` | ``X5LARGE`` | ``5X-LARGE`` | ``X6LARGE`` | ``6X-LARGE``. Consult `warehouse documentation <https://docs.snowflake.com/en/sql-reference/sql/create-warehouse#optional-properties-objectproperties>`_ for the details. Note: removing the size from config will result in the resource recreation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#warehouse_size Warehouse#warehouse_size}
        '''
        result = self._values.get("warehouse_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def warehouse_type(self) -> typing.Optional[builtins.str]:
        '''Specifies warehouse type.

        Valid values are (case-insensitive): ``STANDARD`` | ``SNOWPARK-OPTIMIZED``. Warehouse needs to be suspended to change its type. Provider will handle automatic suspension and resumption if needed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/warehouse#warehouse_type Warehouse#warehouse_type}
        '''
        result = self._values.get("warehouse_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WarehouseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.warehouse.WarehouseParameters",
    jsii_struct_bases=[],
    name_mapping={},
)
class WarehouseParameters:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WarehouseParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WarehouseParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.warehouse.WarehouseParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8759ece9b58d62bfbcc0136eb0456a7abe0fe76cf140767e9928d692bfd175fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "WarehouseParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b4745377f23d99152877b79cd9701a7c58eabc6b89752dca67df9e238db49bb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WarehouseParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a32e949ef4ad68a3326a14425f281e8bb4b31319e884c5695baaf2c344e9164)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2226677ef556ca6329487ef68a15160d7eec52c4d0550f36421e0b83e9447b53)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93d6fea89c04b4b0128b688d5557949cfcb49189c191527c2b8b437453ba6e83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.warehouse.WarehouseParametersMaxConcurrencyLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class WarehouseParametersMaxConcurrencyLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WarehouseParametersMaxConcurrencyLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WarehouseParametersMaxConcurrencyLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.warehouse.WarehouseParametersMaxConcurrencyLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a46a0303e84fd7e5efde6d4ff86db93e402c7158295198277114b7342a62193)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WarehouseParametersMaxConcurrencyLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a9cccb6e233479dce51194dd0665d5029a27cb4edfbbbc3df975a034c41a30c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WarehouseParametersMaxConcurrencyLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de68acec3be596d832a7c88ab5ef87fe9e86ee890a995913b27b7e840702613f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cab4c7b8709c86cd45533d11c4c9de506ccb52d0d4220f72a5631def1be2036b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2ed22487bad45f13c37ee3329e23fdbf46b582069e618c0aead316d5a6fbc99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class WarehouseParametersMaxConcurrencyLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.warehouse.WarehouseParametersMaxConcurrencyLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__177b7f8fbb1844dc93075653aa5a8723ef491372dc616f3c467eb0f24ba18335)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WarehouseParametersMaxConcurrencyLevel]:
        return typing.cast(typing.Optional[WarehouseParametersMaxConcurrencyLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WarehouseParametersMaxConcurrencyLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05a4d5e7f4fc9189af3fbfe775655d623ff621f6034360efedeadfed348f0748)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WarehouseParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.warehouse.WarehouseParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a3aadeea3a768082b5cedc9aa44ee0d6ff1aeb73cdde92029d7e9119b1fcd53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="maxConcurrencyLevel")
    def max_concurrency_level(self) -> WarehouseParametersMaxConcurrencyLevelList:
        return typing.cast(WarehouseParametersMaxConcurrencyLevelList, jsii.get(self, "maxConcurrencyLevel"))

    @builtins.property
    @jsii.member(jsii_name="statementQueuedTimeoutInSeconds")
    def statement_queued_timeout_in_seconds(
        self,
    ) -> "WarehouseParametersStatementQueuedTimeoutInSecondsList":
        return typing.cast("WarehouseParametersStatementQueuedTimeoutInSecondsList", jsii.get(self, "statementQueuedTimeoutInSeconds"))

    @builtins.property
    @jsii.member(jsii_name="statementTimeoutInSeconds")
    def statement_timeout_in_seconds(
        self,
    ) -> "WarehouseParametersStatementTimeoutInSecondsList":
        return typing.cast("WarehouseParametersStatementTimeoutInSecondsList", jsii.get(self, "statementTimeoutInSeconds"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WarehouseParameters]:
        return typing.cast(typing.Optional[WarehouseParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[WarehouseParameters]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15fc840999fe14b028d120ede685fd6425f5cc3e20071ef0659c952e3b7aa235)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.warehouse.WarehouseParametersStatementQueuedTimeoutInSeconds",
    jsii_struct_bases=[],
    name_mapping={},
)
class WarehouseParametersStatementQueuedTimeoutInSeconds:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WarehouseParametersStatementQueuedTimeoutInSeconds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WarehouseParametersStatementQueuedTimeoutInSecondsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.warehouse.WarehouseParametersStatementQueuedTimeoutInSecondsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b096357f30177f5029a74d247173f1a39a1cfddb307d79cdec64f8c6d7b04a02)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WarehouseParametersStatementQueuedTimeoutInSecondsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89595bc7b04b0329c4325f34befa65e0d5fdcdc25d3cccd5ec58fbea8cc956fe)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WarehouseParametersStatementQueuedTimeoutInSecondsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb9298655207889bffdcf898af0387f3c6635217842880ab892a1855138c81e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be1f61c3c7fa56c6fe1b75c7ea924b8441c8387759d99d90d9af263812d9dd9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd1cfe49d234f09b7cfd3628cebffe450edb5c63ea55a2921b33bc53d6703b66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class WarehouseParametersStatementQueuedTimeoutInSecondsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.warehouse.WarehouseParametersStatementQueuedTimeoutInSecondsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a0e19d78090c1640411bb952d8c38ce3d37368393693d288263e89dbf66df6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WarehouseParametersStatementQueuedTimeoutInSeconds]:
        return typing.cast(typing.Optional[WarehouseParametersStatementQueuedTimeoutInSeconds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WarehouseParametersStatementQueuedTimeoutInSeconds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6e9dc8f4c1b53e79c5920694bf90dc00daea168477af10a4165eb96e6610d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.warehouse.WarehouseParametersStatementTimeoutInSeconds",
    jsii_struct_bases=[],
    name_mapping={},
)
class WarehouseParametersStatementTimeoutInSeconds:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WarehouseParametersStatementTimeoutInSeconds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WarehouseParametersStatementTimeoutInSecondsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.warehouse.WarehouseParametersStatementTimeoutInSecondsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a24c064cb38424cbfd5b1a7cee15592155d71b9887e0516a3ed9bca3f6034607)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WarehouseParametersStatementTimeoutInSecondsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2185a51aec18e00d8476ad8fd0293e065db8c60aaeb81a01207aad41e45cd0a0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WarehouseParametersStatementTimeoutInSecondsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba973cbf58a5a420ec75364fd2aa511844de84033116195873ec5293ecc16aa8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5ed173aa714adee19f34add0035b77b37ca6c27a6fb8658038720e268a39d9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__079591db5f07a4781631e5354018577ae22334f42324ecd85a80e7efe9b380f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class WarehouseParametersStatementTimeoutInSecondsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.warehouse.WarehouseParametersStatementTimeoutInSecondsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__043c683ac2aba2ccb71732d12f3582ccca4ec79496dd0313f151c4f0ce8ee7a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WarehouseParametersStatementTimeoutInSeconds]:
        return typing.cast(typing.Optional[WarehouseParametersStatementTimeoutInSeconds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WarehouseParametersStatementTimeoutInSeconds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b0a4fb5ebbd6557460da164ddde447d4b3d170aa43d3790811b64fc0990d1c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.warehouse.WarehouseShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class WarehouseShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WarehouseShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WarehouseShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.warehouse.WarehouseShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d382051715d738d199ed5bb4104777a4727f1711d8fc7aaf3b24c6daac4e40e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "WarehouseShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4d3fc9501a844595b112a2fe7b2529c660158f20e1430ab7a8163736fb0e71f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WarehouseShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2aa746ffa83cb793cc2c34b346958145dac6816305f1bfb64219a1469c56018)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9540df7de6802e85eb4e8aa0c4194bcc8df7c78a1d93da7466f3cabb38b5d033)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bd68b79aa10690ec514ec9fb22550117426ceb177951574e22dd220eb05edfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class WarehouseShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.warehouse.WarehouseShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e1368c125ff8ef9845019794fcd88c359dfbda64a5db12db65f74c7a0b4be81)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="autoResume")
    def auto_resume(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "autoResume"))

    @builtins.property
    @jsii.member(jsii_name="autoSuspend")
    def auto_suspend(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autoSuspend"))

    @builtins.property
    @jsii.member(jsii_name="available")
    def available(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "available"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @builtins.property
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="enableQueryAcceleration")
    def enable_query_acceleration(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enableQueryAcceleration"))

    @builtins.property
    @jsii.member(jsii_name="isCurrent")
    def is_current(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isCurrent"))

    @builtins.property
    @jsii.member(jsii_name="isDefault")
    def is_default(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isDefault"))

    @builtins.property
    @jsii.member(jsii_name="maxClusterCount")
    def max_cluster_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxClusterCount"))

    @builtins.property
    @jsii.member(jsii_name="minClusterCount")
    def min_cluster_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minClusterCount"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="other")
    def other(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "other"))

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @builtins.property
    @jsii.member(jsii_name="ownerRoleType")
    def owner_role_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownerRoleType"))

    @builtins.property
    @jsii.member(jsii_name="provisioning")
    def provisioning(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisioning"))

    @builtins.property
    @jsii.member(jsii_name="queryAccelerationMaxScaleFactor")
    def query_acceleration_max_scale_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queryAccelerationMaxScaleFactor"))

    @builtins.property
    @jsii.member(jsii_name="queued")
    def queued(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queued"))

    @builtins.property
    @jsii.member(jsii_name="quiescing")
    def quiescing(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "quiescing"))

    @builtins.property
    @jsii.member(jsii_name="resourceMonitor")
    def resource_monitor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceMonitor"))

    @builtins.property
    @jsii.member(jsii_name="resumedOn")
    def resumed_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resumedOn"))

    @builtins.property
    @jsii.member(jsii_name="running")
    def running(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "running"))

    @builtins.property
    @jsii.member(jsii_name="scalingPolicy")
    def scaling_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingPolicy"))

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "size"))

    @builtins.property
    @jsii.member(jsii_name="startedClusters")
    def started_clusters(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startedClusters"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="updatedOn")
    def updated_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedOn"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WarehouseShowOutput]:
        return typing.cast(typing.Optional[WarehouseShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[WarehouseShowOutput]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1ac8b69bb8d4a7bb6297bda601965fc6c2a10decab7add4c1653ccc694242aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Warehouse",
    "WarehouseConfig",
    "WarehouseParameters",
    "WarehouseParametersList",
    "WarehouseParametersMaxConcurrencyLevel",
    "WarehouseParametersMaxConcurrencyLevelList",
    "WarehouseParametersMaxConcurrencyLevelOutputReference",
    "WarehouseParametersOutputReference",
    "WarehouseParametersStatementQueuedTimeoutInSeconds",
    "WarehouseParametersStatementQueuedTimeoutInSecondsList",
    "WarehouseParametersStatementQueuedTimeoutInSecondsOutputReference",
    "WarehouseParametersStatementTimeoutInSeconds",
    "WarehouseParametersStatementTimeoutInSecondsList",
    "WarehouseParametersStatementTimeoutInSecondsOutputReference",
    "WarehouseShowOutput",
    "WarehouseShowOutputList",
    "WarehouseShowOutputOutputReference",
]

publication.publish()

def _typecheckingstub__f7a545b9470ddbc13f6797573fe9db4caad9ea0ec20a416254e98f74ad315894(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    auto_resume: typing.Optional[builtins.str] = None,
    auto_suspend: typing.Optional[jsii.Number] = None,
    comment: typing.Optional[builtins.str] = None,
    enable_query_acceleration: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    initially_suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_cluster_count: typing.Optional[jsii.Number] = None,
    max_concurrency_level: typing.Optional[jsii.Number] = None,
    min_cluster_count: typing.Optional[jsii.Number] = None,
    query_acceleration_max_scale_factor: typing.Optional[jsii.Number] = None,
    resource_monitor: typing.Optional[builtins.str] = None,
    scaling_policy: typing.Optional[builtins.str] = None,
    statement_queued_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    statement_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    warehouse_size: typing.Optional[builtins.str] = None,
    warehouse_type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__572da37f5bf450cb7fe3f011f5e0e5d584f32856d369188d26ecdd2bed0c8cea(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e363e0e719321b9f36ba95f42412180d8c83bca4f70f5f58bf54d11faaca1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e33c40876b47a58a42eafec0c16bfa190228c08a23a39eea9350f0f083d61dd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4c985a73dcb01e461dd3d79db0b1b2b150d1b6ad292921dd0553f38596bff56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a9dd2dcf21eba130519e20959255cf814826077dc1a2486f912d9091569c61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46603b6d33e982986e0b443f6a5696f6a33454cc6e0aa6678817badd8cd756ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d176a43f31805f67ca01f79890fb1058791b57d84f2115996086f337ed2e1f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba9c5ca5c139d131448b0430ff14223b8e4d4bb0a0fd5b55adffbbe7796824f7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1a76dc728c5c13221da328191e3e3c34cc72784972ed2e3fc82897c41a05e8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b96edb769e4b81e3cd326f1bc18a50dd3c4dac86feefc24a81934fafe5f777a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7077b71c10d32de0bc3d3c8d12117d655ce00aa136fc82b6a7c73b6d0ec8599(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f96be4446754d4205d1e9d99a2c4abcb4828cb58dbd27f26e599e94fb3c26020(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8e4b5fc94f6dc0de4811839fa018a79668ca9d8203c01cfb6f125c1c11eb185(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da84474f179556752719c65f7b2440f46eb949691133a2f9714d5686438334d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a106de57372b520a40ffb364b03b9b17f28f3178d2a39b83f02ec994035f8e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__142317704b4892b91eab76a9f614fe8251c78e43a9ab129e89de9d627f23595b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb682cffa8639019a3d246df698597f1933be487556ff7d66681abdaec17a65a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2ec6ca1e83f9784c4d21dfe7ac241ada21747ef3247184dfea371249ab7f05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f374449bfcb04875c974ead721be8454c4c46c8a3a696b4e9fd7fbc3003d99(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    auto_resume: typing.Optional[builtins.str] = None,
    auto_suspend: typing.Optional[jsii.Number] = None,
    comment: typing.Optional[builtins.str] = None,
    enable_query_acceleration: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    initially_suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_cluster_count: typing.Optional[jsii.Number] = None,
    max_concurrency_level: typing.Optional[jsii.Number] = None,
    min_cluster_count: typing.Optional[jsii.Number] = None,
    query_acceleration_max_scale_factor: typing.Optional[jsii.Number] = None,
    resource_monitor: typing.Optional[builtins.str] = None,
    scaling_policy: typing.Optional[builtins.str] = None,
    statement_queued_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    statement_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    warehouse_size: typing.Optional[builtins.str] = None,
    warehouse_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8759ece9b58d62bfbcc0136eb0456a7abe0fe76cf140767e9928d692bfd175fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b4745377f23d99152877b79cd9701a7c58eabc6b89752dca67df9e238db49bb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a32e949ef4ad68a3326a14425f281e8bb4b31319e884c5695baaf2c344e9164(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2226677ef556ca6329487ef68a15160d7eec52c4d0550f36421e0b83e9447b53(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d6fea89c04b4b0128b688d5557949cfcb49189c191527c2b8b437453ba6e83(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a46a0303e84fd7e5efde6d4ff86db93e402c7158295198277114b7342a62193(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9cccb6e233479dce51194dd0665d5029a27cb4edfbbbc3df975a034c41a30c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de68acec3be596d832a7c88ab5ef87fe9e86ee890a995913b27b7e840702613f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cab4c7b8709c86cd45533d11c4c9de506ccb52d0d4220f72a5631def1be2036b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2ed22487bad45f13c37ee3329e23fdbf46b582069e618c0aead316d5a6fbc99(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177b7f8fbb1844dc93075653aa5a8723ef491372dc616f3c467eb0f24ba18335(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05a4d5e7f4fc9189af3fbfe775655d623ff621f6034360efedeadfed348f0748(
    value: typing.Optional[WarehouseParametersMaxConcurrencyLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a3aadeea3a768082b5cedc9aa44ee0d6ff1aeb73cdde92029d7e9119b1fcd53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15fc840999fe14b028d120ede685fd6425f5cc3e20071ef0659c952e3b7aa235(
    value: typing.Optional[WarehouseParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b096357f30177f5029a74d247173f1a39a1cfddb307d79cdec64f8c6d7b04a02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89595bc7b04b0329c4325f34befa65e0d5fdcdc25d3cccd5ec58fbea8cc956fe(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb9298655207889bffdcf898af0387f3c6635217842880ab892a1855138c81e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1f61c3c7fa56c6fe1b75c7ea924b8441c8387759d99d90d9af263812d9dd9e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd1cfe49d234f09b7cfd3628cebffe450edb5c63ea55a2921b33bc53d6703b66(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a0e19d78090c1640411bb952d8c38ce3d37368393693d288263e89dbf66df6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6e9dc8f4c1b53e79c5920694bf90dc00daea168477af10a4165eb96e6610d5e(
    value: typing.Optional[WarehouseParametersStatementQueuedTimeoutInSeconds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a24c064cb38424cbfd5b1a7cee15592155d71b9887e0516a3ed9bca3f6034607(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2185a51aec18e00d8476ad8fd0293e065db8c60aaeb81a01207aad41e45cd0a0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba973cbf58a5a420ec75364fd2aa511844de84033116195873ec5293ecc16aa8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5ed173aa714adee19f34add0035b77b37ca6c27a6fb8658038720e268a39d9e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__079591db5f07a4781631e5354018577ae22334f42324ecd85a80e7efe9b380f5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__043c683ac2aba2ccb71732d12f3582ccca4ec79496dd0313f151c4f0ce8ee7a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b0a4fb5ebbd6557460da164ddde447d4b3d170aa43d3790811b64fc0990d1c9(
    value: typing.Optional[WarehouseParametersStatementTimeoutInSeconds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d382051715d738d199ed5bb4104777a4727f1711d8fc7aaf3b24c6daac4e40e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d3fc9501a844595b112a2fe7b2529c660158f20e1430ab7a8163736fb0e71f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2aa746ffa83cb793cc2c34b346958145dac6816305f1bfb64219a1469c56018(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9540df7de6802e85eb4e8aa0c4194bcc8df7c78a1d93da7466f3cabb38b5d033(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bd68b79aa10690ec514ec9fb22550117426ceb177951574e22dd220eb05edfe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e1368c125ff8ef9845019794fcd88c359dfbda64a5db12db65f74c7a0b4be81(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ac8b69bb8d4a7bb6297bda601965fc6c2a10decab7add4c1653ccc694242aa(
    value: typing.Optional[WarehouseShowOutput],
) -> None:
    """Type checking stubs"""
    pass
