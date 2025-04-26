r'''
# `snowflake_external_volume`

Refer to the Terraform Registry for docs: [`snowflake_external_volume`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume).
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


class ExternalVolume(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalVolume.ExternalVolume",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume snowflake_external_volume}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        storage_location: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ExternalVolumeStorageLocation", typing.Dict[builtins.str, typing.Any]]]],
        allow_writes: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume snowflake_external_volume} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Identifier for the external volume; must be unique for your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#name ExternalVolume#name}
        :param storage_location: storage_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#storage_location ExternalVolume#storage_location}
        :param allow_writes: Specifies whether write operations are allowed for the external volume; must be set to TRUE for Iceberg tables that use Snowflake as the catalog. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#allow_writes ExternalVolume#allow_writes}
        :param comment: Specifies a comment for the external volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#comment ExternalVolume#comment}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#id ExternalVolume#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__636e4f0d96219e66fd47857843ef5c2587978b92327d37d4df6cc67ba8f09d26)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ExternalVolumeConfig(
            name=name,
            storage_location=storage_location,
            allow_writes=allow_writes,
            comment=comment,
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
        '''Generates CDKTF code for importing a ExternalVolume resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ExternalVolume to import.
        :param import_from_id: The id of the existing ExternalVolume that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ExternalVolume to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__788dedbd13f1a5d2b24ee051c4817d7c11f6ba5beeead6575b0253506d891307)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putStorageLocation")
    def put_storage_location(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ExternalVolumeStorageLocation", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02351dc9b70b54cb424762a8c52dd207ecf572fd63ce9f5fc5ca2a8e971a8bfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStorageLocation", [value]))

    @jsii.member(jsii_name="resetAllowWrites")
    def reset_allow_writes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowWrites", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

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
    @jsii.member(jsii_name="describeOutput")
    def describe_output(self) -> "ExternalVolumeDescribeOutputList":
        return typing.cast("ExternalVolumeDescribeOutputList", jsii.get(self, "describeOutput"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "ExternalVolumeShowOutputList":
        return typing.cast("ExternalVolumeShowOutputList", jsii.get(self, "showOutput"))

    @builtins.property
    @jsii.member(jsii_name="storageLocation")
    def storage_location(self) -> "ExternalVolumeStorageLocationList":
        return typing.cast("ExternalVolumeStorageLocationList", jsii.get(self, "storageLocation"))

    @builtins.property
    @jsii.member(jsii_name="allowWritesInput")
    def allow_writes_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allowWritesInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageLocationInput")
    def storage_location_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ExternalVolumeStorageLocation"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ExternalVolumeStorageLocation"]]], jsii.get(self, "storageLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="allowWrites")
    def allow_writes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allowWrites"))

    @allow_writes.setter
    def allow_writes(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__967f58535a539063addc420142b36191a7b4e391690a80d56d04385ea7dd3982)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowWrites", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62ca64f76359d670009d62765b3aa70cc39e1657b65c904805020c472b2fdc02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f31a146239069c37af090bf38268b7e0b84ca5f424cd3af23d77567f04b916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b33b1731f2027fa318f67349fc32287c86662c7e298b6032d9e5e2efe5af8636)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalVolume.ExternalVolumeConfig",
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
        "storage_location": "storageLocation",
        "allow_writes": "allowWrites",
        "comment": "comment",
        "id": "id",
    },
)
class ExternalVolumeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        storage_location: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ExternalVolumeStorageLocation", typing.Dict[builtins.str, typing.Any]]]],
        allow_writes: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
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
        :param name: Identifier for the external volume; must be unique for your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#name ExternalVolume#name}
        :param storage_location: storage_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#storage_location ExternalVolume#storage_location}
        :param allow_writes: Specifies whether write operations are allowed for the external volume; must be set to TRUE for Iceberg tables that use Snowflake as the catalog. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#allow_writes ExternalVolume#allow_writes}
        :param comment: Specifies a comment for the external volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#comment ExternalVolume#comment}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#id ExternalVolume#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__960589416c56707a37d97c52a7580906b92a80b5d06f93c420fcb8baaf8a7b69)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument storage_location", value=storage_location, expected_type=type_hints["storage_location"])
            check_type(argname="argument allow_writes", value=allow_writes, expected_type=type_hints["allow_writes"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "storage_location": storage_location,
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
        if allow_writes is not None:
            self._values["allow_writes"] = allow_writes
        if comment is not None:
            self._values["comment"] = comment
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
    def name(self) -> builtins.str:
        '''Identifier for the external volume;

        must be unique for your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#name ExternalVolume#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_location(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ExternalVolumeStorageLocation"]]:
        '''storage_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#storage_location ExternalVolume#storage_location}
        '''
        result = self._values.get("storage_location")
        assert result is not None, "Required property 'storage_location' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ExternalVolumeStorageLocation"]], result)

    @builtins.property
    def allow_writes(self) -> typing.Optional[builtins.str]:
        '''Specifies whether write operations are allowed for the external volume;

        must be set to TRUE for Iceberg tables that use Snowflake as the catalog. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#allow_writes ExternalVolume#allow_writes}
        '''
        result = self._values.get("allow_writes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the external volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#comment ExternalVolume#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#id ExternalVolume#id}.

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
        return "ExternalVolumeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalVolume.ExternalVolumeDescribeOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class ExternalVolumeDescribeOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalVolumeDescribeOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalVolumeDescribeOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalVolume.ExternalVolumeDescribeOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48945399a2123afc62fbd4d82ff9f2e5b5795ac5141fb622cfc9b3a032e13175)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ExternalVolumeDescribeOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7683411e68e3db9192ffe763ef8fe5992e7c42afaf5517fd8e8341d898c0c4a7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalVolumeDescribeOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa12b9d4960763dd441c56c8bc0817b87884563aee964ea85a7a260a349f1df4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55d5451deee33871e4184a4c3bf213863166a75f065904533f3aeee09fd4e233)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae88e45636de7d3307cbaf9f9f7a3014804461f212812a587369c4a26674c107)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ExternalVolumeDescribeOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalVolume.ExternalVolumeDescribeOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cb9badb1d2eadc0dd70512f84f85d03a80a68228d0cd0f112c6a87a500d5792)
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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ExternalVolumeDescribeOutput]:
        return typing.cast(typing.Optional[ExternalVolumeDescribeOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExternalVolumeDescribeOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6454fa1c47e09fd990dcea64b782528403a45b3e0280906ce59e5ecf42cb870)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalVolume.ExternalVolumeShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class ExternalVolumeShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalVolumeShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalVolumeShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalVolume.ExternalVolumeShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__626bba9a5bb7da1cc4b936e5b51274aeb4d70172200c12ea6917300ccdfbc164)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ExternalVolumeShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d9756e8643b242ca5b05b35cbb6f5c2eba0364689ba53f9d00476147103145c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalVolumeShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b0bc3827ac3f30f45077236230686ed394328bbd11b2c1343614c411001b88d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8346f223cdf4ef583785e188b17db2dec2e6a78032d8ffa5252917b72eb4cdbd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee2ba22b1de21a976c66f8eca982d35a5abfc96e85aedc6aff4804ee2f5360ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ExternalVolumeShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalVolume.ExternalVolumeShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0d0355cd7aac0743c68fa693481a4f1d3035597d7aa34b1e5e4a2d50db9ba14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allowWrites")
    def allow_writes(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "allowWrites"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ExternalVolumeShowOutput]:
        return typing.cast(typing.Optional[ExternalVolumeShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ExternalVolumeShowOutput]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abefec2d8bcd3a54fcecc9f2f61a80ae72672419777eeb02457a2fc5f3700989)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalVolume.ExternalVolumeStorageLocation",
    jsii_struct_bases=[],
    name_mapping={
        "storage_base_url": "storageBaseUrl",
        "storage_location_name": "storageLocationName",
        "storage_provider": "storageProvider",
        "azure_tenant_id": "azureTenantId",
        "encryption_kms_key_id": "encryptionKmsKeyId",
        "encryption_type": "encryptionType",
        "storage_aws_role_arn": "storageAwsRoleArn",
    },
)
class ExternalVolumeStorageLocation:
    def __init__(
        self,
        *,
        storage_base_url: builtins.str,
        storage_location_name: builtins.str,
        storage_provider: builtins.str,
        azure_tenant_id: typing.Optional[builtins.str] = None,
        encryption_kms_key_id: typing.Optional[builtins.str] = None,
        encryption_type: typing.Optional[builtins.str] = None,
        storage_aws_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param storage_base_url: Specifies the base URL for your cloud storage location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#storage_base_url ExternalVolume#storage_base_url}
        :param storage_location_name: Name of the storage location. Must be unique for the external volume. Do not use the name ``terraform_provider_sentinel_storage_location`` - this is reserved for the provider for performing update operations. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#storage_location_name ExternalVolume#storage_location_name}
        :param storage_provider: Specifies the cloud storage provider that stores your data files. Valid values are (case-insensitive): ``GCS`` | ``AZURE`` | ``S3`` | ``S3GOV``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#storage_provider ExternalVolume#storage_provider}
        :param azure_tenant_id: Specifies the ID for your Office 365 tenant that the allowed and blocked storage accounts belong to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#azure_tenant_id ExternalVolume#azure_tenant_id}
        :param encryption_kms_key_id: Specifies the ID for the KMS-managed key used to encrypt files. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#encryption_kms_key_id ExternalVolume#encryption_kms_key_id}
        :param encryption_type: Specifies the encryption type used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#encryption_type ExternalVolume#encryption_type}
        :param storage_aws_role_arn: Specifies the case-sensitive Amazon Resource Name (ARN) of the AWS identity and access management (IAM) role that grants privileges on the S3 bucket containing your data files. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#storage_aws_role_arn ExternalVolume#storage_aws_role_arn}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daa5fc9fdfa00a3db78d47e9c415d3f00059bbf0f7c9a18741827815f6a9ee82)
            check_type(argname="argument storage_base_url", value=storage_base_url, expected_type=type_hints["storage_base_url"])
            check_type(argname="argument storage_location_name", value=storage_location_name, expected_type=type_hints["storage_location_name"])
            check_type(argname="argument storage_provider", value=storage_provider, expected_type=type_hints["storage_provider"])
            check_type(argname="argument azure_tenant_id", value=azure_tenant_id, expected_type=type_hints["azure_tenant_id"])
            check_type(argname="argument encryption_kms_key_id", value=encryption_kms_key_id, expected_type=type_hints["encryption_kms_key_id"])
            check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
            check_type(argname="argument storage_aws_role_arn", value=storage_aws_role_arn, expected_type=type_hints["storage_aws_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "storage_base_url": storage_base_url,
            "storage_location_name": storage_location_name,
            "storage_provider": storage_provider,
        }
        if azure_tenant_id is not None:
            self._values["azure_tenant_id"] = azure_tenant_id
        if encryption_kms_key_id is not None:
            self._values["encryption_kms_key_id"] = encryption_kms_key_id
        if encryption_type is not None:
            self._values["encryption_type"] = encryption_type
        if storage_aws_role_arn is not None:
            self._values["storage_aws_role_arn"] = storage_aws_role_arn

    @builtins.property
    def storage_base_url(self) -> builtins.str:
        '''Specifies the base URL for your cloud storage location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#storage_base_url ExternalVolume#storage_base_url}
        '''
        result = self._values.get("storage_base_url")
        assert result is not None, "Required property 'storage_base_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_location_name(self) -> builtins.str:
        '''Name of the storage location.

        Must be unique for the external volume. Do not use the name ``terraform_provider_sentinel_storage_location`` - this is reserved for the provider for performing update operations. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#storage_location_name ExternalVolume#storage_location_name}
        '''
        result = self._values.get("storage_location_name")
        assert result is not None, "Required property 'storage_location_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_provider(self) -> builtins.str:
        '''Specifies the cloud storage provider that stores your data files.

        Valid values are (case-insensitive): ``GCS`` | ``AZURE`` | ``S3`` | ``S3GOV``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#storage_provider ExternalVolume#storage_provider}
        '''
        result = self._values.get("storage_provider")
        assert result is not None, "Required property 'storage_provider' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def azure_tenant_id(self) -> typing.Optional[builtins.str]:
        '''Specifies the ID for your Office 365 tenant that the allowed and blocked storage accounts belong to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#azure_tenant_id ExternalVolume#azure_tenant_id}
        '''
        result = self._values.get("azure_tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Specifies the ID for the KMS-managed key used to encrypt files.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#encryption_kms_key_id ExternalVolume#encryption_kms_key_id}
        '''
        result = self._values.get("encryption_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the encryption type used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#encryption_type ExternalVolume#encryption_type}
        '''
        result = self._values.get("encryption_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_aws_role_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the case-sensitive Amazon Resource Name (ARN) of the AWS identity and access management (IAM) role that grants privileges on the S3 bucket containing your data files.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_volume#storage_aws_role_arn ExternalVolume#storage_aws_role_arn}
        '''
        result = self._values.get("storage_aws_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalVolumeStorageLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalVolumeStorageLocationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalVolume.ExternalVolumeStorageLocationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee7533a9c8968a1533c1c4dac022935b59e7ef03a0cf459518eb97d8e0386f01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ExternalVolumeStorageLocationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ccee0039f71fc08b01d8c0b7681297996596d75c3856ca8f996e43b0035d020)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalVolumeStorageLocationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc036b2c1fa83259a55d957330686954143b9497a48c95e077c7a9d6879a7a01)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9724b4600dd2a5b28de68b601ec3179918aab8fa15d2a068e498134d1deaab38)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ecb24763ea9316cba7902c41f028e9f67c35517ccd28532f490db94e5c9b040)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalVolumeStorageLocation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalVolumeStorageLocation]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalVolumeStorageLocation]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__960299b81ed01339ec4efbc0948bb811b1d60bda97ec7e8c562bbbfb896f9c42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ExternalVolumeStorageLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalVolume.ExternalVolumeStorageLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53f4f57c5be85309f04d25e3d232825790efc5a7e14a223be5e1a2dd9ecb682d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAzureTenantId")
    def reset_azure_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureTenantId", []))

    @jsii.member(jsii_name="resetEncryptionKmsKeyId")
    def reset_encryption_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKmsKeyId", []))

    @jsii.member(jsii_name="resetEncryptionType")
    def reset_encryption_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionType", []))

    @jsii.member(jsii_name="resetStorageAwsRoleArn")
    def reset_storage_aws_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAwsRoleArn", []))

    @builtins.property
    @jsii.member(jsii_name="storageAwsExternalId")
    def storage_aws_external_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAwsExternalId"))

    @builtins.property
    @jsii.member(jsii_name="azureTenantIdInput")
    def azure_tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "azureTenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKmsKeyIdInput")
    def encryption_kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionKmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionTypeInput")
    def encryption_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAwsRoleArnInput")
    def storage_aws_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAwsRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="storageBaseUrlInput")
    def storage_base_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageBaseUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="storageLocationNameInput")
    def storage_location_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageLocationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageProviderInput")
    def storage_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="azureTenantId")
    def azure_tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "azureTenantId"))

    @azure_tenant_id.setter
    def azure_tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac577fed0441898edfd64a083164209cdd196640bb111b26f43a9a6a6de5b91f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureTenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionKmsKeyId")
    def encryption_kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionKmsKeyId"))

    @encryption_kms_key_id.setter
    def encryption_kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a716393a2eed4a2dda22b86c726e58b4d4484c3adf88cd5a1850212a88cd046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionType")
    def encryption_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionType"))

    @encryption_type.setter
    def encryption_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99deb7ab6aaf23e40b9c43314780071e543f10b10ba14a478f00a5fc79a409da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAwsRoleArn")
    def storage_aws_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAwsRoleArn"))

    @storage_aws_role_arn.setter
    def storage_aws_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71001653082fe5127cf017fb2affa1a87bc6b23ee86d083ead8c3299c496a2e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAwsRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageBaseUrl")
    def storage_base_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageBaseUrl"))

    @storage_base_url.setter
    def storage_base_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd77798fc10458b1df8e63e4135edc731d6708eb2593a7687b0bf526f38ab343)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageBaseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageLocationName")
    def storage_location_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageLocationName"))

    @storage_location_name.setter
    def storage_location_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__267370fab99f39d57887daecee9e0caaf67fc14c5d838297947644562b70dd0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageLocationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageProvider")
    def storage_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageProvider"))

    @storage_provider.setter
    def storage_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa892d6d41b823b013cb64383e996099b337e8db85eb05ce085743a2d838e554)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageProvider", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalVolumeStorageLocation]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalVolumeStorageLocation]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalVolumeStorageLocation]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__532eafd57718fdaa8af13642db31d6d83d3adf2fff3fcb962a5d89ed06325f1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ExternalVolume",
    "ExternalVolumeConfig",
    "ExternalVolumeDescribeOutput",
    "ExternalVolumeDescribeOutputList",
    "ExternalVolumeDescribeOutputOutputReference",
    "ExternalVolumeShowOutput",
    "ExternalVolumeShowOutputList",
    "ExternalVolumeShowOutputOutputReference",
    "ExternalVolumeStorageLocation",
    "ExternalVolumeStorageLocationList",
    "ExternalVolumeStorageLocationOutputReference",
]

