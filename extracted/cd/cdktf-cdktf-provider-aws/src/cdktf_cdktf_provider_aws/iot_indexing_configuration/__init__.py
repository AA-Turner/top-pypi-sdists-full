r'''
# `aws_iot_indexing_configuration`

Refer to the Terraform Registry for docs: [`aws_iot_indexing_configuration`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration).
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


class IotIndexingConfiguration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotIndexingConfiguration.IotIndexingConfiguration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration aws_iot_indexing_configuration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        id: typing.Optional[builtins.str] = None,
        thing_group_indexing_configuration: typing.Optional[typing.Union["IotIndexingConfigurationThingGroupIndexingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        thing_indexing_configuration: typing.Optional[typing.Union["IotIndexingConfigurationThingIndexingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration aws_iot_indexing_configuration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#id IotIndexingConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param thing_group_indexing_configuration: thing_group_indexing_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#thing_group_indexing_configuration IotIndexingConfiguration#thing_group_indexing_configuration}
        :param thing_indexing_configuration: thing_indexing_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#thing_indexing_configuration IotIndexingConfiguration#thing_indexing_configuration}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26a60a3f993047844e3effdb22da389b88ff3e87253d8acb440996e6cc466541)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IotIndexingConfigurationConfig(
            id=id,
            thing_group_indexing_configuration=thing_group_indexing_configuration,
            thing_indexing_configuration=thing_indexing_configuration,
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
        '''Generates CDKTF code for importing a IotIndexingConfiguration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IotIndexingConfiguration to import.
        :param import_from_id: The id of the existing IotIndexingConfiguration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IotIndexingConfiguration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de9273eba949a8d35c719561397d95900d3065f03398e7fe1991b3f258068a4f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putThingGroupIndexingConfiguration")
    def put_thing_group_indexing_configuration(
        self,
        *,
        thing_group_indexing_mode: builtins.str,
        custom_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotIndexingConfigurationThingGroupIndexingConfigurationCustomField", typing.Dict[builtins.str, typing.Any]]]]] = None,
        managed_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotIndexingConfigurationThingGroupIndexingConfigurationManagedField", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param thing_group_indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#thing_group_indexing_mode IotIndexingConfiguration#thing_group_indexing_mode}.
        :param custom_field: custom_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#custom_field IotIndexingConfiguration#custom_field}
        :param managed_field: managed_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#managed_field IotIndexingConfiguration#managed_field}
        '''
        value = IotIndexingConfigurationThingGroupIndexingConfiguration(
            thing_group_indexing_mode=thing_group_indexing_mode,
            custom_field=custom_field,
            managed_field=managed_field,
        )

        return typing.cast(None, jsii.invoke(self, "putThingGroupIndexingConfiguration", [value]))

    @jsii.member(jsii_name="putThingIndexingConfiguration")
    def put_thing_indexing_configuration(
        self,
        *,
        thing_indexing_mode: builtins.str,
        custom_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotIndexingConfigurationThingIndexingConfigurationCustomField", typing.Dict[builtins.str, typing.Any]]]]] = None,
        device_defender_indexing_mode: typing.Optional[builtins.str] = None,
        filter: typing.Optional[typing.Union["IotIndexingConfigurationThingIndexingConfigurationFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotIndexingConfigurationThingIndexingConfigurationManagedField", typing.Dict[builtins.str, typing.Any]]]]] = None,
        named_shadow_indexing_mode: typing.Optional[builtins.str] = None,
        thing_connectivity_indexing_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param thing_indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#thing_indexing_mode IotIndexingConfiguration#thing_indexing_mode}.
        :param custom_field: custom_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#custom_field IotIndexingConfiguration#custom_field}
        :param device_defender_indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#device_defender_indexing_mode IotIndexingConfiguration#device_defender_indexing_mode}.
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#filter IotIndexingConfiguration#filter}
        :param managed_field: managed_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#managed_field IotIndexingConfiguration#managed_field}
        :param named_shadow_indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#named_shadow_indexing_mode IotIndexingConfiguration#named_shadow_indexing_mode}.
        :param thing_connectivity_indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#thing_connectivity_indexing_mode IotIndexingConfiguration#thing_connectivity_indexing_mode}.
        '''
        value = IotIndexingConfigurationThingIndexingConfiguration(
            thing_indexing_mode=thing_indexing_mode,
            custom_field=custom_field,
            device_defender_indexing_mode=device_defender_indexing_mode,
            filter=filter,
            managed_field=managed_field,
            named_shadow_indexing_mode=named_shadow_indexing_mode,
            thing_connectivity_indexing_mode=thing_connectivity_indexing_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putThingIndexingConfiguration", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetThingGroupIndexingConfiguration")
    def reset_thing_group_indexing_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThingGroupIndexingConfiguration", []))

    @jsii.member(jsii_name="resetThingIndexingConfiguration")
    def reset_thing_indexing_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThingIndexingConfiguration", []))

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
    @jsii.member(jsii_name="thingGroupIndexingConfiguration")
    def thing_group_indexing_configuration(
        self,
    ) -> "IotIndexingConfigurationThingGroupIndexingConfigurationOutputReference":
        return typing.cast("IotIndexingConfigurationThingGroupIndexingConfigurationOutputReference", jsii.get(self, "thingGroupIndexingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="thingIndexingConfiguration")
    def thing_indexing_configuration(
        self,
    ) -> "IotIndexingConfigurationThingIndexingConfigurationOutputReference":
        return typing.cast("IotIndexingConfigurationThingIndexingConfigurationOutputReference", jsii.get(self, "thingIndexingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="thingGroupIndexingConfigurationInput")
    def thing_group_indexing_configuration_input(
        self,
    ) -> typing.Optional["IotIndexingConfigurationThingGroupIndexingConfiguration"]:
        return typing.cast(typing.Optional["IotIndexingConfigurationThingGroupIndexingConfiguration"], jsii.get(self, "thingGroupIndexingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="thingIndexingConfigurationInput")
    def thing_indexing_configuration_input(
        self,
    ) -> typing.Optional["IotIndexingConfigurationThingIndexingConfiguration"]:
        return typing.cast(typing.Optional["IotIndexingConfigurationThingIndexingConfiguration"], jsii.get(self, "thingIndexingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89b4231912647940e6f6a1daca0145618b74d484fc6ae2907ab14d1a4bdb352e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "id": "id",
        "thing_group_indexing_configuration": "thingGroupIndexingConfiguration",
        "thing_indexing_configuration": "thingIndexingConfiguration",
    },
)
class IotIndexingConfigurationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        id: typing.Optional[builtins.str] = None,
        thing_group_indexing_configuration: typing.Optional[typing.Union["IotIndexingConfigurationThingGroupIndexingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        thing_indexing_configuration: typing.Optional[typing.Union["IotIndexingConfigurationThingIndexingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#id IotIndexingConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param thing_group_indexing_configuration: thing_group_indexing_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#thing_group_indexing_configuration IotIndexingConfiguration#thing_group_indexing_configuration}
        :param thing_indexing_configuration: thing_indexing_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#thing_indexing_configuration IotIndexingConfiguration#thing_indexing_configuration}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(thing_group_indexing_configuration, dict):
            thing_group_indexing_configuration = IotIndexingConfigurationThingGroupIndexingConfiguration(**thing_group_indexing_configuration)
        if isinstance(thing_indexing_configuration, dict):
            thing_indexing_configuration = IotIndexingConfigurationThingIndexingConfiguration(**thing_indexing_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__116ad2196434c2c1c05b7ada1610c1f989c57c4b4c7f08bd7d89ebc9c8655eb9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument thing_group_indexing_configuration", value=thing_group_indexing_configuration, expected_type=type_hints["thing_group_indexing_configuration"])
            check_type(argname="argument thing_indexing_configuration", value=thing_indexing_configuration, expected_type=type_hints["thing_indexing_configuration"])
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
        if id is not None:
            self._values["id"] = id
        if thing_group_indexing_configuration is not None:
            self._values["thing_group_indexing_configuration"] = thing_group_indexing_configuration
        if thing_indexing_configuration is not None:
            self._values["thing_indexing_configuration"] = thing_indexing_configuration

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
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#id IotIndexingConfiguration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def thing_group_indexing_configuration(
        self,
    ) -> typing.Optional["IotIndexingConfigurationThingGroupIndexingConfiguration"]:
        '''thing_group_indexing_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#thing_group_indexing_configuration IotIndexingConfiguration#thing_group_indexing_configuration}
        '''
        result = self._values.get("thing_group_indexing_configuration")
        return typing.cast(typing.Optional["IotIndexingConfigurationThingGroupIndexingConfiguration"], result)

    @builtins.property
    def thing_indexing_configuration(
        self,
    ) -> typing.Optional["IotIndexingConfigurationThingIndexingConfiguration"]:
        '''thing_indexing_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#thing_indexing_configuration IotIndexingConfiguration#thing_indexing_configuration}
        '''
        result = self._values.get("thing_indexing_configuration")
        return typing.cast(typing.Optional["IotIndexingConfigurationThingIndexingConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotIndexingConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingGroupIndexingConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "thing_group_indexing_mode": "thingGroupIndexingMode",
        "custom_field": "customField",
        "managed_field": "managedField",
    },
)
class IotIndexingConfigurationThingGroupIndexingConfiguration:
    def __init__(
        self,
        *,
        thing_group_indexing_mode: builtins.str,
        custom_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotIndexingConfigurationThingGroupIndexingConfigurationCustomField", typing.Dict[builtins.str, typing.Any]]]]] = None,
        managed_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotIndexingConfigurationThingGroupIndexingConfigurationManagedField", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param thing_group_indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#thing_group_indexing_mode IotIndexingConfiguration#thing_group_indexing_mode}.
        :param custom_field: custom_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#custom_field IotIndexingConfiguration#custom_field}
        :param managed_field: managed_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#managed_field IotIndexingConfiguration#managed_field}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e6b06369639a4284ed0a2a38af23b40352b68452b0a7daf11c5ad0494d550b9)
            check_type(argname="argument thing_group_indexing_mode", value=thing_group_indexing_mode, expected_type=type_hints["thing_group_indexing_mode"])
            check_type(argname="argument custom_field", value=custom_field, expected_type=type_hints["custom_field"])
            check_type(argname="argument managed_field", value=managed_field, expected_type=type_hints["managed_field"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "thing_group_indexing_mode": thing_group_indexing_mode,
        }
        if custom_field is not None:
            self._values["custom_field"] = custom_field
        if managed_field is not None:
            self._values["managed_field"] = managed_field

    @builtins.property
    def thing_group_indexing_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#thing_group_indexing_mode IotIndexingConfiguration#thing_group_indexing_mode}.'''
        result = self._values.get("thing_group_indexing_mode")
        assert result is not None, "Required property 'thing_group_indexing_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_field(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotIndexingConfigurationThingGroupIndexingConfigurationCustomField"]]]:
        '''custom_field block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#custom_field IotIndexingConfiguration#custom_field}
        '''
        result = self._values.get("custom_field")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotIndexingConfigurationThingGroupIndexingConfigurationCustomField"]]], result)

    @builtins.property
    def managed_field(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotIndexingConfigurationThingGroupIndexingConfigurationManagedField"]]]:
        '''managed_field block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#managed_field IotIndexingConfiguration#managed_field}
        '''
        result = self._values.get("managed_field")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotIndexingConfigurationThingGroupIndexingConfigurationManagedField"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotIndexingConfigurationThingGroupIndexingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingGroupIndexingConfigurationCustomField",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class IotIndexingConfigurationThingGroupIndexingConfigurationCustomField:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#name IotIndexingConfiguration#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#type IotIndexingConfiguration#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68dc1fc89579048b4ffc6db22bd66563344564415aa3fa2db4c92eaf059b6071)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#name IotIndexingConfiguration#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#type IotIndexingConfiguration#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotIndexingConfigurationThingGroupIndexingConfigurationCustomField(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotIndexingConfigurationThingGroupIndexingConfigurationCustomFieldList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingGroupIndexingConfigurationCustomFieldList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__743545bb0a1b8b894bb70d09e0a09eaf9d90124ef8f188cdb318ee00500b2b34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IotIndexingConfigurationThingGroupIndexingConfigurationCustomFieldOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ace513921ef3e5c373b0449cdb03a8c0137cc56b20801459cfc0f3eb2eb47cc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotIndexingConfigurationThingGroupIndexingConfigurationCustomFieldOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77727ca6e97d9da7c3456ccb6882d1defb86268fd7cea202b54581003d133322)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72a82046a9195e2a6010f1b140b1ee4c850a1dd80740c16b6aab2d95f713b74f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a09a433b974956e8836948837c5511b95ef39baa4e644cbecf336570e80b297)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationCustomField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationCustomField]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationCustomField]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de1cb06f71f3403ac3ac6953916bfc979ee7fcc566f4addbea7b2f152f60ddaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotIndexingConfigurationThingGroupIndexingConfigurationCustomFieldOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingGroupIndexingConfigurationCustomFieldOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80e8c2b90665ab3ea96cbc968a444a60410bf97bb4a632b641aa7a713eaee8d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e6b4105931e55a78d2817606391d6655ac8763cac175794a009ab4bd36067d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__038b50efa9524a4634f9faf7149e71e526ab7aa4e275ac8403f191328483b05a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingGroupIndexingConfigurationCustomField]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingGroupIndexingConfigurationCustomField]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingGroupIndexingConfigurationCustomField]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aa244bb0ca83d0bd53d83e32cff38fee51270a1c9c2209ccd395ff4d477515a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingGroupIndexingConfigurationManagedField",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class IotIndexingConfigurationThingGroupIndexingConfigurationManagedField:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#name IotIndexingConfiguration#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#type IotIndexingConfiguration#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58342f0e119be8ba799dc9d2ae1e93aef02b8ef6c7c2da24b91cbd042a74d2c8)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#name IotIndexingConfiguration#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#type IotIndexingConfiguration#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotIndexingConfigurationThingGroupIndexingConfigurationManagedField(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotIndexingConfigurationThingGroupIndexingConfigurationManagedFieldList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingGroupIndexingConfigurationManagedFieldList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86d3e50e799105c4b3723a84fec9be84a9880049acf1c05e49c8c783d8fe2350)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IotIndexingConfigurationThingGroupIndexingConfigurationManagedFieldOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0835db3c630886afad9ced20fa4149d664d44c7ab25d7ee373abbfb3aea2ea07)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotIndexingConfigurationThingGroupIndexingConfigurationManagedFieldOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c1030b4d6ced9abd592e519229ed1906d6d60ea041561b23cca66a941e6edd0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50126d8f4f95890967038a8c636a54d19a6767b9f8461cd3b67edf50feeeb12b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dc9981028f77ad7f5e16f3b42ec1c79330c933e8ee97d3bab38b267d06ad1c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationManagedField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationManagedField]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationManagedField]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39794c2bfead7871bd77106cb72ff3acdbcc82d1502b49a660ba055022471f08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotIndexingConfigurationThingGroupIndexingConfigurationManagedFieldOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingGroupIndexingConfigurationManagedFieldOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50ba477fbdd198a6593da2fc895127749d431aca68bb4873586b68944306b3aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb33c22cb4204122a711f555ccf592f7cc9d53fdd7e71540018e8c10d4cf3628)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc6868c81ff7b09e840794b6dbe24cd52adc8de1e63df53d91089da22895581b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingGroupIndexingConfigurationManagedField]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingGroupIndexingConfigurationManagedField]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingGroupIndexingConfigurationManagedField]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ad041df3a249b19edf21764f74a097debaf808ab3bdfae002e1876db7e35620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotIndexingConfigurationThingGroupIndexingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingGroupIndexingConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__592bdc470f4b4180dde08023b1166fdc0dc820556f5d9580906362628c61e225)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomField")
    def put_custom_field(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingGroupIndexingConfigurationCustomField, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cde084ab0e1d1f35c61c076b4f518f15b4d288258d4a5b42276fa2c659a8401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomField", [value]))

    @jsii.member(jsii_name="putManagedField")
    def put_managed_field(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingGroupIndexingConfigurationManagedField, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e98bfb54ad625f3f4d56040e9039582cb945c33a4f57e2d2a4da633962a88653)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putManagedField", [value]))

    @jsii.member(jsii_name="resetCustomField")
    def reset_custom_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomField", []))

    @jsii.member(jsii_name="resetManagedField")
    def reset_managed_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedField", []))

    @builtins.property
    @jsii.member(jsii_name="customField")
    def custom_field(
        self,
    ) -> IotIndexingConfigurationThingGroupIndexingConfigurationCustomFieldList:
        return typing.cast(IotIndexingConfigurationThingGroupIndexingConfigurationCustomFieldList, jsii.get(self, "customField"))

    @builtins.property
    @jsii.member(jsii_name="managedField")
    def managed_field(
        self,
    ) -> IotIndexingConfigurationThingGroupIndexingConfigurationManagedFieldList:
        return typing.cast(IotIndexingConfigurationThingGroupIndexingConfigurationManagedFieldList, jsii.get(self, "managedField"))

    @builtins.property
    @jsii.member(jsii_name="customFieldInput")
    def custom_field_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationCustomField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationCustomField]]], jsii.get(self, "customFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="managedFieldInput")
    def managed_field_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationManagedField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationManagedField]]], jsii.get(self, "managedFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="thingGroupIndexingModeInput")
    def thing_group_indexing_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thingGroupIndexingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="thingGroupIndexingMode")
    def thing_group_indexing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thingGroupIndexingMode"))

    @thing_group_indexing_mode.setter
    def thing_group_indexing_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__113e715f3be9ffef6c912d704bc92dc37d7c949928b96bbd60bf4cc95ce69d6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thingGroupIndexingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IotIndexingConfigurationThingGroupIndexingConfiguration]:
        return typing.cast(typing.Optional[IotIndexingConfigurationThingGroupIndexingConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotIndexingConfigurationThingGroupIndexingConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__931d21e5902521208f28ff5be8b2132b62e0faddf8d7ba4cc9a647771f832882)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingIndexingConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "thing_indexing_mode": "thingIndexingMode",
        "custom_field": "customField",
        "device_defender_indexing_mode": "deviceDefenderIndexingMode",
        "filter": "filter",
        "managed_field": "managedField",
        "named_shadow_indexing_mode": "namedShadowIndexingMode",
        "thing_connectivity_indexing_mode": "thingConnectivityIndexingMode",
    },
)
class IotIndexingConfigurationThingIndexingConfiguration:
    def __init__(
        self,
        *,
        thing_indexing_mode: builtins.str,
        custom_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotIndexingConfigurationThingIndexingConfigurationCustomField", typing.Dict[builtins.str, typing.Any]]]]] = None,
        device_defender_indexing_mode: typing.Optional[builtins.str] = None,
        filter: typing.Optional[typing.Union["IotIndexingConfigurationThingIndexingConfigurationFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotIndexingConfigurationThingIndexingConfigurationManagedField", typing.Dict[builtins.str, typing.Any]]]]] = None,
        named_shadow_indexing_mode: typing.Optional[builtins.str] = None,
        thing_connectivity_indexing_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param thing_indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#thing_indexing_mode IotIndexingConfiguration#thing_indexing_mode}.
        :param custom_field: custom_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#custom_field IotIndexingConfiguration#custom_field}
        :param device_defender_indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#device_defender_indexing_mode IotIndexingConfiguration#device_defender_indexing_mode}.
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#filter IotIndexingConfiguration#filter}
        :param managed_field: managed_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#managed_field IotIndexingConfiguration#managed_field}
        :param named_shadow_indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#named_shadow_indexing_mode IotIndexingConfiguration#named_shadow_indexing_mode}.
        :param thing_connectivity_indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#thing_connectivity_indexing_mode IotIndexingConfiguration#thing_connectivity_indexing_mode}.
        '''
        if isinstance(filter, dict):
            filter = IotIndexingConfigurationThingIndexingConfigurationFilter(**filter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c037a24b6b1595bbe40de08bb7169ea0b867aecc7b33fffe4276220fcd9f6134)
            check_type(argname="argument thing_indexing_mode", value=thing_indexing_mode, expected_type=type_hints["thing_indexing_mode"])
            check_type(argname="argument custom_field", value=custom_field, expected_type=type_hints["custom_field"])
            check_type(argname="argument device_defender_indexing_mode", value=device_defender_indexing_mode, expected_type=type_hints["device_defender_indexing_mode"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument managed_field", value=managed_field, expected_type=type_hints["managed_field"])
            check_type(argname="argument named_shadow_indexing_mode", value=named_shadow_indexing_mode, expected_type=type_hints["named_shadow_indexing_mode"])
            check_type(argname="argument thing_connectivity_indexing_mode", value=thing_connectivity_indexing_mode, expected_type=type_hints["thing_connectivity_indexing_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "thing_indexing_mode": thing_indexing_mode,
        }
        if custom_field is not None:
            self._values["custom_field"] = custom_field
        if device_defender_indexing_mode is not None:
            self._values["device_defender_indexing_mode"] = device_defender_indexing_mode
        if filter is not None:
            self._values["filter"] = filter
        if managed_field is not None:
            self._values["managed_field"] = managed_field
        if named_shadow_indexing_mode is not None:
            self._values["named_shadow_indexing_mode"] = named_shadow_indexing_mode
        if thing_connectivity_indexing_mode is not None:
            self._values["thing_connectivity_indexing_mode"] = thing_connectivity_indexing_mode

    @builtins.property
    def thing_indexing_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#thing_indexing_mode IotIndexingConfiguration#thing_indexing_mode}.'''
        result = self._values.get("thing_indexing_mode")
        assert result is not None, "Required property 'thing_indexing_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_field(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotIndexingConfigurationThingIndexingConfigurationCustomField"]]]:
        '''custom_field block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#custom_field IotIndexingConfiguration#custom_field}
        '''
        result = self._values.get("custom_field")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotIndexingConfigurationThingIndexingConfigurationCustomField"]]], result)

    @builtins.property
    def device_defender_indexing_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#device_defender_indexing_mode IotIndexingConfiguration#device_defender_indexing_mode}.'''
        result = self._values.get("device_defender_indexing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional["IotIndexingConfigurationThingIndexingConfigurationFilter"]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#filter IotIndexingConfiguration#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional["IotIndexingConfigurationThingIndexingConfigurationFilter"], result)

    @builtins.property
    def managed_field(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotIndexingConfigurationThingIndexingConfigurationManagedField"]]]:
        '''managed_field block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#managed_field IotIndexingConfiguration#managed_field}
        '''
        result = self._values.get("managed_field")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotIndexingConfigurationThingIndexingConfigurationManagedField"]]], result)

    @builtins.property
    def named_shadow_indexing_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#named_shadow_indexing_mode IotIndexingConfiguration#named_shadow_indexing_mode}.'''
        result = self._values.get("named_shadow_indexing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def thing_connectivity_indexing_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#thing_connectivity_indexing_mode IotIndexingConfiguration#thing_connectivity_indexing_mode}.'''
        result = self._values.get("thing_connectivity_indexing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotIndexingConfigurationThingIndexingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingIndexingConfigurationCustomField",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class IotIndexingConfigurationThingIndexingConfigurationCustomField:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#name IotIndexingConfiguration#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#type IotIndexingConfiguration#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__068f405a2beaac36f4769e2cafbf1c9cc308c4c521a33132087f3dafa54d8d59)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#name IotIndexingConfiguration#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#type IotIndexingConfiguration#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotIndexingConfigurationThingIndexingConfigurationCustomField(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotIndexingConfigurationThingIndexingConfigurationCustomFieldList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingIndexingConfigurationCustomFieldList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fcf4e50ab1db3313bd7971e72614f2ec06a1ddf314fbeb45b41b4f59647cb6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IotIndexingConfigurationThingIndexingConfigurationCustomFieldOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b4308d4edd55cf26b870974ed7ea77f48c4a83a9ea7f70d997b7c9e576949e3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotIndexingConfigurationThingIndexingConfigurationCustomFieldOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d29a207b92a2ebeb0d9b66d1a949aae6e9d2bb22f19e1e1719522903c5edae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a772f83aa63c27d24f9993f445099737883ba96378f2d9d96d595e4ce803eca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__462a1057051e073d8c79c6a1ec4ce755bc70855c200d13445f4f682a9c9447fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationCustomField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationCustomField]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationCustomField]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47fbb835a0d6032dd2286a89d2b81ab82c624ce64c17309927e506a95267de97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotIndexingConfigurationThingIndexingConfigurationCustomFieldOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingIndexingConfigurationCustomFieldOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e02edd06ccaab4f4d5669020ae72c0d7c74436e50f54d705d2ce44ece8c32c86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcccfd9610b3482dc8fa18f8e829ddfde652c7f3637112d1404e2930a52a330b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9569b839f2808d078cb12c04bfe689e942997c8eab42c4656638f91e2ad3f50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingIndexingConfigurationCustomField]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingIndexingConfigurationCustomField]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingIndexingConfigurationCustomField]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62f431bc022f3acbe89069e9bc57f34d647637fb0b0008ad8c1661236d8dedfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingIndexingConfigurationFilter",
    jsii_struct_bases=[],
    name_mapping={"named_shadow_names": "namedShadowNames"},
)
class IotIndexingConfigurationThingIndexingConfigurationFilter:
    def __init__(
        self,
        *,
        named_shadow_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param named_shadow_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#named_shadow_names IotIndexingConfiguration#named_shadow_names}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__965ac93ec4a9376fbcc3aebcd49ccf00aa8fbf01a56df786646ec57ea42c490d)
            check_type(argname="argument named_shadow_names", value=named_shadow_names, expected_type=type_hints["named_shadow_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if named_shadow_names is not None:
            self._values["named_shadow_names"] = named_shadow_names

    @builtins.property
    def named_shadow_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#named_shadow_names IotIndexingConfiguration#named_shadow_names}.'''
        result = self._values.get("named_shadow_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotIndexingConfigurationThingIndexingConfigurationFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotIndexingConfigurationThingIndexingConfigurationFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingIndexingConfigurationFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0aa9b90b4f07b293ba98fe17ef977161fec38b804eeb833be5253b93a9371809)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNamedShadowNames")
    def reset_named_shadow_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamedShadowNames", []))

    @builtins.property
    @jsii.member(jsii_name="namedShadowNamesInput")
    def named_shadow_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "namedShadowNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="namedShadowNames")
    def named_shadow_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "namedShadowNames"))

    @named_shadow_names.setter
    def named_shadow_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__017aae8ae984cc2ed6babd94b9a950aa75858d5689654d0ffa7cdbe5c53bde8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namedShadowNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IotIndexingConfigurationThingIndexingConfigurationFilter]:
        return typing.cast(typing.Optional[IotIndexingConfigurationThingIndexingConfigurationFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotIndexingConfigurationThingIndexingConfigurationFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55bec91c42b7addac079ac1e16b83d0c593f0007fbd988521fd6c93f73b1eb59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingIndexingConfigurationManagedField",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class IotIndexingConfigurationThingIndexingConfigurationManagedField:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#name IotIndexingConfiguration#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#type IotIndexingConfiguration#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__126214ad8112dcbd95a9b06f4cb68e9f38740ff7850c247376ef013338cf7e2a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#name IotIndexingConfiguration#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#type IotIndexingConfiguration#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotIndexingConfigurationThingIndexingConfigurationManagedField(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotIndexingConfigurationThingIndexingConfigurationManagedFieldList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingIndexingConfigurationManagedFieldList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a55f822a73625f1af717bf3ddc944ab57b2132e05db209d82ec37122301dffc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IotIndexingConfigurationThingIndexingConfigurationManagedFieldOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__027606b8cb8dd96fc9e06c982b9ca99059a73d3043d72998bb0e289520163bed)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotIndexingConfigurationThingIndexingConfigurationManagedFieldOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c97597885856c353d3b8acbf93b3763eeaf8c8de47c3ba4341498a5865f14d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e2226607410fa0b2ca8ce33c328264128085629ba72868daea730624bff003c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b74ef6c24612ccccd48d95f6199649fb22ad263d08e13ca91238a9abadc411be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationManagedField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationManagedField]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationManagedField]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c89b92d2577086f6162058eeba70f321b29a05361d3285c06e7796064be35bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotIndexingConfigurationThingIndexingConfigurationManagedFieldOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingIndexingConfigurationManagedFieldOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4305e1665f4ccf0a0a621370ef3c30daf3dbd819b6b119939980ed55fcfee1e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28ca837753c59dd9770f070c998d423a68690d0d8636ef6ac8ea7922f4e2d918)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3933346477b96315cc7fec15546ad6c556f00efcc3198d57c36bf56b48b0fa28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingIndexingConfigurationManagedField]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingIndexingConfigurationManagedField]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingIndexingConfigurationManagedField]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ea94d63dc191a80f6767ba7936ffb452d02a0a358126f68728b9721f048bc93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotIndexingConfigurationThingIndexingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingIndexingConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__795a414274816fcb90899050038da3c75985d34d3543f926709e1a9573c4d829)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomField")
    def put_custom_field(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingIndexingConfigurationCustomField, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72ff86cfc6f0f395cb13ccc753914505ae0c1605c6c7ebb07bd4990ba3cfd723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomField", [value]))

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        *,
        named_shadow_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param named_shadow_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_indexing_configuration#named_shadow_names IotIndexingConfiguration#named_shadow_names}.
        '''
        value = IotIndexingConfigurationThingIndexingConfigurationFilter(
            named_shadow_names=named_shadow_names
        )

        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="putManagedField")
    def put_managed_field(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingIndexingConfigurationManagedField, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__260a80c2d7380d0389c5faebc2b5757b8ddc45a8474f07099d5bf30cf673fca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putManagedField", [value]))

    @jsii.member(jsii_name="resetCustomField")
    def reset_custom_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomField", []))

    @jsii.member(jsii_name="resetDeviceDefenderIndexingMode")
    def reset_device_defender_indexing_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceDefenderIndexingMode", []))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetManagedField")
    def reset_managed_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedField", []))

    @jsii.member(jsii_name="resetNamedShadowIndexingMode")
    def reset_named_shadow_indexing_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamedShadowIndexingMode", []))

    @jsii.member(jsii_name="resetThingConnectivityIndexingMode")
    def reset_thing_connectivity_indexing_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThingConnectivityIndexingMode", []))

    @builtins.property
    @jsii.member(jsii_name="customField")
    def custom_field(
        self,
    ) -> IotIndexingConfigurationThingIndexingConfigurationCustomFieldList:
        return typing.cast(IotIndexingConfigurationThingIndexingConfigurationCustomFieldList, jsii.get(self, "customField"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(
        self,
    ) -> IotIndexingConfigurationThingIndexingConfigurationFilterOutputReference:
        return typing.cast(IotIndexingConfigurationThingIndexingConfigurationFilterOutputReference, jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="managedField")
    def managed_field(
        self,
    ) -> IotIndexingConfigurationThingIndexingConfigurationManagedFieldList:
        return typing.cast(IotIndexingConfigurationThingIndexingConfigurationManagedFieldList, jsii.get(self, "managedField"))

    @builtins.property
    @jsii.member(jsii_name="customFieldInput")
    def custom_field_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationCustomField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationCustomField]]], jsii.get(self, "customFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceDefenderIndexingModeInput")
    def device_defender_indexing_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceDefenderIndexingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[IotIndexingConfigurationThingIndexingConfigurationFilter]:
        return typing.cast(typing.Optional[IotIndexingConfigurationThingIndexingConfigurationFilter], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="managedFieldInput")
    def managed_field_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationManagedField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationManagedField]]], jsii.get(self, "managedFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="namedShadowIndexingModeInput")
    def named_shadow_indexing_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namedShadowIndexingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="thingConnectivityIndexingModeInput")
    def thing_connectivity_indexing_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thingConnectivityIndexingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="thingIndexingModeInput")
    def thing_indexing_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thingIndexingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceDefenderIndexingMode")
    def device_defender_indexing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceDefenderIndexingMode"))

    @device_defender_indexing_mode.setter
    def device_defender_indexing_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05ae1ffac5e71bec99462730fae9acbcc3740013f0d32def637207a39290f087)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceDefenderIndexingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namedShadowIndexingMode")
    def named_shadow_indexing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namedShadowIndexingMode"))

    @named_shadow_indexing_mode.setter
    def named_shadow_indexing_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcffe50d8311b5499cb1aedd709e3741e7db586243d8b1ca235541be0be835dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namedShadowIndexingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thingConnectivityIndexingMode")
    def thing_connectivity_indexing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thingConnectivityIndexingMode"))

    @thing_connectivity_indexing_mode.setter
    def thing_connectivity_indexing_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e451221e812367962568e2aa8ced6530cd8938d589a3262f0575b7fe6a90a55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thingConnectivityIndexingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thingIndexingMode")
    def thing_indexing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thingIndexingMode"))

    @thing_indexing_mode.setter
    def thing_indexing_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00b31318c2928e827dbaed967dcab776fa0f74d3c583cd173f34d6e84ca7d526)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thingIndexingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IotIndexingConfigurationThingIndexingConfiguration]:
        return typing.cast(typing.Optional[IotIndexingConfigurationThingIndexingConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotIndexingConfigurationThingIndexingConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e0339bf92a4ead8b20394d7d91121e6f198eded3d977219d64d43bec6ceba1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "IotIndexingConfiguration",
    "IotIndexingConfigurationConfig",
    "IotIndexingConfigurationThingGroupIndexingConfiguration",
    "IotIndexingConfigurationThingGroupIndexingConfigurationCustomField",
    "IotIndexingConfigurationThingGroupIndexingConfigurationCustomFieldList",
    "IotIndexingConfigurationThingGroupIndexingConfigurationCustomFieldOutputReference",
    "IotIndexingConfigurationThingGroupIndexingConfigurationManagedField",
    "IotIndexingConfigurationThingGroupIndexingConfigurationManagedFieldList",
    "IotIndexingConfigurationThingGroupIndexingConfigurationManagedFieldOutputReference",
    "IotIndexingConfigurationThingGroupIndexingConfigurationOutputReference",
    "IotIndexingConfigurationThingIndexingConfiguration",
    "IotIndexingConfigurationThingIndexingConfigurationCustomField",
    "IotIndexingConfigurationThingIndexingConfigurationCustomFieldList",
    "IotIndexingConfigurationThingIndexingConfigurationCustomFieldOutputReference",
    "IotIndexingConfigurationThingIndexingConfigurationFilter",
    "IotIndexingConfigurationThingIndexingConfigurationFilterOutputReference",
    "IotIndexingConfigurationThingIndexingConfigurationManagedField",
    "IotIndexingConfigurationThingIndexingConfigurationManagedFieldList",
    "IotIndexingConfigurationThingIndexingConfigurationManagedFieldOutputReference",
    "IotIndexingConfigurationThingIndexingConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__26a60a3f993047844e3effdb22da389b88ff3e87253d8acb440996e6cc466541(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    id: typing.Optional[builtins.str] = None,
    thing_group_indexing_configuration: typing.Optional[typing.Union[IotIndexingConfigurationThingGroupIndexingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    thing_indexing_configuration: typing.Optional[typing.Union[IotIndexingConfigurationThingIndexingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__de9273eba949a8d35c719561397d95900d3065f03398e7fe1991b3f258068a4f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b4231912647940e6f6a1daca0145618b74d484fc6ae2907ab14d1a4bdb352e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__116ad2196434c2c1c05b7ada1610c1f989c57c4b4c7f08bd7d89ebc9c8655eb9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    thing_group_indexing_configuration: typing.Optional[typing.Union[IotIndexingConfigurationThingGroupIndexingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    thing_indexing_configuration: typing.Optional[typing.Union[IotIndexingConfigurationThingIndexingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e6b06369639a4284ed0a2a38af23b40352b68452b0a7daf11c5ad0494d550b9(
    *,
    thing_group_indexing_mode: builtins.str,
    custom_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingGroupIndexingConfigurationCustomField, typing.Dict[builtins.str, typing.Any]]]]] = None,
    managed_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingGroupIndexingConfigurationManagedField, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68dc1fc89579048b4ffc6db22bd66563344564415aa3fa2db4c92eaf059b6071(
    *,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__743545bb0a1b8b894bb70d09e0a09eaf9d90124ef8f188cdb318ee00500b2b34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ace513921ef3e5c373b0449cdb03a8c0137cc56b20801459cfc0f3eb2eb47cc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77727ca6e97d9da7c3456ccb6882d1defb86268fd7cea202b54581003d133322(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72a82046a9195e2a6010f1b140b1ee4c850a1dd80740c16b6aab2d95f713b74f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a09a433b974956e8836948837c5511b95ef39baa4e644cbecf336570e80b297(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de1cb06f71f3403ac3ac6953916bfc979ee7fcc566f4addbea7b2f152f60ddaf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationCustomField]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e8c2b90665ab3ea96cbc968a444a60410bf97bb4a632b641aa7a713eaee8d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e6b4105931e55a78d2817606391d6655ac8763cac175794a009ab4bd36067d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__038b50efa9524a4634f9faf7149e71e526ab7aa4e275ac8403f191328483b05a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aa244bb0ca83d0bd53d83e32cff38fee51270a1c9c2209ccd395ff4d477515a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingGroupIndexingConfigurationCustomField]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58342f0e119be8ba799dc9d2ae1e93aef02b8ef6c7c2da24b91cbd042a74d2c8(
    *,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d3e50e799105c4b3723a84fec9be84a9880049acf1c05e49c8c783d8fe2350(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0835db3c630886afad9ced20fa4149d664d44c7ab25d7ee373abbfb3aea2ea07(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c1030b4d6ced9abd592e519229ed1906d6d60ea041561b23cca66a941e6edd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50126d8f4f95890967038a8c636a54d19a6767b9f8461cd3b67edf50feeeb12b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dc9981028f77ad7f5e16f3b42ec1c79330c933e8ee97d3bab38b267d06ad1c5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39794c2bfead7871bd77106cb72ff3acdbcc82d1502b49a660ba055022471f08(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationManagedField]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ba477fbdd198a6593da2fc895127749d431aca68bb4873586b68944306b3aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb33c22cb4204122a711f555ccf592f7cc9d53fdd7e71540018e8c10d4cf3628(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6868c81ff7b09e840794b6dbe24cd52adc8de1e63df53d91089da22895581b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad041df3a249b19edf21764f74a097debaf808ab3bdfae002e1876db7e35620(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingGroupIndexingConfigurationManagedField]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__592bdc470f4b4180dde08023b1166fdc0dc820556f5d9580906362628c61e225(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cde084ab0e1d1f35c61c076b4f518f15b4d288258d4a5b42276fa2c659a8401(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingGroupIndexingConfigurationCustomField, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e98bfb54ad625f3f4d56040e9039582cb945c33a4f57e2d2a4da633962a88653(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingGroupIndexingConfigurationManagedField, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__113e715f3be9ffef6c912d704bc92dc37d7c949928b96bbd60bf4cc95ce69d6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931d21e5902521208f28ff5be8b2132b62e0faddf8d7ba4cc9a647771f832882(
    value: typing.Optional[IotIndexingConfigurationThingGroupIndexingConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c037a24b6b1595bbe40de08bb7169ea0b867aecc7b33fffe4276220fcd9f6134(
    *,
    thing_indexing_mode: builtins.str,
    custom_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingIndexingConfigurationCustomField, typing.Dict[builtins.str, typing.Any]]]]] = None,
    device_defender_indexing_mode: typing.Optional[builtins.str] = None,
    filter: typing.Optional[typing.Union[IotIndexingConfigurationThingIndexingConfigurationFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingIndexingConfigurationManagedField, typing.Dict[builtins.str, typing.Any]]]]] = None,
    named_shadow_indexing_mode: typing.Optional[builtins.str] = None,
    thing_connectivity_indexing_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__068f405a2beaac36f4769e2cafbf1c9cc308c4c521a33132087f3dafa54d8d59(
    *,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fcf4e50ab1db3313bd7971e72614f2ec06a1ddf314fbeb45b41b4f59647cb6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b4308d4edd55cf26b870974ed7ea77f48c4a83a9ea7f70d997b7c9e576949e3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d29a207b92a2ebeb0d9b66d1a949aae6e9d2bb22f19e1e1719522903c5edae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a772f83aa63c27d24f9993f445099737883ba96378f2d9d96d595e4ce803eca(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__462a1057051e073d8c79c6a1ec4ce755bc70855c200d13445f4f682a9c9447fe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47fbb835a0d6032dd2286a89d2b81ab82c624ce64c17309927e506a95267de97(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationCustomField]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e02edd06ccaab4f4d5669020ae72c0d7c74436e50f54d705d2ce44ece8c32c86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcccfd9610b3482dc8fa18f8e829ddfde652c7f3637112d1404e2930a52a330b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9569b839f2808d078cb12c04bfe689e942997c8eab42c4656638f91e2ad3f50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62f431bc022f3acbe89069e9bc57f34d647637fb0b0008ad8c1661236d8dedfd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingIndexingConfigurationCustomField]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__965ac93ec4a9376fbcc3aebcd49ccf00aa8fbf01a56df786646ec57ea42c490d(
    *,
    named_shadow_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa9b90b4f07b293ba98fe17ef977161fec38b804eeb833be5253b93a9371809(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__017aae8ae984cc2ed6babd94b9a950aa75858d5689654d0ffa7cdbe5c53bde8d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55bec91c42b7addac079ac1e16b83d0c593f0007fbd988521fd6c93f73b1eb59(
    value: typing.Optional[IotIndexingConfigurationThingIndexingConfigurationFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__126214ad8112dcbd95a9b06f4cb68e9f38740ff7850c247376ef013338cf7e2a(
    *,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a55f822a73625f1af717bf3ddc944ab57b2132e05db209d82ec37122301dffc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__027606b8cb8dd96fc9e06c982b9ca99059a73d3043d72998bb0e289520163bed(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c97597885856c353d3b8acbf93b3763eeaf8c8de47c3ba4341498a5865f14d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e2226607410fa0b2ca8ce33c328264128085629ba72868daea730624bff003c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b74ef6c24612ccccd48d95f6199649fb22ad263d08e13ca91238a9abadc411be(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c89b92d2577086f6162058eeba70f321b29a05361d3285c06e7796064be35bf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationManagedField]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4305e1665f4ccf0a0a621370ef3c30daf3dbd819b6b119939980ed55fcfee1e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28ca837753c59dd9770f070c998d423a68690d0d8636ef6ac8ea7922f4e2d918(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3933346477b96315cc7fec15546ad6c556f00efcc3198d57c36bf56b48b0fa28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea94d63dc191a80f6767ba7936ffb452d02a0a358126f68728b9721f048bc93(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingIndexingConfigurationManagedField]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__795a414274816fcb90899050038da3c75985d34d3543f926709e1a9573c4d829(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ff86cfc6f0f395cb13ccc753914505ae0c1605c6c7ebb07bd4990ba3cfd723(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingIndexingConfigurationCustomField, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__260a80c2d7380d0389c5faebc2b5757b8ddc45a8474f07099d5bf30cf673fca4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingIndexingConfigurationManagedField, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05ae1ffac5e71bec99462730fae9acbcc3740013f0d32def637207a39290f087(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcffe50d8311b5499cb1aedd709e3741e7db586243d8b1ca235541be0be835dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e451221e812367962568e2aa8ced6530cd8938d589a3262f0575b7fe6a90a55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b31318c2928e827dbaed967dcab776fa0f74d3c583cd173f34d6e84ca7d526(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0339bf92a4ead8b20394d7d91121e6f198eded3d977219d64d43bec6ceba1f(
    value: typing.Optional[IotIndexingConfigurationThingIndexingConfiguration],
) -> None:
    """Type checking stubs"""
    pass
