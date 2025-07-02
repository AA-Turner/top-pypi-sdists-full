r'''
# `azurerm_mssql_job_step`

Refer to the Terraform Registry for docs: [`azurerm_mssql_job_step`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step).
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


class MssqlJobStep(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlJobStep.MssqlJobStep",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step azurerm_mssql_job_step}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        job_credential_id: builtins.str,
        job_id: builtins.str,
        job_step_index: jsii.Number,
        job_target_group_id: builtins.str,
        name: builtins.str,
        sql_script: builtins.str,
        id: typing.Optional[builtins.str] = None,
        initial_retry_interval_seconds: typing.Optional[jsii.Number] = None,
        maximum_retry_interval_seconds: typing.Optional[jsii.Number] = None,
        output_target: typing.Optional[typing.Union["MssqlJobStepOutputTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        retry_interval_backoff_multiplier: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["MssqlJobStepTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step azurerm_mssql_job_step} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param job_credential_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#job_credential_id MssqlJobStep#job_credential_id}.
        :param job_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#job_id MssqlJobStep#job_id}.
        :param job_step_index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#job_step_index MssqlJobStep#job_step_index}.
        :param job_target_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#job_target_group_id MssqlJobStep#job_target_group_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#name MssqlJobStep#name}.
        :param sql_script: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#sql_script MssqlJobStep#sql_script}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#id MssqlJobStep#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_retry_interval_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#initial_retry_interval_seconds MssqlJobStep#initial_retry_interval_seconds}.
        :param maximum_retry_interval_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#maximum_retry_interval_seconds MssqlJobStep#maximum_retry_interval_seconds}.
        :param output_target: output_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#output_target MssqlJobStep#output_target}
        :param retry_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#retry_attempts MssqlJobStep#retry_attempts}.
        :param retry_interval_backoff_multiplier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#retry_interval_backoff_multiplier MssqlJobStep#retry_interval_backoff_multiplier}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#timeouts MssqlJobStep#timeouts}
        :param timeout_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#timeout_seconds MssqlJobStep#timeout_seconds}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50a3fc13c1cef3ac4540a9046b47de0ccca1502751deb463c8bbd1b1c6294f96)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MssqlJobStepConfig(
            job_credential_id=job_credential_id,
            job_id=job_id,
            job_step_index=job_step_index,
            job_target_group_id=job_target_group_id,
            name=name,
            sql_script=sql_script,
            id=id,
            initial_retry_interval_seconds=initial_retry_interval_seconds,
            maximum_retry_interval_seconds=maximum_retry_interval_seconds,
            output_target=output_target,
            retry_attempts=retry_attempts,
            retry_interval_backoff_multiplier=retry_interval_backoff_multiplier,
            timeouts=timeouts,
            timeout_seconds=timeout_seconds,
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
        '''Generates CDKTF code for importing a MssqlJobStep resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MssqlJobStep to import.
        :param import_from_id: The id of the existing MssqlJobStep that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MssqlJobStep to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f795c6a1e45db7bd91617344f6baedd874779387cee7ea3a28416f9839ad68ec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putOutputTarget")
    def put_output_target(
        self,
        *,
        job_credential_id: builtins.str,
        mssql_database_id: builtins.str,
        table_name: builtins.str,
        schema_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param job_credential_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#job_credential_id MssqlJobStep#job_credential_id}.
        :param mssql_database_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#mssql_database_id MssqlJobStep#mssql_database_id}.
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#table_name MssqlJobStep#table_name}.
        :param schema_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#schema_name MssqlJobStep#schema_name}.
        '''
        value = MssqlJobStepOutputTarget(
            job_credential_id=job_credential_id,
            mssql_database_id=mssql_database_id,
            table_name=table_name,
            schema_name=schema_name,
        )

        return typing.cast(None, jsii.invoke(self, "putOutputTarget", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#create MssqlJobStep#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#delete MssqlJobStep#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#read MssqlJobStep#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#update MssqlJobStep#update}.
        '''
        value = MssqlJobStepTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInitialRetryIntervalSeconds")
    def reset_initial_retry_interval_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialRetryIntervalSeconds", []))

    @jsii.member(jsii_name="resetMaximumRetryIntervalSeconds")
    def reset_maximum_retry_interval_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumRetryIntervalSeconds", []))

    @jsii.member(jsii_name="resetOutputTarget")
    def reset_output_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputTarget", []))

    @jsii.member(jsii_name="resetRetryAttempts")
    def reset_retry_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryAttempts", []))

    @jsii.member(jsii_name="resetRetryIntervalBackoffMultiplier")
    def reset_retry_interval_backoff_multiplier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryIntervalBackoffMultiplier", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTimeoutSeconds")
    def reset_timeout_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutSeconds", []))

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
    @jsii.member(jsii_name="outputTarget")
    def output_target(self) -> "MssqlJobStepOutputTargetOutputReference":
        return typing.cast("MssqlJobStepOutputTargetOutputReference", jsii.get(self, "outputTarget"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MssqlJobStepTimeoutsOutputReference":
        return typing.cast("MssqlJobStepTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="initialRetryIntervalSecondsInput")
    def initial_retry_interval_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialRetryIntervalSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="jobCredentialIdInput")
    def job_credential_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobCredentialIdInput"))

    @builtins.property
    @jsii.member(jsii_name="jobIdInput")
    def job_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobIdInput"))

    @builtins.property
    @jsii.member(jsii_name="jobStepIndexInput")
    def job_step_index_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "jobStepIndexInput"))

    @builtins.property
    @jsii.member(jsii_name="jobTargetGroupIdInput")
    def job_target_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobTargetGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumRetryIntervalSecondsInput")
    def maximum_retry_interval_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumRetryIntervalSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="outputTargetInput")
    def output_target_input(self) -> typing.Optional["MssqlJobStepOutputTarget"]:
        return typing.cast(typing.Optional["MssqlJobStepOutputTarget"], jsii.get(self, "outputTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="retryAttemptsInput")
    def retry_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="retryIntervalBackoffMultiplierInput")
    def retry_interval_backoff_multiplier_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryIntervalBackoffMultiplierInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlScriptInput")
    def sql_script_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlScriptInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecondsInput")
    def timeout_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MssqlJobStepTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MssqlJobStepTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bce17a1091d582b2de612020d9522b8831ebccd38339f75e520eadb0e7efa15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialRetryIntervalSeconds")
    def initial_retry_interval_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialRetryIntervalSeconds"))

    @initial_retry_interval_seconds.setter
    def initial_retry_interval_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__270777cd36ab0f5bb67bf75c33a4eac622e4744bb4c85a0fdd1308bfbf681368)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialRetryIntervalSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobCredentialId")
    def job_credential_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobCredentialId"))

    @job_credential_id.setter
    def job_credential_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eac272b802e1f5d481d67efa221695e0b7337ed7278765fbd5dc6a2da673c55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobCredentialId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobId")
    def job_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobId"))

    @job_id.setter
    def job_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fd67d3099273677edcdcc6fa060aad12225f0e6042ca40674aed6c2fb584277)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobStepIndex")
    def job_step_index(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "jobStepIndex"))

    @job_step_index.setter
    def job_step_index(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5a80691b7d07f98c09adb819c64415679627abec353192eea43b3f97ad3769a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobStepIndex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobTargetGroupId")
    def job_target_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobTargetGroupId"))

    @job_target_group_id.setter
    def job_target_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97544c90fed64964010d2ad7a5af30bbbaefd4cbf8f6370eba2516fb0a5d3016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobTargetGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumRetryIntervalSeconds")
    def maximum_retry_interval_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumRetryIntervalSeconds"))

    @maximum_retry_interval_seconds.setter
    def maximum_retry_interval_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acde688bb8fc00d3de63fd1fe4221ce3c2c9f8a396f8bbebbc1e2c665fade199)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumRetryIntervalSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0b689f5953ca10f3cce198423004c10cf0ebbda8181160b0c522056b412229b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryAttempts")
    def retry_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retryAttempts"))

    @retry_attempts.setter
    def retry_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07b6aa0cb40338990ac033cb45e6d37acdebdb99f8626a3a290a6870511ec4dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryIntervalBackoffMultiplier")
    def retry_interval_backoff_multiplier(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retryIntervalBackoffMultiplier"))

    @retry_interval_backoff_multiplier.setter
    def retry_interval_backoff_multiplier(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e0d95fdb66d5a20214918ca1a5dc000190d5f2a3a9cbd135ee0a7d69645685e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryIntervalBackoffMultiplier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlScript")
    def sql_script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlScript"))

    @sql_script.setter
    def sql_script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78f551e20964ce46c264926d7deae8bb4784f095f1295f13d5619deab0687fef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlScript", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7108b7bd8c78ce06f034ff292de77c49e81013f70fa78a66768867cf52fee57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlJobStep.MssqlJobStepConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "job_credential_id": "jobCredentialId",
        "job_id": "jobId",
        "job_step_index": "jobStepIndex",
        "job_target_group_id": "jobTargetGroupId",
        "name": "name",
        "sql_script": "sqlScript",
        "id": "id",
        "initial_retry_interval_seconds": "initialRetryIntervalSeconds",
        "maximum_retry_interval_seconds": "maximumRetryIntervalSeconds",
        "output_target": "outputTarget",
        "retry_attempts": "retryAttempts",
        "retry_interval_backoff_multiplier": "retryIntervalBackoffMultiplier",
        "timeouts": "timeouts",
        "timeout_seconds": "timeoutSeconds",
    },
)
class MssqlJobStepConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        job_credential_id: builtins.str,
        job_id: builtins.str,
        job_step_index: jsii.Number,
        job_target_group_id: builtins.str,
        name: builtins.str,
        sql_script: builtins.str,
        id: typing.Optional[builtins.str] = None,
        initial_retry_interval_seconds: typing.Optional[jsii.Number] = None,
        maximum_retry_interval_seconds: typing.Optional[jsii.Number] = None,
        output_target: typing.Optional[typing.Union["MssqlJobStepOutputTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        retry_interval_backoff_multiplier: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["MssqlJobStepTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param job_credential_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#job_credential_id MssqlJobStep#job_credential_id}.
        :param job_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#job_id MssqlJobStep#job_id}.
        :param job_step_index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#job_step_index MssqlJobStep#job_step_index}.
        :param job_target_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#job_target_group_id MssqlJobStep#job_target_group_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#name MssqlJobStep#name}.
        :param sql_script: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#sql_script MssqlJobStep#sql_script}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#id MssqlJobStep#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_retry_interval_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#initial_retry_interval_seconds MssqlJobStep#initial_retry_interval_seconds}.
        :param maximum_retry_interval_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#maximum_retry_interval_seconds MssqlJobStep#maximum_retry_interval_seconds}.
        :param output_target: output_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#output_target MssqlJobStep#output_target}
        :param retry_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#retry_attempts MssqlJobStep#retry_attempts}.
        :param retry_interval_backoff_multiplier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#retry_interval_backoff_multiplier MssqlJobStep#retry_interval_backoff_multiplier}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#timeouts MssqlJobStep#timeouts}
        :param timeout_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#timeout_seconds MssqlJobStep#timeout_seconds}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(output_target, dict):
            output_target = MssqlJobStepOutputTarget(**output_target)
        if isinstance(timeouts, dict):
            timeouts = MssqlJobStepTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bfb8533effb12e13d1d80eb2c989e4ad03bb7e2da8d0e04d26d4262f3b0c46b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument job_credential_id", value=job_credential_id, expected_type=type_hints["job_credential_id"])
            check_type(argname="argument job_id", value=job_id, expected_type=type_hints["job_id"])
            check_type(argname="argument job_step_index", value=job_step_index, expected_type=type_hints["job_step_index"])
            check_type(argname="argument job_target_group_id", value=job_target_group_id, expected_type=type_hints["job_target_group_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sql_script", value=sql_script, expected_type=type_hints["sql_script"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument initial_retry_interval_seconds", value=initial_retry_interval_seconds, expected_type=type_hints["initial_retry_interval_seconds"])
            check_type(argname="argument maximum_retry_interval_seconds", value=maximum_retry_interval_seconds, expected_type=type_hints["maximum_retry_interval_seconds"])
            check_type(argname="argument output_target", value=output_target, expected_type=type_hints["output_target"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument retry_interval_backoff_multiplier", value=retry_interval_backoff_multiplier, expected_type=type_hints["retry_interval_backoff_multiplier"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument timeout_seconds", value=timeout_seconds, expected_type=type_hints["timeout_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "job_credential_id": job_credential_id,
            "job_id": job_id,
            "job_step_index": job_step_index,
            "job_target_group_id": job_target_group_id,
            "name": name,
            "sql_script": sql_script,
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
        if id is not None:
            self._values["id"] = id
        if initial_retry_interval_seconds is not None:
            self._values["initial_retry_interval_seconds"] = initial_retry_interval_seconds
        if maximum_retry_interval_seconds is not None:
            self._values["maximum_retry_interval_seconds"] = maximum_retry_interval_seconds
        if output_target is not None:
            self._values["output_target"] = output_target
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if retry_interval_backoff_multiplier is not None:
            self._values["retry_interval_backoff_multiplier"] = retry_interval_backoff_multiplier
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if timeout_seconds is not None:
            self._values["timeout_seconds"] = timeout_seconds

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
    def job_credential_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#job_credential_id MssqlJobStep#job_credential_id}.'''
        result = self._values.get("job_credential_id")
        assert result is not None, "Required property 'job_credential_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def job_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#job_id MssqlJobStep#job_id}.'''
        result = self._values.get("job_id")
        assert result is not None, "Required property 'job_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def job_step_index(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#job_step_index MssqlJobStep#job_step_index}.'''
        result = self._values.get("job_step_index")
        assert result is not None, "Required property 'job_step_index' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def job_target_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#job_target_group_id MssqlJobStep#job_target_group_id}.'''
        result = self._values.get("job_target_group_id")
        assert result is not None, "Required property 'job_target_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#name MssqlJobStep#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sql_script(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#sql_script MssqlJobStep#sql_script}.'''
        result = self._values.get("sql_script")
        assert result is not None, "Required property 'sql_script' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#id MssqlJobStep#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_retry_interval_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#initial_retry_interval_seconds MssqlJobStep#initial_retry_interval_seconds}.'''
        result = self._values.get("initial_retry_interval_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_retry_interval_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#maximum_retry_interval_seconds MssqlJobStep#maximum_retry_interval_seconds}.'''
        result = self._values.get("maximum_retry_interval_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def output_target(self) -> typing.Optional["MssqlJobStepOutputTarget"]:
        '''output_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#output_target MssqlJobStep#output_target}
        '''
        result = self._values.get("output_target")
        return typing.cast(typing.Optional["MssqlJobStepOutputTarget"], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#retry_attempts MssqlJobStep#retry_attempts}.'''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_interval_backoff_multiplier(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#retry_interval_backoff_multiplier MssqlJobStep#retry_interval_backoff_multiplier}.'''
        result = self._values.get("retry_interval_backoff_multiplier")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MssqlJobStepTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#timeouts MssqlJobStep#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MssqlJobStepTimeouts"], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#timeout_seconds MssqlJobStep#timeout_seconds}.'''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlJobStepConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlJobStep.MssqlJobStepOutputTarget",
    jsii_struct_bases=[],
    name_mapping={
        "job_credential_id": "jobCredentialId",
        "mssql_database_id": "mssqlDatabaseId",
        "table_name": "tableName",
        "schema_name": "schemaName",
    },
)
class MssqlJobStepOutputTarget:
    def __init__(
        self,
        *,
        job_credential_id: builtins.str,
        mssql_database_id: builtins.str,
        table_name: builtins.str,
        schema_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param job_credential_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#job_credential_id MssqlJobStep#job_credential_id}.
        :param mssql_database_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#mssql_database_id MssqlJobStep#mssql_database_id}.
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#table_name MssqlJobStep#table_name}.
        :param schema_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#schema_name MssqlJobStep#schema_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf7ec0dba18bb4132545c0e695048da68b9666ee4f200524c02ce6c08e0baa00)
            check_type(argname="argument job_credential_id", value=job_credential_id, expected_type=type_hints["job_credential_id"])
            check_type(argname="argument mssql_database_id", value=mssql_database_id, expected_type=type_hints["mssql_database_id"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument schema_name", value=schema_name, expected_type=type_hints["schema_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "job_credential_id": job_credential_id,
            "mssql_database_id": mssql_database_id,
            "table_name": table_name,
        }
        if schema_name is not None:
            self._values["schema_name"] = schema_name

    @builtins.property
    def job_credential_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#job_credential_id MssqlJobStep#job_credential_id}.'''
        result = self._values.get("job_credential_id")
        assert result is not None, "Required property 'job_credential_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mssql_database_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#mssql_database_id MssqlJobStep#mssql_database_id}.'''
        result = self._values.get("mssql_database_id")
        assert result is not None, "Required property 'mssql_database_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#table_name MssqlJobStep#table_name}.'''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#schema_name MssqlJobStep#schema_name}.'''
        result = self._values.get("schema_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlJobStepOutputTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlJobStepOutputTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlJobStep.MssqlJobStepOutputTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__adc96f8054de4f725e7e0ffafce5cb7d1ea0f779bf7677a744e80b48d17bcfc5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSchemaName")
    def reset_schema_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaName", []))

    @builtins.property
    @jsii.member(jsii_name="jobCredentialIdInput")
    def job_credential_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobCredentialIdInput"))

    @builtins.property
    @jsii.member(jsii_name="mssqlDatabaseIdInput")
    def mssql_database_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mssqlDatabaseIdInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaNameInput")
    def schema_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="jobCredentialId")
    def job_credential_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobCredentialId"))

    @job_credential_id.setter
    def job_credential_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71f862967fce18971df60dc8ae2995414c28f475a8bb76cce460d9a06cf16b0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobCredentialId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mssqlDatabaseId")
    def mssql_database_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mssqlDatabaseId"))

    @mssql_database_id.setter
    def mssql_database_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__796b9009f37020a4c20c148ec821b3b0bc4f595956c84461361eaec2d684d27a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mssqlDatabaseId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schemaName")
    def schema_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaName"))

    @schema_name.setter
    def schema_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ef0a527f1c2e07c3e6acbfdd431a2a6cc0ff1206f972ee3f77588c3aae55217)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1bbb99967d17a3d5e352a144ba4b895e1aa3c1b2386a969fa6f68310b9c62d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MssqlJobStepOutputTarget]:
        return typing.cast(typing.Optional[MssqlJobStepOutputTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[MssqlJobStepOutputTarget]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1701b9dbfda141366dfbe123222363bb76c12c1eef9602173149aa6e053025a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlJobStep.MssqlJobStepTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MssqlJobStepTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#create MssqlJobStep#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#delete MssqlJobStep#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#read MssqlJobStep#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#update MssqlJobStep#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73dc186c0422dc63026b01aa7dea49736a70769b644825ab5eb914c24141394c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#create MssqlJobStep#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#delete MssqlJobStep#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#read MssqlJobStep#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_job_step#update MssqlJobStep#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlJobStepTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlJobStepTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlJobStep.MssqlJobStepTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aade16a984db216b95d33b2d20dfd4edc023102a94976bb81bc7f965d36f798a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c5b78a004e57e5644c54bd561676175aa227e93b89452a441fcfce2c6d3a24c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d7de1118f24e2ccd2ed9774c14c65fba655433e8f69155ef4394481884eb65b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__916fbbfbb5132ff1fbb63f635ff2c7c511110757d3058138947b984514c668db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f538ed2b9384516c5346bfac8e20dde48be4e845413545536c52e06d1a1761)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlJobStepTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlJobStepTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlJobStepTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1858effe181cc429d0edb918ce03900214cd3cdc62dfbcd8e140937f696291f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MssqlJobStep",
    "MssqlJobStepConfig",
    "MssqlJobStepOutputTarget",
    "MssqlJobStepOutputTargetOutputReference",
    "MssqlJobStepTimeouts",
    "MssqlJobStepTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__50a3fc13c1cef3ac4540a9046b47de0ccca1502751deb463c8bbd1b1c6294f96(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    job_credential_id: builtins.str,
    job_id: builtins.str,
    job_step_index: jsii.Number,
    job_target_group_id: builtins.str,
    name: builtins.str,
    sql_script: builtins.str,
    id: typing.Optional[builtins.str] = None,
    initial_retry_interval_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_interval_seconds: typing.Optional[jsii.Number] = None,
    output_target: typing.Optional[typing.Union[MssqlJobStepOutputTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    retry_interval_backoff_multiplier: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[MssqlJobStepTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__f795c6a1e45db7bd91617344f6baedd874779387cee7ea3a28416f9839ad68ec(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bce17a1091d582b2de612020d9522b8831ebccd38339f75e520eadb0e7efa15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__270777cd36ab0f5bb67bf75c33a4eac622e4744bb4c85a0fdd1308bfbf681368(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eac272b802e1f5d481d67efa221695e0b7337ed7278765fbd5dc6a2da673c55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fd67d3099273677edcdcc6fa060aad12225f0e6042ca40674aed6c2fb584277(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5a80691b7d07f98c09adb819c64415679627abec353192eea43b3f97ad3769a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97544c90fed64964010d2ad7a5af30bbbaefd4cbf8f6370eba2516fb0a5d3016(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acde688bb8fc00d3de63fd1fe4221ce3c2c9f8a396f8bbebbc1e2c665fade199(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b689f5953ca10f3cce198423004c10cf0ebbda8181160b0c522056b412229b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07b6aa0cb40338990ac033cb45e6d37acdebdb99f8626a3a290a6870511ec4dc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e0d95fdb66d5a20214918ca1a5dc000190d5f2a3a9cbd135ee0a7d69645685e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f551e20964ce46c264926d7deae8bb4784f095f1295f13d5619deab0687fef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7108b7bd8c78ce06f034ff292de77c49e81013f70fa78a66768867cf52fee57(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bfb8533effb12e13d1d80eb2c989e4ad03bb7e2da8d0e04d26d4262f3b0c46b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    job_credential_id: builtins.str,
    job_id: builtins.str,
    job_step_index: jsii.Number,
    job_target_group_id: builtins.str,
    name: builtins.str,
    sql_script: builtins.str,
    id: typing.Optional[builtins.str] = None,
    initial_retry_interval_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_interval_seconds: typing.Optional[jsii.Number] = None,
    output_target: typing.Optional[typing.Union[MssqlJobStepOutputTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    retry_interval_backoff_multiplier: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[MssqlJobStepTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf7ec0dba18bb4132545c0e695048da68b9666ee4f200524c02ce6c08e0baa00(
    *,
    job_credential_id: builtins.str,
    mssql_database_id: builtins.str,
    table_name: builtins.str,
    schema_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adc96f8054de4f725e7e0ffafce5cb7d1ea0f779bf7677a744e80b48d17bcfc5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f862967fce18971df60dc8ae2995414c28f475a8bb76cce460d9a06cf16b0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__796b9009f37020a4c20c148ec821b3b0bc4f595956c84461361eaec2d684d27a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef0a527f1c2e07c3e6acbfdd431a2a6cc0ff1206f972ee3f77588c3aae55217(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1bbb99967d17a3d5e352a144ba4b895e1aa3c1b2386a969fa6f68310b9c62d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1701b9dbfda141366dfbe123222363bb76c12c1eef9602173149aa6e053025a5(
    value: typing.Optional[MssqlJobStepOutputTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73dc186c0422dc63026b01aa7dea49736a70769b644825ab5eb914c24141394c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aade16a984db216b95d33b2d20dfd4edc023102a94976bb81bc7f965d36f798a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5b78a004e57e5644c54bd561676175aa227e93b89452a441fcfce2c6d3a24c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d7de1118f24e2ccd2ed9774c14c65fba655433e8f69155ef4394481884eb65b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__916fbbfbb5132ff1fbb63f635ff2c7c511110757d3058138947b984514c668db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f538ed2b9384516c5346bfac8e20dde48be4e845413545536c52e06d1a1761(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1858effe181cc429d0edb918ce03900214cd3cdc62dfbcd8e140937f696291f4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlJobStepTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
