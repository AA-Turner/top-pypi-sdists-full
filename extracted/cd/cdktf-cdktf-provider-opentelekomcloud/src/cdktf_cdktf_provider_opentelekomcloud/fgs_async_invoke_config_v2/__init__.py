r'''
# `opentelekomcloud_fgs_async_invoke_config_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_fgs_async_invoke_config_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2).
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


class FgsAsyncInvokeConfigV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.fgsAsyncInvokeConfigV2.FgsAsyncInvokeConfigV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2 opentelekomcloud_fgs_async_invoke_config_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        function_urn: builtins.str,
        max_async_event_age_in_seconds: jsii.Number,
        max_async_retry_attempts: jsii.Number,
        id: typing.Optional[builtins.str] = None,
        on_failure: typing.Optional[typing.Union["FgsAsyncInvokeConfigV2OnFailure", typing.Dict[builtins.str, typing.Any]]] = None,
        on_success: typing.Optional[typing.Union["FgsAsyncInvokeConfigV2OnSuccess", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2 opentelekomcloud_fgs_async_invoke_config_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param function_urn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#function_urn FgsAsyncInvokeConfigV2#function_urn}.
        :param max_async_event_age_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#max_async_event_age_in_seconds FgsAsyncInvokeConfigV2#max_async_event_age_in_seconds}.
        :param max_async_retry_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#max_async_retry_attempts FgsAsyncInvokeConfigV2#max_async_retry_attempts}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#id FgsAsyncInvokeConfigV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param on_failure: on_failure block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#on_failure FgsAsyncInvokeConfigV2#on_failure}
        :param on_success: on_success block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#on_success FgsAsyncInvokeConfigV2#on_success}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__614c84f1454506ecf390aea21dab34c4fd0d62a0566de23c9dc1ed31435ec154)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FgsAsyncInvokeConfigV2Config(
            function_urn=function_urn,
            max_async_event_age_in_seconds=max_async_event_age_in_seconds,
            max_async_retry_attempts=max_async_retry_attempts,
            id=id,
            on_failure=on_failure,
            on_success=on_success,
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
        '''Generates CDKTF code for importing a FgsAsyncInvokeConfigV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the FgsAsyncInvokeConfigV2 to import.
        :param import_from_id: The id of the existing FgsAsyncInvokeConfigV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the FgsAsyncInvokeConfigV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e25953b3c3eea4138e80cf9c984b9278b79e73807578979fe0ced60616dd65)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putOnFailure")
    def put_on_failure(self, *, destination: builtins.str, param: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#destination FgsAsyncInvokeConfigV2#destination}.
        :param param: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#param FgsAsyncInvokeConfigV2#param}.
        '''
        value = FgsAsyncInvokeConfigV2OnFailure(destination=destination, param=param)

        return typing.cast(None, jsii.invoke(self, "putOnFailure", [value]))

    @jsii.member(jsii_name="putOnSuccess")
    def put_on_success(self, *, destination: builtins.str, param: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#destination FgsAsyncInvokeConfigV2#destination}.
        :param param: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#param FgsAsyncInvokeConfigV2#param}.
        '''
        value = FgsAsyncInvokeConfigV2OnSuccess(destination=destination, param=param)

        return typing.cast(None, jsii.invoke(self, "putOnSuccess", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOnFailure")
    def reset_on_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnFailure", []))

    @jsii.member(jsii_name="resetOnSuccess")
    def reset_on_success(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnSuccess", []))

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
    @jsii.member(jsii_name="onFailure")
    def on_failure(self) -> "FgsAsyncInvokeConfigV2OnFailureOutputReference":
        return typing.cast("FgsAsyncInvokeConfigV2OnFailureOutputReference", jsii.get(self, "onFailure"))

    @builtins.property
    @jsii.member(jsii_name="onSuccess")
    def on_success(self) -> "FgsAsyncInvokeConfigV2OnSuccessOutputReference":
        return typing.cast("FgsAsyncInvokeConfigV2OnSuccessOutputReference", jsii.get(self, "onSuccess"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="functionUrnInput")
    def function_urn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionUrnInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAsyncEventAgeInSecondsInput")
    def max_async_event_age_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAsyncEventAgeInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAsyncRetryAttemptsInput")
    def max_async_retry_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAsyncRetryAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="onFailureInput")
    def on_failure_input(self) -> typing.Optional["FgsAsyncInvokeConfigV2OnFailure"]:
        return typing.cast(typing.Optional["FgsAsyncInvokeConfigV2OnFailure"], jsii.get(self, "onFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="onSuccessInput")
    def on_success_input(self) -> typing.Optional["FgsAsyncInvokeConfigV2OnSuccess"]:
        return typing.cast(typing.Optional["FgsAsyncInvokeConfigV2OnSuccess"], jsii.get(self, "onSuccessInput"))

    @builtins.property
    @jsii.member(jsii_name="functionUrn")
    def function_urn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionUrn"))

    @function_urn.setter
    def function_urn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eed09a9986073b64340f363c0d32c1d4d41e6274afdf4315f64abc8c215c8e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionUrn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fea9db303f755ed2d1a9c9b604f5b58626b9f97d0eb91e63d164b973b31c6514)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAsyncEventAgeInSeconds")
    def max_async_event_age_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAsyncEventAgeInSeconds"))

    @max_async_event_age_in_seconds.setter
    def max_async_event_age_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__167136df93688be9e2642d1b85591229e52d308d5b5881579f5995d2b627103d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAsyncEventAgeInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAsyncRetryAttempts")
    def max_async_retry_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAsyncRetryAttempts"))

    @max_async_retry_attempts.setter
    def max_async_retry_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37593d1f08fa4fe378776717d8d91a95e7c662990e6153d3c8abe3c2bec09505)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAsyncRetryAttempts", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.fgsAsyncInvokeConfigV2.FgsAsyncInvokeConfigV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "function_urn": "functionUrn",
        "max_async_event_age_in_seconds": "maxAsyncEventAgeInSeconds",
        "max_async_retry_attempts": "maxAsyncRetryAttempts",
        "id": "id",
        "on_failure": "onFailure",
        "on_success": "onSuccess",
    },
)
class FgsAsyncInvokeConfigV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        function_urn: builtins.str,
        max_async_event_age_in_seconds: jsii.Number,
        max_async_retry_attempts: jsii.Number,
        id: typing.Optional[builtins.str] = None,
        on_failure: typing.Optional[typing.Union["FgsAsyncInvokeConfigV2OnFailure", typing.Dict[builtins.str, typing.Any]]] = None,
        on_success: typing.Optional[typing.Union["FgsAsyncInvokeConfigV2OnSuccess", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param function_urn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#function_urn FgsAsyncInvokeConfigV2#function_urn}.
        :param max_async_event_age_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#max_async_event_age_in_seconds FgsAsyncInvokeConfigV2#max_async_event_age_in_seconds}.
        :param max_async_retry_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#max_async_retry_attempts FgsAsyncInvokeConfigV2#max_async_retry_attempts}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#id FgsAsyncInvokeConfigV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param on_failure: on_failure block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#on_failure FgsAsyncInvokeConfigV2#on_failure}
        :param on_success: on_success block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#on_success FgsAsyncInvokeConfigV2#on_success}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(on_failure, dict):
            on_failure = FgsAsyncInvokeConfigV2OnFailure(**on_failure)
        if isinstance(on_success, dict):
            on_success = FgsAsyncInvokeConfigV2OnSuccess(**on_success)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35b73d4602e29075c30cf5d29677548200afdfed92276e0266f7fe95e5f92a14)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument function_urn", value=function_urn, expected_type=type_hints["function_urn"])
            check_type(argname="argument max_async_event_age_in_seconds", value=max_async_event_age_in_seconds, expected_type=type_hints["max_async_event_age_in_seconds"])
            check_type(argname="argument max_async_retry_attempts", value=max_async_retry_attempts, expected_type=type_hints["max_async_retry_attempts"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
            check_type(argname="argument on_success", value=on_success, expected_type=type_hints["on_success"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_urn": function_urn,
            "max_async_event_age_in_seconds": max_async_event_age_in_seconds,
            "max_async_retry_attempts": max_async_retry_attempts,
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
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if on_success is not None:
            self._values["on_success"] = on_success

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
    def function_urn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#function_urn FgsAsyncInvokeConfigV2#function_urn}.'''
        result = self._values.get("function_urn")
        assert result is not None, "Required property 'function_urn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_async_event_age_in_seconds(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#max_async_event_age_in_seconds FgsAsyncInvokeConfigV2#max_async_event_age_in_seconds}.'''
        result = self._values.get("max_async_event_age_in_seconds")
        assert result is not None, "Required property 'max_async_event_age_in_seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def max_async_retry_attempts(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#max_async_retry_attempts FgsAsyncInvokeConfigV2#max_async_retry_attempts}.'''
        result = self._values.get("max_async_retry_attempts")
        assert result is not None, "Required property 'max_async_retry_attempts' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#id FgsAsyncInvokeConfigV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_failure(self) -> typing.Optional["FgsAsyncInvokeConfigV2OnFailure"]:
        '''on_failure block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#on_failure FgsAsyncInvokeConfigV2#on_failure}
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional["FgsAsyncInvokeConfigV2OnFailure"], result)

    @builtins.property
    def on_success(self) -> typing.Optional["FgsAsyncInvokeConfigV2OnSuccess"]:
        '''on_success block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#on_success FgsAsyncInvokeConfigV2#on_success}
        '''
        result = self._values.get("on_success")
        return typing.cast(typing.Optional["FgsAsyncInvokeConfigV2OnSuccess"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FgsAsyncInvokeConfigV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.fgsAsyncInvokeConfigV2.FgsAsyncInvokeConfigV2OnFailure",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination", "param": "param"},
)
class FgsAsyncInvokeConfigV2OnFailure:
    def __init__(self, *, destination: builtins.str, param: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#destination FgsAsyncInvokeConfigV2#destination}.
        :param param: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#param FgsAsyncInvokeConfigV2#param}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b5b3f85ed09bed31800bac99cce894261289bc4f3723667ccb1d64fa18d5208)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument param", value=param, expected_type=type_hints["param"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
            "param": param,
        }

    @builtins.property
    def destination(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#destination FgsAsyncInvokeConfigV2#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def param(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#param FgsAsyncInvokeConfigV2#param}.'''
        result = self._values.get("param")
        assert result is not None, "Required property 'param' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FgsAsyncInvokeConfigV2OnFailure(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FgsAsyncInvokeConfigV2OnFailureOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.fgsAsyncInvokeConfigV2.FgsAsyncInvokeConfigV2OnFailureOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__231c57df8114620cb976e1a16c2667170b153359530ffc50c1b413499ddaa14f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="paramInput")
    def param_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "paramInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d25f30eadb79d82122d8eb69f6f616a655302c8da94a2970f90135f6a8e5c4cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="param")
    def param(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "param"))

    @param.setter
    def param(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21cc0ee14d3942abe88c4dcfee5fd3f953436229016b3683416454561533ed64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "param", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FgsAsyncInvokeConfigV2OnFailure]:
        return typing.cast(typing.Optional[FgsAsyncInvokeConfigV2OnFailure], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FgsAsyncInvokeConfigV2OnFailure],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e76326793e4de3141d98ab3ce87df6f13479971a7ceb404fd7d943fd0a3dcd51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.fgsAsyncInvokeConfigV2.FgsAsyncInvokeConfigV2OnSuccess",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination", "param": "param"},
)
class FgsAsyncInvokeConfigV2OnSuccess:
    def __init__(self, *, destination: builtins.str, param: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#destination FgsAsyncInvokeConfigV2#destination}.
        :param param: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#param FgsAsyncInvokeConfigV2#param}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50d6c1dcc22937843fc1b01ce390c58ebe441c9c2d5c628edc2452a26bf13551)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument param", value=param, expected_type=type_hints["param"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
            "param": param,
        }

    @builtins.property
    def destination(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#destination FgsAsyncInvokeConfigV2#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def param(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_async_invoke_config_v2#param FgsAsyncInvokeConfigV2#param}.'''
        result = self._values.get("param")
        assert result is not None, "Required property 'param' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FgsAsyncInvokeConfigV2OnSuccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FgsAsyncInvokeConfigV2OnSuccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.fgsAsyncInvokeConfigV2.FgsAsyncInvokeConfigV2OnSuccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a69d3912c37d2a8010fba535ca23516bb8a67771a2e2ba9a98277ee45b1a6daa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="paramInput")
    def param_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "paramInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64728a1add6b0eb973cf33536bbf2a694e7d1a8f60f22ce9c1b3387170a4d133)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="param")
    def param(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "param"))

    @param.setter
    def param(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__145c1fc719d9bceb5a72f0c91cbc4aeb8c0c20e797078cc760dccdbad34a7f90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "param", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FgsAsyncInvokeConfigV2OnSuccess]:
        return typing.cast(typing.Optional[FgsAsyncInvokeConfigV2OnSuccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FgsAsyncInvokeConfigV2OnSuccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4300315cbd55d27d29c174bd71818966932ef15f850a6fc304247fe2d39d817f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "FgsAsyncInvokeConfigV2",
    "FgsAsyncInvokeConfigV2Config",
    "FgsAsyncInvokeConfigV2OnFailure",
    "FgsAsyncInvokeConfigV2OnFailureOutputReference",
    "FgsAsyncInvokeConfigV2OnSuccess",
    "FgsAsyncInvokeConfigV2OnSuccessOutputReference",
]

publication.publish()

def _typecheckingstub__614c84f1454506ecf390aea21dab34c4fd0d62a0566de23c9dc1ed31435ec154(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    function_urn: builtins.str,
    max_async_event_age_in_seconds: jsii.Number,
    max_async_retry_attempts: jsii.Number,
    id: typing.Optional[builtins.str] = None,
    on_failure: typing.Optional[typing.Union[FgsAsyncInvokeConfigV2OnFailure, typing.Dict[builtins.str, typing.Any]]] = None,
    on_success: typing.Optional[typing.Union[FgsAsyncInvokeConfigV2OnSuccess, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__04e25953b3c3eea4138e80cf9c984b9278b79e73807578979fe0ced60616dd65(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eed09a9986073b64340f363c0d32c1d4d41e6274afdf4315f64abc8c215c8e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea9db303f755ed2d1a9c9b604f5b58626b9f97d0eb91e63d164b973b31c6514(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__167136df93688be9e2642d1b85591229e52d308d5b5881579f5995d2b627103d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37593d1f08fa4fe378776717d8d91a95e7c662990e6153d3c8abe3c2bec09505(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35b73d4602e29075c30cf5d29677548200afdfed92276e0266f7fe95e5f92a14(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    function_urn: builtins.str,
    max_async_event_age_in_seconds: jsii.Number,
    max_async_retry_attempts: jsii.Number,
    id: typing.Optional[builtins.str] = None,
    on_failure: typing.Optional[typing.Union[FgsAsyncInvokeConfigV2OnFailure, typing.Dict[builtins.str, typing.Any]]] = None,
    on_success: typing.Optional[typing.Union[FgsAsyncInvokeConfigV2OnSuccess, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b5b3f85ed09bed31800bac99cce894261289bc4f3723667ccb1d64fa18d5208(
    *,
    destination: builtins.str,
    param: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__231c57df8114620cb976e1a16c2667170b153359530ffc50c1b413499ddaa14f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d25f30eadb79d82122d8eb69f6f616a655302c8da94a2970f90135f6a8e5c4cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21cc0ee14d3942abe88c4dcfee5fd3f953436229016b3683416454561533ed64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e76326793e4de3141d98ab3ce87df6f13479971a7ceb404fd7d943fd0a3dcd51(
    value: typing.Optional[FgsAsyncInvokeConfigV2OnFailure],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50d6c1dcc22937843fc1b01ce390c58ebe441c9c2d5c628edc2452a26bf13551(
    *,
    destination: builtins.str,
    param: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a69d3912c37d2a8010fba535ca23516bb8a67771a2e2ba9a98277ee45b1a6daa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64728a1add6b0eb973cf33536bbf2a694e7d1a8f60f22ce9c1b3387170a4d133(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145c1fc719d9bceb5a72f0c91cbc4aeb8c0c20e797078cc760dccdbad34a7f90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4300315cbd55d27d29c174bd71818966932ef15f850a6fc304247fe2d39d817f(
    value: typing.Optional[FgsAsyncInvokeConfigV2OnSuccess],
) -> None:
    """Type checking stubs"""
    pass
