r'''
# `google_colab_runtime_template`

Refer to the Terraform Registry for docs: [`google_colab_runtime_template`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template).
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


class GoogleColabRuntimeTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template google_colab_runtime_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        location: builtins.str,
        data_persistent_disk_spec: typing.Optional[typing.Union["GoogleColabRuntimeTemplateDataPersistentDiskSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_spec: typing.Optional[typing.Union["GoogleColabRuntimeTemplateEncryptionSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        euc_config: typing.Optional[typing.Union["GoogleColabRuntimeTemplateEucConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        idle_shutdown_config: typing.Optional[typing.Union["GoogleColabRuntimeTemplateIdleShutdownConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        machine_spec: typing.Optional[typing.Union["GoogleColabRuntimeTemplateMachineSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        network_spec: typing.Optional[typing.Union["GoogleColabRuntimeTemplateNetworkSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        shielded_vm_config: typing.Optional[typing.Union["GoogleColabRuntimeTemplateShieldedVmConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        software_config: typing.Optional[typing.Union["GoogleColabRuntimeTemplateSoftwareConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleColabRuntimeTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template google_colab_runtime_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: Required. The display name of the Runtime Template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#display_name GoogleColabRuntimeTemplate#display_name}
        :param location: The location for the resource: https://cloud.google.com/colab/docs/locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#location GoogleColabRuntimeTemplate#location}
        :param data_persistent_disk_spec: data_persistent_disk_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#data_persistent_disk_spec GoogleColabRuntimeTemplate#data_persistent_disk_spec}
        :param description: The description of the Runtime Template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#description GoogleColabRuntimeTemplate#description}
        :param encryption_spec: encryption_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#encryption_spec GoogleColabRuntimeTemplate#encryption_spec}
        :param euc_config: euc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#euc_config GoogleColabRuntimeTemplate#euc_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#id GoogleColabRuntimeTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param idle_shutdown_config: idle_shutdown_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#idle_shutdown_config GoogleColabRuntimeTemplate#idle_shutdown_config}
        :param labels: Labels to identify and group the runtime template. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#labels GoogleColabRuntimeTemplate#labels}
        :param machine_spec: machine_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#machine_spec GoogleColabRuntimeTemplate#machine_spec}
        :param name: The resource name of the Runtime Template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#name GoogleColabRuntimeTemplate#name}
        :param network_spec: network_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#network_spec GoogleColabRuntimeTemplate#network_spec}
        :param network_tags: Applies the given Compute Engine tags to the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#network_tags GoogleColabRuntimeTemplate#network_tags}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#project GoogleColabRuntimeTemplate#project}.
        :param shielded_vm_config: shielded_vm_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#shielded_vm_config GoogleColabRuntimeTemplate#shielded_vm_config}
        :param software_config: software_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#software_config GoogleColabRuntimeTemplate#software_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#timeouts GoogleColabRuntimeTemplate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b23437dde98e2b405653913408cd74d96a730c99339a5abbd5b2667cd2ad96d1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleColabRuntimeTemplateConfig(
            display_name=display_name,
            location=location,
            data_persistent_disk_spec=data_persistent_disk_spec,
            description=description,
            encryption_spec=encryption_spec,
            euc_config=euc_config,
            id=id,
            idle_shutdown_config=idle_shutdown_config,
            labels=labels,
            machine_spec=machine_spec,
            name=name,
            network_spec=network_spec,
            network_tags=network_tags,
            project=project,
            shielded_vm_config=shielded_vm_config,
            software_config=software_config,
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
        '''Generates CDKTF code for importing a GoogleColabRuntimeTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleColabRuntimeTemplate to import.
        :param import_from_id: The id of the existing GoogleColabRuntimeTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleColabRuntimeTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35425cbffdc48d6d02e75703c1e691d7fec3d8e6fc1d1835229f84bb27c73251)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDataPersistentDiskSpec")
    def put_data_persistent_disk_spec(
        self,
        *,
        disk_size_gb: typing.Optional[builtins.str] = None,
        disk_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_size_gb: The disk size of the runtime in GB. If specified, the diskType must also be specified. The minimum size is 10GB and the maximum is 65536GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#disk_size_gb GoogleColabRuntimeTemplate#disk_size_gb}
        :param disk_type: The type of the persistent disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#disk_type GoogleColabRuntimeTemplate#disk_type}
        '''
        value = GoogleColabRuntimeTemplateDataPersistentDiskSpec(
            disk_size_gb=disk_size_gb, disk_type=disk_type
        )

        return typing.cast(None, jsii.invoke(self, "putDataPersistentDiskSpec", [value]))

    @jsii.member(jsii_name="putEncryptionSpec")
    def put_encryption_spec(
        self,
        *,
        kms_key_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_name: The Cloud KMS encryption key (customer-managed encryption key) used to protect the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#kms_key_name GoogleColabRuntimeTemplate#kms_key_name}
        '''
        value = GoogleColabRuntimeTemplateEncryptionSpec(kms_key_name=kms_key_name)

        return typing.cast(None, jsii.invoke(self, "putEncryptionSpec", [value]))

    @jsii.member(jsii_name="putEucConfig")
    def put_euc_config(
        self,
        *,
        euc_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param euc_disabled: Disable end user credential access for the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#euc_disabled GoogleColabRuntimeTemplate#euc_disabled}
        '''
        value = GoogleColabRuntimeTemplateEucConfig(euc_disabled=euc_disabled)

        return typing.cast(None, jsii.invoke(self, "putEucConfig", [value]))

    @jsii.member(jsii_name="putIdleShutdownConfig")
    def put_idle_shutdown_config(
        self,
        *,
        idle_timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param idle_timeout: The duration after which the runtime is automatically shut down. An input of 0s disables the idle shutdown feature, and a valid range is [10m, 24h]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#idle_timeout GoogleColabRuntimeTemplate#idle_timeout}
        '''
        value = GoogleColabRuntimeTemplateIdleShutdownConfig(idle_timeout=idle_timeout)

        return typing.cast(None, jsii.invoke(self, "putIdleShutdownConfig", [value]))

    @jsii.member(jsii_name="putMachineSpec")
    def put_machine_spec(
        self,
        *,
        accelerator_count: typing.Optional[jsii.Number] = None,
        accelerator_type: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accelerator_count: The number of accelerators used by the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#accelerator_count GoogleColabRuntimeTemplate#accelerator_count}
        :param accelerator_type: The type of hardware accelerator used by the runtime. If specified, acceleratorCount must also be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#accelerator_type GoogleColabRuntimeTemplate#accelerator_type}
        :param machine_type: The Compute Engine machine type selected for the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#machine_type GoogleColabRuntimeTemplate#machine_type}
        '''
        value = GoogleColabRuntimeTemplateMachineSpec(
            accelerator_count=accelerator_count,
            accelerator_type=accelerator_type,
            machine_type=machine_type,
        )

        return typing.cast(None, jsii.invoke(self, "putMachineSpec", [value]))

    @jsii.member(jsii_name="putNetworkSpec")
    def put_network_spec(
        self,
        *,
        enable_internet_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enable_internet_access: Enable public internet access for the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#enable_internet_access GoogleColabRuntimeTemplate#enable_internet_access}
        :param network: The name of the VPC that this runtime is in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#network GoogleColabRuntimeTemplate#network}
        :param subnetwork: The name of the subnetwork that this runtime is in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#subnetwork GoogleColabRuntimeTemplate#subnetwork}
        '''
        value = GoogleColabRuntimeTemplateNetworkSpec(
            enable_internet_access=enable_internet_access,
            network=network,
            subnetwork=subnetwork,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkSpec", [value]))

    @jsii.member(jsii_name="putShieldedVmConfig")
    def put_shielded_vm_config(
        self,
        *,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_secure_boot: Enables secure boot for the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#enable_secure_boot GoogleColabRuntimeTemplate#enable_secure_boot}
        '''
        value = GoogleColabRuntimeTemplateShieldedVmConfig(
            enable_secure_boot=enable_secure_boot
        )

        return typing.cast(None, jsii.invoke(self, "putShieldedVmConfig", [value]))

    @jsii.member(jsii_name="putSoftwareConfig")
    def put_software_config(
        self,
        *,
        env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleColabRuntimeTemplateSoftwareConfigEnv", typing.Dict[builtins.str, typing.Any]]]]] = None,
        post_startup_script_config: typing.Optional[typing.Union["GoogleColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param env: env block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#env GoogleColabRuntimeTemplate#env}
        :param post_startup_script_config: post_startup_script_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#post_startup_script_config GoogleColabRuntimeTemplate#post_startup_script_config}
        '''
        value = GoogleColabRuntimeTemplateSoftwareConfig(
            env=env, post_startup_script_config=post_startup_script_config
        )

        return typing.cast(None, jsii.invoke(self, "putSoftwareConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#create GoogleColabRuntimeTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#delete GoogleColabRuntimeTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#update GoogleColabRuntimeTemplate#update}.
        '''
        value = GoogleColabRuntimeTemplateTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDataPersistentDiskSpec")
    def reset_data_persistent_disk_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataPersistentDiskSpec", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEncryptionSpec")
    def reset_encryption_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionSpec", []))

    @jsii.member(jsii_name="resetEucConfig")
    def reset_euc_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEucConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdleShutdownConfig")
    def reset_idle_shutdown_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdleShutdownConfig", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMachineSpec")
    def reset_machine_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineSpec", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNetworkSpec")
    def reset_network_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkSpec", []))

    @jsii.member(jsii_name="resetNetworkTags")
    def reset_network_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkTags", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetShieldedVmConfig")
    def reset_shielded_vm_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShieldedVmConfig", []))

    @jsii.member(jsii_name="resetSoftwareConfig")
    def reset_software_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSoftwareConfig", []))

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
    @jsii.member(jsii_name="dataPersistentDiskSpec")
    def data_persistent_disk_spec(
        self,
    ) -> "GoogleColabRuntimeTemplateDataPersistentDiskSpecOutputReference":
        return typing.cast("GoogleColabRuntimeTemplateDataPersistentDiskSpecOutputReference", jsii.get(self, "dataPersistentDiskSpec"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="encryptionSpec")
    def encryption_spec(
        self,
    ) -> "GoogleColabRuntimeTemplateEncryptionSpecOutputReference":
        return typing.cast("GoogleColabRuntimeTemplateEncryptionSpecOutputReference", jsii.get(self, "encryptionSpec"))

    @builtins.property
    @jsii.member(jsii_name="eucConfig")
    def euc_config(self) -> "GoogleColabRuntimeTemplateEucConfigOutputReference":
        return typing.cast("GoogleColabRuntimeTemplateEucConfigOutputReference", jsii.get(self, "eucConfig"))

    @builtins.property
    @jsii.member(jsii_name="idleShutdownConfig")
    def idle_shutdown_config(
        self,
    ) -> "GoogleColabRuntimeTemplateIdleShutdownConfigOutputReference":
        return typing.cast("GoogleColabRuntimeTemplateIdleShutdownConfigOutputReference", jsii.get(self, "idleShutdownConfig"))

    @builtins.property
    @jsii.member(jsii_name="machineSpec")
    def machine_spec(self) -> "GoogleColabRuntimeTemplateMachineSpecOutputReference":
        return typing.cast("GoogleColabRuntimeTemplateMachineSpecOutputReference", jsii.get(self, "machineSpec"))

    @builtins.property
    @jsii.member(jsii_name="networkSpec")
    def network_spec(self) -> "GoogleColabRuntimeTemplateNetworkSpecOutputReference":
        return typing.cast("GoogleColabRuntimeTemplateNetworkSpecOutputReference", jsii.get(self, "networkSpec"))

    @builtins.property
    @jsii.member(jsii_name="shieldedVmConfig")
    def shielded_vm_config(
        self,
    ) -> "GoogleColabRuntimeTemplateShieldedVmConfigOutputReference":
        return typing.cast("GoogleColabRuntimeTemplateShieldedVmConfigOutputReference", jsii.get(self, "shieldedVmConfig"))

    @builtins.property
    @jsii.member(jsii_name="softwareConfig")
    def software_config(
        self,
    ) -> "GoogleColabRuntimeTemplateSoftwareConfigOutputReference":
        return typing.cast("GoogleColabRuntimeTemplateSoftwareConfigOutputReference", jsii.get(self, "softwareConfig"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleColabRuntimeTemplateTimeoutsOutputReference":
        return typing.cast("GoogleColabRuntimeTemplateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="dataPersistentDiskSpecInput")
    def data_persistent_disk_spec_input(
        self,
    ) -> typing.Optional["GoogleColabRuntimeTemplateDataPersistentDiskSpec"]:
        return typing.cast(typing.Optional["GoogleColabRuntimeTemplateDataPersistentDiskSpec"], jsii.get(self, "dataPersistentDiskSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionSpecInput")
    def encryption_spec_input(
        self,
    ) -> typing.Optional["GoogleColabRuntimeTemplateEncryptionSpec"]:
        return typing.cast(typing.Optional["GoogleColabRuntimeTemplateEncryptionSpec"], jsii.get(self, "encryptionSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="eucConfigInput")
    def euc_config_input(
        self,
    ) -> typing.Optional["GoogleColabRuntimeTemplateEucConfig"]:
        return typing.cast(typing.Optional["GoogleColabRuntimeTemplateEucConfig"], jsii.get(self, "eucConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="idleShutdownConfigInput")
    def idle_shutdown_config_input(
        self,
    ) -> typing.Optional["GoogleColabRuntimeTemplateIdleShutdownConfig"]:
        return typing.cast(typing.Optional["GoogleColabRuntimeTemplateIdleShutdownConfig"], jsii.get(self, "idleShutdownConfigInput"))

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
    @jsii.member(jsii_name="machineSpecInput")
    def machine_spec_input(
        self,
    ) -> typing.Optional["GoogleColabRuntimeTemplateMachineSpec"]:
        return typing.cast(typing.Optional["GoogleColabRuntimeTemplateMachineSpec"], jsii.get(self, "machineSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkSpecInput")
    def network_spec_input(
        self,
    ) -> typing.Optional["GoogleColabRuntimeTemplateNetworkSpec"]:
        return typing.cast(typing.Optional["GoogleColabRuntimeTemplateNetworkSpec"], jsii.get(self, "networkSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="networkTagsInput")
    def network_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "networkTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="shieldedVmConfigInput")
    def shielded_vm_config_input(
        self,
    ) -> typing.Optional["GoogleColabRuntimeTemplateShieldedVmConfig"]:
        return typing.cast(typing.Optional["GoogleColabRuntimeTemplateShieldedVmConfig"], jsii.get(self, "shieldedVmConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="softwareConfigInput")
    def software_config_input(
        self,
    ) -> typing.Optional["GoogleColabRuntimeTemplateSoftwareConfig"]:
        return typing.cast(typing.Optional["GoogleColabRuntimeTemplateSoftwareConfig"], jsii.get(self, "softwareConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleColabRuntimeTemplateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleColabRuntimeTemplateTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83d1713765eafd90a098fc2cbd9341386b000781e36aab554f0d256afa9bfea6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__894ae7ac3d24143680cdfca8933438cb721d167dd986d52ea0fa648f3c893077)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34f912627d67359b5c335b1384c9c846f94d0d79f9093e8837b91fb9566eef66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f506d06982b0dbc55a64fde8efdeea4242ea979cf5b076326525e1965ca55c0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5dd950ba3bb2bc03a320c7663c9bce2b19fb4c03f16f8f2b25084e1c23d07f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aae665077d911f30fd314ede1fb2d3c14982a0ee8203f9bbddefe7ebe37dc91c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkTags")
    def network_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkTags"))

    @network_tags.setter
    def network_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8d7aa006ea23e2e3317153c7fccf0d919dfee50dca1edaf06c08838e766fdd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b3dc61d198d1534113199675580030ceca6e2bf496089552660c485af3760b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "display_name": "displayName",
        "location": "location",
        "data_persistent_disk_spec": "dataPersistentDiskSpec",
        "description": "description",
        "encryption_spec": "encryptionSpec",
        "euc_config": "eucConfig",
        "id": "id",
        "idle_shutdown_config": "idleShutdownConfig",
        "labels": "labels",
        "machine_spec": "machineSpec",
        "name": "name",
        "network_spec": "networkSpec",
        "network_tags": "networkTags",
        "project": "project",
        "shielded_vm_config": "shieldedVmConfig",
        "software_config": "softwareConfig",
        "timeouts": "timeouts",
    },
)
class GoogleColabRuntimeTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        display_name: builtins.str,
        location: builtins.str,
        data_persistent_disk_spec: typing.Optional[typing.Union["GoogleColabRuntimeTemplateDataPersistentDiskSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_spec: typing.Optional[typing.Union["GoogleColabRuntimeTemplateEncryptionSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        euc_config: typing.Optional[typing.Union["GoogleColabRuntimeTemplateEucConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        idle_shutdown_config: typing.Optional[typing.Union["GoogleColabRuntimeTemplateIdleShutdownConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        machine_spec: typing.Optional[typing.Union["GoogleColabRuntimeTemplateMachineSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        network_spec: typing.Optional[typing.Union["GoogleColabRuntimeTemplateNetworkSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        shielded_vm_config: typing.Optional[typing.Union["GoogleColabRuntimeTemplateShieldedVmConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        software_config: typing.Optional[typing.Union["GoogleColabRuntimeTemplateSoftwareConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleColabRuntimeTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: Required. The display name of the Runtime Template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#display_name GoogleColabRuntimeTemplate#display_name}
        :param location: The location for the resource: https://cloud.google.com/colab/docs/locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#location GoogleColabRuntimeTemplate#location}
        :param data_persistent_disk_spec: data_persistent_disk_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#data_persistent_disk_spec GoogleColabRuntimeTemplate#data_persistent_disk_spec}
        :param description: The description of the Runtime Template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#description GoogleColabRuntimeTemplate#description}
        :param encryption_spec: encryption_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#encryption_spec GoogleColabRuntimeTemplate#encryption_spec}
        :param euc_config: euc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#euc_config GoogleColabRuntimeTemplate#euc_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#id GoogleColabRuntimeTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param idle_shutdown_config: idle_shutdown_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#idle_shutdown_config GoogleColabRuntimeTemplate#idle_shutdown_config}
        :param labels: Labels to identify and group the runtime template. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#labels GoogleColabRuntimeTemplate#labels}
        :param machine_spec: machine_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#machine_spec GoogleColabRuntimeTemplate#machine_spec}
        :param name: The resource name of the Runtime Template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#name GoogleColabRuntimeTemplate#name}
        :param network_spec: network_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#network_spec GoogleColabRuntimeTemplate#network_spec}
        :param network_tags: Applies the given Compute Engine tags to the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#network_tags GoogleColabRuntimeTemplate#network_tags}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#project GoogleColabRuntimeTemplate#project}.
        :param shielded_vm_config: shielded_vm_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#shielded_vm_config GoogleColabRuntimeTemplate#shielded_vm_config}
        :param software_config: software_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#software_config GoogleColabRuntimeTemplate#software_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#timeouts GoogleColabRuntimeTemplate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(data_persistent_disk_spec, dict):
            data_persistent_disk_spec = GoogleColabRuntimeTemplateDataPersistentDiskSpec(**data_persistent_disk_spec)
        if isinstance(encryption_spec, dict):
            encryption_spec = GoogleColabRuntimeTemplateEncryptionSpec(**encryption_spec)
        if isinstance(euc_config, dict):
            euc_config = GoogleColabRuntimeTemplateEucConfig(**euc_config)
        if isinstance(idle_shutdown_config, dict):
            idle_shutdown_config = GoogleColabRuntimeTemplateIdleShutdownConfig(**idle_shutdown_config)
        if isinstance(machine_spec, dict):
            machine_spec = GoogleColabRuntimeTemplateMachineSpec(**machine_spec)
        if isinstance(network_spec, dict):
            network_spec = GoogleColabRuntimeTemplateNetworkSpec(**network_spec)
        if isinstance(shielded_vm_config, dict):
            shielded_vm_config = GoogleColabRuntimeTemplateShieldedVmConfig(**shielded_vm_config)
        if isinstance(software_config, dict):
            software_config = GoogleColabRuntimeTemplateSoftwareConfig(**software_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleColabRuntimeTemplateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cf9a2aa8a8f6b65dfd6534e9b82c937786cd83349139a4455f30c5e607078d1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument data_persistent_disk_spec", value=data_persistent_disk_spec, expected_type=type_hints["data_persistent_disk_spec"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encryption_spec", value=encryption_spec, expected_type=type_hints["encryption_spec"])
            check_type(argname="argument euc_config", value=euc_config, expected_type=type_hints["euc_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument idle_shutdown_config", value=idle_shutdown_config, expected_type=type_hints["idle_shutdown_config"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument machine_spec", value=machine_spec, expected_type=type_hints["machine_spec"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_spec", value=network_spec, expected_type=type_hints["network_spec"])
            check_type(argname="argument network_tags", value=network_tags, expected_type=type_hints["network_tags"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument shielded_vm_config", value=shielded_vm_config, expected_type=type_hints["shielded_vm_config"])
            check_type(argname="argument software_config", value=software_config, expected_type=type_hints["software_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "location": location,
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
        if data_persistent_disk_spec is not None:
            self._values["data_persistent_disk_spec"] = data_persistent_disk_spec
        if description is not None:
            self._values["description"] = description
        if encryption_spec is not None:
            self._values["encryption_spec"] = encryption_spec
        if euc_config is not None:
            self._values["euc_config"] = euc_config
        if id is not None:
            self._values["id"] = id
        if idle_shutdown_config is not None:
            self._values["idle_shutdown_config"] = idle_shutdown_config
        if labels is not None:
            self._values["labels"] = labels
        if machine_spec is not None:
            self._values["machine_spec"] = machine_spec
        if name is not None:
            self._values["name"] = name
        if network_spec is not None:
            self._values["network_spec"] = network_spec
        if network_tags is not None:
            self._values["network_tags"] = network_tags
        if project is not None:
            self._values["project"] = project
        if shielded_vm_config is not None:
            self._values["shielded_vm_config"] = shielded_vm_config
        if software_config is not None:
            self._values["software_config"] = software_config
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
    def display_name(self) -> builtins.str:
        '''Required. The display name of the Runtime Template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#display_name GoogleColabRuntimeTemplate#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource: https://cloud.google.com/colab/docs/locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#location GoogleColabRuntimeTemplate#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_persistent_disk_spec(
        self,
    ) -> typing.Optional["GoogleColabRuntimeTemplateDataPersistentDiskSpec"]:
        '''data_persistent_disk_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#data_persistent_disk_spec GoogleColabRuntimeTemplate#data_persistent_disk_spec}
        '''
        result = self._values.get("data_persistent_disk_spec")
        return typing.cast(typing.Optional["GoogleColabRuntimeTemplateDataPersistentDiskSpec"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the Runtime Template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#description GoogleColabRuntimeTemplate#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_spec(
        self,
    ) -> typing.Optional["GoogleColabRuntimeTemplateEncryptionSpec"]:
        '''encryption_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#encryption_spec GoogleColabRuntimeTemplate#encryption_spec}
        '''
        result = self._values.get("encryption_spec")
        return typing.cast(typing.Optional["GoogleColabRuntimeTemplateEncryptionSpec"], result)

    @builtins.property
    def euc_config(self) -> typing.Optional["GoogleColabRuntimeTemplateEucConfig"]:
        '''euc_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#euc_config GoogleColabRuntimeTemplate#euc_config}
        '''
        result = self._values.get("euc_config")
        return typing.cast(typing.Optional["GoogleColabRuntimeTemplateEucConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#id GoogleColabRuntimeTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idle_shutdown_config(
        self,
    ) -> typing.Optional["GoogleColabRuntimeTemplateIdleShutdownConfig"]:
        '''idle_shutdown_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#idle_shutdown_config GoogleColabRuntimeTemplate#idle_shutdown_config}
        '''
        result = self._values.get("idle_shutdown_config")
        return typing.cast(typing.Optional["GoogleColabRuntimeTemplateIdleShutdownConfig"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels to identify and group the runtime template.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#labels GoogleColabRuntimeTemplate#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def machine_spec(self) -> typing.Optional["GoogleColabRuntimeTemplateMachineSpec"]:
        '''machine_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#machine_spec GoogleColabRuntimeTemplate#machine_spec}
        '''
        result = self._values.get("machine_spec")
        return typing.cast(typing.Optional["GoogleColabRuntimeTemplateMachineSpec"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The resource name of the Runtime Template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#name GoogleColabRuntimeTemplate#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_spec(self) -> typing.Optional["GoogleColabRuntimeTemplateNetworkSpec"]:
        '''network_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#network_spec GoogleColabRuntimeTemplate#network_spec}
        '''
        result = self._values.get("network_spec")
        return typing.cast(typing.Optional["GoogleColabRuntimeTemplateNetworkSpec"], result)

    @builtins.property
    def network_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Applies the given Compute Engine tags to the runtime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#network_tags GoogleColabRuntimeTemplate#network_tags}
        '''
        result = self._values.get("network_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#project GoogleColabRuntimeTemplate#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shielded_vm_config(
        self,
    ) -> typing.Optional["GoogleColabRuntimeTemplateShieldedVmConfig"]:
        '''shielded_vm_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#shielded_vm_config GoogleColabRuntimeTemplate#shielded_vm_config}
        '''
        result = self._values.get("shielded_vm_config")
        return typing.cast(typing.Optional["GoogleColabRuntimeTemplateShieldedVmConfig"], result)

    @builtins.property
    def software_config(
        self,
    ) -> typing.Optional["GoogleColabRuntimeTemplateSoftwareConfig"]:
        '''software_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#software_config GoogleColabRuntimeTemplate#software_config}
        '''
        result = self._values.get("software_config")
        return typing.cast(typing.Optional["GoogleColabRuntimeTemplateSoftwareConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleColabRuntimeTemplateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#timeouts GoogleColabRuntimeTemplate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleColabRuntimeTemplateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleColabRuntimeTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateDataPersistentDiskSpec",
    jsii_struct_bases=[],
    name_mapping={"disk_size_gb": "diskSizeGb", "disk_type": "diskType"},
)
class GoogleColabRuntimeTemplateDataPersistentDiskSpec:
    def __init__(
        self,
        *,
        disk_size_gb: typing.Optional[builtins.str] = None,
        disk_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_size_gb: The disk size of the runtime in GB. If specified, the diskType must also be specified. The minimum size is 10GB and the maximum is 65536GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#disk_size_gb GoogleColabRuntimeTemplate#disk_size_gb}
        :param disk_type: The type of the persistent disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#disk_type GoogleColabRuntimeTemplate#disk_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ab1b8ebc82db896ce9db108ccb68c632bcff1c87cebba41c3e8b6d054af6ed2)
            check_type(argname="argument disk_size_gb", value=disk_size_gb, expected_type=type_hints["disk_size_gb"])
            check_type(argname="argument disk_type", value=disk_type, expected_type=type_hints["disk_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disk_size_gb is not None:
            self._values["disk_size_gb"] = disk_size_gb
        if disk_type is not None:
            self._values["disk_type"] = disk_type

    @builtins.property
    def disk_size_gb(self) -> typing.Optional[builtins.str]:
        '''The disk size of the runtime in GB.

        If specified, the diskType must also be specified. The minimum size is 10GB and the maximum is 65536GB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#disk_size_gb GoogleColabRuntimeTemplate#disk_size_gb}
        '''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_type(self) -> typing.Optional[builtins.str]:
        '''The type of the persistent disk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#disk_type GoogleColabRuntimeTemplate#disk_type}
        '''
        result = self._values.get("disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleColabRuntimeTemplateDataPersistentDiskSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleColabRuntimeTemplateDataPersistentDiskSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateDataPersistentDiskSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b178e27c3eaed514d391b279dd2a3e814c3f8c1e16df0c5729cb4e4e73cfe2ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDiskSizeGb")
    def reset_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskSizeGb", []))

    @jsii.member(jsii_name="resetDiskType")
    def reset_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskType", []))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGbInput")
    def disk_size_gb_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="diskTypeInput")
    def disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b8eb0f4ab96ef7913e48996e70218eda85813e6639ce162383b0fa0535d1ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskType")
    def disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskType"))

    @disk_type.setter
    def disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__686eb456fa33dc5e49f518dbaacf567bdee86349bdf00b2414cd63900c9c53a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleColabRuntimeTemplateDataPersistentDiskSpec]:
        return typing.cast(typing.Optional[GoogleColabRuntimeTemplateDataPersistentDiskSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleColabRuntimeTemplateDataPersistentDiskSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15d008a87fdf06a1364596abc4aff0e0c6757a1c39fad084593223dea644e4f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateEncryptionSpec",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class GoogleColabRuntimeTemplateEncryptionSpec:
    def __init__(self, *, kms_key_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key_name: The Cloud KMS encryption key (customer-managed encryption key) used to protect the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#kms_key_name GoogleColabRuntimeTemplate#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eec6e47cbddef9cdb802b1c5d3915a4e34430961f7367a1d093bf7f5ec17cdc7)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''The Cloud KMS encryption key (customer-managed encryption key) used to protect the runtime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#kms_key_name GoogleColabRuntimeTemplate#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleColabRuntimeTemplateEncryptionSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleColabRuntimeTemplateEncryptionSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateEncryptionSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf2cf77ceb60c63c7e89e87cde66f5f0de8ed21f1895a04b2ebf59390509d3b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a268593a8d6df549d82434de193fbb7a888b1e2265bceb9a0a2de4372ce0826)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleColabRuntimeTemplateEncryptionSpec]:
        return typing.cast(typing.Optional[GoogleColabRuntimeTemplateEncryptionSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleColabRuntimeTemplateEncryptionSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6911dbedde4a0b912e093b77e425a74736533ae681dd0971ad44eac08d80426)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateEucConfig",
    jsii_struct_bases=[],
    name_mapping={"euc_disabled": "eucDisabled"},
)
class GoogleColabRuntimeTemplateEucConfig:
    def __init__(
        self,
        *,
        euc_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param euc_disabled: Disable end user credential access for the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#euc_disabled GoogleColabRuntimeTemplate#euc_disabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e88f12713aa5df05fc23afe9259aa1a4aa1862e0bc6c2df021f80040c7dbd2ac)
            check_type(argname="argument euc_disabled", value=euc_disabled, expected_type=type_hints["euc_disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if euc_disabled is not None:
            self._values["euc_disabled"] = euc_disabled

    @builtins.property
    def euc_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable end user credential access for the runtime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#euc_disabled GoogleColabRuntimeTemplate#euc_disabled}
        '''
        result = self._values.get("euc_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleColabRuntimeTemplateEucConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleColabRuntimeTemplateEucConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateEucConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f1fe5b5dd194ad36c8ae7ef3f4aadc3d4c7c28db46822723f4518c424f3c0d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEucDisabled")
    def reset_euc_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEucDisabled", []))

    @builtins.property
    @jsii.member(jsii_name="eucDisabledInput")
    def euc_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "eucDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="eucDisabled")
    def euc_disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "eucDisabled"))

    @euc_disabled.setter
    def euc_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__514496294d0d8665a5ca904c377bfc2615125a2f60781f32b62354f71beb459b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eucDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleColabRuntimeTemplateEucConfig]:
        return typing.cast(typing.Optional[GoogleColabRuntimeTemplateEucConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleColabRuntimeTemplateEucConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__412883a8c2a3cf786de023d8249df9aac4f00e4287bdf0eaf716c525449731be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateIdleShutdownConfig",
    jsii_struct_bases=[],
    name_mapping={"idle_timeout": "idleTimeout"},
)
class GoogleColabRuntimeTemplateIdleShutdownConfig:
    def __init__(self, *, idle_timeout: typing.Optional[builtins.str] = None) -> None:
        '''
        :param idle_timeout: The duration after which the runtime is automatically shut down. An input of 0s disables the idle shutdown feature, and a valid range is [10m, 24h]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#idle_timeout GoogleColabRuntimeTemplate#idle_timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f33a07f139d045cc3d5a097d6aace69a1eaa3cc4301ab773915361c0a5dcd664)
            check_type(argname="argument idle_timeout", value=idle_timeout, expected_type=type_hints["idle_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if idle_timeout is not None:
            self._values["idle_timeout"] = idle_timeout

    @builtins.property
    def idle_timeout(self) -> typing.Optional[builtins.str]:
        '''The duration after which the runtime is automatically shut down.

        An input of 0s disables the idle shutdown feature, and a valid range is [10m, 24h].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#idle_timeout GoogleColabRuntimeTemplate#idle_timeout}
        '''
        result = self._values.get("idle_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleColabRuntimeTemplateIdleShutdownConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleColabRuntimeTemplateIdleShutdownConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateIdleShutdownConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69dbb573a39a0c755db713cb006212c11e6375eec580e1c11bc92087cdde4550)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIdleTimeout")
    def reset_idle_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdleTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="idleTimeoutInput")
    def idle_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idleTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="idleTimeout")
    def idle_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idleTimeout"))

    @idle_timeout.setter
    def idle_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b0cbd2642ef9514fbb0ac0b6467625fbdfb0222ba09bc2ed4144a837ff533ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleColabRuntimeTemplateIdleShutdownConfig]:
        return typing.cast(typing.Optional[GoogleColabRuntimeTemplateIdleShutdownConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleColabRuntimeTemplateIdleShutdownConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dfa4420273fedf05df18725589f650a223d6852187e6ce519f1a86775dafc10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateMachineSpec",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_count": "acceleratorCount",
        "accelerator_type": "acceleratorType",
        "machine_type": "machineType",
    },
)
class GoogleColabRuntimeTemplateMachineSpec:
    def __init__(
        self,
        *,
        accelerator_count: typing.Optional[jsii.Number] = None,
        accelerator_type: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accelerator_count: The number of accelerators used by the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#accelerator_count GoogleColabRuntimeTemplate#accelerator_count}
        :param accelerator_type: The type of hardware accelerator used by the runtime. If specified, acceleratorCount must also be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#accelerator_type GoogleColabRuntimeTemplate#accelerator_type}
        :param machine_type: The Compute Engine machine type selected for the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#machine_type GoogleColabRuntimeTemplate#machine_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63d861a93bac1e7c560746e19123cc144e127b23f665492c826a23f6ee8648e9)
            check_type(argname="argument accelerator_count", value=accelerator_count, expected_type=type_hints["accelerator_count"])
            check_type(argname="argument accelerator_type", value=accelerator_type, expected_type=type_hints["accelerator_type"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerator_count is not None:
            self._values["accelerator_count"] = accelerator_count
        if accelerator_type is not None:
            self._values["accelerator_type"] = accelerator_type
        if machine_type is not None:
            self._values["machine_type"] = machine_type

    @builtins.property
    def accelerator_count(self) -> typing.Optional[jsii.Number]:
        '''The number of accelerators used by the runtime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#accelerator_count GoogleColabRuntimeTemplate#accelerator_count}
        '''
        result = self._values.get("accelerator_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def accelerator_type(self) -> typing.Optional[builtins.str]:
        '''The type of hardware accelerator used by the runtime. If specified, acceleratorCount must also be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#accelerator_type GoogleColabRuntimeTemplate#accelerator_type}
        '''
        result = self._values.get("accelerator_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine machine type selected for the runtime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#machine_type GoogleColabRuntimeTemplate#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleColabRuntimeTemplateMachineSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleColabRuntimeTemplateMachineSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateMachineSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a0cf00192ba0ac5e8ffd3c9add9f7321743e897ee1ec317ee1fcc230f5b6060)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAcceleratorCount")
    def reset_accelerator_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorCount", []))

    @jsii.member(jsii_name="resetAcceleratorType")
    def reset_accelerator_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorType", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @builtins.property
    @jsii.member(jsii_name="acceleratorCountInput")
    def accelerator_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "acceleratorCountInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTypeInput")
    def accelerator_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceleratorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorCount")
    def accelerator_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "acceleratorCount"))

    @accelerator_count.setter
    def accelerator_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a90351a637424d6a6a7dcd0ae10547a93a6cbd360196b9862f0e068bfbfa39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70761ec794248103455422ba5b9dba3f717225b1b2282c1c6fc242faeda3ef37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6f23528f882c9c121062512a82db15a6f930b13a2dc317b55d22a76e0975017)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleColabRuntimeTemplateMachineSpec]:
        return typing.cast(typing.Optional[GoogleColabRuntimeTemplateMachineSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleColabRuntimeTemplateMachineSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75173316c9780e8c8bab456dcad1a491e6dd6ca423523a19de8086ac8ebe0276)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateNetworkSpec",
    jsii_struct_bases=[],
    name_mapping={
        "enable_internet_access": "enableInternetAccess",
        "network": "network",
        "subnetwork": "subnetwork",
    },
)
class GoogleColabRuntimeTemplateNetworkSpec:
    def __init__(
        self,
        *,
        enable_internet_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enable_internet_access: Enable public internet access for the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#enable_internet_access GoogleColabRuntimeTemplate#enable_internet_access}
        :param network: The name of the VPC that this runtime is in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#network GoogleColabRuntimeTemplate#network}
        :param subnetwork: The name of the subnetwork that this runtime is in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#subnetwork GoogleColabRuntimeTemplate#subnetwork}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0894e66d527a8ee9f89427a1901a00350a5df7c4a73fd63899b79831250eb0b8)
            check_type(argname="argument enable_internet_access", value=enable_internet_access, expected_type=type_hints["enable_internet_access"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument subnetwork", value=subnetwork, expected_type=type_hints["subnetwork"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_internet_access is not None:
            self._values["enable_internet_access"] = enable_internet_access
        if network is not None:
            self._values["network"] = network
        if subnetwork is not None:
            self._values["subnetwork"] = subnetwork

    @builtins.property
    def enable_internet_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable public internet access for the runtime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#enable_internet_access GoogleColabRuntimeTemplate#enable_internet_access}
        '''
        result = self._values.get("enable_internet_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The name of the VPC that this runtime is in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#network GoogleColabRuntimeTemplate#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''The name of the subnetwork that this runtime is in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#subnetwork GoogleColabRuntimeTemplate#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleColabRuntimeTemplateNetworkSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleColabRuntimeTemplateNetworkSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateNetworkSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2af09204c61c686826b0e209125f4af87aff08be7555f48872c9e6d6ec25da1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableInternetAccess")
    def reset_enable_internet_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableInternetAccess", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetSubnetwork")
    def reset_subnetwork(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetwork", []))

    @builtins.property
    @jsii.member(jsii_name="enableInternetAccessInput")
    def enable_internet_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableInternetAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkInput")
    def subnetwork_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="enableInternetAccess")
    def enable_internet_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableInternetAccess"))

    @enable_internet_access.setter
    def enable_internet_access(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdfeaabc6d5da40bcd30169532ed3e770004798e1e3446aef48dd7fb72241b85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableInternetAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f6384ff0ec2e225108e18b042c87eec339d288f9a00045e0b6d44ed29be8716)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a9c7de4d761ba2d0ee04da3aff6acfe29bac0b609a0125636d1747091df67de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleColabRuntimeTemplateNetworkSpec]:
        return typing.cast(typing.Optional[GoogleColabRuntimeTemplateNetworkSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleColabRuntimeTemplateNetworkSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6908d3d5135336f5114e1560c9f012705c24ef64faff2d73fc80d102e3b36bf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateShieldedVmConfig",
    jsii_struct_bases=[],
    name_mapping={"enable_secure_boot": "enableSecureBoot"},
)
class GoogleColabRuntimeTemplateShieldedVmConfig:
    def __init__(
        self,
        *,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_secure_boot: Enables secure boot for the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#enable_secure_boot GoogleColabRuntimeTemplate#enable_secure_boot}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__562bc4d5e023f88a906b3e6bf4d5ad8a713e68c9a340bf23b19a1e344f79b6b7)
            check_type(argname="argument enable_secure_boot", value=enable_secure_boot, expected_type=type_hints["enable_secure_boot"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_secure_boot is not None:
            self._values["enable_secure_boot"] = enable_secure_boot

    @builtins.property
    def enable_secure_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables secure boot for the runtime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#enable_secure_boot GoogleColabRuntimeTemplate#enable_secure_boot}
        '''
        result = self._values.get("enable_secure_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleColabRuntimeTemplateShieldedVmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleColabRuntimeTemplateShieldedVmConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateShieldedVmConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a146246000013d2d033d35fa2a4e2501568e87355b9d4ce83594341d6b689165)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableSecureBoot")
    def reset_enable_secure_boot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSecureBoot", []))

    @builtins.property
    @jsii.member(jsii_name="enableSecureBootInput")
    def enable_secure_boot_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSecureBootInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__beeb417f278293ffd80956e07708af5730325b0b311fcc418b33046ac1076933)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSecureBoot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleColabRuntimeTemplateShieldedVmConfig]:
        return typing.cast(typing.Optional[GoogleColabRuntimeTemplateShieldedVmConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleColabRuntimeTemplateShieldedVmConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d777a6307f3ac35b3e5fe3908f330d2efeead8d9365e3080c846cc7afbf9b4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateSoftwareConfig",
    jsii_struct_bases=[],
    name_mapping={
        "env": "env",
        "post_startup_script_config": "postStartupScriptConfig",
    },
)
class GoogleColabRuntimeTemplateSoftwareConfig:
    def __init__(
        self,
        *,
        env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleColabRuntimeTemplateSoftwareConfigEnv", typing.Dict[builtins.str, typing.Any]]]]] = None,
        post_startup_script_config: typing.Optional[typing.Union["GoogleColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param env: env block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#env GoogleColabRuntimeTemplate#env}
        :param post_startup_script_config: post_startup_script_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#post_startup_script_config GoogleColabRuntimeTemplate#post_startup_script_config}
        '''
        if isinstance(post_startup_script_config, dict):
            post_startup_script_config = GoogleColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig(**post_startup_script_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd561d96f908887bd9fcd2bb08b7be59eb045cfca2fb727a2d900c5a8a34515)
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument post_startup_script_config", value=post_startup_script_config, expected_type=type_hints["post_startup_script_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if env is not None:
            self._values["env"] = env
        if post_startup_script_config is not None:
            self._values["post_startup_script_config"] = post_startup_script_config

    @builtins.property
    def env(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleColabRuntimeTemplateSoftwareConfigEnv"]]]:
        '''env block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#env GoogleColabRuntimeTemplate#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleColabRuntimeTemplateSoftwareConfigEnv"]]], result)

    @builtins.property
    def post_startup_script_config(
        self,
    ) -> typing.Optional["GoogleColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig"]:
        '''post_startup_script_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#post_startup_script_config GoogleColabRuntimeTemplate#post_startup_script_config}
        '''
        result = self._values.get("post_startup_script_config")
        return typing.cast(typing.Optional["GoogleColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleColabRuntimeTemplateSoftwareConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateSoftwareConfigEnv",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class GoogleColabRuntimeTemplateSoftwareConfigEnv:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the environment variable. Must be a valid C identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#name GoogleColabRuntimeTemplate#name}
        :param value: Variables that reference a $(VAR_NAME) are expanded using the previous defined environment variables in the container and any service environment variables. If a variable cannot be resolved, the reference in the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, regardless of whether the variable exists or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#value GoogleColabRuntimeTemplate#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba054350738904dd6c1c82181901f1f8b4b9a53897e8a737b2df6751f2e31f82)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the environment variable. Must be a valid C identifier.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#name GoogleColabRuntimeTemplate#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Variables that reference a $(VAR_NAME) are expanded using the previous defined environment variables in the container and any service environment variables.

        If a variable cannot be resolved, the reference in the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, regardless of whether the variable exists or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#value GoogleColabRuntimeTemplate#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleColabRuntimeTemplateSoftwareConfigEnv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleColabRuntimeTemplateSoftwareConfigEnvList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateSoftwareConfigEnvList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9ac6aa84d9d6e14979512a9a6b9bf14306ca1ada08582f1949fcaa4a927ecf1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleColabRuntimeTemplateSoftwareConfigEnvOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__759ed847bb78a63363040f2cd71d69098800d1558f79e9622ba0bb814fcd0830)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleColabRuntimeTemplateSoftwareConfigEnvOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__194dc315966d9960559879744adc9fd013567bf88075020eced835d5847a5632)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6bb1bc0475aa07e24455374cd731ad5905cd28987e8f7ac225afae73bb76815)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3e1532218ae18c77ebe9335617949d55123cb89fac30e0786ae1e1f38749d89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleColabRuntimeTemplateSoftwareConfigEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleColabRuntimeTemplateSoftwareConfigEnv]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleColabRuntimeTemplateSoftwareConfigEnv]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc93e70b53df856d059185ad411b784bbb6ce080543291c022b29959ba057984)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleColabRuntimeTemplateSoftwareConfigEnvOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateSoftwareConfigEnvOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c52ba8f80553e8cf06a25e9bdda622e5b6c20b749c06f2f895dd66eea8ec1c66)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02c3996b8e0c2c4b5b905d475c31d8b4eb87ee4b933051c60416ed142f3c7b31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8effe672f2a12f68e32028eae227dc12c06b1b9e2e7ebf5e839402130887af49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleColabRuntimeTemplateSoftwareConfigEnv]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleColabRuntimeTemplateSoftwareConfigEnv]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleColabRuntimeTemplateSoftwareConfigEnv]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55491e69feb84e02368f855af54a26c41af9a1cb3238546702ae4a121f722d7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleColabRuntimeTemplateSoftwareConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateSoftwareConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f014a4bdf7e60f91f0b36d378d34c9084776f3cb6019937e1c02e135cba14f22)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEnv")
    def put_env(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleColabRuntimeTemplateSoftwareConfigEnv, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c655c91090a408d86a9bf04cb6be29f062bfb9ac450f2dc6d1d05e5f83d923a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnv", [value]))

    @jsii.member(jsii_name="putPostStartupScriptConfig")
    def put_post_startup_script_config(
        self,
        *,
        post_startup_script: typing.Optional[builtins.str] = None,
        post_startup_script_behavior: typing.Optional[builtins.str] = None,
        post_startup_script_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param post_startup_script: Post startup script to run after runtime is started. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#post_startup_script GoogleColabRuntimeTemplate#post_startup_script}
        :param post_startup_script_behavior: Post startup script behavior that defines download and execution behavior. Possible values: ["RUN_ONCE", "RUN_EVERY_START", "DOWNLOAD_AND_RUN_EVERY_START"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#post_startup_script_behavior GoogleColabRuntimeTemplate#post_startup_script_behavior}
        :param post_startup_script_url: Post startup script url to download. Example: https://bucket/script.sh. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#post_startup_script_url GoogleColabRuntimeTemplate#post_startup_script_url}
        '''
        value = GoogleColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig(
            post_startup_script=post_startup_script,
            post_startup_script_behavior=post_startup_script_behavior,
            post_startup_script_url=post_startup_script_url,
        )

        return typing.cast(None, jsii.invoke(self, "putPostStartupScriptConfig", [value]))

    @jsii.member(jsii_name="resetEnv")
    def reset_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnv", []))

    @jsii.member(jsii_name="resetPostStartupScriptConfig")
    def reset_post_startup_script_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostStartupScriptConfig", []))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> GoogleColabRuntimeTemplateSoftwareConfigEnvList:
        return typing.cast(GoogleColabRuntimeTemplateSoftwareConfigEnvList, jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="postStartupScriptConfig")
    def post_startup_script_config(
        self,
    ) -> "GoogleColabRuntimeTemplateSoftwareConfigPostStartupScriptConfigOutputReference":
        return typing.cast("GoogleColabRuntimeTemplateSoftwareConfigPostStartupScriptConfigOutputReference", jsii.get(self, "postStartupScriptConfig"))

    @builtins.property
    @jsii.member(jsii_name="envInput")
    def env_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleColabRuntimeTemplateSoftwareConfigEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleColabRuntimeTemplateSoftwareConfigEnv]]], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="postStartupScriptConfigInput")
    def post_startup_script_config_input(
        self,
    ) -> typing.Optional["GoogleColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig"]:
        return typing.cast(typing.Optional["GoogleColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig"], jsii.get(self, "postStartupScriptConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleColabRuntimeTemplateSoftwareConfig]:
        return typing.cast(typing.Optional[GoogleColabRuntimeTemplateSoftwareConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleColabRuntimeTemplateSoftwareConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e1af7726f6e7a607f82de01e1d22c656b1db8a4b3cddb96042f4e1a8ab19028)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig",
    jsii_struct_bases=[],
    name_mapping={
        "post_startup_script": "postStartupScript",
        "post_startup_script_behavior": "postStartupScriptBehavior",
        "post_startup_script_url": "postStartupScriptUrl",
    },
)
class GoogleColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig:
    def __init__(
        self,
        *,
        post_startup_script: typing.Optional[builtins.str] = None,
        post_startup_script_behavior: typing.Optional[builtins.str] = None,
        post_startup_script_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param post_startup_script: Post startup script to run after runtime is started. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#post_startup_script GoogleColabRuntimeTemplate#post_startup_script}
        :param post_startup_script_behavior: Post startup script behavior that defines download and execution behavior. Possible values: ["RUN_ONCE", "RUN_EVERY_START", "DOWNLOAD_AND_RUN_EVERY_START"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#post_startup_script_behavior GoogleColabRuntimeTemplate#post_startup_script_behavior}
        :param post_startup_script_url: Post startup script url to download. Example: https://bucket/script.sh. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#post_startup_script_url GoogleColabRuntimeTemplate#post_startup_script_url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84c6ddb22780457811414827e9413661d1e7a18723d6f78264b6618eae666a96)
            check_type(argname="argument post_startup_script", value=post_startup_script, expected_type=type_hints["post_startup_script"])
            check_type(argname="argument post_startup_script_behavior", value=post_startup_script_behavior, expected_type=type_hints["post_startup_script_behavior"])
            check_type(argname="argument post_startup_script_url", value=post_startup_script_url, expected_type=type_hints["post_startup_script_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if post_startup_script is not None:
            self._values["post_startup_script"] = post_startup_script
        if post_startup_script_behavior is not None:
            self._values["post_startup_script_behavior"] = post_startup_script_behavior
        if post_startup_script_url is not None:
            self._values["post_startup_script_url"] = post_startup_script_url

    @builtins.property
    def post_startup_script(self) -> typing.Optional[builtins.str]:
        '''Post startup script to run after runtime is started.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#post_startup_script GoogleColabRuntimeTemplate#post_startup_script}
        '''
        result = self._values.get("post_startup_script")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_startup_script_behavior(self) -> typing.Optional[builtins.str]:
        '''Post startup script behavior that defines download and execution behavior. Possible values: ["RUN_ONCE", "RUN_EVERY_START", "DOWNLOAD_AND_RUN_EVERY_START"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#post_startup_script_behavior GoogleColabRuntimeTemplate#post_startup_script_behavior}
        '''
        result = self._values.get("post_startup_script_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_startup_script_url(self) -> typing.Optional[builtins.str]:
        '''Post startup script url to download. Example: https://bucket/script.sh.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#post_startup_script_url GoogleColabRuntimeTemplate#post_startup_script_url}
        '''
        result = self._values.get("post_startup_script_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleColabRuntimeTemplateSoftwareConfigPostStartupScriptConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateSoftwareConfigPostStartupScriptConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21f294d765ba4d3ad26f343f505a6725be1e59872e67947a9c0b52445a79eba7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPostStartupScript")
    def reset_post_startup_script(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostStartupScript", []))

    @jsii.member(jsii_name="resetPostStartupScriptBehavior")
    def reset_post_startup_script_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostStartupScriptBehavior", []))

    @jsii.member(jsii_name="resetPostStartupScriptUrl")
    def reset_post_startup_script_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostStartupScriptUrl", []))

    @builtins.property
    @jsii.member(jsii_name="postStartupScriptBehaviorInput")
    def post_startup_script_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postStartupScriptBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="postStartupScriptInput")
    def post_startup_script_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postStartupScriptInput"))

    @builtins.property
    @jsii.member(jsii_name="postStartupScriptUrlInput")
    def post_startup_script_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postStartupScriptUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="postStartupScript")
    def post_startup_script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postStartupScript"))

    @post_startup_script.setter
    def post_startup_script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f05ee34bba70b8d87a58f0c02e6add69675b82616670fb154a38a3ee0842eb80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postStartupScript", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postStartupScriptBehavior")
    def post_startup_script_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postStartupScriptBehavior"))

    @post_startup_script_behavior.setter
    def post_startup_script_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa5b42bf840f904d39aa2d1d62702c8cec96178b5d25d42fa4a7ad006551fc12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postStartupScriptBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postStartupScriptUrl")
    def post_startup_script_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postStartupScriptUrl"))

    @post_startup_script_url.setter
    def post_startup_script_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a00061966f5a04c8022d1f03b1eac2a7a1b0c797e9fd2402743e312761030663)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postStartupScriptUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig]:
        return typing.cast(typing.Optional[GoogleColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e65bcdcec18a344ed8eb35866661a176ff5d8b48a63d36ccaeefbd0450793688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleColabRuntimeTemplateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#create GoogleColabRuntimeTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#delete GoogleColabRuntimeTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#update GoogleColabRuntimeTemplate#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__329dfeca61766fe090791b1f19b3b8f6b064567e08dfff45056153e27abc0591)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#create GoogleColabRuntimeTemplate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#delete GoogleColabRuntimeTemplate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_runtime_template#update GoogleColabRuntimeTemplate#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleColabRuntimeTemplateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleColabRuntimeTemplateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabRuntimeTemplate.GoogleColabRuntimeTemplateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__193b4794d3d54246e1c52683f21263f8b3b5886491264e0987ac2f9dd5abe6ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92168f19917fb84591c2c05602c5e3aa5ab80699037c96b65a7ec3304f057767)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__666dc6cdc19ba4855c55abef9a08deb79f1ebe7c26f64d82ce9d104e0a863cf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb82b9542a90531d4d743c536e73917580ed8c358bf5c4aebe49c719aedbaa9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleColabRuntimeTemplateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleColabRuntimeTemplateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleColabRuntimeTemplateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0b9dabafa4eedf972353c9677d07a4fdd51e0145b9dd33845494ebeaba03a83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleColabRuntimeTemplate",
    "GoogleColabRuntimeTemplateConfig",
    "GoogleColabRuntimeTemplateDataPersistentDiskSpec",
    "GoogleColabRuntimeTemplateDataPersistentDiskSpecOutputReference",
    "GoogleColabRuntimeTemplateEncryptionSpec",
    "GoogleColabRuntimeTemplateEncryptionSpecOutputReference",
    "GoogleColabRuntimeTemplateEucConfig",
    "GoogleColabRuntimeTemplateEucConfigOutputReference",
    "GoogleColabRuntimeTemplateIdleShutdownConfig",
    "GoogleColabRuntimeTemplateIdleShutdownConfigOutputReference",
    "GoogleColabRuntimeTemplateMachineSpec",
    "GoogleColabRuntimeTemplateMachineSpecOutputReference",
    "GoogleColabRuntimeTemplateNetworkSpec",
    "GoogleColabRuntimeTemplateNetworkSpecOutputReference",
    "GoogleColabRuntimeTemplateShieldedVmConfig",
    "GoogleColabRuntimeTemplateShieldedVmConfigOutputReference",
    "GoogleColabRuntimeTemplateSoftwareConfig",
    "GoogleColabRuntimeTemplateSoftwareConfigEnv",
    "GoogleColabRuntimeTemplateSoftwareConfigEnvList",
    "GoogleColabRuntimeTemplateSoftwareConfigEnvOutputReference",
    "GoogleColabRuntimeTemplateSoftwareConfigOutputReference",
    "GoogleColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig",
    "GoogleColabRuntimeTemplateSoftwareConfigPostStartupScriptConfigOutputReference",
    "GoogleColabRuntimeTemplateTimeouts",
    "GoogleColabRuntimeTemplateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b23437dde98e2b405653913408cd74d96a730c99339a5abbd5b2667cd2ad96d1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    location: builtins.str,
    data_persistent_disk_spec: typing.Optional[typing.Union[GoogleColabRuntimeTemplateDataPersistentDiskSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    encryption_spec: typing.Optional[typing.Union[GoogleColabRuntimeTemplateEncryptionSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    euc_config: typing.Optional[typing.Union[GoogleColabRuntimeTemplateEucConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    idle_shutdown_config: typing.Optional[typing.Union[GoogleColabRuntimeTemplateIdleShutdownConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    machine_spec: typing.Optional[typing.Union[GoogleColabRuntimeTemplateMachineSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    network_spec: typing.Optional[typing.Union[GoogleColabRuntimeTemplateNetworkSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    shielded_vm_config: typing.Optional[typing.Union[GoogleColabRuntimeTemplateShieldedVmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    software_config: typing.Optional[typing.Union[GoogleColabRuntimeTemplateSoftwareConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleColabRuntimeTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__35425cbffdc48d6d02e75703c1e691d7fec3d8e6fc1d1835229f84bb27c73251(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d1713765eafd90a098fc2cbd9341386b000781e36aab554f0d256afa9bfea6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__894ae7ac3d24143680cdfca8933438cb721d167dd986d52ea0fa648f3c893077(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34f912627d67359b5c335b1384c9c846f94d0d79f9093e8837b91fb9566eef66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f506d06982b0dbc55a64fde8efdeea4242ea979cf5b076326525e1965ca55c0f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5dd950ba3bb2bc03a320c7663c9bce2b19fb4c03f16f8f2b25084e1c23d07f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aae665077d911f30fd314ede1fb2d3c14982a0ee8203f9bbddefe7ebe37dc91c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d7aa006ea23e2e3317153c7fccf0d919dfee50dca1edaf06c08838e766fdd5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b3dc61d198d1534113199675580030ceca6e2bf496089552660c485af3760b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf9a2aa8a8f6b65dfd6534e9b82c937786cd83349139a4455f30c5e607078d1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    location: builtins.str,
    data_persistent_disk_spec: typing.Optional[typing.Union[GoogleColabRuntimeTemplateDataPersistentDiskSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    encryption_spec: typing.Optional[typing.Union[GoogleColabRuntimeTemplateEncryptionSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    euc_config: typing.Optional[typing.Union[GoogleColabRuntimeTemplateEucConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    idle_shutdown_config: typing.Optional[typing.Union[GoogleColabRuntimeTemplateIdleShutdownConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    machine_spec: typing.Optional[typing.Union[GoogleColabRuntimeTemplateMachineSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    network_spec: typing.Optional[typing.Union[GoogleColabRuntimeTemplateNetworkSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    shielded_vm_config: typing.Optional[typing.Union[GoogleColabRuntimeTemplateShieldedVmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    software_config: typing.Optional[typing.Union[GoogleColabRuntimeTemplateSoftwareConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleColabRuntimeTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ab1b8ebc82db896ce9db108ccb68c632bcff1c87cebba41c3e8b6d054af6ed2(
    *,
    disk_size_gb: typing.Optional[builtins.str] = None,
    disk_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b178e27c3eaed514d391b279dd2a3e814c3f8c1e16df0c5729cb4e4e73cfe2ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b8eb0f4ab96ef7913e48996e70218eda85813e6639ce162383b0fa0535d1ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__686eb456fa33dc5e49f518dbaacf567bdee86349bdf00b2414cd63900c9c53a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d008a87fdf06a1364596abc4aff0e0c6757a1c39fad084593223dea644e4f1(
    value: typing.Optional[GoogleColabRuntimeTemplateDataPersistentDiskSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec6e47cbddef9cdb802b1c5d3915a4e34430961f7367a1d093bf7f5ec17cdc7(
    *,
    kms_key_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf2cf77ceb60c63c7e89e87cde66f5f0de8ed21f1895a04b2ebf59390509d3b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a268593a8d6df549d82434de193fbb7a888b1e2265bceb9a0a2de4372ce0826(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6911dbedde4a0b912e093b77e425a74736533ae681dd0971ad44eac08d80426(
    value: typing.Optional[GoogleColabRuntimeTemplateEncryptionSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e88f12713aa5df05fc23afe9259aa1a4aa1862e0bc6c2df021f80040c7dbd2ac(
    *,
    euc_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f1fe5b5dd194ad36c8ae7ef3f4aadc3d4c7c28db46822723f4518c424f3c0d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514496294d0d8665a5ca904c377bfc2615125a2f60781f32b62354f71beb459b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__412883a8c2a3cf786de023d8249df9aac4f00e4287bdf0eaf716c525449731be(
    value: typing.Optional[GoogleColabRuntimeTemplateEucConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f33a07f139d045cc3d5a097d6aace69a1eaa3cc4301ab773915361c0a5dcd664(
    *,
    idle_timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69dbb573a39a0c755db713cb006212c11e6375eec580e1c11bc92087cdde4550(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b0cbd2642ef9514fbb0ac0b6467625fbdfb0222ba09bc2ed4144a837ff533ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dfa4420273fedf05df18725589f650a223d6852187e6ce519f1a86775dafc10(
    value: typing.Optional[GoogleColabRuntimeTemplateIdleShutdownConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63d861a93bac1e7c560746e19123cc144e127b23f665492c826a23f6ee8648e9(
    *,
    accelerator_count: typing.Optional[jsii.Number] = None,
    accelerator_type: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a0cf00192ba0ac5e8ffd3c9add9f7321743e897ee1ec317ee1fcc230f5b6060(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a90351a637424d6a6a7dcd0ae10547a93a6cbd360196b9862f0e068bfbfa39(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70761ec794248103455422ba5b9dba3f717225b1b2282c1c6fc242faeda3ef37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f23528f882c9c121062512a82db15a6f930b13a2dc317b55d22a76e0975017(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75173316c9780e8c8bab456dcad1a491e6dd6ca423523a19de8086ac8ebe0276(
    value: typing.Optional[GoogleColabRuntimeTemplateMachineSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0894e66d527a8ee9f89427a1901a00350a5df7c4a73fd63899b79831250eb0b8(
    *,
    enable_internet_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    network: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2af09204c61c686826b0e209125f4af87aff08be7555f48872c9e6d6ec25da1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdfeaabc6d5da40bcd30169532ed3e770004798e1e3446aef48dd7fb72241b85(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6384ff0ec2e225108e18b042c87eec339d288f9a00045e0b6d44ed29be8716(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a9c7de4d761ba2d0ee04da3aff6acfe29bac0b609a0125636d1747091df67de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6908d3d5135336f5114e1560c9f012705c24ef64faff2d73fc80d102e3b36bf2(
    value: typing.Optional[GoogleColabRuntimeTemplateNetworkSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__562bc4d5e023f88a906b3e6bf4d5ad8a713e68c9a340bf23b19a1e344f79b6b7(
    *,
    enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a146246000013d2d033d35fa2a4e2501568e87355b9d4ce83594341d6b689165(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beeb417f278293ffd80956e07708af5730325b0b311fcc418b33046ac1076933(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d777a6307f3ac35b3e5fe3908f330d2efeead8d9365e3080c846cc7afbf9b4c(
    value: typing.Optional[GoogleColabRuntimeTemplateShieldedVmConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd561d96f908887bd9fcd2bb08b7be59eb045cfca2fb727a2d900c5a8a34515(
    *,
    env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleColabRuntimeTemplateSoftwareConfigEnv, typing.Dict[builtins.str, typing.Any]]]]] = None,
    post_startup_script_config: typing.Optional[typing.Union[GoogleColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba054350738904dd6c1c82181901f1f8b4b9a53897e8a737b2df6751f2e31f82(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ac6aa84d9d6e14979512a9a6b9bf14306ca1ada08582f1949fcaa4a927ecf1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__759ed847bb78a63363040f2cd71d69098800d1558f79e9622ba0bb814fcd0830(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__194dc315966d9960559879744adc9fd013567bf88075020eced835d5847a5632(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6bb1bc0475aa07e24455374cd731ad5905cd28987e8f7ac225afae73bb76815(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e1532218ae18c77ebe9335617949d55123cb89fac30e0786ae1e1f38749d89(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc93e70b53df856d059185ad411b784bbb6ce080543291c022b29959ba057984(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleColabRuntimeTemplateSoftwareConfigEnv]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52ba8f80553e8cf06a25e9bdda622e5b6c20b749c06f2f895dd66eea8ec1c66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c3996b8e0c2c4b5b905d475c31d8b4eb87ee4b933051c60416ed142f3c7b31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8effe672f2a12f68e32028eae227dc12c06b1b9e2e7ebf5e839402130887af49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55491e69feb84e02368f855af54a26c41af9a1cb3238546702ae4a121f722d7b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleColabRuntimeTemplateSoftwareConfigEnv]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f014a4bdf7e60f91f0b36d378d34c9084776f3cb6019937e1c02e135cba14f22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c655c91090a408d86a9bf04cb6be29f062bfb9ac450f2dc6d1d05e5f83d923a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleColabRuntimeTemplateSoftwareConfigEnv, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e1af7726f6e7a607f82de01e1d22c656b1db8a4b3cddb96042f4e1a8ab19028(
    value: typing.Optional[GoogleColabRuntimeTemplateSoftwareConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84c6ddb22780457811414827e9413661d1e7a18723d6f78264b6618eae666a96(
    *,
    post_startup_script: typing.Optional[builtins.str] = None,
    post_startup_script_behavior: typing.Optional[builtins.str] = None,
    post_startup_script_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21f294d765ba4d3ad26f343f505a6725be1e59872e67947a9c0b52445a79eba7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f05ee34bba70b8d87a58f0c02e6add69675b82616670fb154a38a3ee0842eb80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa5b42bf840f904d39aa2d1d62702c8cec96178b5d25d42fa4a7ad006551fc12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a00061966f5a04c8022d1f03b1eac2a7a1b0c797e9fd2402743e312761030663(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e65bcdcec18a344ed8eb35866661a176ff5d8b48a63d36ccaeefbd0450793688(
    value: typing.Optional[GoogleColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__329dfeca61766fe090791b1f19b3b8f6b064567e08dfff45056153e27abc0591(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__193b4794d3d54246e1c52683f21263f8b3b5886491264e0987ac2f9dd5abe6ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92168f19917fb84591c2c05602c5e3aa5ab80699037c96b65a7ec3304f057767(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__666dc6cdc19ba4855c55abef9a08deb79f1ebe7c26f64d82ce9d104e0a863cf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb82b9542a90531d4d743c536e73917580ed8c358bf5c4aebe49c719aedbaa9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0b9dabafa4eedf972353c9677d07a4fdd51e0145b9dd33845494ebeaba03a83(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleColabRuntimeTemplateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
