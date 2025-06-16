r'''
# `google_filestore_instance`

Refer to the Terraform Registry for docs: [`google_filestore_instance`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance).
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


class GoogleFilestoreInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance google_filestore_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        file_shares: typing.Union["GoogleFilestoreInstanceFileShares", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        networks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleFilestoreInstanceNetworks", typing.Dict[builtins.str, typing.Any]]]],
        tier: builtins.str,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deletion_protection_reason: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        directory_services: typing.Optional[typing.Union["GoogleFilestoreInstanceDirectoryServices", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        initial_replication: typing.Optional[typing.Union["GoogleFilestoreInstanceInitialReplication", typing.Dict[builtins.str, typing.Any]]] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        performance_config: typing.Optional[typing.Union["GoogleFilestoreInstancePerformanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["GoogleFilestoreInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance google_filestore_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param file_shares: file_shares block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#file_shares GoogleFilestoreInstance#file_shares}
        :param name: The resource name of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#name GoogleFilestoreInstance#name}
        :param networks: networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#networks GoogleFilestoreInstance#networks}
        :param tier: The service tier of the instance. Possible values include: STANDARD, PREMIUM, BASIC_HDD, BASIC_SSD, HIGH_SCALE_SSD, ZONAL, REGIONAL and ENTERPRISE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#tier GoogleFilestoreInstance#tier}
        :param deletion_protection_enabled: Indicates whether the instance is protected against deletion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#deletion_protection_enabled GoogleFilestoreInstance#deletion_protection_enabled}
        :param deletion_protection_reason: The reason for enabling deletion protection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#deletion_protection_reason GoogleFilestoreInstance#deletion_protection_reason}
        :param description: A description of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#description GoogleFilestoreInstance#description}
        :param directory_services: directory_services block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#directory_services GoogleFilestoreInstance#directory_services}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#id GoogleFilestoreInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_replication: initial_replication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#initial_replication GoogleFilestoreInstance#initial_replication}
        :param kms_key_name: KMS key name used for data encryption. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#kms_key_name GoogleFilestoreInstance#kms_key_name}
        :param labels: Resource labels to represent user-provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#labels GoogleFilestoreInstance#labels}
        :param location: The name of the location of the instance. This can be a region for ENTERPRISE tier instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#location GoogleFilestoreInstance#location}
        :param performance_config: performance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#performance_config GoogleFilestoreInstance#performance_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#project GoogleFilestoreInstance#project}.
        :param protocol: Either NFSv3, for using NFS version 3 as file sharing protocol, or NFSv4.1, for using NFS version 4.1 as file sharing protocol. NFSv4.1 can be used with HIGH_SCALE_SSD, ZONAL, REGIONAL and ENTERPRISE. The default is NFSv3. Default value: "NFS_V3" Possible values: ["NFS_V3", "NFS_V4_1"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#protocol GoogleFilestoreInstance#protocol}
        :param tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored when empty. The field is immutable and causes resource replacement when mutated. This field is only set at create time and modifying this field after creation will trigger recreation. To apply tags to an existing resource, see the 'google_tags_tag_value' resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#tags GoogleFilestoreInstance#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#timeouts GoogleFilestoreInstance#timeouts}
        :param zone: The name of the Filestore zone of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#zone GoogleFilestoreInstance#zone}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b88457e3785dc7c40547af5ea963a8ee18c32cbef9ed8cb998c83852d7336614)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleFilestoreInstanceConfig(
            file_shares=file_shares,
            name=name,
            networks=networks,
            tier=tier,
            deletion_protection_enabled=deletion_protection_enabled,
            deletion_protection_reason=deletion_protection_reason,
            description=description,
            directory_services=directory_services,
            id=id,
            initial_replication=initial_replication,
            kms_key_name=kms_key_name,
            labels=labels,
            location=location,
            performance_config=performance_config,
            project=project,
            protocol=protocol,
            tags=tags,
            timeouts=timeouts,
            zone=zone,
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
        '''Generates CDKTF code for importing a GoogleFilestoreInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleFilestoreInstance to import.
        :param import_from_id: The id of the existing GoogleFilestoreInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleFilestoreInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f1a678fc2d9a5ca3d302cbe7b6576694f69394b3479964886db420c5c7853ab)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDirectoryServices")
    def put_directory_services(
        self,
        *,
        ldap: typing.Optional[typing.Union["GoogleFilestoreInstanceDirectoryServicesLdap", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ldap: ldap block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#ldap GoogleFilestoreInstance#ldap}
        '''
        value = GoogleFilestoreInstanceDirectoryServices(ldap=ldap)

        return typing.cast(None, jsii.invoke(self, "putDirectoryServices", [value]))

    @jsii.member(jsii_name="putFileShares")
    def put_file_shares(
        self,
        *,
        capacity_gb: jsii.Number,
        name: builtins.str,
        nfs_export_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleFilestoreInstanceFileSharesNfsExportOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        source_backup: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param capacity_gb: File share capacity in GiB. This must be at least 1024 GiB for the standard tier, or 2560 GiB for the premium tier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#capacity_gb GoogleFilestoreInstance#capacity_gb}
        :param name: The name of the fileshare (16 characters or less). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#name GoogleFilestoreInstance#name}
        :param nfs_export_options: nfs_export_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#nfs_export_options GoogleFilestoreInstance#nfs_export_options}
        :param source_backup: The resource name of the backup, in the format projects/{projectId}/locations/{locationId}/backups/{backupId}, that this file share has been restored from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#source_backup GoogleFilestoreInstance#source_backup}
        '''
        value = GoogleFilestoreInstanceFileShares(
            capacity_gb=capacity_gb,
            name=name,
            nfs_export_options=nfs_export_options,
            source_backup=source_backup,
        )

        return typing.cast(None, jsii.invoke(self, "putFileShares", [value]))

    @jsii.member(jsii_name="putInitialReplication")
    def put_initial_replication(
        self,
        *,
        replicas: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleFilestoreInstanceInitialReplicationReplicas", typing.Dict[builtins.str, typing.Any]]]]] = None,
        role: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param replicas: replicas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#replicas GoogleFilestoreInstance#replicas}
        :param role: The replication role. Default value: "STANDBY" Possible values: ["ROLE_UNSPECIFIED", "ACTIVE", "STANDBY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#role GoogleFilestoreInstance#role}
        '''
        value = GoogleFilestoreInstanceInitialReplication(replicas=replicas, role=role)

        return typing.cast(None, jsii.invoke(self, "putInitialReplication", [value]))

    @jsii.member(jsii_name="putNetworks")
    def put_networks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleFilestoreInstanceNetworks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2766c9e3eef010c8e2797456727f62e87c689f23ff02f545fecb06278b48c344)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworks", [value]))

    @jsii.member(jsii_name="putPerformanceConfig")
    def put_performance_config(
        self,
        *,
        fixed_iops: typing.Optional[typing.Union["GoogleFilestoreInstancePerformanceConfigFixedIops", typing.Dict[builtins.str, typing.Any]]] = None,
        iops_per_tb: typing.Optional[typing.Union["GoogleFilestoreInstancePerformanceConfigIopsPerTb", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param fixed_iops: fixed_iops block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#fixed_iops GoogleFilestoreInstance#fixed_iops}
        :param iops_per_tb: iops_per_tb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#iops_per_tb GoogleFilestoreInstance#iops_per_tb}
        '''
        value = GoogleFilestoreInstancePerformanceConfig(
            fixed_iops=fixed_iops, iops_per_tb=iops_per_tb
        )

        return typing.cast(None, jsii.invoke(self, "putPerformanceConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#create GoogleFilestoreInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#delete GoogleFilestoreInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#update GoogleFilestoreInstance#update}.
        '''
        value = GoogleFilestoreInstanceTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDeletionProtectionEnabled")
    def reset_deletion_protection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtectionEnabled", []))

    @jsii.member(jsii_name="resetDeletionProtectionReason")
    def reset_deletion_protection_reason(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtectionReason", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDirectoryServices")
    def reset_directory_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirectoryServices", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInitialReplication")
    def reset_initial_replication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialReplication", []))

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetPerformanceConfig")
    def reset_performance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerformanceConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="directoryServices")
    def directory_services(
        self,
    ) -> "GoogleFilestoreInstanceDirectoryServicesOutputReference":
        return typing.cast("GoogleFilestoreInstanceDirectoryServicesOutputReference", jsii.get(self, "directoryServices"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="effectiveReplication")
    def effective_replication(
        self,
    ) -> "GoogleFilestoreInstanceEffectiveReplicationList":
        return typing.cast("GoogleFilestoreInstanceEffectiveReplicationList", jsii.get(self, "effectiveReplication"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="fileShares")
    def file_shares(self) -> "GoogleFilestoreInstanceFileSharesOutputReference":
        return typing.cast("GoogleFilestoreInstanceFileSharesOutputReference", jsii.get(self, "fileShares"))

    @builtins.property
    @jsii.member(jsii_name="initialReplication")
    def initial_replication(
        self,
    ) -> "GoogleFilestoreInstanceInitialReplicationOutputReference":
        return typing.cast("GoogleFilestoreInstanceInitialReplicationOutputReference", jsii.get(self, "initialReplication"))

    @builtins.property
    @jsii.member(jsii_name="networks")
    def networks(self) -> "GoogleFilestoreInstanceNetworksList":
        return typing.cast("GoogleFilestoreInstanceNetworksList", jsii.get(self, "networks"))

    @builtins.property
    @jsii.member(jsii_name="performanceConfig")
    def performance_config(
        self,
    ) -> "GoogleFilestoreInstancePerformanceConfigOutputReference":
        return typing.cast("GoogleFilestoreInstancePerformanceConfigOutputReference", jsii.get(self, "performanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleFilestoreInstanceTimeoutsOutputReference":
        return typing.cast("GoogleFilestoreInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionEnabledInput")
    def deletion_protection_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletionProtectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionReasonInput")
    def deletion_protection_reason_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deletionProtectionReasonInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="directoryServicesInput")
    def directory_services_input(
        self,
    ) -> typing.Optional["GoogleFilestoreInstanceDirectoryServices"]:
        return typing.cast(typing.Optional["GoogleFilestoreInstanceDirectoryServices"], jsii.get(self, "directoryServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="fileSharesInput")
    def file_shares_input(self) -> typing.Optional["GoogleFilestoreInstanceFileShares"]:
        return typing.cast(typing.Optional["GoogleFilestoreInstanceFileShares"], jsii.get(self, "fileSharesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="initialReplicationInput")
    def initial_replication_input(
        self,
    ) -> typing.Optional["GoogleFilestoreInstanceInitialReplication"]:
        return typing.cast(typing.Optional["GoogleFilestoreInstanceInitialReplication"], jsii.get(self, "initialReplicationInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networksInput")
    def networks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleFilestoreInstanceNetworks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleFilestoreInstanceNetworks"]]], jsii.get(self, "networksInput"))

    @builtins.property
    @jsii.member(jsii_name="performanceConfigInput")
    def performance_config_input(
        self,
    ) -> typing.Optional["GoogleFilestoreInstancePerformanceConfig"]:
        return typing.cast(typing.Optional["GoogleFilestoreInstancePerformanceConfig"], jsii.get(self, "performanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="tierInput")
    def tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tierInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleFilestoreInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleFilestoreInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionEnabled")
    def deletion_protection_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deletionProtectionEnabled"))

    @deletion_protection_enabled.setter
    def deletion_protection_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f398ff0d6e16d37ff41f4436acd0603787f9854694ac0434a738550a855eb7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtectionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionReason")
    def deletion_protection_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deletionProtectionReason"))

    @deletion_protection_reason.setter
    def deletion_protection_reason(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bfdf217a6640246c00e06488b197e447f944c650bfb38fc9d5122f675fa1afb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtectionReason", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9d9b9317e7c03eda0dce30cce8c6133fdda43315cb461aebdca8b76fdfe29dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd5b7483fb48b92ed1a45db429c5d53f2a9cad3cce52dcf294c2a7f46a0f2e67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3efbcbd036ba0b66c2251f6664a0e0f2e9f3b17319770725711ae9d889afd155)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fdf6437646652124173290788239e65103c1b702ef5668d051de96654e861ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3b5f7c9736bccbb786865c93cb53377a240ddf40bb5aa9eb1ee05d127870cda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__418b9835a028fbb374bdd586668a3612a9e9bbb5ad4c0a1f532879e36cb0b643)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b87f464c5a9ca070bd7a76a15f70a49ae0b9ad4fb3494d10f64a2fd35fd12756)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ca098cc6fb6e57238ffe0841f67bb8a9205a39b2351fb97f0998b819e038c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__143b64321db8ecb8f24bf46d508f09f1df1188e17046de48f571ffca77840887)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eda75fff777e34779bc68d69fa8c1fe5516381567bf5638316be18e499a664a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aea818df78c7e3cf9aac1ce6701866d1aab49d62aa958d14c6c3d7c5ee97d5a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "file_shares": "fileShares",
        "name": "name",
        "networks": "networks",
        "tier": "tier",
        "deletion_protection_enabled": "deletionProtectionEnabled",
        "deletion_protection_reason": "deletionProtectionReason",
        "description": "description",
        "directory_services": "directoryServices",
        "id": "id",
        "initial_replication": "initialReplication",
        "kms_key_name": "kmsKeyName",
        "labels": "labels",
        "location": "location",
        "performance_config": "performanceConfig",
        "project": "project",
        "protocol": "protocol",
        "tags": "tags",
        "timeouts": "timeouts",
        "zone": "zone",
    },
)
class GoogleFilestoreInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        file_shares: typing.Union["GoogleFilestoreInstanceFileShares", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        networks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleFilestoreInstanceNetworks", typing.Dict[builtins.str, typing.Any]]]],
        tier: builtins.str,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deletion_protection_reason: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        directory_services: typing.Optional[typing.Union["GoogleFilestoreInstanceDirectoryServices", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        initial_replication: typing.Optional[typing.Union["GoogleFilestoreInstanceInitialReplication", typing.Dict[builtins.str, typing.Any]]] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        performance_config: typing.Optional[typing.Union["GoogleFilestoreInstancePerformanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["GoogleFilestoreInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param file_shares: file_shares block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#file_shares GoogleFilestoreInstance#file_shares}
        :param name: The resource name of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#name GoogleFilestoreInstance#name}
        :param networks: networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#networks GoogleFilestoreInstance#networks}
        :param tier: The service tier of the instance. Possible values include: STANDARD, PREMIUM, BASIC_HDD, BASIC_SSD, HIGH_SCALE_SSD, ZONAL, REGIONAL and ENTERPRISE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#tier GoogleFilestoreInstance#tier}
        :param deletion_protection_enabled: Indicates whether the instance is protected against deletion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#deletion_protection_enabled GoogleFilestoreInstance#deletion_protection_enabled}
        :param deletion_protection_reason: The reason for enabling deletion protection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#deletion_protection_reason GoogleFilestoreInstance#deletion_protection_reason}
        :param description: A description of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#description GoogleFilestoreInstance#description}
        :param directory_services: directory_services block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#directory_services GoogleFilestoreInstance#directory_services}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#id GoogleFilestoreInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_replication: initial_replication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#initial_replication GoogleFilestoreInstance#initial_replication}
        :param kms_key_name: KMS key name used for data encryption. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#kms_key_name GoogleFilestoreInstance#kms_key_name}
        :param labels: Resource labels to represent user-provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#labels GoogleFilestoreInstance#labels}
        :param location: The name of the location of the instance. This can be a region for ENTERPRISE tier instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#location GoogleFilestoreInstance#location}
        :param performance_config: performance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#performance_config GoogleFilestoreInstance#performance_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#project GoogleFilestoreInstance#project}.
        :param protocol: Either NFSv3, for using NFS version 3 as file sharing protocol, or NFSv4.1, for using NFS version 4.1 as file sharing protocol. NFSv4.1 can be used with HIGH_SCALE_SSD, ZONAL, REGIONAL and ENTERPRISE. The default is NFSv3. Default value: "NFS_V3" Possible values: ["NFS_V3", "NFS_V4_1"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#protocol GoogleFilestoreInstance#protocol}
        :param tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored when empty. The field is immutable and causes resource replacement when mutated. This field is only set at create time and modifying this field after creation will trigger recreation. To apply tags to an existing resource, see the 'google_tags_tag_value' resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#tags GoogleFilestoreInstance#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#timeouts GoogleFilestoreInstance#timeouts}
        :param zone: The name of the Filestore zone of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#zone GoogleFilestoreInstance#zone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(file_shares, dict):
            file_shares = GoogleFilestoreInstanceFileShares(**file_shares)
        if isinstance(directory_services, dict):
            directory_services = GoogleFilestoreInstanceDirectoryServices(**directory_services)
        if isinstance(initial_replication, dict):
            initial_replication = GoogleFilestoreInstanceInitialReplication(**initial_replication)
        if isinstance(performance_config, dict):
            performance_config = GoogleFilestoreInstancePerformanceConfig(**performance_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleFilestoreInstanceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2a8debe325b213b7082dbefdfda63ff26e1e95c390e3c7359b96b44919a15a8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument file_shares", value=file_shares, expected_type=type_hints["file_shares"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument networks", value=networks, expected_type=type_hints["networks"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument deletion_protection_enabled", value=deletion_protection_enabled, expected_type=type_hints["deletion_protection_enabled"])
            check_type(argname="argument deletion_protection_reason", value=deletion_protection_reason, expected_type=type_hints["deletion_protection_reason"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument directory_services", value=directory_services, expected_type=type_hints["directory_services"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument initial_replication", value=initial_replication, expected_type=type_hints["initial_replication"])
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument performance_config", value=performance_config, expected_type=type_hints["performance_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file_shares": file_shares,
            "name": name,
            "networks": networks,
            "tier": tier,
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
        if deletion_protection_enabled is not None:
            self._values["deletion_protection_enabled"] = deletion_protection_enabled
        if deletion_protection_reason is not None:
            self._values["deletion_protection_reason"] = deletion_protection_reason
        if description is not None:
            self._values["description"] = description
        if directory_services is not None:
            self._values["directory_services"] = directory_services
        if id is not None:
            self._values["id"] = id
        if initial_replication is not None:
            self._values["initial_replication"] = initial_replication
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name
        if labels is not None:
            self._values["labels"] = labels
        if location is not None:
            self._values["location"] = location
        if performance_config is not None:
            self._values["performance_config"] = performance_config
        if project is not None:
            self._values["project"] = project
        if protocol is not None:
            self._values["protocol"] = protocol
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if zone is not None:
            self._values["zone"] = zone

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
    def file_shares(self) -> "GoogleFilestoreInstanceFileShares":
        '''file_shares block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#file_shares GoogleFilestoreInstance#file_shares}
        '''
        result = self._values.get("file_shares")
        assert result is not None, "Required property 'file_shares' is missing"
        return typing.cast("GoogleFilestoreInstanceFileShares", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The resource name of the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#name GoogleFilestoreInstance#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def networks(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleFilestoreInstanceNetworks"]]:
        '''networks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#networks GoogleFilestoreInstance#networks}
        '''
        result = self._values.get("networks")
        assert result is not None, "Required property 'networks' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleFilestoreInstanceNetworks"]], result)

    @builtins.property
    def tier(self) -> builtins.str:
        '''The service tier of the instance. Possible values include: STANDARD, PREMIUM, BASIC_HDD, BASIC_SSD, HIGH_SCALE_SSD, ZONAL, REGIONAL and ENTERPRISE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#tier GoogleFilestoreInstance#tier}
        '''
        result = self._values.get("tier")
        assert result is not None, "Required property 'tier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deletion_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether the instance is protected against deletion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#deletion_protection_enabled GoogleFilestoreInstance#deletion_protection_enabled}
        '''
        result = self._values.get("deletion_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def deletion_protection_reason(self) -> typing.Optional[builtins.str]:
        '''The reason for enabling deletion protection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#deletion_protection_reason GoogleFilestoreInstance#deletion_protection_reason}
        '''
        result = self._values.get("deletion_protection_reason")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#description GoogleFilestoreInstance#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def directory_services(
        self,
    ) -> typing.Optional["GoogleFilestoreInstanceDirectoryServices"]:
        '''directory_services block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#directory_services GoogleFilestoreInstance#directory_services}
        '''
        result = self._values.get("directory_services")
        return typing.cast(typing.Optional["GoogleFilestoreInstanceDirectoryServices"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#id GoogleFilestoreInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_replication(
        self,
    ) -> typing.Optional["GoogleFilestoreInstanceInitialReplication"]:
        '''initial_replication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#initial_replication GoogleFilestoreInstance#initial_replication}
        '''
        result = self._values.get("initial_replication")
        return typing.cast(typing.Optional["GoogleFilestoreInstanceInitialReplication"], result)

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''KMS key name used for data encryption.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#kms_key_name GoogleFilestoreInstance#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Resource labels to represent user-provided metadata.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#labels GoogleFilestoreInstance#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The name of the location of the instance. This can be a region for ENTERPRISE tier instances.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#location GoogleFilestoreInstance#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def performance_config(
        self,
    ) -> typing.Optional["GoogleFilestoreInstancePerformanceConfig"]:
        '''performance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#performance_config GoogleFilestoreInstance#performance_config}
        '''
        result = self._values.get("performance_config")
        return typing.cast(typing.Optional["GoogleFilestoreInstancePerformanceConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#project GoogleFilestoreInstance#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Either NFSv3, for using NFS version 3 as file sharing protocol, or NFSv4.1, for using NFS version 4.1 as file sharing protocol. NFSv4.1 can be used with HIGH_SCALE_SSD, ZONAL, REGIONAL and ENTERPRISE. The default is NFSv3. Default value: "NFS_V3" Possible values: ["NFS_V3", "NFS_V4_1"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#protocol GoogleFilestoreInstance#protocol}
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of resource manager tags.

        Resource manager tag keys
        and values have the same definition as resource manager
        tags. Keys must be in the format tagKeys/{tag_key_id},
        and values are in the format tagValues/456. The field is
        ignored when empty. The field is immutable and causes
        resource replacement when mutated. This field is only set
        at create time and modifying this field after creation
        will trigger recreation. To apply tags to an existing
        resource, see the 'google_tags_tag_value' resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#tags GoogleFilestoreInstance#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleFilestoreInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#timeouts GoogleFilestoreInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleFilestoreInstanceTimeouts"], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''The name of the Filestore zone of the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#zone GoogleFilestoreInstance#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleFilestoreInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceDirectoryServices",
    jsii_struct_bases=[],
    name_mapping={"ldap": "ldap"},
)
class GoogleFilestoreInstanceDirectoryServices:
    def __init__(
        self,
        *,
        ldap: typing.Optional[typing.Union["GoogleFilestoreInstanceDirectoryServicesLdap", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ldap: ldap block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#ldap GoogleFilestoreInstance#ldap}
        '''
        if isinstance(ldap, dict):
            ldap = GoogleFilestoreInstanceDirectoryServicesLdap(**ldap)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f218b4dc7d64415c1fd555512268b0aa7faa76164a4aef692f04637a26a7899c)
            check_type(argname="argument ldap", value=ldap, expected_type=type_hints["ldap"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ldap is not None:
            self._values["ldap"] = ldap

    @builtins.property
    def ldap(self) -> typing.Optional["GoogleFilestoreInstanceDirectoryServicesLdap"]:
        '''ldap block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#ldap GoogleFilestoreInstance#ldap}
        '''
        result = self._values.get("ldap")
        return typing.cast(typing.Optional["GoogleFilestoreInstanceDirectoryServicesLdap"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleFilestoreInstanceDirectoryServices(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceDirectoryServicesLdap",
    jsii_struct_bases=[],
    name_mapping={
        "domain": "domain",
        "servers": "servers",
        "groups_ou": "groupsOu",
        "users_ou": "usersOu",
    },
)
class GoogleFilestoreInstanceDirectoryServicesLdap:
    def __init__(
        self,
        *,
        domain: builtins.str,
        servers: typing.Sequence[builtins.str],
        groups_ou: typing.Optional[builtins.str] = None,
        users_ou: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param domain: The LDAP domain name in the format of 'my-domain.com'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#domain GoogleFilestoreInstance#domain}
        :param servers: The servers names are used for specifying the LDAP servers names. The LDAP servers names can come with two formats: 1. DNS name, for example: 'ldap.example1.com', 'ldap.example2.com'. 2. IP address, for example: '10.0.0.1', '10.0.0.2', '10.0.0.3'. All servers names must be in the same format: either all DNS names or all IP addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#servers GoogleFilestoreInstance#servers}
        :param groups_ou: The groups Organizational Unit (OU) is optional. This parameter is a hint to allow faster lookup in the LDAP namespace. In case that this parameter is not provided, Filestore instance will query the whole LDAP namespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#groups_ou GoogleFilestoreInstance#groups_ou}
        :param users_ou: The users Organizational Unit (OU) is optional. This parameter is a hint to allow faster lookup in the LDAP namespace. In case that this parameter is not provided, Filestore instance will query the whole LDAP namespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#users_ou GoogleFilestoreInstance#users_ou}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12208d29c8fa8861e20f859b6303968815a949a81083a44e01932601bf350554)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument servers", value=servers, expected_type=type_hints["servers"])
            check_type(argname="argument groups_ou", value=groups_ou, expected_type=type_hints["groups_ou"])
            check_type(argname="argument users_ou", value=users_ou, expected_type=type_hints["users_ou"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain": domain,
            "servers": servers,
        }
        if groups_ou is not None:
            self._values["groups_ou"] = groups_ou
        if users_ou is not None:
            self._values["users_ou"] = users_ou

    @builtins.property
    def domain(self) -> builtins.str:
        '''The LDAP domain name in the format of 'my-domain.com'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#domain GoogleFilestoreInstance#domain}
        '''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def servers(self) -> typing.List[builtins.str]:
        '''The servers names are used for specifying the LDAP servers names.

        The LDAP servers names can come with two formats:

        1. DNS name, for example: 'ldap.example1.com', 'ldap.example2.com'.
        2. IP address, for example: '10.0.0.1', '10.0.0.2', '10.0.0.3'.
           All servers names must be in the same format: either all DNS names or all
           IP addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#servers GoogleFilestoreInstance#servers}
        '''
        result = self._values.get("servers")
        assert result is not None, "Required property 'servers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def groups_ou(self) -> typing.Optional[builtins.str]:
        '''The groups Organizational Unit (OU) is optional.

        This parameter is a hint
        to allow faster lookup in the LDAP namespace. In case that this parameter
        is not provided, Filestore instance will query the whole LDAP namespace.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#groups_ou GoogleFilestoreInstance#groups_ou}
        '''
        result = self._values.get("groups_ou")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def users_ou(self) -> typing.Optional[builtins.str]:
        '''The users Organizational Unit (OU) is optional.

        This parameter is a hint
        to allow faster lookup in the LDAP namespace. In case that this parameter
        is not provided, Filestore instance will query the whole LDAP namespace.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#users_ou GoogleFilestoreInstance#users_ou}
        '''
        result = self._values.get("users_ou")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleFilestoreInstanceDirectoryServicesLdap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleFilestoreInstanceDirectoryServicesLdapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceDirectoryServicesLdapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40da28da8d00c77e21454bff3cd64977a737be73e9549ec429c806b91e2b8e76)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGroupsOu")
    def reset_groups_ou(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupsOu", []))

    @jsii.member(jsii_name="resetUsersOu")
    def reset_users_ou(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsersOu", []))

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsOuInput")
    def groups_ou_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupsOuInput"))

    @builtins.property
    @jsii.member(jsii_name="serversInput")
    def servers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "serversInput"))

    @builtins.property
    @jsii.member(jsii_name="usersOuInput")
    def users_ou_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usersOuInput"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3d696c3cbe7034d69a62c0ee30a3362ea94410b56bd12a40fb4376a75da34e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupsOu")
    def groups_ou(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupsOu"))

    @groups_ou.setter
    def groups_ou(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71b216cef9144dfe5b58f1d8a4fa261fcb54689b0006604dc732803e1d1623aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsOu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servers")
    def servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "servers"))

    @servers.setter
    def servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__754606bd8b005676d1bc640267ca64042a9264e0ebd5d87923405981f23d70d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="usersOu")
    def users_ou(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usersOu"))

    @users_ou.setter
    def users_ou(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de9046de0c050dc826f46258baa17cbdcf00968159add239950d76dd9f5ad5f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usersOu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleFilestoreInstanceDirectoryServicesLdap]:
        return typing.cast(typing.Optional[GoogleFilestoreInstanceDirectoryServicesLdap], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleFilestoreInstanceDirectoryServicesLdap],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8dfaec4727babc01f6092778fd93cdf178df990b527382b497b5aa5fddd9bdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleFilestoreInstanceDirectoryServicesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceDirectoryServicesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa8ac2831803231ad7a94c38e1f3fc76ebf7f12a3dfb2724feb994e50d893139)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLdap")
    def put_ldap(
        self,
        *,
        domain: builtins.str,
        servers: typing.Sequence[builtins.str],
        groups_ou: typing.Optional[builtins.str] = None,
        users_ou: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param domain: The LDAP domain name in the format of 'my-domain.com'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#domain GoogleFilestoreInstance#domain}
        :param servers: The servers names are used for specifying the LDAP servers names. The LDAP servers names can come with two formats: 1. DNS name, for example: 'ldap.example1.com', 'ldap.example2.com'. 2. IP address, for example: '10.0.0.1', '10.0.0.2', '10.0.0.3'. All servers names must be in the same format: either all DNS names or all IP addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#servers GoogleFilestoreInstance#servers}
        :param groups_ou: The groups Organizational Unit (OU) is optional. This parameter is a hint to allow faster lookup in the LDAP namespace. In case that this parameter is not provided, Filestore instance will query the whole LDAP namespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#groups_ou GoogleFilestoreInstance#groups_ou}
        :param users_ou: The users Organizational Unit (OU) is optional. This parameter is a hint to allow faster lookup in the LDAP namespace. In case that this parameter is not provided, Filestore instance will query the whole LDAP namespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#users_ou GoogleFilestoreInstance#users_ou}
        '''
        value = GoogleFilestoreInstanceDirectoryServicesLdap(
            domain=domain, servers=servers, groups_ou=groups_ou, users_ou=users_ou
        )

        return typing.cast(None, jsii.invoke(self, "putLdap", [value]))

    @jsii.member(jsii_name="resetLdap")
    def reset_ldap(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLdap", []))

    @builtins.property
    @jsii.member(jsii_name="ldap")
    def ldap(self) -> GoogleFilestoreInstanceDirectoryServicesLdapOutputReference:
        return typing.cast(GoogleFilestoreInstanceDirectoryServicesLdapOutputReference, jsii.get(self, "ldap"))

    @builtins.property
    @jsii.member(jsii_name="ldapInput")
    def ldap_input(
        self,
    ) -> typing.Optional[GoogleFilestoreInstanceDirectoryServicesLdap]:
        return typing.cast(typing.Optional[GoogleFilestoreInstanceDirectoryServicesLdap], jsii.get(self, "ldapInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleFilestoreInstanceDirectoryServices]:
        return typing.cast(typing.Optional[GoogleFilestoreInstanceDirectoryServices], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleFilestoreInstanceDirectoryServices],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4720f08135e64ea0a8729e2667307b934cc6e7a504ca964e5f233d7eaed4fc26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceEffectiveReplication",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleFilestoreInstanceEffectiveReplication:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleFilestoreInstanceEffectiveReplication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleFilestoreInstanceEffectiveReplicationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceEffectiveReplicationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8118820eed4a700d002d16dfe1c9a2f479ba7fb8a8e500b751fcd33f2f59bee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleFilestoreInstanceEffectiveReplicationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d524284a361ec74c152c8ba27820897f408a984942ec2cd8ca478bccd5e8d9fe)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleFilestoreInstanceEffectiveReplicationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05fc395f88ba059598751216a65165407e509bb83f241ee9ce1470a743c0e7ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6808f51ee3a28f0483b656796da2e2ea8cc5eeaa66c6400e3288905d06ecac99)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa038b1feedb6626f6322b5a6e3530e0ce44cb4d7de72458831ee5eb745dbb45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleFilestoreInstanceEffectiveReplicationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceEffectiveReplicationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__697f9a4c958ecf1056d793fe43301b6cbfd8d34fb5f4fd3cb4e9e628c51c56f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="replicas")
    def replicas(self) -> "GoogleFilestoreInstanceEffectiveReplicationReplicasList":
        return typing.cast("GoogleFilestoreInstanceEffectiveReplicationReplicasList", jsii.get(self, "replicas"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleFilestoreInstanceEffectiveReplication]:
        return typing.cast(typing.Optional[GoogleFilestoreInstanceEffectiveReplication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleFilestoreInstanceEffectiveReplication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b528ede62aa841672d02f7fdf2b94d847f7e8380a69b5c647c96600247c54ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceEffectiveReplicationReplicas",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleFilestoreInstanceEffectiveReplicationReplicas:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleFilestoreInstanceEffectiveReplicationReplicas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleFilestoreInstanceEffectiveReplicationReplicasList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceEffectiveReplicationReplicasList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27ed76cb65ea7a9d8788d25d90a2a67b0a24c6e96aa6d49704754b9fd0567473)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleFilestoreInstanceEffectiveReplicationReplicasOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66353901348b91b995deb46e1e2315cd90cadd3d17ebbb4944374dc7a200a5d2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleFilestoreInstanceEffectiveReplicationReplicasOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c27f27664819d62a633ccdf2049b8d9683b6028aa4b40a2c72b1a92afc70ad7b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__505186d2234bc48eb8b2ca04a66a8e54af878696ce8cce1e68fbcd16e1126b9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__916ca734e9f274d607fdbced0a521a4288399654400610d6d768b6aebb429dae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleFilestoreInstanceEffectiveReplicationReplicasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceEffectiveReplicationReplicasOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bdf5b922a4ab31ff6b54a626a4edbf832077f6e03da50e198b115b2eeec6c55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="lastActiveSyncTime")
    def last_active_sync_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastActiveSyncTime"))

    @builtins.property
    @jsii.member(jsii_name="peerInstance")
    def peer_instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerInstance"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateReasons")
    def state_reasons(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stateReasons"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleFilestoreInstanceEffectiveReplicationReplicas]:
        return typing.cast(typing.Optional[GoogleFilestoreInstanceEffectiveReplicationReplicas], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleFilestoreInstanceEffectiveReplicationReplicas],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dfe0da378f15881effa4a8ecbdf392cdc9d75dcfa73abef01ebda78d4d81804)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceFileShares",
    jsii_struct_bases=[],
    name_mapping={
        "capacity_gb": "capacityGb",
        "name": "name",
        "nfs_export_options": "nfsExportOptions",
        "source_backup": "sourceBackup",
    },
)
class GoogleFilestoreInstanceFileShares:
    def __init__(
        self,
        *,
        capacity_gb: jsii.Number,
        name: builtins.str,
        nfs_export_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleFilestoreInstanceFileSharesNfsExportOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        source_backup: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param capacity_gb: File share capacity in GiB. This must be at least 1024 GiB for the standard tier, or 2560 GiB for the premium tier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#capacity_gb GoogleFilestoreInstance#capacity_gb}
        :param name: The name of the fileshare (16 characters or less). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#name GoogleFilestoreInstance#name}
        :param nfs_export_options: nfs_export_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#nfs_export_options GoogleFilestoreInstance#nfs_export_options}
        :param source_backup: The resource name of the backup, in the format projects/{projectId}/locations/{locationId}/backups/{backupId}, that this file share has been restored from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#source_backup GoogleFilestoreInstance#source_backup}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd57291f3d705664db7ec150a663f07f191bbace866871f9d04be783ae2c7758)
            check_type(argname="argument capacity_gb", value=capacity_gb, expected_type=type_hints["capacity_gb"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument nfs_export_options", value=nfs_export_options, expected_type=type_hints["nfs_export_options"])
            check_type(argname="argument source_backup", value=source_backup, expected_type=type_hints["source_backup"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capacity_gb": capacity_gb,
            "name": name,
        }
        if nfs_export_options is not None:
            self._values["nfs_export_options"] = nfs_export_options
        if source_backup is not None:
            self._values["source_backup"] = source_backup

    @builtins.property
    def capacity_gb(self) -> jsii.Number:
        '''File share capacity in GiB.

        This must be at least 1024 GiB
        for the standard tier, or 2560 GiB for the premium tier.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#capacity_gb GoogleFilestoreInstance#capacity_gb}
        '''
        result = self._values.get("capacity_gb")
        assert result is not None, "Required property 'capacity_gb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the fileshare (16 characters or less).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#name GoogleFilestoreInstance#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def nfs_export_options(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleFilestoreInstanceFileSharesNfsExportOptions"]]]:
        '''nfs_export_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#nfs_export_options GoogleFilestoreInstance#nfs_export_options}
        '''
        result = self._values.get("nfs_export_options")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleFilestoreInstanceFileSharesNfsExportOptions"]]], result)

    @builtins.property
    def source_backup(self) -> typing.Optional[builtins.str]:
        '''The resource name of the backup, in the format projects/{projectId}/locations/{locationId}/backups/{backupId}, that this file share has been restored from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#source_backup GoogleFilestoreInstance#source_backup}
        '''
        result = self._values.get("source_backup")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleFilestoreInstanceFileShares(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceFileSharesNfsExportOptions",
    jsii_struct_bases=[],
    name_mapping={
        "access_mode": "accessMode",
        "anon_gid": "anonGid",
        "anon_uid": "anonUid",
        "ip_ranges": "ipRanges",
        "network": "network",
        "squash_mode": "squashMode",
    },
)
class GoogleFilestoreInstanceFileSharesNfsExportOptions:
    def __init__(
        self,
        *,
        access_mode: typing.Optional[builtins.str] = None,
        anon_gid: typing.Optional[jsii.Number] = None,
        anon_uid: typing.Optional[jsii.Number] = None,
        ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        network: typing.Optional[builtins.str] = None,
        squash_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_mode: Either READ_ONLY, for allowing only read requests on the exported directory, or READ_WRITE, for allowing both read and write requests. The default is READ_WRITE. Default value: "READ_WRITE" Possible values: ["READ_ONLY", "READ_WRITE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#access_mode GoogleFilestoreInstance#access_mode}
        :param anon_gid: An integer representing the anonymous group id with a default value of 65534. Anon_gid may only be set with squashMode of ROOT_SQUASH. An error will be returned if this field is specified for other squashMode settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#anon_gid GoogleFilestoreInstance#anon_gid}
        :param anon_uid: An integer representing the anonymous user id with a default value of 65534. Anon_uid may only be set with squashMode of ROOT_SQUASH. An error will be returned if this field is specified for other squashMode settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#anon_uid GoogleFilestoreInstance#anon_uid}
        :param ip_ranges: List of either IPv4 addresses, or ranges in CIDR notation which may mount the file share. Overlapping IP ranges are not allowed, both within and across NfsExportOptions. An error will be returned. The limit is 64 IP ranges/addresses for each FileShareConfig among all NfsExportOptions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#ip_ranges GoogleFilestoreInstance#ip_ranges}
        :param network: The source VPC network for 'ip_ranges'. Required for instances using Private Service Connect, optional otherwise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#network GoogleFilestoreInstance#network}
        :param squash_mode: Either NO_ROOT_SQUASH, for allowing root access on the exported directory, or ROOT_SQUASH, for not allowing root access. The default is NO_ROOT_SQUASH. Default value: "NO_ROOT_SQUASH" Possible values: ["NO_ROOT_SQUASH", "ROOT_SQUASH"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#squash_mode GoogleFilestoreInstance#squash_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3ad3b6df0273fa42ecd7aca1287c4bbdba091ac981e7762a6a7bb037ffd253a)
            check_type(argname="argument access_mode", value=access_mode, expected_type=type_hints["access_mode"])
            check_type(argname="argument anon_gid", value=anon_gid, expected_type=type_hints["anon_gid"])
            check_type(argname="argument anon_uid", value=anon_uid, expected_type=type_hints["anon_uid"])
            check_type(argname="argument ip_ranges", value=ip_ranges, expected_type=type_hints["ip_ranges"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument squash_mode", value=squash_mode, expected_type=type_hints["squash_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_mode is not None:
            self._values["access_mode"] = access_mode
        if anon_gid is not None:
            self._values["anon_gid"] = anon_gid
        if anon_uid is not None:
            self._values["anon_uid"] = anon_uid
        if ip_ranges is not None:
            self._values["ip_ranges"] = ip_ranges
        if network is not None:
            self._values["network"] = network
        if squash_mode is not None:
            self._values["squash_mode"] = squash_mode

    @builtins.property
    def access_mode(self) -> typing.Optional[builtins.str]:
        '''Either READ_ONLY, for allowing only read requests on the exported directory, or READ_WRITE, for allowing both read and write requests.

        The default is READ_WRITE. Default value: "READ_WRITE" Possible values: ["READ_ONLY", "READ_WRITE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#access_mode GoogleFilestoreInstance#access_mode}
        '''
        result = self._values.get("access_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def anon_gid(self) -> typing.Optional[jsii.Number]:
        '''An integer representing the anonymous group id with a default value of 65534.

        Anon_gid may only be set with squashMode of ROOT_SQUASH. An error will be returned
        if this field is specified for other squashMode settings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#anon_gid GoogleFilestoreInstance#anon_gid}
        '''
        result = self._values.get("anon_gid")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def anon_uid(self) -> typing.Optional[jsii.Number]:
        '''An integer representing the anonymous user id with a default value of 65534.

        Anon_uid may only be set with squashMode of ROOT_SQUASH. An error will be returned
        if this field is specified for other squashMode settings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#anon_uid GoogleFilestoreInstance#anon_uid}
        '''
        result = self._values.get("anon_uid")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of either IPv4 addresses, or ranges in CIDR notation which may mount the file share.

        Overlapping IP ranges are not allowed, both within and across NfsExportOptions. An error will be returned.
        The limit is 64 IP ranges/addresses for each FileShareConfig among all NfsExportOptions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#ip_ranges GoogleFilestoreInstance#ip_ranges}
        '''
        result = self._values.get("ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The source VPC network for 'ip_ranges'. Required for instances using Private Service Connect, optional otherwise.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#network GoogleFilestoreInstance#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def squash_mode(self) -> typing.Optional[builtins.str]:
        '''Either NO_ROOT_SQUASH, for allowing root access on the exported directory, or ROOT_SQUASH, for not allowing root access.

        The default is NO_ROOT_SQUASH. Default value: "NO_ROOT_SQUASH" Possible values: ["NO_ROOT_SQUASH", "ROOT_SQUASH"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#squash_mode GoogleFilestoreInstance#squash_mode}
        '''
        result = self._values.get("squash_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleFilestoreInstanceFileSharesNfsExportOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleFilestoreInstanceFileSharesNfsExportOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceFileSharesNfsExportOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c8f6ee2b21b6cbe93fd02a5ffdadec17b1b04a3804decc4900e95b9fab14f98)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleFilestoreInstanceFileSharesNfsExportOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__882616ff5c669bc729f1db97916c0f059bb3cf1e225a8ba661b6443a7242a6bc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleFilestoreInstanceFileSharesNfsExportOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d62bdce834be709bae4ce67a5e51e4ec92ca1f271ed160a76f5937e324969c1d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c647f72f0a160232dfb63dff6ea95847b2fbdd10789d2eca54adef48b95aa1af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__034f4ff85d58eda4036a0ef6eabaed78878cea747a3400f801871641710952a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFilestoreInstanceFileSharesNfsExportOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFilestoreInstanceFileSharesNfsExportOptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFilestoreInstanceFileSharesNfsExportOptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f1a6673344f655b1ac8abf977931949d9522d49d38222bf7ed8799faf6c0e98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleFilestoreInstanceFileSharesNfsExportOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceFileSharesNfsExportOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8e87baaf6684b6ad8d7e6b6d91fdcbe23cc67e4e94c4806c7c3dd275bd28c04)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccessMode")
    def reset_access_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessMode", []))

    @jsii.member(jsii_name="resetAnonGid")
    def reset_anon_gid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnonGid", []))

    @jsii.member(jsii_name="resetAnonUid")
    def reset_anon_uid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnonUid", []))

    @jsii.member(jsii_name="resetIpRanges")
    def reset_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpRanges", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetSquashMode")
    def reset_squash_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSquashMode", []))

    @builtins.property
    @jsii.member(jsii_name="accessModeInput")
    def access_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessModeInput"))

    @builtins.property
    @jsii.member(jsii_name="anonGidInput")
    def anon_gid_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "anonGidInput"))

    @builtins.property
    @jsii.member(jsii_name="anonUidInput")
    def anon_uid_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "anonUidInput"))

    @builtins.property
    @jsii.member(jsii_name="ipRangesInput")
    def ip_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="squashModeInput")
    def squash_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "squashModeInput"))

    @builtins.property
    @jsii.member(jsii_name="accessMode")
    def access_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessMode"))

    @access_mode.setter
    def access_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aa8ec6064405b4b60ab1b293d6cb61d63c4dd6a1a15b046b279ce9fe7bd9f5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="anonGid")
    def anon_gid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "anonGid"))

    @anon_gid.setter
    def anon_gid(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6286ff150543ef723de6d9e5c0d0a1bc61860eb2160ac52408bdde4c70ea065a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "anonGid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="anonUid")
    def anon_uid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "anonUid"))

    @anon_uid.setter
    def anon_uid(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d27ab4c6b8830c2d0bf8b7010902355175b69a1385ef0dd529619c376fd951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "anonUid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipRanges")
    def ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipRanges"))

    @ip_ranges.setter
    def ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a458c43141713ac260ac7f40a9a8a8db63fee5376f49c09fb219b1dc93d915b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71d2bcfe85da366b53c7949dcdac6528bd188eca49a337080fb3ec6792bb29e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="squashMode")
    def squash_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "squashMode"))

    @squash_mode.setter
    def squash_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c91037cae3be225e119f5c0d287416bec93ff5ff70b34699845a43ef060ff23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "squashMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFilestoreInstanceFileSharesNfsExportOptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFilestoreInstanceFileSharesNfsExportOptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFilestoreInstanceFileSharesNfsExportOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__670d35be3d722ca3ec185cd455d671e158659f64f07e02781f0cb1437347c5b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleFilestoreInstanceFileSharesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceFileSharesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6956da7957dfc6df9c7331051fbe251d91a1caf3a58a251fd75d563a1705ef05)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNfsExportOptions")
    def put_nfs_export_options(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleFilestoreInstanceFileSharesNfsExportOptions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__230641751f771a9bb769c490e983c8d432027671f8ed6028c8553c454caba0dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNfsExportOptions", [value]))

    @jsii.member(jsii_name="resetNfsExportOptions")
    def reset_nfs_export_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNfsExportOptions", []))

    @jsii.member(jsii_name="resetSourceBackup")
    def reset_source_backup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceBackup", []))

    @builtins.property
    @jsii.member(jsii_name="nfsExportOptions")
    def nfs_export_options(
        self,
    ) -> GoogleFilestoreInstanceFileSharesNfsExportOptionsList:
        return typing.cast(GoogleFilestoreInstanceFileSharesNfsExportOptionsList, jsii.get(self, "nfsExportOptions"))

    @builtins.property
    @jsii.member(jsii_name="capacityGbInput")
    def capacity_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "capacityGbInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nfsExportOptionsInput")
    def nfs_export_options_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFilestoreInstanceFileSharesNfsExportOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFilestoreInstanceFileSharesNfsExportOptions]]], jsii.get(self, "nfsExportOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceBackupInput")
    def source_backup_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceBackupInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityGb")
    def capacity_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "capacityGb"))

    @capacity_gb.setter
    def capacity_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73598b957e39afee40caf98288d11569e0634e47a85ff5fdf13e6b677b873549)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25c3abeb1698a85173e525b2242cbb16656e303480fac4d2a0c1e5eb2531387f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceBackup")
    def source_backup(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceBackup"))

    @source_backup.setter
    def source_backup(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb49770ac3bd7b5b1a0733c1b7b2c7c86dd6c596c1fa27e524a4518dad347bf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceBackup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleFilestoreInstanceFileShares]:
        return typing.cast(typing.Optional[GoogleFilestoreInstanceFileShares], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleFilestoreInstanceFileShares],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aaf87371e96401c65d164c93a76f6ddb3d908ac25238522abf338307db55162)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceInitialReplication",
    jsii_struct_bases=[],
    name_mapping={"replicas": "replicas", "role": "role"},
)
class GoogleFilestoreInstanceInitialReplication:
    def __init__(
        self,
        *,
        replicas: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleFilestoreInstanceInitialReplicationReplicas", typing.Dict[builtins.str, typing.Any]]]]] = None,
        role: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param replicas: replicas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#replicas GoogleFilestoreInstance#replicas}
        :param role: The replication role. Default value: "STANDBY" Possible values: ["ROLE_UNSPECIFIED", "ACTIVE", "STANDBY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#role GoogleFilestoreInstance#role}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db86139f6a820519776aca30a5d0630718109da84f7b7ef4870cf8629d61e1cf)
            check_type(argname="argument replicas", value=replicas, expected_type=type_hints["replicas"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if replicas is not None:
            self._values["replicas"] = replicas
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def replicas(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleFilestoreInstanceInitialReplicationReplicas"]]]:
        '''replicas block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#replicas GoogleFilestoreInstance#replicas}
        '''
        result = self._values.get("replicas")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleFilestoreInstanceInitialReplicationReplicas"]]], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''The replication role. Default value: "STANDBY" Possible values: ["ROLE_UNSPECIFIED", "ACTIVE", "STANDBY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#role GoogleFilestoreInstance#role}
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleFilestoreInstanceInitialReplication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleFilestoreInstanceInitialReplicationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceInitialReplicationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e2958e2c1e82045c4d18c83678473ffac815dd1cd029c5aa4daaecad36c2eef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putReplicas")
    def put_replicas(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleFilestoreInstanceInitialReplicationReplicas", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a281313cd05137de1047adca3102f58bd3bcc73929097d8fb1971cab5e41abd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putReplicas", [value]))

    @jsii.member(jsii_name="resetReplicas")
    def reset_replicas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicas", []))

    @jsii.member(jsii_name="resetRole")
    def reset_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRole", []))

    @builtins.property
    @jsii.member(jsii_name="replicas")
    def replicas(self) -> "GoogleFilestoreInstanceInitialReplicationReplicasList":
        return typing.cast("GoogleFilestoreInstanceInitialReplicationReplicasList", jsii.get(self, "replicas"))

    @builtins.property
    @jsii.member(jsii_name="replicasInput")
    def replicas_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleFilestoreInstanceInitialReplicationReplicas"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleFilestoreInstanceInitialReplicationReplicas"]]], jsii.get(self, "replicasInput"))

    @builtins.property
    @jsii.member(jsii_name="roleInput")
    def role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleInput"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08dd0c50ed092cd6fff0ad24764ada99120a6389b4799d724e3a5b9942090990)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleFilestoreInstanceInitialReplication]:
        return typing.cast(typing.Optional[GoogleFilestoreInstanceInitialReplication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleFilestoreInstanceInitialReplication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__316f7786d75e8e282bcabb552a95036650713e8b08f3fd82b4c8b606af6133e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceInitialReplicationReplicas",
    jsii_struct_bases=[],
    name_mapping={"peer_instance": "peerInstance"},
)
class GoogleFilestoreInstanceInitialReplicationReplicas:
    def __init__(self, *, peer_instance: builtins.str) -> None:
        '''
        :param peer_instance: The peer instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#peer_instance GoogleFilestoreInstance#peer_instance}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32c6b1b5c840baec113e1d0063b3ef05e7fcb84ff2d33268c6c7c4eac2dd861f)
            check_type(argname="argument peer_instance", value=peer_instance, expected_type=type_hints["peer_instance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "peer_instance": peer_instance,
        }

    @builtins.property
    def peer_instance(self) -> builtins.str:
        '''The peer instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#peer_instance GoogleFilestoreInstance#peer_instance}
        '''
        result = self._values.get("peer_instance")
        assert result is not None, "Required property 'peer_instance' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleFilestoreInstanceInitialReplicationReplicas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleFilestoreInstanceInitialReplicationReplicasList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceInitialReplicationReplicasList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4355504253dae7ffdb39944a7226cfdfe0ec3d148f0c1dfbc02ab5ffcc3e7276)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleFilestoreInstanceInitialReplicationReplicasOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71fd2a51524a114f313dd793edc41b05f1ca0983e1b7cf7367b62404219c08c5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleFilestoreInstanceInitialReplicationReplicasOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85b53b8617567fef53f81153403cb0d41c396ac1fd8b05276e6f7198fe8384fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d55d14509b90398d30803e495795c393449ab4336035bd8d87aa19d4d78bf65)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0549e4907ffeffb0cdb420e2ec6a13d125e8a2cdd9614d7889fa99dcde449855)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFilestoreInstanceInitialReplicationReplicas]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFilestoreInstanceInitialReplicationReplicas]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFilestoreInstanceInitialReplicationReplicas]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d77a4eb9e292cf609ad3af7ed6d6ab97c907393555e345bf98ebc327875a8904)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleFilestoreInstanceInitialReplicationReplicasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceInitialReplicationReplicasOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97742ae79d5ddd928deb0309826b7c511adf1605d7b7e38c1a76da3ebadc7f08)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="peerInstanceInput")
    def peer_instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="peerInstance")
    def peer_instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerInstance"))

    @peer_instance.setter
    def peer_instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0724cf9b7303a04883c5960f7b1929c2d5b43a86be0dbea61a2c7b33775221e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFilestoreInstanceInitialReplicationReplicas]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFilestoreInstanceInitialReplicationReplicas]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFilestoreInstanceInitialReplicationReplicas]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f4b3658c089bdae0ca8dac978d11d6a2821cebe4e2f34ed1c21ad92e3cf39cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceNetworks",
    jsii_struct_bases=[],
    name_mapping={
        "modes": "modes",
        "network": "network",
        "connect_mode": "connectMode",
        "psc_config": "pscConfig",
        "reserved_ip_range": "reservedIpRange",
    },
)
class GoogleFilestoreInstanceNetworks:
    def __init__(
        self,
        *,
        modes: typing.Sequence[builtins.str],
        network: builtins.str,
        connect_mode: typing.Optional[builtins.str] = None,
        psc_config: typing.Optional[typing.Union["GoogleFilestoreInstanceNetworksPscConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        reserved_ip_range: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param modes: IP versions for which the instance has IP addresses assigned. Possible values: ["ADDRESS_MODE_UNSPECIFIED", "MODE_IPV4", "MODE_IPV6"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#modes GoogleFilestoreInstance#modes}
        :param network: The name of the GCE VPC network to which the instance is connected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#network GoogleFilestoreInstance#network}
        :param connect_mode: The network connect mode of the Filestore instance. If not provided, the connect mode defaults to DIRECT_PEERING. Default value: "DIRECT_PEERING" Possible values: ["DIRECT_PEERING", "PRIVATE_SERVICE_ACCESS", "PRIVATE_SERVICE_CONNECT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#connect_mode GoogleFilestoreInstance#connect_mode}
        :param psc_config: psc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#psc_config GoogleFilestoreInstance#psc_config}
        :param reserved_ip_range: A /29 CIDR block that identifies the range of IP addresses reserved for this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#reserved_ip_range GoogleFilestoreInstance#reserved_ip_range}
        '''
        if isinstance(psc_config, dict):
            psc_config = GoogleFilestoreInstanceNetworksPscConfig(**psc_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d6b28b943f20a0b6b30fa7802d80b2a76c0470ac3ad71e48b2b5db34c53465b)
            check_type(argname="argument modes", value=modes, expected_type=type_hints["modes"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument connect_mode", value=connect_mode, expected_type=type_hints["connect_mode"])
            check_type(argname="argument psc_config", value=psc_config, expected_type=type_hints["psc_config"])
            check_type(argname="argument reserved_ip_range", value=reserved_ip_range, expected_type=type_hints["reserved_ip_range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "modes": modes,
            "network": network,
        }
        if connect_mode is not None:
            self._values["connect_mode"] = connect_mode
        if psc_config is not None:
            self._values["psc_config"] = psc_config
        if reserved_ip_range is not None:
            self._values["reserved_ip_range"] = reserved_ip_range

    @builtins.property
    def modes(self) -> typing.List[builtins.str]:
        '''IP versions for which the instance has IP addresses assigned. Possible values: ["ADDRESS_MODE_UNSPECIFIED", "MODE_IPV4", "MODE_IPV6"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#modes GoogleFilestoreInstance#modes}
        '''
        result = self._values.get("modes")
        assert result is not None, "Required property 'modes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def network(self) -> builtins.str:
        '''The name of the GCE VPC network to which the instance is connected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#network GoogleFilestoreInstance#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connect_mode(self) -> typing.Optional[builtins.str]:
        '''The network connect mode of the Filestore instance.

        If not provided, the connect mode defaults to
        DIRECT_PEERING. Default value: "DIRECT_PEERING" Possible values: ["DIRECT_PEERING", "PRIVATE_SERVICE_ACCESS", "PRIVATE_SERVICE_CONNECT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#connect_mode GoogleFilestoreInstance#connect_mode}
        '''
        result = self._values.get("connect_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def psc_config(self) -> typing.Optional["GoogleFilestoreInstanceNetworksPscConfig"]:
        '''psc_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#psc_config GoogleFilestoreInstance#psc_config}
        '''
        result = self._values.get("psc_config")
        return typing.cast(typing.Optional["GoogleFilestoreInstanceNetworksPscConfig"], result)

    @builtins.property
    def reserved_ip_range(self) -> typing.Optional[builtins.str]:
        '''A /29 CIDR block that identifies the range of IP addresses reserved for this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#reserved_ip_range GoogleFilestoreInstance#reserved_ip_range}
        '''
        result = self._values.get("reserved_ip_range")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleFilestoreInstanceNetworks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleFilestoreInstanceNetworksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceNetworksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94efa6dbaa55cc5f23aa57656a6939f90eedc5343eb903c3a7d08efe78dcfc62)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleFilestoreInstanceNetworksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b9d47cabe692bac496767a35196c5c227450433163b3c8cdc4ab1eae14473ed)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleFilestoreInstanceNetworksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bd23800ddb8cc4a10a3cd81345fb8d04f77a7a8c8b354751202a44eb6205e01)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2534565232d3cf507294f373f490c3983b6d8536b34bc6a1cf153febd4433f0d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa5e63cb6c2f6258c662667e5983ec672a7c0e6f2be04e141104e413c9495286)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFilestoreInstanceNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFilestoreInstanceNetworks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFilestoreInstanceNetworks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e82b759b1cc980b855956b3d69f807738bb24246e0448c5e9890493c4424b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleFilestoreInstanceNetworksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceNetworksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4e6973cd3c0424b00b39bec477d7a0d7e905b7deb43bf464b71af9e2672893d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPscConfig")
    def put_psc_config(
        self,
        *,
        endpoint_project: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoint_project: Consumer service project in which the Private Service Connect endpoint would be set up. This is optional, and only relevant in case the network is a shared VPC. If this is not specified, the endpoint would be set up in the VPC host project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#endpoint_project GoogleFilestoreInstance#endpoint_project}
        '''
        value = GoogleFilestoreInstanceNetworksPscConfig(
            endpoint_project=endpoint_project
        )

        return typing.cast(None, jsii.invoke(self, "putPscConfig", [value]))

    @jsii.member(jsii_name="resetConnectMode")
    def reset_connect_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectMode", []))

    @jsii.member(jsii_name="resetPscConfig")
    def reset_psc_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPscConfig", []))

    @jsii.member(jsii_name="resetReservedIpRange")
    def reset_reserved_ip_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservedIpRange", []))

    @builtins.property
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipAddresses"))

    @builtins.property
    @jsii.member(jsii_name="pscConfig")
    def psc_config(self) -> "GoogleFilestoreInstanceNetworksPscConfigOutputReference":
        return typing.cast("GoogleFilestoreInstanceNetworksPscConfigOutputReference", jsii.get(self, "pscConfig"))

    @builtins.property
    @jsii.member(jsii_name="connectModeInput")
    def connect_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectModeInput"))

    @builtins.property
    @jsii.member(jsii_name="modesInput")
    def modes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "modesInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="pscConfigInput")
    def psc_config_input(
        self,
    ) -> typing.Optional["GoogleFilestoreInstanceNetworksPscConfig"]:
        return typing.cast(typing.Optional["GoogleFilestoreInstanceNetworksPscConfig"], jsii.get(self, "pscConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="reservedIpRangeInput")
    def reserved_ip_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reservedIpRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="connectMode")
    def connect_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectMode"))

    @connect_mode.setter
    def connect_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bba3ee1e2e33de959852bff5761505d4bc5996a0517a3e2c6be3535142f71911)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modes")
    def modes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "modes"))

    @modes.setter
    def modes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa60a0b622d5fc66ed48a87fa63fd19e9004922f3883d64e777b8c13a3c36d0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__968608d3fa37252ee5afd506326b38f91cd79133da174bddc002a19901f99cf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reservedIpRange")
    def reserved_ip_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reservedIpRange"))

    @reserved_ip_range.setter
    def reserved_ip_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__820d4756086f34c65d498fa0c18de8c74a686a8443df6eecfc158282dabc0e5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservedIpRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFilestoreInstanceNetworks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFilestoreInstanceNetworks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFilestoreInstanceNetworks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b8f182222a8d02f37bf1981d1f41baf9bf0cf449285e57503f36b5bf6ad1ad2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceNetworksPscConfig",
    jsii_struct_bases=[],
    name_mapping={"endpoint_project": "endpointProject"},
)
class GoogleFilestoreInstanceNetworksPscConfig:
    def __init__(
        self,
        *,
        endpoint_project: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoint_project: Consumer service project in which the Private Service Connect endpoint would be set up. This is optional, and only relevant in case the network is a shared VPC. If this is not specified, the endpoint would be set up in the VPC host project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#endpoint_project GoogleFilestoreInstance#endpoint_project}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fca8337353bc487dad57e09788c417bbe7c43dacb16460e2f9129fe82ce5198)
            check_type(argname="argument endpoint_project", value=endpoint_project, expected_type=type_hints["endpoint_project"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if endpoint_project is not None:
            self._values["endpoint_project"] = endpoint_project

    @builtins.property
    def endpoint_project(self) -> typing.Optional[builtins.str]:
        '''Consumer service project in which the Private Service Connect endpoint would be set up.

        This is optional, and only relevant in case the network
        is a shared VPC. If this is not specified, the endpoint would be set up
        in the VPC host project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#endpoint_project GoogleFilestoreInstance#endpoint_project}
        '''
        result = self._values.get("endpoint_project")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleFilestoreInstanceNetworksPscConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleFilestoreInstanceNetworksPscConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceNetworksPscConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a34fdceee218f35dd2611fafec11a4168585ae39829422375420ed6b1673b5ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEndpointProject")
    def reset_endpoint_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointProject", []))

    @builtins.property
    @jsii.member(jsii_name="endpointProjectInput")
    def endpoint_project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointProjectInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointProject")
    def endpoint_project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointProject"))

    @endpoint_project.setter
    def endpoint_project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24830b65265fc1f9650627fe572581af7ebb765c6b978f2823f466ee229d4b64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointProject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleFilestoreInstanceNetworksPscConfig]:
        return typing.cast(typing.Optional[GoogleFilestoreInstanceNetworksPscConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleFilestoreInstanceNetworksPscConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2124093221d01a3b88c097ecfb310d0fcb1ab5f5ee96892e286022eeae9db4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstancePerformanceConfig",
    jsii_struct_bases=[],
    name_mapping={"fixed_iops": "fixedIops", "iops_per_tb": "iopsPerTb"},
)
class GoogleFilestoreInstancePerformanceConfig:
    def __init__(
        self,
        *,
        fixed_iops: typing.Optional[typing.Union["GoogleFilestoreInstancePerformanceConfigFixedIops", typing.Dict[builtins.str, typing.Any]]] = None,
        iops_per_tb: typing.Optional[typing.Union["GoogleFilestoreInstancePerformanceConfigIopsPerTb", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param fixed_iops: fixed_iops block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#fixed_iops GoogleFilestoreInstance#fixed_iops}
        :param iops_per_tb: iops_per_tb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#iops_per_tb GoogleFilestoreInstance#iops_per_tb}
        '''
        if isinstance(fixed_iops, dict):
            fixed_iops = GoogleFilestoreInstancePerformanceConfigFixedIops(**fixed_iops)
        if isinstance(iops_per_tb, dict):
            iops_per_tb = GoogleFilestoreInstancePerformanceConfigIopsPerTb(**iops_per_tb)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__675caefc2a4cb330e81c65541409bde22ad01f361fb6e103ea1165eec45b9b04)
            check_type(argname="argument fixed_iops", value=fixed_iops, expected_type=type_hints["fixed_iops"])
            check_type(argname="argument iops_per_tb", value=iops_per_tb, expected_type=type_hints["iops_per_tb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fixed_iops is not None:
            self._values["fixed_iops"] = fixed_iops
        if iops_per_tb is not None:
            self._values["iops_per_tb"] = iops_per_tb

    @builtins.property
    def fixed_iops(
        self,
    ) -> typing.Optional["GoogleFilestoreInstancePerformanceConfigFixedIops"]:
        '''fixed_iops block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#fixed_iops GoogleFilestoreInstance#fixed_iops}
        '''
        result = self._values.get("fixed_iops")
        return typing.cast(typing.Optional["GoogleFilestoreInstancePerformanceConfigFixedIops"], result)

    @builtins.property
    def iops_per_tb(
        self,
    ) -> typing.Optional["GoogleFilestoreInstancePerformanceConfigIopsPerTb"]:
        '''iops_per_tb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#iops_per_tb GoogleFilestoreInstance#iops_per_tb}
        '''
        result = self._values.get("iops_per_tb")
        return typing.cast(typing.Optional["GoogleFilestoreInstancePerformanceConfigIopsPerTb"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleFilestoreInstancePerformanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstancePerformanceConfigFixedIops",
    jsii_struct_bases=[],
    name_mapping={"max_iops": "maxIops"},
)
class GoogleFilestoreInstancePerformanceConfigFixedIops:
    def __init__(self, *, max_iops: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param max_iops: The number of IOPS to provision for the instance. max_iops must be in multiple of 1000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#max_iops GoogleFilestoreInstance#max_iops}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bf205d747fd822c2930b08003899ce3ad68554285613266eb80031233569f23)
            check_type(argname="argument max_iops", value=max_iops, expected_type=type_hints["max_iops"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_iops is not None:
            self._values["max_iops"] = max_iops

    @builtins.property
    def max_iops(self) -> typing.Optional[jsii.Number]:
        '''The number of IOPS to provision for the instance. max_iops must be in multiple of 1000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#max_iops GoogleFilestoreInstance#max_iops}
        '''
        result = self._values.get("max_iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleFilestoreInstancePerformanceConfigFixedIops(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleFilestoreInstancePerformanceConfigFixedIopsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstancePerformanceConfigFixedIopsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__589568bd7edac98b8815a505de8329687cb6c74c38c92b7894a1e87539eb2fed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxIops")
    def reset_max_iops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxIops", []))

    @builtins.property
    @jsii.member(jsii_name="maxIopsInput")
    def max_iops_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxIopsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxIops")
    def max_iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIops"))

    @max_iops.setter
    def max_iops(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d73e5f8d82ff94357fa00fdb4bdc55a3de67d270c2d071263c74cf08c6ad165b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIops", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleFilestoreInstancePerformanceConfigFixedIops]:
        return typing.cast(typing.Optional[GoogleFilestoreInstancePerformanceConfigFixedIops], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleFilestoreInstancePerformanceConfigFixedIops],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a765ecd586a500e9b6f101a5503b8b27aba4b35ec7087068d85ff2bfdf3109bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstancePerformanceConfigIopsPerTb",
    jsii_struct_bases=[],
    name_mapping={"max_iops_per_tb": "maxIopsPerTb"},
)
class GoogleFilestoreInstancePerformanceConfigIopsPerTb:
    def __init__(self, *, max_iops_per_tb: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param max_iops_per_tb: The instance max IOPS will be calculated by multiplying the capacity of the instance (TB) by max_iops_per_tb, and rounding to the nearest 1000. The instance max IOPS will be changed dynamically based on the instance capacity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#max_iops_per_tb GoogleFilestoreInstance#max_iops_per_tb}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__848db6b1df0e1e99028deaa977a7de949ac3f81ea01897992ba2839416b10dc2)
            check_type(argname="argument max_iops_per_tb", value=max_iops_per_tb, expected_type=type_hints["max_iops_per_tb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_iops_per_tb is not None:
            self._values["max_iops_per_tb"] = max_iops_per_tb

    @builtins.property
    def max_iops_per_tb(self) -> typing.Optional[jsii.Number]:
        '''The instance max IOPS will be calculated by multiplying the capacity of the instance (TB) by max_iops_per_tb, and rounding to the nearest 1000.

        The instance max IOPS
        will be changed dynamically based on the instance
        capacity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#max_iops_per_tb GoogleFilestoreInstance#max_iops_per_tb}
        '''
        result = self._values.get("max_iops_per_tb")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleFilestoreInstancePerformanceConfigIopsPerTb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleFilestoreInstancePerformanceConfigIopsPerTbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstancePerformanceConfigIopsPerTbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71b12b944f0e24695fecd117138091c4bd907df9cfbb762982a2d072853741d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxIopsPerTb")
    def reset_max_iops_per_tb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxIopsPerTb", []))

    @builtins.property
    @jsii.member(jsii_name="maxIopsPerTbInput")
    def max_iops_per_tb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxIopsPerTbInput"))

    @builtins.property
    @jsii.member(jsii_name="maxIopsPerTb")
    def max_iops_per_tb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIopsPerTb"))

    @max_iops_per_tb.setter
    def max_iops_per_tb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3669028e2d8bfcac52df25f4f8f6b5c6a1dc16bcbee290abbabde88c569466f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIopsPerTb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleFilestoreInstancePerformanceConfigIopsPerTb]:
        return typing.cast(typing.Optional[GoogleFilestoreInstancePerformanceConfigIopsPerTb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleFilestoreInstancePerformanceConfigIopsPerTb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecb6eee1720d32b27846e8ad8eaf667c2b2b7e4d097d96fd9c71a0d3a64de03c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleFilestoreInstancePerformanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstancePerformanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__622457bfd7342bcd55f032b5ce29ce752657c20cede67b4ff317505a65afbf67)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFixedIops")
    def put_fixed_iops(self, *, max_iops: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param max_iops: The number of IOPS to provision for the instance. max_iops must be in multiple of 1000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#max_iops GoogleFilestoreInstance#max_iops}
        '''
        value = GoogleFilestoreInstancePerformanceConfigFixedIops(max_iops=max_iops)

        return typing.cast(None, jsii.invoke(self, "putFixedIops", [value]))

    @jsii.member(jsii_name="putIopsPerTb")
    def put_iops_per_tb(
        self,
        *,
        max_iops_per_tb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_iops_per_tb: The instance max IOPS will be calculated by multiplying the capacity of the instance (TB) by max_iops_per_tb, and rounding to the nearest 1000. The instance max IOPS will be changed dynamically based on the instance capacity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#max_iops_per_tb GoogleFilestoreInstance#max_iops_per_tb}
        '''
        value = GoogleFilestoreInstancePerformanceConfigIopsPerTb(
            max_iops_per_tb=max_iops_per_tb
        )

        return typing.cast(None, jsii.invoke(self, "putIopsPerTb", [value]))

    @jsii.member(jsii_name="resetFixedIops")
    def reset_fixed_iops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedIops", []))

    @jsii.member(jsii_name="resetIopsPerTb")
    def reset_iops_per_tb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIopsPerTb", []))

    @builtins.property
    @jsii.member(jsii_name="fixedIops")
    def fixed_iops(
        self,
    ) -> GoogleFilestoreInstancePerformanceConfigFixedIopsOutputReference:
        return typing.cast(GoogleFilestoreInstancePerformanceConfigFixedIopsOutputReference, jsii.get(self, "fixedIops"))

    @builtins.property
    @jsii.member(jsii_name="iopsPerTb")
    def iops_per_tb(
        self,
    ) -> GoogleFilestoreInstancePerformanceConfigIopsPerTbOutputReference:
        return typing.cast(GoogleFilestoreInstancePerformanceConfigIopsPerTbOutputReference, jsii.get(self, "iopsPerTb"))

    @builtins.property
    @jsii.member(jsii_name="fixedIopsInput")
    def fixed_iops_input(
        self,
    ) -> typing.Optional[GoogleFilestoreInstancePerformanceConfigFixedIops]:
        return typing.cast(typing.Optional[GoogleFilestoreInstancePerformanceConfigFixedIops], jsii.get(self, "fixedIopsInput"))

    @builtins.property
    @jsii.member(jsii_name="iopsPerTbInput")
    def iops_per_tb_input(
        self,
    ) -> typing.Optional[GoogleFilestoreInstancePerformanceConfigIopsPerTb]:
        return typing.cast(typing.Optional[GoogleFilestoreInstancePerformanceConfigIopsPerTb], jsii.get(self, "iopsPerTbInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleFilestoreInstancePerformanceConfig]:
        return typing.cast(typing.Optional[GoogleFilestoreInstancePerformanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleFilestoreInstancePerformanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4449a144cdc6e59864fb960910a7d4279e47ec970a0891aa8e2705040fcebd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleFilestoreInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#create GoogleFilestoreInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#delete GoogleFilestoreInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#update GoogleFilestoreInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1fc068a16b1a3888aa5f00c0d42aba7acd802b1b1e58993f65423f6977fa11a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#create GoogleFilestoreInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#delete GoogleFilestoreInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_filestore_instance#update GoogleFilestoreInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleFilestoreInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleFilestoreInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFilestoreInstance.GoogleFilestoreInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__966e39354be18db153021cf3133b3fe5aa7e89134e203e45fbe237c68fa926f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4f64f75b4fe732c28b16f050090e27c2fbc5a27f9891afcd178092d3d8ba228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a5b7e3e0cb5ddb27385ed5a35022d41fa378c35ae77e911c8097be8d92a97d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be23136e9105e02cd984ade10a9fe845027b716e4e65563ef9f142eede32d476)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFilestoreInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFilestoreInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFilestoreInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eea970d8c6c2f02a046088ab652387753d9c1e98badfc5a0740ca277f8bf317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleFilestoreInstance",
    "GoogleFilestoreInstanceConfig",
    "GoogleFilestoreInstanceDirectoryServices",
    "GoogleFilestoreInstanceDirectoryServicesLdap",
    "GoogleFilestoreInstanceDirectoryServicesLdapOutputReference",
    "GoogleFilestoreInstanceDirectoryServicesOutputReference",
    "GoogleFilestoreInstanceEffectiveReplication",
    "GoogleFilestoreInstanceEffectiveReplicationList",
    "GoogleFilestoreInstanceEffectiveReplicationOutputReference",
    "GoogleFilestoreInstanceEffectiveReplicationReplicas",
    "GoogleFilestoreInstanceEffectiveReplicationReplicasList",
    "GoogleFilestoreInstanceEffectiveReplicationReplicasOutputReference",
    "GoogleFilestoreInstanceFileShares",
    "GoogleFilestoreInstanceFileSharesNfsExportOptions",
    "GoogleFilestoreInstanceFileSharesNfsExportOptionsList",
    "GoogleFilestoreInstanceFileSharesNfsExportOptionsOutputReference",
    "GoogleFilestoreInstanceFileSharesOutputReference",
    "GoogleFilestoreInstanceInitialReplication",
    "GoogleFilestoreInstanceInitialReplicationOutputReference",
    "GoogleFilestoreInstanceInitialReplicationReplicas",
    "GoogleFilestoreInstanceInitialReplicationReplicasList",
    "GoogleFilestoreInstanceInitialReplicationReplicasOutputReference",
    "GoogleFilestoreInstanceNetworks",
    "GoogleFilestoreInstanceNetworksList",
    "GoogleFilestoreInstanceNetworksOutputReference",
    "GoogleFilestoreInstanceNetworksPscConfig",
    "GoogleFilestoreInstanceNetworksPscConfigOutputReference",
    "GoogleFilestoreInstancePerformanceConfig",
    "GoogleFilestoreInstancePerformanceConfigFixedIops",
    "GoogleFilestoreInstancePerformanceConfigFixedIopsOutputReference",
    "GoogleFilestoreInstancePerformanceConfigIopsPerTb",
    "GoogleFilestoreInstancePerformanceConfigIopsPerTbOutputReference",
    "GoogleFilestoreInstancePerformanceConfigOutputReference",
    "GoogleFilestoreInstanceTimeouts",
    "GoogleFilestoreInstanceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b88457e3785dc7c40547af5ea963a8ee18c32cbef9ed8cb998c83852d7336614(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    file_shares: typing.Union[GoogleFilestoreInstanceFileShares, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    networks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleFilestoreInstanceNetworks, typing.Dict[builtins.str, typing.Any]]]],
    tier: builtins.str,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deletion_protection_reason: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    directory_services: typing.Optional[typing.Union[GoogleFilestoreInstanceDirectoryServices, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    initial_replication: typing.Optional[typing.Union[GoogleFilestoreInstanceInitialReplication, typing.Dict[builtins.str, typing.Any]]] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    performance_config: typing.Optional[typing.Union[GoogleFilestoreInstancePerformanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[GoogleFilestoreInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zone: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__4f1a678fc2d9a5ca3d302cbe7b6576694f69394b3479964886db420c5c7853ab(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2766c9e3eef010c8e2797456727f62e87c689f23ff02f545fecb06278b48c344(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleFilestoreInstanceNetworks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f398ff0d6e16d37ff41f4436acd0603787f9854694ac0434a738550a855eb7b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bfdf217a6640246c00e06488b197e447f944c650bfb38fc9d5122f675fa1afb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9d9b9317e7c03eda0dce30cce8c6133fdda43315cb461aebdca8b76fdfe29dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd5b7483fb48b92ed1a45db429c5d53f2a9cad3cce52dcf294c2a7f46a0f2e67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3efbcbd036ba0b66c2251f6664a0e0f2e9f3b17319770725711ae9d889afd155(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fdf6437646652124173290788239e65103c1b702ef5668d051de96654e861ea(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3b5f7c9736bccbb786865c93cb53377a240ddf40bb5aa9eb1ee05d127870cda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__418b9835a028fbb374bdd586668a3612a9e9bbb5ad4c0a1f532879e36cb0b643(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b87f464c5a9ca070bd7a76a15f70a49ae0b9ad4fb3494d10f64a2fd35fd12756(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ca098cc6fb6e57238ffe0841f67bb8a9205a39b2351fb97f0998b819e038c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__143b64321db8ecb8f24bf46d508f09f1df1188e17046de48f571ffca77840887(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eda75fff777e34779bc68d69fa8c1fe5516381567bf5638316be18e499a664a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aea818df78c7e3cf9aac1ce6701866d1aab49d62aa958d14c6c3d7c5ee97d5a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2a8debe325b213b7082dbefdfda63ff26e1e95c390e3c7359b96b44919a15a8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    file_shares: typing.Union[GoogleFilestoreInstanceFileShares, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    networks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleFilestoreInstanceNetworks, typing.Dict[builtins.str, typing.Any]]]],
    tier: builtins.str,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deletion_protection_reason: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    directory_services: typing.Optional[typing.Union[GoogleFilestoreInstanceDirectoryServices, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    initial_replication: typing.Optional[typing.Union[GoogleFilestoreInstanceInitialReplication, typing.Dict[builtins.str, typing.Any]]] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    performance_config: typing.Optional[typing.Union[GoogleFilestoreInstancePerformanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[GoogleFilestoreInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f218b4dc7d64415c1fd555512268b0aa7faa76164a4aef692f04637a26a7899c(
    *,
    ldap: typing.Optional[typing.Union[GoogleFilestoreInstanceDirectoryServicesLdap, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12208d29c8fa8861e20f859b6303968815a949a81083a44e01932601bf350554(
    *,
    domain: builtins.str,
    servers: typing.Sequence[builtins.str],
    groups_ou: typing.Optional[builtins.str] = None,
    users_ou: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40da28da8d00c77e21454bff3cd64977a737be73e9549ec429c806b91e2b8e76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d696c3cbe7034d69a62c0ee30a3362ea94410b56bd12a40fb4376a75da34e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71b216cef9144dfe5b58f1d8a4fa261fcb54689b0006604dc732803e1d1623aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__754606bd8b005676d1bc640267ca64042a9264e0ebd5d87923405981f23d70d0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de9046de0c050dc826f46258baa17cbdcf00968159add239950d76dd9f5ad5f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8dfaec4727babc01f6092778fd93cdf178df990b527382b497b5aa5fddd9bdd(
    value: typing.Optional[GoogleFilestoreInstanceDirectoryServicesLdap],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa8ac2831803231ad7a94c38e1f3fc76ebf7f12a3dfb2724feb994e50d893139(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4720f08135e64ea0a8729e2667307b934cc6e7a504ca964e5f233d7eaed4fc26(
    value: typing.Optional[GoogleFilestoreInstanceDirectoryServices],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8118820eed4a700d002d16dfe1c9a2f479ba7fb8a8e500b751fcd33f2f59bee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d524284a361ec74c152c8ba27820897f408a984942ec2cd8ca478bccd5e8d9fe(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05fc395f88ba059598751216a65165407e509bb83f241ee9ce1470a743c0e7ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6808f51ee3a28f0483b656796da2e2ea8cc5eeaa66c6400e3288905d06ecac99(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa038b1feedb6626f6322b5a6e3530e0ce44cb4d7de72458831ee5eb745dbb45(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__697f9a4c958ecf1056d793fe43301b6cbfd8d34fb5f4fd3cb4e9e628c51c56f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b528ede62aa841672d02f7fdf2b94d847f7e8380a69b5c647c96600247c54ec(
    value: typing.Optional[GoogleFilestoreInstanceEffectiveReplication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27ed76cb65ea7a9d8788d25d90a2a67b0a24c6e96aa6d49704754b9fd0567473(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66353901348b91b995deb46e1e2315cd90cadd3d17ebbb4944374dc7a200a5d2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c27f27664819d62a633ccdf2049b8d9683b6028aa4b40a2c72b1a92afc70ad7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__505186d2234bc48eb8b2ca04a66a8e54af878696ce8cce1e68fbcd16e1126b9e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__916ca734e9f274d607fdbced0a521a4288399654400610d6d768b6aebb429dae(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bdf5b922a4ab31ff6b54a626a4edbf832077f6e03da50e198b115b2eeec6c55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dfe0da378f15881effa4a8ecbdf392cdc9d75dcfa73abef01ebda78d4d81804(
    value: typing.Optional[GoogleFilestoreInstanceEffectiveReplicationReplicas],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd57291f3d705664db7ec150a663f07f191bbace866871f9d04be783ae2c7758(
    *,
    capacity_gb: jsii.Number,
    name: builtins.str,
    nfs_export_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleFilestoreInstanceFileSharesNfsExportOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    source_backup: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3ad3b6df0273fa42ecd7aca1287c4bbdba091ac981e7762a6a7bb037ffd253a(
    *,
    access_mode: typing.Optional[builtins.str] = None,
    anon_gid: typing.Optional[jsii.Number] = None,
    anon_uid: typing.Optional[jsii.Number] = None,
    ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    network: typing.Optional[builtins.str] = None,
    squash_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c8f6ee2b21b6cbe93fd02a5ffdadec17b1b04a3804decc4900e95b9fab14f98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882616ff5c669bc729f1db97916c0f059bb3cf1e225a8ba661b6443a7242a6bc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d62bdce834be709bae4ce67a5e51e4ec92ca1f271ed160a76f5937e324969c1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c647f72f0a160232dfb63dff6ea95847b2fbdd10789d2eca54adef48b95aa1af(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__034f4ff85d58eda4036a0ef6eabaed78878cea747a3400f801871641710952a7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f1a6673344f655b1ac8abf977931949d9522d49d38222bf7ed8799faf6c0e98(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFilestoreInstanceFileSharesNfsExportOptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e87baaf6684b6ad8d7e6b6d91fdcbe23cc67e4e94c4806c7c3dd275bd28c04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa8ec6064405b4b60ab1b293d6cb61d63c4dd6a1a15b046b279ce9fe7bd9f5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6286ff150543ef723de6d9e5c0d0a1bc61860eb2160ac52408bdde4c70ea065a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d27ab4c6b8830c2d0bf8b7010902355175b69a1385ef0dd529619c376fd951(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a458c43141713ac260ac7f40a9a8a8db63fee5376f49c09fb219b1dc93d915b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71d2bcfe85da366b53c7949dcdac6528bd188eca49a337080fb3ec6792bb29e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c91037cae3be225e119f5c0d287416bec93ff5ff70b34699845a43ef060ff23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__670d35be3d722ca3ec185cd455d671e158659f64f07e02781f0cb1437347c5b5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFilestoreInstanceFileSharesNfsExportOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6956da7957dfc6df9c7331051fbe251d91a1caf3a58a251fd75d563a1705ef05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230641751f771a9bb769c490e983c8d432027671f8ed6028c8553c454caba0dd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleFilestoreInstanceFileSharesNfsExportOptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73598b957e39afee40caf98288d11569e0634e47a85ff5fdf13e6b677b873549(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25c3abeb1698a85173e525b2242cbb16656e303480fac4d2a0c1e5eb2531387f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb49770ac3bd7b5b1a0733c1b7b2c7c86dd6c596c1fa27e524a4518dad347bf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aaf87371e96401c65d164c93a76f6ddb3d908ac25238522abf338307db55162(
    value: typing.Optional[GoogleFilestoreInstanceFileShares],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db86139f6a820519776aca30a5d0630718109da84f7b7ef4870cf8629d61e1cf(
    *,
    replicas: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleFilestoreInstanceInitialReplicationReplicas, typing.Dict[builtins.str, typing.Any]]]]] = None,
    role: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e2958e2c1e82045c4d18c83678473ffac815dd1cd029c5aa4daaecad36c2eef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a281313cd05137de1047adca3102f58bd3bcc73929097d8fb1971cab5e41abd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleFilestoreInstanceInitialReplicationReplicas, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08dd0c50ed092cd6fff0ad24764ada99120a6389b4799d724e3a5b9942090990(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316f7786d75e8e282bcabb552a95036650713e8b08f3fd82b4c8b606af6133e8(
    value: typing.Optional[GoogleFilestoreInstanceInitialReplication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32c6b1b5c840baec113e1d0063b3ef05e7fcb84ff2d33268c6c7c4eac2dd861f(
    *,
    peer_instance: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4355504253dae7ffdb39944a7226cfdfe0ec3d148f0c1dfbc02ab5ffcc3e7276(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71fd2a51524a114f313dd793edc41b05f1ca0983e1b7cf7367b62404219c08c5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b53b8617567fef53f81153403cb0d41c396ac1fd8b05276e6f7198fe8384fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d55d14509b90398d30803e495795c393449ab4336035bd8d87aa19d4d78bf65(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0549e4907ffeffb0cdb420e2ec6a13d125e8a2cdd9614d7889fa99dcde449855(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d77a4eb9e292cf609ad3af7ed6d6ab97c907393555e345bf98ebc327875a8904(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFilestoreInstanceInitialReplicationReplicas]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97742ae79d5ddd928deb0309826b7c511adf1605d7b7e38c1a76da3ebadc7f08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0724cf9b7303a04883c5960f7b1929c2d5b43a86be0dbea61a2c7b33775221e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f4b3658c089bdae0ca8dac978d11d6a2821cebe4e2f34ed1c21ad92e3cf39cf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFilestoreInstanceInitialReplicationReplicas]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d6b28b943f20a0b6b30fa7802d80b2a76c0470ac3ad71e48b2b5db34c53465b(
    *,
    modes: typing.Sequence[builtins.str],
    network: builtins.str,
    connect_mode: typing.Optional[builtins.str] = None,
    psc_config: typing.Optional[typing.Union[GoogleFilestoreInstanceNetworksPscConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    reserved_ip_range: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94efa6dbaa55cc5f23aa57656a6939f90eedc5343eb903c3a7d08efe78dcfc62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b9d47cabe692bac496767a35196c5c227450433163b3c8cdc4ab1eae14473ed(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd23800ddb8cc4a10a3cd81345fb8d04f77a7a8c8b354751202a44eb6205e01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2534565232d3cf507294f373f490c3983b6d8536b34bc6a1cf153febd4433f0d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa5e63cb6c2f6258c662667e5983ec672a7c0e6f2be04e141104e413c9495286(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e82b759b1cc980b855956b3d69f807738bb24246e0448c5e9890493c4424b1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFilestoreInstanceNetworks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4e6973cd3c0424b00b39bec477d7a0d7e905b7deb43bf464b71af9e2672893d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bba3ee1e2e33de959852bff5761505d4bc5996a0517a3e2c6be3535142f71911(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa60a0b622d5fc66ed48a87fa63fd19e9004922f3883d64e777b8c13a3c36d0f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__968608d3fa37252ee5afd506326b38f91cd79133da174bddc002a19901f99cf6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__820d4756086f34c65d498fa0c18de8c74a686a8443df6eecfc158282dabc0e5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b8f182222a8d02f37bf1981d1f41baf9bf0cf449285e57503f36b5bf6ad1ad2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFilestoreInstanceNetworks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fca8337353bc487dad57e09788c417bbe7c43dacb16460e2f9129fe82ce5198(
    *,
    endpoint_project: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34fdceee218f35dd2611fafec11a4168585ae39829422375420ed6b1673b5ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24830b65265fc1f9650627fe572581af7ebb765c6b978f2823f466ee229d4b64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2124093221d01a3b88c097ecfb310d0fcb1ab5f5ee96892e286022eeae9db4(
    value: typing.Optional[GoogleFilestoreInstanceNetworksPscConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__675caefc2a4cb330e81c65541409bde22ad01f361fb6e103ea1165eec45b9b04(
    *,
    fixed_iops: typing.Optional[typing.Union[GoogleFilestoreInstancePerformanceConfigFixedIops, typing.Dict[builtins.str, typing.Any]]] = None,
    iops_per_tb: typing.Optional[typing.Union[GoogleFilestoreInstancePerformanceConfigIopsPerTb, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bf205d747fd822c2930b08003899ce3ad68554285613266eb80031233569f23(
    *,
    max_iops: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__589568bd7edac98b8815a505de8329687cb6c74c38c92b7894a1e87539eb2fed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73e5f8d82ff94357fa00fdb4bdc55a3de67d270c2d071263c74cf08c6ad165b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a765ecd586a500e9b6f101a5503b8b27aba4b35ec7087068d85ff2bfdf3109bf(
    value: typing.Optional[GoogleFilestoreInstancePerformanceConfigFixedIops],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__848db6b1df0e1e99028deaa977a7de949ac3f81ea01897992ba2839416b10dc2(
    *,
    max_iops_per_tb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71b12b944f0e24695fecd117138091c4bd907df9cfbb762982a2d072853741d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3669028e2d8bfcac52df25f4f8f6b5c6a1dc16bcbee290abbabde88c569466f7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb6eee1720d32b27846e8ad8eaf667c2b2b7e4d097d96fd9c71a0d3a64de03c(
    value: typing.Optional[GoogleFilestoreInstancePerformanceConfigIopsPerTb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622457bfd7342bcd55f032b5ce29ce752657c20cede67b4ff317505a65afbf67(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4449a144cdc6e59864fb960910a7d4279e47ec970a0891aa8e2705040fcebd9(
    value: typing.Optional[GoogleFilestoreInstancePerformanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1fc068a16b1a3888aa5f00c0d42aba7acd802b1b1e58993f65423f6977fa11a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__966e39354be18db153021cf3133b3fe5aa7e89134e203e45fbe237c68fa926f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f64f75b4fe732c28b16f050090e27c2fbc5a27f9891afcd178092d3d8ba228(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5b7e3e0cb5ddb27385ed5a35022d41fa378c35ae77e911c8097be8d92a97d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be23136e9105e02cd984ade10a9fe845027b716e4e65563ef9f142eede32d476(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eea970d8c6c2f02a046088ab652387753d9c1e98badfc5a0740ca277f8bf317(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFilestoreInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
