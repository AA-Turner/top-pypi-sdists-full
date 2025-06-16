r'''
# `google_notebooks_runtime`

Refer to the Terraform Registry for docs: [`google_notebooks_runtime`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime).
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


class GoogleNotebooksRuntime(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntime",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime google_notebooks_runtime}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        access_config: typing.Optional[typing.Union["GoogleNotebooksRuntimeAccessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        software_config: typing.Optional[typing.Union["GoogleNotebooksRuntimeSoftwareConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleNotebooksRuntimeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_machine: typing.Optional[typing.Union["GoogleNotebooksRuntimeVirtualMachine", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime google_notebooks_runtime} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: A reference to the zone where the machine resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#location GoogleNotebooksRuntime#location}
        :param name: The name specified for the Notebook runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#name GoogleNotebooksRuntime#name}
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#access_config GoogleNotebooksRuntime#access_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#id GoogleNotebooksRuntime#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels to associate with this runtime. Label **keys** must contain 1 to 63 characters, and must conform to [RFC 1035] (https://www.ietf.org/rfc/rfc1035.txt). Label **values** may be empty, but, if present, must contain 1 to 63 characters, and must conform to `RFC 1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. No more than 32 labels can be associated with a cluster. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#labels GoogleNotebooksRuntime#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#project GoogleNotebooksRuntime#project}.
        :param software_config: software_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#software_config GoogleNotebooksRuntime#software_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#timeouts GoogleNotebooksRuntime#timeouts}
        :param virtual_machine: virtual_machine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#virtual_machine GoogleNotebooksRuntime#virtual_machine}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18515721895903fbb71b7f101a14a1ecbbf85412122ebeb10a30b8bd2ec76d48)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleNotebooksRuntimeConfig(
            location=location,
            name=name,
            access_config=access_config,
            id=id,
            labels=labels,
            project=project,
            software_config=software_config,
            timeouts=timeouts,
            virtual_machine=virtual_machine,
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
        '''Generates CDKTF code for importing a GoogleNotebooksRuntime resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleNotebooksRuntime to import.
        :param import_from_id: The id of the existing GoogleNotebooksRuntime that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleNotebooksRuntime to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f02ee26a228eaa479d33deeaa06e6444878c790df9e1bd2fd9ebb372cff94115)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAccessConfig")
    def put_access_config(
        self,
        *,
        access_type: typing.Optional[builtins.str] = None,
        runtime_owner: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_type: The type of access mode this instance. For valid values, see 'https://cloud.google.com/vertex-ai/docs/workbench/reference/ rest/v1/projects.locations.runtimes#RuntimeAccessType'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#access_type GoogleNotebooksRuntime#access_type}
        :param runtime_owner: The owner of this runtime after creation. Format: 'alias@example.com'. Currently supports one owner only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#runtime_owner GoogleNotebooksRuntime#runtime_owner}
        '''
        value = GoogleNotebooksRuntimeAccessConfig(
            access_type=access_type, runtime_owner=runtime_owner
        )

        return typing.cast(None, jsii.invoke(self, "putAccessConfig", [value]))

    @jsii.member(jsii_name="putSoftwareConfig")
    def put_software_config(
        self,
        *,
        custom_gpu_driver_path: typing.Optional[builtins.str] = None,
        enable_health_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        idle_shutdown: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        idle_shutdown_timeout: typing.Optional[jsii.Number] = None,
        install_gpu_driver: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kernels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNotebooksRuntimeSoftwareConfigKernels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        notebook_upgrade_schedule: typing.Optional[builtins.str] = None,
        post_startup_script: typing.Optional[builtins.str] = None,
        post_startup_script_behavior: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_gpu_driver_path: Specify a custom Cloud Storage path where the GPU driver is stored. If not specified, we'll automatically choose from official GPU drivers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#custom_gpu_driver_path GoogleNotebooksRuntime#custom_gpu_driver_path}
        :param enable_health_monitoring: Verifies core internal services are running. Default: True. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#enable_health_monitoring GoogleNotebooksRuntime#enable_health_monitoring}
        :param idle_shutdown: Runtime will automatically shutdown after idle_shutdown_time. Default: True. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#idle_shutdown GoogleNotebooksRuntime#idle_shutdown}
        :param idle_shutdown_timeout: Time in minutes to wait before shuting down runtime. Default: 180 minutes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#idle_shutdown_timeout GoogleNotebooksRuntime#idle_shutdown_timeout}
        :param install_gpu_driver: Install Nvidia Driver automatically. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#install_gpu_driver GoogleNotebooksRuntime#install_gpu_driver}
        :param kernels: kernels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#kernels GoogleNotebooksRuntime#kernels}
        :param notebook_upgrade_schedule: Cron expression in UTC timezone for schedule instance auto upgrade. Please follow the `cron format <https://en.wikipedia.org/wiki/Cron>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#notebook_upgrade_schedule GoogleNotebooksRuntime#notebook_upgrade_schedule}
        :param post_startup_script: Path to a Bash script that automatically runs after a notebook instance fully boots up. The path must be a URL or Cloud Storage path (gs://path-to-file/file-name). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#post_startup_script GoogleNotebooksRuntime#post_startup_script}
        :param post_startup_script_behavior: Behavior for the post startup script. Possible values: ["POST_STARTUP_SCRIPT_BEHAVIOR_UNSPECIFIED", "RUN_EVERY_START", "DOWNLOAD_AND_RUN_EVERY_START"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#post_startup_script_behavior GoogleNotebooksRuntime#post_startup_script_behavior}
        '''
        value = GoogleNotebooksRuntimeSoftwareConfig(
            custom_gpu_driver_path=custom_gpu_driver_path,
            enable_health_monitoring=enable_health_monitoring,
            idle_shutdown=idle_shutdown,
            idle_shutdown_timeout=idle_shutdown_timeout,
            install_gpu_driver=install_gpu_driver,
            kernels=kernels,
            notebook_upgrade_schedule=notebook_upgrade_schedule,
            post_startup_script=post_startup_script,
            post_startup_script_behavior=post_startup_script_behavior,
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#create GoogleNotebooksRuntime#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#delete GoogleNotebooksRuntime#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#update GoogleNotebooksRuntime#update}.
        '''
        value = GoogleNotebooksRuntimeTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVirtualMachine")
    def put_virtual_machine(
        self,
        *,
        virtual_machine_config: typing.Optional[typing.Union["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param virtual_machine_config: virtual_machine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#virtual_machine_config GoogleNotebooksRuntime#virtual_machine_config}
        '''
        value = GoogleNotebooksRuntimeVirtualMachine(
            virtual_machine_config=virtual_machine_config
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualMachine", [value]))

    @jsii.member(jsii_name="resetAccessConfig")
    def reset_access_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSoftwareConfig")
    def reset_software_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSoftwareConfig", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVirtualMachine")
    def reset_virtual_machine(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualMachine", []))

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
    @jsii.member(jsii_name="accessConfig")
    def access_config(self) -> "GoogleNotebooksRuntimeAccessConfigOutputReference":
        return typing.cast("GoogleNotebooksRuntimeAccessConfigOutputReference", jsii.get(self, "accessConfig"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="healthState")
    def health_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthState"))

    @builtins.property
    @jsii.member(jsii_name="metrics")
    def metrics(self) -> "GoogleNotebooksRuntimeMetricsList":
        return typing.cast("GoogleNotebooksRuntimeMetricsList", jsii.get(self, "metrics"))

    @builtins.property
    @jsii.member(jsii_name="softwareConfig")
    def software_config(self) -> "GoogleNotebooksRuntimeSoftwareConfigOutputReference":
        return typing.cast("GoogleNotebooksRuntimeSoftwareConfigOutputReference", jsii.get(self, "softwareConfig"))

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
    def timeouts(self) -> "GoogleNotebooksRuntimeTimeoutsOutputReference":
        return typing.cast("GoogleNotebooksRuntimeTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachine")
    def virtual_machine(self) -> "GoogleNotebooksRuntimeVirtualMachineOutputReference":
        return typing.cast("GoogleNotebooksRuntimeVirtualMachineOutputReference", jsii.get(self, "virtualMachine"))

    @builtins.property
    @jsii.member(jsii_name="accessConfigInput")
    def access_config_input(
        self,
    ) -> typing.Optional["GoogleNotebooksRuntimeAccessConfig"]:
        return typing.cast(typing.Optional["GoogleNotebooksRuntimeAccessConfig"], jsii.get(self, "accessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

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
    @jsii.member(jsii_name="softwareConfigInput")
    def software_config_input(
        self,
    ) -> typing.Optional["GoogleNotebooksRuntimeSoftwareConfig"]:
        return typing.cast(typing.Optional["GoogleNotebooksRuntimeSoftwareConfig"], jsii.get(self, "softwareConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNotebooksRuntimeTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNotebooksRuntimeTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineInput")
    def virtual_machine_input(
        self,
    ) -> typing.Optional["GoogleNotebooksRuntimeVirtualMachine"]:
        return typing.cast(typing.Optional["GoogleNotebooksRuntimeVirtualMachine"], jsii.get(self, "virtualMachineInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eb1f0f7ec622536e07c1e8a2fedfdb71b96bd1fe87b8632d89b87ac284b78be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3aad6f9ee801c2a7ea903389d2516eb52c44526f48664537fdbf12f9ac99a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8af8e71d48c68fe3ba50eae014b0d378e5247cb2fe3db2c8f452c4d80b5b07a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ea5742f14bb6346378afe0aba00f84c5e2e5492cb187448a314922db90cc15a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe90830393afe41c95c28896817163f8dfe7f4f6b305560ccf02b96e77485d31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeAccessConfig",
    jsii_struct_bases=[],
    name_mapping={"access_type": "accessType", "runtime_owner": "runtimeOwner"},
)
class GoogleNotebooksRuntimeAccessConfig:
    def __init__(
        self,
        *,
        access_type: typing.Optional[builtins.str] = None,
        runtime_owner: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_type: The type of access mode this instance. For valid values, see 'https://cloud.google.com/vertex-ai/docs/workbench/reference/ rest/v1/projects.locations.runtimes#RuntimeAccessType'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#access_type GoogleNotebooksRuntime#access_type}
        :param runtime_owner: The owner of this runtime after creation. Format: 'alias@example.com'. Currently supports one owner only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#runtime_owner GoogleNotebooksRuntime#runtime_owner}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ddf77ac5db0fa99072a87b41c8c9463c683695218cef2e40ede818f37d90a66)
            check_type(argname="argument access_type", value=access_type, expected_type=type_hints["access_type"])
            check_type(argname="argument runtime_owner", value=runtime_owner, expected_type=type_hints["runtime_owner"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_type is not None:
            self._values["access_type"] = access_type
        if runtime_owner is not None:
            self._values["runtime_owner"] = runtime_owner

    @builtins.property
    def access_type(self) -> typing.Optional[builtins.str]:
        '''The type of access mode this instance. For valid values, see 'https://cloud.google.com/vertex-ai/docs/workbench/reference/ rest/v1/projects.locations.runtimes#RuntimeAccessType'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#access_type GoogleNotebooksRuntime#access_type}
        '''
        result = self._values.get("access_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_owner(self) -> typing.Optional[builtins.str]:
        '''The owner of this runtime after creation. Format: 'alias@example.com'. Currently supports one owner only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#runtime_owner GoogleNotebooksRuntime#runtime_owner}
        '''
        result = self._values.get("runtime_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNotebooksRuntimeAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNotebooksRuntimeAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6dcb6d673c491963fce8d8c0fb76c6827c74dc70926b0db8cd95489812c8518)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccessType")
    def reset_access_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessType", []))

    @jsii.member(jsii_name="resetRuntimeOwner")
    def reset_runtime_owner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeOwner", []))

    @builtins.property
    @jsii.member(jsii_name="proxyUri")
    def proxy_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyUri"))

    @builtins.property
    @jsii.member(jsii_name="accessTypeInput")
    def access_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeOwnerInput")
    def runtime_owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeOwnerInput"))

    @builtins.property
    @jsii.member(jsii_name="accessType")
    def access_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessType"))

    @access_type.setter
    def access_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e06f9ea3421e6a87e8e12e35bd37bf3cead56e099371e6074c6e3162b22afb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeOwner")
    def runtime_owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeOwner"))

    @runtime_owner.setter
    def runtime_owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a202680fa04f26a9bffb23ee078590efd27b3b2f4f6260987ea07b55807f0e53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeOwner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleNotebooksRuntimeAccessConfig]:
        return typing.cast(typing.Optional[GoogleNotebooksRuntimeAccessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNotebooksRuntimeAccessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19066932c6c31111bc9857bc612c7224b67a892e306db55a4f1ff34fe064c618)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeConfig",
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
        "access_config": "accessConfig",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "software_config": "softwareConfig",
        "timeouts": "timeouts",
        "virtual_machine": "virtualMachine",
    },
)
class GoogleNotebooksRuntimeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        access_config: typing.Optional[typing.Union[GoogleNotebooksRuntimeAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        software_config: typing.Optional[typing.Union["GoogleNotebooksRuntimeSoftwareConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleNotebooksRuntimeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_machine: typing.Optional[typing.Union["GoogleNotebooksRuntimeVirtualMachine", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: A reference to the zone where the machine resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#location GoogleNotebooksRuntime#location}
        :param name: The name specified for the Notebook runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#name GoogleNotebooksRuntime#name}
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#access_config GoogleNotebooksRuntime#access_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#id GoogleNotebooksRuntime#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels to associate with this runtime. Label **keys** must contain 1 to 63 characters, and must conform to [RFC 1035] (https://www.ietf.org/rfc/rfc1035.txt). Label **values** may be empty, but, if present, must contain 1 to 63 characters, and must conform to `RFC 1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. No more than 32 labels can be associated with a cluster. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#labels GoogleNotebooksRuntime#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#project GoogleNotebooksRuntime#project}.
        :param software_config: software_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#software_config GoogleNotebooksRuntime#software_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#timeouts GoogleNotebooksRuntime#timeouts}
        :param virtual_machine: virtual_machine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#virtual_machine GoogleNotebooksRuntime#virtual_machine}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(access_config, dict):
            access_config = GoogleNotebooksRuntimeAccessConfig(**access_config)
        if isinstance(software_config, dict):
            software_config = GoogleNotebooksRuntimeSoftwareConfig(**software_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleNotebooksRuntimeTimeouts(**timeouts)
        if isinstance(virtual_machine, dict):
            virtual_machine = GoogleNotebooksRuntimeVirtualMachine(**virtual_machine)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57cc16778a19b750bbd7fc7f6b7ed4ededf2746c55f93ec03525be916ac2b0d5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument access_config", value=access_config, expected_type=type_hints["access_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument software_config", value=software_config, expected_type=type_hints["software_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument virtual_machine", value=virtual_machine, expected_type=type_hints["virtual_machine"])
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
        if access_config is not None:
            self._values["access_config"] = access_config
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if software_config is not None:
            self._values["software_config"] = software_config
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if virtual_machine is not None:
            self._values["virtual_machine"] = virtual_machine

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
        '''A reference to the zone where the machine resides.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#location GoogleNotebooksRuntime#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name specified for the Notebook runtime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#name GoogleNotebooksRuntime#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_config(self) -> typing.Optional[GoogleNotebooksRuntimeAccessConfig]:
        '''access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#access_config GoogleNotebooksRuntime#access_config}
        '''
        result = self._values.get("access_config")
        return typing.cast(typing.Optional[GoogleNotebooksRuntimeAccessConfig], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#id GoogleNotebooksRuntime#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The labels to associate with this runtime.

        Label **keys** must
        contain 1 to 63 characters, and must conform to [RFC 1035]
        (https://www.ietf.org/rfc/rfc1035.txt). Label **values** may be
        empty, but, if present, must contain 1 to 63 characters, and must
        conform to `RFC 1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. No
        more than 32 labels can be associated with a cluster.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#labels GoogleNotebooksRuntime#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#project GoogleNotebooksRuntime#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def software_config(
        self,
    ) -> typing.Optional["GoogleNotebooksRuntimeSoftwareConfig"]:
        '''software_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#software_config GoogleNotebooksRuntime#software_config}
        '''
        result = self._values.get("software_config")
        return typing.cast(typing.Optional["GoogleNotebooksRuntimeSoftwareConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleNotebooksRuntimeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#timeouts GoogleNotebooksRuntime#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleNotebooksRuntimeTimeouts"], result)

    @builtins.property
    def virtual_machine(
        self,
    ) -> typing.Optional["GoogleNotebooksRuntimeVirtualMachine"]:
        '''virtual_machine block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#virtual_machine GoogleNotebooksRuntime#virtual_machine}
        '''
        result = self._values.get("virtual_machine")
        return typing.cast(typing.Optional["GoogleNotebooksRuntimeVirtualMachine"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNotebooksRuntimeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeMetrics",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleNotebooksRuntimeMetrics:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNotebooksRuntimeMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNotebooksRuntimeMetricsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeMetricsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9de48644de57950a7fe7a0f9f0624f692acc07d823f38c7f54ad0b16de6e24be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GoogleNotebooksRuntimeMetricsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__420b17d877aa42f7026b146501b8829d9498da9889b7cb21c16926cda370975c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNotebooksRuntimeMetricsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb373e62e7897800cd957b84259309a3a7d05a45e9e1ddcecca709198ac1fc7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a8769afc57f5435a3be5dea4783d10a12c43869d039ddf4066f196763f7b285)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c1cb7151cf090ae5d10e26e7337159eca31361ce06da28bb484bea3d97177a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleNotebooksRuntimeMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2da6a5244ac23d1b4128ffec32cdd62598711d2fedcedd07650ae8cfc92fecb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="systemMetrics")
    def system_metrics(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "systemMetrics"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleNotebooksRuntimeMetrics]:
        return typing.cast(typing.Optional[GoogleNotebooksRuntimeMetrics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNotebooksRuntimeMetrics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c21c3173df77a90d3b7deadd688becf98b61b999bc2bd8b9f0055ee1afae4e62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeSoftwareConfig",
    jsii_struct_bases=[],
    name_mapping={
        "custom_gpu_driver_path": "customGpuDriverPath",
        "enable_health_monitoring": "enableHealthMonitoring",
        "idle_shutdown": "idleShutdown",
        "idle_shutdown_timeout": "idleShutdownTimeout",
        "install_gpu_driver": "installGpuDriver",
        "kernels": "kernels",
        "notebook_upgrade_schedule": "notebookUpgradeSchedule",
        "post_startup_script": "postStartupScript",
        "post_startup_script_behavior": "postStartupScriptBehavior",
    },
)
class GoogleNotebooksRuntimeSoftwareConfig:
    def __init__(
        self,
        *,
        custom_gpu_driver_path: typing.Optional[builtins.str] = None,
        enable_health_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        idle_shutdown: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        idle_shutdown_timeout: typing.Optional[jsii.Number] = None,
        install_gpu_driver: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kernels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNotebooksRuntimeSoftwareConfigKernels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        notebook_upgrade_schedule: typing.Optional[builtins.str] = None,
        post_startup_script: typing.Optional[builtins.str] = None,
        post_startup_script_behavior: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_gpu_driver_path: Specify a custom Cloud Storage path where the GPU driver is stored. If not specified, we'll automatically choose from official GPU drivers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#custom_gpu_driver_path GoogleNotebooksRuntime#custom_gpu_driver_path}
        :param enable_health_monitoring: Verifies core internal services are running. Default: True. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#enable_health_monitoring GoogleNotebooksRuntime#enable_health_monitoring}
        :param idle_shutdown: Runtime will automatically shutdown after idle_shutdown_time. Default: True. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#idle_shutdown GoogleNotebooksRuntime#idle_shutdown}
        :param idle_shutdown_timeout: Time in minutes to wait before shuting down runtime. Default: 180 minutes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#idle_shutdown_timeout GoogleNotebooksRuntime#idle_shutdown_timeout}
        :param install_gpu_driver: Install Nvidia Driver automatically. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#install_gpu_driver GoogleNotebooksRuntime#install_gpu_driver}
        :param kernels: kernels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#kernels GoogleNotebooksRuntime#kernels}
        :param notebook_upgrade_schedule: Cron expression in UTC timezone for schedule instance auto upgrade. Please follow the `cron format <https://en.wikipedia.org/wiki/Cron>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#notebook_upgrade_schedule GoogleNotebooksRuntime#notebook_upgrade_schedule}
        :param post_startup_script: Path to a Bash script that automatically runs after a notebook instance fully boots up. The path must be a URL or Cloud Storage path (gs://path-to-file/file-name). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#post_startup_script GoogleNotebooksRuntime#post_startup_script}
        :param post_startup_script_behavior: Behavior for the post startup script. Possible values: ["POST_STARTUP_SCRIPT_BEHAVIOR_UNSPECIFIED", "RUN_EVERY_START", "DOWNLOAD_AND_RUN_EVERY_START"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#post_startup_script_behavior GoogleNotebooksRuntime#post_startup_script_behavior}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43eb5fb242f21167589124f6aae474161c041ccd495c6668eb275163d96fae1d)
            check_type(argname="argument custom_gpu_driver_path", value=custom_gpu_driver_path, expected_type=type_hints["custom_gpu_driver_path"])
            check_type(argname="argument enable_health_monitoring", value=enable_health_monitoring, expected_type=type_hints["enable_health_monitoring"])
            check_type(argname="argument idle_shutdown", value=idle_shutdown, expected_type=type_hints["idle_shutdown"])
            check_type(argname="argument idle_shutdown_timeout", value=idle_shutdown_timeout, expected_type=type_hints["idle_shutdown_timeout"])
            check_type(argname="argument install_gpu_driver", value=install_gpu_driver, expected_type=type_hints["install_gpu_driver"])
            check_type(argname="argument kernels", value=kernels, expected_type=type_hints["kernels"])
            check_type(argname="argument notebook_upgrade_schedule", value=notebook_upgrade_schedule, expected_type=type_hints["notebook_upgrade_schedule"])
            check_type(argname="argument post_startup_script", value=post_startup_script, expected_type=type_hints["post_startup_script"])
            check_type(argname="argument post_startup_script_behavior", value=post_startup_script_behavior, expected_type=type_hints["post_startup_script_behavior"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_gpu_driver_path is not None:
            self._values["custom_gpu_driver_path"] = custom_gpu_driver_path
        if enable_health_monitoring is not None:
            self._values["enable_health_monitoring"] = enable_health_monitoring
        if idle_shutdown is not None:
            self._values["idle_shutdown"] = idle_shutdown
        if idle_shutdown_timeout is not None:
            self._values["idle_shutdown_timeout"] = idle_shutdown_timeout
        if install_gpu_driver is not None:
            self._values["install_gpu_driver"] = install_gpu_driver
        if kernels is not None:
            self._values["kernels"] = kernels
        if notebook_upgrade_schedule is not None:
            self._values["notebook_upgrade_schedule"] = notebook_upgrade_schedule
        if post_startup_script is not None:
            self._values["post_startup_script"] = post_startup_script
        if post_startup_script_behavior is not None:
            self._values["post_startup_script_behavior"] = post_startup_script_behavior

    @builtins.property
    def custom_gpu_driver_path(self) -> typing.Optional[builtins.str]:
        '''Specify a custom Cloud Storage path where the GPU driver is stored.

        If not specified, we'll automatically choose from official GPU drivers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#custom_gpu_driver_path GoogleNotebooksRuntime#custom_gpu_driver_path}
        '''
        result = self._values.get("custom_gpu_driver_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_health_monitoring(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Verifies core internal services are running. Default: True.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#enable_health_monitoring GoogleNotebooksRuntime#enable_health_monitoring}
        '''
        result = self._values.get("enable_health_monitoring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def idle_shutdown(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Runtime will automatically shutdown after idle_shutdown_time. Default: True.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#idle_shutdown GoogleNotebooksRuntime#idle_shutdown}
        '''
        result = self._values.get("idle_shutdown")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def idle_shutdown_timeout(self) -> typing.Optional[jsii.Number]:
        '''Time in minutes to wait before shuting down runtime. Default: 180 minutes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#idle_shutdown_timeout GoogleNotebooksRuntime#idle_shutdown_timeout}
        '''
        result = self._values.get("idle_shutdown_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def install_gpu_driver(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Install Nvidia Driver automatically.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#install_gpu_driver GoogleNotebooksRuntime#install_gpu_driver}
        '''
        result = self._values.get("install_gpu_driver")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def kernels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNotebooksRuntimeSoftwareConfigKernels"]]]:
        '''kernels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#kernels GoogleNotebooksRuntime#kernels}
        '''
        result = self._values.get("kernels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNotebooksRuntimeSoftwareConfigKernels"]]], result)

    @builtins.property
    def notebook_upgrade_schedule(self) -> typing.Optional[builtins.str]:
        '''Cron expression in UTC timezone for schedule instance auto upgrade. Please follow the `cron format <https://en.wikipedia.org/wiki/Cron>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#notebook_upgrade_schedule GoogleNotebooksRuntime#notebook_upgrade_schedule}
        '''
        result = self._values.get("notebook_upgrade_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_startup_script(self) -> typing.Optional[builtins.str]:
        '''Path to a Bash script that automatically runs after a notebook instance fully boots up.

        The path must be a URL or
        Cloud Storage path (gs://path-to-file/file-name).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#post_startup_script GoogleNotebooksRuntime#post_startup_script}
        '''
        result = self._values.get("post_startup_script")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_startup_script_behavior(self) -> typing.Optional[builtins.str]:
        '''Behavior for the post startup script. Possible values: ["POST_STARTUP_SCRIPT_BEHAVIOR_UNSPECIFIED", "RUN_EVERY_START", "DOWNLOAD_AND_RUN_EVERY_START"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#post_startup_script_behavior GoogleNotebooksRuntime#post_startup_script_behavior}
        '''
        result = self._values.get("post_startup_script_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNotebooksRuntimeSoftwareConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeSoftwareConfigKernels",
    jsii_struct_bases=[],
    name_mapping={"repository": "repository", "tag": "tag"},
)
class GoogleNotebooksRuntimeSoftwareConfigKernels:
    def __init__(
        self,
        *,
        repository: builtins.str,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repository: The path to the container image repository. For example: gcr.io/{project_id}/{imageName}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#repository GoogleNotebooksRuntime#repository}
        :param tag: The tag of the container image. If not specified, this defaults to the latest tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#tag GoogleNotebooksRuntime#tag}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b98d6f91a8d1be54bbf4ba505b819640b68ce67f971078f0de64ebc0d612ae55)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#repository GoogleNotebooksRuntime#repository}
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''The tag of the container image. If not specified, this defaults to the latest tag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#tag GoogleNotebooksRuntime#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNotebooksRuntimeSoftwareConfigKernels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNotebooksRuntimeSoftwareConfigKernelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeSoftwareConfigKernelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e3c6d47bbd6ba6e7c0aa9364f507b390849383faa5829efedd28977949e46cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNotebooksRuntimeSoftwareConfigKernelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0bf10870b43b651bb0a2794766dce97800cdffcbd575950c4590622850011ab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNotebooksRuntimeSoftwareConfigKernelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fd177a81e41d01e39a9e82e37ac7a26e7a823ae8981cd5fac68d973a64d174a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__316591e869501ffddd64042996cbaacf3bdc05508918d8e86f70b63d9afc5abf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c40ec6bcd26ebfdb85faebdf79db3a01ec7bcf463fccb5b4239c56c2d4be0c74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNotebooksRuntimeSoftwareConfigKernels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNotebooksRuntimeSoftwareConfigKernels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNotebooksRuntimeSoftwareConfigKernels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f58c8f8e25ecb04620ef6bc958c6e2a83223acc848beab08c3143fc26801e87e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNotebooksRuntimeSoftwareConfigKernelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeSoftwareConfigKernelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ac21190a4b2461600f0d42e12841b9c8f18eb4b7de6f6a11b95fb0919dd38a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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
            type_hints = typing.get_type_hints(_typecheckingstub__813e289afc5549cf979c81d1759b9488f9e3a3f524e99223c904c244c268ba39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eec9805a2145eefceaeb885b338e275b80894007beffe70f0821b66320d8b988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNotebooksRuntimeSoftwareConfigKernels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNotebooksRuntimeSoftwareConfigKernels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNotebooksRuntimeSoftwareConfigKernels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5ddf7802cc37c96f70871026afcf3cb8626438d3aef21651a4e5d78513a0fbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNotebooksRuntimeSoftwareConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeSoftwareConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00b4f2ccac17691ca4b6b3872cd5946875adc5d783a73ee770c09b19615ba9f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putKernels")
    def put_kernels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNotebooksRuntimeSoftwareConfigKernels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67c2613589cd8a52fe2c0b8f296edb30873795c60a836506597f1aa905cf06a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putKernels", [value]))

    @jsii.member(jsii_name="resetCustomGpuDriverPath")
    def reset_custom_gpu_driver_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomGpuDriverPath", []))

    @jsii.member(jsii_name="resetEnableHealthMonitoring")
    def reset_enable_health_monitoring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableHealthMonitoring", []))

    @jsii.member(jsii_name="resetIdleShutdown")
    def reset_idle_shutdown(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdleShutdown", []))

    @jsii.member(jsii_name="resetIdleShutdownTimeout")
    def reset_idle_shutdown_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdleShutdownTimeout", []))

    @jsii.member(jsii_name="resetInstallGpuDriver")
    def reset_install_gpu_driver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstallGpuDriver", []))

    @jsii.member(jsii_name="resetKernels")
    def reset_kernels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKernels", []))

    @jsii.member(jsii_name="resetNotebookUpgradeSchedule")
    def reset_notebook_upgrade_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotebookUpgradeSchedule", []))

    @jsii.member(jsii_name="resetPostStartupScript")
    def reset_post_startup_script(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostStartupScript", []))

    @jsii.member(jsii_name="resetPostStartupScriptBehavior")
    def reset_post_startup_script_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostStartupScriptBehavior", []))

    @builtins.property
    @jsii.member(jsii_name="kernels")
    def kernels(self) -> GoogleNotebooksRuntimeSoftwareConfigKernelsList:
        return typing.cast(GoogleNotebooksRuntimeSoftwareConfigKernelsList, jsii.get(self, "kernels"))

    @builtins.property
    @jsii.member(jsii_name="upgradeable")
    def upgradeable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "upgradeable"))

    @builtins.property
    @jsii.member(jsii_name="customGpuDriverPathInput")
    def custom_gpu_driver_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customGpuDriverPathInput"))

    @builtins.property
    @jsii.member(jsii_name="enableHealthMonitoringInput")
    def enable_health_monitoring_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableHealthMonitoringInput"))

    @builtins.property
    @jsii.member(jsii_name="idleShutdownInput")
    def idle_shutdown_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "idleShutdownInput"))

    @builtins.property
    @jsii.member(jsii_name="idleShutdownTimeoutInput")
    def idle_shutdown_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "idleShutdownTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="installGpuDriverInput")
    def install_gpu_driver_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "installGpuDriverInput"))

    @builtins.property
    @jsii.member(jsii_name="kernelsInput")
    def kernels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNotebooksRuntimeSoftwareConfigKernels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNotebooksRuntimeSoftwareConfigKernels]]], jsii.get(self, "kernelsInput"))

    @builtins.property
    @jsii.member(jsii_name="notebookUpgradeScheduleInput")
    def notebook_upgrade_schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notebookUpgradeScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="postStartupScriptBehaviorInput")
    def post_startup_script_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postStartupScriptBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="postStartupScriptInput")
    def post_startup_script_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postStartupScriptInput"))

    @builtins.property
    @jsii.member(jsii_name="customGpuDriverPath")
    def custom_gpu_driver_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customGpuDriverPath"))

    @custom_gpu_driver_path.setter
    def custom_gpu_driver_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c70242ac761dae975b117465ca6228e43c3bb4b70bc38780336f45a483f7cb08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customGpuDriverPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableHealthMonitoring")
    def enable_health_monitoring(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableHealthMonitoring"))

    @enable_health_monitoring.setter
    def enable_health_monitoring(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6c3886d37fd61e5ec26b470f6705ee2b4715d3a1cad91b690058303adb675ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableHealthMonitoring", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idleShutdown")
    def idle_shutdown(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "idleShutdown"))

    @idle_shutdown.setter
    def idle_shutdown(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d78a645bfc84d099b37b8eb55c2e3b740fc105fc6fe721c571f457f95c569a74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleShutdown", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idleShutdownTimeout")
    def idle_shutdown_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "idleShutdownTimeout"))

    @idle_shutdown_timeout.setter
    def idle_shutdown_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97f1b72350065e04eabbae0c7f5414164d1bcb42d9f1a9af12243461461103e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleShutdownTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="installGpuDriver")
    def install_gpu_driver(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "installGpuDriver"))

    @install_gpu_driver.setter
    def install_gpu_driver(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe22db4492baf802a00905530b6354d7aa8fa4ddd956876b795efd177539daf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "installGpuDriver", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notebookUpgradeSchedule")
    def notebook_upgrade_schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notebookUpgradeSchedule"))

    @notebook_upgrade_schedule.setter
    def notebook_upgrade_schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d436556529b43b4834bdb100334d70fedfcb763f8a74a7d375d3217e59fa5673)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notebookUpgradeSchedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postStartupScript")
    def post_startup_script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postStartupScript"))

    @post_startup_script.setter
    def post_startup_script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9fe66497a7e101d880f8d474616c4330c07966e6390ed5e16400229d4f1fb75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postStartupScript", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postStartupScriptBehavior")
    def post_startup_script_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postStartupScriptBehavior"))

    @post_startup_script_behavior.setter
    def post_startup_script_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bb0dc82d39da27f70bf427a8cd3042dc0e054f2c58c1d353eebc097335bc20d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postStartupScriptBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleNotebooksRuntimeSoftwareConfig]:
        return typing.cast(typing.Optional[GoogleNotebooksRuntimeSoftwareConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNotebooksRuntimeSoftwareConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87c09ef08bed7f96253c30f609544aff7e46dac079ac55311dfcdf11e7c1aabb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleNotebooksRuntimeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#create GoogleNotebooksRuntime#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#delete GoogleNotebooksRuntime#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#update GoogleNotebooksRuntime#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eae06ed3df479b075b81c1f38233986ec623e3c53114e823947bf7add633ef0)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#create GoogleNotebooksRuntime#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#delete GoogleNotebooksRuntime#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#update GoogleNotebooksRuntime#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNotebooksRuntimeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNotebooksRuntimeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c33d8a1071f628595d54dc799f30246144733ce37df91d8b8de996bcd5a7997b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69b454fe8cd23452ecaea4c1f34e63ab498c7d2209241803efde53ca282270f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c2381423251cb06fd6dd725178f5f1c91d1e259d877b6a6a599d10a92ffcb8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd2385e26d8507de41604dc5c5eb1eb59e5b65605040182e339ef359641f70f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNotebooksRuntimeTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNotebooksRuntimeTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNotebooksRuntimeTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9f01c6dbb77723f9cf052343e12d0124caf15f6b1f134b0e5fdb709fbc13731)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeVirtualMachine",
    jsii_struct_bases=[],
    name_mapping={"virtual_machine_config": "virtualMachineConfig"},
)
class GoogleNotebooksRuntimeVirtualMachine:
    def __init__(
        self,
        *,
        virtual_machine_config: typing.Optional[typing.Union["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param virtual_machine_config: virtual_machine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#virtual_machine_config GoogleNotebooksRuntime#virtual_machine_config}
        '''
        if isinstance(virtual_machine_config, dict):
            virtual_machine_config = GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfig(**virtual_machine_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27d44e8708731e656cef9711870163ea86587eb6e4a9c38b8f6500212c0238c3)
            check_type(argname="argument virtual_machine_config", value=virtual_machine_config, expected_type=type_hints["virtual_machine_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if virtual_machine_config is not None:
            self._values["virtual_machine_config"] = virtual_machine_config

    @builtins.property
    def virtual_machine_config(
        self,
    ) -> typing.Optional["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfig"]:
        '''virtual_machine_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#virtual_machine_config GoogleNotebooksRuntime#virtual_machine_config}
        '''
        result = self._values.get("virtual_machine_config")
        return typing.cast(typing.Optional["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNotebooksRuntimeVirtualMachine(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNotebooksRuntimeVirtualMachineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeVirtualMachineOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1721e82ace880dd48f4f86b01c8e08e023e512888fe63efa89b23dfe6680c732)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVirtualMachineConfig")
    def put_virtual_machine_config(
        self,
        *,
        data_disk: typing.Union["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk", typing.Dict[builtins.str, typing.Any]],
        machine_type: builtins.str,
        accelerator_config: typing.Optional[typing.Union["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        container_images: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryption_config: typing.Optional[typing.Union["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        internal_ip_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network: typing.Optional[builtins.str] = None,
        nic_type: typing.Optional[builtins.str] = None,
        reserved_ip_range: typing.Optional[builtins.str] = None,
        shielded_instance_config: typing.Optional[typing.Union["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        subnet: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param data_disk: data_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#data_disk GoogleNotebooksRuntime#data_disk}
        :param machine_type: The Compute Engine machine type used for runtimes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#machine_type GoogleNotebooksRuntime#machine_type}
        :param accelerator_config: accelerator_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#accelerator_config GoogleNotebooksRuntime#accelerator_config}
        :param container_images: container_images block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#container_images GoogleNotebooksRuntime#container_images}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#encryption_config GoogleNotebooksRuntime#encryption_config}
        :param internal_ip_only: If true, runtime will only have internal IP addresses. By default, runtimes are not restricted to internal IP addresses, and will have ephemeral external IP addresses assigned to each vm. This 'internal_ip_only' restriction can only be enabled for subnetwork enabled networks, and all dependencies must be configured to be accessible without external IP addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#internal_ip_only GoogleNotebooksRuntime#internal_ip_only}
        :param labels: The labels to associate with this runtime. Label **keys** must contain 1 to 63 characters, and must conform to [RFC 1035] (https://www.ietf.org/rfc/rfc1035.txt). Label **values** may be empty, but, if present, must contain 1 to 63 characters, and must conform to `RFC 1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. No more than 32 labels can be associated with a cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#labels GoogleNotebooksRuntime#labels}
        :param metadata: The Compute Engine metadata entries to add to virtual machine. (see [Project and instance metadata](https://cloud.google.com /compute/docs/storing-retrieving-metadata#project_and_instance _metadata)). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#metadata GoogleNotebooksRuntime#metadata}
        :param network: The Compute Engine network to be used for machine communications. Cannot be specified with subnetwork. If neither 'network' nor 'subnet' is specified, the "default" network of the project is used, if it exists. A full URL or partial URI. Examples: - 'https://www.googleapis.com/compute/v1/projects/[project_id]/ regions/global/default' - 'projects/[project_id]/regions/global/default' Runtimes are managed resources inside Google Infrastructure. Runtimes support the following network configurations: - Google Managed Network (Network & subnet are empty) - Consumer Project VPC (network & subnet are required). Requires configuring Private Service Access. - Shared VPC (network & subnet are required). Requires configuring Private Service Access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#network GoogleNotebooksRuntime#network}
        :param nic_type: The type of vNIC to be used on this interface. This may be gVNIC or VirtioNet. Possible values: ["UNSPECIFIED_NIC_TYPE", "VIRTIO_NET", "GVNIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#nic_type GoogleNotebooksRuntime#nic_type}
        :param reserved_ip_range: Reserved IP Range name is used for VPC Peering. The subnetwork allocation will use the range *name* if it's assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#reserved_ip_range GoogleNotebooksRuntime#reserved_ip_range}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#shielded_instance_config GoogleNotebooksRuntime#shielded_instance_config}
        :param subnet: The Compute Engine subnetwork to be used for machine communications. Cannot be specified with network. A full URL or partial URI are valid. Examples: - 'https://www.googleapis.com/compute/v1/projects/[project_id]/ regions/us-east1/subnetworks/sub0' - 'projects/[project_id]/regions/us-east1/subnetworks/sub0' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#subnet GoogleNotebooksRuntime#subnet}
        :param tags: The Compute Engine tags to add to runtime (see [Tagging instances] (https://cloud.google.com/compute/docs/ label-or-tag-resources#tags)). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#tags GoogleNotebooksRuntime#tags}
        '''
        value = GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfig(
            data_disk=data_disk,
            machine_type=machine_type,
            accelerator_config=accelerator_config,
            container_images=container_images,
            encryption_config=encryption_config,
            internal_ip_only=internal_ip_only,
            labels=labels,
            metadata=metadata,
            network=network,
            nic_type=nic_type,
            reserved_ip_range=reserved_ip_range,
            shielded_instance_config=shielded_instance_config,
            subnet=subnet,
            tags=tags,
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualMachineConfig", [value]))

    @jsii.member(jsii_name="resetVirtualMachineConfig")
    def reset_virtual_machine_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualMachineConfig", []))

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @builtins.property
    @jsii.member(jsii_name="instanceName")
    def instance_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceName"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineConfig")
    def virtual_machine_config(
        self,
    ) -> "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigOutputReference":
        return typing.cast("GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigOutputReference", jsii.get(self, "virtualMachineConfig"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineConfigInput")
    def virtual_machine_config_input(
        self,
    ) -> typing.Optional["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfig"]:
        return typing.cast(typing.Optional["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfig"], jsii.get(self, "virtualMachineConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleNotebooksRuntimeVirtualMachine]:
        return typing.cast(typing.Optional[GoogleNotebooksRuntimeVirtualMachine], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNotebooksRuntimeVirtualMachine],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__959925c8929e620e6e7d5378fe0c4a450eb8f0122e0fb0fd9cbc3c076b10fd1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfig",
    jsii_struct_bases=[],
    name_mapping={
        "data_disk": "dataDisk",
        "machine_type": "machineType",
        "accelerator_config": "acceleratorConfig",
        "container_images": "containerImages",
        "encryption_config": "encryptionConfig",
        "internal_ip_only": "internalIpOnly",
        "labels": "labels",
        "metadata": "metadata",
        "network": "network",
        "nic_type": "nicType",
        "reserved_ip_range": "reservedIpRange",
        "shielded_instance_config": "shieldedInstanceConfig",
        "subnet": "subnet",
        "tags": "tags",
    },
)
class GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfig:
    def __init__(
        self,
        *,
        data_disk: typing.Union["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk", typing.Dict[builtins.str, typing.Any]],
        machine_type: builtins.str,
        accelerator_config: typing.Optional[typing.Union["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        container_images: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryption_config: typing.Optional[typing.Union["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        internal_ip_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network: typing.Optional[builtins.str] = None,
        nic_type: typing.Optional[builtins.str] = None,
        reserved_ip_range: typing.Optional[builtins.str] = None,
        shielded_instance_config: typing.Optional[typing.Union["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        subnet: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param data_disk: data_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#data_disk GoogleNotebooksRuntime#data_disk}
        :param machine_type: The Compute Engine machine type used for runtimes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#machine_type GoogleNotebooksRuntime#machine_type}
        :param accelerator_config: accelerator_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#accelerator_config GoogleNotebooksRuntime#accelerator_config}
        :param container_images: container_images block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#container_images GoogleNotebooksRuntime#container_images}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#encryption_config GoogleNotebooksRuntime#encryption_config}
        :param internal_ip_only: If true, runtime will only have internal IP addresses. By default, runtimes are not restricted to internal IP addresses, and will have ephemeral external IP addresses assigned to each vm. This 'internal_ip_only' restriction can only be enabled for subnetwork enabled networks, and all dependencies must be configured to be accessible without external IP addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#internal_ip_only GoogleNotebooksRuntime#internal_ip_only}
        :param labels: The labels to associate with this runtime. Label **keys** must contain 1 to 63 characters, and must conform to [RFC 1035] (https://www.ietf.org/rfc/rfc1035.txt). Label **values** may be empty, but, if present, must contain 1 to 63 characters, and must conform to `RFC 1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. No more than 32 labels can be associated with a cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#labels GoogleNotebooksRuntime#labels}
        :param metadata: The Compute Engine metadata entries to add to virtual machine. (see [Project and instance metadata](https://cloud.google.com /compute/docs/storing-retrieving-metadata#project_and_instance _metadata)). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#metadata GoogleNotebooksRuntime#metadata}
        :param network: The Compute Engine network to be used for machine communications. Cannot be specified with subnetwork. If neither 'network' nor 'subnet' is specified, the "default" network of the project is used, if it exists. A full URL or partial URI. Examples: - 'https://www.googleapis.com/compute/v1/projects/[project_id]/ regions/global/default' - 'projects/[project_id]/regions/global/default' Runtimes are managed resources inside Google Infrastructure. Runtimes support the following network configurations: - Google Managed Network (Network & subnet are empty) - Consumer Project VPC (network & subnet are required). Requires configuring Private Service Access. - Shared VPC (network & subnet are required). Requires configuring Private Service Access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#network GoogleNotebooksRuntime#network}
        :param nic_type: The type of vNIC to be used on this interface. This may be gVNIC or VirtioNet. Possible values: ["UNSPECIFIED_NIC_TYPE", "VIRTIO_NET", "GVNIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#nic_type GoogleNotebooksRuntime#nic_type}
        :param reserved_ip_range: Reserved IP Range name is used for VPC Peering. The subnetwork allocation will use the range *name* if it's assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#reserved_ip_range GoogleNotebooksRuntime#reserved_ip_range}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#shielded_instance_config GoogleNotebooksRuntime#shielded_instance_config}
        :param subnet: The Compute Engine subnetwork to be used for machine communications. Cannot be specified with network. A full URL or partial URI are valid. Examples: - 'https://www.googleapis.com/compute/v1/projects/[project_id]/ regions/us-east1/subnetworks/sub0' - 'projects/[project_id]/regions/us-east1/subnetworks/sub0' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#subnet GoogleNotebooksRuntime#subnet}
        :param tags: The Compute Engine tags to add to runtime (see [Tagging instances] (https://cloud.google.com/compute/docs/ label-or-tag-resources#tags)). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#tags GoogleNotebooksRuntime#tags}
        '''
        if isinstance(data_disk, dict):
            data_disk = GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk(**data_disk)
        if isinstance(accelerator_config, dict):
            accelerator_config = GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig(**accelerator_config)
        if isinstance(encryption_config, dict):
            encryption_config = GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig(**encryption_config)
        if isinstance(shielded_instance_config, dict):
            shielded_instance_config = GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig(**shielded_instance_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__308814d450cde56f771c8e9b6a26af0c6505d65e0df61fff589942fa0a3b102e)
            check_type(argname="argument data_disk", value=data_disk, expected_type=type_hints["data_disk"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument accelerator_config", value=accelerator_config, expected_type=type_hints["accelerator_config"])
            check_type(argname="argument container_images", value=container_images, expected_type=type_hints["container_images"])
            check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            check_type(argname="argument internal_ip_only", value=internal_ip_only, expected_type=type_hints["internal_ip_only"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument nic_type", value=nic_type, expected_type=type_hints["nic_type"])
            check_type(argname="argument reserved_ip_range", value=reserved_ip_range, expected_type=type_hints["reserved_ip_range"])
            check_type(argname="argument shielded_instance_config", value=shielded_instance_config, expected_type=type_hints["shielded_instance_config"])
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_disk": data_disk,
            "machine_type": machine_type,
        }
        if accelerator_config is not None:
            self._values["accelerator_config"] = accelerator_config
        if container_images is not None:
            self._values["container_images"] = container_images
        if encryption_config is not None:
            self._values["encryption_config"] = encryption_config
        if internal_ip_only is not None:
            self._values["internal_ip_only"] = internal_ip_only
        if labels is not None:
            self._values["labels"] = labels
        if metadata is not None:
            self._values["metadata"] = metadata
        if network is not None:
            self._values["network"] = network
        if nic_type is not None:
            self._values["nic_type"] = nic_type
        if reserved_ip_range is not None:
            self._values["reserved_ip_range"] = reserved_ip_range
        if shielded_instance_config is not None:
            self._values["shielded_instance_config"] = shielded_instance_config
        if subnet is not None:
            self._values["subnet"] = subnet
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def data_disk(
        self,
    ) -> "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk":
        '''data_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#data_disk GoogleNotebooksRuntime#data_disk}
        '''
        result = self._values.get("data_disk")
        assert result is not None, "Required property 'data_disk' is missing"
        return typing.cast("GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk", result)

    @builtins.property
    def machine_type(self) -> builtins.str:
        '''The Compute Engine machine type used for runtimes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#machine_type GoogleNotebooksRuntime#machine_type}
        '''
        result = self._values.get("machine_type")
        assert result is not None, "Required property 'machine_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accelerator_config(
        self,
    ) -> typing.Optional["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig"]:
        '''accelerator_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#accelerator_config GoogleNotebooksRuntime#accelerator_config}
        '''
        result = self._values.get("accelerator_config")
        return typing.cast(typing.Optional["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig"], result)

    @builtins.property
    def container_images(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages"]]]:
        '''container_images block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#container_images GoogleNotebooksRuntime#container_images}
        '''
        result = self._values.get("container_images")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages"]]], result)

    @builtins.property
    def encryption_config(
        self,
    ) -> typing.Optional["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig"]:
        '''encryption_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#encryption_config GoogleNotebooksRuntime#encryption_config}
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig"], result)

    @builtins.property
    def internal_ip_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, runtime will only have internal IP addresses.

        By default,
        runtimes are not restricted to internal IP addresses, and will
        have ephemeral external IP addresses assigned to each vm. This
        'internal_ip_only' restriction can only be enabled for subnetwork
        enabled networks, and all dependencies must be configured to be
        accessible without external IP addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#internal_ip_only GoogleNotebooksRuntime#internal_ip_only}
        '''
        result = self._values.get("internal_ip_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The labels to associate with this runtime.

        Label **keys** must
        contain 1 to 63 characters, and must conform to [RFC 1035]
        (https://www.ietf.org/rfc/rfc1035.txt). Label **values** may be
        empty, but, if present, must contain 1 to 63 characters, and must
        conform to `RFC 1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. No
        more than 32 labels can be associated with a cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#labels GoogleNotebooksRuntime#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The Compute Engine metadata entries to add to virtual machine. (see [Project and instance metadata](https://cloud.google.com /compute/docs/storing-retrieving-metadata#project_and_instance _metadata)).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#metadata GoogleNotebooksRuntime#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine network to be used for machine communications.

        Cannot be specified with subnetwork. If neither 'network' nor
        'subnet' is specified, the "default" network of the project is
        used, if it exists. A full URL or partial URI. Examples:

        - 'https://www.googleapis.com/compute/v1/projects/[project_id]/
          regions/global/default'
        - 'projects/[project_id]/regions/global/default'
          Runtimes are managed resources inside Google Infrastructure.
          Runtimes support the following network configurations:
        - Google Managed Network (Network & subnet are empty)
        - Consumer Project VPC (network & subnet are required). Requires
          configuring Private Service Access.
        - Shared VPC (network & subnet are required). Requires
          configuring Private Service Access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#network GoogleNotebooksRuntime#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nic_type(self) -> typing.Optional[builtins.str]:
        '''The type of vNIC to be used on this interface.

        This may be gVNIC
        or VirtioNet. Possible values: ["UNSPECIFIED_NIC_TYPE", "VIRTIO_NET", "GVNIC"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#nic_type GoogleNotebooksRuntime#nic_type}
        '''
        result = self._values.get("nic_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reserved_ip_range(self) -> typing.Optional[builtins.str]:
        '''Reserved IP Range name is used for VPC Peering. The subnetwork allocation will use the range *name* if it's assigned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#reserved_ip_range GoogleNotebooksRuntime#reserved_ip_range}
        '''
        result = self._values.get("reserved_ip_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shielded_instance_config(
        self,
    ) -> typing.Optional["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig"]:
        '''shielded_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#shielded_instance_config GoogleNotebooksRuntime#shielded_instance_config}
        '''
        result = self._values.get("shielded_instance_config")
        return typing.cast(typing.Optional["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig"], result)

    @builtins.property
    def subnet(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine subnetwork to be used for machine communications.

        Cannot be specified with network. A full URL or
        partial URI are valid. Examples:

        - 'https://www.googleapis.com/compute/v1/projects/[project_id]/
          regions/us-east1/subnetworks/sub0'
        - 'projects/[project_id]/regions/us-east1/subnetworks/sub0'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#subnet GoogleNotebooksRuntime#subnet}
        '''
        result = self._values.get("subnet")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Compute Engine tags to add to runtime (see [Tagging instances] (https://cloud.google.com/compute/docs/ label-or-tag-resources#tags)).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#tags GoogleNotebooksRuntime#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig",
    jsii_struct_bases=[],
    name_mapping={"core_count": "coreCount", "type": "type"},
)
class GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig:
    def __init__(
        self,
        *,
        core_count: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param core_count: Count of cores of this accelerator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#core_count GoogleNotebooksRuntime#core_count}
        :param type: Accelerator model. For valid values, see 'https://cloud.google.com/vertex-ai/docs/workbench/reference/ rest/v1/projects.locations.runtimes#AcceleratorType'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#type GoogleNotebooksRuntime#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa12cb61c0e29d4ec1b2afb893324bc1c5b4f0cc45682f339949efe0470fe36a)
            check_type(argname="argument core_count", value=core_count, expected_type=type_hints["core_count"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if core_count is not None:
            self._values["core_count"] = core_count
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def core_count(self) -> typing.Optional[jsii.Number]:
        '''Count of cores of this accelerator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#core_count GoogleNotebooksRuntime#core_count}
        '''
        result = self._values.get("core_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Accelerator model. For valid values, see 'https://cloud.google.com/vertex-ai/docs/workbench/reference/ rest/v1/projects.locations.runtimes#AcceleratorType'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#type GoogleNotebooksRuntime#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__917c0780bfc0bf3496654ce57d2cd21db463feaaa9f8226effc29381e5eed01b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCoreCount")
    def reset_core_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoreCount", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="coreCountInput")
    def core_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "coreCountInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="coreCount")
    def core_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "coreCount"))

    @core_count.setter
    def core_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b147d82d6dce94e68dcd261f9df2f2916a00314398b84460615acc5f752be986)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coreCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16deb3f3a641ba03a7f7b7ddcbf0d69b79bc3f8c00650c239d06a8206c3dcf82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig]:
        return typing.cast(typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb4a88ba44737ba9bce60971e16121d1404a75da0e8ad8e8e9913819b7d038d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages",
    jsii_struct_bases=[],
    name_mapping={"repository": "repository", "tag": "tag"},
)
class GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages:
    def __init__(
        self,
        *,
        repository: builtins.str,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repository: The path to the container image repository. For example: gcr.io/{project_id}/{imageName}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#repository GoogleNotebooksRuntime#repository}
        :param tag: The tag of the container image. If not specified, this defaults to the latest tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#tag GoogleNotebooksRuntime#tag}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a0fdf1d779ddc4c34ac8c1ea3c7094c7144b3436df954db13f3a1321d8aad3c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#repository GoogleNotebooksRuntime#repository}
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''The tag of the container image. If not specified, this defaults to the latest tag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#tag GoogleNotebooksRuntime#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75d927bfd7c17e06d4ec2f7bbcd3fb9100ff2ce9761a8e974ecff2945fb3160d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87367ea174b986055b6b4eed2fda6a89daad061c9c26d31d3a2a41b6d0464e6c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07272dad45028b5d38fb2919a62b2cafdbdb212c59eba1610e55706698dfab59)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bce3d13842ac6a71dbf8c5ef4f055419ac8ec3842d179b28b40191161d17106)
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
            type_hints = typing.get_type_hints(_typecheckingstub__466466876585f351c8c397ec4c6fb47c4c2536fb5106cd242ded709acb727cbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__301c693a728daf80e373b13426dc7c9df27d7a7e25600c32cdbdfd0e23c95b71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26ce2de6f94598b86f6714abb54af915cab93a20fbac8513b8587af55c8b2ba4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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
            type_hints = typing.get_type_hints(_typecheckingstub__af94ca2f027734989a7968034a8344af1d9c611d552ddfa77153ee5457b8ce45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ea7eca860e0e56345d1d11bb3883b2485f5df2608fa4a52df6c95952c8b7d95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afcf2cf25c8beda29fdea75cf50fdd6ad4a14b4297ddbf0990d47ed254e11478)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk",
    jsii_struct_bases=[],
    name_mapping={
        "initialize_params": "initializeParams",
        "interface": "interface",
        "mode": "mode",
        "source": "source",
        "type": "type",
    },
)
class GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk:
    def __init__(
        self,
        *,
        initialize_params: typing.Optional[typing.Union["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams", typing.Dict[builtins.str, typing.Any]]] = None,
        interface: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param initialize_params: initialize_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#initialize_params GoogleNotebooksRuntime#initialize_params}
        :param interface: "Specifies the disk interface to use for attaching this disk, which is either SCSI or NVME. The default is SCSI. Persistent disks must always use SCSI and the request will fail if you attempt to attach a persistent disk in any other format than SCSI. Local SSDs can use either NVME or SCSI. For performance characteristics of SCSI over NVMe, see Local SSD performance. Valid values: * NVME * SCSI". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#interface GoogleNotebooksRuntime#interface}
        :param mode: The mode in which to attach this disk, either READ_WRITE or READ_ONLY. If not specified, the default is to attach the disk in READ_WRITE mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#mode GoogleNotebooksRuntime#mode}
        :param source: Specifies a valid partial or full URL to an existing Persistent Disk resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#source GoogleNotebooksRuntime#source}
        :param type: Specifies the type of the disk, either SCRATCH or PERSISTENT. If not specified, the default is PERSISTENT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#type GoogleNotebooksRuntime#type}
        '''
        if isinstance(initialize_params, dict):
            initialize_params = GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams(**initialize_params)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__712c88c3b9b6da005c696ca7b35c362805aeba43ff434826417442ce26ad05fb)
            check_type(argname="argument initialize_params", value=initialize_params, expected_type=type_hints["initialize_params"])
            check_type(argname="argument interface", value=interface, expected_type=type_hints["interface"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if initialize_params is not None:
            self._values["initialize_params"] = initialize_params
        if interface is not None:
            self._values["interface"] = interface
        if mode is not None:
            self._values["mode"] = mode
        if source is not None:
            self._values["source"] = source
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def initialize_params(
        self,
    ) -> typing.Optional["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams"]:
        '''initialize_params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#initialize_params GoogleNotebooksRuntime#initialize_params}
        '''
        result = self._values.get("initialize_params")
        return typing.cast(typing.Optional["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams"], result)

    @builtins.property
    def interface(self) -> typing.Optional[builtins.str]:
        '''"Specifies the disk interface to use for attaching this disk, which is either SCSI or NVME.

        The default is SCSI. Persistent
        disks must always use SCSI and the request will fail if you attempt
        to attach a persistent disk in any other format than SCSI. Local SSDs
        can use either NVME or SCSI. For performance characteristics of SCSI
        over NVMe, see Local SSD performance. Valid values: * NVME * SCSI".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#interface GoogleNotebooksRuntime#interface}
        '''
        result = self._values.get("interface")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''The mode in which to attach this disk, either READ_WRITE or READ_ONLY.

        If not specified, the default is to attach
        the disk in READ_WRITE mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#mode GoogleNotebooksRuntime#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Specifies a valid partial or full URL to an existing Persistent Disk resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#source GoogleNotebooksRuntime#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of the disk, either SCRATCH or PERSISTENT. If not specified, the default is PERSISTENT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#type GoogleNotebooksRuntime#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "disk_name": "diskName",
        "disk_size_gb": "diskSizeGb",
        "disk_type": "diskType",
        "labels": "labels",
    },
)
class GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        disk_name: typing.Optional[builtins.str] = None,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        disk_type: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param description: Provide this property when creating the disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#description GoogleNotebooksRuntime#description}
        :param disk_name: Specifies the disk name. If not specified, the default is to use the name of the instance. If the disk with the instance name exists already in the given zone/region, a new name will be automatically generated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#disk_name GoogleNotebooksRuntime#disk_name}
        :param disk_size_gb: Specifies the size of the disk in base-2 GB. If not specified, the disk will be the same size as the image (usually 10GB). If specified, the size must be equal to or larger than 10GB. Default 100 GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#disk_size_gb GoogleNotebooksRuntime#disk_size_gb}
        :param disk_type: The type of the boot disk attached to this runtime, defaults to standard persistent disk. For valid values, see 'https://cloud.google.com/vertex-ai/docs/workbench/ reference/rest/v1/projects.locations.runtimes#disktype'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#disk_type GoogleNotebooksRuntime#disk_type}
        :param labels: Labels to apply to this disk. These can be later modified by the disks.setLabels method. This field is only applicable for persistent disks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#labels GoogleNotebooksRuntime#labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77d816422b1e6f1ff9d1677f1e80f4790b6431f40b00de858cee524eb13b25e1)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disk_name", value=disk_name, expected_type=type_hints["disk_name"])
            check_type(argname="argument disk_size_gb", value=disk_size_gb, expected_type=type_hints["disk_size_gb"])
            check_type(argname="argument disk_type", value=disk_type, expected_type=type_hints["disk_type"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if disk_name is not None:
            self._values["disk_name"] = disk_name
        if disk_size_gb is not None:
            self._values["disk_size_gb"] = disk_size_gb
        if disk_type is not None:
            self._values["disk_type"] = disk_type
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Provide this property when creating the disk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#description GoogleNotebooksRuntime#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the disk name.

        If not specified, the default is
        to use the name of the instance. If the disk with the
        instance name exists already in the given zone/region, a
        new name will be automatically generated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#disk_name GoogleNotebooksRuntime#disk_name}
        '''
        result = self._values.get("disk_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Specifies the size of the disk in base-2 GB.

        If not
        specified, the disk will be the same size as the image
        (usually 10GB). If specified, the size must be equal to
        or larger than 10GB. Default 100 GB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#disk_size_gb GoogleNotebooksRuntime#disk_size_gb}
        '''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_type(self) -> typing.Optional[builtins.str]:
        '''The type of the boot disk attached to this runtime, defaults to standard persistent disk. For valid values, see 'https://cloud.google.com/vertex-ai/docs/workbench/ reference/rest/v1/projects.locations.runtimes#disktype'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#disk_type GoogleNotebooksRuntime#disk_type}
        '''
        result = self._values.get("disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels to apply to this disk.

        These can be later modified
        by the disks.setLabels method. This field is only
        applicable for persistent disks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#labels GoogleNotebooksRuntime#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80d2dca9ce359f32f652ccdeb62b6a35f2175a03d29817ba97fc7c131254e11a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDiskName")
    def reset_disk_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskName", []))

    @jsii.member(jsii_name="resetDiskSizeGb")
    def reset_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskSizeGb", []))

    @jsii.member(jsii_name="resetDiskType")
    def reset_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskType", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="diskNameInput")
    def disk_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskNameInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGbInput")
    def disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="diskTypeInput")
    def disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50cefdec72d56d69db1dd4e8d813a49e865f5428ce0f385176c4faaae42ad2c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskName")
    def disk_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskName"))

    @disk_name.setter
    def disk_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58c6f8711b6b957c5e8d3f8291a468d6bc28472b83833c53681b1abac7282ae5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39c43b8ebcb8bac6f38bab6d5ed8c40f890d7670a5b3f65a56048af59621036d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskType")
    def disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskType"))

    @disk_type.setter
    def disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39aeff20c9eb846437d8a35d18b06933adf888cac89f7f8c2f300fddcb23148b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e6bfc21239f76a73b6cb690fa17e9e4324753db44c3f8c2ff2a9030443f1288)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams]:
        return typing.cast(typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__036f5c6fb99927df0e4abfe16356ed7194a49562d6fc45e3f621ae2b805bdfa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42c2c9313a149aea3295a056a82d3d9130ea847ed23bb3b30fbbf3592eafa9cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInitializeParams")
    def put_initialize_params(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        disk_name: typing.Optional[builtins.str] = None,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        disk_type: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param description: Provide this property when creating the disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#description GoogleNotebooksRuntime#description}
        :param disk_name: Specifies the disk name. If not specified, the default is to use the name of the instance. If the disk with the instance name exists already in the given zone/region, a new name will be automatically generated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#disk_name GoogleNotebooksRuntime#disk_name}
        :param disk_size_gb: Specifies the size of the disk in base-2 GB. If not specified, the disk will be the same size as the image (usually 10GB). If specified, the size must be equal to or larger than 10GB. Default 100 GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#disk_size_gb GoogleNotebooksRuntime#disk_size_gb}
        :param disk_type: The type of the boot disk attached to this runtime, defaults to standard persistent disk. For valid values, see 'https://cloud.google.com/vertex-ai/docs/workbench/ reference/rest/v1/projects.locations.runtimes#disktype'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#disk_type GoogleNotebooksRuntime#disk_type}
        :param labels: Labels to apply to this disk. These can be later modified by the disks.setLabels method. This field is only applicable for persistent disks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#labels GoogleNotebooksRuntime#labels}
        '''
        value = GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams(
            description=description,
            disk_name=disk_name,
            disk_size_gb=disk_size_gb,
            disk_type=disk_type,
            labels=labels,
        )

        return typing.cast(None, jsii.invoke(self, "putInitializeParams", [value]))

    @jsii.member(jsii_name="resetInitializeParams")
    def reset_initialize_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitializeParams", []))

    @jsii.member(jsii_name="resetInterface")
    def reset_interface(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterface", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="autoDelete")
    def auto_delete(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "autoDelete"))

    @builtins.property
    @jsii.member(jsii_name="boot")
    def boot(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "boot"))

    @builtins.property
    @jsii.member(jsii_name="deviceName")
    def device_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceName"))

    @builtins.property
    @jsii.member(jsii_name="guestOsFeatures")
    def guest_os_features(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "guestOsFeatures"))

    @builtins.property
    @jsii.member(jsii_name="index")
    def index(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "index"))

    @builtins.property
    @jsii.member(jsii_name="initializeParams")
    def initialize_params(
        self,
    ) -> GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParamsOutputReference:
        return typing.cast(GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParamsOutputReference, jsii.get(self, "initializeParams"))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @builtins.property
    @jsii.member(jsii_name="licenses")
    def licenses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "licenses"))

    @builtins.property
    @jsii.member(jsii_name="initializeParamsInput")
    def initialize_params_input(
        self,
    ) -> typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams]:
        return typing.cast(typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams], jsii.get(self, "initializeParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="interfaceInput")
    def interface_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interfaceInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="interface")
    def interface(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interface"))

    @interface.setter
    def interface(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b996135344f61f0550ac55b66530a25087bfe3e1b2faab670510ab6f3053688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interface", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9892bab905c9bd5be820197c73a45e624362baf0e5edf2c7c980c91725cadc86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8c91dfb080152c99c5af15c90e7a51fc8ec57290ed46cc15c32cdae37fc341e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__460aff7005e9d4a8bfe610d5b41cbd594e7618d23ade787d53f211570c0819ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk]:
        return typing.cast(typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca21ce2c87cf57742681d0891581b2d3967ab231a33a25279a30f3f4fe7aeb74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig",
    jsii_struct_bases=[],
    name_mapping={"kms_key": "kmsKey"},
)
class GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig:
    def __init__(self, *, kms_key: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key: The Cloud KMS resource identifier of the customer-managed encryption key used to protect a resource, such as a disks. It has the following format: 'projects/{PROJECT_ID}/locations/{REGION}/keyRings/ {KEY_RING_NAME}/cryptoKeys/{KEY_NAME}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#kms_key GoogleNotebooksRuntime#kms_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63ecd5795655e113191546162d6f516270a8626b8efa0c804d38e7c5cfca3646)
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The Cloud KMS resource identifier of the customer-managed encryption key used to protect a resource, such as a disks.

        It has the following format:
        'projects/{PROJECT_ID}/locations/{REGION}/keyRings/
        {KEY_RING_NAME}/cryptoKeys/{KEY_NAME}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#kms_key GoogleNotebooksRuntime#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca27ae79707770a03b2acfec13ffe1d855a092803cef0989948ce7dcdfa7bbef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bc839e6b0ab22754d069fa2e516e866412a2cd6f7faea21a3b6a12be298beb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig]:
        return typing.cast(typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9300fd54f9414ed8e4b8babaac93760d3df04769918fdf9657bcca8681fe24fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa3f62e57bba57ae146639517c028b9b4595fee86a61b80f0b590b813b24dcc1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAcceleratorConfig")
    def put_accelerator_config(
        self,
        *,
        core_count: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param core_count: Count of cores of this accelerator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#core_count GoogleNotebooksRuntime#core_count}
        :param type: Accelerator model. For valid values, see 'https://cloud.google.com/vertex-ai/docs/workbench/reference/ rest/v1/projects.locations.runtimes#AcceleratorType'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#type GoogleNotebooksRuntime#type}
        '''
        value = GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig(
            core_count=core_count, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putAcceleratorConfig", [value]))

    @jsii.member(jsii_name="putContainerImages")
    def put_container_images(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21ae080cdaf10efbec436b771898a43d5e4826f804662c5e0ca32802fbfcec98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContainerImages", [value]))

    @jsii.member(jsii_name="putDataDisk")
    def put_data_disk(
        self,
        *,
        initialize_params: typing.Optional[typing.Union[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams, typing.Dict[builtins.str, typing.Any]]] = None,
        interface: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param initialize_params: initialize_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#initialize_params GoogleNotebooksRuntime#initialize_params}
        :param interface: "Specifies the disk interface to use for attaching this disk, which is either SCSI or NVME. The default is SCSI. Persistent disks must always use SCSI and the request will fail if you attempt to attach a persistent disk in any other format than SCSI. Local SSDs can use either NVME or SCSI. For performance characteristics of SCSI over NVMe, see Local SSD performance. Valid values: * NVME * SCSI". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#interface GoogleNotebooksRuntime#interface}
        :param mode: The mode in which to attach this disk, either READ_WRITE or READ_ONLY. If not specified, the default is to attach the disk in READ_WRITE mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#mode GoogleNotebooksRuntime#mode}
        :param source: Specifies a valid partial or full URL to an existing Persistent Disk resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#source GoogleNotebooksRuntime#source}
        :param type: Specifies the type of the disk, either SCRATCH or PERSISTENT. If not specified, the default is PERSISTENT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#type GoogleNotebooksRuntime#type}
        '''
        value = GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk(
            initialize_params=initialize_params,
            interface=interface,
            mode=mode,
            source=source,
            type=type,
        )

        return typing.cast(None, jsii.invoke(self, "putDataDisk", [value]))

    @jsii.member(jsii_name="putEncryptionConfig")
    def put_encryption_config(
        self,
        *,
        kms_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key: The Cloud KMS resource identifier of the customer-managed encryption key used to protect a resource, such as a disks. It has the following format: 'projects/{PROJECT_ID}/locations/{REGION}/keyRings/ {KEY_RING_NAME}/cryptoKeys/{KEY_NAME}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#kms_key GoogleNotebooksRuntime#kms_key}
        '''
        value = GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig(
            kms_key=kms_key
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfig", [value]))

    @jsii.member(jsii_name="putShieldedInstanceConfig")
    def put_shielded_instance_config(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Defines whether the instance has integrity monitoring enabled. Enables monitoring and attestation of the boot integrity of the instance. The attestation is performed against the integrity policy baseline. This baseline is initially derived from the implicitly trusted boot image when the instance is created. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#enable_integrity_monitoring GoogleNotebooksRuntime#enable_integrity_monitoring}
        :param enable_secure_boot: Defines whether the instance has Secure Boot enabled.Secure Boot helps ensure that the system only runs authentic software by verifying the digital signature of all boot components, and halting the boot process if signature verification fails. Disabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#enable_secure_boot GoogleNotebooksRuntime#enable_secure_boot}
        :param enable_vtpm: Defines whether the instance has the vTPM enabled. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#enable_vtpm GoogleNotebooksRuntime#enable_vtpm}
        '''
        value = GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig(
            enable_integrity_monitoring=enable_integrity_monitoring,
            enable_secure_boot=enable_secure_boot,
            enable_vtpm=enable_vtpm,
        )

        return typing.cast(None, jsii.invoke(self, "putShieldedInstanceConfig", [value]))

    @jsii.member(jsii_name="resetAcceleratorConfig")
    def reset_accelerator_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorConfig", []))

    @jsii.member(jsii_name="resetContainerImages")
    def reset_container_images(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerImages", []))

    @jsii.member(jsii_name="resetEncryptionConfig")
    def reset_encryption_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfig", []))

    @jsii.member(jsii_name="resetInternalIpOnly")
    def reset_internal_ip_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternalIpOnly", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetNicType")
    def reset_nic_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNicType", []))

    @jsii.member(jsii_name="resetReservedIpRange")
    def reset_reserved_ip_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservedIpRange", []))

    @jsii.member(jsii_name="resetShieldedInstanceConfig")
    def reset_shielded_instance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShieldedInstanceConfig", []))

    @jsii.member(jsii_name="resetSubnet")
    def reset_subnet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnet", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @builtins.property
    @jsii.member(jsii_name="acceleratorConfig")
    def accelerator_config(
        self,
    ) -> GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfigOutputReference:
        return typing.cast(GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfigOutputReference, jsii.get(self, "acceleratorConfig"))

    @builtins.property
    @jsii.member(jsii_name="containerImages")
    def container_images(
        self,
    ) -> GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImagesList:
        return typing.cast(GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImagesList, jsii.get(self, "containerImages"))

    @builtins.property
    @jsii.member(jsii_name="dataDisk")
    def data_disk(
        self,
    ) -> GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskOutputReference:
        return typing.cast(GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskOutputReference, jsii.get(self, "dataDisk"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfig")
    def encryption_config(
        self,
    ) -> GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfigOutputReference:
        return typing.cast(GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfigOutputReference, jsii.get(self, "encryptionConfig"))

    @builtins.property
    @jsii.member(jsii_name="guestAttributes")
    def guest_attributes(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "guestAttributes"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfig")
    def shielded_instance_config(
        self,
    ) -> "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfigOutputReference":
        return typing.cast("GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfigOutputReference", jsii.get(self, "shieldedInstanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorConfigInput")
    def accelerator_config_input(
        self,
    ) -> typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig]:
        return typing.cast(typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig], jsii.get(self, "acceleratorConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="containerImagesInput")
    def container_images_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages]]], jsii.get(self, "containerImagesInput"))

    @builtins.property
    @jsii.member(jsii_name="dataDiskInput")
    def data_disk_input(
        self,
    ) -> typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk]:
        return typing.cast(typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk], jsii.get(self, "dataDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigInput")
    def encryption_config_input(
        self,
    ) -> typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig]:
        return typing.cast(typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig], jsii.get(self, "encryptionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalIpOnlyInput")
    def internal_ip_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalIpOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

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
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="nicTypeInput")
    def nic_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nicTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="reservedIpRangeInput")
    def reserved_ip_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reservedIpRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfigInput")
    def shielded_instance_config_input(
        self,
    ) -> typing.Optional["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig"]:
        return typing.cast(typing.Optional["GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig"], jsii.get(self, "shieldedInstanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetInput")
    def subnet_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalIpOnly")
    def internal_ip_only(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "internalIpOnly"))

    @internal_ip_only.setter
    def internal_ip_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6aa0f9d6ce3099afe0a8dc97d4b06f3759c817d2de2a1d29a9fbd05c25d699d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalIpOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64379c562482756ab487030f117301df6ea8651ed83ec90f822f9596e5d31604)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f783f2187ab2cac67b7156fbb90619c22da29542e345c98cafe468df0f50a32a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c770374023378e6234e08b89ac4c06569060902a7cbf76d58b1edbda9ac85a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e80f6c3452903afa2d11129a0006e2f4d7ee5d1a36f415cbd15788282e8fbdb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nicType")
    def nic_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nicType"))

    @nic_type.setter
    def nic_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b392f51d208111b2ddcd28b6a7e5962010b3fd5131a0f754086613a560a24ec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nicType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reservedIpRange")
    def reserved_ip_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reservedIpRange"))

    @reserved_ip_range.setter
    def reserved_ip_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52a1aab2fc93230ba2acd274269a6604cb0315f08c4b283af2104764ef13811c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservedIpRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnet")
    def subnet(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnet"))

    @subnet.setter
    def subnet(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df70cffa5c8502e993b0afb4aceaece881ad95649f0f1a2ba08d8b127f45ad28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f48fd0417dad4bc94e89173340bcab5ce255c93f9d66a9b31c8fca9030381561)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfig]:
        return typing.cast(typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f32ebf82a18d94e77f613639049e2a65c438cf7b745260880be44ae7fd5fb7a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_integrity_monitoring": "enableIntegrityMonitoring",
        "enable_secure_boot": "enableSecureBoot",
        "enable_vtpm": "enableVtpm",
    },
)
class GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig:
    def __init__(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Defines whether the instance has integrity monitoring enabled. Enables monitoring and attestation of the boot integrity of the instance. The attestation is performed against the integrity policy baseline. This baseline is initially derived from the implicitly trusted boot image when the instance is created. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#enable_integrity_monitoring GoogleNotebooksRuntime#enable_integrity_monitoring}
        :param enable_secure_boot: Defines whether the instance has Secure Boot enabled.Secure Boot helps ensure that the system only runs authentic software by verifying the digital signature of all boot components, and halting the boot process if signature verification fails. Disabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#enable_secure_boot GoogleNotebooksRuntime#enable_secure_boot}
        :param enable_vtpm: Defines whether the instance has the vTPM enabled. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#enable_vtpm GoogleNotebooksRuntime#enable_vtpm}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7e01a379fbeac88f419bc03d3eae2061cec16fd7cee3b39a78ab28290251e83)
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
        '''Defines whether the instance has integrity monitoring enabled.

        Enables monitoring and attestation of the boot integrity of
        the instance. The attestation is performed against the
        integrity policy baseline. This baseline is initially derived
        from the implicitly trusted boot image when the instance is
        created. Enabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#enable_integrity_monitoring GoogleNotebooksRuntime#enable_integrity_monitoring}
        '''
        result = self._values.get("enable_integrity_monitoring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_secure_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether the instance has Secure Boot enabled.Secure Boot helps ensure that the system only runs authentic software by verifying the digital signature of all boot components, and halting the boot process if signature verification fails. Disabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#enable_secure_boot GoogleNotebooksRuntime#enable_secure_boot}
        '''
        result = self._values.get("enable_secure_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_vtpm(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether the instance has the vTPM enabled. Enabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_notebooks_runtime#enable_vtpm GoogleNotebooksRuntime#enable_vtpm}
        '''
        result = self._values.get("enable_vtpm")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNotebooksRuntime.GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b27205d26a3d97b0421c858d17303a2961e139b3e284cfef226fd059a474750)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a389fd714da4aa5e293cd46b6662995d0cec09e26485abbdee8356590962f88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__119fa1e235127f3fb2e55f768e1ba80060998ebc7a9aa2851f460e4c3ba3103b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d93f20bf27ebce0e0df25e7d8293fecd634896dc0048f7fc6febe3a6cd5bd98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableVtpm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig]:
        return typing.cast(typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__274e1801c2e9b5d7860f0fde240ed42c0c6cd22f6e30933697ff082b78db74a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleNotebooksRuntime",
    "GoogleNotebooksRuntimeAccessConfig",
    "GoogleNotebooksRuntimeAccessConfigOutputReference",
    "GoogleNotebooksRuntimeConfig",
    "GoogleNotebooksRuntimeMetrics",
    "GoogleNotebooksRuntimeMetricsList",
    "GoogleNotebooksRuntimeMetricsOutputReference",
    "GoogleNotebooksRuntimeSoftwareConfig",
    "GoogleNotebooksRuntimeSoftwareConfigKernels",
    "GoogleNotebooksRuntimeSoftwareConfigKernelsList",
    "GoogleNotebooksRuntimeSoftwareConfigKernelsOutputReference",
    "GoogleNotebooksRuntimeSoftwareConfigOutputReference",
    "GoogleNotebooksRuntimeTimeouts",
    "GoogleNotebooksRuntimeTimeoutsOutputReference",
    "GoogleNotebooksRuntimeVirtualMachine",
    "GoogleNotebooksRuntimeVirtualMachineOutputReference",
    "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfig",
    "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig",
    "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfigOutputReference",
    "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages",
    "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImagesList",
    "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImagesOutputReference",
    "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk",
    "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams",
    "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParamsOutputReference",
    "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskOutputReference",
    "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig",
    "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfigOutputReference",
    "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigOutputReference",
    "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig",
    "GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfigOutputReference",
]

publication.publish()

def _typecheckingstub__18515721895903fbb71b7f101a14a1ecbbf85412122ebeb10a30b8bd2ec76d48(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    access_config: typing.Optional[typing.Union[GoogleNotebooksRuntimeAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    software_config: typing.Optional[typing.Union[GoogleNotebooksRuntimeSoftwareConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleNotebooksRuntimeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_machine: typing.Optional[typing.Union[GoogleNotebooksRuntimeVirtualMachine, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f02ee26a228eaa479d33deeaa06e6444878c790df9e1bd2fd9ebb372cff94115(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb1f0f7ec622536e07c1e8a2fedfdb71b96bd1fe87b8632d89b87ac284b78be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3aad6f9ee801c2a7ea903389d2516eb52c44526f48664537fdbf12f9ac99a9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8af8e71d48c68fe3ba50eae014b0d378e5247cb2fe3db2c8f452c4d80b5b07a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ea5742f14bb6346378afe0aba00f84c5e2e5492cb187448a314922db90cc15a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe90830393afe41c95c28896817163f8dfe7f4f6b305560ccf02b96e77485d31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ddf77ac5db0fa99072a87b41c8c9463c683695218cef2e40ede818f37d90a66(
    *,
    access_type: typing.Optional[builtins.str] = None,
    runtime_owner: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6dcb6d673c491963fce8d8c0fb76c6827c74dc70926b0db8cd95489812c8518(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e06f9ea3421e6a87e8e12e35bd37bf3cead56e099371e6074c6e3162b22afb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a202680fa04f26a9bffb23ee078590efd27b3b2f4f6260987ea07b55807f0e53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19066932c6c31111bc9857bc612c7224b67a892e306db55a4f1ff34fe064c618(
    value: typing.Optional[GoogleNotebooksRuntimeAccessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57cc16778a19b750bbd7fc7f6b7ed4ededf2746c55f93ec03525be916ac2b0d5(
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
    access_config: typing.Optional[typing.Union[GoogleNotebooksRuntimeAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    software_config: typing.Optional[typing.Union[GoogleNotebooksRuntimeSoftwareConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleNotebooksRuntimeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_machine: typing.Optional[typing.Union[GoogleNotebooksRuntimeVirtualMachine, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de48644de57950a7fe7a0f9f0624f692acc07d823f38c7f54ad0b16de6e24be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__420b17d877aa42f7026b146501b8829d9498da9889b7cb21c16926cda370975c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb373e62e7897800cd957b84259309a3a7d05a45e9e1ddcecca709198ac1fc7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a8769afc57f5435a3be5dea4783d10a12c43869d039ddf4066f196763f7b285(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c1cb7151cf090ae5d10e26e7337159eca31361ce06da28bb484bea3d97177a8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2da6a5244ac23d1b4128ffec32cdd62598711d2fedcedd07650ae8cfc92fecb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c21c3173df77a90d3b7deadd688becf98b61b999bc2bd8b9f0055ee1afae4e62(
    value: typing.Optional[GoogleNotebooksRuntimeMetrics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43eb5fb242f21167589124f6aae474161c041ccd495c6668eb275163d96fae1d(
    *,
    custom_gpu_driver_path: typing.Optional[builtins.str] = None,
    enable_health_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    idle_shutdown: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    idle_shutdown_timeout: typing.Optional[jsii.Number] = None,
    install_gpu_driver: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    kernels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNotebooksRuntimeSoftwareConfigKernels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    notebook_upgrade_schedule: typing.Optional[builtins.str] = None,
    post_startup_script: typing.Optional[builtins.str] = None,
    post_startup_script_behavior: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b98d6f91a8d1be54bbf4ba505b819640b68ce67f971078f0de64ebc0d612ae55(
    *,
    repository: builtins.str,
    tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e3c6d47bbd6ba6e7c0aa9364f507b390849383faa5829efedd28977949e46cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0bf10870b43b651bb0a2794766dce97800cdffcbd575950c4590622850011ab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fd177a81e41d01e39a9e82e37ac7a26e7a823ae8981cd5fac68d973a64d174a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316591e869501ffddd64042996cbaacf3bdc05508918d8e86f70b63d9afc5abf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c40ec6bcd26ebfdb85faebdf79db3a01ec7bcf463fccb5b4239c56c2d4be0c74(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f58c8f8e25ecb04620ef6bc958c6e2a83223acc848beab08c3143fc26801e87e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNotebooksRuntimeSoftwareConfigKernels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac21190a4b2461600f0d42e12841b9c8f18eb4b7de6f6a11b95fb0919dd38a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__813e289afc5549cf979c81d1759b9488f9e3a3f524e99223c904c244c268ba39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec9805a2145eefceaeb885b338e275b80894007beffe70f0821b66320d8b988(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5ddf7802cc37c96f70871026afcf3cb8626438d3aef21651a4e5d78513a0fbf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNotebooksRuntimeSoftwareConfigKernels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b4f2ccac17691ca4b6b3872cd5946875adc5d783a73ee770c09b19615ba9f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67c2613589cd8a52fe2c0b8f296edb30873795c60a836506597f1aa905cf06a4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNotebooksRuntimeSoftwareConfigKernels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c70242ac761dae975b117465ca6228e43c3bb4b70bc38780336f45a483f7cb08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c3886d37fd61e5ec26b470f6705ee2b4715d3a1cad91b690058303adb675ba(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d78a645bfc84d099b37b8eb55c2e3b740fc105fc6fe721c571f457f95c569a74(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f1b72350065e04eabbae0c7f5414164d1bcb42d9f1a9af12243461461103e2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe22db4492baf802a00905530b6354d7aa8fa4ddd956876b795efd177539daf3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d436556529b43b4834bdb100334d70fedfcb763f8a74a7d375d3217e59fa5673(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9fe66497a7e101d880f8d474616c4330c07966e6390ed5e16400229d4f1fb75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb0dc82d39da27f70bf427a8cd3042dc0e054f2c58c1d353eebc097335bc20d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c09ef08bed7f96253c30f609544aff7e46dac079ac55311dfcdf11e7c1aabb(
    value: typing.Optional[GoogleNotebooksRuntimeSoftwareConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eae06ed3df479b075b81c1f38233986ec623e3c53114e823947bf7add633ef0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33d8a1071f628595d54dc799f30246144733ce37df91d8b8de996bcd5a7997b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b454fe8cd23452ecaea4c1f34e63ab498c7d2209241803efde53ca282270f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c2381423251cb06fd6dd725178f5f1c91d1e259d877b6a6a599d10a92ffcb8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd2385e26d8507de41604dc5c5eb1eb59e5b65605040182e339ef359641f70f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9f01c6dbb77723f9cf052343e12d0124caf15f6b1f134b0e5fdb709fbc13731(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNotebooksRuntimeTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27d44e8708731e656cef9711870163ea86587eb6e4a9c38b8f6500212c0238c3(
    *,
    virtual_machine_config: typing.Optional[typing.Union[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1721e82ace880dd48f4f86b01c8e08e023e512888fe63efa89b23dfe6680c732(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__959925c8929e620e6e7d5378fe0c4a450eb8f0122e0fb0fd9cbc3c076b10fd1e(
    value: typing.Optional[GoogleNotebooksRuntimeVirtualMachine],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__308814d450cde56f771c8e9b6a26af0c6505d65e0df61fff589942fa0a3b102e(
    *,
    data_disk: typing.Union[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk, typing.Dict[builtins.str, typing.Any]],
    machine_type: builtins.str,
    accelerator_config: typing.Optional[typing.Union[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    container_images: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages, typing.Dict[builtins.str, typing.Any]]]]] = None,
    encryption_config: typing.Optional[typing.Union[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    internal_ip_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    network: typing.Optional[builtins.str] = None,
    nic_type: typing.Optional[builtins.str] = None,
    reserved_ip_range: typing.Optional[builtins.str] = None,
    shielded_instance_config: typing.Optional[typing.Union[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    subnet: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa12cb61c0e29d4ec1b2afb893324bc1c5b4f0cc45682f339949efe0470fe36a(
    *,
    core_count: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__917c0780bfc0bf3496654ce57d2cd21db463feaaa9f8226effc29381e5eed01b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b147d82d6dce94e68dcd261f9df2f2916a00314398b84460615acc5f752be986(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16deb3f3a641ba03a7f7b7ddcbf0d69b79bc3f8c00650c239d06a8206c3dcf82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb4a88ba44737ba9bce60971e16121d1404a75da0e8ad8e8e9913819b7d038d6(
    value: typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a0fdf1d779ddc4c34ac8c1ea3c7094c7144b3436df954db13f3a1321d8aad3c(
    *,
    repository: builtins.str,
    tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d927bfd7c17e06d4ec2f7bbcd3fb9100ff2ce9761a8e974ecff2945fb3160d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87367ea174b986055b6b4eed2fda6a89daad061c9c26d31d3a2a41b6d0464e6c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07272dad45028b5d38fb2919a62b2cafdbdb212c59eba1610e55706698dfab59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bce3d13842ac6a71dbf8c5ef4f055419ac8ec3842d179b28b40191161d17106(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466466876585f351c8c397ec4c6fb47c4c2536fb5106cd242ded709acb727cbc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__301c693a728daf80e373b13426dc7c9df27d7a7e25600c32cdbdfd0e23c95b71(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ce2de6f94598b86f6714abb54af915cab93a20fbac8513b8587af55c8b2ba4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af94ca2f027734989a7968034a8344af1d9c611d552ddfa77153ee5457b8ce45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ea7eca860e0e56345d1d11bb3883b2485f5df2608fa4a52df6c95952c8b7d95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afcf2cf25c8beda29fdea75cf50fdd6ad4a14b4297ddbf0990d47ed254e11478(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__712c88c3b9b6da005c696ca7b35c362805aeba43ff434826417442ce26ad05fb(
    *,
    initialize_params: typing.Optional[typing.Union[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams, typing.Dict[builtins.str, typing.Any]]] = None,
    interface: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d816422b1e6f1ff9d1677f1e80f4790b6431f40b00de858cee524eb13b25e1(
    *,
    description: typing.Optional[builtins.str] = None,
    disk_name: typing.Optional[builtins.str] = None,
    disk_size_gb: typing.Optional[jsii.Number] = None,
    disk_type: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d2dca9ce359f32f652ccdeb62b6a35f2175a03d29817ba97fc7c131254e11a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50cefdec72d56d69db1dd4e8d813a49e865f5428ce0f385176c4faaae42ad2c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58c6f8711b6b957c5e8d3f8291a468d6bc28472b83833c53681b1abac7282ae5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39c43b8ebcb8bac6f38bab6d5ed8c40f890d7670a5b3f65a56048af59621036d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39aeff20c9eb846437d8a35d18b06933adf888cac89f7f8c2f300fddcb23148b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e6bfc21239f76a73b6cb690fa17e9e4324753db44c3f8c2ff2a9030443f1288(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__036f5c6fb99927df0e4abfe16356ed7194a49562d6fc45e3f621ae2b805bdfa8(
    value: typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42c2c9313a149aea3295a056a82d3d9130ea847ed23bb3b30fbbf3592eafa9cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b996135344f61f0550ac55b66530a25087bfe3e1b2faab670510ab6f3053688(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9892bab905c9bd5be820197c73a45e624362baf0e5edf2c7c980c91725cadc86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8c91dfb080152c99c5af15c90e7a51fc8ec57290ed46cc15c32cdae37fc341e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__460aff7005e9d4a8bfe610d5b41cbd594e7618d23ade787d53f211570c0819ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca21ce2c87cf57742681d0891581b2d3967ab231a33a25279a30f3f4fe7aeb74(
    value: typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63ecd5795655e113191546162d6f516270a8626b8efa0c804d38e7c5cfca3646(
    *,
    kms_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca27ae79707770a03b2acfec13ffe1d855a092803cef0989948ce7dcdfa7bbef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc839e6b0ab22754d069fa2e516e866412a2cd6f7faea21a3b6a12be298beb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9300fd54f9414ed8e4b8babaac93760d3df04769918fdf9657bcca8681fe24fa(
    value: typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3f62e57bba57ae146639517c028b9b4595fee86a61b80f0b590b813b24dcc1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ae080cdaf10efbec436b771898a43d5e4826f804662c5e0ca32802fbfcec98(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6aa0f9d6ce3099afe0a8dc97d4b06f3759c817d2de2a1d29a9fbd05c25d699d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64379c562482756ab487030f117301df6ea8651ed83ec90f822f9596e5d31604(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f783f2187ab2cac67b7156fbb90619c22da29542e345c98cafe468df0f50a32a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c770374023378e6234e08b89ac4c06569060902a7cbf76d58b1edbda9ac85a7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e80f6c3452903afa2d11129a0006e2f4d7ee5d1a36f415cbd15788282e8fbdb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b392f51d208111b2ddcd28b6a7e5962010b3fd5131a0f754086613a560a24ec7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52a1aab2fc93230ba2acd274269a6604cb0315f08c4b283af2104764ef13811c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df70cffa5c8502e993b0afb4aceaece881ad95649f0f1a2ba08d8b127f45ad28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f48fd0417dad4bc94e89173340bcab5ce255c93f9d66a9b31c8fca9030381561(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f32ebf82a18d94e77f613639049e2a65c438cf7b745260880be44ae7fd5fb7a9(
    value: typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7e01a379fbeac88f419bc03d3eae2061cec16fd7cee3b39a78ab28290251e83(
    *,
    enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b27205d26a3d97b0421c858d17303a2961e139b3e284cfef226fd059a474750(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a389fd714da4aa5e293cd46b6662995d0cec09e26485abbdee8356590962f88(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__119fa1e235127f3fb2e55f768e1ba80060998ebc7a9aa2851f460e4c3ba3103b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d93f20bf27ebce0e0df25e7d8293fecd634896dc0048f7fc6febe3a6cd5bd98(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__274e1801c2e9b5d7860f0fde240ed42c0c6cd22f6e30933697ff082b78db74a5(
    value: typing.Optional[GoogleNotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass
