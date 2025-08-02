r'''
# `opentelekomcloud_obs_bucket_inventory`

Refer to the Terraform Registry for docs: [`opentelekomcloud_obs_bucket_inventory`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory).
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


class ObsBucketInventory(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketInventory.ObsBucketInventory",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory opentelekomcloud_obs_bucket_inventory}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        bucket: builtins.str,
        configuration_id: builtins.str,
        destination: typing.Union["ObsBucketInventoryDestination", typing.Dict[builtins.str, typing.Any]],
        frequency: builtins.str,
        included_object_versions: builtins.str,
        is_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        filter_prefix: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        optional_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory opentelekomcloud_obs_bucket_inventory} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#bucket ObsBucketInventory#bucket}.
        :param configuration_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#configuration_id ObsBucketInventory#configuration_id}.
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#destination ObsBucketInventory#destination}
        :param frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#frequency ObsBucketInventory#frequency}.
        :param included_object_versions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#included_object_versions ObsBucketInventory#included_object_versions}.
        :param is_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#is_enabled ObsBucketInventory#is_enabled}.
        :param filter_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#filter_prefix ObsBucketInventory#filter_prefix}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#id ObsBucketInventory#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param optional_fields: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#optional_fields ObsBucketInventory#optional_fields}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1faf11809b5b9d197766b0c26f183f34e691d5c8cc211efba870cf1ac855810b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ObsBucketInventoryConfig(
            bucket=bucket,
            configuration_id=configuration_id,
            destination=destination,
            frequency=frequency,
            included_object_versions=included_object_versions,
            is_enabled=is_enabled,
            filter_prefix=filter_prefix,
            id=id,
            optional_fields=optional_fields,
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
        '''Generates CDKTF code for importing a ObsBucketInventory resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ObsBucketInventory to import.
        :param import_from_id: The id of the existing ObsBucketInventory that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ObsBucketInventory to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d070793f3327fb72fdf0757370e2e3e016daf0bd5bc4fc47f0415c7a8cd9a8ff)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDestination")
    def put_destination(
        self,
        *,
        bucket: builtins.str,
        format: builtins.str,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#bucket ObsBucketInventory#bucket}.
        :param format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#format ObsBucketInventory#format}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#prefix ObsBucketInventory#prefix}.
        '''
        value = ObsBucketInventoryDestination(
            bucket=bucket, format=format, prefix=prefix
        )

        return typing.cast(None, jsii.invoke(self, "putDestination", [value]))

    @jsii.member(jsii_name="resetFilterPrefix")
    def reset_filter_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterPrefix", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOptionalFields")
    def reset_optional_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptionalFields", []))

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
    @jsii.member(jsii_name="destination")
    def destination(self) -> "ObsBucketInventoryDestinationOutputReference":
        return typing.cast("ObsBucketInventoryDestinationOutputReference", jsii.get(self, "destination"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="configurationIdInput")
    def configuration_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configurationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional["ObsBucketInventoryDestination"]:
        return typing.cast(typing.Optional["ObsBucketInventoryDestination"], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="filterPrefixInput")
    def filter_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="frequencyInput")
    def frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includedObjectVersionsInput")
    def included_object_versions_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "includedObjectVersionsInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="optionalFieldsInput")
    def optional_fields_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "optionalFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf7cde4438eef0124dcbe8c786ccd22dce6b649318248898b8433b7a791f91c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="configurationId")
    def configuration_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configurationId"))

    @configuration_id.setter
    def configuration_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4767676e08ae0202cc161d3caf61046cdaff6760a852be2583c713d7ddd6884)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configurationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterPrefix")
    def filter_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterPrefix"))

    @filter_prefix.setter
    def filter_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b97f7b98a6ee102082ee895707e9621d333a111b5ae27c7eabdc1f56954149ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequency"))

    @frequency.setter
    def frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82dc23663431ab597e0882d09801d4398013deb5ad12f5d442669a0a372975ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acf660986d67456f6db3210d2a80eaae541c68e716247f48da7106a8b44bfbe2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedObjectVersions")
    def included_object_versions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "includedObjectVersions"))

    @included_object_versions.setter
    def included_object_versions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f547bc6eeb47c3975862c3760ad9fc18d6d263bc4d546032c3ccd487f97f81d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedObjectVersions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__307707757ee57b52e6e7a81eb046b3d1c3909f7522a60baa8cec67a164ecb34d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="optionalFields")
    def optional_fields(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "optionalFields"))

    @optional_fields.setter
    def optional_fields(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9f142c6bc316039aa903cce5ba0d6936fe3e0d09fb7b57105c5bf60e7676b86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optionalFields", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketInventory.ObsBucketInventoryConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "bucket": "bucket",
        "configuration_id": "configurationId",
        "destination": "destination",
        "frequency": "frequency",
        "included_object_versions": "includedObjectVersions",
        "is_enabled": "isEnabled",
        "filter_prefix": "filterPrefix",
        "id": "id",
        "optional_fields": "optionalFields",
    },
)
class ObsBucketInventoryConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bucket: builtins.str,
        configuration_id: builtins.str,
        destination: typing.Union["ObsBucketInventoryDestination", typing.Dict[builtins.str, typing.Any]],
        frequency: builtins.str,
        included_object_versions: builtins.str,
        is_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        filter_prefix: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        optional_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#bucket ObsBucketInventory#bucket}.
        :param configuration_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#configuration_id ObsBucketInventory#configuration_id}.
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#destination ObsBucketInventory#destination}
        :param frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#frequency ObsBucketInventory#frequency}.
        :param included_object_versions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#included_object_versions ObsBucketInventory#included_object_versions}.
        :param is_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#is_enabled ObsBucketInventory#is_enabled}.
        :param filter_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#filter_prefix ObsBucketInventory#filter_prefix}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#id ObsBucketInventory#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param optional_fields: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#optional_fields ObsBucketInventory#optional_fields}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(destination, dict):
            destination = ObsBucketInventoryDestination(**destination)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07935a3aae200455a30d3af0d9bb2333dbdd15d7634502a560dd687e81857b80)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument configuration_id", value=configuration_id, expected_type=type_hints["configuration_id"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument included_object_versions", value=included_object_versions, expected_type=type_hints["included_object_versions"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument filter_prefix", value=filter_prefix, expected_type=type_hints["filter_prefix"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument optional_fields", value=optional_fields, expected_type=type_hints["optional_fields"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "configuration_id": configuration_id,
            "destination": destination,
            "frequency": frequency,
            "included_object_versions": included_object_versions,
            "is_enabled": is_enabled,
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
        if filter_prefix is not None:
            self._values["filter_prefix"] = filter_prefix
        if id is not None:
            self._values["id"] = id
        if optional_fields is not None:
            self._values["optional_fields"] = optional_fields

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
    def bucket(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#bucket ObsBucketInventory#bucket}.'''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#configuration_id ObsBucketInventory#configuration_id}.'''
        result = self._values.get("configuration_id")
        assert result is not None, "Required property 'configuration_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination(self) -> "ObsBucketInventoryDestination":
        '''destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#destination ObsBucketInventory#destination}
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast("ObsBucketInventoryDestination", result)

    @builtins.property
    def frequency(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#frequency ObsBucketInventory#frequency}.'''
        result = self._values.get("frequency")
        assert result is not None, "Required property 'frequency' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def included_object_versions(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#included_object_versions ObsBucketInventory#included_object_versions}.'''
        result = self._values.get("included_object_versions")
        assert result is not None, "Required property 'included_object_versions' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#is_enabled ObsBucketInventory#is_enabled}.'''
        result = self._values.get("is_enabled")
        assert result is not None, "Required property 'is_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def filter_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#filter_prefix ObsBucketInventory#filter_prefix}.'''
        result = self._values.get("filter_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#id ObsBucketInventory#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#optional_fields ObsBucketInventory#optional_fields}.'''
        result = self._values.get("optional_fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketInventoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketInventory.ObsBucketInventoryDestination",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "format": "format", "prefix": "prefix"},
)
class ObsBucketInventoryDestination:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        format: builtins.str,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#bucket ObsBucketInventory#bucket}.
        :param format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#format ObsBucketInventory#format}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#prefix ObsBucketInventory#prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6cecfd34dc5b1b865dc0774034ed442ac8a4355691a1c1aa7ff8ea12e924152)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "format": format,
        }
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#bucket ObsBucketInventory#bucket}.'''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def format(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#format ObsBucketInventory#format}.'''
        result = self._values.get("format")
        assert result is not None, "Required property 'format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_inventory#prefix ObsBucketInventory#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketInventoryDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObsBucketInventoryDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketInventory.ObsBucketInventoryDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca3550ab31b8e9ed54ff7ba988e57b791555acc2bd9ee91086cd4770268d41a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="formatInput")
    def format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "formatInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3df9208a0aa4d5c80f302b97974bf71fea760b6b17ed2352276d78a62fd8f9c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "format"))

    @format.setter
    def format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7048c268670ff7ada8ed4545701940886ca884b1b70e2d9d13b1705f189bcd75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "format", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ed335bfc6155ac8551dcad026029d928a88a3a61028ba57b642bd7a7e920e26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ObsBucketInventoryDestination]:
        return typing.cast(typing.Optional[ObsBucketInventoryDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ObsBucketInventoryDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdf48d3c07d4ae7b21e03ddfd9d06422e279a11c3940c7fe2bbb6fc810f9961c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ObsBucketInventory",
    "ObsBucketInventoryConfig",
    "ObsBucketInventoryDestination",
    "ObsBucketInventoryDestinationOutputReference",
]

publication.publish()

def _typecheckingstub__1faf11809b5b9d197766b0c26f183f34e691d5c8cc211efba870cf1ac855810b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    bucket: builtins.str,
    configuration_id: builtins.str,
    destination: typing.Union[ObsBucketInventoryDestination, typing.Dict[builtins.str, typing.Any]],
    frequency: builtins.str,
    included_object_versions: builtins.str,
    is_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    filter_prefix: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    optional_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__d070793f3327fb72fdf0757370e2e3e016daf0bd5bc4fc47f0415c7a8cd9a8ff(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf7cde4438eef0124dcbe8c786ccd22dce6b649318248898b8433b7a791f91c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4767676e08ae0202cc161d3caf61046cdaff6760a852be2583c713d7ddd6884(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b97f7b98a6ee102082ee895707e9621d333a111b5ae27c7eabdc1f56954149ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82dc23663431ab597e0882d09801d4398013deb5ad12f5d442669a0a372975ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf660986d67456f6db3210d2a80eaae541c68e716247f48da7106a8b44bfbe2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f547bc6eeb47c3975862c3760ad9fc18d6d263bc4d546032c3ccd487f97f81d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__307707757ee57b52e6e7a81eb046b3d1c3909f7522a60baa8cec67a164ecb34d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9f142c6bc316039aa903cce5ba0d6936fe3e0d09fb7b57105c5bf60e7676b86(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07935a3aae200455a30d3af0d9bb2333dbdd15d7634502a560dd687e81857b80(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bucket: builtins.str,
    configuration_id: builtins.str,
    destination: typing.Union[ObsBucketInventoryDestination, typing.Dict[builtins.str, typing.Any]],
    frequency: builtins.str,
    included_object_versions: builtins.str,
    is_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    filter_prefix: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    optional_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6cecfd34dc5b1b865dc0774034ed442ac8a4355691a1c1aa7ff8ea12e924152(
    *,
    bucket: builtins.str,
    format: builtins.str,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca3550ab31b8e9ed54ff7ba988e57b791555acc2bd9ee91086cd4770268d41a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3df9208a0aa4d5c80f302b97974bf71fea760b6b17ed2352276d78a62fd8f9c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7048c268670ff7ada8ed4545701940886ca884b1b70e2d9d13b1705f189bcd75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed335bfc6155ac8551dcad026029d928a88a3a61028ba57b642bd7a7e920e26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf48d3c07d4ae7b21e03ddfd9d06422e279a11c3940c7fe2bbb6fc810f9961c(
    value: typing.Optional[ObsBucketInventoryDestination],
) -> None:
    """Type checking stubs"""
    pass
