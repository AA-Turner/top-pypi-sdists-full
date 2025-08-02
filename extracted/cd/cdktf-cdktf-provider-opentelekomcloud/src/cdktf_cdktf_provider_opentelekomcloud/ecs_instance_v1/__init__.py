r'''
# `opentelekomcloud_ecs_instance_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_ecs_instance_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1).
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


class EcsInstanceV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ecsInstanceV1.EcsInstanceV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1 opentelekomcloud_ecs_instance_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        flavor: builtins.str,
        image_id: builtins.str,
        name: builtins.str,
        nics: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EcsInstanceV1Nics", typing.Dict[builtins.str, typing.Any]]]],
        vpc_id: builtins.str,
        auto_recovery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        data_disks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EcsInstanceV1DataDisks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        delete_disks_on_termination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        key_name: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Union["EcsInstanceV1Metadata", typing.Dict[builtins.str, typing.Any]]] = None,
        os_scheduler_hints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EcsInstanceV1OsSchedulerHints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        password: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        system_disk_kms_id: typing.Optional[builtins.str] = None,
        system_disk_size: typing.Optional[jsii.Number] = None,
        system_disk_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["EcsInstanceV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_data: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1 opentelekomcloud_ecs_instance_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#flavor EcsInstanceV1#flavor}.
        :param image_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#image_id EcsInstanceV1#image_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#name EcsInstanceV1#name}.
        :param nics: nics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#nics EcsInstanceV1#nics}
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#vpc_id EcsInstanceV1#vpc_id}.
        :param auto_recovery: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#auto_recovery EcsInstanceV1#auto_recovery}.
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#availability_zone EcsInstanceV1#availability_zone}.
        :param data_disks: data_disks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#data_disks EcsInstanceV1#data_disks}
        :param delete_disks_on_termination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#delete_disks_on_termination EcsInstanceV1#delete_disks_on_termination}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#id EcsInstanceV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#key_name EcsInstanceV1#key_name}.
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#metadata EcsInstanceV1#metadata}
        :param os_scheduler_hints: os_scheduler_hints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#os_scheduler_hints EcsInstanceV1#os_scheduler_hints}
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#password EcsInstanceV1#password}.
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#security_groups EcsInstanceV1#security_groups}.
        :param system_disk_kms_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#system_disk_kms_id EcsInstanceV1#system_disk_kms_id}.
        :param system_disk_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#system_disk_size EcsInstanceV1#system_disk_size}.
        :param system_disk_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#system_disk_type EcsInstanceV1#system_disk_type}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#tags EcsInstanceV1#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#timeouts EcsInstanceV1#timeouts}
        :param user_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#user_data EcsInstanceV1#user_data}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96244114cb7df1f914941bdd0b405c08f0085c85246b3f01fffeb44b8c9b5650)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EcsInstanceV1Config(
            flavor=flavor,
            image_id=image_id,
            name=name,
            nics=nics,
            vpc_id=vpc_id,
            auto_recovery=auto_recovery,
            availability_zone=availability_zone,
            data_disks=data_disks,
            delete_disks_on_termination=delete_disks_on_termination,
            id=id,
            key_name=key_name,
            metadata=metadata,
            os_scheduler_hints=os_scheduler_hints,
            password=password,
            security_groups=security_groups,
            system_disk_kms_id=system_disk_kms_id,
            system_disk_size=system_disk_size,
            system_disk_type=system_disk_type,
            tags=tags,
            timeouts=timeouts,
            user_data=user_data,
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
        '''Generates CDKTF code for importing a EcsInstanceV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EcsInstanceV1 to import.
        :param import_from_id: The id of the existing EcsInstanceV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EcsInstanceV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__342405298025e5b109b2de2b0cc3ca610577306ac70c4724b15a6dd56c54e4a9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDataDisks")
    def put_data_disks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EcsInstanceV1DataDisks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72c4a26716d73d61cfae9c4d122fea5a08d5801cbf76194008a3030acc6b8392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataDisks", [value]))

    @jsii.member(jsii_name="putMetadata")
    def put_metadata(
        self,
        *,
        agency_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param agency_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#agency_name EcsInstanceV1#agency_name}.
        '''
        value = EcsInstanceV1Metadata(agency_name=agency_name)

        return typing.cast(None, jsii.invoke(self, "putMetadata", [value]))

    @jsii.member(jsii_name="putNics")
    def put_nics(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EcsInstanceV1Nics", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe5121df134a409faf493ee936997e89eefe50a317609698727e58c05fc73df8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNics", [value]))

    @jsii.member(jsii_name="putOsSchedulerHints")
    def put_os_scheduler_hints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EcsInstanceV1OsSchedulerHints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8f319c45d0dd790c68d5cbb0ad49bc5d7d1883b763232d30774869580b9e3a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOsSchedulerHints", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#create EcsInstanceV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#delete EcsInstanceV1#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#update EcsInstanceV1#update}.
        '''
        value = EcsInstanceV1Timeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAutoRecovery")
    def reset_auto_recovery(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoRecovery", []))

    @jsii.member(jsii_name="resetAvailabilityZone")
    def reset_availability_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityZone", []))

    @jsii.member(jsii_name="resetDataDisks")
    def reset_data_disks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataDisks", []))

    @jsii.member(jsii_name="resetDeleteDisksOnTermination")
    def reset_delete_disks_on_termination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteDisksOnTermination", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKeyName")
    def reset_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyName", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetOsSchedulerHints")
    def reset_os_scheduler_hints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsSchedulerHints", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetSecurityGroups")
    def reset_security_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroups", []))

    @jsii.member(jsii_name="resetSystemDiskKmsId")
    def reset_system_disk_kms_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemDiskKmsId", []))

    @jsii.member(jsii_name="resetSystemDiskSize")
    def reset_system_disk_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemDiskSize", []))

    @jsii.member(jsii_name="resetSystemDiskType")
    def reset_system_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemDiskType", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUserData")
    def reset_user_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserData", []))

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
    @jsii.member(jsii_name="dataDisks")
    def data_disks(self) -> "EcsInstanceV1DataDisksList":
        return typing.cast("EcsInstanceV1DataDisksList", jsii.get(self, "dataDisks"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> "EcsInstanceV1MetadataOutputReference":
        return typing.cast("EcsInstanceV1MetadataOutputReference", jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="nics")
    def nics(self) -> "EcsInstanceV1NicsList":
        return typing.cast("EcsInstanceV1NicsList", jsii.get(self, "nics"))

    @builtins.property
    @jsii.member(jsii_name="osSchedulerHints")
    def os_scheduler_hints(self) -> "EcsInstanceV1OsSchedulerHintsList":
        return typing.cast("EcsInstanceV1OsSchedulerHintsList", jsii.get(self, "osSchedulerHints"))

    @builtins.property
    @jsii.member(jsii_name="systemDiskId")
    def system_disk_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "systemDiskId"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "EcsInstanceV1TimeoutsOutputReference":
        return typing.cast("EcsInstanceV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="volumesAttached")
    def volumes_attached(self) -> "EcsInstanceV1VolumesAttachedList":
        return typing.cast("EcsInstanceV1VolumesAttachedList", jsii.get(self, "volumesAttached"))

    @builtins.property
    @jsii.member(jsii_name="autoRecoveryInput")
    def auto_recovery_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoRecoveryInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneInput")
    def availability_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="dataDisksInput")
    def data_disks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EcsInstanceV1DataDisks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EcsInstanceV1DataDisks"]]], jsii.get(self, "dataDisksInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteDisksOnTerminationInput")
    def delete_disks_on_termination_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteDisksOnTerminationInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorInput")
    def flavor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageIdInput")
    def image_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyNameInput")
    def key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional["EcsInstanceV1Metadata"]:
        return typing.cast(typing.Optional["EcsInstanceV1Metadata"], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nicsInput")
    def nics_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EcsInstanceV1Nics"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EcsInstanceV1Nics"]]], jsii.get(self, "nicsInput"))

    @builtins.property
    @jsii.member(jsii_name="osSchedulerHintsInput")
    def os_scheduler_hints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EcsInstanceV1OsSchedulerHints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EcsInstanceV1OsSchedulerHints"]]], jsii.get(self, "osSchedulerHintsInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupsInput")
    def security_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="systemDiskKmsIdInput")
    def system_disk_kms_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "systemDiskKmsIdInput"))

    @builtins.property
    @jsii.member(jsii_name="systemDiskSizeInput")
    def system_disk_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "systemDiskSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="systemDiskTypeInput")
    def system_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "systemDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EcsInstanceV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EcsInstanceV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userDataInput")
    def user_data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userDataInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="autoRecovery")
    def auto_recovery(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoRecovery"))

    @auto_recovery.setter
    def auto_recovery(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45b41ebf653ed600bb7ea400a0001fab64f53ae5d6a8a00b662bc497f74eb5b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoRecovery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff97261196b82fb67316722b514fc3ce7daf652658538e9cffb940d9c1834bc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteDisksOnTermination")
    def delete_disks_on_termination(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteDisksOnTermination"))

    @delete_disks_on_termination.setter
    def delete_disks_on_termination(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af2ba6eacd20710c008f717bce02870d2db952aee6edf7b7756af85dc2191bf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteDisksOnTermination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flavor")
    def flavor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavor"))

    @flavor.setter
    def flavor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c732075738c830d512bd6ed7708ebbaff93d035124dd5e474e02e547954a744)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17866ac6bf095ef27feb31747d99aaa083b3bbf3605dee42118c149e5ee80b50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageId"))

    @image_id.setter
    def image_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5517509a5d9c97fc75d0ecf5844f32b9b0acba9160f4aab595b372cb22a7db0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyName")
    def key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyName"))

    @key_name.setter
    def key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6393aaad3030eb6418d1851f0c69e7c871fe0accf78de5608705f9fa1f971bf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc0f26ae5bb9f8e11b43207b9277f43c09a5f60184d439f5a75823e6d9cf1e36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2885b1f2b290d4ef48db0723e68de227b9729672620999251f1762e3f8f2ab72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroups"))

    @security_groups.setter
    def security_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e9b2e40ccff46df545bac2b9161e4b86dd3a0eeed97791223018cf1e19fb3e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemDiskKmsId")
    def system_disk_kms_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "systemDiskKmsId"))

    @system_disk_kms_id.setter
    def system_disk_kms_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6232d91329c62866f7c54ebfe461d61010625ea1fe5424e7a138c252daf7da92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemDiskKmsId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemDiskSize")
    def system_disk_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "systemDiskSize"))

    @system_disk_size.setter
    def system_disk_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__963713dc3753cad3d8453587f528da06e75d6cc4df8670c77eb9494af26357f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemDiskSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemDiskType")
    def system_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "systemDiskType"))

    @system_disk_type.setter
    def system_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2251f5746c417d1a6a6e9b1f9342bb43c879308d6927394a9ee1b68f684dadcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemDiskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a149f5007e462e21528daa54fbff0cf0b89548d140c4db095eedab7ee0412c45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userData")
    def user_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userData"))

    @user_data.setter
    def user_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3291e5c34c91865258934a19b4d1a93bf04e02d6002dbd895c31ab9c64d08b6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4684386d34d8a4ea88fdf3d89ed6b286bc2ae0f70cb46fab4abc2df429e8001f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ecsInstanceV1.EcsInstanceV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "flavor": "flavor",
        "image_id": "imageId",
        "name": "name",
        "nics": "nics",
        "vpc_id": "vpcId",
        "auto_recovery": "autoRecovery",
        "availability_zone": "availabilityZone",
        "data_disks": "dataDisks",
        "delete_disks_on_termination": "deleteDisksOnTermination",
        "id": "id",
        "key_name": "keyName",
        "metadata": "metadata",
        "os_scheduler_hints": "osSchedulerHints",
        "password": "password",
        "security_groups": "securityGroups",
        "system_disk_kms_id": "systemDiskKmsId",
        "system_disk_size": "systemDiskSize",
        "system_disk_type": "systemDiskType",
        "tags": "tags",
        "timeouts": "timeouts",
        "user_data": "userData",
    },
)
class EcsInstanceV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        flavor: builtins.str,
        image_id: builtins.str,
        name: builtins.str,
        nics: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EcsInstanceV1Nics", typing.Dict[builtins.str, typing.Any]]]],
        vpc_id: builtins.str,
        auto_recovery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        data_disks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EcsInstanceV1DataDisks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        delete_disks_on_termination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        key_name: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Union["EcsInstanceV1Metadata", typing.Dict[builtins.str, typing.Any]]] = None,
        os_scheduler_hints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EcsInstanceV1OsSchedulerHints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        password: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        system_disk_kms_id: typing.Optional[builtins.str] = None,
        system_disk_size: typing.Optional[jsii.Number] = None,
        system_disk_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["EcsInstanceV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_data: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#flavor EcsInstanceV1#flavor}.
        :param image_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#image_id EcsInstanceV1#image_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#name EcsInstanceV1#name}.
        :param nics: nics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#nics EcsInstanceV1#nics}
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#vpc_id EcsInstanceV1#vpc_id}.
        :param auto_recovery: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#auto_recovery EcsInstanceV1#auto_recovery}.
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#availability_zone EcsInstanceV1#availability_zone}.
        :param data_disks: data_disks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#data_disks EcsInstanceV1#data_disks}
        :param delete_disks_on_termination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#delete_disks_on_termination EcsInstanceV1#delete_disks_on_termination}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#id EcsInstanceV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#key_name EcsInstanceV1#key_name}.
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#metadata EcsInstanceV1#metadata}
        :param os_scheduler_hints: os_scheduler_hints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#os_scheduler_hints EcsInstanceV1#os_scheduler_hints}
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#password EcsInstanceV1#password}.
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#security_groups EcsInstanceV1#security_groups}.
        :param system_disk_kms_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#system_disk_kms_id EcsInstanceV1#system_disk_kms_id}.
        :param system_disk_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#system_disk_size EcsInstanceV1#system_disk_size}.
        :param system_disk_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#system_disk_type EcsInstanceV1#system_disk_type}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#tags EcsInstanceV1#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#timeouts EcsInstanceV1#timeouts}
        :param user_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#user_data EcsInstanceV1#user_data}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(metadata, dict):
            metadata = EcsInstanceV1Metadata(**metadata)
        if isinstance(timeouts, dict):
            timeouts = EcsInstanceV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__282714a43369c85da130cddb5a566dc8c682b6a4fb6315ca63311ba505050095)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument flavor", value=flavor, expected_type=type_hints["flavor"])
            check_type(argname="argument image_id", value=image_id, expected_type=type_hints["image_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument nics", value=nics, expected_type=type_hints["nics"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument auto_recovery", value=auto_recovery, expected_type=type_hints["auto_recovery"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument data_disks", value=data_disks, expected_type=type_hints["data_disks"])
            check_type(argname="argument delete_disks_on_termination", value=delete_disks_on_termination, expected_type=type_hints["delete_disks_on_termination"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument os_scheduler_hints", value=os_scheduler_hints, expected_type=type_hints["os_scheduler_hints"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument system_disk_kms_id", value=system_disk_kms_id, expected_type=type_hints["system_disk_kms_id"])
            check_type(argname="argument system_disk_size", value=system_disk_size, expected_type=type_hints["system_disk_size"])
            check_type(argname="argument system_disk_type", value=system_disk_type, expected_type=type_hints["system_disk_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "flavor": flavor,
            "image_id": image_id,
            "name": name,
            "nics": nics,
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
        if auto_recovery is not None:
            self._values["auto_recovery"] = auto_recovery
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if data_disks is not None:
            self._values["data_disks"] = data_disks
        if delete_disks_on_termination is not None:
            self._values["delete_disks_on_termination"] = delete_disks_on_termination
        if id is not None:
            self._values["id"] = id
        if key_name is not None:
            self._values["key_name"] = key_name
        if metadata is not None:
            self._values["metadata"] = metadata
        if os_scheduler_hints is not None:
            self._values["os_scheduler_hints"] = os_scheduler_hints
        if password is not None:
            self._values["password"] = password
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if system_disk_kms_id is not None:
            self._values["system_disk_kms_id"] = system_disk_kms_id
        if system_disk_size is not None:
            self._values["system_disk_size"] = system_disk_size
        if system_disk_type is not None:
            self._values["system_disk_type"] = system_disk_type
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if user_data is not None:
            self._values["user_data"] = user_data

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
    def flavor(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#flavor EcsInstanceV1#flavor}.'''
        result = self._values.get("flavor")
        assert result is not None, "Required property 'flavor' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#image_id EcsInstanceV1#image_id}.'''
        result = self._values.get("image_id")
        assert result is not None, "Required property 'image_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#name EcsInstanceV1#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def nics(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EcsInstanceV1Nics"]]:
        '''nics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#nics EcsInstanceV1#nics}
        '''
        result = self._values.get("nics")
        assert result is not None, "Required property 'nics' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EcsInstanceV1Nics"]], result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#vpc_id EcsInstanceV1#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_recovery(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#auto_recovery EcsInstanceV1#auto_recovery}.'''
        result = self._values.get("auto_recovery")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#availability_zone EcsInstanceV1#availability_zone}.'''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_disks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EcsInstanceV1DataDisks"]]]:
        '''data_disks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#data_disks EcsInstanceV1#data_disks}
        '''
        result = self._values.get("data_disks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EcsInstanceV1DataDisks"]]], result)

    @builtins.property
    def delete_disks_on_termination(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#delete_disks_on_termination EcsInstanceV1#delete_disks_on_termination}.'''
        result = self._values.get("delete_disks_on_termination")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#id EcsInstanceV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#key_name EcsInstanceV1#key_name}.'''
        result = self._values.get("key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional["EcsInstanceV1Metadata"]:
        '''metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#metadata EcsInstanceV1#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional["EcsInstanceV1Metadata"], result)

    @builtins.property
    def os_scheduler_hints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EcsInstanceV1OsSchedulerHints"]]]:
        '''os_scheduler_hints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#os_scheduler_hints EcsInstanceV1#os_scheduler_hints}
        '''
        result = self._values.get("os_scheduler_hints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EcsInstanceV1OsSchedulerHints"]]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#password EcsInstanceV1#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#security_groups EcsInstanceV1#security_groups}.'''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def system_disk_kms_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#system_disk_kms_id EcsInstanceV1#system_disk_kms_id}.'''
        result = self._values.get("system_disk_kms_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def system_disk_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#system_disk_size EcsInstanceV1#system_disk_size}.'''
        result = self._values.get("system_disk_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def system_disk_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#system_disk_type EcsInstanceV1#system_disk_type}.'''
        result = self._values.get("system_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#tags EcsInstanceV1#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["EcsInstanceV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#timeouts EcsInstanceV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["EcsInstanceV1Timeouts"], result)

    @builtins.property
    def user_data(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#user_data EcsInstanceV1#user_data}.'''
        result = self._values.get("user_data")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsInstanceV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ecsInstanceV1.EcsInstanceV1DataDisks",
    jsii_struct_bases=[],
    name_mapping={
        "size": "size",
        "type": "type",
        "kms_id": "kmsId",
        "snapshot_id": "snapshotId",
    },
)
class EcsInstanceV1DataDisks:
    def __init__(
        self,
        *,
        size: jsii.Number,
        type: builtins.str,
        kms_id: typing.Optional[builtins.str] = None,
        snapshot_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#size EcsInstanceV1#size}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#type EcsInstanceV1#type}.
        :param kms_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#kms_id EcsInstanceV1#kms_id}.
        :param snapshot_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#snapshot_id EcsInstanceV1#snapshot_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05989798e9bdddff730951c32d131463ee210e0f51928886a40819ea62699044)
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument kms_id", value=kms_id, expected_type=type_hints["kms_id"])
            check_type(argname="argument snapshot_id", value=snapshot_id, expected_type=type_hints["snapshot_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "size": size,
            "type": type,
        }
        if kms_id is not None:
            self._values["kms_id"] = kms_id
        if snapshot_id is not None:
            self._values["snapshot_id"] = snapshot_id

    @builtins.property
    def size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#size EcsInstanceV1#size}.'''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#type EcsInstanceV1#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#kms_id EcsInstanceV1#kms_id}.'''
        result = self._values.get("kms_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#snapshot_id EcsInstanceV1#snapshot_id}.'''
        result = self._values.get("snapshot_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsInstanceV1DataDisks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsInstanceV1DataDisksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ecsInstanceV1.EcsInstanceV1DataDisksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7be066e312c8db56c11cbf53fea21c3d0dd23fd7989a0e93df17fb6e23318d8a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EcsInstanceV1DataDisksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f326e67f2b8205c8edb63d7484107bd08d18e9da274789a6edeac4abb2b6d7df)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EcsInstanceV1DataDisksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8e20935ea7597c37b8549f0c0386f77ebcfbb7a576ea349d4700965561904ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__42dd16ca9b85f042cd9d6cd770b1b08e05b58cc7e8f78e2a132da1815ca4f340)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e91fe7944902956d10182b2c93494a271fe8be9282b033b94f00c6ac5f21b14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EcsInstanceV1DataDisks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EcsInstanceV1DataDisks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EcsInstanceV1DataDisks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b9522bf6636e802374e8e68dc3879b8f50a8b8ae8535973c066c8b07c04241f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EcsInstanceV1DataDisksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ecsInstanceV1.EcsInstanceV1DataDisksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48bcb0740958643426d4699d58a789b54d75150118faba184d61190ba33bc103)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKmsId")
    def reset_kms_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsId", []))

    @jsii.member(jsii_name="resetSnapshotId")
    def reset_snapshot_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshotId", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="kmsIdInput")
    def kms_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotIdInput")
    def snapshot_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotIdInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsId")
    def kms_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsId"))

    @kms_id.setter
    def kms_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dcd4e6b865e306782d58d441ad5a50c29fde336258c831f15a66e0632c70877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db46ae72bd17746c0f3300fea544172d610c227a43f8a8cb39c05fb05e166bcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotId")
    def snapshot_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snapshotId"))

    @snapshot_id.setter
    def snapshot_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a5bdb30120b8600b82b0a3f2718ec486594df2fcb9569308bc5a7caed802add)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__792811c772baccb468266e67392fbca77f596ffa19bc7174ecd87ee524778158)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EcsInstanceV1DataDisks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EcsInstanceV1DataDisks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EcsInstanceV1DataDisks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a72f06c5c62edf7f4e79f4c2246fbb5597962b9a6803a6b1e6ac9f3944c2ecbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ecsInstanceV1.EcsInstanceV1Metadata",
    jsii_struct_bases=[],
    name_mapping={"agency_name": "agencyName"},
)
class EcsInstanceV1Metadata:
    def __init__(self, *, agency_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param agency_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#agency_name EcsInstanceV1#agency_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__301d23ee6db65b613826b2a50b68b4a15b18c0b4d6dbec7763bae32bb9099f56)
            check_type(argname="argument agency_name", value=agency_name, expected_type=type_hints["agency_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if agency_name is not None:
            self._values["agency_name"] = agency_name

    @builtins.property
    def agency_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#agency_name EcsInstanceV1#agency_name}.'''
        result = self._values.get("agency_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsInstanceV1Metadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsInstanceV1MetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ecsInstanceV1.EcsInstanceV1MetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f268747b22f51ac17849feed431a203ef0ca03481a63b6beef5ea874ac92590)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAgencyName")
    def reset_agency_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgencyName", []))

    @builtins.property
    @jsii.member(jsii_name="agencyNameInput")
    def agency_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agencyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="agencyName")
    def agency_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agencyName"))

    @agency_name.setter
    def agency_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a55171e5223c2d03b5189ce80cb805da5df8274ad6ad6bf8268997fa01b9e059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agencyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EcsInstanceV1Metadata]:
        return typing.cast(typing.Optional[EcsInstanceV1Metadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EcsInstanceV1Metadata]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50cb403804e073f81caef0bdf50cd29d315c244be789eda81cb7d61abccada62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ecsInstanceV1.EcsInstanceV1Nics",
    jsii_struct_bases=[],
    name_mapping={
        "network_id": "networkId",
        "ip_address": "ipAddress",
        "ipv6_enable": "ipv6Enable",
    },
)
class EcsInstanceV1Nics:
    def __init__(
        self,
        *,
        network_id: builtins.str,
        ip_address: typing.Optional[builtins.str] = None,
        ipv6_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#network_id EcsInstanceV1#network_id}.
        :param ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#ip_address EcsInstanceV1#ip_address}.
        :param ipv6_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#ipv6_enable EcsInstanceV1#ipv6_enable}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__302dee08ca1f4b43d7cdcb6981c3f138c9aaac6993045e72bc52ca832eb979a3)
            check_type(argname="argument network_id", value=network_id, expected_type=type_hints["network_id"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument ipv6_enable", value=ipv6_enable, expected_type=type_hints["ipv6_enable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_id": network_id,
        }
        if ip_address is not None:
            self._values["ip_address"] = ip_address
        if ipv6_enable is not None:
            self._values["ipv6_enable"] = ipv6_enable

    @builtins.property
    def network_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#network_id EcsInstanceV1#network_id}.'''
        result = self._values.get("network_id")
        assert result is not None, "Required property 'network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#ip_address EcsInstanceV1#ip_address}.'''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv6_enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#ipv6_enable EcsInstanceV1#ipv6_enable}.'''
        result = self._values.get("ipv6_enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsInstanceV1Nics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsInstanceV1NicsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ecsInstanceV1.EcsInstanceV1NicsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7cc60cbc1da3e633d0262329c7391c45e103a6ff5888dd5f72e5749672005c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EcsInstanceV1NicsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3a5aedaee106caf7a8ce872309a5230758b13e8eab5f0022ffdffa98d019dfb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EcsInstanceV1NicsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46a2204fb5bfbff48bcc045c40a4442c4122e0b866dde68afa1279b9f7e10bbe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23db3bd648e9bac67fe12995e3989bdcd3aeb7256d42de4e233a78a60dc41ca5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e96c5f74361c1080871e2e45f57e5edc9bda29d1963fe1de1c466bca559e1e3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EcsInstanceV1Nics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EcsInstanceV1Nics]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EcsInstanceV1Nics]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0203e9ecd8e93778b394441d4c0c6266ee3770864189c75abf5defadce8f8ac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EcsInstanceV1NicsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ecsInstanceV1.EcsInstanceV1NicsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2710a4959378a5ae767a13103545347883817f62b50c0b9f246f35ff939d0ff7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @jsii.member(jsii_name="resetIpv6Enable")
    def reset_ipv6_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv6Enable", []))

    @builtins.property
    @jsii.member(jsii_name="ipv6Address")
    def ipv6_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6Address"))

    @builtins.property
    @jsii.member(jsii_name="macAddress")
    def mac_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "macAddress"))

    @builtins.property
    @jsii.member(jsii_name="portId")
    def port_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portId"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6EnableInput")
    def ipv6_enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ipv6EnableInput"))

    @builtins.property
    @jsii.member(jsii_name="networkIdInput")
    def network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62170ad44c3d3f563c504e04d30123420241dc8630f6ddf0cd256e50edc262b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv6Enable")
    def ipv6_enable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ipv6Enable"))

    @ipv6_enable.setter
    def ipv6_enable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__391162156129dadc63b4f71003affc2c08db6bdffc75060eeb99fdd05a0c5568)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6Enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkId")
    def network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkId"))

    @network_id.setter
    def network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825ccea9f6b4e7186cb8ac1f17b3e9f03d01c3eb127ce542bf5c3df17fc90b6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EcsInstanceV1Nics]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EcsInstanceV1Nics]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EcsInstanceV1Nics]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__859cebe938762e554d7cab7e8bef14f0e9871d36a56b145fe31cc55dfb86ed46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ecsInstanceV1.EcsInstanceV1OsSchedulerHints",
    jsii_struct_bases=[],
    name_mapping={
        "dedicated_host_id": "dedicatedHostId",
        "group": "group",
        "tenancy": "tenancy",
    },
)
class EcsInstanceV1OsSchedulerHints:
    def __init__(
        self,
        *,
        dedicated_host_id: typing.Optional[builtins.str] = None,
        group: typing.Optional[builtins.str] = None,
        tenancy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dedicated_host_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#dedicated_host_id EcsInstanceV1#dedicated_host_id}.
        :param group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#group EcsInstanceV1#group}.
        :param tenancy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#tenancy EcsInstanceV1#tenancy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a34ef2031c0862831474375bdd5f74312dd802cda618b13fe32e9836332e4063)
            check_type(argname="argument dedicated_host_id", value=dedicated_host_id, expected_type=type_hints["dedicated_host_id"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument tenancy", value=tenancy, expected_type=type_hints["tenancy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dedicated_host_id is not None:
            self._values["dedicated_host_id"] = dedicated_host_id
        if group is not None:
            self._values["group"] = group
        if tenancy is not None:
            self._values["tenancy"] = tenancy

    @builtins.property
    def dedicated_host_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#dedicated_host_id EcsInstanceV1#dedicated_host_id}.'''
        result = self._values.get("dedicated_host_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#group EcsInstanceV1#group}.'''
        result = self._values.get("group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenancy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#tenancy EcsInstanceV1#tenancy}.'''
        result = self._values.get("tenancy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsInstanceV1OsSchedulerHints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsInstanceV1OsSchedulerHintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ecsInstanceV1.EcsInstanceV1OsSchedulerHintsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a657638a1f05b570346cbf9645ca00867386b4e5b69f2750d59f7f8d2fa4bee1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EcsInstanceV1OsSchedulerHintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a747afb9d5610056965f5dd7062667d506b37c6f16c44bcb8af982a8584e765e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EcsInstanceV1OsSchedulerHintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5438c5e3d7b19988c2ad254a9d359c94a2f713182672055554ec70104ebc83d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ae618587c3497880f731ae5fa8392d846ad61fc22c9804a9442a238cb71b72c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7253ffbf0c711f782ed13386a17ea0c1f5ef56bd39463306051ea08e65b9c3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EcsInstanceV1OsSchedulerHints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EcsInstanceV1OsSchedulerHints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EcsInstanceV1OsSchedulerHints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53e09b9c887b4523b169f4759f83bafe07961090601ac540db98990eb47e17bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EcsInstanceV1OsSchedulerHintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ecsInstanceV1.EcsInstanceV1OsSchedulerHintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__edb85c0b39bf5ebddcbbb5484a68c9025eb3891f739011b39b87f6db38d962a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDedicatedHostId")
    def reset_dedicated_host_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDedicatedHostId", []))

    @jsii.member(jsii_name="resetGroup")
    def reset_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroup", []))

    @jsii.member(jsii_name="resetTenancy")
    def reset_tenancy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenancy", []))

    @builtins.property
    @jsii.member(jsii_name="dedicatedHostIdInput")
    def dedicated_host_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dedicatedHostIdInput"))

    @builtins.property
    @jsii.member(jsii_name="groupInput")
    def group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupInput"))

    @builtins.property
    @jsii.member(jsii_name="tenancyInput")
    def tenancy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenancyInput"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedHostId")
    def dedicated_host_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dedicatedHostId"))

    @dedicated_host_id.setter
    def dedicated_host_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12b4898d7366ba8c93ab42850701379cacf22123606b47eefb551d40d29e59f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dedicatedHostId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "group"))

    @group.setter
    def group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccf5109cf99d88c6fa0ffd986af6b201e0813a573f657e46519faa8c8fee71bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenancy")
    def tenancy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenancy"))

    @tenancy.setter
    def tenancy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42814990d52825b1f2aaaae90f16ad9e4751db6e8d7afca101e9e6c187c56dca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenancy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EcsInstanceV1OsSchedulerHints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EcsInstanceV1OsSchedulerHints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EcsInstanceV1OsSchedulerHints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb3d8bb954a18c0bc98746dacaa916b9d5e946a835fed136612ffc01f6557a22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ecsInstanceV1.EcsInstanceV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class EcsInstanceV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#create EcsInstanceV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#delete EcsInstanceV1#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#update EcsInstanceV1#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b608106ce6e8684329ea14a79b22296edde8c69c9a6d26f4c621ced4136ac22)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#create EcsInstanceV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#delete EcsInstanceV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ecs_instance_v1#update EcsInstanceV1#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsInstanceV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsInstanceV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ecsInstanceV1.EcsInstanceV1TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c75c5f3c25d6ff37ffaac7a2a0b35fa11dec60cafbfb0a55737ed9fa776ca39)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffc734c0c20120b3b9644bf972ddd24cefe0255a2971a42ac11dd256ddb2cfc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2ef160d90d008728b49b184f1bc1fde2387824d25882a67819b347508207c20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b340b333a9be7b0282bc9646ffc481da148cc2bf5914de63539b3f3a59be6c74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EcsInstanceV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EcsInstanceV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EcsInstanceV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b4e46aabecff3bbf00f36e7e5e0d04da0f1f96ae2d7d24cad834017ee02ceac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ecsInstanceV1.EcsInstanceV1VolumesAttached",
    jsii_struct_bases=[],
    name_mapping={},
)
class EcsInstanceV1VolumesAttached:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsInstanceV1VolumesAttached(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsInstanceV1VolumesAttachedList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ecsInstanceV1.EcsInstanceV1VolumesAttachedList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29089c80714ff76fd2543a6b5a963c811d94d780a7592c2928841f014c2ef073)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EcsInstanceV1VolumesAttachedOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7af30be44ab97104d34019fb68daab53ebe83cc45637184c4caf1445074db727)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EcsInstanceV1VolumesAttachedOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__998ec149540b84a9899c4b1ac15dfc186d67a470ba0d5ce571621b0eee7f22f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59dae125651ef31778eb34bd155724f29bbd39297dde441584603ad660ccdbed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eaf076de6e496eb863552a9bccbe1e44f21acd9083ee9e776d856cbc0e5538fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class EcsInstanceV1VolumesAttachedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ecsInstanceV1.EcsInstanceV1VolumesAttachedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__513e2160a17b0e9554ca6496cbcad6f3f1f69dd97092f466289d850823663de7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="kmsId")
    def kms_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsId"))

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @builtins.property
    @jsii.member(jsii_name="snapshotId")
    def snapshot_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snapshotId"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EcsInstanceV1VolumesAttached]:
        return typing.cast(typing.Optional[EcsInstanceV1VolumesAttached], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EcsInstanceV1VolumesAttached],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__294597dc1abc92469ebc19fcd4bc989369e9bf087563283d5d3b046a93bfc63f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "EcsInstanceV1",
    "EcsInstanceV1Config",
    "EcsInstanceV1DataDisks",
    "EcsInstanceV1DataDisksList",
    "EcsInstanceV1DataDisksOutputReference",
    "EcsInstanceV1Metadata",
    "EcsInstanceV1MetadataOutputReference",
    "EcsInstanceV1Nics",
    "EcsInstanceV1NicsList",
    "EcsInstanceV1NicsOutputReference",
    "EcsInstanceV1OsSchedulerHints",
    "EcsInstanceV1OsSchedulerHintsList",
    "EcsInstanceV1OsSchedulerHintsOutputReference",
    "EcsInstanceV1Timeouts",
    "EcsInstanceV1TimeoutsOutputReference",
    "EcsInstanceV1VolumesAttached",
    "EcsInstanceV1VolumesAttachedList",
    "EcsInstanceV1VolumesAttachedOutputReference",
]

