r'''
# `google_dataproc_session_template`

Refer to the Terraform Registry for docs: [`google_dataproc_session_template`](https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template).
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


class GoogleDataprocSessionTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocSessionTemplate.GoogleDataprocSessionTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template google_dataproc_session_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        environment_config: typing.Optional[typing.Union["GoogleDataprocSessionTemplateEnvironmentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        jupyter_session: typing.Optional[typing.Union["GoogleDataprocSessionTemplateJupyterSession", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        runtime_config: typing.Optional[typing.Union["GoogleDataprocSessionTemplateRuntimeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_connect_session: typing.Optional[typing.Union["GoogleDataprocSessionTemplateSparkConnectSession", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataprocSessionTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template google_dataproc_session_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The resource name of the session template in the following format: projects/{project}/locations/{location}/sessionTemplates/{template_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#name GoogleDataprocSessionTemplate#name}
        :param environment_config: environment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#environment_config GoogleDataprocSessionTemplate#environment_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#id GoogleDataprocSessionTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jupyter_session: jupyter_session block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#jupyter_session GoogleDataprocSessionTemplate#jupyter_session}
        :param labels: The labels to associate with this session template. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#labels GoogleDataprocSessionTemplate#labels}
        :param location: The location in which the session template will be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#location GoogleDataprocSessionTemplate#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#project GoogleDataprocSessionTemplate#project}.
        :param runtime_config: runtime_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#runtime_config GoogleDataprocSessionTemplate#runtime_config}
        :param spark_connect_session: spark_connect_session block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#spark_connect_session GoogleDataprocSessionTemplate#spark_connect_session}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#timeouts GoogleDataprocSessionTemplate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d1d71de0e05f8307207f58113db40d72b5f3bccbc825c02b21f196053ff3dee)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDataprocSessionTemplateConfig(
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
        '''Generates CDKTF code for importing a GoogleDataprocSessionTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDataprocSessionTemplate to import.
        :param import_from_id: The id of the existing GoogleDataprocSessionTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDataprocSessionTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fcb8b882f8dcfc4cb86751337dd496ca503155c660d061f6adf1de779c41c1a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEnvironmentConfig")
    def put_environment_config(
        self,
        *,
        execution_config: typing.Optional[typing.Union["GoogleDataprocSessionTemplateEnvironmentConfigExecutionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        peripherals_config: typing.Optional[typing.Union["GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param execution_config: execution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#execution_config GoogleDataprocSessionTemplate#execution_config}
        :param peripherals_config: peripherals_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#peripherals_config GoogleDataprocSessionTemplate#peripherals_config}
        '''
        value = GoogleDataprocSessionTemplateEnvironmentConfig(
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
        :param display_name: Display name, shown in the Jupyter kernelspec card. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#display_name GoogleDataprocSessionTemplate#display_name}
        :param kernel: Kernel to be used with Jupyter interactive session. Possible values: ["PYTHON", "SCALA"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#kernel GoogleDataprocSessionTemplate#kernel}
        '''
        value = GoogleDataprocSessionTemplateJupyterSession(
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
        :param container_image: Optional custom container image for the job runtime environment. If not specified, a default container image will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#container_image GoogleDataprocSessionTemplate#container_image}
        :param properties: A mapping of property names to values, which are used to configure workload execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#properties GoogleDataprocSessionTemplate#properties}
        :param version: Version of the session runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#version GoogleDataprocSessionTemplate#version}
        '''
        value = GoogleDataprocSessionTemplateRuntimeConfig(
            container_image=container_image, properties=properties, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putRuntimeConfig", [value]))

    @jsii.member(jsii_name="putSparkConnectSession")
    def put_spark_connect_session(self) -> None:
        value = GoogleDataprocSessionTemplateSparkConnectSession()

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#create GoogleDataprocSessionTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#delete GoogleDataprocSessionTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#update GoogleDataprocSessionTemplate#update}.
        '''
        value = GoogleDataprocSessionTemplateTimeouts(
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
    ) -> "GoogleDataprocSessionTemplateEnvironmentConfigOutputReference":
        return typing.cast("GoogleDataprocSessionTemplateEnvironmentConfigOutputReference", jsii.get(self, "environmentConfig"))

    @builtins.property
    @jsii.member(jsii_name="jupyterSession")
    def jupyter_session(
        self,
    ) -> "GoogleDataprocSessionTemplateJupyterSessionOutputReference":
        return typing.cast("GoogleDataprocSessionTemplateJupyterSessionOutputReference", jsii.get(self, "jupyterSession"))

    @builtins.property
    @jsii.member(jsii_name="runtimeConfig")
    def runtime_config(
        self,
    ) -> "GoogleDataprocSessionTemplateRuntimeConfigOutputReference":
        return typing.cast("GoogleDataprocSessionTemplateRuntimeConfigOutputReference", jsii.get(self, "runtimeConfig"))

    @builtins.property
    @jsii.member(jsii_name="sparkConnectSession")
    def spark_connect_session(
        self,
    ) -> "GoogleDataprocSessionTemplateSparkConnectSessionOutputReference":
        return typing.cast("GoogleDataprocSessionTemplateSparkConnectSessionOutputReference", jsii.get(self, "sparkConnectSession"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleDataprocSessionTemplateTimeoutsOutputReference":
        return typing.cast("GoogleDataprocSessionTemplateTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["GoogleDataprocSessionTemplateEnvironmentConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocSessionTemplateEnvironmentConfig"], jsii.get(self, "environmentConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="jupyterSessionInput")
    def jupyter_session_input(
        self,
    ) -> typing.Optional["GoogleDataprocSessionTemplateJupyterSession"]:
        return typing.cast(typing.Optional["GoogleDataprocSessionTemplateJupyterSession"], jsii.get(self, "jupyterSessionInput"))

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
    ) -> typing.Optional["GoogleDataprocSessionTemplateRuntimeConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocSessionTemplateRuntimeConfig"], jsii.get(self, "runtimeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkConnectSessionInput")
    def spark_connect_session_input(
        self,
    ) -> typing.Optional["GoogleDataprocSessionTemplateSparkConnectSession"]:
        return typing.cast(typing.Optional["GoogleDataprocSessionTemplateSparkConnectSession"], jsii.get(self, "sparkConnectSessionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataprocSessionTemplateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataprocSessionTemplateTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85ac8b6191a9b0c26a93593c276e730375b1ce891fd7fbb6c438d7e35cafc297)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69b3f6caceb2cda8d6ffde4a4d301e05abf04803858534ad91dbcbdf877bf550)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b01ae4c83ea37e061369c4e09bab45592cd01c417a39424707c17a8a5c2069b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bd9dcff0f8798e9e312d9ddcb1aa0da1b053415b8a10736b6abb0e9084c8397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__505265141f9faf36c9101ae5f4004407881d82ace84535921d278622b0d186d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocSessionTemplate.GoogleDataprocSessionTemplateConfig",
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
class GoogleDataprocSessionTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        environment_config: typing.Optional[typing.Union["GoogleDataprocSessionTemplateEnvironmentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        jupyter_session: typing.Optional[typing.Union["GoogleDataprocSessionTemplateJupyterSession", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        runtime_config: typing.Optional[typing.Union["GoogleDataprocSessionTemplateRuntimeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_connect_session: typing.Optional[typing.Union["GoogleDataprocSessionTemplateSparkConnectSession", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataprocSessionTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The resource name of the session template in the following format: projects/{project}/locations/{location}/sessionTemplates/{template_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#name GoogleDataprocSessionTemplate#name}
        :param environment_config: environment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#environment_config GoogleDataprocSessionTemplate#environment_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#id GoogleDataprocSessionTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jupyter_session: jupyter_session block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#jupyter_session GoogleDataprocSessionTemplate#jupyter_session}
        :param labels: The labels to associate with this session template. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#labels GoogleDataprocSessionTemplate#labels}
        :param location: The location in which the session template will be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#location GoogleDataprocSessionTemplate#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#project GoogleDataprocSessionTemplate#project}.
        :param runtime_config: runtime_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#runtime_config GoogleDataprocSessionTemplate#runtime_config}
        :param spark_connect_session: spark_connect_session block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#spark_connect_session GoogleDataprocSessionTemplate#spark_connect_session}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#timeouts GoogleDataprocSessionTemplate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(environment_config, dict):
            environment_config = GoogleDataprocSessionTemplateEnvironmentConfig(**environment_config)
        if isinstance(jupyter_session, dict):
            jupyter_session = GoogleDataprocSessionTemplateJupyterSession(**jupyter_session)
        if isinstance(runtime_config, dict):
            runtime_config = GoogleDataprocSessionTemplateRuntimeConfig(**runtime_config)
        if isinstance(spark_connect_session, dict):
            spark_connect_session = GoogleDataprocSessionTemplateSparkConnectSession(**spark_connect_session)
        if isinstance(timeouts, dict):
            timeouts = GoogleDataprocSessionTemplateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0aeea7cd6f6467ab4bf6e3f88aa3e71628749b55ecbc15c769bd36a340bccbf)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#name GoogleDataprocSessionTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def environment_config(
        self,
    ) -> typing.Optional["GoogleDataprocSessionTemplateEnvironmentConfig"]:
        '''environment_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#environment_config GoogleDataprocSessionTemplate#environment_config}
        '''
        result = self._values.get("environment_config")
        return typing.cast(typing.Optional["GoogleDataprocSessionTemplateEnvironmentConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#id GoogleDataprocSessionTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jupyter_session(
        self,
    ) -> typing.Optional["GoogleDataprocSessionTemplateJupyterSession"]:
        '''jupyter_session block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#jupyter_session GoogleDataprocSessionTemplate#jupyter_session}
        '''
        result = self._values.get("jupyter_session")
        return typing.cast(typing.Optional["GoogleDataprocSessionTemplateJupyterSession"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The labels to associate with this session template.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#labels GoogleDataprocSessionTemplate#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location in which the session template will be created in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#location GoogleDataprocSessionTemplate#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#project GoogleDataprocSessionTemplate#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_config(
        self,
    ) -> typing.Optional["GoogleDataprocSessionTemplateRuntimeConfig"]:
        '''runtime_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#runtime_config GoogleDataprocSessionTemplate#runtime_config}
        '''
        result = self._values.get("runtime_config")
        return typing.cast(typing.Optional["GoogleDataprocSessionTemplateRuntimeConfig"], result)

    @builtins.property
    def spark_connect_session(
        self,
    ) -> typing.Optional["GoogleDataprocSessionTemplateSparkConnectSession"]:
        '''spark_connect_session block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#spark_connect_session GoogleDataprocSessionTemplate#spark_connect_session}
        '''
        result = self._values.get("spark_connect_session")
        return typing.cast(typing.Optional["GoogleDataprocSessionTemplateSparkConnectSession"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDataprocSessionTemplateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#timeouts GoogleDataprocSessionTemplate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDataprocSessionTemplateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocSessionTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocSessionTemplate.GoogleDataprocSessionTemplateEnvironmentConfig",
    jsii_struct_bases=[],
    name_mapping={
        "execution_config": "executionConfig",
        "peripherals_config": "peripheralsConfig",
    },
)
class GoogleDataprocSessionTemplateEnvironmentConfig:
    def __init__(
        self,
        *,
        execution_config: typing.Optional[typing.Union["GoogleDataprocSessionTemplateEnvironmentConfigExecutionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        peripherals_config: typing.Optional[typing.Union["GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param execution_config: execution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#execution_config GoogleDataprocSessionTemplate#execution_config}
        :param peripherals_config: peripherals_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#peripherals_config GoogleDataprocSessionTemplate#peripherals_config}
        '''
        if isinstance(execution_config, dict):
            execution_config = GoogleDataprocSessionTemplateEnvironmentConfigExecutionConfig(**execution_config)
        if isinstance(peripherals_config, dict):
            peripherals_config = GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfig(**peripherals_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85b535d4a70bef6798398282ebf8bc52d0eb3d102ab1524a31177534f1218590)
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
    ) -> typing.Optional["GoogleDataprocSessionTemplateEnvironmentConfigExecutionConfig"]:
        '''execution_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#execution_config GoogleDataprocSessionTemplate#execution_config}
        '''
        result = self._values.get("execution_config")
        return typing.cast(typing.Optional["GoogleDataprocSessionTemplateEnvironmentConfigExecutionConfig"], result)

    @builtins.property
    def peripherals_config(
        self,
    ) -> typing.Optional["GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfig"]:
        '''peripherals_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#peripherals_config GoogleDataprocSessionTemplate#peripherals_config}
        '''
        result = self._values.get("peripherals_config")
        return typing.cast(typing.Optional["GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocSessionTemplateEnvironmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocSessionTemplate.GoogleDataprocSessionTemplateEnvironmentConfigExecutionConfig",
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
class GoogleDataprocSessionTemplateEnvironmentConfigExecutionConfig:
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
        :param kms_key: The Cloud KMS key to use for encryption. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#kms_key GoogleDataprocSessionTemplate#kms_key}
        :param network_tags: Tags used for network traffic control. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#network_tags GoogleDataprocSessionTemplate#network_tags}
        :param service_account: Service account that used to execute workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#service_account GoogleDataprocSessionTemplate#service_account}
        :param staging_bucket: A Cloud Storage bucket used to stage workload dependencies, config files, and store workload output and other ephemeral data, such as Spark history files. If you do not specify a staging bucket, Cloud Dataproc will determine a Cloud Storage location according to the region where your workload is running, and then create and manage project-level, per-location staging and temporary buckets. This field requires a Cloud Storage bucket name, not a gs://... URI to a Cloud Storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#staging_bucket GoogleDataprocSessionTemplate#staging_bucket}
        :param subnetwork_uri: Subnetwork configuration for workload execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#subnetwork_uri GoogleDataprocSessionTemplate#subnetwork_uri}
        :param ttl: The duration after which the workload will be terminated. When the workload exceeds this duration, it will be unconditionally terminated without waiting for ongoing work to finish. If ttl is not specified for a session workload, the workload will be allowed to run until it exits naturally (or run forever without exiting). If ttl is not specified for an interactive session, it defaults to 24 hours. If ttl is not specified for a batch that uses 2.1+ runtime version, it defaults to 4 hours. Minimum value is 10 minutes; maximum value is 14 days. If both ttl and idleTtl are specified (for an interactive session), the conditions are treated as OR conditions: the workload will be terminated when it has been idle for idleTtl or when ttl has been exceeded, whichever occurs first. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#ttl GoogleDataprocSessionTemplate#ttl}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__138f4a7012855226cbd8b7796bdbe991a6ef21f758c551936d4f2dfb12ec3680)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#kms_key GoogleDataprocSessionTemplate#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags used for network traffic control.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#network_tags GoogleDataprocSessionTemplate#network_tags}
        '''
        result = self._values.get("network_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''Service account that used to execute workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#service_account GoogleDataprocSessionTemplate#service_account}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#staging_bucket GoogleDataprocSessionTemplate#staging_bucket}
        '''
        result = self._values.get("staging_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork_uri(self) -> typing.Optional[builtins.str]:
        '''Subnetwork configuration for workload execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#subnetwork_uri GoogleDataprocSessionTemplate#subnetwork_uri}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#ttl GoogleDataprocSessionTemplate#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocSessionTemplateEnvironmentConfigExecutionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocSessionTemplateEnvironmentConfigExecutionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocSessionTemplate.GoogleDataprocSessionTemplateEnvironmentConfigExecutionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b37b3fe327395f836abd22e2dc6b63a9e2ea160aa4c1952bd63090e5d09c9402)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b85b7a945c0e315c581ef0760ea16848cf527e3cffefc52dfd27351e9a672158)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkTags")
    def network_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkTags"))

    @network_tags.setter
    def network_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f93f54b2a439425b6c4c2278de288004a41dff4b7f13c47f265f0e029cb052a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddf18c7aec90cfd8025a188faf67072453119681ca4e22893227268717477454)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stagingBucket")
    def staging_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stagingBucket"))

    @staging_bucket.setter
    def staging_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75392aa1ad33a2e96ed8b06214bb72e9e834249c36b0199d5927dee3ed0070f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stagingBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetworkUri")
    def subnetwork_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetworkUri"))

    @subnetwork_uri.setter
    def subnetwork_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a769fb3211906fe70c294ace5c90f97250d0f735073ba2593017321fd27ee8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetworkUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd623ab935baa59d2f7718ceaeb2ee78e8819d4e662d4d48b1f5d0428889050d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocSessionTemplateEnvironmentConfigExecutionConfig]:
        return typing.cast(typing.Optional[GoogleDataprocSessionTemplateEnvironmentConfigExecutionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocSessionTemplateEnvironmentConfigExecutionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48dbcd51a2c149a99deaa8b546cbc716f37bc897ae931ea5a10251ac8fb8eec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocSessionTemplateEnvironmentConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocSessionTemplate.GoogleDataprocSessionTemplateEnvironmentConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de3881c92700760708734dbdedd48677fa24609e78ec446756c5f6f3f887ecb2)
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
        :param kms_key: The Cloud KMS key to use for encryption. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#kms_key GoogleDataprocSessionTemplate#kms_key}
        :param network_tags: Tags used for network traffic control. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#network_tags GoogleDataprocSessionTemplate#network_tags}
        :param service_account: Service account that used to execute workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#service_account GoogleDataprocSessionTemplate#service_account}
        :param staging_bucket: A Cloud Storage bucket used to stage workload dependencies, config files, and store workload output and other ephemeral data, such as Spark history files. If you do not specify a staging bucket, Cloud Dataproc will determine a Cloud Storage location according to the region where your workload is running, and then create and manage project-level, per-location staging and temporary buckets. This field requires a Cloud Storage bucket name, not a gs://... URI to a Cloud Storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#staging_bucket GoogleDataprocSessionTemplate#staging_bucket}
        :param subnetwork_uri: Subnetwork configuration for workload execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#subnetwork_uri GoogleDataprocSessionTemplate#subnetwork_uri}
        :param ttl: The duration after which the workload will be terminated. When the workload exceeds this duration, it will be unconditionally terminated without waiting for ongoing work to finish. If ttl is not specified for a session workload, the workload will be allowed to run until it exits naturally (or run forever without exiting). If ttl is not specified for an interactive session, it defaults to 24 hours. If ttl is not specified for a batch that uses 2.1+ runtime version, it defaults to 4 hours. Minimum value is 10 minutes; maximum value is 14 days. If both ttl and idleTtl are specified (for an interactive session), the conditions are treated as OR conditions: the workload will be terminated when it has been idle for idleTtl or when ttl has been exceeded, whichever occurs first. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#ttl GoogleDataprocSessionTemplate#ttl}
        '''
        value = GoogleDataprocSessionTemplateEnvironmentConfigExecutionConfig(
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
        spark_history_server_config: typing.Optional[typing.Union["GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metastore_service: Resource name of an existing Dataproc Metastore service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#metastore_service GoogleDataprocSessionTemplate#metastore_service}
        :param spark_history_server_config: spark_history_server_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#spark_history_server_config GoogleDataprocSessionTemplate#spark_history_server_config}
        '''
        value = GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfig(
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
    ) -> GoogleDataprocSessionTemplateEnvironmentConfigExecutionConfigOutputReference:
        return typing.cast(GoogleDataprocSessionTemplateEnvironmentConfigExecutionConfigOutputReference, jsii.get(self, "executionConfig"))

    @builtins.property
    @jsii.member(jsii_name="peripheralsConfig")
    def peripherals_config(
        self,
    ) -> "GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigOutputReference":
        return typing.cast("GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigOutputReference", jsii.get(self, "peripheralsConfig"))

    @builtins.property
    @jsii.member(jsii_name="executionConfigInput")
    def execution_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocSessionTemplateEnvironmentConfigExecutionConfig]:
        return typing.cast(typing.Optional[GoogleDataprocSessionTemplateEnvironmentConfigExecutionConfig], jsii.get(self, "executionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="peripheralsConfigInput")
    def peripherals_config_input(
        self,
    ) -> typing.Optional["GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfig"], jsii.get(self, "peripheralsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocSessionTemplateEnvironmentConfig]:
        return typing.cast(typing.Optional[GoogleDataprocSessionTemplateEnvironmentConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocSessionTemplateEnvironmentConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4b8bd0756da282b6087332e37a9459768bfd18fca0f14d40be1509782ac30ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocSessionTemplate.GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "metastore_service": "metastoreService",
        "spark_history_server_config": "sparkHistoryServerConfig",
    },
)
class GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfig:
    def __init__(
        self,
        *,
        metastore_service: typing.Optional[builtins.str] = None,
        spark_history_server_config: typing.Optional[typing.Union["GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metastore_service: Resource name of an existing Dataproc Metastore service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#metastore_service GoogleDataprocSessionTemplate#metastore_service}
        :param spark_history_server_config: spark_history_server_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#spark_history_server_config GoogleDataprocSessionTemplate#spark_history_server_config}
        '''
        if isinstance(spark_history_server_config, dict):
            spark_history_server_config = GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig(**spark_history_server_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc4c357fbb0a4e096210557d8e92d8a0fcc0cc92a9f2db13c5363a9ddb5cf85d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#metastore_service GoogleDataprocSessionTemplate#metastore_service}
        '''
        result = self._values.get("metastore_service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spark_history_server_config(
        self,
    ) -> typing.Optional["GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig"]:
        '''spark_history_server_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#spark_history_server_config GoogleDataprocSessionTemplate#spark_history_server_config}
        '''
        result = self._values.get("spark_history_server_config")
        return typing.cast(typing.Optional["GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocSessionTemplate.GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce9c5f49067fac0d5067dbb4f57815ed01769905d1a9206837526b8ae700346c)
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
        :param dataproc_cluster: Resource name of an existing Dataproc Cluster to act as a Spark History Server for the workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#dataproc_cluster GoogleDataprocSessionTemplate#dataproc_cluster}
        '''
        value = GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig(
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
    ) -> "GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfigOutputReference":
        return typing.cast("GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfigOutputReference", jsii.get(self, "sparkHistoryServerConfig"))

    @builtins.property
    @jsii.member(jsii_name="metastoreServiceInput")
    def metastore_service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metastoreServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkHistoryServerConfigInput")
    def spark_history_server_config_input(
        self,
    ) -> typing.Optional["GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig"], jsii.get(self, "sparkHistoryServerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="metastoreService")
    def metastore_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metastoreService"))

    @metastore_service.setter
    def metastore_service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34f16b325c1e0a187c12db16d0ecdf9cd4f52841a4bcf4b6e5bc3a182936ac5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metastoreService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfig]:
        return typing.cast(typing.Optional[GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cde1b4c0857e47e7e1447427bc15025cd3cda913b6b8a818e6e556d5f43ae8e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocSessionTemplate.GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig",
    jsii_struct_bases=[],
    name_mapping={"dataproc_cluster": "dataprocCluster"},
)
class GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig:
    def __init__(
        self,
        *,
        dataproc_cluster: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataproc_cluster: Resource name of an existing Dataproc Cluster to act as a Spark History Server for the workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#dataproc_cluster GoogleDataprocSessionTemplate#dataproc_cluster}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd0920fe4b586a6a127a093589f590d4b690076f58ae54ed3773a96402c75e8a)
            check_type(argname="argument dataproc_cluster", value=dataproc_cluster, expected_type=type_hints["dataproc_cluster"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dataproc_cluster is not None:
            self._values["dataproc_cluster"] = dataproc_cluster

    @builtins.property
    def dataproc_cluster(self) -> typing.Optional[builtins.str]:
        '''Resource name of an existing Dataproc Cluster to act as a Spark History Server for the workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#dataproc_cluster GoogleDataprocSessionTemplate#dataproc_cluster}
        '''
        result = self._values.get("dataproc_cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocSessionTemplate.GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eadf747cca1d675be304790ae20052c84ea9785090fdf3bd1702fe322009104f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e54e453fd344449757aa0a57e6d421a78b098894a5d1ed4463912ff894cf7db2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataprocCluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig]:
        return typing.cast(typing.Optional[GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8deff343d74a46f23f548fc1199f5578222d9498985fa22939b2873f5cb9a18f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocSessionTemplate.GoogleDataprocSessionTemplateJupyterSession",
    jsii_struct_bases=[],
    name_mapping={"display_name": "displayName", "kernel": "kernel"},
)
class GoogleDataprocSessionTemplateJupyterSession:
    def __init__(
        self,
        *,
        display_name: typing.Optional[builtins.str] = None,
        kernel: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param display_name: Display name, shown in the Jupyter kernelspec card. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#display_name GoogleDataprocSessionTemplate#display_name}
        :param kernel: Kernel to be used with Jupyter interactive session. Possible values: ["PYTHON", "SCALA"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#kernel GoogleDataprocSessionTemplate#kernel}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44ef2bbef6d09f9b298c10693395e87b6a202fbc98f0352a28f473ca721b0326)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#display_name GoogleDataprocSessionTemplate#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kernel(self) -> typing.Optional[builtins.str]:
        '''Kernel to be used with Jupyter interactive session. Possible values: ["PYTHON", "SCALA"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#kernel GoogleDataprocSessionTemplate#kernel}
        '''
        result = self._values.get("kernel")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocSessionTemplateJupyterSession(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocSessionTemplateJupyterSessionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocSessionTemplate.GoogleDataprocSessionTemplateJupyterSessionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e87c3c366756c63eafb6b357fd308a9ee931de2c31865a20eb0d8d2277c7ca75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6a80f68b7f41fd4593d3c16ea2267d8be795cf3ac48cfc4e5f1bbccc26a38d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kernel")
    def kernel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kernel"))

    @kernel.setter
    def kernel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3d748500787178bf51aa2a6142a5f8cab2875722de2178ab245ee85f0cf8e21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kernel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocSessionTemplateJupyterSession]:
        return typing.cast(typing.Optional[GoogleDataprocSessionTemplateJupyterSession], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocSessionTemplateJupyterSession],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8f2a6d4ddf9663f3272e195de6a550a82a034aedb48b4a5e2be95f520d33044)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocSessionTemplate.GoogleDataprocSessionTemplateRuntimeConfig",
    jsii_struct_bases=[],
    name_mapping={
        "container_image": "containerImage",
        "properties": "properties",
        "version": "version",
    },
)
class GoogleDataprocSessionTemplateRuntimeConfig:
    def __init__(
        self,
        *,
        container_image: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_image: Optional custom container image for the job runtime environment. If not specified, a default container image will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#container_image GoogleDataprocSessionTemplate#container_image}
        :param properties: A mapping of property names to values, which are used to configure workload execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#properties GoogleDataprocSessionTemplate#properties}
        :param version: Version of the session runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#version GoogleDataprocSessionTemplate#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f454fc71ed001a41c0edaaed466e844b807b13025e996ca9dcc4d971d17ffab)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#container_image GoogleDataprocSessionTemplate#container_image}
        '''
        result = self._values.get("container_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping of property names to values, which are used to configure workload execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#properties GoogleDataprocSessionTemplate#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of the session runtime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#version GoogleDataprocSessionTemplate#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocSessionTemplateRuntimeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocSessionTemplateRuntimeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocSessionTemplate.GoogleDataprocSessionTemplateRuntimeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8a6faa375bed2e79fb82cfa1bd5f661b266f11517cadc978cb80be7f08a8af5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfd2d267c0647d6bcf535f11e63755d598671bb5f69456b0067f4efcc6a3047a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerImage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ef7ed584398e62d78b28bb5a10939791dbaf90256195fdff86885d461ce0481)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c214e6da29ce7d0f4adc5b0e5f63294596e48ef1f1e9358b62251b6971ee996)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocSessionTemplateRuntimeConfig]:
        return typing.cast(typing.Optional[GoogleDataprocSessionTemplateRuntimeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocSessionTemplateRuntimeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e00c7b27575ac4c6c685cf5b45d42465d20192d28cb8efba5e54fdd19e56f95b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocSessionTemplate.GoogleDataprocSessionTemplateSparkConnectSession",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataprocSessionTemplateSparkConnectSession:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocSessionTemplateSparkConnectSession(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocSessionTemplateSparkConnectSessionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocSessionTemplate.GoogleDataprocSessionTemplateSparkConnectSessionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f21da95a5248871e375e17c7c3e5306c8ef5c2b1f13b17807449291ec1e7b39)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocSessionTemplateSparkConnectSession]:
        return typing.cast(typing.Optional[GoogleDataprocSessionTemplateSparkConnectSession], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocSessionTemplateSparkConnectSession],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4186a0cf80f98cb785414f3c7758773598053577e68027015d0b31cfd40775e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocSessionTemplate.GoogleDataprocSessionTemplateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDataprocSessionTemplateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#create GoogleDataprocSessionTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#delete GoogleDataprocSessionTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#update GoogleDataprocSessionTemplate#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0adadeb3dffbabc6d357088f57afbf8bdc1579f50c76ffda9935195baf72f62c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#create GoogleDataprocSessionTemplate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#delete GoogleDataprocSessionTemplate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dataproc_session_template#update GoogleDataprocSessionTemplate#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocSessionTemplateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocSessionTemplateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocSessionTemplate.GoogleDataprocSessionTemplateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__194207ca492bd99d71eeff4b3189567cd105be811bb0995189ba75e256fe2a10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d347319a77dd2445ecee45a6476fc2058df325bd1e92fd8ad51502fb17f34066)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__812d8463d547967a9660705c57291893f673f1da4ab68a9850ee972d67b1bb81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d3d5a47a9290a9871b2cb0291461447919a9a9a4673208210c99170ac7aae98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocSessionTemplateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocSessionTemplateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocSessionTemplateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8807816c29fe233e6a2013a9651a57596e0f907642b747dc4c89d316f87782c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDataprocSessionTemplate",
    "GoogleDataprocSessionTemplateConfig",
    "GoogleDataprocSessionTemplateEnvironmentConfig",
    "GoogleDataprocSessionTemplateEnvironmentConfigExecutionConfig",
    "GoogleDataprocSessionTemplateEnvironmentConfigExecutionConfigOutputReference",
    "GoogleDataprocSessionTemplateEnvironmentConfigOutputReference",
    "GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfig",
    "GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigOutputReference",
    "GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig",
    "GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfigOutputReference",
    "GoogleDataprocSessionTemplateJupyterSession",
    "GoogleDataprocSessionTemplateJupyterSessionOutputReference",
    "GoogleDataprocSessionTemplateRuntimeConfig",
    "GoogleDataprocSessionTemplateRuntimeConfigOutputReference",
    "GoogleDataprocSessionTemplateSparkConnectSession",
    "GoogleDataprocSessionTemplateSparkConnectSessionOutputReference",
    "GoogleDataprocSessionTemplateTimeouts",
    "GoogleDataprocSessionTemplateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__9d1d71de0e05f8307207f58113db40d72b5f3bccbc825c02b21f196053ff3dee(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    environment_config: typing.Optional[typing.Union[GoogleDataprocSessionTemplateEnvironmentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    jupyter_session: typing.Optional[typing.Union[GoogleDataprocSessionTemplateJupyterSession, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    runtime_config: typing.Optional[typing.Union[GoogleDataprocSessionTemplateRuntimeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_connect_session: typing.Optional[typing.Union[GoogleDataprocSessionTemplateSparkConnectSession, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataprocSessionTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4fcb8b882f8dcfc4cb86751337dd496ca503155c660d061f6adf1de779c41c1a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85ac8b6191a9b0c26a93593c276e730375b1ce891fd7fbb6c438d7e35cafc297(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b3f6caceb2cda8d6ffde4a4d301e05abf04803858534ad91dbcbdf877bf550(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b01ae4c83ea37e061369c4e09bab45592cd01c417a39424707c17a8a5c2069b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bd9dcff0f8798e9e312d9ddcb1aa0da1b053415b8a10736b6abb0e9084c8397(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__505265141f9faf36c9101ae5f4004407881d82ace84535921d278622b0d186d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0aeea7cd6f6467ab4bf6e3f88aa3e71628749b55ecbc15c769bd36a340bccbf(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    environment_config: typing.Optional[typing.Union[GoogleDataprocSessionTemplateEnvironmentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    jupyter_session: typing.Optional[typing.Union[GoogleDataprocSessionTemplateJupyterSession, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    runtime_config: typing.Optional[typing.Union[GoogleDataprocSessionTemplateRuntimeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_connect_session: typing.Optional[typing.Union[GoogleDataprocSessionTemplateSparkConnectSession, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataprocSessionTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b535d4a70bef6798398282ebf8bc52d0eb3d102ab1524a31177534f1218590(
    *,
    execution_config: typing.Optional[typing.Union[GoogleDataprocSessionTemplateEnvironmentConfigExecutionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    peripherals_config: typing.Optional[typing.Union[GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138f4a7012855226cbd8b7796bdbe991a6ef21f758c551936d4f2dfb12ec3680(
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

def _typecheckingstub__b37b3fe327395f836abd22e2dc6b63a9e2ea160aa4c1952bd63090e5d09c9402(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b85b7a945c0e315c581ef0760ea16848cf527e3cffefc52dfd27351e9a672158(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f93f54b2a439425b6c4c2278de288004a41dff4b7f13c47f265f0e029cb052a0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddf18c7aec90cfd8025a188faf67072453119681ca4e22893227268717477454(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75392aa1ad33a2e96ed8b06214bb72e9e834249c36b0199d5927dee3ed0070f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a769fb3211906fe70c294ace5c90f97250d0f735073ba2593017321fd27ee8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd623ab935baa59d2f7718ceaeb2ee78e8819d4e662d4d48b1f5d0428889050d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48dbcd51a2c149a99deaa8b546cbc716f37bc897ae931ea5a10251ac8fb8eec5(
    value: typing.Optional[GoogleDataprocSessionTemplateEnvironmentConfigExecutionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3881c92700760708734dbdedd48677fa24609e78ec446756c5f6f3f887ecb2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b8bd0756da282b6087332e37a9459768bfd18fca0f14d40be1509782ac30ea(
    value: typing.Optional[GoogleDataprocSessionTemplateEnvironmentConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc4c357fbb0a4e096210557d8e92d8a0fcc0cc92a9f2db13c5363a9ddb5cf85d(
    *,
    metastore_service: typing.Optional[builtins.str] = None,
    spark_history_server_config: typing.Optional[typing.Union[GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce9c5f49067fac0d5067dbb4f57815ed01769905d1a9206837526b8ae700346c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34f16b325c1e0a187c12db16d0ecdf9cd4f52841a4bcf4b6e5bc3a182936ac5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cde1b4c0857e47e7e1447427bc15025cd3cda913b6b8a818e6e556d5f43ae8e4(
    value: typing.Optional[GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd0920fe4b586a6a127a093589f590d4b690076f58ae54ed3773a96402c75e8a(
    *,
    dataproc_cluster: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eadf747cca1d675be304790ae20052c84ea9785090fdf3bd1702fe322009104f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e54e453fd344449757aa0a57e6d421a78b098894a5d1ed4463912ff894cf7db2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8deff343d74a46f23f548fc1199f5578222d9498985fa22939b2873f5cb9a18f(
    value: typing.Optional[GoogleDataprocSessionTemplateEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ef2bbef6d09f9b298c10693395e87b6a202fbc98f0352a28f473ca721b0326(
    *,
    display_name: typing.Optional[builtins.str] = None,
    kernel: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e87c3c366756c63eafb6b357fd308a9ee931de2c31865a20eb0d8d2277c7ca75(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6a80f68b7f41fd4593d3c16ea2267d8be795cf3ac48cfc4e5f1bbccc26a38d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d748500787178bf51aa2a6142a5f8cab2875722de2178ab245ee85f0cf8e21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f2a6d4ddf9663f3272e195de6a550a82a034aedb48b4a5e2be95f520d33044(
    value: typing.Optional[GoogleDataprocSessionTemplateJupyterSession],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f454fc71ed001a41c0edaaed466e844b807b13025e996ca9dcc4d971d17ffab(
    *,
    container_image: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a6faa375bed2e79fb82cfa1bd5f661b266f11517cadc978cb80be7f08a8af5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd2d267c0647d6bcf535f11e63755d598671bb5f69456b0067f4efcc6a3047a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ef7ed584398e62d78b28bb5a10939791dbaf90256195fdff86885d461ce0481(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c214e6da29ce7d0f4adc5b0e5f63294596e48ef1f1e9358b62251b6971ee996(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e00c7b27575ac4c6c685cf5b45d42465d20192d28cb8efba5e54fdd19e56f95b(
    value: typing.Optional[GoogleDataprocSessionTemplateRuntimeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f21da95a5248871e375e17c7c3e5306c8ef5c2b1f13b17807449291ec1e7b39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4186a0cf80f98cb785414f3c7758773598053577e68027015d0b31cfd40775e5(
    value: typing.Optional[GoogleDataprocSessionTemplateSparkConnectSession],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0adadeb3dffbabc6d357088f57afbf8bdc1579f50c76ffda9935195baf72f62c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__194207ca492bd99d71eeff4b3189567cd105be811bb0995189ba75e256fe2a10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d347319a77dd2445ecee45a6476fc2058df325bd1e92fd8ad51502fb17f34066(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__812d8463d547967a9660705c57291893f673f1da4ab68a9850ee972d67b1bb81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d3d5a47a9290a9871b2cb0291461447919a9a9a4673208210c99170ac7aae98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8807816c29fe233e6a2013a9651a57596e0f907642b747dc4c89d316f87782c2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocSessionTemplateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
