r'''
# `google_colab_runtime_template`

Refer to the Terraform Registry for docs: [`google_colab_runtime_template`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template).
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


class ColabRuntimeTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template google_colab_runtime_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        location: builtins.str,
        data_persistent_disk_spec: typing.Optional[typing.Union["ColabRuntimeTemplateDataPersistentDiskSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_spec: typing.Optional[typing.Union["ColabRuntimeTemplateEncryptionSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        euc_config: typing.Optional[typing.Union["ColabRuntimeTemplateEucConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        idle_shutdown_config: typing.Optional[typing.Union["ColabRuntimeTemplateIdleShutdownConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        machine_spec: typing.Optional[typing.Union["ColabRuntimeTemplateMachineSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        network_spec: typing.Optional[typing.Union["ColabRuntimeTemplateNetworkSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        shielded_vm_config: typing.Optional[typing.Union["ColabRuntimeTemplateShieldedVmConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        software_config: typing.Optional[typing.Union["ColabRuntimeTemplateSoftwareConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ColabRuntimeTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template google_colab_runtime_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: Required. The display name of the Runtime Template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#display_name ColabRuntimeTemplate#display_name}
        :param location: The location for the resource: https://cloud.google.com/colab/docs/locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#location ColabRuntimeTemplate#location}
        :param data_persistent_disk_spec: data_persistent_disk_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#data_persistent_disk_spec ColabRuntimeTemplate#data_persistent_disk_spec}
        :param description: The description of the Runtime Template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#description ColabRuntimeTemplate#description}
        :param encryption_spec: encryption_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#encryption_spec ColabRuntimeTemplate#encryption_spec}
        :param euc_config: euc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#euc_config ColabRuntimeTemplate#euc_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#id ColabRuntimeTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param idle_shutdown_config: idle_shutdown_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#idle_shutdown_config ColabRuntimeTemplate#idle_shutdown_config}
        :param labels: Labels to identify and group the runtime template. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#labels ColabRuntimeTemplate#labels}
        :param machine_spec: machine_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#machine_spec ColabRuntimeTemplate#machine_spec}
        :param name: The resource name of the Runtime Template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#name ColabRuntimeTemplate#name}
        :param network_spec: network_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#network_spec ColabRuntimeTemplate#network_spec}
        :param network_tags: Applies the given Compute Engine tags to the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#network_tags ColabRuntimeTemplate#network_tags}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#project ColabRuntimeTemplate#project}.
        :param shielded_vm_config: shielded_vm_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#shielded_vm_config ColabRuntimeTemplate#shielded_vm_config}
        :param software_config: software_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#software_config ColabRuntimeTemplate#software_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#timeouts ColabRuntimeTemplate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9db1219f73f879802a4e83b2caabbbf02a56fb89448dde71577cba37eee69ade)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ColabRuntimeTemplateConfig(
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
        '''Generates CDKTF code for importing a ColabRuntimeTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ColabRuntimeTemplate to import.
        :param import_from_id: The id of the existing ColabRuntimeTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ColabRuntimeTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76f8049ea0c90d22244a316c2b98ca7a21fb0232dcfce807bd59f1bb35eadcc6)
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
        :param disk_size_gb: The disk size of the runtime in GB. If specified, the diskType must also be specified. The minimum size is 10GB and the maximum is 65536GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#disk_size_gb ColabRuntimeTemplate#disk_size_gb}
        :param disk_type: The type of the persistent disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#disk_type ColabRuntimeTemplate#disk_type}
        '''
        value = ColabRuntimeTemplateDataPersistentDiskSpec(
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
        :param kms_key_name: The Cloud KMS encryption key (customer-managed encryption key) used to protect the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#kms_key_name ColabRuntimeTemplate#kms_key_name}
        '''
        value = ColabRuntimeTemplateEncryptionSpec(kms_key_name=kms_key_name)

        return typing.cast(None, jsii.invoke(self, "putEncryptionSpec", [value]))

    @jsii.member(jsii_name="putEucConfig")
    def put_euc_config(
        self,
        *,
        euc_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param euc_disabled: Disable end user credential access for the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#euc_disabled ColabRuntimeTemplate#euc_disabled}
        '''
        value = ColabRuntimeTemplateEucConfig(euc_disabled=euc_disabled)

        return typing.cast(None, jsii.invoke(self, "putEucConfig", [value]))

    @jsii.member(jsii_name="putIdleShutdownConfig")
    def put_idle_shutdown_config(
        self,
        *,
        idle_timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param idle_timeout: The duration after which the runtime is automatically shut down. An input of 0s disables the idle shutdown feature, and a valid range is [10m, 24h]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#idle_timeout ColabRuntimeTemplate#idle_timeout}
        '''
        value = ColabRuntimeTemplateIdleShutdownConfig(idle_timeout=idle_timeout)

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
        :param accelerator_count: The number of accelerators used by the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#accelerator_count ColabRuntimeTemplate#accelerator_count}
        :param accelerator_type: The type of hardware accelerator used by the runtime. If specified, acceleratorCount must also be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#accelerator_type ColabRuntimeTemplate#accelerator_type}
        :param machine_type: The Compute Engine machine type selected for the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#machine_type ColabRuntimeTemplate#machine_type}
        '''
        value = ColabRuntimeTemplateMachineSpec(
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
        :param enable_internet_access: Enable public internet access for the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#enable_internet_access ColabRuntimeTemplate#enable_internet_access}
        :param network: The name of the VPC that this runtime is in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#network ColabRuntimeTemplate#network}
        :param subnetwork: The name of the subnetwork that this runtime is in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#subnetwork ColabRuntimeTemplate#subnetwork}
        '''
        value = ColabRuntimeTemplateNetworkSpec(
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
        :param enable_secure_boot: Enables secure boot for the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#enable_secure_boot ColabRuntimeTemplate#enable_secure_boot}
        '''
        value = ColabRuntimeTemplateShieldedVmConfig(
            enable_secure_boot=enable_secure_boot
        )

        return typing.cast(None, jsii.invoke(self, "putShieldedVmConfig", [value]))

    @jsii.member(jsii_name="putSoftwareConfig")
    def put_software_config(
        self,
        *,
        env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ColabRuntimeTemplateSoftwareConfigEnv", typing.Dict[builtins.str, typing.Any]]]]] = None,
        post_startup_script_config: typing.Optional[typing.Union["ColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param env: env block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#env ColabRuntimeTemplate#env}
        :param post_startup_script_config: post_startup_script_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#post_startup_script_config ColabRuntimeTemplate#post_startup_script_config}
        '''
        value = ColabRuntimeTemplateSoftwareConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#create ColabRuntimeTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#delete ColabRuntimeTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#update ColabRuntimeTemplate#update}.
        '''
        value = ColabRuntimeTemplateTimeouts(
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
    ) -> "ColabRuntimeTemplateDataPersistentDiskSpecOutputReference":
        return typing.cast("ColabRuntimeTemplateDataPersistentDiskSpecOutputReference", jsii.get(self, "dataPersistentDiskSpec"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="encryptionSpec")
    def encryption_spec(self) -> "ColabRuntimeTemplateEncryptionSpecOutputReference":
        return typing.cast("ColabRuntimeTemplateEncryptionSpecOutputReference", jsii.get(self, "encryptionSpec"))

    @builtins.property
    @jsii.member(jsii_name="eucConfig")
    def euc_config(self) -> "ColabRuntimeTemplateEucConfigOutputReference":
        return typing.cast("ColabRuntimeTemplateEucConfigOutputReference", jsii.get(self, "eucConfig"))

    @builtins.property
    @jsii.member(jsii_name="idleShutdownConfig")
    def idle_shutdown_config(
        self,
    ) -> "ColabRuntimeTemplateIdleShutdownConfigOutputReference":
        return typing.cast("ColabRuntimeTemplateIdleShutdownConfigOutputReference", jsii.get(self, "idleShutdownConfig"))

    @builtins.property
    @jsii.member(jsii_name="machineSpec")
    def machine_spec(self) -> "ColabRuntimeTemplateMachineSpecOutputReference":
        return typing.cast("ColabRuntimeTemplateMachineSpecOutputReference", jsii.get(self, "machineSpec"))

    @builtins.property
    @jsii.member(jsii_name="networkSpec")
    def network_spec(self) -> "ColabRuntimeTemplateNetworkSpecOutputReference":
        return typing.cast("ColabRuntimeTemplateNetworkSpecOutputReference", jsii.get(self, "networkSpec"))

    @builtins.property
    @jsii.member(jsii_name="shieldedVmConfig")
    def shielded_vm_config(
        self,
    ) -> "ColabRuntimeTemplateShieldedVmConfigOutputReference":
        return typing.cast("ColabRuntimeTemplateShieldedVmConfigOutputReference", jsii.get(self, "shieldedVmConfig"))

    @builtins.property
    @jsii.member(jsii_name="softwareConfig")
    def software_config(self) -> "ColabRuntimeTemplateSoftwareConfigOutputReference":
        return typing.cast("ColabRuntimeTemplateSoftwareConfigOutputReference", jsii.get(self, "softwareConfig"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ColabRuntimeTemplateTimeoutsOutputReference":
        return typing.cast("ColabRuntimeTemplateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="dataPersistentDiskSpecInput")
    def data_persistent_disk_spec_input(
        self,
    ) -> typing.Optional["ColabRuntimeTemplateDataPersistentDiskSpec"]:
        return typing.cast(typing.Optional["ColabRuntimeTemplateDataPersistentDiskSpec"], jsii.get(self, "dataPersistentDiskSpecInput"))

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
    ) -> typing.Optional["ColabRuntimeTemplateEncryptionSpec"]:
        return typing.cast(typing.Optional["ColabRuntimeTemplateEncryptionSpec"], jsii.get(self, "encryptionSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="eucConfigInput")
    def euc_config_input(self) -> typing.Optional["ColabRuntimeTemplateEucConfig"]:
        return typing.cast(typing.Optional["ColabRuntimeTemplateEucConfig"], jsii.get(self, "eucConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="idleShutdownConfigInput")
    def idle_shutdown_config_input(
        self,
    ) -> typing.Optional["ColabRuntimeTemplateIdleShutdownConfig"]:
        return typing.cast(typing.Optional["ColabRuntimeTemplateIdleShutdownConfig"], jsii.get(self, "idleShutdownConfigInput"))

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
    def machine_spec_input(self) -> typing.Optional["ColabRuntimeTemplateMachineSpec"]:
        return typing.cast(typing.Optional["ColabRuntimeTemplateMachineSpec"], jsii.get(self, "machineSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkSpecInput")
    def network_spec_input(self) -> typing.Optional["ColabRuntimeTemplateNetworkSpec"]:
        return typing.cast(typing.Optional["ColabRuntimeTemplateNetworkSpec"], jsii.get(self, "networkSpecInput"))

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
    ) -> typing.Optional["ColabRuntimeTemplateShieldedVmConfig"]:
        return typing.cast(typing.Optional["ColabRuntimeTemplateShieldedVmConfig"], jsii.get(self, "shieldedVmConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="softwareConfigInput")
    def software_config_input(
        self,
    ) -> typing.Optional["ColabRuntimeTemplateSoftwareConfig"]:
        return typing.cast(typing.Optional["ColabRuntimeTemplateSoftwareConfig"], jsii.get(self, "softwareConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ColabRuntimeTemplateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ColabRuntimeTemplateTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cca38125e886fd78a2c422a4f686fb95a799e310da71a53d23a77e749e23ccd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5339ec2c16f020fe87cd3469465ffe5c1f667dc12a79be8dbb769ed7d8cd774)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9335e4ffa742c96f7e3ffde371bb992e269e627b5919032cb0d7eaa1d0a53f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c6f8f982928814e64b8af14f1c3845e0c63730b2e9dd5dbcd81a6d36035df4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b444f12639e26c53593a2c66ae6de726a8986d4d9035bd7edf744b63d7959a8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22e59ad14d5185d483d8999da525f63dd356577cefe9dee5a45068d7d60ae15f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkTags")
    def network_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkTags"))

    @network_tags.setter
    def network_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be618bd9a0302d9ad68327a3d3f5e8fc51eb6bf920ed6d9650e5f0dd319d5fd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eac57be85dbb76de326e78750f7da2484e1e68448c01aa0c4360893263037db3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateConfig",
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
class ColabRuntimeTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        data_persistent_disk_spec: typing.Optional[typing.Union["ColabRuntimeTemplateDataPersistentDiskSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_spec: typing.Optional[typing.Union["ColabRuntimeTemplateEncryptionSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        euc_config: typing.Optional[typing.Union["ColabRuntimeTemplateEucConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        idle_shutdown_config: typing.Optional[typing.Union["ColabRuntimeTemplateIdleShutdownConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        machine_spec: typing.Optional[typing.Union["ColabRuntimeTemplateMachineSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        network_spec: typing.Optional[typing.Union["ColabRuntimeTemplateNetworkSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        shielded_vm_config: typing.Optional[typing.Union["ColabRuntimeTemplateShieldedVmConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        software_config: typing.Optional[typing.Union["ColabRuntimeTemplateSoftwareConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ColabRuntimeTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: Required. The display name of the Runtime Template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#display_name ColabRuntimeTemplate#display_name}
        :param location: The location for the resource: https://cloud.google.com/colab/docs/locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#location ColabRuntimeTemplate#location}
        :param data_persistent_disk_spec: data_persistent_disk_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#data_persistent_disk_spec ColabRuntimeTemplate#data_persistent_disk_spec}
        :param description: The description of the Runtime Template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#description ColabRuntimeTemplate#description}
        :param encryption_spec: encryption_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#encryption_spec ColabRuntimeTemplate#encryption_spec}
        :param euc_config: euc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#euc_config ColabRuntimeTemplate#euc_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#id ColabRuntimeTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param idle_shutdown_config: idle_shutdown_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#idle_shutdown_config ColabRuntimeTemplate#idle_shutdown_config}
        :param labels: Labels to identify and group the runtime template. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#labels ColabRuntimeTemplate#labels}
        :param machine_spec: machine_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#machine_spec ColabRuntimeTemplate#machine_spec}
        :param name: The resource name of the Runtime Template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#name ColabRuntimeTemplate#name}
        :param network_spec: network_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#network_spec ColabRuntimeTemplate#network_spec}
        :param network_tags: Applies the given Compute Engine tags to the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#network_tags ColabRuntimeTemplate#network_tags}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#project ColabRuntimeTemplate#project}.
        :param shielded_vm_config: shielded_vm_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#shielded_vm_config ColabRuntimeTemplate#shielded_vm_config}
        :param software_config: software_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#software_config ColabRuntimeTemplate#software_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#timeouts ColabRuntimeTemplate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(data_persistent_disk_spec, dict):
            data_persistent_disk_spec = ColabRuntimeTemplateDataPersistentDiskSpec(**data_persistent_disk_spec)
        if isinstance(encryption_spec, dict):
            encryption_spec = ColabRuntimeTemplateEncryptionSpec(**encryption_spec)
        if isinstance(euc_config, dict):
            euc_config = ColabRuntimeTemplateEucConfig(**euc_config)
        if isinstance(idle_shutdown_config, dict):
            idle_shutdown_config = ColabRuntimeTemplateIdleShutdownConfig(**idle_shutdown_config)
        if isinstance(machine_spec, dict):
            machine_spec = ColabRuntimeTemplateMachineSpec(**machine_spec)
        if isinstance(network_spec, dict):
            network_spec = ColabRuntimeTemplateNetworkSpec(**network_spec)
        if isinstance(shielded_vm_config, dict):
            shielded_vm_config = ColabRuntimeTemplateShieldedVmConfig(**shielded_vm_config)
        if isinstance(software_config, dict):
            software_config = ColabRuntimeTemplateSoftwareConfig(**software_config)
        if isinstance(timeouts, dict):
            timeouts = ColabRuntimeTemplateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33f28aeb359535f0a6caf987afad5b808f7b572cfd333424162153dc9bedca21)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#display_name ColabRuntimeTemplate#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource: https://cloud.google.com/colab/docs/locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#location ColabRuntimeTemplate#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_persistent_disk_spec(
        self,
    ) -> typing.Optional["ColabRuntimeTemplateDataPersistentDiskSpec"]:
        '''data_persistent_disk_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#data_persistent_disk_spec ColabRuntimeTemplate#data_persistent_disk_spec}
        '''
        result = self._values.get("data_persistent_disk_spec")
        return typing.cast(typing.Optional["ColabRuntimeTemplateDataPersistentDiskSpec"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the Runtime Template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#description ColabRuntimeTemplate#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_spec(self) -> typing.Optional["ColabRuntimeTemplateEncryptionSpec"]:
        '''encryption_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#encryption_spec ColabRuntimeTemplate#encryption_spec}
        '''
        result = self._values.get("encryption_spec")
        return typing.cast(typing.Optional["ColabRuntimeTemplateEncryptionSpec"], result)

    @builtins.property
    def euc_config(self) -> typing.Optional["ColabRuntimeTemplateEucConfig"]:
        '''euc_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#euc_config ColabRuntimeTemplate#euc_config}
        '''
        result = self._values.get("euc_config")
        return typing.cast(typing.Optional["ColabRuntimeTemplateEucConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#id ColabRuntimeTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idle_shutdown_config(
        self,
    ) -> typing.Optional["ColabRuntimeTemplateIdleShutdownConfig"]:
        '''idle_shutdown_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#idle_shutdown_config ColabRuntimeTemplate#idle_shutdown_config}
        '''
        result = self._values.get("idle_shutdown_config")
        return typing.cast(typing.Optional["ColabRuntimeTemplateIdleShutdownConfig"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels to identify and group the runtime template.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#labels ColabRuntimeTemplate#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def machine_spec(self) -> typing.Optional["ColabRuntimeTemplateMachineSpec"]:
        '''machine_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#machine_spec ColabRuntimeTemplate#machine_spec}
        '''
        result = self._values.get("machine_spec")
        return typing.cast(typing.Optional["ColabRuntimeTemplateMachineSpec"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The resource name of the Runtime Template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#name ColabRuntimeTemplate#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_spec(self) -> typing.Optional["ColabRuntimeTemplateNetworkSpec"]:
        '''network_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#network_spec ColabRuntimeTemplate#network_spec}
        '''
        result = self._values.get("network_spec")
        return typing.cast(typing.Optional["ColabRuntimeTemplateNetworkSpec"], result)

    @builtins.property
    def network_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Applies the given Compute Engine tags to the runtime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#network_tags ColabRuntimeTemplate#network_tags}
        '''
        result = self._values.get("network_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#project ColabRuntimeTemplate#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shielded_vm_config(
        self,
    ) -> typing.Optional["ColabRuntimeTemplateShieldedVmConfig"]:
        '''shielded_vm_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#shielded_vm_config ColabRuntimeTemplate#shielded_vm_config}
        '''
        result = self._values.get("shielded_vm_config")
        return typing.cast(typing.Optional["ColabRuntimeTemplateShieldedVmConfig"], result)

    @builtins.property
    def software_config(self) -> typing.Optional["ColabRuntimeTemplateSoftwareConfig"]:
        '''software_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#software_config ColabRuntimeTemplate#software_config}
        '''
        result = self._values.get("software_config")
        return typing.cast(typing.Optional["ColabRuntimeTemplateSoftwareConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ColabRuntimeTemplateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#timeouts ColabRuntimeTemplate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ColabRuntimeTemplateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColabRuntimeTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateDataPersistentDiskSpec",
    jsii_struct_bases=[],
    name_mapping={"disk_size_gb": "diskSizeGb", "disk_type": "diskType"},
)
class ColabRuntimeTemplateDataPersistentDiskSpec:
    def __init__(
        self,
        *,
        disk_size_gb: typing.Optional[builtins.str] = None,
        disk_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_size_gb: The disk size of the runtime in GB. If specified, the diskType must also be specified. The minimum size is 10GB and the maximum is 65536GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#disk_size_gb ColabRuntimeTemplate#disk_size_gb}
        :param disk_type: The type of the persistent disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#disk_type ColabRuntimeTemplate#disk_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c29d6432826bf1cf41524b43d3789bc6c326cff83963916a09c2b42bdf4e4029)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#disk_size_gb ColabRuntimeTemplate#disk_size_gb}
        '''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_type(self) -> typing.Optional[builtins.str]:
        '''The type of the persistent disk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#disk_type ColabRuntimeTemplate#disk_type}
        '''
        result = self._values.get("disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColabRuntimeTemplateDataPersistentDiskSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ColabRuntimeTemplateDataPersistentDiskSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateDataPersistentDiskSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a65ac1b9d60d12b8a3bfcf68d0cd2395da53a55bf3351ee191f8786c2136cd03)
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
            type_hints = typing.get_type_hints(_typecheckingstub__073b279eb5824e2ec807db4bdfea649cecdfb60ac979d35f27ba942345682f52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskType")
    def disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskType"))

    @disk_type.setter
    def disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed7f7fca83cf74e4d5ee3333cf66a54cc3196a91cdbf3f427b18bbf8239c634a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ColabRuntimeTemplateDataPersistentDiskSpec]:
        return typing.cast(typing.Optional[ColabRuntimeTemplateDataPersistentDiskSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ColabRuntimeTemplateDataPersistentDiskSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc2e3b9660e8af2e5c77da8d1a1bad31eef301359ea9df2dd07100a8e7228a44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateEncryptionSpec",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class ColabRuntimeTemplateEncryptionSpec:
    def __init__(self, *, kms_key_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key_name: The Cloud KMS encryption key (customer-managed encryption key) used to protect the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#kms_key_name ColabRuntimeTemplate#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__991eee6c2e3e53855408fe8dd6e4ee63de97d3ca9095f1031fe26cba86d70968)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''The Cloud KMS encryption key (customer-managed encryption key) used to protect the runtime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#kms_key_name ColabRuntimeTemplate#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColabRuntimeTemplateEncryptionSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ColabRuntimeTemplateEncryptionSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateEncryptionSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__579989bc13798a441e19dfc491b4ea432a03a3c397b221405c69c6528c2fc847)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c88232a2622a8a11c12f331b040c9b6e87f4c4d94afcb2a57b3baa66f0141fd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ColabRuntimeTemplateEncryptionSpec]:
        return typing.cast(typing.Optional[ColabRuntimeTemplateEncryptionSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ColabRuntimeTemplateEncryptionSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96096ef123c2e249b60e165f4b97a6f425e2739ac61b7c3638b483820677ea68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateEucConfig",
    jsii_struct_bases=[],
    name_mapping={"euc_disabled": "eucDisabled"},
)
class ColabRuntimeTemplateEucConfig:
    def __init__(
        self,
        *,
        euc_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param euc_disabled: Disable end user credential access for the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#euc_disabled ColabRuntimeTemplate#euc_disabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd088f4a26252210e7ef74090d3ce9a5993d021c2cd5f13d59b06ae58a68c9a4)
            check_type(argname="argument euc_disabled", value=euc_disabled, expected_type=type_hints["euc_disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if euc_disabled is not None:
            self._values["euc_disabled"] = euc_disabled

    @builtins.property
    def euc_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable end user credential access for the runtime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#euc_disabled ColabRuntimeTemplate#euc_disabled}
        '''
        result = self._values.get("euc_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColabRuntimeTemplateEucConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ColabRuntimeTemplateEucConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateEucConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5238794a7fe9e2e1a72a4ab5630d8ffe24b804dfb68fe2bd177fafac886abf63)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c215596fbf4bd560ac13cf93079b33ac6a1cede93f1b92c82381558cd1379f83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eucDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ColabRuntimeTemplateEucConfig]:
        return typing.cast(typing.Optional[ColabRuntimeTemplateEucConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ColabRuntimeTemplateEucConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e2da37d3598611aee0228aa5fca06251be77b483cf4d8954b6caf3660d55ccd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateIdleShutdownConfig",
    jsii_struct_bases=[],
    name_mapping={"idle_timeout": "idleTimeout"},
)
class ColabRuntimeTemplateIdleShutdownConfig:
    def __init__(self, *, idle_timeout: typing.Optional[builtins.str] = None) -> None:
        '''
        :param idle_timeout: The duration after which the runtime is automatically shut down. An input of 0s disables the idle shutdown feature, and a valid range is [10m, 24h]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#idle_timeout ColabRuntimeTemplate#idle_timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6873d295a0a6c7a7e935d4514611c966c62a5796f2f5b57e70fa14cde4807630)
            check_type(argname="argument idle_timeout", value=idle_timeout, expected_type=type_hints["idle_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if idle_timeout is not None:
            self._values["idle_timeout"] = idle_timeout

    @builtins.property
    def idle_timeout(self) -> typing.Optional[builtins.str]:
        '''The duration after which the runtime is automatically shut down.

        An input of 0s disables the idle shutdown feature, and a valid range is [10m, 24h].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#idle_timeout ColabRuntimeTemplate#idle_timeout}
        '''
        result = self._values.get("idle_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColabRuntimeTemplateIdleShutdownConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ColabRuntimeTemplateIdleShutdownConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateIdleShutdownConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__037c78f9f03685f0c5a1f51b15c73bef3cb89d67b0eea0394191d9662af2944e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed5510d97d7992d6b42b71465dfe2086345e7fd1d5d33b598b701e1ccd0d0d3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ColabRuntimeTemplateIdleShutdownConfig]:
        return typing.cast(typing.Optional[ColabRuntimeTemplateIdleShutdownConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ColabRuntimeTemplateIdleShutdownConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e94fa81e71851dfcf599b4ab3087a1b491b900e4733a8505d3bc41cab45dda75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateMachineSpec",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_count": "acceleratorCount",
        "accelerator_type": "acceleratorType",
        "machine_type": "machineType",
    },
)
class ColabRuntimeTemplateMachineSpec:
    def __init__(
        self,
        *,
        accelerator_count: typing.Optional[jsii.Number] = None,
        accelerator_type: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accelerator_count: The number of accelerators used by the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#accelerator_count ColabRuntimeTemplate#accelerator_count}
        :param accelerator_type: The type of hardware accelerator used by the runtime. If specified, acceleratorCount must also be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#accelerator_type ColabRuntimeTemplate#accelerator_type}
        :param machine_type: The Compute Engine machine type selected for the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#machine_type ColabRuntimeTemplate#machine_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8cf1b5dd9e6fd84d13d56d48065a294cf37ef5d1f9116113cb3f63372d19591)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#accelerator_count ColabRuntimeTemplate#accelerator_count}
        '''
        result = self._values.get("accelerator_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def accelerator_type(self) -> typing.Optional[builtins.str]:
        '''The type of hardware accelerator used by the runtime. If specified, acceleratorCount must also be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#accelerator_type ColabRuntimeTemplate#accelerator_type}
        '''
        result = self._values.get("accelerator_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine machine type selected for the runtime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#machine_type ColabRuntimeTemplate#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColabRuntimeTemplateMachineSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ColabRuntimeTemplateMachineSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateMachineSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__152bd81bac8743ba166a6ce584ad6eb54f11436e83c1c74d850adde1a4866d1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45369532598b4e01e15d12f5eb74c005c36782658c97ade48b01ad17f555f1a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f61e2f9ee0f5da84dd4361b610716562656cd8db9bdf0ad7a2a8553a767e65bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64f42be24a1c94c05fe3c9e5475ade49a830685d779102c5ac628a83ae2b0bde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ColabRuntimeTemplateMachineSpec]:
        return typing.cast(typing.Optional[ColabRuntimeTemplateMachineSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ColabRuntimeTemplateMachineSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00ceb8a92fbc3dd7c00e91b42e9338d5dbf24e3aa8433479ef5a2584f1e5d355)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateNetworkSpec",
    jsii_struct_bases=[],
    name_mapping={
        "enable_internet_access": "enableInternetAccess",
        "network": "network",
        "subnetwork": "subnetwork",
    },
)
class ColabRuntimeTemplateNetworkSpec:
    def __init__(
        self,
        *,
        enable_internet_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enable_internet_access: Enable public internet access for the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#enable_internet_access ColabRuntimeTemplate#enable_internet_access}
        :param network: The name of the VPC that this runtime is in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#network ColabRuntimeTemplate#network}
        :param subnetwork: The name of the subnetwork that this runtime is in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#subnetwork ColabRuntimeTemplate#subnetwork}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12fff0d2c04365c3431735be1cad8e0c91af21c2bb87be7a79e85d5afe65e9eb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#enable_internet_access ColabRuntimeTemplate#enable_internet_access}
        '''
        result = self._values.get("enable_internet_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The name of the VPC that this runtime is in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#network ColabRuntimeTemplate#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''The name of the subnetwork that this runtime is in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#subnetwork ColabRuntimeTemplate#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColabRuntimeTemplateNetworkSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ColabRuntimeTemplateNetworkSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateNetworkSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e95395883fb6ce4e94f822906d5734be2e194f7dc7c820078878a195e009866)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85a6eb8cf6aa738154ac72c52e0142d0addb08845083dac765e27bceeace8071)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableInternetAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__364d291e83b256d581f2b690076c4060a1ec2686e14c6308e7dd92518f36d68c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7245c40ff7853e2058e531d17881eb822b8027ca8593ece2fba65ac2b842486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ColabRuntimeTemplateNetworkSpec]:
        return typing.cast(typing.Optional[ColabRuntimeTemplateNetworkSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ColabRuntimeTemplateNetworkSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d9e38c5f14738eec679d1848a75a2f9d9b888b5c02e44f42dfcb03c368440ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateShieldedVmConfig",
    jsii_struct_bases=[],
    name_mapping={"enable_secure_boot": "enableSecureBoot"},
)
class ColabRuntimeTemplateShieldedVmConfig:
    def __init__(
        self,
        *,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_secure_boot: Enables secure boot for the runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#enable_secure_boot ColabRuntimeTemplate#enable_secure_boot}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dbd06c67186a4b392cefce4167bb85912ee87d7f3d4ed832700bbe3bdf2ae36)
            check_type(argname="argument enable_secure_boot", value=enable_secure_boot, expected_type=type_hints["enable_secure_boot"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_secure_boot is not None:
            self._values["enable_secure_boot"] = enable_secure_boot

    @builtins.property
    def enable_secure_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables secure boot for the runtime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#enable_secure_boot ColabRuntimeTemplate#enable_secure_boot}
        '''
        result = self._values.get("enable_secure_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColabRuntimeTemplateShieldedVmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ColabRuntimeTemplateShieldedVmConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateShieldedVmConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__775bb993e4c855c1cda01602a2544be6aac34e94402916558ad936ef2ffb1bab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74f6a1504ed41b31553e6bd8bba546dde94211c89c505cc951f7aafed6282ce9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSecureBoot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ColabRuntimeTemplateShieldedVmConfig]:
        return typing.cast(typing.Optional[ColabRuntimeTemplateShieldedVmConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ColabRuntimeTemplateShieldedVmConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab411d79381b4aa0578c95323092eabe005be340fa0be1237e30b50e25104c71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateSoftwareConfig",
    jsii_struct_bases=[],
    name_mapping={
        "env": "env",
        "post_startup_script_config": "postStartupScriptConfig",
    },
)
class ColabRuntimeTemplateSoftwareConfig:
    def __init__(
        self,
        *,
        env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ColabRuntimeTemplateSoftwareConfigEnv", typing.Dict[builtins.str, typing.Any]]]]] = None,
        post_startup_script_config: typing.Optional[typing.Union["ColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param env: env block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#env ColabRuntimeTemplate#env}
        :param post_startup_script_config: post_startup_script_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#post_startup_script_config ColabRuntimeTemplate#post_startup_script_config}
        '''
        if isinstance(post_startup_script_config, dict):
            post_startup_script_config = ColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig(**post_startup_script_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f1b3eb13a101abe84fabe90a309443739299f796f9ed6f3562621f2a4ab5f47)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ColabRuntimeTemplateSoftwareConfigEnv"]]]:
        '''env block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#env ColabRuntimeTemplate#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ColabRuntimeTemplateSoftwareConfigEnv"]]], result)

    @builtins.property
    def post_startup_script_config(
        self,
    ) -> typing.Optional["ColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig"]:
        '''post_startup_script_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#post_startup_script_config ColabRuntimeTemplate#post_startup_script_config}
        '''
        result = self._values.get("post_startup_script_config")
        return typing.cast(typing.Optional["ColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColabRuntimeTemplateSoftwareConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateSoftwareConfigEnv",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ColabRuntimeTemplateSoftwareConfigEnv:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the environment variable. Must be a valid C identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#name ColabRuntimeTemplate#name}
        :param value: Variables that reference a $(VAR_NAME) are expanded using the previous defined environment variables in the container and any service environment variables. If a variable cannot be resolved, the reference in the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, regardless of whether the variable exists or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#value ColabRuntimeTemplate#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__defa69caf6658ff38e3a9c0a41ca17d8dbf8e5a796810a961c1b1db5eefa8409)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#name ColabRuntimeTemplate#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Variables that reference a $(VAR_NAME) are expanded using the previous defined environment variables in the container and any service environment variables.

        If a variable cannot be resolved, the reference in the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, regardless of whether the variable exists or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#value ColabRuntimeTemplate#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColabRuntimeTemplateSoftwareConfigEnv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ColabRuntimeTemplateSoftwareConfigEnvList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateSoftwareConfigEnvList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1edb0345aacc6ae89a9ea76cb830d6d8572c7b59567d61aa3de67e316a27b45)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ColabRuntimeTemplateSoftwareConfigEnvOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25416e2f05ed136566351843f8a73c34cbf5ccb362acba02d85b3bfe045f1641)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ColabRuntimeTemplateSoftwareConfigEnvOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__907c2bee6d58b1a945ffc026262d526962f5b1e31b9636824dcbfc45f6d58c19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdbc4f30c4a9ed98880ad31c4964332010148cfef41e13e558f9f62902ac2a5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59853d822586886e65630ce7190fd424e8a795fb847462421bf5b6c4962dd3ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ColabRuntimeTemplateSoftwareConfigEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ColabRuntimeTemplateSoftwareConfigEnv]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ColabRuntimeTemplateSoftwareConfigEnv]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e217b6401e9e3e04fd86dd5d84f3bf643aadf2f1944418d2ee2d50c2ff395ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ColabRuntimeTemplateSoftwareConfigEnvOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateSoftwareConfigEnvOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f62b49f4244f7bb5d1d8e72fe835b4d8de124600c5a50e1409cb5df73f911fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6fd947455a666f50b3284d2ddd971d695781eba2e254aff5fd8d3992487bec2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2f914d88924ac1b9d9b63dc6968c80bacd70731f71d9db44c6805d2c5f39c46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ColabRuntimeTemplateSoftwareConfigEnv]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ColabRuntimeTemplateSoftwareConfigEnv]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ColabRuntimeTemplateSoftwareConfigEnv]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a87629f70306cbe2cf8de8b78ae03c251f5e8df4c24a28e05a9ccb895d5281c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ColabRuntimeTemplateSoftwareConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateSoftwareConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e06f46ef0903b166007018cae1948925623ac3fcacf3f97b08882fbf2907dfe8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEnv")
    def put_env(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ColabRuntimeTemplateSoftwareConfigEnv, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27e48e6048c4d464f9487fe1c912473e7cfa3c17ad996c2599f69727cdea31a7)
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
        :param post_startup_script: Post startup script to run after runtime is started. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#post_startup_script ColabRuntimeTemplate#post_startup_script}
        :param post_startup_script_behavior: Post startup script behavior that defines download and execution behavior. Possible values: ["RUN_ONCE", "RUN_EVERY_START", "DOWNLOAD_AND_RUN_EVERY_START"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#post_startup_script_behavior ColabRuntimeTemplate#post_startup_script_behavior}
        :param post_startup_script_url: Post startup script url to download. Example: https://bucket/script.sh. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#post_startup_script_url ColabRuntimeTemplate#post_startup_script_url}
        '''
        value = ColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig(
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
    def env(self) -> ColabRuntimeTemplateSoftwareConfigEnvList:
        return typing.cast(ColabRuntimeTemplateSoftwareConfigEnvList, jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="postStartupScriptConfig")
    def post_startup_script_config(
        self,
    ) -> "ColabRuntimeTemplateSoftwareConfigPostStartupScriptConfigOutputReference":
        return typing.cast("ColabRuntimeTemplateSoftwareConfigPostStartupScriptConfigOutputReference", jsii.get(self, "postStartupScriptConfig"))

    @builtins.property
    @jsii.member(jsii_name="envInput")
    def env_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ColabRuntimeTemplateSoftwareConfigEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ColabRuntimeTemplateSoftwareConfigEnv]]], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="postStartupScriptConfigInput")
    def post_startup_script_config_input(
        self,
    ) -> typing.Optional["ColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig"]:
        return typing.cast(typing.Optional["ColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig"], jsii.get(self, "postStartupScriptConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ColabRuntimeTemplateSoftwareConfig]:
        return typing.cast(typing.Optional[ColabRuntimeTemplateSoftwareConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ColabRuntimeTemplateSoftwareConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66edef88c103bcd21e24ab929c4a14f500dea435a6aea9d9cf4a7106eb85eae2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig",
    jsii_struct_bases=[],
    name_mapping={
        "post_startup_script": "postStartupScript",
        "post_startup_script_behavior": "postStartupScriptBehavior",
        "post_startup_script_url": "postStartupScriptUrl",
    },
)
class ColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig:
    def __init__(
        self,
        *,
        post_startup_script: typing.Optional[builtins.str] = None,
        post_startup_script_behavior: typing.Optional[builtins.str] = None,
        post_startup_script_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param post_startup_script: Post startup script to run after runtime is started. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#post_startup_script ColabRuntimeTemplate#post_startup_script}
        :param post_startup_script_behavior: Post startup script behavior that defines download and execution behavior. Possible values: ["RUN_ONCE", "RUN_EVERY_START", "DOWNLOAD_AND_RUN_EVERY_START"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#post_startup_script_behavior ColabRuntimeTemplate#post_startup_script_behavior}
        :param post_startup_script_url: Post startup script url to download. Example: https://bucket/script.sh. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#post_startup_script_url ColabRuntimeTemplate#post_startup_script_url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d44211220d188026611e51d0066de20d28a2f821799e0eb5187498f50c2a9c3d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#post_startup_script ColabRuntimeTemplate#post_startup_script}
        '''
        result = self._values.get("post_startup_script")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_startup_script_behavior(self) -> typing.Optional[builtins.str]:
        '''Post startup script behavior that defines download and execution behavior. Possible values: ["RUN_ONCE", "RUN_EVERY_START", "DOWNLOAD_AND_RUN_EVERY_START"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#post_startup_script_behavior ColabRuntimeTemplate#post_startup_script_behavior}
        '''
        result = self._values.get("post_startup_script_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_startup_script_url(self) -> typing.Optional[builtins.str]:
        '''Post startup script url to download. Example: https://bucket/script.sh.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#post_startup_script_url ColabRuntimeTemplate#post_startup_script_url}
        '''
        result = self._values.get("post_startup_script_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ColabRuntimeTemplateSoftwareConfigPostStartupScriptConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateSoftwareConfigPostStartupScriptConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6b5ff5bbfa436f257535a922a266a9bece69f20d54536d6b279474f74185ebc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a499722bf47059898095f3ca33b043cd59f5daecc0bb3490574cf4737a5f768d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postStartupScript", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postStartupScriptBehavior")
    def post_startup_script_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postStartupScriptBehavior"))

    @post_startup_script_behavior.setter
    def post_startup_script_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68d357a1276018bbe0e83423838566dadd3db78d111b39c631e9dff05f12c08a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postStartupScriptBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postStartupScriptUrl")
    def post_startup_script_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postStartupScriptUrl"))

    @post_startup_script_url.setter
    def post_startup_script_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fd14b394cd47868bc87036ce5e4610b278eefe0dd486e64bb2e8d911f1d74d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postStartupScriptUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig]:
        return typing.cast(typing.Optional[ColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f225499ee0018802cca9a093f650834118d554224cb2453716f2bc7d9e882998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ColabRuntimeTemplateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#create ColabRuntimeTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#delete ColabRuntimeTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#update ColabRuntimeTemplate#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0536c6a1b7cd8c768a6992f93b674fc41d0bc2d0f3d7755a54f53fd4347f4554)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#create ColabRuntimeTemplate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#delete ColabRuntimeTemplate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_runtime_template#update ColabRuntimeTemplate#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColabRuntimeTemplateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ColabRuntimeTemplateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabRuntimeTemplate.ColabRuntimeTemplateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a0ff82abdf50fbaa0da6924227a31d25cbbf86a8efd5037066b886d5f4087c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14fa0527c35c2d13261a248c66ac6fb4e5d13ada82a29a5a07512b8161b5c039)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73970e7296e0e54e94f676422c6444303aba52145b688be03cd8a6083272b4ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1e55568aecbf7929c4cbb32a54479919a85840e6a7016b3daae07ac814eb565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ColabRuntimeTemplateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ColabRuntimeTemplateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ColabRuntimeTemplateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cae48a37c20501b6d65b4ba88292d53af08af9cb732ed1f18e32355000bff043)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ColabRuntimeTemplate",
    "ColabRuntimeTemplateConfig",
    "ColabRuntimeTemplateDataPersistentDiskSpec",
    "ColabRuntimeTemplateDataPersistentDiskSpecOutputReference",
    "ColabRuntimeTemplateEncryptionSpec",
    "ColabRuntimeTemplateEncryptionSpecOutputReference",
    "ColabRuntimeTemplateEucConfig",
    "ColabRuntimeTemplateEucConfigOutputReference",
    "ColabRuntimeTemplateIdleShutdownConfig",
    "ColabRuntimeTemplateIdleShutdownConfigOutputReference",
    "ColabRuntimeTemplateMachineSpec",
    "ColabRuntimeTemplateMachineSpecOutputReference",
    "ColabRuntimeTemplateNetworkSpec",
    "ColabRuntimeTemplateNetworkSpecOutputReference",
    "ColabRuntimeTemplateShieldedVmConfig",
    "ColabRuntimeTemplateShieldedVmConfigOutputReference",
    "ColabRuntimeTemplateSoftwareConfig",
    "ColabRuntimeTemplateSoftwareConfigEnv",
    "ColabRuntimeTemplateSoftwareConfigEnvList",
    "ColabRuntimeTemplateSoftwareConfigEnvOutputReference",
    "ColabRuntimeTemplateSoftwareConfigOutputReference",
    "ColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig",
    "ColabRuntimeTemplateSoftwareConfigPostStartupScriptConfigOutputReference",
    "ColabRuntimeTemplateTimeouts",
    "ColabRuntimeTemplateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__9db1219f73f879802a4e83b2caabbbf02a56fb89448dde71577cba37eee69ade(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    location: builtins.str,
    data_persistent_disk_spec: typing.Optional[typing.Union[ColabRuntimeTemplateDataPersistentDiskSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    encryption_spec: typing.Optional[typing.Union[ColabRuntimeTemplateEncryptionSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    euc_config: typing.Optional[typing.Union[ColabRuntimeTemplateEucConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    idle_shutdown_config: typing.Optional[typing.Union[ColabRuntimeTemplateIdleShutdownConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    machine_spec: typing.Optional[typing.Union[ColabRuntimeTemplateMachineSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    network_spec: typing.Optional[typing.Union[ColabRuntimeTemplateNetworkSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    shielded_vm_config: typing.Optional[typing.Union[ColabRuntimeTemplateShieldedVmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    software_config: typing.Optional[typing.Union[ColabRuntimeTemplateSoftwareConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ColabRuntimeTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__76f8049ea0c90d22244a316c2b98ca7a21fb0232dcfce807bd59f1bb35eadcc6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cca38125e886fd78a2c422a4f686fb95a799e310da71a53d23a77e749e23ccd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5339ec2c16f020fe87cd3469465ffe5c1f667dc12a79be8dbb769ed7d8cd774(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9335e4ffa742c96f7e3ffde371bb992e269e627b5919032cb0d7eaa1d0a53f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6f8f982928814e64b8af14f1c3845e0c63730b2e9dd5dbcd81a6d36035df4c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b444f12639e26c53593a2c66ae6de726a8986d4d9035bd7edf744b63d7959a8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22e59ad14d5185d483d8999da525f63dd356577cefe9dee5a45068d7d60ae15f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be618bd9a0302d9ad68327a3d3f5e8fc51eb6bf920ed6d9650e5f0dd319d5fd5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac57be85dbb76de326e78750f7da2484e1e68448c01aa0c4360893263037db3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33f28aeb359535f0a6caf987afad5b808f7b572cfd333424162153dc9bedca21(
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
    data_persistent_disk_spec: typing.Optional[typing.Union[ColabRuntimeTemplateDataPersistentDiskSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    encryption_spec: typing.Optional[typing.Union[ColabRuntimeTemplateEncryptionSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    euc_config: typing.Optional[typing.Union[ColabRuntimeTemplateEucConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    idle_shutdown_config: typing.Optional[typing.Union[ColabRuntimeTemplateIdleShutdownConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    machine_spec: typing.Optional[typing.Union[ColabRuntimeTemplateMachineSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    network_spec: typing.Optional[typing.Union[ColabRuntimeTemplateNetworkSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    shielded_vm_config: typing.Optional[typing.Union[ColabRuntimeTemplateShieldedVmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    software_config: typing.Optional[typing.Union[ColabRuntimeTemplateSoftwareConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ColabRuntimeTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c29d6432826bf1cf41524b43d3789bc6c326cff83963916a09c2b42bdf4e4029(
    *,
    disk_size_gb: typing.Optional[builtins.str] = None,
    disk_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a65ac1b9d60d12b8a3bfcf68d0cd2395da53a55bf3351ee191f8786c2136cd03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073b279eb5824e2ec807db4bdfea649cecdfb60ac979d35f27ba942345682f52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed7f7fca83cf74e4d5ee3333cf66a54cc3196a91cdbf3f427b18bbf8239c634a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc2e3b9660e8af2e5c77da8d1a1bad31eef301359ea9df2dd07100a8e7228a44(
    value: typing.Optional[ColabRuntimeTemplateDataPersistentDiskSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__991eee6c2e3e53855408fe8dd6e4ee63de97d3ca9095f1031fe26cba86d70968(
    *,
    kms_key_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579989bc13798a441e19dfc491b4ea432a03a3c397b221405c69c6528c2fc847(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c88232a2622a8a11c12f331b040c9b6e87f4c4d94afcb2a57b3baa66f0141fd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96096ef123c2e249b60e165f4b97a6f425e2739ac61b7c3638b483820677ea68(
    value: typing.Optional[ColabRuntimeTemplateEncryptionSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd088f4a26252210e7ef74090d3ce9a5993d021c2cd5f13d59b06ae58a68c9a4(
    *,
    euc_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5238794a7fe9e2e1a72a4ab5630d8ffe24b804dfb68fe2bd177fafac886abf63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c215596fbf4bd560ac13cf93079b33ac6a1cede93f1b92c82381558cd1379f83(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e2da37d3598611aee0228aa5fca06251be77b483cf4d8954b6caf3660d55ccd(
    value: typing.Optional[ColabRuntimeTemplateEucConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6873d295a0a6c7a7e935d4514611c966c62a5796f2f5b57e70fa14cde4807630(
    *,
    idle_timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__037c78f9f03685f0c5a1f51b15c73bef3cb89d67b0eea0394191d9662af2944e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed5510d97d7992d6b42b71465dfe2086345e7fd1d5d33b598b701e1ccd0d0d3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e94fa81e71851dfcf599b4ab3087a1b491b900e4733a8505d3bc41cab45dda75(
    value: typing.Optional[ColabRuntimeTemplateIdleShutdownConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8cf1b5dd9e6fd84d13d56d48065a294cf37ef5d1f9116113cb3f63372d19591(
    *,
    accelerator_count: typing.Optional[jsii.Number] = None,
    accelerator_type: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__152bd81bac8743ba166a6ce584ad6eb54f11436e83c1c74d850adde1a4866d1b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45369532598b4e01e15d12f5eb74c005c36782658c97ade48b01ad17f555f1a8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f61e2f9ee0f5da84dd4361b610716562656cd8db9bdf0ad7a2a8553a767e65bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f42be24a1c94c05fe3c9e5475ade49a830685d779102c5ac628a83ae2b0bde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ceb8a92fbc3dd7c00e91b42e9338d5dbf24e3aa8433479ef5a2584f1e5d355(
    value: typing.Optional[ColabRuntimeTemplateMachineSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12fff0d2c04365c3431735be1cad8e0c91af21c2bb87be7a79e85d5afe65e9eb(
    *,
    enable_internet_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    network: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e95395883fb6ce4e94f822906d5734be2e194f7dc7c820078878a195e009866(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85a6eb8cf6aa738154ac72c52e0142d0addb08845083dac765e27bceeace8071(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__364d291e83b256d581f2b690076c4060a1ec2686e14c6308e7dd92518f36d68c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7245c40ff7853e2058e531d17881eb822b8027ca8593ece2fba65ac2b842486(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d9e38c5f14738eec679d1848a75a2f9d9b888b5c02e44f42dfcb03c368440ce(
    value: typing.Optional[ColabRuntimeTemplateNetworkSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dbd06c67186a4b392cefce4167bb85912ee87d7f3d4ed832700bbe3bdf2ae36(
    *,
    enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__775bb993e4c855c1cda01602a2544be6aac34e94402916558ad936ef2ffb1bab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f6a1504ed41b31553e6bd8bba546dde94211c89c505cc951f7aafed6282ce9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab411d79381b4aa0578c95323092eabe005be340fa0be1237e30b50e25104c71(
    value: typing.Optional[ColabRuntimeTemplateShieldedVmConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f1b3eb13a101abe84fabe90a309443739299f796f9ed6f3562621f2a4ab5f47(
    *,
    env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ColabRuntimeTemplateSoftwareConfigEnv, typing.Dict[builtins.str, typing.Any]]]]] = None,
    post_startup_script_config: typing.Optional[typing.Union[ColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__defa69caf6658ff38e3a9c0a41ca17d8dbf8e5a796810a961c1b1db5eefa8409(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1edb0345aacc6ae89a9ea76cb830d6d8572c7b59567d61aa3de67e316a27b45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25416e2f05ed136566351843f8a73c34cbf5ccb362acba02d85b3bfe045f1641(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__907c2bee6d58b1a945ffc026262d526962f5b1e31b9636824dcbfc45f6d58c19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdbc4f30c4a9ed98880ad31c4964332010148cfef41e13e558f9f62902ac2a5b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59853d822586886e65630ce7190fd424e8a795fb847462421bf5b6c4962dd3ec(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e217b6401e9e3e04fd86dd5d84f3bf643aadf2f1944418d2ee2d50c2ff395ea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ColabRuntimeTemplateSoftwareConfigEnv]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f62b49f4244f7bb5d1d8e72fe835b4d8de124600c5a50e1409cb5df73f911fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6fd947455a666f50b3284d2ddd971d695781eba2e254aff5fd8d3992487bec2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2f914d88924ac1b9d9b63dc6968c80bacd70731f71d9db44c6805d2c5f39c46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a87629f70306cbe2cf8de8b78ae03c251f5e8df4c24a28e05a9ccb895d5281c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ColabRuntimeTemplateSoftwareConfigEnv]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e06f46ef0903b166007018cae1948925623ac3fcacf3f97b08882fbf2907dfe8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e48e6048c4d464f9487fe1c912473e7cfa3c17ad996c2599f69727cdea31a7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ColabRuntimeTemplateSoftwareConfigEnv, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66edef88c103bcd21e24ab929c4a14f500dea435a6aea9d9cf4a7106eb85eae2(
    value: typing.Optional[ColabRuntimeTemplateSoftwareConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44211220d188026611e51d0066de20d28a2f821799e0eb5187498f50c2a9c3d(
    *,
    post_startup_script: typing.Optional[builtins.str] = None,
    post_startup_script_behavior: typing.Optional[builtins.str] = None,
    post_startup_script_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b5ff5bbfa436f257535a922a266a9bece69f20d54536d6b279474f74185ebc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a499722bf47059898095f3ca33b043cd59f5daecc0bb3490574cf4737a5f768d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68d357a1276018bbe0e83423838566dadd3db78d111b39c631e9dff05f12c08a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd14b394cd47868bc87036ce5e4610b278eefe0dd486e64bb2e8d911f1d74d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f225499ee0018802cca9a093f650834118d554224cb2453716f2bc7d9e882998(
    value: typing.Optional[ColabRuntimeTemplateSoftwareConfigPostStartupScriptConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0536c6a1b7cd8c768a6992f93b674fc41d0bc2d0f3d7755a54f53fd4347f4554(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a0ff82abdf50fbaa0da6924227a31d25cbbf86a8efd5037066b886d5f4087c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14fa0527c35c2d13261a248c66ac6fb4e5d13ada82a29a5a07512b8161b5c039(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73970e7296e0e54e94f676422c6444303aba52145b688be03cd8a6083272b4ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e55568aecbf7929c4cbb32a54479919a85840e6a7016b3daae07ac814eb565(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae48a37c20501b6d65b4ba88292d53af08af9cb732ed1f18e32355000bff043(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ColabRuntimeTemplateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