publication.publish()

def _typecheckingstub__96244114cb7df1f914941bdd0b405c08f0085c85246b3f01fffeb44b8c9b5650(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    flavor: builtins.str,
    image_id: builtins.str,
    name: builtins.str,
    nics: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EcsInstanceV1Nics, typing.Dict[builtins.str, typing.Any]]]],
    vpc_id: builtins.str,
    auto_recovery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    availability_zone: typing.Optional[builtins.str] = None,
    data_disks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EcsInstanceV1DataDisks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    delete_disks_on_termination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    key_name: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Union[EcsInstanceV1Metadata, typing.Dict[builtins.str, typing.Any]]] = None,
    os_scheduler_hints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EcsInstanceV1OsSchedulerHints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    password: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    system_disk_kms_id: typing.Optional[builtins.str] = None,
    system_disk_size: typing.Optional[jsii.Number] = None,
    system_disk_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[EcsInstanceV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_data: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__342405298025e5b109b2de2b0cc3ca610577306ac70c4724b15a6dd56c54e4a9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72c4a26716d73d61cfae9c4d122fea5a08d5801cbf76194008a3030acc6b8392(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EcsInstanceV1DataDisks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe5121df134a409faf493ee936997e89eefe50a317609698727e58c05fc73df8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EcsInstanceV1Nics, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f319c45d0dd790c68d5cbb0ad49bc5d7d1883b763232d30774869580b9e3a2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EcsInstanceV1OsSchedulerHints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45b41ebf653ed600bb7ea400a0001fab64f53ae5d6a8a00b662bc497f74eb5b6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff97261196b82fb67316722b514fc3ce7daf652658538e9cffb940d9c1834bc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af2ba6eacd20710c008f717bce02870d2db952aee6edf7b7756af85dc2191bf6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c732075738c830d512bd6ed7708ebbaff93d035124dd5e474e02e547954a744(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17866ac6bf095ef27feb31747d99aaa083b3bbf3605dee42118c149e5ee80b50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5517509a5d9c97fc75d0ecf5844f32b9b0acba9160f4aab595b372cb22a7db0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6393aaad3030eb6418d1851f0c69e7c871fe0accf78de5608705f9fa1f971bf8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc0f26ae5bb9f8e11b43207b9277f43c09a5f60184d439f5a75823e6d9cf1e36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2885b1f2b290d4ef48db0723e68de227b9729672620999251f1762e3f8f2ab72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e9b2e40ccff46df545bac2b9161e4b86dd3a0eeed97791223018cf1e19fb3e4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6232d91329c62866f7c54ebfe461d61010625ea1fe5424e7a138c252daf7da92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__963713dc3753cad3d8453587f528da06e75d6cc4df8670c77eb9494af26357f1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2251f5746c417d1a6a6e9b1f9342bb43c879308d6927394a9ee1b68f684dadcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a149f5007e462e21528daa54fbff0cf0b89548d140c4db095eedab7ee0412c45(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3291e5c34c91865258934a19b4d1a93bf04e02d6002dbd895c31ab9c64d08b6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4684386d34d8a4ea88fdf3d89ed6b286bc2ae0f70cb46fab4abc2df429e8001f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__282714a43369c85da130cddb5a566dc8c682b6a4fb6315ca63311ba505050095(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    flavor: builtins.str,
    image_id: builtins.str,
    name: builtins.str,
    nics: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EcsInstanceV1Nics, typing.Dict[builtins.str, typing.Any]]]],
    vpc_id: builtins.str,
    auto_recovery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    availability_zone: typing.Optional[builtins.str] = None,
    data_disks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EcsInstanceV1DataDisks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    delete_disks_on_termination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    key_name: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Union[EcsInstanceV1Metadata, typing.Dict[builtins.str, typing.Any]]] = None,
    os_scheduler_hints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EcsInstanceV1OsSchedulerHints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    password: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    system_disk_kms_id: typing.Optional[builtins.str] = None,
    system_disk_size: typing.Optional[jsii.Number] = None,
    system_disk_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[EcsInstanceV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05989798e9bdddff730951c32d131463ee210e0f51928886a40819ea62699044(
    *,
    size: jsii.Number,
    type: builtins.str,
    kms_id: typing.Optional[builtins.str] = None,
    snapshot_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be066e312c8db56c11cbf53fea21c3d0dd23fd7989a0e93df17fb6e23318d8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f326e67f2b8205c8edb63d7484107bd08d18e9da274789a6edeac4abb2b6d7df(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8e20935ea7597c37b8549f0c0386f77ebcfbb7a576ea349d4700965561904ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42dd16ca9b85f042cd9d6cd770b1b08e05b58cc7e8f78e2a132da1815ca4f340(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e91fe7944902956d10182b2c93494a271fe8be9282b033b94f00c6ac5f21b14(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b9522bf6636e802374e8e68dc3879b8f50a8b8ae8535973c066c8b07c04241f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EcsInstanceV1DataDisks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48bcb0740958643426d4699d58a789b54d75150118faba184d61190ba33bc103(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dcd4e6b865e306782d58d441ad5a50c29fde336258c831f15a66e0632c70877(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db46ae72bd17746c0f3300fea544172d610c227a43f8a8cb39c05fb05e166bcc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a5bdb30120b8600b82b0a3f2718ec486594df2fcb9569308bc5a7caed802add(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__792811c772baccb468266e67392fbca77f596ffa19bc7174ecd87ee524778158(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a72f06c5c62edf7f4e79f4c2246fbb5597962b9a6803a6b1e6ac9f3944c2ecbb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EcsInstanceV1DataDisks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__301d23ee6db65b613826b2a50b68b4a15b18c0b4d6dbec7763bae32bb9099f56(
    *,
    agency_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f268747b22f51ac17849feed431a203ef0ca03481a63b6beef5ea874ac92590(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a55171e5223c2d03b5189ce80cb805da5df8274ad6ad6bf8268997fa01b9e059(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50cb403804e073f81caef0bdf50cd29d315c244be789eda81cb7d61abccada62(
    value: typing.Optional[EcsInstanceV1Metadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__302dee08ca1f4b43d7cdcb6981c3f138c9aaac6993045e72bc52ca832eb979a3(
    *,
    network_id: builtins.str,
    ip_address: typing.Optional[builtins.str] = None,
    ipv6_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7cc60cbc1da3e633d0262329c7391c45e103a6ff5888dd5f72e5749672005c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a5aedaee106caf7a8ce872309a5230758b13e8eab5f0022ffdffa98d019dfb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a2204fb5bfbff48bcc045c40a4442c4122e0b866dde68afa1279b9f7e10bbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23db3bd648e9bac67fe12995e3989bdcd3aeb7256d42de4e233a78a60dc41ca5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e96c5f74361c1080871e2e45f57e5edc9bda29d1963fe1de1c466bca559e1e3a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0203e9ecd8e93778b394441d4c0c6266ee3770864189c75abf5defadce8f8ac6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EcsInstanceV1Nics]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2710a4959378a5ae767a13103545347883817f62b50c0b9f246f35ff939d0ff7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62170ad44c3d3f563c504e04d30123420241dc8630f6ddf0cd256e50edc262b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__391162156129dadc63b4f71003affc2c08db6bdffc75060eeb99fdd05a0c5568(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825ccea9f6b4e7186cb8ac1f17b3e9f03d01c3eb127ce542bf5c3df17fc90b6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__859cebe938762e554d7cab7e8bef14f0e9871d36a56b145fe31cc55dfb86ed46(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EcsInstanceV1Nics]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34ef2031c0862831474375bdd5f74312dd802cda618b13fe32e9836332e4063(
    *,
    dedicated_host_id: typing.Optional[builtins.str] = None,
    group: typing.Optional[builtins.str] = None,
    tenancy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a657638a1f05b570346cbf9645ca00867386b4e5b69f2750d59f7f8d2fa4bee1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a747afb9d5610056965f5dd7062667d506b37c6f16c44bcb8af982a8584e765e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5438c5e3d7b19988c2ad254a9d359c94a2f713182672055554ec70104ebc83d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae618587c3497880f731ae5fa8392d846ad61fc22c9804a9442a238cb71b72c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7253ffbf0c711f782ed13386a17ea0c1f5ef56bd39463306051ea08e65b9c3b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53e09b9c887b4523b169f4759f83bafe07961090601ac540db98990eb47e17bd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EcsInstanceV1OsSchedulerHints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb85c0b39bf5ebddcbbb5484a68c9025eb3891f739011b39b87f6db38d962a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b4898d7366ba8c93ab42850701379cacf22123606b47eefb551d40d29e59f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf5109cf99d88c6fa0ffd986af6b201e0813a573f657e46519faa8c8fee71bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42814990d52825b1f2aaaae90f16ad9e4751db6e8d7afca101e9e6c187c56dca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb3d8bb954a18c0bc98746dacaa916b9d5e946a835fed136612ffc01f6557a22(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EcsInstanceV1OsSchedulerHints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b608106ce6e8684329ea14a79b22296edde8c69c9a6d26f4c621ced4136ac22(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c75c5f3c25d6ff37ffaac7a2a0b35fa11dec60cafbfb0a55737ed9fa776ca39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffc734c0c20120b3b9644bf972ddd24cefe0255a2971a42ac11dd256ddb2cfc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ef160d90d008728b49b184f1bc1fde2387824d25882a67819b347508207c20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b340b333a9be7b0282bc9646ffc481da148cc2bf5914de63539b3f3a59be6c74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4e46aabecff3bbf00f36e7e5e0d04da0f1f96ae2d7d24cad834017ee02ceac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EcsInstanceV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29089c80714ff76fd2543a6b5a963c811d94d780a7592c2928841f014c2ef073(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af30be44ab97104d34019fb68daab53ebe83cc45637184c4caf1445074db727(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__998ec149540b84a9899c4b1ac15dfc186d67a470ba0d5ce571621b0eee7f22f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59dae125651ef31778eb34bd155724f29bbd39297dde441584603ad660ccdbed(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaf076de6e496eb863552a9bccbe1e44f21acd9083ee9e776d856cbc0e5538fb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__513e2160a17b0e9554ca6496cbcad6f3f1f69dd97092f466289d850823663de7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__294597dc1abc92469ebc19fcd4bc989369e9bf087563283d5d3b046a93bfc63f(
    value: typing.Optional[EcsInstanceV1VolumesAttached],
) -> None:
    """Type checking stubs"""
    pass
