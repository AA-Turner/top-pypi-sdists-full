r'''
# `google_filestore_instance`

Refer to the Terraform Registry for docs: [`google_filestore_instance`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance).
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


class FilestoreInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance google_filestore_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        file_shares: typing.Union["FilestoreInstanceFileShares", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        networks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FilestoreInstanceNetworks", typing.Dict[builtins.str, typing.Any]]]],
        tier: builtins.str,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deletion_protection_reason: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        initial_replication: typing.Optional[typing.Union["FilestoreInstanceInitialReplication", typing.Dict[builtins.str, typing.Any]]] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        performance_config: typing.Optional[typing.Union["FilestoreInstancePerformanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["FilestoreInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance google_filestore_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param file_shares: file_shares block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#file_shares FilestoreInstance#file_shares}
        :param name: The resource name of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#name FilestoreInstance#name}
        :param networks: networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#networks FilestoreInstance#networks}
        :param tier: The service tier of the instance. Possible values include: STANDARD, PREMIUM, BASIC_HDD, BASIC_SSD, HIGH_SCALE_SSD, ZONAL, REGIONAL and ENTERPRISE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#tier FilestoreInstance#tier}
        :param deletion_protection_enabled: Indicates whether the instance is protected against deletion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#deletion_protection_enabled FilestoreInstance#deletion_protection_enabled}
        :param deletion_protection_reason: The reason for enabling deletion protection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#deletion_protection_reason FilestoreInstance#deletion_protection_reason}
        :param description: A description of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#description FilestoreInstance#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#id FilestoreInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_replication: initial_replication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#initial_replication FilestoreInstance#initial_replication}
        :param kms_key_name: KMS key name used for data encryption. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#kms_key_name FilestoreInstance#kms_key_name}
        :param labels: Resource labels to represent user-provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#labels FilestoreInstance#labels}
        :param location: The name of the location of the instance. This can be a region for ENTERPRISE tier instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#location FilestoreInstance#location}
        :param performance_config: performance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#performance_config FilestoreInstance#performance_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#project FilestoreInstance#project}.
        :param protocol: Either NFSv3, for using NFS version 3 as file sharing protocol, or NFSv4.1, for using NFS version 4.1 as file sharing protocol. NFSv4.1 can be used with HIGH_SCALE_SSD, ZONAL, REGIONAL and ENTERPRISE. The default is NFSv3. Default value: "NFS_V3" Possible values: ["NFS_V3", "NFS_V4_1"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#protocol FilestoreInstance#protocol}
        :param tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored when empty. The field is immutable and causes resource replacement when mutated. This field is only set at create time and modifying this field after creation will trigger recreation. To apply tags to an existing resource, see the 'google_tags_tag_value' resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#tags FilestoreInstance#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#timeouts FilestoreInstance#timeouts}
        :param zone: The name of the Filestore zone of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#zone FilestoreInstance#zone}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85347811711caef03bbff6021f42be93d19ec7bee5d913457707f128201a62ee)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FilestoreInstanceConfig(
            file_shares=file_shares,
            name=name,
            networks=networks,
            tier=tier,
            deletion_protection_enabled=deletion_protection_enabled,
            deletion_protection_reason=deletion_protection_reason,
            description=description,
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
        '''Generates CDKTF code for importing a FilestoreInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the FilestoreInstance to import.
        :param import_from_id: The id of the existing FilestoreInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the FilestoreInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d47c3174eed7f4866aafeda0e58d94ae36ff02d0365371f5bac98cf9ed1bf52e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFileShares")
    def put_file_shares(
        self,
        *,
        capacity_gb: jsii.Number,
        name: builtins.str,
        nfs_export_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FilestoreInstanceFileSharesNfsExportOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        source_backup: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param capacity_gb: File share capacity in GiB. This must be at least 1024 GiB for the standard tier, or 2560 GiB for the premium tier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#capacity_gb FilestoreInstance#capacity_gb}
        :param name: The name of the fileshare (16 characters or less). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#name FilestoreInstance#name}
        :param nfs_export_options: nfs_export_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#nfs_export_options FilestoreInstance#nfs_export_options}
        :param source_backup: The resource name of the backup, in the format projects/{projectId}/locations/{locationId}/backups/{backupId}, that this file share has been restored from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#source_backup FilestoreInstance#source_backup}
        '''
        value = FilestoreInstanceFileShares(
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
        replicas: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FilestoreInstanceInitialReplicationReplicas", typing.Dict[builtins.str, typing.Any]]]]] = None,
        role: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param replicas: replicas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#replicas FilestoreInstance#replicas}
        :param role: The replication role. Default value: "STANDBY" Possible values: ["ROLE_UNSPECIFIED", "ACTIVE", "STANDBY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#role FilestoreInstance#role}
        '''
        value = FilestoreInstanceInitialReplication(replicas=replicas, role=role)

        return typing.cast(None, jsii.invoke(self, "putInitialReplication", [value]))

    @jsii.member(jsii_name="putNetworks")
    def put_networks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FilestoreInstanceNetworks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a266fe5121f906fad86ad03cbf451d043ca9886e34cbc3a9b4c93f2f788e7fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworks", [value]))

    @jsii.member(jsii_name="putPerformanceConfig")
    def put_performance_config(
        self,
        *,
        fixed_iops: typing.Optional[typing.Union["FilestoreInstancePerformanceConfigFixedIops", typing.Dict[builtins.str, typing.Any]]] = None,
        iops_per_tb: typing.Optional[typing.Union["FilestoreInstancePerformanceConfigIopsPerTb", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param fixed_iops: fixed_iops block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#fixed_iops FilestoreInstance#fixed_iops}
        :param iops_per_tb: iops_per_tb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#iops_per_tb FilestoreInstance#iops_per_tb}
        '''
        value = FilestoreInstancePerformanceConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#create FilestoreInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#delete FilestoreInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#update FilestoreInstance#update}.
        '''
        value = FilestoreInstanceTimeouts(create=create, delete=delete, update=update)

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
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="effectiveReplication")
    def effective_replication(self) -> "FilestoreInstanceEffectiveReplicationList":
        return typing.cast("FilestoreInstanceEffectiveReplicationList", jsii.get(self, "effectiveReplication"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="fileShares")
    def file_shares(self) -> "FilestoreInstanceFileSharesOutputReference":
        return typing.cast("FilestoreInstanceFileSharesOutputReference", jsii.get(self, "fileShares"))

    @builtins.property
    @jsii.member(jsii_name="initialReplication")
    def initial_replication(
        self,
    ) -> "FilestoreInstanceInitialReplicationOutputReference":
        return typing.cast("FilestoreInstanceInitialReplicationOutputReference", jsii.get(self, "initialReplication"))

    @builtins.property
    @jsii.member(jsii_name="networks")
    def networks(self) -> "FilestoreInstanceNetworksList":
        return typing.cast("FilestoreInstanceNetworksList", jsii.get(self, "networks"))

    @builtins.property
    @jsii.member(jsii_name="performanceConfig")
    def performance_config(self) -> "FilestoreInstancePerformanceConfigOutputReference":
        return typing.cast("FilestoreInstancePerformanceConfigOutputReference", jsii.get(self, "performanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "FilestoreInstanceTimeoutsOutputReference":
        return typing.cast("FilestoreInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    @jsii.member(jsii_name="fileSharesInput")
    def file_shares_input(self) -> typing.Optional["FilestoreInstanceFileShares"]:
        return typing.cast(typing.Optional["FilestoreInstanceFileShares"], jsii.get(self, "fileSharesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="initialReplicationInput")
    def initial_replication_input(
        self,
    ) -> typing.Optional["FilestoreInstanceInitialReplication"]:
        return typing.cast(typing.Optional["FilestoreInstanceInitialReplication"], jsii.get(self, "initialReplicationInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FilestoreInstanceNetworks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FilestoreInstanceNetworks"]]], jsii.get(self, "networksInput"))

    @builtins.property
    @jsii.member(jsii_name="performanceConfigInput")
    def performance_config_input(
        self,
    ) -> typing.Optional["FilestoreInstancePerformanceConfig"]:
        return typing.cast(typing.Optional["FilestoreInstancePerformanceConfig"], jsii.get(self, "performanceConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FilestoreInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FilestoreInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c69c169821047f9a4e5de5d5affed5aee8aeba097d1f8e34deb20eb89767004e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtectionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionReason")
    def deletion_protection_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deletionProtectionReason"))

    @deletion_protection_reason.setter
    def deletion_protection_reason(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b90e5cc8351b490799c120082d705b31ac91e98486d85e21257274f344d5cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtectionReason", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fa141b1a75ae66610ce7c0033db5af77999ae4999f9edb6e15e6b05cd328a22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6154b1ad32ae6a1f4a89c470e9552bca4cfa2d942e29ff61dcafd3658b1b01b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2bcdc11d144edbac1600623b1fdad90f84030237279d215285b28822517a78a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a017b7b97be0e045de649421cbd018e28d04637250512909fe6d953bbe6dc06d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bbb405e6d73da82850f5fe0176af4bf1aba7dda0e6e0477f3b42a522749e1d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c81081de52a6a692b58db18610b6839e2578cd5172f906ff0b30bfc1a93478d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__381b4685dacc732ff726b61c265983d72294601b8162d7e5cb6f85906e4fa6ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c99be7fa1c4828207135fb5c7268fb3c76d0f9d3c032c25a1a46fd47d24bcb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b95d75fdb9e2c3f2cf27a07fbaf7e418dd01c77022aa55c31505808edcc41c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13377d598ba026afd7fe5f9d89b2183c35e993151ab52d2d573c528eb4faf4c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d354abbc4e1bd438643d6e9fcea39806f193eaa90227f360689dc0de59713e0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstanceConfig",
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
class FilestoreInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        file_shares: typing.Union["FilestoreInstanceFileShares", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        networks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FilestoreInstanceNetworks", typing.Dict[builtins.str, typing.Any]]]],
        tier: builtins.str,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deletion_protection_reason: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        initial_replication: typing.Optional[typing.Union["FilestoreInstanceInitialReplication", typing.Dict[builtins.str, typing.Any]]] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        performance_config: typing.Optional[typing.Union["FilestoreInstancePerformanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["FilestoreInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param file_shares: file_shares block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#file_shares FilestoreInstance#file_shares}
        :param name: The resource name of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#name FilestoreInstance#name}
        :param networks: networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#networks FilestoreInstance#networks}
        :param tier: The service tier of the instance. Possible values include: STANDARD, PREMIUM, BASIC_HDD, BASIC_SSD, HIGH_SCALE_SSD, ZONAL, REGIONAL and ENTERPRISE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#tier FilestoreInstance#tier}
        :param deletion_protection_enabled: Indicates whether the instance is protected against deletion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#deletion_protection_enabled FilestoreInstance#deletion_protection_enabled}
        :param deletion_protection_reason: The reason for enabling deletion protection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#deletion_protection_reason FilestoreInstance#deletion_protection_reason}
        :param description: A description of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#description FilestoreInstance#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#id FilestoreInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_replication: initial_replication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#initial_replication FilestoreInstance#initial_replication}
        :param kms_key_name: KMS key name used for data encryption. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#kms_key_name FilestoreInstance#kms_key_name}
        :param labels: Resource labels to represent user-provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#labels FilestoreInstance#labels}
        :param location: The name of the location of the instance. This can be a region for ENTERPRISE tier instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#location FilestoreInstance#location}
        :param performance_config: performance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#performance_config FilestoreInstance#performance_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#project FilestoreInstance#project}.
        :param protocol: Either NFSv3, for using NFS version 3 as file sharing protocol, or NFSv4.1, for using NFS version 4.1 as file sharing protocol. NFSv4.1 can be used with HIGH_SCALE_SSD, ZONAL, REGIONAL and ENTERPRISE. The default is NFSv3. Default value: "NFS_V3" Possible values: ["NFS_V3", "NFS_V4_1"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#protocol FilestoreInstance#protocol}
        :param tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored when empty. The field is immutable and causes resource replacement when mutated. This field is only set at create time and modifying this field after creation will trigger recreation. To apply tags to an existing resource, see the 'google_tags_tag_value' resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#tags FilestoreInstance#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#timeouts FilestoreInstance#timeouts}
        :param zone: The name of the Filestore zone of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#zone FilestoreInstance#zone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(file_shares, dict):
            file_shares = FilestoreInstanceFileShares(**file_shares)
        if isinstance(initial_replication, dict):
            initial_replication = FilestoreInstanceInitialReplication(**initial_replication)
        if isinstance(performance_config, dict):
            performance_config = FilestoreInstancePerformanceConfig(**performance_config)
        if isinstance(timeouts, dict):
            timeouts = FilestoreInstanceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aea3047c69df2917fca515d54c1b0a5677e0be7b826c7b390b52d7e5878a292)
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
    def file_shares(self) -> "FilestoreInstanceFileShares":
        '''file_shares block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#file_shares FilestoreInstance#file_shares}
        '''
        result = self._values.get("file_shares")
        assert result is not None, "Required property 'file_shares' is missing"
        return typing.cast("FilestoreInstanceFileShares", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The resource name of the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#name FilestoreInstance#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def networks(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FilestoreInstanceNetworks"]]:
        '''networks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#networks FilestoreInstance#networks}
        '''
        result = self._values.get("networks")
        assert result is not None, "Required property 'networks' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FilestoreInstanceNetworks"]], result)

    @builtins.property
    def tier(self) -> builtins.str:
        '''The service tier of the instance. Possible values include: STANDARD, PREMIUM, BASIC_HDD, BASIC_SSD, HIGH_SCALE_SSD, ZONAL, REGIONAL and ENTERPRISE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#tier FilestoreInstance#tier}
        '''
        result = self._values.get("tier")
        assert result is not None, "Required property 'tier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deletion_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether the instance is protected against deletion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#deletion_protection_enabled FilestoreInstance#deletion_protection_enabled}
        '''
        result = self._values.get("deletion_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def deletion_protection_reason(self) -> typing.Optional[builtins.str]:
        '''The reason for enabling deletion protection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#deletion_protection_reason FilestoreInstance#deletion_protection_reason}
        '''
        result = self._values.get("deletion_protection_reason")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#description FilestoreInstance#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#id FilestoreInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_replication(
        self,
    ) -> typing.Optional["FilestoreInstanceInitialReplication"]:
        '''initial_replication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#initial_replication FilestoreInstance#initial_replication}
        '''
        result = self._values.get("initial_replication")
        return typing.cast(typing.Optional["FilestoreInstanceInitialReplication"], result)

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''KMS key name used for data encryption.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#kms_key_name FilestoreInstance#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Resource labels to represent user-provided metadata.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#labels FilestoreInstance#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The name of the location of the instance. This can be a region for ENTERPRISE tier instances.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#location FilestoreInstance#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def performance_config(
        self,
    ) -> typing.Optional["FilestoreInstancePerformanceConfig"]:
        '''performance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#performance_config FilestoreInstance#performance_config}
        '''
        result = self._values.get("performance_config")
        return typing.cast(typing.Optional["FilestoreInstancePerformanceConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#project FilestoreInstance#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Either NFSv3, for using NFS version 3 as file sharing protocol, or NFSv4.1, for using NFS version 4.1 as file sharing protocol. NFSv4.1 can be used with HIGH_SCALE_SSD, ZONAL, REGIONAL and ENTERPRISE. The default is NFSv3. Default value: "NFS_V3" Possible values: ["NFS_V3", "NFS_V4_1"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#protocol FilestoreInstance#protocol}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#tags FilestoreInstance#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["FilestoreInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#timeouts FilestoreInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["FilestoreInstanceTimeouts"], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''The name of the Filestore zone of the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#zone FilestoreInstance#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FilestoreInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstanceEffectiveReplication",
    jsii_struct_bases=[],
    name_mapping={},
)
class FilestoreInstanceEffectiveReplication:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FilestoreInstanceEffectiveReplication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FilestoreInstanceEffectiveReplicationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstanceEffectiveReplicationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57e17e6d79121f339de8250da40a7fa79963657f62009e3640e9ca518453167b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FilestoreInstanceEffectiveReplicationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2cb9e02f8515be73252e6670563b886fbb3e87308e6551c9f20fc8e9e4d048b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FilestoreInstanceEffectiveReplicationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65c15831b0606ca3c26d9ef1814d861c71602b0c331500daeb0577c5db8c5701)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02796c15ffb2f9aa29145b0df9ba84f83a65ad5ce036cc9ac0d249167682a510)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53454e677a6786232f1f5400d58d4ca0473b82f6f996f86cbf43d3a45d83244b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FilestoreInstanceEffectiveReplicationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstanceEffectiveReplicationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ce2b339d49ac8c71eec508d99148596aa8bd370021906dd24057bb691a7adab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="replicas")
    def replicas(self) -> "FilestoreInstanceEffectiveReplicationReplicasList":
        return typing.cast("FilestoreInstanceEffectiveReplicationReplicasList", jsii.get(self, "replicas"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FilestoreInstanceEffectiveReplication]:
        return typing.cast(typing.Optional[FilestoreInstanceEffectiveReplication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FilestoreInstanceEffectiveReplication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d50d373876aaeeaf5cfa1d4d80e0c9f72f55e2d9be1800237dad444d061d9bcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstanceEffectiveReplicationReplicas",
    jsii_struct_bases=[],
    name_mapping={},
)
class FilestoreInstanceEffectiveReplicationReplicas:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FilestoreInstanceEffectiveReplicationReplicas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FilestoreInstanceEffectiveReplicationReplicasList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstanceEffectiveReplicationReplicasList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55457c71dfe426fb847200fe90ba562174f1f9b2841461d31a4c49101b15f757)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FilestoreInstanceEffectiveReplicationReplicasOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aa1ed13ac6191c97a62d84978e96794b2b2e6085790b074dbfa38b0ebb78683)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FilestoreInstanceEffectiveReplicationReplicasOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a688d5a01f71e45e73badce5e260b02208cbb6a101b5802e1f6b7c497ae2485)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2709089001deb2d759e9a9bc066b1049cfd1aa5735bb9ed805a8433408192358)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ea094a2a903a86c9f19c47068447fccc3794127ef175df6b166ee5f35a0ca79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FilestoreInstanceEffectiveReplicationReplicasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstanceEffectiveReplicationReplicasOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__667d5f1e9e7a1be7ae8a398bf4b873d823baf1028b3d6b27abf1a0b480dbabfc)
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
    ) -> typing.Optional[FilestoreInstanceEffectiveReplicationReplicas]:
        return typing.cast(typing.Optional[FilestoreInstanceEffectiveReplicationReplicas], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FilestoreInstanceEffectiveReplicationReplicas],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bc6b954ffdd9a5194a92302f8f4384b01c58de24cd4ae8100c97db61cbde94b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstanceFileShares",
    jsii_struct_bases=[],
    name_mapping={
        "capacity_gb": "capacityGb",
        "name": "name",
        "nfs_export_options": "nfsExportOptions",
        "source_backup": "sourceBackup",
    },
)
class FilestoreInstanceFileShares:
    def __init__(
        self,
        *,
        capacity_gb: jsii.Number,
        name: builtins.str,
        nfs_export_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FilestoreInstanceFileSharesNfsExportOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        source_backup: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param capacity_gb: File share capacity in GiB. This must be at least 1024 GiB for the standard tier, or 2560 GiB for the premium tier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#capacity_gb FilestoreInstance#capacity_gb}
        :param name: The name of the fileshare (16 characters or less). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#name FilestoreInstance#name}
        :param nfs_export_options: nfs_export_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#nfs_export_options FilestoreInstance#nfs_export_options}
        :param source_backup: The resource name of the backup, in the format projects/{projectId}/locations/{locationId}/backups/{backupId}, that this file share has been restored from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#source_backup FilestoreInstance#source_backup}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a40f8b69cdf281b74186cad919d58f821b4db1d9da73ef69c2ced566c139e8c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#capacity_gb FilestoreInstance#capacity_gb}
        '''
        result = self._values.get("capacity_gb")
        assert result is not None, "Required property 'capacity_gb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the fileshare (16 characters or less).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#name FilestoreInstance#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def nfs_export_options(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FilestoreInstanceFileSharesNfsExportOptions"]]]:
        '''nfs_export_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#nfs_export_options FilestoreInstance#nfs_export_options}
        '''
        result = self._values.get("nfs_export_options")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FilestoreInstanceFileSharesNfsExportOptions"]]], result)

    @builtins.property
    def source_backup(self) -> typing.Optional[builtins.str]:
        '''The resource name of the backup, in the format projects/{projectId}/locations/{locationId}/backups/{backupId}, that this file share has been restored from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#source_backup FilestoreInstance#source_backup}
        '''
        result = self._values.get("source_backup")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FilestoreInstanceFileShares(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstanceFileSharesNfsExportOptions",
    jsii_struct_bases=[],
    name_mapping={
        "access_mode": "accessMode",
        "anon_gid": "anonGid",
        "anon_uid": "anonUid",
        "ip_ranges": "ipRanges",
        "squash_mode": "squashMode",
    },
)
class FilestoreInstanceFileSharesNfsExportOptions:
    def __init__(
        self,
        *,
        access_mode: typing.Optional[builtins.str] = None,
        anon_gid: typing.Optional[jsii.Number] = None,
        anon_uid: typing.Optional[jsii.Number] = None,
        ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        squash_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_mode: Either READ_ONLY, for allowing only read requests on the exported directory, or READ_WRITE, for allowing both read and write requests. The default is READ_WRITE. Default value: "READ_WRITE" Possible values: ["READ_ONLY", "READ_WRITE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#access_mode FilestoreInstance#access_mode}
        :param anon_gid: An integer representing the anonymous group id with a default value of 65534. Anon_gid may only be set with squashMode of ROOT_SQUASH. An error will be returned if this field is specified for other squashMode settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#anon_gid FilestoreInstance#anon_gid}
        :param anon_uid: An integer representing the anonymous user id with a default value of 65534. Anon_uid may only be set with squashMode of ROOT_SQUASH. An error will be returned if this field is specified for other squashMode settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#anon_uid FilestoreInstance#anon_uid}
        :param ip_ranges: List of either IPv4 addresses, or ranges in CIDR notation which may mount the file share. Overlapping IP ranges are not allowed, both within and across NfsExportOptions. An error will be returned. The limit is 64 IP ranges/addresses for each FileShareConfig among all NfsExportOptions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#ip_ranges FilestoreInstance#ip_ranges}
        :param squash_mode: Either NO_ROOT_SQUASH, for allowing root access on the exported directory, or ROOT_SQUASH, for not allowing root access. The default is NO_ROOT_SQUASH. Default value: "NO_ROOT_SQUASH" Possible values: ["NO_ROOT_SQUASH", "ROOT_SQUASH"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#squash_mode FilestoreInstance#squash_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4f09240d8c8c9b3e435c80fe9941d148c197d156089b176c38622b10494b359)
            check_type(argname="argument access_mode", value=access_mode, expected_type=type_hints["access_mode"])
            check_type(argname="argument anon_gid", value=anon_gid, expected_type=type_hints["anon_gid"])
            check_type(argname="argument anon_uid", value=anon_uid, expected_type=type_hints["anon_uid"])
            check_type(argname="argument ip_ranges", value=ip_ranges, expected_type=type_hints["ip_ranges"])
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
        if squash_mode is not None:
            self._values["squash_mode"] = squash_mode

    @builtins.property
    def access_mode(self) -> typing.Optional[builtins.str]:
        '''Either READ_ONLY, for allowing only read requests on the exported directory, or READ_WRITE, for allowing both read and write requests.

        The default is READ_WRITE. Default value: "READ_WRITE" Possible values: ["READ_ONLY", "READ_WRITE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#access_mode FilestoreInstance#access_mode}
        '''
        result = self._values.get("access_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def anon_gid(self) -> typing.Optional[jsii.Number]:
        '''An integer representing the anonymous group id with a default value of 65534.

        Anon_gid may only be set with squashMode of ROOT_SQUASH. An error will be returned
        if this field is specified for other squashMode settings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#anon_gid FilestoreInstance#anon_gid}
        '''
        result = self._values.get("anon_gid")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def anon_uid(self) -> typing.Optional[jsii.Number]:
        '''An integer representing the anonymous user id with a default value of 65534.

        Anon_uid may only be set with squashMode of ROOT_SQUASH. An error will be returned
        if this field is specified for other squashMode settings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#anon_uid FilestoreInstance#anon_uid}
        '''
        result = self._values.get("anon_uid")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of either IPv4 addresses, or ranges in CIDR notation which may mount the file share.

        Overlapping IP ranges are not allowed, both within and across NfsExportOptions. An error will be returned.
        The limit is 64 IP ranges/addresses for each FileShareConfig among all NfsExportOptions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#ip_ranges FilestoreInstance#ip_ranges}
        '''
        result = self._values.get("ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def squash_mode(self) -> typing.Optional[builtins.str]:
        '''Either NO_ROOT_SQUASH, for allowing root access on the exported directory, or ROOT_SQUASH, for not allowing root access.

        The default is NO_ROOT_SQUASH. Default value: "NO_ROOT_SQUASH" Possible values: ["NO_ROOT_SQUASH", "ROOT_SQUASH"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#squash_mode FilestoreInstance#squash_mode}
        '''
        result = self._values.get("squash_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FilestoreInstanceFileSharesNfsExportOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FilestoreInstanceFileSharesNfsExportOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstanceFileSharesNfsExportOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61985706813f731b5da45b53212cdb5d5c780ba1e1cd4331ccbb83fb96056c0b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FilestoreInstanceFileSharesNfsExportOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd98b350530e2a00dfeb626de82b909b4a62c7be4aa0ec03a76d0c8cf461c899)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FilestoreInstanceFileSharesNfsExportOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__761ccb816aeeedd6f230c754d99442ce63f8285ad905d8f694b412f3d07c2034)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14215a7bd07ccf32eb893ff0b69fd8002c133f5dae5fefd05fe68496f5a88003)
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
            type_hints = typing.get_type_hints(_typecheckingstub__891c13e125a3b33f40adafd88893402aab2adb5b6ce6791f176aa4e98b7e5f63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FilestoreInstanceFileSharesNfsExportOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FilestoreInstanceFileSharesNfsExportOptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FilestoreInstanceFileSharesNfsExportOptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20d49d59b69467e8a9eb124ecfa671c2eab47c54da37db879d56d4b9809cc743)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FilestoreInstanceFileSharesNfsExportOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstanceFileSharesNfsExportOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5906d92fb64a7667148c36eb855abd8f295c52f72befc5fc3835f00039b8c9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d997102f15e6076686661f163209bafcbd09296568e99e69975f6f9bf0ecb4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="anonGid")
    def anon_gid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "anonGid"))

    @anon_gid.setter
    def anon_gid(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5813d60bd69a5951afb45488e1d1c6f8cf9f78f8701111b5837c36e7dbfe6be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "anonGid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="anonUid")
    def anon_uid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "anonUid"))

    @anon_uid.setter
    def anon_uid(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c86fa2f386a67c57b29ac080b19fe9240531e0b953ecf113b4cdccc387875db2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "anonUid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipRanges")
    def ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipRanges"))

    @ip_ranges.setter
    def ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2686eeff31b8b7404907d5094736e67cd0f62325ec139fd6aee988a24f7f08a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="squashMode")
    def squash_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "squashMode"))

    @squash_mode.setter
    def squash_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fad6687e40a770145d7e390b519aeff14dd36e6bc3c566181f85183c32c4c0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "squashMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FilestoreInstanceFileSharesNfsExportOptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FilestoreInstanceFileSharesNfsExportOptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FilestoreInstanceFileSharesNfsExportOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19c886894bbb25c6811068b5dd8742b1bf7f04dc5e1bea4d09629a84fc920a4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FilestoreInstanceFileSharesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstanceFileSharesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__003d4cc20d5e398d9e6a296700349e84b98cc7db90c9328fa6bfc3ebcc13aab6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNfsExportOptions")
    def put_nfs_export_options(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FilestoreInstanceFileSharesNfsExportOptions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24fa889c7179cdcff1e4a61351246ec41b45a38e603309fc8c325bafb6892f5e)
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
    def nfs_export_options(self) -> FilestoreInstanceFileSharesNfsExportOptionsList:
        return typing.cast(FilestoreInstanceFileSharesNfsExportOptionsList, jsii.get(self, "nfsExportOptions"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FilestoreInstanceFileSharesNfsExportOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FilestoreInstanceFileSharesNfsExportOptions]]], jsii.get(self, "nfsExportOptionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a4cdfdb1c0fc251a36faf18bf4e4cf281ca16b64e907154335d408b009b2e228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca38d07222d27e5dbbaea1c3f9c69a90518de727c9d08612666082b93c0a4b2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceBackup")
    def source_backup(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceBackup"))

    @source_backup.setter
    def source_backup(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66657cbb20ce4752dad0bf6dab69554633cdbf68b2ac84b931970895be64ff29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceBackup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FilestoreInstanceFileShares]:
        return typing.cast(typing.Optional[FilestoreInstanceFileShares], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FilestoreInstanceFileShares],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__166c2b2395fab8f079be05e1593a3794d94305f3f0814362db60c8c5f5603cac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstanceInitialReplication",
    jsii_struct_bases=[],
    name_mapping={"replicas": "replicas", "role": "role"},
)
class FilestoreInstanceInitialReplication:
    def __init__(
        self,
        *,
        replicas: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FilestoreInstanceInitialReplicationReplicas", typing.Dict[builtins.str, typing.Any]]]]] = None,
        role: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param replicas: replicas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#replicas FilestoreInstance#replicas}
        :param role: The replication role. Default value: "STANDBY" Possible values: ["ROLE_UNSPECIFIED", "ACTIVE", "STANDBY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#role FilestoreInstance#role}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfa0d44d3d1a30d071310d2b83f08756f1dd1efd44a41a5c3d00a7787949247d)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FilestoreInstanceInitialReplicationReplicas"]]]:
        '''replicas block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#replicas FilestoreInstance#replicas}
        '''
        result = self._values.get("replicas")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FilestoreInstanceInitialReplicationReplicas"]]], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''The replication role. Default value: "STANDBY" Possible values: ["ROLE_UNSPECIFIED", "ACTIVE", "STANDBY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#role FilestoreInstance#role}
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FilestoreInstanceInitialReplication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FilestoreInstanceInitialReplicationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstanceInitialReplicationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8df9ccfcf18c3204c507d99a599f892f94ec98bca941aa72d66fd4d45a19343)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putReplicas")
    def put_replicas(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FilestoreInstanceInitialReplicationReplicas", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0fa64e3dbeada48232e1ca65714e703ca276d8da0f2a07af5793b52904c7b80)
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
    def replicas(self) -> "FilestoreInstanceInitialReplicationReplicasList":
        return typing.cast("FilestoreInstanceInitialReplicationReplicasList", jsii.get(self, "replicas"))

    @builtins.property
    @jsii.member(jsii_name="replicasInput")
    def replicas_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FilestoreInstanceInitialReplicationReplicas"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FilestoreInstanceInitialReplicationReplicas"]]], jsii.get(self, "replicasInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3ad2197855377f81eca34de9d49110b7934adbd131faf9d04d98d450adc18353)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FilestoreInstanceInitialReplication]:
        return typing.cast(typing.Optional[FilestoreInstanceInitialReplication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FilestoreInstanceInitialReplication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39d08e5f63f9a7e53c10cabaee72d4118875310fe769c4a673e5a1cb5d2c06c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstanceInitialReplicationReplicas",
    jsii_struct_bases=[],
    name_mapping={"peer_instance": "peerInstance"},
)
class FilestoreInstanceInitialReplicationReplicas:
    def __init__(self, *, peer_instance: builtins.str) -> None:
        '''
        :param peer_instance: The peer instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#peer_instance FilestoreInstance#peer_instance}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efde858380367303244ba90cd00962b1bbfcf6e82ecdaf8f146a209e011a6cc5)
            check_type(argname="argument peer_instance", value=peer_instance, expected_type=type_hints["peer_instance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "peer_instance": peer_instance,
        }

    @builtins.property
    def peer_instance(self) -> builtins.str:
        '''The peer instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#peer_instance FilestoreInstance#peer_instance}
        '''
        result = self._values.get("peer_instance")
        assert result is not None, "Required property 'peer_instance' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FilestoreInstanceInitialReplicationReplicas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FilestoreInstanceInitialReplicationReplicasList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstanceInitialReplicationReplicasList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4499ee913d38976c818c95972c20ce14f3f8443448bbab67ca73584f2b1ab1ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FilestoreInstanceInitialReplicationReplicasOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cf00d4f64f1c409ee6cfb07af7708bdafb4b839430a50a4ee9e8e10b9aac1a4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FilestoreInstanceInitialReplicationReplicasOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc80ef4d0576b89ed9fcf15578de9938b2cdee705d151dd4aab4e2b0a80e7536)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e492868702d17060eafc10c4b7499355a47161b2e0d506aba7eb1a61937411e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__002456282e62427fd5e5173d8cd5e337c3d076bce1f35116b1dcae3db345e0c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FilestoreInstanceInitialReplicationReplicas]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FilestoreInstanceInitialReplicationReplicas]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FilestoreInstanceInitialReplicationReplicas]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f5ef6ff7179a77248a5c7ea2dcb7482182777e1d7ab94968a710c90bea794a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FilestoreInstanceInitialReplicationReplicasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstanceInitialReplicationReplicasOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__032498d3008c0e49b4005ac4290590ea7c6de23d3a0f6eaba52f8cab68629cd1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3230591eab22d91a8d842b5f8fe25d14f2853d3e66118530e465a9d2a77e24e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FilestoreInstanceInitialReplicationReplicas]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FilestoreInstanceInitialReplicationReplicas]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FilestoreInstanceInitialReplicationReplicas]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38f685877db515970a4a9131ea82591f79b781f3f170526beeba14a71d693c34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstanceNetworks",
    jsii_struct_bases=[],
    name_mapping={
        "modes": "modes",
        "network": "network",
        "connect_mode": "connectMode",
        "reserved_ip_range": "reservedIpRange",
    },
)
class FilestoreInstanceNetworks:
    def __init__(
        self,
        *,
        modes: typing.Sequence[builtins.str],
        network: builtins.str,
        connect_mode: typing.Optional[builtins.str] = None,
        reserved_ip_range: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param modes: IP versions for which the instance has IP addresses assigned. Possible values: ["ADDRESS_MODE_UNSPECIFIED", "MODE_IPV4", "MODE_IPV6"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#modes FilestoreInstance#modes}
        :param network: The name of the GCE VPC network to which the instance is connected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#network FilestoreInstance#network}
        :param connect_mode: The network connect mode of the Filestore instance. If not provided, the connect mode defaults to DIRECT_PEERING. Default value: "DIRECT_PEERING" Possible values: ["DIRECT_PEERING", "PRIVATE_SERVICE_ACCESS", "PRIVATE_SERVICE_CONNECT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#connect_mode FilestoreInstance#connect_mode}
        :param reserved_ip_range: A /29 CIDR block that identifies the range of IP addresses reserved for this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#reserved_ip_range FilestoreInstance#reserved_ip_range}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41dfd05f7041ba508f286713c57a6b5bd20d04ee126faf0ddc92b4bd1edc218a)
            check_type(argname="argument modes", value=modes, expected_type=type_hints["modes"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument connect_mode", value=connect_mode, expected_type=type_hints["connect_mode"])
            check_type(argname="argument reserved_ip_range", value=reserved_ip_range, expected_type=type_hints["reserved_ip_range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "modes": modes,
            "network": network,
        }
        if connect_mode is not None:
            self._values["connect_mode"] = connect_mode
        if reserved_ip_range is not None:
            self._values["reserved_ip_range"] = reserved_ip_range

    @builtins.property
    def modes(self) -> typing.List[builtins.str]:
        '''IP versions for which the instance has IP addresses assigned. Possible values: ["ADDRESS_MODE_UNSPECIFIED", "MODE_IPV4", "MODE_IPV6"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#modes FilestoreInstance#modes}
        '''
        result = self._values.get("modes")
        assert result is not None, "Required property 'modes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def network(self) -> builtins.str:
        '''The name of the GCE VPC network to which the instance is connected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#network FilestoreInstance#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connect_mode(self) -> typing.Optional[builtins.str]:
        '''The network connect mode of the Filestore instance.

        If not provided, the connect mode defaults to
        DIRECT_PEERING. Default value: "DIRECT_PEERING" Possible values: ["DIRECT_PEERING", "PRIVATE_SERVICE_ACCESS", "PRIVATE_SERVICE_CONNECT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#connect_mode FilestoreInstance#connect_mode}
        '''
        result = self._values.get("connect_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reserved_ip_range(self) -> typing.Optional[builtins.str]:
        '''A /29 CIDR block that identifies the range of IP addresses reserved for this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#reserved_ip_range FilestoreInstance#reserved_ip_range}
        '''
        result = self._values.get("reserved_ip_range")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FilestoreInstanceNetworks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FilestoreInstanceNetworksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstanceNetworksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f563e8302497b28afc9ff9973ddb85471c2d2a977b39bea8b0c7ab73bed8de4a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FilestoreInstanceNetworksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc2346738f5d38a607bc169168d152ad6b6a71dddbc5940ebafebf6717033095)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FilestoreInstanceNetworksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb3fcdc378391617c8764d6c61246bb437416713b7ba2fd3914960208c926e83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b81fda9576acd8caf6514ac40ad39664a23d071cd7bee70a6399a6902b62516c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4285a8156e9b6f9ec4c6e5a4ee8e6a72b934cf1724654588d06cb775b427356f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FilestoreInstanceNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FilestoreInstanceNetworks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FilestoreInstanceNetworks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6581c388d6bc27072a525e181075ac23d9d561ebadbec8b92fd18b3b350af6b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FilestoreInstanceNetworksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstanceNetworksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de14cd710b9551b74a7582bb26db5a34e4fcc6b9493aa22993329dc387a0bad3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConnectMode")
    def reset_connect_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectMode", []))

    @jsii.member(jsii_name="resetReservedIpRange")
    def reset_reserved_ip_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservedIpRange", []))

    @builtins.property
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipAddresses"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__cdf431b54bfeacf9e5ab27da23cc59c18a393f7da0563398ceb330108d99cfbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modes")
    def modes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "modes"))

    @modes.setter
    def modes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad32dda00cdc0c667b9be5f11f6c79ac869588823ca9f6605cd691a89cbc7ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdec87675b8e500b93ff408bd21344f36efeeea35bb7d4502dc92087ccf9aaed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reservedIpRange")
    def reserved_ip_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reservedIpRange"))

    @reserved_ip_range.setter
    def reserved_ip_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85b76bcab831f5ac302b49a32396c55e203f954be139e5b2524a86e0daadbfac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservedIpRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FilestoreInstanceNetworks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FilestoreInstanceNetworks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FilestoreInstanceNetworks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b78e1af4403bda3b964336d5237403d40a4811e794bd28147494847bf9956c16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstancePerformanceConfig",
    jsii_struct_bases=[],
    name_mapping={"fixed_iops": "fixedIops", "iops_per_tb": "iopsPerTb"},
)
class FilestoreInstancePerformanceConfig:
    def __init__(
        self,
        *,
        fixed_iops: typing.Optional[typing.Union["FilestoreInstancePerformanceConfigFixedIops", typing.Dict[builtins.str, typing.Any]]] = None,
        iops_per_tb: typing.Optional[typing.Union["FilestoreInstancePerformanceConfigIopsPerTb", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param fixed_iops: fixed_iops block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#fixed_iops FilestoreInstance#fixed_iops}
        :param iops_per_tb: iops_per_tb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#iops_per_tb FilestoreInstance#iops_per_tb}
        '''
        if isinstance(fixed_iops, dict):
            fixed_iops = FilestoreInstancePerformanceConfigFixedIops(**fixed_iops)
        if isinstance(iops_per_tb, dict):
            iops_per_tb = FilestoreInstancePerformanceConfigIopsPerTb(**iops_per_tb)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5fd6202b38e8582b1b61efde96c77fef6dcf931a35f57bd4591559e00766d50)
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
    ) -> typing.Optional["FilestoreInstancePerformanceConfigFixedIops"]:
        '''fixed_iops block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#fixed_iops FilestoreInstance#fixed_iops}
        '''
        result = self._values.get("fixed_iops")
        return typing.cast(typing.Optional["FilestoreInstancePerformanceConfigFixedIops"], result)

    @builtins.property
    def iops_per_tb(
        self,
    ) -> typing.Optional["FilestoreInstancePerformanceConfigIopsPerTb"]:
        '''iops_per_tb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#iops_per_tb FilestoreInstance#iops_per_tb}
        '''
        result = self._values.get("iops_per_tb")
        return typing.cast(typing.Optional["FilestoreInstancePerformanceConfigIopsPerTb"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FilestoreInstancePerformanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstancePerformanceConfigFixedIops",
    jsii_struct_bases=[],
    name_mapping={"max_iops": "maxIops"},
)
class FilestoreInstancePerformanceConfigFixedIops:
    def __init__(self, *, max_iops: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param max_iops: The number of IOPS to provision for the instance. max_iops must be in multiple of 1000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#max_iops FilestoreInstance#max_iops}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0846d0ad2d4098f7afa8b94685f06482d71e688be1a83a3e0f8371784e18f05e)
            check_type(argname="argument max_iops", value=max_iops, expected_type=type_hints["max_iops"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_iops is not None:
            self._values["max_iops"] = max_iops

    @builtins.property
    def max_iops(self) -> typing.Optional[jsii.Number]:
        '''The number of IOPS to provision for the instance. max_iops must be in multiple of 1000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#max_iops FilestoreInstance#max_iops}
        '''
        result = self._values.get("max_iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FilestoreInstancePerformanceConfigFixedIops(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FilestoreInstancePerformanceConfigFixedIopsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstancePerformanceConfigFixedIopsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ef9c03acd10e9f73819967c5750593e6d0240e60149a26bb7c3c608579a4d88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__071067b411509305ac4c66201660cf7bdb91a96eb47515ea5093b9f11eba6908)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIops", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FilestoreInstancePerformanceConfigFixedIops]:
        return typing.cast(typing.Optional[FilestoreInstancePerformanceConfigFixedIops], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FilestoreInstancePerformanceConfigFixedIops],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cf830d96d1e9ef93c4b64e90e8d188bab84041228fdc0a9ea06d8fe576989ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstancePerformanceConfigIopsPerTb",
    jsii_struct_bases=[],
    name_mapping={"max_iops_per_tb": "maxIopsPerTb"},
)
class FilestoreInstancePerformanceConfigIopsPerTb:
    def __init__(self, *, max_iops_per_tb: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param max_iops_per_tb: The instance max IOPS will be calculated by multiplying the capacity of the instance (TB) by max_iops_per_tb, and rounding to the nearest 1000. The instance max IOPS will be changed dynamically based on the instance capacity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#max_iops_per_tb FilestoreInstance#max_iops_per_tb}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__882397484c1807d7fa9bd0ec842d31d505c513f889f9e300e715613e2353eead)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#max_iops_per_tb FilestoreInstance#max_iops_per_tb}
        '''
        result = self._values.get("max_iops_per_tb")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FilestoreInstancePerformanceConfigIopsPerTb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FilestoreInstancePerformanceConfigIopsPerTbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstancePerformanceConfigIopsPerTbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95f06ed027c90582a3373d1072a711ca8304e80c64e3f149a8e5463a931c955b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebcbef563983372480cd24afb161cf0f411e7110906964f106aba7a8484ba8d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIopsPerTb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FilestoreInstancePerformanceConfigIopsPerTb]:
        return typing.cast(typing.Optional[FilestoreInstancePerformanceConfigIopsPerTb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FilestoreInstancePerformanceConfigIopsPerTb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4dc23568eca1b8dfefff96bd488fb0877485f542e89d3447346fcf37c44439e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FilestoreInstancePerformanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstancePerformanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c8f2bdb290e90116791d27c27e7e9b69e0257fcdb69319643692eae1591aeeb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFixedIops")
    def put_fixed_iops(self, *, max_iops: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param max_iops: The number of IOPS to provision for the instance. max_iops must be in multiple of 1000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#max_iops FilestoreInstance#max_iops}
        '''
        value = FilestoreInstancePerformanceConfigFixedIops(max_iops=max_iops)

        return typing.cast(None, jsii.invoke(self, "putFixedIops", [value]))

    @jsii.member(jsii_name="putIopsPerTb")
    def put_iops_per_tb(
        self,
        *,
        max_iops_per_tb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_iops_per_tb: The instance max IOPS will be calculated by multiplying the capacity of the instance (TB) by max_iops_per_tb, and rounding to the nearest 1000. The instance max IOPS will be changed dynamically based on the instance capacity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#max_iops_per_tb FilestoreInstance#max_iops_per_tb}
        '''
        value = FilestoreInstancePerformanceConfigIopsPerTb(
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
    def fixed_iops(self) -> FilestoreInstancePerformanceConfigFixedIopsOutputReference:
        return typing.cast(FilestoreInstancePerformanceConfigFixedIopsOutputReference, jsii.get(self, "fixedIops"))

    @builtins.property
    @jsii.member(jsii_name="iopsPerTb")
    def iops_per_tb(self) -> FilestoreInstancePerformanceConfigIopsPerTbOutputReference:
        return typing.cast(FilestoreInstancePerformanceConfigIopsPerTbOutputReference, jsii.get(self, "iopsPerTb"))

    @builtins.property
    @jsii.member(jsii_name="fixedIopsInput")
    def fixed_iops_input(
        self,
    ) -> typing.Optional[FilestoreInstancePerformanceConfigFixedIops]:
        return typing.cast(typing.Optional[FilestoreInstancePerformanceConfigFixedIops], jsii.get(self, "fixedIopsInput"))

    @builtins.property
    @jsii.member(jsii_name="iopsPerTbInput")
    def iops_per_tb_input(
        self,
    ) -> typing.Optional[FilestoreInstancePerformanceConfigIopsPerTb]:
        return typing.cast(typing.Optional[FilestoreInstancePerformanceConfigIopsPerTb], jsii.get(self, "iopsPerTbInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FilestoreInstancePerformanceConfig]:
        return typing.cast(typing.Optional[FilestoreInstancePerformanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FilestoreInstancePerformanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52d3f019749927a39d4fdfe958ae73c95ebf4ded4986c67d6ec131c6d572a995)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class FilestoreInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#create FilestoreInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#delete FilestoreInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#update FilestoreInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26d7f5d375fefc29ef07597a9cd628291f3004d447a461aff6394314fca4a917)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#create FilestoreInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#delete FilestoreInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/filestore_instance#update FilestoreInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FilestoreInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FilestoreInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.filestoreInstance.FilestoreInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8ce5f04735b02a9e8f084e7e4659b1e4186fb5c7919e90029aecc26ec8a8c5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a65d5161b650b7bbb3e516324afb198274e30008e2fa48ad629eced6e5c8af0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3205ebd16786780225cea5855a916ae97b08e43c464b0a6763f30b71c261b01d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__630190084d09c121c03fa8af8a7db616a214e113a6023d0e5a7ea695605d629a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FilestoreInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FilestoreInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FilestoreInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19dee96e0ebaaf2b103efeafac0295c03dafcd18b32f0759af17f860092f5f6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "FilestoreInstance",
    "FilestoreInstanceConfig",
    "FilestoreInstanceEffectiveReplication",
    "FilestoreInstanceEffectiveReplicationList",
    "FilestoreInstanceEffectiveReplicationOutputReference",
    "FilestoreInstanceEffectiveReplicationReplicas",
    "FilestoreInstanceEffectiveReplicationReplicasList",
    "FilestoreInstanceEffectiveReplicationReplicasOutputReference",
    "FilestoreInstanceFileShares",
    "FilestoreInstanceFileSharesNfsExportOptions",
    "FilestoreInstanceFileSharesNfsExportOptionsList",
    "FilestoreInstanceFileSharesNfsExportOptionsOutputReference",
    "FilestoreInstanceFileSharesOutputReference",
    "FilestoreInstanceInitialReplication",
    "FilestoreInstanceInitialReplicationOutputReference",
    "FilestoreInstanceInitialReplicationReplicas",
    "FilestoreInstanceInitialReplicationReplicasList",
    "FilestoreInstanceInitialReplicationReplicasOutputReference",
    "FilestoreInstanceNetworks",
    "FilestoreInstanceNetworksList",
    "FilestoreInstanceNetworksOutputReference",
    "FilestoreInstancePerformanceConfig",
    "FilestoreInstancePerformanceConfigFixedIops",
    "FilestoreInstancePerformanceConfigFixedIopsOutputReference",
    "FilestoreInstancePerformanceConfigIopsPerTb",
    "FilestoreInstancePerformanceConfigIopsPerTbOutputReference",
    "FilestoreInstancePerformanceConfigOutputReference",
    "FilestoreInstanceTimeouts",
    "FilestoreInstanceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__85347811711caef03bbff6021f42be93d19ec7bee5d913457707f128201a62ee(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    file_shares: typing.Union[FilestoreInstanceFileShares, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    networks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FilestoreInstanceNetworks, typing.Dict[builtins.str, typing.Any]]]],
    tier: builtins.str,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deletion_protection_reason: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    initial_replication: typing.Optional[typing.Union[FilestoreInstanceInitialReplication, typing.Dict[builtins.str, typing.Any]]] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    performance_config: typing.Optional[typing.Union[FilestoreInstancePerformanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[FilestoreInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d47c3174eed7f4866aafeda0e58d94ae36ff02d0365371f5bac98cf9ed1bf52e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a266fe5121f906fad86ad03cbf451d043ca9886e34cbc3a9b4c93f2f788e7fd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FilestoreInstanceNetworks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c69c169821047f9a4e5de5d5affed5aee8aeba097d1f8e34deb20eb89767004e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b90e5cc8351b490799c120082d705b31ac91e98486d85e21257274f344d5cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa141b1a75ae66610ce7c0033db5af77999ae4999f9edb6e15e6b05cd328a22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6154b1ad32ae6a1f4a89c470e9552bca4cfa2d942e29ff61dcafd3658b1b01b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2bcdc11d144edbac1600623b1fdad90f84030237279d215285b28822517a78a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a017b7b97be0e045de649421cbd018e28d04637250512909fe6d953bbe6dc06d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bbb405e6d73da82850f5fe0176af4bf1aba7dda0e6e0477f3b42a522749e1d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c81081de52a6a692b58db18610b6839e2578cd5172f906ff0b30bfc1a93478d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381b4685dacc732ff726b61c265983d72294601b8162d7e5cb6f85906e4fa6ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c99be7fa1c4828207135fb5c7268fb3c76d0f9d3c032c25a1a46fd47d24bcb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b95d75fdb9e2c3f2cf27a07fbaf7e418dd01c77022aa55c31505808edcc41c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13377d598ba026afd7fe5f9d89b2183c35e993151ab52d2d573c528eb4faf4c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d354abbc4e1bd438643d6e9fcea39806f193eaa90227f360689dc0de59713e0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aea3047c69df2917fca515d54c1b0a5677e0be7b826c7b390b52d7e5878a292(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    file_shares: typing.Union[FilestoreInstanceFileShares, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    networks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FilestoreInstanceNetworks, typing.Dict[builtins.str, typing.Any]]]],
    tier: builtins.str,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deletion_protection_reason: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    initial_replication: typing.Optional[typing.Union[FilestoreInstanceInitialReplication, typing.Dict[builtins.str, typing.Any]]] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    performance_config: typing.Optional[typing.Union[FilestoreInstancePerformanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[FilestoreInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57e17e6d79121f339de8250da40a7fa79963657f62009e3640e9ca518453167b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2cb9e02f8515be73252e6670563b886fbb3e87308e6551c9f20fc8e9e4d048b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c15831b0606ca3c26d9ef1814d861c71602b0c331500daeb0577c5db8c5701(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02796c15ffb2f9aa29145b0df9ba84f83a65ad5ce036cc9ac0d249167682a510(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53454e677a6786232f1f5400d58d4ca0473b82f6f996f86cbf43d3a45d83244b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce2b339d49ac8c71eec508d99148596aa8bd370021906dd24057bb691a7adab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50d373876aaeeaf5cfa1d4d80e0c9f72f55e2d9be1800237dad444d061d9bcf(
    value: typing.Optional[FilestoreInstanceEffectiveReplication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55457c71dfe426fb847200fe90ba562174f1f9b2841461d31a4c49101b15f757(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aa1ed13ac6191c97a62d84978e96794b2b2e6085790b074dbfa38b0ebb78683(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a688d5a01f71e45e73badce5e260b02208cbb6a101b5802e1f6b7c497ae2485(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2709089001deb2d759e9a9bc066b1049cfd1aa5735bb9ed805a8433408192358(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ea094a2a903a86c9f19c47068447fccc3794127ef175df6b166ee5f35a0ca79(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__667d5f1e9e7a1be7ae8a398bf4b873d823baf1028b3d6b27abf1a0b480dbabfc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc6b954ffdd9a5194a92302f8f4384b01c58de24cd4ae8100c97db61cbde94b(
    value: typing.Optional[FilestoreInstanceEffectiveReplicationReplicas],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a40f8b69cdf281b74186cad919d58f821b4db1d9da73ef69c2ced566c139e8c(
    *,
    capacity_gb: jsii.Number,
    name: builtins.str,
    nfs_export_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FilestoreInstanceFileSharesNfsExportOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    source_backup: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f09240d8c8c9b3e435c80fe9941d148c197d156089b176c38622b10494b359(
    *,
    access_mode: typing.Optional[builtins.str] = None,
    anon_gid: typing.Optional[jsii.Number] = None,
    anon_uid: typing.Optional[jsii.Number] = None,
    ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    squash_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61985706813f731b5da45b53212cdb5d5c780ba1e1cd4331ccbb83fb96056c0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd98b350530e2a00dfeb626de82b909b4a62c7be4aa0ec03a76d0c8cf461c899(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__761ccb816aeeedd6f230c754d99442ce63f8285ad905d8f694b412f3d07c2034(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14215a7bd07ccf32eb893ff0b69fd8002c133f5dae5fefd05fe68496f5a88003(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__891c13e125a3b33f40adafd88893402aab2adb5b6ce6791f176aa4e98b7e5f63(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20d49d59b69467e8a9eb124ecfa671c2eab47c54da37db879d56d4b9809cc743(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FilestoreInstanceFileSharesNfsExportOptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5906d92fb64a7667148c36eb855abd8f295c52f72befc5fc3835f00039b8c9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d997102f15e6076686661f163209bafcbd09296568e99e69975f6f9bf0ecb4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5813d60bd69a5951afb45488e1d1c6f8cf9f78f8701111b5837c36e7dbfe6be(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c86fa2f386a67c57b29ac080b19fe9240531e0b953ecf113b4cdccc387875db2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2686eeff31b8b7404907d5094736e67cd0f62325ec139fd6aee988a24f7f08a6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fad6687e40a770145d7e390b519aeff14dd36e6bc3c566181f85183c32c4c0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c886894bbb25c6811068b5dd8742b1bf7f04dc5e1bea4d09629a84fc920a4f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FilestoreInstanceFileSharesNfsExportOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__003d4cc20d5e398d9e6a296700349e84b98cc7db90c9328fa6bfc3ebcc13aab6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24fa889c7179cdcff1e4a61351246ec41b45a38e603309fc8c325bafb6892f5e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FilestoreInstanceFileSharesNfsExportOptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4cdfdb1c0fc251a36faf18bf4e4cf281ca16b64e907154335d408b009b2e228(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca38d07222d27e5dbbaea1c3f9c69a90518de727c9d08612666082b93c0a4b2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66657cbb20ce4752dad0bf6dab69554633cdbf68b2ac84b931970895be64ff29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__166c2b2395fab8f079be05e1593a3794d94305f3f0814362db60c8c5f5603cac(
    value: typing.Optional[FilestoreInstanceFileShares],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa0d44d3d1a30d071310d2b83f08756f1dd1efd44a41a5c3d00a7787949247d(
    *,
    replicas: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FilestoreInstanceInitialReplicationReplicas, typing.Dict[builtins.str, typing.Any]]]]] = None,
    role: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8df9ccfcf18c3204c507d99a599f892f94ec98bca941aa72d66fd4d45a19343(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0fa64e3dbeada48232e1ca65714e703ca276d8da0f2a07af5793b52904c7b80(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FilestoreInstanceInitialReplicationReplicas, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad2197855377f81eca34de9d49110b7934adbd131faf9d04d98d450adc18353(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d08e5f63f9a7e53c10cabaee72d4118875310fe769c4a673e5a1cb5d2c06c9(
    value: typing.Optional[FilestoreInstanceInitialReplication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efde858380367303244ba90cd00962b1bbfcf6e82ecdaf8f146a209e011a6cc5(
    *,
    peer_instance: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4499ee913d38976c818c95972c20ce14f3f8443448bbab67ca73584f2b1ab1ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cf00d4f64f1c409ee6cfb07af7708bdafb4b839430a50a4ee9e8e10b9aac1a4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc80ef4d0576b89ed9fcf15578de9938b2cdee705d151dd4aab4e2b0a80e7536(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e492868702d17060eafc10c4b7499355a47161b2e0d506aba7eb1a61937411e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__002456282e62427fd5e5173d8cd5e337c3d076bce1f35116b1dcae3db345e0c0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f5ef6ff7179a77248a5c7ea2dcb7482182777e1d7ab94968a710c90bea794a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FilestoreInstanceInitialReplicationReplicas]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__032498d3008c0e49b4005ac4290590ea7c6de23d3a0f6eaba52f8cab68629cd1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3230591eab22d91a8d842b5f8fe25d14f2853d3e66118530e465a9d2a77e24e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38f685877db515970a4a9131ea82591f79b781f3f170526beeba14a71d693c34(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FilestoreInstanceInitialReplicationReplicas]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41dfd05f7041ba508f286713c57a6b5bd20d04ee126faf0ddc92b4bd1edc218a(
    *,
    modes: typing.Sequence[builtins.str],
    network: builtins.str,
    connect_mode: typing.Optional[builtins.str] = None,
    reserved_ip_range: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f563e8302497b28afc9ff9973ddb85471c2d2a977b39bea8b0c7ab73bed8de4a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2346738f5d38a607bc169168d152ad6b6a71dddbc5940ebafebf6717033095(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb3fcdc378391617c8764d6c61246bb437416713b7ba2fd3914960208c926e83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b81fda9576acd8caf6514ac40ad39664a23d071cd7bee70a6399a6902b62516c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4285a8156e9b6f9ec4c6e5a4ee8e6a72b934cf1724654588d06cb775b427356f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6581c388d6bc27072a525e181075ac23d9d561ebadbec8b92fd18b3b350af6b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FilestoreInstanceNetworks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de14cd710b9551b74a7582bb26db5a34e4fcc6b9493aa22993329dc387a0bad3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdf431b54bfeacf9e5ab27da23cc59c18a393f7da0563398ceb330108d99cfbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad32dda00cdc0c667b9be5f11f6c79ac869588823ca9f6605cd691a89cbc7ba(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdec87675b8e500b93ff408bd21344f36efeeea35bb7d4502dc92087ccf9aaed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b76bcab831f5ac302b49a32396c55e203f954be139e5b2524a86e0daadbfac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b78e1af4403bda3b964336d5237403d40a4811e794bd28147494847bf9956c16(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FilestoreInstanceNetworks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5fd6202b38e8582b1b61efde96c77fef6dcf931a35f57bd4591559e00766d50(
    *,
    fixed_iops: typing.Optional[typing.Union[FilestoreInstancePerformanceConfigFixedIops, typing.Dict[builtins.str, typing.Any]]] = None,
    iops_per_tb: typing.Optional[typing.Union[FilestoreInstancePerformanceConfigIopsPerTb, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0846d0ad2d4098f7afa8b94685f06482d71e688be1a83a3e0f8371784e18f05e(
    *,
    max_iops: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ef9c03acd10e9f73819967c5750593e6d0240e60149a26bb7c3c608579a4d88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__071067b411509305ac4c66201660cf7bdb91a96eb47515ea5093b9f11eba6908(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cf830d96d1e9ef93c4b64e90e8d188bab84041228fdc0a9ea06d8fe576989ef(
    value: typing.Optional[FilestoreInstancePerformanceConfigFixedIops],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882397484c1807d7fa9bd0ec842d31d505c513f889f9e300e715613e2353eead(
    *,
    max_iops_per_tb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f06ed027c90582a3373d1072a711ca8304e80c64e3f149a8e5463a931c955b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebcbef563983372480cd24afb161cf0f411e7110906964f106aba7a8484ba8d2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4dc23568eca1b8dfefff96bd488fb0877485f542e89d3447346fcf37c44439e(
    value: typing.Optional[FilestoreInstancePerformanceConfigIopsPerTb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c8f2bdb290e90116791d27c27e7e9b69e0257fcdb69319643692eae1591aeeb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52d3f019749927a39d4fdfe958ae73c95ebf4ded4986c67d6ec131c6d572a995(
    value: typing.Optional[FilestoreInstancePerformanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26d7f5d375fefc29ef07597a9cd628291f3004d447a461aff6394314fca4a917(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8ce5f04735b02a9e8f084e7e4659b1e4186fb5c7919e90029aecc26ec8a8c5d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a65d5161b650b7bbb3e516324afb198274e30008e2fa48ad629eced6e5c8af0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3205ebd16786780225cea5855a916ae97b08e43c464b0a6763f30b71c261b01d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630190084d09c121c03fa8af8a7db616a214e113a6023d0e5a7ea695605d629a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19dee96e0ebaaf2b103efeafac0295c03dafcd18b32f0759af17f860092f5f6e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FilestoreInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
