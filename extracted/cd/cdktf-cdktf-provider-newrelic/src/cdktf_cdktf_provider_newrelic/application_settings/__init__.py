r'''
# `newrelic_application_settings`

Refer to the Terraform Registry for docs: [`newrelic_application_settings`](https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings).
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


class ApplicationSettings(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.applicationSettings.ApplicationSettings",
):
    '''Represents a {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings newrelic_application_settings}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        app_apdex_threshold: typing.Optional[jsii.Number] = None,
        enable_real_user_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_slow_sql: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_thread_profiler: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        end_user_apdex_threshold: typing.Optional[jsii.Number] = None,
        error_collector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationSettingsErrorCollector", typing.Dict[builtins.str, typing.Any]]]]] = None,
        guid: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tracer_type: typing.Optional[builtins.str] = None,
        transaction_tracer: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationSettingsTransactionTracer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        use_server_side_config: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings newrelic_application_settings} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param app_apdex_threshold: The response time threshold value for Apdex score calculation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#app_apdex_threshold ApplicationSettings#app_apdex_threshold}
        :param enable_real_user_monitoring: Dummy field to support backward compatibility of previous version.should be removed with next major version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#enable_real_user_monitoring ApplicationSettings#enable_real_user_monitoring}
        :param enable_slow_sql: Samples and reports the slowest database queries in your traces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#enable_slow_sql ApplicationSettings#enable_slow_sql}
        :param enable_thread_profiler: Enable or disable the thread profiler. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#enable_thread_profiler ApplicationSettings#enable_thread_profiler}
        :param end_user_apdex_threshold: Dummy field to support backward compatibility of previous version.should be removed with next major version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#end_user_apdex_threshold ApplicationSettings#end_user_apdex_threshold}
        :param error_collector: error_collector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#error_collector ApplicationSettings#error_collector}
        :param guid: The GUID of the application in New Relic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#guid ApplicationSettings#guid}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#id ApplicationSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: The name of the application in New Relic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#name ApplicationSettings#name}
        :param tracer_type: The type of tracer to use, either 'CROSS_APPLICATION_TRACER', 'DISTRIBUTED_TRACING', 'NONE', or 'OPT_OUT'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#tracer_type ApplicationSettings#tracer_type}
        :param transaction_tracer: transaction_tracer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#transaction_tracer ApplicationSettings#transaction_tracer}
        :param use_server_side_config: Enable or disable server side monitoring. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#use_server_side_config ApplicationSettings#use_server_side_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7797f81b4beabb76c8b23553e1fadd5d46a512fc6a6e816d2ecaed7bc863410)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApplicationSettingsConfig(
            app_apdex_threshold=app_apdex_threshold,
            enable_real_user_monitoring=enable_real_user_monitoring,
            enable_slow_sql=enable_slow_sql,
            enable_thread_profiler=enable_thread_profiler,
            end_user_apdex_threshold=end_user_apdex_threshold,
            error_collector=error_collector,
            guid=guid,
            id=id,
            name=name,
            tracer_type=tracer_type,
            transaction_tracer=transaction_tracer,
            use_server_side_config=use_server_side_config,
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
        '''Generates CDKTF code for importing a ApplicationSettings resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApplicationSettings to import.
        :param import_from_id: The id of the existing ApplicationSettings that should be imported. Refer to the {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApplicationSettings to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bef9f570b1b6409393918092a771105dc118631972b7424f6e86608950e59f54)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putErrorCollector")
    def put_error_collector(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationSettingsErrorCollector", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b4f6374ed8bc52fdbbaaa579b4f24b047fa8ceef8bca3581444c82a39f815a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putErrorCollector", [value]))

    @jsii.member(jsii_name="putTransactionTracer")
    def put_transaction_tracer(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationSettingsTransactionTracer", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ce4f30d776ca3df5fc022525a767d1834925d94360a60c10129acb8a73ad812)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTransactionTracer", [value]))

    @jsii.member(jsii_name="resetAppApdexThreshold")
    def reset_app_apdex_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppApdexThreshold", []))

    @jsii.member(jsii_name="resetEnableRealUserMonitoring")
    def reset_enable_real_user_monitoring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableRealUserMonitoring", []))

    @jsii.member(jsii_name="resetEnableSlowSql")
    def reset_enable_slow_sql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSlowSql", []))

    @jsii.member(jsii_name="resetEnableThreadProfiler")
    def reset_enable_thread_profiler(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableThreadProfiler", []))

    @jsii.member(jsii_name="resetEndUserApdexThreshold")
    def reset_end_user_apdex_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndUserApdexThreshold", []))

    @jsii.member(jsii_name="resetErrorCollector")
    def reset_error_collector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorCollector", []))

    @jsii.member(jsii_name="resetGuid")
    def reset_guid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGuid", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetTracerType")
    def reset_tracer_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTracerType", []))

    @jsii.member(jsii_name="resetTransactionTracer")
    def reset_transaction_tracer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransactionTracer", []))

    @jsii.member(jsii_name="resetUseServerSideConfig")
    def reset_use_server_side_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseServerSideConfig", []))

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
    @jsii.member(jsii_name="errorCollector")
    def error_collector(self) -> "ApplicationSettingsErrorCollectorList":
        return typing.cast("ApplicationSettingsErrorCollectorList", jsii.get(self, "errorCollector"))

    @builtins.property
    @jsii.member(jsii_name="isImported")
    def is_imported(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isImported"))

    @builtins.property
    @jsii.member(jsii_name="transactionTracer")
    def transaction_tracer(self) -> "ApplicationSettingsTransactionTracerList":
        return typing.cast("ApplicationSettingsTransactionTracerList", jsii.get(self, "transactionTracer"))

    @builtins.property
    @jsii.member(jsii_name="appApdexThresholdInput")
    def app_apdex_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "appApdexThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="enableRealUserMonitoringInput")
    def enable_real_user_monitoring_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableRealUserMonitoringInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSlowSqlInput")
    def enable_slow_sql_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSlowSqlInput"))

    @builtins.property
    @jsii.member(jsii_name="enableThreadProfilerInput")
    def enable_thread_profiler_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableThreadProfilerInput"))

    @builtins.property
    @jsii.member(jsii_name="endUserApdexThresholdInput")
    def end_user_apdex_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "endUserApdexThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="errorCollectorInput")
    def error_collector_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationSettingsErrorCollector"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationSettingsErrorCollector"]]], jsii.get(self, "errorCollectorInput"))

    @builtins.property
    @jsii.member(jsii_name="guidInput")
    def guid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "guidInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="tracerTypeInput")
    def tracer_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tracerTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="transactionTracerInput")
    def transaction_tracer_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationSettingsTransactionTracer"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationSettingsTransactionTracer"]]], jsii.get(self, "transactionTracerInput"))

    @builtins.property
    @jsii.member(jsii_name="useServerSideConfigInput")
    def use_server_side_config_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useServerSideConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="appApdexThreshold")
    def app_apdex_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "appApdexThreshold"))

    @app_apdex_threshold.setter
    def app_apdex_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29a01cec5206478d58bf73a0298ad00682a10d5ff430ef82ff3b12c9c0125aab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appApdexThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableRealUserMonitoring")
    def enable_real_user_monitoring(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableRealUserMonitoring"))

    @enable_real_user_monitoring.setter
    def enable_real_user_monitoring(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e05a9968192e3c7eee16de2b7f41b200a7b7423d93bf1fff4accc2c14f2efd95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableRealUserMonitoring", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableSlowSql")
    def enable_slow_sql(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSlowSql"))

    @enable_slow_sql.setter
    def enable_slow_sql(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ee020b605290a66e2dc40bfd390d81891f1f7d8586c757a4142e2cc82fb9aac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSlowSql", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableThreadProfiler")
    def enable_thread_profiler(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableThreadProfiler"))

    @enable_thread_profiler.setter
    def enable_thread_profiler(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd76ab79bdb574726724e9b67077c6ebfa051534e895b7f68df21c5ae63d8305)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableThreadProfiler", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endUserApdexThreshold")
    def end_user_apdex_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "endUserApdexThreshold"))

    @end_user_apdex_threshold.setter
    def end_user_apdex_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__767bbdb0142bd90210e9e7dd00058ddacc8024b691342cb08787ae24de1e0674)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endUserApdexThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="guid")
    def guid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "guid"))

    @guid.setter
    def guid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0e374a7f26ba5dfaa783e8660de2b87df95d77204ff25651d85172cc344a1b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e61858e4c2e8c6b39d9c33380aec217e374127b0a4702d788463dc1681afc10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06abc014284bd38b6b968fa216499a355cff6900b6f471ca7c2f2822e81d96bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tracerType")
    def tracer_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tracerType"))

    @tracer_type.setter
    def tracer_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05a13956c703c067b5b2ed17f1e21cd40b01d7d2fb489af0e9b25449f6bdc165)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tracerType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useServerSideConfig")
    def use_server_side_config(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useServerSideConfig"))

    @use_server_side_config.setter
    def use_server_side_config(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34d0b607077c22ce0f2f09cd4349470d315aa7ac1b67d80de0588f0485f5301b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useServerSideConfig", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.applicationSettings.ApplicationSettingsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "app_apdex_threshold": "appApdexThreshold",
        "enable_real_user_monitoring": "enableRealUserMonitoring",
        "enable_slow_sql": "enableSlowSql",
        "enable_thread_profiler": "enableThreadProfiler",
        "end_user_apdex_threshold": "endUserApdexThreshold",
        "error_collector": "errorCollector",
        "guid": "guid",
        "id": "id",
        "name": "name",
        "tracer_type": "tracerType",
        "transaction_tracer": "transactionTracer",
        "use_server_side_config": "useServerSideConfig",
    },
)
class ApplicationSettingsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        app_apdex_threshold: typing.Optional[jsii.Number] = None,
        enable_real_user_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_slow_sql: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_thread_profiler: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        end_user_apdex_threshold: typing.Optional[jsii.Number] = None,
        error_collector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationSettingsErrorCollector", typing.Dict[builtins.str, typing.Any]]]]] = None,
        guid: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tracer_type: typing.Optional[builtins.str] = None,
        transaction_tracer: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationSettingsTransactionTracer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        use_server_side_config: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param app_apdex_threshold: The response time threshold value for Apdex score calculation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#app_apdex_threshold ApplicationSettings#app_apdex_threshold}
        :param enable_real_user_monitoring: Dummy field to support backward compatibility of previous version.should be removed with next major version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#enable_real_user_monitoring ApplicationSettings#enable_real_user_monitoring}
        :param enable_slow_sql: Samples and reports the slowest database queries in your traces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#enable_slow_sql ApplicationSettings#enable_slow_sql}
        :param enable_thread_profiler: Enable or disable the thread profiler. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#enable_thread_profiler ApplicationSettings#enable_thread_profiler}
        :param end_user_apdex_threshold: Dummy field to support backward compatibility of previous version.should be removed with next major version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#end_user_apdex_threshold ApplicationSettings#end_user_apdex_threshold}
        :param error_collector: error_collector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#error_collector ApplicationSettings#error_collector}
        :param guid: The GUID of the application in New Relic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#guid ApplicationSettings#guid}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#id ApplicationSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: The name of the application in New Relic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#name ApplicationSettings#name}
        :param tracer_type: The type of tracer to use, either 'CROSS_APPLICATION_TRACER', 'DISTRIBUTED_TRACING', 'NONE', or 'OPT_OUT'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#tracer_type ApplicationSettings#tracer_type}
        :param transaction_tracer: transaction_tracer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#transaction_tracer ApplicationSettings#transaction_tracer}
        :param use_server_side_config: Enable or disable server side monitoring. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#use_server_side_config ApplicationSettings#use_server_side_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__543787d805174e2ea9e2c92790b4477ce9bb231c59312336a134c28ae3006107)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument app_apdex_threshold", value=app_apdex_threshold, expected_type=type_hints["app_apdex_threshold"])
            check_type(argname="argument enable_real_user_monitoring", value=enable_real_user_monitoring, expected_type=type_hints["enable_real_user_monitoring"])
            check_type(argname="argument enable_slow_sql", value=enable_slow_sql, expected_type=type_hints["enable_slow_sql"])
            check_type(argname="argument enable_thread_profiler", value=enable_thread_profiler, expected_type=type_hints["enable_thread_profiler"])
            check_type(argname="argument end_user_apdex_threshold", value=end_user_apdex_threshold, expected_type=type_hints["end_user_apdex_threshold"])
            check_type(argname="argument error_collector", value=error_collector, expected_type=type_hints["error_collector"])
            check_type(argname="argument guid", value=guid, expected_type=type_hints["guid"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tracer_type", value=tracer_type, expected_type=type_hints["tracer_type"])
            check_type(argname="argument transaction_tracer", value=transaction_tracer, expected_type=type_hints["transaction_tracer"])
            check_type(argname="argument use_server_side_config", value=use_server_side_config, expected_type=type_hints["use_server_side_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if app_apdex_threshold is not None:
            self._values["app_apdex_threshold"] = app_apdex_threshold
        if enable_real_user_monitoring is not None:
            self._values["enable_real_user_monitoring"] = enable_real_user_monitoring
        if enable_slow_sql is not None:
            self._values["enable_slow_sql"] = enable_slow_sql
        if enable_thread_profiler is not None:
            self._values["enable_thread_profiler"] = enable_thread_profiler
        if end_user_apdex_threshold is not None:
            self._values["end_user_apdex_threshold"] = end_user_apdex_threshold
        if error_collector is not None:
            self._values["error_collector"] = error_collector
        if guid is not None:
            self._values["guid"] = guid
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name
        if tracer_type is not None:
            self._values["tracer_type"] = tracer_type
        if transaction_tracer is not None:
            self._values["transaction_tracer"] = transaction_tracer
        if use_server_side_config is not None:
            self._values["use_server_side_config"] = use_server_side_config

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
    def app_apdex_threshold(self) -> typing.Optional[jsii.Number]:
        '''The response time threshold value for Apdex score calculation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#app_apdex_threshold ApplicationSettings#app_apdex_threshold}
        '''
        result = self._values.get("app_apdex_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_real_user_monitoring(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Dummy field to support backward compatibility of previous version.should be removed with next major version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#enable_real_user_monitoring ApplicationSettings#enable_real_user_monitoring}
        '''
        result = self._values.get("enable_real_user_monitoring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_slow_sql(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Samples and reports the slowest database queries in your traces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#enable_slow_sql ApplicationSettings#enable_slow_sql}
        '''
        result = self._values.get("enable_slow_sql")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_thread_profiler(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable or disable the thread profiler.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#enable_thread_profiler ApplicationSettings#enable_thread_profiler}
        '''
        result = self._values.get("enable_thread_profiler")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def end_user_apdex_threshold(self) -> typing.Optional[jsii.Number]:
        '''Dummy field to support backward compatibility of previous version.should be removed with next major version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#end_user_apdex_threshold ApplicationSettings#end_user_apdex_threshold}
        '''
        result = self._values.get("end_user_apdex_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def error_collector(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationSettingsErrorCollector"]]]:
        '''error_collector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#error_collector ApplicationSettings#error_collector}
        '''
        result = self._values.get("error_collector")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationSettingsErrorCollector"]]], result)

    @builtins.property
    def guid(self) -> typing.Optional[builtins.str]:
        '''The GUID of the application in New Relic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#guid ApplicationSettings#guid}
        '''
        result = self._values.get("guid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#id ApplicationSettings#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the application in New Relic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#name ApplicationSettings#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tracer_type(self) -> typing.Optional[builtins.str]:
        '''The type of tracer to use, either 'CROSS_APPLICATION_TRACER', 'DISTRIBUTED_TRACING', 'NONE', or 'OPT_OUT'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#tracer_type ApplicationSettings#tracer_type}
        '''
        result = self._values.get("tracer_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transaction_tracer(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationSettingsTransactionTracer"]]]:
        '''transaction_tracer block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#transaction_tracer ApplicationSettings#transaction_tracer}
        '''
        result = self._values.get("transaction_tracer")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationSettingsTransactionTracer"]]], result)

    @builtins.property
    def use_server_side_config(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable or disable server side monitoring.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#use_server_side_config ApplicationSettings#use_server_side_config}
        '''
        result = self._values.get("use_server_side_config")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationSettingsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.applicationSettings.ApplicationSettingsErrorCollector",
    jsii_struct_bases=[],
    name_mapping={
        "expected_error_classes": "expectedErrorClasses",
        "expected_error_codes": "expectedErrorCodes",
        "ignored_error_classes": "ignoredErrorClasses",
        "ignored_error_codes": "ignoredErrorCodes",
    },
)
class ApplicationSettingsErrorCollector:
    def __init__(
        self,
        *,
        expected_error_classes: typing.Optional[typing.Sequence[builtins.str]] = None,
        expected_error_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        ignored_error_classes: typing.Optional[typing.Sequence[builtins.str]] = None,
        ignored_error_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param expected_error_classes: A list of error classes that are expected and should not trigger alerts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#expected_error_classes ApplicationSettings#expected_error_classes}
        :param expected_error_codes: A list of error codes that are expected and should not trigger alerts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#expected_error_codes ApplicationSettings#expected_error_codes}
        :param ignored_error_classes: A list of error classes that should be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#ignored_error_classes ApplicationSettings#ignored_error_classes}
        :param ignored_error_codes: A list of error codes that should be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#ignored_error_codes ApplicationSettings#ignored_error_codes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8395be5d29384305bc752e8e7fb78386e57b9d0631f69a5867394fe9f0577f91)
            check_type(argname="argument expected_error_classes", value=expected_error_classes, expected_type=type_hints["expected_error_classes"])
            check_type(argname="argument expected_error_codes", value=expected_error_codes, expected_type=type_hints["expected_error_codes"])
            check_type(argname="argument ignored_error_classes", value=ignored_error_classes, expected_type=type_hints["ignored_error_classes"])
            check_type(argname="argument ignored_error_codes", value=ignored_error_codes, expected_type=type_hints["ignored_error_codes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if expected_error_classes is not None:
            self._values["expected_error_classes"] = expected_error_classes
        if expected_error_codes is not None:
            self._values["expected_error_codes"] = expected_error_codes
        if ignored_error_classes is not None:
            self._values["ignored_error_classes"] = ignored_error_classes
        if ignored_error_codes is not None:
            self._values["ignored_error_codes"] = ignored_error_codes

    @builtins.property
    def expected_error_classes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of error classes that are expected and should not trigger alerts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#expected_error_classes ApplicationSettings#expected_error_classes}
        '''
        result = self._values.get("expected_error_classes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def expected_error_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of error codes that are expected and should not trigger alerts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#expected_error_codes ApplicationSettings#expected_error_codes}
        '''
        result = self._values.get("expected_error_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ignored_error_classes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of error classes that should be ignored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#ignored_error_classes ApplicationSettings#ignored_error_classes}
        '''
        result = self._values.get("ignored_error_classes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ignored_error_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of error codes that should be ignored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#ignored_error_codes ApplicationSettings#ignored_error_codes}
        '''
        result = self._values.get("ignored_error_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationSettingsErrorCollector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationSettingsErrorCollectorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.applicationSettings.ApplicationSettingsErrorCollectorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f22ecb6b94f30a3849f086719203dde11c5d9e668602a4869b2c7da5e048e8d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationSettingsErrorCollectorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__700efea3903088a1b67f79007120341ec436b8fd8a3b42b742e59a7f2a40c1ca)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationSettingsErrorCollectorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b54e9e6145e25e3091aabe91569ddbcc4cea31e8a20a607e80b288e76f61d787)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa0bb2414fd5404521c3f66572f67a1aeedc781d1060c65345f75e4f9f34de96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9bb8bede4fd3f34e1fe9e5b1d822b27f179359698d338ce20392824c27b592e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationSettingsErrorCollector]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationSettingsErrorCollector]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationSettingsErrorCollector]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ee44b81f37cfc5596babf4e12c9a1d7e8a71ad3bf3d01c74d15f9733a36c62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationSettingsErrorCollectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.applicationSettings.ApplicationSettingsErrorCollectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0abe3fd146ddc9c634a3cbc1372ad45e8cf5eb6c3c1ac923b915f4d34aed116)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExpectedErrorClasses")
    def reset_expected_error_classes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpectedErrorClasses", []))

    @jsii.member(jsii_name="resetExpectedErrorCodes")
    def reset_expected_error_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpectedErrorCodes", []))

    @jsii.member(jsii_name="resetIgnoredErrorClasses")
    def reset_ignored_error_classes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoredErrorClasses", []))

    @jsii.member(jsii_name="resetIgnoredErrorCodes")
    def reset_ignored_error_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoredErrorCodes", []))

    @builtins.property
    @jsii.member(jsii_name="expectedErrorClassesInput")
    def expected_error_classes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "expectedErrorClassesInput"))

    @builtins.property
    @jsii.member(jsii_name="expectedErrorCodesInput")
    def expected_error_codes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "expectedErrorCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoredErrorClassesInput")
    def ignored_error_classes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ignoredErrorClassesInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoredErrorCodesInput")
    def ignored_error_codes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ignoredErrorCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="expectedErrorClasses")
    def expected_error_classes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "expectedErrorClasses"))

    @expected_error_classes.setter
    def expected_error_classes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd0f32bf09d89a47d490ce1f2d157542f318256de375d69619e3f7189480a92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expectedErrorClasses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expectedErrorCodes")
    def expected_error_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "expectedErrorCodes"))

    @expected_error_codes.setter
    def expected_error_codes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ca11499f2f886de70d9073220bab50a7b98f54b6ea9e17df5f3db1c99cb3176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expectedErrorCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoredErrorClasses")
    def ignored_error_classes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ignoredErrorClasses"))

    @ignored_error_classes.setter
    def ignored_error_classes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6e4807cefa2abbc1e5ce51094326d6be32be01cd386245bab7ba78c22d1e37a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoredErrorClasses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoredErrorCodes")
    def ignored_error_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ignoredErrorCodes"))

    @ignored_error_codes.setter
    def ignored_error_codes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5066530fa2cd87df7bef3ed1bfcd531e140127f4a4516747f1600a69c0d8bfd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoredErrorCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationSettingsErrorCollector]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationSettingsErrorCollector]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationSettingsErrorCollector]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc8114dc81598295c105bccd1ee73d778c4f26bfabd4f11ff16700ee78618c4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.applicationSettings.ApplicationSettingsTransactionTracer",
    jsii_struct_bases=[],
    name_mapping={
        "explain_query_plans": "explainQueryPlans",
        "sql": "sql",
        "stack_trace_threshold_value": "stackTraceThresholdValue",
        "transaction_threshold_type": "transactionThresholdType",
        "transaction_threshold_value": "transactionThresholdValue",
    },
)
class ApplicationSettingsTransactionTracer:
    def __init__(
        self,
        *,
        explain_query_plans: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationSettingsTransactionTracerExplainQueryPlans", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sql: typing.Optional[typing.Union["ApplicationSettingsTransactionTracerSql", typing.Dict[builtins.str, typing.Any]]] = None,
        stack_trace_threshold_value: typing.Optional[jsii.Number] = None,
        transaction_threshold_type: typing.Optional[builtins.str] = None,
        transaction_threshold_value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param explain_query_plans: explain_query_plans block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#explain_query_plans ApplicationSettings#explain_query_plans}
        :param sql: sql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#sql ApplicationSettings#sql}
        :param stack_trace_threshold_value: The response time threshold value for capturing stack traces of SQL queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#stack_trace_threshold_value ApplicationSettings#stack_trace_threshold_value}
        :param transaction_threshold_type: The type of threshold for transaction tracing, either 'APDEX_F' or 'VALUE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#transaction_threshold_type ApplicationSettings#transaction_threshold_type}
        :param transaction_threshold_value: The threshold value for transaction tracing when 'transaction_threshold_type' is 'VALUE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#transaction_threshold_value ApplicationSettings#transaction_threshold_value}
        '''
        if isinstance(sql, dict):
            sql = ApplicationSettingsTransactionTracerSql(**sql)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36788c0ec50b5455b0522afac224382dde2d0a0e5a4e74c1631120c028c67f8f)
            check_type(argname="argument explain_query_plans", value=explain_query_plans, expected_type=type_hints["explain_query_plans"])
            check_type(argname="argument sql", value=sql, expected_type=type_hints["sql"])
            check_type(argname="argument stack_trace_threshold_value", value=stack_trace_threshold_value, expected_type=type_hints["stack_trace_threshold_value"])
            check_type(argname="argument transaction_threshold_type", value=transaction_threshold_type, expected_type=type_hints["transaction_threshold_type"])
            check_type(argname="argument transaction_threshold_value", value=transaction_threshold_value, expected_type=type_hints["transaction_threshold_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if explain_query_plans is not None:
            self._values["explain_query_plans"] = explain_query_plans
        if sql is not None:
            self._values["sql"] = sql
        if stack_trace_threshold_value is not None:
            self._values["stack_trace_threshold_value"] = stack_trace_threshold_value
        if transaction_threshold_type is not None:
            self._values["transaction_threshold_type"] = transaction_threshold_type
        if transaction_threshold_value is not None:
            self._values["transaction_threshold_value"] = transaction_threshold_value

    @builtins.property
    def explain_query_plans(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationSettingsTransactionTracerExplainQueryPlans"]]]:
        '''explain_query_plans block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#explain_query_plans ApplicationSettings#explain_query_plans}
        '''
        result = self._values.get("explain_query_plans")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationSettingsTransactionTracerExplainQueryPlans"]]], result)

    @builtins.property
    def sql(self) -> typing.Optional["ApplicationSettingsTransactionTracerSql"]:
        '''sql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#sql ApplicationSettings#sql}
        '''
        result = self._values.get("sql")
        return typing.cast(typing.Optional["ApplicationSettingsTransactionTracerSql"], result)

    @builtins.property
    def stack_trace_threshold_value(self) -> typing.Optional[jsii.Number]:
        '''The response time threshold value for capturing stack traces of SQL queries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#stack_trace_threshold_value ApplicationSettings#stack_trace_threshold_value}
        '''
        result = self._values.get("stack_trace_threshold_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def transaction_threshold_type(self) -> typing.Optional[builtins.str]:
        '''The type of threshold for transaction tracing, either 'APDEX_F' or 'VALUE'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#transaction_threshold_type ApplicationSettings#transaction_threshold_type}
        '''
        result = self._values.get("transaction_threshold_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transaction_threshold_value(self) -> typing.Optional[jsii.Number]:
        '''The threshold value for transaction tracing when 'transaction_threshold_type' is 'VALUE'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#transaction_threshold_value ApplicationSettings#transaction_threshold_value}
        '''
        result = self._values.get("transaction_threshold_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationSettingsTransactionTracer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.applicationSettings.ApplicationSettingsTransactionTracerExplainQueryPlans",
    jsii_struct_bases=[],
    name_mapping={
        "query_plan_threshold_type": "queryPlanThresholdType",
        "query_plan_threshold_value": "queryPlanThresholdValue",
    },
)
class ApplicationSettingsTransactionTracerExplainQueryPlans:
    def __init__(
        self,
        *,
        query_plan_threshold_type: typing.Optional[builtins.str] = None,
        query_plan_threshold_value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param query_plan_threshold_type: The type of threshold for explain plans, either 'APDEX_F' or 'VALUE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#query_plan_threshold_type ApplicationSettings#query_plan_threshold_type}
        :param query_plan_threshold_value: The threshold value for explain plans when 'query_plan_threshold_type' is 'VALUE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#query_plan_threshold_value ApplicationSettings#query_plan_threshold_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4738c562695c9f9faa2efc558d05c513a654aaa6477310eaae5564d53a7e261)
            check_type(argname="argument query_plan_threshold_type", value=query_plan_threshold_type, expected_type=type_hints["query_plan_threshold_type"])
            check_type(argname="argument query_plan_threshold_value", value=query_plan_threshold_value, expected_type=type_hints["query_plan_threshold_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if query_plan_threshold_type is not None:
            self._values["query_plan_threshold_type"] = query_plan_threshold_type
        if query_plan_threshold_value is not None:
            self._values["query_plan_threshold_value"] = query_plan_threshold_value

    @builtins.property
    def query_plan_threshold_type(self) -> typing.Optional[builtins.str]:
        '''The type of threshold for explain plans, either 'APDEX_F' or 'VALUE'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#query_plan_threshold_type ApplicationSettings#query_plan_threshold_type}
        '''
        result = self._values.get("query_plan_threshold_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_plan_threshold_value(self) -> typing.Optional[jsii.Number]:
        '''The threshold value for explain plans when 'query_plan_threshold_type' is 'VALUE'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#query_plan_threshold_value ApplicationSettings#query_plan_threshold_value}
        '''
        result = self._values.get("query_plan_threshold_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationSettingsTransactionTracerExplainQueryPlans(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationSettingsTransactionTracerExplainQueryPlansList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.applicationSettings.ApplicationSettingsTransactionTracerExplainQueryPlansList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54c6f0c84dcc329691cd63bdc81ce21ed99e5a98852e2d592610506e79402a9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationSettingsTransactionTracerExplainQueryPlansOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f7f40794cc9b09e57092c371719c9f241cb3fbfb3238ad920c558468ee60e3f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationSettingsTransactionTracerExplainQueryPlansOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e8a5ded8df3d5d05dcaa88576bbf50b8fcead8a4c989ea15f1b7882c8073c23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e23fe318bd38a55238cda2abdbe623c23ae0fe87e5f581055fdd772351ea741)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6193dc4cab593c9fc74d9cbbc76bf0c19dcec09bbd83733145ed72c9e6d4d53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationSettingsTransactionTracerExplainQueryPlans]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationSettingsTransactionTracerExplainQueryPlans]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationSettingsTransactionTracerExplainQueryPlans]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__583d45dbd6c22d70b36a41f75b93bbb92c35a82f5ef80eb0e0ccc4257ee17e1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationSettingsTransactionTracerExplainQueryPlansOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.applicationSettings.ApplicationSettingsTransactionTracerExplainQueryPlansOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2daccd7d713d4938f4a22f57f7a70e00c9af18d0b8246ad9b611db2e04e388b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetQueryPlanThresholdType")
    def reset_query_plan_threshold_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryPlanThresholdType", []))

    @jsii.member(jsii_name="resetQueryPlanThresholdValue")
    def reset_query_plan_threshold_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryPlanThresholdValue", []))

    @builtins.property
    @jsii.member(jsii_name="queryPlanThresholdTypeInput")
    def query_plan_threshold_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryPlanThresholdTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="queryPlanThresholdValueInput")
    def query_plan_threshold_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "queryPlanThresholdValueInput"))

    @builtins.property
    @jsii.member(jsii_name="queryPlanThresholdType")
    def query_plan_threshold_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryPlanThresholdType"))

    @query_plan_threshold_type.setter
    def query_plan_threshold_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__354da3ea24e56d83e5efbd146a45a9dc19d65f7a2040cbf49138f90cd3658402)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryPlanThresholdType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryPlanThresholdValue")
    def query_plan_threshold_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queryPlanThresholdValue"))

    @query_plan_threshold_value.setter
    def query_plan_threshold_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd784645baad4a3280991c97ec77dc710989c1274aa209044bf840040d31c598)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryPlanThresholdValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationSettingsTransactionTracerExplainQueryPlans]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationSettingsTransactionTracerExplainQueryPlans]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationSettingsTransactionTracerExplainQueryPlans]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce43af2e7a0ff262bd1d5935e5d40506149c0950650ce7771f53911bec324ca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationSettingsTransactionTracerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.applicationSettings.ApplicationSettingsTransactionTracerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2dbcbf9ceeebd7ac0715838658d913bc2bcef18564937a09beccb4632ce499a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationSettingsTransactionTracerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a4ace2961e9ece7921db4b90228e451e258a3b858764959e2e8daa70e26398d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationSettingsTransactionTracerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a006eed497d5057d5d4a6cd1d26ebc1deb1cc51a6674c2ac8a6c93dbefcbd29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffd8d5278ceb7eda309ca75202bbf6e795987dce1f51df67a981ec2e64ef6877)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34b4a00e102594a371fb10f81ee24d6c4af6c3a68a47ec7fed0470776029ca3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationSettingsTransactionTracer]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationSettingsTransactionTracer]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationSettingsTransactionTracer]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__816001d6ee34b589c54457ad0b143d1084ca81e8d8b18af3a2e7058ceb1cf5ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationSettingsTransactionTracerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.applicationSettings.ApplicationSettingsTransactionTracerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f91426e20fcb401fbd9f976546e060dde311d080da2f569546ae43d2d880141b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putExplainQueryPlans")
    def put_explain_query_plans(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationSettingsTransactionTracerExplainQueryPlans, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f37cc6f90d5d0fff5a521b332c9d3361a1cc4d4f7dd3dfe5cec87305cf33053)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExplainQueryPlans", [value]))

    @jsii.member(jsii_name="putSql")
    def put_sql(self, *, record_sql: builtins.str) -> None:
        '''
        :param record_sql: The level of SQL recording, either 'OBFUSCATED', 'OFF', or 'RAW'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#record_sql ApplicationSettings#record_sql}
        '''
        value = ApplicationSettingsTransactionTracerSql(record_sql=record_sql)

        return typing.cast(None, jsii.invoke(self, "putSql", [value]))

    @jsii.member(jsii_name="resetExplainQueryPlans")
    def reset_explain_query_plans(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExplainQueryPlans", []))

    @jsii.member(jsii_name="resetSql")
    def reset_sql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSql", []))

    @jsii.member(jsii_name="resetStackTraceThresholdValue")
    def reset_stack_trace_threshold_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStackTraceThresholdValue", []))

    @jsii.member(jsii_name="resetTransactionThresholdType")
    def reset_transaction_threshold_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransactionThresholdType", []))

    @jsii.member(jsii_name="resetTransactionThresholdValue")
    def reset_transaction_threshold_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransactionThresholdValue", []))

    @builtins.property
    @jsii.member(jsii_name="explainQueryPlans")
    def explain_query_plans(
        self,
    ) -> ApplicationSettingsTransactionTracerExplainQueryPlansList:
        return typing.cast(ApplicationSettingsTransactionTracerExplainQueryPlansList, jsii.get(self, "explainQueryPlans"))

    @builtins.property
    @jsii.member(jsii_name="sql")
    def sql(self) -> "ApplicationSettingsTransactionTracerSqlOutputReference":
        return typing.cast("ApplicationSettingsTransactionTracerSqlOutputReference", jsii.get(self, "sql"))

    @builtins.property
    @jsii.member(jsii_name="explainQueryPlansInput")
    def explain_query_plans_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationSettingsTransactionTracerExplainQueryPlans]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationSettingsTransactionTracerExplainQueryPlans]]], jsii.get(self, "explainQueryPlansInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlInput")
    def sql_input(self) -> typing.Optional["ApplicationSettingsTransactionTracerSql"]:
        return typing.cast(typing.Optional["ApplicationSettingsTransactionTracerSql"], jsii.get(self, "sqlInput"))

    @builtins.property
    @jsii.member(jsii_name="stackTraceThresholdValueInput")
    def stack_trace_threshold_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "stackTraceThresholdValueInput"))

    @builtins.property
    @jsii.member(jsii_name="transactionThresholdTypeInput")
    def transaction_threshold_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transactionThresholdTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="transactionThresholdValueInput")
    def transaction_threshold_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "transactionThresholdValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stackTraceThresholdValue")
    def stack_trace_threshold_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "stackTraceThresholdValue"))

    @stack_trace_threshold_value.setter
    def stack_trace_threshold_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c7a0e1a5f9272a191e394fc758b75fb1fe2052519580a16843af3da771e2d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stackTraceThresholdValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transactionThresholdType")
    def transaction_threshold_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transactionThresholdType"))

    @transaction_threshold_type.setter
    def transaction_threshold_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8b1bcea20f91cb14543390a1ac4a61eeba9170f2f1871f94eddd23cf3b5d92d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transactionThresholdType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transactionThresholdValue")
    def transaction_threshold_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "transactionThresholdValue"))

    @transaction_threshold_value.setter
    def transaction_threshold_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f59ab1be2884a0261ffe5213c6a18e95befb29b74cd49c054368dba8c94e55db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transactionThresholdValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationSettingsTransactionTracer]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationSettingsTransactionTracer]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationSettingsTransactionTracer]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0330bea8f3ae07add052d33984f1c965d66a7443fb2638de10cd36f362a76a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.applicationSettings.ApplicationSettingsTransactionTracerSql",
    jsii_struct_bases=[],
    name_mapping={"record_sql": "recordSql"},
)
class ApplicationSettingsTransactionTracerSql:
    def __init__(self, *, record_sql: builtins.str) -> None:
        '''
        :param record_sql: The level of SQL recording, either 'OBFUSCATED', 'OFF', or 'RAW'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#record_sql ApplicationSettings#record_sql}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37cf8d21b0afa765ca7b6626e3f3a1370237d06ea73d6051209fa88b1aa350a9)
            check_type(argname="argument record_sql", value=record_sql, expected_type=type_hints["record_sql"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "record_sql": record_sql,
        }

    @builtins.property
    def record_sql(self) -> builtins.str:
        '''The level of SQL recording, either 'OBFUSCATED', 'OFF', or 'RAW'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/application_settings#record_sql ApplicationSettings#record_sql}
        '''
        result = self._values.get("record_sql")
        assert result is not None, "Required property 'record_sql' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationSettingsTransactionTracerSql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationSettingsTransactionTracerSqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.applicationSettings.ApplicationSettingsTransactionTracerSqlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe946c800565b8dcf9ad9dfe9efc408532874cc26f45556897ecd00ca2626501)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="recordSqlInput")
    def record_sql_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordSqlInput"))

    @builtins.property
    @jsii.member(jsii_name="recordSql")
    def record_sql(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordSql"))

    @record_sql.setter
    def record_sql(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fe6077960338b9d10e7e07e7887c9184e1b01b998d198012ab21df6562ea34f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordSql", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApplicationSettingsTransactionTracerSql]:
        return typing.cast(typing.Optional[ApplicationSettingsTransactionTracerSql], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApplicationSettingsTransactionTracerSql],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f1fc0ea3770bcd218c9b3e120df99552d9bc070c85670cc9faca8e5026ae3e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApplicationSettings",
    "ApplicationSettingsConfig",
    "ApplicationSettingsErrorCollector",
    "ApplicationSettingsErrorCollectorList",
    "ApplicationSettingsErrorCollectorOutputReference",
    "ApplicationSettingsTransactionTracer",
    "ApplicationSettingsTransactionTracerExplainQueryPlans",
    "ApplicationSettingsTransactionTracerExplainQueryPlansList",
    "ApplicationSettingsTransactionTracerExplainQueryPlansOutputReference",
    "ApplicationSettingsTransactionTracerList",
    "ApplicationSettingsTransactionTracerOutputReference",
    "ApplicationSettingsTransactionTracerSql",
    "ApplicationSettingsTransactionTracerSqlOutputReference",
]

publication.publish()

def _typecheckingstub__d7797f81b4beabb76c8b23553e1fadd5d46a512fc6a6e816d2ecaed7bc863410(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    app_apdex_threshold: typing.Optional[jsii.Number] = None,
    enable_real_user_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_slow_sql: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_thread_profiler: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    end_user_apdex_threshold: typing.Optional[jsii.Number] = None,
    error_collector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationSettingsErrorCollector, typing.Dict[builtins.str, typing.Any]]]]] = None,
    guid: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tracer_type: typing.Optional[builtins.str] = None,
    transaction_tracer: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationSettingsTransactionTracer, typing.Dict[builtins.str, typing.Any]]]]] = None,
    use_server_side_config: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__bef9f570b1b6409393918092a771105dc118631972b7424f6e86608950e59f54(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b4f6374ed8bc52fdbbaaa579b4f24b047fa8ceef8bca3581444c82a39f815a2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationSettingsErrorCollector, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce4f30d776ca3df5fc022525a767d1834925d94360a60c10129acb8a73ad812(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationSettingsTransactionTracer, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29a01cec5206478d58bf73a0298ad00682a10d5ff430ef82ff3b12c9c0125aab(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e05a9968192e3c7eee16de2b7f41b200a7b7423d93bf1fff4accc2c14f2efd95(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ee020b605290a66e2dc40bfd390d81891f1f7d8586c757a4142e2cc82fb9aac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd76ab79bdb574726724e9b67077c6ebfa051534e895b7f68df21c5ae63d8305(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__767bbdb0142bd90210e9e7dd00058ddacc8024b691342cb08787ae24de1e0674(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0e374a7f26ba5dfaa783e8660de2b87df95d77204ff25651d85172cc344a1b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e61858e4c2e8c6b39d9c33380aec217e374127b0a4702d788463dc1681afc10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06abc014284bd38b6b968fa216499a355cff6900b6f471ca7c2f2822e81d96bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05a13956c703c067b5b2ed17f1e21cd40b01d7d2fb489af0e9b25449f6bdc165(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34d0b607077c22ce0f2f09cd4349470d315aa7ac1b67d80de0588f0485f5301b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__543787d805174e2ea9e2c92790b4477ce9bb231c59312336a134c28ae3006107(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    app_apdex_threshold: typing.Optional[jsii.Number] = None,
    enable_real_user_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_slow_sql: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_thread_profiler: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    end_user_apdex_threshold: typing.Optional[jsii.Number] = None,
    error_collector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationSettingsErrorCollector, typing.Dict[builtins.str, typing.Any]]]]] = None,
    guid: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tracer_type: typing.Optional[builtins.str] = None,
    transaction_tracer: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationSettingsTransactionTracer, typing.Dict[builtins.str, typing.Any]]]]] = None,
    use_server_side_config: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8395be5d29384305bc752e8e7fb78386e57b9d0631f69a5867394fe9f0577f91(
    *,
    expected_error_classes: typing.Optional[typing.Sequence[builtins.str]] = None,
    expected_error_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ignored_error_classes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ignored_error_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f22ecb6b94f30a3849f086719203dde11c5d9e668602a4869b2c7da5e048e8d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__700efea3903088a1b67f79007120341ec436b8fd8a3b42b742e59a7f2a40c1ca(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b54e9e6145e25e3091aabe91569ddbcc4cea31e8a20a607e80b288e76f61d787(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa0bb2414fd5404521c3f66572f67a1aeedc781d1060c65345f75e4f9f34de96(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9bb8bede4fd3f34e1fe9e5b1d822b27f179359698d338ce20392824c27b592e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ee44b81f37cfc5596babf4e12c9a1d7e8a71ad3bf3d01c74d15f9733a36c62(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationSettingsErrorCollector]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0abe3fd146ddc9c634a3cbc1372ad45e8cf5eb6c3c1ac923b915f4d34aed116(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd0f32bf09d89a47d490ce1f2d157542f318256de375d69619e3f7189480a92(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ca11499f2f886de70d9073220bab50a7b98f54b6ea9e17df5f3db1c99cb3176(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6e4807cefa2abbc1e5ce51094326d6be32be01cd386245bab7ba78c22d1e37a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5066530fa2cd87df7bef3ed1bfcd531e140127f4a4516747f1600a69c0d8bfd4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc8114dc81598295c105bccd1ee73d778c4f26bfabd4f11ff16700ee78618c4f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationSettingsErrorCollector]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36788c0ec50b5455b0522afac224382dde2d0a0e5a4e74c1631120c028c67f8f(
    *,
    explain_query_plans: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationSettingsTransactionTracerExplainQueryPlans, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sql: typing.Optional[typing.Union[ApplicationSettingsTransactionTracerSql, typing.Dict[builtins.str, typing.Any]]] = None,
    stack_trace_threshold_value: typing.Optional[jsii.Number] = None,
    transaction_threshold_type: typing.Optional[builtins.str] = None,
    transaction_threshold_value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4738c562695c9f9faa2efc558d05c513a654aaa6477310eaae5564d53a7e261(
    *,
    query_plan_threshold_type: typing.Optional[builtins.str] = None,
    query_plan_threshold_value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c6f0c84dcc329691cd63bdc81ce21ed99e5a98852e2d592610506e79402a9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f7f40794cc9b09e57092c371719c9f241cb3fbfb3238ad920c558468ee60e3f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8a5ded8df3d5d05dcaa88576bbf50b8fcead8a4c989ea15f1b7882c8073c23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e23fe318bd38a55238cda2abdbe623c23ae0fe87e5f581055fdd772351ea741(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6193dc4cab593c9fc74d9cbbc76bf0c19dcec09bbd83733145ed72c9e6d4d53(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__583d45dbd6c22d70b36a41f75b93bbb92c35a82f5ef80eb0e0ccc4257ee17e1c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationSettingsTransactionTracerExplainQueryPlans]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2daccd7d713d4938f4a22f57f7a70e00c9af18d0b8246ad9b611db2e04e388b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354da3ea24e56d83e5efbd146a45a9dc19d65f7a2040cbf49138f90cd3658402(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd784645baad4a3280991c97ec77dc710989c1274aa209044bf840040d31c598(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce43af2e7a0ff262bd1d5935e5d40506149c0950650ce7771f53911bec324ca4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationSettingsTransactionTracerExplainQueryPlans]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2dbcbf9ceeebd7ac0715838658d913bc2bcef18564937a09beccb4632ce499a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a4ace2961e9ece7921db4b90228e451e258a3b858764959e2e8daa70e26398d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a006eed497d5057d5d4a6cd1d26ebc1deb1cc51a6674c2ac8a6c93dbefcbd29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd8d5278ceb7eda309ca75202bbf6e795987dce1f51df67a981ec2e64ef6877(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b4a00e102594a371fb10f81ee24d6c4af6c3a68a47ec7fed0470776029ca3e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__816001d6ee34b589c54457ad0b143d1084ca81e8d8b18af3a2e7058ceb1cf5ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationSettingsTransactionTracer]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f91426e20fcb401fbd9f976546e060dde311d080da2f569546ae43d2d880141b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f37cc6f90d5d0fff5a521b332c9d3361a1cc4d4f7dd3dfe5cec87305cf33053(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationSettingsTransactionTracerExplainQueryPlans, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c7a0e1a5f9272a191e394fc758b75fb1fe2052519580a16843af3da771e2d7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8b1bcea20f91cb14543390a1ac4a61eeba9170f2f1871f94eddd23cf3b5d92d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f59ab1be2884a0261ffe5213c6a18e95befb29b74cd49c054368dba8c94e55db(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0330bea8f3ae07add052d33984f1c965d66a7443fb2638de10cd36f362a76a2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationSettingsTransactionTracer]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37cf8d21b0afa765ca7b6626e3f3a1370237d06ea73d6051209fa88b1aa350a9(
    *,
    record_sql: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe946c800565b8dcf9ad9dfe9efc408532874cc26f45556897ecd00ca2626501(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe6077960338b9d10e7e07e7887c9184e1b01b998d198012ab21df6562ea34f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f1fc0ea3770bcd218c9b3e120df99552d9bc070c85670cc9faca8e5026ae3e4(
    value: typing.Optional[ApplicationSettingsTransactionTracerSql],
) -> None:
    """Type checking stubs"""
    pass
