r'''
# `google_colab_notebook_execution`

Refer to the Terraform Registry for docs: [`google_colab_notebook_execution`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution).
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


class ColabNotebookExecution(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabNotebookExecution.ColabNotebookExecution",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution google_colab_notebook_execution}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        gcs_output_uri: builtins.str,
        location: builtins.str,
        dataform_repository_source: typing.Optional[typing.Union["ColabNotebookExecutionDataformRepositorySource", typing.Dict[builtins.str, typing.Any]]] = None,
        direct_notebook_source: typing.Optional[typing.Union["ColabNotebookExecutionDirectNotebookSource", typing.Dict[builtins.str, typing.Any]]] = None,
        execution_timeout: typing.Optional[builtins.str] = None,
        execution_user: typing.Optional[builtins.str] = None,
        gcs_notebook_source: typing.Optional[typing.Union["ColabNotebookExecutionGcsNotebookSource", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        notebook_execution_job_id: typing.Optional[builtins.str] = None,
        notebook_runtime_template_resource_name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ColabNotebookExecutionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution google_colab_notebook_execution} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: Required. The display name of the Notebook Execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#display_name ColabNotebookExecution#display_name}
        :param gcs_output_uri: The Cloud Storage location to upload the result to. Format:'gs://bucket-name'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#gcs_output_uri ColabNotebookExecution#gcs_output_uri}
        :param location: The location for the resource: https://cloud.google.com/colab/docs/locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#location ColabNotebookExecution#location}
        :param dataform_repository_source: dataform_repository_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#dataform_repository_source ColabNotebookExecution#dataform_repository_source}
        :param direct_notebook_source: direct_notebook_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#direct_notebook_source ColabNotebookExecution#direct_notebook_source}
        :param execution_timeout: Max running time of the execution job in seconds (default 86400s / 24 hrs). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#execution_timeout ColabNotebookExecution#execution_timeout}
        :param execution_user: The user email to run the execution as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#execution_user ColabNotebookExecution#execution_user}
        :param gcs_notebook_source: gcs_notebook_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#gcs_notebook_source ColabNotebookExecution#gcs_notebook_source}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#id ColabNotebookExecution#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notebook_execution_job_id: User specified ID for the Notebook Execution Job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#notebook_execution_job_id ColabNotebookExecution#notebook_execution_job_id}
        :param notebook_runtime_template_resource_name: The NotebookRuntimeTemplate to source compute configuration from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#notebook_runtime_template_resource_name ColabNotebookExecution#notebook_runtime_template_resource_name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#project ColabNotebookExecution#project}.
        :param service_account: The service account to run the execution as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#service_account ColabNotebookExecution#service_account}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#timeouts ColabNotebookExecution#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78aced19506212f1d9ae05b87e83b1be8e73d0dd5e68211c647f12dd68b2e6b1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ColabNotebookExecutionConfig(
            display_name=display_name,
            gcs_output_uri=gcs_output_uri,
            location=location,
            dataform_repository_source=dataform_repository_source,
            direct_notebook_source=direct_notebook_source,
            execution_timeout=execution_timeout,
            execution_user=execution_user,
            gcs_notebook_source=gcs_notebook_source,
            id=id,
            notebook_execution_job_id=notebook_execution_job_id,
            notebook_runtime_template_resource_name=notebook_runtime_template_resource_name,
            project=project,
            service_account=service_account,
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
        '''Generates CDKTF code for importing a ColabNotebookExecution resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ColabNotebookExecution to import.
        :param import_from_id: The id of the existing ColabNotebookExecution that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ColabNotebookExecution to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e9651f7b15d05744edf7f0277c50f899e202e5cf382e52bc2faf88109c2afca)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDataformRepositorySource")
    def put_dataform_repository_source(
        self,
        *,
        dataform_repository_resource_name: builtins.str,
        commit_sha: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataform_repository_resource_name: The resource name of the Dataform Repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#dataform_repository_resource_name ColabNotebookExecution#dataform_repository_resource_name}
        :param commit_sha: The commit SHA to read repository with. If unset, the file will be read at HEAD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#commit_sha ColabNotebookExecution#commit_sha}
        '''
        value = ColabNotebookExecutionDataformRepositorySource(
            dataform_repository_resource_name=dataform_repository_resource_name,
            commit_sha=commit_sha,
        )

        return typing.cast(None, jsii.invoke(self, "putDataformRepositorySource", [value]))

    @jsii.member(jsii_name="putDirectNotebookSource")
    def put_direct_notebook_source(self, *, content: builtins.str) -> None:
        '''
        :param content: The base64-encoded contents of the input notebook file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#content ColabNotebookExecution#content}
        '''
        value = ColabNotebookExecutionDirectNotebookSource(content=content)

        return typing.cast(None, jsii.invoke(self, "putDirectNotebookSource", [value]))

    @jsii.member(jsii_name="putGcsNotebookSource")
    def put_gcs_notebook_source(
        self,
        *,
        uri: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: The Cloud Storage uri pointing to the ipynb file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#uri ColabNotebookExecution#uri}
        :param generation: The version of the Cloud Storage object to read. If unset, the current version of the object is read. See https://cloud.google.com/storage/docs/metadata#generation-number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#generation ColabNotebookExecution#generation}
        '''
        value = ColabNotebookExecutionGcsNotebookSource(uri=uri, generation=generation)

        return typing.cast(None, jsii.invoke(self, "putGcsNotebookSource", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#create ColabNotebookExecution#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#delete ColabNotebookExecution#delete}.
        '''
        value = ColabNotebookExecutionTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDataformRepositorySource")
    def reset_dataform_repository_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataformRepositorySource", []))

    @jsii.member(jsii_name="resetDirectNotebookSource")
    def reset_direct_notebook_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirectNotebookSource", []))

    @jsii.member(jsii_name="resetExecutionTimeout")
    def reset_execution_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionTimeout", []))

    @jsii.member(jsii_name="resetExecutionUser")
    def reset_execution_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionUser", []))

    @jsii.member(jsii_name="resetGcsNotebookSource")
    def reset_gcs_notebook_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcsNotebookSource", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNotebookExecutionJobId")
    def reset_notebook_execution_job_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotebookExecutionJobId", []))

    @jsii.member(jsii_name="resetNotebookRuntimeTemplateResourceName")
    def reset_notebook_runtime_template_resource_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotebookRuntimeTemplateResourceName", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

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
    @jsii.member(jsii_name="dataformRepositorySource")
    def dataform_repository_source(
        self,
    ) -> "ColabNotebookExecutionDataformRepositorySourceOutputReference":
        return typing.cast("ColabNotebookExecutionDataformRepositorySourceOutputReference", jsii.get(self, "dataformRepositorySource"))

    @builtins.property
    @jsii.member(jsii_name="directNotebookSource")
    def direct_notebook_source(
        self,
    ) -> "ColabNotebookExecutionDirectNotebookSourceOutputReference":
        return typing.cast("ColabNotebookExecutionDirectNotebookSourceOutputReference", jsii.get(self, "directNotebookSource"))

    @builtins.property
    @jsii.member(jsii_name="gcsNotebookSource")
    def gcs_notebook_source(
        self,
    ) -> "ColabNotebookExecutionGcsNotebookSourceOutputReference":
        return typing.cast("ColabNotebookExecutionGcsNotebookSourceOutputReference", jsii.get(self, "gcsNotebookSource"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ColabNotebookExecutionTimeoutsOutputReference":
        return typing.cast("ColabNotebookExecutionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="dataformRepositorySourceInput")
    def dataform_repository_source_input(
        self,
    ) -> typing.Optional["ColabNotebookExecutionDataformRepositorySource"]:
        return typing.cast(typing.Optional["ColabNotebookExecutionDataformRepositorySource"], jsii.get(self, "dataformRepositorySourceInput"))

    @builtins.property
    @jsii.member(jsii_name="directNotebookSourceInput")
    def direct_notebook_source_input(
        self,
    ) -> typing.Optional["ColabNotebookExecutionDirectNotebookSource"]:
        return typing.cast(typing.Optional["ColabNotebookExecutionDirectNotebookSource"], jsii.get(self, "directNotebookSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="executionTimeoutInput")
    def execution_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="executionUserInput")
    def execution_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionUserInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsNotebookSourceInput")
    def gcs_notebook_source_input(
        self,
    ) -> typing.Optional["ColabNotebookExecutionGcsNotebookSource"]:
        return typing.cast(typing.Optional["ColabNotebookExecutionGcsNotebookSource"], jsii.get(self, "gcsNotebookSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsOutputUriInput")
    def gcs_output_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcsOutputUriInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="notebookExecutionJobIdInput")
    def notebook_execution_job_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notebookExecutionJobIdInput"))

    @builtins.property
    @jsii.member(jsii_name="notebookRuntimeTemplateResourceNameInput")
    def notebook_runtime_template_resource_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notebookRuntimeTemplateResourceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ColabNotebookExecutionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ColabNotebookExecutionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30da227675d3adf03532d7107efe28bbee110908d077608cbdc52c2e5031b4ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionTimeout")
    def execution_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionTimeout"))

    @execution_timeout.setter
    def execution_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c086223ad87e1e64bc2c3bcd2df3afe160fa5714f575cd26e2e9a90a2f871b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionUser")
    def execution_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionUser"))

    @execution_user.setter
    def execution_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd7c261b7e4182c7241b83da35be722bc19c108b4a044b425bcee61f20503de5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gcsOutputUri")
    def gcs_output_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcsOutputUri"))

    @gcs_output_uri.setter
    def gcs_output_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f1aa06a97fbb169c8d92f49d2edf2233f1e6198d6792febb1f40e6bb6c60b39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcsOutputUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37b5fb4da5159fa99a0a153fdc941ff008bf44d9fae3ed0aff42bc564dd8e999)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e67c149be0784200a16d36a66c1ecf77679065fc80ca8159650a5715da8756a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notebookExecutionJobId")
    def notebook_execution_job_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notebookExecutionJobId"))

    @notebook_execution_job_id.setter
    def notebook_execution_job_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2c542390a40cc83132586b3e8839e446f0fa771403462ec4bbb1f9644e8667d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notebookExecutionJobId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notebookRuntimeTemplateResourceName")
    def notebook_runtime_template_resource_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notebookRuntimeTemplateResourceName"))

    @notebook_runtime_template_resource_name.setter
    def notebook_runtime_template_resource_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d26f275e9bb7d231d13886925239df672fd72fa83c0daf1dbe720a5ad216e0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notebookRuntimeTemplateResourceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4534bdac2bf1b193fc4530e5cdd96722339d127d4421bc2e7a4660a39c4bcf7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc1e111ef1a4a90247cb63249144c1555c5e0a3453f8291a67f8515ccc8eef48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.colabNotebookExecution.ColabNotebookExecutionConfig",
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
        "gcs_output_uri": "gcsOutputUri",
        "location": "location",
        "dataform_repository_source": "dataformRepositorySource",
        "direct_notebook_source": "directNotebookSource",
        "execution_timeout": "executionTimeout",
        "execution_user": "executionUser",
        "gcs_notebook_source": "gcsNotebookSource",
        "id": "id",
        "notebook_execution_job_id": "notebookExecutionJobId",
        "notebook_runtime_template_resource_name": "notebookRuntimeTemplateResourceName",
        "project": "project",
        "service_account": "serviceAccount",
        "timeouts": "timeouts",
    },
)
class ColabNotebookExecutionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        gcs_output_uri: builtins.str,
        location: builtins.str,
        dataform_repository_source: typing.Optional[typing.Union["ColabNotebookExecutionDataformRepositorySource", typing.Dict[builtins.str, typing.Any]]] = None,
        direct_notebook_source: typing.Optional[typing.Union["ColabNotebookExecutionDirectNotebookSource", typing.Dict[builtins.str, typing.Any]]] = None,
        execution_timeout: typing.Optional[builtins.str] = None,
        execution_user: typing.Optional[builtins.str] = None,
        gcs_notebook_source: typing.Optional[typing.Union["ColabNotebookExecutionGcsNotebookSource", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        notebook_execution_job_id: typing.Optional[builtins.str] = None,
        notebook_runtime_template_resource_name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ColabNotebookExecutionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: Required. The display name of the Notebook Execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#display_name ColabNotebookExecution#display_name}
        :param gcs_output_uri: The Cloud Storage location to upload the result to. Format:'gs://bucket-name'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#gcs_output_uri ColabNotebookExecution#gcs_output_uri}
        :param location: The location for the resource: https://cloud.google.com/colab/docs/locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#location ColabNotebookExecution#location}
        :param dataform_repository_source: dataform_repository_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#dataform_repository_source ColabNotebookExecution#dataform_repository_source}
        :param direct_notebook_source: direct_notebook_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#direct_notebook_source ColabNotebookExecution#direct_notebook_source}
        :param execution_timeout: Max running time of the execution job in seconds (default 86400s / 24 hrs). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#execution_timeout ColabNotebookExecution#execution_timeout}
        :param execution_user: The user email to run the execution as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#execution_user ColabNotebookExecution#execution_user}
        :param gcs_notebook_source: gcs_notebook_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#gcs_notebook_source ColabNotebookExecution#gcs_notebook_source}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#id ColabNotebookExecution#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notebook_execution_job_id: User specified ID for the Notebook Execution Job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#notebook_execution_job_id ColabNotebookExecution#notebook_execution_job_id}
        :param notebook_runtime_template_resource_name: The NotebookRuntimeTemplate to source compute configuration from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#notebook_runtime_template_resource_name ColabNotebookExecution#notebook_runtime_template_resource_name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#project ColabNotebookExecution#project}.
        :param service_account: The service account to run the execution as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#service_account ColabNotebookExecution#service_account}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#timeouts ColabNotebookExecution#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(dataform_repository_source, dict):
            dataform_repository_source = ColabNotebookExecutionDataformRepositorySource(**dataform_repository_source)
        if isinstance(direct_notebook_source, dict):
            direct_notebook_source = ColabNotebookExecutionDirectNotebookSource(**direct_notebook_source)
        if isinstance(gcs_notebook_source, dict):
            gcs_notebook_source = ColabNotebookExecutionGcsNotebookSource(**gcs_notebook_source)
        if isinstance(timeouts, dict):
            timeouts = ColabNotebookExecutionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__323e884aa371c15841c9899ef35be6539e0410e5ae6f340dbf03f641d40846bf)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument gcs_output_uri", value=gcs_output_uri, expected_type=type_hints["gcs_output_uri"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument dataform_repository_source", value=dataform_repository_source, expected_type=type_hints["dataform_repository_source"])
            check_type(argname="argument direct_notebook_source", value=direct_notebook_source, expected_type=type_hints["direct_notebook_source"])
            check_type(argname="argument execution_timeout", value=execution_timeout, expected_type=type_hints["execution_timeout"])
            check_type(argname="argument execution_user", value=execution_user, expected_type=type_hints["execution_user"])
            check_type(argname="argument gcs_notebook_source", value=gcs_notebook_source, expected_type=type_hints["gcs_notebook_source"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument notebook_execution_job_id", value=notebook_execution_job_id, expected_type=type_hints["notebook_execution_job_id"])
            check_type(argname="argument notebook_runtime_template_resource_name", value=notebook_runtime_template_resource_name, expected_type=type_hints["notebook_runtime_template_resource_name"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "gcs_output_uri": gcs_output_uri,
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
        if dataform_repository_source is not None:
            self._values["dataform_repository_source"] = dataform_repository_source
        if direct_notebook_source is not None:
            self._values["direct_notebook_source"] = direct_notebook_source
        if execution_timeout is not None:
            self._values["execution_timeout"] = execution_timeout
        if execution_user is not None:
            self._values["execution_user"] = execution_user
        if gcs_notebook_source is not None:
            self._values["gcs_notebook_source"] = gcs_notebook_source
        if id is not None:
            self._values["id"] = id
        if notebook_execution_job_id is not None:
            self._values["notebook_execution_job_id"] = notebook_execution_job_id
        if notebook_runtime_template_resource_name is not None:
            self._values["notebook_runtime_template_resource_name"] = notebook_runtime_template_resource_name
        if project is not None:
            self._values["project"] = project
        if service_account is not None:
            self._values["service_account"] = service_account
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
        '''Required. The display name of the Notebook Execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#display_name ColabNotebookExecution#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gcs_output_uri(self) -> builtins.str:
        '''The Cloud Storage location to upload the result to. Format:'gs://bucket-name'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#gcs_output_uri ColabNotebookExecution#gcs_output_uri}
        '''
        result = self._values.get("gcs_output_uri")
        assert result is not None, "Required property 'gcs_output_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource: https://cloud.google.com/colab/docs/locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#location ColabNotebookExecution#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dataform_repository_source(
        self,
    ) -> typing.Optional["ColabNotebookExecutionDataformRepositorySource"]:
        '''dataform_repository_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#dataform_repository_source ColabNotebookExecution#dataform_repository_source}
        '''
        result = self._values.get("dataform_repository_source")
        return typing.cast(typing.Optional["ColabNotebookExecutionDataformRepositorySource"], result)

    @builtins.property
    def direct_notebook_source(
        self,
    ) -> typing.Optional["ColabNotebookExecutionDirectNotebookSource"]:
        '''direct_notebook_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#direct_notebook_source ColabNotebookExecution#direct_notebook_source}
        '''
        result = self._values.get("direct_notebook_source")
        return typing.cast(typing.Optional["ColabNotebookExecutionDirectNotebookSource"], result)

    @builtins.property
    def execution_timeout(self) -> typing.Optional[builtins.str]:
        '''Max running time of the execution job in seconds (default 86400s / 24 hrs).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#execution_timeout ColabNotebookExecution#execution_timeout}
        '''
        result = self._values.get("execution_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_user(self) -> typing.Optional[builtins.str]:
        '''The user email to run the execution as.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#execution_user ColabNotebookExecution#execution_user}
        '''
        result = self._values.get("execution_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcs_notebook_source(
        self,
    ) -> typing.Optional["ColabNotebookExecutionGcsNotebookSource"]:
        '''gcs_notebook_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#gcs_notebook_source ColabNotebookExecution#gcs_notebook_source}
        '''
        result = self._values.get("gcs_notebook_source")
        return typing.cast(typing.Optional["ColabNotebookExecutionGcsNotebookSource"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#id ColabNotebookExecution#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notebook_execution_job_id(self) -> typing.Optional[builtins.str]:
        '''User specified ID for the Notebook Execution Job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#notebook_execution_job_id ColabNotebookExecution#notebook_execution_job_id}
        '''
        result = self._values.get("notebook_execution_job_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notebook_runtime_template_resource_name(self) -> typing.Optional[builtins.str]:
        '''The NotebookRuntimeTemplate to source compute configuration from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#notebook_runtime_template_resource_name ColabNotebookExecution#notebook_runtime_template_resource_name}
        '''
        result = self._values.get("notebook_runtime_template_resource_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#project ColabNotebookExecution#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''The service account to run the execution as.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#service_account ColabNotebookExecution#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ColabNotebookExecutionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#timeouts ColabNotebookExecution#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ColabNotebookExecutionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColabNotebookExecutionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.colabNotebookExecution.ColabNotebookExecutionDataformRepositorySource",
    jsii_struct_bases=[],
    name_mapping={
        "dataform_repository_resource_name": "dataformRepositoryResourceName",
        "commit_sha": "commitSha",
    },
)
class ColabNotebookExecutionDataformRepositorySource:
    def __init__(
        self,
        *,
        dataform_repository_resource_name: builtins.str,
        commit_sha: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataform_repository_resource_name: The resource name of the Dataform Repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#dataform_repository_resource_name ColabNotebookExecution#dataform_repository_resource_name}
        :param commit_sha: The commit SHA to read repository with. If unset, the file will be read at HEAD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#commit_sha ColabNotebookExecution#commit_sha}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2e3861fbbaf48396eb1e1b682d6bf11892af3a7bfde1ae6b4758f14f1a9c772)
            check_type(argname="argument dataform_repository_resource_name", value=dataform_repository_resource_name, expected_type=type_hints["dataform_repository_resource_name"])
            check_type(argname="argument commit_sha", value=commit_sha, expected_type=type_hints["commit_sha"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataform_repository_resource_name": dataform_repository_resource_name,
        }
        if commit_sha is not None:
            self._values["commit_sha"] = commit_sha

    @builtins.property
    def dataform_repository_resource_name(self) -> builtins.str:
        '''The resource name of the Dataform Repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#dataform_repository_resource_name ColabNotebookExecution#dataform_repository_resource_name}
        '''
        result = self._values.get("dataform_repository_resource_name")
        assert result is not None, "Required property 'dataform_repository_resource_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def commit_sha(self) -> typing.Optional[builtins.str]:
        '''The commit SHA to read repository with. If unset, the file will be read at HEAD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#commit_sha ColabNotebookExecution#commit_sha}
        '''
        result = self._values.get("commit_sha")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColabNotebookExecutionDataformRepositorySource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ColabNotebookExecutionDataformRepositorySourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabNotebookExecution.ColabNotebookExecutionDataformRepositorySourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe95ab2c0fb1f5c66c982ea5de13f97536fdaa2285f99264395809c99682c2b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCommitSha")
    def reset_commit_sha(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitSha", []))

    @builtins.property
    @jsii.member(jsii_name="commitShaInput")
    def commit_sha_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commitShaInput"))

    @builtins.property
    @jsii.member(jsii_name="dataformRepositoryResourceNameInput")
    def dataform_repository_resource_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataformRepositoryResourceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="commitSha")
    def commit_sha(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitSha"))

    @commit_sha.setter
    def commit_sha(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62c2e280006fcf6fca31e3c91d38b6133a81c47f6f5891cbc39ba9758022d29d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitSha", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataformRepositoryResourceName")
    def dataform_repository_resource_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataformRepositoryResourceName"))

    @dataform_repository_resource_name.setter
    def dataform_repository_resource_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff4e7dc515815d28319823b73f21ac5345ec4939adb14fdaa6fb694b05e4fdcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataformRepositoryResourceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ColabNotebookExecutionDataformRepositorySource]:
        return typing.cast(typing.Optional[ColabNotebookExecutionDataformRepositorySource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ColabNotebookExecutionDataformRepositorySource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fecdc0e4b677047175b5aef8ac4aff17255c0478a5fb5f396acbc6c3f26622d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.colabNotebookExecution.ColabNotebookExecutionDirectNotebookSource",
    jsii_struct_bases=[],
    name_mapping={"content": "content"},
)
class ColabNotebookExecutionDirectNotebookSource:
    def __init__(self, *, content: builtins.str) -> None:
        '''
        :param content: The base64-encoded contents of the input notebook file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#content ColabNotebookExecution#content}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__334d9ed4742a35125b26f44a82d8af471e20ab7a99749cd25123ca296eb2ee19)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
        }

    @builtins.property
    def content(self) -> builtins.str:
        '''The base64-encoded contents of the input notebook file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#content ColabNotebookExecution#content}
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColabNotebookExecutionDirectNotebookSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ColabNotebookExecutionDirectNotebookSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabNotebookExecution.ColabNotebookExecutionDirectNotebookSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__225433320a1ea10e450b7d08c7121d7fe3bf175c029f2492fc472128fcce8312)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b50bdc399413732630b7d5c350cecfa9e9517bfe153c70532f6d743b6aa21e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ColabNotebookExecutionDirectNotebookSource]:
        return typing.cast(typing.Optional[ColabNotebookExecutionDirectNotebookSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ColabNotebookExecutionDirectNotebookSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b28b70b9afcd0bb0437feb6ddd3ceb23d86f107cada395ed8ce9fe314034ca7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.colabNotebookExecution.ColabNotebookExecutionGcsNotebookSource",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "generation": "generation"},
)
class ColabNotebookExecutionGcsNotebookSource:
    def __init__(
        self,
        *,
        uri: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: The Cloud Storage uri pointing to the ipynb file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#uri ColabNotebookExecution#uri}
        :param generation: The version of the Cloud Storage object to read. If unset, the current version of the object is read. See https://cloud.google.com/storage/docs/metadata#generation-number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#generation ColabNotebookExecution#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd11ce3c5674d964247134857bcae79130cff8ba2698d2ceba686813cea8e708)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument generation", value=generation, expected_type=type_hints["generation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }
        if generation is not None:
            self._values["generation"] = generation

    @builtins.property
    def uri(self) -> builtins.str:
        '''The Cloud Storage uri pointing to the ipynb file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#uri ColabNotebookExecution#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''The version of the Cloud Storage object to read.

        If unset, the current version of the object is read. See https://cloud.google.com/storage/docs/metadata#generation-number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#generation ColabNotebookExecution#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColabNotebookExecutionGcsNotebookSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ColabNotebookExecutionGcsNotebookSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabNotebookExecution.ColabNotebookExecutionGcsNotebookSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9db02fe12bef8c2a082fa6eecc9262677b9c89f47f50f4150a68a4dbc6dcbcf6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGeneration")
    def reset_generation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeneration", []))

    @builtins.property
    @jsii.member(jsii_name="generationInput")
    def generation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "generationInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e9cb6958b7ace2488455628dc288f880bad5be5f9e486fa89b8ddce008d3f82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d910ef4c7e3f1165fb516d473c02ecd49b94a26c8d996129fee1bd8cde204556)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ColabNotebookExecutionGcsNotebookSource]:
        return typing.cast(typing.Optional[ColabNotebookExecutionGcsNotebookSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ColabNotebookExecutionGcsNotebookSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7849b522946627665fd569232025dd45c9e73f18a63a308949e916469c326fc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.colabNotebookExecution.ColabNotebookExecutionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class ColabNotebookExecutionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#create ColabNotebookExecution#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#delete ColabNotebookExecution#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a369f85acea3d899542cc12ecd494d4925b5da2109fd9cfef4793f681c25046a)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#create ColabNotebookExecution#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_notebook_execution#delete ColabNotebookExecution#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColabNotebookExecutionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ColabNotebookExecutionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabNotebookExecution.ColabNotebookExecutionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35d59ed0be9812e7ca8d2680cc9e5cd4075e7d633bfe04c1b0cff328d3366cd9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2615d4b2c367e91fe4dff50ac4ee714eceb0dd1b7371b91cb4b8ae27567bd35d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe45e6ccd17ff57f087b3e56c990cf3ffb748f89ea3da97a95028115687706c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ColabNotebookExecutionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ColabNotebookExecutionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ColabNotebookExecutionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1852b31b58f3808cb856aaeb9d3650011912740638c6ca62abfbedc24413063)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ColabNotebookExecution",
    "ColabNotebookExecutionConfig",
    "ColabNotebookExecutionDataformRepositorySource",
    "ColabNotebookExecutionDataformRepositorySourceOutputReference",
    "ColabNotebookExecutionDirectNotebookSource",
    "ColabNotebookExecutionDirectNotebookSourceOutputReference",
    "ColabNotebookExecutionGcsNotebookSource",
    "ColabNotebookExecutionGcsNotebookSourceOutputReference",
    "ColabNotebookExecutionTimeouts",
    "ColabNotebookExecutionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__78aced19506212f1d9ae05b87e83b1be8e73d0dd5e68211c647f12dd68b2e6b1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    gcs_output_uri: builtins.str,
    location: builtins.str,
    dataform_repository_source: typing.Optional[typing.Union[ColabNotebookExecutionDataformRepositorySource, typing.Dict[builtins.str, typing.Any]]] = None,
    direct_notebook_source: typing.Optional[typing.Union[ColabNotebookExecutionDirectNotebookSource, typing.Dict[builtins.str, typing.Any]]] = None,
    execution_timeout: typing.Optional[builtins.str] = None,
    execution_user: typing.Optional[builtins.str] = None,
    gcs_notebook_source: typing.Optional[typing.Union[ColabNotebookExecutionGcsNotebookSource, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    notebook_execution_job_id: typing.Optional[builtins.str] = None,
    notebook_runtime_template_resource_name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ColabNotebookExecutionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8e9651f7b15d05744edf7f0277c50f899e202e5cf382e52bc2faf88109c2afca(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30da227675d3adf03532d7107efe28bbee110908d077608cbdc52c2e5031b4ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c086223ad87e1e64bc2c3bcd2df3afe160fa5714f575cd26e2e9a90a2f871b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd7c261b7e4182c7241b83da35be722bc19c108b4a044b425bcee61f20503de5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f1aa06a97fbb169c8d92f49d2edf2233f1e6198d6792febb1f40e6bb6c60b39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37b5fb4da5159fa99a0a153fdc941ff008bf44d9fae3ed0aff42bc564dd8e999(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e67c149be0784200a16d36a66c1ecf77679065fc80ca8159650a5715da8756a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2c542390a40cc83132586b3e8839e446f0fa771403462ec4bbb1f9644e8667d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d26f275e9bb7d231d13886925239df672fd72fa83c0daf1dbe720a5ad216e0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4534bdac2bf1b193fc4530e5cdd96722339d127d4421bc2e7a4660a39c4bcf7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc1e111ef1a4a90247cb63249144c1555c5e0a3453f8291a67f8515ccc8eef48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__323e884aa371c15841c9899ef35be6539e0410e5ae6f340dbf03f641d40846bf(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    gcs_output_uri: builtins.str,
    location: builtins.str,
    dataform_repository_source: typing.Optional[typing.Union[ColabNotebookExecutionDataformRepositorySource, typing.Dict[builtins.str, typing.Any]]] = None,
    direct_notebook_source: typing.Optional[typing.Union[ColabNotebookExecutionDirectNotebookSource, typing.Dict[builtins.str, typing.Any]]] = None,
    execution_timeout: typing.Optional[builtins.str] = None,
    execution_user: typing.Optional[builtins.str] = None,
    gcs_notebook_source: typing.Optional[typing.Union[ColabNotebookExecutionGcsNotebookSource, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    notebook_execution_job_id: typing.Optional[builtins.str] = None,
    notebook_runtime_template_resource_name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ColabNotebookExecutionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2e3861fbbaf48396eb1e1b682d6bf11892af3a7bfde1ae6b4758f14f1a9c772(
    *,
    dataform_repository_resource_name: builtins.str,
    commit_sha: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe95ab2c0fb1f5c66c982ea5de13f97536fdaa2285f99264395809c99682c2b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c2e280006fcf6fca31e3c91d38b6133a81c47f6f5891cbc39ba9758022d29d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff4e7dc515815d28319823b73f21ac5345ec4939adb14fdaa6fb694b05e4fdcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fecdc0e4b677047175b5aef8ac4aff17255c0478a5fb5f396acbc6c3f26622d(
    value: typing.Optional[ColabNotebookExecutionDataformRepositorySource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__334d9ed4742a35125b26f44a82d8af471e20ab7a99749cd25123ca296eb2ee19(
    *,
    content: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225433320a1ea10e450b7d08c7121d7fe3bf175c029f2492fc472128fcce8312(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b50bdc399413732630b7d5c350cecfa9e9517bfe153c70532f6d743b6aa21e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b28b70b9afcd0bb0437feb6ddd3ceb23d86f107cada395ed8ce9fe314034ca7b(
    value: typing.Optional[ColabNotebookExecutionDirectNotebookSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd11ce3c5674d964247134857bcae79130cff8ba2698d2ceba686813cea8e708(
    *,
    uri: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9db02fe12bef8c2a082fa6eecc9262677b9c89f47f50f4150a68a4dbc6dcbcf6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e9cb6958b7ace2488455628dc288f880bad5be5f9e486fa89b8ddce008d3f82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d910ef4c7e3f1165fb516d473c02ecd49b94a26c8d996129fee1bd8cde204556(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7849b522946627665fd569232025dd45c9e73f18a63a308949e916469c326fc4(
    value: typing.Optional[ColabNotebookExecutionGcsNotebookSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a369f85acea3d899542cc12ecd494d4925b5da2109fd9cfef4793f681c25046a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35d59ed0be9812e7ca8d2680cc9e5cd4075e7d633bfe04c1b0cff328d3366cd9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2615d4b2c367e91fe4dff50ac4ee714eceb0dd1b7371b91cb4b8ae27567bd35d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe45e6ccd17ff57f087b3e56c990cf3ffb748f89ea3da97a95028115687706c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1852b31b58f3808cb856aaeb9d3650011912740638c6ca62abfbedc24413063(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ColabNotebookExecutionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
