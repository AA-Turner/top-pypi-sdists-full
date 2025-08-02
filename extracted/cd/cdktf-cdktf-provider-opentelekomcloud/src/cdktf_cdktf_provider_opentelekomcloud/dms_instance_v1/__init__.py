r'''
# `opentelekomcloud_dms_instance_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_dms_instance_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1).
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


class DmsInstanceV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dmsInstanceV1.DmsInstanceV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1 opentelekomcloud_dms_instance_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        available_zones: typing.Sequence[builtins.str],
        engine: builtins.str,
        engine_version: builtins.str,
        name: builtins.str,
        product_id: builtins.str,
        security_group_id: builtins.str,
        storage_space: jsii.Number,
        storage_spec_code: builtins.str,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        access_user: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        maintain_begin: typing.Optional[builtins.str] = None,
        maintain_end: typing.Optional[builtins.str] = None,
        partition_num: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        retention_policy: typing.Optional[builtins.str] = None,
        specification: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1 opentelekomcloud_dms_instance_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param available_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#available_zones DmsInstanceV1#available_zones}.
        :param engine: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#engine DmsInstanceV1#engine}.
        :param engine_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#engine_version DmsInstanceV1#engine_version}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#name DmsInstanceV1#name}.
        :param product_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#product_id DmsInstanceV1#product_id}.
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#security_group_id DmsInstanceV1#security_group_id}.
        :param storage_space: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#storage_space DmsInstanceV1#storage_space}.
        :param storage_spec_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#storage_spec_code DmsInstanceV1#storage_spec_code}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#subnet_id DmsInstanceV1#subnet_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#vpc_id DmsInstanceV1#vpc_id}.
        :param access_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#access_user DmsInstanceV1#access_user}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#description DmsInstanceV1#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#id DmsInstanceV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintain_begin: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#maintain_begin DmsInstanceV1#maintain_begin}.
        :param maintain_end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#maintain_end DmsInstanceV1#maintain_end}.
        :param partition_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#partition_num DmsInstanceV1#partition_num}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#password DmsInstanceV1#password}.
        :param retention_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#retention_policy DmsInstanceV1#retention_policy}.
        :param specification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#specification DmsInstanceV1#specification}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bb114ba721b8e95570a6a109167ef2eaa387f7e48db0f896e6f29be89d523c3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DmsInstanceV1Config(
            available_zones=available_zones,
            engine=engine,
            engine_version=engine_version,
            name=name,
            product_id=product_id,
            security_group_id=security_group_id,
            storage_space=storage_space,
            storage_spec_code=storage_spec_code,
            subnet_id=subnet_id,
            vpc_id=vpc_id,
            access_user=access_user,
            description=description,
            id=id,
            maintain_begin=maintain_begin,
            maintain_end=maintain_end,
            partition_num=partition_num,
            password=password,
            retention_policy=retention_policy,
            specification=specification,
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
        '''Generates CDKTF code for importing a DmsInstanceV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DmsInstanceV1 to import.
        :param import_from_id: The id of the existing DmsInstanceV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DmsInstanceV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e724f03c5596b71fc1f120c7fd11b5cc896ed544591780dd8ea9e14c24eba403)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAccessUser")
    def reset_access_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessUser", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaintainBegin")
    def reset_maintain_begin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintainBegin", []))

    @jsii.member(jsii_name="resetMaintainEnd")
    def reset_maintain_end(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintainEnd", []))

    @jsii.member(jsii_name="resetPartitionNum")
    def reset_partition_num(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartitionNum", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetRetentionPolicy")
    def reset_retention_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPolicy", []))

    @jsii.member(jsii_name="resetSpecification")
    def reset_specification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpecification", []))

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
    @jsii.member(jsii_name="connectAddress")
    def connect_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectAddress"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="orderId")
    def order_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orderId"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="resourceSpecCode")
    def resource_spec_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceSpecCode"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupName")
    def security_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupName"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="subnetName")
    def subnet_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetName"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="usedStorageSpace")
    def used_storage_space(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "usedStorageSpace"))

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userId"))

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @builtins.property
    @jsii.member(jsii_name="vpcName")
    def vpc_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcName"))

    @builtins.property
    @jsii.member(jsii_name="accessUserInput")
    def access_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessUserInput"))

    @builtins.property
    @jsii.member(jsii_name="availableZonesInput")
    def available_zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "availableZonesInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="engineInput")
    def engine_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineInput"))

    @builtins.property
    @jsii.member(jsii_name="engineVersionInput")
    def engine_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="maintainBeginInput")
    def maintain_begin_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maintainBeginInput"))

    @builtins.property
    @jsii.member(jsii_name="maintainEndInput")
    def maintain_end_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maintainEndInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionNumInput")
    def partition_num_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "partitionNumInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="productIdInput")
    def product_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "productIdInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyInput")
    def retention_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdInput")
    def security_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="specificationInput")
    def specification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "specificationInput"))

    @builtins.property
    @jsii.member(jsii_name="storageSpaceInput")
    def storage_space_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "storageSpaceInput"))

    @builtins.property
    @jsii.member(jsii_name="storageSpecCodeInput")
    def storage_spec_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageSpecCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accessUser")
    def access_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessUser"))

    @access_user.setter
    def access_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__436e3045d965762146d1bcfbfc13ff2d560206e5c7002cccf9c9a1e88ba3d362)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availableZones")
    def available_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availableZones"))

    @available_zones.setter
    def available_zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f3f3ff550a2ac5e556e9218c87b13ea3069df8eccd0ef83f7377afeaa74ca85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availableZones", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca0614abb2fcdea760cdfd7c6e5ee6357f216bf98bf4907d30b70991b84759be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engine")
    def engine(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engine"))

    @engine.setter
    def engine(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d2e32235d8af5bdfd7482b65de759239012ea60d4e142786e1108852190b788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engineVersion"))

    @engine_version.setter
    def engine_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a78d86033b3c39a7b0c9edbf997771be901c52709f717ce462056d0a07feafa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3c1b599c8c1523532655f8467ec6a0baec7dbeedbf1e3c9845eef145bafecb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintainBegin")
    def maintain_begin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintainBegin"))

    @maintain_begin.setter
    def maintain_begin(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fbf72ed33da6124c51cb8326070f90384748dfdc5b846904c38c7245be419cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintainBegin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintainEnd")
    def maintain_end(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintainEnd"))

    @maintain_end.setter
    def maintain_end(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__685137a1b24e439c38ea93f75e03ffdc2ed58183b06814261d102b17ad96c2ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintainEnd", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b00cf5c52be4c4a8567d08fe911a83139f0ab8eec7cffa7f76f10f65508e184)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partitionNum")
    def partition_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "partitionNum"))

    @partition_num.setter
    def partition_num(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c46e5252bf739b0392c812c23b8d756ee36f0c0651fca885dfe8254fd3918656)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitionNum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30ffba94d018bb868c6813b0a4a1d8927f2375b6c17267c50d8902d16fdafe28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="productId")
    def product_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "productId"))

    @product_id.setter
    def product_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__616650ba64862d22fb282996c5f5e3baf11f674f53ff56df844889edfc186a48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionPolicy")
    def retention_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionPolicy"))

    @retention_policy.setter
    def retention_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d39274c0622897d706208ca018aadb13eb8d6f24ff5ade2d502c1a58fb96acb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupId"))

    @security_group_id.setter
    def security_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6f7a0a1ce233f0f5c93ebcc3a9f7579b0edf5bdc1ea86e2a29a45ab29eab9e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="specification")
    def specification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "specification"))

    @specification.setter
    def specification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72fd5837393d8a2b2f462e17f6bdeded2ac98a7a73228ac4f665ee32a4dc6e5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "specification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageSpace")
    def storage_space(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageSpace"))

    @storage_space.setter
    def storage_space(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42f28550d3f19991ba2155a662404a3ce01c2e989f8d87aa9a06c33ec65813f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageSpace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageSpecCode")
    def storage_spec_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageSpecCode"))

    @storage_spec_code.setter
    def storage_spec_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c5603cb4251981d5060ef882b33163cfba5a685233f23f24273cd7f7357eff7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageSpecCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8d820595ac263f4a10b3c2c66cf3312941f50885a65b4b9a13764f2cc763aee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8c4200130f8283da67105724a78587eed3c127da1afc5c2ee74cb87ec4cd46c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dmsInstanceV1.DmsInstanceV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "available_zones": "availableZones",
        "engine": "engine",
        "engine_version": "engineVersion",
        "name": "name",
        "product_id": "productId",
        "security_group_id": "securityGroupId",
        "storage_space": "storageSpace",
        "storage_spec_code": "storageSpecCode",
        "subnet_id": "subnetId",
        "vpc_id": "vpcId",
        "access_user": "accessUser",
        "description": "description",
        "id": "id",
        "maintain_begin": "maintainBegin",
        "maintain_end": "maintainEnd",
        "partition_num": "partitionNum",
        "password": "password",
        "retention_policy": "retentionPolicy",
        "specification": "specification",
    },
)
class DmsInstanceV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        available_zones: typing.Sequence[builtins.str],
        engine: builtins.str,
        engine_version: builtins.str,
        name: builtins.str,
        product_id: builtins.str,
        security_group_id: builtins.str,
        storage_space: jsii.Number,
        storage_spec_code: builtins.str,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        access_user: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        maintain_begin: typing.Optional[builtins.str] = None,
        maintain_end: typing.Optional[builtins.str] = None,
        partition_num: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        retention_policy: typing.Optional[builtins.str] = None,
        specification: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param available_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#available_zones DmsInstanceV1#available_zones}.
        :param engine: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#engine DmsInstanceV1#engine}.
        :param engine_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#engine_version DmsInstanceV1#engine_version}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#name DmsInstanceV1#name}.
        :param product_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#product_id DmsInstanceV1#product_id}.
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#security_group_id DmsInstanceV1#security_group_id}.
        :param storage_space: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#storage_space DmsInstanceV1#storage_space}.
        :param storage_spec_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#storage_spec_code DmsInstanceV1#storage_spec_code}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#subnet_id DmsInstanceV1#subnet_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#vpc_id DmsInstanceV1#vpc_id}.
        :param access_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#access_user DmsInstanceV1#access_user}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#description DmsInstanceV1#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#id DmsInstanceV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintain_begin: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#maintain_begin DmsInstanceV1#maintain_begin}.
        :param maintain_end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#maintain_end DmsInstanceV1#maintain_end}.
        :param partition_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#partition_num DmsInstanceV1#partition_num}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#password DmsInstanceV1#password}.
        :param retention_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#retention_policy DmsInstanceV1#retention_policy}.
        :param specification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#specification DmsInstanceV1#specification}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__873e468040c37b1e7d48e2a71626f1f22f4896dfee1c3c376708b2dcfae7de6c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument available_zones", value=available_zones, expected_type=type_hints["available_zones"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
            check_type(argname="argument security_group_id", value=security_group_id, expected_type=type_hints["security_group_id"])
            check_type(argname="argument storage_space", value=storage_space, expected_type=type_hints["storage_space"])
            check_type(argname="argument storage_spec_code", value=storage_spec_code, expected_type=type_hints["storage_spec_code"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument access_user", value=access_user, expected_type=type_hints["access_user"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument maintain_begin", value=maintain_begin, expected_type=type_hints["maintain_begin"])
            check_type(argname="argument maintain_end", value=maintain_end, expected_type=type_hints["maintain_end"])
            check_type(argname="argument partition_num", value=partition_num, expected_type=type_hints["partition_num"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument retention_policy", value=retention_policy, expected_type=type_hints["retention_policy"])
            check_type(argname="argument specification", value=specification, expected_type=type_hints["specification"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "available_zones": available_zones,
            "engine": engine,
            "engine_version": engine_version,
            "name": name,
            "product_id": product_id,
            "security_group_id": security_group_id,
            "storage_space": storage_space,
            "storage_spec_code": storage_spec_code,
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
        if access_user is not None:
            self._values["access_user"] = access_user
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if maintain_begin is not None:
            self._values["maintain_begin"] = maintain_begin
        if maintain_end is not None:
            self._values["maintain_end"] = maintain_end
        if partition_num is not None:
            self._values["partition_num"] = partition_num
        if password is not None:
            self._values["password"] = password
        if retention_policy is not None:
            self._values["retention_policy"] = retention_policy
        if specification is not None:
            self._values["specification"] = specification

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
    def available_zones(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#available_zones DmsInstanceV1#available_zones}.'''
        result = self._values.get("available_zones")
        assert result is not None, "Required property 'available_zones' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def engine(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#engine DmsInstanceV1#engine}.'''
        result = self._values.get("engine")
        assert result is not None, "Required property 'engine' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def engine_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#engine_version DmsInstanceV1#engine_version}.'''
        result = self._values.get("engine_version")
        assert result is not None, "Required property 'engine_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#name DmsInstanceV1#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def product_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#product_id DmsInstanceV1#product_id}.'''
        result = self._values.get("product_id")
        assert result is not None, "Required property 'product_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#security_group_id DmsInstanceV1#security_group_id}.'''
        result = self._values.get("security_group_id")
        assert result is not None, "Required property 'security_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_space(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#storage_space DmsInstanceV1#storage_space}.'''
        result = self._values.get("storage_space")
        assert result is not None, "Required property 'storage_space' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def storage_spec_code(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#storage_spec_code DmsInstanceV1#storage_spec_code}.'''
        result = self._values.get("storage_spec_code")
        assert result is not None, "Required property 'storage_spec_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#subnet_id DmsInstanceV1#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#vpc_id DmsInstanceV1#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_user(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#access_user DmsInstanceV1#access_user}.'''
        result = self._values.get("access_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#description DmsInstanceV1#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#id DmsInstanceV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintain_begin(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#maintain_begin DmsInstanceV1#maintain_begin}.'''
        result = self._values.get("maintain_begin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintain_end(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#maintain_end DmsInstanceV1#maintain_end}.'''
        result = self._values.get("maintain_end")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partition_num(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#partition_num DmsInstanceV1#partition_num}.'''
        result = self._values.get("partition_num")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#password DmsInstanceV1#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#retention_policy DmsInstanceV1#retention_policy}.'''
        result = self._values.get("retention_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def specification(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v1#specification DmsInstanceV1#specification}.'''
        result = self._values.get("specification")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsInstanceV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DmsInstanceV1",
    "DmsInstanceV1Config",
]

publication.publish()

def _typecheckingstub__1bb114ba721b8e95570a6a109167ef2eaa387f7e48db0f896e6f29be89d523c3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    available_zones: typing.Sequence[builtins.str],
    engine: builtins.str,
    engine_version: builtins.str,
    name: builtins.str,
    product_id: builtins.str,
    security_group_id: builtins.str,
    storage_space: jsii.Number,
    storage_spec_code: builtins.str,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    access_user: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    maintain_begin: typing.Optional[builtins.str] = None,
    maintain_end: typing.Optional[builtins.str] = None,
    partition_num: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    retention_policy: typing.Optional[builtins.str] = None,
    specification: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__e724f03c5596b71fc1f120c7fd11b5cc896ed544591780dd8ea9e14c24eba403(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__436e3045d965762146d1bcfbfc13ff2d560206e5c7002cccf9c9a1e88ba3d362(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3f3ff550a2ac5e556e9218c87b13ea3069df8eccd0ef83f7377afeaa74ca85(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca0614abb2fcdea760cdfd7c6e5ee6357f216bf98bf4907d30b70991b84759be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d2e32235d8af5bdfd7482b65de759239012ea60d4e142786e1108852190b788(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a78d86033b3c39a7b0c9edbf997771be901c52709f717ce462056d0a07feafa7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3c1b599c8c1523532655f8467ec6a0baec7dbeedbf1e3c9845eef145bafecb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fbf72ed33da6124c51cb8326070f90384748dfdc5b846904c38c7245be419cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__685137a1b24e439c38ea93f75e03ffdc2ed58183b06814261d102b17ad96c2ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b00cf5c52be4c4a8567d08fe911a83139f0ab8eec7cffa7f76f10f65508e184(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c46e5252bf739b0392c812c23b8d756ee36f0c0651fca885dfe8254fd3918656(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ffba94d018bb868c6813b0a4a1d8927f2375b6c17267c50d8902d16fdafe28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__616650ba64862d22fb282996c5f5e3baf11f674f53ff56df844889edfc186a48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d39274c0622897d706208ca018aadb13eb8d6f24ff5ade2d502c1a58fb96acb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f7a0a1ce233f0f5c93ebcc3a9f7579b0edf5bdc1ea86e2a29a45ab29eab9e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72fd5837393d8a2b2f462e17f6bdeded2ac98a7a73228ac4f665ee32a4dc6e5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f28550d3f19991ba2155a662404a3ce01c2e989f8d87aa9a06c33ec65813f1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c5603cb4251981d5060ef882b33163cfba5a685233f23f24273cd7f7357eff7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d820595ac263f4a10b3c2c66cf3312941f50885a65b4b9a13764f2cc763aee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8c4200130f8283da67105724a78587eed3c127da1afc5c2ee74cb87ec4cd46c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873e468040c37b1e7d48e2a71626f1f22f4896dfee1c3c376708b2dcfae7de6c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    available_zones: typing.Sequence[builtins.str],
    engine: builtins.str,
    engine_version: builtins.str,
    name: builtins.str,
    product_id: builtins.str,
    security_group_id: builtins.str,
    storage_space: jsii.Number,
    storage_spec_code: builtins.str,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    access_user: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    maintain_begin: typing.Optional[builtins.str] = None,
    maintain_end: typing.Optional[builtins.str] = None,
    partition_num: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    retention_policy: typing.Optional[builtins.str] = None,
    specification: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
