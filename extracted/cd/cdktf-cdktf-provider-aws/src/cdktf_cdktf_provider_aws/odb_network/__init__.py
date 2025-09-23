r'''
# `aws_odb_network`

Refer to the Terraform Registry for docs: [`aws_odb_network`](https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network).
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


class OdbNetwork(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbNetwork.OdbNetwork",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network aws_odb_network}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        availability_zone_id: builtins.str,
        backup_subnet_cidr: builtins.str,
        client_subnet_cidr: builtins.str,
        display_name: builtins.str,
        s3_access: builtins.str,
        zero_etl_access: builtins.str,
        availability_zone: typing.Optional[builtins.str] = None,
        custom_domain_name: typing.Optional[builtins.str] = None,
        default_dns_prefix: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        s3_policy_document: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["OdbNetworkTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network aws_odb_network} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param availability_zone_id: The AZ ID of the AZ where the ODB network is located. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#availability_zone_id OdbNetwork#availability_zone_id}
        :param backup_subnet_cidr: The CIDR range of the backup subnet for the ODB network. Changing this will force terraform to create new resource. Constraints: - Must not overlap with the CIDR range of the client subnet. - Must not overlap with the CIDR ranges of the VPCs that are connected to the ODB network. - Must not use the following CIDR ranges that are reserved by OCI: - 100.106.0.0/16 and 100.107.0.0/16 - 169.254.0.0/16 - 224.0.0.0 - 239.255.255.255 - 240.0.0.0 - 255.255.255.255 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#backup_subnet_cidr OdbNetwork#backup_subnet_cidr}
        :param client_subnet_cidr: The CIDR notation for the network resource. Changing this will force terraform to create new resource. Constraints: - Must not overlap with the CIDR range of the backup subnet. - Must not overlap with the CIDR ranges of the VPCs that are connected to the ODB network. - Must not use the following CIDR ranges that are reserved by OCI: - 100.106.0.0/16 and 100.107.0.0/16 - 169.254.0.0/16 - 224.0.0.0 - 239.255.255.255 - 240.0.0.0 - 255.255.255.255 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#client_subnet_cidr OdbNetwork#client_subnet_cidr}
        :param display_name: The user-friendly name for the odb network. Changing this will force terraform to create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#display_name OdbNetwork#display_name}
        :param s3_access: Specifies the configuration for Amazon S3 access from the ODB network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#s3_access OdbNetwork#s3_access}
        :param zero_etl_access: Specifies the configuration for Zero-ETL access from the ODB network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#zero_etl_access OdbNetwork#zero_etl_access}
        :param availability_zone: The name of the Availability Zone (AZ) where the odb network is located. Changing this will force terraform to create new resource Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#availability_zone OdbNetwork#availability_zone}
        :param custom_domain_name: The name of the custom domain that the network is located. custom_domain_name and default_dns_prefix both can't be given. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#custom_domain_name OdbNetwork#custom_domain_name}
        :param default_dns_prefix: The default DNS prefix for the network resource. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#default_dns_prefix OdbNetwork#default_dns_prefix}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#region OdbNetwork#region}
        :param s3_policy_document: Specifies the endpoint policy for Amazon S3 access from the ODB network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#s3_policy_document OdbNetwork#s3_policy_document}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#tags OdbNetwork#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#timeouts OdbNetwork#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5476bb961b9a8e4f0ad793fb790ae4ca0bea6b85b042645f9dc1b5df959bd8fa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = OdbNetworkConfig(
            availability_zone_id=availability_zone_id,
            backup_subnet_cidr=backup_subnet_cidr,
            client_subnet_cidr=client_subnet_cidr,
            display_name=display_name,
            s3_access=s3_access,
            zero_etl_access=zero_etl_access,
            availability_zone=availability_zone,
            custom_domain_name=custom_domain_name,
            default_dns_prefix=default_dns_prefix,
            region=region,
            s3_policy_document=s3_policy_document,
            tags=tags,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a OdbNetwork resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OdbNetwork to import.
        :param import_from_id: The id of the existing OdbNetwork that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OdbNetwork to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eefb4a817068b1a1a97f7713d5bb79df33af2f16567e336dec6dfd3e3d9bf06)
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
        :param create: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#create OdbNetwork#create}
        :param delete: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#delete OdbNetwork#delete}
        :param update: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#update OdbNetwork#update}
        '''
        value = OdbNetworkTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAvailabilityZone")
    def reset_availability_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityZone", []))

    @jsii.member(jsii_name="resetCustomDomainName")
    def reset_custom_domain_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomDomainName", []))

    @jsii.member(jsii_name="resetDefaultDnsPrefix")
    def reset_default_dns_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultDnsPrefix", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetS3PolicyDocument")
    def reset_s3_policy_document(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3PolicyDocument", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="managedServices")
    def managed_services(self) -> "OdbNetworkManagedServicesList":
        return typing.cast("OdbNetworkManagedServicesList", jsii.get(self, "managedServices"))

    @builtins.property
    @jsii.member(jsii_name="ociDnsForwardingConfigs")
    def oci_dns_forwarding_configs(self) -> "OdbNetworkOciDnsForwardingConfigsList":
        return typing.cast("OdbNetworkOciDnsForwardingConfigsList", jsii.get(self, "ociDnsForwardingConfigs"))

    @builtins.property
    @jsii.member(jsii_name="ociNetworkAnchorId")
    def oci_network_anchor_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ociNetworkAnchorId"))

    @builtins.property
    @jsii.member(jsii_name="ociNetworkAnchorUrl")
    def oci_network_anchor_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ociNetworkAnchorUrl"))

    @builtins.property
    @jsii.member(jsii_name="ociResourceAnchorName")
    def oci_resource_anchor_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ociResourceAnchorName"))

    @builtins.property
    @jsii.member(jsii_name="ociVcnId")
    def oci_vcn_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ociVcnId"))

    @builtins.property
    @jsii.member(jsii_name="ociVcnUrl")
    def oci_vcn_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ociVcnUrl"))

    @builtins.property
    @jsii.member(jsii_name="peeredCidrs")
    def peered_cidrs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "peeredCidrs"))

    @builtins.property
    @jsii.member(jsii_name="percentProgress")
    def percent_progress(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percentProgress"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="statusReason")
    def status_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statusReason"))

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tagsAll"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "OdbNetworkTimeoutsOutputReference":
        return typing.cast("OdbNetworkTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneIdInput")
    def availability_zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneInput")
    def availability_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="backupSubnetCidrInput")
    def backup_subnet_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupSubnetCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSubnetCidrInput")
    def client_subnet_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSubnetCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="customDomainNameInput")
    def custom_domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customDomainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultDnsPrefixInput")
    def default_dns_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultDnsPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="s3AccessInput")
    def s3_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3AccessInput"))

    @builtins.property
    @jsii.member(jsii_name="s3PolicyDocumentInput")
    def s3_policy_document_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3PolicyDocumentInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OdbNetworkTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OdbNetworkTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="zeroEtlAccessInput")
    def zero_etl_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zeroEtlAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__442ee7d1736b299f62823b3eb315db990f66e1c9b135f21e5bfbd3a265f4bc0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneId")
    def availability_zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZoneId"))

    @availability_zone_id.setter
    def availability_zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0916e8abbbdfe004b595f2bd81770d5d01f66be84ecc0c3a84da1d50ea6cd7d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZoneId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backupSubnetCidr")
    def backup_subnet_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupSubnetCidr"))

    @backup_subnet_cidr.setter
    def backup_subnet_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d2f0580b16d5202d407ce55964730ec9effe85eff4133998600298777996e19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupSubnetCidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSubnetCidr")
    def client_subnet_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSubnetCidr"))

    @client_subnet_cidr.setter
    def client_subnet_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ab33eb5987ab01f3fb70832d91ca20f34ac425bd47f3b02fb98ad261927bccd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSubnetCidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customDomainName")
    def custom_domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customDomainName"))

    @custom_domain_name.setter
    def custom_domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85b78bc42057f2b79d4913913d836532d5088146a08b6280c5bcce4475f97a62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customDomainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultDnsPrefix")
    def default_dns_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultDnsPrefix"))

    @default_dns_prefix.setter
    def default_dns_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc442a6da7d2020d4d5cc09a88fd172535741f90f65fd31e3d0c24f18a5f769a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultDnsPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c619f09762ccbbfd20032c2a264cb83724e33b456aba28dfca5df5080a27ff16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d21d01086a214898400d6cd149e97af257387700f7f79742fb52a6c95ab5355c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3Access")
    def s3_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Access"))

    @s3_access.setter
    def s3_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ceba1d981f44297e721dc2359f9b022c784e8b74db0abb263f78cd45e8014da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Access", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3PolicyDocument")
    def s3_policy_document(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3PolicyDocument"))

    @s3_policy_document.setter
    def s3_policy_document(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6284a2b10466a8e6c252c4eb8a863ed931afc50f47a66b70f28d7e7a314a8a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3PolicyDocument", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14e83b5543bb00806e79c46f1b58d66871f2547c88b2d87ddd3b4c4030bb4c56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zeroEtlAccess")
    def zero_etl_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zeroEtlAccess"))

    @zero_etl_access.setter
    def zero_etl_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__999ee20a1f228e9d5420c1937fac2f7a2997f3ff743c7e6877aebbd454d073ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zeroEtlAccess", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.odbNetwork.OdbNetworkConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "availability_zone_id": "availabilityZoneId",
        "backup_subnet_cidr": "backupSubnetCidr",
        "client_subnet_cidr": "clientSubnetCidr",
        "display_name": "displayName",
        "s3_access": "s3Access",
        "zero_etl_access": "zeroEtlAccess",
        "availability_zone": "availabilityZone",
        "custom_domain_name": "customDomainName",
        "default_dns_prefix": "defaultDnsPrefix",
        "region": "region",
        "s3_policy_document": "s3PolicyDocument",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class OdbNetworkConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        availability_zone_id: builtins.str,
        backup_subnet_cidr: builtins.str,
        client_subnet_cidr: builtins.str,
        display_name: builtins.str,
        s3_access: builtins.str,
        zero_etl_access: builtins.str,
        availability_zone: typing.Optional[builtins.str] = None,
        custom_domain_name: typing.Optional[builtins.str] = None,
        default_dns_prefix: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        s3_policy_document: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["OdbNetworkTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param availability_zone_id: The AZ ID of the AZ where the ODB network is located. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#availability_zone_id OdbNetwork#availability_zone_id}
        :param backup_subnet_cidr: The CIDR range of the backup subnet for the ODB network. Changing this will force terraform to create new resource. Constraints: - Must not overlap with the CIDR range of the client subnet. - Must not overlap with the CIDR ranges of the VPCs that are connected to the ODB network. - Must not use the following CIDR ranges that are reserved by OCI: - 100.106.0.0/16 and 100.107.0.0/16 - 169.254.0.0/16 - 224.0.0.0 - 239.255.255.255 - 240.0.0.0 - 255.255.255.255 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#backup_subnet_cidr OdbNetwork#backup_subnet_cidr}
        :param client_subnet_cidr: The CIDR notation for the network resource. Changing this will force terraform to create new resource. Constraints: - Must not overlap with the CIDR range of the backup subnet. - Must not overlap with the CIDR ranges of the VPCs that are connected to the ODB network. - Must not use the following CIDR ranges that are reserved by OCI: - 100.106.0.0/16 and 100.107.0.0/16 - 169.254.0.0/16 - 224.0.0.0 - 239.255.255.255 - 240.0.0.0 - 255.255.255.255 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#client_subnet_cidr OdbNetwork#client_subnet_cidr}
        :param display_name: The user-friendly name for the odb network. Changing this will force terraform to create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#display_name OdbNetwork#display_name}
        :param s3_access: Specifies the configuration for Amazon S3 access from the ODB network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#s3_access OdbNetwork#s3_access}
        :param zero_etl_access: Specifies the configuration for Zero-ETL access from the ODB network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#zero_etl_access OdbNetwork#zero_etl_access}
        :param availability_zone: The name of the Availability Zone (AZ) where the odb network is located. Changing this will force terraform to create new resource Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#availability_zone OdbNetwork#availability_zone}
        :param custom_domain_name: The name of the custom domain that the network is located. custom_domain_name and default_dns_prefix both can't be given. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#custom_domain_name OdbNetwork#custom_domain_name}
        :param default_dns_prefix: The default DNS prefix for the network resource. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#default_dns_prefix OdbNetwork#default_dns_prefix}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#region OdbNetwork#region}
        :param s3_policy_document: Specifies the endpoint policy for Amazon S3 access from the ODB network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#s3_policy_document OdbNetwork#s3_policy_document}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#tags OdbNetwork#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#timeouts OdbNetwork#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = OdbNetworkTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74c097d9f095f8babba4e664edd7bcb6191e66ee18060e52bcbaac20031df4cb)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument availability_zone_id", value=availability_zone_id, expected_type=type_hints["availability_zone_id"])
            check_type(argname="argument backup_subnet_cidr", value=backup_subnet_cidr, expected_type=type_hints["backup_subnet_cidr"])
            check_type(argname="argument client_subnet_cidr", value=client_subnet_cidr, expected_type=type_hints["client_subnet_cidr"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument s3_access", value=s3_access, expected_type=type_hints["s3_access"])
            check_type(argname="argument zero_etl_access", value=zero_etl_access, expected_type=type_hints["zero_etl_access"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument custom_domain_name", value=custom_domain_name, expected_type=type_hints["custom_domain_name"])
            check_type(argname="argument default_dns_prefix", value=default_dns_prefix, expected_type=type_hints["default_dns_prefix"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument s3_policy_document", value=s3_policy_document, expected_type=type_hints["s3_policy_document"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "availability_zone_id": availability_zone_id,
            "backup_subnet_cidr": backup_subnet_cidr,
            "client_subnet_cidr": client_subnet_cidr,
            "display_name": display_name,
            "s3_access": s3_access,
            "zero_etl_access": zero_etl_access,
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
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if custom_domain_name is not None:
            self._values["custom_domain_name"] = custom_domain_name
        if default_dns_prefix is not None:
            self._values["default_dns_prefix"] = default_dns_prefix
        if region is not None:
            self._values["region"] = region
        if s3_policy_document is not None:
            self._values["s3_policy_document"] = s3_policy_document
        if tags is not None:
            self._values["tags"] = tags
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
    def availability_zone_id(self) -> builtins.str:
        '''The AZ ID of the AZ where the ODB network is located.

        Changing this will force terraform to create new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#availability_zone_id OdbNetwork#availability_zone_id}
        '''
        result = self._values.get("availability_zone_id")
        assert result is not None, "Required property 'availability_zone_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_subnet_cidr(self) -> builtins.str:
        '''The CIDR range of the backup subnet for the ODB network.

        Changing this will force terraform to create new resource.
        Constraints:

        - Must not overlap with the CIDR range of the client subnet.
        - Must not overlap with the CIDR ranges of the VPCs that are connected to the
          ODB network.
        - Must not use the following CIDR ranges that are reserved by OCI:
        - 100.106.0.0/16 and 100.107.0.0/16
        - 169.254.0.0/16
        - 224.0.0.0 - 239.255.255.255
        - 240.0.0.0 - 255.255.255.255

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#backup_subnet_cidr OdbNetwork#backup_subnet_cidr}
        '''
        result = self._values.get("backup_subnet_cidr")
        assert result is not None, "Required property 'backup_subnet_cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_subnet_cidr(self) -> builtins.str:
        '''The CIDR notation for the network resource.

        Changing this will force terraform to create new resource.
        Constraints:

        - Must not overlap with the CIDR range of the backup subnet.
        - Must not overlap with the CIDR ranges of the VPCs that are connected to the
          ODB network.
        - Must not use the following CIDR ranges that are reserved by OCI:
        - 100.106.0.0/16 and 100.107.0.0/16
        - 169.254.0.0/16
        - 224.0.0.0 - 239.255.255.255
        - 240.0.0.0 - 255.255.255.255

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#client_subnet_cidr OdbNetwork#client_subnet_cidr}
        '''
        result = self._values.get("client_subnet_cidr")
        assert result is not None, "Required property 'client_subnet_cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The user-friendly name for the odb network. Changing this will force terraform to create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#display_name OdbNetwork#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_access(self) -> builtins.str:
        '''Specifies the configuration for Amazon S3 access from the ODB network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#s3_access OdbNetwork#s3_access}
        '''
        result = self._values.get("s3_access")
        assert result is not None, "Required property 's3_access' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def zero_etl_access(self) -> builtins.str:
        '''Specifies the configuration for Zero-ETL access from the ODB network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#zero_etl_access OdbNetwork#zero_etl_access}
        '''
        result = self._values.get("zero_etl_access")
        assert result is not None, "Required property 'zero_etl_access' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The name of the Availability Zone (AZ) where the odb network is located.

        Changing this will force terraform to create new resource

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#availability_zone OdbNetwork#availability_zone}
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_domain_name(self) -> typing.Optional[builtins.str]:
        '''The name of the custom domain that the network is located. custom_domain_name and default_dns_prefix both can't be given.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#custom_domain_name OdbNetwork#custom_domain_name}
        '''
        result = self._values.get("custom_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_dns_prefix(self) -> typing.Optional[builtins.str]:
        '''The default DNS prefix for the network resource. Changing this will force terraform to create new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#default_dns_prefix OdbNetwork#default_dns_prefix}
        '''
        result = self._values.get("default_dns_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#region OdbNetwork#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_policy_document(self) -> typing.Optional[builtins.str]:
        '''Specifies the endpoint policy for Amazon S3 access from the ODB network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#s3_policy_document OdbNetwork#s3_policy_document}
        '''
        result = self._values.get("s3_policy_document")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#tags OdbNetwork#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["OdbNetworkTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#timeouts OdbNetwork#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["OdbNetworkTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OdbNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.odbNetwork.OdbNetworkManagedServices",
    jsii_struct_bases=[],
    name_mapping={},
)
class OdbNetworkManagedServices:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OdbNetworkManagedServices(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OdbNetworkManagedServicesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbNetwork.OdbNetworkManagedServicesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce4235daf7357901033983dc7af080bd0e41f79499ed5421de9c57579f4a1655)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OdbNetworkManagedServicesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d374c41d659924594dc6c6da67ed77d51ebf29c1114e262be7c8e8b80ba1b9b2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OdbNetworkManagedServicesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bae0b9f1439945dfe469615563cabfa5d1988b8f86c0d8709e8a015eef1544b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a54e6fb42c38288e76cd9e43343f982c4a3bdfdaca76b8aae20751711e2badde)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5ef37eecc59254ba18c7fe0e9511b7d03ebf7382de07090c5ddf0e611799a51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.odbNetwork.OdbNetworkManagedServicesManagedS3BackupAccess",
    jsii_struct_bases=[],
    name_mapping={},
)
class OdbNetworkManagedServicesManagedS3BackupAccess:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OdbNetworkManagedServicesManagedS3BackupAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OdbNetworkManagedServicesManagedS3BackupAccessList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbNetwork.OdbNetworkManagedServicesManagedS3BackupAccessList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5248a3e4b46d27dcfd2dd3d9cc4287444f9e27713a221dee633e7b85c0df5ef7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OdbNetworkManagedServicesManagedS3BackupAccessOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca9733fbfd3256e81c4e1d047bd673403db0d614352ee40be01d91435034f078)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OdbNetworkManagedServicesManagedS3BackupAccessOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__290032007310a33e5ee1ac6a19b20490fb3f5fdc325cba529e53e7a2b24d1bb9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f16e5d342a742226c665ea6df0a688aff59a9b59e1e204adf9b7c006fdaa1f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40d48cb726b5d55fa672ccd642f719baa814e18727ae04578e992a76c3e5da17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OdbNetworkManagedServicesManagedS3BackupAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbNetwork.OdbNetworkManagedServicesManagedS3BackupAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df64bf6beb5083f37fb9d8eee3b0bc7d56df61daa098f1ca14597c04b4e906e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="ipv4Addresses")
    def ipv4_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipv4Addresses"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OdbNetworkManagedServicesManagedS3BackupAccess]:
        return typing.cast(typing.Optional[OdbNetworkManagedServicesManagedS3BackupAccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OdbNetworkManagedServicesManagedS3BackupAccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c482765e770c6db3e378beeeec84a14d2bcc6183f5428a812943b2ca4d21b7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OdbNetworkManagedServicesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbNetwork.OdbNetworkManagedServicesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30855eb8cb722bce111b0051d62b99405a4a48df7deff74dd0436607acd32bb9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="managedS3BackupAccess")
    def managed_s3_backup_access(
        self,
    ) -> OdbNetworkManagedServicesManagedS3BackupAccessList:
        return typing.cast(OdbNetworkManagedServicesManagedS3BackupAccessList, jsii.get(self, "managedS3BackupAccess"))

    @builtins.property
    @jsii.member(jsii_name="managedServiceIpv4Cidrs")
    def managed_service_ipv4_cidrs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "managedServiceIpv4Cidrs"))

    @builtins.property
    @jsii.member(jsii_name="resourceGatewayArn")
    def resource_gateway_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGatewayArn"))

    @builtins.property
    @jsii.member(jsii_name="s3Access")
    def s3_access(self) -> "OdbNetworkManagedServicesS3AccessList":
        return typing.cast("OdbNetworkManagedServicesS3AccessList", jsii.get(self, "s3Access"))

    @builtins.property
    @jsii.member(jsii_name="serviceNetworkArn")
    def service_network_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceNetworkArn"))

    @builtins.property
    @jsii.member(jsii_name="serviceNetworkEndpoint")
    def service_network_endpoint(
        self,
    ) -> "OdbNetworkManagedServicesServiceNetworkEndpointList":
        return typing.cast("OdbNetworkManagedServicesServiceNetworkEndpointList", jsii.get(self, "serviceNetworkEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="zeroEtlAccess")
    def zero_etl_access(self) -> "OdbNetworkManagedServicesZeroEtlAccessList":
        return typing.cast("OdbNetworkManagedServicesZeroEtlAccessList", jsii.get(self, "zeroEtlAccess"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OdbNetworkManagedServices]:
        return typing.cast(typing.Optional[OdbNetworkManagedServices], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[OdbNetworkManagedServices]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8180c192bc0085a1514355e99d0fdbed98ea45078654555ef00bbffe82907ca5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.odbNetwork.OdbNetworkManagedServicesS3Access",
    jsii_struct_bases=[],
    name_mapping={},
)
class OdbNetworkManagedServicesS3Access:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OdbNetworkManagedServicesS3Access(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OdbNetworkManagedServicesS3AccessList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbNetwork.OdbNetworkManagedServicesS3AccessList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2594ae0dc9c7537f984339ad9cb3149a21aa1080e310dfaa4d2700514d22371f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OdbNetworkManagedServicesS3AccessOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c77e66f1722316a22b7842f5cb381eace12fb64f9223aa14e1476beaf23c06a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OdbNetworkManagedServicesS3AccessOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac909136c1dc251e9ce3365e58c52d044257082aab482f7eb31c8319866dc0b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fff4a978e1c86b9ba3ef6b8c7f911d80c12bda58b8d9d3d11005bae238c0a128)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ed18b63579f327b964a1021d8e88f18eec447d2b4513ee1025c1d765148a049)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OdbNetworkManagedServicesS3AccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbNetwork.OdbNetworkManagedServicesS3AccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74e95234ebcfdd69260e66e40ca5cc4c1f41c6d27f540620407d5df93e184b0a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="ipv4Addresses")
    def ipv4_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipv4Addresses"))

    @builtins.property
    @jsii.member(jsii_name="s3PolicyDocument")
    def s3_policy_document(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3PolicyDocument"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OdbNetworkManagedServicesS3Access]:
        return typing.cast(typing.Optional[OdbNetworkManagedServicesS3Access], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OdbNetworkManagedServicesS3Access],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccfb5a4fca4fa1fd0538063c0d388a9ee9b64ef2995b1d5cf105798f0ef841e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.odbNetwork.OdbNetworkManagedServicesServiceNetworkEndpoint",
    jsii_struct_bases=[],
    name_mapping={},
)
class OdbNetworkManagedServicesServiceNetworkEndpoint:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OdbNetworkManagedServicesServiceNetworkEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OdbNetworkManagedServicesServiceNetworkEndpointList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbNetwork.OdbNetworkManagedServicesServiceNetworkEndpointList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3160f7dc3da92359c3fd3d7b7c793cd8d67b35d7abb5684c4d3162d461ff7ccd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OdbNetworkManagedServicesServiceNetworkEndpointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75ed48d817bdbbf5173d256842b6904d41a471992a2b1375b6c327ddd81e4e44)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OdbNetworkManagedServicesServiceNetworkEndpointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db43210c95c83041dd6e86c3376b5bf77c4843dd1895f20c6ab10a638c0fcdd5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__299b566bd976a9b77a5c3fd74080ad17f743c3212d901a41475ed80e7caeff6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91668414b3ae3790adad8f8943348c297482766b2a35d015bc96ec0d0624c78c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OdbNetworkManagedServicesServiceNetworkEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbNetwork.OdbNetworkManagedServicesServiceNetworkEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1e5051aab7c6439b330a4dd1d0cf7ea41036e6f5da52521c9143b921c163641)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="vpcEndpointId")
    def vpc_endpoint_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcEndpointId"))

    @builtins.property
    @jsii.member(jsii_name="vpcEndpointType")
    def vpc_endpoint_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcEndpointType"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OdbNetworkManagedServicesServiceNetworkEndpoint]:
        return typing.cast(typing.Optional[OdbNetworkManagedServicesServiceNetworkEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OdbNetworkManagedServicesServiceNetworkEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5af14fb1e81376279b9a05841c105aee21c5a123dea84512938e8f0a9f51fc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.odbNetwork.OdbNetworkManagedServicesZeroEtlAccess",
    jsii_struct_bases=[],
    name_mapping={},
)
class OdbNetworkManagedServicesZeroEtlAccess:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OdbNetworkManagedServicesZeroEtlAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OdbNetworkManagedServicesZeroEtlAccessList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbNetwork.OdbNetworkManagedServicesZeroEtlAccessList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bcad6785ae9ef95f4a27c4ecd3f5f850cc989cf8f7c2252b37efda619699b94)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OdbNetworkManagedServicesZeroEtlAccessOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab01cb0af78b0acae8b4429b0aa7679860414832f9113b8ff3892d137cf8b9a1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OdbNetworkManagedServicesZeroEtlAccessOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abe1a1e4124e28434e6afda88e93d9f7f934c45ad17ec9b908f0d98997f081d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86423c434ef3c8b77619c5d1a2b04135bf80252cdcd84ad8ed75d52bd63cefab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9472280d41cdf78a37f8e06c6c89ae77d828fdb93ede63e7a27683116089a526)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OdbNetworkManagedServicesZeroEtlAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbNetwork.OdbNetworkManagedServicesZeroEtlAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__306277a3f938d74b96e393b7f0f1ade27d0a7ec21ccda54c48ec0f048c7ac728)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="cidr")
    def cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cidr"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OdbNetworkManagedServicesZeroEtlAccess]:
        return typing.cast(typing.Optional[OdbNetworkManagedServicesZeroEtlAccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OdbNetworkManagedServicesZeroEtlAccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a50fdb46c88e844141793616b64d8d402395005388779362ffe91e369d2aabe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.odbNetwork.OdbNetworkOciDnsForwardingConfigs",
    jsii_struct_bases=[],
    name_mapping={},
)
class OdbNetworkOciDnsForwardingConfigs:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OdbNetworkOciDnsForwardingConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OdbNetworkOciDnsForwardingConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbNetwork.OdbNetworkOciDnsForwardingConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__506f93cdda522c4cb6a2b1b97beb7d51b4b037e099a882ac87dc8a528abc9273)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OdbNetworkOciDnsForwardingConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3a468e09efe789d77fd5bde25f8d62647486576e7795ca726e6215257f39fa0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OdbNetworkOciDnsForwardingConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62418cf8d738eaf4e301610d982cfed58bcdb2e5cb520499c44939a058c8d849)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5014251dc04c6bdcc5f633b73fd63d1df14632f068ef959a3e9facb5a2e23838)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b4cfd12f043c4654977a169f355f0f5d77769e719a95b73c2f552347bbbf44f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OdbNetworkOciDnsForwardingConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbNetwork.OdbNetworkOciDnsForwardingConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98c3090e64ed18e1db6e5c3fb58aaf2cf1b86294beea76f04f63a9b486ab05fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="ociDnsListenerIp")
    def oci_dns_listener_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ociDnsListenerIp"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OdbNetworkOciDnsForwardingConfigs]:
        return typing.cast(typing.Optional[OdbNetworkOciDnsForwardingConfigs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OdbNetworkOciDnsForwardingConfigs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a002e468d9e92737f970d860ebbc9a34c223bff27eb32073844683400e3def33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.odbNetwork.OdbNetworkTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class OdbNetworkTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#create OdbNetwork#create}
        :param delete: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#delete OdbNetwork#delete}
        :param update: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#update OdbNetwork#update}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb711bfbf09327973741181815acd99828558e9d5872609b5ded3a7266d78f6d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#create OdbNetwork#create}
        '''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#delete OdbNetwork#delete}
        '''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_network#update OdbNetwork#update}
        '''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OdbNetworkTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OdbNetworkTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbNetwork.OdbNetworkTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__acb433b53b6060018dcd4fd689ac3055752b233c9107f4c8eb6116d404a19385)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65c03df430938faf94ed19ac558685a988f709c92ba87d0b66082a6b03a5d2d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c900243b47599ae5209d3a70c09f45a2f65013f2392bfd24db1cfc3a767ff44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef041fa33a618db5914ca59f1d4004bf1325f9d47eda84e30770efc05f004afc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbNetworkTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbNetworkTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbNetworkTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c313ba2a843a38f4cf8cb1a6943e4ddd05fc55497357dd96ab61fa34745e34e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "OdbNetwork",
    "OdbNetworkConfig",
    "OdbNetworkManagedServices",
    "OdbNetworkManagedServicesList",
    "OdbNetworkManagedServicesManagedS3BackupAccess",
    "OdbNetworkManagedServicesManagedS3BackupAccessList",
    "OdbNetworkManagedServicesManagedS3BackupAccessOutputReference",
    "OdbNetworkManagedServicesOutputReference",
    "OdbNetworkManagedServicesS3Access",
    "OdbNetworkManagedServicesS3AccessList",
    "OdbNetworkManagedServicesS3AccessOutputReference",
    "OdbNetworkManagedServicesServiceNetworkEndpoint",
    "OdbNetworkManagedServicesServiceNetworkEndpointList",
    "OdbNetworkManagedServicesServiceNetworkEndpointOutputReference",
    "OdbNetworkManagedServicesZeroEtlAccess",
    "OdbNetworkManagedServicesZeroEtlAccessList",
    "OdbNetworkManagedServicesZeroEtlAccessOutputReference",
    "OdbNetworkOciDnsForwardingConfigs",
    "OdbNetworkOciDnsForwardingConfigsList",
    "OdbNetworkOciDnsForwardingConfigsOutputReference",
    "OdbNetworkTimeouts",
    "OdbNetworkTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__5476bb961b9a8e4f0ad793fb790ae4ca0bea6b85b042645f9dc1b5df959bd8fa(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    availability_zone_id: builtins.str,
    backup_subnet_cidr: builtins.str,
    client_subnet_cidr: builtins.str,
    display_name: builtins.str,
    s3_access: builtins.str,
    zero_etl_access: builtins.str,
    availability_zone: typing.Optional[builtins.str] = None,
    custom_domain_name: typing.Optional[builtins.str] = None,
    default_dns_prefix: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    s3_policy_document: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[OdbNetworkTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6eefb4a817068b1a1a97f7713d5bb79df33af2f16567e336dec6dfd3e3d9bf06(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__442ee7d1736b299f62823b3eb315db990f66e1c9b135f21e5bfbd3a265f4bc0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0916e8abbbdfe004b595f2bd81770d5d01f66be84ecc0c3a84da1d50ea6cd7d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d2f0580b16d5202d407ce55964730ec9effe85eff4133998600298777996e19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab33eb5987ab01f3fb70832d91ca20f34ac425bd47f3b02fb98ad261927bccd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b78bc42057f2b79d4913913d836532d5088146a08b6280c5bcce4475f97a62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc442a6da7d2020d4d5cc09a88fd172535741f90f65fd31e3d0c24f18a5f769a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c619f09762ccbbfd20032c2a264cb83724e33b456aba28dfca5df5080a27ff16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d21d01086a214898400d6cd149e97af257387700f7f79742fb52a6c95ab5355c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ceba1d981f44297e721dc2359f9b022c784e8b74db0abb263f78cd45e8014da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6284a2b10466a8e6c252c4eb8a863ed931afc50f47a66b70f28d7e7a314a8a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14e83b5543bb00806e79c46f1b58d66871f2547c88b2d87ddd3b4c4030bb4c56(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__999ee20a1f228e9d5420c1937fac2f7a2997f3ff743c7e6877aebbd454d073ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c097d9f095f8babba4e664edd7bcb6191e66ee18060e52bcbaac20031df4cb(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    availability_zone_id: builtins.str,
    backup_subnet_cidr: builtins.str,
    client_subnet_cidr: builtins.str,
    display_name: builtins.str,
    s3_access: builtins.str,
    zero_etl_access: builtins.str,
    availability_zone: typing.Optional[builtins.str] = None,
    custom_domain_name: typing.Optional[builtins.str] = None,
    default_dns_prefix: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    s3_policy_document: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[OdbNetworkTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce4235daf7357901033983dc7af080bd0e41f79499ed5421de9c57579f4a1655(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d374c41d659924594dc6c6da67ed77d51ebf29c1114e262be7c8e8b80ba1b9b2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae0b9f1439945dfe469615563cabfa5d1988b8f86c0d8709e8a015eef1544b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54e6fb42c38288e76cd9e43343f982c4a3bdfdaca76b8aae20751711e2badde(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5ef37eecc59254ba18c7fe0e9511b7d03ebf7382de07090c5ddf0e611799a51(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5248a3e4b46d27dcfd2dd3d9cc4287444f9e27713a221dee633e7b85c0df5ef7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca9733fbfd3256e81c4e1d047bd673403db0d614352ee40be01d91435034f078(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__290032007310a33e5ee1ac6a19b20490fb3f5fdc325cba529e53e7a2b24d1bb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f16e5d342a742226c665ea6df0a688aff59a9b59e1e204adf9b7c006fdaa1f9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40d48cb726b5d55fa672ccd642f719baa814e18727ae04578e992a76c3e5da17(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df64bf6beb5083f37fb9d8eee3b0bc7d56df61daa098f1ca14597c04b4e906e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c482765e770c6db3e378beeeec84a14d2bcc6183f5428a812943b2ca4d21b7d(
    value: typing.Optional[OdbNetworkManagedServicesManagedS3BackupAccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30855eb8cb722bce111b0051d62b99405a4a48df7deff74dd0436607acd32bb9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8180c192bc0085a1514355e99d0fdbed98ea45078654555ef00bbffe82907ca5(
    value: typing.Optional[OdbNetworkManagedServices],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2594ae0dc9c7537f984339ad9cb3149a21aa1080e310dfaa4d2700514d22371f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c77e66f1722316a22b7842f5cb381eace12fb64f9223aa14e1476beaf23c06a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac909136c1dc251e9ce3365e58c52d044257082aab482f7eb31c8319866dc0b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff4a978e1c86b9ba3ef6b8c7f911d80c12bda58b8d9d3d11005bae238c0a128(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed18b63579f327b964a1021d8e88f18eec447d2b4513ee1025c1d765148a049(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74e95234ebcfdd69260e66e40ca5cc4c1f41c6d27f540620407d5df93e184b0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccfb5a4fca4fa1fd0538063c0d388a9ee9b64ef2995b1d5cf105798f0ef841e2(
    value: typing.Optional[OdbNetworkManagedServicesS3Access],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3160f7dc3da92359c3fd3d7b7c793cd8d67b35d7abb5684c4d3162d461ff7ccd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ed48d817bdbbf5173d256842b6904d41a471992a2b1375b6c327ddd81e4e44(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db43210c95c83041dd6e86c3376b5bf77c4843dd1895f20c6ab10a638c0fcdd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__299b566bd976a9b77a5c3fd74080ad17f743c3212d901a41475ed80e7caeff6c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91668414b3ae3790adad8f8943348c297482766b2a35d015bc96ec0d0624c78c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e5051aab7c6439b330a4dd1d0cf7ea41036e6f5da52521c9143b921c163641(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5af14fb1e81376279b9a05841c105aee21c5a123dea84512938e8f0a9f51fc8(
    value: typing.Optional[OdbNetworkManagedServicesServiceNetworkEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bcad6785ae9ef95f4a27c4ecd3f5f850cc989cf8f7c2252b37efda619699b94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab01cb0af78b0acae8b4429b0aa7679860414832f9113b8ff3892d137cf8b9a1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe1a1e4124e28434e6afda88e93d9f7f934c45ad17ec9b908f0d98997f081d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86423c434ef3c8b77619c5d1a2b04135bf80252cdcd84ad8ed75d52bd63cefab(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9472280d41cdf78a37f8e06c6c89ae77d828fdb93ede63e7a27683116089a526(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__306277a3f938d74b96e393b7f0f1ade27d0a7ec21ccda54c48ec0f048c7ac728(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a50fdb46c88e844141793616b64d8d402395005388779362ffe91e369d2aabe6(
    value: typing.Optional[OdbNetworkManagedServicesZeroEtlAccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__506f93cdda522c4cb6a2b1b97beb7d51b4b037e099a882ac87dc8a528abc9273(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3a468e09efe789d77fd5bde25f8d62647486576e7795ca726e6215257f39fa0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62418cf8d738eaf4e301610d982cfed58bcdb2e5cb520499c44939a058c8d849(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5014251dc04c6bdcc5f633b73fd63d1df14632f068ef959a3e9facb5a2e23838(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4cfd12f043c4654977a169f355f0f5d77769e719a95b73c2f552347bbbf44f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c3090e64ed18e1db6e5c3fb58aaf2cf1b86294beea76f04f63a9b486ab05fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a002e468d9e92737f970d860ebbc9a34c223bff27eb32073844683400e3def33(
    value: typing.Optional[OdbNetworkOciDnsForwardingConfigs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb711bfbf09327973741181815acd99828558e9d5872609b5ded3a7266d78f6d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acb433b53b6060018dcd4fd689ac3055752b233c9107f4c8eb6116d404a19385(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c03df430938faf94ed19ac558685a988f709c92ba87d0b66082a6b03a5d2d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c900243b47599ae5209d3a70c09f45a2f65013f2392bfd24db1cfc3a767ff44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef041fa33a618db5914ca59f1d4004bf1325f9d47eda84e30770efc05f004afc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c313ba2a843a38f4cf8cb1a6943e4ddd05fc55497357dd96ab61fa34745e34e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbNetworkTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
