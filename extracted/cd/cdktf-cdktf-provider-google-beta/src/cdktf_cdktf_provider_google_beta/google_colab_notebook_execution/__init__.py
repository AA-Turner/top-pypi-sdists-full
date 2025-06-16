r'''
# `google_colab_notebook_execution`

Refer to the Terraform Registry for docs: [`google_colab_notebook_execution`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution).
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


class GoogleColabNotebookExecution(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabNotebookExecution.GoogleColabNotebookExecution",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution google_colab_notebook_execution}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        gcs_output_uri: builtins.str,
        location: builtins.str,
        dataform_repository_source: typing.Optional[typing.Union["GoogleColabNotebookExecutionDataformRepositorySource", typing.Dict[builtins.str, typing.Any]]] = None,
        direct_notebook_source: typing.Optional[typing.Union["GoogleColabNotebookExecutionDirectNotebookSource", typing.Dict[builtins.str, typing.Any]]] = None,
        execution_timeout: typing.Optional[builtins.str] = None,
        execution_user: typing.Optional[builtins.str] = None,
        gcs_notebook_source: typing.Optional[typing.Union["GoogleColabNotebookExecutionGcsNotebookSource", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        notebook_execution_job_id: typing.Optional[builtins.str] = None,
        notebook_runtime_template_resource_name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleColabNotebookExecutionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution google_colab_notebook_execution} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: Required. The display name of the Notebook Execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#display_name GoogleColabNotebookExecution#display_name}
        :param gcs_output_uri: The Cloud Storage location to upload the result to. Format:'gs://bucket-name'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#gcs_output_uri GoogleColabNotebookExecution#gcs_output_uri}
        :param location: The location for the resource: https://cloud.google.com/colab/docs/locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#location GoogleColabNotebookExecution#location}
        :param dataform_repository_source: dataform_repository_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#dataform_repository_source GoogleColabNotebookExecution#dataform_repository_source}
        :param direct_notebook_source: direct_notebook_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#direct_notebook_source GoogleColabNotebookExecution#direct_notebook_source}
        :param execution_timeout: Max running time of the execution job in seconds (default 86400s / 24 hrs). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#execution_timeout GoogleColabNotebookExecution#execution_timeout}
        :param execution_user: The user email to run the execution as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#execution_user GoogleColabNotebookExecution#execution_user}
        :param gcs_notebook_source: gcs_notebook_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#gcs_notebook_source GoogleColabNotebookExecution#gcs_notebook_source}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#id GoogleColabNotebookExecution#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notebook_execution_job_id: User specified ID for the Notebook Execution Job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#notebook_execution_job_id GoogleColabNotebookExecution#notebook_execution_job_id}
        :param notebook_runtime_template_resource_name: The NotebookRuntimeTemplate to source compute configuration from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#notebook_runtime_template_resource_name GoogleColabNotebookExecution#notebook_runtime_template_resource_name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#project GoogleColabNotebookExecution#project}.
        :param service_account: The service account to run the execution as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#service_account GoogleColabNotebookExecution#service_account}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#timeouts GoogleColabNotebookExecution#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6759acaeee6bddb3e8e012c848362d97e927b9bd8b7227b09f45a5cc5675db3f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleColabNotebookExecutionConfig(
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
        '''Generates CDKTF code for importing a GoogleColabNotebookExecution resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleColabNotebookExecution to import.
        :param import_from_id: The id of the existing GoogleColabNotebookExecution that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleColabNotebookExecution to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5f811d3aa53b24c4e24b46d46dc9c0ed31549e2b91fa48726109f41f28fab04)
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
        :param dataform_repository_resource_name: The resource name of the Dataform Repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#dataform_repository_resource_name GoogleColabNotebookExecution#dataform_repository_resource_name}
        :param commit_sha: The commit SHA to read repository with. If unset, the file will be read at HEAD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#commit_sha GoogleColabNotebookExecution#commit_sha}
        '''
        value = GoogleColabNotebookExecutionDataformRepositorySource(
            dataform_repository_resource_name=dataform_repository_resource_name,
            commit_sha=commit_sha,
        )

        return typing.cast(None, jsii.invoke(self, "putDataformRepositorySource", [value]))

    @jsii.member(jsii_name="putDirectNotebookSource")
    def put_direct_notebook_source(self, *, content: builtins.str) -> None:
        '''
        :param content: The base64-encoded contents of the input notebook file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#content GoogleColabNotebookExecution#content}
        '''
        value = GoogleColabNotebookExecutionDirectNotebookSource(content=content)

        return typing.cast(None, jsii.invoke(self, "putDirectNotebookSource", [value]))

    @jsii.member(jsii_name="putGcsNotebookSource")
    def put_gcs_notebook_source(
        self,
        *,
        uri: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: The Cloud Storage uri pointing to the ipynb file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#uri GoogleColabNotebookExecution#uri}
        :param generation: The version of the Cloud Storage object to read. If unset, the current version of the object is read. See https://cloud.google.com/storage/docs/metadata#generation-number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#generation GoogleColabNotebookExecution#generation}
        '''
        value = GoogleColabNotebookExecutionGcsNotebookSource(
            uri=uri, generation=generation
        )

        return typing.cast(None, jsii.invoke(self, "putGcsNotebookSource", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#create GoogleColabNotebookExecution#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#delete GoogleColabNotebookExecution#delete}.
        '''
        value = GoogleColabNotebookExecutionTimeouts(create=create, delete=delete)

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
    ) -> "GoogleColabNotebookExecutionDataformRepositorySourceOutputReference":
        return typing.cast("GoogleColabNotebookExecutionDataformRepositorySourceOutputReference", jsii.get(self, "dataformRepositorySource"))

    @builtins.property
    @jsii.member(jsii_name="directNotebookSource")
    def direct_notebook_source(
        self,
    ) -> "GoogleColabNotebookExecutionDirectNotebookSourceOutputReference":
        return typing.cast("GoogleColabNotebookExecutionDirectNotebookSourceOutputReference", jsii.get(self, "directNotebookSource"))

    @builtins.property
    @jsii.member(jsii_name="gcsNotebookSource")
    def gcs_notebook_source(
        self,
    ) -> "GoogleColabNotebookExecutionGcsNotebookSourceOutputReference":
        return typing.cast("GoogleColabNotebookExecutionGcsNotebookSourceOutputReference", jsii.get(self, "gcsNotebookSource"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleColabNotebookExecutionTimeoutsOutputReference":
        return typing.cast("GoogleColabNotebookExecutionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="dataformRepositorySourceInput")
    def dataform_repository_source_input(
        self,
    ) -> typing.Optional["GoogleColabNotebookExecutionDataformRepositorySource"]:
        return typing.cast(typing.Optional["GoogleColabNotebookExecutionDataformRepositorySource"], jsii.get(self, "dataformRepositorySourceInput"))

    @builtins.property
    @jsii.member(jsii_name="directNotebookSourceInput")
    def direct_notebook_source_input(
        self,
    ) -> typing.Optional["GoogleColabNotebookExecutionDirectNotebookSource"]:
        return typing.cast(typing.Optional["GoogleColabNotebookExecutionDirectNotebookSource"], jsii.get(self, "directNotebookSourceInput"))

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
    ) -> typing.Optional["GoogleColabNotebookExecutionGcsNotebookSource"]:
        return typing.cast(typing.Optional["GoogleColabNotebookExecutionGcsNotebookSource"], jsii.get(self, "gcsNotebookSourceInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleColabNotebookExecutionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleColabNotebookExecutionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c039801e10712ebe30e8e06feb052b38047f65de70185be56840a3854af2cce6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionTimeout")
    def execution_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionTimeout"))

    @execution_timeout.setter
    def execution_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ac93ce6102524b54d45bad96d6f2d945d2c1435a1d48dce0044667f552362dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionUser")
    def execution_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionUser"))

    @execution_user.setter
    def execution_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d58086719b4600ffd49131579d0208edcbc0ed6396870403157caad2eaf4b68a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gcsOutputUri")
    def gcs_output_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcsOutputUri"))

    @gcs_output_uri.setter
    def gcs_output_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c4364862e36e2cbebad9038c809ef9e3152c14737a6fa2bdd7d680b35098764)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcsOutputUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1035e9318e7da81b2b3a2b027bcfdfd34a9d0d95374a9df9d263238cc8be803f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c7bb664bced1c7dd9aa60452e64eae547ab839909da6ac6c890b3694943c9fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notebookExecutionJobId")
    def notebook_execution_job_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notebookExecutionJobId"))

    @notebook_execution_job_id.setter
    def notebook_execution_job_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62dd0b43a9c8e121f4891c44ec5c3d3960e04e223a48b96b53b17f2e06ecc089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notebookExecutionJobId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notebookRuntimeTemplateResourceName")
    def notebook_runtime_template_resource_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notebookRuntimeTemplateResourceName"))

    @notebook_runtime_template_resource_name.setter
    def notebook_runtime_template_resource_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5414cbeda95b103a702d72d602fcebf1ccdc5df8d2704da656daa7b1db25e21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notebookRuntimeTemplateResourceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f354537ee2791665b1bc041bd8239b19d9d761fbfd4c7f12e4a61191c5ac7b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6125408992dd6c8925182742a8fd6b09d6af3ec9d6914dfa1b264ec939aa2914)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleColabNotebookExecution.GoogleColabNotebookExecutionConfig",
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
class GoogleColabNotebookExecutionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        dataform_repository_source: typing.Optional[typing.Union["GoogleColabNotebookExecutionDataformRepositorySource", typing.Dict[builtins.str, typing.Any]]] = None,
        direct_notebook_source: typing.Optional[typing.Union["GoogleColabNotebookExecutionDirectNotebookSource", typing.Dict[builtins.str, typing.Any]]] = None,
        execution_timeout: typing.Optional[builtins.str] = None,
        execution_user: typing.Optional[builtins.str] = None,
        gcs_notebook_source: typing.Optional[typing.Union["GoogleColabNotebookExecutionGcsNotebookSource", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        notebook_execution_job_id: typing.Optional[builtins.str] = None,
        notebook_runtime_template_resource_name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleColabNotebookExecutionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: Required. The display name of the Notebook Execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#display_name GoogleColabNotebookExecution#display_name}
        :param gcs_output_uri: The Cloud Storage location to upload the result to. Format:'gs://bucket-name'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#gcs_output_uri GoogleColabNotebookExecution#gcs_output_uri}
        :param location: The location for the resource: https://cloud.google.com/colab/docs/locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#location GoogleColabNotebookExecution#location}
        :param dataform_repository_source: dataform_repository_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#dataform_repository_source GoogleColabNotebookExecution#dataform_repository_source}
        :param direct_notebook_source: direct_notebook_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#direct_notebook_source GoogleColabNotebookExecution#direct_notebook_source}
        :param execution_timeout: Max running time of the execution job in seconds (default 86400s / 24 hrs). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#execution_timeout GoogleColabNotebookExecution#execution_timeout}
        :param execution_user: The user email to run the execution as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#execution_user GoogleColabNotebookExecution#execution_user}
        :param gcs_notebook_source: gcs_notebook_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#gcs_notebook_source GoogleColabNotebookExecution#gcs_notebook_source}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#id GoogleColabNotebookExecution#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notebook_execution_job_id: User specified ID for the Notebook Execution Job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#notebook_execution_job_id GoogleColabNotebookExecution#notebook_execution_job_id}
        :param notebook_runtime_template_resource_name: The NotebookRuntimeTemplate to source compute configuration from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#notebook_runtime_template_resource_name GoogleColabNotebookExecution#notebook_runtime_template_resource_name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#project GoogleColabNotebookExecution#project}.
        :param service_account: The service account to run the execution as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#service_account GoogleColabNotebookExecution#service_account}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#timeouts GoogleColabNotebookExecution#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(dataform_repository_source, dict):
            dataform_repository_source = GoogleColabNotebookExecutionDataformRepositorySource(**dataform_repository_source)
        if isinstance(direct_notebook_source, dict):
            direct_notebook_source = GoogleColabNotebookExecutionDirectNotebookSource(**direct_notebook_source)
        if isinstance(gcs_notebook_source, dict):
            gcs_notebook_source = GoogleColabNotebookExecutionGcsNotebookSource(**gcs_notebook_source)
        if isinstance(timeouts, dict):
            timeouts = GoogleColabNotebookExecutionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aceb5ba818b2a07d94c98706554e5f104e6aa5a5d005e48ac2f45dea54611e33)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#display_name GoogleColabNotebookExecution#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gcs_output_uri(self) -> builtins.str:
        '''The Cloud Storage location to upload the result to. Format:'gs://bucket-name'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#gcs_output_uri GoogleColabNotebookExecution#gcs_output_uri}
        '''
        result = self._values.get("gcs_output_uri")
        assert result is not None, "Required property 'gcs_output_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource: https://cloud.google.com/colab/docs/locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#location GoogleColabNotebookExecution#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dataform_repository_source(
        self,
    ) -> typing.Optional["GoogleColabNotebookExecutionDataformRepositorySource"]:
        '''dataform_repository_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#dataform_repository_source GoogleColabNotebookExecution#dataform_repository_source}
        '''
        result = self._values.get("dataform_repository_source")
        return typing.cast(typing.Optional["GoogleColabNotebookExecutionDataformRepositorySource"], result)

    @builtins.property
    def direct_notebook_source(
        self,
    ) -> typing.Optional["GoogleColabNotebookExecutionDirectNotebookSource"]:
        '''direct_notebook_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#direct_notebook_source GoogleColabNotebookExecution#direct_notebook_source}
        '''
        result = self._values.get("direct_notebook_source")
        return typing.cast(typing.Optional["GoogleColabNotebookExecutionDirectNotebookSource"], result)

    @builtins.property
    def execution_timeout(self) -> typing.Optional[builtins.str]:
        '''Max running time of the execution job in seconds (default 86400s / 24 hrs).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#execution_timeout GoogleColabNotebookExecution#execution_timeout}
        '''
        result = self._values.get("execution_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_user(self) -> typing.Optional[builtins.str]:
        '''The user email to run the execution as.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#execution_user GoogleColabNotebookExecution#execution_user}
        '''
        result = self._values.get("execution_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcs_notebook_source(
        self,
    ) -> typing.Optional["GoogleColabNotebookExecutionGcsNotebookSource"]:
        '''gcs_notebook_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#gcs_notebook_source GoogleColabNotebookExecution#gcs_notebook_source}
        '''
        result = self._values.get("gcs_notebook_source")
        return typing.cast(typing.Optional["GoogleColabNotebookExecutionGcsNotebookSource"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#id GoogleColabNotebookExecution#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notebook_execution_job_id(self) -> typing.Optional[builtins.str]:
        '''User specified ID for the Notebook Execution Job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#notebook_execution_job_id GoogleColabNotebookExecution#notebook_execution_job_id}
        '''
        result = self._values.get("notebook_execution_job_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notebook_runtime_template_resource_name(self) -> typing.Optional[builtins.str]:
        '''The NotebookRuntimeTemplate to source compute configuration from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#notebook_runtime_template_resource_name GoogleColabNotebookExecution#notebook_runtime_template_resource_name}
        '''
        result = self._values.get("notebook_runtime_template_resource_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#project GoogleColabNotebookExecution#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''The service account to run the execution as.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#service_account GoogleColabNotebookExecution#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleColabNotebookExecutionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#timeouts GoogleColabNotebookExecution#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleColabNotebookExecutionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleColabNotebookExecutionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleColabNotebookExecution.GoogleColabNotebookExecutionDataformRepositorySource",
    jsii_struct_bases=[],
    name_mapping={
        "dataform_repository_resource_name": "dataformRepositoryResourceName",
        "commit_sha": "commitSha",
    },
)
class GoogleColabNotebookExecutionDataformRepositorySource:
    def __init__(
        self,
        *,
        dataform_repository_resource_name: builtins.str,
        commit_sha: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataform_repository_resource_name: The resource name of the Dataform Repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#dataform_repository_resource_name GoogleColabNotebookExecution#dataform_repository_resource_name}
        :param commit_sha: The commit SHA to read repository with. If unset, the file will be read at HEAD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#commit_sha GoogleColabNotebookExecution#commit_sha}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51b658d9b67cf4944034d25a6e238b2be57fd48694c70303d24da1bfe6e981e3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#dataform_repository_resource_name GoogleColabNotebookExecution#dataform_repository_resource_name}
        '''
        result = self._values.get("dataform_repository_resource_name")
        assert result is not None, "Required property 'dataform_repository_resource_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def commit_sha(self) -> typing.Optional[builtins.str]:
        '''The commit SHA to read repository with. If unset, the file will be read at HEAD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#commit_sha GoogleColabNotebookExecution#commit_sha}
        '''
        result = self._values.get("commit_sha")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleColabNotebookExecutionDataformRepositorySource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleColabNotebookExecutionDataformRepositorySourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabNotebookExecution.GoogleColabNotebookExecutionDataformRepositorySourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebceb535725e94072688637fb4d60d3d21cb2c3d893c57ede5b433d6ca6931f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__13e4217ec17e509f60e597a45444202fefd9fb84c9437df6fecec8b834ead90d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitSha", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataformRepositoryResourceName")
    def dataform_repository_resource_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataformRepositoryResourceName"))

    @dataform_repository_resource_name.setter
    def dataform_repository_resource_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c31c91823313d5a67f1a0fb55145b2dc64964bcb9b7637e87929a767be47293)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataformRepositoryResourceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleColabNotebookExecutionDataformRepositorySource]:
        return typing.cast(typing.Optional[GoogleColabNotebookExecutionDataformRepositorySource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleColabNotebookExecutionDataformRepositorySource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd780338acc105ac7ad2c3c57c480c1d84410233bfa10445f95728d7cfdacd68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleColabNotebookExecution.GoogleColabNotebookExecutionDirectNotebookSource",
    jsii_struct_bases=[],
    name_mapping={"content": "content"},
)
class GoogleColabNotebookExecutionDirectNotebookSource:
    def __init__(self, *, content: builtins.str) -> None:
        '''
        :param content: The base64-encoded contents of the input notebook file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#content GoogleColabNotebookExecution#content}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3bd2bd220d8055dbccc38e19a84f44fc36f179cdcf53425181faf84c7551eda)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
        }

    @builtins.property
    def content(self) -> builtins.str:
        '''The base64-encoded contents of the input notebook file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#content GoogleColabNotebookExecution#content}
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleColabNotebookExecutionDirectNotebookSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleColabNotebookExecutionDirectNotebookSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabNotebookExecution.GoogleColabNotebookExecutionDirectNotebookSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad8366577d0b052eb846ec4089fb8380a47da9522ba7645deb10fb5abba3cdec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3081e9d2bfe59bc9cfd5abba289da9244fe29af4e9e8ba34d1883a8a84f65458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleColabNotebookExecutionDirectNotebookSource]:
        return typing.cast(typing.Optional[GoogleColabNotebookExecutionDirectNotebookSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleColabNotebookExecutionDirectNotebookSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67f257d2af7be9aa1e5a36bf8ce58358880cbab7c9a3f5243c5e09b8474bc2d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleColabNotebookExecution.GoogleColabNotebookExecutionGcsNotebookSource",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "generation": "generation"},
)
class GoogleColabNotebookExecutionGcsNotebookSource:
    def __init__(
        self,
        *,
        uri: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: The Cloud Storage uri pointing to the ipynb file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#uri GoogleColabNotebookExecution#uri}
        :param generation: The version of the Cloud Storage object to read. If unset, the current version of the object is read. See https://cloud.google.com/storage/docs/metadata#generation-number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#generation GoogleColabNotebookExecution#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94e6cb27364e89711e74d5bce12cc5f5f6b0651b87cbf39a1564ed09ba938f66)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#uri GoogleColabNotebookExecution#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''The version of the Cloud Storage object to read.

        If unset, the current version of the object is read. See https://cloud.google.com/storage/docs/metadata#generation-number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#generation GoogleColabNotebookExecution#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleColabNotebookExecutionGcsNotebookSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleColabNotebookExecutionGcsNotebookSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabNotebookExecution.GoogleColabNotebookExecutionGcsNotebookSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9d744e9499fb0471885251413ab9cd1e0fc29a0e85c343e20d7c153bfb8d262)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b01c284b06fc343ffe3803317da9482edcd80b186faa32e1c248a60a17819594)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bca889d996bacd3719fea0dff942cae82a957010aed72ab50a18c107b2443f23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleColabNotebookExecutionGcsNotebookSource]:
        return typing.cast(typing.Optional[GoogleColabNotebookExecutionGcsNotebookSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleColabNotebookExecutionGcsNotebookSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddf7327cbf89c407c6bb5f4a257ae626f6d6a944541c961e8aae9eda24d14cbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleColabNotebookExecution.GoogleColabNotebookExecutionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class GoogleColabNotebookExecutionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#create GoogleColabNotebookExecution#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#delete GoogleColabNotebookExecution#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__513d2dccc2547d663f57726020f59ff6db0d79d7ad36a01dd2bc9eb949fe1cf5)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#create GoogleColabNotebookExecution#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_notebook_execution#delete GoogleColabNotebookExecution#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleColabNotebookExecutionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleColabNotebookExecutionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabNotebookExecution.GoogleColabNotebookExecutionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d581e6a1ad568b94de9b8b06ca22985e0ac2d50d22af1723343026cfbc4f9fab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e0cfc9372243e98433b77f89d772b1268feb14309c2603c314ecc1e22893a03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9d2bc0542452b4ef635185c562727d8c35bd2d7cc0dd534e7538d09805a0db6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleColabNotebookExecutionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleColabNotebookExecutionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleColabNotebookExecutionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c047ae61abc594dcaf19a137f1934585ae968442f568c4c07dda2422b10ba0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleColabNotebookExecution",
    "GoogleColabNotebookExecutionConfig",
    "GoogleColabNotebookExecutionDataformRepositorySource",
    "GoogleColabNotebookExecutionDataformRepositorySourceOutputReference",
    "GoogleColabNotebookExecutionDirectNotebookSource",
    "GoogleColabNotebookExecutionDirectNotebookSourceOutputReference",
    "GoogleColabNotebookExecutionGcsNotebookSource",
    "GoogleColabNotebookExecutionGcsNotebookSourceOutputReference",
    "GoogleColabNotebookExecutionTimeouts",
    "GoogleColabNotebookExecutionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__6759acaeee6bddb3e8e012c848362d97e927b9bd8b7227b09f45a5cc5675db3f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    gcs_output_uri: builtins.str,
    location: builtins.str,
    dataform_repository_source: typing.Optional[typing.Union[GoogleColabNotebookExecutionDataformRepositorySource, typing.Dict[builtins.str, typing.Any]]] = None,
    direct_notebook_source: typing.Optional[typing.Union[GoogleColabNotebookExecutionDirectNotebookSource, typing.Dict[builtins.str, typing.Any]]] = None,
    execution_timeout: typing.Optional[builtins.str] = None,
    execution_user: typing.Optional[builtins.str] = None,
    gcs_notebook_source: typing.Optional[typing.Union[GoogleColabNotebookExecutionGcsNotebookSource, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    notebook_execution_job_id: typing.Optional[builtins.str] = None,
    notebook_runtime_template_resource_name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleColabNotebookExecutionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f5f811d3aa53b24c4e24b46d46dc9c0ed31549e2b91fa48726109f41f28fab04(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c039801e10712ebe30e8e06feb052b38047f65de70185be56840a3854af2cce6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ac93ce6102524b54d45bad96d6f2d945d2c1435a1d48dce0044667f552362dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58086719b4600ffd49131579d0208edcbc0ed6396870403157caad2eaf4b68a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4364862e36e2cbebad9038c809ef9e3152c14737a6fa2bdd7d680b35098764(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1035e9318e7da81b2b3a2b027bcfdfd34a9d0d95374a9df9d263238cc8be803f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c7bb664bced1c7dd9aa60452e64eae547ab839909da6ac6c890b3694943c9fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62dd0b43a9c8e121f4891c44ec5c3d3960e04e223a48b96b53b17f2e06ecc089(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5414cbeda95b103a702d72d602fcebf1ccdc5df8d2704da656daa7b1db25e21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f354537ee2791665b1bc041bd8239b19d9d761fbfd4c7f12e4a61191c5ac7b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6125408992dd6c8925182742a8fd6b09d6af3ec9d6914dfa1b264ec939aa2914(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aceb5ba818b2a07d94c98706554e5f104e6aa5a5d005e48ac2f45dea54611e33(
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
    dataform_repository_source: typing.Optional[typing.Union[GoogleColabNotebookExecutionDataformRepositorySource, typing.Dict[builtins.str, typing.Any]]] = None,
    direct_notebook_source: typing.Optional[typing.Union[GoogleColabNotebookExecutionDirectNotebookSource, typing.Dict[builtins.str, typing.Any]]] = None,
    execution_timeout: typing.Optional[builtins.str] = None,
    execution_user: typing.Optional[builtins.str] = None,
    gcs_notebook_source: typing.Optional[typing.Union[GoogleColabNotebookExecutionGcsNotebookSource, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    notebook_execution_job_id: typing.Optional[builtins.str] = None,
    notebook_runtime_template_resource_name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleColabNotebookExecutionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51b658d9b67cf4944034d25a6e238b2be57fd48694c70303d24da1bfe6e981e3(
    *,
    dataform_repository_resource_name: builtins.str,
    commit_sha: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebceb535725e94072688637fb4d60d3d21cb2c3d893c57ede5b433d6ca6931f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e4217ec17e509f60e597a45444202fefd9fb84c9437df6fecec8b834ead90d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c31c91823313d5a67f1a0fb55145b2dc64964bcb9b7637e87929a767be47293(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd780338acc105ac7ad2c3c57c480c1d84410233bfa10445f95728d7cfdacd68(
    value: typing.Optional[GoogleColabNotebookExecutionDataformRepositorySource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3bd2bd220d8055dbccc38e19a84f44fc36f179cdcf53425181faf84c7551eda(
    *,
    content: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad8366577d0b052eb846ec4089fb8380a47da9522ba7645deb10fb5abba3cdec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3081e9d2bfe59bc9cfd5abba289da9244fe29af4e9e8ba34d1883a8a84f65458(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67f257d2af7be9aa1e5a36bf8ce58358880cbab7c9a3f5243c5e09b8474bc2d0(
    value: typing.Optional[GoogleColabNotebookExecutionDirectNotebookSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94e6cb27364e89711e74d5bce12cc5f5f6b0651b87cbf39a1564ed09ba938f66(
    *,
    uri: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9d744e9499fb0471885251413ab9cd1e0fc29a0e85c343e20d7c153bfb8d262(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b01c284b06fc343ffe3803317da9482edcd80b186faa32e1c248a60a17819594(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bca889d996bacd3719fea0dff942cae82a957010aed72ab50a18c107b2443f23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddf7327cbf89c407c6bb5f4a257ae626f6d6a944541c961e8aae9eda24d14cbe(
    value: typing.Optional[GoogleColabNotebookExecutionGcsNotebookSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__513d2dccc2547d663f57726020f59ff6db0d79d7ad36a01dd2bc9eb949fe1cf5(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d581e6a1ad568b94de9b8b06ca22985e0ac2d50d22af1723343026cfbc4f9fab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0cfc9372243e98433b77f89d772b1268feb14309c2603c314ecc1e22893a03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9d2bc0542452b4ef635185c562727d8c35bd2d7cc0dd534e7538d09805a0db6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c047ae61abc594dcaf19a137f1934585ae968442f568c4c07dda2422b10ba0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleColabNotebookExecutionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
