r'''
# `google_network_connectivity_internal_range`

Refer to the Terraform Registry for docs: [`google_network_connectivity_internal_range`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range).
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


class NetworkConnectivityInternalRange(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivityInternalRange.NetworkConnectivityInternalRange",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range google_network_connectivity_internal_range}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        network: builtins.str,
        peering: builtins.str,
        usage: builtins.str,
        description: typing.Optional[builtins.str] = None,
        exclude_cidr_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        immutable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_cidr_range: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        migration: typing.Optional[typing.Union["NetworkConnectivityInternalRangeMigration", typing.Dict[builtins.str, typing.Any]]] = None,
        overlaps: typing.Optional[typing.Sequence[builtins.str]] = None,
        prefix_length: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        target_cidr_range: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["NetworkConnectivityInternalRangeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range google_network_connectivity_internal_range} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the policy based route. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#name NetworkConnectivityInternalRange#name}
        :param network: Fully-qualified URL of the network that this route applies to, for example: projects/my-project/global/networks/my-network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#network NetworkConnectivityInternalRange#network}
        :param peering: The type of peering set for this internal range. Possible values: ["FOR_SELF", "FOR_PEER", "NOT_SHARED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#peering NetworkConnectivityInternalRange#peering}
        :param usage: The type of usage set for this InternalRange. Possible values: ["FOR_VPC", "EXTERNAL_TO_VPC", "FOR_MIGRATION"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#usage NetworkConnectivityInternalRange#usage}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#description NetworkConnectivityInternalRange#description}
        :param exclude_cidr_ranges: Optional. List of IP CIDR ranges to be excluded. Resulting reserved Internal Range will not overlap with any CIDR blocks mentioned in this list. Only IPv4 CIDR ranges are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#exclude_cidr_ranges NetworkConnectivityInternalRange#exclude_cidr_ranges}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#id NetworkConnectivityInternalRange#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param immutable: Immutable ranges cannot have their fields modified, except for labels and description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#immutable NetworkConnectivityInternalRange#immutable}
        :param ip_cidr_range: The IP range that this internal range defines. NOTE: IPv6 ranges are limited to usage=EXTERNAL_TO_VPC and peering=FOR_SELF NOTE: For IPv6 Ranges this field is compulsory, i.e. the address range must be specified explicitly. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#ip_cidr_range NetworkConnectivityInternalRange#ip_cidr_range}
        :param labels: User-defined labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#labels NetworkConnectivityInternalRange#labels}
        :param migration: migration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#migration NetworkConnectivityInternalRange#migration}
        :param overlaps: Optional. Types of resources that are allowed to overlap with the current internal range. Possible values: ["OVERLAP_ROUTE_RANGE", "OVERLAP_EXISTING_SUBNET_RANGE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#overlaps NetworkConnectivityInternalRange#overlaps}
        :param prefix_length: An alternate to ipCidrRange. Can be set when trying to create a reservation that automatically finds a free range of the given size. If both ipCidrRange and prefixLength are set, there is an error if the range sizes do not match. Can also be used during updates to change the range size. NOTE: For IPv6 this field only works if ip_cidr_range is set as well, and both fields must match. In other words, with IPv6 this field only works as a redundant parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#prefix_length NetworkConnectivityInternalRange#prefix_length}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#project NetworkConnectivityInternalRange#project}.
        :param target_cidr_range: Optional. Can be set to narrow down or pick a different address space while searching for a free range. If not set, defaults to the "10.0.0.0/8" address space. This can be used to search in other rfc-1918 address spaces like "172.16.0.0/12" and "192.168.0.0/16" or non-rfc-1918 address spaces used in the VPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#target_cidr_range NetworkConnectivityInternalRange#target_cidr_range}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#timeouts NetworkConnectivityInternalRange#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be338ef48ae14708004513321571d56d581222d8269aba8a877809b7c6d0b9dd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkConnectivityInternalRangeConfig(
            name=name,
            network=network,
            peering=peering,
            usage=usage,
            description=description,
            exclude_cidr_ranges=exclude_cidr_ranges,
            id=id,
            immutable=immutable,
            ip_cidr_range=ip_cidr_range,
            labels=labels,
            migration=migration,
            overlaps=overlaps,
            prefix_length=prefix_length,
            project=project,
            target_cidr_range=target_cidr_range,
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
        '''Generates CDKTF code for importing a NetworkConnectivityInternalRange resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkConnectivityInternalRange to import.
        :param import_from_id: The id of the existing NetworkConnectivityInternalRange that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkConnectivityInternalRange to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec9f35ade3b4e9bb37402c7efc46a2d8a5136580bd27641458c417b05197cdf7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMigration")
    def put_migration(self, *, source: builtins.str, target: builtins.str) -> None:
        '''
        :param source: Resource path as an URI of the source resource, for example a subnet. The project for the source resource should match the project for the InternalRange. An example /projects/{project}/regions/{region}/subnetworks/{subnet} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#source NetworkConnectivityInternalRange#source}
        :param target: Resource path of the target resource. The target project can be different, as in the cases when migrating to peer networks. The resource may not exist yet. For example /projects/{project}/regions/{region}/subnetworks/{subnet} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#target NetworkConnectivityInternalRange#target}
        '''
        value = NetworkConnectivityInternalRangeMigration(source=source, target=target)

        return typing.cast(None, jsii.invoke(self, "putMigration", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#create NetworkConnectivityInternalRange#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#delete NetworkConnectivityInternalRange#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#update NetworkConnectivityInternalRange#update}.
        '''
        value = NetworkConnectivityInternalRangeTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExcludeCidrRanges")
    def reset_exclude_cidr_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeCidrRanges", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImmutable")
    def reset_immutable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImmutable", []))

    @jsii.member(jsii_name="resetIpCidrRange")
    def reset_ip_cidr_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpCidrRange", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMigration")
    def reset_migration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMigration", []))

    @jsii.member(jsii_name="resetOverlaps")
    def reset_overlaps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverlaps", []))

    @jsii.member(jsii_name="resetPrefixLength")
    def reset_prefix_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixLength", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTargetCidrRange")
    def reset_target_cidr_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetCidrRange", []))

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
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="migration")
    def migration(self) -> "NetworkConnectivityInternalRangeMigrationOutputReference":
        return typing.cast("NetworkConnectivityInternalRangeMigrationOutputReference", jsii.get(self, "migration"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetworkConnectivityInternalRangeTimeoutsOutputReference":
        return typing.cast("NetworkConnectivityInternalRangeTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "users"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeCidrRangesInput")
    def exclude_cidr_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludeCidrRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="immutableInput")
    def immutable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "immutableInput"))

    @builtins.property
    @jsii.member(jsii_name="ipCidrRangeInput")
    def ip_cidr_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipCidrRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="migrationInput")
    def migration_input(
        self,
    ) -> typing.Optional["NetworkConnectivityInternalRangeMigration"]:
        return typing.cast(typing.Optional["NetworkConnectivityInternalRangeMigration"], jsii.get(self, "migrationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="overlapsInput")
    def overlaps_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "overlapsInput"))

    @builtins.property
    @jsii.member(jsii_name="peeringInput")
    def peering_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peeringInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixLengthInput")
    def prefix_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "prefixLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="targetCidrRangeInput")
    def target_cidr_range_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "targetCidrRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkConnectivityInternalRangeTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkConnectivityInternalRangeTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="usageInput")
    def usage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usageInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e5520417627d7122b9f5dabab4a0ddaeb3952ca98970bd04d0d51ccd6922f50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeCidrRanges")
    def exclude_cidr_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludeCidrRanges"))

    @exclude_cidr_ranges.setter
    def exclude_cidr_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__584ff1ffd4ee1af0d21893489975100a89150112a2e5c9e16933677aaed6f8f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeCidrRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__439d7b17099dd2d3e485f8143d4a8f2789818a88b386691da8e0aa734b287a3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="immutable")
    def immutable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "immutable"))

    @immutable.setter
    def immutable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__048c6784c388202dadd18d88d6d26e7442beb2fe46e05a2dc5bebd924ea83d51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "immutable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipCidrRange")
    def ip_cidr_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipCidrRange"))

    @ip_cidr_range.setter
    def ip_cidr_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae4c6e3ddbd886f1a56220780c7b8a567d15897edde370c9858d865ba16bfc23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipCidrRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__454e5327b344049675a6d56dfad5157228d690e0a6ab8b38df6711282cd3b1f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bec23a38e952d9267ae8cd507caba8b262dc38a1f3be1f2984aee187a3f83af9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5fd59fb64873f036b8057bdb7dcb061c1ba066f38f6ad2cd2f4551387117859)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overlaps")
    def overlaps(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "overlaps"))

    @overlaps.setter
    def overlaps(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30f02b019e783bedcfdf2fbd9cf701a2183949a2763d78b31106e3f937d0a02e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overlaps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peering")
    def peering(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peering"))

    @peering.setter
    def peering(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33ef7b617cef9ca14dfa572290cc69fa66ddbd6f60a404da8ac9fa622d1438af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peering", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefixLength")
    def prefix_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "prefixLength"))

    @prefix_length.setter
    def prefix_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6866fa491dcdf9a7c08f4b3dcab0ff176a6b79b2491badd0060ed365c4eb240)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c2ce1f1546239852c5c83e6fade07bd8f7e9c7c34bfb55425db01258cf2220d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetCidrRange")
    def target_cidr_range(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetCidrRange"))

    @target_cidr_range.setter
    def target_cidr_range(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__808ebb102a2a3dd95d40d293010e6ed07db31bc933e0fc0bc05eda6347a71e4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetCidrRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="usage")
    def usage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usage"))

    @usage.setter
    def usage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c834ccebf74e29513bb43223680d069cd53364fd64cb723afe5787edc55a7f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usage", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivityInternalRange.NetworkConnectivityInternalRangeConfig",
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
        "network": "network",
        "peering": "peering",
        "usage": "usage",
        "description": "description",
        "exclude_cidr_ranges": "excludeCidrRanges",
        "id": "id",
        "immutable": "immutable",
        "ip_cidr_range": "ipCidrRange",
        "labels": "labels",
        "migration": "migration",
        "overlaps": "overlaps",
        "prefix_length": "prefixLength",
        "project": "project",
        "target_cidr_range": "targetCidrRange",
        "timeouts": "timeouts",
    },
)
class NetworkConnectivityInternalRangeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        network: builtins.str,
        peering: builtins.str,
        usage: builtins.str,
        description: typing.Optional[builtins.str] = None,
        exclude_cidr_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        immutable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_cidr_range: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        migration: typing.Optional[typing.Union["NetworkConnectivityInternalRangeMigration", typing.Dict[builtins.str, typing.Any]]] = None,
        overlaps: typing.Optional[typing.Sequence[builtins.str]] = None,
        prefix_length: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        target_cidr_range: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["NetworkConnectivityInternalRangeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the policy based route. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#name NetworkConnectivityInternalRange#name}
        :param network: Fully-qualified URL of the network that this route applies to, for example: projects/my-project/global/networks/my-network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#network NetworkConnectivityInternalRange#network}
        :param peering: The type of peering set for this internal range. Possible values: ["FOR_SELF", "FOR_PEER", "NOT_SHARED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#peering NetworkConnectivityInternalRange#peering}
        :param usage: The type of usage set for this InternalRange. Possible values: ["FOR_VPC", "EXTERNAL_TO_VPC", "FOR_MIGRATION"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#usage NetworkConnectivityInternalRange#usage}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#description NetworkConnectivityInternalRange#description}
        :param exclude_cidr_ranges: Optional. List of IP CIDR ranges to be excluded. Resulting reserved Internal Range will not overlap with any CIDR blocks mentioned in this list. Only IPv4 CIDR ranges are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#exclude_cidr_ranges NetworkConnectivityInternalRange#exclude_cidr_ranges}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#id NetworkConnectivityInternalRange#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param immutable: Immutable ranges cannot have their fields modified, except for labels and description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#immutable NetworkConnectivityInternalRange#immutable}
        :param ip_cidr_range: The IP range that this internal range defines. NOTE: IPv6 ranges are limited to usage=EXTERNAL_TO_VPC and peering=FOR_SELF NOTE: For IPv6 Ranges this field is compulsory, i.e. the address range must be specified explicitly. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#ip_cidr_range NetworkConnectivityInternalRange#ip_cidr_range}
        :param labels: User-defined labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#labels NetworkConnectivityInternalRange#labels}
        :param migration: migration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#migration NetworkConnectivityInternalRange#migration}
        :param overlaps: Optional. Types of resources that are allowed to overlap with the current internal range. Possible values: ["OVERLAP_ROUTE_RANGE", "OVERLAP_EXISTING_SUBNET_RANGE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#overlaps NetworkConnectivityInternalRange#overlaps}
        :param prefix_length: An alternate to ipCidrRange. Can be set when trying to create a reservation that automatically finds a free range of the given size. If both ipCidrRange and prefixLength are set, there is an error if the range sizes do not match. Can also be used during updates to change the range size. NOTE: For IPv6 this field only works if ip_cidr_range is set as well, and both fields must match. In other words, with IPv6 this field only works as a redundant parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#prefix_length NetworkConnectivityInternalRange#prefix_length}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#project NetworkConnectivityInternalRange#project}.
        :param target_cidr_range: Optional. Can be set to narrow down or pick a different address space while searching for a free range. If not set, defaults to the "10.0.0.0/8" address space. This can be used to search in other rfc-1918 address spaces like "172.16.0.0/12" and "192.168.0.0/16" or non-rfc-1918 address spaces used in the VPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#target_cidr_range NetworkConnectivityInternalRange#target_cidr_range}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#timeouts NetworkConnectivityInternalRange#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(migration, dict):
            migration = NetworkConnectivityInternalRangeMigration(**migration)
        if isinstance(timeouts, dict):
            timeouts = NetworkConnectivityInternalRangeTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6005f86fe91fbe9da477837a36de5985ecd48eef41a7d8d146be1588d06d146d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument peering", value=peering, expected_type=type_hints["peering"])
            check_type(argname="argument usage", value=usage, expected_type=type_hints["usage"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument exclude_cidr_ranges", value=exclude_cidr_ranges, expected_type=type_hints["exclude_cidr_ranges"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument immutable", value=immutable, expected_type=type_hints["immutable"])
            check_type(argname="argument ip_cidr_range", value=ip_cidr_range, expected_type=type_hints["ip_cidr_range"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument migration", value=migration, expected_type=type_hints["migration"])
            check_type(argname="argument overlaps", value=overlaps, expected_type=type_hints["overlaps"])
            check_type(argname="argument prefix_length", value=prefix_length, expected_type=type_hints["prefix_length"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument target_cidr_range", value=target_cidr_range, expected_type=type_hints["target_cidr_range"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "network": network,
            "peering": peering,
            "usage": usage,
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
        if description is not None:
            self._values["description"] = description
        if exclude_cidr_ranges is not None:
            self._values["exclude_cidr_ranges"] = exclude_cidr_ranges
        if id is not None:
            self._values["id"] = id
        if immutable is not None:
            self._values["immutable"] = immutable
        if ip_cidr_range is not None:
            self._values["ip_cidr_range"] = ip_cidr_range
        if labels is not None:
            self._values["labels"] = labels
        if migration is not None:
            self._values["migration"] = migration
        if overlaps is not None:
            self._values["overlaps"] = overlaps
        if prefix_length is not None:
            self._values["prefix_length"] = prefix_length
        if project is not None:
            self._values["project"] = project
        if target_cidr_range is not None:
            self._values["target_cidr_range"] = target_cidr_range
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
    def name(self) -> builtins.str:
        '''The name of the policy based route.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#name NetworkConnectivityInternalRange#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network(self) -> builtins.str:
        '''Fully-qualified URL of the network that this route applies to, for example: projects/my-project/global/networks/my-network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#network NetworkConnectivityInternalRange#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peering(self) -> builtins.str:
        '''The type of peering set for this internal range. Possible values: ["FOR_SELF", "FOR_PEER", "NOT_SHARED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#peering NetworkConnectivityInternalRange#peering}
        '''
        result = self._values.get("peering")
        assert result is not None, "Required property 'peering' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def usage(self) -> builtins.str:
        '''The type of usage set for this InternalRange. Possible values: ["FOR_VPC", "EXTERNAL_TO_VPC", "FOR_MIGRATION"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#usage NetworkConnectivityInternalRange#usage}
        '''
        result = self._values.get("usage")
        assert result is not None, "Required property 'usage' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#description NetworkConnectivityInternalRange#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclude_cidr_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        List of IP CIDR ranges to be excluded. Resulting reserved Internal Range will not overlap with any CIDR blocks mentioned in this list.
        Only IPv4 CIDR ranges are supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#exclude_cidr_ranges NetworkConnectivityInternalRange#exclude_cidr_ranges}
        '''
        result = self._values.get("exclude_cidr_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#id NetworkConnectivityInternalRange#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def immutable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Immutable ranges cannot have their fields modified, except for labels and description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#immutable NetworkConnectivityInternalRange#immutable}
        '''
        result = self._values.get("immutable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ip_cidr_range(self) -> typing.Optional[builtins.str]:
        '''The IP range that this internal range defines.

        NOTE: IPv6 ranges are limited to usage=EXTERNAL_TO_VPC and peering=FOR_SELF
        NOTE: For IPv6 Ranges this field is compulsory, i.e. the address range must be specified explicitly.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#ip_cidr_range NetworkConnectivityInternalRange#ip_cidr_range}
        '''
        result = self._values.get("ip_cidr_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-defined labels.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#labels NetworkConnectivityInternalRange#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def migration(self) -> typing.Optional["NetworkConnectivityInternalRangeMigration"]:
        '''migration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#migration NetworkConnectivityInternalRange#migration}
        '''
        result = self._values.get("migration")
        return typing.cast(typing.Optional["NetworkConnectivityInternalRangeMigration"], result)

    @builtins.property
    def overlaps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. Types of resources that are allowed to overlap with the current internal range. Possible values: ["OVERLAP_ROUTE_RANGE", "OVERLAP_EXISTING_SUBNET_RANGE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#overlaps NetworkConnectivityInternalRange#overlaps}
        '''
        result = self._values.get("overlaps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def prefix_length(self) -> typing.Optional[jsii.Number]:
        '''An alternate to ipCidrRange.

        Can be set when trying to create a reservation that automatically finds a free range of the given size.
        If both ipCidrRange and prefixLength are set, there is an error if the range sizes do not match. Can also be used during updates to change the range size.
        NOTE: For IPv6 this field only works if ip_cidr_range is set as well, and both fields must match. In other words, with IPv6 this field only works as
        a redundant parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#prefix_length NetworkConnectivityInternalRange#prefix_length}
        '''
        result = self._values.get("prefix_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#project NetworkConnectivityInternalRange#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_cidr_range(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        Can be set to narrow down or pick a different address space while searching for a free range.
        If not set, defaults to the "10.0.0.0/8" address space. This can be used to search in other rfc-1918 address spaces like "172.16.0.0/12" and "192.168.0.0/16" or non-rfc-1918 address spaces used in the VPC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#target_cidr_range NetworkConnectivityInternalRange#target_cidr_range}
        '''
        result = self._values.get("target_cidr_range")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetworkConnectivityInternalRangeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#timeouts NetworkConnectivityInternalRange#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetworkConnectivityInternalRangeTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivityInternalRangeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivityInternalRange.NetworkConnectivityInternalRangeMigration",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "target": "target"},
)
class NetworkConnectivityInternalRangeMigration:
    def __init__(self, *, source: builtins.str, target: builtins.str) -> None:
        '''
        :param source: Resource path as an URI of the source resource, for example a subnet. The project for the source resource should match the project for the InternalRange. An example /projects/{project}/regions/{region}/subnetworks/{subnet} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#source NetworkConnectivityInternalRange#source}
        :param target: Resource path of the target resource. The target project can be different, as in the cases when migrating to peer networks. The resource may not exist yet. For example /projects/{project}/regions/{region}/subnetworks/{subnet} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#target NetworkConnectivityInternalRange#target}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f68257f94f5c2f108ca81a550889a9b3e076abea44dfbde2be7aed222afe885)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
            "target": target,
        }

    @builtins.property
    def source(self) -> builtins.str:
        '''Resource path as an URI of the source resource, for example a subnet.

        The project for the source resource should match the project for the
        InternalRange.
        An example /projects/{project}/regions/{region}/subnetworks/{subnet}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#source NetworkConnectivityInternalRange#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Resource path of the target resource.

        The target project can be
        different, as in the cases when migrating to peer networks. The resource
        may not exist yet.
        For example /projects/{project}/regions/{region}/subnetworks/{subnet}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#target NetworkConnectivityInternalRange#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivityInternalRangeMigration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectivityInternalRangeMigrationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivityInternalRange.NetworkConnectivityInternalRangeMigrationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d3fb24d081cf6ff121c67504f9c8fab352a4ce9d3d4ef15572e256753eb0e3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a83b1b62dfb0e53d2f06938825d49f6751915eff0fa2f1904bbb80bac0e4dc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c9b1e104b2db7f8338b926700552ddc8a3c7268c5cde54921c7da44551d1ccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkConnectivityInternalRangeMigration]:
        return typing.cast(typing.Optional[NetworkConnectivityInternalRangeMigration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkConnectivityInternalRangeMigration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__295bee4e9658e80bd2938bd970f066f661f017b573186c2e11c4576311bbfcf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivityInternalRange.NetworkConnectivityInternalRangeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class NetworkConnectivityInternalRangeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#create NetworkConnectivityInternalRange#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#delete NetworkConnectivityInternalRange#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#update NetworkConnectivityInternalRange#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98a596a05ba25bb034c3d3b4cf3ec04061f647fc119fd31d2e5faf9cbbfa8a1b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#create NetworkConnectivityInternalRange#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#delete NetworkConnectivityInternalRange#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_internal_range#update NetworkConnectivityInternalRange#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivityInternalRangeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectivityInternalRangeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivityInternalRange.NetworkConnectivityInternalRangeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e80b1c0340b22bdd5b2cedcc081b23428216a4cca0b89191b1fbaa6e1674fa15)
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
            type_hints = typing.get_type_hints(_typecheckingstub__655945f65662c0621bb58b26b5604509968d452ad63f01d55c03a0af02b5c62a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e71d909d89b8d443f5fd4d70c0187009fe82a123a639b2c436f2b1563517f079)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92f50e1195937964739d26bc3c945435a4a94482721448596d3d5063fd136455)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectivityInternalRangeTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectivityInternalRangeTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectivityInternalRangeTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd767bdb478f46500013995beb483619338f0acf393f19f0668a769373a23c98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetworkConnectivityInternalRange",
    "NetworkConnectivityInternalRangeConfig",
    "NetworkConnectivityInternalRangeMigration",
    "NetworkConnectivityInternalRangeMigrationOutputReference",
    "NetworkConnectivityInternalRangeTimeouts",
    "NetworkConnectivityInternalRangeTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__be338ef48ae14708004513321571d56d581222d8269aba8a877809b7c6d0b9dd(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    network: builtins.str,
    peering: builtins.str,
    usage: builtins.str,
    description: typing.Optional[builtins.str] = None,
    exclude_cidr_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    immutable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ip_cidr_range: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    migration: typing.Optional[typing.Union[NetworkConnectivityInternalRangeMigration, typing.Dict[builtins.str, typing.Any]]] = None,
    overlaps: typing.Optional[typing.Sequence[builtins.str]] = None,
    prefix_length: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    target_cidr_range: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[NetworkConnectivityInternalRangeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ec9f35ade3b4e9bb37402c7efc46a2d8a5136580bd27641458c417b05197cdf7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e5520417627d7122b9f5dabab4a0ddaeb3952ca98970bd04d0d51ccd6922f50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__584ff1ffd4ee1af0d21893489975100a89150112a2e5c9e16933677aaed6f8f4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__439d7b17099dd2d3e485f8143d4a8f2789818a88b386691da8e0aa734b287a3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__048c6784c388202dadd18d88d6d26e7442beb2fe46e05a2dc5bebd924ea83d51(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae4c6e3ddbd886f1a56220780c7b8a567d15897edde370c9858d865ba16bfc23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__454e5327b344049675a6d56dfad5157228d690e0a6ab8b38df6711282cd3b1f0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec23a38e952d9267ae8cd507caba8b262dc38a1f3be1f2984aee187a3f83af9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5fd59fb64873f036b8057bdb7dcb061c1ba066f38f6ad2cd2f4551387117859(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f02b019e783bedcfdf2fbd9cf701a2183949a2763d78b31106e3f937d0a02e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ef7b617cef9ca14dfa572290cc69fa66ddbd6f60a404da8ac9fa622d1438af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6866fa491dcdf9a7c08f4b3dcab0ff176a6b79b2491badd0060ed365c4eb240(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c2ce1f1546239852c5c83e6fade07bd8f7e9c7c34bfb55425db01258cf2220d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__808ebb102a2a3dd95d40d293010e6ed07db31bc933e0fc0bc05eda6347a71e4b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c834ccebf74e29513bb43223680d069cd53364fd64cb723afe5787edc55a7f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6005f86fe91fbe9da477837a36de5985ecd48eef41a7d8d146be1588d06d146d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    network: builtins.str,
    peering: builtins.str,
    usage: builtins.str,
    description: typing.Optional[builtins.str] = None,
    exclude_cidr_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    immutable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ip_cidr_range: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    migration: typing.Optional[typing.Union[NetworkConnectivityInternalRangeMigration, typing.Dict[builtins.str, typing.Any]]] = None,
    overlaps: typing.Optional[typing.Sequence[builtins.str]] = None,
    prefix_length: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    target_cidr_range: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[NetworkConnectivityInternalRangeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f68257f94f5c2f108ca81a550889a9b3e076abea44dfbde2be7aed222afe885(
    *,
    source: builtins.str,
    target: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d3fb24d081cf6ff121c67504f9c8fab352a4ce9d3d4ef15572e256753eb0e3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a83b1b62dfb0e53d2f06938825d49f6751915eff0fa2f1904bbb80bac0e4dc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c9b1e104b2db7f8338b926700552ddc8a3c7268c5cde54921c7da44551d1ccf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__295bee4e9658e80bd2938bd970f066f661f017b573186c2e11c4576311bbfcf2(
    value: typing.Optional[NetworkConnectivityInternalRangeMigration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a596a05ba25bb034c3d3b4cf3ec04061f647fc119fd31d2e5faf9cbbfa8a1b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e80b1c0340b22bdd5b2cedcc081b23428216a4cca0b89191b1fbaa6e1674fa15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__655945f65662c0621bb58b26b5604509968d452ad63f01d55c03a0af02b5c62a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e71d909d89b8d443f5fd4d70c0187009fe82a123a639b2c436f2b1563517f079(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92f50e1195937964739d26bc3c945435a4a94482721448596d3d5063fd136455(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd767bdb478f46500013995beb483619338f0acf393f19f0668a769373a23c98(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectivityInternalRangeTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
