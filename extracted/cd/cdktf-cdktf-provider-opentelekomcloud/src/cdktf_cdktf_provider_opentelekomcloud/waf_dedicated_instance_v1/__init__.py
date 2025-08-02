r'''
# `opentelekomcloud_waf_dedicated_instance_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_waf_dedicated_instance_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1).
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


class WafDedicatedInstanceV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedInstanceV1.WafDedicatedInstanceV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1 opentelekomcloud_waf_dedicated_instance_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        availability_zone: builtins.str,
        flavor: builtins.str,
        name: builtins.str,
        security_group: typing.Sequence[builtins.str],
        specification: builtins.str,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        architecture: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        res_tenant: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["WafDedicatedInstanceV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1 opentelekomcloud_waf_dedicated_instance_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#availability_zone WafDedicatedInstanceV1#availability_zone}.
        :param flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#flavor WafDedicatedInstanceV1#flavor}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#name WafDedicatedInstanceV1#name}.
        :param security_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#security_group WafDedicatedInstanceV1#security_group}.
        :param specification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#specification WafDedicatedInstanceV1#specification}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#subnet_id WafDedicatedInstanceV1#subnet_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#vpc_id WafDedicatedInstanceV1#vpc_id}.
        :param architecture: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#architecture WafDedicatedInstanceV1#architecture}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#id WafDedicatedInstanceV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#region WafDedicatedInstanceV1#region}.
        :param res_tenant: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#res_tenant WafDedicatedInstanceV1#res_tenant}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#timeouts WafDedicatedInstanceV1#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3be2d53284a7217f3c769ded557c91a22f4f0b0ad2c137fd4bd33de7990da053)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = WafDedicatedInstanceV1Config(
            availability_zone=availability_zone,
            flavor=flavor,
            name=name,
            security_group=security_group,
            specification=specification,
            subnet_id=subnet_id,
            vpc_id=vpc_id,
            architecture=architecture,
            id=id,
            region=region,
            res_tenant=res_tenant,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a WafDedicatedInstanceV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WafDedicatedInstanceV1 to import.
        :param import_from_id: The id of the existing WafDedicatedInstanceV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WafDedicatedInstanceV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a82b64fb6ecf96efa681c526eeecf0b775b75fe809122865c33b7043aacfa6d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#create WafDedicatedInstanceV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#delete WafDedicatedInstanceV1#delete}.
        '''
        value = WafDedicatedInstanceV1Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetArchitecture")
    def reset_architecture(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchitecture", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetResTenant")
    def reset_res_tenant(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResTenant", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="accessStatus")
    def access_status(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accessStatus"))

    @builtins.property
    @jsii.member(jsii_name="billingStatus")
    def billing_status(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "billingStatus"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="serverId")
    def server_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverId"))

    @builtins.property
    @jsii.member(jsii_name="serviceIp")
    def service_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceIp"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "WafDedicatedInstanceV1TimeoutsOutputReference":
        return typing.cast("WafDedicatedInstanceV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="upgradable")
    def upgradable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "upgradable"))

    @builtins.property
    @jsii.member(jsii_name="architectureInput")
    def architecture_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "architectureInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneInput")
    def availability_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorInput")
    def flavor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="resTenantInput")
    def res_tenant_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "resTenantInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupInput")
    def security_group_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="specificationInput")
    def specification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "specificationInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WafDedicatedInstanceV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WafDedicatedInstanceV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="architecture")
    def architecture(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "architecture"))

    @architecture.setter
    def architecture(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d63ee0bf4f5cee217519c9fd2384901c77003f7b35f5ff276a98c3a825c354ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "architecture", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6863649f5aabba79ac6d4590d3f52d3970b481c98503e7af2d7190d8b346fb92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flavor")
    def flavor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavor"))

    @flavor.setter
    def flavor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cb7c3c0f50d5403706cc372fbde5e462d709581b45faa391265b075fd2a847c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b11690715059e7c0cfd5cb4c0c44e79e5e157b0de61616179765e2d9d8417d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e83103e53cc81fe4e30719c4f061b32b058ee6f3ae3bec10de6dfad2bf680e22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa59e47b6279d258458dfd723be6c3722bf79d898fdd7bb9ba2f19df8ef4e6f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resTenant")
    def res_tenant(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "resTenant"))

    @res_tenant.setter
    def res_tenant(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94e9539a91b4cd6c5fbe5bc19252f48d75cf1f2fb5e077c37387114d21230280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resTenant", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroup"))

    @security_group.setter
    def security_group(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dc2cb77ed717823c08c4ad7b157e86a58699432edcb34b031a6b34e9d57b4b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="specification")
    def specification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "specification"))

    @specification.setter
    def specification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e39e01b24d0b267c34a2b9179ed34dd8d70a51068f6700a2b15c49143619718)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "specification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__739a9255ea0504150f85aa103a64baaac230e8c0559c57dd928d340c2d0b5e77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b2125066fc84c6b3a8642eb9d96788daaed84be6e01c226a06202344ec4f6e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedInstanceV1.WafDedicatedInstanceV1Config",
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
        "flavor": "flavor",
        "name": "name",
        "security_group": "securityGroup",
        "specification": "specification",
        "subnet_id": "subnetId",
        "vpc_id": "vpcId",
        "architecture": "architecture",
        "id": "id",
        "region": "region",
        "res_tenant": "resTenant",
        "timeouts": "timeouts",
    },
)
class WafDedicatedInstanceV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        availability_zone: builtins.str,
        flavor: builtins.str,
        name: builtins.str,
        security_group: typing.Sequence[builtins.str],
        specification: builtins.str,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        architecture: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        res_tenant: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["WafDedicatedInstanceV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#availability_zone WafDedicatedInstanceV1#availability_zone}.
        :param flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#flavor WafDedicatedInstanceV1#flavor}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#name WafDedicatedInstanceV1#name}.
        :param security_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#security_group WafDedicatedInstanceV1#security_group}.
        :param specification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#specification WafDedicatedInstanceV1#specification}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#subnet_id WafDedicatedInstanceV1#subnet_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#vpc_id WafDedicatedInstanceV1#vpc_id}.
        :param architecture: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#architecture WafDedicatedInstanceV1#architecture}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#id WafDedicatedInstanceV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#region WafDedicatedInstanceV1#region}.
        :param res_tenant: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#res_tenant WafDedicatedInstanceV1#res_tenant}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#timeouts WafDedicatedInstanceV1#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = WafDedicatedInstanceV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f545b4ac37702dadcd180e90229e1273b22a99df0b94bc867ee544447b8efb9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument flavor", value=flavor, expected_type=type_hints["flavor"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument specification", value=specification, expected_type=type_hints["specification"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument res_tenant", value=res_tenant, expected_type=type_hints["res_tenant"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "availability_zone": availability_zone,
            "flavor": flavor,
            "name": name,
            "security_group": security_group,
            "specification": specification,
            "subnet_id": subnet_id,
            "vpc_id": vpc_id,
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
        if architecture is not None:
            self._values["architecture"] = architecture
        if id is not None:
            self._values["id"] = id
        if region is not None:
            self._values["region"] = region
        if res_tenant is not None:
            self._values["res_tenant"] = res_tenant
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def availability_zone(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#availability_zone WafDedicatedInstanceV1#availability_zone}.'''
        result = self._values.get("availability_zone")
        assert result is not None, "Required property 'availability_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def flavor(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#flavor WafDedicatedInstanceV1#flavor}.'''
        result = self._values.get("flavor")
        assert result is not None, "Required property 'flavor' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#name WafDedicatedInstanceV1#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_group(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#security_group WafDedicatedInstanceV1#security_group}.'''
        result = self._values.get("security_group")
        assert result is not None, "Required property 'security_group' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def specification(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#specification WafDedicatedInstanceV1#specification}.'''
        result = self._values.get("specification")
        assert result is not None, "Required property 'specification' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#subnet_id WafDedicatedInstanceV1#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#vpc_id WafDedicatedInstanceV1#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def architecture(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#architecture WafDedicatedInstanceV1#architecture}.'''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#id WafDedicatedInstanceV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#region WafDedicatedInstanceV1#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def res_tenant(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#res_tenant WafDedicatedInstanceV1#res_tenant}.'''
        result = self._values.get("res_tenant")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["WafDedicatedInstanceV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#timeouts WafDedicatedInstanceV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["WafDedicatedInstanceV1Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDedicatedInstanceV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedInstanceV1.WafDedicatedInstanceV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class WafDedicatedInstanceV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#create WafDedicatedInstanceV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#delete WafDedicatedInstanceV1#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef43cc0d12997fb92eeb9dd6f5c03f4b72b5821027a8ef96c132a1c696c2aaa0)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#create WafDedicatedInstanceV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_instance_v1#delete WafDedicatedInstanceV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDedicatedInstanceV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafDedicatedInstanceV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedInstanceV1.WafDedicatedInstanceV1TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd1b8f55aabe85b071dfbbc10ab7cc2dedaf2a4bbb0a4ade01a9cb7e7f9dbd47)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae6c9172634e044e5a71402ddfa01a41e0bc877ef5ca796162921d551f56af4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e290e94930277572bad1e31953dda2c44a2f342a27c696f85fc19568bf6edca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedInstanceV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedInstanceV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedInstanceV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f80bbeab8ef9a985b1be437da6839d8b2d2e45ba6bd9a5e792f71ec9b46c3151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "WafDedicatedInstanceV1",
    "WafDedicatedInstanceV1Config",
    "WafDedicatedInstanceV1Timeouts",
    "WafDedicatedInstanceV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__3be2d53284a7217f3c769ded557c91a22f4f0b0ad2c137fd4bd33de7990da053(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    availability_zone: builtins.str,
    flavor: builtins.str,
    name: builtins.str,
    security_group: typing.Sequence[builtins.str],
    specification: builtins.str,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    architecture: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    res_tenant: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[WafDedicatedInstanceV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2a82b64fb6ecf96efa681c526eeecf0b775b75fe809122865c33b7043aacfa6d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63ee0bf4f5cee217519c9fd2384901c77003f7b35f5ff276a98c3a825c354ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6863649f5aabba79ac6d4590d3f52d3970b481c98503e7af2d7190d8b346fb92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb7c3c0f50d5403706cc372fbde5e462d709581b45faa391265b075fd2a847c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b11690715059e7c0cfd5cb4c0c44e79e5e157b0de61616179765e2d9d8417d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e83103e53cc81fe4e30719c4f061b32b058ee6f3ae3bec10de6dfad2bf680e22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa59e47b6279d258458dfd723be6c3722bf79d898fdd7bb9ba2f19df8ef4e6f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94e9539a91b4cd6c5fbe5bc19252f48d75cf1f2fb5e077c37387114d21230280(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dc2cb77ed717823c08c4ad7b157e86a58699432edcb34b031a6b34e9d57b4b4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e39e01b24d0b267c34a2b9179ed34dd8d70a51068f6700a2b15c49143619718(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__739a9255ea0504150f85aa103a64baaac230e8c0559c57dd928d340c2d0b5e77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b2125066fc84c6b3a8642eb9d96788daaed84be6e01c226a06202344ec4f6e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f545b4ac37702dadcd180e90229e1273b22a99df0b94bc867ee544447b8efb9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    availability_zone: builtins.str,
    flavor: builtins.str,
    name: builtins.str,
    security_group: typing.Sequence[builtins.str],
    specification: builtins.str,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    architecture: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    res_tenant: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[WafDedicatedInstanceV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef43cc0d12997fb92eeb9dd6f5c03f4b72b5821027a8ef96c132a1c696c2aaa0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd1b8f55aabe85b071dfbbc10ab7cc2dedaf2a4bbb0a4ade01a9cb7e7f9dbd47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae6c9172634e044e5a71402ddfa01a41e0bc877ef5ca796162921d551f56af4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e290e94930277572bad1e31953dda2c44a2f342a27c696f85fc19568bf6edca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f80bbeab8ef9a985b1be437da6839d8b2d2e45ba6bd9a5e792f71ec9b46c3151(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedInstanceV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
