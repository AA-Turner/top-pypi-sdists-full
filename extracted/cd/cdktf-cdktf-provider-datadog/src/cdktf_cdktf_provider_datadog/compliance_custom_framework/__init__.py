r'''
# `datadog_compliance_custom_framework`

Refer to the Terraform Registry for docs: [`datadog_compliance_custom_framework`](https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework).
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


class ComplianceCustomFramework(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.complianceCustomFramework.ComplianceCustomFramework",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework datadog_compliance_custom_framework}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        handle: builtins.str,
        name: builtins.str,
        version: builtins.str,
        icon_url: typing.Optional[builtins.str] = None,
        requirements: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComplianceCustomFrameworkRequirements", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework datadog_compliance_custom_framework} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param handle: The framework handle. String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#handle ComplianceCustomFramework#handle}
        :param name: The framework name. String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#name ComplianceCustomFramework#name}
        :param version: The framework version. String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#version ComplianceCustomFramework#version}
        :param icon_url: The URL of the icon representing the framework. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#icon_url ComplianceCustomFramework#icon_url}
        :param requirements: requirements block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#requirements ComplianceCustomFramework#requirements}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__467db4a425a55c4027d971fb8d3d5618d0a6380328ac8f9c95f0cc5bf49c5329)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = ComplianceCustomFrameworkConfig(
            handle=handle,
            name=name,
            version=version,
            icon_url=icon_url,
            requirements=requirements,
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
        '''Generates CDKTF code for importing a ComplianceCustomFramework resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComplianceCustomFramework to import.
        :param import_from_id: The id of the existing ComplianceCustomFramework that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComplianceCustomFramework to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b631ab59bb74661807e36b8a7cb3c00db1398f47d758c3139efd26df8aa3a734)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRequirements")
    def put_requirements(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComplianceCustomFrameworkRequirements", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecd8386e95f444e31074b70864cb695b18efdc4f1d93647f4249052b21103b69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequirements", [value]))

    @jsii.member(jsii_name="resetIconUrl")
    def reset_icon_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIconUrl", []))

    @jsii.member(jsii_name="resetRequirements")
    def reset_requirements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequirements", []))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="requirements")
    def requirements(self) -> "ComplianceCustomFrameworkRequirementsList":
        return typing.cast("ComplianceCustomFrameworkRequirementsList", jsii.get(self, "requirements"))

    @builtins.property
    @jsii.member(jsii_name="handleInput")
    def handle_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "handleInput"))

    @builtins.property
    @jsii.member(jsii_name="iconUrlInput")
    def icon_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iconUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="requirementsInput")
    def requirements_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComplianceCustomFrameworkRequirements"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComplianceCustomFrameworkRequirements"]]], jsii.get(self, "requirementsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="handle")
    def handle(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "handle"))

    @handle.setter
    def handle(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c632031af4721540902545c0b7deda8eacd56eea918c776d652a4ecc65490922)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "handle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iconUrl")
    def icon_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iconUrl"))

    @icon_url.setter
    def icon_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78d325a7f2bd6a7cf2ef8d8a1240f288b495af5d114c44955ab20959508c2b8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iconUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0dcb58de286cd667f2c12f791b73b27aa533a779df3c5e7abfde94f0e3b5b51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__895b43f75aa509545128b1d6c920514fb9c62e12693dd65e9924ce81128393df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.complianceCustomFramework.ComplianceCustomFrameworkConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "handle": "handle",
        "name": "name",
        "version": "version",
        "icon_url": "iconUrl",
        "requirements": "requirements",
    },
)
class ComplianceCustomFrameworkConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        handle: builtins.str,
        name: builtins.str,
        version: builtins.str,
        icon_url: typing.Optional[builtins.str] = None,
        requirements: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComplianceCustomFrameworkRequirements", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param handle: The framework handle. String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#handle ComplianceCustomFramework#handle}
        :param name: The framework name. String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#name ComplianceCustomFramework#name}
        :param version: The framework version. String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#version ComplianceCustomFramework#version}
        :param icon_url: The URL of the icon representing the framework. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#icon_url ComplianceCustomFramework#icon_url}
        :param requirements: requirements block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#requirements ComplianceCustomFramework#requirements}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bce965951764a67a3778821b1b3408ecbf0fc4056cc87ffd4479f98cf4b51f1e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument handle", value=handle, expected_type=type_hints["handle"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument icon_url", value=icon_url, expected_type=type_hints["icon_url"])
            check_type(argname="argument requirements", value=requirements, expected_type=type_hints["requirements"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "handle": handle,
            "name": name,
            "version": version,
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
        if icon_url is not None:
            self._values["icon_url"] = icon_url
        if requirements is not None:
            self._values["requirements"] = requirements

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
    def handle(self) -> builtins.str:
        '''The framework handle. String length must be at least 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#handle ComplianceCustomFramework#handle}
        '''
        result = self._values.get("handle")
        assert result is not None, "Required property 'handle' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The framework name. String length must be at least 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#name ComplianceCustomFramework#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''The framework version. String length must be at least 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#version ComplianceCustomFramework#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def icon_url(self) -> typing.Optional[builtins.str]:
        '''The URL of the icon representing the framework.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#icon_url ComplianceCustomFramework#icon_url}
        '''
        result = self._values.get("icon_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def requirements(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComplianceCustomFrameworkRequirements"]]]:
        '''requirements block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#requirements ComplianceCustomFramework#requirements}
        '''
        result = self._values.get("requirements")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComplianceCustomFrameworkRequirements"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComplianceCustomFrameworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.complianceCustomFramework.ComplianceCustomFrameworkRequirements",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "controls": "controls"},
)
class ComplianceCustomFrameworkRequirements:
    def __init__(
        self,
        *,
        name: builtins.str,
        controls: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComplianceCustomFrameworkRequirementsControls", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: The name of the requirement. String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#name ComplianceCustomFramework#name}
        :param controls: controls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#controls ComplianceCustomFramework#controls}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9cb760fd005aec3b74fe56b2661abd92b7c162476b779ef8ab8e567e2beb403)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument controls", value=controls, expected_type=type_hints["controls"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if controls is not None:
            self._values["controls"] = controls

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the requirement. String length must be at least 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#name ComplianceCustomFramework#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def controls(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComplianceCustomFrameworkRequirementsControls"]]]:
        '''controls block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#controls ComplianceCustomFramework#controls}
        '''
        result = self._values.get("controls")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComplianceCustomFrameworkRequirementsControls"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComplianceCustomFrameworkRequirements(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.complianceCustomFramework.ComplianceCustomFrameworkRequirementsControls",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "rules_id": "rulesId"},
)
class ComplianceCustomFrameworkRequirementsControls:
    def __init__(
        self,
        *,
        name: builtins.str,
        rules_id: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: The name of the control. String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#name ComplianceCustomFramework#name}
        :param rules_id: The set of rules IDs for the control. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#rules_id ComplianceCustomFramework#rules_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b34414a21116081dab839183808f826aa7efcf8b4688a08aa2246fa5586a7d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rules_id", value=rules_id, expected_type=type_hints["rules_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "rules_id": rules_id,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the control. String length must be at least 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#name ComplianceCustomFramework#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rules_id(self) -> typing.List[builtins.str]:
        '''The set of rules IDs for the control.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/compliance_custom_framework#rules_id ComplianceCustomFramework#rules_id}
        '''
        result = self._values.get("rules_id")
        assert result is not None, "Required property 'rules_id' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComplianceCustomFrameworkRequirementsControls(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComplianceCustomFrameworkRequirementsControlsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.complianceCustomFramework.ComplianceCustomFrameworkRequirementsControlsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5dcb5781f1ee05e3d32a9178c69a70b74f15a3e3acb6a42c265374e0336a72b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComplianceCustomFrameworkRequirementsControlsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__605aab75b97d8b94e52947da675673f8b98e79634d51b529d7d08bff223ffe09)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComplianceCustomFrameworkRequirementsControlsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__543afc366bd31c780b637bbe20f825a0aef3277085e221285775bc22ae18a7d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7311196e8091c7989a6071871ffe5a7f77f86dbf9953939145a90ddab3c95ee0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__359157209f3e83c5469d56e67a0e11b1db31bc3bd3b51bd52c5a28973baabe13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComplianceCustomFrameworkRequirementsControls]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComplianceCustomFrameworkRequirementsControls]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComplianceCustomFrameworkRequirementsControls]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db8b01248dfb2a6866c339be374528d1c5d6956adca4441cee2e8db71f684379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComplianceCustomFrameworkRequirementsControlsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.complianceCustomFramework.ComplianceCustomFrameworkRequirementsControlsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e884a809ce559f384b57910aaec19ec4db06039dbadd199939263b2bfad3158)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesIdInput")
    def rules_id_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rulesIdInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a56bfe5a8fab1910bc472fbadb17f5cce5d4d0f9619795f084dd46dfe66fd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rulesId")
    def rules_id(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rulesId"))

    @rules_id.setter
    def rules_id(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc5be1fc4ae61d3cf7ab2bcecc1ceddba0c9b297fe3c7b3fa9500dad00ac404a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rulesId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComplianceCustomFrameworkRequirementsControls]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComplianceCustomFrameworkRequirementsControls]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComplianceCustomFrameworkRequirementsControls]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__639b4d0fc8e45b97a0933c2e61d083b9dfa0c1383101d3d3fcbb6ab85c46eebe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComplianceCustomFrameworkRequirementsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.complianceCustomFramework.ComplianceCustomFrameworkRequirementsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db83f3553f767b2ccf81d8290c16952f169bb787ca7e4e4d45ced3a59462fe37)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComplianceCustomFrameworkRequirementsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0526123b280df3dc94267534a89fa6b57c6d64bb6797a949bd835f4ab147949b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComplianceCustomFrameworkRequirementsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e2cc2b344da055866d547c1a55c0c1ebd84436c76eb5dd1b9e8aa2dde6a3bf2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__400a4fcf7ebf03335996f1319053c6267a0a1f76efa10a3817b7ea490afb2288)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91d819b3c08e0f1b535dfe6ce6817eafb6fd886993277806ec390f80c502753a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComplianceCustomFrameworkRequirements]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComplianceCustomFrameworkRequirements]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComplianceCustomFrameworkRequirements]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23453486da95bda4692dfd787d86e57a59dfb5eab1385a3beba330832778859c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComplianceCustomFrameworkRequirementsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.complianceCustomFramework.ComplianceCustomFrameworkRequirementsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36e25388bbeb4739b2693677bb3299bd914aaaaec6aa037caab7e53c2b20bc6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putControls")
    def put_controls(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComplianceCustomFrameworkRequirementsControls, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c9de9b0c37364b7cf9b2dd91d8530c7b7ba00439dc758e9e3b909d557e1b998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putControls", [value]))

    @jsii.member(jsii_name="resetControls")
    def reset_controls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControls", []))

    @builtins.property
    @jsii.member(jsii_name="controls")
    def controls(self) -> ComplianceCustomFrameworkRequirementsControlsList:
        return typing.cast(ComplianceCustomFrameworkRequirementsControlsList, jsii.get(self, "controls"))

    @builtins.property
    @jsii.member(jsii_name="controlsInput")
    def controls_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComplianceCustomFrameworkRequirementsControls]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComplianceCustomFrameworkRequirementsControls]]], jsii.get(self, "controlsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49557dc0b766f7a199c676381f37a7412df7eb2143ea20d6fad8267e98d8fcc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComplianceCustomFrameworkRequirements]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComplianceCustomFrameworkRequirements]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComplianceCustomFrameworkRequirements]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d76b7f1216887125475062d2cff855cfc5af36531ab30b120be5b83f7ee1d1da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComplianceCustomFramework",
    "ComplianceCustomFrameworkConfig",
    "ComplianceCustomFrameworkRequirements",
    "ComplianceCustomFrameworkRequirementsControls",
    "ComplianceCustomFrameworkRequirementsControlsList",
    "ComplianceCustomFrameworkRequirementsControlsOutputReference",
    "ComplianceCustomFrameworkRequirementsList",
    "ComplianceCustomFrameworkRequirementsOutputReference",
]

