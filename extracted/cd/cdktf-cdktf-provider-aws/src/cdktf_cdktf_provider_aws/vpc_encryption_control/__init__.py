r'''
# `aws_vpc_encryption_control`

Refer to the Terraform Registry for docs: [`aws_vpc_encryption_control`](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control).
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


class VpcEncryptionControl(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.vpcEncryptionControl.VpcEncryptionControl",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control aws_vpc_encryption_control}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        mode: builtins.str,
        vpc_id: builtins.str,
        egress_only_internet_gateway_exclusion: typing.Optional[builtins.str] = None,
        elastic_file_system_exclusion: typing.Optional[builtins.str] = None,
        internet_gateway_exclusion: typing.Optional[builtins.str] = None,
        lambda_exclusion: typing.Optional[builtins.str] = None,
        nat_gateway_exclusion: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["VpcEncryptionControlTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_private_gateway_exclusion: typing.Optional[builtins.str] = None,
        vpc_lattice_exclusion: typing.Optional[builtins.str] = None,
        vpc_peering_exclusion: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control aws_vpc_encryption_control} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#mode VpcEncryptionControl#mode}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#vpc_id VpcEncryptionControl#vpc_id}.
        :param egress_only_internet_gateway_exclusion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#egress_only_internet_gateway_exclusion VpcEncryptionControl#egress_only_internet_gateway_exclusion}.
        :param elastic_file_system_exclusion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#elastic_file_system_exclusion VpcEncryptionControl#elastic_file_system_exclusion}.
        :param internet_gateway_exclusion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#internet_gateway_exclusion VpcEncryptionControl#internet_gateway_exclusion}.
        :param lambda_exclusion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#lambda_exclusion VpcEncryptionControl#lambda_exclusion}.
        :param nat_gateway_exclusion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#nat_gateway_exclusion VpcEncryptionControl#nat_gateway_exclusion}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#region VpcEncryptionControl#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#tags VpcEncryptionControl#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#timeouts VpcEncryptionControl#timeouts}
        :param virtual_private_gateway_exclusion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#virtual_private_gateway_exclusion VpcEncryptionControl#virtual_private_gateway_exclusion}.
        :param vpc_lattice_exclusion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#vpc_lattice_exclusion VpcEncryptionControl#vpc_lattice_exclusion}.
        :param vpc_peering_exclusion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#vpc_peering_exclusion VpcEncryptionControl#vpc_peering_exclusion}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0d6ad2075dc90cabcbd5510b23dd0af6a612d56656da89d0f533692c4a1e25c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = VpcEncryptionControlConfig(
            mode=mode,
            vpc_id=vpc_id,
            egress_only_internet_gateway_exclusion=egress_only_internet_gateway_exclusion,
            elastic_file_system_exclusion=elastic_file_system_exclusion,
            internet_gateway_exclusion=internet_gateway_exclusion,
            lambda_exclusion=lambda_exclusion,
            nat_gateway_exclusion=nat_gateway_exclusion,
            region=region,
            tags=tags,
            timeouts=timeouts,
            virtual_private_gateway_exclusion=virtual_private_gateway_exclusion,
            vpc_lattice_exclusion=vpc_lattice_exclusion,
            vpc_peering_exclusion=vpc_peering_exclusion,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a VpcEncryptionControl resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VpcEncryptionControl to import.
        :param import_from_id: The id of the existing VpcEncryptionControl that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VpcEncryptionControl to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee22fefb929805d7acc076c944023363e664881ef596834383a32a803c6a00fc)
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
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#create VpcEncryptionControl#create}
        :param delete: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#delete VpcEncryptionControl#delete}
        :param update: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#update VpcEncryptionControl#update}
        '''
        value = VpcEncryptionControlTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetEgressOnlyInternetGatewayExclusion")
    def reset_egress_only_internet_gateway_exclusion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgressOnlyInternetGatewayExclusion", []))

    @jsii.member(jsii_name="resetElasticFileSystemExclusion")
    def reset_elastic_file_system_exclusion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticFileSystemExclusion", []))

    @jsii.member(jsii_name="resetInternetGatewayExclusion")
    def reset_internet_gateway_exclusion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternetGatewayExclusion", []))

    @jsii.member(jsii_name="resetLambdaExclusion")
    def reset_lambda_exclusion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaExclusion", []))

    @jsii.member(jsii_name="resetNatGatewayExclusion")
    def reset_nat_gateway_exclusion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNatGatewayExclusion", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVirtualPrivateGatewayExclusion")
    def reset_virtual_private_gateway_exclusion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualPrivateGatewayExclusion", []))

    @jsii.member(jsii_name="resetVpcLatticeExclusion")
    def reset_vpc_lattice_exclusion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcLatticeExclusion", []))

    @jsii.member(jsii_name="resetVpcPeeringExclusion")
    def reset_vpc_peering_exclusion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcPeeringExclusion", []))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="resourceExclusions")
    def resource_exclusions(
        self,
    ) -> "VpcEncryptionControlResourceExclusionsOutputReference":
        return typing.cast("VpcEncryptionControlResourceExclusionsOutputReference", jsii.get(self, "resourceExclusions"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateMessage")
    def state_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateMessage"))

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tagsAll"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VpcEncryptionControlTimeoutsOutputReference":
        return typing.cast("VpcEncryptionControlTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="egressOnlyInternetGatewayExclusionInput")
    def egress_only_internet_gateway_exclusion_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "egressOnlyInternetGatewayExclusionInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticFileSystemExclusionInput")
    def elastic_file_system_exclusion_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "elasticFileSystemExclusionInput"))

    @builtins.property
    @jsii.member(jsii_name="internetGatewayExclusionInput")
    def internet_gateway_exclusion_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "internetGatewayExclusionInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaExclusionInput")
    def lambda_exclusion_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lambdaExclusionInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="natGatewayExclusionInput")
    def nat_gateway_exclusion_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "natGatewayExclusionInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VpcEncryptionControlTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VpcEncryptionControlTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualPrivateGatewayExclusionInput")
    def virtual_private_gateway_exclusion_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualPrivateGatewayExclusionInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcLatticeExclusionInput")
    def vpc_lattice_exclusion_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcLatticeExclusionInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcPeeringExclusionInput")
    def vpc_peering_exclusion_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcPeeringExclusionInput"))

    @builtins.property
    @jsii.member(jsii_name="egressOnlyInternetGatewayExclusion")
    def egress_only_internet_gateway_exclusion(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "egressOnlyInternetGatewayExclusion"))

    @egress_only_internet_gateway_exclusion.setter
    def egress_only_internet_gateway_exclusion(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dad19da599c821c303c16dc4431a730d4edb4f4940a9bea659a4d8f712bc0e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "egressOnlyInternetGatewayExclusion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="elasticFileSystemExclusion")
    def elastic_file_system_exclusion(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "elasticFileSystemExclusion"))

    @elastic_file_system_exclusion.setter
    def elastic_file_system_exclusion(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19f76f9e8874ad2a109f0581bbf86ba09411ec33a5d10eccc4cb00a698b577ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticFileSystemExclusion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internetGatewayExclusion")
    def internet_gateway_exclusion(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "internetGatewayExclusion"))

    @internet_gateway_exclusion.setter
    def internet_gateway_exclusion(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21128e07f8633cfa03bbfcf0f6a0b4fe3ae06d62f56ccd1ed1a84c6484cc3ffe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internetGatewayExclusion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lambdaExclusion")
    def lambda_exclusion(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lambdaExclusion"))

    @lambda_exclusion.setter
    def lambda_exclusion(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b1c8e05c4bf254834b68836ef54c20da686d65f190e2d59fbc8c7e223c4387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaExclusion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b04820fbb19411cb7037e8eb63b48cf39f51c7c87216ca917eebcc1e94e4d61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="natGatewayExclusion")
    def nat_gateway_exclusion(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "natGatewayExclusion"))

    @nat_gateway_exclusion.setter
    def nat_gateway_exclusion(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42e27d4b2f08a9085e7588c3c68dbcf15d22383340bee0c7d7a15083f0ebb785)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "natGatewayExclusion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6843966dc0548f65f7a3798ef7f1ffd8a598721f1010eaa42c59be3fe8ca983)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da409e64088176d328e9b16c1656df909ab81bd79a7eb6c7c7e1c299589bff64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualPrivateGatewayExclusion")
    def virtual_private_gateway_exclusion(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualPrivateGatewayExclusion"))

    @virtual_private_gateway_exclusion.setter
    def virtual_private_gateway_exclusion(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__143c6b5ed997a3f8d71795c88e7dbeca74ba55ae783c71e3a4bd8643065d1580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualPrivateGatewayExclusion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e4dec4f7006992bb4ffbf66487a4b80b2076927a592c3b28bf48aa09655849b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcLatticeExclusion")
    def vpc_lattice_exclusion(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcLatticeExclusion"))

    @vpc_lattice_exclusion.setter
    def vpc_lattice_exclusion(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5813b4190f204579b655b7ccca9fb6ca853febaddfbf261b059f44fb18b0336)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcLatticeExclusion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcPeeringExclusion")
    def vpc_peering_exclusion(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcPeeringExclusion"))

    @vpc_peering_exclusion.setter
    def vpc_peering_exclusion(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68d3dde36b2bb6049ae7c9b7a2e267a028e5c8bd1d468bd4409b26f3fa6a2fc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcPeeringExclusion", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.vpcEncryptionControl.VpcEncryptionControlConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "mode": "mode",
        "vpc_id": "vpcId",
        "egress_only_internet_gateway_exclusion": "egressOnlyInternetGatewayExclusion",
        "elastic_file_system_exclusion": "elasticFileSystemExclusion",
        "internet_gateway_exclusion": "internetGatewayExclusion",
        "lambda_exclusion": "lambdaExclusion",
        "nat_gateway_exclusion": "natGatewayExclusion",
        "region": "region",
        "tags": "tags",
        "timeouts": "timeouts",
        "virtual_private_gateway_exclusion": "virtualPrivateGatewayExclusion",
        "vpc_lattice_exclusion": "vpcLatticeExclusion",
        "vpc_peering_exclusion": "vpcPeeringExclusion",
    },
)
class VpcEncryptionControlConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        mode: builtins.str,
        vpc_id: builtins.str,
        egress_only_internet_gateway_exclusion: typing.Optional[builtins.str] = None,
        elastic_file_system_exclusion: typing.Optional[builtins.str] = None,
        internet_gateway_exclusion: typing.Optional[builtins.str] = None,
        lambda_exclusion: typing.Optional[builtins.str] = None,
        nat_gateway_exclusion: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["VpcEncryptionControlTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_private_gateway_exclusion: typing.Optional[builtins.str] = None,
        vpc_lattice_exclusion: typing.Optional[builtins.str] = None,
        vpc_peering_exclusion: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#mode VpcEncryptionControl#mode}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#vpc_id VpcEncryptionControl#vpc_id}.
        :param egress_only_internet_gateway_exclusion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#egress_only_internet_gateway_exclusion VpcEncryptionControl#egress_only_internet_gateway_exclusion}.
        :param elastic_file_system_exclusion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#elastic_file_system_exclusion VpcEncryptionControl#elastic_file_system_exclusion}.
        :param internet_gateway_exclusion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#internet_gateway_exclusion VpcEncryptionControl#internet_gateway_exclusion}.
        :param lambda_exclusion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#lambda_exclusion VpcEncryptionControl#lambda_exclusion}.
        :param nat_gateway_exclusion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#nat_gateway_exclusion VpcEncryptionControl#nat_gateway_exclusion}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#region VpcEncryptionControl#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#tags VpcEncryptionControl#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#timeouts VpcEncryptionControl#timeouts}
        :param virtual_private_gateway_exclusion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#virtual_private_gateway_exclusion VpcEncryptionControl#virtual_private_gateway_exclusion}.
        :param vpc_lattice_exclusion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#vpc_lattice_exclusion VpcEncryptionControl#vpc_lattice_exclusion}.
        :param vpc_peering_exclusion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#vpc_peering_exclusion VpcEncryptionControl#vpc_peering_exclusion}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = VpcEncryptionControlTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a23c2cd749b828c118a018c802533cc85a23b2c8e21ccbcd1fdb892d8beff51)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument egress_only_internet_gateway_exclusion", value=egress_only_internet_gateway_exclusion, expected_type=type_hints["egress_only_internet_gateway_exclusion"])
            check_type(argname="argument elastic_file_system_exclusion", value=elastic_file_system_exclusion, expected_type=type_hints["elastic_file_system_exclusion"])
            check_type(argname="argument internet_gateway_exclusion", value=internet_gateway_exclusion, expected_type=type_hints["internet_gateway_exclusion"])
            check_type(argname="argument lambda_exclusion", value=lambda_exclusion, expected_type=type_hints["lambda_exclusion"])
            check_type(argname="argument nat_gateway_exclusion", value=nat_gateway_exclusion, expected_type=type_hints["nat_gateway_exclusion"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument virtual_private_gateway_exclusion", value=virtual_private_gateway_exclusion, expected_type=type_hints["virtual_private_gateway_exclusion"])
            check_type(argname="argument vpc_lattice_exclusion", value=vpc_lattice_exclusion, expected_type=type_hints["vpc_lattice_exclusion"])
            check_type(argname="argument vpc_peering_exclusion", value=vpc_peering_exclusion, expected_type=type_hints["vpc_peering_exclusion"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
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
        if egress_only_internet_gateway_exclusion is not None:
            self._values["egress_only_internet_gateway_exclusion"] = egress_only_internet_gateway_exclusion
        if elastic_file_system_exclusion is not None:
            self._values["elastic_file_system_exclusion"] = elastic_file_system_exclusion
        if internet_gateway_exclusion is not None:
            self._values["internet_gateway_exclusion"] = internet_gateway_exclusion
        if lambda_exclusion is not None:
            self._values["lambda_exclusion"] = lambda_exclusion
        if nat_gateway_exclusion is not None:
            self._values["nat_gateway_exclusion"] = nat_gateway_exclusion
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if virtual_private_gateway_exclusion is not None:
            self._values["virtual_private_gateway_exclusion"] = virtual_private_gateway_exclusion
        if vpc_lattice_exclusion is not None:
            self._values["vpc_lattice_exclusion"] = vpc_lattice_exclusion
        if vpc_peering_exclusion is not None:
            self._values["vpc_peering_exclusion"] = vpc_peering_exclusion

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
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#mode VpcEncryptionControl#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#vpc_id VpcEncryptionControl#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def egress_only_internet_gateway_exclusion(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#egress_only_internet_gateway_exclusion VpcEncryptionControl#egress_only_internet_gateway_exclusion}.'''
        result = self._values.get("egress_only_internet_gateway_exclusion")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elastic_file_system_exclusion(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#elastic_file_system_exclusion VpcEncryptionControl#elastic_file_system_exclusion}.'''
        result = self._values.get("elastic_file_system_exclusion")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def internet_gateway_exclusion(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#internet_gateway_exclusion VpcEncryptionControl#internet_gateway_exclusion}.'''
        result = self._values.get("internet_gateway_exclusion")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lambda_exclusion(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#lambda_exclusion VpcEncryptionControl#lambda_exclusion}.'''
        result = self._values.get("lambda_exclusion")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nat_gateway_exclusion(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#nat_gateway_exclusion VpcEncryptionControl#nat_gateway_exclusion}.'''
        result = self._values.get("nat_gateway_exclusion")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#region VpcEncryptionControl#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#tags VpcEncryptionControl#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VpcEncryptionControlTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#timeouts VpcEncryptionControl#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VpcEncryptionControlTimeouts"], result)

    @builtins.property
    def virtual_private_gateway_exclusion(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#virtual_private_gateway_exclusion VpcEncryptionControl#virtual_private_gateway_exclusion}.'''
        result = self._values.get("virtual_private_gateway_exclusion")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_lattice_exclusion(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#vpc_lattice_exclusion VpcEncryptionControl#vpc_lattice_exclusion}.'''
        result = self._values.get("vpc_lattice_exclusion")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_peering_exclusion(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#vpc_peering_exclusion VpcEncryptionControl#vpc_peering_exclusion}.'''
        result = self._values.get("vpc_peering_exclusion")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcEncryptionControlConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.vpcEncryptionControl.VpcEncryptionControlResourceExclusions",
    jsii_struct_bases=[],
    name_mapping={},
)
class VpcEncryptionControlResourceExclusions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcEncryptionControlResourceExclusions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.vpcEncryptionControl.VpcEncryptionControlResourceExclusionsEgressOnlyInternetGateway",
    jsii_struct_bases=[],
    name_mapping={},
)
class VpcEncryptionControlResourceExclusionsEgressOnlyInternetGateway:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcEncryptionControlResourceExclusionsEgressOnlyInternetGateway(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpcEncryptionControlResourceExclusionsEgressOnlyInternetGatewayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.vpcEncryptionControl.VpcEncryptionControlResourceExclusionsEgressOnlyInternetGatewayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49a8783f9cac1777ef83854f48a05f706321a4ba9dc702fb441b2a28ed739dcb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateMessage")
    def state_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VpcEncryptionControlResourceExclusionsEgressOnlyInternetGateway]:
        return typing.cast(typing.Optional[VpcEncryptionControlResourceExclusionsEgressOnlyInternetGateway], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VpcEncryptionControlResourceExclusionsEgressOnlyInternetGateway],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51dc4efd8d36ac04a24032aa5df30c64cddd8e93a2f5b6d8c2beba2a389df7e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.vpcEncryptionControl.VpcEncryptionControlResourceExclusionsElasticFileSystem",
    jsii_struct_bases=[],
    name_mapping={},
)
class VpcEncryptionControlResourceExclusionsElasticFileSystem:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcEncryptionControlResourceExclusionsElasticFileSystem(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpcEncryptionControlResourceExclusionsElasticFileSystemOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.vpcEncryptionControl.VpcEncryptionControlResourceExclusionsElasticFileSystemOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdfc2c7dce967b061c0db867fb5d9ead1bea3ae39f7a22199df55d6560c46642)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateMessage")
    def state_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VpcEncryptionControlResourceExclusionsElasticFileSystem]:
        return typing.cast(typing.Optional[VpcEncryptionControlResourceExclusionsElasticFileSystem], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VpcEncryptionControlResourceExclusionsElasticFileSystem],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2cf665890a9fbbb06e62d2a94e08a1cae3daed8427e3e234032564ea6501349)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.vpcEncryptionControl.VpcEncryptionControlResourceExclusionsInternetGateway",
    jsii_struct_bases=[],
    name_mapping={},
)
class VpcEncryptionControlResourceExclusionsInternetGateway:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcEncryptionControlResourceExclusionsInternetGateway(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpcEncryptionControlResourceExclusionsInternetGatewayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.vpcEncryptionControl.VpcEncryptionControlResourceExclusionsInternetGatewayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8840a3cc5edbb9b2a214a82d91c3cddc7d6fec9db2ab953e70a447565fab6c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateMessage")
    def state_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VpcEncryptionControlResourceExclusionsInternetGateway]:
        return typing.cast(typing.Optional[VpcEncryptionControlResourceExclusionsInternetGateway], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VpcEncryptionControlResourceExclusionsInternetGateway],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8527cf49c9f2d9edac41a1acea2871372a0e85508cafb68d271caadae296069)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.vpcEncryptionControl.VpcEncryptionControlResourceExclusionsLambda",
    jsii_struct_bases=[],
    name_mapping={},
)
class VpcEncryptionControlResourceExclusionsLambda:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcEncryptionControlResourceExclusionsLambda(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpcEncryptionControlResourceExclusionsLambdaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.vpcEncryptionControl.VpcEncryptionControlResourceExclusionsLambdaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__acdb832537ada1b317f91f07714ded6b92df3e9522a77b6d8b6d31dbe1c20861)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateMessage")
    def state_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VpcEncryptionControlResourceExclusionsLambda]:
        return typing.cast(typing.Optional[VpcEncryptionControlResourceExclusionsLambda], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VpcEncryptionControlResourceExclusionsLambda],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c223584d046718ef86354dcb9ce589065985ef0ada3b33fe1e52a6599d74ffb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.vpcEncryptionControl.VpcEncryptionControlResourceExclusionsNatGateway",
    jsii_struct_bases=[],
    name_mapping={},
)
class VpcEncryptionControlResourceExclusionsNatGateway:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcEncryptionControlResourceExclusionsNatGateway(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpcEncryptionControlResourceExclusionsNatGatewayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.vpcEncryptionControl.VpcEncryptionControlResourceExclusionsNatGatewayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0496a4c143b0d92d4c34485ed69cf59deb93b0727dec8171a8e7ce4b5834979f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateMessage")
    def state_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VpcEncryptionControlResourceExclusionsNatGateway]:
        return typing.cast(typing.Optional[VpcEncryptionControlResourceExclusionsNatGateway], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VpcEncryptionControlResourceExclusionsNatGateway],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f62c8c7cf1c14e046a7155166e4b83af3a88608567d770a9d374ea42c46ba6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VpcEncryptionControlResourceExclusionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.vpcEncryptionControl.VpcEncryptionControlResourceExclusionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79f452a8e372943898ebfc8aa60c51a19ed29db0f509c6731c7f31c8a645e49e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="egressOnlyInternetGateway")
    def egress_only_internet_gateway(
        self,
    ) -> VpcEncryptionControlResourceExclusionsEgressOnlyInternetGatewayOutputReference:
        return typing.cast(VpcEncryptionControlResourceExclusionsEgressOnlyInternetGatewayOutputReference, jsii.get(self, "egressOnlyInternetGateway"))

    @builtins.property
    @jsii.member(jsii_name="elasticFileSystem")
    def elastic_file_system(
        self,
    ) -> VpcEncryptionControlResourceExclusionsElasticFileSystemOutputReference:
        return typing.cast(VpcEncryptionControlResourceExclusionsElasticFileSystemOutputReference, jsii.get(self, "elasticFileSystem"))

    @builtins.property
    @jsii.member(jsii_name="internetGateway")
    def internet_gateway(
        self,
    ) -> VpcEncryptionControlResourceExclusionsInternetGatewayOutputReference:
        return typing.cast(VpcEncryptionControlResourceExclusionsInternetGatewayOutputReference, jsii.get(self, "internetGateway"))

    @builtins.property
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> VpcEncryptionControlResourceExclusionsLambdaOutputReference:
        return typing.cast(VpcEncryptionControlResourceExclusionsLambdaOutputReference, jsii.get(self, "lambda"))

    @builtins.property
    @jsii.member(jsii_name="natGateway")
    def nat_gateway(
        self,
    ) -> VpcEncryptionControlResourceExclusionsNatGatewayOutputReference:
        return typing.cast(VpcEncryptionControlResourceExclusionsNatGatewayOutputReference, jsii.get(self, "natGateway"))

    @builtins.property
    @jsii.member(jsii_name="virtualPrivateGateway")
    def virtual_private_gateway(
        self,
    ) -> "VpcEncryptionControlResourceExclusionsVirtualPrivateGatewayOutputReference":
        return typing.cast("VpcEncryptionControlResourceExclusionsVirtualPrivateGatewayOutputReference", jsii.get(self, "virtualPrivateGateway"))

    @builtins.property
    @jsii.member(jsii_name="vpcLattice")
    def vpc_lattice(
        self,
    ) -> "VpcEncryptionControlResourceExclusionsVpcLatticeOutputReference":
        return typing.cast("VpcEncryptionControlResourceExclusionsVpcLatticeOutputReference", jsii.get(self, "vpcLattice"))

    @builtins.property
    @jsii.member(jsii_name="vpcPeering")
    def vpc_peering(
        self,
    ) -> "VpcEncryptionControlResourceExclusionsVpcPeeringOutputReference":
        return typing.cast("VpcEncryptionControlResourceExclusionsVpcPeeringOutputReference", jsii.get(self, "vpcPeering"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VpcEncryptionControlResourceExclusions]:
        return typing.cast(typing.Optional[VpcEncryptionControlResourceExclusions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VpcEncryptionControlResourceExclusions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40e26782c0bda78bcb715512afa893203b2938afc7702b7c3860459ad82e29c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.vpcEncryptionControl.VpcEncryptionControlResourceExclusionsVirtualPrivateGateway",
    jsii_struct_bases=[],
    name_mapping={},
)
class VpcEncryptionControlResourceExclusionsVirtualPrivateGateway:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcEncryptionControlResourceExclusionsVirtualPrivateGateway(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpcEncryptionControlResourceExclusionsVirtualPrivateGatewayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.vpcEncryptionControl.VpcEncryptionControlResourceExclusionsVirtualPrivateGatewayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d12cfa0e190b34ab5e0d524c794ddfea2112cf38522c8756d3aa143a98e7878)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateMessage")
    def state_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VpcEncryptionControlResourceExclusionsVirtualPrivateGateway]:
        return typing.cast(typing.Optional[VpcEncryptionControlResourceExclusionsVirtualPrivateGateway], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VpcEncryptionControlResourceExclusionsVirtualPrivateGateway],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe6dc6826176b0487a86463b234f856cb213c52b599ef865f5039c4525500680)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.vpcEncryptionControl.VpcEncryptionControlResourceExclusionsVpcLattice",
    jsii_struct_bases=[],
    name_mapping={},
)
class VpcEncryptionControlResourceExclusionsVpcLattice:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcEncryptionControlResourceExclusionsVpcLattice(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpcEncryptionControlResourceExclusionsVpcLatticeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.vpcEncryptionControl.VpcEncryptionControlResourceExclusionsVpcLatticeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20f550bdea92ed30f159d94649ec220ac6e4175c638b82ab76856931bd417e11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateMessage")
    def state_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VpcEncryptionControlResourceExclusionsVpcLattice]:
        return typing.cast(typing.Optional[VpcEncryptionControlResourceExclusionsVpcLattice], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VpcEncryptionControlResourceExclusionsVpcLattice],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__714556400ca5661219000e49793b59c87da26100ec2d58e87375ec44f117e77b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.vpcEncryptionControl.VpcEncryptionControlResourceExclusionsVpcPeering",
    jsii_struct_bases=[],
    name_mapping={},
)
class VpcEncryptionControlResourceExclusionsVpcPeering:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcEncryptionControlResourceExclusionsVpcPeering(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpcEncryptionControlResourceExclusionsVpcPeeringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.vpcEncryptionControl.VpcEncryptionControlResourceExclusionsVpcPeeringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90312fd8c4c7ce2a220a6b0393cceaaa7c3896e4544521818d94f81dab0fd7b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateMessage")
    def state_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VpcEncryptionControlResourceExclusionsVpcPeering]:
        return typing.cast(typing.Optional[VpcEncryptionControlResourceExclusionsVpcPeering], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VpcEncryptionControlResourceExclusionsVpcPeering],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ab02311c2a9d9a124755943f2862262c15cc9df3dba1f57c739452db672d229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.vpcEncryptionControl.VpcEncryptionControlTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class VpcEncryptionControlTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#create VpcEncryptionControl#create}
        :param delete: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#delete VpcEncryptionControl#delete}
        :param update: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#update VpcEncryptionControl#update}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ffccfff1b230ed30ccd3786d9c54478dccfbb2c630f91f932618b3728e878d)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#create VpcEncryptionControl#create}
        '''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#delete VpcEncryptionControl#delete}
        '''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc_encryption_control#update VpcEncryptionControl#update}
        '''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcEncryptionControlTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpcEncryptionControlTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.vpcEncryptionControl.VpcEncryptionControlTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c57ef343bf63fc6509ec2eb07d347de599e2980c80fc9c848c741186b1efc3c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b2a18cc540a6b9751f073b4320de819a552729cfca220d0329174fe6f93449c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e85c752cee8aa9e77545a8b954b99933dfdcd87a4917dc6e62b218b01c07031d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__763037221e2a9ba94a908a486c52252b870da18664ad465ea8595dbb88257393)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpcEncryptionControlTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpcEncryptionControlTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpcEncryptionControlTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d3b6d5e8e34acb67f7dfdc354cc594a2f6346a65cfe0be4e0add4d4370d6c41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VpcEncryptionControl",
    "VpcEncryptionControlConfig",
    "VpcEncryptionControlResourceExclusions",
    "VpcEncryptionControlResourceExclusionsEgressOnlyInternetGateway",
    "VpcEncryptionControlResourceExclusionsEgressOnlyInternetGatewayOutputReference",
    "VpcEncryptionControlResourceExclusionsElasticFileSystem",
    "VpcEncryptionControlResourceExclusionsElasticFileSystemOutputReference",
    "VpcEncryptionControlResourceExclusionsInternetGateway",
    "VpcEncryptionControlResourceExclusionsInternetGatewayOutputReference",
    "VpcEncryptionControlResourceExclusionsLambda",
    "VpcEncryptionControlResourceExclusionsLambdaOutputReference",
    "VpcEncryptionControlResourceExclusionsNatGateway",
    "VpcEncryptionControlResourceExclusionsNatGatewayOutputReference",
    "VpcEncryptionControlResourceExclusionsOutputReference",
    "VpcEncryptionControlResourceExclusionsVirtualPrivateGateway",
    "VpcEncryptionControlResourceExclusionsVirtualPrivateGatewayOutputReference",
    "VpcEncryptionControlResourceExclusionsVpcLattice",
    "VpcEncryptionControlResourceExclusionsVpcLatticeOutputReference",
    "VpcEncryptionControlResourceExclusionsVpcPeering",
    "VpcEncryptionControlResourceExclusionsVpcPeeringOutputReference",
    "VpcEncryptionControlTimeouts",
    "VpcEncryptionControlTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c0d6ad2075dc90cabcbd5510b23dd0af6a612d56656da89d0f533692c4a1e25c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    mode: builtins.str,
    vpc_id: builtins.str,
    egress_only_internet_gateway_exclusion: typing.Optional[builtins.str] = None,
    elastic_file_system_exclusion: typing.Optional[builtins.str] = None,
    internet_gateway_exclusion: typing.Optional[builtins.str] = None,
    lambda_exclusion: typing.Optional[builtins.str] = None,
    nat_gateway_exclusion: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[VpcEncryptionControlTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_private_gateway_exclusion: typing.Optional[builtins.str] = None,
    vpc_lattice_exclusion: typing.Optional[builtins.str] = None,
    vpc_peering_exclusion: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__ee22fefb929805d7acc076c944023363e664881ef596834383a32a803c6a00fc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dad19da599c821c303c16dc4431a730d4edb4f4940a9bea659a4d8f712bc0e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f76f9e8874ad2a109f0581bbf86ba09411ec33a5d10eccc4cb00a698b577ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21128e07f8633cfa03bbfcf0f6a0b4fe3ae06d62f56ccd1ed1a84c6484cc3ffe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b1c8e05c4bf254834b68836ef54c20da686d65f190e2d59fbc8c7e223c4387(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b04820fbb19411cb7037e8eb63b48cf39f51c7c87216ca917eebcc1e94e4d61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42e27d4b2f08a9085e7588c3c68dbcf15d22383340bee0c7d7a15083f0ebb785(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6843966dc0548f65f7a3798ef7f1ffd8a598721f1010eaa42c59be3fe8ca983(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da409e64088176d328e9b16c1656df909ab81bd79a7eb6c7c7e1c299589bff64(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__143c6b5ed997a3f8d71795c88e7dbeca74ba55ae783c71e3a4bd8643065d1580(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e4dec4f7006992bb4ffbf66487a4b80b2076927a592c3b28bf48aa09655849b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5813b4190f204579b655b7ccca9fb6ca853febaddfbf261b059f44fb18b0336(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68d3dde36b2bb6049ae7c9b7a2e267a028e5c8bd1d468bd4409b26f3fa6a2fc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a23c2cd749b828c118a018c802533cc85a23b2c8e21ccbcd1fdb892d8beff51(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mode: builtins.str,
    vpc_id: builtins.str,
    egress_only_internet_gateway_exclusion: typing.Optional[builtins.str] = None,
    elastic_file_system_exclusion: typing.Optional[builtins.str] = None,
    internet_gateway_exclusion: typing.Optional[builtins.str] = None,
    lambda_exclusion: typing.Optional[builtins.str] = None,
    nat_gateway_exclusion: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[VpcEncryptionControlTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_private_gateway_exclusion: typing.Optional[builtins.str] = None,
    vpc_lattice_exclusion: typing.Optional[builtins.str] = None,
    vpc_peering_exclusion: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49a8783f9cac1777ef83854f48a05f706321a4ba9dc702fb441b2a28ed739dcb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51dc4efd8d36ac04a24032aa5df30c64cddd8e93a2f5b6d8c2beba2a389df7e9(
    value: typing.Optional[VpcEncryptionControlResourceExclusionsEgressOnlyInternetGateway],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdfc2c7dce967b061c0db867fb5d9ead1bea3ae39f7a22199df55d6560c46642(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2cf665890a9fbbb06e62d2a94e08a1cae3daed8427e3e234032564ea6501349(
    value: typing.Optional[VpcEncryptionControlResourceExclusionsElasticFileSystem],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8840a3cc5edbb9b2a214a82d91c3cddc7d6fec9db2ab953e70a447565fab6c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8527cf49c9f2d9edac41a1acea2871372a0e85508cafb68d271caadae296069(
    value: typing.Optional[VpcEncryptionControlResourceExclusionsInternetGateway],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acdb832537ada1b317f91f07714ded6b92df3e9522a77b6d8b6d31dbe1c20861(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c223584d046718ef86354dcb9ce589065985ef0ada3b33fe1e52a6599d74ffb7(
    value: typing.Optional[VpcEncryptionControlResourceExclusionsLambda],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0496a4c143b0d92d4c34485ed69cf59deb93b0727dec8171a8e7ce4b5834979f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f62c8c7cf1c14e046a7155166e4b83af3a88608567d770a9d374ea42c46ba6f(
    value: typing.Optional[VpcEncryptionControlResourceExclusionsNatGateway],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f452a8e372943898ebfc8aa60c51a19ed29db0f509c6731c7f31c8a645e49e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e26782c0bda78bcb715512afa893203b2938afc7702b7c3860459ad82e29c7(
    value: typing.Optional[VpcEncryptionControlResourceExclusions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d12cfa0e190b34ab5e0d524c794ddfea2112cf38522c8756d3aa143a98e7878(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe6dc6826176b0487a86463b234f856cb213c52b599ef865f5039c4525500680(
    value: typing.Optional[VpcEncryptionControlResourceExclusionsVirtualPrivateGateway],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f550bdea92ed30f159d94649ec220ac6e4175c638b82ab76856931bd417e11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714556400ca5661219000e49793b59c87da26100ec2d58e87375ec44f117e77b(
    value: typing.Optional[VpcEncryptionControlResourceExclusionsVpcLattice],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90312fd8c4c7ce2a220a6b0393cceaaa7c3896e4544521818d94f81dab0fd7b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ab02311c2a9d9a124755943f2862262c15cc9df3dba1f57c739452db672d229(
    value: typing.Optional[VpcEncryptionControlResourceExclusionsVpcPeering],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ffccfff1b230ed30ccd3786d9c54478dccfbb2c630f91f932618b3728e878d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c57ef343bf63fc6509ec2eb07d347de599e2980c80fc9c848c741186b1efc3c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b2a18cc540a6b9751f073b4320de819a552729cfca220d0329174fe6f93449c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e85c752cee8aa9e77545a8b954b99933dfdcd87a4917dc6e62b218b01c07031d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__763037221e2a9ba94a908a486c52252b870da18664ad465ea8595dbb88257393(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d3b6d5e8e34acb67f7dfdc354cc594a2f6346a65cfe0be4e0add4d4370d6c41(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpcEncryptionControlTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
