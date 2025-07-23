r'''
# `google_notebooks_runtime`

Refer to the Terraform Registry for docs: [`google_notebooks_runtime`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime).
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


class NotebooksRuntime(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntime",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime google_notebooks_runtime}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        access_config: typing.Optional[typing.Union["NotebooksRuntimeAccessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        software_config: typing.Optional[typing.Union["NotebooksRuntimeSoftwareConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["NotebooksRuntimeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_machine: typing.Optional[typing.Union["NotebooksRuntimeVirtualMachine", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime google_notebooks_runtime} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: A reference to the zone where the machine resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#location NotebooksRuntime#location}
        :param name: The name specified for the Notebook runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#name NotebooksRuntime#name}
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#access_config NotebooksRuntime#access_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#id NotebooksRuntime#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels to associate with this runtime. Label **keys** must contain 1 to 63 characters, and must conform to [RFC 1035] (https://www.ietf.org/rfc/rfc1035.txt). Label **values** may be empty, but, if present, must contain 1 to 63 characters, and must conform to `RFC 1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. No more than 32 labels can be associated with a cluster. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#labels NotebooksRuntime#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#project NotebooksRuntime#project}.
        :param software_config: software_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#software_config NotebooksRuntime#software_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#timeouts NotebooksRuntime#timeouts}
        :param virtual_machine: virtual_machine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#virtual_machine NotebooksRuntime#virtual_machine}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__538f5371073e53053f64ff03aea5d925f3604c2235ec4b48af8b1c0515bdb122)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NotebooksRuntimeConfig(
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
        '''Generates CDKTF code for importing a NotebooksRuntime resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NotebooksRuntime to import.
        :param import_from_id: The id of the existing NotebooksRuntime that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NotebooksRuntime to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4041763cd159c5306192fd90bd439723cd33ff62feb62c852471dc0fcde67e0)
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
        :param access_type: The type of access mode this instance. For valid values, see 'https://cloud.google.com/vertex-ai/docs/workbench/reference/ rest/v1/projects.locations.runtimes#RuntimeAccessType'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#access_type NotebooksRuntime#access_type}
        :param runtime_owner: The owner of this runtime after creation. Format: 'alias@example.com'. Currently supports one owner only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#runtime_owner NotebooksRuntime#runtime_owner}
        '''
        value = NotebooksRuntimeAccessConfig(
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
        kernels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NotebooksRuntimeSoftwareConfigKernels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        notebook_upgrade_schedule: typing.Optional[builtins.str] = None,
        post_startup_script: typing.Optional[builtins.str] = None,
        post_startup_script_behavior: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_gpu_driver_path: Specify a custom Cloud Storage path where the GPU driver is stored. If not specified, we'll automatically choose from official GPU drivers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#custom_gpu_driver_path NotebooksRuntime#custom_gpu_driver_path}
        :param enable_health_monitoring: Verifies core internal services are running. Default: True. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#enable_health_monitoring NotebooksRuntime#enable_health_monitoring}
        :param idle_shutdown: Runtime will automatically shutdown after idle_shutdown_time. Default: True. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#idle_shutdown NotebooksRuntime#idle_shutdown}
        :param idle_shutdown_timeout: Time in minutes to wait before shuting down runtime. Default: 180 minutes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#idle_shutdown_timeout NotebooksRuntime#idle_shutdown_timeout}
        :param install_gpu_driver: Install Nvidia Driver automatically. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#install_gpu_driver NotebooksRuntime#install_gpu_driver}
        :param kernels: kernels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#kernels NotebooksRuntime#kernels}
        :param notebook_upgrade_schedule: Cron expression in UTC timezone for schedule instance auto upgrade. Please follow the `cron format <https://en.wikipedia.org/wiki/Cron>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#notebook_upgrade_schedule NotebooksRuntime#notebook_upgrade_schedule}
        :param post_startup_script: Path to a Bash script that automatically runs after a notebook instance fully boots up. The path must be a URL or Cloud Storage path (gs://path-to-file/file-name). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#post_startup_script NotebooksRuntime#post_startup_script}
        :param post_startup_script_behavior: Behavior for the post startup script. Possible values: ["POST_STARTUP_SCRIPT_BEHAVIOR_UNSPECIFIED", "RUN_EVERY_START", "DOWNLOAD_AND_RUN_EVERY_START"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#post_startup_script_behavior NotebooksRuntime#post_startup_script_behavior}
        '''
        value = NotebooksRuntimeSoftwareConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#create NotebooksRuntime#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#delete NotebooksRuntime#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#update NotebooksRuntime#update}.
        '''
        value = NotebooksRuntimeTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVirtualMachine")
    def put_virtual_machine(
        self,
        *,
        virtual_machine_config: typing.Optional[typing.Union["NotebooksRuntimeVirtualMachineVirtualMachineConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param virtual_machine_config: virtual_machine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#virtual_machine_config NotebooksRuntime#virtual_machine_config}
        '''
        value = NotebooksRuntimeVirtualMachine(
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
    def access_config(self) -> "NotebooksRuntimeAccessConfigOutputReference":
        return typing.cast("NotebooksRuntimeAccessConfigOutputReference", jsii.get(self, "accessConfig"))

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
    def metrics(self) -> "NotebooksRuntimeMetricsList":
        return typing.cast("NotebooksRuntimeMetricsList", jsii.get(self, "metrics"))

    @builtins.property
    @jsii.member(jsii_name="softwareConfig")
    def software_config(self) -> "NotebooksRuntimeSoftwareConfigOutputReference":
        return typing.cast("NotebooksRuntimeSoftwareConfigOutputReference", jsii.get(self, "softwareConfig"))

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
    def timeouts(self) -> "NotebooksRuntimeTimeoutsOutputReference":
        return typing.cast("NotebooksRuntimeTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachine")
    def virtual_machine(self) -> "NotebooksRuntimeVirtualMachineOutputReference":
        return typing.cast("NotebooksRuntimeVirtualMachineOutputReference", jsii.get(self, "virtualMachine"))

    @builtins.property
    @jsii.member(jsii_name="accessConfigInput")
    def access_config_input(self) -> typing.Optional["NotebooksRuntimeAccessConfig"]:
        return typing.cast(typing.Optional["NotebooksRuntimeAccessConfig"], jsii.get(self, "accessConfigInput"))

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
    ) -> typing.Optional["NotebooksRuntimeSoftwareConfig"]:
        return typing.cast(typing.Optional["NotebooksRuntimeSoftwareConfig"], jsii.get(self, "softwareConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NotebooksRuntimeTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NotebooksRuntimeTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineInput")
    def virtual_machine_input(
        self,
    ) -> typing.Optional["NotebooksRuntimeVirtualMachine"]:
        return typing.cast(typing.Optional["NotebooksRuntimeVirtualMachine"], jsii.get(self, "virtualMachineInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bac97a06af70d9b6c6656aa506f54ec7426c9a8b9885f80fab511f3b93d26054)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db0390213f5ab1aed52e2ea40966dce1bcc1af267c26efc299ff3d0ea41c51cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbdc16fe09ff602f1dc37123257a9655aeaafad1abb79718e1dc0493355f6407)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e1c6ab29c3fc0b86ed4660f64e0df774653f2d48c983dc8c1ac02336ecd2940)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81cf537c961dd88786b8aff002bdc40b726661b936adb2100c9b8203c5f7bd38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeAccessConfig",
    jsii_struct_bases=[],
    name_mapping={"access_type": "accessType", "runtime_owner": "runtimeOwner"},
)
class NotebooksRuntimeAccessConfig:
    def __init__(
        self,
        *,
        access_type: typing.Optional[builtins.str] = None,
        runtime_owner: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_type: The type of access mode this instance. For valid values, see 'https://cloud.google.com/vertex-ai/docs/workbench/reference/ rest/v1/projects.locations.runtimes#RuntimeAccessType'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#access_type NotebooksRuntime#access_type}
        :param runtime_owner: The owner of this runtime after creation. Format: 'alias@example.com'. Currently supports one owner only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#runtime_owner NotebooksRuntime#runtime_owner}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ca88bd179817874965ad2b85c4aaba760a00b63f9a92a1e1c528a19a558779f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#access_type NotebooksRuntime#access_type}
        '''
        result = self._values.get("access_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_owner(self) -> typing.Optional[builtins.str]:
        '''The owner of this runtime after creation. Format: 'alias@example.com'. Currently supports one owner only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#runtime_owner NotebooksRuntime#runtime_owner}
        '''
        result = self._values.get("runtime_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebooksRuntimeAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NotebooksRuntimeAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e63edfb28bf584fd41fdaa08886b93005517d6b1ccb36fb035fe65a8c776c4dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68573e197ed2948b5d6d59add52b9a9446b90265473ac0b948a5586365502d79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeOwner")
    def runtime_owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeOwner"))

    @runtime_owner.setter
    def runtime_owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53d718f48b1e1f6500c989f8e3dbd09dad212ab4efc83ad144e970e477ead53e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeOwner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NotebooksRuntimeAccessConfig]:
        return typing.cast(typing.Optional[NotebooksRuntimeAccessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NotebooksRuntimeAccessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__392d6e31bbe3990a5e5f5ce60fc1d367c2fec23ae7e50ddb744e8d5d9c20580f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeConfig",
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
class NotebooksRuntimeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        access_config: typing.Optional[typing.Union[NotebooksRuntimeAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        software_config: typing.Optional[typing.Union["NotebooksRuntimeSoftwareConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["NotebooksRuntimeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_machine: typing.Optional[typing.Union["NotebooksRuntimeVirtualMachine", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: A reference to the zone where the machine resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#location NotebooksRuntime#location}
        :param name: The name specified for the Notebook runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#name NotebooksRuntime#name}
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#access_config NotebooksRuntime#access_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#id NotebooksRuntime#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels to associate with this runtime. Label **keys** must contain 1 to 63 characters, and must conform to [RFC 1035] (https://www.ietf.org/rfc/rfc1035.txt). Label **values** may be empty, but, if present, must contain 1 to 63 characters, and must conform to `RFC 1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. No more than 32 labels can be associated with a cluster. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#labels NotebooksRuntime#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#project NotebooksRuntime#project}.
        :param software_config: software_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#software_config NotebooksRuntime#software_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#timeouts NotebooksRuntime#timeouts}
        :param virtual_machine: virtual_machine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#virtual_machine NotebooksRuntime#virtual_machine}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(access_config, dict):
            access_config = NotebooksRuntimeAccessConfig(**access_config)
        if isinstance(software_config, dict):
            software_config = NotebooksRuntimeSoftwareConfig(**software_config)
        if isinstance(timeouts, dict):
            timeouts = NotebooksRuntimeTimeouts(**timeouts)
        if isinstance(virtual_machine, dict):
            virtual_machine = NotebooksRuntimeVirtualMachine(**virtual_machine)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7277f1b620710067f454680e647b2350824602ec2807895bf2323322e6b5e4e4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#location NotebooksRuntime#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name specified for the Notebook runtime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#name NotebooksRuntime#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_config(self) -> typing.Optional[NotebooksRuntimeAccessConfig]:
        '''access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#access_config NotebooksRuntime#access_config}
        '''
        result = self._values.get("access_config")
        return typing.cast(typing.Optional[NotebooksRuntimeAccessConfig], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#id NotebooksRuntime#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#labels NotebooksRuntime#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#project NotebooksRuntime#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def software_config(self) -> typing.Optional["NotebooksRuntimeSoftwareConfig"]:
        '''software_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#software_config NotebooksRuntime#software_config}
        '''
        result = self._values.get("software_config")
        return typing.cast(typing.Optional["NotebooksRuntimeSoftwareConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NotebooksRuntimeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#timeouts NotebooksRuntime#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NotebooksRuntimeTimeouts"], result)

    @builtins.property
    def virtual_machine(self) -> typing.Optional["NotebooksRuntimeVirtualMachine"]:
        '''virtual_machine block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#virtual_machine NotebooksRuntime#virtual_machine}
        '''
        result = self._values.get("virtual_machine")
        return typing.cast(typing.Optional["NotebooksRuntimeVirtualMachine"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebooksRuntimeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeMetrics",
    jsii_struct_bases=[],
    name_mapping={},
)
class NotebooksRuntimeMetrics:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebooksRuntimeMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NotebooksRuntimeMetricsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeMetricsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__edca6f7b762cefcffbe6ee409bb43253e53a51aec6e940db7af0f66a699b1441)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "NotebooksRuntimeMetricsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f740aeee35ccd95f34ca986f97e3087c5ed8fd029575a81d6662c8f266a4031)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NotebooksRuntimeMetricsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cada24f09a7411f029e3a531fad9cfed22c8ef1fc1f834c9bde5ad2b720d70f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb8d5599baec48c86f106e14f844a66fadd8b63d229fec4ed9600356f2b1d52c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4867d11b1d57661905e0dcae7d483902a16ccd422631d9f097d3b94f301efc46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class NotebooksRuntimeMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b205ae1169040a3e4f457e1b160db9f1dd3a599390d57fc65a7cb250d0a275c)
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
    def internal_value(self) -> typing.Optional[NotebooksRuntimeMetrics]:
        return typing.cast(typing.Optional[NotebooksRuntimeMetrics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[NotebooksRuntimeMetrics]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__848d938767efe8589d028b5aa5d30dd59cbee0ffab239e10992a0ab93adeca22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeSoftwareConfig",
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
class NotebooksRuntimeSoftwareConfig:
    def __init__(
        self,
        *,
        custom_gpu_driver_path: typing.Optional[builtins.str] = None,
        enable_health_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        idle_shutdown: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        idle_shutdown_timeout: typing.Optional[jsii.Number] = None,
        install_gpu_driver: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kernels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NotebooksRuntimeSoftwareConfigKernels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        notebook_upgrade_schedule: typing.Optional[builtins.str] = None,
        post_startup_script: typing.Optional[builtins.str] = None,
        post_startup_script_behavior: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_gpu_driver_path: Specify a custom Cloud Storage path where the GPU driver is stored. If not specified, we'll automatically choose from official GPU drivers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#custom_gpu_driver_path NotebooksRuntime#custom_gpu_driver_path}
        :param enable_health_monitoring: Verifies core internal services are running. Default: True. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#enable_health_monitoring NotebooksRuntime#enable_health_monitoring}
        :param idle_shutdown: Runtime will automatically shutdown after idle_shutdown_time. Default: True. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#idle_shutdown NotebooksRuntime#idle_shutdown}
        :param idle_shutdown_timeout: Time in minutes to wait before shuting down runtime. Default: 180 minutes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#idle_shutdown_timeout NotebooksRuntime#idle_shutdown_timeout}
        :param install_gpu_driver: Install Nvidia Driver automatically. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#install_gpu_driver NotebooksRuntime#install_gpu_driver}
        :param kernels: kernels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#kernels NotebooksRuntime#kernels}
        :param notebook_upgrade_schedule: Cron expression in UTC timezone for schedule instance auto upgrade. Please follow the `cron format <https://en.wikipedia.org/wiki/Cron>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#notebook_upgrade_schedule NotebooksRuntime#notebook_upgrade_schedule}
        :param post_startup_script: Path to a Bash script that automatically runs after a notebook instance fully boots up. The path must be a URL or Cloud Storage path (gs://path-to-file/file-name). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#post_startup_script NotebooksRuntime#post_startup_script}
        :param post_startup_script_behavior: Behavior for the post startup script. Possible values: ["POST_STARTUP_SCRIPT_BEHAVIOR_UNSPECIFIED", "RUN_EVERY_START", "DOWNLOAD_AND_RUN_EVERY_START"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#post_startup_script_behavior NotebooksRuntime#post_startup_script_behavior}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e72ae8716b8627284757ee8e6167e7dc10ce965a5c85cc37d838c93897fa9627)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#custom_gpu_driver_path NotebooksRuntime#custom_gpu_driver_path}
        '''
        result = self._values.get("custom_gpu_driver_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_health_monitoring(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Verifies core internal services are running. Default: True.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#enable_health_monitoring NotebooksRuntime#enable_health_monitoring}
        '''
        result = self._values.get("enable_health_monitoring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def idle_shutdown(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Runtime will automatically shutdown after idle_shutdown_time. Default: True.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#idle_shutdown NotebooksRuntime#idle_shutdown}
        '''
        result = self._values.get("idle_shutdown")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def idle_shutdown_timeout(self) -> typing.Optional[jsii.Number]:
        '''Time in minutes to wait before shuting down runtime. Default: 180 minutes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#idle_shutdown_timeout NotebooksRuntime#idle_shutdown_timeout}
        '''
        result = self._values.get("idle_shutdown_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def install_gpu_driver(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Install Nvidia Driver automatically.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#install_gpu_driver NotebooksRuntime#install_gpu_driver}
        '''
        result = self._values.get("install_gpu_driver")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def kernels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NotebooksRuntimeSoftwareConfigKernels"]]]:
        '''kernels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#kernels NotebooksRuntime#kernels}
        '''
        result = self._values.get("kernels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NotebooksRuntimeSoftwareConfigKernels"]]], result)

    @builtins.property
    def notebook_upgrade_schedule(self) -> typing.Optional[builtins.str]:
        '''Cron expression in UTC timezone for schedule instance auto upgrade. Please follow the `cron format <https://en.wikipedia.org/wiki/Cron>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#notebook_upgrade_schedule NotebooksRuntime#notebook_upgrade_schedule}
        '''
        result = self._values.get("notebook_upgrade_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_startup_script(self) -> typing.Optional[builtins.str]:
        '''Path to a Bash script that automatically runs after a notebook instance fully boots up.

        The path must be a URL or
        Cloud Storage path (gs://path-to-file/file-name).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#post_startup_script NotebooksRuntime#post_startup_script}
        '''
        result = self._values.get("post_startup_script")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_startup_script_behavior(self) -> typing.Optional[builtins.str]:
        '''Behavior for the post startup script. Possible values: ["POST_STARTUP_SCRIPT_BEHAVIOR_UNSPECIFIED", "RUN_EVERY_START", "DOWNLOAD_AND_RUN_EVERY_START"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#post_startup_script_behavior NotebooksRuntime#post_startup_script_behavior}
        '''
        result = self._values.get("post_startup_script_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebooksRuntimeSoftwareConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeSoftwareConfigKernels",
    jsii_struct_bases=[],
    name_mapping={"repository": "repository", "tag": "tag"},
)
class NotebooksRuntimeSoftwareConfigKernels:
    def __init__(
        self,
        *,
        repository: builtins.str,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repository: The path to the container image repository. For example: gcr.io/{project_id}/{imageName}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#repository NotebooksRuntime#repository}
        :param tag: The tag of the container image. If not specified, this defaults to the latest tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#tag NotebooksRuntime#tag}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__052fc3403b6dfad04078599ae41363d36bcbe2af4646f69f915e1166b6bada78)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#repository NotebooksRuntime#repository}
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''The tag of the container image. If not specified, this defaults to the latest tag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#tag NotebooksRuntime#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebooksRuntimeSoftwareConfigKernels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NotebooksRuntimeSoftwareConfigKernelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeSoftwareConfigKernelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5dc296b6950595ca9ff22d68da70b622b3f982e2421b84ef973821720ba7244)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NotebooksRuntimeSoftwareConfigKernelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99d655ffb7fc3ba951d4da99534fa3234b9c363eca575c719155c52843b41550)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NotebooksRuntimeSoftwareConfigKernelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8924c4a3be66430c75e1ff4517d775fd64b3b005a2d9637b90dd0f38d61cc1e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__13b326862c3588b3babc53919506da07c6c49d75b85cd76c201bb2d15e4818aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__759fc549311f2304fb771e7efc2fcf22dbbe1d60cd8885d0e780142362a09a5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NotebooksRuntimeSoftwareConfigKernels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NotebooksRuntimeSoftwareConfigKernels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NotebooksRuntimeSoftwareConfigKernels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76f5ba1c90ce597bb900cf5ab05d434b841490bd055f3b362b5e4bd5a8886da4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NotebooksRuntimeSoftwareConfigKernelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeSoftwareConfigKernelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9bf2a03a251d1f980db32a3312a75d4b5f56405dbfa3bb8ba532b49c39bb229)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9579e15807400219e1a2ae01fd29fd918899df1771c4400e8e6063c12193ae72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fafdfecbd364a77cc342ddf98d78401e06a231121749b65abb01d3921a58f6be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NotebooksRuntimeSoftwareConfigKernels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NotebooksRuntimeSoftwareConfigKernels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NotebooksRuntimeSoftwareConfigKernels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cf9c6083f4d9ca1f4d39ed89794d3c37b627ddfe388e6e940a5c279526cb286)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NotebooksRuntimeSoftwareConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeSoftwareConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d01ce5fe70c3300070d4aca274e8551de3c7d9830d16cc91c54a28610b114b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putKernels")
    def put_kernels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NotebooksRuntimeSoftwareConfigKernels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__770f86841c30636ceae9ed654bc8fe3152fc4a66efb418462028d20c3e9c9ca6)
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
    def kernels(self) -> NotebooksRuntimeSoftwareConfigKernelsList:
        return typing.cast(NotebooksRuntimeSoftwareConfigKernelsList, jsii.get(self, "kernels"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NotebooksRuntimeSoftwareConfigKernels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NotebooksRuntimeSoftwareConfigKernels]]], jsii.get(self, "kernelsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0e733d9dfd8d2a833074e996fa60f2f7b65bf916052ff6cb373f2597327518ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aff68b1e662956e97a3a4120d9870a6fb39bab55d257a57e64dd409e3dc9c39d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fb63a818062f37fe52ebcf56c3c0dd1a0716077e7afa71c4ca41e08dcb6cbee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleShutdown", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idleShutdownTimeout")
    def idle_shutdown_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "idleShutdownTimeout"))

    @idle_shutdown_timeout.setter
    def idle_shutdown_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9efa728159dadaaed4faeec75aa74f8fe87791dbdb706f6045818106dd4cc684)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1102339bc8e300cc552f49effda99ee928aae06a0bed0e447945800ce42e4bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "installGpuDriver", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notebookUpgradeSchedule")
    def notebook_upgrade_schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notebookUpgradeSchedule"))

    @notebook_upgrade_schedule.setter
    def notebook_upgrade_schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b3b1524123f23dc04dfba87262886efee2e61aeacec2cbd146329ab052a71f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notebookUpgradeSchedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postStartupScript")
    def post_startup_script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postStartupScript"))

    @post_startup_script.setter
    def post_startup_script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12d662ffb8e1e2f4039986e84cca30e88d41df8de6ed41f824f299209b4528bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postStartupScript", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postStartupScriptBehavior")
    def post_startup_script_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postStartupScriptBehavior"))

    @post_startup_script_behavior.setter
    def post_startup_script_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adb6015af20d27a49586767db95013e2e171c215dbdb65b1eac44f82fff35f4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postStartupScriptBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NotebooksRuntimeSoftwareConfig]:
        return typing.cast(typing.Optional[NotebooksRuntimeSoftwareConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NotebooksRuntimeSoftwareConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b7a6f759a93706a6e8508a8d94eceeddd904901cfd16563ddfb0a1746a4cb6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class NotebooksRuntimeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#create NotebooksRuntime#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#delete NotebooksRuntime#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#update NotebooksRuntime#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac521fd37f4c9926107259a6e3ae06eaf204cf5b13f39ad1ccc984bcb1d39915)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#create NotebooksRuntime#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#delete NotebooksRuntime#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#update NotebooksRuntime#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebooksRuntimeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NotebooksRuntimeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__261741b2fd52b6d984cff4074ba77f85fe0e86af09eed09ff8cb63480cf0da45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2b17ad8bfbbc8f14858e0b323931b251606fc856abac18befd63ad9f790ac06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a74d39100cbcd4c5d131c15cb07ea48e1d2ad843b6e30c3d5f374d4be0fb3f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adc2a8a081b5e5e931daac094869e8c57ae7d185d020934437a78fd62fa9d826)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NotebooksRuntimeTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NotebooksRuntimeTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NotebooksRuntimeTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaaf7f0cc53237d3e4f9ba96f28053177181db18be3a6dacd5bcae77feb175af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeVirtualMachine",
    jsii_struct_bases=[],
    name_mapping={"virtual_machine_config": "virtualMachineConfig"},
)
class NotebooksRuntimeVirtualMachine:
    def __init__(
        self,
        *,
        virtual_machine_config: typing.Optional[typing.Union["NotebooksRuntimeVirtualMachineVirtualMachineConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param virtual_machine_config: virtual_machine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#virtual_machine_config NotebooksRuntime#virtual_machine_config}
        '''
        if isinstance(virtual_machine_config, dict):
            virtual_machine_config = NotebooksRuntimeVirtualMachineVirtualMachineConfig(**virtual_machine_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf5ce8a5cd4ac08fab1139ba74543b8f5d8b8889b2805bab510b9bdf86a3e388)
            check_type(argname="argument virtual_machine_config", value=virtual_machine_config, expected_type=type_hints["virtual_machine_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if virtual_machine_config is not None:
            self._values["virtual_machine_config"] = virtual_machine_config

    @builtins.property
    def virtual_machine_config(
        self,
    ) -> typing.Optional["NotebooksRuntimeVirtualMachineVirtualMachineConfig"]:
        '''virtual_machine_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#virtual_machine_config NotebooksRuntime#virtual_machine_config}
        '''
        result = self._values.get("virtual_machine_config")
        return typing.cast(typing.Optional["NotebooksRuntimeVirtualMachineVirtualMachineConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebooksRuntimeVirtualMachine(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NotebooksRuntimeVirtualMachineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeVirtualMachineOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3174bea105ddc8daab514ec952d7668aae2b722fdb7d2c61203f06ab84dfb8a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVirtualMachineConfig")
    def put_virtual_machine_config(
        self,
        *,
        data_disk: typing.Union["NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk", typing.Dict[builtins.str, typing.Any]],
        machine_type: builtins.str,
        accelerator_config: typing.Optional[typing.Union["NotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        container_images: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryption_config: typing.Optional[typing.Union["NotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        internal_ip_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network: typing.Optional[builtins.str] = None,
        nic_type: typing.Optional[builtins.str] = None,
        reserved_ip_range: typing.Optional[builtins.str] = None,
        shielded_instance_config: typing.Optional[typing.Union["NotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        subnet: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param data_disk: data_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#data_disk NotebooksRuntime#data_disk}
        :param machine_type: The Compute Engine machine type used for runtimes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#machine_type NotebooksRuntime#machine_type}
        :param accelerator_config: accelerator_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#accelerator_config NotebooksRuntime#accelerator_config}
        :param container_images: container_images block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#container_images NotebooksRuntime#container_images}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#encryption_config NotebooksRuntime#encryption_config}
        :param internal_ip_only: If true, runtime will only have internal IP addresses. By default, runtimes are not restricted to internal IP addresses, and will have ephemeral external IP addresses assigned to each vm. This 'internal_ip_only' restriction can only be enabled for subnetwork enabled networks, and all dependencies must be configured to be accessible without external IP addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#internal_ip_only NotebooksRuntime#internal_ip_only}
        :param labels: The labels to associate with this runtime. Label **keys** must contain 1 to 63 characters, and must conform to [RFC 1035] (https://www.ietf.org/rfc/rfc1035.txt). Label **values** may be empty, but, if present, must contain 1 to 63 characters, and must conform to `RFC 1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. No more than 32 labels can be associated with a cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#labels NotebooksRuntime#labels}
        :param metadata: The Compute Engine metadata entries to add to virtual machine. (see [Project and instance metadata](https://cloud.google.com /compute/docs/storing-retrieving-metadata#project_and_instance _metadata)). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#metadata NotebooksRuntime#metadata}
        :param network: The Compute Engine network to be used for machine communications. Cannot be specified with subnetwork. If neither 'network' nor 'subnet' is specified, the "default" network of the project is used, if it exists. A full URL or partial URI. Examples: - 'https://www.googleapis.com/compute/v1/projects/[project_id]/ regions/global/default' - 'projects/[project_id]/regions/global/default' Runtimes are managed resources inside Google Infrastructure. Runtimes support the following network configurations: - Google Managed Network (Network & subnet are empty) - Consumer Project VPC (network & subnet are required). Requires configuring Private Service Access. - Shared VPC (network & subnet are required). Requires configuring Private Service Access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#network NotebooksRuntime#network}
        :param nic_type: The type of vNIC to be used on this interface. This may be gVNIC or VirtioNet. Possible values: ["UNSPECIFIED_NIC_TYPE", "VIRTIO_NET", "GVNIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#nic_type NotebooksRuntime#nic_type}
        :param reserved_ip_range: Reserved IP Range name is used for VPC Peering. The subnetwork allocation will use the range *name* if it's assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#reserved_ip_range NotebooksRuntime#reserved_ip_range}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#shielded_instance_config NotebooksRuntime#shielded_instance_config}
        :param subnet: The Compute Engine subnetwork to be used for machine communications. Cannot be specified with network. A full URL or partial URI are valid. Examples: - 'https://www.googleapis.com/compute/v1/projects/[project_id]/ regions/us-east1/subnetworks/sub0' - 'projects/[project_id]/regions/us-east1/subnetworks/sub0' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#subnet NotebooksRuntime#subnet}
        :param tags: The Compute Engine tags to add to runtime (see [Tagging instances] (https://cloud.google.com/compute/docs/ label-or-tag-resources#tags)). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#tags NotebooksRuntime#tags}
        '''
        value = NotebooksRuntimeVirtualMachineVirtualMachineConfig(
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
    ) -> "NotebooksRuntimeVirtualMachineVirtualMachineConfigOutputReference":
        return typing.cast("NotebooksRuntimeVirtualMachineVirtualMachineConfigOutputReference", jsii.get(self, "virtualMachineConfig"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineConfigInput")
    def virtual_machine_config_input(
        self,
    ) -> typing.Optional["NotebooksRuntimeVirtualMachineVirtualMachineConfig"]:
        return typing.cast(typing.Optional["NotebooksRuntimeVirtualMachineVirtualMachineConfig"], jsii.get(self, "virtualMachineConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NotebooksRuntimeVirtualMachine]:
        return typing.cast(typing.Optional[NotebooksRuntimeVirtualMachine], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NotebooksRuntimeVirtualMachine],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87118287f4f4a2a13e3f7bce31a1caf6b741cd1016a7aa7b572aa90ab8022c5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeVirtualMachineVirtualMachineConfig",
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
class NotebooksRuntimeVirtualMachineVirtualMachineConfig:
    def __init__(
        self,
        *,
        data_disk: typing.Union["NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk", typing.Dict[builtins.str, typing.Any]],
        machine_type: builtins.str,
        accelerator_config: typing.Optional[typing.Union["NotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        container_images: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryption_config: typing.Optional[typing.Union["NotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        internal_ip_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network: typing.Optional[builtins.str] = None,
        nic_type: typing.Optional[builtins.str] = None,
        reserved_ip_range: typing.Optional[builtins.str] = None,
        shielded_instance_config: typing.Optional[typing.Union["NotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        subnet: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param data_disk: data_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#data_disk NotebooksRuntime#data_disk}
        :param machine_type: The Compute Engine machine type used for runtimes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#machine_type NotebooksRuntime#machine_type}
        :param accelerator_config: accelerator_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#accelerator_config NotebooksRuntime#accelerator_config}
        :param container_images: container_images block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#container_images NotebooksRuntime#container_images}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#encryption_config NotebooksRuntime#encryption_config}
        :param internal_ip_only: If true, runtime will only have internal IP addresses. By default, runtimes are not restricted to internal IP addresses, and will have ephemeral external IP addresses assigned to each vm. This 'internal_ip_only' restriction can only be enabled for subnetwork enabled networks, and all dependencies must be configured to be accessible without external IP addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#internal_ip_only NotebooksRuntime#internal_ip_only}
        :param labels: The labels to associate with this runtime. Label **keys** must contain 1 to 63 characters, and must conform to [RFC 1035] (https://www.ietf.org/rfc/rfc1035.txt). Label **values** may be empty, but, if present, must contain 1 to 63 characters, and must conform to `RFC 1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. No more than 32 labels can be associated with a cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#labels NotebooksRuntime#labels}
        :param metadata: The Compute Engine metadata entries to add to virtual machine. (see [Project and instance metadata](https://cloud.google.com /compute/docs/storing-retrieving-metadata#project_and_instance _metadata)). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#metadata NotebooksRuntime#metadata}
        :param network: The Compute Engine network to be used for machine communications. Cannot be specified with subnetwork. If neither 'network' nor 'subnet' is specified, the "default" network of the project is used, if it exists. A full URL or partial URI. Examples: - 'https://www.googleapis.com/compute/v1/projects/[project_id]/ regions/global/default' - 'projects/[project_id]/regions/global/default' Runtimes are managed resources inside Google Infrastructure. Runtimes support the following network configurations: - Google Managed Network (Network & subnet are empty) - Consumer Project VPC (network & subnet are required). Requires configuring Private Service Access. - Shared VPC (network & subnet are required). Requires configuring Private Service Access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#network NotebooksRuntime#network}
        :param nic_type: The type of vNIC to be used on this interface. This may be gVNIC or VirtioNet. Possible values: ["UNSPECIFIED_NIC_TYPE", "VIRTIO_NET", "GVNIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#nic_type NotebooksRuntime#nic_type}
        :param reserved_ip_range: Reserved IP Range name is used for VPC Peering. The subnetwork allocation will use the range *name* if it's assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#reserved_ip_range NotebooksRuntime#reserved_ip_range}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#shielded_instance_config NotebooksRuntime#shielded_instance_config}
        :param subnet: The Compute Engine subnetwork to be used for machine communications. Cannot be specified with network. A full URL or partial URI are valid. Examples: - 'https://www.googleapis.com/compute/v1/projects/[project_id]/ regions/us-east1/subnetworks/sub0' - 'projects/[project_id]/regions/us-east1/subnetworks/sub0' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#subnet NotebooksRuntime#subnet}
        :param tags: The Compute Engine tags to add to runtime (see [Tagging instances] (https://cloud.google.com/compute/docs/ label-or-tag-resources#tags)). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#tags NotebooksRuntime#tags}
        '''
        if isinstance(data_disk, dict):
            data_disk = NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk(**data_disk)
        if isinstance(accelerator_config, dict):
            accelerator_config = NotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig(**accelerator_config)
        if isinstance(encryption_config, dict):
            encryption_config = NotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig(**encryption_config)
        if isinstance(shielded_instance_config, dict):
            shielded_instance_config = NotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig(**shielded_instance_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1532e9410715a2be2fd76ae62612c0364b4244ace5b0f907685f4038ea77199)
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
    def data_disk(self) -> "NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk":
        '''data_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#data_disk NotebooksRuntime#data_disk}
        '''
        result = self._values.get("data_disk")
        assert result is not None, "Required property 'data_disk' is missing"
        return typing.cast("NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk", result)

    @builtins.property
    def machine_type(self) -> builtins.str:
        '''The Compute Engine machine type used for runtimes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#machine_type NotebooksRuntime#machine_type}
        '''
        result = self._values.get("machine_type")
        assert result is not None, "Required property 'machine_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accelerator_config(
        self,
    ) -> typing.Optional["NotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig"]:
        '''accelerator_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#accelerator_config NotebooksRuntime#accelerator_config}
        '''
        result = self._values.get("accelerator_config")
        return typing.cast(typing.Optional["NotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig"], result)

    @builtins.property
    def container_images(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages"]]]:
        '''container_images block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#container_images NotebooksRuntime#container_images}
        '''
        result = self._values.get("container_images")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages"]]], result)

    @builtins.property
    def encryption_config(
        self,
    ) -> typing.Optional["NotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig"]:
        '''encryption_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#encryption_config NotebooksRuntime#encryption_config}
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional["NotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig"], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#internal_ip_only NotebooksRuntime#internal_ip_only}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#labels NotebooksRuntime#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The Compute Engine metadata entries to add to virtual machine. (see [Project and instance metadata](https://cloud.google.com /compute/docs/storing-retrieving-metadata#project_and_instance _metadata)).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#metadata NotebooksRuntime#metadata}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#network NotebooksRuntime#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nic_type(self) -> typing.Optional[builtins.str]:
        '''The type of vNIC to be used on this interface.

        This may be gVNIC
        or VirtioNet. Possible values: ["UNSPECIFIED_NIC_TYPE", "VIRTIO_NET", "GVNIC"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#nic_type NotebooksRuntime#nic_type}
        '''
        result = self._values.get("nic_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reserved_ip_range(self) -> typing.Optional[builtins.str]:
        '''Reserved IP Range name is used for VPC Peering. The subnetwork allocation will use the range *name* if it's assigned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#reserved_ip_range NotebooksRuntime#reserved_ip_range}
        '''
        result = self._values.get("reserved_ip_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shielded_instance_config(
        self,
    ) -> typing.Optional["NotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig"]:
        '''shielded_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#shielded_instance_config NotebooksRuntime#shielded_instance_config}
        '''
        result = self._values.get("shielded_instance_config")
        return typing.cast(typing.Optional["NotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig"], result)

    @builtins.property
    def subnet(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine subnetwork to be used for machine communications.

        Cannot be specified with network. A full URL or
        partial URI are valid. Examples:

        - 'https://www.googleapis.com/compute/v1/projects/[project_id]/
          regions/us-east1/subnetworks/sub0'
        - 'projects/[project_id]/regions/us-east1/subnetworks/sub0'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#subnet NotebooksRuntime#subnet}
        '''
        result = self._values.get("subnet")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Compute Engine tags to add to runtime (see [Tagging instances] (https://cloud.google.com/compute/docs/ label-or-tag-resources#tags)).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#tags NotebooksRuntime#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebooksRuntimeVirtualMachineVirtualMachineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig",
    jsii_struct_bases=[],
    name_mapping={"core_count": "coreCount", "type": "type"},
)
class NotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig:
    def __init__(
        self,
        *,
        core_count: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param core_count: Count of cores of this accelerator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#core_count NotebooksRuntime#core_count}
        :param type: Accelerator model. For valid values, see 'https://cloud.google.com/vertex-ai/docs/workbench/reference/ rest/v1/projects.locations.runtimes#AcceleratorType'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#type NotebooksRuntime#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fddb912ce72f4f51dce310574a28dcc5d764b5268883e0048577347b8e07d5b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#core_count NotebooksRuntime#core_count}
        '''
        result = self._values.get("core_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Accelerator model. For valid values, see 'https://cloud.google.com/vertex-ai/docs/workbench/reference/ rest/v1/projects.locations.runtimes#AcceleratorType'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#type NotebooksRuntime#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d5467d020a68877bfb91805da0f156b08fe3eb42ed3d2008eab3adcb48eee9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c780b4abc2eafa0b596a204763be2b492757c82e87a3052614a7fb113486d994)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coreCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86cf42be4b4b0bf40733df8b57aa2171a3f52659f27e884b5edf121a0562c3e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig]:
        return typing.cast(typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__905c0547be6a90d0d04389aa5262fb184c1ee4cd3441516247bd1654a3b57889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages",
    jsii_struct_bases=[],
    name_mapping={"repository": "repository", "tag": "tag"},
)
class NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages:
    def __init__(
        self,
        *,
        repository: builtins.str,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repository: The path to the container image repository. For example: gcr.io/{project_id}/{imageName}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#repository NotebooksRuntime#repository}
        :param tag: The tag of the container image. If not specified, this defaults to the latest tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#tag NotebooksRuntime#tag}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abad28c9aae098473694982ec1cade54c4b6876e68be37eddb1da29944f652ba)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#repository NotebooksRuntime#repository}
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''The tag of the container image. If not specified, this defaults to the latest tag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#tag NotebooksRuntime#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7530045880d88c2558c9c13bdc4fc72a2427b2e4a246036ff007c6e6a28ef50a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__232a56233e33253964c8fb27b37a9169424207ba904ad9e477551f19fa81d644)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d50a74ecd569fdf045d63bc68ca540ae0a7ab348fddf3cef39149bf0a31f3868)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e93fbd03597711f29b4789f01992670eaac243f32a9e95e0b4dd2bdfa788664)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd187a35bdfcc3c661a5ee645948e5174ffdb55b65520136d4dd3456f505c5f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bb226fbb77da21734f9097e2b7857f52fab18c05a52cfa2531f914ea45deb35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d4dae87bceedcf20b7d9baf5061a61ea4d70f86b9446fc358868fd29a6726fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b85ddf3614a82ad65b7ace7540b789a882a34369bdf2114fa878c2e4db2ff09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a78c6c078045b27b15923a986e7ffab9570b6c48ce98be72676c196fb9fc18d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bfb5a9c143d5afbe3394dbd5b7017fd77cb6db9dceb27d3ee2727f1bfeaffd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk",
    jsii_struct_bases=[],
    name_mapping={
        "initialize_params": "initializeParams",
        "interface": "interface",
        "mode": "mode",
        "source": "source",
        "type": "type",
    },
)
class NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk:
    def __init__(
        self,
        *,
        initialize_params: typing.Optional[typing.Union["NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams", typing.Dict[builtins.str, typing.Any]]] = None,
        interface: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param initialize_params: initialize_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#initialize_params NotebooksRuntime#initialize_params}
        :param interface: "Specifies the disk interface to use for attaching this disk, which is either SCSI or NVME. The default is SCSI. Persistent disks must always use SCSI and the request will fail if you attempt to attach a persistent disk in any other format than SCSI. Local SSDs can use either NVME or SCSI. For performance characteristics of SCSI over NVMe, see Local SSD performance. Valid values: * NVME * SCSI". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#interface NotebooksRuntime#interface}
        :param mode: The mode in which to attach this disk, either READ_WRITE or READ_ONLY. If not specified, the default is to attach the disk in READ_WRITE mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#mode NotebooksRuntime#mode}
        :param source: Specifies a valid partial or full URL to an existing Persistent Disk resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#source NotebooksRuntime#source}
        :param type: Specifies the type of the disk, either SCRATCH or PERSISTENT. If not specified, the default is PERSISTENT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#type NotebooksRuntime#type}
        '''
        if isinstance(initialize_params, dict):
            initialize_params = NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams(**initialize_params)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd9d2970a3109a2a7d77b75abf2dc61e93286180b22969e7c30a53061248b341)
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
    ) -> typing.Optional["NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams"]:
        '''initialize_params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#initialize_params NotebooksRuntime#initialize_params}
        '''
        result = self._values.get("initialize_params")
        return typing.cast(typing.Optional["NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams"], result)

    @builtins.property
    def interface(self) -> typing.Optional[builtins.str]:
        '''"Specifies the disk interface to use for attaching this disk, which is either SCSI or NVME.

        The default is SCSI. Persistent
        disks must always use SCSI and the request will fail if you attempt
        to attach a persistent disk in any other format than SCSI. Local SSDs
        can use either NVME or SCSI. For performance characteristics of SCSI
        over NVMe, see Local SSD performance. Valid values: * NVME * SCSI".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#interface NotebooksRuntime#interface}
        '''
        result = self._values.get("interface")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''The mode in which to attach this disk, either READ_WRITE or READ_ONLY.

        If not specified, the default is to attach
        the disk in READ_WRITE mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#mode NotebooksRuntime#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Specifies a valid partial or full URL to an existing Persistent Disk resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#source NotebooksRuntime#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of the disk, either SCRATCH or PERSISTENT. If not specified, the default is PERSISTENT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#type NotebooksRuntime#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "disk_name": "diskName",
        "disk_size_gb": "diskSizeGb",
        "disk_type": "diskType",
        "labels": "labels",
    },
)
class NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams:
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
        :param description: Provide this property when creating the disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#description NotebooksRuntime#description}
        :param disk_name: Specifies the disk name. If not specified, the default is to use the name of the instance. If the disk with the instance name exists already in the given zone/region, a new name will be automatically generated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#disk_name NotebooksRuntime#disk_name}
        :param disk_size_gb: Specifies the size of the disk in base-2 GB. If not specified, the disk will be the same size as the image (usually 10GB). If specified, the size must be equal to or larger than 10GB. Default 100 GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#disk_size_gb NotebooksRuntime#disk_size_gb}
        :param disk_type: The type of the boot disk attached to this runtime, defaults to standard persistent disk. For valid values, see 'https://cloud.google.com/vertex-ai/docs/workbench/ reference/rest/v1/projects.locations.runtimes#disktype'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#disk_type NotebooksRuntime#disk_type}
        :param labels: Labels to apply to this disk. These can be later modified by the disks.setLabels method. This field is only applicable for persistent disks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#labels NotebooksRuntime#labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc33f93320d80efb74490103cfd63d9f916b035d535ea03e38ce94f6594cb34f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#description NotebooksRuntime#description}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#disk_name NotebooksRuntime#disk_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#disk_size_gb NotebooksRuntime#disk_size_gb}
        '''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_type(self) -> typing.Optional[builtins.str]:
        '''The type of the boot disk attached to this runtime, defaults to standard persistent disk. For valid values, see 'https://cloud.google.com/vertex-ai/docs/workbench/ reference/rest/v1/projects.locations.runtimes#disktype'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#disk_type NotebooksRuntime#disk_type}
        '''
        result = self._values.get("disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels to apply to this disk.

        These can be later modified
        by the disks.setLabels method. This field is only
        applicable for persistent disks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#labels NotebooksRuntime#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e90a5c10e895af270527c7d79e350e7ce8c0b5d720bb7dab2e5f61aff09a3db0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01a2217308ddb9edda841b9e37586eeaba6922d282b10263235c470b2df7352e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskName")
    def disk_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskName"))

    @disk_name.setter
    def disk_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb8b7b42bf9b387b3116d10990ae83f40538f64ae18b9058f5d98e5ee5088695)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66956e8cb1e4a7922897cc1338b50d10f9fa54a621b0e6ab01b535290fb6ad4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskType")
    def disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskType"))

    @disk_type.setter
    def disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e85f6a4095281ee6cacc9c7771a57a2e5f489e378691d4dcc78118bcec2d51df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b58010155e05cfe8a531bdc36f12265d79885c83486f055332c99f53efc879e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams]:
        return typing.cast(typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b85da51f8e460eeb8333b8c991bf3cae17a201ea38cbebeeb4a86d8471b1e1e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07487004a84515a76bf06532d89bb89cc32e802a6de1bbd82f2bb8ada776fcc6)
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
        :param description: Provide this property when creating the disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#description NotebooksRuntime#description}
        :param disk_name: Specifies the disk name. If not specified, the default is to use the name of the instance. If the disk with the instance name exists already in the given zone/region, a new name will be automatically generated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#disk_name NotebooksRuntime#disk_name}
        :param disk_size_gb: Specifies the size of the disk in base-2 GB. If not specified, the disk will be the same size as the image (usually 10GB). If specified, the size must be equal to or larger than 10GB. Default 100 GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#disk_size_gb NotebooksRuntime#disk_size_gb}
        :param disk_type: The type of the boot disk attached to this runtime, defaults to standard persistent disk. For valid values, see 'https://cloud.google.com/vertex-ai/docs/workbench/ reference/rest/v1/projects.locations.runtimes#disktype'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#disk_type NotebooksRuntime#disk_type}
        :param labels: Labels to apply to this disk. These can be later modified by the disks.setLabels method. This field is only applicable for persistent disks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#labels NotebooksRuntime#labels}
        '''
        value = NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams(
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
    ) -> NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParamsOutputReference:
        return typing.cast(NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParamsOutputReference, jsii.get(self, "initializeParams"))

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
    ) -> typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams]:
        return typing.cast(typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams], jsii.get(self, "initializeParamsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6b768ab575ea45b4bc77c999d0d09f5fc4ada24d3b871a3ef28930782833bc8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interface", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__777af3304ff03e0bb6c47fbf4f72d530341d7f15bcfd6e75f4196df9c3fd92b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62d90327b6f9ffd49f9d4be9fc4fae2e2310b84afa18ff03b6710d8c20897b5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85ad223b69c8e03f809dc9865261d34540dcdd1ff8eec1c8a81a018cef5d8f7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk]:
        return typing.cast(typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fda7863869bdf19d037546d3161cb46bde80697aa6c0d3a3822cc5d2e27d349c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig",
    jsii_struct_bases=[],
    name_mapping={"kms_key": "kmsKey"},
)
class NotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig:
    def __init__(self, *, kms_key: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key: The Cloud KMS resource identifier of the customer-managed encryption key used to protect a resource, such as a disks. It has the following format: 'projects/{PROJECT_ID}/locations/{REGION}/keyRings/ {KEY_RING_NAME}/cryptoKeys/{KEY_NAME}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#kms_key NotebooksRuntime#kms_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82defab698e5a452cfa1a6ed4dda89fa623905daab548b3dfbcf646fd0a0b3b1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#kms_key NotebooksRuntime#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9f3e48a8c33110965e355abdb2e508f0941c054f1a0c46fe15216ad5a8d29b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3f7fde0fce6aea0e13bbee8b51a3f126011fbce870292edfba33ad1cdc578a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig]:
        return typing.cast(typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5203006fd167fffdc989ef9d5f1d6b3deea19e4628f7b135a7d61c8962e32f94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NotebooksRuntimeVirtualMachineVirtualMachineConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeVirtualMachineVirtualMachineConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__225d5acb67baaac8c9db3d5828815e0e4d2f5bb98c99337dd7f7b48c06359f89)
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
        :param core_count: Count of cores of this accelerator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#core_count NotebooksRuntime#core_count}
        :param type: Accelerator model. For valid values, see 'https://cloud.google.com/vertex-ai/docs/workbench/reference/ rest/v1/projects.locations.runtimes#AcceleratorType'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#type NotebooksRuntime#type}
        '''
        value = NotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig(
            core_count=core_count, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putAcceleratorConfig", [value]))

    @jsii.member(jsii_name="putContainerImages")
    def put_container_images(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__687bf217664fdd3f715036033a9f5fe75a9144556cdcb88397e74b9f2c920d7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContainerImages", [value]))

    @jsii.member(jsii_name="putDataDisk")
    def put_data_disk(
        self,
        *,
        initialize_params: typing.Optional[typing.Union[NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams, typing.Dict[builtins.str, typing.Any]]] = None,
        interface: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param initialize_params: initialize_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#initialize_params NotebooksRuntime#initialize_params}
        :param interface: "Specifies the disk interface to use for attaching this disk, which is either SCSI or NVME. The default is SCSI. Persistent disks must always use SCSI and the request will fail if you attempt to attach a persistent disk in any other format than SCSI. Local SSDs can use either NVME or SCSI. For performance characteristics of SCSI over NVMe, see Local SSD performance. Valid values: * NVME * SCSI". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#interface NotebooksRuntime#interface}
        :param mode: The mode in which to attach this disk, either READ_WRITE or READ_ONLY. If not specified, the default is to attach the disk in READ_WRITE mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#mode NotebooksRuntime#mode}
        :param source: Specifies a valid partial or full URL to an existing Persistent Disk resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#source NotebooksRuntime#source}
        :param type: Specifies the type of the disk, either SCRATCH or PERSISTENT. If not specified, the default is PERSISTENT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#type NotebooksRuntime#type}
        '''
        value = NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk(
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
        :param kms_key: The Cloud KMS resource identifier of the customer-managed encryption key used to protect a resource, such as a disks. It has the following format: 'projects/{PROJECT_ID}/locations/{REGION}/keyRings/ {KEY_RING_NAME}/cryptoKeys/{KEY_NAME}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#kms_key NotebooksRuntime#kms_key}
        '''
        value = NotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig(
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
        :param enable_integrity_monitoring: Defines whether the instance has integrity monitoring enabled. Enables monitoring and attestation of the boot integrity of the instance. The attestation is performed against the integrity policy baseline. This baseline is initially derived from the implicitly trusted boot image when the instance is created. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#enable_integrity_monitoring NotebooksRuntime#enable_integrity_monitoring}
        :param enable_secure_boot: Defines whether the instance has Secure Boot enabled.Secure Boot helps ensure that the system only runs authentic software by verifying the digital signature of all boot components, and halting the boot process if signature verification fails. Disabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#enable_secure_boot NotebooksRuntime#enable_secure_boot}
        :param enable_vtpm: Defines whether the instance has the vTPM enabled. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#enable_vtpm NotebooksRuntime#enable_vtpm}
        '''
        value = NotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig(
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
    ) -> NotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfigOutputReference:
        return typing.cast(NotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfigOutputReference, jsii.get(self, "acceleratorConfig"))

    @builtins.property
    @jsii.member(jsii_name="containerImages")
    def container_images(
        self,
    ) -> NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImagesList:
        return typing.cast(NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImagesList, jsii.get(self, "containerImages"))

    @builtins.property
    @jsii.member(jsii_name="dataDisk")
    def data_disk(
        self,
    ) -> NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskOutputReference:
        return typing.cast(NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskOutputReference, jsii.get(self, "dataDisk"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfig")
    def encryption_config(
        self,
    ) -> NotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfigOutputReference:
        return typing.cast(NotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfigOutputReference, jsii.get(self, "encryptionConfig"))

    @builtins.property
    @jsii.member(jsii_name="guestAttributes")
    def guest_attributes(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "guestAttributes"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfig")
    def shielded_instance_config(
        self,
    ) -> "NotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfigOutputReference":
        return typing.cast("NotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfigOutputReference", jsii.get(self, "shieldedInstanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorConfigInput")
    def accelerator_config_input(
        self,
    ) -> typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig]:
        return typing.cast(typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig], jsii.get(self, "acceleratorConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="containerImagesInput")
    def container_images_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages]]], jsii.get(self, "containerImagesInput"))

    @builtins.property
    @jsii.member(jsii_name="dataDiskInput")
    def data_disk_input(
        self,
    ) -> typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk]:
        return typing.cast(typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk], jsii.get(self, "dataDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigInput")
    def encryption_config_input(
        self,
    ) -> typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig]:
        return typing.cast(typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig], jsii.get(self, "encryptionConfigInput"))

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
    ) -> typing.Optional["NotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig"]:
        return typing.cast(typing.Optional["NotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig"], jsii.get(self, "shieldedInstanceConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3d9a0fe616deb406f2540fc8182f24b101d0efb89fa1f1b054c4c13c813070a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalIpOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c4624eda5f17db5a1dd5a22beb084c6365075a3b18e2f7c613f24d6af38ebc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95f4b1a24feb4c119a76eced7621c7d44ad270075dd19347c10c9ed5f644862f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e75aea59336000ac12a75ea85f1c7546f49e4b230450053de21991deeb559f19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ffb05203b25b23091959a8d5c61d339bcbedb4b357e6208e4cb8bed772c7959)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nicType")
    def nic_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nicType"))

    @nic_type.setter
    def nic_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa55cae5457cf2e238222989090abaab9563e64a88a40dc0e4bad9b273096de1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nicType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reservedIpRange")
    def reserved_ip_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reservedIpRange"))

    @reserved_ip_range.setter
    def reserved_ip_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b9c068a90e7db2ca5d5aafecb2d4e2e5f76b441d895b3653804193c284e3854)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservedIpRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnet")
    def subnet(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnet"))

    @subnet.setter
    def subnet(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e79f58a6ba2128cec62f04bd7bb8ae3cdcb396678dae7007d502c365c5ca2dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adaff8fd0d72800e4e70cd8670465155cecffbc39ab60dc07b622083008d42bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfig]:
        return typing.cast(typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a5d87b4e9ed4d3ec89b51e46b0d83c688a40972efdc2a248e248cd9f7b7f589)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_integrity_monitoring": "enableIntegrityMonitoring",
        "enable_secure_boot": "enableSecureBoot",
        "enable_vtpm": "enableVtpm",
    },
)
class NotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig:
    def __init__(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Defines whether the instance has integrity monitoring enabled. Enables monitoring and attestation of the boot integrity of the instance. The attestation is performed against the integrity policy baseline. This baseline is initially derived from the implicitly trusted boot image when the instance is created. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#enable_integrity_monitoring NotebooksRuntime#enable_integrity_monitoring}
        :param enable_secure_boot: Defines whether the instance has Secure Boot enabled.Secure Boot helps ensure that the system only runs authentic software by verifying the digital signature of all boot components, and halting the boot process if signature verification fails. Disabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#enable_secure_boot NotebooksRuntime#enable_secure_boot}
        :param enable_vtpm: Defines whether the instance has the vTPM enabled. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#enable_vtpm NotebooksRuntime#enable_vtpm}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85b1117a2bb8b40e0c522976556e7077dd84231bc3470e1ef59af23a9a713a4a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#enable_integrity_monitoring NotebooksRuntime#enable_integrity_monitoring}
        '''
        result = self._values.get("enable_integrity_monitoring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_secure_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether the instance has Secure Boot enabled.Secure Boot helps ensure that the system only runs authentic software by verifying the digital signature of all boot components, and halting the boot process if signature verification fails. Disabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#enable_secure_boot NotebooksRuntime#enable_secure_boot}
        '''
        result = self._values.get("enable_secure_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_vtpm(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether the instance has the vTPM enabled. Enabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_runtime#enable_vtpm NotebooksRuntime#enable_vtpm}
        '''
        result = self._values.get("enable_vtpm")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksRuntime.NotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89b6f18ddcacbb1b48fa694821a8fbbee07be38a2fc1a26eaa18d6326b6288ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4aa69044a18e934ea69f6f4eeaec4c4ebf5f0617a0aa404bb66d62e3cbdacf46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cea47d6318c65ea976e951c763902af61ed0a4cae8c0f504df92c506fee1fe6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__704116b7ec659d7a2fe5fa9ee4fbd53030dd3d1ca4d46124deb2a78f9cf924ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableVtpm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig]:
        return typing.cast(typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb0cfc852dc91b5a7176f051cbd803178f88919d98e1a6bf534ede965cbf0ced)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NotebooksRuntime",
    "NotebooksRuntimeAccessConfig",
    "NotebooksRuntimeAccessConfigOutputReference",
    "NotebooksRuntimeConfig",
    "NotebooksRuntimeMetrics",
    "NotebooksRuntimeMetricsList",
    "NotebooksRuntimeMetricsOutputReference",
    "NotebooksRuntimeSoftwareConfig",
    "NotebooksRuntimeSoftwareConfigKernels",
    "NotebooksRuntimeSoftwareConfigKernelsList",
    "NotebooksRuntimeSoftwareConfigKernelsOutputReference",
    "NotebooksRuntimeSoftwareConfigOutputReference",
    "NotebooksRuntimeTimeouts",
    "NotebooksRuntimeTimeoutsOutputReference",
    "NotebooksRuntimeVirtualMachine",
    "NotebooksRuntimeVirtualMachineOutputReference",
    "NotebooksRuntimeVirtualMachineVirtualMachineConfig",
    "NotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig",
    "NotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfigOutputReference",
    "NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages",
    "NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImagesList",
    "NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImagesOutputReference",
    "NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk",
    "NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams",
    "NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParamsOutputReference",
    "NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskOutputReference",
    "NotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig",
    "NotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfigOutputReference",
    "NotebooksRuntimeVirtualMachineVirtualMachineConfigOutputReference",
    "NotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig",
    "NotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfigOutputReference",
]

publication.publish()

def _typecheckingstub__538f5371073e53053f64ff03aea5d925f3604c2235ec4b48af8b1c0515bdb122(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    access_config: typing.Optional[typing.Union[NotebooksRuntimeAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    software_config: typing.Optional[typing.Union[NotebooksRuntimeSoftwareConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[NotebooksRuntimeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_machine: typing.Optional[typing.Union[NotebooksRuntimeVirtualMachine, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e4041763cd159c5306192fd90bd439723cd33ff62feb62c852471dc0fcde67e0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac97a06af70d9b6c6656aa506f54ec7426c9a8b9885f80fab511f3b93d26054(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0390213f5ab1aed52e2ea40966dce1bcc1af267c26efc299ff3d0ea41c51cb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbdc16fe09ff602f1dc37123257a9655aeaafad1abb79718e1dc0493355f6407(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e1c6ab29c3fc0b86ed4660f64e0df774653f2d48c983dc8c1ac02336ecd2940(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81cf537c961dd88786b8aff002bdc40b726661b936adb2100c9b8203c5f7bd38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca88bd179817874965ad2b85c4aaba760a00b63f9a92a1e1c528a19a558779f(
    *,
    access_type: typing.Optional[builtins.str] = None,
    runtime_owner: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63edfb28bf584fd41fdaa08886b93005517d6b1ccb36fb035fe65a8c776c4dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68573e197ed2948b5d6d59add52b9a9446b90265473ac0b948a5586365502d79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53d718f48b1e1f6500c989f8e3dbd09dad212ab4efc83ad144e970e477ead53e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__392d6e31bbe3990a5e5f5ce60fc1d367c2fec23ae7e50ddb744e8d5d9c20580f(
    value: typing.Optional[NotebooksRuntimeAccessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7277f1b620710067f454680e647b2350824602ec2807895bf2323322e6b5e4e4(
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
    access_config: typing.Optional[typing.Union[NotebooksRuntimeAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    software_config: typing.Optional[typing.Union[NotebooksRuntimeSoftwareConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[NotebooksRuntimeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_machine: typing.Optional[typing.Union[NotebooksRuntimeVirtualMachine, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edca6f7b762cefcffbe6ee409bb43253e53a51aec6e940db7af0f66a699b1441(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f740aeee35ccd95f34ca986f97e3087c5ed8fd029575a81d6662c8f266a4031(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cada24f09a7411f029e3a531fad9cfed22c8ef1fc1f834c9bde5ad2b720d70f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb8d5599baec48c86f106e14f844a66fadd8b63d229fec4ed9600356f2b1d52c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4867d11b1d57661905e0dcae7d483902a16ccd422631d9f097d3b94f301efc46(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b205ae1169040a3e4f457e1b160db9f1dd3a599390d57fc65a7cb250d0a275c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__848d938767efe8589d028b5aa5d30dd59cbee0ffab239e10992a0ab93adeca22(
    value: typing.Optional[NotebooksRuntimeMetrics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e72ae8716b8627284757ee8e6167e7dc10ce965a5c85cc37d838c93897fa9627(
    *,
    custom_gpu_driver_path: typing.Optional[builtins.str] = None,
    enable_health_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    idle_shutdown: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    idle_shutdown_timeout: typing.Optional[jsii.Number] = None,
    install_gpu_driver: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    kernels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NotebooksRuntimeSoftwareConfigKernels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    notebook_upgrade_schedule: typing.Optional[builtins.str] = None,
    post_startup_script: typing.Optional[builtins.str] = None,
    post_startup_script_behavior: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__052fc3403b6dfad04078599ae41363d36bcbe2af4646f69f915e1166b6bada78(
    *,
    repository: builtins.str,
    tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5dc296b6950595ca9ff22d68da70b622b3f982e2421b84ef973821720ba7244(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d655ffb7fc3ba951d4da99534fa3234b9c363eca575c719155c52843b41550(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8924c4a3be66430c75e1ff4517d775fd64b3b005a2d9637b90dd0f38d61cc1e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13b326862c3588b3babc53919506da07c6c49d75b85cd76c201bb2d15e4818aa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__759fc549311f2304fb771e7efc2fcf22dbbe1d60cd8885d0e780142362a09a5b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f5ba1c90ce597bb900cf5ab05d434b841490bd055f3b362b5e4bd5a8886da4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NotebooksRuntimeSoftwareConfigKernels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9bf2a03a251d1f980db32a3312a75d4b5f56405dbfa3bb8ba532b49c39bb229(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9579e15807400219e1a2ae01fd29fd918899df1771c4400e8e6063c12193ae72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fafdfecbd364a77cc342ddf98d78401e06a231121749b65abb01d3921a58f6be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cf9c6083f4d9ca1f4d39ed89794d3c37b627ddfe388e6e940a5c279526cb286(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NotebooksRuntimeSoftwareConfigKernels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d01ce5fe70c3300070d4aca274e8551de3c7d9830d16cc91c54a28610b114b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__770f86841c30636ceae9ed654bc8fe3152fc4a66efb418462028d20c3e9c9ca6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NotebooksRuntimeSoftwareConfigKernels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e733d9dfd8d2a833074e996fa60f2f7b65bf916052ff6cb373f2597327518ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aff68b1e662956e97a3a4120d9870a6fb39bab55d257a57e64dd409e3dc9c39d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb63a818062f37fe52ebcf56c3c0dd1a0716077e7afa71c4ca41e08dcb6cbee(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9efa728159dadaaed4faeec75aa74f8fe87791dbdb706f6045818106dd4cc684(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1102339bc8e300cc552f49effda99ee928aae06a0bed0e447945800ce42e4bf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b3b1524123f23dc04dfba87262886efee2e61aeacec2cbd146329ab052a71f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d662ffb8e1e2f4039986e84cca30e88d41df8de6ed41f824f299209b4528bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adb6015af20d27a49586767db95013e2e171c215dbdb65b1eac44f82fff35f4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b7a6f759a93706a6e8508a8d94eceeddd904901cfd16563ddfb0a1746a4cb6d(
    value: typing.Optional[NotebooksRuntimeSoftwareConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac521fd37f4c9926107259a6e3ae06eaf204cf5b13f39ad1ccc984bcb1d39915(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__261741b2fd52b6d984cff4074ba77f85fe0e86af09eed09ff8cb63480cf0da45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2b17ad8bfbbc8f14858e0b323931b251606fc856abac18befd63ad9f790ac06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a74d39100cbcd4c5d131c15cb07ea48e1d2ad843b6e30c3d5f374d4be0fb3f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adc2a8a081b5e5e931daac094869e8c57ae7d185d020934437a78fd62fa9d826(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaaf7f0cc53237d3e4f9ba96f28053177181db18be3a6dacd5bcae77feb175af(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NotebooksRuntimeTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf5ce8a5cd4ac08fab1139ba74543b8f5d8b8889b2805bab510b9bdf86a3e388(
    *,
    virtual_machine_config: typing.Optional[typing.Union[NotebooksRuntimeVirtualMachineVirtualMachineConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3174bea105ddc8daab514ec952d7668aae2b722fdb7d2c61203f06ab84dfb8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87118287f4f4a2a13e3f7bce31a1caf6b741cd1016a7aa7b572aa90ab8022c5e(
    value: typing.Optional[NotebooksRuntimeVirtualMachine],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1532e9410715a2be2fd76ae62612c0364b4244ace5b0f907685f4038ea77199(
    *,
    data_disk: typing.Union[NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk, typing.Dict[builtins.str, typing.Any]],
    machine_type: builtins.str,
    accelerator_config: typing.Optional[typing.Union[NotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    container_images: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages, typing.Dict[builtins.str, typing.Any]]]]] = None,
    encryption_config: typing.Optional[typing.Union[NotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    internal_ip_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    network: typing.Optional[builtins.str] = None,
    nic_type: typing.Optional[builtins.str] = None,
    reserved_ip_range: typing.Optional[builtins.str] = None,
    shielded_instance_config: typing.Optional[typing.Union[NotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    subnet: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fddb912ce72f4f51dce310574a28dcc5d764b5268883e0048577347b8e07d5b(
    *,
    core_count: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5467d020a68877bfb91805da0f156b08fe3eb42ed3d2008eab3adcb48eee9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c780b4abc2eafa0b596a204763be2b492757c82e87a3052614a7fb113486d994(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86cf42be4b4b0bf40733df8b57aa2171a3f52659f27e884b5edf121a0562c3e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__905c0547be6a90d0d04389aa5262fb184c1ee4cd3441516247bd1654a3b57889(
    value: typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigAcceleratorConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abad28c9aae098473694982ec1cade54c4b6876e68be37eddb1da29944f652ba(
    *,
    repository: builtins.str,
    tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7530045880d88c2558c9c13bdc4fc72a2427b2e4a246036ff007c6e6a28ef50a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__232a56233e33253964c8fb27b37a9169424207ba904ad9e477551f19fa81d644(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50a74ecd569fdf045d63bc68ca540ae0a7ab348fddf3cef39149bf0a31f3868(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e93fbd03597711f29b4789f01992670eaac243f32a9e95e0b4dd2bdfa788664(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd187a35bdfcc3c661a5ee645948e5174ffdb55b65520136d4dd3456f505c5f8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bb226fbb77da21734f9097e2b7857f52fab18c05a52cfa2531f914ea45deb35(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d4dae87bceedcf20b7d9baf5061a61ea4d70f86b9446fc358868fd29a6726fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b85ddf3614a82ad65b7ace7540b789a882a34369bdf2114fa878c2e4db2ff09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a78c6c078045b27b15923a986e7ffab9570b6c48ce98be72676c196fb9fc18d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bfb5a9c143d5afbe3394dbd5b7017fd77cb6db9dceb27d3ee2727f1bfeaffd2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd9d2970a3109a2a7d77b75abf2dc61e93286180b22969e7c30a53061248b341(
    *,
    initialize_params: typing.Optional[typing.Union[NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams, typing.Dict[builtins.str, typing.Any]]] = None,
    interface: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc33f93320d80efb74490103cfd63d9f916b035d535ea03e38ce94f6594cb34f(
    *,
    description: typing.Optional[builtins.str] = None,
    disk_name: typing.Optional[builtins.str] = None,
    disk_size_gb: typing.Optional[jsii.Number] = None,
    disk_type: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e90a5c10e895af270527c7d79e350e7ce8c0b5d720bb7dab2e5f61aff09a3db0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a2217308ddb9edda841b9e37586eeaba6922d282b10263235c470b2df7352e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb8b7b42bf9b387b3116d10990ae83f40538f64ae18b9058f5d98e5ee5088695(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66956e8cb1e4a7922897cc1338b50d10f9fa54a621b0e6ab01b535290fb6ad4f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e85f6a4095281ee6cacc9c7771a57a2e5f489e378691d4dcc78118bcec2d51df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b58010155e05cfe8a531bdc36f12265d79885c83486f055332c99f53efc879e0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b85da51f8e460eeb8333b8c991bf3cae17a201ea38cbebeeb4a86d8471b1e1e2(
    value: typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParams],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07487004a84515a76bf06532d89bb89cc32e802a6de1bbd82f2bb8ada776fcc6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b768ab575ea45b4bc77c999d0d09f5fc4ada24d3b871a3ef28930782833bc8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__777af3304ff03e0bb6c47fbf4f72d530341d7f15bcfd6e75f4196df9c3fd92b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62d90327b6f9ffd49f9d4be9fc4fae2e2310b84afa18ff03b6710d8c20897b5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85ad223b69c8e03f809dc9865261d34540dcdd1ff8eec1c8a81a018cef5d8f7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fda7863869bdf19d037546d3161cb46bde80697aa6c0d3a3822cc5d2e27d349c(
    value: typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigDataDisk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82defab698e5a452cfa1a6ed4dda89fa623905daab548b3dfbcf646fd0a0b3b1(
    *,
    kms_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9f3e48a8c33110965e355abdb2e508f0941c054f1a0c46fe15216ad5a8d29b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f7fde0fce6aea0e13bbee8b51a3f126011fbce870292edfba33ad1cdc578a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5203006fd167fffdc989ef9d5f1d6b3deea19e4628f7b135a7d61c8962e32f94(
    value: typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigEncryptionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225d5acb67baaac8c9db3d5828815e0e4d2f5bb98c99337dd7f7b48c06359f89(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__687bf217664fdd3f715036033a9f5fe75a9144556cdcb88397e74b9f2c920d7b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NotebooksRuntimeVirtualMachineVirtualMachineConfigContainerImages, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d9a0fe616deb406f2540fc8182f24b101d0efb89fa1f1b054c4c13c813070a9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c4624eda5f17db5a1dd5a22beb084c6365075a3b18e2f7c613f24d6af38ebc1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f4b1a24feb4c119a76eced7621c7d44ad270075dd19347c10c9ed5f644862f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e75aea59336000ac12a75ea85f1c7546f49e4b230450053de21991deeb559f19(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ffb05203b25b23091959a8d5c61d339bcbedb4b357e6208e4cb8bed772c7959(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa55cae5457cf2e238222989090abaab9563e64a88a40dc0e4bad9b273096de1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b9c068a90e7db2ca5d5aafecb2d4e2e5f76b441d895b3653804193c284e3854(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e79f58a6ba2128cec62f04bd7bb8ae3cdcb396678dae7007d502c365c5ca2dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adaff8fd0d72800e4e70cd8670465155cecffbc39ab60dc07b622083008d42bf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a5d87b4e9ed4d3ec89b51e46b0d83c688a40972efdc2a248e248cd9f7b7f589(
    value: typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b1117a2bb8b40e0c522976556e7077dd84231bc3470e1ef59af23a9a713a4a(
    *,
    enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b6f18ddcacbb1b48fa694821a8fbbee07be38a2fc1a26eaa18d6326b6288ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aa69044a18e934ea69f6f4eeaec4c4ebf5f0617a0aa404bb66d62e3cbdacf46(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cea47d6318c65ea976e951c763902af61ed0a4cae8c0f504df92c506fee1fe6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__704116b7ec659d7a2fe5fa9ee4fbd53030dd3d1ca4d46124deb2a78f9cf924ae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb0cfc852dc91b5a7176f051cbd803178f88919d98e1a6bf534ede965cbf0ced(
    value: typing.Optional[NotebooksRuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass
