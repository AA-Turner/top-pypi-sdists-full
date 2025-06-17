r'''
# `pagerduty_extension_servicenow`

Refer to the Terraform Registry for docs: [`pagerduty_extension_servicenow`](https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow).
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


class ExtensionServicenow(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.extensionServicenow.ExtensionServicenow",
):
    '''Represents a {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow pagerduty_extension_servicenow}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        extension_objects: typing.Sequence[builtins.str],
        extension_schema: builtins.str,
        referer: builtins.str,
        snow_password: builtins.str,
        snow_user: builtins.str,
        sync_options: builtins.str,
        target: builtins.str,
        task_type: builtins.str,
        endpoint_url: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        summary: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow pagerduty_extension_servicenow} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param extension_objects: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#extension_objects ExtensionServicenow#extension_objects}.
        :param extension_schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#extension_schema ExtensionServicenow#extension_schema}.
        :param referer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#referer ExtensionServicenow#referer}.
        :param snow_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#snow_password ExtensionServicenow#snow_password}.
        :param snow_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#snow_user ExtensionServicenow#snow_user}.
        :param sync_options: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#sync_options ExtensionServicenow#sync_options}.
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#target ExtensionServicenow#target}.
        :param task_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#task_type ExtensionServicenow#task_type}.
        :param endpoint_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#endpoint_url ExtensionServicenow#endpoint_url}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#name ExtensionServicenow#name}.
        :param summary: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#summary ExtensionServicenow#summary}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#type ExtensionServicenow#type}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f21b52c56034696c6898902978666b4465ba121ec4bfc084edee0878abc2e189)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = ExtensionServicenowConfig(
            extension_objects=extension_objects,
            extension_schema=extension_schema,
            referer=referer,
            snow_password=snow_password,
            snow_user=snow_user,
            sync_options=sync_options,
            target=target,
            task_type=task_type,
            endpoint_url=endpoint_url,
            name=name,
            summary=summary,
            type=type,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a ExtensionServicenow resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ExtensionServicenow to import.
        :param import_from_id: The id of the existing ExtensionServicenow that should be imported. Refer to the {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ExtensionServicenow to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0920e414721b1a2a677c9684b0fb89c8a06396af8eeff7ac7cdf86f85ecae363)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetEndpointUrl")
    def reset_endpoint_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointUrl", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSummary")
    def reset_summary(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSummary", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

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
    @jsii.member(jsii_name="htmlUrl")
    def html_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "htmlUrl"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="endpointUrlInput")
    def endpoint_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="extensionObjectsInput")
    def extension_objects_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "extensionObjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="extensionSchemaInput")
    def extension_schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "extensionSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="refererInput")
    def referer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "refererInput"))

    @builtins.property
    @jsii.member(jsii_name="snowPasswordInput")
    def snow_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snowPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="snowUserInput")
    def snow_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snowUserInput"))

    @builtins.property
    @jsii.member(jsii_name="summaryInput")
    def summary_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "summaryInput"))

    @builtins.property
    @jsii.member(jsii_name="syncOptionsInput")
    def sync_options_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "syncOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="taskTypeInput")
    def task_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "taskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointUrl")
    def endpoint_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointUrl"))

    @endpoint_url.setter
    def endpoint_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__767192c58e3bab281548b7e9c949d33c67446174abe2de2752040aa3fc4d9eab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extensionObjects")
    def extension_objects(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "extensionObjects"))

    @extension_objects.setter
    def extension_objects(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c7c430c26a351af1d429d1f77fcf7a50490139df2f945ad82d7fb806a9762d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extensionObjects", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extensionSchema")
    def extension_schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "extensionSchema"))

    @extension_schema.setter
    def extension_schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4be55040f94e2d98a0d05e910c913f62b1a0263ad0759b4082c42a98ed4a777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extensionSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b58846b739101a580ec25208e4b8d8602e2222733218e7f7816198d9ef882f4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="referer")
    def referer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "referer"))

    @referer.setter
    def referer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c65230bd593e43f2c30e44abb15243844b00bf569180f70bf88f7c0ded5e373)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snowPassword")
    def snow_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snowPassword"))

    @snow_password.setter
    def snow_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccd21f4d336d2af39ad80509029aa4ec757218cced0f1e03977d45d43df5bab1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snowPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snowUser")
    def snow_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snowUser"))

    @snow_user.setter
    def snow_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c3bf8786dcddf85d9190e86309a4cf6dae032f5ffc60fbbeae5c2218b4ea09f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snowUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="summary")
    def summary(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "summary"))

    @summary.setter
    def summary(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c4836fc628efd1cb03046cc8fb7d883a90753aa8cc5404c328489412b46ead)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "summary", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncOptions")
    def sync_options(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncOptions"))

    @sync_options.setter
    def sync_options(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c75fa8c41093ba4b25fe3a8ee2d65c5ace1bee9603cedfd5776ed99e9eb1fab2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__146d08ddd162ead4ccea27e01a0050f99045d6bca172b396dfbbf6c201044fbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskType")
    def task_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taskType"))

    @task_type.setter
    def task_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cef3525855f3858f8abf0a6797fe7dd375548e33d9acfa987acbf6af821e62a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__328f754d387b2bd51870516bd0f82af153fd9f67c397c0acf0fc09aa5767ede1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.extensionServicenow.ExtensionServicenowConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "extension_objects": "extensionObjects",
        "extension_schema": "extensionSchema",
        "referer": "referer",
        "snow_password": "snowPassword",
        "snow_user": "snowUser",
        "sync_options": "syncOptions",
        "target": "target",
        "task_type": "taskType",
        "endpoint_url": "endpointUrl",
        "name": "name",
        "summary": "summary",
        "type": "type",
    },
)
class ExtensionServicenowConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        extension_objects: typing.Sequence[builtins.str],
        extension_schema: builtins.str,
        referer: builtins.str,
        snow_password: builtins.str,
        snow_user: builtins.str,
        sync_options: builtins.str,
        target: builtins.str,
        task_type: builtins.str,
        endpoint_url: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        summary: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param extension_objects: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#extension_objects ExtensionServicenow#extension_objects}.
        :param extension_schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#extension_schema ExtensionServicenow#extension_schema}.
        :param referer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#referer ExtensionServicenow#referer}.
        :param snow_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#snow_password ExtensionServicenow#snow_password}.
        :param snow_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#snow_user ExtensionServicenow#snow_user}.
        :param sync_options: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#sync_options ExtensionServicenow#sync_options}.
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#target ExtensionServicenow#target}.
        :param task_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#task_type ExtensionServicenow#task_type}.
        :param endpoint_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#endpoint_url ExtensionServicenow#endpoint_url}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#name ExtensionServicenow#name}.
        :param summary: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#summary ExtensionServicenow#summary}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#type ExtensionServicenow#type}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0beb07f50e3ee575d5382e6c7d7d46e3ab187397ee327befb9837e33dfdc9405)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument extension_objects", value=extension_objects, expected_type=type_hints["extension_objects"])
            check_type(argname="argument extension_schema", value=extension_schema, expected_type=type_hints["extension_schema"])
            check_type(argname="argument referer", value=referer, expected_type=type_hints["referer"])
            check_type(argname="argument snow_password", value=snow_password, expected_type=type_hints["snow_password"])
            check_type(argname="argument snow_user", value=snow_user, expected_type=type_hints["snow_user"])
            check_type(argname="argument sync_options", value=sync_options, expected_type=type_hints["sync_options"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument task_type", value=task_type, expected_type=type_hints["task_type"])
            check_type(argname="argument endpoint_url", value=endpoint_url, expected_type=type_hints["endpoint_url"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument summary", value=summary, expected_type=type_hints["summary"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "extension_objects": extension_objects,
            "extension_schema": extension_schema,
            "referer": referer,
            "snow_password": snow_password,
            "snow_user": snow_user,
            "sync_options": sync_options,
            "target": target,
            "task_type": task_type,
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
        if endpoint_url is not None:
            self._values["endpoint_url"] = endpoint_url
        if name is not None:
            self._values["name"] = name
        if summary is not None:
            self._values["summary"] = summary
        if type is not None:
            self._values["type"] = type

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
    def extension_objects(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#extension_objects ExtensionServicenow#extension_objects}.'''
        result = self._values.get("extension_objects")
        assert result is not None, "Required property 'extension_objects' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def extension_schema(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#extension_schema ExtensionServicenow#extension_schema}.'''
        result = self._values.get("extension_schema")
        assert result is not None, "Required property 'extension_schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def referer(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#referer ExtensionServicenow#referer}.'''
        result = self._values.get("referer")
        assert result is not None, "Required property 'referer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def snow_password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#snow_password ExtensionServicenow#snow_password}.'''
        result = self._values.get("snow_password")
        assert result is not None, "Required property 'snow_password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def snow_user(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#snow_user ExtensionServicenow#snow_user}.'''
        result = self._values.get("snow_user")
        assert result is not None, "Required property 'snow_user' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sync_options(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#sync_options ExtensionServicenow#sync_options}.'''
        result = self._values.get("sync_options")
        assert result is not None, "Required property 'sync_options' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#target ExtensionServicenow#target}.'''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def task_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#task_type ExtensionServicenow#task_type}.'''
        result = self._values.get("task_type")
        assert result is not None, "Required property 'task_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def endpoint_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#endpoint_url ExtensionServicenow#endpoint_url}.'''
        result = self._values.get("endpoint_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#name ExtensionServicenow#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def summary(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#summary ExtensionServicenow#summary}.'''
        result = self._values.get("summary")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/extension_servicenow#type ExtensionServicenow#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExtensionServicenowConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ExtensionServicenow",
    "ExtensionServicenowConfig",
]

publication.publish()

def _typecheckingstub__f21b52c56034696c6898902978666b4465ba121ec4bfc084edee0878abc2e189(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    extension_objects: typing.Sequence[builtins.str],
    extension_schema: builtins.str,
    referer: builtins.str,
    snow_password: builtins.str,
    snow_user: builtins.str,
    sync_options: builtins.str,
    target: builtins.str,
    task_type: builtins.str,
    endpoint_url: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    summary: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__0920e414721b1a2a677c9684b0fb89c8a06396af8eeff7ac7cdf86f85ecae363(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__767192c58e3bab281548b7e9c949d33c67446174abe2de2752040aa3fc4d9eab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c7c430c26a351af1d429d1f77fcf7a50490139df2f945ad82d7fb806a9762d1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4be55040f94e2d98a0d05e910c913f62b1a0263ad0759b4082c42a98ed4a777(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b58846b739101a580ec25208e4b8d8602e2222733218e7f7816198d9ef882f4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c65230bd593e43f2c30e44abb15243844b00bf569180f70bf88f7c0ded5e373(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccd21f4d336d2af39ad80509029aa4ec757218cced0f1e03977d45d43df5bab1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c3bf8786dcddf85d9190e86309a4cf6dae032f5ffc60fbbeae5c2218b4ea09f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c4836fc628efd1cb03046cc8fb7d883a90753aa8cc5404c328489412b46ead(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c75fa8c41093ba4b25fe3a8ee2d65c5ace1bee9603cedfd5776ed99e9eb1fab2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__146d08ddd162ead4ccea27e01a0050f99045d6bca172b396dfbbf6c201044fbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cef3525855f3858f8abf0a6797fe7dd375548e33d9acfa987acbf6af821e62a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__328f754d387b2bd51870516bd0f82af153fd9f67c397c0acf0fc09aa5767ede1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0beb07f50e3ee575d5382e6c7d7d46e3ab187397ee327befb9837e33dfdc9405(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    extension_objects: typing.Sequence[builtins.str],
    extension_schema: builtins.str,
    referer: builtins.str,
    snow_password: builtins.str,
    snow_user: builtins.str,
    sync_options: builtins.str,
    target: builtins.str,
    task_type: builtins.str,
    endpoint_url: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    summary: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
