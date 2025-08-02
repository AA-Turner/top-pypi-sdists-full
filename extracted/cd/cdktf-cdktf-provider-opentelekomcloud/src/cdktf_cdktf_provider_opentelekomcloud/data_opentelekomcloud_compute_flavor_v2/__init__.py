r'''
# `data_opentelekomcloud_compute_flavor_v2`

Refer to the Terraform Registry for docs: [`data_opentelekomcloud_compute_flavor_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2).
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


class DataOpentelekomcloudComputeFlavorV2(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudComputeFlavorV2.DataOpentelekomcloudComputeFlavorV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2 opentelekomcloud_compute_flavor_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        availability_zone: typing.Optional[builtins.str] = None,
        disk: typing.Optional[jsii.Number] = None,
        flavor_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        min_disk: typing.Optional[jsii.Number] = None,
        min_ram: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        ram: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[builtins.str] = None,
        rx_tx_factor: typing.Optional[jsii.Number] = None,
        swap: typing.Optional[jsii.Number] = None,
        vcpus: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2 opentelekomcloud_compute_flavor_v2} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#availability_zone DataOpentelekomcloudComputeFlavorV2#availability_zone}.
        :param disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#disk DataOpentelekomcloudComputeFlavorV2#disk}.
        :param flavor_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#flavor_id DataOpentelekomcloudComputeFlavorV2#flavor_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#id DataOpentelekomcloudComputeFlavorV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param min_disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#min_disk DataOpentelekomcloudComputeFlavorV2#min_disk}.
        :param min_ram: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#min_ram DataOpentelekomcloudComputeFlavorV2#min_ram}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#name DataOpentelekomcloudComputeFlavorV2#name}.
        :param ram: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#ram DataOpentelekomcloudComputeFlavorV2#ram}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#region DataOpentelekomcloudComputeFlavorV2#region}.
        :param resource_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#resource_type DataOpentelekomcloudComputeFlavorV2#resource_type}.
        :param rx_tx_factor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#rx_tx_factor DataOpentelekomcloudComputeFlavorV2#rx_tx_factor}.
        :param swap: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#swap DataOpentelekomcloudComputeFlavorV2#swap}.
        :param vcpus: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#vcpus DataOpentelekomcloudComputeFlavorV2#vcpus}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ddd8031c58151f9b08565398b10f1b8b61c46baae28d96777d2b3a516f92945)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataOpentelekomcloudComputeFlavorV2Config(
            availability_zone=availability_zone,
            disk=disk,
            flavor_id=flavor_id,
            id=id,
            min_disk=min_disk,
            min_ram=min_ram,
            name=name,
            ram=ram,
            region=region,
            resource_type=resource_type,
            rx_tx_factor=rx_tx_factor,
            swap=swap,
            vcpus=vcpus,
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
        '''Generates CDKTF code for importing a DataOpentelekomcloudComputeFlavorV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOpentelekomcloudComputeFlavorV2 to import.
        :param import_from_id: The id of the existing DataOpentelekomcloudComputeFlavorV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOpentelekomcloudComputeFlavorV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__884b257601db4066f82410b9ff043b9e238f17f93c82b205b2640bffd746dd9c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAvailabilityZone")
    def reset_availability_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityZone", []))

    @jsii.member(jsii_name="resetDisk")
    def reset_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisk", []))

    @jsii.member(jsii_name="resetFlavorId")
    def reset_flavor_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlavorId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMinDisk")
    def reset_min_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinDisk", []))

    @jsii.member(jsii_name="resetMinRam")
    def reset_min_ram(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinRam", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetRam")
    def reset_ram(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRam", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetResourceType")
    def reset_resource_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceType", []))

    @jsii.member(jsii_name="resetRxTxFactor")
    def reset_rx_tx_factor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRxTxFactor", []))

    @jsii.member(jsii_name="resetSwap")
    def reset_swap(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSwap", []))

    @jsii.member(jsii_name="resetVcpus")
    def reset_vcpus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVcpus", []))

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
    @jsii.member(jsii_name="extraSpecs")
    def extra_specs(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "extraSpecs"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneInput")
    def availability_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="diskInput")
    def disk_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorIdInput")
    def flavor_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="minDiskInput")
    def min_disk_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="minRamInput")
    def min_ram_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minRamInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="ramInput")
    def ram_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ramInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypeInput")
    def resource_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="rxTxFactorInput")
    def rx_tx_factor_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rxTxFactorInput"))

    @builtins.property
    @jsii.member(jsii_name="swapInput")
    def swap_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "swapInput"))

    @builtins.property
    @jsii.member(jsii_name="vcpusInput")
    def vcpus_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vcpusInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b61d1fdbaead17d84d1f9e1c6d59b3f556fe0e8a7952a60e9b856b8c9e3563d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disk")
    def disk(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "disk"))

    @disk.setter
    def disk(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9efd05d1f530d9c51897e2b37b8adc65bbab876331a87504f621e1abb6f6960b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flavorId")
    def flavor_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavorId"))

    @flavor_id.setter
    def flavor_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e146dbf84e3c99e403941acf8162d373efbdc1e8f0808c4fb6d1b5a48249b0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavorId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b02d82d76d136c13382e0c9f526708915184be875f74002a609b6fd9c7ae1df0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minDisk")
    def min_disk(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minDisk"))

    @min_disk.setter
    def min_disk(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4c81315a67cb7b2c4fef0fef7ded0e2cbbcd13bded809d3e01279fb394a162a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minDisk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minRam")
    def min_ram(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minRam"))

    @min_ram.setter
    def min_ram(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ba4ae9ffec710a5e5ec2cb96d550f3595f0fb7b0d5486c30df513d525ff51df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minRam", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3db93a629ff923d68ede17e9e510386d9f27783a539c15596aca3223aa9048d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ram")
    def ram(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ram"))

    @ram.setter
    def ram(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ba4ead334fc69ca522be6e1be7400037bf622e9da0a75da976d8435de70a105)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ram", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b333bf8398c3b5fcd329b46b3498884caad60a84e78da4a3ec0a59b5bf00fdc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82df31dbe832ce65d17d164b6a2684337bd815736b6797d1f6b14b233a1f654b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rxTxFactor")
    def rx_tx_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rxTxFactor"))

    @rx_tx_factor.setter
    def rx_tx_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d06d0006976a97c64e2ebf43ccf9a0e2f9dc1c99429818f18338d39dca85b58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rxTxFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="swap")
    def swap(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "swap"))

    @swap.setter
    def swap(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4151edede4edcd00e50a113436da073ae8d3e954b2b4aa305c2d54e0790ed683)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "swap", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vcpus")
    def vcpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vcpus"))

    @vcpus.setter
    def vcpus(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3d6dd4abf21352b680d755a66e936f1990503600e18cc9b76085a70e0c1b571)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vcpus", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudComputeFlavorV2.DataOpentelekomcloudComputeFlavorV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "availability_zone": "availabilityZone",
        "disk": "disk",
        "flavor_id": "flavorId",
        "id": "id",
        "min_disk": "minDisk",
        "min_ram": "minRam",
        "name": "name",
        "ram": "ram",
        "region": "region",
        "resource_type": "resourceType",
        "rx_tx_factor": "rxTxFactor",
        "swap": "swap",
        "vcpus": "vcpus",
    },
)
class DataOpentelekomcloudComputeFlavorV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        availability_zone: typing.Optional[builtins.str] = None,
        disk: typing.Optional[jsii.Number] = None,
        flavor_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        min_disk: typing.Optional[jsii.Number] = None,
        min_ram: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        ram: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[builtins.str] = None,
        rx_tx_factor: typing.Optional[jsii.Number] = None,
        swap: typing.Optional[jsii.Number] = None,
        vcpus: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#availability_zone DataOpentelekomcloudComputeFlavorV2#availability_zone}.
        :param disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#disk DataOpentelekomcloudComputeFlavorV2#disk}.
        :param flavor_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#flavor_id DataOpentelekomcloudComputeFlavorV2#flavor_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#id DataOpentelekomcloudComputeFlavorV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param min_disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#min_disk DataOpentelekomcloudComputeFlavorV2#min_disk}.
        :param min_ram: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#min_ram DataOpentelekomcloudComputeFlavorV2#min_ram}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#name DataOpentelekomcloudComputeFlavorV2#name}.
        :param ram: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#ram DataOpentelekomcloudComputeFlavorV2#ram}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#region DataOpentelekomcloudComputeFlavorV2#region}.
        :param resource_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#resource_type DataOpentelekomcloudComputeFlavorV2#resource_type}.
        :param rx_tx_factor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#rx_tx_factor DataOpentelekomcloudComputeFlavorV2#rx_tx_factor}.
        :param swap: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#swap DataOpentelekomcloudComputeFlavorV2#swap}.
        :param vcpus: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#vcpus DataOpentelekomcloudComputeFlavorV2#vcpus}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe89fd2982447ffa64907ad190cd37e26ea356b56e92b1d3f38fccfdb5deb7bc)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument disk", value=disk, expected_type=type_hints["disk"])
            check_type(argname="argument flavor_id", value=flavor_id, expected_type=type_hints["flavor_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument min_disk", value=min_disk, expected_type=type_hints["min_disk"])
            check_type(argname="argument min_ram", value=min_ram, expected_type=type_hints["min_ram"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ram", value=ram, expected_type=type_hints["ram"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument rx_tx_factor", value=rx_tx_factor, expected_type=type_hints["rx_tx_factor"])
            check_type(argname="argument swap", value=swap, expected_type=type_hints["swap"])
            check_type(argname="argument vcpus", value=vcpus, expected_type=type_hints["vcpus"])
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
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if disk is not None:
            self._values["disk"] = disk
        if flavor_id is not None:
            self._values["flavor_id"] = flavor_id
        if id is not None:
            self._values["id"] = id
        if min_disk is not None:
            self._values["min_disk"] = min_disk
        if min_ram is not None:
            self._values["min_ram"] = min_ram
        if name is not None:
            self._values["name"] = name
        if ram is not None:
            self._values["ram"] = ram
        if region is not None:
            self._values["region"] = region
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if rx_tx_factor is not None:
            self._values["rx_tx_factor"] = rx_tx_factor
        if swap is not None:
            self._values["swap"] = swap
        if vcpus is not None:
            self._values["vcpus"] = vcpus

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
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#availability_zone DataOpentelekomcloudComputeFlavorV2#availability_zone}.'''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#disk DataOpentelekomcloudComputeFlavorV2#disk}.'''
        result = self._values.get("disk")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def flavor_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#flavor_id DataOpentelekomcloudComputeFlavorV2#flavor_id}.'''
        result = self._values.get("flavor_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#id DataOpentelekomcloudComputeFlavorV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_disk(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#min_disk DataOpentelekomcloudComputeFlavorV2#min_disk}.'''
        result = self._values.get("min_disk")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_ram(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#min_ram DataOpentelekomcloudComputeFlavorV2#min_ram}.'''
        result = self._values.get("min_ram")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#name DataOpentelekomcloudComputeFlavorV2#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ram(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#ram DataOpentelekomcloudComputeFlavorV2#ram}.'''
        result = self._values.get("ram")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#region DataOpentelekomcloudComputeFlavorV2#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#resource_type DataOpentelekomcloudComputeFlavorV2#resource_type}.'''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rx_tx_factor(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#rx_tx_factor DataOpentelekomcloudComputeFlavorV2#rx_tx_factor}.'''
        result = self._values.get("rx_tx_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def swap(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#swap DataOpentelekomcloudComputeFlavorV2#swap}.'''
        result = self._values.get("swap")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vcpus(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/compute_flavor_v2#vcpus DataOpentelekomcloudComputeFlavorV2#vcpus}.'''
        result = self._values.get("vcpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudComputeFlavorV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataOpentelekomcloudComputeFlavorV2",
    "DataOpentelekomcloudComputeFlavorV2Config",
]

publication.publish()

def _typecheckingstub__4ddd8031c58151f9b08565398b10f1b8b61c46baae28d96777d2b3a516f92945(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    disk: typing.Optional[jsii.Number] = None,
    flavor_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    min_disk: typing.Optional[jsii.Number] = None,
    min_ram: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    ram: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    resource_type: typing.Optional[builtins.str] = None,
    rx_tx_factor: typing.Optional[jsii.Number] = None,
    swap: typing.Optional[jsii.Number] = None,
    vcpus: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__884b257601db4066f82410b9ff043b9e238f17f93c82b205b2640bffd746dd9c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b61d1fdbaead17d84d1f9e1c6d59b3f556fe0e8a7952a60e9b856b8c9e3563d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9efd05d1f530d9c51897e2b37b8adc65bbab876331a87504f621e1abb6f6960b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e146dbf84e3c99e403941acf8162d373efbdc1e8f0808c4fb6d1b5a48249b0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b02d82d76d136c13382e0c9f526708915184be875f74002a609b6fd9c7ae1df0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4c81315a67cb7b2c4fef0fef7ded0e2cbbcd13bded809d3e01279fb394a162a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ba4ae9ffec710a5e5ec2cb96d550f3595f0fb7b0d5486c30df513d525ff51df(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3db93a629ff923d68ede17e9e510386d9f27783a539c15596aca3223aa9048d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ba4ead334fc69ca522be6e1be7400037bf622e9da0a75da976d8435de70a105(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b333bf8398c3b5fcd329b46b3498884caad60a84e78da4a3ec0a59b5bf00fdc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82df31dbe832ce65d17d164b6a2684337bd815736b6797d1f6b14b233a1f654b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d06d0006976a97c64e2ebf43ccf9a0e2f9dc1c99429818f18338d39dca85b58(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4151edede4edcd00e50a113436da073ae8d3e954b2b4aa305c2d54e0790ed683(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d6dd4abf21352b680d755a66e936f1990503600e18cc9b76085a70e0c1b571(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe89fd2982447ffa64907ad190cd37e26ea356b56e92b1d3f38fccfdb5deb7bc(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    availability_zone: typing.Optional[builtins.str] = None,
    disk: typing.Optional[jsii.Number] = None,
    flavor_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    min_disk: typing.Optional[jsii.Number] = None,
    min_ram: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    ram: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    resource_type: typing.Optional[builtins.str] = None,
    rx_tx_factor: typing.Optional[jsii.Number] = None,
    swap: typing.Optional[jsii.Number] = None,
    vcpus: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
