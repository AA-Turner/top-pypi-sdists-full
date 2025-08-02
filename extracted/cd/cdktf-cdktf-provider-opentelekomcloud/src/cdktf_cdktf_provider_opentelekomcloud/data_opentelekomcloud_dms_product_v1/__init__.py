r'''
# `data_opentelekomcloud_dms_product_v1`

Refer to the Terraform Registry for docs: [`data_opentelekomcloud_dms_product_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1).
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


class DataOpentelekomcloudDmsProductV1(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudDmsProductV1.DataOpentelekomcloudDmsProductV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1 opentelekomcloud_dms_product_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        engine: builtins.str,
        instance_type: builtins.str,
        bandwidth: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        io_type: typing.Optional[builtins.str] = None,
        node_num: typing.Optional[builtins.str] = None,
        partition_num: typing.Optional[builtins.str] = None,
        storage: typing.Optional[builtins.str] = None,
        storage_spec_code: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        vm_specification: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1 opentelekomcloud_dms_product_v1} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param engine: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#engine DataOpentelekomcloudDmsProductV1#engine}.
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#instance_type DataOpentelekomcloudDmsProductV1#instance_type}.
        :param bandwidth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#bandwidth DataOpentelekomcloudDmsProductV1#bandwidth}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#id DataOpentelekomcloudDmsProductV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param io_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#io_type DataOpentelekomcloudDmsProductV1#io_type}.
        :param node_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#node_num DataOpentelekomcloudDmsProductV1#node_num}.
        :param partition_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#partition_num DataOpentelekomcloudDmsProductV1#partition_num}.
        :param storage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#storage DataOpentelekomcloudDmsProductV1#storage}.
        :param storage_spec_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#storage_spec_code DataOpentelekomcloudDmsProductV1#storage_spec_code}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#version DataOpentelekomcloudDmsProductV1#version}.
        :param vm_specification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#vm_specification DataOpentelekomcloudDmsProductV1#vm_specification}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__213f70680a659d4e43a60895d5630178bc71fcfbcfad5b4aa015de9acdba383b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataOpentelekomcloudDmsProductV1Config(
            engine=engine,
            instance_type=instance_type,
            bandwidth=bandwidth,
            id=id,
            io_type=io_type,
            node_num=node_num,
            partition_num=partition_num,
            storage=storage,
            storage_spec_code=storage_spec_code,
            version=version,
            vm_specification=vm_specification,
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
        '''Generates CDKTF code for importing a DataOpentelekomcloudDmsProductV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOpentelekomcloudDmsProductV1 to import.
        :param import_from_id: The id of the existing DataOpentelekomcloudDmsProductV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOpentelekomcloudDmsProductV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__617f0d0a859298db3322e878d9a8a2da54f29bcaf0931ab5897a4e4a64cb4733)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetBandwidth")
    def reset_bandwidth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidth", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIoType")
    def reset_io_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIoType", []))

    @jsii.member(jsii_name="resetNodeNum")
    def reset_node_num(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeNum", []))

    @jsii.member(jsii_name="resetPartitionNum")
    def reset_partition_num(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartitionNum", []))

    @jsii.member(jsii_name="resetStorage")
    def reset_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorage", []))

    @jsii.member(jsii_name="resetStorageSpecCode")
    def reset_storage_spec_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageSpecCode", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @jsii.member(jsii_name="resetVmSpecification")
    def reset_vm_specification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmSpecification", []))

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
    @jsii.member(jsii_name="bandwidthInput")
    def bandwidth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bandwidthInput"))

    @builtins.property
    @jsii.member(jsii_name="engineInput")
    def engine_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="ioTypeInput")
    def io_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ioTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeNumInput")
    def node_num_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeNumInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionNumInput")
    def partition_num_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partitionNumInput"))

    @builtins.property
    @jsii.member(jsii_name="storageInput")
    def storage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageInput"))

    @builtins.property
    @jsii.member(jsii_name="storageSpecCodeInput")
    def storage_spec_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageSpecCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="vmSpecificationInput")
    def vm_specification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmSpecificationInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidth")
    def bandwidth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidth"))

    @bandwidth.setter
    def bandwidth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f117cc586fcdfc84f07f17cd4dff51e650ff970a2ac31babd2f6b75ab2fdc87e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engine")
    def engine(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engine"))

    @engine.setter
    def engine(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2692287e7ad5dbe123c2ffd6ed58d2e531277f8ee3e34cee77c07ffce4ea7e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__405ef0dfeac8819ead5cc20d24521630e131c8758db9e02eda63a82e0dd678eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc0e03ecd5d2d2156fcc9f257a2f2cd0380f19169223c2c93d45ea259806fd4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ioType")
    def io_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ioType"))

    @io_type.setter
    def io_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ebfc03cbc0faefa342b9dccf4fa39b33a2b3342b332b586fde5167ba1ceca2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ioType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeNum")
    def node_num(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeNum"))

    @node_num.setter
    def node_num(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eff1b887973c12097982f441491f8f8aafc9bb600e7e4e464c106458c99a2998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeNum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partitionNum")
    def partition_num(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partitionNum"))

    @partition_num.setter
    def partition_num(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc6cc0869a973140e8e7773b305ab3f5fdb06c5ec4b9808dff4e666c45783c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitionNum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storage")
    def storage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storage"))

    @storage.setter
    def storage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03822664c7b421f4d1c4047ae3bb2eca4290ae1b8f8fe9740de0134448029913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageSpecCode")
    def storage_spec_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageSpecCode"))

    @storage_spec_code.setter
    def storage_spec_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa190d676b7daed005b2ed0d8875a4decc2f4585e268d8e9db3fb6457c9463d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageSpecCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f844e95b71a705323d7e625e018ad58d6fbe1905265628a906e8872494238979)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSpecification")
    def vm_specification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSpecification"))

    @vm_specification.setter
    def vm_specification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c32138da7fa3bf92d787f022d6dc45fcd99ee12193ef1f71b10a37fdd3482ecf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSpecification", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudDmsProductV1.DataOpentelekomcloudDmsProductV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "engine": "engine",
        "instance_type": "instanceType",
        "bandwidth": "bandwidth",
        "id": "id",
        "io_type": "ioType",
        "node_num": "nodeNum",
        "partition_num": "partitionNum",
        "storage": "storage",
        "storage_spec_code": "storageSpecCode",
        "version": "version",
        "vm_specification": "vmSpecification",
    },
)
class DataOpentelekomcloudDmsProductV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        engine: builtins.str,
        instance_type: builtins.str,
        bandwidth: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        io_type: typing.Optional[builtins.str] = None,
        node_num: typing.Optional[builtins.str] = None,
        partition_num: typing.Optional[builtins.str] = None,
        storage: typing.Optional[builtins.str] = None,
        storage_spec_code: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        vm_specification: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param engine: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#engine DataOpentelekomcloudDmsProductV1#engine}.
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#instance_type DataOpentelekomcloudDmsProductV1#instance_type}.
        :param bandwidth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#bandwidth DataOpentelekomcloudDmsProductV1#bandwidth}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#id DataOpentelekomcloudDmsProductV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param io_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#io_type DataOpentelekomcloudDmsProductV1#io_type}.
        :param node_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#node_num DataOpentelekomcloudDmsProductV1#node_num}.
        :param partition_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#partition_num DataOpentelekomcloudDmsProductV1#partition_num}.
        :param storage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#storage DataOpentelekomcloudDmsProductV1#storage}.
        :param storage_spec_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#storage_spec_code DataOpentelekomcloudDmsProductV1#storage_spec_code}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#version DataOpentelekomcloudDmsProductV1#version}.
        :param vm_specification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#vm_specification DataOpentelekomcloudDmsProductV1#vm_specification}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__185d8d3c58d87a9593ed5b3ecc7fd1b713aec4d866f553f718c5fde547e413f7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument bandwidth", value=bandwidth, expected_type=type_hints["bandwidth"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument io_type", value=io_type, expected_type=type_hints["io_type"])
            check_type(argname="argument node_num", value=node_num, expected_type=type_hints["node_num"])
            check_type(argname="argument partition_num", value=partition_num, expected_type=type_hints["partition_num"])
            check_type(argname="argument storage", value=storage, expected_type=type_hints["storage"])
            check_type(argname="argument storage_spec_code", value=storage_spec_code, expected_type=type_hints["storage_spec_code"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument vm_specification", value=vm_specification, expected_type=type_hints["vm_specification"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "engine": engine,
            "instance_type": instance_type,
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
        if bandwidth is not None:
            self._values["bandwidth"] = bandwidth
        if id is not None:
            self._values["id"] = id
        if io_type is not None:
            self._values["io_type"] = io_type
        if node_num is not None:
            self._values["node_num"] = node_num
        if partition_num is not None:
            self._values["partition_num"] = partition_num
        if storage is not None:
            self._values["storage"] = storage
        if storage_spec_code is not None:
            self._values["storage_spec_code"] = storage_spec_code
        if version is not None:
            self._values["version"] = version
        if vm_specification is not None:
            self._values["vm_specification"] = vm_specification

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
    def engine(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#engine DataOpentelekomcloudDmsProductV1#engine}.'''
        result = self._values.get("engine")
        assert result is not None, "Required property 'engine' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#instance_type DataOpentelekomcloudDmsProductV1#instance_type}.'''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bandwidth(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#bandwidth DataOpentelekomcloudDmsProductV1#bandwidth}.'''
        result = self._values.get("bandwidth")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#id DataOpentelekomcloudDmsProductV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def io_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#io_type DataOpentelekomcloudDmsProductV1#io_type}.'''
        result = self._values.get("io_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_num(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#node_num DataOpentelekomcloudDmsProductV1#node_num}.'''
        result = self._values.get("node_num")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partition_num(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#partition_num DataOpentelekomcloudDmsProductV1#partition_num}.'''
        result = self._values.get("partition_num")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#storage DataOpentelekomcloudDmsProductV1#storage}.'''
        result = self._values.get("storage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_spec_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#storage_spec_code DataOpentelekomcloudDmsProductV1#storage_spec_code}.'''
        result = self._values.get("storage_spec_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#version DataOpentelekomcloudDmsProductV1#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vm_specification(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/dms_product_v1#vm_specification DataOpentelekomcloudDmsProductV1#vm_specification}.'''
        result = self._values.get("vm_specification")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudDmsProductV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataOpentelekomcloudDmsProductV1",
    "DataOpentelekomcloudDmsProductV1Config",
]

publication.publish()

def _typecheckingstub__213f70680a659d4e43a60895d5630178bc71fcfbcfad5b4aa015de9acdba383b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    engine: builtins.str,
    instance_type: builtins.str,
    bandwidth: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    io_type: typing.Optional[builtins.str] = None,
    node_num: typing.Optional[builtins.str] = None,
    partition_num: typing.Optional[builtins.str] = None,
    storage: typing.Optional[builtins.str] = None,
    storage_spec_code: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
    vm_specification: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__617f0d0a859298db3322e878d9a8a2da54f29bcaf0931ab5897a4e4a64cb4733(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f117cc586fcdfc84f07f17cd4dff51e650ff970a2ac31babd2f6b75ab2fdc87e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2692287e7ad5dbe123c2ffd6ed58d2e531277f8ee3e34cee77c07ffce4ea7e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__405ef0dfeac8819ead5cc20d24521630e131c8758db9e02eda63a82e0dd678eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc0e03ecd5d2d2156fcc9f257a2f2cd0380f19169223c2c93d45ea259806fd4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ebfc03cbc0faefa342b9dccf4fa39b33a2b3342b332b586fde5167ba1ceca2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eff1b887973c12097982f441491f8f8aafc9bb600e7e4e464c106458c99a2998(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc6cc0869a973140e8e7773b305ab3f5fdb06c5ec4b9808dff4e666c45783c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03822664c7b421f4d1c4047ae3bb2eca4290ae1b8f8fe9740de0134448029913(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa190d676b7daed005b2ed0d8875a4decc2f4585e268d8e9db3fb6457c9463d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f844e95b71a705323d7e625e018ad58d6fbe1905265628a906e8872494238979(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c32138da7fa3bf92d787f022d6dc45fcd99ee12193ef1f71b10a37fdd3482ecf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__185d8d3c58d87a9593ed5b3ecc7fd1b713aec4d866f553f718c5fde547e413f7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    engine: builtins.str,
    instance_type: builtins.str,
    bandwidth: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    io_type: typing.Optional[builtins.str] = None,
    node_num: typing.Optional[builtins.str] = None,
    partition_num: typing.Optional[builtins.str] = None,
    storage: typing.Optional[builtins.str] = None,
    storage_spec_code: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
    vm_specification: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
