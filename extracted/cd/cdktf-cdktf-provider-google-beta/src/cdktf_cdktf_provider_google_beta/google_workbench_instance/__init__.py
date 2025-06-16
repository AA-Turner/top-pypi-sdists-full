r'''
# `google_workbench_instance`

Refer to the Terraform Registry for docs: [`google_workbench_instance`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance).
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


class GoogleWorkbenchInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance google_workbench_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        desired_state: typing.Optional[builtins.str] = None,
        disable_proxy_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_third_party_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gce_setup: typing.Optional[typing.Union["GoogleWorkbenchInstanceGceSetup", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_id: typing.Optional[builtins.str] = None,
        instance_owners: typing.Optional[typing.Sequence[builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleWorkbenchInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance google_workbench_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Part of 'parent'. See documentation of 'projectsId'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#location GoogleWorkbenchInstance#location}
        :param name: The name of this workbench instance. Format: 'projects/{project_id}/locations/{location}/instances/{instance_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#name GoogleWorkbenchInstance#name}
        :param desired_state: Desired state of the Workbench Instance. Set this field to 'ACTIVE' to start the Instance, and 'STOPPED' to stop the Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#desired_state GoogleWorkbenchInstance#desired_state}
        :param disable_proxy_access: Optional. If true, the workbench instance will not register with the proxy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disable_proxy_access GoogleWorkbenchInstance#disable_proxy_access}
        :param enable_third_party_identity: Flag that specifies that a notebook can be accessed with third party identity provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#enable_third_party_identity GoogleWorkbenchInstance#enable_third_party_identity}
        :param gce_setup: gce_setup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#gce_setup GoogleWorkbenchInstance#gce_setup}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#id GoogleWorkbenchInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_id: Required. User-defined unique ID of this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#instance_id GoogleWorkbenchInstance#instance_id}
        :param instance_owners: 'Optional. Input only. The owner of this instance after creation. Format: 'alias@example.com' Currently supports one owner only. If not specified, all of the service account users of your VM instance''s service account can use the instance. If specified, sets the access mode to 'Single user'. For more details, see https://cloud.google.com/vertex-ai/docs/workbench/instances/manage-access-jupyterlab' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#instance_owners GoogleWorkbenchInstance#instance_owners}
        :param labels: Optional. Labels to apply to this instance. These can be later modified by the UpdateInstance method. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#labels GoogleWorkbenchInstance#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#project GoogleWorkbenchInstance#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#timeouts GoogleWorkbenchInstance#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79e27cba1328d539db3272891440efb692427ca6579e16f34fb2679897e1605f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleWorkbenchInstanceConfig(
            location=location,
            name=name,
            desired_state=desired_state,
            disable_proxy_access=disable_proxy_access,
            enable_third_party_identity=enable_third_party_identity,
            gce_setup=gce_setup,
            id=id,
            instance_id=instance_id,
            instance_owners=instance_owners,
            labels=labels,
            project=project,
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
        '''Generates CDKTF code for importing a GoogleWorkbenchInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleWorkbenchInstance to import.
        :param import_from_id: The id of the existing GoogleWorkbenchInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleWorkbenchInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1ffbef6e3455e34e11be77462d05f72be2adb1ff4a2ad7a1ba7c60c47f2a9a7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putGceSetup")
    def put_gce_setup(
        self,
        *,
        accelerator_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleWorkbenchInstanceGceSetupAcceleratorConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        boot_disk: typing.Optional[typing.Union["GoogleWorkbenchInstanceGceSetupBootDisk", typing.Dict[builtins.str, typing.Any]]] = None,
        confidential_instance_config: typing.Optional[typing.Union["GoogleWorkbenchInstanceGceSetupConfidentialInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        container_image: typing.Optional[typing.Union["GoogleWorkbenchInstanceGceSetupContainerImage", typing.Dict[builtins.str, typing.Any]]] = None,
        data_disks: typing.Optional[typing.Union["GoogleWorkbenchInstanceGceSetupDataDisks", typing.Dict[builtins.str, typing.Any]]] = None,
        disable_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_ip_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        machine_type: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network_interfaces: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleWorkbenchInstanceGceSetupNetworkInterfaces", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_accounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleWorkbenchInstanceGceSetupServiceAccounts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        shielded_instance_config: typing.Optional[typing.Union["GoogleWorkbenchInstanceGceSetupShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        vm_image: typing.Optional[typing.Union["GoogleWorkbenchInstanceGceSetupVmImage", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param accelerator_configs: accelerator_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#accelerator_configs GoogleWorkbenchInstance#accelerator_configs}
        :param boot_disk: boot_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#boot_disk GoogleWorkbenchInstance#boot_disk}
        :param confidential_instance_config: confidential_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#confidential_instance_config GoogleWorkbenchInstance#confidential_instance_config}
        :param container_image: container_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#container_image GoogleWorkbenchInstance#container_image}
        :param data_disks: data_disks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#data_disks GoogleWorkbenchInstance#data_disks}
        :param disable_public_ip: Optional. If true, no external IP will be assigned to this VM instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disable_public_ip GoogleWorkbenchInstance#disable_public_ip}
        :param enable_ip_forwarding: Optional. Flag to enable ip forwarding or not, default false/off. https://cloud.google.com/vpc/docs/using-routes#canipforward. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#enable_ip_forwarding GoogleWorkbenchInstance#enable_ip_forwarding}
        :param machine_type: Optional. The machine type of the VM instance. https://cloud.google.com/compute/docs/machine-resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#machine_type GoogleWorkbenchInstance#machine_type}
        :param metadata: Optional. Custom metadata to apply to this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#metadata GoogleWorkbenchInstance#metadata}
        :param network_interfaces: network_interfaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#network_interfaces GoogleWorkbenchInstance#network_interfaces}
        :param service_accounts: service_accounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#service_accounts GoogleWorkbenchInstance#service_accounts}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#shielded_instance_config GoogleWorkbenchInstance#shielded_instance_config}
        :param tags: Optional. The Compute Engine tags to add to instance (see `Tagging instances <https://cloud.google.com/compute/docs/label-or-tag-resources#tags>`_). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#tags GoogleWorkbenchInstance#tags}
        :param vm_image: vm_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#vm_image GoogleWorkbenchInstance#vm_image}
        '''
        value = GoogleWorkbenchInstanceGceSetup(
            accelerator_configs=accelerator_configs,
            boot_disk=boot_disk,
            confidential_instance_config=confidential_instance_config,
            container_image=container_image,
            data_disks=data_disks,
            disable_public_ip=disable_public_ip,
            enable_ip_forwarding=enable_ip_forwarding,
            machine_type=machine_type,
            metadata=metadata,
            network_interfaces=network_interfaces,
            service_accounts=service_accounts,
            shielded_instance_config=shielded_instance_config,
            tags=tags,
            vm_image=vm_image,
        )

        return typing.cast(None, jsii.invoke(self, "putGceSetup", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#create GoogleWorkbenchInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#delete GoogleWorkbenchInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#update GoogleWorkbenchInstance#update}.
        '''
        value = GoogleWorkbenchInstanceTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDesiredState")
    def reset_desired_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDesiredState", []))

    @jsii.member(jsii_name="resetDisableProxyAccess")
    def reset_disable_proxy_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableProxyAccess", []))

    @jsii.member(jsii_name="resetEnableThirdPartyIdentity")
    def reset_enable_third_party_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableThirdPartyIdentity", []))

    @jsii.member(jsii_name="resetGceSetup")
    def reset_gce_setup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGceSetup", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInstanceId")
    def reset_instance_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceId", []))

    @jsii.member(jsii_name="resetInstanceOwners")
    def reset_instance_owners(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceOwners", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="creator")
    def creator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creator"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="gceSetup")
    def gce_setup(self) -> "GoogleWorkbenchInstanceGceSetupOutputReference":
        return typing.cast("GoogleWorkbenchInstanceGceSetupOutputReference", jsii.get(self, "gceSetup"))

    @builtins.property
    @jsii.member(jsii_name="healthInfo")
    def health_info(self) -> "GoogleWorkbenchInstanceHealthInfoList":
        return typing.cast("GoogleWorkbenchInstanceHealthInfoList", jsii.get(self, "healthInfo"))

    @builtins.property
    @jsii.member(jsii_name="healthState")
    def health_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthState"))

    @builtins.property
    @jsii.member(jsii_name="proxyUri")
    def proxy_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyUri"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleWorkbenchInstanceTimeoutsOutputReference":
        return typing.cast("GoogleWorkbenchInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="upgradeHistory")
    def upgrade_history(self) -> "GoogleWorkbenchInstanceUpgradeHistoryList":
        return typing.cast("GoogleWorkbenchInstanceUpgradeHistoryList", jsii.get(self, "upgradeHistory"))

    @builtins.property
    @jsii.member(jsii_name="desiredStateInput")
    def desired_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "desiredStateInput"))

    @builtins.property
    @jsii.member(jsii_name="disableProxyAccessInput")
    def disable_proxy_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableProxyAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="enableThirdPartyIdentityInput")
    def enable_third_party_identity_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableThirdPartyIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="gceSetupInput")
    def gce_setup_input(self) -> typing.Optional["GoogleWorkbenchInstanceGceSetup"]:
        return typing.cast(typing.Optional["GoogleWorkbenchInstanceGceSetup"], jsii.get(self, "gceSetupInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdInput")
    def instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceOwnersInput")
    def instance_owners_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "instanceOwnersInput"))

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
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleWorkbenchInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleWorkbenchInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredState")
    def desired_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "desiredState"))

    @desired_state.setter
    def desired_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff0a39c4ac90fb5c3a188010a95558f150a0d558f71f6ccfa6e27ec122720a58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "desiredState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableProxyAccess")
    def disable_proxy_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableProxyAccess"))

    @disable_proxy_access.setter
    def disable_proxy_access(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53dee8f2bbd65fb34d9e54582463d942ae3b87072948d0af5a023194120f611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableProxyAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableThirdPartyIdentity")
    def enable_third_party_identity(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableThirdPartyIdentity"))

    @enable_third_party_identity.setter
    def enable_third_party_identity(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be829248f0d26f3d3612d64ab33a4399d67585e633b96d65c9efbd32e6b4aab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableThirdPartyIdentity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__558c30142d06ab2603c8b37ab2f0f29a55bb01e9bcfdd052b3cc95336780920d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9310838de99d5df5bf97c19e6a19ba70ff19b034853efc8697e5f18566f7b9df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceOwners")
    def instance_owners(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceOwners"))

    @instance_owners.setter
    def instance_owners(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a2b8b0c7bc7e999ba798556eac2cab81a03820ff2f422f8124711ec8f4b51c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceOwners", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d367780c13e1015e392c644913ca11ad56a0843e3d4f66518db8622f95fe10d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5484f6c7f94979b767ce68a37dfee5f840b66e1fe6a4f06a019abbdc65961d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__125e0a8d138ae15d27d8139cb38f2bd924a1103f0ac2ba3852b2e30b73716bf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__805d8bea81fede28b687fdd1ac1d0be83bd4107791117da9dc493d7145cefa69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "desired_state": "desiredState",
        "disable_proxy_access": "disableProxyAccess",
        "enable_third_party_identity": "enableThirdPartyIdentity",
        "gce_setup": "gceSetup",
        "id": "id",
        "instance_id": "instanceId",
        "instance_owners": "instanceOwners",
        "labels": "labels",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleWorkbenchInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        name: builtins.str,
        desired_state: typing.Optional[builtins.str] = None,
        disable_proxy_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_third_party_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gce_setup: typing.Optional[typing.Union["GoogleWorkbenchInstanceGceSetup", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_id: typing.Optional[builtins.str] = None,
        instance_owners: typing.Optional[typing.Sequence[builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleWorkbenchInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Part of 'parent'. See documentation of 'projectsId'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#location GoogleWorkbenchInstance#location}
        :param name: The name of this workbench instance. Format: 'projects/{project_id}/locations/{location}/instances/{instance_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#name GoogleWorkbenchInstance#name}
        :param desired_state: Desired state of the Workbench Instance. Set this field to 'ACTIVE' to start the Instance, and 'STOPPED' to stop the Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#desired_state GoogleWorkbenchInstance#desired_state}
        :param disable_proxy_access: Optional. If true, the workbench instance will not register with the proxy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disable_proxy_access GoogleWorkbenchInstance#disable_proxy_access}
        :param enable_third_party_identity: Flag that specifies that a notebook can be accessed with third party identity provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#enable_third_party_identity GoogleWorkbenchInstance#enable_third_party_identity}
        :param gce_setup: gce_setup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#gce_setup GoogleWorkbenchInstance#gce_setup}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#id GoogleWorkbenchInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_id: Required. User-defined unique ID of this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#instance_id GoogleWorkbenchInstance#instance_id}
        :param instance_owners: 'Optional. Input only. The owner of this instance after creation. Format: 'alias@example.com' Currently supports one owner only. If not specified, all of the service account users of your VM instance''s service account can use the instance. If specified, sets the access mode to 'Single user'. For more details, see https://cloud.google.com/vertex-ai/docs/workbench/instances/manage-access-jupyterlab' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#instance_owners GoogleWorkbenchInstance#instance_owners}
        :param labels: Optional. Labels to apply to this instance. These can be later modified by the UpdateInstance method. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#labels GoogleWorkbenchInstance#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#project GoogleWorkbenchInstance#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#timeouts GoogleWorkbenchInstance#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(gce_setup, dict):
            gce_setup = GoogleWorkbenchInstanceGceSetup(**gce_setup)
        if isinstance(timeouts, dict):
            timeouts = GoogleWorkbenchInstanceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4030cf79fb19100ae93bdf179373455be412fb43cff86c430c8ab8cfc05f5928)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument desired_state", value=desired_state, expected_type=type_hints["desired_state"])
            check_type(argname="argument disable_proxy_access", value=disable_proxy_access, expected_type=type_hints["disable_proxy_access"])
            check_type(argname="argument enable_third_party_identity", value=enable_third_party_identity, expected_type=type_hints["enable_third_party_identity"])
            check_type(argname="argument gce_setup", value=gce_setup, expected_type=type_hints["gce_setup"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument instance_owners", value=instance_owners, expected_type=type_hints["instance_owners"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
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
        if desired_state is not None:
            self._values["desired_state"] = desired_state
        if disable_proxy_access is not None:
            self._values["disable_proxy_access"] = disable_proxy_access
        if enable_third_party_identity is not None:
            self._values["enable_third_party_identity"] = enable_third_party_identity
        if gce_setup is not None:
            self._values["gce_setup"] = gce_setup
        if id is not None:
            self._values["id"] = id
        if instance_id is not None:
            self._values["instance_id"] = instance_id
        if instance_owners is not None:
            self._values["instance_owners"] = instance_owners
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
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
    def location(self) -> builtins.str:
        '''Part of 'parent'. See documentation of 'projectsId'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#location GoogleWorkbenchInstance#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of this workbench instance. Format: 'projects/{project_id}/locations/{location}/instances/{instance_id}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#name GoogleWorkbenchInstance#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def desired_state(self) -> typing.Optional[builtins.str]:
        '''Desired state of the Workbench Instance.

        Set this field to 'ACTIVE' to start the Instance, and 'STOPPED' to stop the Instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#desired_state GoogleWorkbenchInstance#desired_state}
        '''
        result = self._values.get("desired_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_proxy_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. If true, the workbench instance will not register with the proxy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disable_proxy_access GoogleWorkbenchInstance#disable_proxy_access}
        '''
        result = self._values.get("disable_proxy_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_third_party_identity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag that specifies that a notebook can be accessed with third party identity provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#enable_third_party_identity GoogleWorkbenchInstance#enable_third_party_identity}
        '''
        result = self._values.get("enable_third_party_identity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gce_setup(self) -> typing.Optional["GoogleWorkbenchInstanceGceSetup"]:
        '''gce_setup block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#gce_setup GoogleWorkbenchInstance#gce_setup}
        '''
        result = self._values.get("gce_setup")
        return typing.cast(typing.Optional["GoogleWorkbenchInstanceGceSetup"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#id GoogleWorkbenchInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''Required. User-defined unique ID of this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#instance_id GoogleWorkbenchInstance#instance_id}
        '''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_owners(self) -> typing.Optional[typing.List[builtins.str]]:
        ''''Optional.

        Input only. The owner of this instance after creation. Format:
        'alias@example.com' Currently supports one owner only. If not specified, all of
        the service account users of your VM instance''s service account can use the instance.
        If specified, sets the access mode to 'Single user'. For more details, see
        https://cloud.google.com/vertex-ai/docs/workbench/instances/manage-access-jupyterlab'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#instance_owners GoogleWorkbenchInstance#instance_owners}
        '''
        result = self._values.get("instance_owners")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. Labels to apply to this instance. These can be later modified by the UpdateInstance method.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#labels GoogleWorkbenchInstance#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#project GoogleWorkbenchInstance#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleWorkbenchInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#timeouts GoogleWorkbenchInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleWorkbenchInstanceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkbenchInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetup",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_configs": "acceleratorConfigs",
        "boot_disk": "bootDisk",
        "confidential_instance_config": "confidentialInstanceConfig",
        "container_image": "containerImage",
        "data_disks": "dataDisks",
        "disable_public_ip": "disablePublicIp",
        "enable_ip_forwarding": "enableIpForwarding",
        "machine_type": "machineType",
        "metadata": "metadata",
        "network_interfaces": "networkInterfaces",
        "service_accounts": "serviceAccounts",
        "shielded_instance_config": "shieldedInstanceConfig",
        "tags": "tags",
        "vm_image": "vmImage",
    },
)
class GoogleWorkbenchInstanceGceSetup:
    def __init__(
        self,
        *,
        accelerator_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleWorkbenchInstanceGceSetupAcceleratorConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        boot_disk: typing.Optional[typing.Union["GoogleWorkbenchInstanceGceSetupBootDisk", typing.Dict[builtins.str, typing.Any]]] = None,
        confidential_instance_config: typing.Optional[typing.Union["GoogleWorkbenchInstanceGceSetupConfidentialInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        container_image: typing.Optional[typing.Union["GoogleWorkbenchInstanceGceSetupContainerImage", typing.Dict[builtins.str, typing.Any]]] = None,
        data_disks: typing.Optional[typing.Union["GoogleWorkbenchInstanceGceSetupDataDisks", typing.Dict[builtins.str, typing.Any]]] = None,
        disable_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_ip_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        machine_type: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network_interfaces: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleWorkbenchInstanceGceSetupNetworkInterfaces", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_accounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleWorkbenchInstanceGceSetupServiceAccounts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        shielded_instance_config: typing.Optional[typing.Union["GoogleWorkbenchInstanceGceSetupShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        vm_image: typing.Optional[typing.Union["GoogleWorkbenchInstanceGceSetupVmImage", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param accelerator_configs: accelerator_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#accelerator_configs GoogleWorkbenchInstance#accelerator_configs}
        :param boot_disk: boot_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#boot_disk GoogleWorkbenchInstance#boot_disk}
        :param confidential_instance_config: confidential_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#confidential_instance_config GoogleWorkbenchInstance#confidential_instance_config}
        :param container_image: container_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#container_image GoogleWorkbenchInstance#container_image}
        :param data_disks: data_disks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#data_disks GoogleWorkbenchInstance#data_disks}
        :param disable_public_ip: Optional. If true, no external IP will be assigned to this VM instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disable_public_ip GoogleWorkbenchInstance#disable_public_ip}
        :param enable_ip_forwarding: Optional. Flag to enable ip forwarding or not, default false/off. https://cloud.google.com/vpc/docs/using-routes#canipforward. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#enable_ip_forwarding GoogleWorkbenchInstance#enable_ip_forwarding}
        :param machine_type: Optional. The machine type of the VM instance. https://cloud.google.com/compute/docs/machine-resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#machine_type GoogleWorkbenchInstance#machine_type}
        :param metadata: Optional. Custom metadata to apply to this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#metadata GoogleWorkbenchInstance#metadata}
        :param network_interfaces: network_interfaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#network_interfaces GoogleWorkbenchInstance#network_interfaces}
        :param service_accounts: service_accounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#service_accounts GoogleWorkbenchInstance#service_accounts}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#shielded_instance_config GoogleWorkbenchInstance#shielded_instance_config}
        :param tags: Optional. The Compute Engine tags to add to instance (see `Tagging instances <https://cloud.google.com/compute/docs/label-or-tag-resources#tags>`_). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#tags GoogleWorkbenchInstance#tags}
        :param vm_image: vm_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#vm_image GoogleWorkbenchInstance#vm_image}
        '''
        if isinstance(boot_disk, dict):
            boot_disk = GoogleWorkbenchInstanceGceSetupBootDisk(**boot_disk)
        if isinstance(confidential_instance_config, dict):
            confidential_instance_config = GoogleWorkbenchInstanceGceSetupConfidentialInstanceConfig(**confidential_instance_config)
        if isinstance(container_image, dict):
            container_image = GoogleWorkbenchInstanceGceSetupContainerImage(**container_image)
        if isinstance(data_disks, dict):
            data_disks = GoogleWorkbenchInstanceGceSetupDataDisks(**data_disks)
        if isinstance(shielded_instance_config, dict):
            shielded_instance_config = GoogleWorkbenchInstanceGceSetupShieldedInstanceConfig(**shielded_instance_config)
        if isinstance(vm_image, dict):
            vm_image = GoogleWorkbenchInstanceGceSetupVmImage(**vm_image)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1accb2772934bcfcedf95f72a3248e4ba6d7a23b5c8dc225160c260d98f9088)
            check_type(argname="argument accelerator_configs", value=accelerator_configs, expected_type=type_hints["accelerator_configs"])
            check_type(argname="argument boot_disk", value=boot_disk, expected_type=type_hints["boot_disk"])
            check_type(argname="argument confidential_instance_config", value=confidential_instance_config, expected_type=type_hints["confidential_instance_config"])
            check_type(argname="argument container_image", value=container_image, expected_type=type_hints["container_image"])
            check_type(argname="argument data_disks", value=data_disks, expected_type=type_hints["data_disks"])
            check_type(argname="argument disable_public_ip", value=disable_public_ip, expected_type=type_hints["disable_public_ip"])
            check_type(argname="argument enable_ip_forwarding", value=enable_ip_forwarding, expected_type=type_hints["enable_ip_forwarding"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument network_interfaces", value=network_interfaces, expected_type=type_hints["network_interfaces"])
            check_type(argname="argument service_accounts", value=service_accounts, expected_type=type_hints["service_accounts"])
            check_type(argname="argument shielded_instance_config", value=shielded_instance_config, expected_type=type_hints["shielded_instance_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vm_image", value=vm_image, expected_type=type_hints["vm_image"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerator_configs is not None:
            self._values["accelerator_configs"] = accelerator_configs
        if boot_disk is not None:
            self._values["boot_disk"] = boot_disk
        if confidential_instance_config is not None:
            self._values["confidential_instance_config"] = confidential_instance_config
        if container_image is not None:
            self._values["container_image"] = container_image
        if data_disks is not None:
            self._values["data_disks"] = data_disks
        if disable_public_ip is not None:
            self._values["disable_public_ip"] = disable_public_ip
        if enable_ip_forwarding is not None:
            self._values["enable_ip_forwarding"] = enable_ip_forwarding
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if metadata is not None:
            self._values["metadata"] = metadata
        if network_interfaces is not None:
            self._values["network_interfaces"] = network_interfaces
        if service_accounts is not None:
            self._values["service_accounts"] = service_accounts
        if shielded_instance_config is not None:
            self._values["shielded_instance_config"] = shielded_instance_config
        if tags is not None:
            self._values["tags"] = tags
        if vm_image is not None:
            self._values["vm_image"] = vm_image

    @builtins.property
    def accelerator_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkbenchInstanceGceSetupAcceleratorConfigs"]]]:
        '''accelerator_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#accelerator_configs GoogleWorkbenchInstance#accelerator_configs}
        '''
        result = self._values.get("accelerator_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkbenchInstanceGceSetupAcceleratorConfigs"]]], result)

    @builtins.property
    def boot_disk(self) -> typing.Optional["GoogleWorkbenchInstanceGceSetupBootDisk"]:
        '''boot_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#boot_disk GoogleWorkbenchInstance#boot_disk}
        '''
        result = self._values.get("boot_disk")
        return typing.cast(typing.Optional["GoogleWorkbenchInstanceGceSetupBootDisk"], result)

    @builtins.property
    def confidential_instance_config(
        self,
    ) -> typing.Optional["GoogleWorkbenchInstanceGceSetupConfidentialInstanceConfig"]:
        '''confidential_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#confidential_instance_config GoogleWorkbenchInstance#confidential_instance_config}
        '''
        result = self._values.get("confidential_instance_config")
        return typing.cast(typing.Optional["GoogleWorkbenchInstanceGceSetupConfidentialInstanceConfig"], result)

    @builtins.property
    def container_image(
        self,
    ) -> typing.Optional["GoogleWorkbenchInstanceGceSetupContainerImage"]:
        '''container_image block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#container_image GoogleWorkbenchInstance#container_image}
        '''
        result = self._values.get("container_image")
        return typing.cast(typing.Optional["GoogleWorkbenchInstanceGceSetupContainerImage"], result)

    @builtins.property
    def data_disks(self) -> typing.Optional["GoogleWorkbenchInstanceGceSetupDataDisks"]:
        '''data_disks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#data_disks GoogleWorkbenchInstance#data_disks}
        '''
        result = self._values.get("data_disks")
        return typing.cast(typing.Optional["GoogleWorkbenchInstanceGceSetupDataDisks"], result)

    @builtins.property
    def disable_public_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. If true, no external IP will be assigned to this VM instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disable_public_ip GoogleWorkbenchInstance#disable_public_ip}
        '''
        result = self._values.get("disable_public_ip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_ip_forwarding(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. Flag to enable ip forwarding or not, default false/off. https://cloud.google.com/vpc/docs/using-routes#canipforward.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#enable_ip_forwarding GoogleWorkbenchInstance#enable_ip_forwarding}
        '''
        result = self._values.get("enable_ip_forwarding")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''Optional. The machine type of the VM instance. https://cloud.google.com/compute/docs/machine-resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#machine_type GoogleWorkbenchInstance#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. Custom metadata to apply to this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#metadata GoogleWorkbenchInstance#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def network_interfaces(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkbenchInstanceGceSetupNetworkInterfaces"]]]:
        '''network_interfaces block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#network_interfaces GoogleWorkbenchInstance#network_interfaces}
        '''
        result = self._values.get("network_interfaces")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkbenchInstanceGceSetupNetworkInterfaces"]]], result)

    @builtins.property
    def service_accounts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkbenchInstanceGceSetupServiceAccounts"]]]:
        '''service_accounts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#service_accounts GoogleWorkbenchInstance#service_accounts}
        '''
        result = self._values.get("service_accounts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkbenchInstanceGceSetupServiceAccounts"]]], result)

    @builtins.property
    def shielded_instance_config(
        self,
    ) -> typing.Optional["GoogleWorkbenchInstanceGceSetupShieldedInstanceConfig"]:
        '''shielded_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#shielded_instance_config GoogleWorkbenchInstance#shielded_instance_config}
        '''
        result = self._values.get("shielded_instance_config")
        return typing.cast(typing.Optional["GoogleWorkbenchInstanceGceSetupShieldedInstanceConfig"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. The Compute Engine tags to add to instance (see `Tagging instances <https://cloud.google.com/compute/docs/label-or-tag-resources#tags>`_).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#tags GoogleWorkbenchInstance#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vm_image(self) -> typing.Optional["GoogleWorkbenchInstanceGceSetupVmImage"]:
        '''vm_image block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#vm_image GoogleWorkbenchInstance#vm_image}
        '''
        result = self._values.get("vm_image")
        return typing.cast(typing.Optional["GoogleWorkbenchInstanceGceSetupVmImage"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkbenchInstanceGceSetup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupAcceleratorConfigs",
    jsii_struct_bases=[],
    name_mapping={"core_count": "coreCount", "type": "type"},
)
class GoogleWorkbenchInstanceGceSetupAcceleratorConfigs:
    def __init__(
        self,
        *,
        core_count: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param core_count: Optional. Count of cores of this accelerator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#core_count GoogleWorkbenchInstance#core_count}
        :param type: Optional. Type of this accelerator. Possible values: ["NVIDIA_TESLA_P100", "NVIDIA_TESLA_V100", "NVIDIA_TESLA_P4", "NVIDIA_TESLA_T4", "NVIDIA_TESLA_A100", "NVIDIA_A100_80GB", "NVIDIA_L4", "NVIDIA_TESLA_T4_VWS", "NVIDIA_TESLA_P100_VWS", "NVIDIA_TESLA_P4_VWS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#type GoogleWorkbenchInstance#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__785ac42bb12283ef184ded10f5f5e4149ae6cb42f6ea6e0fdd77f75dace5ac12)
            check_type(argname="argument core_count", value=core_count, expected_type=type_hints["core_count"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if core_count is not None:
            self._values["core_count"] = core_count
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def core_count(self) -> typing.Optional[builtins.str]:
        '''Optional. Count of cores of this accelerator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#core_count GoogleWorkbenchInstance#core_count}
        '''
        result = self._values.get("core_count")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Optional. Type of this accelerator. Possible values: ["NVIDIA_TESLA_P100", "NVIDIA_TESLA_V100", "NVIDIA_TESLA_P4", "NVIDIA_TESLA_T4", "NVIDIA_TESLA_A100", "NVIDIA_A100_80GB", "NVIDIA_L4", "NVIDIA_TESLA_T4_VWS", "NVIDIA_TESLA_P100_VWS", "NVIDIA_TESLA_P4_VWS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#type GoogleWorkbenchInstance#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkbenchInstanceGceSetupAcceleratorConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkbenchInstanceGceSetupAcceleratorConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupAcceleratorConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa92c4a4fe5c98657b8b6a4ec9b3bd155a437f58e08eb88ee0a2919036380781)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleWorkbenchInstanceGceSetupAcceleratorConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8623a5b62aea6bcb83f5d7a981670a8707215ceae0bd38b6199729132ec028dc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleWorkbenchInstanceGceSetupAcceleratorConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3296a6b6c51e15e8b8a82088763fc2c46f50dd4b0de80e3599489d7ddf317152)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30b01e625ab0250e4d970c3d38d60691e85c12a7863f9b8db49da347f48d6b18)
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
            type_hints = typing.get_type_hints(_typecheckingstub__008cf437e26d4129b6ff7c715d116c3d07895ce0fab32253cb21766f287fcb9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkbenchInstanceGceSetupAcceleratorConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkbenchInstanceGceSetupAcceleratorConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkbenchInstanceGceSetupAcceleratorConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2523f7db67dfe41dc884a76129f243204404c31e20a811dbc82653551133188a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleWorkbenchInstanceGceSetupAcceleratorConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupAcceleratorConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a254f3ac8e1b0dc196ee69068fdc0eba1da869c9f5f565da2cc1ce54294206ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCoreCount")
    def reset_core_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoreCount", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="coreCountInput")
    def core_count_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "coreCountInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="coreCount")
    def core_count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "coreCount"))

    @core_count.setter
    def core_count(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50905350d97e54150b3faf218797524b7f7da692b598bd1f7e3db8d64a47ea95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coreCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f89a6db06d8670e762d0d1e43db0e688cb53e5037b70364c03cfcb3cf4f4def5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkbenchInstanceGceSetupAcceleratorConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkbenchInstanceGceSetupAcceleratorConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkbenchInstanceGceSetupAcceleratorConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__144ca4c5eb4da82e6ab243677d928b1e15c8a4df43dade89a7476220b41d3858)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupBootDisk",
    jsii_struct_bases=[],
    name_mapping={
        "disk_encryption": "diskEncryption",
        "disk_size_gb": "diskSizeGb",
        "disk_type": "diskType",
        "kms_key": "kmsKey",
    },
)
class GoogleWorkbenchInstanceGceSetupBootDisk:
    def __init__(
        self,
        *,
        disk_encryption: typing.Optional[builtins.str] = None,
        disk_size_gb: typing.Optional[builtins.str] = None,
        disk_type: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_encryption: Optional. Input only. Disk encryption method used on the boot and data disks, defaults to GMEK. Possible values: ["GMEK", "CMEK"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disk_encryption GoogleWorkbenchInstance#disk_encryption}
        :param disk_size_gb: Optional. The size of the boot disk in GB attached to this instance, up to a maximum of 64000 GB (64 TB). If not specified, this defaults to the recommended value of 150GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disk_size_gb GoogleWorkbenchInstance#disk_size_gb}
        :param disk_type: Optional. Indicates the type of the disk. Possible values: ["PD_STANDARD", "PD_SSD", "PD_BALANCED", "PD_EXTREME"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disk_type GoogleWorkbenchInstance#disk_type}
        :param kms_key: 'Optional. The KMS key used to encrypt the disks, only applicable if disk_encryption is CMEK. Format: 'projects/{project_id}/locations/{location}/keyRings/{key_ring_id}/cryptoKeys/{key_id}' Learn more about using your own encryption keys.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#kms_key GoogleWorkbenchInstance#kms_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bb726a73ab5bc37e4b46e18e8b8cb837f3b0d93772d4f9d490cf6017c1afab0)
            check_type(argname="argument disk_encryption", value=disk_encryption, expected_type=type_hints["disk_encryption"])
            check_type(argname="argument disk_size_gb", value=disk_size_gb, expected_type=type_hints["disk_size_gb"])
            check_type(argname="argument disk_type", value=disk_type, expected_type=type_hints["disk_type"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disk_encryption is not None:
            self._values["disk_encryption"] = disk_encryption
        if disk_size_gb is not None:
            self._values["disk_size_gb"] = disk_size_gb
        if disk_type is not None:
            self._values["disk_type"] = disk_type
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def disk_encryption(self) -> typing.Optional[builtins.str]:
        '''Optional. Input only. Disk encryption method used on the boot and data disks, defaults to GMEK. Possible values: ["GMEK", "CMEK"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disk_encryption GoogleWorkbenchInstance#disk_encryption}
        '''
        result = self._values.get("disk_encryption")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_size_gb(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The size of the boot disk in GB attached to this instance,
        up to a maximum of 64000 GB (64 TB). If not specified, this defaults to the
        recommended value of 150GB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disk_size_gb GoogleWorkbenchInstance#disk_size_gb}
        '''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_type(self) -> typing.Optional[builtins.str]:
        '''Optional. Indicates the type of the disk. Possible values: ["PD_STANDARD", "PD_SSD", "PD_BALANCED", "PD_EXTREME"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disk_type GoogleWorkbenchInstance#disk_type}
        '''
        result = self._values.get("disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        ''''Optional.

        The KMS key used to encrypt the disks, only
        applicable if disk_encryption is CMEK. Format: 'projects/{project_id}/locations/{location}/keyRings/{key_ring_id}/cryptoKeys/{key_id}'
        Learn more about using your own encryption keys.'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#kms_key GoogleWorkbenchInstance#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkbenchInstanceGceSetupBootDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkbenchInstanceGceSetupBootDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupBootDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d172fd08e8f8434525cf12fec7a51b4bc7fdb911be99675c1581d2a97ad5ab1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDiskEncryption")
    def reset_disk_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryption", []))

    @jsii.member(jsii_name="resetDiskSizeGb")
    def reset_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskSizeGb", []))

    @jsii.member(jsii_name="resetDiskType")
    def reset_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskType", []))

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionInput")
    def disk_encryption_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGbInput")
    def disk_size_gb_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="diskTypeInput")
    def disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryption")
    def disk_encryption(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryption"))

    @disk_encryption.setter
    def disk_encryption(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49f3fb9d13099ca4f744475b6b01f774edc28e5dadb3f455c3e93313a13bf9aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65232d63bdc0a1790a9e323c3731f366cb1d1c4afd0ed02c36da9096ffb290f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskType")
    def disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskType"))

    @disk_type.setter
    def disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5310038c52252ca8c9cadc7c50aa0cca65bc341dd0a4c275439ba49a9a8744cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__414faa05ea8a8719f54aaf6d41326fe318c980b14bfed34cd1f2ce7d33552590)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleWorkbenchInstanceGceSetupBootDisk]:
        return typing.cast(typing.Optional[GoogleWorkbenchInstanceGceSetupBootDisk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleWorkbenchInstanceGceSetupBootDisk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c23b0b6c2e086e7bb1c5e6009f12a321bb932485907d3f0d8287d98a593e083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupConfidentialInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={"confidential_instance_type": "confidentialInstanceType"},
)
class GoogleWorkbenchInstanceGceSetupConfidentialInstanceConfig:
    def __init__(
        self,
        *,
        confidential_instance_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param confidential_instance_type: Defines the type of technology used by the confidential instance. Possible values: ["SEV"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#confidential_instance_type GoogleWorkbenchInstance#confidential_instance_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a3cec256939313e4c4bb3dc9d88df50a8d0eedb7926e434c101567e3c33f957)
            check_type(argname="argument confidential_instance_type", value=confidential_instance_type, expected_type=type_hints["confidential_instance_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if confidential_instance_type is not None:
            self._values["confidential_instance_type"] = confidential_instance_type

    @builtins.property
    def confidential_instance_type(self) -> typing.Optional[builtins.str]:
        '''Defines the type of technology used by the confidential instance. Possible values: ["SEV"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#confidential_instance_type GoogleWorkbenchInstance#confidential_instance_type}
        '''
        result = self._values.get("confidential_instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkbenchInstanceGceSetupConfidentialInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkbenchInstanceGceSetupConfidentialInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupConfidentialInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca565113f6bfcfb299234b75d613963d1fbc2835bf72639a2374bec1387e7924)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConfidentialInstanceType")
    def reset_confidential_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidentialInstanceType", []))

    @builtins.property
    @jsii.member(jsii_name="confidentialInstanceTypeInput")
    def confidential_instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "confidentialInstanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="confidentialInstanceType")
    def confidential_instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "confidentialInstanceType"))

    @confidential_instance_type.setter
    def confidential_instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f20e995e599f572943c8041fe5827e74f6079ec05cd44930e5c667af63d1d95b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidentialInstanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleWorkbenchInstanceGceSetupConfidentialInstanceConfig]:
        return typing.cast(typing.Optional[GoogleWorkbenchInstanceGceSetupConfidentialInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleWorkbenchInstanceGceSetupConfidentialInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b290e9d94935e401b5b6e936dfb991b59ca91cabe4f8501152a9c31e949125aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupContainerImage",
    jsii_struct_bases=[],
    name_mapping={"repository": "repository", "tag": "tag"},
)
class GoogleWorkbenchInstanceGceSetupContainerImage:
    def __init__(
        self,
        *,
        repository: builtins.str,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repository: The path to the container image repository. For example: gcr.io/{project_id}/{imageName}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#repository GoogleWorkbenchInstance#repository}
        :param tag: The tag of the container image. If not specified, this defaults to the latest tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#tag GoogleWorkbenchInstance#tag}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ba12d30c6e173ef027fa5507ad93ee12779209ebf8410df3149849ed4b73e02)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository": repository,
        }
        if tag is not None:
            self._values["tag"] = tag

    @builtins.property
    def repository(self) -> builtins.str:
        '''The path to the container image repository. For example: gcr.io/{project_id}/{imageName}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#repository GoogleWorkbenchInstance#repository}
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''The tag of the container image. If not specified, this defaults to the latest tag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#tag GoogleWorkbenchInstance#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkbenchInstanceGceSetupContainerImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkbenchInstanceGceSetupContainerImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupContainerImageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__300db7a7e32ef452205c27a54cdfa63941cad689fc1e9880fa10478b47d3ad51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f9e97482504ab11529924f121dc651818f343863a50e43151c355daba6637f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0710e05b9481f735271e401b1141397ee5972be0c78931ba8ae1c4fd2c2203bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleWorkbenchInstanceGceSetupContainerImage]:
        return typing.cast(typing.Optional[GoogleWorkbenchInstanceGceSetupContainerImage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleWorkbenchInstanceGceSetupContainerImage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__179f52f9925615a1c3155e5fa5f2a6b9ca59d06d64346093ff41c50658577841)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupDataDisks",
    jsii_struct_bases=[],
    name_mapping={
        "disk_encryption": "diskEncryption",
        "disk_size_gb": "diskSizeGb",
        "disk_type": "diskType",
        "kms_key": "kmsKey",
    },
)
class GoogleWorkbenchInstanceGceSetupDataDisks:
    def __init__(
        self,
        *,
        disk_encryption: typing.Optional[builtins.str] = None,
        disk_size_gb: typing.Optional[builtins.str] = None,
        disk_type: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_encryption: Optional. Input only. Disk encryption method used on the boot and data disks, defaults to GMEK. Possible values: ["GMEK", "CMEK"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disk_encryption GoogleWorkbenchInstance#disk_encryption}
        :param disk_size_gb: Optional. The size of the disk in GB attached to this VM instance, up to a maximum of 64000 GB (64 TB). If not specified, this defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disk_size_gb GoogleWorkbenchInstance#disk_size_gb}
        :param disk_type: Optional. Input only. Indicates the type of the disk. Possible values: ["PD_STANDARD", "PD_SSD", "PD_BALANCED", "PD_EXTREME"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disk_type GoogleWorkbenchInstance#disk_type}
        :param kms_key: 'Optional. The KMS key used to encrypt the disks, only applicable if disk_encryption is CMEK. Format: 'projects/{project_id}/locations/{location}/keyRings/{key_ring_id}/cryptoKeys/{key_id}' Learn more about using your own encryption keys.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#kms_key GoogleWorkbenchInstance#kms_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a25a1ba2035e45b5c56b74d67595a9e30f56f5d5da0ab7b40f8fe71b7fc48298)
            check_type(argname="argument disk_encryption", value=disk_encryption, expected_type=type_hints["disk_encryption"])
            check_type(argname="argument disk_size_gb", value=disk_size_gb, expected_type=type_hints["disk_size_gb"])
            check_type(argname="argument disk_type", value=disk_type, expected_type=type_hints["disk_type"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disk_encryption is not None:
            self._values["disk_encryption"] = disk_encryption
        if disk_size_gb is not None:
            self._values["disk_size_gb"] = disk_size_gb
        if disk_type is not None:
            self._values["disk_type"] = disk_type
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def disk_encryption(self) -> typing.Optional[builtins.str]:
        '''Optional. Input only. Disk encryption method used on the boot and data disks, defaults to GMEK. Possible values: ["GMEK", "CMEK"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disk_encryption GoogleWorkbenchInstance#disk_encryption}
        '''
        result = self._values.get("disk_encryption")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_size_gb(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The size of the disk in GB attached to this VM instance,
        up to a maximum of 64000 GB (64 TB). If not specified, this defaults to
        100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disk_size_gb GoogleWorkbenchInstance#disk_size_gb}
        '''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_type(self) -> typing.Optional[builtins.str]:
        '''Optional. Input only. Indicates the type of the disk. Possible values: ["PD_STANDARD", "PD_SSD", "PD_BALANCED", "PD_EXTREME"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disk_type GoogleWorkbenchInstance#disk_type}
        '''
        result = self._values.get("disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        ''''Optional.

        The KMS key used to encrypt the disks,
        only applicable if disk_encryption is CMEK. Format: 'projects/{project_id}/locations/{location}/keyRings/{key_ring_id}/cryptoKeys/{key_id}'
        Learn more about using your own encryption keys.'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#kms_key GoogleWorkbenchInstance#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkbenchInstanceGceSetupDataDisks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkbenchInstanceGceSetupDataDisksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupDataDisksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__993bf2eb332e8d38482521c71ad1bd7f60a2a99ab274099e9c0934ffe020e500)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDiskEncryption")
    def reset_disk_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryption", []))

    @jsii.member(jsii_name="resetDiskSizeGb")
    def reset_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskSizeGb", []))

    @jsii.member(jsii_name="resetDiskType")
    def reset_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskType", []))

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionInput")
    def disk_encryption_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGbInput")
    def disk_size_gb_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="diskTypeInput")
    def disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryption")
    def disk_encryption(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryption"))

    @disk_encryption.setter
    def disk_encryption(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b69667b64fee0aaaf3806f4cc96a926070738c0fb396786ef84672c3ccdf7656)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__880c53989793938354a7ef67adc744d728d93f398b4c4153527159364bc9c3fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskType")
    def disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskType"))

    @disk_type.setter
    def disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19002d6585176543da9ec16f6f27bf2fae49eefc5a545174a420a88da914ed9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ced8bce1a006f515abb2661144fca99ad4f3c8a1c11ea9d48fbcea26a63008)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleWorkbenchInstanceGceSetupDataDisks]:
        return typing.cast(typing.Optional[GoogleWorkbenchInstanceGceSetupDataDisks], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleWorkbenchInstanceGceSetupDataDisks],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb0aca2d180926114c2dbf35c89d79e11613feaf2b13b935bef08f5e2509eacd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupNetworkInterfaces",
    jsii_struct_bases=[],
    name_mapping={
        "access_configs": "accessConfigs",
        "network": "network",
        "nic_type": "nicType",
        "subnet": "subnet",
    },
)
class GoogleWorkbenchInstanceGceSetupNetworkInterfaces:
    def __init__(
        self,
        *,
        access_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network: typing.Optional[builtins.str] = None,
        nic_type: typing.Optional[builtins.str] = None,
        subnet: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_configs: access_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#access_configs GoogleWorkbenchInstance#access_configs}
        :param network: Optional. The name of the VPC that this VM instance is in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#network GoogleWorkbenchInstance#network}
        :param nic_type: Optional. The type of vNIC to be used on this interface. This may be gVNIC or VirtioNet. Possible values: ["VIRTIO_NET", "GVNIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#nic_type GoogleWorkbenchInstance#nic_type}
        :param subnet: Optional. The name of the subnet that this VM instance is in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#subnet GoogleWorkbenchInstance#subnet}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1a75cd02a1564f1f6a51d387b54d7cfbbf3ed5b0fd5a3176fc153345415d19b)
            check_type(argname="argument access_configs", value=access_configs, expected_type=type_hints["access_configs"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument nic_type", value=nic_type, expected_type=type_hints["nic_type"])
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_configs is not None:
            self._values["access_configs"] = access_configs
        if network is not None:
            self._values["network"] = network
        if nic_type is not None:
            self._values["nic_type"] = nic_type
        if subnet is not None:
            self._values["subnet"] = subnet

    @builtins.property
    def access_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs"]]]:
        '''access_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#access_configs GoogleWorkbenchInstance#access_configs}
        '''
        result = self._values.get("access_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs"]]], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''Optional. The name of the VPC that this VM instance is in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#network GoogleWorkbenchInstance#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nic_type(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The type of vNIC to be used on this interface. This
        may be gVNIC or VirtioNet. Possible values: ["VIRTIO_NET", "GVNIC"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#nic_type GoogleWorkbenchInstance#nic_type}
        '''
        result = self._values.get("nic_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet(self) -> typing.Optional[builtins.str]:
        '''Optional. The name of the subnet that this VM instance is in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#subnet GoogleWorkbenchInstance#subnet}
        '''
        result = self._values.get("subnet")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkbenchInstanceGceSetupNetworkInterfaces(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs",
    jsii_struct_bases=[],
    name_mapping={"external_ip": "externalIp"},
)
class GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs:
    def __init__(self, *, external_ip: builtins.str) -> None:
        '''
        :param external_ip: An external IP address associated with this instance. Specify an unused static external IP address available to the project or leave this field undefined to use an IP from a shared ephemeral IP address pool. If you specify a static external IP address, it must live in the same region as the zone of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#external_ip GoogleWorkbenchInstance#external_ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c776f4d1e00259fe5c54c99a7a364dcc2374e3caaacdc37e2b9bd6fe66cf87d3)
            check_type(argname="argument external_ip", value=external_ip, expected_type=type_hints["external_ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "external_ip": external_ip,
        }

    @builtins.property
    def external_ip(self) -> builtins.str:
        '''An external IP address associated with this instance.

        Specify an unused
        static external IP address available to the project or leave this field
        undefined to use an IP from a shared ephemeral IP address pool. If you
        specify a static external IP address, it must live in the same region as
        the zone of the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#external_ip GoogleWorkbenchInstance#external_ip}
        '''
        result = self._values.get("external_ip")
        assert result is not None, "Required property 'external_ip' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b676c600df134e3889c29d7d1bb137ec68de7bb2ca57363c342e9518232199d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fb9050b09156a3ff6f394f74e4e6d004e6fd96d28dcfd87fd351904d444ffbc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38c677b140074a9549aebf6a7f59de4176aea0414d0e5da6dd1f1e0b01bc1b96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__798195d4c8a98c35e46a9606d8299b8c2cf6ad022491651dd564bdb454579f1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f375931329ff6396966c6cbd4d4aa1cf62b0556dcf30e3c2d2c2337c86da37c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8880aea219b8b62ba651af33cb247c495d608f06dd8a4b212e77e9bb9398b618)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7c7adedd334e17c0d047a9fb5ca02e7e71dd819ae8cdae8fa083183061263f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="externalIpInput")
    def external_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalIpInput"))

    @builtins.property
    @jsii.member(jsii_name="externalIp")
    def external_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalIp"))

    @external_ip.setter
    def external_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__684145c3dfc460531e8b36dbd7b810f4ffd7dc98e64515f9fbe65a5634638aa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7510ed2160a5516de47bbfdf539fbc782732b029e554f49e9be9564fb1892432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleWorkbenchInstanceGceSetupNetworkInterfacesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupNetworkInterfacesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c0efc3b859a11750c160e050ac24a81e2a5703dbf3809cc8f72cce60d547c5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleWorkbenchInstanceGceSetupNetworkInterfacesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dbdf6f16376c6bff86caa66cf07c6203cb56c2ee60dcc4f3c14ebf5cc39d938)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleWorkbenchInstanceGceSetupNetworkInterfacesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92da5c5989ad4ebcff1b3b92b9bc32e3aac98c55e903efb82db192c5a2813c90)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c527293921a2cd247a8d09ba7fb7955bb0b2dd217cb4748061b7d3e1897a7640)
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
            type_hints = typing.get_type_hints(_typecheckingstub__593d1822f1d9cc6f36fed096c473fd5cd1b8eb5fa6eee3108fff8b49396940be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkbenchInstanceGceSetupNetworkInterfaces]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkbenchInstanceGceSetupNetworkInterfaces]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkbenchInstanceGceSetupNetworkInterfaces]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e90618709ad5c365021978a5eef38777a72e9592f157af43fa98f6c515f0288)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleWorkbenchInstanceGceSetupNetworkInterfacesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupNetworkInterfacesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a59ffb434cd3fbbd3ce1725d54333f54e4bf1d7d0145899895f6ad81ff254cd1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAccessConfigs")
    def put_access_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25e29c7f0894d12c503d1b33c9f45cd9ed89cb8d0fa21a2658442211ee2e19d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccessConfigs", [value]))

    @jsii.member(jsii_name="resetAccessConfigs")
    def reset_access_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessConfigs", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetNicType")
    def reset_nic_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNicType", []))

    @jsii.member(jsii_name="resetSubnet")
    def reset_subnet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnet", []))

    @builtins.property
    @jsii.member(jsii_name="accessConfigs")
    def access_configs(
        self,
    ) -> GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigsList:
        return typing.cast(GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigsList, jsii.get(self, "accessConfigs"))

    @builtins.property
    @jsii.member(jsii_name="accessConfigsInput")
    def access_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs]]], jsii.get(self, "accessConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="nicTypeInput")
    def nic_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nicTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetInput")
    def subnet_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetInput"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51b67a7975f2a755310d609206c63491cd0cb0aa89b9bc9356d7fd3f899d2384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nicType")
    def nic_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nicType"))

    @nic_type.setter
    def nic_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ff812108ace575a6e7e44e88d86f4754b535ef0f34ff84364d2b4757d827816)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nicType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnet")
    def subnet(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnet"))

    @subnet.setter
    def subnet(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ce3a4b4c081d401da8c237bbfa450b1431360d598bfe0e1300cec57a22f4c5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkbenchInstanceGceSetupNetworkInterfaces]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkbenchInstanceGceSetupNetworkInterfaces]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkbenchInstanceGceSetupNetworkInterfaces]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46fc78952cdba79d33c472dc856d00b793a93a8487cb91726101b4305a25e4d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleWorkbenchInstanceGceSetupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fbc5d215d80f6f41fa24c8baeb277ffba3e627742ae51545c2daddd20a1c378)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAcceleratorConfigs")
    def put_accelerator_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkbenchInstanceGceSetupAcceleratorConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f45f969de8fc7d2027efb133cd2b28121800bf7268c794422cd2b22efa59ace)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAcceleratorConfigs", [value]))

    @jsii.member(jsii_name="putBootDisk")
    def put_boot_disk(
        self,
        *,
        disk_encryption: typing.Optional[builtins.str] = None,
        disk_size_gb: typing.Optional[builtins.str] = None,
        disk_type: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_encryption: Optional. Input only. Disk encryption method used on the boot and data disks, defaults to GMEK. Possible values: ["GMEK", "CMEK"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disk_encryption GoogleWorkbenchInstance#disk_encryption}
        :param disk_size_gb: Optional. The size of the boot disk in GB attached to this instance, up to a maximum of 64000 GB (64 TB). If not specified, this defaults to the recommended value of 150GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disk_size_gb GoogleWorkbenchInstance#disk_size_gb}
        :param disk_type: Optional. Indicates the type of the disk. Possible values: ["PD_STANDARD", "PD_SSD", "PD_BALANCED", "PD_EXTREME"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disk_type GoogleWorkbenchInstance#disk_type}
        :param kms_key: 'Optional. The KMS key used to encrypt the disks, only applicable if disk_encryption is CMEK. Format: 'projects/{project_id}/locations/{location}/keyRings/{key_ring_id}/cryptoKeys/{key_id}' Learn more about using your own encryption keys.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#kms_key GoogleWorkbenchInstance#kms_key}
        '''
        value = GoogleWorkbenchInstanceGceSetupBootDisk(
            disk_encryption=disk_encryption,
            disk_size_gb=disk_size_gb,
            disk_type=disk_type,
            kms_key=kms_key,
        )

        return typing.cast(None, jsii.invoke(self, "putBootDisk", [value]))

    @jsii.member(jsii_name="putConfidentialInstanceConfig")
    def put_confidential_instance_config(
        self,
        *,
        confidential_instance_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param confidential_instance_type: Defines the type of technology used by the confidential instance. Possible values: ["SEV"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#confidential_instance_type GoogleWorkbenchInstance#confidential_instance_type}
        '''
        value = GoogleWorkbenchInstanceGceSetupConfidentialInstanceConfig(
            confidential_instance_type=confidential_instance_type
        )

        return typing.cast(None, jsii.invoke(self, "putConfidentialInstanceConfig", [value]))

    @jsii.member(jsii_name="putContainerImage")
    def put_container_image(
        self,
        *,
        repository: builtins.str,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repository: The path to the container image repository. For example: gcr.io/{project_id}/{imageName}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#repository GoogleWorkbenchInstance#repository}
        :param tag: The tag of the container image. If not specified, this defaults to the latest tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#tag GoogleWorkbenchInstance#tag}
        '''
        value = GoogleWorkbenchInstanceGceSetupContainerImage(
            repository=repository, tag=tag
        )

        return typing.cast(None, jsii.invoke(self, "putContainerImage", [value]))

    @jsii.member(jsii_name="putDataDisks")
    def put_data_disks(
        self,
        *,
        disk_encryption: typing.Optional[builtins.str] = None,
        disk_size_gb: typing.Optional[builtins.str] = None,
        disk_type: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_encryption: Optional. Input only. Disk encryption method used on the boot and data disks, defaults to GMEK. Possible values: ["GMEK", "CMEK"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disk_encryption GoogleWorkbenchInstance#disk_encryption}
        :param disk_size_gb: Optional. The size of the disk in GB attached to this VM instance, up to a maximum of 64000 GB (64 TB). If not specified, this defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disk_size_gb GoogleWorkbenchInstance#disk_size_gb}
        :param disk_type: Optional. Input only. Indicates the type of the disk. Possible values: ["PD_STANDARD", "PD_SSD", "PD_BALANCED", "PD_EXTREME"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#disk_type GoogleWorkbenchInstance#disk_type}
        :param kms_key: 'Optional. The KMS key used to encrypt the disks, only applicable if disk_encryption is CMEK. Format: 'projects/{project_id}/locations/{location}/keyRings/{key_ring_id}/cryptoKeys/{key_id}' Learn more about using your own encryption keys.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#kms_key GoogleWorkbenchInstance#kms_key}
        '''
        value = GoogleWorkbenchInstanceGceSetupDataDisks(
            disk_encryption=disk_encryption,
            disk_size_gb=disk_size_gb,
            disk_type=disk_type,
            kms_key=kms_key,
        )

        return typing.cast(None, jsii.invoke(self, "putDataDisks", [value]))

    @jsii.member(jsii_name="putNetworkInterfaces")
    def put_network_interfaces(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkbenchInstanceGceSetupNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af5a5a1b984db9b464641ba21f6e90d42a49252e8454688bfdd5ef824e7cff16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworkInterfaces", [value]))

    @jsii.member(jsii_name="putServiceAccounts")
    def put_service_accounts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleWorkbenchInstanceGceSetupServiceAccounts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b88755bdacfd6a23011f060052a7f5d51e2d34b9d55a4852fb6d12cb9dd12f67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putServiceAccounts", [value]))

    @jsii.member(jsii_name="putShieldedInstanceConfig")
    def put_shielded_instance_config(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Optional. Defines whether the VM instance has integrity monitoring enabled. Enables monitoring and attestation of the boot integrity of the VM instance. The attestation is performed against the integrity policy baseline. This baseline is initially derived from the implicitly trusted boot image when the VM instance is created. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#enable_integrity_monitoring GoogleWorkbenchInstance#enable_integrity_monitoring}
        :param enable_secure_boot: Optional. Defines whether the VM instance has Secure Boot enabled. Secure Boot helps ensure that the system only runs authentic software by verifying the digital signature of all boot components, and halting the boot process if signature verification fails. Disabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#enable_secure_boot GoogleWorkbenchInstance#enable_secure_boot}
        :param enable_vtpm: Optional. Defines whether the VM instance has the vTPM enabled. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#enable_vtpm GoogleWorkbenchInstance#enable_vtpm}
        '''
        value = GoogleWorkbenchInstanceGceSetupShieldedInstanceConfig(
            enable_integrity_monitoring=enable_integrity_monitoring,
            enable_secure_boot=enable_secure_boot,
            enable_vtpm=enable_vtpm,
        )

        return typing.cast(None, jsii.invoke(self, "putShieldedInstanceConfig", [value]))

    @jsii.member(jsii_name="putVmImage")
    def put_vm_image(
        self,
        *,
        family: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param family: Optional. Use this VM image family to find the image; the newest image in this family will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#family GoogleWorkbenchInstance#family}
        :param name: Optional. Use VM image name to find the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#name GoogleWorkbenchInstance#name}
        :param project: The name of the Google Cloud project that this VM image belongs to. Format: {project_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#project GoogleWorkbenchInstance#project}
        '''
        value = GoogleWorkbenchInstanceGceSetupVmImage(
            family=family, name=name, project=project
        )

        return typing.cast(None, jsii.invoke(self, "putVmImage", [value]))

    @jsii.member(jsii_name="resetAcceleratorConfigs")
    def reset_accelerator_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorConfigs", []))

    @jsii.member(jsii_name="resetBootDisk")
    def reset_boot_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDisk", []))

    @jsii.member(jsii_name="resetConfidentialInstanceConfig")
    def reset_confidential_instance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidentialInstanceConfig", []))

    @jsii.member(jsii_name="resetContainerImage")
    def reset_container_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerImage", []))

    @jsii.member(jsii_name="resetDataDisks")
    def reset_data_disks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataDisks", []))

    @jsii.member(jsii_name="resetDisablePublicIp")
    def reset_disable_public_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisablePublicIp", []))

    @jsii.member(jsii_name="resetEnableIpForwarding")
    def reset_enable_ip_forwarding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableIpForwarding", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetNetworkInterfaces")
    def reset_network_interfaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkInterfaces", []))

    @jsii.member(jsii_name="resetServiceAccounts")
    def reset_service_accounts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccounts", []))

    @jsii.member(jsii_name="resetShieldedInstanceConfig")
    def reset_shielded_instance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShieldedInstanceConfig", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetVmImage")
    def reset_vm_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmImage", []))

    @builtins.property
    @jsii.member(jsii_name="acceleratorConfigs")
    def accelerator_configs(
        self,
    ) -> GoogleWorkbenchInstanceGceSetupAcceleratorConfigsList:
        return typing.cast(GoogleWorkbenchInstanceGceSetupAcceleratorConfigsList, jsii.get(self, "acceleratorConfigs"))

    @builtins.property
    @jsii.member(jsii_name="bootDisk")
    def boot_disk(self) -> GoogleWorkbenchInstanceGceSetupBootDiskOutputReference:
        return typing.cast(GoogleWorkbenchInstanceGceSetupBootDiskOutputReference, jsii.get(self, "bootDisk"))

    @builtins.property
    @jsii.member(jsii_name="confidentialInstanceConfig")
    def confidential_instance_config(
        self,
    ) -> GoogleWorkbenchInstanceGceSetupConfidentialInstanceConfigOutputReference:
        return typing.cast(GoogleWorkbenchInstanceGceSetupConfidentialInstanceConfigOutputReference, jsii.get(self, "confidentialInstanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="containerImage")
    def container_image(
        self,
    ) -> GoogleWorkbenchInstanceGceSetupContainerImageOutputReference:
        return typing.cast(GoogleWorkbenchInstanceGceSetupContainerImageOutputReference, jsii.get(self, "containerImage"))

    @builtins.property
    @jsii.member(jsii_name="dataDisks")
    def data_disks(self) -> GoogleWorkbenchInstanceGceSetupDataDisksOutputReference:
        return typing.cast(GoogleWorkbenchInstanceGceSetupDataDisksOutputReference, jsii.get(self, "dataDisks"))

    @builtins.property
    @jsii.member(jsii_name="networkInterfaces")
    def network_interfaces(
        self,
    ) -> GoogleWorkbenchInstanceGceSetupNetworkInterfacesList:
        return typing.cast(GoogleWorkbenchInstanceGceSetupNetworkInterfacesList, jsii.get(self, "networkInterfaces"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccounts")
    def service_accounts(self) -> "GoogleWorkbenchInstanceGceSetupServiceAccountsList":
        return typing.cast("GoogleWorkbenchInstanceGceSetupServiceAccountsList", jsii.get(self, "serviceAccounts"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfig")
    def shielded_instance_config(
        self,
    ) -> "GoogleWorkbenchInstanceGceSetupShieldedInstanceConfigOutputReference":
        return typing.cast("GoogleWorkbenchInstanceGceSetupShieldedInstanceConfigOutputReference", jsii.get(self, "shieldedInstanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="vmImage")
    def vm_image(self) -> "GoogleWorkbenchInstanceGceSetupVmImageOutputReference":
        return typing.cast("GoogleWorkbenchInstanceGceSetupVmImageOutputReference", jsii.get(self, "vmImage"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorConfigsInput")
    def accelerator_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkbenchInstanceGceSetupAcceleratorConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkbenchInstanceGceSetupAcceleratorConfigs]]], jsii.get(self, "acceleratorConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskInput")
    def boot_disk_input(
        self,
    ) -> typing.Optional[GoogleWorkbenchInstanceGceSetupBootDisk]:
        return typing.cast(typing.Optional[GoogleWorkbenchInstanceGceSetupBootDisk], jsii.get(self, "bootDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="confidentialInstanceConfigInput")
    def confidential_instance_config_input(
        self,
    ) -> typing.Optional[GoogleWorkbenchInstanceGceSetupConfidentialInstanceConfig]:
        return typing.cast(typing.Optional[GoogleWorkbenchInstanceGceSetupConfidentialInstanceConfig], jsii.get(self, "confidentialInstanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="containerImageInput")
    def container_image_input(
        self,
    ) -> typing.Optional[GoogleWorkbenchInstanceGceSetupContainerImage]:
        return typing.cast(typing.Optional[GoogleWorkbenchInstanceGceSetupContainerImage], jsii.get(self, "containerImageInput"))

    @builtins.property
    @jsii.member(jsii_name="dataDisksInput")
    def data_disks_input(
        self,
    ) -> typing.Optional[GoogleWorkbenchInstanceGceSetupDataDisks]:
        return typing.cast(typing.Optional[GoogleWorkbenchInstanceGceSetupDataDisks], jsii.get(self, "dataDisksInput"))

    @builtins.property
    @jsii.member(jsii_name="disablePublicIpInput")
    def disable_public_ip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disablePublicIpInput"))

    @builtins.property
    @jsii.member(jsii_name="enableIpForwardingInput")
    def enable_ip_forwarding_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableIpForwardingInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInterfacesInput")
    def network_interfaces_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkbenchInstanceGceSetupNetworkInterfaces]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkbenchInstanceGceSetupNetworkInterfaces]]], jsii.get(self, "networkInterfacesInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountsInput")
    def service_accounts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkbenchInstanceGceSetupServiceAccounts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkbenchInstanceGceSetupServiceAccounts"]]], jsii.get(self, "serviceAccountsInput"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfigInput")
    def shielded_instance_config_input(
        self,
    ) -> typing.Optional["GoogleWorkbenchInstanceGceSetupShieldedInstanceConfig"]:
        return typing.cast(typing.Optional["GoogleWorkbenchInstanceGceSetupShieldedInstanceConfig"], jsii.get(self, "shieldedInstanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="vmImageInput")
    def vm_image_input(
        self,
    ) -> typing.Optional["GoogleWorkbenchInstanceGceSetupVmImage"]:
        return typing.cast(typing.Optional["GoogleWorkbenchInstanceGceSetupVmImage"], jsii.get(self, "vmImageInput"))

    @builtins.property
    @jsii.member(jsii_name="disablePublicIp")
    def disable_public_ip(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disablePublicIp"))

    @disable_public_ip.setter
    def disable_public_ip(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a546692c565ec155085942e1f0a558255a58a63e54514f2b2a21b1bceb139a4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disablePublicIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableIpForwarding")
    def enable_ip_forwarding(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableIpForwarding"))

    @enable_ip_forwarding.setter
    def enable_ip_forwarding(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3f4fcd48239291cd863724605cd86fe9d0f9623836c976130afca678b2a2686)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableIpForwarding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90b0eaba47871b0838bac0e5ba772a4ba72236765fd32cbf2ddc591c3576fb5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2a8b83b20c1b93e4c204c6ab7c226bcd9a3cfcb3bca688ef3b011f7e7c37f70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__997c08634d988d996a5513891fbd2052fc0987b239545d385d2307378268a237)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleWorkbenchInstanceGceSetup]:
        return typing.cast(typing.Optional[GoogleWorkbenchInstanceGceSetup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleWorkbenchInstanceGceSetup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15d10bc189c798e379eb01d2012c61c236cb384917c251d7eb648ac1491289c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupServiceAccounts",
    jsii_struct_bases=[],
    name_mapping={"email": "email"},
)
class GoogleWorkbenchInstanceGceSetupServiceAccounts:
    def __init__(self, *, email: typing.Optional[builtins.str] = None) -> None:
        '''
        :param email: Optional. Email address of the service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#email GoogleWorkbenchInstance#email}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ea30d841b6f6bb447b13855d305c3881fdcb49042983f66b5351e693739ba4)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if email is not None:
            self._values["email"] = email

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Optional. Email address of the service account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#email GoogleWorkbenchInstance#email}
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkbenchInstanceGceSetupServiceAccounts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkbenchInstanceGceSetupServiceAccountsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupServiceAccountsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fabe7294ac6a5a31814ef9a0cfdd544ab2dba66a9d9a84e10f21492a22d0c06e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleWorkbenchInstanceGceSetupServiceAccountsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83077a9a56fa7d8dad2e36d1e48c9fc76ecdb53913fa67fa394a9fd38d4ff066)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleWorkbenchInstanceGceSetupServiceAccountsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a77e4e6e1ff10dd2f2c28e19bc2cddf95625b4bebf0f57bab957196a07a2eed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8e590eb39c6c79d177226464eda0eda77765a0b933e72a5217be84f420828e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1317ae920ecc186f0969670cf21a567339324a9316bbae27a7c4f8b411360206)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkbenchInstanceGceSetupServiceAccounts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkbenchInstanceGceSetupServiceAccounts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkbenchInstanceGceSetupServiceAccounts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6781c71b8c376b3a29027082c7756e9c3fc4a02c7a45e5a971afc964026f47c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleWorkbenchInstanceGceSetupServiceAccountsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupServiceAccountsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dff9d694e7da07b1cb5afd490578858cacc8d5a1208b5646ba6c7b5b764057b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__797a69be5f604346a1bace38f42d959d3b57f2e05be443c09eab0479327d4ae1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkbenchInstanceGceSetupServiceAccounts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkbenchInstanceGceSetupServiceAccounts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkbenchInstanceGceSetupServiceAccounts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd717fa22f8b4124ba317a44c9c3794ee2bbde1666b4433befd97661046af0bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupShieldedInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_integrity_monitoring": "enableIntegrityMonitoring",
        "enable_secure_boot": "enableSecureBoot",
        "enable_vtpm": "enableVtpm",
    },
)
class GoogleWorkbenchInstanceGceSetupShieldedInstanceConfig:
    def __init__(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Optional. Defines whether the VM instance has integrity monitoring enabled. Enables monitoring and attestation of the boot integrity of the VM instance. The attestation is performed against the integrity policy baseline. This baseline is initially derived from the implicitly trusted boot image when the VM instance is created. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#enable_integrity_monitoring GoogleWorkbenchInstance#enable_integrity_monitoring}
        :param enable_secure_boot: Optional. Defines whether the VM instance has Secure Boot enabled. Secure Boot helps ensure that the system only runs authentic software by verifying the digital signature of all boot components, and halting the boot process if signature verification fails. Disabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#enable_secure_boot GoogleWorkbenchInstance#enable_secure_boot}
        :param enable_vtpm: Optional. Defines whether the VM instance has the vTPM enabled. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#enable_vtpm GoogleWorkbenchInstance#enable_vtpm}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6efd1022656f651f0bca9c44fbb902f25d5fb1c1e276079200c261510d2e940)
            check_type(argname="argument enable_integrity_monitoring", value=enable_integrity_monitoring, expected_type=type_hints["enable_integrity_monitoring"])
            check_type(argname="argument enable_secure_boot", value=enable_secure_boot, expected_type=type_hints["enable_secure_boot"])
            check_type(argname="argument enable_vtpm", value=enable_vtpm, expected_type=type_hints["enable_vtpm"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_integrity_monitoring is not None:
            self._values["enable_integrity_monitoring"] = enable_integrity_monitoring
        if enable_secure_boot is not None:
            self._values["enable_secure_boot"] = enable_secure_boot
        if enable_vtpm is not None:
            self._values["enable_vtpm"] = enable_vtpm

    @builtins.property
    def enable_integrity_monitoring(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Defines whether the VM instance has integrity monitoring
        enabled. Enables monitoring and attestation of the boot integrity of the VM
        instance. The attestation is performed against the integrity policy baseline.
        This baseline is initially derived from the implicitly trusted boot image
        when the VM instance is created. Enabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#enable_integrity_monitoring GoogleWorkbenchInstance#enable_integrity_monitoring}
        '''
        result = self._values.get("enable_integrity_monitoring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_secure_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Defines whether the VM instance has Secure Boot enabled.
        Secure Boot helps ensure that the system only runs authentic software by verifying
        the digital signature of all boot components, and halting the boot process
        if signature verification fails. Disabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#enable_secure_boot GoogleWorkbenchInstance#enable_secure_boot}
        '''
        result = self._values.get("enable_secure_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_vtpm(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. Defines whether the VM instance has the vTPM enabled. Enabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#enable_vtpm GoogleWorkbenchInstance#enable_vtpm}
        '''
        result = self._values.get("enable_vtpm")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkbenchInstanceGceSetupShieldedInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkbenchInstanceGceSetupShieldedInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupShieldedInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c18d4822998debfdb787d8c92fdfd3b689f25e6af8b03f85328c5ba08297e810)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableIntegrityMonitoring")
    def reset_enable_integrity_monitoring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableIntegrityMonitoring", []))

    @jsii.member(jsii_name="resetEnableSecureBoot")
    def reset_enable_secure_boot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSecureBoot", []))

    @jsii.member(jsii_name="resetEnableVtpm")
    def reset_enable_vtpm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableVtpm", []))

    @builtins.property
    @jsii.member(jsii_name="enableIntegrityMonitoringInput")
    def enable_integrity_monitoring_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableIntegrityMonitoringInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSecureBootInput")
    def enable_secure_boot_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSecureBootInput"))

    @builtins.property
    @jsii.member(jsii_name="enableVtpmInput")
    def enable_vtpm_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableVtpmInput"))

    @builtins.property
    @jsii.member(jsii_name="enableIntegrityMonitoring")
    def enable_integrity_monitoring(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableIntegrityMonitoring"))

    @enable_integrity_monitoring.setter
    def enable_integrity_monitoring(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dccc04baf8be88fdeb1b7da502c9624f291322423ba402ebe76e4ce1d09ecfa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableIntegrityMonitoring", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableSecureBoot")
    def enable_secure_boot(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSecureBoot"))

    @enable_secure_boot.setter
    def enable_secure_boot(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7248fbadf2841ea45a064c386b1e9e588d850555ead7e7adc74d96d0f50fd998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSecureBoot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableVtpm")
    def enable_vtpm(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableVtpm"))

    @enable_vtpm.setter
    def enable_vtpm(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e933b5dddabd2d5ecaf7060cdfdd5a33a0f473898528214ab1a437552f2f229d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableVtpm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleWorkbenchInstanceGceSetupShieldedInstanceConfig]:
        return typing.cast(typing.Optional[GoogleWorkbenchInstanceGceSetupShieldedInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleWorkbenchInstanceGceSetupShieldedInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__291b75c04c4676a792143f9eb2e02085226019fd122e03d5c04a4352713ca483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupVmImage",
    jsii_struct_bases=[],
    name_mapping={"family": "family", "name": "name", "project": "project"},
)
class GoogleWorkbenchInstanceGceSetupVmImage:
    def __init__(
        self,
        *,
        family: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param family: Optional. Use this VM image family to find the image; the newest image in this family will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#family GoogleWorkbenchInstance#family}
        :param name: Optional. Use VM image name to find the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#name GoogleWorkbenchInstance#name}
        :param project: The name of the Google Cloud project that this VM image belongs to. Format: {project_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#project GoogleWorkbenchInstance#project}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fcba216d11582878fb284f6941c5a241070cf1276d14d071dc0a54802e365d7)
            check_type(argname="argument family", value=family, expected_type=type_hints["family"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if family is not None:
            self._values["family"] = family
        if name is not None:
            self._values["name"] = name
        if project is not None:
            self._values["project"] = project

    @builtins.property
    def family(self) -> typing.Optional[builtins.str]:
        '''Optional. Use this VM image family to find the image; the newest image in this family will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#family GoogleWorkbenchInstance#family}
        '''
        result = self._values.get("family")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Optional. Use VM image name to find the image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#name GoogleWorkbenchInstance#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The name of the Google Cloud project that this VM image belongs to. Format: {project_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#project GoogleWorkbenchInstance#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkbenchInstanceGceSetupVmImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkbenchInstanceGceSetupVmImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceGceSetupVmImageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd88bde688133b0c586595f2483c6b2c7a6adfc4de219245468aa275520d2ed1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFamily")
    def reset_family(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFamily", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @builtins.property
    @jsii.member(jsii_name="familyInput")
    def family_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "familyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="family")
    def family(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "family"))

    @family.setter
    def family(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2383e0cbb7b331bde24954f859738a0616f86b1ad8b5f24d4c8c9d09f159b35b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "family", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29a986df7dae5d95088f02c1c8c7b5e65d04d2f47fb437a6aa6d6d67706d59df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86fdaee7caa6bf0ecf01b2d46a3b74c6a937d6d00df97870f51ae745fd9560fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleWorkbenchInstanceGceSetupVmImage]:
        return typing.cast(typing.Optional[GoogleWorkbenchInstanceGceSetupVmImage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleWorkbenchInstanceGceSetupVmImage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__607c68464845e58d840d2878b11d146dca8a29d8f96774ecb78caa03047d9389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceHealthInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleWorkbenchInstanceHealthInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkbenchInstanceHealthInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkbenchInstanceHealthInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceHealthInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__203656ddb06c8d6a39a78ddd4b6a0dfbc67746fecde936bf2581eb360bc1ae40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleWorkbenchInstanceHealthInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7790b81977acc961f418d803578c16a7959de07d736a8a6bd17b6dbc334875da)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleWorkbenchInstanceHealthInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93de88f4ec5d5ead947647eda78977f24b7bfefd59e31486c98d779d8dae9737)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f85f7c779ec4c2e202de10859dedf4016d091ad78a321c614469b7ca7f4abbf6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47bbdd795a1848c0e9f981c1002a4c1f68a9aa9c377d3f29df88606ae8e03876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleWorkbenchInstanceHealthInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceHealthInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6063c3507befafc16ee5b89854324a53f46c6583dcd0c47c4f86a6c6cc1db3c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleWorkbenchInstanceHealthInfo]:
        return typing.cast(typing.Optional[GoogleWorkbenchInstanceHealthInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleWorkbenchInstanceHealthInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5db19def0fe68b6614ab836dc612432e24142868b7dfc534e56dfc3e546fc92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleWorkbenchInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#create GoogleWorkbenchInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#delete GoogleWorkbenchInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#update GoogleWorkbenchInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56747ba5e6a2904199aa9c0e55c8698136304de9c94c04cdf7708a48b555f5d3)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#create GoogleWorkbenchInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#delete GoogleWorkbenchInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workbench_instance#update GoogleWorkbenchInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkbenchInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkbenchInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a028e488e509e1d1fd941ed168b03b988b33a97764c60dbda15a481ae1fd1c90)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5f89ae3694d712773c62701eb42b98d9c34122f2b1c88448cfbff730af44c76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21970f17b6f926e6e4b86bd68792d5ffb5260935c79399ba6011d38037109905)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2735c0168a759d6b4f682ee664f00ef259f901e77fd90d4dd1be74878506f6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkbenchInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkbenchInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkbenchInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cab6f8f3917c7071e80306cc77d3aad94b00fe928fcfd7705dcc25079c4c82a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceUpgradeHistory",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleWorkbenchInstanceUpgradeHistory:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkbenchInstanceUpgradeHistory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkbenchInstanceUpgradeHistoryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceUpgradeHistoryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__301bad3629c6d8e77a1e7a292c71681093c49997935b0b53c6319e65058d8545)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleWorkbenchInstanceUpgradeHistoryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a93ec97854a08df24f3b43dbe1e40787421761a660c3e8933ab5d90d24264eb6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleWorkbenchInstanceUpgradeHistoryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b6ebacd3513d0af77c4b370fa057d6fa940f0ea7d41fc16c3f5c362bddbf35a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e71f5588aa2389655e7205e04f61817d6dbd5bf68fe985544453702bb15d6fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5016f69ef46fb2013afc2bcb9bd50b50721334ccbfe6e167ee0cf470cc0f5fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleWorkbenchInstanceUpgradeHistoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkbenchInstance.GoogleWorkbenchInstanceUpgradeHistoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52f1c014ab1798dfd3cc4823c4a2d1618cfe11c971278fc2e004e45636f0ab87)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="containerImage")
    def container_image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerImage"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="framework")
    def framework(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "framework"))

    @builtins.property
    @jsii.member(jsii_name="snapshot")
    def snapshot(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snapshot"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="targetVersion")
    def target_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetVersion"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="vmImage")
    def vm_image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmImage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleWorkbenchInstanceUpgradeHistory]:
        return typing.cast(typing.Optional[GoogleWorkbenchInstanceUpgradeHistory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleWorkbenchInstanceUpgradeHistory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9c6f55a5b7c907ac7d47148e9a9f9e482f50b0d9403910408214e9b338171c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleWorkbenchInstance",
    "GoogleWorkbenchInstanceConfig",
    "GoogleWorkbenchInstanceGceSetup",
    "GoogleWorkbenchInstanceGceSetupAcceleratorConfigs",
    "GoogleWorkbenchInstanceGceSetupAcceleratorConfigsList",
    "GoogleWorkbenchInstanceGceSetupAcceleratorConfigsOutputReference",
    "GoogleWorkbenchInstanceGceSetupBootDisk",
    "GoogleWorkbenchInstanceGceSetupBootDiskOutputReference",
    "GoogleWorkbenchInstanceGceSetupConfidentialInstanceConfig",
    "GoogleWorkbenchInstanceGceSetupConfidentialInstanceConfigOutputReference",
    "GoogleWorkbenchInstanceGceSetupContainerImage",
    "GoogleWorkbenchInstanceGceSetupContainerImageOutputReference",
    "GoogleWorkbenchInstanceGceSetupDataDisks",
    "GoogleWorkbenchInstanceGceSetupDataDisksOutputReference",
    "GoogleWorkbenchInstanceGceSetupNetworkInterfaces",
    "GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs",
    "GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigsList",
    "GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigsOutputReference",
    "GoogleWorkbenchInstanceGceSetupNetworkInterfacesList",
    "GoogleWorkbenchInstanceGceSetupNetworkInterfacesOutputReference",
    "GoogleWorkbenchInstanceGceSetupOutputReference",
    "GoogleWorkbenchInstanceGceSetupServiceAccounts",
    "GoogleWorkbenchInstanceGceSetupServiceAccountsList",
    "GoogleWorkbenchInstanceGceSetupServiceAccountsOutputReference",
    "GoogleWorkbenchInstanceGceSetupShieldedInstanceConfig",
    "GoogleWorkbenchInstanceGceSetupShieldedInstanceConfigOutputReference",
    "GoogleWorkbenchInstanceGceSetupVmImage",
    "GoogleWorkbenchInstanceGceSetupVmImageOutputReference",
    "GoogleWorkbenchInstanceHealthInfo",
    "GoogleWorkbenchInstanceHealthInfoList",
    "GoogleWorkbenchInstanceHealthInfoOutputReference",
    "GoogleWorkbenchInstanceTimeouts",
    "GoogleWorkbenchInstanceTimeoutsOutputReference",
    "GoogleWorkbenchInstanceUpgradeHistory",
    "GoogleWorkbenchInstanceUpgradeHistoryList",
    "GoogleWorkbenchInstanceUpgradeHistoryOutputReference",
]

publication.publish()

def _typecheckingstub__79e27cba1328d539db3272891440efb692427ca6579e16f34fb2679897e1605f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    desired_state: typing.Optional[builtins.str] = None,
    disable_proxy_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_third_party_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gce_setup: typing.Optional[typing.Union[GoogleWorkbenchInstanceGceSetup, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_id: typing.Optional[builtins.str] = None,
    instance_owners: typing.Optional[typing.Sequence[builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleWorkbenchInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c1ffbef6e3455e34e11be77462d05f72be2adb1ff4a2ad7a1ba7c60c47f2a9a7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff0a39c4ac90fb5c3a188010a95558f150a0d558f71f6ccfa6e27ec122720a58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53dee8f2bbd65fb34d9e54582463d942ae3b87072948d0af5a023194120f611(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be829248f0d26f3d3612d64ab33a4399d67585e633b96d65c9efbd32e6b4aab(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__558c30142d06ab2603c8b37ab2f0f29a55bb01e9bcfdd052b3cc95336780920d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9310838de99d5df5bf97c19e6a19ba70ff19b034853efc8697e5f18566f7b9df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2b8b0c7bc7e999ba798556eac2cab81a03820ff2f422f8124711ec8f4b51c4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d367780c13e1015e392c644913ca11ad56a0843e3d4f66518db8622f95fe10d4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5484f6c7f94979b767ce68a37dfee5f840b66e1fe6a4f06a019abbdc65961d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125e0a8d138ae15d27d8139cb38f2bd924a1103f0ac2ba3852b2e30b73716bf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__805d8bea81fede28b687fdd1ac1d0be83bd4107791117da9dc493d7145cefa69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4030cf79fb19100ae93bdf179373455be412fb43cff86c430c8ab8cfc05f5928(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    desired_state: typing.Optional[builtins.str] = None,
    disable_proxy_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_third_party_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gce_setup: typing.Optional[typing.Union[GoogleWorkbenchInstanceGceSetup, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_id: typing.Optional[builtins.str] = None,
    instance_owners: typing.Optional[typing.Sequence[builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleWorkbenchInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1accb2772934bcfcedf95f72a3248e4ba6d7a23b5c8dc225160c260d98f9088(
    *,
    accelerator_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkbenchInstanceGceSetupAcceleratorConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    boot_disk: typing.Optional[typing.Union[GoogleWorkbenchInstanceGceSetupBootDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    confidential_instance_config: typing.Optional[typing.Union[GoogleWorkbenchInstanceGceSetupConfidentialInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    container_image: typing.Optional[typing.Union[GoogleWorkbenchInstanceGceSetupContainerImage, typing.Dict[builtins.str, typing.Any]]] = None,
    data_disks: typing.Optional[typing.Union[GoogleWorkbenchInstanceGceSetupDataDisks, typing.Dict[builtins.str, typing.Any]]] = None,
    disable_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_ip_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    machine_type: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    network_interfaces: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkbenchInstanceGceSetupNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_accounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkbenchInstanceGceSetupServiceAccounts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    shielded_instance_config: typing.Optional[typing.Union[GoogleWorkbenchInstanceGceSetupShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    vm_image: typing.Optional[typing.Union[GoogleWorkbenchInstanceGceSetupVmImage, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__785ac42bb12283ef184ded10f5f5e4149ae6cb42f6ea6e0fdd77f75dace5ac12(
    *,
    core_count: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa92c4a4fe5c98657b8b6a4ec9b3bd155a437f58e08eb88ee0a2919036380781(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8623a5b62aea6bcb83f5d7a981670a8707215ceae0bd38b6199729132ec028dc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3296a6b6c51e15e8b8a82088763fc2c46f50dd4b0de80e3599489d7ddf317152(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b01e625ab0250e4d970c3d38d60691e85c12a7863f9b8db49da347f48d6b18(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__008cf437e26d4129b6ff7c715d116c3d07895ce0fab32253cb21766f287fcb9a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2523f7db67dfe41dc884a76129f243204404c31e20a811dbc82653551133188a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkbenchInstanceGceSetupAcceleratorConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a254f3ac8e1b0dc196ee69068fdc0eba1da869c9f5f565da2cc1ce54294206ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50905350d97e54150b3faf218797524b7f7da692b598bd1f7e3db8d64a47ea95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f89a6db06d8670e762d0d1e43db0e688cb53e5037b70364c03cfcb3cf4f4def5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__144ca4c5eb4da82e6ab243677d928b1e15c8a4df43dade89a7476220b41d3858(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkbenchInstanceGceSetupAcceleratorConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bb726a73ab5bc37e4b46e18e8b8cb837f3b0d93772d4f9d490cf6017c1afab0(
    *,
    disk_encryption: typing.Optional[builtins.str] = None,
    disk_size_gb: typing.Optional[builtins.str] = None,
    disk_type: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d172fd08e8f8434525cf12fec7a51b4bc7fdb911be99675c1581d2a97ad5ab1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49f3fb9d13099ca4f744475b6b01f774edc28e5dadb3f455c3e93313a13bf9aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65232d63bdc0a1790a9e323c3731f366cb1d1c4afd0ed02c36da9096ffb290f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5310038c52252ca8c9cadc7c50aa0cca65bc341dd0a4c275439ba49a9a8744cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__414faa05ea8a8719f54aaf6d41326fe318c980b14bfed34cd1f2ce7d33552590(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c23b0b6c2e086e7bb1c5e6009f12a321bb932485907d3f0d8287d98a593e083(
    value: typing.Optional[GoogleWorkbenchInstanceGceSetupBootDisk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3cec256939313e4c4bb3dc9d88df50a8d0eedb7926e434c101567e3c33f957(
    *,
    confidential_instance_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca565113f6bfcfb299234b75d613963d1fbc2835bf72639a2374bec1387e7924(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f20e995e599f572943c8041fe5827e74f6079ec05cd44930e5c667af63d1d95b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b290e9d94935e401b5b6e936dfb991b59ca91cabe4f8501152a9c31e949125aa(
    value: typing.Optional[GoogleWorkbenchInstanceGceSetupConfidentialInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ba12d30c6e173ef027fa5507ad93ee12779209ebf8410df3149849ed4b73e02(
    *,
    repository: builtins.str,
    tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300db7a7e32ef452205c27a54cdfa63941cad689fc1e9880fa10478b47d3ad51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f9e97482504ab11529924f121dc651818f343863a50e43151c355daba6637f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0710e05b9481f735271e401b1141397ee5972be0c78931ba8ae1c4fd2c2203bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__179f52f9925615a1c3155e5fa5f2a6b9ca59d06d64346093ff41c50658577841(
    value: typing.Optional[GoogleWorkbenchInstanceGceSetupContainerImage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a25a1ba2035e45b5c56b74d67595a9e30f56f5d5da0ab7b40f8fe71b7fc48298(
    *,
    disk_encryption: typing.Optional[builtins.str] = None,
    disk_size_gb: typing.Optional[builtins.str] = None,
    disk_type: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__993bf2eb332e8d38482521c71ad1bd7f60a2a99ab274099e9c0934ffe020e500(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69667b64fee0aaaf3806f4cc96a926070738c0fb396786ef84672c3ccdf7656(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880c53989793938354a7ef67adc744d728d93f398b4c4153527159364bc9c3fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19002d6585176543da9ec16f6f27bf2fae49eefc5a545174a420a88da914ed9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ced8bce1a006f515abb2661144fca99ad4f3c8a1c11ea9d48fbcea26a63008(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0aca2d180926114c2dbf35c89d79e11613feaf2b13b935bef08f5e2509eacd(
    value: typing.Optional[GoogleWorkbenchInstanceGceSetupDataDisks],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a75cd02a1564f1f6a51d387b54d7cfbbf3ed5b0fd5a3176fc153345415d19b(
    *,
    access_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network: typing.Optional[builtins.str] = None,
    nic_type: typing.Optional[builtins.str] = None,
    subnet: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c776f4d1e00259fe5c54c99a7a364dcc2374e3caaacdc37e2b9bd6fe66cf87d3(
    *,
    external_ip: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b676c600df134e3889c29d7d1bb137ec68de7bb2ca57363c342e9518232199d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb9050b09156a3ff6f394f74e4e6d004e6fd96d28dcfd87fd351904d444ffbc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38c677b140074a9549aebf6a7f59de4176aea0414d0e5da6dd1f1e0b01bc1b96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__798195d4c8a98c35e46a9606d8299b8c2cf6ad022491651dd564bdb454579f1e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f375931329ff6396966c6cbd4d4aa1cf62b0556dcf30e3c2d2c2337c86da37c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8880aea219b8b62ba651af33cb247c495d608f06dd8a4b212e77e9bb9398b618(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c7adedd334e17c0d047a9fb5ca02e7e71dd819ae8cdae8fa083183061263f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__684145c3dfc460531e8b36dbd7b810f4ffd7dc98e64515f9fbe65a5634638aa4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7510ed2160a5516de47bbfdf539fbc782732b029e554f49e9be9564fb1892432(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c0efc3b859a11750c160e050ac24a81e2a5703dbf3809cc8f72cce60d547c5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dbdf6f16376c6bff86caa66cf07c6203cb56c2ee60dcc4f3c14ebf5cc39d938(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92da5c5989ad4ebcff1b3b92b9bc32e3aac98c55e903efb82db192c5a2813c90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c527293921a2cd247a8d09ba7fb7955bb0b2dd217cb4748061b7d3e1897a7640(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__593d1822f1d9cc6f36fed096c473fd5cd1b8eb5fa6eee3108fff8b49396940be(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e90618709ad5c365021978a5eef38777a72e9592f157af43fa98f6c515f0288(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkbenchInstanceGceSetupNetworkInterfaces]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a59ffb434cd3fbbd3ce1725d54333f54e4bf1d7d0145899895f6ad81ff254cd1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25e29c7f0894d12c503d1b33c9f45cd9ed89cb8d0fa21a2658442211ee2e19d2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51b67a7975f2a755310d609206c63491cd0cb0aa89b9bc9356d7fd3f899d2384(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ff812108ace575a6e7e44e88d86f4754b535ef0f34ff84364d2b4757d827816(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce3a4b4c081d401da8c237bbfa450b1431360d598bfe0e1300cec57a22f4c5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46fc78952cdba79d33c472dc856d00b793a93a8487cb91726101b4305a25e4d2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkbenchInstanceGceSetupNetworkInterfaces]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fbc5d215d80f6f41fa24c8baeb277ffba3e627742ae51545c2daddd20a1c378(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f45f969de8fc7d2027efb133cd2b28121800bf7268c794422cd2b22efa59ace(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkbenchInstanceGceSetupAcceleratorConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af5a5a1b984db9b464641ba21f6e90d42a49252e8454688bfdd5ef824e7cff16(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkbenchInstanceGceSetupNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88755bdacfd6a23011f060052a7f5d51e2d34b9d55a4852fb6d12cb9dd12f67(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkbenchInstanceGceSetupServiceAccounts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a546692c565ec155085942e1f0a558255a58a63e54514f2b2a21b1bceb139a4b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3f4fcd48239291cd863724605cd86fe9d0f9623836c976130afca678b2a2686(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90b0eaba47871b0838bac0e5ba772a4ba72236765fd32cbf2ddc591c3576fb5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2a8b83b20c1b93e4c204c6ab7c226bcd9a3cfcb3bca688ef3b011f7e7c37f70(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997c08634d988d996a5513891fbd2052fc0987b239545d385d2307378268a237(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d10bc189c798e379eb01d2012c61c236cb384917c251d7eb648ac1491289c2(
    value: typing.Optional[GoogleWorkbenchInstanceGceSetup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ea30d841b6f6bb447b13855d305c3881fdcb49042983f66b5351e693739ba4(
    *,
    email: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fabe7294ac6a5a31814ef9a0cfdd544ab2dba66a9d9a84e10f21492a22d0c06e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83077a9a56fa7d8dad2e36d1e48c9fc76ecdb53913fa67fa394a9fd38d4ff066(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a77e4e6e1ff10dd2f2c28e19bc2cddf95625b4bebf0f57bab957196a07a2eed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e590eb39c6c79d177226464eda0eda77765a0b933e72a5217be84f420828e0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1317ae920ecc186f0969670cf21a567339324a9316bbae27a7c4f8b411360206(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6781c71b8c376b3a29027082c7756e9c3fc4a02c7a45e5a971afc964026f47c9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkbenchInstanceGceSetupServiceAccounts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff9d694e7da07b1cb5afd490578858cacc8d5a1208b5646ba6c7b5b764057b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797a69be5f604346a1bace38f42d959d3b57f2e05be443c09eab0479327d4ae1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd717fa22f8b4124ba317a44c9c3794ee2bbde1666b4433befd97661046af0bf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkbenchInstanceGceSetupServiceAccounts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6efd1022656f651f0bca9c44fbb902f25d5fb1c1e276079200c261510d2e940(
    *,
    enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c18d4822998debfdb787d8c92fdfd3b689f25e6af8b03f85328c5ba08297e810(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dccc04baf8be88fdeb1b7da502c9624f291322423ba402ebe76e4ce1d09ecfa2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7248fbadf2841ea45a064c386b1e9e588d850555ead7e7adc74d96d0f50fd998(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e933b5dddabd2d5ecaf7060cdfdd5a33a0f473898528214ab1a437552f2f229d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__291b75c04c4676a792143f9eb2e02085226019fd122e03d5c04a4352713ca483(
    value: typing.Optional[GoogleWorkbenchInstanceGceSetupShieldedInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fcba216d11582878fb284f6941c5a241070cf1276d14d071dc0a54802e365d7(
    *,
    family: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd88bde688133b0c586595f2483c6b2c7a6adfc4de219245468aa275520d2ed1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2383e0cbb7b331bde24954f859738a0616f86b1ad8b5f24d4c8c9d09f159b35b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29a986df7dae5d95088f02c1c8c7b5e65d04d2f47fb437a6aa6d6d67706d59df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86fdaee7caa6bf0ecf01b2d46a3b74c6a937d6d00df97870f51ae745fd9560fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607c68464845e58d840d2878b11d146dca8a29d8f96774ecb78caa03047d9389(
    value: typing.Optional[GoogleWorkbenchInstanceGceSetupVmImage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__203656ddb06c8d6a39a78ddd4b6a0dfbc67746fecde936bf2581eb360bc1ae40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7790b81977acc961f418d803578c16a7959de07d736a8a6bd17b6dbc334875da(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93de88f4ec5d5ead947647eda78977f24b7bfefd59e31486c98d779d8dae9737(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f85f7c779ec4c2e202de10859dedf4016d091ad78a321c614469b7ca7f4abbf6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47bbdd795a1848c0e9f981c1002a4c1f68a9aa9c377d3f29df88606ae8e03876(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6063c3507befafc16ee5b89854324a53f46c6583dcd0c47c4f86a6c6cc1db3c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5db19def0fe68b6614ab836dc612432e24142868b7dfc534e56dfc3e546fc92(
    value: typing.Optional[GoogleWorkbenchInstanceHealthInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56747ba5e6a2904199aa9c0e55c8698136304de9c94c04cdf7708a48b555f5d3(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a028e488e509e1d1fd941ed168b03b988b33a97764c60dbda15a481ae1fd1c90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f89ae3694d712773c62701eb42b98d9c34122f2b1c88448cfbff730af44c76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21970f17b6f926e6e4b86bd68792d5ffb5260935c79399ba6011d38037109905(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2735c0168a759d6b4f682ee664f00ef259f901e77fd90d4dd1be74878506f6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cab6f8f3917c7071e80306cc77d3aad94b00fe928fcfd7705dcc25079c4c82a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkbenchInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__301bad3629c6d8e77a1e7a292c71681093c49997935b0b53c6319e65058d8545(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a93ec97854a08df24f3b43dbe1e40787421761a660c3e8933ab5d90d24264eb6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b6ebacd3513d0af77c4b370fa057d6fa940f0ea7d41fc16c3f5c362bddbf35a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e71f5588aa2389655e7205e04f61817d6dbd5bf68fe985544453702bb15d6fa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5016f69ef46fb2013afc2bcb9bd50b50721334ccbfe6e167ee0cf470cc0f5fe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f1c014ab1798dfd3cc4823c4a2d1618cfe11c971278fc2e004e45636f0ab87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9c6f55a5b7c907ac7d47148e9a9f9e482f50b0d9403910408214e9b338171c3(
    value: typing.Optional[GoogleWorkbenchInstanceUpgradeHistory],
) -> None:
    """Type checking stubs"""
    pass
