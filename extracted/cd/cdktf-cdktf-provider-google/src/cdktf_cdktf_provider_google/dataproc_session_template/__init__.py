r'''
# `google_dataproc_session_template`

Refer to the Terraform Registry for docs: [`google_dataproc_session_template`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template).
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


class DataprocSessionTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocSessionTemplate.DataprocSessionTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template google_dataproc_session_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        environment_config: typing.Optional[typing.Union["DataprocSessionTemplateEnvironmentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        jupyter_session: typing.Optional[typing.Union["DataprocSessionTemplateJupyterSession", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        runtime_config: typing.Optional[typing.Union["DataprocSessionTemplateRuntimeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_connect_session: typing.Optional[typing.Union["DataprocSessionTemplateSparkConnectSession", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DataprocSessionTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template google_dataproc_session_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The resource name of the session template in the following format: projects/{project}/locations/{location}/sessionTemplates/{template_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#name DataprocSessionTemplate#name}
        :param environment_config: environment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#environment_config DataprocSessionTemplate#environment_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#id DataprocSessionTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jupyter_session: jupyter_session block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#jupyter_session DataprocSessionTemplate#jupyter_session}
        :param labels: The labels to associate with this session template. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#labels DataprocSessionTemplate#labels}
        :param location: The location in which the session template will be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#location DataprocSessionTemplate#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#project DataprocSessionTemplate#project}.
        :param runtime_config: runtime_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#runtime_config DataprocSessionTemplate#runtime_config}
        :param spark_connect_session: spark_connect_session block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#spark_connect_session DataprocSessionTemplate#spark_connect_session}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#timeouts DataprocSessionTemplate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5fa9c162e4246d9889bd6140b594bd2b34dea970e85978ad66872a0fdd1c3da)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataprocSessionTemplateConfig(
            name=name,
            environment_config=environment_config,
            id=id,
            jupyter_session=jupyter_session,
            labels=labels,
            location=location,
            project=project,
            runtime_config=runtime_config,
            spark_connect_session=spark_connect_session,
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
        '''Generates CDKTF code for importing a DataprocSessionTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataprocSessionTemplate to import.
        :param import_from_id: The id of the existing DataprocSessionTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataprocSessionTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6b6a35475222428f5c9977c8e43e7381d2db58cf46c9da70ee187b10be62d47)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEnvironmentConfig")
    def put_environment_config(
        self,
        *,
        execution_config: typing.Optional[typing.Union["DataprocSessionTemplateEnvironmentConfigExecutionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        peripherals_config: typing.Optional[typing.Union["DataprocSessionTemplateEnvironmentConfigPeripheralsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param execution_config: execution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#execution_config DataprocSessionTemplate#execution_config}
        :param peripherals_config: peripherals_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#peripherals_config DataprocSessionTemplate#peripherals_config}
        '''
        value = DataprocSessionTemplateEnvironmentConfig(
            execution_config=execution_config, peripherals_config=peripherals_config
        )

        return typing.cast(None, jsii.invoke(self, "putEnvironmentConfig", [value]))

    @jsii.member(jsii_name="putJupyterSession")
    def put_jupyter_session(
        self,
        *,
        display_name: typing.Optional[builtins.str] = None,
        kernel: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param display_name: Display name, shown in the Jupyter kernelspec card. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#display_name DataprocSessionTemplate#display_name}
        :param kernel: Kernel to be used with Jupyter interactive session. Possible values: ["PYTHON", "SCALA"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#kernel DataprocSessionTemplate#kernel}
        '''
        value = DataprocSessionTemplateJupyterSession(
            display_name=display_name, kernel=kernel
        )

        return typing.cast(None, jsii.invoke(self, "putJupyterSession", [value]))

    @jsii.member(jsii_name="putRuntimeConfig")
    def put_runtime_config(
        self,
        *,
        container_image: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_image: Optional custom container image for the job runtime environment. If not specified, a default container image will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#container_image DataprocSessionTemplate#container_image}
        :param properties: A mapping of property names to values, which are used to configure workload execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#properties DataprocSessionTemplate#properties}
        :param version: Version of the session runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#version DataprocSessionTemplate#version}
        '''
        value = DataprocSessionTemplateRuntimeConfig(
            container_image=container_image, properties=properties, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putRuntimeConfig", [value]))

    @jsii.member(jsii_name="putSparkConnectSession")
    def put_spark_connect_session(self) -> None:
        value = DataprocSessionTemplateSparkConnectSession()

        return typing.cast(None, jsii.invoke(self, "putSparkConnectSession", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#create DataprocSessionTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#delete DataprocSessionTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#update DataprocSessionTemplate#update}.
        '''
        value = DataprocSessionTemplateTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetEnvironmentConfig")
    def reset_environment_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironmentConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetJupyterSession")
    def reset_jupyter_session(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJupyterSession", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRuntimeConfig")
    def reset_runtime_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeConfig", []))

    @jsii.member(jsii_name="resetSparkConnectSession")
    def reset_spark_connect_session(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkConnectSession", []))

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
    @jsii.member(jsii_name="environmentConfig")
    def environment_config(
        self,
    ) -> "DataprocSessionTemplateEnvironmentConfigOutputReference":
        return typing.cast("DataprocSessionTemplateEnvironmentConfigOutputReference", jsii.get(self, "environmentConfig"))

    @builtins.property
    @jsii.member(jsii_name="jupyterSession")
    def jupyter_session(self) -> "DataprocSessionTemplateJupyterSessionOutputReference":
        return typing.cast("DataprocSessionTemplateJupyterSessionOutputReference", jsii.get(self, "jupyterSession"))

    @builtins.property
    @jsii.member(jsii_name="runtimeConfig")
    def runtime_config(self) -> "DataprocSessionTemplateRuntimeConfigOutputReference":
        return typing.cast("DataprocSessionTemplateRuntimeConfigOutputReference", jsii.get(self, "runtimeConfig"))

    @builtins.property
    @jsii.member(jsii_name="sparkConnectSession")
    def spark_connect_session(
        self,
    ) -> "DataprocSessionTemplateSparkConnectSessionOutputReference":
        return typing.cast("DataprocSessionTemplateSparkConnectSessionOutputReference", jsii.get(self, "sparkConnectSession"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataprocSessionTemplateTimeoutsOutputReference":
        return typing.cast("DataprocSessionTemplateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uuid"))

    @builtins.property
    @jsii.member(jsii_name="environmentConfigInput")
    def environment_config_input(
        self,
    ) -> typing.Optional["DataprocSessionTemplateEnvironmentConfig"]:
        return typing.cast(typing.Optional["DataprocSessionTemplateEnvironmentConfig"], jsii.get(self, "environmentConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="jupyterSessionInput")
    def jupyter_session_input(
        self,
    ) -> typing.Optional["DataprocSessionTemplateJupyterSession"]:
        return typing.cast(typing.Optional["DataprocSessionTemplateJupyterSession"], jsii.get(self, "jupyterSessionInput"))

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
    @jsii.member(jsii_name="runtimeConfigInput")
    def runtime_config_input(
        self,
    ) -> typing.Optional["DataprocSessionTemplateRuntimeConfig"]:
        return typing.cast(typing.Optional["DataprocSessionTemplateRuntimeConfig"], jsii.get(self, "runtimeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkConnectSessionInput")
    def spark_connect_session_input(
        self,
    ) -> typing.Optional["DataprocSessionTemplateSparkConnectSession"]:
        return typing.cast(typing.Optional["DataprocSessionTemplateSparkConnectSession"], jsii.get(self, "sparkConnectSessionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataprocSessionTemplateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataprocSessionTemplateTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b32e06810b7d2cc59c3bcfbefd08f23a1f6e282c90725bf05b596dd8a9bf4ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c81de4996ce69269aa51fe51f03bd60549b0b655b72d1ebb21536304f5d4c9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9678c928012a3ae16d53224f97cb3b4e07d129e0a1dd1f9ec81f4dd4a55f70d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b88be3e63786cd5f1bdaebf82b995becdb48984c63fa1f05e10659e83aa68c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba363bc0286f593e3208626a9d6de602ac28b29575da584b75f3bd5bab1376b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocSessionTemplate.DataprocSessionTemplateConfig",
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
        "environment_config": "environmentConfig",
        "id": "id",
        "jupyter_session": "jupyterSession",
        "labels": "labels",
        "location": "location",
        "project": "project",
        "runtime_config": "runtimeConfig",
        "spark_connect_session": "sparkConnectSession",
        "timeouts": "timeouts",
    },
)
class DataprocSessionTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        environment_config: typing.Optional[typing.Union["DataprocSessionTemplateEnvironmentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        jupyter_session: typing.Optional[typing.Union["DataprocSessionTemplateJupyterSession", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        runtime_config: typing.Optional[typing.Union["DataprocSessionTemplateRuntimeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_connect_session: typing.Optional[typing.Union["DataprocSessionTemplateSparkConnectSession", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DataprocSessionTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The resource name of the session template in the following format: projects/{project}/locations/{location}/sessionTemplates/{template_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#name DataprocSessionTemplate#name}
        :param environment_config: environment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#environment_config DataprocSessionTemplate#environment_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#id DataprocSessionTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jupyter_session: jupyter_session block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#jupyter_session DataprocSessionTemplate#jupyter_session}
        :param labels: The labels to associate with this session template. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#labels DataprocSessionTemplate#labels}
        :param location: The location in which the session template will be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#location DataprocSessionTemplate#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#project DataprocSessionTemplate#project}.
        :param runtime_config: runtime_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#runtime_config DataprocSessionTemplate#runtime_config}
        :param spark_connect_session: spark_connect_session block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#spark_connect_session DataprocSessionTemplate#spark_connect_session}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#timeouts DataprocSessionTemplate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(environment_config, dict):
            environment_config = DataprocSessionTemplateEnvironmentConfig(**environment_config)
        if isinstance(jupyter_session, dict):
            jupyter_session = DataprocSessionTemplateJupyterSession(**jupyter_session)
        if isinstance(runtime_config, dict):
            runtime_config = DataprocSessionTemplateRuntimeConfig(**runtime_config)
        if isinstance(spark_connect_session, dict):
            spark_connect_session = DataprocSessionTemplateSparkConnectSession(**spark_connect_session)
        if isinstance(timeouts, dict):
            timeouts = DataprocSessionTemplateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e600ae3c7151dca60aadc5268d17461b01ab369cfd89f0d14e684b69403c296)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument environment_config", value=environment_config, expected_type=type_hints["environment_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument jupyter_session", value=jupyter_session, expected_type=type_hints["jupyter_session"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument runtime_config", value=runtime_config, expected_type=type_hints["runtime_config"])
            check_type(argname="argument spark_connect_session", value=spark_connect_session, expected_type=type_hints["spark_connect_session"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
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
        if environment_config is not None:
            self._values["environment_config"] = environment_config
        if id is not None:
            self._values["id"] = id
        if jupyter_session is not None:
            self._values["jupyter_session"] = jupyter_session
        if labels is not None:
            self._values["labels"] = labels
        if location is not None:
            self._values["location"] = location
        if project is not None:
            self._values["project"] = project
        if runtime_config is not None:
            self._values["runtime_config"] = runtime_config
        if spark_connect_session is not None:
            self._values["spark_connect_session"] = spark_connect_session
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
    def name(self) -> builtins.str:
        '''The resource name of the session template in the following format: projects/{project}/locations/{location}/sessionTemplates/{template_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#name DataprocSessionTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def environment_config(
        self,
    ) -> typing.Optional["DataprocSessionTemplateEnvironmentConfig"]:
        '''environment_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#environment_config DataprocSessionTemplate#environment_config}
        '''
        result = self._values.get("environment_config")
        return typing.cast(typing.Optional["DataprocSessionTemplateEnvironmentConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#id DataprocSessionTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jupyter_session(
        self,
    ) -> typing.Optional["DataprocSessionTemplateJupyterSession"]:
        '''jupyter_session block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#jupyter_session DataprocSessionTemplate#jupyter_session}
        '''
        result = self._values.get("jupyter_session")
        return typing.cast(typing.Optional["DataprocSessionTemplateJupyterSession"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The labels to associate with this session template.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#labels DataprocSessionTemplate#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location in which the session template will be created in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#location DataprocSessionTemplate#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#project DataprocSessionTemplate#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_config(self) -> typing.Optional["DataprocSessionTemplateRuntimeConfig"]:
        '''runtime_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#runtime_config DataprocSessionTemplate#runtime_config}
        '''
        result = self._values.get("runtime_config")
        return typing.cast(typing.Optional["DataprocSessionTemplateRuntimeConfig"], result)

    @builtins.property
    def spark_connect_session(
        self,
    ) -> typing.Optional["DataprocSessionTemplateSparkConnectSession"]:
        '''spark_connect_session block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#spark_connect_session DataprocSessionTemplate#spark_connect_session}
        '''
        result = self._values.get("spark_connect_session")
        return typing.cast(typing.Optional["DataprocSessionTemplateSparkConnectSession"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataprocSessionTemplateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#timeouts DataprocSessionTemplate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataprocSessionTemplateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocSessionTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocSessionTemplate.DataprocSessionTemplateEnvironmentConfig",
    jsii_struct_bases=[],
    name_mapping={
        "execution_config": "executionConfig",
        "peripherals_config": "peripheralsConfig",
    },
)
class DataprocSessionTemplateEnvironmentConfig:
    def __init__(
        self,
        *,
        execution_config: typing.Optional[typing.Union["DataprocSessionTemplateEnvironmentConfigExecutionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        peripherals_config: typing.Optional[typing.Union["DataprocSessionTemplateEnvironmentConfigPeripheralsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param execution_config: execution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#execution_config DataprocSessionTemplate#execution_config}
        :param peripherals_config: peripherals_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#peripherals_config DataprocSessionTemplate#peripherals_config}
        '''
        if isinstance(execution_config, dict):
            execution_config = DataprocSessionTemplateEnvironmentConfigExecutionConfig(**execution_config)
        if isinstance(peripherals_config, dict):
            peripherals_config = DataprocSessionTemplateEnvironmentConfigPeripheralsConfig(**peripherals_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__206799d30edea13161dff4be404d24bcf47adc35d2d08bb523c6c3423a100cfd)
            check_type(argname="argument execution_config", value=execution_config, expected_type=type_hints["execution_config"])
            check_type(argname="argument peripherals_config", value=peripherals_config, expected_type=type_hints["peripherals_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if execution_config is not None:
            self._values["execution_config"] = execution_config
        if peripherals_config is not None:
            self._values["peripherals_config"] = peripherals_config

    @builtins.property
    def execution_config(
        self,
    ) -> typing.Optional["DataprocSessionTemplateEnvironmentConfigExecutionConfig"]:
        '''execution_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#execution_config DataprocSessionTemplate#execution_config}
        '''
        result = self._values.get("execution_config")
        return typing.cast(typing.Optional["DataprocSessionTemplateEnvironmentConfigExecutionConfig"], result)

    @builtins.property
    def peripherals_config(
        self,
    ) -> typing.Optional["DataprocSessionTemplateEnvironmentConfigPeripheralsConfig"]:
        '''peripherals_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#peripherals_config DataprocSessionTemplate#peripherals_config}
        '''
        result = self._values.get("peripherals_config")
        return typing.cast(typing.Optional["DataprocSessionTemplateEnvironmentConfigPeripheralsConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocSessionTemplateEnvironmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocSessionTemplate.DataprocSessionTemplateEnvironmentConfigExecutionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key": "kmsKey",
        "network_tags": "networkTags",
        "service_account": "serviceAccount",
        "staging_bucket": "stagingBucket",
        "subnetwork_uri": "subnetworkUri",
        "ttl": "ttl",
    },
)
class DataprocSessionTemplateEnvironmentConfigExecutionConfig:
    def __init__(
        self,
        *,
        kms_key: typing.Optional[builtins.str] = None,
        network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_account: typing.Optional[builtins.str] = None,
        staging_bucket: typing.Optional[builtins.str] = None,
        subnetwork_uri: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key: The Cloud KMS key to use for encryption. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#kms_key DataprocSessionTemplate#kms_key}
        :param network_tags: Tags used for network traffic control. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#network_tags DataprocSessionTemplate#network_tags}
        :param service_account: Service account that used to execute workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#service_account DataprocSessionTemplate#service_account}
        :param staging_bucket: A Cloud Storage bucket used to stage workload dependencies, config files, and store workload output and other ephemeral data, such as Spark history files. If you do not specify a staging bucket, Cloud Dataproc will determine a Cloud Storage location according to the region where your workload is running, and then create and manage project-level, per-location staging and temporary buckets. This field requires a Cloud Storage bucket name, not a gs://... URI to a Cloud Storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#staging_bucket DataprocSessionTemplate#staging_bucket}
        :param subnetwork_uri: Subnetwork configuration for workload execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#subnetwork_uri DataprocSessionTemplate#subnetwork_uri}
        :param ttl: The duration after which the workload will be terminated. When the workload exceeds this duration, it will be unconditionally terminated without waiting for ongoing work to finish. If ttl is not specified for a session workload, the workload will be allowed to run until it exits naturally (or run forever without exiting). If ttl is not specified for an interactive session, it defaults to 24 hours. If ttl is not specified for a batch that uses 2.1+ runtime version, it defaults to 4 hours. Minimum value is 10 minutes; maximum value is 14 days. If both ttl and idleTtl are specified (for an interactive session), the conditions are treated as OR conditions: the workload will be terminated when it has been idle for idleTtl or when ttl has been exceeded, whichever occurs first. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#ttl DataprocSessionTemplate#ttl}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5166259c1ac803767adfbe107cce46ea849eb511864d75c3c88774f7a03056ec)
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument network_tags", value=network_tags, expected_type=type_hints["network_tags"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument staging_bucket", value=staging_bucket, expected_type=type_hints["staging_bucket"])
            check_type(argname="argument subnetwork_uri", value=subnetwork_uri, expected_type=type_hints["subnetwork_uri"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if network_tags is not None:
            self._values["network_tags"] = network_tags
        if service_account is not None:
            self._values["service_account"] = service_account
        if staging_bucket is not None:
            self._values["staging_bucket"] = staging_bucket
        if subnetwork_uri is not None:
            self._values["subnetwork_uri"] = subnetwork_uri
        if ttl is not None:
            self._values["ttl"] = ttl

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The Cloud KMS key to use for encryption.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#kms_key DataprocSessionTemplate#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags used for network traffic control.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#network_tags DataprocSessionTemplate#network_tags}
        '''
        result = self._values.get("network_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''Service account that used to execute workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#service_account DataprocSessionTemplate#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def staging_bucket(self) -> typing.Optional[builtins.str]:
        '''A Cloud Storage bucket used to stage workload dependencies, config files, and store workload output and other ephemeral data, such as Spark history files.

        If you do not specify a staging bucket,
        Cloud Dataproc will determine a Cloud Storage location according to the region where your workload is running,
        and then create and manage project-level, per-location staging and temporary buckets.
        This field requires a Cloud Storage bucket name, not a gs://... URI to a Cloud Storage bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#staging_bucket DataprocSessionTemplate#staging_bucket}
        '''
        result = self._values.get("staging_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork_uri(self) -> typing.Optional[builtins.str]:
        '''Subnetwork configuration for workload execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#subnetwork_uri DataprocSessionTemplate#subnetwork_uri}
        '''
        result = self._values.get("subnetwork_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ttl(self) -> typing.Optional[builtins.str]:
        '''The duration after which the workload will be terminated.

        When the workload exceeds this duration, it will be unconditionally terminated without waiting for ongoing
        work to finish. If ttl is not specified for a session workload, the workload will be allowed to run until it
        exits naturally (or run forever without exiting). If ttl is not specified for an interactive session,
        it defaults to 24 hours. If ttl is not specified for a batch that uses 2.1+ runtime version, it defaults to 4 hours.
        Minimum value is 10 minutes; maximum value is 14 days. If both ttl and idleTtl are specified (for an interactive session),
        the conditions are treated as OR conditions: the workload will be terminated when it has been idle for idleTtl or
        when ttl has been exceeded, whichever occurs first.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#ttl DataprocSessionTemplate#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocSessionTemplateEnvironmentConfigExecutionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocSessionTemplateEnvironmentConfigExecutionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocSessionTemplate.DataprocSessionTemplateEnvironmentConfigExecutionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__afec590208a0b437f0923f41c0e6f4e7ba00c9a8d6287fbf91afbfb0e0b12ab0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

    @jsii.member(jsii_name="resetNetworkTags")
    def reset_network_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkTags", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetStagingBucket")
    def reset_staging_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStagingBucket", []))

    @jsii.member(jsii_name="resetSubnetworkUri")
    def reset_subnetwork_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetworkUri", []))

    @jsii.member(jsii_name="resetTtl")
    def reset_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTtl", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="networkTagsInput")
    def network_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "networkTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="stagingBucketInput")
    def staging_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stagingBucketInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkUriInput")
    def subnetwork_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetworkUriInput"))

    @builtins.property
    @jsii.member(jsii_name="ttlInput")
    def ttl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1c4edb08fa2331c3c1433a1bedc5dfd29b0395ab7252c30874305d866d35a8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkTags")
    def network_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkTags"))

    @network_tags.setter
    def network_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__198d6790e8821b334b7082f46c5931f558ba99a1279d6edb831f9b729ea500df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b38fcb809938ea66a4b60955c75fdd35c08fbf61721fbbaa4d8d6913886d75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stagingBucket")
    def staging_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stagingBucket"))

    @staging_bucket.setter
    def staging_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d96ace5e51b9afb614d9c6d56c7e9569993f97e9e07b0e63ae4d72f7c7dfe411)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stagingBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetworkUri")
    def subnetwork_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetworkUri"))

    @subnetwork_uri.setter
    def subnetwork_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d36513bc505093af76ae250877d895d676900920e9dd1ef996c83b4afb6a3f62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetworkUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4337e305a3aad604ed4443624a0b36fde1052dfaeca5da11af4a23c18bad7ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocSessionTemplateEnvironmentConfigExecutionConfig]:
        return typing.cast(typing.Optional[DataprocSessionTemplateEnvironmentConfigExecutionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocSessionTemplateEnvironmentConfigExecutionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cebfd3251f470dbb825753867aca3e55e9d2d8748f791e6b8c190932af9ebd3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocSessionTemplateEnvironmentConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocSessionTemplate.DataprocSessionTemplateEnvironmentConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__182cb64ef267eb7df096c0e357693dd6c04357598dd32041c2880d4f8e3e6d00)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExecutionConfig")
    def put_execution_config(
        self,
        *,
        kms_key: typing.Optional[builtins.str] = None,
        network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_account: typing.Optional[builtins.str] = None,
        staging_bucket: typing.Optional[builtins.str] = None,
        subnetwork_uri: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key: The Cloud KMS key to use for encryption. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#kms_key DataprocSessionTemplate#kms_key}
        :param network_tags: Tags used for network traffic control. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#network_tags DataprocSessionTemplate#network_tags}
        :param service_account: Service account that used to execute workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#service_account DataprocSessionTemplate#service_account}
        :param staging_bucket: A Cloud Storage bucket used to stage workload dependencies, config files, and store workload output and other ephemeral data, such as Spark history files. If you do not specify a staging bucket, Cloud Dataproc will determine a Cloud Storage location according to the region where your workload is running, and then create and manage project-level, per-location staging and temporary buckets. This field requires a Cloud Storage bucket name, not a gs://... URI to a Cloud Storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#staging_bucket DataprocSessionTemplate#staging_bucket}
        :param subnetwork_uri: Subnetwork configuration for workload execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#subnetwork_uri DataprocSessionTemplate#subnetwork_uri}
        :param ttl: The duration after which the workload will be terminated. When the workload exceeds this duration, it will be unconditionally terminated without waiting for ongoing work to finish. If ttl is not specified for a session workload, the workload will be allowed to run until it exits naturally (or run forever without exiting). If ttl is not specified for an interactive session, it defaults to 24 hours. If ttl is not specified for a batch that uses 2.1+ runtime version, it defaults to 4 hours. Minimum value is 10 minutes; maximum value is 14 days. If both ttl and idleTtl are specified (for an interactive session), the conditions are treated as OR conditions: the workload will be terminated when it has been idle for idleTtl or when ttl has been exceeded, whichever occurs first. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#ttl DataprocSessionTemplate#ttl}
        '''
        value = DataprocSessionTemplateEnvironmentConfigExecutionConfig(
            kms_key=kms_key,
            network_tags=network_tags,
            service_account=service_account,
            staging_bucket=staging_bucket,
            subnetwork_uri=subnetwork_uri,
            ttl=ttl,
        )

        return typing.cast(None, jsii.invoke(self, "putExecutionConfig", [value]))

    @jsii.member(jsii_name="putPeripheralsConfig")
    def put_peripherals_config(
        self,
        *,
        metastore_service: typing.Optional[builtins.str] = None,
        spark_history_server_config: typing.Optional[typing.Union["DataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metastore_service: Resource name of an existing Dataproc Metastore service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#metastore_service DataprocSessionTemplate#metastore_service}
        :param spark_history_server_config: spark_history_server_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#spark_history_server_config DataprocSessionTemplate#spark_history_server_config}
        '''
        value = DataprocSessionTemplateEnvironmentConfigPeripheralsConfig(
            metastore_service=metastore_service,
            spark_history_server_config=spark_history_server_config,
        )

        return typing.cast(None, jsii.invoke(self, "putPeripheralsConfig", [value]))

    @jsii.member(jsii_name="resetExecutionConfig")
    def reset_execution_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionConfig", []))

    @jsii.member(jsii_name="resetPeripheralsConfig")
    def reset_peripherals_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeripheralsConfig", []))

    @builtins.property
    @jsii.member(jsii_name="executionConfig")
    def execution_config(
        self,
    ) -> DataprocSessionTemplateEnvironmentConfigExecutionConfigOutputReference:
        return typing.cast(DataprocSessionTemplateEnvironmentConfigExecutionConfigOutputReference, jsii.get(self, "executionConfig"))

    @builtins.property
    @jsii.member(jsii_name="peripheralsConfig")
    def peripherals_config(
        self,
    ) -> "DataprocSessionTemplateEnvironmentConfigPeripheralsConfigOutputReference":
        return typing.cast("DataprocSessionTemplateEnvironmentConfigPeripheralsConfigOutputReference", jsii.get(self, "peripheralsConfig"))

    @builtins.property
    @jsii.member(jsii_name="executionConfigInput")
    def execution_config_input(
        self,
    ) -> typing.Optional[DataprocSessionTemplateEnvironmentConfigExecutionConfig]:
        return typing.cast(typing.Optional[DataprocSessionTemplateEnvironmentConfigExecutionConfig], jsii.get(self, "executionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="peripheralsConfigInput")
    def peripherals_config_input(
        self,
    ) -> typing.Optional["DataprocSessionTemplateEnvironmentConfigPeripheralsConfig"]:
        return typing.cast(typing.Optional["DataprocSessionTemplateEnvironmentConfigPeripheralsConfig"], jsii.get(self, "peripheralsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocSessionTemplateEnvironmentConfig]:
        return typing.cast(typing.Optional[DataprocSessionTemplateEnvironmentConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocSessionTemplateEnvironmentConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8806c683c4bc24616d90a549426b1f8f9054d77f9123c97086e0c77cbd6eb84c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocSessionTemplate.DataprocSessionTemplateEnvironmentConfigPeripheralsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "metastore_service": "metastoreService",
        "spark_history_server_config": "sparkHistoryServerConfig",
    },
)
class DataprocSessionTemplateEnvironmentConfigPeripheralsConfig:
    def __init__(
        self,
        *,
        metastore_service: typing.Optional[builtins.str] = None,
        spark_history_server_config: typing.Optional[typing.Union["DataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metastore_service: Resource name of an existing Dataproc Metastore service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#metastore_service DataprocSessionTemplate#metastore_service}
        :param spark_history_server_config: spark_history_server_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#spark_history_server_config DataprocSessionTemplate#spark_history_server_config}
        '''
        if isinstance(spark_history_server_config, dict):
            spark_history_server_config = DataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig(**spark_history_server_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5785a9ee6542978c17d9caa16228f2a2e8bf0cebc78c7d7ced839a2ed8104647)
            check_type(argname="argument metastore_service", value=metastore_service, expected_type=type_hints["metastore_service"])
            check_type(argname="argument spark_history_server_config", value=spark_history_server_config, expected_type=type_hints["spark_history_server_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metastore_service is not None:
            self._values["metastore_service"] = metastore_service
        if spark_history_server_config is not None:
            self._values["spark_history_server_config"] = spark_history_server_config

    @builtins.property
    def metastore_service(self) -> typing.Optional[builtins.str]:
        '''Resource name of an existing Dataproc Metastore service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#metastore_service DataprocSessionTemplate#metastore_service}
        '''
        result = self._values.get("metastore_service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spark_history_server_config(
        self,
    ) -> typing.Optional["DataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig"]:
        '''spark_history_server_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#spark_history_server_config DataprocSessionTemplate#spark_history_server_config}
        '''
        result = self._values.get("spark_history_server_config")
        return typing.cast(typing.Optional["DataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocSessionTemplateEnvironmentConfigPeripheralsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocSessionTemplateEnvironmentConfigPeripheralsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocSessionTemplate.DataprocSessionTemplateEnvironmentConfigPeripheralsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f95647f931d4b4741d7c119a1f2b61daf02f7949264adad0197c4a73295dd46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSparkHistoryServerConfig")
    def put_spark_history_server_config(
        self,
        *,
        dataproc_cluster: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataproc_cluster: Resource name of an existing Dataproc Cluster to act as a Spark History Server for the workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#dataproc_cluster DataprocSessionTemplate#dataproc_cluster}
        '''
        value = DataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig(
            dataproc_cluster=dataproc_cluster
        )

        return typing.cast(None, jsii.invoke(self, "putSparkHistoryServerConfig", [value]))

    @jsii.member(jsii_name="resetMetastoreService")
    def reset_metastore_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetastoreService", []))

    @jsii.member(jsii_name="resetSparkHistoryServerConfig")
    def reset_spark_history_server_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkHistoryServerConfig", []))

    @builtins.property
    @jsii.member(jsii_name="sparkHistoryServerConfig")
    def spark_history_server_config(
        self,
    ) -> "DataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfigOutputReference":
        return typing.cast("DataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfigOutputReference", jsii.get(self, "sparkHistoryServerConfig"))

    @builtins.property
    @jsii.member(jsii_name="metastoreServiceInput")
    def metastore_service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metastoreServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkHistoryServerConfigInput")
    def spark_history_server_config_input(
        self,
    ) -> typing.Optional["DataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig"]:
        return typing.cast(typing.Optional["DataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig"], jsii.get(self, "sparkHistoryServerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="metastoreService")
    def metastore_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metastoreService"))

    @metastore_service.setter
    def metastore_service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eadce457f032a188fdff6daac133d1c525e813cd471cb5f12a7ef1ee7d316076)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metastoreService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocSessionTemplateEnvironmentConfigPeripheralsConfig]:
        return typing.cast(typing.Optional[DataprocSessionTemplateEnvironmentConfigPeripheralsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocSessionTemplateEnvironmentConfigPeripheralsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6378d49eae14e69858f81a93c998f25a54996f243fbf970bca9d39100245857b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocSessionTemplate.DataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig",
    jsii_struct_bases=[],
    name_mapping={"dataproc_cluster": "dataprocCluster"},
)
class DataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig:
    def __init__(
        self,
        *,
        dataproc_cluster: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataproc_cluster: Resource name of an existing Dataproc Cluster to act as a Spark History Server for the workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#dataproc_cluster DataprocSessionTemplate#dataproc_cluster}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2845ff97a1d1957c68b4999e9306bc49b2b64edc1f1bcf23d0dc7ac6fdba1e0)
            check_type(argname="argument dataproc_cluster", value=dataproc_cluster, expected_type=type_hints["dataproc_cluster"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dataproc_cluster is not None:
            self._values["dataproc_cluster"] = dataproc_cluster

    @builtins.property
    def dataproc_cluster(self) -> typing.Optional[builtins.str]:
        '''Resource name of an existing Dataproc Cluster to act as a Spark History Server for the workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#dataproc_cluster DataprocSessionTemplate#dataproc_cluster}
        '''
        result = self._values.get("dataproc_cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocSessionTemplate.DataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__047db62a8e7970ecd8bf4ff574b656000a970ac602632c8a2e7323bca3a90cf0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDataprocCluster")
    def reset_dataproc_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataprocCluster", []))

    @builtins.property
    @jsii.member(jsii_name="dataprocClusterInput")
    def dataproc_cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataprocClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="dataprocCluster")
    def dataproc_cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataprocCluster"))

    @dataproc_cluster.setter
    def dataproc_cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c131230cd5eb7b70b23142185113ae52cb4efb5ede0851d604b6b9869f586ae5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataprocCluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig]:
        return typing.cast(typing.Optional[DataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c572a17f31661d33f72045a041acf061694ad89b46eca58a837bb215eff5d12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocSessionTemplate.DataprocSessionTemplateJupyterSession",
    jsii_struct_bases=[],
    name_mapping={"display_name": "displayName", "kernel": "kernel"},
)
class DataprocSessionTemplateJupyterSession:
    def __init__(
        self,
        *,
        display_name: typing.Optional[builtins.str] = None,
        kernel: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param display_name: Display name, shown in the Jupyter kernelspec card. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#display_name DataprocSessionTemplate#display_name}
        :param kernel: Kernel to be used with Jupyter interactive session. Possible values: ["PYTHON", "SCALA"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#kernel DataprocSessionTemplate#kernel}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d76be43440e657e2cf9f9d16e870713160b4a483527409f795fddb3ab2ecb7)
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument kernel", value=kernel, expected_type=type_hints["kernel"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if display_name is not None:
            self._values["display_name"] = display_name
        if kernel is not None:
            self._values["kernel"] = kernel

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Display name, shown in the Jupyter kernelspec card.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#display_name DataprocSessionTemplate#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kernel(self) -> typing.Optional[builtins.str]:
        '''Kernel to be used with Jupyter interactive session. Possible values: ["PYTHON", "SCALA"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#kernel DataprocSessionTemplate#kernel}
        '''
        result = self._values.get("kernel")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocSessionTemplateJupyterSession(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocSessionTemplateJupyterSessionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocSessionTemplate.DataprocSessionTemplateJupyterSessionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__337e632f18592b329e7d6ad69a0758d1bba728a742b187df3eed812cac47bf33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetKernel")
    def reset_kernel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKernel", []))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="kernelInput")
    def kernel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kernelInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a24b5ccd3dae7408328788116014e49b4dd2a2057f7c1cfb5f92176d617c75e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kernel")
    def kernel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kernel"))

    @kernel.setter
    def kernel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3ed0b53f7bf659def0ad4d025cb823d81ad8d617d586fb8212a0cc5da8c1b8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kernel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocSessionTemplateJupyterSession]:
        return typing.cast(typing.Optional[DataprocSessionTemplateJupyterSession], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocSessionTemplateJupyterSession],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__713535eceeb6a2de0f9862690295cc69767f502693fc6894d9b5bc12cd63e19a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocSessionTemplate.DataprocSessionTemplateRuntimeConfig",
    jsii_struct_bases=[],
    name_mapping={
        "container_image": "containerImage",
        "properties": "properties",
        "version": "version",
    },
)
class DataprocSessionTemplateRuntimeConfig:
    def __init__(
        self,
        *,
        container_image: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_image: Optional custom container image for the job runtime environment. If not specified, a default container image will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#container_image DataprocSessionTemplate#container_image}
        :param properties: A mapping of property names to values, which are used to configure workload execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#properties DataprocSessionTemplate#properties}
        :param version: Version of the session runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#version DataprocSessionTemplate#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40a83ee8a98a2133ade12574aa3746b9538a6617a8f98b9254506a521f7b87c6)
            check_type(argname="argument container_image", value=container_image, expected_type=type_hints["container_image"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_image is not None:
            self._values["container_image"] = container_image
        if properties is not None:
            self._values["properties"] = properties
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def container_image(self) -> typing.Optional[builtins.str]:
        '''Optional custom container image for the job runtime environment. If not specified, a default container image will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#container_image DataprocSessionTemplate#container_image}
        '''
        result = self._values.get("container_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping of property names to values, which are used to configure workload execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#properties DataprocSessionTemplate#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of the session runtime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#version DataprocSessionTemplate#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocSessionTemplateRuntimeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocSessionTemplateRuntimeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocSessionTemplate.DataprocSessionTemplateRuntimeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13cce4601d41a1b2282e074fecbcafaf5363f8e65e4970c441c5ec9230b3b10e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContainerImage")
    def reset_container_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerImage", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="effectiveProperties")
    def effective_properties(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveProperties"))

    @builtins.property
    @jsii.member(jsii_name="containerImageInput")
    def container_image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerImageInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="containerImage")
    def container_image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerImage"))

    @container_image.setter
    def container_image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09d8a052d7f24575ed8608a22fbbab8075580fd07cb71b3621c4404bfcb5ac9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerImage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e68502ed66657de88069a50e29dd18c9a24217eecf313b330b070706829d25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8ffc107422acc5c046058b2f5c72bc4a4153e7c5811bd3106ff74a0435f0c6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocSessionTemplateRuntimeConfig]:
        return typing.cast(typing.Optional[DataprocSessionTemplateRuntimeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocSessionTemplateRuntimeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ee76c39e6e6abd09f11cc47ecb7e59f626d1dced1cf9c5bd90d02af92ca65e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocSessionTemplate.DataprocSessionTemplateSparkConnectSession",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataprocSessionTemplateSparkConnectSession:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocSessionTemplateSparkConnectSession(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocSessionTemplateSparkConnectSessionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocSessionTemplate.DataprocSessionTemplateSparkConnectSessionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b416f47ab96a01bc013b622e0ea86ae98d7361e34d32c6585f37277b88c97b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocSessionTemplateSparkConnectSession]:
        return typing.cast(typing.Optional[DataprocSessionTemplateSparkConnectSession], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocSessionTemplateSparkConnectSession],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2972999dfd8254b73485373ea7b9e889413add3158ccf3d6e10dbc5066b2710c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocSessionTemplate.DataprocSessionTemplateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DataprocSessionTemplateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#create DataprocSessionTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#delete DataprocSessionTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#update DataprocSessionTemplate#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f971ac06bdd6c17aefe2fe612fd6b35a5594d1486c1b668127c0b70a1548556b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#create DataprocSessionTemplate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#delete DataprocSessionTemplate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_session_template#update DataprocSessionTemplate#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocSessionTemplateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocSessionTemplateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocSessionTemplate.DataprocSessionTemplateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__120933c851c444e58bf0d716182c2ee522265b909cf5c2382844c6cf48ca3114)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f30294f8c16ad0d2b60a4b220d87176cc5e90803497e7ecf2ab636a21cdd4699)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ac942baae4fad716f763b20b81f8e5c27c13b43757383d218f738f40bf26c7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a429f256c3502004625205ca9a9c4ecb4a55301d1ccd6a1e897c84dc4a6bafb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocSessionTemplateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocSessionTemplateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocSessionTemplateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f44335c9b7c8f8ecabd93bc814742a18446e43b851e956b2f71a949e2580f2d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataprocSessionTemplate",
    "DataprocSessionTemplateConfig",
    "DataprocSessionTemplateEnvironmentConfig",
    "DataprocSessionTemplateEnvironmentConfigExecutionConfig",
    "DataprocSessionTemplateEnvironmentConfigExecutionConfigOutputReference",
    "DataprocSessionTemplateEnvironmentConfigOutputReference",
    "DataprocSessionTemplateEnvironmentConfigPeripheralsConfig",
    "DataprocSessionTemplateEnvironmentConfigPeripheralsConfigOutputReference",
    "DataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig",
    "DataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfigOutputReference",
    "DataprocSessionTemplateJupyterSession",
    "DataprocSessionTemplateJupyterSessionOutputReference",
    "DataprocSessionTemplateRuntimeConfig",
    "DataprocSessionTemplateRuntimeConfigOutputReference",
    "DataprocSessionTemplateSparkConnectSession",
    "DataprocSessionTemplateSparkConnectSessionOutputReference",
    "DataprocSessionTemplateTimeouts",
    "DataprocSessionTemplateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b5fa9c162e4246d9889bd6140b594bd2b34dea970e85978ad66872a0fdd1c3da(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    environment_config: typing.Optional[typing.Union[DataprocSessionTemplateEnvironmentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    jupyter_session: typing.Optional[typing.Union[DataprocSessionTemplateJupyterSession, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    runtime_config: typing.Optional[typing.Union[DataprocSessionTemplateRuntimeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_connect_session: typing.Optional[typing.Union[DataprocSessionTemplateSparkConnectSession, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DataprocSessionTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b6b6a35475222428f5c9977c8e43e7381d2db58cf46c9da70ee187b10be62d47(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b32e06810b7d2cc59c3bcfbefd08f23a1f6e282c90725bf05b596dd8a9bf4ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c81de4996ce69269aa51fe51f03bd60549b0b655b72d1ebb21536304f5d4c9f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9678c928012a3ae16d53224f97cb3b4e07d129e0a1dd1f9ec81f4dd4a55f70d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b88be3e63786cd5f1bdaebf82b995becdb48984c63fa1f05e10659e83aa68c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba363bc0286f593e3208626a9d6de602ac28b29575da584b75f3bd5bab1376b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e600ae3c7151dca60aadc5268d17461b01ab369cfd89f0d14e684b69403c296(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    environment_config: typing.Optional[typing.Union[DataprocSessionTemplateEnvironmentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    jupyter_session: typing.Optional[typing.Union[DataprocSessionTemplateJupyterSession, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    runtime_config: typing.Optional[typing.Union[DataprocSessionTemplateRuntimeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_connect_session: typing.Optional[typing.Union[DataprocSessionTemplateSparkConnectSession, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DataprocSessionTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__206799d30edea13161dff4be404d24bcf47adc35d2d08bb523c6c3423a100cfd(
    *,
    execution_config: typing.Optional[typing.Union[DataprocSessionTemplateEnvironmentConfigExecutionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    peripherals_config: typing.Optional[typing.Union[DataprocSessionTemplateEnvironmentConfigPeripheralsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5166259c1ac803767adfbe107cce46ea849eb511864d75c3c88774f7a03056ec(
    *,
    kms_key: typing.Optional[builtins.str] = None,
    network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    service_account: typing.Optional[builtins.str] = None,
    staging_bucket: typing.Optional[builtins.str] = None,
    subnetwork_uri: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afec590208a0b437f0923f41c0e6f4e7ba00c9a8d6287fbf91afbfb0e0b12ab0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1c4edb08fa2331c3c1433a1bedc5dfd29b0395ab7252c30874305d866d35a8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198d6790e8821b334b7082f46c5931f558ba99a1279d6edb831f9b729ea500df(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b38fcb809938ea66a4b60955c75fdd35c08fbf61721fbbaa4d8d6913886d75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d96ace5e51b9afb614d9c6d56c7e9569993f97e9e07b0e63ae4d72f7c7dfe411(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d36513bc505093af76ae250877d895d676900920e9dd1ef996c83b4afb6a3f62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4337e305a3aad604ed4443624a0b36fde1052dfaeca5da11af4a23c18bad7ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cebfd3251f470dbb825753867aca3e55e9d2d8748f791e6b8c190932af9ebd3b(
    value: typing.Optional[DataprocSessionTemplateEnvironmentConfigExecutionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__182cb64ef267eb7df096c0e357693dd6c04357598dd32041c2880d4f8e3e6d00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8806c683c4bc24616d90a549426b1f8f9054d77f9123c97086e0c77cbd6eb84c(
    value: typing.Optional[DataprocSessionTemplateEnvironmentConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5785a9ee6542978c17d9caa16228f2a2e8bf0cebc78c7d7ced839a2ed8104647(
    *,
    metastore_service: typing.Optional[builtins.str] = None,
    spark_history_server_config: typing.Optional[typing.Union[DataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f95647f931d4b4741d7c119a1f2b61daf02f7949264adad0197c4a73295dd46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eadce457f032a188fdff6daac133d1c525e813cd471cb5f12a7ef1ee7d316076(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6378d49eae14e69858f81a93c998f25a54996f243fbf970bca9d39100245857b(
    value: typing.Optional[DataprocSessionTemplateEnvironmentConfigPeripheralsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2845ff97a1d1957c68b4999e9306bc49b2b64edc1f1bcf23d0dc7ac6fdba1e0(
    *,
    dataproc_cluster: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047db62a8e7970ecd8bf4ff574b656000a970ac602632c8a2e7323bca3a90cf0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c131230cd5eb7b70b23142185113ae52cb4efb5ede0851d604b6b9869f586ae5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c572a17f31661d33f72045a041acf061694ad89b46eca58a837bb215eff5d12(
    value: typing.Optional[DataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d76be43440e657e2cf9f9d16e870713160b4a483527409f795fddb3ab2ecb7(
    *,
    display_name: typing.Optional[builtins.str] = None,
    kernel: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__337e632f18592b329e7d6ad69a0758d1bba728a742b187df3eed812cac47bf33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a24b5ccd3dae7408328788116014e49b4dd2a2057f7c1cfb5f92176d617c75e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3ed0b53f7bf659def0ad4d025cb823d81ad8d617d586fb8212a0cc5da8c1b8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__713535eceeb6a2de0f9862690295cc69767f502693fc6894d9b5bc12cd63e19a(
    value: typing.Optional[DataprocSessionTemplateJupyterSession],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a83ee8a98a2133ade12574aa3746b9538a6617a8f98b9254506a521f7b87c6(
    *,
    container_image: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13cce4601d41a1b2282e074fecbcafaf5363f8e65e4970c441c5ec9230b3b10e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d8a052d7f24575ed8608a22fbbab8075580fd07cb71b3621c4404bfcb5ac9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e68502ed66657de88069a50e29dd18c9a24217eecf313b330b070706829d25(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ffc107422acc5c046058b2f5c72bc4a4153e7c5811bd3106ff74a0435f0c6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ee76c39e6e6abd09f11cc47ecb7e59f626d1dced1cf9c5bd90d02af92ca65e2(
    value: typing.Optional[DataprocSessionTemplateRuntimeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b416f47ab96a01bc013b622e0ea86ae98d7361e34d32c6585f37277b88c97b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2972999dfd8254b73485373ea7b9e889413add3158ccf3d6e10dbc5066b2710c(
    value: typing.Optional[DataprocSessionTemplateSparkConnectSession],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f971ac06bdd6c17aefe2fe612fd6b35a5594d1486c1b668127c0b70a1548556b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__120933c851c444e58bf0d716182c2ee522265b909cf5c2382844c6cf48ca3114(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f30294f8c16ad0d2b60a4b220d87176cc5e90803497e7ecf2ab636a21cdd4699(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac942baae4fad716f763b20b81f8e5c27c13b43757383d218f738f40bf26c7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a429f256c3502004625205ca9a9c4ecb4a55301d1ccd6a1e897c84dc4a6bafb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f44335c9b7c8f8ecabd93bc814742a18446e43b851e956b2f71a949e2580f2d0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocSessionTemplateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
