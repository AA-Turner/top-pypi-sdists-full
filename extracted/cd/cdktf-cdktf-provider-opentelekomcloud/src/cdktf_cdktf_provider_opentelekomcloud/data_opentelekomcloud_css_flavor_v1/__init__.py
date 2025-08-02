r'''
# `data_opentelekomcloud_css_flavor_v1`

Refer to the Terraform Registry for docs: [`data_opentelekomcloud_css_flavor_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1).
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


class DataOpentelekomcloudCssFlavorV1(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCssFlavorV1.DataOpentelekomcloudCssFlavorV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1 opentelekomcloud_css_flavor_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        disk_range: typing.Optional[typing.Union["DataOpentelekomcloudCssFlavorV1DiskRange", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        min_cpu: typing.Optional[jsii.Number] = None,
        min_ram: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1 opentelekomcloud_css_flavor_v1} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param disk_range: disk_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#disk_range DataOpentelekomcloudCssFlavorV1#disk_range}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#id DataOpentelekomcloudCssFlavorV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param min_cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#min_cpu DataOpentelekomcloudCssFlavorV1#min_cpu}.
        :param min_ram: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#min_ram DataOpentelekomcloudCssFlavorV1#min_ram}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#name DataOpentelekomcloudCssFlavorV1#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#type DataOpentelekomcloudCssFlavorV1#type}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#version DataOpentelekomcloudCssFlavorV1#version}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d584523472665d61c0a56a003409423eea0b05d75c5762b4c1c36dd061b646ed)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataOpentelekomcloudCssFlavorV1Config(
            disk_range=disk_range,
            id=id,
            min_cpu=min_cpu,
            min_ram=min_ram,
            name=name,
            type=type,
            version=version,
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
        '''Generates CDKTF code for importing a DataOpentelekomcloudCssFlavorV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOpentelekomcloudCssFlavorV1 to import.
        :param import_from_id: The id of the existing DataOpentelekomcloudCssFlavorV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOpentelekomcloudCssFlavorV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6096dd8a1be1ce7e11025b0fc12b01d79b730f5b35d9078c49bc9cb6dc9d058c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDiskRange")
    def put_disk_range(
        self,
        *,
        min_from: typing.Optional[jsii.Number] = None,
        min_to: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param min_from: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#min_from DataOpentelekomcloudCssFlavorV1#min_from}.
        :param min_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#min_to DataOpentelekomcloudCssFlavorV1#min_to}.
        '''
        value = DataOpentelekomcloudCssFlavorV1DiskRange(
            min_from=min_from, min_to=min_to
        )

        return typing.cast(None, jsii.invoke(self, "putDiskRange", [value]))

    @jsii.member(jsii_name="resetDiskRange")
    def reset_disk_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskRange", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMinCpu")
    def reset_min_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinCpu", []))

    @jsii.member(jsii_name="resetMinRam")
    def reset_min_ram(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinRam", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

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
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpu"))

    @builtins.property
    @jsii.member(jsii_name="diskRange")
    def disk_range(self) -> "DataOpentelekomcloudCssFlavorV1DiskRangeOutputReference":
        return typing.cast("DataOpentelekomcloudCssFlavorV1DiskRangeOutputReference", jsii.get(self, "diskRange"))

    @builtins.property
    @jsii.member(jsii_name="ram")
    def ram(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ram"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="diskRangeInput")
    def disk_range_input(
        self,
    ) -> typing.Optional["DataOpentelekomcloudCssFlavorV1DiskRange"]:
        return typing.cast(typing.Optional["DataOpentelekomcloudCssFlavorV1DiskRange"], jsii.get(self, "diskRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="minCpuInput")
    def min_cpu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minCpuInput"))

    @builtins.property
    @jsii.member(jsii_name="minRamInput")
    def min_ram_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minRamInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a06ef430ce1df160ed29eea99b5738f705feeb9eba34703682f9ddd1207cd010)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minCpu")
    def min_cpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minCpu"))

    @min_cpu.setter
    def min_cpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c46f2155fa727d635ab889260f5e0444256e95cc50ba99c373940731c443905b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minRam")
    def min_ram(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minRam"))

    @min_ram.setter
    def min_ram(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d0bb3ab70925eeceffd84fde08710863f2a66ff73c6cbf14dfe2910d6a62700)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minRam", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1e0d5a19a42d76de53da05e49df5fd8b579eca74ef65ad0bbf37544cead41b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e83c70ca9fb60ac00e13c9c0a1a1106c82905e495dc0107ec2fb5005ff66f053)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a94d507da940d7a10c16205e0a7bda090580f1326d02ec9d5ca03e1b49a69b74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCssFlavorV1.DataOpentelekomcloudCssFlavorV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "disk_range": "diskRange",
        "id": "id",
        "min_cpu": "minCpu",
        "min_ram": "minRam",
        "name": "name",
        "type": "type",
        "version": "version",
    },
)
class DataOpentelekomcloudCssFlavorV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        disk_range: typing.Optional[typing.Union["DataOpentelekomcloudCssFlavorV1DiskRange", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        min_cpu: typing.Optional[jsii.Number] = None,
        min_ram: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param disk_range: disk_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#disk_range DataOpentelekomcloudCssFlavorV1#disk_range}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#id DataOpentelekomcloudCssFlavorV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param min_cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#min_cpu DataOpentelekomcloudCssFlavorV1#min_cpu}.
        :param min_ram: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#min_ram DataOpentelekomcloudCssFlavorV1#min_ram}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#name DataOpentelekomcloudCssFlavorV1#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#type DataOpentelekomcloudCssFlavorV1#type}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#version DataOpentelekomcloudCssFlavorV1#version}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(disk_range, dict):
            disk_range = DataOpentelekomcloudCssFlavorV1DiskRange(**disk_range)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ab3dadae4fbb7e1d0ea6a2acead80979ae970e0b1c7dec3571ccd153cbbd60e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument disk_range", value=disk_range, expected_type=type_hints["disk_range"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument min_cpu", value=min_cpu, expected_type=type_hints["min_cpu"])
            check_type(argname="argument min_ram", value=min_ram, expected_type=type_hints["min_ram"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
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
        if disk_range is not None:
            self._values["disk_range"] = disk_range
        if id is not None:
            self._values["id"] = id
        if min_cpu is not None:
            self._values["min_cpu"] = min_cpu
        if min_ram is not None:
            self._values["min_ram"] = min_ram
        if name is not None:
            self._values["name"] = name
        if type is not None:
            self._values["type"] = type
        if version is not None:
            self._values["version"] = version

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
    def disk_range(self) -> typing.Optional["DataOpentelekomcloudCssFlavorV1DiskRange"]:
        '''disk_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#disk_range DataOpentelekomcloudCssFlavorV1#disk_range}
        '''
        result = self._values.get("disk_range")
        return typing.cast(typing.Optional["DataOpentelekomcloudCssFlavorV1DiskRange"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#id DataOpentelekomcloudCssFlavorV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_cpu(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#min_cpu DataOpentelekomcloudCssFlavorV1#min_cpu}.'''
        result = self._values.get("min_cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_ram(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#min_ram DataOpentelekomcloudCssFlavorV1#min_ram}.'''
        result = self._values.get("min_ram")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#name DataOpentelekomcloudCssFlavorV1#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#type DataOpentelekomcloudCssFlavorV1#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#version DataOpentelekomcloudCssFlavorV1#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudCssFlavorV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCssFlavorV1.DataOpentelekomcloudCssFlavorV1DiskRange",
    jsii_struct_bases=[],
    name_mapping={"min_from": "minFrom", "min_to": "minTo"},
)
class DataOpentelekomcloudCssFlavorV1DiskRange:
    def __init__(
        self,
        *,
        min_from: typing.Optional[jsii.Number] = None,
        min_to: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param min_from: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#min_from DataOpentelekomcloudCssFlavorV1#min_from}.
        :param min_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#min_to DataOpentelekomcloudCssFlavorV1#min_to}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65c2de23cd503c02e07fffc3fd1d28550173e2328aba25284234a3a80566e6e6)
            check_type(argname="argument min_from", value=min_from, expected_type=type_hints["min_from"])
            check_type(argname="argument min_to", value=min_to, expected_type=type_hints["min_to"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if min_from is not None:
            self._values["min_from"] = min_from
        if min_to is not None:
            self._values["min_to"] = min_to

    @builtins.property
    def min_from(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#min_from DataOpentelekomcloudCssFlavorV1#min_from}.'''
        result = self._values.get("min_from")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_to(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/css_flavor_v1#min_to DataOpentelekomcloudCssFlavorV1#min_to}.'''
        result = self._values.get("min_to")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudCssFlavorV1DiskRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOpentelekomcloudCssFlavorV1DiskRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCssFlavorV1.DataOpentelekomcloudCssFlavorV1DiskRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95249e808e324d7e2531b906289bde693f09eff5c1526f71c1358a5d3f0114a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMinFrom")
    def reset_min_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinFrom", []))

    @jsii.member(jsii_name="resetMinTo")
    def reset_min_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinTo", []))

    @builtins.property
    @jsii.member(jsii_name="from")
    def from_(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "from"))

    @builtins.property
    @jsii.member(jsii_name="to")
    def to(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "to"))

    @builtins.property
    @jsii.member(jsii_name="minFromInput")
    def min_from_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minFromInput"))

    @builtins.property
    @jsii.member(jsii_name="minToInput")
    def min_to_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minToInput"))

    @builtins.property
    @jsii.member(jsii_name="minFrom")
    def min_from(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minFrom"))

    @min_from.setter
    def min_from(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__177da4e633770cdb4e5eb9022ef08a6e76f543a4a9ff1356e93f43141409a9f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minFrom", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minTo")
    def min_to(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minTo"))

    @min_to.setter
    def min_to(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd6023babf9dadee1c8665d7f980474e39d5a24f52f7ce04350ab75b2ef205fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minTo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataOpentelekomcloudCssFlavorV1DiskRange]:
        return typing.cast(typing.Optional[DataOpentelekomcloudCssFlavorV1DiskRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOpentelekomcloudCssFlavorV1DiskRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccc7ac08b29bc2a6ea5ec790ee31c4461b1ef8e25065fa25ffd9baa24cab80fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataOpentelekomcloudCssFlavorV1",
    "DataOpentelekomcloudCssFlavorV1Config",
    "DataOpentelekomcloudCssFlavorV1DiskRange",
    "DataOpentelekomcloudCssFlavorV1DiskRangeOutputReference",
]

publication.publish()

def _typecheckingstub__d584523472665d61c0a56a003409423eea0b05d75c5762b4c1c36dd061b646ed(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    disk_range: typing.Optional[typing.Union[DataOpentelekomcloudCssFlavorV1DiskRange, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    min_cpu: typing.Optional[jsii.Number] = None,
    min_ram: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__6096dd8a1be1ce7e11025b0fc12b01d79b730f5b35d9078c49bc9cb6dc9d058c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a06ef430ce1df160ed29eea99b5738f705feeb9eba34703682f9ddd1207cd010(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c46f2155fa727d635ab889260f5e0444256e95cc50ba99c373940731c443905b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d0bb3ab70925eeceffd84fde08710863f2a66ff73c6cbf14dfe2910d6a62700(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e0d5a19a42d76de53da05e49df5fd8b579eca74ef65ad0bbf37544cead41b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e83c70ca9fb60ac00e13c9c0a1a1106c82905e495dc0107ec2fb5005ff66f053(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a94d507da940d7a10c16205e0a7bda090580f1326d02ec9d5ca03e1b49a69b74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ab3dadae4fbb7e1d0ea6a2acead80979ae970e0b1c7dec3571ccd153cbbd60e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    disk_range: typing.Optional[typing.Union[DataOpentelekomcloudCssFlavorV1DiskRange, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    min_cpu: typing.Optional[jsii.Number] = None,
    min_ram: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c2de23cd503c02e07fffc3fd1d28550173e2328aba25284234a3a80566e6e6(
    *,
    min_from: typing.Optional[jsii.Number] = None,
    min_to: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95249e808e324d7e2531b906289bde693f09eff5c1526f71c1358a5d3f0114a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177da4e633770cdb4e5eb9022ef08a6e76f543a4a9ff1356e93f43141409a9f7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd6023babf9dadee1c8665d7f980474e39d5a24f52f7ce04350ab75b2ef205fc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccc7ac08b29bc2a6ea5ec790ee31c4461b1ef8e25065fa25ffd9baa24cab80fa(
    value: typing.Optional[DataOpentelekomcloudCssFlavorV1DiskRange],
) -> None:
    """Type checking stubs"""
    pass
