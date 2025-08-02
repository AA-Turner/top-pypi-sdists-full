r'''
# `opentelekomcloud_compute_instance_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_compute_instance_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2).
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


class ComputeInstanceV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.computeInstanceV2.ComputeInstanceV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2 opentelekomcloud_compute_instance_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        access_ip_v4: typing.Optional[builtins.str] = None,
        access_ip_v6: typing.Optional[builtins.str] = None,
        admin_pass: typing.Optional[builtins.str] = None,
        auto_recovery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        block_device: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceV2BlockDevice", typing.Dict[builtins.str, typing.Any]]]]] = None,
        config_drive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        flavor_id: typing.Optional[builtins.str] = None,
        flavor_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_id: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        key_pair: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceV2Network", typing.Dict[builtins.str, typing.Any]]]]] = None,
        power_state: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        scheduler_hints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceV2SchedulerHints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        ssh_private_key_path: typing.Optional[builtins.str] = None,
        stop_before_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeInstanceV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_data: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2 opentelekomcloud_compute_instance_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#name ComputeInstanceV2#name}.
        :param access_ip_v4: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#access_ip_v4 ComputeInstanceV2#access_ip_v4}.
        :param access_ip_v6: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#access_ip_v6 ComputeInstanceV2#access_ip_v6}.
        :param admin_pass: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#admin_pass ComputeInstanceV2#admin_pass}.
        :param auto_recovery: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#auto_recovery ComputeInstanceV2#auto_recovery}.
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#availability_zone ComputeInstanceV2#availability_zone}.
        :param block_device: block_device block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#block_device ComputeInstanceV2#block_device}
        :param config_drive: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#config_drive ComputeInstanceV2#config_drive}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#description ComputeInstanceV2#description}.
        :param flavor_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#flavor_id ComputeInstanceV2#flavor_id}.
        :param flavor_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#flavor_name ComputeInstanceV2#flavor_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#id ComputeInstanceV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#image_id ComputeInstanceV2#image_id}.
        :param image_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#image_name ComputeInstanceV2#image_name}.
        :param key_pair: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#key_pair ComputeInstanceV2#key_pair}.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#metadata ComputeInstanceV2#metadata}.
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#network ComputeInstanceV2#network}
        :param power_state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#power_state ComputeInstanceV2#power_state}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#region ComputeInstanceV2#region}.
        :param scheduler_hints: scheduler_hints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#scheduler_hints ComputeInstanceV2#scheduler_hints}
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#security_groups ComputeInstanceV2#security_groups}.
        :param ssh_private_key_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#ssh_private_key_path ComputeInstanceV2#ssh_private_key_path}.
        :param stop_before_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#stop_before_destroy ComputeInstanceV2#stop_before_destroy}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#tags ComputeInstanceV2#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#timeouts ComputeInstanceV2#timeouts}
        :param user_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#user_data ComputeInstanceV2#user_data}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c4f0ba648cd3f98d76aa7e7f886d04103f6ac96462ede7771af4bbdb54dc6aa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeInstanceV2Config(
            name=name,
            access_ip_v4=access_ip_v4,
            access_ip_v6=access_ip_v6,
            admin_pass=admin_pass,
            auto_recovery=auto_recovery,
            availability_zone=availability_zone,
            block_device=block_device,
            config_drive=config_drive,
            description=description,
            flavor_id=flavor_id,
            flavor_name=flavor_name,
            id=id,
            image_id=image_id,
            image_name=image_name,
            key_pair=key_pair,
            metadata=metadata,
            network=network,
            power_state=power_state,
            region=region,
            scheduler_hints=scheduler_hints,
            security_groups=security_groups,
            ssh_private_key_path=ssh_private_key_path,
            stop_before_destroy=stop_before_destroy,
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
        '''Generates CDKTF code for importing a ComputeInstanceV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeInstanceV2 to import.
        :param import_from_id: The id of the existing ComputeInstanceV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeInstanceV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7007d54c911939637cc73a661f77b36ed44207524fdbefc0b86fbc6ff5405ec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBlockDevice")
    def put_block_device(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceV2BlockDevice", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3948a329eb1abecb9bc81dd98b3e660529d0059afbb6dd51e4b7f6526e5ee56a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBlockDevice", [value]))

    @jsii.member(jsii_name="putNetwork")
    def put_network(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceV2Network", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c38331257c8effeabe93698719817267115bf151e398f6a9747173f04062fe5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetwork", [value]))

    @jsii.member(jsii_name="putSchedulerHints")
    def put_scheduler_hints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceV2SchedulerHints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__709806699cd03dc0b8faf6e08b43e2b40aeaefa638022641623ad6086b6272ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSchedulerHints", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#create ComputeInstanceV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#delete ComputeInstanceV2#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#update ComputeInstanceV2#update}.
        '''
        value = ComputeInstanceV2Timeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAccessIpV4")
    def reset_access_ip_v4(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessIpV4", []))

    @jsii.member(jsii_name="resetAccessIpV6")
    def reset_access_ip_v6(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessIpV6", []))

    @jsii.member(jsii_name="resetAdminPass")
    def reset_admin_pass(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminPass", []))

    @jsii.member(jsii_name="resetAutoRecovery")
    def reset_auto_recovery(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoRecovery", []))

    @jsii.member(jsii_name="resetAvailabilityZone")
    def reset_availability_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityZone", []))

    @jsii.member(jsii_name="resetBlockDevice")
    def reset_block_device(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockDevice", []))

    @jsii.member(jsii_name="resetConfigDrive")
    def reset_config_drive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigDrive", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetFlavorId")
    def reset_flavor_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlavorId", []))

    @jsii.member(jsii_name="resetFlavorName")
    def reset_flavor_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlavorName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImageId")
    def reset_image_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageId", []))

    @jsii.member(jsii_name="resetImageName")
    def reset_image_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageName", []))

    @jsii.member(jsii_name="resetKeyPair")
    def reset_key_pair(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyPair", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetPowerState")
    def reset_power_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPowerState", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSchedulerHints")
    def reset_scheduler_hints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedulerHints", []))

    @jsii.member(jsii_name="resetSecurityGroups")
    def reset_security_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroups", []))

    @jsii.member(jsii_name="resetSshPrivateKeyPath")
    def reset_ssh_private_key_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshPrivateKeyPath", []))

    @jsii.member(jsii_name="resetStopBeforeDestroy")
    def reset_stop_before_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStopBeforeDestroy", []))

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
    @jsii.member(jsii_name="allMetadata")
    def all_metadata(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "allMetadata"))

    @builtins.property
    @jsii.member(jsii_name="blockDevice")
    def block_device(self) -> "ComputeInstanceV2BlockDeviceList":
        return typing.cast("ComputeInstanceV2BlockDeviceList", jsii.get(self, "blockDevice"))

    @builtins.property
    @jsii.member(jsii_name="encryptedPassword")
    def encrypted_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptedPassword"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> "ComputeInstanceV2NetworkList":
        return typing.cast("ComputeInstanceV2NetworkList", jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @builtins.property
    @jsii.member(jsii_name="schedulerHints")
    def scheduler_hints(self) -> "ComputeInstanceV2SchedulerHintsList":
        return typing.cast("ComputeInstanceV2SchedulerHintsList", jsii.get(self, "schedulerHints"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeInstanceV2TimeoutsOutputReference":
        return typing.cast("ComputeInstanceV2TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="volumeAttached")
    def volume_attached(self) -> "ComputeInstanceV2VolumeAttachedList":
        return typing.cast("ComputeInstanceV2VolumeAttachedList", jsii.get(self, "volumeAttached"))

    @builtins.property
    @jsii.member(jsii_name="accessIpV4Input")
    def access_ip_v4_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessIpV4Input"))

    @builtins.property
    @jsii.member(jsii_name="accessIpV6Input")
    def access_ip_v6_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessIpV6Input"))

    @builtins.property
    @jsii.member(jsii_name="adminPassInput")
    def admin_pass_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminPassInput"))

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
    @jsii.member(jsii_name="blockDeviceInput")
    def block_device_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2BlockDevice"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2BlockDevice"]]], jsii.get(self, "blockDeviceInput"))

    @builtins.property
    @jsii.member(jsii_name="configDriveInput")
    def config_drive_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "configDriveInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorIdInput")
    def flavor_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorNameInput")
    def flavor_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageIdInput")
    def image_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageIdInput"))

    @builtins.property
    @jsii.member(jsii_name="imageNameInput")
    def image_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageNameInput"))

    @builtins.property
    @jsii.member(jsii_name="keyPairInput")
    def key_pair_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyPairInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2Network"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2Network"]]], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="powerStateInput")
    def power_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "powerStateInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="schedulerHintsInput")
    def scheduler_hints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2SchedulerHints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2SchedulerHints"]]], jsii.get(self, "schedulerHintsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupsInput")
    def security_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="sshPrivateKeyPathInput")
    def ssh_private_key_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sshPrivateKeyPathInput"))

    @builtins.property
    @jsii.member(jsii_name="stopBeforeDestroyInput")
    def stop_before_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "stopBeforeDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeInstanceV2Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeInstanceV2Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userDataInput")
    def user_data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userDataInput"))

    @builtins.property
    @jsii.member(jsii_name="accessIpV4")
    def access_ip_v4(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessIpV4"))

    @access_ip_v4.setter
    def access_ip_v4(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad2b2c4a7d36c6dc19c033d8dd6ce80400651199c76300a41a55dbbc0c521521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessIpV4", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accessIpV6")
    def access_ip_v6(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessIpV6"))

    @access_ip_v6.setter
    def access_ip_v6(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__184bac835066a25150e613f0d41647b29c2c52a4899efbbb08e6beb76b0dff3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessIpV6", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="adminPass")
    def admin_pass(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminPass"))

    @admin_pass.setter
    def admin_pass(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e65d94348b16ef07fe0454cbef175c9e35692c5a4e7e52d87df8651057590476)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminPass", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__b64c114b668081995e46322fb571115605357f555537f61867928b39ef656722)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoRecovery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e607db08f30fa3a9e803b222aae322bd24506f03140c9c915fee5e06067d199)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="configDrive")
    def config_drive(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "configDrive"))

    @config_drive.setter
    def config_drive(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__823bec9958e57a90653a5316c86dec17cff1c1de3e4d49cf2a15de630437173d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configDrive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4e771edb41a5165f3a4877e7b098ccb5506963162a6c035e73605e34683f830)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flavorId")
    def flavor_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavorId"))

    @flavor_id.setter
    def flavor_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfdc3d2b60cccc311ec8e7cd9d9bf910108836daedc900718bc2947f5b4157fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavorId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flavorName")
    def flavor_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavorName"))

    @flavor_name.setter
    def flavor_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e536d772fdb40839b40b225fbc72fd7c5d8a405be47827c975626fd34fd622e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavorName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c46cd3d62f646219c596215297f938e4ab2456f7d62bee7423e4fc6c2ad0e662)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageId"))

    @image_id.setter
    def image_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f79db97243002514ddf7bd62f2c2fa7cbb6e5df2f26bc5ee0e1dac900299954)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d03caf2672f1e310c5482c800324f559093ff4668fc6b94ea375f3d188317c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyPair")
    def key_pair(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyPair"))

    @key_pair.setter
    def key_pair(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd65704750f789b2e23d4484f3f38cb41e728826c3afa1105d705d1bc81bb223)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyPair", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b55ec6bf8afa59cff5bb734883527f5985bf6993605a381b1a718592d7cc928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39405b6b709ed0fc0eaecef2117a3554a5626f09368005856a1df4d49a0b7e02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="powerState")
    def power_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "powerState"))

    @power_state.setter
    def power_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b31111d4a091db923ac3dcf4203002fb6d1717898271c865c48884cd013a5f97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "powerState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11e28cc0fd6ab2e17c9b5446edf01eb286ed284af130a86c65bda32dc3ea3079)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroups"))

    @security_groups.setter
    def security_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf47f4d6e35958f2e2153ef3e6dbee10f578601ddcf4cf6239138860de09ac28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshPrivateKeyPath")
    def ssh_private_key_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshPrivateKeyPath"))

    @ssh_private_key_path.setter
    def ssh_private_key_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0f1fe0751999d67c05f53d5f7703171e041b708762048e6e977e898a00bd7f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPrivateKeyPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stopBeforeDestroy")
    def stop_before_destroy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "stopBeforeDestroy"))

    @stop_before_destroy.setter
    def stop_before_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a2861e80365d142c94c4ef1ab59c8dfedef36fe3040c2bd90a0c9d63d9360f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stopBeforeDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e5d85a93605a80debc896c88aad3afe3cd3467400f41279e019cf7fd305fbc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userData")
    def user_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userData"))

    @user_data.setter
    def user_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa43bcee0bd62f3fe59920fd3d0492e055efb88177ac18d3462a97002302e180)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userData", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.computeInstanceV2.ComputeInstanceV2BlockDevice",
    jsii_struct_bases=[],
    name_mapping={
        "source_type": "sourceType",
        "boot_index": "bootIndex",
        "delete_on_termination": "deleteOnTermination",
        "destination_type": "destinationType",
        "device_name": "deviceName",
        "guest_format": "guestFormat",
        "uuid": "uuid",
        "volume_size": "volumeSize",
        "volume_type": "volumeType",
    },
)
class ComputeInstanceV2BlockDevice:
    def __init__(
        self,
        *,
        source_type: builtins.str,
        boot_index: typing.Optional[jsii.Number] = None,
        delete_on_termination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        destination_type: typing.Optional[builtins.str] = None,
        device_name: typing.Optional[builtins.str] = None,
        guest_format: typing.Optional[builtins.str] = None,
        uuid: typing.Optional[builtins.str] = None,
        volume_size: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#source_type ComputeInstanceV2#source_type}.
        :param boot_index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#boot_index ComputeInstanceV2#boot_index}.
        :param delete_on_termination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#delete_on_termination ComputeInstanceV2#delete_on_termination}.
        :param destination_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#destination_type ComputeInstanceV2#destination_type}.
        :param device_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#device_name ComputeInstanceV2#device_name}.
        :param guest_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#guest_format ComputeInstanceV2#guest_format}.
        :param uuid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#uuid ComputeInstanceV2#uuid}.
        :param volume_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#volume_size ComputeInstanceV2#volume_size}.
        :param volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#volume_type ComputeInstanceV2#volume_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac938f8497d5ace4989a7d674e51797ab0415df09c38b51fd662fb16908120da)
            check_type(argname="argument source_type", value=source_type, expected_type=type_hints["source_type"])
            check_type(argname="argument boot_index", value=boot_index, expected_type=type_hints["boot_index"])
            check_type(argname="argument delete_on_termination", value=delete_on_termination, expected_type=type_hints["delete_on_termination"])
            check_type(argname="argument destination_type", value=destination_type, expected_type=type_hints["destination_type"])
            check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
            check_type(argname="argument guest_format", value=guest_format, expected_type=type_hints["guest_format"])
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
            check_type(argname="argument volume_size", value=volume_size, expected_type=type_hints["volume_size"])
            check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_type": source_type,
        }
        if boot_index is not None:
            self._values["boot_index"] = boot_index
        if delete_on_termination is not None:
            self._values["delete_on_termination"] = delete_on_termination
        if destination_type is not None:
            self._values["destination_type"] = destination_type
        if device_name is not None:
            self._values["device_name"] = device_name
        if guest_format is not None:
            self._values["guest_format"] = guest_format
        if uuid is not None:
            self._values["uuid"] = uuid
        if volume_size is not None:
            self._values["volume_size"] = volume_size
        if volume_type is not None:
            self._values["volume_type"] = volume_type

    @builtins.property
    def source_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#source_type ComputeInstanceV2#source_type}.'''
        result = self._values.get("source_type")
        assert result is not None, "Required property 'source_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def boot_index(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#boot_index ComputeInstanceV2#boot_index}.'''
        result = self._values.get("boot_index")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def delete_on_termination(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#delete_on_termination ComputeInstanceV2#delete_on_termination}.'''
        result = self._values.get("delete_on_termination")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def destination_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#destination_type ComputeInstanceV2#destination_type}.'''
        result = self._values.get("destination_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#device_name ComputeInstanceV2#device_name}.'''
        result = self._values.get("device_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def guest_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#guest_format ComputeInstanceV2#guest_format}.'''
        result = self._values.get("guest_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uuid(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#uuid ComputeInstanceV2#uuid}.'''
        result = self._values.get("uuid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volume_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#volume_size ComputeInstanceV2#volume_size}.'''
        result = self._values.get("volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#volume_type ComputeInstanceV2#volume_type}.'''
        result = self._values.get("volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceV2BlockDevice(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceV2BlockDeviceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.computeInstanceV2.ComputeInstanceV2BlockDeviceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6227bab43eae31982feb306cd5bf60f4e9148aef0f42f2aaab36dfe176e550d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ComputeInstanceV2BlockDeviceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c16ec38e8b1c60ddd8cd37413982428305f4ebb5c705806c1604dcfd1744b3f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceV2BlockDeviceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4371b1814370d0e93035ef747acf15632d481ff1bf236daaa5b794d39d39788)
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
            type_hints = typing.get_type_hints(_typecheckingstub__312375cd9954941be88e45be95c3573e9ae7e30bb0fc40f1dcc67d499d5e780e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfef4da25e247ec4237a507b10b78df058faf59aa6848a8b8b06648a1123328f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2BlockDevice]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2BlockDevice]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2BlockDevice]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c88841e5ce508cdc7d87dfe5d2bd84f0fee09ad3c37b74f647fb27cfc712d2cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceV2BlockDeviceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.computeInstanceV2.ComputeInstanceV2BlockDeviceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd26bc75eb72575e2f60dbd23d3602acb92de00e5ed7a8c365be267e680f473a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBootIndex")
    def reset_boot_index(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootIndex", []))

    @jsii.member(jsii_name="resetDeleteOnTermination")
    def reset_delete_on_termination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteOnTermination", []))

    @jsii.member(jsii_name="resetDestinationType")
    def reset_destination_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationType", []))

    @jsii.member(jsii_name="resetDeviceName")
    def reset_device_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceName", []))

    @jsii.member(jsii_name="resetGuestFormat")
    def reset_guest_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGuestFormat", []))

    @jsii.member(jsii_name="resetUuid")
    def reset_uuid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUuid", []))

    @jsii.member(jsii_name="resetVolumeSize")
    def reset_volume_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeSize", []))

    @jsii.member(jsii_name="resetVolumeType")
    def reset_volume_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeType", []))

    @builtins.property
    @jsii.member(jsii_name="bootIndexInput")
    def boot_index_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootIndexInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteOnTerminationInput")
    def delete_on_termination_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteOnTerminationInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationTypeInput")
    def destination_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceNameInput")
    def device_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="guestFormatInput")
    def guest_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "guestFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceTypeInput")
    def source_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="uuidInput")
    def uuid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uuidInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeSizeInput")
    def volume_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "volumeSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeTypeInput")
    def volume_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="bootIndex")
    def boot_index(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bootIndex"))

    @boot_index.setter
    def boot_index(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd4c3f4ff21dc281c8163ef11a332e63754085461d5b374cd8d31dd3af75517f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootIndex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteOnTermination")
    def delete_on_termination(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteOnTermination"))

    @delete_on_termination.setter
    def delete_on_termination(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24e9a53c17ec7151c588861d58fbcb2396ac3b22f6afd30e1eb57c4caec140ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteOnTermination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationType")
    def destination_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationType"))

    @destination_type.setter
    def destination_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5865f7fa323c42880de5ddb07b30d12867b82275f8694b7e19ec3833726a257)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceName")
    def device_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceName"))

    @device_name.setter
    def device_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__051366e9aaa1ffb36aaf09c21f5b86f03cc1260be28dbfc3d1627b0a267e8bde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="guestFormat")
    def guest_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "guestFormat"))

    @guest_format.setter
    def guest_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2ab082e3d45844b11a1d855857b35a806d492c49b566936d1b275ae49d6914)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guestFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceType")
    def source_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceType"))

    @source_type.setter
    def source_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9f23ea22fa40745fdf3e87f3055a32707d89316225131d932a1b26a9d59f03a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uuid"))

    @uuid.setter
    def uuid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58424265792dca541cd9e555ee5ef0d22679e7c8d40b53cf5b67d60d3e1b9601)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uuid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeSize")
    def volume_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "volumeSize"))

    @volume_size.setter
    def volume_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c677a0ef19f1642685cdec8a197f4d16ce29395c738cf8179dfe637c32870fc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeType")
    def volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeType"))

    @volume_type.setter
    def volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a63e588ad318aee3a2912490e92c972c9dddc11e15fab73372a81e968b65ea7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2BlockDevice]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2BlockDevice]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2BlockDevice]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc1b50e9a18b527299f01857bd2205c4ae116da7eb3162305f4f0332006235b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.computeInstanceV2.ComputeInstanceV2Config",
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
        "access_ip_v4": "accessIpV4",
        "access_ip_v6": "accessIpV6",
        "admin_pass": "adminPass",
        "auto_recovery": "autoRecovery",
        "availability_zone": "availabilityZone",
        "block_device": "blockDevice",
        "config_drive": "configDrive",
        "description": "description",
        "flavor_id": "flavorId",
        "flavor_name": "flavorName",
        "id": "id",
        "image_id": "imageId",
        "image_name": "imageName",
        "key_pair": "keyPair",
        "metadata": "metadata",
        "network": "network",
        "power_state": "powerState",
        "region": "region",
        "scheduler_hints": "schedulerHints",
        "security_groups": "securityGroups",
        "ssh_private_key_path": "sshPrivateKeyPath",
        "stop_before_destroy": "stopBeforeDestroy",
        "tags": "tags",
        "timeouts": "timeouts",
        "user_data": "userData",
    },
)
class ComputeInstanceV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        access_ip_v4: typing.Optional[builtins.str] = None,
        access_ip_v6: typing.Optional[builtins.str] = None,
        admin_pass: typing.Optional[builtins.str] = None,
        auto_recovery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        block_device: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceV2BlockDevice, typing.Dict[builtins.str, typing.Any]]]]] = None,
        config_drive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        flavor_id: typing.Optional[builtins.str] = None,
        flavor_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_id: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        key_pair: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceV2Network", typing.Dict[builtins.str, typing.Any]]]]] = None,
        power_state: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        scheduler_hints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceV2SchedulerHints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        ssh_private_key_path: typing.Optional[builtins.str] = None,
        stop_before_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeInstanceV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#name ComputeInstanceV2#name}.
        :param access_ip_v4: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#access_ip_v4 ComputeInstanceV2#access_ip_v4}.
        :param access_ip_v6: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#access_ip_v6 ComputeInstanceV2#access_ip_v6}.
        :param admin_pass: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#admin_pass ComputeInstanceV2#admin_pass}.
        :param auto_recovery: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#auto_recovery ComputeInstanceV2#auto_recovery}.
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#availability_zone ComputeInstanceV2#availability_zone}.
        :param block_device: block_device block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#block_device ComputeInstanceV2#block_device}
        :param config_drive: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#config_drive ComputeInstanceV2#config_drive}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#description ComputeInstanceV2#description}.
        :param flavor_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#flavor_id ComputeInstanceV2#flavor_id}.
        :param flavor_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#flavor_name ComputeInstanceV2#flavor_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#id ComputeInstanceV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#image_id ComputeInstanceV2#image_id}.
        :param image_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#image_name ComputeInstanceV2#image_name}.
        :param key_pair: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#key_pair ComputeInstanceV2#key_pair}.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#metadata ComputeInstanceV2#metadata}.
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#network ComputeInstanceV2#network}
        :param power_state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#power_state ComputeInstanceV2#power_state}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#region ComputeInstanceV2#region}.
        :param scheduler_hints: scheduler_hints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#scheduler_hints ComputeInstanceV2#scheduler_hints}
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#security_groups ComputeInstanceV2#security_groups}.
        :param ssh_private_key_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#ssh_private_key_path ComputeInstanceV2#ssh_private_key_path}.
        :param stop_before_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#stop_before_destroy ComputeInstanceV2#stop_before_destroy}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#tags ComputeInstanceV2#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#timeouts ComputeInstanceV2#timeouts}
        :param user_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#user_data ComputeInstanceV2#user_data}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ComputeInstanceV2Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8f64251f2da76f16e2c683357639bc31e16e82b8e137614aa6f886bb19cf1d7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument access_ip_v4", value=access_ip_v4, expected_type=type_hints["access_ip_v4"])
            check_type(argname="argument access_ip_v6", value=access_ip_v6, expected_type=type_hints["access_ip_v6"])
            check_type(argname="argument admin_pass", value=admin_pass, expected_type=type_hints["admin_pass"])
            check_type(argname="argument auto_recovery", value=auto_recovery, expected_type=type_hints["auto_recovery"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument block_device", value=block_device, expected_type=type_hints["block_device"])
            check_type(argname="argument config_drive", value=config_drive, expected_type=type_hints["config_drive"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument flavor_id", value=flavor_id, expected_type=type_hints["flavor_id"])
            check_type(argname="argument flavor_name", value=flavor_name, expected_type=type_hints["flavor_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_id", value=image_id, expected_type=type_hints["image_id"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument key_pair", value=key_pair, expected_type=type_hints["key_pair"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument power_state", value=power_state, expected_type=type_hints["power_state"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument scheduler_hints", value=scheduler_hints, expected_type=type_hints["scheduler_hints"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument ssh_private_key_path", value=ssh_private_key_path, expected_type=type_hints["ssh_private_key_path"])
            check_type(argname="argument stop_before_destroy", value=stop_before_destroy, expected_type=type_hints["stop_before_destroy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
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
        if access_ip_v4 is not None:
            self._values["access_ip_v4"] = access_ip_v4
        if access_ip_v6 is not None:
            self._values["access_ip_v6"] = access_ip_v6
        if admin_pass is not None:
            self._values["admin_pass"] = admin_pass
        if auto_recovery is not None:
            self._values["auto_recovery"] = auto_recovery
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if block_device is not None:
            self._values["block_device"] = block_device
        if config_drive is not None:
            self._values["config_drive"] = config_drive
        if description is not None:
            self._values["description"] = description
        if flavor_id is not None:
            self._values["flavor_id"] = flavor_id
        if flavor_name is not None:
            self._values["flavor_name"] = flavor_name
        if id is not None:
            self._values["id"] = id
        if image_id is not None:
            self._values["image_id"] = image_id
        if image_name is not None:
            self._values["image_name"] = image_name
        if key_pair is not None:
            self._values["key_pair"] = key_pair
        if metadata is not None:
            self._values["metadata"] = metadata
        if network is not None:
            self._values["network"] = network
        if power_state is not None:
            self._values["power_state"] = power_state
        if region is not None:
            self._values["region"] = region
        if scheduler_hints is not None:
            self._values["scheduler_hints"] = scheduler_hints
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if ssh_private_key_path is not None:
            self._values["ssh_private_key_path"] = ssh_private_key_path
        if stop_before_destroy is not None:
            self._values["stop_before_destroy"] = stop_before_destroy
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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#name ComputeInstanceV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_ip_v4(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#access_ip_v4 ComputeInstanceV2#access_ip_v4}.'''
        result = self._values.get("access_ip_v4")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def access_ip_v6(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#access_ip_v6 ComputeInstanceV2#access_ip_v6}.'''
        result = self._values.get("access_ip_v6")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def admin_pass(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#admin_pass ComputeInstanceV2#admin_pass}.'''
        result = self._values.get("admin_pass")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_recovery(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#auto_recovery ComputeInstanceV2#auto_recovery}.'''
        result = self._values.get("auto_recovery")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#availability_zone ComputeInstanceV2#availability_zone}.'''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def block_device(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2BlockDevice]]]:
        '''block_device block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#block_device ComputeInstanceV2#block_device}
        '''
        result = self._values.get("block_device")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2BlockDevice]]], result)

    @builtins.property
    def config_drive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#config_drive ComputeInstanceV2#config_drive}.'''
        result = self._values.get("config_drive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#description ComputeInstanceV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flavor_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#flavor_id ComputeInstanceV2#flavor_id}.'''
        result = self._values.get("flavor_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flavor_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#flavor_name ComputeInstanceV2#flavor_name}.'''
        result = self._values.get("flavor_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#id ComputeInstanceV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#image_id ComputeInstanceV2#image_id}.'''
        result = self._values.get("image_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#image_name ComputeInstanceV2#image_name}.'''
        result = self._values.get("image_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_pair(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#key_pair ComputeInstanceV2#key_pair}.'''
        result = self._values.get("key_pair")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#metadata ComputeInstanceV2#metadata}.'''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def network(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2Network"]]]:
        '''network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#network ComputeInstanceV2#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2Network"]]], result)

    @builtins.property
    def power_state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#power_state ComputeInstanceV2#power_state}.'''
        result = self._values.get("power_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#region ComputeInstanceV2#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheduler_hints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2SchedulerHints"]]]:
        '''scheduler_hints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#scheduler_hints ComputeInstanceV2#scheduler_hints}
        '''
        result = self._values.get("scheduler_hints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2SchedulerHints"]]], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#security_groups ComputeInstanceV2#security_groups}.'''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ssh_private_key_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#ssh_private_key_path ComputeInstanceV2#ssh_private_key_path}.'''
        result = self._values.get("ssh_private_key_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stop_before_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#stop_before_destroy ComputeInstanceV2#stop_before_destroy}.'''
        result = self._values.get("stop_before_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#tags ComputeInstanceV2#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeInstanceV2Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#timeouts ComputeInstanceV2#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeInstanceV2Timeouts"], result)

    @builtins.property
    def user_data(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#user_data ComputeInstanceV2#user_data}.'''
        result = self._values.get("user_data")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.computeInstanceV2.ComputeInstanceV2Network",
    jsii_struct_bases=[],
    name_mapping={
        "access_network": "accessNetwork",
        "fixed_ip_v4": "fixedIpV4",
        "fixed_ip_v6": "fixedIpV6",
        "name": "name",
        "port": "port",
        "uuid": "uuid",
    },
)
class ComputeInstanceV2Network:
    def __init__(
        self,
        *,
        access_network: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fixed_ip_v4: typing.Optional[builtins.str] = None,
        fixed_ip_v6: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        port: typing.Optional[builtins.str] = None,
        uuid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_network: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#access_network ComputeInstanceV2#access_network}.
        :param fixed_ip_v4: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#fixed_ip_v4 ComputeInstanceV2#fixed_ip_v4}.
        :param fixed_ip_v6: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#fixed_ip_v6 ComputeInstanceV2#fixed_ip_v6}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#name ComputeInstanceV2#name}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#port ComputeInstanceV2#port}.
        :param uuid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#uuid ComputeInstanceV2#uuid}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a43100c307fa5ddadd8b39751d1fb10240eed4db3e47ef9aba6099b87f6f2f)
            check_type(argname="argument access_network", value=access_network, expected_type=type_hints["access_network"])
            check_type(argname="argument fixed_ip_v4", value=fixed_ip_v4, expected_type=type_hints["fixed_ip_v4"])
            check_type(argname="argument fixed_ip_v6", value=fixed_ip_v6, expected_type=type_hints["fixed_ip_v6"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_network is not None:
            self._values["access_network"] = access_network
        if fixed_ip_v4 is not None:
            self._values["fixed_ip_v4"] = fixed_ip_v4
        if fixed_ip_v6 is not None:
            self._values["fixed_ip_v6"] = fixed_ip_v6
        if name is not None:
            self._values["name"] = name
        if port is not None:
            self._values["port"] = port
        if uuid is not None:
            self._values["uuid"] = uuid

    @builtins.property
    def access_network(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#access_network ComputeInstanceV2#access_network}.'''
        result = self._values.get("access_network")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fixed_ip_v4(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#fixed_ip_v4 ComputeInstanceV2#fixed_ip_v4}.'''
        result = self._values.get("fixed_ip_v4")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fixed_ip_v6(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#fixed_ip_v6 ComputeInstanceV2#fixed_ip_v6}.'''
        result = self._values.get("fixed_ip_v6")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#name ComputeInstanceV2#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#port ComputeInstanceV2#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uuid(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#uuid ComputeInstanceV2#uuid}.'''
        result = self._values.get("uuid")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceV2Network(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceV2NetworkList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.computeInstanceV2.ComputeInstanceV2NetworkList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__958010d2b0b858f33615678741266b75a07d2100af998e60f3b324424053e7eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ComputeInstanceV2NetworkOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16322b8a83e1926c93451a21986f781d86b07dae8aa44d83a6a3f50b5f6477d7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceV2NetworkOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3105f2fcb29286a1efd341a91fa9059ff29572551e5468762c6bf54d3d9b9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a24ab55bed47b4946ee96ba4d4456b7347f9423816510c330f1ac47bb36d17c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40f8d13e639887a0c70de74006f2a521a9804c6c70e7b7f3d67f5ccbabef9260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2Network]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2Network]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2Network]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f28328b279d0bb676e793ac1cbcf4ac58d54931dd38689284a2fc0549362c712)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceV2NetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.computeInstanceV2.ComputeInstanceV2NetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18481da0ee500eb3aacc8135c8301c401e8d0abbb1284c6a939a8cf63fd0435f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccessNetwork")
    def reset_access_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessNetwork", []))

    @jsii.member(jsii_name="resetFixedIpV4")
    def reset_fixed_ip_v4(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedIpV4", []))

    @jsii.member(jsii_name="resetFixedIpV6")
    def reset_fixed_ip_v6(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedIpV6", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetUuid")
    def reset_uuid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUuid", []))

    @builtins.property
    @jsii.member(jsii_name="mac")
    def mac(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mac"))

    @builtins.property
    @jsii.member(jsii_name="accessNetworkInput")
    def access_network_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "accessNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedIpV4Input")
    def fixed_ip_v4_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fixedIpV4Input"))

    @builtins.property
    @jsii.member(jsii_name="fixedIpV6Input")
    def fixed_ip_v6_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fixedIpV6Input"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="uuidInput")
    def uuid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uuidInput"))

    @builtins.property
    @jsii.member(jsii_name="accessNetwork")
    def access_network(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "accessNetwork"))

    @access_network.setter
    def access_network(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da4da8e6605d4f61ff0cf19e89a50d36582c7c3990850eb9541d3cdf7b7762ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fixedIpV4")
    def fixed_ip_v4(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fixedIpV4"))

    @fixed_ip_v4.setter
    def fixed_ip_v4(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b67981b9bb6cf1904ee612070287ec329e1d5dd0f54957edafc3a58d23acbde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedIpV4", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fixedIpV6")
    def fixed_ip_v6(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fixedIpV6"))

    @fixed_ip_v6.setter
    def fixed_ip_v6(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c24cd0c3ea34d2d4b698fe2582b5984ab6397e0876fd59504b095acdffd5f9a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedIpV6", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d19787c12f1754adcd00aa4256571814b825666b06eed48ee6c677fc64c2ce59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82120d03d494b7f79511d2679ec77f9aa86f6023ad613b8dd105723a56582ad4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uuid"))

    @uuid.setter
    def uuid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b89a045d45dcd24c108b6d490d41456eaf8a285df8aedead80431760db81a82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uuid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2Network]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2Network]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2Network]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baf1b38e24bbf9393da088bbbab58ae4726e020d8c67739b7915a4479550a798)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.computeInstanceV2.ComputeInstanceV2SchedulerHints",
    jsii_struct_bases=[],
    name_mapping={
        "build_near_host_ip": "buildNearHostIp",
        "deh_id": "dehId",
        "different_host": "differentHost",
        "group": "group",
        "query": "query",
        "same_host": "sameHost",
        "target_cell": "targetCell",
        "tenancy": "tenancy",
    },
)
class ComputeInstanceV2SchedulerHints:
    def __init__(
        self,
        *,
        build_near_host_ip: typing.Optional[builtins.str] = None,
        deh_id: typing.Optional[builtins.str] = None,
        different_host: typing.Optional[typing.Sequence[builtins.str]] = None,
        group: typing.Optional[builtins.str] = None,
        query: typing.Optional[typing.Sequence[builtins.str]] = None,
        same_host: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_cell: typing.Optional[builtins.str] = None,
        tenancy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param build_near_host_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#build_near_host_ip ComputeInstanceV2#build_near_host_ip}.
        :param deh_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#deh_id ComputeInstanceV2#deh_id}.
        :param different_host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#different_host ComputeInstanceV2#different_host}.
        :param group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#group ComputeInstanceV2#group}.
        :param query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#query ComputeInstanceV2#query}.
        :param same_host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#same_host ComputeInstanceV2#same_host}.
        :param target_cell: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#target_cell ComputeInstanceV2#target_cell}.
        :param tenancy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#tenancy ComputeInstanceV2#tenancy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b930e18de0630276e8e39079926e7a1ddadf90bd51448731ffa35d1b6f5399d9)
            check_type(argname="argument build_near_host_ip", value=build_near_host_ip, expected_type=type_hints["build_near_host_ip"])
            check_type(argname="argument deh_id", value=deh_id, expected_type=type_hints["deh_id"])
            check_type(argname="argument different_host", value=different_host, expected_type=type_hints["different_host"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument same_host", value=same_host, expected_type=type_hints["same_host"])
            check_type(argname="argument target_cell", value=target_cell, expected_type=type_hints["target_cell"])
            check_type(argname="argument tenancy", value=tenancy, expected_type=type_hints["tenancy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if build_near_host_ip is not None:
            self._values["build_near_host_ip"] = build_near_host_ip
        if deh_id is not None:
            self._values["deh_id"] = deh_id
        if different_host is not None:
            self._values["different_host"] = different_host
        if group is not None:
            self._values["group"] = group
        if query is not None:
            self._values["query"] = query
        if same_host is not None:
            self._values["same_host"] = same_host
        if target_cell is not None:
            self._values["target_cell"] = target_cell
        if tenancy is not None:
            self._values["tenancy"] = tenancy

    @builtins.property
    def build_near_host_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#build_near_host_ip ComputeInstanceV2#build_near_host_ip}.'''
        result = self._values.get("build_near_host_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deh_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#deh_id ComputeInstanceV2#deh_id}.'''
        result = self._values.get("deh_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def different_host(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#different_host ComputeInstanceV2#different_host}.'''
        result = self._values.get("different_host")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def group(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#group ComputeInstanceV2#group}.'''
        result = self._values.get("group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#query ComputeInstanceV2#query}.'''
        result = self._values.get("query")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def same_host(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#same_host ComputeInstanceV2#same_host}.'''
        result = self._values.get("same_host")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def target_cell(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#target_cell ComputeInstanceV2#target_cell}.'''
        result = self._values.get("target_cell")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenancy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#tenancy ComputeInstanceV2#tenancy}.'''
        result = self._values.get("tenancy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceV2SchedulerHints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceV2SchedulerHintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.computeInstanceV2.ComputeInstanceV2SchedulerHintsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbc05ed948ab828e661e0b786c595294d61810198bf4350aa33cdda08eb80b6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceV2SchedulerHintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__682e917d9e9ae5b29c6265bc8827eff74ecf37dfbbb17e32b03a9640203b6fa3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceV2SchedulerHintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17862f1a3b85b808ea740c7cef1edc7f4ada8722472517f22e8ae996d9c8d8c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12b4a1a701f46eb8e5b73a0b0797b6adacb19fb8c5974d2d243ad42eba15e241)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe72c8ba4b394ab8272cb24c57e86719776459db0d979ee34b386871ce8b7315)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2SchedulerHints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2SchedulerHints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2SchedulerHints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__893d81f85f930acf437e50a3467a640243be5f180baef99aff90d07be1d27a46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceV2SchedulerHintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.computeInstanceV2.ComputeInstanceV2SchedulerHintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccadbce87762ea7b983bb2616e25823f8809092a3c69f9c0ea70bf85d0a91756)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBuildNearHostIp")
    def reset_build_near_host_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildNearHostIp", []))

    @jsii.member(jsii_name="resetDehId")
    def reset_deh_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDehId", []))

    @jsii.member(jsii_name="resetDifferentHost")
    def reset_different_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDifferentHost", []))

    @jsii.member(jsii_name="resetGroup")
    def reset_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroup", []))

    @jsii.member(jsii_name="resetQuery")
    def reset_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuery", []))

    @jsii.member(jsii_name="resetSameHost")
    def reset_same_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSameHost", []))

    @jsii.member(jsii_name="resetTargetCell")
    def reset_target_cell(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetCell", []))

    @jsii.member(jsii_name="resetTenancy")
    def reset_tenancy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenancy", []))

    @builtins.property
    @jsii.member(jsii_name="buildNearHostIpInput")
    def build_near_host_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildNearHostIpInput"))

    @builtins.property
    @jsii.member(jsii_name="dehIdInput")
    def deh_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dehIdInput"))

    @builtins.property
    @jsii.member(jsii_name="differentHostInput")
    def different_host_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "differentHostInput"))

    @builtins.property
    @jsii.member(jsii_name="groupInput")
    def group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="sameHostInput")
    def same_host_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sameHostInput"))

    @builtins.property
    @jsii.member(jsii_name="targetCellInput")
    def target_cell_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetCellInput"))

    @builtins.property
    @jsii.member(jsii_name="tenancyInput")
    def tenancy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenancyInput"))

    @builtins.property
    @jsii.member(jsii_name="buildNearHostIp")
    def build_near_host_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildNearHostIp"))

    @build_near_host_ip.setter
    def build_near_host_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03e7d511f520a5de95ff4b4f4cee6bf2759cb30bb83ee2ba572193a8596da01a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildNearHostIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dehId")
    def deh_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dehId"))

    @deh_id.setter
    def deh_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa78d47d775f82d191a4259863fb7908a74386dc9e3d272bf03b6008978e5ee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dehId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="differentHost")
    def different_host(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "differentHost"))

    @different_host.setter
    def different_host(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7d93ae6b98e5037c0cc580a6ff44f12f0c29ce535048aafdba5c23e93469349)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "differentHost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "group"))

    @group.setter
    def group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1804d74e46dc639f7e6360efd241c20d1600e7c79a1d9462527db24bce0bc7d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "query"))

    @query.setter
    def query(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82057a7a3a158eb42b50783969b3fce3651005280caa9d215bf27e3aa12c6af0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sameHost")
    def same_host(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sameHost"))

    @same_host.setter
    def same_host(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a25e83242d0ec589dbde9de829be1e1ffac57c5afd2256352b705c537dcbd2fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sameHost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetCell")
    def target_cell(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetCell"))

    @target_cell.setter
    def target_cell(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e72a8302ffa4678b9cd3583ebc9c0003dc27a55355d9f7fafbba86b1f531d10e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetCell", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenancy")
    def tenancy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenancy"))

    @tenancy.setter
    def tenancy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2403aaafdd66590cf74da581a2f3e0d1d22c4e73a9be52ae7381d3f823cd23f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenancy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2SchedulerHints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2SchedulerHints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2SchedulerHints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2895893695f240408a8acbe03edf4a4427e77cadf01b5c50f6bff6ded24c827e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.computeInstanceV2.ComputeInstanceV2Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeInstanceV2Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#create ComputeInstanceV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#delete ComputeInstanceV2#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#update ComputeInstanceV2#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71f229037b3f4f3b3cba0d60f8ee4dc6c1ad6b037d7d3242756b016c5bd08970)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#create ComputeInstanceV2#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#delete ComputeInstanceV2#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_instance_v2#update ComputeInstanceV2#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceV2Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceV2TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.computeInstanceV2.ComputeInstanceV2TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b8134d80d92638f0bf735337c69408776353bfb1f7b82ecb057a77655c3651b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce73761eab580301f76b4099237b5a160dcf00b061810943c723faae94d52085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3081694664b95ac2f533d7f075feff89d177dac003d441773e82e40e4b2a7a5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87ccea338dd9c2944ac0b8e8be53111786daf3ef1ba9bc9be5736a1c709f74a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca70294c5513aa1cd37c002fbd6f2c10a79f6e5a165ff44d9fb2c86543cba6b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.computeInstanceV2.ComputeInstanceV2VolumeAttached",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeInstanceV2VolumeAttached:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceV2VolumeAttached(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceV2VolumeAttachedList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.computeInstanceV2.ComputeInstanceV2VolumeAttachedList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b50118d80087855dc213b229eae34f5aee03f61f9cf3b2b102942502af5e0918)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceV2VolumeAttachedOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecd06e8d9ccfc76b74bcd75496b9d4442460b65f684ee4b955b8438b8d0fba54)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceV2VolumeAttachedOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e1843e1e872f15c5345e23b7b6d0d8d1ac6fa62e7a13d465945bf0167a1fa65)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2ea33cc0675cbf7eace40d94c5563f8ec3f153f4b3a797362938ca199e6d26b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c03d0f870672ba3fed7ce696c81e91541be19f734f2f677415e63672f829041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceV2VolumeAttachedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.computeInstanceV2.ComputeInstanceV2VolumeAttachedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8b9b800480aabfb01fb08f63abb8db53e53d21e0b1939508a4fd68dd26d4941)
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
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeInstanceV2VolumeAttached]:
        return typing.cast(typing.Optional[ComputeInstanceV2VolumeAttached], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceV2VolumeAttached],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d33cb82d72ef5997d08c63008e7804133c0f7799e0cd35dc10e6385bb2a2e462)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeInstanceV2",
    "ComputeInstanceV2BlockDevice",
    "ComputeInstanceV2BlockDeviceList",
    "ComputeInstanceV2BlockDeviceOutputReference",
    "ComputeInstanceV2Config",
    "ComputeInstanceV2Network",
    "ComputeInstanceV2NetworkList",
    "ComputeInstanceV2NetworkOutputReference",
    "ComputeInstanceV2SchedulerHints",
    "ComputeInstanceV2SchedulerHintsList",
    "ComputeInstanceV2SchedulerHintsOutputReference",
    "ComputeInstanceV2Timeouts",
    "ComputeInstanceV2TimeoutsOutputReference",
    "ComputeInstanceV2VolumeAttached",
    "ComputeInstanceV2VolumeAttachedList",
    "ComputeInstanceV2VolumeAttachedOutputReference",
]

publication.publish()

def _typecheckingstub__8c4f0ba648cd3f98d76aa7e7f886d04103f6ac96462ede7771af4bbdb54dc6aa(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    access_ip_v4: typing.Optional[builtins.str] = None,
    access_ip_v6: typing.Optional[builtins.str] = None,
    admin_pass: typing.Optional[builtins.str] = None,
    auto_recovery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    availability_zone: typing.Optional[builtins.str] = None,
    block_device: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceV2BlockDevice, typing.Dict[builtins.str, typing.Any]]]]] = None,
    config_drive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    flavor_id: typing.Optional[builtins.str] = None,
    flavor_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    image_id: typing.Optional[builtins.str] = None,
    image_name: typing.Optional[builtins.str] = None,
    key_pair: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceV2Network, typing.Dict[builtins.str, typing.Any]]]]] = None,
    power_state: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    scheduler_hints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceV2SchedulerHints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ssh_private_key_path: typing.Optional[builtins.str] = None,
    stop_before_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeInstanceV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__a7007d54c911939637cc73a661f77b36ed44207524fdbefc0b86fbc6ff5405ec(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3948a329eb1abecb9bc81dd98b3e660529d0059afbb6dd51e4b7f6526e5ee56a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceV2BlockDevice, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c38331257c8effeabe93698719817267115bf151e398f6a9747173f04062fe5d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceV2Network, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__709806699cd03dc0b8faf6e08b43e2b40aeaefa638022641623ad6086b6272ec(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceV2SchedulerHints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad2b2c4a7d36c6dc19c033d8dd6ce80400651199c76300a41a55dbbc0c521521(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__184bac835066a25150e613f0d41647b29c2c52a4899efbbb08e6beb76b0dff3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e65d94348b16ef07fe0454cbef175c9e35692c5a4e7e52d87df8651057590476(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b64c114b668081995e46322fb571115605357f555537f61867928b39ef656722(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e607db08f30fa3a9e803b222aae322bd24506f03140c9c915fee5e06067d199(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__823bec9958e57a90653a5316c86dec17cff1c1de3e4d49cf2a15de630437173d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e771edb41a5165f3a4877e7b098ccb5506963162a6c035e73605e34683f830(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfdc3d2b60cccc311ec8e7cd9d9bf910108836daedc900718bc2947f5b4157fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e536d772fdb40839b40b225fbc72fd7c5d8a405be47827c975626fd34fd622e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c46cd3d62f646219c596215297f938e4ab2456f7d62bee7423e4fc6c2ad0e662(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f79db97243002514ddf7bd62f2c2fa7cbb6e5df2f26bc5ee0e1dac900299954(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d03caf2672f1e310c5482c800324f559093ff4668fc6b94ea375f3d188317c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd65704750f789b2e23d4484f3f38cb41e728826c3afa1105d705d1bc81bb223(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b55ec6bf8afa59cff5bb734883527f5985bf6993605a381b1a718592d7cc928(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39405b6b709ed0fc0eaecef2117a3554a5626f09368005856a1df4d49a0b7e02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31111d4a091db923ac3dcf4203002fb6d1717898271c865c48884cd013a5f97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e28cc0fd6ab2e17c9b5446edf01eb286ed284af130a86c65bda32dc3ea3079(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf47f4d6e35958f2e2153ef3e6dbee10f578601ddcf4cf6239138860de09ac28(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f1fe0751999d67c05f53d5f7703171e041b708762048e6e977e898a00bd7f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a2861e80365d142c94c4ef1ab59c8dfedef36fe3040c2bd90a0c9d63d9360f4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e5d85a93605a80debc896c88aad3afe3cd3467400f41279e019cf7fd305fbc0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa43bcee0bd62f3fe59920fd3d0492e055efb88177ac18d3462a97002302e180(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac938f8497d5ace4989a7d674e51797ab0415df09c38b51fd662fb16908120da(
    *,
    source_type: builtins.str,
    boot_index: typing.Optional[jsii.Number] = None,
    delete_on_termination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    destination_type: typing.Optional[builtins.str] = None,
    device_name: typing.Optional[builtins.str] = None,
    guest_format: typing.Optional[builtins.str] = None,
    uuid: typing.Optional[builtins.str] = None,
    volume_size: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6227bab43eae31982feb306cd5bf60f4e9148aef0f42f2aaab36dfe176e550d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c16ec38e8b1c60ddd8cd37413982428305f4ebb5c705806c1604dcfd1744b3f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4371b1814370d0e93035ef747acf15632d481ff1bf236daaa5b794d39d39788(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__312375cd9954941be88e45be95c3573e9ae7e30bb0fc40f1dcc67d499d5e780e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfef4da25e247ec4237a507b10b78df058faf59aa6848a8b8b06648a1123328f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c88841e5ce508cdc7d87dfe5d2bd84f0fee09ad3c37b74f647fb27cfc712d2cd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2BlockDevice]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd26bc75eb72575e2f60dbd23d3602acb92de00e5ed7a8c365be267e680f473a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd4c3f4ff21dc281c8163ef11a332e63754085461d5b374cd8d31dd3af75517f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e9a53c17ec7151c588861d58fbcb2396ac3b22f6afd30e1eb57c4caec140ee(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5865f7fa323c42880de5ddb07b30d12867b82275f8694b7e19ec3833726a257(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__051366e9aaa1ffb36aaf09c21f5b86f03cc1260be28dbfc3d1627b0a267e8bde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2ab082e3d45844b11a1d855857b35a806d492c49b566936d1b275ae49d6914(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9f23ea22fa40745fdf3e87f3055a32707d89316225131d932a1b26a9d59f03a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58424265792dca541cd9e555ee5ef0d22679e7c8d40b53cf5b67d60d3e1b9601(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c677a0ef19f1642685cdec8a197f4d16ce29395c738cf8179dfe637c32870fc5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a63e588ad318aee3a2912490e92c972c9dddc11e15fab73372a81e968b65ea7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc1b50e9a18b527299f01857bd2205c4ae116da7eb3162305f4f0332006235b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2BlockDevice]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8f64251f2da76f16e2c683357639bc31e16e82b8e137614aa6f886bb19cf1d7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    access_ip_v4: typing.Optional[builtins.str] = None,
    access_ip_v6: typing.Optional[builtins.str] = None,
    admin_pass: typing.Optional[builtins.str] = None,
    auto_recovery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    availability_zone: typing.Optional[builtins.str] = None,
    block_device: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceV2BlockDevice, typing.Dict[builtins.str, typing.Any]]]]] = None,
    config_drive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    flavor_id: typing.Optional[builtins.str] = None,
    flavor_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    image_id: typing.Optional[builtins.str] = None,
    image_name: typing.Optional[builtins.str] = None,
    key_pair: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceV2Network, typing.Dict[builtins.str, typing.Any]]]]] = None,
    power_state: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    scheduler_hints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceV2SchedulerHints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ssh_private_key_path: typing.Optional[builtins.str] = None,
    stop_before_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeInstanceV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a43100c307fa5ddadd8b39751d1fb10240eed4db3e47ef9aba6099b87f6f2f(
    *,
    access_network: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fixed_ip_v4: typing.Optional[builtins.str] = None,
    fixed_ip_v6: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    port: typing.Optional[builtins.str] = None,
    uuid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958010d2b0b858f33615678741266b75a07d2100af998e60f3b324424053e7eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16322b8a83e1926c93451a21986f781d86b07dae8aa44d83a6a3f50b5f6477d7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3105f2fcb29286a1efd341a91fa9059ff29572551e5468762c6bf54d3d9b9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a24ab55bed47b4946ee96ba4d4456b7347f9423816510c330f1ac47bb36d17c7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f8d13e639887a0c70de74006f2a521a9804c6c70e7b7f3d67f5ccbabef9260(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f28328b279d0bb676e793ac1cbcf4ac58d54931dd38689284a2fc0549362c712(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2Network]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18481da0ee500eb3aacc8135c8301c401e8d0abbb1284c6a939a8cf63fd0435f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da4da8e6605d4f61ff0cf19e89a50d36582c7c3990850eb9541d3cdf7b7762ba(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b67981b9bb6cf1904ee612070287ec329e1d5dd0f54957edafc3a58d23acbde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c24cd0c3ea34d2d4b698fe2582b5984ab6397e0876fd59504b095acdffd5f9a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d19787c12f1754adcd00aa4256571814b825666b06eed48ee6c677fc64c2ce59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82120d03d494b7f79511d2679ec77f9aa86f6023ad613b8dd105723a56582ad4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b89a045d45dcd24c108b6d490d41456eaf8a285df8aedead80431760db81a82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baf1b38e24bbf9393da088bbbab58ae4726e020d8c67739b7915a4479550a798(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2Network]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b930e18de0630276e8e39079926e7a1ddadf90bd51448731ffa35d1b6f5399d9(
    *,
    build_near_host_ip: typing.Optional[builtins.str] = None,
    deh_id: typing.Optional[builtins.str] = None,
    different_host: typing.Optional[typing.Sequence[builtins.str]] = None,
    group: typing.Optional[builtins.str] = None,
    query: typing.Optional[typing.Sequence[builtins.str]] = None,
    same_host: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_cell: typing.Optional[builtins.str] = None,
    tenancy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbc05ed948ab828e661e0b786c595294d61810198bf4350aa33cdda08eb80b6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__682e917d9e9ae5b29c6265bc8827eff74ecf37dfbbb17e32b03a9640203b6fa3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17862f1a3b85b808ea740c7cef1edc7f4ada8722472517f22e8ae996d9c8d8c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b4a1a701f46eb8e5b73a0b0797b6adacb19fb8c5974d2d243ad42eba15e241(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe72c8ba4b394ab8272cb24c57e86719776459db0d979ee34b386871ce8b7315(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__893d81f85f930acf437e50a3467a640243be5f180baef99aff90d07be1d27a46(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2SchedulerHints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccadbce87762ea7b983bb2616e25823f8809092a3c69f9c0ea70bf85d0a91756(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03e7d511f520a5de95ff4b4f4cee6bf2759cb30bb83ee2ba572193a8596da01a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa78d47d775f82d191a4259863fb7908a74386dc9e3d272bf03b6008978e5ee7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d93ae6b98e5037c0cc580a6ff44f12f0c29ce535048aafdba5c23e93469349(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1804d74e46dc639f7e6360efd241c20d1600e7c79a1d9462527db24bce0bc7d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82057a7a3a158eb42b50783969b3fce3651005280caa9d215bf27e3aa12c6af0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a25e83242d0ec589dbde9de829be1e1ffac57c5afd2256352b705c537dcbd2fb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e72a8302ffa4678b9cd3583ebc9c0003dc27a55355d9f7fafbba86b1f531d10e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2403aaafdd66590cf74da581a2f3e0d1d22c4e73a9be52ae7381d3f823cd23f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2895893695f240408a8acbe03edf4a4427e77cadf01b5c50f6bff6ded24c827e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2SchedulerHints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f229037b3f4f3b3cba0d60f8ee4dc6c1ad6b037d7d3242756b016c5bd08970(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8134d80d92638f0bf735337c69408776353bfb1f7b82ecb057a77655c3651b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce73761eab580301f76b4099237b5a160dcf00b061810943c723faae94d52085(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3081694664b95ac2f533d7f075feff89d177dac003d441773e82e40e4b2a7a5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87ccea338dd9c2944ac0b8e8be53111786daf3ef1ba9bc9be5736a1c709f74a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca70294c5513aa1cd37c002fbd6f2c10a79f6e5a165ff44d9fb2c86543cba6b9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2Timeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b50118d80087855dc213b229eae34f5aee03f61f9cf3b2b102942502af5e0918(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecd06e8d9ccfc76b74bcd75496b9d4442460b65f684ee4b955b8438b8d0fba54(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e1843e1e872f15c5345e23b7b6d0d8d1ac6fa62e7a13d465945bf0167a1fa65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2ea33cc0675cbf7eace40d94c5563f8ec3f153f4b3a797362938ca199e6d26b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c03d0f870672ba3fed7ce696c81e91541be19f734f2f677415e63672f829041(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b9b800480aabfb01fb08f63abb8db53e53d21e0b1939508a4fd68dd26d4941(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d33cb82d72ef5997d08c63008e7804133c0f7799e0cd35dc10e6385bb2a2e462(
    value: typing.Optional[ComputeInstanceV2VolumeAttached],
) -> None:
    """Type checking stubs"""
    pass