publication.publish()

def _typecheckingstub__636e4f0d96219e66fd47857843ef5c2587978b92327d37d4df6cc67ba8f09d26(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    storage_location: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ExternalVolumeStorageLocation, typing.Dict[builtins.str, typing.Any]]]],
    allow_writes: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__788dedbd13f1a5d2b24ee051c4817d7c11f6ba5beeead6575b0253506d891307(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02351dc9b70b54cb424762a8c52dd207ecf572fd63ce9f5fc5ca2a8e971a8bfc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ExternalVolumeStorageLocation, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967f58535a539063addc420142b36191a7b4e391690a80d56d04385ea7dd3982(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62ca64f76359d670009d62765b3aa70cc39e1657b65c904805020c472b2fdc02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f31a146239069c37af090bf38268b7e0b84ca5f424cd3af23d77567f04b916(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33b1731f2027fa318f67349fc32287c86662c7e298b6032d9e5e2efe5af8636(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__960589416c56707a37d97c52a7580906b92a80b5d06f93c420fcb8baaf8a7b69(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    storage_location: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ExternalVolumeStorageLocation, typing.Dict[builtins.str, typing.Any]]]],
    allow_writes: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48945399a2123afc62fbd4d82ff9f2e5b5795ac5141fb622cfc9b3a032e13175(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7683411e68e3db9192ffe763ef8fe5992e7c42afaf5517fd8e8341d898c0c4a7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa12b9d4960763dd441c56c8bc0817b87884563aee964ea85a7a260a349f1df4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55d5451deee33871e4184a4c3bf213863166a75f065904533f3aeee09fd4e233(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae88e45636de7d3307cbaf9f9f7a3014804461f212812a587369c4a26674c107(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cb9badb1d2eadc0dd70512f84f85d03a80a68228d0cd0f112c6a87a500d5792(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6454fa1c47e09fd990dcea64b782528403a45b3e0280906ce59e5ecf42cb870(
    value: typing.Optional[ExternalVolumeDescribeOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__626bba9a5bb7da1cc4b936e5b51274aeb4d70172200c12ea6917300ccdfbc164(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d9756e8643b242ca5b05b35cbb6f5c2eba0364689ba53f9d00476147103145c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b0bc3827ac3f30f45077236230686ed394328bbd11b2c1343614c411001b88d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8346f223cdf4ef583785e188b17db2dec2e6a78032d8ffa5252917b72eb4cdbd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee2ba22b1de21a976c66f8eca982d35a5abfc96e85aedc6aff4804ee2f5360ce(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0d0355cd7aac0743c68fa693481a4f1d3035597d7aa34b1e5e4a2d50db9ba14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abefec2d8bcd3a54fcecc9f2f61a80ae72672419777eeb02457a2fc5f3700989(
    value: typing.Optional[ExternalVolumeShowOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daa5fc9fdfa00a3db78d47e9c415d3f00059bbf0f7c9a18741827815f6a9ee82(
    *,
    storage_base_url: builtins.str,
    storage_location_name: builtins.str,
    storage_provider: builtins.str,
    azure_tenant_id: typing.Optional[builtins.str] = None,
    encryption_kms_key_id: typing.Optional[builtins.str] = None,
    encryption_type: typing.Optional[builtins.str] = None,
    storage_aws_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee7533a9c8968a1533c1c4dac022935b59e7ef03a0cf459518eb97d8e0386f01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ccee0039f71fc08b01d8c0b7681297996596d75c3856ca8f996e43b0035d020(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc036b2c1fa83259a55d957330686954143b9497a48c95e077c7a9d6879a7a01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9724b4600dd2a5b28de68b601ec3179918aab8fa15d2a068e498134d1deaab38(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ecb24763ea9316cba7902c41f028e9f67c35517ccd28532f490db94e5c9b040(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__960299b81ed01339ec4efbc0948bb811b1d60bda97ec7e8c562bbbfb896f9c42(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalVolumeStorageLocation]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f4f57c5be85309f04d25e3d232825790efc5a7e14a223be5e1a2dd9ecb682d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac577fed0441898edfd64a083164209cdd196640bb111b26f43a9a6a6de5b91f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a716393a2eed4a2dda22b86c726e58b4d4484c3adf88cd5a1850212a88cd046(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99deb7ab6aaf23e40b9c43314780071e543f10b10ba14a478f00a5fc79a409da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71001653082fe5127cf017fb2affa1a87bc6b23ee86d083ead8c3299c496a2e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd77798fc10458b1df8e63e4135edc731d6708eb2593a7687b0bf526f38ab343(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267370fab99f39d57887daecee9e0caaf67fc14c5d838297947644562b70dd0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa892d6d41b823b013cb64383e996099b337e8db85eb05ce085743a2d838e554(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__532eafd57718fdaa8af13642db31d6d83d3adf2fff3fcb962a5d89ed06325f1b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalVolumeStorageLocation]],
) -> None:
    """Type checking stubs"""
    pass