publication.publish()

def _typecheckingstub__467db4a425a55c4027d971fb8d3d5618d0a6380328ac8f9c95f0cc5bf49c5329(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    handle: builtins.str,
    name: builtins.str,
    version: builtins.str,
    icon_url: typing.Optional[builtins.str] = None,
    requirements: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComplianceCustomFrameworkRequirements, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__b631ab59bb74661807e36b8a7cb3c00db1398f47d758c3139efd26df8aa3a734(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecd8386e95f444e31074b70864cb695b18efdc4f1d93647f4249052b21103b69(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComplianceCustomFrameworkRequirements, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c632031af4721540902545c0b7deda8eacd56eea918c776d652a4ecc65490922(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78d325a7f2bd6a7cf2ef8d8a1240f288b495af5d114c44955ab20959508c2b8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0dcb58de286cd667f2c12f791b73b27aa533a779df3c5e7abfde94f0e3b5b51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__895b43f75aa509545128b1d6c920514fb9c62e12693dd65e9924ce81128393df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce965951764a67a3778821b1b3408ecbf0fc4056cc87ffd4479f98cf4b51f1e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    handle: builtins.str,
    name: builtins.str,
    version: builtins.str,
    icon_url: typing.Optional[builtins.str] = None,
    requirements: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComplianceCustomFrameworkRequirements, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9cb760fd005aec3b74fe56b2661abd92b7c162476b779ef8ab8e567e2beb403(
    *,
    name: builtins.str,
    controls: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComplianceCustomFrameworkRequirementsControls, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b34414a21116081dab839183808f826aa7efcf8b4688a08aa2246fa5586a7d(
    *,
    name: builtins.str,
    rules_id: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dcb5781f1ee05e3d32a9178c69a70b74f15a3e3acb6a42c265374e0336a72b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__605aab75b97d8b94e52947da675673f8b98e79634d51b529d7d08bff223ffe09(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__543afc366bd31c780b637bbe20f825a0aef3277085e221285775bc22ae18a7d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7311196e8091c7989a6071871ffe5a7f77f86dbf9953939145a90ddab3c95ee0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__359157209f3e83c5469d56e67a0e11b1db31bc3bd3b51bd52c5a28973baabe13(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db8b01248dfb2a6866c339be374528d1c5d6956adca4441cee2e8db71f684379(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComplianceCustomFrameworkRequirementsControls]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e884a809ce559f384b57910aaec19ec4db06039dbadd199939263b2bfad3158(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a56bfe5a8fab1910bc472fbadb17f5cce5d4d0f9619795f084dd46dfe66fd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc5be1fc4ae61d3cf7ab2bcecc1ceddba0c9b297fe3c7b3fa9500dad00ac404a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__639b4d0fc8e45b97a0933c2e61d083b9dfa0c1383101d3d3fcbb6ab85c46eebe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComplianceCustomFrameworkRequirementsControls]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db83f3553f767b2ccf81d8290c16952f169bb787ca7e4e4d45ced3a59462fe37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0526123b280df3dc94267534a89fa6b57c6d64bb6797a949bd835f4ab147949b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e2cc2b344da055866d547c1a55c0c1ebd84436c76eb5dd1b9e8aa2dde6a3bf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400a4fcf7ebf03335996f1319053c6267a0a1f76efa10a3817b7ea490afb2288(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d819b3c08e0f1b535dfe6ce6817eafb6fd886993277806ec390f80c502753a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23453486da95bda4692dfd787d86e57a59dfb5eab1385a3beba330832778859c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComplianceCustomFrameworkRequirements]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36e25388bbeb4739b2693677bb3299bd914aaaaec6aa037caab7e53c2b20bc6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c9de9b0c37364b7cf9b2dd91d8530c7b7ba00439dc758e9e3b909d557e1b998(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComplianceCustomFrameworkRequirementsControls, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49557dc0b766f7a199c676381f37a7412df7eb2143ea20d6fad8267e98d8fcc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76b7f1216887125475062d2cff855cfc5af36531ab30b120be5b83f7ee1d1da(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComplianceCustomFrameworkRequirements]],
) -> None:
    """Type checking stubs"""
    pass
