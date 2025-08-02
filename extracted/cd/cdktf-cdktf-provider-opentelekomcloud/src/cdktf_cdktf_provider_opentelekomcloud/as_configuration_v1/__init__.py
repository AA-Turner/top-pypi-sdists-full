r'''
# `opentelekomcloud_as_configuration_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_as_configuration_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1).
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


class AsConfigurationV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asConfigurationV1.AsConfigurationV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1 opentelekomcloud_as_configuration_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        instance_config: typing.Union["AsConfigurationV1InstanceConfig", typing.Dict[builtins.str, typing.Any]],
        scaling_configuration_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1 opentelekomcloud_as_configuration_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param instance_config: instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#instance_config AsConfigurationV1#instance_config}
        :param scaling_configuration_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#scaling_configuration_name AsConfigurationV1#scaling_configuration_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#id AsConfigurationV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#region AsConfigurationV1#region}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d2b9a449f242f99971494dcdccc59881dbc019ac771d916d7a7c27b893d60f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AsConfigurationV1Config(
            instance_config=instance_config,
            scaling_configuration_name=scaling_configuration_name,
            id=id,
            region=region,
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
        '''Generates CDKTF code for importing a AsConfigurationV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AsConfigurationV1 to import.
        :param import_from_id: The id of the existing AsConfigurationV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AsConfigurationV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a614e0b940bf8405c59e4eaefe6be5d633c3042ccb479f8cf07808360c10650b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putInstanceConfig")
    def put_instance_config(
        self,
        *,
        key_name: builtins.str,
        disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AsConfigurationV1InstanceConfigDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        flavor: typing.Optional[builtins.str] = None,
        image: typing.Optional[builtins.str] = None,
        instance_id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        personality: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AsConfigurationV1InstanceConfigPersonality", typing.Dict[builtins.str, typing.Any]]]]] = None,
        public_ip: typing.Optional[typing.Union["AsConfigurationV1InstanceConfigPublicIp", typing.Dict[builtins.str, typing.Any]]] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_data: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#key_name AsConfigurationV1#key_name}.
        :param disk: disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#disk AsConfigurationV1#disk}
        :param flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#flavor AsConfigurationV1#flavor}.
        :param image: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#image AsConfigurationV1#image}.
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#instance_id AsConfigurationV1#instance_id}.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#metadata AsConfigurationV1#metadata}.
        :param personality: personality block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#personality AsConfigurationV1#personality}
        :param public_ip: public_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#public_ip AsConfigurationV1#public_ip}
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#security_groups AsConfigurationV1#security_groups}.
        :param user_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#user_data AsConfigurationV1#user_data}.
        '''
        value = AsConfigurationV1InstanceConfig(
            key_name=key_name,
            disk=disk,
            flavor=flavor,
            image=image,
            instance_id=instance_id,
            metadata=metadata,
            personality=personality,
            public_ip=public_ip,
            security_groups=security_groups,
            user_data=user_data,
        )

        return typing.cast(None, jsii.invoke(self, "putInstanceConfig", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

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
    @jsii.member(jsii_name="instanceConfig")
    def instance_config(self) -> "AsConfigurationV1InstanceConfigOutputReference":
        return typing.cast("AsConfigurationV1InstanceConfigOutputReference", jsii.get(self, "instanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceConfigInput")
    def instance_config_input(
        self,
    ) -> typing.Optional["AsConfigurationV1InstanceConfig"]:
        return typing.cast(typing.Optional["AsConfigurationV1InstanceConfig"], jsii.get(self, "instanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingConfigurationNameInput")
    def scaling_configuration_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalingConfigurationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__612fe2f7af0e0649daec341a04cee624aa4be1f0aa0181ff6771a8dc86de4576)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__512535eff4340271062eac01cf7b5f1ef5ad3eb18fdd955e411ccafb8f62da1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scalingConfigurationName")
    def scaling_configuration_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingConfigurationName"))

    @scaling_configuration_name.setter
    def scaling_configuration_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cb03179bbbd3b9e681ab0efff910c31264c9cc3649596f7daf7959138e16a85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingConfigurationName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asConfigurationV1.AsConfigurationV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "instance_config": "instanceConfig",
        "scaling_configuration_name": "scalingConfigurationName",
        "id": "id",
        "region": "region",
    },
)
class AsConfigurationV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        instance_config: typing.Union["AsConfigurationV1InstanceConfig", typing.Dict[builtins.str, typing.Any]],
        scaling_configuration_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param instance_config: instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#instance_config AsConfigurationV1#instance_config}
        :param scaling_configuration_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#scaling_configuration_name AsConfigurationV1#scaling_configuration_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#id AsConfigurationV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#region AsConfigurationV1#region}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(instance_config, dict):
            instance_config = AsConfigurationV1InstanceConfig(**instance_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f73362da314007b75d90718bb4119d1a69b229ebf75d8422a66cc611bba6d6c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument instance_config", value=instance_config, expected_type=type_hints["instance_config"])
            check_type(argname="argument scaling_configuration_name", value=scaling_configuration_name, expected_type=type_hints["scaling_configuration_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_config": instance_config,
            "scaling_configuration_name": scaling_configuration_name,
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
        if region is not None:
            self._values["region"] = region

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
    def instance_config(self) -> "AsConfigurationV1InstanceConfig":
        '''instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#instance_config AsConfigurationV1#instance_config}
        '''
        result = self._values.get("instance_config")
        assert result is not None, "Required property 'instance_config' is missing"
        return typing.cast("AsConfigurationV1InstanceConfig", result)

    @builtins.property
    def scaling_configuration_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#scaling_configuration_name AsConfigurationV1#scaling_configuration_name}.'''
        result = self._values.get("scaling_configuration_name")
        assert result is not None, "Required property 'scaling_configuration_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#id AsConfigurationV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#region AsConfigurationV1#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsConfigurationV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asConfigurationV1.AsConfigurationV1InstanceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "key_name": "keyName",
        "disk": "disk",
        "flavor": "flavor",
        "image": "image",
        "instance_id": "instanceId",
        "metadata": "metadata",
        "personality": "personality",
        "public_ip": "publicIp",
        "security_groups": "securityGroups",
        "user_data": "userData",
    },
)
class AsConfigurationV1InstanceConfig:
    def __init__(
        self,
        *,
        key_name: builtins.str,
        disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AsConfigurationV1InstanceConfigDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        flavor: typing.Optional[builtins.str] = None,
        image: typing.Optional[builtins.str] = None,
        instance_id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        personality: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AsConfigurationV1InstanceConfigPersonality", typing.Dict[builtins.str, typing.Any]]]]] = None,
        public_ip: typing.Optional[typing.Union["AsConfigurationV1InstanceConfigPublicIp", typing.Dict[builtins.str, typing.Any]]] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_data: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#key_name AsConfigurationV1#key_name}.
        :param disk: disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#disk AsConfigurationV1#disk}
        :param flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#flavor AsConfigurationV1#flavor}.
        :param image: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#image AsConfigurationV1#image}.
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#instance_id AsConfigurationV1#instance_id}.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#metadata AsConfigurationV1#metadata}.
        :param personality: personality block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#personality AsConfigurationV1#personality}
        :param public_ip: public_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#public_ip AsConfigurationV1#public_ip}
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#security_groups AsConfigurationV1#security_groups}.
        :param user_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#user_data AsConfigurationV1#user_data}.
        '''
        if isinstance(public_ip, dict):
            public_ip = AsConfigurationV1InstanceConfigPublicIp(**public_ip)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f33ed89ab3a969744b14fb646058ebd01c62cecf2db6b20b94a0051bbe2fe83)
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument disk", value=disk, expected_type=type_hints["disk"])
            check_type(argname="argument flavor", value=flavor, expected_type=type_hints["flavor"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument personality", value=personality, expected_type=type_hints["personality"])
            check_type(argname="argument public_ip", value=public_ip, expected_type=type_hints["public_ip"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_name": key_name,
        }
        if disk is not None:
            self._values["disk"] = disk
        if flavor is not None:
            self._values["flavor"] = flavor
        if image is not None:
            self._values["image"] = image
        if instance_id is not None:
            self._values["instance_id"] = instance_id
        if metadata is not None:
            self._values["metadata"] = metadata
        if personality is not None:
            self._values["personality"] = personality
        if public_ip is not None:
            self._values["public_ip"] = public_ip
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if user_data is not None:
            self._values["user_data"] = user_data

    @builtins.property
    def key_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#key_name AsConfigurationV1#key_name}.'''
        result = self._values.get("key_name")
        assert result is not None, "Required property 'key_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disk(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AsConfigurationV1InstanceConfigDisk"]]]:
        '''disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#disk AsConfigurationV1#disk}
        '''
        result = self._values.get("disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AsConfigurationV1InstanceConfigDisk"]]], result)

    @builtins.property
    def flavor(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#flavor AsConfigurationV1#flavor}.'''
        result = self._values.get("flavor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#image AsConfigurationV1#image}.'''
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#instance_id AsConfigurationV1#instance_id}.'''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#metadata AsConfigurationV1#metadata}.'''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def personality(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AsConfigurationV1InstanceConfigPersonality"]]]:
        '''personality block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#personality AsConfigurationV1#personality}
        '''
        result = self._values.get("personality")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AsConfigurationV1InstanceConfigPersonality"]]], result)

    @builtins.property
    def public_ip(self) -> typing.Optional["AsConfigurationV1InstanceConfigPublicIp"]:
        '''public_ip block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#public_ip AsConfigurationV1#public_ip}
        '''
        result = self._values.get("public_ip")
        return typing.cast(typing.Optional["AsConfigurationV1InstanceConfigPublicIp"], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#security_groups AsConfigurationV1#security_groups}.'''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_data(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#user_data AsConfigurationV1#user_data}.'''
        result = self._values.get("user_data")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsConfigurationV1InstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asConfigurationV1.AsConfigurationV1InstanceConfigDisk",
    jsii_struct_bases=[],
    name_mapping={
        "disk_type": "diskType",
        "size": "size",
        "volume_type": "volumeType",
        "kms_id": "kmsId",
    },
)
class AsConfigurationV1InstanceConfigDisk:
    def __init__(
        self,
        *,
        disk_type: builtins.str,
        size: jsii.Number,
        volume_type: builtins.str,
        kms_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#disk_type AsConfigurationV1#disk_type}.
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#size AsConfigurationV1#size}.
        :param volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#volume_type AsConfigurationV1#volume_type}.
        :param kms_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#kms_id AsConfigurationV1#kms_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e695d640c13ec4082b1158a53057096e8069e895c0ad84bd6bdd6008d240b0cc)
            check_type(argname="argument disk_type", value=disk_type, expected_type=type_hints["disk_type"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
            check_type(argname="argument kms_id", value=kms_id, expected_type=type_hints["kms_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disk_type": disk_type,
            "size": size,
            "volume_type": volume_type,
        }
        if kms_id is not None:
            self._values["kms_id"] = kms_id

    @builtins.property
    def disk_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#disk_type AsConfigurationV1#disk_type}.'''
        result = self._values.get("disk_type")
        assert result is not None, "Required property 'disk_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#size AsConfigurationV1#size}.'''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def volume_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#volume_type AsConfigurationV1#volume_type}.'''
        result = self._values.get("volume_type")
        assert result is not None, "Required property 'volume_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#kms_id AsConfigurationV1#kms_id}.'''
        result = self._values.get("kms_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsConfigurationV1InstanceConfigDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AsConfigurationV1InstanceConfigDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asConfigurationV1.AsConfigurationV1InstanceConfigDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d7cd43f44e1dd70094b6a630b872888aa70dcda54522e78a30249e283eb97bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AsConfigurationV1InstanceConfigDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__967b4df55a9018c4549b28902390ebd50391c86a6c9d329696c8b3c18432f681)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AsConfigurationV1InstanceConfigDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f14a936c2b66a9c25883cc1d5205e040b033af8af139fc3737db7ed73d34cba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c99564ce75bd9ff1fe3ff5303c87bc3e7846ac1dfd677f3aaf4368b8f674bdc9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfbb6206642047905d568052d33abe7209c895d7b3ac20675221457720355a18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsConfigurationV1InstanceConfigDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsConfigurationV1InstanceConfigDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsConfigurationV1InstanceConfigDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__263331334a5328b641bf0d1d7c689e1c3a6e86491677c2d0ab8b590a0394567b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AsConfigurationV1InstanceConfigDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asConfigurationV1.AsConfigurationV1InstanceConfigDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a41b3465f25b3fb41380957d2e42026bcc2cda5374550e86dfc9ad73789e959)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKmsId")
    def reset_kms_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsId", []))

    @builtins.property
    @jsii.member(jsii_name="diskTypeInput")
    def disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsIdInput")
    def kms_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeTypeInput")
    def volume_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="diskType")
    def disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskType"))

    @disk_type.setter
    def disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a9e39cccc9827f0937f4f67390d04d7319bc32ebec843b39c0947da04d9ad4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsId")
    def kms_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsId"))

    @kms_id.setter
    def kms_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea2f02692cf81a1186ef2d555d814815d3208fa1a962d2507c3966a1820b42b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b31533da30e83a5a46c22ec0a170f923e69dce03a2e0eb8e55a7e28078b0d73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeType")
    def volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeType"))

    @volume_type.setter
    def volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397af872483c952e7f4949307ea15b298b891cdda2021725f3cf4daaae985097)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsConfigurationV1InstanceConfigDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsConfigurationV1InstanceConfigDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsConfigurationV1InstanceConfigDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8825ae411f7143d99cea031b60030e6e7f8f0d12006e2297e5a34061b9df2044)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AsConfigurationV1InstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asConfigurationV1.AsConfigurationV1InstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8adafa2b40c4d592f7a400babe8318b528519f7ff49eaddd60557dce4e24361)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDisk")
    def put_disk(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AsConfigurationV1InstanceConfigDisk, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__457723c4ea7ede38789b82bbe58f06de9a1a3e82b094b92b220dcbe0e764d267)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDisk", [value]))

    @jsii.member(jsii_name="putPersonality")
    def put_personality(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AsConfigurationV1InstanceConfigPersonality", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c4f0e693929517fcdbb839dd9e91b306969b37bc0616b13d190f21e61314afe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPersonality", [value]))

    @jsii.member(jsii_name="putPublicIp")
    def put_public_ip(
        self,
        *,
        eip: typing.Union["AsConfigurationV1InstanceConfigPublicIpEip", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param eip: eip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#eip AsConfigurationV1#eip}
        '''
        value = AsConfigurationV1InstanceConfigPublicIp(eip=eip)

        return typing.cast(None, jsii.invoke(self, "putPublicIp", [value]))

    @jsii.member(jsii_name="resetDisk")
    def reset_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisk", []))

    @jsii.member(jsii_name="resetFlavor")
    def reset_flavor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlavor", []))

    @jsii.member(jsii_name="resetImage")
    def reset_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImage", []))

    @jsii.member(jsii_name="resetInstanceId")
    def reset_instance_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceId", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetPersonality")
    def reset_personality(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPersonality", []))

    @jsii.member(jsii_name="resetPublicIp")
    def reset_public_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicIp", []))

    @jsii.member(jsii_name="resetSecurityGroups")
    def reset_security_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroups", []))

    @jsii.member(jsii_name="resetUserData")
    def reset_user_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserData", []))

    @builtins.property
    @jsii.member(jsii_name="disk")
    def disk(self) -> AsConfigurationV1InstanceConfigDiskList:
        return typing.cast(AsConfigurationV1InstanceConfigDiskList, jsii.get(self, "disk"))

    @builtins.property
    @jsii.member(jsii_name="personality")
    def personality(self) -> "AsConfigurationV1InstanceConfigPersonalityList":
        return typing.cast("AsConfigurationV1InstanceConfigPersonalityList", jsii.get(self, "personality"))

    @builtins.property
    @jsii.member(jsii_name="publicIp")
    def public_ip(self) -> "AsConfigurationV1InstanceConfigPublicIpOutputReference":
        return typing.cast("AsConfigurationV1InstanceConfigPublicIpOutputReference", jsii.get(self, "publicIp"))

    @builtins.property
    @jsii.member(jsii_name="diskInput")
    def disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsConfigurationV1InstanceConfigDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsConfigurationV1InstanceConfigDisk]]], jsii.get(self, "diskInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorInput")
    def flavor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdInput")
    def instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyNameInput")
    def key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="personalityInput")
    def personality_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AsConfigurationV1InstanceConfigPersonality"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AsConfigurationV1InstanceConfigPersonality"]]], jsii.get(self, "personalityInput"))

    @builtins.property
    @jsii.member(jsii_name="publicIpInput")
    def public_ip_input(
        self,
    ) -> typing.Optional["AsConfigurationV1InstanceConfigPublicIp"]:
        return typing.cast(typing.Optional["AsConfigurationV1InstanceConfigPublicIp"], jsii.get(self, "publicIpInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupsInput")
    def security_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="userDataInput")
    def user_data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userDataInput"))

    @builtins.property
    @jsii.member(jsii_name="flavor")
    def flavor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavor"))

    @flavor.setter
    def flavor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97512337487f92e81a33bba160fb0aa20e7869bb049a0d3c353f195d563b0e48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__834184d9039614301036f898661cccaa2482302a1800d75a2f23bb9ab42817dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a74a0b3dffa910bbb8cedf388a8e6cef28734f2e2e02550e02a5635df38dbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyName")
    def key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyName"))

    @key_name.setter
    def key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb57bebba073dacb0bc357c9f5212dfcc1cc8ebcdf186946edb0cc50bd61434)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e19f77ad8f76806900e599a33a70ed16e8d572e21f0fc01d499985acea69de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroups"))

    @security_groups.setter
    def security_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfde9fce5752de5fb9dbd1cdb7dc2dd7d8728c2cceecd33d68bbb54fab16f445)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userData")
    def user_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userData"))

    @user_data.setter
    def user_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a2cb2fcf41b4428c43535544ffcb3a26517cf920523bac575316ab5c6cd6c55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AsConfigurationV1InstanceConfig]:
        return typing.cast(typing.Optional[AsConfigurationV1InstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AsConfigurationV1InstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2938f883077a98a180cdc658ec69f964d9c5105240c0ec296297dad76241a10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asConfigurationV1.AsConfigurationV1InstanceConfigPersonality",
    jsii_struct_bases=[],
    name_mapping={"content": "content", "path": "path"},
)
class AsConfigurationV1InstanceConfigPersonality:
    def __init__(self, *, content: builtins.str, path: builtins.str) -> None:
        '''
        :param content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#content AsConfigurationV1#content}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#path AsConfigurationV1#path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__422080c6dcba79b6aec12e50cf1ed422b1bab2442b5e6bc24b1726c198a724eb)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "path": path,
        }

    @builtins.property
    def content(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#content AsConfigurationV1#content}.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#path AsConfigurationV1#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsConfigurationV1InstanceConfigPersonality(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AsConfigurationV1InstanceConfigPersonalityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asConfigurationV1.AsConfigurationV1InstanceConfigPersonalityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cd9a08b1a6668c3a0ceda591329305ad38693157cd5bfd5a467ce0c36d5cf5e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AsConfigurationV1InstanceConfigPersonalityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bbf518a77ef15ce65cca517511b65af013bbbedaa453a3a6bb423e5c3a34632)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AsConfigurationV1InstanceConfigPersonalityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0f6d1be3ebef9123c8f075aa29b3a89387538aebe5bc2c59dc5a379664f58e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b13dfdac6de15993b26d15d380a40c013db55938d5b6e5574099256c09541502)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ed12e7e00be16fa2aa40d49f8baf33ec57fee4763fbb9c3bfd4dbf3d921b4f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsConfigurationV1InstanceConfigPersonality]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsConfigurationV1InstanceConfigPersonality]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsConfigurationV1InstanceConfigPersonality]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fcb673a70b0b1644ef316437eb5a568c41b7aec36e69661deee8dfe60d5ad6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AsConfigurationV1InstanceConfigPersonalityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asConfigurationV1.AsConfigurationV1InstanceConfigPersonalityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e90701aa99aa1f31ba5a073c41e393c7610eafd77bd95e96961b0b18e40e9a91)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05b566333f0eec6082d24d90d91b26810e574e85416725d9c9f62123c43ac0d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbbe9a72c6ad79b5c2ef1320f5e7eb50aed43752c1699a0206f0b101b0bdb0a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsConfigurationV1InstanceConfigPersonality]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsConfigurationV1InstanceConfigPersonality]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsConfigurationV1InstanceConfigPersonality]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0193fbb6666710c14d6ce9e726a4cf1e1051930a3ca71bdcf3db880ddf3ea73c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asConfigurationV1.AsConfigurationV1InstanceConfigPublicIp",
    jsii_struct_bases=[],
    name_mapping={"eip": "eip"},
)
class AsConfigurationV1InstanceConfigPublicIp:
    def __init__(
        self,
        *,
        eip: typing.Union["AsConfigurationV1InstanceConfigPublicIpEip", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param eip: eip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#eip AsConfigurationV1#eip}
        '''
        if isinstance(eip, dict):
            eip = AsConfigurationV1InstanceConfigPublicIpEip(**eip)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccb95c8219058fe2e1d075854c4cefdd3939f56c0a883dd0ded0696ce639e79f)
            check_type(argname="argument eip", value=eip, expected_type=type_hints["eip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "eip": eip,
        }

    @builtins.property
    def eip(self) -> "AsConfigurationV1InstanceConfigPublicIpEip":
        '''eip block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#eip AsConfigurationV1#eip}
        '''
        result = self._values.get("eip")
        assert result is not None, "Required property 'eip' is missing"
        return typing.cast("AsConfigurationV1InstanceConfigPublicIpEip", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsConfigurationV1InstanceConfigPublicIp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asConfigurationV1.AsConfigurationV1InstanceConfigPublicIpEip",
    jsii_struct_bases=[],
    name_mapping={"bandwidth": "bandwidth", "ip_type": "ipType"},
)
class AsConfigurationV1InstanceConfigPublicIpEip:
    def __init__(
        self,
        *,
        bandwidth: typing.Union["AsConfigurationV1InstanceConfigPublicIpEipBandwidth", typing.Dict[builtins.str, typing.Any]],
        ip_type: builtins.str,
    ) -> None:
        '''
        :param bandwidth: bandwidth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#bandwidth AsConfigurationV1#bandwidth}
        :param ip_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#ip_type AsConfigurationV1#ip_type}.
        '''
        if isinstance(bandwidth, dict):
            bandwidth = AsConfigurationV1InstanceConfigPublicIpEipBandwidth(**bandwidth)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__083ed79fd0932920398deb1877749d15f7644b48391328b2b2a8cc653cf3e465)
            check_type(argname="argument bandwidth", value=bandwidth, expected_type=type_hints["bandwidth"])
            check_type(argname="argument ip_type", value=ip_type, expected_type=type_hints["ip_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bandwidth": bandwidth,
            "ip_type": ip_type,
        }

    @builtins.property
    def bandwidth(self) -> "AsConfigurationV1InstanceConfigPublicIpEipBandwidth":
        '''bandwidth block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#bandwidth AsConfigurationV1#bandwidth}
        '''
        result = self._values.get("bandwidth")
        assert result is not None, "Required property 'bandwidth' is missing"
        return typing.cast("AsConfigurationV1InstanceConfigPublicIpEipBandwidth", result)

    @builtins.property
    def ip_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#ip_type AsConfigurationV1#ip_type}.'''
        result = self._values.get("ip_type")
        assert result is not None, "Required property 'ip_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsConfigurationV1InstanceConfigPublicIpEip(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asConfigurationV1.AsConfigurationV1InstanceConfigPublicIpEipBandwidth",
    jsii_struct_bases=[],
    name_mapping={
        "charging_mode": "chargingMode",
        "share_type": "shareType",
        "size": "size",
    },
)
class AsConfigurationV1InstanceConfigPublicIpEipBandwidth:
    def __init__(
        self,
        *,
        charging_mode: builtins.str,
        share_type: builtins.str,
        size: jsii.Number,
    ) -> None:
        '''
        :param charging_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#charging_mode AsConfigurationV1#charging_mode}.
        :param share_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#share_type AsConfigurationV1#share_type}.
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#size AsConfigurationV1#size}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72079c95fc454087c573fd2156f417e4e1d358ffb070f5b89a4c54cb5b5a1db7)
            check_type(argname="argument charging_mode", value=charging_mode, expected_type=type_hints["charging_mode"])
            check_type(argname="argument share_type", value=share_type, expected_type=type_hints["share_type"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "charging_mode": charging_mode,
            "share_type": share_type,
            "size": size,
        }

    @builtins.property
    def charging_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#charging_mode AsConfigurationV1#charging_mode}.'''
        result = self._values.get("charging_mode")
        assert result is not None, "Required property 'charging_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def share_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#share_type AsConfigurationV1#share_type}.'''
        result = self._values.get("share_type")
        assert result is not None, "Required property 'share_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#size AsConfigurationV1#size}.'''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsConfigurationV1InstanceConfigPublicIpEipBandwidth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AsConfigurationV1InstanceConfigPublicIpEipBandwidthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asConfigurationV1.AsConfigurationV1InstanceConfigPublicIpEipBandwidthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a6a677891ee345c735b6ace22d62dab66f08fd4ea8d0b981025488d65bd33ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="chargingModeInput")
    def charging_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "chargingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="shareTypeInput")
    def share_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shareTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="chargingMode")
    def charging_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "chargingMode"))

    @charging_mode.setter
    def charging_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95fb027f2fab97a1e1f96e36b9dc48385093b9727fd373fe0a74826fb53ab471)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "chargingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shareType")
    def share_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shareType"))

    @share_type.setter
    def share_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fdd2db8933945f67732fadc592ef5fb8379ade6c2f32c50777bc713e99ab4b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shareType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f254be786459748cab03be8412e778840e63e1cc73ecb94cc9b8f7b11066033b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AsConfigurationV1InstanceConfigPublicIpEipBandwidth]:
        return typing.cast(typing.Optional[AsConfigurationV1InstanceConfigPublicIpEipBandwidth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AsConfigurationV1InstanceConfigPublicIpEipBandwidth],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddbab29c5c4091cb85a823768d204e145a61d3646c301071ffed36b7380efcf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AsConfigurationV1InstanceConfigPublicIpEipOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asConfigurationV1.AsConfigurationV1InstanceConfigPublicIpEipOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b3a78f424e6bac920c4cd40cbe9632f6aab455f581ac8cbf74d0703801dc1d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBandwidth")
    def put_bandwidth(
        self,
        *,
        charging_mode: builtins.str,
        share_type: builtins.str,
        size: jsii.Number,
    ) -> None:
        '''
        :param charging_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#charging_mode AsConfigurationV1#charging_mode}.
        :param share_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#share_type AsConfigurationV1#share_type}.
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#size AsConfigurationV1#size}.
        '''
        value = AsConfigurationV1InstanceConfigPublicIpEipBandwidth(
            charging_mode=charging_mode, share_type=share_type, size=size
        )

        return typing.cast(None, jsii.invoke(self, "putBandwidth", [value]))

    @builtins.property
    @jsii.member(jsii_name="bandwidth")
    def bandwidth(
        self,
    ) -> AsConfigurationV1InstanceConfigPublicIpEipBandwidthOutputReference:
        return typing.cast(AsConfigurationV1InstanceConfigPublicIpEipBandwidthOutputReference, jsii.get(self, "bandwidth"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthInput")
    def bandwidth_input(
        self,
    ) -> typing.Optional[AsConfigurationV1InstanceConfigPublicIpEipBandwidth]:
        return typing.cast(typing.Optional[AsConfigurationV1InstanceConfigPublicIpEipBandwidth], jsii.get(self, "bandwidthInput"))

    @builtins.property
    @jsii.member(jsii_name="ipTypeInput")
    def ip_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="ipType")
    def ip_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipType"))

    @ip_type.setter
    def ip_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4df3cd6a1d2cd1165fc54458aff118968510b3defbd63622efcf37928b52d8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AsConfigurationV1InstanceConfigPublicIpEip]:
        return typing.cast(typing.Optional[AsConfigurationV1InstanceConfigPublicIpEip], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AsConfigurationV1InstanceConfigPublicIpEip],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f592ea9cda77b853b50bcc7621fb6b0a8362b111c55f9001de6ad7a4c5bb62b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AsConfigurationV1InstanceConfigPublicIpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asConfigurationV1.AsConfigurationV1InstanceConfigPublicIpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34dbdafaf73e83b71979e6815dc3d6a36ef6f88084829271adf00ba35d40a7c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEip")
    def put_eip(
        self,
        *,
        bandwidth: typing.Union[AsConfigurationV1InstanceConfigPublicIpEipBandwidth, typing.Dict[builtins.str, typing.Any]],
        ip_type: builtins.str,
    ) -> None:
        '''
        :param bandwidth: bandwidth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#bandwidth AsConfigurationV1#bandwidth}
        :param ip_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_configuration_v1#ip_type AsConfigurationV1#ip_type}.
        '''
        value = AsConfigurationV1InstanceConfigPublicIpEip(
            bandwidth=bandwidth, ip_type=ip_type
        )

        return typing.cast(None, jsii.invoke(self, "putEip", [value]))

    @builtins.property
    @jsii.member(jsii_name="eip")
    def eip(self) -> AsConfigurationV1InstanceConfigPublicIpEipOutputReference:
        return typing.cast(AsConfigurationV1InstanceConfigPublicIpEipOutputReference, jsii.get(self, "eip"))

    @builtins.property
    @jsii.member(jsii_name="eipInput")
    def eip_input(self) -> typing.Optional[AsConfigurationV1InstanceConfigPublicIpEip]:
        return typing.cast(typing.Optional[AsConfigurationV1InstanceConfigPublicIpEip], jsii.get(self, "eipInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AsConfigurationV1InstanceConfigPublicIp]:
        return typing.cast(typing.Optional[AsConfigurationV1InstanceConfigPublicIp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AsConfigurationV1InstanceConfigPublicIp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22d46bc617696a35039a01f17a1625462bb5451b5c67797f70e60a0a5f39a2e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AsConfigurationV1",
    "AsConfigurationV1Config",
    "AsConfigurationV1InstanceConfig",
    "AsConfigurationV1InstanceConfigDisk",
    "AsConfigurationV1InstanceConfigDiskList",
    "AsConfigurationV1InstanceConfigDiskOutputReference",
    "AsConfigurationV1InstanceConfigOutputReference",
    "AsConfigurationV1InstanceConfigPersonality",
    "AsConfigurationV1InstanceConfigPersonalityList",
    "AsConfigurationV1InstanceConfigPersonalityOutputReference",
    "AsConfigurationV1InstanceConfigPublicIp",
    "AsConfigurationV1InstanceConfigPublicIpEip",
    "AsConfigurationV1InstanceConfigPublicIpEipBandwidth",
    "AsConfigurationV1InstanceConfigPublicIpEipBandwidthOutputReference",
    "AsConfigurationV1InstanceConfigPublicIpEipOutputReference",
    "AsConfigurationV1InstanceConfigPublicIpOutputReference",
]

publication.publish()

def _typecheckingstub__14d2b9a449f242f99971494dcdccc59881dbc019ac771d916d7a7c27b893d60f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    instance_config: typing.Union[AsConfigurationV1InstanceConfig, typing.Dict[builtins.str, typing.Any]],
    scaling_configuration_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__a614e0b940bf8405c59e4eaefe6be5d633c3042ccb479f8cf07808360c10650b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__612fe2f7af0e0649daec341a04cee624aa4be1f0aa0181ff6771a8dc86de4576(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__512535eff4340271062eac01cf7b5f1ef5ad3eb18fdd955e411ccafb8f62da1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cb03179bbbd3b9e681ab0efff910c31264c9cc3649596f7daf7959138e16a85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f73362da314007b75d90718bb4119d1a69b229ebf75d8422a66cc611bba6d6c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    instance_config: typing.Union[AsConfigurationV1InstanceConfig, typing.Dict[builtins.str, typing.Any]],
    scaling_configuration_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f33ed89ab3a969744b14fb646058ebd01c62cecf2db6b20b94a0051bbe2fe83(
    *,
    key_name: builtins.str,
    disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AsConfigurationV1InstanceConfigDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    flavor: typing.Optional[builtins.str] = None,
    image: typing.Optional[builtins.str] = None,
    instance_id: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    personality: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AsConfigurationV1InstanceConfigPersonality, typing.Dict[builtins.str, typing.Any]]]]] = None,
    public_ip: typing.Optional[typing.Union[AsConfigurationV1InstanceConfigPublicIp, typing.Dict[builtins.str, typing.Any]]] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e695d640c13ec4082b1158a53057096e8069e895c0ad84bd6bdd6008d240b0cc(
    *,
    disk_type: builtins.str,
    size: jsii.Number,
    volume_type: builtins.str,
    kms_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d7cd43f44e1dd70094b6a630b872888aa70dcda54522e78a30249e283eb97bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967b4df55a9018c4549b28902390ebd50391c86a6c9d329696c8b3c18432f681(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f14a936c2b66a9c25883cc1d5205e040b033af8af139fc3737db7ed73d34cba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c99564ce75bd9ff1fe3ff5303c87bc3e7846ac1dfd677f3aaf4368b8f674bdc9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfbb6206642047905d568052d33abe7209c895d7b3ac20675221457720355a18(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__263331334a5328b641bf0d1d7c689e1c3a6e86491677c2d0ab8b590a0394567b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsConfigurationV1InstanceConfigDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a41b3465f25b3fb41380957d2e42026bcc2cda5374550e86dfc9ad73789e959(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9e39cccc9827f0937f4f67390d04d7319bc32ebec843b39c0947da04d9ad4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea2f02692cf81a1186ef2d555d814815d3208fa1a962d2507c3966a1820b42b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b31533da30e83a5a46c22ec0a170f923e69dce03a2e0eb8e55a7e28078b0d73(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397af872483c952e7f4949307ea15b298b891cdda2021725f3cf4daaae985097(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8825ae411f7143d99cea031b60030e6e7f8f0d12006e2297e5a34061b9df2044(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsConfigurationV1InstanceConfigDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8adafa2b40c4d592f7a400babe8318b528519f7ff49eaddd60557dce4e24361(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__457723c4ea7ede38789b82bbe58f06de9a1a3e82b094b92b220dcbe0e764d267(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AsConfigurationV1InstanceConfigDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4f0e693929517fcdbb839dd9e91b306969b37bc0616b13d190f21e61314afe(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AsConfigurationV1InstanceConfigPersonality, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97512337487f92e81a33bba160fb0aa20e7869bb049a0d3c353f195d563b0e48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__834184d9039614301036f898661cccaa2482302a1800d75a2f23bb9ab42817dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a74a0b3dffa910bbb8cedf388a8e6cef28734f2e2e02550e02a5635df38dbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb57bebba073dacb0bc357c9f5212dfcc1cc8ebcdf186946edb0cc50bd61434(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e19f77ad8f76806900e599a33a70ed16e8d572e21f0fc01d499985acea69de(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfde9fce5752de5fb9dbd1cdb7dc2dd7d8728c2cceecd33d68bbb54fab16f445(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a2cb2fcf41b4428c43535544ffcb3a26517cf920523bac575316ab5c6cd6c55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2938f883077a98a180cdc658ec69f964d9c5105240c0ec296297dad76241a10(
    value: typing.Optional[AsConfigurationV1InstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__422080c6dcba79b6aec12e50cf1ed422b1bab2442b5e6bc24b1726c198a724eb(
    *,
    content: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd9a08b1a6668c3a0ceda591329305ad38693157cd5bfd5a467ce0c36d5cf5e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bbf518a77ef15ce65cca517511b65af013bbbedaa453a3a6bb423e5c3a34632(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0f6d1be3ebef9123c8f075aa29b3a89387538aebe5bc2c59dc5a379664f58e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b13dfdac6de15993b26d15d380a40c013db55938d5b6e5574099256c09541502(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed12e7e00be16fa2aa40d49f8baf33ec57fee4763fbb9c3bfd4dbf3d921b4f1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fcb673a70b0b1644ef316437eb5a568c41b7aec36e69661deee8dfe60d5ad6f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsConfigurationV1InstanceConfigPersonality]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e90701aa99aa1f31ba5a073c41e393c7610eafd77bd95e96961b0b18e40e9a91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05b566333f0eec6082d24d90d91b26810e574e85416725d9c9f62123c43ac0d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbbe9a72c6ad79b5c2ef1320f5e7eb50aed43752c1699a0206f0b101b0bdb0a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0193fbb6666710c14d6ce9e726a4cf1e1051930a3ca71bdcf3db880ddf3ea73c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsConfigurationV1InstanceConfigPersonality]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccb95c8219058fe2e1d075854c4cefdd3939f56c0a883dd0ded0696ce639e79f(
    *,
    eip: typing.Union[AsConfigurationV1InstanceConfigPublicIpEip, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083ed79fd0932920398deb1877749d15f7644b48391328b2b2a8cc653cf3e465(
    *,
    bandwidth: typing.Union[AsConfigurationV1InstanceConfigPublicIpEipBandwidth, typing.Dict[builtins.str, typing.Any]],
    ip_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72079c95fc454087c573fd2156f417e4e1d358ffb070f5b89a4c54cb5b5a1db7(
    *,
    charging_mode: builtins.str,
    share_type: builtins.str,
    size: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a6a677891ee345c735b6ace22d62dab66f08fd4ea8d0b981025488d65bd33ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95fb027f2fab97a1e1f96e36b9dc48385093b9727fd373fe0a74826fb53ab471(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fdd2db8933945f67732fadc592ef5fb8379ade6c2f32c50777bc713e99ab4b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f254be786459748cab03be8412e778840e63e1cc73ecb94cc9b8f7b11066033b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddbab29c5c4091cb85a823768d204e145a61d3646c301071ffed36b7380efcf3(
    value: typing.Optional[AsConfigurationV1InstanceConfigPublicIpEipBandwidth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b3a78f424e6bac920c4cd40cbe9632f6aab455f581ac8cbf74d0703801dc1d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4df3cd6a1d2cd1165fc54458aff118968510b3defbd63622efcf37928b52d8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f592ea9cda77b853b50bcc7621fb6b0a8362b111c55f9001de6ad7a4c5bb62b(
    value: typing.Optional[AsConfigurationV1InstanceConfigPublicIpEip],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34dbdafaf73e83b71979e6815dc3d6a36ef6f88084829271adf00ba35d40a7c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22d46bc617696a35039a01f17a1625462bb5451b5c67797f70e60a0a5f39a2e5(
    value: typing.Optional[AsConfigurationV1InstanceConfigPublicIp],
) -> None:
    """Type checking stubs"""
    pass
