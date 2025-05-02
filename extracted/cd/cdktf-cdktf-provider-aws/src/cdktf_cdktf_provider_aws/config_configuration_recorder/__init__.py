r'''
# `aws_config_configuration_recorder`

Refer to the Terraform Registry for docs: [`aws_config_configuration_recorder`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder).
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


class ConfigConfigurationRecorder(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.configConfigurationRecorder.ConfigConfigurationRecorder",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder aws_config_configuration_recorder}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        role_arn: builtins.str,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        recording_group: typing.Optional[typing.Union["ConfigConfigurationRecorderRecordingGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        recording_mode: typing.Optional[typing.Union["ConfigConfigurationRecorderRecordingMode", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder aws_config_configuration_recorder} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#role_arn ConfigConfigurationRecorder#role_arn}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#id ConfigConfigurationRecorder#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#name ConfigConfigurationRecorder#name}.
        :param recording_group: recording_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#recording_group ConfigConfigurationRecorder#recording_group}
        :param recording_mode: recording_mode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#recording_mode ConfigConfigurationRecorder#recording_mode}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2841188513eb315ed250afbfee2a4f5083c21b5faae6754a25cfc7d915cd811)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ConfigConfigurationRecorderConfig(
            role_arn=role_arn,
            id=id,
            name=name,
            recording_group=recording_group,
            recording_mode=recording_mode,
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
        '''Generates CDKTF code for importing a ConfigConfigurationRecorder resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ConfigConfigurationRecorder to import.
        :param import_from_id: The id of the existing ConfigConfigurationRecorder that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ConfigConfigurationRecorder to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0b136d7d0a0076655f8e7b04f73870f35fc46291065f4f39e5679a9dab3eb17)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRecordingGroup")
    def put_recording_group(
        self,
        *,
        all_supported: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclusion_by_resource_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        include_global_resource_types: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        recording_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ConfigConfigurationRecorderRecordingGroupRecordingStrategy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param all_supported: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#all_supported ConfigConfigurationRecorder#all_supported}.
        :param exclusion_by_resource_types: exclusion_by_resource_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#exclusion_by_resource_types ConfigConfigurationRecorder#exclusion_by_resource_types}
        :param include_global_resource_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#include_global_resource_types ConfigConfigurationRecorder#include_global_resource_types}.
        :param recording_strategy: recording_strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#recording_strategy ConfigConfigurationRecorder#recording_strategy}
        :param resource_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#resource_types ConfigConfigurationRecorder#resource_types}.
        '''
        value = ConfigConfigurationRecorderRecordingGroup(
            all_supported=all_supported,
            exclusion_by_resource_types=exclusion_by_resource_types,
            include_global_resource_types=include_global_resource_types,
            recording_strategy=recording_strategy,
            resource_types=resource_types,
        )

        return typing.cast(None, jsii.invoke(self, "putRecordingGroup", [value]))

    @jsii.member(jsii_name="putRecordingMode")
    def put_recording_mode(
        self,
        *,
        recording_frequency: typing.Optional[builtins.str] = None,
        recording_mode_override: typing.Optional[typing.Union["ConfigConfigurationRecorderRecordingModeRecordingModeOverride", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param recording_frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#recording_frequency ConfigConfigurationRecorder#recording_frequency}.
        :param recording_mode_override: recording_mode_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#recording_mode_override ConfigConfigurationRecorder#recording_mode_override}
        '''
        value = ConfigConfigurationRecorderRecordingMode(
            recording_frequency=recording_frequency,
            recording_mode_override=recording_mode_override,
        )

        return typing.cast(None, jsii.invoke(self, "putRecordingMode", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetRecordingGroup")
    def reset_recording_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecordingGroup", []))

    @jsii.member(jsii_name="resetRecordingMode")
    def reset_recording_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecordingMode", []))

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
    @jsii.member(jsii_name="recordingGroup")
    def recording_group(
        self,
    ) -> "ConfigConfigurationRecorderRecordingGroupOutputReference":
        return typing.cast("ConfigConfigurationRecorderRecordingGroupOutputReference", jsii.get(self, "recordingGroup"))

    @builtins.property
    @jsii.member(jsii_name="recordingMode")
    def recording_mode(
        self,
    ) -> "ConfigConfigurationRecorderRecordingModeOutputReference":
        return typing.cast("ConfigConfigurationRecorderRecordingModeOutputReference", jsii.get(self, "recordingMode"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="recordingGroupInput")
    def recording_group_input(
        self,
    ) -> typing.Optional["ConfigConfigurationRecorderRecordingGroup"]:
        return typing.cast(typing.Optional["ConfigConfigurationRecorderRecordingGroup"], jsii.get(self, "recordingGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="recordingModeInput")
    def recording_mode_input(
        self,
    ) -> typing.Optional["ConfigConfigurationRecorderRecordingMode"]:
        return typing.cast(typing.Optional["ConfigConfigurationRecorderRecordingMode"], jsii.get(self, "recordingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a84a7ea446d3e7f1896fc1e577520fdb566557030e0c1bdb363f06dad22ceca2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__429385fdfe98e49321bf0a8730d312fe8e2a7b1c403ff1debb56252c2ab5e135)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__537cf897d3b8d3869cef524733467375011f74f83f9ffcad0ec1a83c7ec8a681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.configConfigurationRecorder.ConfigConfigurationRecorderConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "role_arn": "roleArn",
        "id": "id",
        "name": "name",
        "recording_group": "recordingGroup",
        "recording_mode": "recordingMode",
    },
)
class ConfigConfigurationRecorderConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        role_arn: builtins.str,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        recording_group: typing.Optional[typing.Union["ConfigConfigurationRecorderRecordingGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        recording_mode: typing.Optional[typing.Union["ConfigConfigurationRecorderRecordingMode", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#role_arn ConfigConfigurationRecorder#role_arn}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#id ConfigConfigurationRecorder#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#name ConfigConfigurationRecorder#name}.
        :param recording_group: recording_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#recording_group ConfigConfigurationRecorder#recording_group}
        :param recording_mode: recording_mode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#recording_mode ConfigConfigurationRecorder#recording_mode}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(recording_group, dict):
            recording_group = ConfigConfigurationRecorderRecordingGroup(**recording_group)
        if isinstance(recording_mode, dict):
            recording_mode = ConfigConfigurationRecorderRecordingMode(**recording_mode)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81e04e5eee3181224f2992bb9a20f58e528256c64e21fa1945f8491592a72711)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument recording_group", value=recording_group, expected_type=type_hints["recording_group"])
            check_type(argname="argument recording_mode", value=recording_mode, expected_type=type_hints["recording_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
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
        if name is not None:
            self._values["name"] = name
        if recording_group is not None:
            self._values["recording_group"] = recording_group
        if recording_mode is not None:
            self._values["recording_mode"] = recording_mode

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
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#role_arn ConfigConfigurationRecorder#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#id ConfigConfigurationRecorder#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#name ConfigConfigurationRecorder#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recording_group(
        self,
    ) -> typing.Optional["ConfigConfigurationRecorderRecordingGroup"]:
        '''recording_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#recording_group ConfigConfigurationRecorder#recording_group}
        '''
        result = self._values.get("recording_group")
        return typing.cast(typing.Optional["ConfigConfigurationRecorderRecordingGroup"], result)

    @builtins.property
    def recording_mode(
        self,
    ) -> typing.Optional["ConfigConfigurationRecorderRecordingMode"]:
        '''recording_mode block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#recording_mode ConfigConfigurationRecorder#recording_mode}
        '''
        result = self._values.get("recording_mode")
        return typing.cast(typing.Optional["ConfigConfigurationRecorderRecordingMode"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConfigConfigurationRecorderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.configConfigurationRecorder.ConfigConfigurationRecorderRecordingGroup",
    jsii_struct_bases=[],
    name_mapping={
        "all_supported": "allSupported",
        "exclusion_by_resource_types": "exclusionByResourceTypes",
        "include_global_resource_types": "includeGlobalResourceTypes",
        "recording_strategy": "recordingStrategy",
        "resource_types": "resourceTypes",
    },
)
class ConfigConfigurationRecorderRecordingGroup:
    def __init__(
        self,
        *,
        all_supported: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclusion_by_resource_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        include_global_resource_types: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        recording_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ConfigConfigurationRecorderRecordingGroupRecordingStrategy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param all_supported: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#all_supported ConfigConfigurationRecorder#all_supported}.
        :param exclusion_by_resource_types: exclusion_by_resource_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#exclusion_by_resource_types ConfigConfigurationRecorder#exclusion_by_resource_types}
        :param include_global_resource_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#include_global_resource_types ConfigConfigurationRecorder#include_global_resource_types}.
        :param recording_strategy: recording_strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#recording_strategy ConfigConfigurationRecorder#recording_strategy}
        :param resource_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#resource_types ConfigConfigurationRecorder#resource_types}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f39aff10d1d33792f72ba5f13b532f6d7e711b0cf7c557a4218f0893b1282f8)
            check_type(argname="argument all_supported", value=all_supported, expected_type=type_hints["all_supported"])
            check_type(argname="argument exclusion_by_resource_types", value=exclusion_by_resource_types, expected_type=type_hints["exclusion_by_resource_types"])
            check_type(argname="argument include_global_resource_types", value=include_global_resource_types, expected_type=type_hints["include_global_resource_types"])
            check_type(argname="argument recording_strategy", value=recording_strategy, expected_type=type_hints["recording_strategy"])
            check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if all_supported is not None:
            self._values["all_supported"] = all_supported
        if exclusion_by_resource_types is not None:
            self._values["exclusion_by_resource_types"] = exclusion_by_resource_types
        if include_global_resource_types is not None:
            self._values["include_global_resource_types"] = include_global_resource_types
        if recording_strategy is not None:
            self._values["recording_strategy"] = recording_strategy
        if resource_types is not None:
            self._values["resource_types"] = resource_types

    @builtins.property
    def all_supported(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#all_supported ConfigConfigurationRecorder#all_supported}.'''
        result = self._values.get("all_supported")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def exclusion_by_resource_types(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypes"]]]:
        '''exclusion_by_resource_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#exclusion_by_resource_types ConfigConfigurationRecorder#exclusion_by_resource_types}
        '''
        result = self._values.get("exclusion_by_resource_types")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypes"]]], result)

    @builtins.property
    def include_global_resource_types(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#include_global_resource_types ConfigConfigurationRecorder#include_global_resource_types}.'''
        result = self._values.get("include_global_resource_types")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def recording_strategy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ConfigConfigurationRecorderRecordingGroupRecordingStrategy"]]]:
        '''recording_strategy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#recording_strategy ConfigConfigurationRecorder#recording_strategy}
        '''
        result = self._values.get("recording_strategy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ConfigConfigurationRecorderRecordingGroupRecordingStrategy"]]], result)

    @builtins.property
    def resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#resource_types ConfigConfigurationRecorder#resource_types}.'''
        result = self._values.get("resource_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConfigConfigurationRecorderRecordingGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.configConfigurationRecorder.ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypes",
    jsii_struct_bases=[],
    name_mapping={"resource_types": "resourceTypes"},
)
class ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypes:
    def __init__(
        self,
        *,
        resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param resource_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#resource_types ConfigConfigurationRecorder#resource_types}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f40f7f7c593b383255af714f30997e97c5c444e6205e4accfb80ad04924e948)
            check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_types is not None:
            self._values["resource_types"] = resource_types

    @builtins.property
    def resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#resource_types ConfigConfigurationRecorder#resource_types}.'''
        result = self._values.get("resource_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.configConfigurationRecorder.ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f35131e4101f84cf87d8038078af5ea91aa557641f8e20e92a2af0b82803c5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfd59c2e3eff40b115797c67c01ec10f0a9f8317c920e6c1bcfb2b61f48c756c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6739f3a108c89b446a2ee8815a283ed2cd94605de388560dbd8417449089f9b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66673bcec1728a1edeca95be463d0d67ddb9ffcec94f330d6c5ead0d3dce6ea7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1b34925113a8f20205e00996e3d32eb802bdace1c7b042d8827c06c2f3af79c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5d0926de86045a74e21111dcc7c7b8ccc035f691fa6d4c994881c3367a128b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.configConfigurationRecorder.ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84ebf97fe24f33d75fbf34b7eee683d77e0079200009b0a53ac68f4eab4c79a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetResourceTypes")
    def reset_resource_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceTypes", []))

    @builtins.property
    @jsii.member(jsii_name="resourceTypesInput")
    def resource_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypes")
    def resource_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceTypes"))

    @resource_types.setter
    def resource_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae037681c3c789d135ef9b0ee0b56cbd2d934a05194b03a1aa90f4bd8b39f8f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__053ecda8158c3ae4a596c52607bf200af2ee30dc3dc12e0c513931c0be04d25c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ConfigConfigurationRecorderRecordingGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.configConfigurationRecorder.ConfigConfigurationRecorderRecordingGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f28de3f8f3d85f915a2ee82f0d174e569b4a402346bdf9734a7f7f0210906441)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExclusionByResourceTypes")
    def put_exclusion_by_resource_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02fc097a9a147e2e5c8fa448be55d271091a91e9b058fcc3c262a9e5dfbe5526)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExclusionByResourceTypes", [value]))

    @jsii.member(jsii_name="putRecordingStrategy")
    def put_recording_strategy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ConfigConfigurationRecorderRecordingGroupRecordingStrategy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a1bdaa97fb8e1c5fa6c5df3e69c3b75db0ccbc1850c02a701dd6fa1fc9a5e45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRecordingStrategy", [value]))

    @jsii.member(jsii_name="resetAllSupported")
    def reset_all_supported(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllSupported", []))

    @jsii.member(jsii_name="resetExclusionByResourceTypes")
    def reset_exclusion_by_resource_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusionByResourceTypes", []))

    @jsii.member(jsii_name="resetIncludeGlobalResourceTypes")
    def reset_include_global_resource_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeGlobalResourceTypes", []))

    @jsii.member(jsii_name="resetRecordingStrategy")
    def reset_recording_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecordingStrategy", []))

    @jsii.member(jsii_name="resetResourceTypes")
    def reset_resource_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceTypes", []))

    @builtins.property
    @jsii.member(jsii_name="exclusionByResourceTypes")
    def exclusion_by_resource_types(
        self,
    ) -> ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypesList:
        return typing.cast(ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypesList, jsii.get(self, "exclusionByResourceTypes"))

    @builtins.property
    @jsii.member(jsii_name="recordingStrategy")
    def recording_strategy(
        self,
    ) -> "ConfigConfigurationRecorderRecordingGroupRecordingStrategyList":
        return typing.cast("ConfigConfigurationRecorderRecordingGroupRecordingStrategyList", jsii.get(self, "recordingStrategy"))

    @builtins.property
    @jsii.member(jsii_name="allSupportedInput")
    def all_supported_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allSupportedInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionByResourceTypesInput")
    def exclusion_by_resource_types_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypes]]], jsii.get(self, "exclusionByResourceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="includeGlobalResourceTypesInput")
    def include_global_resource_types_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeGlobalResourceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="recordingStrategyInput")
    def recording_strategy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ConfigConfigurationRecorderRecordingGroupRecordingStrategy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ConfigConfigurationRecorderRecordingGroupRecordingStrategy"]]], jsii.get(self, "recordingStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypesInput")
    def resource_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="allSupported")
    def all_supported(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allSupported"))

    @all_supported.setter
    def all_supported(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57537acdae7ffdbcceab507d497f5ba95d61f4ddf8e7598236848e81782c34e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allSupported", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeGlobalResourceTypes")
    def include_global_resource_types(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeGlobalResourceTypes"))

    @include_global_resource_types.setter
    def include_global_resource_types(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__345da09ed54577018b15352a595062795d7618e923650cefe76380ca20ac5a9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeGlobalResourceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceTypes")
    def resource_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceTypes"))

    @resource_types.setter
    def resource_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7571821817b7cad8cefa68bf50e76fde1c8726a74595f61c21c31f192000db27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ConfigConfigurationRecorderRecordingGroup]:
        return typing.cast(typing.Optional[ConfigConfigurationRecorderRecordingGroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConfigConfigurationRecorderRecordingGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40f3780f742838b789c3d46e66d65cdc983f3b5a22121461754af07c234b79b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.configConfigurationRecorder.ConfigConfigurationRecorderRecordingGroupRecordingStrategy",
    jsii_struct_bases=[],
    name_mapping={"use_only": "useOnly"},
)
class ConfigConfigurationRecorderRecordingGroupRecordingStrategy:
    def __init__(self, *, use_only: typing.Optional[builtins.str] = None) -> None:
        '''
        :param use_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#use_only ConfigConfigurationRecorder#use_only}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01e4e8cfa69912672e8fa67df67e266cdfbf11c791887eb8a2a61c64f89e0c0b)
            check_type(argname="argument use_only", value=use_only, expected_type=type_hints["use_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if use_only is not None:
            self._values["use_only"] = use_only

    @builtins.property
    def use_only(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#use_only ConfigConfigurationRecorder#use_only}.'''
        result = self._values.get("use_only")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConfigConfigurationRecorderRecordingGroupRecordingStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConfigConfigurationRecorderRecordingGroupRecordingStrategyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.configConfigurationRecorder.ConfigConfigurationRecorderRecordingGroupRecordingStrategyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2676b40632d8ea849bda495f495231f5acc7f88f1dc022e7aa9dfcf0d086e6f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ConfigConfigurationRecorderRecordingGroupRecordingStrategyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bbfe82e53233395e73e4df4007f3f4a8a06145a5422c37291d75ee77ce99978)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ConfigConfigurationRecorderRecordingGroupRecordingStrategyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc90aadf7444e70eb3eee1b0d6268d30e4ea7815d59183ee6b6837e4843c6a8e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5334ed86eb30193f55c279fa336ab494566d18e25e1f9aa8cac00d0a344688fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a790a6657d8ce18ce393c53b4caf2052f265b8cd2d9bbdf53b009551a23a3865)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ConfigConfigurationRecorderRecordingGroupRecordingStrategy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ConfigConfigurationRecorderRecordingGroupRecordingStrategy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ConfigConfigurationRecorderRecordingGroupRecordingStrategy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0627a346dc6bfcb7b271ea8df0ca8f7562f8e9322df8e162943f81f8644ce537)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ConfigConfigurationRecorderRecordingGroupRecordingStrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.configConfigurationRecorder.ConfigConfigurationRecorderRecordingGroupRecordingStrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ada19529a835e9fa4395d3c2ec1da2992f2c543faca0b156fc2321012dfa52a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetUseOnly")
    def reset_use_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseOnly", []))

    @builtins.property
    @jsii.member(jsii_name="useOnlyInput")
    def use_only_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "useOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="useOnly")
    def use_only(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "useOnly"))

    @use_only.setter
    def use_only(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42059662f72fc3422b8274f54c601f5770378d9b087fe7b8309567df6c1bdb1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ConfigConfigurationRecorderRecordingGroupRecordingStrategy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ConfigConfigurationRecorderRecordingGroupRecordingStrategy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ConfigConfigurationRecorderRecordingGroupRecordingStrategy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3516eeea4e75ecba12aec1fd12ac708c02f25ace676c230ff41534e6c7940e15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.configConfigurationRecorder.ConfigConfigurationRecorderRecordingMode",
    jsii_struct_bases=[],
    name_mapping={
        "recording_frequency": "recordingFrequency",
        "recording_mode_override": "recordingModeOverride",
    },
)
class ConfigConfigurationRecorderRecordingMode:
    def __init__(
        self,
        *,
        recording_frequency: typing.Optional[builtins.str] = None,
        recording_mode_override: typing.Optional[typing.Union["ConfigConfigurationRecorderRecordingModeRecordingModeOverride", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param recording_frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#recording_frequency ConfigConfigurationRecorder#recording_frequency}.
        :param recording_mode_override: recording_mode_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#recording_mode_override ConfigConfigurationRecorder#recording_mode_override}
        '''
        if isinstance(recording_mode_override, dict):
            recording_mode_override = ConfigConfigurationRecorderRecordingModeRecordingModeOverride(**recording_mode_override)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3951103ccc60fecadd48400229cd8b3e52c3c4918abf7aa0b5a8ab77c3ca9a40)
            check_type(argname="argument recording_frequency", value=recording_frequency, expected_type=type_hints["recording_frequency"])
            check_type(argname="argument recording_mode_override", value=recording_mode_override, expected_type=type_hints["recording_mode_override"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if recording_frequency is not None:
            self._values["recording_frequency"] = recording_frequency
        if recording_mode_override is not None:
            self._values["recording_mode_override"] = recording_mode_override

    @builtins.property
    def recording_frequency(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#recording_frequency ConfigConfigurationRecorder#recording_frequency}.'''
        result = self._values.get("recording_frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recording_mode_override(
        self,
    ) -> typing.Optional["ConfigConfigurationRecorderRecordingModeRecordingModeOverride"]:
        '''recording_mode_override block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#recording_mode_override ConfigConfigurationRecorder#recording_mode_override}
        '''
        result = self._values.get("recording_mode_override")
        return typing.cast(typing.Optional["ConfigConfigurationRecorderRecordingModeRecordingModeOverride"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConfigConfigurationRecorderRecordingMode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConfigConfigurationRecorderRecordingModeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.configConfigurationRecorder.ConfigConfigurationRecorderRecordingModeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ee12e8b9d12b8d9c00d88a8eb2a951f76234769591576373c8ce56906f35225)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRecordingModeOverride")
    def put_recording_mode_override(
        self,
        *,
        recording_frequency: builtins.str,
        resource_types: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param recording_frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#recording_frequency ConfigConfigurationRecorder#recording_frequency}.
        :param resource_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#resource_types ConfigConfigurationRecorder#resource_types}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#description ConfigConfigurationRecorder#description}.
        '''
        value = ConfigConfigurationRecorderRecordingModeRecordingModeOverride(
            recording_frequency=recording_frequency,
            resource_types=resource_types,
            description=description,
        )

        return typing.cast(None, jsii.invoke(self, "putRecordingModeOverride", [value]))

    @jsii.member(jsii_name="resetRecordingFrequency")
    def reset_recording_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecordingFrequency", []))

    @jsii.member(jsii_name="resetRecordingModeOverride")
    def reset_recording_mode_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecordingModeOverride", []))

    @builtins.property
    @jsii.member(jsii_name="recordingModeOverride")
    def recording_mode_override(
        self,
    ) -> "ConfigConfigurationRecorderRecordingModeRecordingModeOverrideOutputReference":
        return typing.cast("ConfigConfigurationRecorderRecordingModeRecordingModeOverrideOutputReference", jsii.get(self, "recordingModeOverride"))

    @builtins.property
    @jsii.member(jsii_name="recordingFrequencyInput")
    def recording_frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordingFrequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="recordingModeOverrideInput")
    def recording_mode_override_input(
        self,
    ) -> typing.Optional["ConfigConfigurationRecorderRecordingModeRecordingModeOverride"]:
        return typing.cast(typing.Optional["ConfigConfigurationRecorderRecordingModeRecordingModeOverride"], jsii.get(self, "recordingModeOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="recordingFrequency")
    def recording_frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordingFrequency"))

    @recording_frequency.setter
    def recording_frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70140bdeb30e3526b6fd78463d501a9ef5df3e18434273c922ded2edb1516579)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordingFrequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ConfigConfigurationRecorderRecordingMode]:
        return typing.cast(typing.Optional[ConfigConfigurationRecorderRecordingMode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConfigConfigurationRecorderRecordingMode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abab5623ff60a8cd959f8f554bec77c60f7393afd427d9a65a7b1f67d927955c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.configConfigurationRecorder.ConfigConfigurationRecorderRecordingModeRecordingModeOverride",
    jsii_struct_bases=[],
    name_mapping={
        "recording_frequency": "recordingFrequency",
        "resource_types": "resourceTypes",
        "description": "description",
    },
)
class ConfigConfigurationRecorderRecordingModeRecordingModeOverride:
    def __init__(
        self,
        *,
        recording_frequency: builtins.str,
        resource_types: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param recording_frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#recording_frequency ConfigConfigurationRecorder#recording_frequency}.
        :param resource_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#resource_types ConfigConfigurationRecorder#resource_types}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#description ConfigConfigurationRecorder#description}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de5e3998ca0e2b15f809dd8c32395031bac1f279acc2db7e1d1cd5e38948f9be)
            check_type(argname="argument recording_frequency", value=recording_frequency, expected_type=type_hints["recording_frequency"])
            check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "recording_frequency": recording_frequency,
            "resource_types": resource_types,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def recording_frequency(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#recording_frequency ConfigConfigurationRecorder#recording_frequency}.'''
        result = self._values.get("recording_frequency")
        assert result is not None, "Required property 'recording_frequency' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_types(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#resource_types ConfigConfigurationRecorder#resource_types}.'''
        result = self._values.get("resource_types")
        assert result is not None, "Required property 'resource_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/config_configuration_recorder#description ConfigConfigurationRecorder#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConfigConfigurationRecorderRecordingModeRecordingModeOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConfigConfigurationRecorderRecordingModeRecordingModeOverrideOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.configConfigurationRecorder.ConfigConfigurationRecorderRecordingModeRecordingModeOverrideOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a31c1c26d4156160043ea4859a8b9e701baa67b95a4d988671ccbf2d36210979)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="recordingFrequencyInput")
    def recording_frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordingFrequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypesInput")
    def resource_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a877bd5c946d4f679cc1b5af7ea1b2263046acf181e3ae1f1053f14dd020a70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recordingFrequency")
    def recording_frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordingFrequency"))

    @recording_frequency.setter
    def recording_frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e73e795b1c1c47be88cd7332cac69e24b05efd5889fa3bdf9b8e88b5e53ee74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordingFrequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceTypes")
    def resource_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceTypes"))

    @resource_types.setter
    def resource_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a570fb145d1ab3f3d7455e2fd15df7e5597372c8efc43d51006989c6d37e93a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ConfigConfigurationRecorderRecordingModeRecordingModeOverride]:
        return typing.cast(typing.Optional[ConfigConfigurationRecorderRecordingModeRecordingModeOverride], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConfigConfigurationRecorderRecordingModeRecordingModeOverride],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5019f36dd709b8020f5b55ae9d4b55eb5e1f2bc74f9f9ca72c461dffa0456d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ConfigConfigurationRecorder",
    "ConfigConfigurationRecorderConfig",
    "ConfigConfigurationRecorderRecordingGroup",
    "ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypes",
    "ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypesList",
    "ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypesOutputReference",
    "ConfigConfigurationRecorderRecordingGroupOutputReference",
    "ConfigConfigurationRecorderRecordingGroupRecordingStrategy",
    "ConfigConfigurationRecorderRecordingGroupRecordingStrategyList",
    "ConfigConfigurationRecorderRecordingGroupRecordingStrategyOutputReference",
    "ConfigConfigurationRecorderRecordingMode",
    "ConfigConfigurationRecorderRecordingModeOutputReference",
    "ConfigConfigurationRecorderRecordingModeRecordingModeOverride",
    "ConfigConfigurationRecorderRecordingModeRecordingModeOverrideOutputReference",
]

publication.publish()

def _typecheckingstub__c2841188513eb315ed250afbfee2a4f5083c21b5faae6754a25cfc7d915cd811(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    role_arn: builtins.str,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    recording_group: typing.Optional[typing.Union[ConfigConfigurationRecorderRecordingGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    recording_mode: typing.Optional[typing.Union[ConfigConfigurationRecorderRecordingMode, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c0b136d7d0a0076655f8e7b04f73870f35fc46291065f4f39e5679a9dab3eb17(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a84a7ea446d3e7f1896fc1e577520fdb566557030e0c1bdb363f06dad22ceca2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__429385fdfe98e49321bf0a8730d312fe8e2a7b1c403ff1debb56252c2ab5e135(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__537cf897d3b8d3869cef524733467375011f74f83f9ffcad0ec1a83c7ec8a681(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81e04e5eee3181224f2992bb9a20f58e528256c64e21fa1945f8491592a72711(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    role_arn: builtins.str,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    recording_group: typing.Optional[typing.Union[ConfigConfigurationRecorderRecordingGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    recording_mode: typing.Optional[typing.Union[ConfigConfigurationRecorderRecordingMode, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f39aff10d1d33792f72ba5f13b532f6d7e711b0cf7c557a4218f0893b1282f8(
    *,
    all_supported: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exclusion_by_resource_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    include_global_resource_types: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    recording_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ConfigConfigurationRecorderRecordingGroupRecordingStrategy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f40f7f7c593b383255af714f30997e97c5c444e6205e4accfb80ad04924e948(
    *,
    resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f35131e4101f84cf87d8038078af5ea91aa557641f8e20e92a2af0b82803c5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfd59c2e3eff40b115797c67c01ec10f0a9f8317c920e6c1bcfb2b61f48c756c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6739f3a108c89b446a2ee8815a283ed2cd94605de388560dbd8417449089f9b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66673bcec1728a1edeca95be463d0d67ddb9ffcec94f330d6c5ead0d3dce6ea7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1b34925113a8f20205e00996e3d32eb802bdace1c7b042d8827c06c2f3af79c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d0926de86045a74e21111dcc7c7b8ccc035f691fa6d4c994881c3367a128b3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ebf97fe24f33d75fbf34b7eee683d77e0079200009b0a53ac68f4eab4c79a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae037681c3c789d135ef9b0ee0b56cbd2d934a05194b03a1aa90f4bd8b39f8f0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__053ecda8158c3ae4a596c52607bf200af2ee30dc3dc12e0c513931c0be04d25c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f28de3f8f3d85f915a2ee82f0d174e569b4a402346bdf9734a7f7f0210906441(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02fc097a9a147e2e5c8fa448be55d271091a91e9b058fcc3c262a9e5dfbe5526(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ConfigConfigurationRecorderRecordingGroupExclusionByResourceTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a1bdaa97fb8e1c5fa6c5df3e69c3b75db0ccbc1850c02a701dd6fa1fc9a5e45(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ConfigConfigurationRecorderRecordingGroupRecordingStrategy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57537acdae7ffdbcceab507d497f5ba95d61f4ddf8e7598236848e81782c34e5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__345da09ed54577018b15352a595062795d7618e923650cefe76380ca20ac5a9d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7571821817b7cad8cefa68bf50e76fde1c8726a74595f61c21c31f192000db27(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f3780f742838b789c3d46e66d65cdc983f3b5a22121461754af07c234b79b3(
    value: typing.Optional[ConfigConfigurationRecorderRecordingGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01e4e8cfa69912672e8fa67df67e266cdfbf11c791887eb8a2a61c64f89e0c0b(
    *,
    use_only: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2676b40632d8ea849bda495f495231f5acc7f88f1dc022e7aa9dfcf0d086e6f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bbfe82e53233395e73e4df4007f3f4a8a06145a5422c37291d75ee77ce99978(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc90aadf7444e70eb3eee1b0d6268d30e4ea7815d59183ee6b6837e4843c6a8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5334ed86eb30193f55c279fa336ab494566d18e25e1f9aa8cac00d0a344688fe(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a790a6657d8ce18ce393c53b4caf2052f265b8cd2d9bbdf53b009551a23a3865(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0627a346dc6bfcb7b271ea8df0ca8f7562f8e9322df8e162943f81f8644ce537(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ConfigConfigurationRecorderRecordingGroupRecordingStrategy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ada19529a835e9fa4395d3c2ec1da2992f2c543faca0b156fc2321012dfa52a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42059662f72fc3422b8274f54c601f5770378d9b087fe7b8309567df6c1bdb1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3516eeea4e75ecba12aec1fd12ac708c02f25ace676c230ff41534e6c7940e15(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ConfigConfigurationRecorderRecordingGroupRecordingStrategy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3951103ccc60fecadd48400229cd8b3e52c3c4918abf7aa0b5a8ab77c3ca9a40(
    *,
    recording_frequency: typing.Optional[builtins.str] = None,
    recording_mode_override: typing.Optional[typing.Union[ConfigConfigurationRecorderRecordingModeRecordingModeOverride, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee12e8b9d12b8d9c00d88a8eb2a951f76234769591576373c8ce56906f35225(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70140bdeb30e3526b6fd78463d501a9ef5df3e18434273c922ded2edb1516579(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abab5623ff60a8cd959f8f554bec77c60f7393afd427d9a65a7b1f67d927955c(
    value: typing.Optional[ConfigConfigurationRecorderRecordingMode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de5e3998ca0e2b15f809dd8c32395031bac1f279acc2db7e1d1cd5e38948f9be(
    *,
    recording_frequency: builtins.str,
    resource_types: typing.Sequence[builtins.str],
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31c1c26d4156160043ea4859a8b9e701baa67b95a4d988671ccbf2d36210979(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a877bd5c946d4f679cc1b5af7ea1b2263046acf181e3ae1f1053f14dd020a70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e73e795b1c1c47be88cd7332cac69e24b05efd5889fa3bdf9b8e88b5e53ee74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a570fb145d1ab3f3d7455e2fd15df7e5597372c8efc43d51006989c6d37e93a0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5019f36dd709b8020f5b55ae9d4b55eb5e1f2bc74f9f9ca72c461dffa0456d8(
    value: typing.Optional[ConfigConfigurationRecorderRecordingModeRecordingModeOverride],
) -> None:
    """Type checking stubs"""
    pass
