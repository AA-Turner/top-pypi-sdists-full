r'''
# `google_workbench_instance`

Refer to the Terraform Registry for docs: [`google_workbench_instance`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance).
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


class WorkbenchInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance google_workbench_instance}.'''

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
        gce_setup: typing.Optional[typing.Union["WorkbenchInstanceGceSetup", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_id: typing.Optional[builtins.str] = None,
        instance_owners: typing.Optional[typing.Sequence[builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["WorkbenchInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance google_workbench_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Part of 'parent'. See documentation of 'projectsId'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#location WorkbenchInstance#location}
        :param name: The name of this workbench instance. Format: 'projects/{project_id}/locations/{location}/instances/{instance_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#name WorkbenchInstance#name}
        :param desired_state: Desired state of the Workbench Instance. Set this field to 'ACTIVE' to start the Instance, and 'STOPPED' to stop the Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#desired_state WorkbenchInstance#desired_state}
        :param disable_proxy_access: Optional. If true, the workbench instance will not register with the proxy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disable_proxy_access WorkbenchInstance#disable_proxy_access}
        :param enable_third_party_identity: Flag that specifies that a notebook can be accessed with third party identity provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#enable_third_party_identity WorkbenchInstance#enable_third_party_identity}
        :param gce_setup: gce_setup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#gce_setup WorkbenchInstance#gce_setup}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#id WorkbenchInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_id: Required. User-defined unique ID of this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#instance_id WorkbenchInstance#instance_id}
        :param instance_owners: 'Optional. Input only. The owner of this instance after creation. Format: 'alias@example.com' Currently supports one owner only. If not specified, all of the service account users of your VM instance''s service account can use the instance. If specified, sets the access mode to 'Single user'. For more details, see https://cloud.google.com/vertex-ai/docs/workbench/instances/manage-access-jupyterlab' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#instance_owners WorkbenchInstance#instance_owners}
        :param labels: Optional. Labels to apply to this instance. These can be later modified by the UpdateInstance method. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#labels WorkbenchInstance#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#project WorkbenchInstance#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#timeouts WorkbenchInstance#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10c94479665759d01351563c4e758a3208e02b8de6dfea620e4440b5e929e334)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = WorkbenchInstanceConfig(
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
        '''Generates CDKTF code for importing a WorkbenchInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WorkbenchInstance to import.
        :param import_from_id: The id of the existing WorkbenchInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WorkbenchInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6082fa889728480d194929d6506c776c5073d2fe278aeccf3d4a46d5f72441cf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putGceSetup")
    def put_gce_setup(
        self,
        *,
        accelerator_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkbenchInstanceGceSetupAcceleratorConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        boot_disk: typing.Optional[typing.Union["WorkbenchInstanceGceSetupBootDisk", typing.Dict[builtins.str, typing.Any]]] = None,
        confidential_instance_config: typing.Optional[typing.Union["WorkbenchInstanceGceSetupConfidentialInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        container_image: typing.Optional[typing.Union["WorkbenchInstanceGceSetupContainerImage", typing.Dict[builtins.str, typing.Any]]] = None,
        data_disks: typing.Optional[typing.Union["WorkbenchInstanceGceSetupDataDisks", typing.Dict[builtins.str, typing.Any]]] = None,
        disable_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_ip_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        machine_type: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network_interfaces: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkbenchInstanceGceSetupNetworkInterfaces", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_accounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkbenchInstanceGceSetupServiceAccounts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        shielded_instance_config: typing.Optional[typing.Union["WorkbenchInstanceGceSetupShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        vm_image: typing.Optional[typing.Union["WorkbenchInstanceGceSetupVmImage", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param accelerator_configs: accelerator_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#accelerator_configs WorkbenchInstance#accelerator_configs}
        :param boot_disk: boot_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#boot_disk WorkbenchInstance#boot_disk}
        :param confidential_instance_config: confidential_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#confidential_instance_config WorkbenchInstance#confidential_instance_config}
        :param container_image: container_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#container_image WorkbenchInstance#container_image}
        :param data_disks: data_disks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#data_disks WorkbenchInstance#data_disks}
        :param disable_public_ip: Optional. If true, no external IP will be assigned to this VM instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disable_public_ip WorkbenchInstance#disable_public_ip}
        :param enable_ip_forwarding: Optional. Flag to enable ip forwarding or not, default false/off. https://cloud.google.com/vpc/docs/using-routes#canipforward. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#enable_ip_forwarding WorkbenchInstance#enable_ip_forwarding}
        :param machine_type: Optional. The machine type of the VM instance. https://cloud.google.com/compute/docs/machine-resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#machine_type WorkbenchInstance#machine_type}
        :param metadata: Optional. Custom metadata to apply to this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#metadata WorkbenchInstance#metadata}
        :param network_interfaces: network_interfaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#network_interfaces WorkbenchInstance#network_interfaces}
        :param service_accounts: service_accounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#service_accounts WorkbenchInstance#service_accounts}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#shielded_instance_config WorkbenchInstance#shielded_instance_config}
        :param tags: Optional. The Compute Engine tags to add to instance (see `Tagging instances <https://cloud.google.com/compute/docs/label-or-tag-resources#tags>`_). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#tags WorkbenchInstance#tags}
        :param vm_image: vm_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#vm_image WorkbenchInstance#vm_image}
        '''
        value = WorkbenchInstanceGceSetup(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#create WorkbenchInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#delete WorkbenchInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#update WorkbenchInstance#update}.
        '''
        value = WorkbenchInstanceTimeouts(create=create, delete=delete, update=update)

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
    def gce_setup(self) -> "WorkbenchInstanceGceSetupOutputReference":
        return typing.cast("WorkbenchInstanceGceSetupOutputReference", jsii.get(self, "gceSetup"))

    @builtins.property
    @jsii.member(jsii_name="healthInfo")
    def health_info(self) -> "WorkbenchInstanceHealthInfoList":
        return typing.cast("WorkbenchInstanceHealthInfoList", jsii.get(self, "healthInfo"))

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
    def timeouts(self) -> "WorkbenchInstanceTimeoutsOutputReference":
        return typing.cast("WorkbenchInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="upgradeHistory")
    def upgrade_history(self) -> "WorkbenchInstanceUpgradeHistoryList":
        return typing.cast("WorkbenchInstanceUpgradeHistoryList", jsii.get(self, "upgradeHistory"))

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
    def gce_setup_input(self) -> typing.Optional["WorkbenchInstanceGceSetup"]:
        return typing.cast(typing.Optional["WorkbenchInstanceGceSetup"], jsii.get(self, "gceSetupInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WorkbenchInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WorkbenchInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredState")
    def desired_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "desiredState"))

    @desired_state.setter
    def desired_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__409beea1b3d54245e1f8bbfa7ab85c4c5ac82fe19692e2f6d021258d8f8d5737)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70c7faa95675ab34ecc85291147270595e009a68ef429d2cc6dc1200d50cfe98)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccf337e9683a0f5604e786d7cbd453565804def6726822b277cfb4a4ac99f5e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableThirdPartyIdentity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eab9b2f985674be82cc0ce8efa54e4bc7b88dbec11ab6f1ef513b4938ae8485c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bc0ff47222a2268d05cf27074b0ae9cc5aa130b201103cd7ae847a9e82d767b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceOwners")
    def instance_owners(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceOwners"))

    @instance_owners.setter
    def instance_owners(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04dc4110b4b3a0272dd7077113fa9c11aab6981a94c7e8ea1cbff7058d9ea2bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceOwners", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61e3f97a7dd63f10b8a7e627e98c6487c81fb885b63dddbd7091c4850e99c8bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__850cb5e28c9df7b68285f6d6ed6e6271f57aaba2a92c8b251c867955257310d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e88b542fe536c46260c390c7069b85d4d1cc0260272fc73f20f6c66c400a98c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__647f9043810f6468a0be0b58ab062f060322b784726af5c4fb540f9d83bd02d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceConfig",
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
class WorkbenchInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        gce_setup: typing.Optional[typing.Union["WorkbenchInstanceGceSetup", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_id: typing.Optional[builtins.str] = None,
        instance_owners: typing.Optional[typing.Sequence[builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["WorkbenchInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Part of 'parent'. See documentation of 'projectsId'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#location WorkbenchInstance#location}
        :param name: The name of this workbench instance. Format: 'projects/{project_id}/locations/{location}/instances/{instance_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#name WorkbenchInstance#name}
        :param desired_state: Desired state of the Workbench Instance. Set this field to 'ACTIVE' to start the Instance, and 'STOPPED' to stop the Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#desired_state WorkbenchInstance#desired_state}
        :param disable_proxy_access: Optional. If true, the workbench instance will not register with the proxy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disable_proxy_access WorkbenchInstance#disable_proxy_access}
        :param enable_third_party_identity: Flag that specifies that a notebook can be accessed with third party identity provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#enable_third_party_identity WorkbenchInstance#enable_third_party_identity}
        :param gce_setup: gce_setup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#gce_setup WorkbenchInstance#gce_setup}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#id WorkbenchInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_id: Required. User-defined unique ID of this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#instance_id WorkbenchInstance#instance_id}
        :param instance_owners: 'Optional. Input only. The owner of this instance after creation. Format: 'alias@example.com' Currently supports one owner only. If not specified, all of the service account users of your VM instance''s service account can use the instance. If specified, sets the access mode to 'Single user'. For more details, see https://cloud.google.com/vertex-ai/docs/workbench/instances/manage-access-jupyterlab' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#instance_owners WorkbenchInstance#instance_owners}
        :param labels: Optional. Labels to apply to this instance. These can be later modified by the UpdateInstance method. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#labels WorkbenchInstance#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#project WorkbenchInstance#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#timeouts WorkbenchInstance#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(gce_setup, dict):
            gce_setup = WorkbenchInstanceGceSetup(**gce_setup)
        if isinstance(timeouts, dict):
            timeouts = WorkbenchInstanceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f009fd960f2bbe7214c302490b0275807fef93911cc3c56dd0380547444ee9c1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#location WorkbenchInstance#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of this workbench instance. Format: 'projects/{project_id}/locations/{location}/instances/{instance_id}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#name WorkbenchInstance#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def desired_state(self) -> typing.Optional[builtins.str]:
        '''Desired state of the Workbench Instance.

        Set this field to 'ACTIVE' to start the Instance, and 'STOPPED' to stop the Instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#desired_state WorkbenchInstance#desired_state}
        '''
        result = self._values.get("desired_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_proxy_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. If true, the workbench instance will not register with the proxy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disable_proxy_access WorkbenchInstance#disable_proxy_access}
        '''
        result = self._values.get("disable_proxy_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_third_party_identity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag that specifies that a notebook can be accessed with third party identity provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#enable_third_party_identity WorkbenchInstance#enable_third_party_identity}
        '''
        result = self._values.get("enable_third_party_identity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gce_setup(self) -> typing.Optional["WorkbenchInstanceGceSetup"]:
        '''gce_setup block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#gce_setup WorkbenchInstance#gce_setup}
        '''
        result = self._values.get("gce_setup")
        return typing.cast(typing.Optional["WorkbenchInstanceGceSetup"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#id WorkbenchInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''Required. User-defined unique ID of this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#instance_id WorkbenchInstance#instance_id}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#instance_owners WorkbenchInstance#instance_owners}
        '''
        result = self._values.get("instance_owners")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. Labels to apply to this instance. These can be later modified by the UpdateInstance method.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#labels WorkbenchInstance#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#project WorkbenchInstance#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["WorkbenchInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#timeouts WorkbenchInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["WorkbenchInstanceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkbenchInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetup",
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
class WorkbenchInstanceGceSetup:
    def __init__(
        self,
        *,
        accelerator_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkbenchInstanceGceSetupAcceleratorConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        boot_disk: typing.Optional[typing.Union["WorkbenchInstanceGceSetupBootDisk", typing.Dict[builtins.str, typing.Any]]] = None,
        confidential_instance_config: typing.Optional[typing.Union["WorkbenchInstanceGceSetupConfidentialInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        container_image: typing.Optional[typing.Union["WorkbenchInstanceGceSetupContainerImage", typing.Dict[builtins.str, typing.Any]]] = None,
        data_disks: typing.Optional[typing.Union["WorkbenchInstanceGceSetupDataDisks", typing.Dict[builtins.str, typing.Any]]] = None,
        disable_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_ip_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        machine_type: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network_interfaces: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkbenchInstanceGceSetupNetworkInterfaces", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_accounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkbenchInstanceGceSetupServiceAccounts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        shielded_instance_config: typing.Optional[typing.Union["WorkbenchInstanceGceSetupShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        vm_image: typing.Optional[typing.Union["WorkbenchInstanceGceSetupVmImage", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param accelerator_configs: accelerator_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#accelerator_configs WorkbenchInstance#accelerator_configs}
        :param boot_disk: boot_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#boot_disk WorkbenchInstance#boot_disk}
        :param confidential_instance_config: confidential_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#confidential_instance_config WorkbenchInstance#confidential_instance_config}
        :param container_image: container_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#container_image WorkbenchInstance#container_image}
        :param data_disks: data_disks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#data_disks WorkbenchInstance#data_disks}
        :param disable_public_ip: Optional. If true, no external IP will be assigned to this VM instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disable_public_ip WorkbenchInstance#disable_public_ip}
        :param enable_ip_forwarding: Optional. Flag to enable ip forwarding or not, default false/off. https://cloud.google.com/vpc/docs/using-routes#canipforward. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#enable_ip_forwarding WorkbenchInstance#enable_ip_forwarding}
        :param machine_type: Optional. The machine type of the VM instance. https://cloud.google.com/compute/docs/machine-resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#machine_type WorkbenchInstance#machine_type}
        :param metadata: Optional. Custom metadata to apply to this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#metadata WorkbenchInstance#metadata}
        :param network_interfaces: network_interfaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#network_interfaces WorkbenchInstance#network_interfaces}
        :param service_accounts: service_accounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#service_accounts WorkbenchInstance#service_accounts}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#shielded_instance_config WorkbenchInstance#shielded_instance_config}
        :param tags: Optional. The Compute Engine tags to add to instance (see `Tagging instances <https://cloud.google.com/compute/docs/label-or-tag-resources#tags>`_). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#tags WorkbenchInstance#tags}
        :param vm_image: vm_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#vm_image WorkbenchInstance#vm_image}
        '''
        if isinstance(boot_disk, dict):
            boot_disk = WorkbenchInstanceGceSetupBootDisk(**boot_disk)
        if isinstance(confidential_instance_config, dict):
            confidential_instance_config = WorkbenchInstanceGceSetupConfidentialInstanceConfig(**confidential_instance_config)
        if isinstance(container_image, dict):
            container_image = WorkbenchInstanceGceSetupContainerImage(**container_image)
        if isinstance(data_disks, dict):
            data_disks = WorkbenchInstanceGceSetupDataDisks(**data_disks)
        if isinstance(shielded_instance_config, dict):
            shielded_instance_config = WorkbenchInstanceGceSetupShieldedInstanceConfig(**shielded_instance_config)
        if isinstance(vm_image, dict):
            vm_image = WorkbenchInstanceGceSetupVmImage(**vm_image)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c393af382860c38243ff8796ddbf63f69f0c49abf180c3ea5ef4b9214c6097d1)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkbenchInstanceGceSetupAcceleratorConfigs"]]]:
        '''accelerator_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#accelerator_configs WorkbenchInstance#accelerator_configs}
        '''
        result = self._values.get("accelerator_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkbenchInstanceGceSetupAcceleratorConfigs"]]], result)

    @builtins.property
    def boot_disk(self) -> typing.Optional["WorkbenchInstanceGceSetupBootDisk"]:
        '''boot_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#boot_disk WorkbenchInstance#boot_disk}
        '''
        result = self._values.get("boot_disk")
        return typing.cast(typing.Optional["WorkbenchInstanceGceSetupBootDisk"], result)

    @builtins.property
    def confidential_instance_config(
        self,
    ) -> typing.Optional["WorkbenchInstanceGceSetupConfidentialInstanceConfig"]:
        '''confidential_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#confidential_instance_config WorkbenchInstance#confidential_instance_config}
        '''
        result = self._values.get("confidential_instance_config")
        return typing.cast(typing.Optional["WorkbenchInstanceGceSetupConfidentialInstanceConfig"], result)

    @builtins.property
    def container_image(
        self,
    ) -> typing.Optional["WorkbenchInstanceGceSetupContainerImage"]:
        '''container_image block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#container_image WorkbenchInstance#container_image}
        '''
        result = self._values.get("container_image")
        return typing.cast(typing.Optional["WorkbenchInstanceGceSetupContainerImage"], result)

    @builtins.property
    def data_disks(self) -> typing.Optional["WorkbenchInstanceGceSetupDataDisks"]:
        '''data_disks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#data_disks WorkbenchInstance#data_disks}
        '''
        result = self._values.get("data_disks")
        return typing.cast(typing.Optional["WorkbenchInstanceGceSetupDataDisks"], result)

    @builtins.property
    def disable_public_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. If true, no external IP will be assigned to this VM instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disable_public_ip WorkbenchInstance#disable_public_ip}
        '''
        result = self._values.get("disable_public_ip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_ip_forwarding(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. Flag to enable ip forwarding or not, default false/off. https://cloud.google.com/vpc/docs/using-routes#canipforward.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#enable_ip_forwarding WorkbenchInstance#enable_ip_forwarding}
        '''
        result = self._values.get("enable_ip_forwarding")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''Optional. The machine type of the VM instance. https://cloud.google.com/compute/docs/machine-resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#machine_type WorkbenchInstance#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. Custom metadata to apply to this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#metadata WorkbenchInstance#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def network_interfaces(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkbenchInstanceGceSetupNetworkInterfaces"]]]:
        '''network_interfaces block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#network_interfaces WorkbenchInstance#network_interfaces}
        '''
        result = self._values.get("network_interfaces")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkbenchInstanceGceSetupNetworkInterfaces"]]], result)

    @builtins.property
    def service_accounts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkbenchInstanceGceSetupServiceAccounts"]]]:
        '''service_accounts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#service_accounts WorkbenchInstance#service_accounts}
        '''
        result = self._values.get("service_accounts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkbenchInstanceGceSetupServiceAccounts"]]], result)

    @builtins.property
    def shielded_instance_config(
        self,
    ) -> typing.Optional["WorkbenchInstanceGceSetupShieldedInstanceConfig"]:
        '''shielded_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#shielded_instance_config WorkbenchInstance#shielded_instance_config}
        '''
        result = self._values.get("shielded_instance_config")
        return typing.cast(typing.Optional["WorkbenchInstanceGceSetupShieldedInstanceConfig"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. The Compute Engine tags to add to instance (see `Tagging instances <https://cloud.google.com/compute/docs/label-or-tag-resources#tags>`_).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#tags WorkbenchInstance#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vm_image(self) -> typing.Optional["WorkbenchInstanceGceSetupVmImage"]:
        '''vm_image block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#vm_image WorkbenchInstance#vm_image}
        '''
        result = self._values.get("vm_image")
        return typing.cast(typing.Optional["WorkbenchInstanceGceSetupVmImage"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkbenchInstanceGceSetup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupAcceleratorConfigs",
    jsii_struct_bases=[],
    name_mapping={"core_count": "coreCount", "type": "type"},
)
class WorkbenchInstanceGceSetupAcceleratorConfigs:
    def __init__(
        self,
        *,
        core_count: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param core_count: Optional. Count of cores of this accelerator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#core_count WorkbenchInstance#core_count}
        :param type: Optional. Type of this accelerator. Possible values: ["NVIDIA_TESLA_P100", "NVIDIA_TESLA_V100", "NVIDIA_TESLA_P4", "NVIDIA_TESLA_T4", "NVIDIA_TESLA_A100", "NVIDIA_A100_80GB", "NVIDIA_L4", "NVIDIA_TESLA_T4_VWS", "NVIDIA_TESLA_P100_VWS", "NVIDIA_TESLA_P4_VWS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#type WorkbenchInstance#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2bef2ddfc5ff419973f84a663fcaa28729604120a470e1548a4a7f4b9ba84d7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#core_count WorkbenchInstance#core_count}
        '''
        result = self._values.get("core_count")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Optional. Type of this accelerator. Possible values: ["NVIDIA_TESLA_P100", "NVIDIA_TESLA_V100", "NVIDIA_TESLA_P4", "NVIDIA_TESLA_T4", "NVIDIA_TESLA_A100", "NVIDIA_A100_80GB", "NVIDIA_L4", "NVIDIA_TESLA_T4_VWS", "NVIDIA_TESLA_P100_VWS", "NVIDIA_TESLA_P4_VWS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#type WorkbenchInstance#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkbenchInstanceGceSetupAcceleratorConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkbenchInstanceGceSetupAcceleratorConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupAcceleratorConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48ad3213803496f32907d53482996b1936038b0e4f0c7c6e168c7a16f1716139)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkbenchInstanceGceSetupAcceleratorConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49c15166bd7eacc1ed09e4c612552c6f3cd29c4d896be5ca3225ddb4bd1a68bf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkbenchInstanceGceSetupAcceleratorConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75bbc134b1f43c39fbd6a4ae37147e2921961e667897fe178d217d08dcc3de70)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb65425a6a2f4800177fb9cde9207201b56ce4a8da4bed57e5d14a23630b073a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cd30c28fa0259c8f2d0bc45b42598611f82050b385ba8ccb0855933766fae2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkbenchInstanceGceSetupAcceleratorConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkbenchInstanceGceSetupAcceleratorConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkbenchInstanceGceSetupAcceleratorConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__412258ed1f93dc0e28c8c4f7849d62511eb3aaad3588eefbcaa036f1d03090b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkbenchInstanceGceSetupAcceleratorConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupAcceleratorConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9393f2817a1f792043cd4a2a15778d1c56d2426c29a0e71b06c89138d4481111)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50077e2871cd24f672659d68f390e741e71516044862a2be9feab6bddd398e14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coreCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__effed3658769fcce86035a064d678d54df22ab12e4a52b8b65d686d29a4be0f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkbenchInstanceGceSetupAcceleratorConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkbenchInstanceGceSetupAcceleratorConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkbenchInstanceGceSetupAcceleratorConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__413f3b359df4a7d3de22b77a476e5c1fad66dd1e422cb26f7d72bcd6b1085a6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupBootDisk",
    jsii_struct_bases=[],
    name_mapping={
        "disk_encryption": "diskEncryption",
        "disk_size_gb": "diskSizeGb",
        "disk_type": "diskType",
        "kms_key": "kmsKey",
    },
)
class WorkbenchInstanceGceSetupBootDisk:
    def __init__(
        self,
        *,
        disk_encryption: typing.Optional[builtins.str] = None,
        disk_size_gb: typing.Optional[builtins.str] = None,
        disk_type: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_encryption: Optional. Input only. Disk encryption method used on the boot and data disks, defaults to GMEK. Possible values: ["GMEK", "CMEK"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disk_encryption WorkbenchInstance#disk_encryption}
        :param disk_size_gb: Optional. The size of the boot disk in GB attached to this instance, up to a maximum of 64000 GB (64 TB). If not specified, this defaults to the recommended value of 150GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disk_size_gb WorkbenchInstance#disk_size_gb}
        :param disk_type: Optional. Indicates the type of the disk. Possible values: ["PD_STANDARD", "PD_SSD", "PD_BALANCED", "PD_EXTREME"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disk_type WorkbenchInstance#disk_type}
        :param kms_key: 'Optional. The KMS key used to encrypt the disks, only applicable if disk_encryption is CMEK. Format: 'projects/{project_id}/locations/{location}/keyRings/{key_ring_id}/cryptoKeys/{key_id}' Learn more about using your own encryption keys.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#kms_key WorkbenchInstance#kms_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3ad0edb74c3c9270a0372d133a9832fecd6cfb090a090021481a135054551f5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disk_encryption WorkbenchInstance#disk_encryption}
        '''
        result = self._values.get("disk_encryption")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_size_gb(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The size of the boot disk in GB attached to this instance,
        up to a maximum of 64000 GB (64 TB). If not specified, this defaults to the
        recommended value of 150GB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disk_size_gb WorkbenchInstance#disk_size_gb}
        '''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_type(self) -> typing.Optional[builtins.str]:
        '''Optional. Indicates the type of the disk. Possible values: ["PD_STANDARD", "PD_SSD", "PD_BALANCED", "PD_EXTREME"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disk_type WorkbenchInstance#disk_type}
        '''
        result = self._values.get("disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        ''''Optional.

        The KMS key used to encrypt the disks, only
        applicable if disk_encryption is CMEK. Format: 'projects/{project_id}/locations/{location}/keyRings/{key_ring_id}/cryptoKeys/{key_id}'
        Learn more about using your own encryption keys.'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#kms_key WorkbenchInstance#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkbenchInstanceGceSetupBootDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkbenchInstanceGceSetupBootDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupBootDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d62e34120274eb0aec49d421cf79860db9e414cd7faaadfc48e7b4d8a27adee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbf182a3056f333eb1cb806b9834f446fd9b497bf61d26823cb70045ac7ae1d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91c9110f7c8a9bb7af94d5a02c0d3f50fe9a2440837fa9140bcfe3b07457c48f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskType")
    def disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskType"))

    @disk_type.setter
    def disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__142951b270c478ce9022b98edd4eec14453e8a5fd5ab3fb5d190a7636c6298a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9852926ba231bcf75fd3692fe96381611960077cb40e0a2eaa11b42d4bd810b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WorkbenchInstanceGceSetupBootDisk]:
        return typing.cast(typing.Optional[WorkbenchInstanceGceSetupBootDisk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkbenchInstanceGceSetupBootDisk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__044e24f428aca9a7164464682210659c78b15741526cb9c38c52016145d252bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupConfidentialInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={"confidential_instance_type": "confidentialInstanceType"},
)
class WorkbenchInstanceGceSetupConfidentialInstanceConfig:
    def __init__(
        self,
        *,
        confidential_instance_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param confidential_instance_type: Defines the type of technology used by the confidential instance. Possible values: ["SEV"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#confidential_instance_type WorkbenchInstance#confidential_instance_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325bdc5a723f4ce20a4b68abc0e7ac1f6855640a8d01d95fbd7bd88aa35bf902)
            check_type(argname="argument confidential_instance_type", value=confidential_instance_type, expected_type=type_hints["confidential_instance_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if confidential_instance_type is not None:
            self._values["confidential_instance_type"] = confidential_instance_type

    @builtins.property
    def confidential_instance_type(self) -> typing.Optional[builtins.str]:
        '''Defines the type of technology used by the confidential instance. Possible values: ["SEV"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#confidential_instance_type WorkbenchInstance#confidential_instance_type}
        '''
        result = self._values.get("confidential_instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkbenchInstanceGceSetupConfidentialInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkbenchInstanceGceSetupConfidentialInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupConfidentialInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d451d282cd44f38b0d16ad2bbabfc3891dda07c1ec69f152fed4cfa0d5aed21)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0c06bae028a45f862ef5e70e0cce3bfaf88fc4b8aa117500cfeee8a90063457)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidentialInstanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkbenchInstanceGceSetupConfidentialInstanceConfig]:
        return typing.cast(typing.Optional[WorkbenchInstanceGceSetupConfidentialInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkbenchInstanceGceSetupConfidentialInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef6b44b708249817591a6c8afdea74d8596655049ce94c8d9f88e37cce0c8c99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupContainerImage",
    jsii_struct_bases=[],
    name_mapping={"repository": "repository", "tag": "tag"},
)
class WorkbenchInstanceGceSetupContainerImage:
    def __init__(
        self,
        *,
        repository: builtins.str,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repository: The path to the container image repository. For example: gcr.io/{project_id}/{imageName}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#repository WorkbenchInstance#repository}
        :param tag: The tag of the container image. If not specified, this defaults to the latest tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#tag WorkbenchInstance#tag}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f48cff80679ab1f9cd7e3ee77f4d59fbdd48f0795dceadc3fbf9a9ebf244647f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#repository WorkbenchInstance#repository}
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''The tag of the container image. If not specified, this defaults to the latest tag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#tag WorkbenchInstance#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkbenchInstanceGceSetupContainerImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkbenchInstanceGceSetupContainerImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupContainerImageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__adcd4bbc5e151e15861c0da6b120648c33ebfc4ccaadecb0eec1ab4f979a8885)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53b7beb631db8e9246be44af9766f8202fe41cbc35537a6acdde1417e429f1aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f10586c58c451b75c2f0e818ba9f55ff21e2a5f31403ca0ef4c2778a3176ada5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkbenchInstanceGceSetupContainerImage]:
        return typing.cast(typing.Optional[WorkbenchInstanceGceSetupContainerImage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkbenchInstanceGceSetupContainerImage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e8e348205ef9dd646253a7705d8bb4d9d1e5c7cd9bd4d143dbd4feeaa8f5242)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupDataDisks",
    jsii_struct_bases=[],
    name_mapping={
        "disk_encryption": "diskEncryption",
        "disk_size_gb": "diskSizeGb",
        "disk_type": "diskType",
        "kms_key": "kmsKey",
    },
)
class WorkbenchInstanceGceSetupDataDisks:
    def __init__(
        self,
        *,
        disk_encryption: typing.Optional[builtins.str] = None,
        disk_size_gb: typing.Optional[builtins.str] = None,
        disk_type: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_encryption: Optional. Input only. Disk encryption method used on the boot and data disks, defaults to GMEK. Possible values: ["GMEK", "CMEK"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disk_encryption WorkbenchInstance#disk_encryption}
        :param disk_size_gb: Optional. The size of the disk in GB attached to this VM instance, up to a maximum of 64000 GB (64 TB). If not specified, this defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disk_size_gb WorkbenchInstance#disk_size_gb}
        :param disk_type: Optional. Input only. Indicates the type of the disk. Possible values: ["PD_STANDARD", "PD_SSD", "PD_BALANCED", "PD_EXTREME"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disk_type WorkbenchInstance#disk_type}
        :param kms_key: 'Optional. The KMS key used to encrypt the disks, only applicable if disk_encryption is CMEK. Format: 'projects/{project_id}/locations/{location}/keyRings/{key_ring_id}/cryptoKeys/{key_id}' Learn more about using your own encryption keys.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#kms_key WorkbenchInstance#kms_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e745778ec4eb76c3d0c67312472e5a022e70f981a50feb14e108a58df5220d7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disk_encryption WorkbenchInstance#disk_encryption}
        '''
        result = self._values.get("disk_encryption")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_size_gb(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The size of the disk in GB attached to this VM instance,
        up to a maximum of 64000 GB (64 TB). If not specified, this defaults to
        100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disk_size_gb WorkbenchInstance#disk_size_gb}
        '''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_type(self) -> typing.Optional[builtins.str]:
        '''Optional. Input only. Indicates the type of the disk. Possible values: ["PD_STANDARD", "PD_SSD", "PD_BALANCED", "PD_EXTREME"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disk_type WorkbenchInstance#disk_type}
        '''
        result = self._values.get("disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        ''''Optional.

        The KMS key used to encrypt the disks,
        only applicable if disk_encryption is CMEK. Format: 'projects/{project_id}/locations/{location}/keyRings/{key_ring_id}/cryptoKeys/{key_id}'
        Learn more about using your own encryption keys.'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#kms_key WorkbenchInstance#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkbenchInstanceGceSetupDataDisks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkbenchInstanceGceSetupDataDisksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupDataDisksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4559dbbf1aed1e76a5ea1e58e8868d88898ae80715770cdb22c6d83cf2cce992)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26c43810ee7106a4dce700f33312724ee137710755ca0f6025ecbf54fbfdd803)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99c27849b6fd625713f253b3aa2dfcd4013c13b4784851860135c31ff30fe440)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskType")
    def disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskType"))

    @disk_type.setter
    def disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac5876f9e7aaf84c353c82cfcf1f63328b4d3ffea1dedecce7887a7e399ed4a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f1b938d27e99fe509496eaccb1964a77021dc19d71b3ffec60939864e557115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WorkbenchInstanceGceSetupDataDisks]:
        return typing.cast(typing.Optional[WorkbenchInstanceGceSetupDataDisks], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkbenchInstanceGceSetupDataDisks],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faede199139410b1596a44e5d1e05caaff440a8898f3d0ea75f37f4c02f6aaa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupNetworkInterfaces",
    jsii_struct_bases=[],
    name_mapping={
        "access_configs": "accessConfigs",
        "network": "network",
        "nic_type": "nicType",
        "subnet": "subnet",
    },
)
class WorkbenchInstanceGceSetupNetworkInterfaces:
    def __init__(
        self,
        *,
        access_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network: typing.Optional[builtins.str] = None,
        nic_type: typing.Optional[builtins.str] = None,
        subnet: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_configs: access_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#access_configs WorkbenchInstance#access_configs}
        :param network: Optional. The name of the VPC that this VM instance is in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#network WorkbenchInstance#network}
        :param nic_type: Optional. The type of vNIC to be used on this interface. This may be gVNIC or VirtioNet. Possible values: ["VIRTIO_NET", "GVNIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#nic_type WorkbenchInstance#nic_type}
        :param subnet: Optional. The name of the subnet that this VM instance is in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#subnet WorkbenchInstance#subnet}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15cc9c707ab709643298c24566b24fb7c597362015adc9bdfa96979973e73413)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs"]]]:
        '''access_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#access_configs WorkbenchInstance#access_configs}
        '''
        result = self._values.get("access_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs"]]], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''Optional. The name of the VPC that this VM instance is in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#network WorkbenchInstance#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nic_type(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The type of vNIC to be used on this interface. This
        may be gVNIC or VirtioNet. Possible values: ["VIRTIO_NET", "GVNIC"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#nic_type WorkbenchInstance#nic_type}
        '''
        result = self._values.get("nic_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet(self) -> typing.Optional[builtins.str]:
        '''Optional. The name of the subnet that this VM instance is in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#subnet WorkbenchInstance#subnet}
        '''
        result = self._values.get("subnet")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkbenchInstanceGceSetupNetworkInterfaces(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs",
    jsii_struct_bases=[],
    name_mapping={"external_ip": "externalIp"},
)
class WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs:
    def __init__(self, *, external_ip: builtins.str) -> None:
        '''
        :param external_ip: An external IP address associated with this instance. Specify an unused static external IP address available to the project or leave this field undefined to use an IP from a shared ephemeral IP address pool. If you specify a static external IP address, it must live in the same region as the zone of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#external_ip WorkbenchInstance#external_ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4403a1379a5a46bad7f028fbeb662d54f206b39117be2250e748e2a32bdc22f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#external_ip WorkbenchInstance#external_ip}
        '''
        result = self._values.get("external_ip")
        assert result is not None, "Required property 'external_ip' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__afe7f9b256e98f4a40307aec9fbc6ce7377a855a9692171c5ea418fa457e9fe9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8de7d076bc1e5c4c65892984fa08b8d7c26cac9263afa7c170fe700937703f40)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f62a17b84eaa3538c1794a0cd0990179e806854294a4c258bdbdf36c43813a9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec32112dec4359dafb4338de2724c62b735ad1aee5032b4d3ece4aacc22a6d30)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6e6e7dfaeb7e0b99de1600dfbbd21ebbf60484cad84ccfdba9246f900bf992f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__349dc99dc12fb4b6fa72356857f5eb056e9b6254a9beed414af01f7e45738a57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a1fac7fc53d30248481f697ffaddfbf8d3f27d5bf728c2032d75eb592fcfbf2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f56d2d3d5ca8189b7838c71126e7eb559b6f8e93f6fc924d897ebe522998b33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5738db3abadb2a09975e0bf23b0bc8903240d0922bcfb932cb3b596677a5799e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkbenchInstanceGceSetupNetworkInterfacesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupNetworkInterfacesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__157bbbd4d77b304a9731a03df2618df7066fdd1f4ef79e5494129956c6c8d3d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkbenchInstanceGceSetupNetworkInterfacesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e59f984a8495d02c4a9db6b2779c4fbb1e9af56f3dc10cde3b829fd0c8998cd6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkbenchInstanceGceSetupNetworkInterfacesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0654d7907e2d8a41749bed51135946464c5633a00b60ad17551bfcf9b7b8c77d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d93c3b613ee026abb507bf534f6c526b56ad4d4d4abec82b95c631cf13e5cf60)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bee2f0840b731f628cd86e22b08769c58ccf3c515b5a522cf0bdcbc21483dade)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkbenchInstanceGceSetupNetworkInterfaces]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkbenchInstanceGceSetupNetworkInterfaces]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkbenchInstanceGceSetupNetworkInterfaces]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aa989f9b58b123182545b1c4c4c639096d76361e280571a49cb390615d17303)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkbenchInstanceGceSetupNetworkInterfacesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupNetworkInterfacesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0fc8e957b2eda93faaf167263bf0505adda896684e5623c627776363c7edcd4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAccessConfigs")
    def put_access_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26b344a82b56b12c56b5253e58004b40d3cd855ee8c8e8ba5e42b5ff4a7b4629)
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
    ) -> WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigsList:
        return typing.cast(WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigsList, jsii.get(self, "accessConfigs"))

    @builtins.property
    @jsii.member(jsii_name="accessConfigsInput")
    def access_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs]]], jsii.get(self, "accessConfigsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2909ca44168c7a14818743b50a0e4c6970aea8d4ed90b6cfd9646868b5b212c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nicType")
    def nic_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nicType"))

    @nic_type.setter
    def nic_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bab40ff2b882a56a38ed1ba341b8db9d5f2c1c05cbe3584264fbf9a42322a9d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nicType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnet")
    def subnet(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnet"))

    @subnet.setter
    def subnet(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a1767d1d962047faf950cbe03b30dc3bcb5254c2a54e24d3bf152610eff500)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkbenchInstanceGceSetupNetworkInterfaces]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkbenchInstanceGceSetupNetworkInterfaces]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkbenchInstanceGceSetupNetworkInterfaces]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a0728592bbb6a980a639789c913fc2ccae26b1f5509773905ff83704959ba00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkbenchInstanceGceSetupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a57640e0422d89cab16b9c28b9cd9f9c01e1c79135196003192a7731764be369)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAcceleratorConfigs")
    def put_accelerator_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkbenchInstanceGceSetupAcceleratorConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ac682077523b6386192faf6a426e34033ad06c78fc8a907b561c3354a5e2430)
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
        :param disk_encryption: Optional. Input only. Disk encryption method used on the boot and data disks, defaults to GMEK. Possible values: ["GMEK", "CMEK"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disk_encryption WorkbenchInstance#disk_encryption}
        :param disk_size_gb: Optional. The size of the boot disk in GB attached to this instance, up to a maximum of 64000 GB (64 TB). If not specified, this defaults to the recommended value of 150GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disk_size_gb WorkbenchInstance#disk_size_gb}
        :param disk_type: Optional. Indicates the type of the disk. Possible values: ["PD_STANDARD", "PD_SSD", "PD_BALANCED", "PD_EXTREME"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disk_type WorkbenchInstance#disk_type}
        :param kms_key: 'Optional. The KMS key used to encrypt the disks, only applicable if disk_encryption is CMEK. Format: 'projects/{project_id}/locations/{location}/keyRings/{key_ring_id}/cryptoKeys/{key_id}' Learn more about using your own encryption keys.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#kms_key WorkbenchInstance#kms_key}
        '''
        value = WorkbenchInstanceGceSetupBootDisk(
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
        :param confidential_instance_type: Defines the type of technology used by the confidential instance. Possible values: ["SEV"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#confidential_instance_type WorkbenchInstance#confidential_instance_type}
        '''
        value = WorkbenchInstanceGceSetupConfidentialInstanceConfig(
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
        :param repository: The path to the container image repository. For example: gcr.io/{project_id}/{imageName}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#repository WorkbenchInstance#repository}
        :param tag: The tag of the container image. If not specified, this defaults to the latest tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#tag WorkbenchInstance#tag}
        '''
        value = WorkbenchInstanceGceSetupContainerImage(repository=repository, tag=tag)

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
        :param disk_encryption: Optional. Input only. Disk encryption method used on the boot and data disks, defaults to GMEK. Possible values: ["GMEK", "CMEK"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disk_encryption WorkbenchInstance#disk_encryption}
        :param disk_size_gb: Optional. The size of the disk in GB attached to this VM instance, up to a maximum of 64000 GB (64 TB). If not specified, this defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disk_size_gb WorkbenchInstance#disk_size_gb}
        :param disk_type: Optional. Input only. Indicates the type of the disk. Possible values: ["PD_STANDARD", "PD_SSD", "PD_BALANCED", "PD_EXTREME"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#disk_type WorkbenchInstance#disk_type}
        :param kms_key: 'Optional. The KMS key used to encrypt the disks, only applicable if disk_encryption is CMEK. Format: 'projects/{project_id}/locations/{location}/keyRings/{key_ring_id}/cryptoKeys/{key_id}' Learn more about using your own encryption keys.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#kms_key WorkbenchInstance#kms_key}
        '''
        value = WorkbenchInstanceGceSetupDataDisks(
            disk_encryption=disk_encryption,
            disk_size_gb=disk_size_gb,
            disk_type=disk_type,
            kms_key=kms_key,
        )

        return typing.cast(None, jsii.invoke(self, "putDataDisks", [value]))

    @jsii.member(jsii_name="putNetworkInterfaces")
    def put_network_interfaces(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkbenchInstanceGceSetupNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a976ccb27037532017cd64acb76349b86846fc219af3d5774080dcc727eb836)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworkInterfaces", [value]))

    @jsii.member(jsii_name="putServiceAccounts")
    def put_service_accounts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkbenchInstanceGceSetupServiceAccounts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41fc26bf0d0ba5d7c1d34564d7328d5af5fe7b732410ebc5c8af43f7aacd4656)
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
        :param enable_integrity_monitoring: Optional. Defines whether the VM instance has integrity monitoring enabled. Enables monitoring and attestation of the boot integrity of the VM instance. The attestation is performed against the integrity policy baseline. This baseline is initially derived from the implicitly trusted boot image when the VM instance is created. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#enable_integrity_monitoring WorkbenchInstance#enable_integrity_monitoring}
        :param enable_secure_boot: Optional. Defines whether the VM instance has Secure Boot enabled. Secure Boot helps ensure that the system only runs authentic software by verifying the digital signature of all boot components, and halting the boot process if signature verification fails. Disabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#enable_secure_boot WorkbenchInstance#enable_secure_boot}
        :param enable_vtpm: Optional. Defines whether the VM instance has the vTPM enabled. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#enable_vtpm WorkbenchInstance#enable_vtpm}
        '''
        value = WorkbenchInstanceGceSetupShieldedInstanceConfig(
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
        :param family: Optional. Use this VM image family to find the image; the newest image in this family will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#family WorkbenchInstance#family}
        :param name: Optional. Use VM image name to find the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#name WorkbenchInstance#name}
        :param project: The name of the Google Cloud project that this VM image belongs to. Format: {project_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#project WorkbenchInstance#project}
        '''
        value = WorkbenchInstanceGceSetupVmImage(
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
    def accelerator_configs(self) -> WorkbenchInstanceGceSetupAcceleratorConfigsList:
        return typing.cast(WorkbenchInstanceGceSetupAcceleratorConfigsList, jsii.get(self, "acceleratorConfigs"))

    @builtins.property
    @jsii.member(jsii_name="bootDisk")
    def boot_disk(self) -> WorkbenchInstanceGceSetupBootDiskOutputReference:
        return typing.cast(WorkbenchInstanceGceSetupBootDiskOutputReference, jsii.get(self, "bootDisk"))

    @builtins.property
    @jsii.member(jsii_name="confidentialInstanceConfig")
    def confidential_instance_config(
        self,
    ) -> WorkbenchInstanceGceSetupConfidentialInstanceConfigOutputReference:
        return typing.cast(WorkbenchInstanceGceSetupConfidentialInstanceConfigOutputReference, jsii.get(self, "confidentialInstanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="containerImage")
    def container_image(self) -> WorkbenchInstanceGceSetupContainerImageOutputReference:
        return typing.cast(WorkbenchInstanceGceSetupContainerImageOutputReference, jsii.get(self, "containerImage"))

    @builtins.property
    @jsii.member(jsii_name="dataDisks")
    def data_disks(self) -> WorkbenchInstanceGceSetupDataDisksOutputReference:
        return typing.cast(WorkbenchInstanceGceSetupDataDisksOutputReference, jsii.get(self, "dataDisks"))

    @builtins.property
    @jsii.member(jsii_name="networkInterfaces")
    def network_interfaces(self) -> WorkbenchInstanceGceSetupNetworkInterfacesList:
        return typing.cast(WorkbenchInstanceGceSetupNetworkInterfacesList, jsii.get(self, "networkInterfaces"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccounts")
    def service_accounts(self) -> "WorkbenchInstanceGceSetupServiceAccountsList":
        return typing.cast("WorkbenchInstanceGceSetupServiceAccountsList", jsii.get(self, "serviceAccounts"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfig")
    def shielded_instance_config(
        self,
    ) -> "WorkbenchInstanceGceSetupShieldedInstanceConfigOutputReference":
        return typing.cast("WorkbenchInstanceGceSetupShieldedInstanceConfigOutputReference", jsii.get(self, "shieldedInstanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="vmImage")
    def vm_image(self) -> "WorkbenchInstanceGceSetupVmImageOutputReference":
        return typing.cast("WorkbenchInstanceGceSetupVmImageOutputReference", jsii.get(self, "vmImage"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorConfigsInput")
    def accelerator_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkbenchInstanceGceSetupAcceleratorConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkbenchInstanceGceSetupAcceleratorConfigs]]], jsii.get(self, "acceleratorConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskInput")
    def boot_disk_input(self) -> typing.Optional[WorkbenchInstanceGceSetupBootDisk]:
        return typing.cast(typing.Optional[WorkbenchInstanceGceSetupBootDisk], jsii.get(self, "bootDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="confidentialInstanceConfigInput")
    def confidential_instance_config_input(
        self,
    ) -> typing.Optional[WorkbenchInstanceGceSetupConfidentialInstanceConfig]:
        return typing.cast(typing.Optional[WorkbenchInstanceGceSetupConfidentialInstanceConfig], jsii.get(self, "confidentialInstanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="containerImageInput")
    def container_image_input(
        self,
    ) -> typing.Optional[WorkbenchInstanceGceSetupContainerImage]:
        return typing.cast(typing.Optional[WorkbenchInstanceGceSetupContainerImage], jsii.get(self, "containerImageInput"))

    @builtins.property
    @jsii.member(jsii_name="dataDisksInput")
    def data_disks_input(self) -> typing.Optional[WorkbenchInstanceGceSetupDataDisks]:
        return typing.cast(typing.Optional[WorkbenchInstanceGceSetupDataDisks], jsii.get(self, "dataDisksInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkbenchInstanceGceSetupNetworkInterfaces]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkbenchInstanceGceSetupNetworkInterfaces]]], jsii.get(self, "networkInterfacesInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountsInput")
    def service_accounts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkbenchInstanceGceSetupServiceAccounts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkbenchInstanceGceSetupServiceAccounts"]]], jsii.get(self, "serviceAccountsInput"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfigInput")
    def shielded_instance_config_input(
        self,
    ) -> typing.Optional["WorkbenchInstanceGceSetupShieldedInstanceConfig"]:
        return typing.cast(typing.Optional["WorkbenchInstanceGceSetupShieldedInstanceConfig"], jsii.get(self, "shieldedInstanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="vmImageInput")
    def vm_image_input(self) -> typing.Optional["WorkbenchInstanceGceSetupVmImage"]:
        return typing.cast(typing.Optional["WorkbenchInstanceGceSetupVmImage"], jsii.get(self, "vmImageInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1be6173171710327409abe977867f8d93c931c09675ba9c4c9137ef1b3782b7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__882457b83e965f47cfbcafedd6734528737fde10e76fe29a365c4662391f7688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableIpForwarding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba68e07986a55ca213be8d0575a017d069954d4e576b333ac50ac13bae8aee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f3fa573947dabca736438934d5d6b26e9c73a0f478bf8713241c9d190eb2d52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3deacf0925a924304e24097328498f3cbbda8943f460f8807eb6f4bfc631c566)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WorkbenchInstanceGceSetup]:
        return typing.cast(typing.Optional[WorkbenchInstanceGceSetup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[WorkbenchInstanceGceSetup]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7781d84e9fa2cf9f27d57c82c4efb4437c788d69c126aeb40ae31d027dcf3f08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupServiceAccounts",
    jsii_struct_bases=[],
    name_mapping={"email": "email"},
)
class WorkbenchInstanceGceSetupServiceAccounts:
    def __init__(self, *, email: typing.Optional[builtins.str] = None) -> None:
        '''
        :param email: Optional. Email address of the service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#email WorkbenchInstance#email}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64129ed1030987a968e65f9bdd05c75d9060e4b28e43ef352a245baf8eab344c)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if email is not None:
            self._values["email"] = email

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Optional. Email address of the service account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#email WorkbenchInstance#email}
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkbenchInstanceGceSetupServiceAccounts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkbenchInstanceGceSetupServiceAccountsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupServiceAccountsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e19806e75f8081997436a552b7662402d4fd1f9b61d0b10d33343aeb5829e0bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkbenchInstanceGceSetupServiceAccountsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5099601bc51d58262e8f72958d67d82ae6a84971174a9629f2c349bd0ddedc99)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkbenchInstanceGceSetupServiceAccountsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53dacc75a4e35d6837918728f627189e2a3b8dcc58a2af5173066c8042deb8b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc4444c272999c7393ca54810ae112464a8ddb9309d2db88a18576cc30cd2068)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e95f80eac34cc6c1fbc66612209165e261cbf201a4b8da7afd521f02287c623)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkbenchInstanceGceSetupServiceAccounts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkbenchInstanceGceSetupServiceAccounts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkbenchInstanceGceSetupServiceAccounts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbddc0545296ef712361f012bac5694a94e6defe66c9f27379f61fd3b22de519)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkbenchInstanceGceSetupServiceAccountsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupServiceAccountsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8169a7954997430a3b00a0bc3ac86ace6e49e73c6e044dfc4eff771e965c39b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b465ec196d7250a6432edf7913efe7f8f373583d0bc784461acce43c4a02237d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkbenchInstanceGceSetupServiceAccounts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkbenchInstanceGceSetupServiceAccounts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkbenchInstanceGceSetupServiceAccounts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aabd3008be66e5f2a8226e03dca9f8bf3cc9fca65922a8592e68ebdc0fca8ff6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupShieldedInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_integrity_monitoring": "enableIntegrityMonitoring",
        "enable_secure_boot": "enableSecureBoot",
        "enable_vtpm": "enableVtpm",
    },
)
class WorkbenchInstanceGceSetupShieldedInstanceConfig:
    def __init__(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Optional. Defines whether the VM instance has integrity monitoring enabled. Enables monitoring and attestation of the boot integrity of the VM instance. The attestation is performed against the integrity policy baseline. This baseline is initially derived from the implicitly trusted boot image when the VM instance is created. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#enable_integrity_monitoring WorkbenchInstance#enable_integrity_monitoring}
        :param enable_secure_boot: Optional. Defines whether the VM instance has Secure Boot enabled. Secure Boot helps ensure that the system only runs authentic software by verifying the digital signature of all boot components, and halting the boot process if signature verification fails. Disabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#enable_secure_boot WorkbenchInstance#enable_secure_boot}
        :param enable_vtpm: Optional. Defines whether the VM instance has the vTPM enabled. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#enable_vtpm WorkbenchInstance#enable_vtpm}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac498eb9226b6aa08c8db6cfb6d0734893fde72723ec7ea2e504860cac3b7b2e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#enable_integrity_monitoring WorkbenchInstance#enable_integrity_monitoring}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#enable_secure_boot WorkbenchInstance#enable_secure_boot}
        '''
        result = self._values.get("enable_secure_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_vtpm(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. Defines whether the VM instance has the vTPM enabled. Enabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#enable_vtpm WorkbenchInstance#enable_vtpm}
        '''
        result = self._values.get("enable_vtpm")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkbenchInstanceGceSetupShieldedInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkbenchInstanceGceSetupShieldedInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupShieldedInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe6d07ba3f66b2b03352541c955428dcc6a8f1c1e8cffec39bcfa03cf0022259)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05ca8c3858355043faa2cc05b7505f7569aef7b3ae1227b580954fcebe2eb52f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8d50eb27d1c6f69720606fe00c103fe069ee3e0b5a2166acbd60dc09f0b6f96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1c0271bfef878581802eeaaef720b160f540a7988b2771a907498526169e1c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableVtpm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkbenchInstanceGceSetupShieldedInstanceConfig]:
        return typing.cast(typing.Optional[WorkbenchInstanceGceSetupShieldedInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkbenchInstanceGceSetupShieldedInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9872e6941cae23adf1978f1d263efd9540ff69a17d4c674e66e59607a06f93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupVmImage",
    jsii_struct_bases=[],
    name_mapping={"family": "family", "name": "name", "project": "project"},
)
class WorkbenchInstanceGceSetupVmImage:
    def __init__(
        self,
        *,
        family: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param family: Optional. Use this VM image family to find the image; the newest image in this family will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#family WorkbenchInstance#family}
        :param name: Optional. Use VM image name to find the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#name WorkbenchInstance#name}
        :param project: The name of the Google Cloud project that this VM image belongs to. Format: {project_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#project WorkbenchInstance#project}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15ec4797b7a3ea8bbc63e44566d4f28139b06bf64b16014a002b9ab7c80ba64d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#family WorkbenchInstance#family}
        '''
        result = self._values.get("family")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Optional. Use VM image name to find the image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#name WorkbenchInstance#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The name of the Google Cloud project that this VM image belongs to. Format: {project_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#project WorkbenchInstance#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkbenchInstanceGceSetupVmImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkbenchInstanceGceSetupVmImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceGceSetupVmImageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__157e89adb12b86ea93ef239908563fc9446f50c394c3ae7ffb58bf264652d0b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f0fbc60420a5e1dea375bdbbf5dd02e2041d2bcf159ec75dc03d89f39926b72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "family", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0722b067ac115542502a4d30e89be117e56299e1fda9b080e6f372efa2c68d0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bf59b72318d891956f953ec883e79f5ce14ed2a5013c68491f14b9b327edfab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WorkbenchInstanceGceSetupVmImage]:
        return typing.cast(typing.Optional[WorkbenchInstanceGceSetupVmImage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkbenchInstanceGceSetupVmImage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d4afb2b14c8e6cc00802abc58bd69eefa0142ad2b70eaabd29db50f72cdaae7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceHealthInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class WorkbenchInstanceHealthInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkbenchInstanceHealthInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkbenchInstanceHealthInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceHealthInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6b9149995a226c3f63aac9e04674b829b501966ce8b31208a026834428d9961)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "WorkbenchInstanceHealthInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26adc341d006fbeb95fcbdab587b6d7586f12c25b5ad5960416bbef4c0a7a5db)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkbenchInstanceHealthInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e1167342fb1e7f1783990fdef3d497fc5a825df104c5eed5f133e2c8fc73991)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dda1aa8416b3e94b6d01869e72607e484d414cd000ec76e5470449ea253f3529)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ec3cd37d15da766bc25d730039f144f833d804c16c88e157f36a7fff0b0ecb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class WorkbenchInstanceHealthInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceHealthInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c28f97993ec406aa2981548120e3f7f6f7ab7c7738a1fe7e76ec5811c898c4f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WorkbenchInstanceHealthInfo]:
        return typing.cast(typing.Optional[WorkbenchInstanceHealthInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkbenchInstanceHealthInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc8482cf769b7ef0ce0a08585874a584146947e8006383fd52e5c2fc4fc8dc9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class WorkbenchInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#create WorkbenchInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#delete WorkbenchInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#update WorkbenchInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__936e5a598175cbec0146ec272799baba99560f98a92e05a60fb4d469f4eeab34)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#create WorkbenchInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#delete WorkbenchInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/workbench_instance#update WorkbenchInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkbenchInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkbenchInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81156630bb92e34e54a54da2d9e8a33ff8194993f7f9c2337bf17e97cac6aada)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9e2af35f5a2f5748c7b268c957b967a42e6f60927030da3a97da69ae91fc702)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b6cd379952a906c496da51e5a4fdb1bb10e07ba51b6c3b65bf8d15e77807230)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2cb91397268a101a8dc7dbd309a974a5d35f54cd37d2821325427b1e593c1f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkbenchInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkbenchInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkbenchInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19dd0836a9014d8174de63a81039170a4b7a9bdfa96514a46bc4808f8c3214a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceUpgradeHistory",
    jsii_struct_bases=[],
    name_mapping={},
)
class WorkbenchInstanceUpgradeHistory:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkbenchInstanceUpgradeHistory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkbenchInstanceUpgradeHistoryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceUpgradeHistoryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5dd82aa7b5d5cf4d2c9ce5a0a8c72537c0e7af4b0387180f0683703d953d14d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkbenchInstanceUpgradeHistoryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a87555c12b57780e953ce56215efbb732a08b2b0cf73a734cc1e1858514711fa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkbenchInstanceUpgradeHistoryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__269dafc64650d6a6c0beb737ebbe6bc0a9c0225503b6bf49585ef14190a416a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5c66c0f2f12492bd1dddeb13fa8d9d3d6a9ec2aaaa550c2d696d405a6186121)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0ee2c0c8f5ea3cb2c63bdcebd9cdcdb821ee6c36e22df32af5b7ab30e4acad0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class WorkbenchInstanceUpgradeHistoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.workbenchInstance.WorkbenchInstanceUpgradeHistoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdc1a15bc007e1785a48090830ff97cc28563066dd22def41fb788d323b200db)
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
    def internal_value(self) -> typing.Optional[WorkbenchInstanceUpgradeHistory]:
        return typing.cast(typing.Optional[WorkbenchInstanceUpgradeHistory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkbenchInstanceUpgradeHistory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ad32b5233d8d97b18ae4de56019d6e9d490854b1ada326d2df52d179936d4e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "WorkbenchInstance",
    "WorkbenchInstanceConfig",
    "WorkbenchInstanceGceSetup",
    "WorkbenchInstanceGceSetupAcceleratorConfigs",
    "WorkbenchInstanceGceSetupAcceleratorConfigsList",
    "WorkbenchInstanceGceSetupAcceleratorConfigsOutputReference",
    "WorkbenchInstanceGceSetupBootDisk",
    "WorkbenchInstanceGceSetupBootDiskOutputReference",
    "WorkbenchInstanceGceSetupConfidentialInstanceConfig",
    "WorkbenchInstanceGceSetupConfidentialInstanceConfigOutputReference",
    "WorkbenchInstanceGceSetupContainerImage",
    "WorkbenchInstanceGceSetupContainerImageOutputReference",
    "WorkbenchInstanceGceSetupDataDisks",
    "WorkbenchInstanceGceSetupDataDisksOutputReference",
    "WorkbenchInstanceGceSetupNetworkInterfaces",
    "WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs",
    "WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigsList",
    "WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigsOutputReference",
    "WorkbenchInstanceGceSetupNetworkInterfacesList",
    "WorkbenchInstanceGceSetupNetworkInterfacesOutputReference",
    "WorkbenchInstanceGceSetupOutputReference",
    "WorkbenchInstanceGceSetupServiceAccounts",
    "WorkbenchInstanceGceSetupServiceAccountsList",
    "WorkbenchInstanceGceSetupServiceAccountsOutputReference",
    "WorkbenchInstanceGceSetupShieldedInstanceConfig",
    "WorkbenchInstanceGceSetupShieldedInstanceConfigOutputReference",
    "WorkbenchInstanceGceSetupVmImage",
    "WorkbenchInstanceGceSetupVmImageOutputReference",
    "WorkbenchInstanceHealthInfo",
    "WorkbenchInstanceHealthInfoList",
    "WorkbenchInstanceHealthInfoOutputReference",
    "WorkbenchInstanceTimeouts",
    "WorkbenchInstanceTimeoutsOutputReference",
    "WorkbenchInstanceUpgradeHistory",
    "WorkbenchInstanceUpgradeHistoryList",
    "WorkbenchInstanceUpgradeHistoryOutputReference",
]

publication.publish()

def _typecheckingstub__10c94479665759d01351563c4e758a3208e02b8de6dfea620e4440b5e929e334(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    desired_state: typing.Optional[builtins.str] = None,
    disable_proxy_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_third_party_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gce_setup: typing.Optional[typing.Union[WorkbenchInstanceGceSetup, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_id: typing.Optional[builtins.str] = None,
    instance_owners: typing.Optional[typing.Sequence[builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[WorkbenchInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6082fa889728480d194929d6506c776c5073d2fe278aeccf3d4a46d5f72441cf(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__409beea1b3d54245e1f8bbfa7ab85c4c5ac82fe19692e2f6d021258d8f8d5737(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70c7faa95675ab34ecc85291147270595e009a68ef429d2cc6dc1200d50cfe98(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf337e9683a0f5604e786d7cbd453565804def6726822b277cfb4a4ac99f5e5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eab9b2f985674be82cc0ce8efa54e4bc7b88dbec11ab6f1ef513b4938ae8485c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bc0ff47222a2268d05cf27074b0ae9cc5aa130b201103cd7ae847a9e82d767b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04dc4110b4b3a0272dd7077113fa9c11aab6981a94c7e8ea1cbff7058d9ea2bf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61e3f97a7dd63f10b8a7e627e98c6487c81fb885b63dddbd7091c4850e99c8bf(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__850cb5e28c9df7b68285f6d6ed6e6271f57aaba2a92c8b251c867955257310d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e88b542fe536c46260c390c7069b85d4d1cc0260272fc73f20f6c66c400a98c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__647f9043810f6468a0be0b58ab062f060322b784726af5c4fb540f9d83bd02d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f009fd960f2bbe7214c302490b0275807fef93911cc3c56dd0380547444ee9c1(
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
    gce_setup: typing.Optional[typing.Union[WorkbenchInstanceGceSetup, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_id: typing.Optional[builtins.str] = None,
    instance_owners: typing.Optional[typing.Sequence[builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[WorkbenchInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c393af382860c38243ff8796ddbf63f69f0c49abf180c3ea5ef4b9214c6097d1(
    *,
    accelerator_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkbenchInstanceGceSetupAcceleratorConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    boot_disk: typing.Optional[typing.Union[WorkbenchInstanceGceSetupBootDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    confidential_instance_config: typing.Optional[typing.Union[WorkbenchInstanceGceSetupConfidentialInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    container_image: typing.Optional[typing.Union[WorkbenchInstanceGceSetupContainerImage, typing.Dict[builtins.str, typing.Any]]] = None,
    data_disks: typing.Optional[typing.Union[WorkbenchInstanceGceSetupDataDisks, typing.Dict[builtins.str, typing.Any]]] = None,
    disable_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_ip_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    machine_type: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    network_interfaces: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkbenchInstanceGceSetupNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_accounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkbenchInstanceGceSetupServiceAccounts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    shielded_instance_config: typing.Optional[typing.Union[WorkbenchInstanceGceSetupShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    vm_image: typing.Optional[typing.Union[WorkbenchInstanceGceSetupVmImage, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2bef2ddfc5ff419973f84a663fcaa28729604120a470e1548a4a7f4b9ba84d7(
    *,
    core_count: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48ad3213803496f32907d53482996b1936038b0e4f0c7c6e168c7a16f1716139(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49c15166bd7eacc1ed09e4c612552c6f3cd29c4d896be5ca3225ddb4bd1a68bf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75bbc134b1f43c39fbd6a4ae37147e2921961e667897fe178d217d08dcc3de70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb65425a6a2f4800177fb9cde9207201b56ce4a8da4bed57e5d14a23630b073a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cd30c28fa0259c8f2d0bc45b42598611f82050b385ba8ccb0855933766fae2a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__412258ed1f93dc0e28c8c4f7849d62511eb3aaad3588eefbcaa036f1d03090b8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkbenchInstanceGceSetupAcceleratorConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9393f2817a1f792043cd4a2a15778d1c56d2426c29a0e71b06c89138d4481111(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50077e2871cd24f672659d68f390e741e71516044862a2be9feab6bddd398e14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__effed3658769fcce86035a064d678d54df22ab12e4a52b8b65d686d29a4be0f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__413f3b359df4a7d3de22b77a476e5c1fad66dd1e422cb26f7d72bcd6b1085a6f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkbenchInstanceGceSetupAcceleratorConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ad0edb74c3c9270a0372d133a9832fecd6cfb090a090021481a135054551f5(
    *,
    disk_encryption: typing.Optional[builtins.str] = None,
    disk_size_gb: typing.Optional[builtins.str] = None,
    disk_type: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d62e34120274eb0aec49d421cf79860db9e414cd7faaadfc48e7b4d8a27adee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbf182a3056f333eb1cb806b9834f446fd9b497bf61d26823cb70045ac7ae1d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91c9110f7c8a9bb7af94d5a02c0d3f50fe9a2440837fa9140bcfe3b07457c48f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__142951b270c478ce9022b98edd4eec14453e8a5fd5ab3fb5d190a7636c6298a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9852926ba231bcf75fd3692fe96381611960077cb40e0a2eaa11b42d4bd810b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__044e24f428aca9a7164464682210659c78b15741526cb9c38c52016145d252bd(
    value: typing.Optional[WorkbenchInstanceGceSetupBootDisk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325bdc5a723f4ce20a4b68abc0e7ac1f6855640a8d01d95fbd7bd88aa35bf902(
    *,
    confidential_instance_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d451d282cd44f38b0d16ad2bbabfc3891dda07c1ec69f152fed4cfa0d5aed21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c06bae028a45f862ef5e70e0cce3bfaf88fc4b8aa117500cfeee8a90063457(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef6b44b708249817591a6c8afdea74d8596655049ce94c8d9f88e37cce0c8c99(
    value: typing.Optional[WorkbenchInstanceGceSetupConfidentialInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f48cff80679ab1f9cd7e3ee77f4d59fbdd48f0795dceadc3fbf9a9ebf244647f(
    *,
    repository: builtins.str,
    tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adcd4bbc5e151e15861c0da6b120648c33ebfc4ccaadecb0eec1ab4f979a8885(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b7beb631db8e9246be44af9766f8202fe41cbc35537a6acdde1417e429f1aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10586c58c451b75c2f0e818ba9f55ff21e2a5f31403ca0ef4c2778a3176ada5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e8e348205ef9dd646253a7705d8bb4d9d1e5c7cd9bd4d143dbd4feeaa8f5242(
    value: typing.Optional[WorkbenchInstanceGceSetupContainerImage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e745778ec4eb76c3d0c67312472e5a022e70f981a50feb14e108a58df5220d7(
    *,
    disk_encryption: typing.Optional[builtins.str] = None,
    disk_size_gb: typing.Optional[builtins.str] = None,
    disk_type: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4559dbbf1aed1e76a5ea1e58e8868d88898ae80715770cdb22c6d83cf2cce992(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26c43810ee7106a4dce700f33312724ee137710755ca0f6025ecbf54fbfdd803(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99c27849b6fd625713f253b3aa2dfcd4013c13b4784851860135c31ff30fe440(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac5876f9e7aaf84c353c82cfcf1f63328b4d3ffea1dedecce7887a7e399ed4a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f1b938d27e99fe509496eaccb1964a77021dc19d71b3ffec60939864e557115(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faede199139410b1596a44e5d1e05caaff440a8898f3d0ea75f37f4c02f6aaa8(
    value: typing.Optional[WorkbenchInstanceGceSetupDataDisks],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15cc9c707ab709643298c24566b24fb7c597362015adc9bdfa96979973e73413(
    *,
    access_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network: typing.Optional[builtins.str] = None,
    nic_type: typing.Optional[builtins.str] = None,
    subnet: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4403a1379a5a46bad7f028fbeb662d54f206b39117be2250e748e2a32bdc22f(
    *,
    external_ip: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afe7f9b256e98f4a40307aec9fbc6ce7377a855a9692171c5ea418fa457e9fe9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8de7d076bc1e5c4c65892984fa08b8d7c26cac9263afa7c170fe700937703f40(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62a17b84eaa3538c1794a0cd0990179e806854294a4c258bdbdf36c43813a9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec32112dec4359dafb4338de2724c62b735ad1aee5032b4d3ece4aacc22a6d30(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6e6e7dfaeb7e0b99de1600dfbbd21ebbf60484cad84ccfdba9246f900bf992f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__349dc99dc12fb4b6fa72356857f5eb056e9b6254a9beed414af01f7e45738a57(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a1fac7fc53d30248481f697ffaddfbf8d3f27d5bf728c2032d75eb592fcfbf2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f56d2d3d5ca8189b7838c71126e7eb559b6f8e93f6fc924d897ebe522998b33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5738db3abadb2a09975e0bf23b0bc8903240d0922bcfb932cb3b596677a5799e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__157bbbd4d77b304a9731a03df2618df7066fdd1f4ef79e5494129956c6c8d3d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e59f984a8495d02c4a9db6b2779c4fbb1e9af56f3dc10cde3b829fd0c8998cd6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0654d7907e2d8a41749bed51135946464c5633a00b60ad17551bfcf9b7b8c77d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d93c3b613ee026abb507bf534f6c526b56ad4d4d4abec82b95c631cf13e5cf60(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee2f0840b731f628cd86e22b08769c58ccf3c515b5a522cf0bdcbc21483dade(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aa989f9b58b123182545b1c4c4c639096d76361e280571a49cb390615d17303(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkbenchInstanceGceSetupNetworkInterfaces]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0fc8e957b2eda93faaf167263bf0505adda896684e5623c627776363c7edcd4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26b344a82b56b12c56b5253e58004b40d3cd855ee8c8e8ba5e42b5ff4a7b4629(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkbenchInstanceGceSetupNetworkInterfacesAccessConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2909ca44168c7a14818743b50a0e4c6970aea8d4ed90b6cfd9646868b5b212c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bab40ff2b882a56a38ed1ba341b8db9d5f2c1c05cbe3584264fbf9a42322a9d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a1767d1d962047faf950cbe03b30dc3bcb5254c2a54e24d3bf152610eff500(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a0728592bbb6a980a639789c913fc2ccae26b1f5509773905ff83704959ba00(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkbenchInstanceGceSetupNetworkInterfaces]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a57640e0422d89cab16b9c28b9cd9f9c01e1c79135196003192a7731764be369(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ac682077523b6386192faf6a426e34033ad06c78fc8a907b561c3354a5e2430(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkbenchInstanceGceSetupAcceleratorConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a976ccb27037532017cd64acb76349b86846fc219af3d5774080dcc727eb836(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkbenchInstanceGceSetupNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41fc26bf0d0ba5d7c1d34564d7328d5af5fe7b732410ebc5c8af43f7aacd4656(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkbenchInstanceGceSetupServiceAccounts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1be6173171710327409abe977867f8d93c931c09675ba9c4c9137ef1b3782b7d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882457b83e965f47cfbcafedd6734528737fde10e76fe29a365c4662391f7688(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba68e07986a55ca213be8d0575a017d069954d4e576b333ac50ac13bae8aee4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3fa573947dabca736438934d5d6b26e9c73a0f478bf8713241c9d190eb2d52(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3deacf0925a924304e24097328498f3cbbda8943f460f8807eb6f4bfc631c566(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7781d84e9fa2cf9f27d57c82c4efb4437c788d69c126aeb40ae31d027dcf3f08(
    value: typing.Optional[WorkbenchInstanceGceSetup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64129ed1030987a968e65f9bdd05c75d9060e4b28e43ef352a245baf8eab344c(
    *,
    email: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e19806e75f8081997436a552b7662402d4fd1f9b61d0b10d33343aeb5829e0bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5099601bc51d58262e8f72958d67d82ae6a84971174a9629f2c349bd0ddedc99(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53dacc75a4e35d6837918728f627189e2a3b8dcc58a2af5173066c8042deb8b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc4444c272999c7393ca54810ae112464a8ddb9309d2db88a18576cc30cd2068(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e95f80eac34cc6c1fbc66612209165e261cbf201a4b8da7afd521f02287c623(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbddc0545296ef712361f012bac5694a94e6defe66c9f27379f61fd3b22de519(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkbenchInstanceGceSetupServiceAccounts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8169a7954997430a3b00a0bc3ac86ace6e49e73c6e044dfc4eff771e965c39b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b465ec196d7250a6432edf7913efe7f8f373583d0bc784461acce43c4a02237d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aabd3008be66e5f2a8226e03dca9f8bf3cc9fca65922a8592e68ebdc0fca8ff6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkbenchInstanceGceSetupServiceAccounts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac498eb9226b6aa08c8db6cfb6d0734893fde72723ec7ea2e504860cac3b7b2e(
    *,
    enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe6d07ba3f66b2b03352541c955428dcc6a8f1c1e8cffec39bcfa03cf0022259(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05ca8c3858355043faa2cc05b7505f7569aef7b3ae1227b580954fcebe2eb52f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8d50eb27d1c6f69720606fe00c103fe069ee3e0b5a2166acbd60dc09f0b6f96(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c0271bfef878581802eeaaef720b160f540a7988b2771a907498526169e1c0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9872e6941cae23adf1978f1d263efd9540ff69a17d4c674e66e59607a06f93(
    value: typing.Optional[WorkbenchInstanceGceSetupShieldedInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ec4797b7a3ea8bbc63e44566d4f28139b06bf64b16014a002b9ab7c80ba64d(
    *,
    family: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__157e89adb12b86ea93ef239908563fc9446f50c394c3ae7ffb58bf264652d0b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0fbc60420a5e1dea375bdbbf5dd02e2041d2bcf159ec75dc03d89f39926b72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0722b067ac115542502a4d30e89be117e56299e1fda9b080e6f372efa2c68d0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bf59b72318d891956f953ec883e79f5ce14ed2a5013c68491f14b9b327edfab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d4afb2b14c8e6cc00802abc58bd69eefa0142ad2b70eaabd29db50f72cdaae7(
    value: typing.Optional[WorkbenchInstanceGceSetupVmImage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6b9149995a226c3f63aac9e04674b829b501966ce8b31208a026834428d9961(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26adc341d006fbeb95fcbdab587b6d7586f12c25b5ad5960416bbef4c0a7a5db(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e1167342fb1e7f1783990fdef3d497fc5a825df104c5eed5f133e2c8fc73991(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dda1aa8416b3e94b6d01869e72607e484d414cd000ec76e5470449ea253f3529(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ec3cd37d15da766bc25d730039f144f833d804c16c88e157f36a7fff0b0ecb7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c28f97993ec406aa2981548120e3f7f6f7ab7c7738a1fe7e76ec5811c898c4f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc8482cf769b7ef0ce0a08585874a584146947e8006383fd52e5c2fc4fc8dc9d(
    value: typing.Optional[WorkbenchInstanceHealthInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__936e5a598175cbec0146ec272799baba99560f98a92e05a60fb4d469f4eeab34(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81156630bb92e34e54a54da2d9e8a33ff8194993f7f9c2337bf17e97cac6aada(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9e2af35f5a2f5748c7b268c957b967a42e6f60927030da3a97da69ae91fc702(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6cd379952a906c496da51e5a4fdb1bb10e07ba51b6c3b65bf8d15e77807230(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2cb91397268a101a8dc7dbd309a974a5d35f54cd37d2821325427b1e593c1f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19dd0836a9014d8174de63a81039170a4b7a9bdfa96514a46bc4808f8c3214a6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkbenchInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5dd82aa7b5d5cf4d2c9ce5a0a8c72537c0e7af4b0387180f0683703d953d14d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87555c12b57780e953ce56215efbb732a08b2b0cf73a734cc1e1858514711fa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__269dafc64650d6a6c0beb737ebbe6bc0a9c0225503b6bf49585ef14190a416a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c66c0f2f12492bd1dddeb13fa8d9d3d6a9ec2aaaa550c2d696d405a6186121(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0ee2c0c8f5ea3cb2c63bdcebd9cdcdb821ee6c36e22df32af5b7ab30e4acad0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc1a15bc007e1785a48090830ff97cc28563066dd22def41fb788d323b200db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad32b5233d8d97b18ae4de56019d6e9d490854b1ada326d2df52d179936d4e2(
    value: typing.Optional[WorkbenchInstanceUpgradeHistory],
) -> None:
    """Type checking stubs"""
    pass
