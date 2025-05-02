r'''
# `aws_connect_user_hierarchy_structure`

Refer to the Terraform Registry for docs: [`aws_connect_user_hierarchy_structure`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure).
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


class ConnectUserHierarchyStructure(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructure",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure aws_connect_user_hierarchy_structure}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        hierarchy_structure: typing.Union["ConnectUserHierarchyStructureHierarchyStructure", typing.Dict[builtins.str, typing.Any]],
        instance_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure aws_connect_user_hierarchy_structure} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param hierarchy_structure: hierarchy_structure block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#hierarchy_structure ConnectUserHierarchyStructure#hierarchy_structure}
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#instance_id ConnectUserHierarchyStructure#instance_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#id ConnectUserHierarchyStructure#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a9ecc9636e84f6f1919ed4e1fff48ead0497d233702d01f097f28673d5dc44f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ConnectUserHierarchyStructureConfig(
            hierarchy_structure=hierarchy_structure,
            instance_id=instance_id,
            id=id,
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
        '''Generates CDKTF code for importing a ConnectUserHierarchyStructure resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ConnectUserHierarchyStructure to import.
        :param import_from_id: The id of the existing ConnectUserHierarchyStructure that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ConnectUserHierarchyStructure to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59a11bc970da4fe907a5f9720ff02a9e3b3289aa12a321fc19eb1de6cd82e8ec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putHierarchyStructure")
    def put_hierarchy_structure(
        self,
        *,
        level_five: typing.Optional[typing.Union["ConnectUserHierarchyStructureHierarchyStructureLevelFive", typing.Dict[builtins.str, typing.Any]]] = None,
        level_four: typing.Optional[typing.Union["ConnectUserHierarchyStructureHierarchyStructureLevelFour", typing.Dict[builtins.str, typing.Any]]] = None,
        level_one: typing.Optional[typing.Union["ConnectUserHierarchyStructureHierarchyStructureLevelOne", typing.Dict[builtins.str, typing.Any]]] = None,
        level_three: typing.Optional[typing.Union["ConnectUserHierarchyStructureHierarchyStructureLevelThree", typing.Dict[builtins.str, typing.Any]]] = None,
        level_two: typing.Optional[typing.Union["ConnectUserHierarchyStructureHierarchyStructureLevelTwo", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param level_five: level_five block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#level_five ConnectUserHierarchyStructure#level_five}
        :param level_four: level_four block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#level_four ConnectUserHierarchyStructure#level_four}
        :param level_one: level_one block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#level_one ConnectUserHierarchyStructure#level_one}
        :param level_three: level_three block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#level_three ConnectUserHierarchyStructure#level_three}
        :param level_two: level_two block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#level_two ConnectUserHierarchyStructure#level_two}
        '''
        value = ConnectUserHierarchyStructureHierarchyStructure(
            level_five=level_five,
            level_four=level_four,
            level_one=level_one,
            level_three=level_three,
            level_two=level_two,
        )

        return typing.cast(None, jsii.invoke(self, "putHierarchyStructure", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="hierarchyStructure")
    def hierarchy_structure(
        self,
    ) -> "ConnectUserHierarchyStructureHierarchyStructureOutputReference":
        return typing.cast("ConnectUserHierarchyStructureHierarchyStructureOutputReference", jsii.get(self, "hierarchyStructure"))

    @builtins.property
    @jsii.member(jsii_name="hierarchyStructureInput")
    def hierarchy_structure_input(
        self,
    ) -> typing.Optional["ConnectUserHierarchyStructureHierarchyStructure"]:
        return typing.cast(typing.Optional["ConnectUserHierarchyStructureHierarchyStructure"], jsii.get(self, "hierarchyStructureInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdInput")
    def instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16af0530bf433f583cb296e5c456708f27a310aed24afb0fdf12251ffe9e9827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0752d9cb5fcef8fc8a35599d55d12736ed1e498774714587fa5b88e3a3f55fe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "hierarchy_structure": "hierarchyStructure",
        "instance_id": "instanceId",
        "id": "id",
    },
)
class ConnectUserHierarchyStructureConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        hierarchy_structure: typing.Union["ConnectUserHierarchyStructureHierarchyStructure", typing.Dict[builtins.str, typing.Any]],
        instance_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param hierarchy_structure: hierarchy_structure block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#hierarchy_structure ConnectUserHierarchyStructure#hierarchy_structure}
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#instance_id ConnectUserHierarchyStructure#instance_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#id ConnectUserHierarchyStructure#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(hierarchy_structure, dict):
            hierarchy_structure = ConnectUserHierarchyStructureHierarchyStructure(**hierarchy_structure)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__145451ce2d9398949a194a591627bc458f5d27df9190aa43f75a34002618a3ff)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument hierarchy_structure", value=hierarchy_structure, expected_type=type_hints["hierarchy_structure"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hierarchy_structure": hierarchy_structure,
            "instance_id": instance_id,
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
    def hierarchy_structure(self) -> "ConnectUserHierarchyStructureHierarchyStructure":
        '''hierarchy_structure block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#hierarchy_structure ConnectUserHierarchyStructure#hierarchy_structure}
        '''
        result = self._values.get("hierarchy_structure")
        assert result is not None, "Required property 'hierarchy_structure' is missing"
        return typing.cast("ConnectUserHierarchyStructureHierarchyStructure", result)

    @builtins.property
    def instance_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#instance_id ConnectUserHierarchyStructure#instance_id}.'''
        result = self._values.get("instance_id")
        assert result is not None, "Required property 'instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#id ConnectUserHierarchyStructure#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConnectUserHierarchyStructureConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructure",
    jsii_struct_bases=[],
    name_mapping={
        "level_five": "levelFive",
        "level_four": "levelFour",
        "level_one": "levelOne",
        "level_three": "levelThree",
        "level_two": "levelTwo",
    },
)
class ConnectUserHierarchyStructureHierarchyStructure:
    def __init__(
        self,
        *,
        level_five: typing.Optional[typing.Union["ConnectUserHierarchyStructureHierarchyStructureLevelFive", typing.Dict[builtins.str, typing.Any]]] = None,
        level_four: typing.Optional[typing.Union["ConnectUserHierarchyStructureHierarchyStructureLevelFour", typing.Dict[builtins.str, typing.Any]]] = None,
        level_one: typing.Optional[typing.Union["ConnectUserHierarchyStructureHierarchyStructureLevelOne", typing.Dict[builtins.str, typing.Any]]] = None,
        level_three: typing.Optional[typing.Union["ConnectUserHierarchyStructureHierarchyStructureLevelThree", typing.Dict[builtins.str, typing.Any]]] = None,
        level_two: typing.Optional[typing.Union["ConnectUserHierarchyStructureHierarchyStructureLevelTwo", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param level_five: level_five block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#level_five ConnectUserHierarchyStructure#level_five}
        :param level_four: level_four block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#level_four ConnectUserHierarchyStructure#level_four}
        :param level_one: level_one block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#level_one ConnectUserHierarchyStructure#level_one}
        :param level_three: level_three block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#level_three ConnectUserHierarchyStructure#level_three}
        :param level_two: level_two block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#level_two ConnectUserHierarchyStructure#level_two}
        '''
        if isinstance(level_five, dict):
            level_five = ConnectUserHierarchyStructureHierarchyStructureLevelFive(**level_five)
        if isinstance(level_four, dict):
            level_four = ConnectUserHierarchyStructureHierarchyStructureLevelFour(**level_four)
        if isinstance(level_one, dict):
            level_one = ConnectUserHierarchyStructureHierarchyStructureLevelOne(**level_one)
        if isinstance(level_three, dict):
            level_three = ConnectUserHierarchyStructureHierarchyStructureLevelThree(**level_three)
        if isinstance(level_two, dict):
            level_two = ConnectUserHierarchyStructureHierarchyStructureLevelTwo(**level_two)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eb37e395410a0b3a84b59164943179295bedfa231b0d8f8c2051c9fa9a497f9)
            check_type(argname="argument level_five", value=level_five, expected_type=type_hints["level_five"])
            check_type(argname="argument level_four", value=level_four, expected_type=type_hints["level_four"])
            check_type(argname="argument level_one", value=level_one, expected_type=type_hints["level_one"])
            check_type(argname="argument level_three", value=level_three, expected_type=type_hints["level_three"])
            check_type(argname="argument level_two", value=level_two, expected_type=type_hints["level_two"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if level_five is not None:
            self._values["level_five"] = level_five
        if level_four is not None:
            self._values["level_four"] = level_four
        if level_one is not None:
            self._values["level_one"] = level_one
        if level_three is not None:
            self._values["level_three"] = level_three
        if level_two is not None:
            self._values["level_two"] = level_two

    @builtins.property
    def level_five(
        self,
    ) -> typing.Optional["ConnectUserHierarchyStructureHierarchyStructureLevelFive"]:
        '''level_five block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#level_five ConnectUserHierarchyStructure#level_five}
        '''
        result = self._values.get("level_five")
        return typing.cast(typing.Optional["ConnectUserHierarchyStructureHierarchyStructureLevelFive"], result)

    @builtins.property
    def level_four(
        self,
    ) -> typing.Optional["ConnectUserHierarchyStructureHierarchyStructureLevelFour"]:
        '''level_four block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#level_four ConnectUserHierarchyStructure#level_four}
        '''
        result = self._values.get("level_four")
        return typing.cast(typing.Optional["ConnectUserHierarchyStructureHierarchyStructureLevelFour"], result)

    @builtins.property
    def level_one(
        self,
    ) -> typing.Optional["ConnectUserHierarchyStructureHierarchyStructureLevelOne"]:
        '''level_one block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#level_one ConnectUserHierarchyStructure#level_one}
        '''
        result = self._values.get("level_one")
        return typing.cast(typing.Optional["ConnectUserHierarchyStructureHierarchyStructureLevelOne"], result)

    @builtins.property
    def level_three(
        self,
    ) -> typing.Optional["ConnectUserHierarchyStructureHierarchyStructureLevelThree"]:
        '''level_three block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#level_three ConnectUserHierarchyStructure#level_three}
        '''
        result = self._values.get("level_three")
        return typing.cast(typing.Optional["ConnectUserHierarchyStructureHierarchyStructureLevelThree"], result)

    @builtins.property
    def level_two(
        self,
    ) -> typing.Optional["ConnectUserHierarchyStructureHierarchyStructureLevelTwo"]:
        '''level_two block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#level_two ConnectUserHierarchyStructure#level_two}
        '''
        result = self._values.get("level_two")
        return typing.cast(typing.Optional["ConnectUserHierarchyStructureHierarchyStructureLevelTwo"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConnectUserHierarchyStructureHierarchyStructure(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructureLevelFive",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ConnectUserHierarchyStructureHierarchyStructureLevelFive:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74b03c79896a414749107a03d77c41dfa2f7735f25f66fc767b7a7ef540bd67e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConnectUserHierarchyStructureHierarchyStructureLevelFive(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConnectUserHierarchyStructureHierarchyStructureLevelFiveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructureLevelFiveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f104c901807eeb9f2ffe38a7e19cd77f7b68e4af676a862c966fd4de54fa2bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__08e48248f04ec2278b1cacbcd58d047ec46ccff401cb05d613aeecf9476d9f00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFive]:
        return typing.cast(typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFive], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFive],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57feb8d655901fffedf3c84fee1da37fb69f72bf2206f614e8f3eea73a3fa386)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructureLevelFour",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ConnectUserHierarchyStructureHierarchyStructureLevelFour:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81400cf98f8308334e877fdf5678f7508a37cb81137b86f4a0773286511713fb)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConnectUserHierarchyStructureHierarchyStructureLevelFour(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConnectUserHierarchyStructureHierarchyStructureLevelFourOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructureLevelFourOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c705f07efd490e98c62d8d19162a887bddd17fff97ef970f6712af49bd30f65)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c37853f265a87f2d3024e92e7b67753cc317560948ef57615dffbff158e0adb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFour]:
        return typing.cast(typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFour], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFour],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d037c2c5476d8886313ad288c742fc6dbb97e77ab0d6b1ff9950f4bef94c9698)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructureLevelOne",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ConnectUserHierarchyStructureHierarchyStructureLevelOne:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1ca1346ff95cd7175d7557b8b13aa85787f27e73aa6bb0391d6961082bee8d2)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConnectUserHierarchyStructureHierarchyStructureLevelOne(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConnectUserHierarchyStructureHierarchyStructureLevelOneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructureLevelOneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ce3839b548cd7b73d30e7993d2a6bdf74bbb675de5603d9b27e66701623e922)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__211cc59e3dbc688416b37ecc91630a731c94235425daed6d8842e18adbb55f26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelOne]:
        return typing.cast(typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelOne], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelOne],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e581eb3039ab7228676e1f63bdfacee88d590fe796402d01b92320411b0518d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructureLevelThree",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ConnectUserHierarchyStructureHierarchyStructureLevelThree:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8e026ba1ab8d64bfdf9e4b1d4ba14adacc2806163890e1beef805e2c1b0da45)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConnectUserHierarchyStructureHierarchyStructureLevelThree(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConnectUserHierarchyStructureHierarchyStructureLevelThreeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructureLevelThreeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81b3b6e96d520d07c4075f4b4506cb054e2b3e8153126e3a1a2cf64e2419410c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5206fde508a86f5047005ed239c63895c9267fd5c42bd2275c8ad9d74d308ed8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelThree]:
        return typing.cast(typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelThree], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelThree],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fb20adbc65907684e6a78b4911744164ef87ee759adc7d237913c19aa98591a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructureLevelTwo",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ConnectUserHierarchyStructureHierarchyStructureLevelTwo:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2152b058ba43c1f8b4a2078d5f044655d467552a56b27ba73765b5a6ce04b241)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConnectUserHierarchyStructureHierarchyStructureLevelTwo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConnectUserHierarchyStructureHierarchyStructureLevelTwoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructureLevelTwoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf19f884351805202b5105da091c4cce3f28743011916a64b1aa50470ef9d22e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0d0d9ee4a2b4121ee076b9ab7fb8568212f6327044f5cdd82470af7db534b19d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelTwo]:
        return typing.cast(typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelTwo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelTwo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc7290a9c1f64037754310f288572f78c530e85c6fa7ea5418141b2710af0d11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ConnectUserHierarchyStructureHierarchyStructureOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructureOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__080f1e8ad8fe864e318f194c80b89ef5bcf41a1c6cb0f2984cca14ad27d96faa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLevelFive")
    def put_level_five(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.
        '''
        value = ConnectUserHierarchyStructureHierarchyStructureLevelFive(name=name)

        return typing.cast(None, jsii.invoke(self, "putLevelFive", [value]))

    @jsii.member(jsii_name="putLevelFour")
    def put_level_four(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.
        '''
        value = ConnectUserHierarchyStructureHierarchyStructureLevelFour(name=name)

        return typing.cast(None, jsii.invoke(self, "putLevelFour", [value]))

    @jsii.member(jsii_name="putLevelOne")
    def put_level_one(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.
        '''
        value = ConnectUserHierarchyStructureHierarchyStructureLevelOne(name=name)

        return typing.cast(None, jsii.invoke(self, "putLevelOne", [value]))

    @jsii.member(jsii_name="putLevelThree")
    def put_level_three(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.
        '''
        value = ConnectUserHierarchyStructureHierarchyStructureLevelThree(name=name)

        return typing.cast(None, jsii.invoke(self, "putLevelThree", [value]))

    @jsii.member(jsii_name="putLevelTwo")
    def put_level_two(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.
        '''
        value = ConnectUserHierarchyStructureHierarchyStructureLevelTwo(name=name)

        return typing.cast(None, jsii.invoke(self, "putLevelTwo", [value]))

    @jsii.member(jsii_name="resetLevelFive")
    def reset_level_five(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLevelFive", []))

    @jsii.member(jsii_name="resetLevelFour")
    def reset_level_four(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLevelFour", []))

    @jsii.member(jsii_name="resetLevelOne")
    def reset_level_one(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLevelOne", []))

    @jsii.member(jsii_name="resetLevelThree")
    def reset_level_three(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLevelThree", []))

    @jsii.member(jsii_name="resetLevelTwo")
    def reset_level_two(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLevelTwo", []))

    @builtins.property
    @jsii.member(jsii_name="levelFive")
    def level_five(
        self,
    ) -> ConnectUserHierarchyStructureHierarchyStructureLevelFiveOutputReference:
        return typing.cast(ConnectUserHierarchyStructureHierarchyStructureLevelFiveOutputReference, jsii.get(self, "levelFive"))

    @builtins.property
    @jsii.member(jsii_name="levelFour")
    def level_four(
        self,
    ) -> ConnectUserHierarchyStructureHierarchyStructureLevelFourOutputReference:
        return typing.cast(ConnectUserHierarchyStructureHierarchyStructureLevelFourOutputReference, jsii.get(self, "levelFour"))

    @builtins.property
    @jsii.member(jsii_name="levelOne")
    def level_one(
        self,
    ) -> ConnectUserHierarchyStructureHierarchyStructureLevelOneOutputReference:
        return typing.cast(ConnectUserHierarchyStructureHierarchyStructureLevelOneOutputReference, jsii.get(self, "levelOne"))

    @builtins.property
    @jsii.member(jsii_name="levelThree")
    def level_three(
        self,
    ) -> ConnectUserHierarchyStructureHierarchyStructureLevelThreeOutputReference:
        return typing.cast(ConnectUserHierarchyStructureHierarchyStructureLevelThreeOutputReference, jsii.get(self, "levelThree"))

    @builtins.property
    @jsii.member(jsii_name="levelTwo")
    def level_two(
        self,
    ) -> ConnectUserHierarchyStructureHierarchyStructureLevelTwoOutputReference:
        return typing.cast(ConnectUserHierarchyStructureHierarchyStructureLevelTwoOutputReference, jsii.get(self, "levelTwo"))

    @builtins.property
    @jsii.member(jsii_name="levelFiveInput")
    def level_five_input(
        self,
    ) -> typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFive]:
        return typing.cast(typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFive], jsii.get(self, "levelFiveInput"))

    @builtins.property
    @jsii.member(jsii_name="levelFourInput")
    def level_four_input(
        self,
    ) -> typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFour]:
        return typing.cast(typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFour], jsii.get(self, "levelFourInput"))

    @builtins.property
    @jsii.member(jsii_name="levelOneInput")
    def level_one_input(
        self,
    ) -> typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelOne]:
        return typing.cast(typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelOne], jsii.get(self, "levelOneInput"))

    @builtins.property
    @jsii.member(jsii_name="levelThreeInput")
    def level_three_input(
        self,
    ) -> typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelThree]:
        return typing.cast(typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelThree], jsii.get(self, "levelThreeInput"))

    @builtins.property
    @jsii.member(jsii_name="levelTwoInput")
    def level_two_input(
        self,
    ) -> typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelTwo]:
        return typing.cast(typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelTwo], jsii.get(self, "levelTwoInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ConnectUserHierarchyStructureHierarchyStructure]:
        return typing.cast(typing.Optional[ConnectUserHierarchyStructureHierarchyStructure], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructure],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb27f948b09af5ad73ce2133f44b81a28ecd644c0d0ab7f49f2f0c5e3eb42350)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ConnectUserHierarchyStructure",
    "ConnectUserHierarchyStructureConfig",
    "ConnectUserHierarchyStructureHierarchyStructure",
    "ConnectUserHierarchyStructureHierarchyStructureLevelFive",
    "ConnectUserHierarchyStructureHierarchyStructureLevelFiveOutputReference",
    "ConnectUserHierarchyStructureHierarchyStructureLevelFour",
    "ConnectUserHierarchyStructureHierarchyStructureLevelFourOutputReference",
    "ConnectUserHierarchyStructureHierarchyStructureLevelOne",
    "ConnectUserHierarchyStructureHierarchyStructureLevelOneOutputReference",
    "ConnectUserHierarchyStructureHierarchyStructureLevelThree",
    "ConnectUserHierarchyStructureHierarchyStructureLevelThreeOutputReference",
    "ConnectUserHierarchyStructureHierarchyStructureLevelTwo",
    "ConnectUserHierarchyStructureHierarchyStructureLevelTwoOutputReference",
    "ConnectUserHierarchyStructureHierarchyStructureOutputReference",
]

publication.publish()

def _typecheckingstub__7a9ecc9636e84f6f1919ed4e1fff48ead0497d233702d01f097f28673d5dc44f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    hierarchy_structure: typing.Union[ConnectUserHierarchyStructureHierarchyStructure, typing.Dict[builtins.str, typing.Any]],
    instance_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__59a11bc970da4fe907a5f9720ff02a9e3b3289aa12a321fc19eb1de6cd82e8ec(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16af0530bf433f583cb296e5c456708f27a310aed24afb0fdf12251ffe9e9827(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0752d9cb5fcef8fc8a35599d55d12736ed1e498774714587fa5b88e3a3f55fe6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145451ce2d9398949a194a591627bc458f5d27df9190aa43f75a34002618a3ff(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hierarchy_structure: typing.Union[ConnectUserHierarchyStructureHierarchyStructure, typing.Dict[builtins.str, typing.Any]],
    instance_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb37e395410a0b3a84b59164943179295bedfa231b0d8f8c2051c9fa9a497f9(
    *,
    level_five: typing.Optional[typing.Union[ConnectUserHierarchyStructureHierarchyStructureLevelFive, typing.Dict[builtins.str, typing.Any]]] = None,
    level_four: typing.Optional[typing.Union[ConnectUserHierarchyStructureHierarchyStructureLevelFour, typing.Dict[builtins.str, typing.Any]]] = None,
    level_one: typing.Optional[typing.Union[ConnectUserHierarchyStructureHierarchyStructureLevelOne, typing.Dict[builtins.str, typing.Any]]] = None,
    level_three: typing.Optional[typing.Union[ConnectUserHierarchyStructureHierarchyStructureLevelThree, typing.Dict[builtins.str, typing.Any]]] = None,
    level_two: typing.Optional[typing.Union[ConnectUserHierarchyStructureHierarchyStructureLevelTwo, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b03c79896a414749107a03d77c41dfa2f7735f25f66fc767b7a7ef540bd67e(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f104c901807eeb9f2ffe38a7e19cd77f7b68e4af676a862c966fd4de54fa2bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08e48248f04ec2278b1cacbcd58d047ec46ccff401cb05d613aeecf9476d9f00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57feb8d655901fffedf3c84fee1da37fb69f72bf2206f614e8f3eea73a3fa386(
    value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFive],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81400cf98f8308334e877fdf5678f7508a37cb81137b86f4a0773286511713fb(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c705f07efd490e98c62d8d19162a887bddd17fff97ef970f6712af49bd30f65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37853f265a87f2d3024e92e7b67753cc317560948ef57615dffbff158e0adb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d037c2c5476d8886313ad288c742fc6dbb97e77ab0d6b1ff9950f4bef94c9698(
    value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFour],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ca1346ff95cd7175d7557b8b13aa85787f27e73aa6bb0391d6961082bee8d2(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce3839b548cd7b73d30e7993d2a6bdf74bbb675de5603d9b27e66701623e922(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211cc59e3dbc688416b37ecc91630a731c94235425daed6d8842e18adbb55f26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e581eb3039ab7228676e1f63bdfacee88d590fe796402d01b92320411b0518d3(
    value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelOne],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8e026ba1ab8d64bfdf9e4b1d4ba14adacc2806163890e1beef805e2c1b0da45(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b3b6e96d520d07c4075f4b4506cb054e2b3e8153126e3a1a2cf64e2419410c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5206fde508a86f5047005ed239c63895c9267fd5c42bd2275c8ad9d74d308ed8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb20adbc65907684e6a78b4911744164ef87ee759adc7d237913c19aa98591a(
    value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelThree],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2152b058ba43c1f8b4a2078d5f044655d467552a56b27ba73765b5a6ce04b241(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf19f884351805202b5105da091c4cce3f28743011916a64b1aa50470ef9d22e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d0d9ee4a2b4121ee076b9ab7fb8568212f6327044f5cdd82470af7db534b19d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc7290a9c1f64037754310f288572f78c530e85c6fa7ea5418141b2710af0d11(
    value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelTwo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__080f1e8ad8fe864e318f194c80b89ef5bcf41a1c6cb0f2984cca14ad27d96faa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb27f948b09af5ad73ce2133f44b81a28ecd644c0d0ab7f49f2f0c5e3eb42350(
    value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructure],
) -> None:
    """Type checking stubs"""
    pass
