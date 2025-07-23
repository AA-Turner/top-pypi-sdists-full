r'''
# `google_dataproc_workflow_template`

Refer to the Terraform Registry for docs: [`google_dataproc_workflow_template`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template).
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


class DataprocWorkflowTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template google_dataproc_workflow_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        jobs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataprocWorkflowTemplateJobs", typing.Dict[builtins.str, typing.Any]]]],
        location: builtins.str,
        name: builtins.str,
        placement: typing.Union["DataprocWorkflowTemplatePlacement", typing.Dict[builtins.str, typing.Any]],
        dag_timeout: typing.Optional[builtins.str] = None,
        encryption_config: typing.Optional[typing.Union["DataprocWorkflowTemplateEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataprocWorkflowTemplateParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataprocWorkflowTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template google_dataproc_workflow_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param jobs: jobs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#jobs DataprocWorkflowTemplate#jobs}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#location DataprocWorkflowTemplate#location}
        :param name: Output only. The resource name of the workflow template, as described in https://cloud.google.com/apis/design/resource_names. * For ``projects.regions.workflowTemplates``, the resource name of the template has the following format: ``projects/{project_id}/regions/{region}/workflowTemplates/{template_id}`` * For ``projects.locations.workflowTemplates``, the resource name of the template has the following format: ``projects/{project_id}/locations/{location}/workflowTemplates/{template_id}`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#name DataprocWorkflowTemplate#name}
        :param placement: placement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#placement DataprocWorkflowTemplate#placement}
        :param dag_timeout: Optional. Timeout duration for the DAG of jobs, expressed in seconds (see `JSON representation of duration <https://developers.google.com/protocol-buffers/docs/proto3#json>`_). The timeout duration must be from 10 minutes ("600s") to 24 hours ("86400s"). The timer begins when the first job is submitted. If the workflow is running at the end of the timeout period, any remaining jobs are cancelled, the workflow is ended, and if the workflow was running on a `managed cluster </dataproc/docs/concepts/workflows/using-workflows#configuring_or_selecting_a_cluster>`_, the cluster is deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#dag_timeout DataprocWorkflowTemplate#dag_timeout}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#encryption_config DataprocWorkflowTemplate#encryption_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#id DataprocWorkflowTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. The labels to associate with this template. These labels will be propagated to all jobs and clusters created by the workflow instance. Label **keys** must contain 1 to 63 characters, and must conform to `RFC 1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. Label **values** may be empty, but, if present, must contain 1 to 63 characters, and must conform to `RFC 1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. No more than 32 labels can be associated with a template. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field ``effective_labels`` for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#labels DataprocWorkflowTemplate#labels}
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#parameters DataprocWorkflowTemplate#parameters}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#project DataprocWorkflowTemplate#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#timeouts DataprocWorkflowTemplate#timeouts}
        :param version: Output only. The current version of this workflow template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#version DataprocWorkflowTemplate#version}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9830cc9f26a89586c2c6b6abe4442c509d35f14cc92942a386cf1f41201434b8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataprocWorkflowTemplateConfig(
            jobs=jobs,
            location=location,
            name=name,
            placement=placement,
            dag_timeout=dag_timeout,
            encryption_config=encryption_config,
            id=id,
            labels=labels,
            parameters=parameters,
            project=project,
            timeouts=timeouts,
            version=version,
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
        '''Generates CDKTF code for importing a DataprocWorkflowTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataprocWorkflowTemplate to import.
        :param import_from_id: The id of the existing DataprocWorkflowTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataprocWorkflowTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f985950335ab131271164edc200e9112b7c74216e9e2cadfca0b93a64c758bb4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEncryptionConfig")
    def put_encryption_config(
        self,
        *,
        kms_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key: Optional. The Cloud KMS key name to use for encryption. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#kms_key DataprocWorkflowTemplate#kms_key}
        '''
        value = DataprocWorkflowTemplateEncryptionConfig(kms_key=kms_key)

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfig", [value]))

    @jsii.member(jsii_name="putJobs")
    def put_jobs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataprocWorkflowTemplateJobs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b8382b5345d5a741523c60fa964aa30313cc3086e45adc21eb9c159ca54b25f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putJobs", [value]))

    @jsii.member(jsii_name="putParameters")
    def put_parameters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataprocWorkflowTemplateParameters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ae39eb98d79839d93bf02d68e83aeeeb8c531a070340a3bc509dae82ab0f0b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParameters", [value]))

    @jsii.member(jsii_name="putPlacement")
    def put_placement(
        self,
        *,
        cluster_selector: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementClusterSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_cluster: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementManagedCluster", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cluster_selector: cluster_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#cluster_selector DataprocWorkflowTemplate#cluster_selector}
        :param managed_cluster: managed_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#managed_cluster DataprocWorkflowTemplate#managed_cluster}
        '''
        value = DataprocWorkflowTemplatePlacement(
            cluster_selector=cluster_selector, managed_cluster=managed_cluster
        )

        return typing.cast(None, jsii.invoke(self, "putPlacement", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#create DataprocWorkflowTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#delete DataprocWorkflowTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#update DataprocWorkflowTemplate#update}.
        '''
        value = DataprocWorkflowTemplateTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDagTimeout")
    def reset_dag_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDagTimeout", []))

    @jsii.member(jsii_name="resetEncryptionConfig")
    def reset_encryption_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

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
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfig")
    def encryption_config(
        self,
    ) -> "DataprocWorkflowTemplateEncryptionConfigOutputReference":
        return typing.cast("DataprocWorkflowTemplateEncryptionConfigOutputReference", jsii.get(self, "encryptionConfig"))

    @builtins.property
    @jsii.member(jsii_name="jobs")
    def jobs(self) -> "DataprocWorkflowTemplateJobsList":
        return typing.cast("DataprocWorkflowTemplateJobsList", jsii.get(self, "jobs"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> "DataprocWorkflowTemplateParametersList":
        return typing.cast("DataprocWorkflowTemplateParametersList", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="placement")
    def placement(self) -> "DataprocWorkflowTemplatePlacementOutputReference":
        return typing.cast("DataprocWorkflowTemplatePlacementOutputReference", jsii.get(self, "placement"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataprocWorkflowTemplateTimeoutsOutputReference":
        return typing.cast("DataprocWorkflowTemplateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="dagTimeoutInput")
    def dag_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dagTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigInput")
    def encryption_config_input(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateEncryptionConfig"]:
        return typing.cast(typing.Optional["DataprocWorkflowTemplateEncryptionConfig"], jsii.get(self, "encryptionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="jobsInput")
    def jobs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocWorkflowTemplateJobs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocWorkflowTemplateJobs"]]], jsii.get(self, "jobsInput"))

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
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocWorkflowTemplateParameters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocWorkflowTemplateParameters"]]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="placementInput")
    def placement_input(self) -> typing.Optional["DataprocWorkflowTemplatePlacement"]:
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacement"], jsii.get(self, "placementInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataprocWorkflowTemplateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataprocWorkflowTemplateTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="dagTimeout")
    def dag_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dagTimeout"))

    @dag_timeout.setter
    def dag_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5610ad25355a5fb2dbac7af1674896e0232a13e70ec8ca81616e9efdfecfeb6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dagTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0a15632f88ff9973bd18afc8188aafacfbecb46148f17028be1b9751e74a2e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22ce9dcab23c03a5aaf4daa0425d19474835b66116621702190b5ec1035132c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e869f89d1322c38e727892a4455afb8847631531f90f94c111c4275cd863f905)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4480355dcf97e700c09636e3c4c817e43489569e1a76a1057ec2d42d5d6237e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e20168a74ab2570d6975144af96d7c0df997f1d0defa59302004e60b3117280b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "version"))

    @version.setter
    def version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb7814abbbc35bff2cd6446d9633551989a46bab30eed5939f66ee7d190d72d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "jobs": "jobs",
        "location": "location",
        "name": "name",
        "placement": "placement",
        "dag_timeout": "dagTimeout",
        "encryption_config": "encryptionConfig",
        "id": "id",
        "labels": "labels",
        "parameters": "parameters",
        "project": "project",
        "timeouts": "timeouts",
        "version": "version",
    },
)
class DataprocWorkflowTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        jobs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataprocWorkflowTemplateJobs", typing.Dict[builtins.str, typing.Any]]]],
        location: builtins.str,
        name: builtins.str,
        placement: typing.Union["DataprocWorkflowTemplatePlacement", typing.Dict[builtins.str, typing.Any]],
        dag_timeout: typing.Optional[builtins.str] = None,
        encryption_config: typing.Optional[typing.Union["DataprocWorkflowTemplateEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataprocWorkflowTemplateParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataprocWorkflowTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param jobs: jobs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#jobs DataprocWorkflowTemplate#jobs}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#location DataprocWorkflowTemplate#location}
        :param name: Output only. The resource name of the workflow template, as described in https://cloud.google.com/apis/design/resource_names. * For ``projects.regions.workflowTemplates``, the resource name of the template has the following format: ``projects/{project_id}/regions/{region}/workflowTemplates/{template_id}`` * For ``projects.locations.workflowTemplates``, the resource name of the template has the following format: ``projects/{project_id}/locations/{location}/workflowTemplates/{template_id}`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#name DataprocWorkflowTemplate#name}
        :param placement: placement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#placement DataprocWorkflowTemplate#placement}
        :param dag_timeout: Optional. Timeout duration for the DAG of jobs, expressed in seconds (see `JSON representation of duration <https://developers.google.com/protocol-buffers/docs/proto3#json>`_). The timeout duration must be from 10 minutes ("600s") to 24 hours ("86400s"). The timer begins when the first job is submitted. If the workflow is running at the end of the timeout period, any remaining jobs are cancelled, the workflow is ended, and if the workflow was running on a `managed cluster </dataproc/docs/concepts/workflows/using-workflows#configuring_or_selecting_a_cluster>`_, the cluster is deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#dag_timeout DataprocWorkflowTemplate#dag_timeout}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#encryption_config DataprocWorkflowTemplate#encryption_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#id DataprocWorkflowTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. The labels to associate with this template. These labels will be propagated to all jobs and clusters created by the workflow instance. Label **keys** must contain 1 to 63 characters, and must conform to `RFC 1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. Label **values** may be empty, but, if present, must contain 1 to 63 characters, and must conform to `RFC 1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. No more than 32 labels can be associated with a template. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field ``effective_labels`` for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#labels DataprocWorkflowTemplate#labels}
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#parameters DataprocWorkflowTemplate#parameters}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#project DataprocWorkflowTemplate#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#timeouts DataprocWorkflowTemplate#timeouts}
        :param version: Output only. The current version of this workflow template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#version DataprocWorkflowTemplate#version}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(placement, dict):
            placement = DataprocWorkflowTemplatePlacement(**placement)
        if isinstance(encryption_config, dict):
            encryption_config = DataprocWorkflowTemplateEncryptionConfig(**encryption_config)
        if isinstance(timeouts, dict):
            timeouts = DataprocWorkflowTemplateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b50eb05c4c9f00e119d3886b927e492be1879301ab49d75050dd9c8374f25f4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument jobs", value=jobs, expected_type=type_hints["jobs"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument placement", value=placement, expected_type=type_hints["placement"])
            check_type(argname="argument dag_timeout", value=dag_timeout, expected_type=type_hints["dag_timeout"])
            check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "jobs": jobs,
            "location": location,
            "name": name,
            "placement": placement,
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
        if dag_timeout is not None:
            self._values["dag_timeout"] = dag_timeout
        if encryption_config is not None:
            self._values["encryption_config"] = encryption_config
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if parameters is not None:
            self._values["parameters"] = parameters
        if project is not None:
            self._values["project"] = project
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if version is not None:
            self._values["version"] = version

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
    def jobs(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocWorkflowTemplateJobs"]]:
        '''jobs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#jobs DataprocWorkflowTemplate#jobs}
        '''
        result = self._values.get("jobs")
        assert result is not None, "Required property 'jobs' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocWorkflowTemplateJobs"]], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#location DataprocWorkflowTemplate#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Output only.

        The resource name of the workflow template, as described in https://cloud.google.com/apis/design/resource_names. * For ``projects.regions.workflowTemplates``, the resource name of the template has the following format: ``projects/{project_id}/regions/{region}/workflowTemplates/{template_id}`` * For ``projects.locations.workflowTemplates``, the resource name of the template has the following format: ``projects/{project_id}/locations/{location}/workflowTemplates/{template_id}``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#name DataprocWorkflowTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def placement(self) -> "DataprocWorkflowTemplatePlacement":
        '''placement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#placement DataprocWorkflowTemplate#placement}
        '''
        result = self._values.get("placement")
        assert result is not None, "Required property 'placement' is missing"
        return typing.cast("DataprocWorkflowTemplatePlacement", result)

    @builtins.property
    def dag_timeout(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Timeout duration for the DAG of jobs, expressed in seconds (see `JSON representation of duration <https://developers.google.com/protocol-buffers/docs/proto3#json>`_). The timeout duration must be from 10 minutes ("600s") to 24 hours ("86400s"). The timer begins when the first job is submitted. If the workflow is running at the end of the timeout period, any remaining jobs are cancelled, the workflow is ended, and if the workflow was running on a `managed cluster </dataproc/docs/concepts/workflows/using-workflows#configuring_or_selecting_a_cluster>`_, the cluster is deleted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#dag_timeout DataprocWorkflowTemplate#dag_timeout}
        '''
        result = self._values.get("dag_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_config(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateEncryptionConfig"]:
        '''encryption_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#encryption_config DataprocWorkflowTemplate#encryption_config}
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateEncryptionConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#id DataprocWorkflowTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        The labels to associate with this template. These labels will be propagated to all jobs and clusters created by the workflow instance. Label **keys** must contain 1 to 63 characters, and must conform to `RFC 1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. Label **values** may be empty, but, if present, must contain 1 to 63 characters, and must conform to `RFC 1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. No more than 32 labels can be associated with a template.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field ``effective_labels`` for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#labels DataprocWorkflowTemplate#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocWorkflowTemplateParameters"]]]:
        '''parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#parameters DataprocWorkflowTemplate#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocWorkflowTemplateParameters"]]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#project DataprocWorkflowTemplate#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataprocWorkflowTemplateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#timeouts DataprocWorkflowTemplate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateTimeouts"], result)

    @builtins.property
    def version(self) -> typing.Optional[jsii.Number]:
        '''Output only. The current version of this workflow template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#version DataprocWorkflowTemplate#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateEncryptionConfig",
    jsii_struct_bases=[],
    name_mapping={"kms_key": "kmsKey"},
)
class DataprocWorkflowTemplateEncryptionConfig:
    def __init__(self, *, kms_key: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key: Optional. The Cloud KMS key name to use for encryption. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#kms_key DataprocWorkflowTemplate#kms_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d439bebb6863495086a504766ad25cedc9a572fd8d32852935dff1748d510e0f)
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''Optional. The Cloud KMS key name to use for encryption.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#kms_key DataprocWorkflowTemplate#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateEncryptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplateEncryptionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateEncryptionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22e2cf7ae0906f920b6eaef791eca2bfc6d507654f1343865c6f2d13efa05fac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19a9eb7f23795c9654f65f2ffc447348285a76a25fe55d6d096f04892f3773bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateEncryptionConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateEncryptionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateEncryptionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32f8645946a33096d80f8a9718fda93b50e6f54356055de530514617314f2fa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobs",
    jsii_struct_bases=[],
    name_mapping={
        "step_id": "stepId",
        "hadoop_job": "hadoopJob",
        "hive_job": "hiveJob",
        "labels": "labels",
        "pig_job": "pigJob",
        "prerequisite_step_ids": "prerequisiteStepIds",
        "presto_job": "prestoJob",
        "pyspark_job": "pysparkJob",
        "scheduling": "scheduling",
        "spark_job": "sparkJob",
        "spark_r_job": "sparkRJob",
        "spark_sql_job": "sparkSqlJob",
    },
)
class DataprocWorkflowTemplateJobs:
    def __init__(
        self,
        *,
        step_id: builtins.str,
        hadoop_job: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsHadoopJob", typing.Dict[builtins.str, typing.Any]]] = None,
        hive_job: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsHiveJob", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        pig_job: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsPigJob", typing.Dict[builtins.str, typing.Any]]] = None,
        prerequisite_step_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        presto_job: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsPrestoJob", typing.Dict[builtins.str, typing.Any]]] = None,
        pyspark_job: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsPysparkJob", typing.Dict[builtins.str, typing.Any]]] = None,
        scheduling: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsScheduling", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_job: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsSparkJob", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_r_job: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsSparkRJob", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_sql_job: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsSparkSqlJob", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param step_id: Required. The step id. The id must be unique among all jobs within the template. The step id is used as prefix for job id, as job ``goog-dataproc-workflow-step-id`` label, and in prerequisiteStepIds field from other steps. The id must contain only letters (a-z, A-Z), numbers (0-9), underscores (_), and hyphens (-). Cannot begin or end with underscore or hyphen. Must consist of between 3 and 50 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#step_id DataprocWorkflowTemplate#step_id}
        :param hadoop_job: hadoop_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#hadoop_job DataprocWorkflowTemplate#hadoop_job}
        :param hive_job: hive_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#hive_job DataprocWorkflowTemplate#hive_job}
        :param labels: Optional. The labels to associate with this job. Label keys must be between 1 and 63 characters long, and must conform to the following regular expression: p{Ll}p{Lo}{0,62} Label values must be between 1 and 63 characters long, and must conform to the following regular expression: [p{Ll}p{Lo}p{N}_-]{0,63} No more than 32 labels can be associated with a given job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#labels DataprocWorkflowTemplate#labels}
        :param pig_job: pig_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#pig_job DataprocWorkflowTemplate#pig_job}
        :param prerequisite_step_ids: Optional. The optional list of prerequisite job step_ids. If not specified, the job will start at the beginning of workflow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#prerequisite_step_ids DataprocWorkflowTemplate#prerequisite_step_ids}
        :param presto_job: presto_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#presto_job DataprocWorkflowTemplate#presto_job}
        :param pyspark_job: pyspark_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#pyspark_job DataprocWorkflowTemplate#pyspark_job}
        :param scheduling: scheduling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#scheduling DataprocWorkflowTemplate#scheduling}
        :param spark_job: spark_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#spark_job DataprocWorkflowTemplate#spark_job}
        :param spark_r_job: spark_r_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#spark_r_job DataprocWorkflowTemplate#spark_r_job}
        :param spark_sql_job: spark_sql_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#spark_sql_job DataprocWorkflowTemplate#spark_sql_job}
        '''
        if isinstance(hadoop_job, dict):
            hadoop_job = DataprocWorkflowTemplateJobsHadoopJob(**hadoop_job)
        if isinstance(hive_job, dict):
            hive_job = DataprocWorkflowTemplateJobsHiveJob(**hive_job)
        if isinstance(pig_job, dict):
            pig_job = DataprocWorkflowTemplateJobsPigJob(**pig_job)
        if isinstance(presto_job, dict):
            presto_job = DataprocWorkflowTemplateJobsPrestoJob(**presto_job)
        if isinstance(pyspark_job, dict):
            pyspark_job = DataprocWorkflowTemplateJobsPysparkJob(**pyspark_job)
        if isinstance(scheduling, dict):
            scheduling = DataprocWorkflowTemplateJobsScheduling(**scheduling)
        if isinstance(spark_job, dict):
            spark_job = DataprocWorkflowTemplateJobsSparkJob(**spark_job)
        if isinstance(spark_r_job, dict):
            spark_r_job = DataprocWorkflowTemplateJobsSparkRJob(**spark_r_job)
        if isinstance(spark_sql_job, dict):
            spark_sql_job = DataprocWorkflowTemplateJobsSparkSqlJob(**spark_sql_job)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c0d1b66dd50b722b6da850985a1c1527c42676592b8ecebc1ef11cae1cabd0a)
            check_type(argname="argument step_id", value=step_id, expected_type=type_hints["step_id"])
            check_type(argname="argument hadoop_job", value=hadoop_job, expected_type=type_hints["hadoop_job"])
            check_type(argname="argument hive_job", value=hive_job, expected_type=type_hints["hive_job"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument pig_job", value=pig_job, expected_type=type_hints["pig_job"])
            check_type(argname="argument prerequisite_step_ids", value=prerequisite_step_ids, expected_type=type_hints["prerequisite_step_ids"])
            check_type(argname="argument presto_job", value=presto_job, expected_type=type_hints["presto_job"])
            check_type(argname="argument pyspark_job", value=pyspark_job, expected_type=type_hints["pyspark_job"])
            check_type(argname="argument scheduling", value=scheduling, expected_type=type_hints["scheduling"])
            check_type(argname="argument spark_job", value=spark_job, expected_type=type_hints["spark_job"])
            check_type(argname="argument spark_r_job", value=spark_r_job, expected_type=type_hints["spark_r_job"])
            check_type(argname="argument spark_sql_job", value=spark_sql_job, expected_type=type_hints["spark_sql_job"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "step_id": step_id,
        }
        if hadoop_job is not None:
            self._values["hadoop_job"] = hadoop_job
        if hive_job is not None:
            self._values["hive_job"] = hive_job
        if labels is not None:
            self._values["labels"] = labels
        if pig_job is not None:
            self._values["pig_job"] = pig_job
        if prerequisite_step_ids is not None:
            self._values["prerequisite_step_ids"] = prerequisite_step_ids
        if presto_job is not None:
            self._values["presto_job"] = presto_job
        if pyspark_job is not None:
            self._values["pyspark_job"] = pyspark_job
        if scheduling is not None:
            self._values["scheduling"] = scheduling
        if spark_job is not None:
            self._values["spark_job"] = spark_job
        if spark_r_job is not None:
            self._values["spark_r_job"] = spark_r_job
        if spark_sql_job is not None:
            self._values["spark_sql_job"] = spark_sql_job

    @builtins.property
    def step_id(self) -> builtins.str:
        '''Required.

        The step id. The id must be unique among all jobs within the template. The step id is used as prefix for job id, as job ``goog-dataproc-workflow-step-id`` label, and in prerequisiteStepIds field from other steps. The id must contain only letters (a-z, A-Z), numbers (0-9), underscores (_), and hyphens (-). Cannot begin or end with underscore or hyphen. Must consist of between 3 and 50 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#step_id DataprocWorkflowTemplate#step_id}
        '''
        result = self._values.get("step_id")
        assert result is not None, "Required property 'step_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hadoop_job(self) -> typing.Optional["DataprocWorkflowTemplateJobsHadoopJob"]:
        '''hadoop_job block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#hadoop_job DataprocWorkflowTemplate#hadoop_job}
        '''
        result = self._values.get("hadoop_job")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsHadoopJob"], result)

    @builtins.property
    def hive_job(self) -> typing.Optional["DataprocWorkflowTemplateJobsHiveJob"]:
        '''hive_job block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#hive_job DataprocWorkflowTemplate#hive_job}
        '''
        result = self._values.get("hive_job")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsHiveJob"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        The labels to associate with this job. Label keys must be between 1 and 63 characters long, and must conform to the following regular expression: p{Ll}p{Lo}{0,62} Label values must be between 1 and 63 characters long, and must conform to the following regular expression: [p{Ll}p{Lo}p{N}_-]{0,63} No more than 32 labels can be associated with a given job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#labels DataprocWorkflowTemplate#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def pig_job(self) -> typing.Optional["DataprocWorkflowTemplateJobsPigJob"]:
        '''pig_job block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#pig_job DataprocWorkflowTemplate#pig_job}
        '''
        result = self._values.get("pig_job")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsPigJob"], result)

    @builtins.property
    def prerequisite_step_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        The optional list of prerequisite job step_ids. If not specified, the job will start at the beginning of workflow.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#prerequisite_step_ids DataprocWorkflowTemplate#prerequisite_step_ids}
        '''
        result = self._values.get("prerequisite_step_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def presto_job(self) -> typing.Optional["DataprocWorkflowTemplateJobsPrestoJob"]:
        '''presto_job block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#presto_job DataprocWorkflowTemplate#presto_job}
        '''
        result = self._values.get("presto_job")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsPrestoJob"], result)

    @builtins.property
    def pyspark_job(self) -> typing.Optional["DataprocWorkflowTemplateJobsPysparkJob"]:
        '''pyspark_job block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#pyspark_job DataprocWorkflowTemplate#pyspark_job}
        '''
        result = self._values.get("pyspark_job")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsPysparkJob"], result)

    @builtins.property
    def scheduling(self) -> typing.Optional["DataprocWorkflowTemplateJobsScheduling"]:
        '''scheduling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#scheduling DataprocWorkflowTemplate#scheduling}
        '''
        result = self._values.get("scheduling")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsScheduling"], result)

    @builtins.property
    def spark_job(self) -> typing.Optional["DataprocWorkflowTemplateJobsSparkJob"]:
        '''spark_job block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#spark_job DataprocWorkflowTemplate#spark_job}
        '''
        result = self._values.get("spark_job")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsSparkJob"], result)

    @builtins.property
    def spark_r_job(self) -> typing.Optional["DataprocWorkflowTemplateJobsSparkRJob"]:
        '''spark_r_job block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#spark_r_job DataprocWorkflowTemplate#spark_r_job}
        '''
        result = self._values.get("spark_r_job")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsSparkRJob"], result)

    @builtins.property
    def spark_sql_job(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateJobsSparkSqlJob"]:
        '''spark_sql_job block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#spark_sql_job DataprocWorkflowTemplate#spark_sql_job}
        '''
        result = self._values.get("spark_sql_job")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsSparkSqlJob"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateJobs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsHadoopJob",
    jsii_struct_bases=[],
    name_mapping={
        "archive_uris": "archiveUris",
        "args": "args",
        "file_uris": "fileUris",
        "jar_file_uris": "jarFileUris",
        "logging_config": "loggingConfig",
        "main_class": "mainClass",
        "main_jar_file_uri": "mainJarFileUri",
        "properties": "properties",
    },
)
class DataprocWorkflowTemplateJobsHadoopJob:
    def __init__(
        self,
        *,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsHadoopJobLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        main_class: typing.Optional[builtins.str] = None,
        main_jar_file_uri: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param archive_uris: Optional. HCFS URIs of archives to be extracted in the working directory of Hadoop drivers and tasks. Supported file types: .jar, .tar, .tar.gz, .tgz, or .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#archive_uris DataprocWorkflowTemplate#archive_uris}
        :param args: Optional. The arguments to pass to the driver. Do not include arguments, such as ``-libjars`` or ``-Dfoo=bar``, that can be set as job properties, since a collision may occur that causes an incorrect job submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#args DataprocWorkflowTemplate#args}
        :param file_uris: Optional. HCFS (Hadoop Compatible Filesystem) URIs of files to be copied to the working directory of Hadoop drivers and distributed tasks. Useful for naively parallel tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#file_uris DataprocWorkflowTemplate#file_uris}
        :param jar_file_uris: Optional. Jar file URIs to add to the CLASSPATHs of the Hadoop driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#jar_file_uris DataprocWorkflowTemplate#jar_file_uris}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#logging_config DataprocWorkflowTemplate#logging_config}
        :param main_class: The name of the driver's main class. The jar file containing the class must be in the default CLASSPATH or specified in ``jar_file_uris``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#main_class DataprocWorkflowTemplate#main_class}
        :param main_jar_file_uri: The HCFS URI of the jar file containing the main class. Examples: 'gs://foo-bucket/analytics-binaries/extract-useful-metrics-mr.jar' 'hdfs:/tmp/test-samples/custom-wordcount.jar' 'file:///home/usr/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#main_jar_file_uri DataprocWorkflowTemplate#main_jar_file_uri}
        :param properties: Optional. A mapping of property names to values, used to configure Hadoop. Properties that conflict with values set by the Dataproc API may be overwritten. Can include properties set in /etc/hadoop/conf/*-site and classes in user code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        '''
        if isinstance(logging_config, dict):
            logging_config = DataprocWorkflowTemplateJobsHadoopJobLoggingConfig(**logging_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e33c355518e475289849858a0b682d48445ffce3a23633ca54de2528b3b8a7d1)
            check_type(argname="argument archive_uris", value=archive_uris, expected_type=type_hints["archive_uris"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument file_uris", value=file_uris, expected_type=type_hints["file_uris"])
            check_type(argname="argument jar_file_uris", value=jar_file_uris, expected_type=type_hints["jar_file_uris"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument main_class", value=main_class, expected_type=type_hints["main_class"])
            check_type(argname="argument main_jar_file_uri", value=main_jar_file_uri, expected_type=type_hints["main_jar_file_uri"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if archive_uris is not None:
            self._values["archive_uris"] = archive_uris
        if args is not None:
            self._values["args"] = args
        if file_uris is not None:
            self._values["file_uris"] = file_uris
        if jar_file_uris is not None:
            self._values["jar_file_uris"] = jar_file_uris
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if main_class is not None:
            self._values["main_class"] = main_class
        if main_jar_file_uri is not None:
            self._values["main_jar_file_uri"] = main_jar_file_uri
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def archive_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        HCFS URIs of archives to be extracted in the working directory of Hadoop drivers and tasks. Supported file types: .jar, .tar, .tar.gz, .tgz, or .zip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#archive_uris DataprocWorkflowTemplate#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        The arguments to pass to the driver. Do not include arguments, such as ``-libjars`` or ``-Dfoo=bar``, that can be set as job properties, since a collision may occur that causes an incorrect job submission.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#args DataprocWorkflowTemplate#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        HCFS (Hadoop Compatible Filesystem) URIs of files to be copied to the working directory of Hadoop drivers and distributed tasks. Useful for naively parallel tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#file_uris DataprocWorkflowTemplate#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jar_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. Jar file URIs to add to the CLASSPATHs of the Hadoop driver and tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#jar_file_uris DataprocWorkflowTemplate#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateJobsHadoopJobLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#logging_config DataprocWorkflowTemplate#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsHadoopJobLoggingConfig"], result)

    @builtins.property
    def main_class(self) -> typing.Optional[builtins.str]:
        '''The name of the driver's main class.

        The jar file containing the class must be in the default CLASSPATH or specified in ``jar_file_uris``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#main_class DataprocWorkflowTemplate#main_class}
        '''
        result = self._values.get("main_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def main_jar_file_uri(self) -> typing.Optional[builtins.str]:
        '''The HCFS URI of the jar file containing the main class. Examples: 'gs://foo-bucket/analytics-binaries/extract-useful-metrics-mr.jar' 'hdfs:/tmp/test-samples/custom-wordcount.jar' 'file:///home/usr/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#main_jar_file_uri DataprocWorkflowTemplate#main_jar_file_uri}
        '''
        result = self._values.get("main_jar_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        A mapping of property names to values, used to configure Hadoop. Properties that conflict with values set by the Dataproc API may be overwritten. Can include properties set in /etc/hadoop/conf/*-site and classes in user code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateJobsHadoopJob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsHadoopJobLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"driver_log_levels": "driverLogLevels"},
)
class DataprocWorkflowTemplateJobsHadoopJobLoggingConfig:
    def __init__(
        self,
        *,
        driver_log_levels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param driver_log_levels: The per-package log levels for the driver. This may include "root" package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#driver_log_levels DataprocWorkflowTemplate#driver_log_levels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f131cce8b64a118408aca7e0cec717d00843bbad284dd88e9c3c85711430d58)
            check_type(argname="argument driver_log_levels", value=driver_log_levels, expected_type=type_hints["driver_log_levels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if driver_log_levels is not None:
            self._values["driver_log_levels"] = driver_log_levels

    @builtins.property
    def driver_log_levels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The per-package log levels for the driver.

        This may include "root" package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#driver_log_levels DataprocWorkflowTemplate#driver_log_levels}
        '''
        result = self._values.get("driver_log_levels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateJobsHadoopJobLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplateJobsHadoopJobLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsHadoopJobLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e1fd30ee46295a0dbaff2999a064b2b1865a4e7041e635bff66613004b33159)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDriverLogLevels")
    def reset_driver_log_levels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDriverLogLevels", []))

    @builtins.property
    @jsii.member(jsii_name="driverLogLevelsInput")
    def driver_log_levels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "driverLogLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="driverLogLevels")
    def driver_log_levels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "driverLogLevels"))

    @driver_log_levels.setter
    def driver_log_levels(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e82f7b27771a1520df4d962dd1002803d1ab9a3e80302dcf0cf893715b83a5a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverLogLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateJobsHadoopJobLoggingConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsHadoopJobLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateJobsHadoopJobLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b92f337a8343155b805703af004a47dc1bb11a443967c3c684dbba10a11ffcdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplateJobsHadoopJobOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsHadoopJobOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98a8dbbc6ce15d10cd1c87f0bf1b8ff1ae150ca141946c58503328180d9852d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        driver_log_levels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param driver_log_levels: The per-package log levels for the driver. This may include "root" package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#driver_log_levels DataprocWorkflowTemplate#driver_log_levels}
        '''
        value = DataprocWorkflowTemplateJobsHadoopJobLoggingConfig(
            driver_log_levels=driver_log_levels
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

    @jsii.member(jsii_name="resetArchiveUris")
    def reset_archive_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchiveUris", []))

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetFileUris")
    def reset_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileUris", []))

    @jsii.member(jsii_name="resetJarFileUris")
    def reset_jar_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJarFileUris", []))

    @jsii.member(jsii_name="resetLoggingConfig")
    def reset_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfig", []))

    @jsii.member(jsii_name="resetMainClass")
    def reset_main_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMainClass", []))

    @jsii.member(jsii_name="resetMainJarFileUri")
    def reset_main_jar_file_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMainJarFileUri", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(
        self,
    ) -> DataprocWorkflowTemplateJobsHadoopJobLoggingConfigOutputReference:
        return typing.cast(DataprocWorkflowTemplateJobsHadoopJobLoggingConfigOutputReference, jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="archiveUrisInput")
    def archive_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "archiveUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="fileUrisInput")
    def file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "fileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="jarFileUrisInput")
    def jar_file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jarFileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfigInput")
    def logging_config_input(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateJobsHadoopJobLoggingConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsHadoopJobLoggingConfig], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="mainClassInput")
    def main_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mainClassInput"))

    @builtins.property
    @jsii.member(jsii_name="mainJarFileUriInput")
    def main_jar_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mainJarFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="archiveUris")
    def archive_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "archiveUris"))

    @archive_uris.setter
    def archive_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4b42ef617021d95fd5064d5367d6419d585c52e040b588dc609e78be3cdbf94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__544a6fdbaea92c59d6d6cf26d8b6d52174c329fcc258c15fdab70a53558a45d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__223718cb1f153ed4a359f1964555cc4ee6634a75fdc4e5d8310b6a4cb6717b39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jarFileUris")
    def jar_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jarFileUris"))

    @jar_file_uris.setter
    def jar_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8db64929038fb9a9ef351ed917380e7e0aaa7668281cef823999884b53ec85a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainClass")
    def main_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainClass"))

    @main_class.setter
    def main_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03e9da5ab51fc0656af44b81c2f8061231caa885aab1140ec930facaacbbd1f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainJarFileUri")
    def main_jar_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainJarFileUri"))

    @main_jar_file_uri.setter
    def main_jar_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcd0bc418dbbf0ed3c10b2d8ba1781f46af8864976b07a8c7271311e13eca9ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainJarFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d26818d6ed07ab6ad4cc7797639b5eb991bbb12c09d382426650c4dbb784895)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocWorkflowTemplateJobsHadoopJob]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsHadoopJob], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateJobsHadoopJob],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d7426b0ed4b8de107b31eb807cae95ba6a836564ef7741359fb49e70f600f3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsHiveJob",
    jsii_struct_bases=[],
    name_mapping={
        "continue_on_failure": "continueOnFailure",
        "jar_file_uris": "jarFileUris",
        "properties": "properties",
        "query_file_uri": "queryFileUri",
        "query_list": "queryList",
        "script_variables": "scriptVariables",
    },
)
class DataprocWorkflowTemplateJobsHiveJob:
    def __init__(
        self,
        *,
        continue_on_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        query_file_uri: typing.Optional[builtins.str] = None,
        query_list: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsHiveJobQueryListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
        script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param continue_on_failure: Optional. Whether to continue executing queries if a query fails. The default value is ``false``. Setting to ``true`` can be useful when executing independent parallel queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#continue_on_failure DataprocWorkflowTemplate#continue_on_failure}
        :param jar_file_uris: Optional. HCFS URIs of jar files to add to the CLASSPATH of the Hive server and Hadoop MapReduce (MR) tasks. Can contain Hive SerDes and UDFs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#jar_file_uris DataprocWorkflowTemplate#jar_file_uris}
        :param properties: Optional. A mapping of property names and values, used to configure Hive. Properties that conflict with values set by the Dataproc API may be overwritten. Can include properties set in /etc/hadoop/conf/*-site.xml, /etc/hive/conf/hive-site.xml, and classes in user code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        :param query_file_uri: The HCFS URI of the script that contains Hive queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_file_uri DataprocWorkflowTemplate#query_file_uri}
        :param query_list: query_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_list DataprocWorkflowTemplate#query_list}
        :param script_variables: Optional. Mapping of query variable names to values (equivalent to the Hive command: ``SET name="value";``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#script_variables DataprocWorkflowTemplate#script_variables}
        '''
        if isinstance(query_list, dict):
            query_list = DataprocWorkflowTemplateJobsHiveJobQueryListStruct(**query_list)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1a39c4daa737734d1f6b801d9af93f698fcef024af64bc69ec2d69819eb3cb2)
            check_type(argname="argument continue_on_failure", value=continue_on_failure, expected_type=type_hints["continue_on_failure"])
            check_type(argname="argument jar_file_uris", value=jar_file_uris, expected_type=type_hints["jar_file_uris"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument query_file_uri", value=query_file_uri, expected_type=type_hints["query_file_uri"])
            check_type(argname="argument query_list", value=query_list, expected_type=type_hints["query_list"])
            check_type(argname="argument script_variables", value=script_variables, expected_type=type_hints["script_variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if continue_on_failure is not None:
            self._values["continue_on_failure"] = continue_on_failure
        if jar_file_uris is not None:
            self._values["jar_file_uris"] = jar_file_uris
        if properties is not None:
            self._values["properties"] = properties
        if query_file_uri is not None:
            self._values["query_file_uri"] = query_file_uri
        if query_list is not None:
            self._values["query_list"] = query_list
        if script_variables is not None:
            self._values["script_variables"] = script_variables

    @builtins.property
    def continue_on_failure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Whether to continue executing queries if a query fails. The default value is ``false``. Setting to ``true`` can be useful when executing independent parallel queries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#continue_on_failure DataprocWorkflowTemplate#continue_on_failure}
        '''
        result = self._values.get("continue_on_failure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def jar_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        HCFS URIs of jar files to add to the CLASSPATH of the Hive server and Hadoop MapReduce (MR) tasks. Can contain Hive SerDes and UDFs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#jar_file_uris DataprocWorkflowTemplate#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        A mapping of property names and values, used to configure Hive. Properties that conflict with values set by the Dataproc API may be overwritten. Can include properties set in /etc/hadoop/conf/*-site.xml, /etc/hive/conf/hive-site.xml, and classes in user code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def query_file_uri(self) -> typing.Optional[builtins.str]:
        '''The HCFS URI of the script that contains Hive queries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_file_uri DataprocWorkflowTemplate#query_file_uri}
        '''
        result = self._values.get("query_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_list(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateJobsHiveJobQueryListStruct"]:
        '''query_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_list DataprocWorkflowTemplate#query_list}
        '''
        result = self._values.get("query_list")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsHiveJobQueryListStruct"], result)

    @builtins.property
    def script_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. Mapping of query variable names to values (equivalent to the Hive command: ``SET name="value";``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#script_variables DataprocWorkflowTemplate#script_variables}
        '''
        result = self._values.get("script_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateJobsHiveJob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplateJobsHiveJobOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsHiveJobOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__562de03011484117b184c6a51022467ee4aa02aa60ac1180b5675c33cc8058a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putQueryList")
    def put_query_list(self, *, queries: typing.Sequence[builtins.str]) -> None:
        '''
        :param queries: Required. The queries to execute. You do not need to end a query expression with a semicolon. Multiple queries can be specified in one string by separating each with a semicolon. Here is an example of a Dataproc API snippet that uses a QueryList to specify a HiveJob: "hiveJob": { "queryList": { "queries": [ "query1", "query2", "query3;query4", ] } } Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#queries DataprocWorkflowTemplate#queries}
        '''
        value = DataprocWorkflowTemplateJobsHiveJobQueryListStruct(queries=queries)

        return typing.cast(None, jsii.invoke(self, "putQueryList", [value]))

    @jsii.member(jsii_name="resetContinueOnFailure")
    def reset_continue_on_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContinueOnFailure", []))

    @jsii.member(jsii_name="resetJarFileUris")
    def reset_jar_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJarFileUris", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @jsii.member(jsii_name="resetQueryFileUri")
    def reset_query_file_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryFileUri", []))

    @jsii.member(jsii_name="resetQueryList")
    def reset_query_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryList", []))

    @jsii.member(jsii_name="resetScriptVariables")
    def reset_script_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScriptVariables", []))

    @builtins.property
    @jsii.member(jsii_name="queryList")
    def query_list(
        self,
    ) -> "DataprocWorkflowTemplateJobsHiveJobQueryListStructOutputReference":
        return typing.cast("DataprocWorkflowTemplateJobsHiveJobQueryListStructOutputReference", jsii.get(self, "queryList"))

    @builtins.property
    @jsii.member(jsii_name="continueOnFailureInput")
    def continue_on_failure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "continueOnFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="jarFileUrisInput")
    def jar_file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jarFileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="queryFileUriInput")
    def query_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="queryListInput")
    def query_list_input(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateJobsHiveJobQueryListStruct"]:
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsHiveJobQueryListStruct"], jsii.get(self, "queryListInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptVariablesInput")
    def script_variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "scriptVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="continueOnFailure")
    def continue_on_failure(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "continueOnFailure"))

    @continue_on_failure.setter
    def continue_on_failure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89f695be95aeab0822e6c381ca0c2164f0472030e254c684cfff5deb997e145e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "continueOnFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jarFileUris")
    def jar_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jarFileUris"))

    @jar_file_uris.setter
    def jar_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c30e4504039dfd98eeac48711f13855b5919e6e5afacc785ea409c06d743c68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50052ca4ab890fccaf9b29ebe8801665b33410d60f4f3629ccb52a71a8e80bc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryFileUri")
    def query_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryFileUri"))

    @query_file_uri.setter
    def query_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae78151622f6fb9a415f00beca6d6dda6d448d642bdbe0fc0e42859231f03432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scriptVariables")
    def script_variables(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "scriptVariables"))

    @script_variables.setter
    def script_variables(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7df0c4025468cf473a27a5a56d5296c8fc38fa80e86cb4b4387fc286259742d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocWorkflowTemplateJobsHiveJob]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsHiveJob], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateJobsHiveJob],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fb63d22a3cb20d91913c73b979ef9d749947788e952b3774e96b5f06e902fc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsHiveJobQueryListStruct",
    jsii_struct_bases=[],
    name_mapping={"queries": "queries"},
)
class DataprocWorkflowTemplateJobsHiveJobQueryListStruct:
    def __init__(self, *, queries: typing.Sequence[builtins.str]) -> None:
        '''
        :param queries: Required. The queries to execute. You do not need to end a query expression with a semicolon. Multiple queries can be specified in one string by separating each with a semicolon. Here is an example of a Dataproc API snippet that uses a QueryList to specify a HiveJob: "hiveJob": { "queryList": { "queries": [ "query1", "query2", "query3;query4", ] } } Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#queries DataprocWorkflowTemplate#queries}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbca1c8603e5944f31137811503c01f8c988675f262483b25aed8fb278c650f9)
            check_type(argname="argument queries", value=queries, expected_type=type_hints["queries"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "queries": queries,
        }

    @builtins.property
    def queries(self) -> typing.List[builtins.str]:
        '''Required.

        The queries to execute. You do not need to end a query expression with a semicolon. Multiple queries can be specified in one string by separating each with a semicolon. Here is an example of a Dataproc API snippet that uses a QueryList to specify a HiveJob: "hiveJob": { "queryList": { "queries": [ "query1", "query2", "query3;query4", ] } }

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#queries DataprocWorkflowTemplate#queries}
        '''
        result = self._values.get("queries")
        assert result is not None, "Required property 'queries' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateJobsHiveJobQueryListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplateJobsHiveJobQueryListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsHiveJobQueryListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20116c617692fb9e566d5dd18da5be186b124344560dbdcf6dcd92045aa874a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="queriesInput")
    def queries_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queriesInput"))

    @builtins.property
    @jsii.member(jsii_name="queries")
    def queries(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queries"))

    @queries.setter
    def queries(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd6a6a975f4787b98ebe66d55887248c97dc677e999818574ab83ed5057f478c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateJobsHiveJobQueryListStruct]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsHiveJobQueryListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateJobsHiveJobQueryListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c787e3876a998d0dc15ea024f324dca1eb6e37725ed3eebb2f01fd759d8f02ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplateJobsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__090a56b73373cd95c8f4a49c6fbd5e4a7f65192a35d467d4e3c5da0e14389193)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataprocWorkflowTemplateJobsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__014bb647252a938f25cbbc70e82a4d7a82a94dd0e80e1ba662b0480e5e1acbe7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataprocWorkflowTemplateJobsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da0a9131c66c4d097f4584251465b9b920f60d8e007b0e77fc802916d506209e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bb9c20c6e8f1d24947d308b2ece27f76403e0ed43738084f509d4f9db2a3544)
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
            type_hints = typing.get_type_hints(_typecheckingstub__885c751b85992db26ebe91be7b9f9166afc5d745bf93734741f63abc076bfcf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplateJobs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplateJobs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplateJobs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d006f0760b989718f7e14cb8e48d088241cd54f5216e00e32796e5b6a445235c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplateJobsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db04c30a58e21d31fa29eb006b30ed9a673b1ac947968c14f8077b88b48ccc65)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHadoopJob")
    def put_hadoop_job(
        self,
        *,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union[DataprocWorkflowTemplateJobsHadoopJobLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        main_class: typing.Optional[builtins.str] = None,
        main_jar_file_uri: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param archive_uris: Optional. HCFS URIs of archives to be extracted in the working directory of Hadoop drivers and tasks. Supported file types: .jar, .tar, .tar.gz, .tgz, or .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#archive_uris DataprocWorkflowTemplate#archive_uris}
        :param args: Optional. The arguments to pass to the driver. Do not include arguments, such as ``-libjars`` or ``-Dfoo=bar``, that can be set as job properties, since a collision may occur that causes an incorrect job submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#args DataprocWorkflowTemplate#args}
        :param file_uris: Optional. HCFS (Hadoop Compatible Filesystem) URIs of files to be copied to the working directory of Hadoop drivers and distributed tasks. Useful for naively parallel tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#file_uris DataprocWorkflowTemplate#file_uris}
        :param jar_file_uris: Optional. Jar file URIs to add to the CLASSPATHs of the Hadoop driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#jar_file_uris DataprocWorkflowTemplate#jar_file_uris}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#logging_config DataprocWorkflowTemplate#logging_config}
        :param main_class: The name of the driver's main class. The jar file containing the class must be in the default CLASSPATH or specified in ``jar_file_uris``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#main_class DataprocWorkflowTemplate#main_class}
        :param main_jar_file_uri: The HCFS URI of the jar file containing the main class. Examples: 'gs://foo-bucket/analytics-binaries/extract-useful-metrics-mr.jar' 'hdfs:/tmp/test-samples/custom-wordcount.jar' 'file:///home/usr/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#main_jar_file_uri DataprocWorkflowTemplate#main_jar_file_uri}
        :param properties: Optional. A mapping of property names to values, used to configure Hadoop. Properties that conflict with values set by the Dataproc API may be overwritten. Can include properties set in /etc/hadoop/conf/*-site and classes in user code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        '''
        value = DataprocWorkflowTemplateJobsHadoopJob(
            archive_uris=archive_uris,
            args=args,
            file_uris=file_uris,
            jar_file_uris=jar_file_uris,
            logging_config=logging_config,
            main_class=main_class,
            main_jar_file_uri=main_jar_file_uri,
            properties=properties,
        )

        return typing.cast(None, jsii.invoke(self, "putHadoopJob", [value]))

    @jsii.member(jsii_name="putHiveJob")
    def put_hive_job(
        self,
        *,
        continue_on_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        query_file_uri: typing.Optional[builtins.str] = None,
        query_list: typing.Optional[typing.Union[DataprocWorkflowTemplateJobsHiveJobQueryListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
        script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param continue_on_failure: Optional. Whether to continue executing queries if a query fails. The default value is ``false``. Setting to ``true`` can be useful when executing independent parallel queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#continue_on_failure DataprocWorkflowTemplate#continue_on_failure}
        :param jar_file_uris: Optional. HCFS URIs of jar files to add to the CLASSPATH of the Hive server and Hadoop MapReduce (MR) tasks. Can contain Hive SerDes and UDFs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#jar_file_uris DataprocWorkflowTemplate#jar_file_uris}
        :param properties: Optional. A mapping of property names and values, used to configure Hive. Properties that conflict with values set by the Dataproc API may be overwritten. Can include properties set in /etc/hadoop/conf/*-site.xml, /etc/hive/conf/hive-site.xml, and classes in user code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        :param query_file_uri: The HCFS URI of the script that contains Hive queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_file_uri DataprocWorkflowTemplate#query_file_uri}
        :param query_list: query_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_list DataprocWorkflowTemplate#query_list}
        :param script_variables: Optional. Mapping of query variable names to values (equivalent to the Hive command: ``SET name="value";``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#script_variables DataprocWorkflowTemplate#script_variables}
        '''
        value = DataprocWorkflowTemplateJobsHiveJob(
            continue_on_failure=continue_on_failure,
            jar_file_uris=jar_file_uris,
            properties=properties,
            query_file_uri=query_file_uri,
            query_list=query_list,
            script_variables=script_variables,
        )

        return typing.cast(None, jsii.invoke(self, "putHiveJob", [value]))

    @jsii.member(jsii_name="putPigJob")
    def put_pig_job(
        self,
        *,
        continue_on_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsPigJobLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        query_file_uri: typing.Optional[builtins.str] = None,
        query_list: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsPigJobQueryListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
        script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param continue_on_failure: Optional. Whether to continue executing queries if a query fails. The default value is ``false``. Setting to ``true`` can be useful when executing independent parallel queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#continue_on_failure DataprocWorkflowTemplate#continue_on_failure}
        :param jar_file_uris: Optional. HCFS URIs of jar files to add to the CLASSPATH of the Pig Client and Hadoop MapReduce (MR) tasks. Can contain Pig UDFs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#jar_file_uris DataprocWorkflowTemplate#jar_file_uris}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#logging_config DataprocWorkflowTemplate#logging_config}
        :param properties: Optional. A mapping of property names to values, used to configure Pig. Properties that conflict with values set by the Dataproc API may be overwritten. Can include properties set in /etc/hadoop/conf/*-site.xml, /etc/pig/conf/pig.properties, and classes in user code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        :param query_file_uri: The HCFS URI of the script that contains the Pig queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_file_uri DataprocWorkflowTemplate#query_file_uri}
        :param query_list: query_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_list DataprocWorkflowTemplate#query_list}
        :param script_variables: Optional. Mapping of query variable names to values (equivalent to the Pig command: ``name=[value]``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#script_variables DataprocWorkflowTemplate#script_variables}
        '''
        value = DataprocWorkflowTemplateJobsPigJob(
            continue_on_failure=continue_on_failure,
            jar_file_uris=jar_file_uris,
            logging_config=logging_config,
            properties=properties,
            query_file_uri=query_file_uri,
            query_list=query_list,
            script_variables=script_variables,
        )

        return typing.cast(None, jsii.invoke(self, "putPigJob", [value]))

    @jsii.member(jsii_name="putPrestoJob")
    def put_presto_job(
        self,
        *,
        client_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        continue_on_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        logging_config: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsPrestoJobLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        output_format: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        query_file_uri: typing.Optional[builtins.str] = None,
        query_list: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsPrestoJobQueryListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_tags: Optional. Presto client tags to attach to this query. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#client_tags DataprocWorkflowTemplate#client_tags}
        :param continue_on_failure: Optional. Whether to continue executing queries if a query fails. The default value is ``false``. Setting to ``true`` can be useful when executing independent parallel queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#continue_on_failure DataprocWorkflowTemplate#continue_on_failure}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#logging_config DataprocWorkflowTemplate#logging_config}
        :param output_format: Optional. The format in which query output will be displayed. See the Presto documentation for supported output formats. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#output_format DataprocWorkflowTemplate#output_format}
        :param properties: Optional. A mapping of property names to values. Used to set Presto `session properties <https://prestodb.io/docs/current/sql/set-session.html>`_ Equivalent to using the --session flag in the Presto CLI Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        :param query_file_uri: The HCFS URI of the script that contains SQL queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_file_uri DataprocWorkflowTemplate#query_file_uri}
        :param query_list: query_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_list DataprocWorkflowTemplate#query_list}
        '''
        value = DataprocWorkflowTemplateJobsPrestoJob(
            client_tags=client_tags,
            continue_on_failure=continue_on_failure,
            logging_config=logging_config,
            output_format=output_format,
            properties=properties,
            query_file_uri=query_file_uri,
            query_list=query_list,
        )

        return typing.cast(None, jsii.invoke(self, "putPrestoJob", [value]))

    @jsii.member(jsii_name="putPysparkJob")
    def put_pyspark_job(
        self,
        *,
        main_python_file_uri: builtins.str,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsPysparkJobLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        python_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param main_python_file_uri: Required. The HCFS URI of the main Python file to use as the driver. Must be a .py file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#main_python_file_uri DataprocWorkflowTemplate#main_python_file_uri}
        :param archive_uris: Optional. HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#archive_uris DataprocWorkflowTemplate#archive_uris}
        :param args: Optional. The arguments to pass to the driver. Do not include arguments, such as ``--conf``, that can be set as job properties, since a collision may occur that causes an incorrect job submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#args DataprocWorkflowTemplate#args}
        :param file_uris: Optional. HCFS URIs of files to be placed in the working directory of each executor. Useful for naively parallel tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#file_uris DataprocWorkflowTemplate#file_uris}
        :param jar_file_uris: Optional. HCFS URIs of jar files to add to the CLASSPATHs of the Python driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#jar_file_uris DataprocWorkflowTemplate#jar_file_uris}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#logging_config DataprocWorkflowTemplate#logging_config}
        :param properties: Optional. A mapping of property names to values, used to configure PySpark. Properties that conflict with values set by the Dataproc API may be overwritten. Can include properties set in /etc/spark/conf/spark-defaults.conf and classes in user code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        :param python_file_uris: Optional. HCFS file URIs of Python files to pass to the PySpark framework. Supported file types: .py, .egg, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#python_file_uris DataprocWorkflowTemplate#python_file_uris}
        '''
        value = DataprocWorkflowTemplateJobsPysparkJob(
            main_python_file_uri=main_python_file_uri,
            archive_uris=archive_uris,
            args=args,
            file_uris=file_uris,
            jar_file_uris=jar_file_uris,
            logging_config=logging_config,
            properties=properties,
            python_file_uris=python_file_uris,
        )

        return typing.cast(None, jsii.invoke(self, "putPysparkJob", [value]))

    @jsii.member(jsii_name="putScheduling")
    def put_scheduling(
        self,
        *,
        max_failures_per_hour: typing.Optional[jsii.Number] = None,
        max_failures_total: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_failures_per_hour: Optional. Maximum number of times per hour a driver may be restarted as a result of driver exiting with non-zero code before job is reported failed. A job may be reported as thrashing if driver exits with non-zero code 4 times within 10 minute window. Maximum value is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#max_failures_per_hour DataprocWorkflowTemplate#max_failures_per_hour}
        :param max_failures_total: Optional. Maximum number of times in total a driver may be restarted as a result of driver exiting with non-zero code before job is reported failed. Maximum value is 240. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#max_failures_total DataprocWorkflowTemplate#max_failures_total}
        '''
        value = DataprocWorkflowTemplateJobsScheduling(
            max_failures_per_hour=max_failures_per_hour,
            max_failures_total=max_failures_total,
        )

        return typing.cast(None, jsii.invoke(self, "putScheduling", [value]))

    @jsii.member(jsii_name="putSparkJob")
    def put_spark_job(
        self,
        *,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsSparkJobLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        main_class: typing.Optional[builtins.str] = None,
        main_jar_file_uri: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param archive_uris: Optional. HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#archive_uris DataprocWorkflowTemplate#archive_uris}
        :param args: Optional. The arguments to pass to the driver. Do not include arguments, such as ``--conf``, that can be set as job properties, since a collision may occur that causes an incorrect job submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#args DataprocWorkflowTemplate#args}
        :param file_uris: Optional. HCFS URIs of files to be placed in the working directory of each executor. Useful for naively parallel tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#file_uris DataprocWorkflowTemplate#file_uris}
        :param jar_file_uris: Optional. HCFS URIs of jar files to add to the CLASSPATHs of the Spark driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#jar_file_uris DataprocWorkflowTemplate#jar_file_uris}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#logging_config DataprocWorkflowTemplate#logging_config}
        :param main_class: The name of the driver's main class. The jar file that contains the class must be in the default CLASSPATH or specified in ``jar_file_uris``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#main_class DataprocWorkflowTemplate#main_class}
        :param main_jar_file_uri: The HCFS URI of the jar file that contains the main class. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#main_jar_file_uri DataprocWorkflowTemplate#main_jar_file_uri}
        :param properties: Optional. A mapping of property names to values, used to configure Spark. Properties that conflict with values set by the Dataproc API may be overwritten. Can include properties set in /etc/spark/conf/spark-defaults.conf and classes in user code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        '''
        value = DataprocWorkflowTemplateJobsSparkJob(
            archive_uris=archive_uris,
            args=args,
            file_uris=file_uris,
            jar_file_uris=jar_file_uris,
            logging_config=logging_config,
            main_class=main_class,
            main_jar_file_uri=main_jar_file_uri,
            properties=properties,
        )

        return typing.cast(None, jsii.invoke(self, "putSparkJob", [value]))

    @jsii.member(jsii_name="putSparkRJob")
    def put_spark_r_job(
        self,
        *,
        main_r_file_uri: builtins.str,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsSparkRJobLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param main_r_file_uri: Required. The HCFS URI of the main R file to use as the driver. Must be a .R file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#main_r_file_uri DataprocWorkflowTemplate#main_r_file_uri}
        :param archive_uris: Optional. HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#archive_uris DataprocWorkflowTemplate#archive_uris}
        :param args: Optional. The arguments to pass to the driver. Do not include arguments, such as ``--conf``, that can be set as job properties, since a collision may occur that causes an incorrect job submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#args DataprocWorkflowTemplate#args}
        :param file_uris: Optional. HCFS URIs of files to be placed in the working directory of each executor. Useful for naively parallel tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#file_uris DataprocWorkflowTemplate#file_uris}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#logging_config DataprocWorkflowTemplate#logging_config}
        :param properties: Optional. A mapping of property names to values, used to configure SparkR. Properties that conflict with values set by the Dataproc API may be overwritten. Can include properties set in /etc/spark/conf/spark-defaults.conf and classes in user code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        '''
        value = DataprocWorkflowTemplateJobsSparkRJob(
            main_r_file_uri=main_r_file_uri,
            archive_uris=archive_uris,
            args=args,
            file_uris=file_uris,
            logging_config=logging_config,
            properties=properties,
        )

        return typing.cast(None, jsii.invoke(self, "putSparkRJob", [value]))

    @jsii.member(jsii_name="putSparkSqlJob")
    def put_spark_sql_job(
        self,
        *,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsSparkSqlJobLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        query_file_uri: typing.Optional[builtins.str] = None,
        query_list: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsSparkSqlJobQueryListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
        script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param jar_file_uris: Optional. HCFS URIs of jar files to be added to the Spark CLASSPATH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#jar_file_uris DataprocWorkflowTemplate#jar_file_uris}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#logging_config DataprocWorkflowTemplate#logging_config}
        :param properties: Optional. A mapping of property names to values, used to configure Spark SQL's SparkConf. Properties that conflict with values set by the Dataproc API may be overwritten. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        :param query_file_uri: The HCFS URI of the script that contains SQL queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_file_uri DataprocWorkflowTemplate#query_file_uri}
        :param query_list: query_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_list DataprocWorkflowTemplate#query_list}
        :param script_variables: Optional. Mapping of query variable names to values (equivalent to the Spark SQL command: SET ``name="value";``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#script_variables DataprocWorkflowTemplate#script_variables}
        '''
        value = DataprocWorkflowTemplateJobsSparkSqlJob(
            jar_file_uris=jar_file_uris,
            logging_config=logging_config,
            properties=properties,
            query_file_uri=query_file_uri,
            query_list=query_list,
            script_variables=script_variables,
        )

        return typing.cast(None, jsii.invoke(self, "putSparkSqlJob", [value]))

    @jsii.member(jsii_name="resetHadoopJob")
    def reset_hadoop_job(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHadoopJob", []))

    @jsii.member(jsii_name="resetHiveJob")
    def reset_hive_job(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHiveJob", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetPigJob")
    def reset_pig_job(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPigJob", []))

    @jsii.member(jsii_name="resetPrerequisiteStepIds")
    def reset_prerequisite_step_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrerequisiteStepIds", []))

    @jsii.member(jsii_name="resetPrestoJob")
    def reset_presto_job(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrestoJob", []))

    @jsii.member(jsii_name="resetPysparkJob")
    def reset_pyspark_job(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPysparkJob", []))

    @jsii.member(jsii_name="resetScheduling")
    def reset_scheduling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduling", []))

    @jsii.member(jsii_name="resetSparkJob")
    def reset_spark_job(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkJob", []))

    @jsii.member(jsii_name="resetSparkRJob")
    def reset_spark_r_job(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkRJob", []))

    @jsii.member(jsii_name="resetSparkSqlJob")
    def reset_spark_sql_job(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkSqlJob", []))

    @builtins.property
    @jsii.member(jsii_name="hadoopJob")
    def hadoop_job(self) -> DataprocWorkflowTemplateJobsHadoopJobOutputReference:
        return typing.cast(DataprocWorkflowTemplateJobsHadoopJobOutputReference, jsii.get(self, "hadoopJob"))

    @builtins.property
    @jsii.member(jsii_name="hiveJob")
    def hive_job(self) -> DataprocWorkflowTemplateJobsHiveJobOutputReference:
        return typing.cast(DataprocWorkflowTemplateJobsHiveJobOutputReference, jsii.get(self, "hiveJob"))

    @builtins.property
    @jsii.member(jsii_name="pigJob")
    def pig_job(self) -> "DataprocWorkflowTemplateJobsPigJobOutputReference":
        return typing.cast("DataprocWorkflowTemplateJobsPigJobOutputReference", jsii.get(self, "pigJob"))

    @builtins.property
    @jsii.member(jsii_name="prestoJob")
    def presto_job(self) -> "DataprocWorkflowTemplateJobsPrestoJobOutputReference":
        return typing.cast("DataprocWorkflowTemplateJobsPrestoJobOutputReference", jsii.get(self, "prestoJob"))

    @builtins.property
    @jsii.member(jsii_name="pysparkJob")
    def pyspark_job(self) -> "DataprocWorkflowTemplateJobsPysparkJobOutputReference":
        return typing.cast("DataprocWorkflowTemplateJobsPysparkJobOutputReference", jsii.get(self, "pysparkJob"))

    @builtins.property
    @jsii.member(jsii_name="scheduling")
    def scheduling(self) -> "DataprocWorkflowTemplateJobsSchedulingOutputReference":
        return typing.cast("DataprocWorkflowTemplateJobsSchedulingOutputReference", jsii.get(self, "scheduling"))

    @builtins.property
    @jsii.member(jsii_name="sparkJob")
    def spark_job(self) -> "DataprocWorkflowTemplateJobsSparkJobOutputReference":
        return typing.cast("DataprocWorkflowTemplateJobsSparkJobOutputReference", jsii.get(self, "sparkJob"))

    @builtins.property
    @jsii.member(jsii_name="sparkRJob")
    def spark_r_job(self) -> "DataprocWorkflowTemplateJobsSparkRJobOutputReference":
        return typing.cast("DataprocWorkflowTemplateJobsSparkRJobOutputReference", jsii.get(self, "sparkRJob"))

    @builtins.property
    @jsii.member(jsii_name="sparkSqlJob")
    def spark_sql_job(self) -> "DataprocWorkflowTemplateJobsSparkSqlJobOutputReference":
        return typing.cast("DataprocWorkflowTemplateJobsSparkSqlJobOutputReference", jsii.get(self, "sparkSqlJob"))

    @builtins.property
    @jsii.member(jsii_name="hadoopJobInput")
    def hadoop_job_input(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateJobsHadoopJob]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsHadoopJob], jsii.get(self, "hadoopJobInput"))

    @builtins.property
    @jsii.member(jsii_name="hiveJobInput")
    def hive_job_input(self) -> typing.Optional[DataprocWorkflowTemplateJobsHiveJob]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsHiveJob], jsii.get(self, "hiveJobInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="pigJobInput")
    def pig_job_input(self) -> typing.Optional["DataprocWorkflowTemplateJobsPigJob"]:
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsPigJob"], jsii.get(self, "pigJobInput"))

    @builtins.property
    @jsii.member(jsii_name="prerequisiteStepIdsInput")
    def prerequisite_step_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "prerequisiteStepIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="prestoJobInput")
    def presto_job_input(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateJobsPrestoJob"]:
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsPrestoJob"], jsii.get(self, "prestoJobInput"))

    @builtins.property
    @jsii.member(jsii_name="pysparkJobInput")
    def pyspark_job_input(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateJobsPysparkJob"]:
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsPysparkJob"], jsii.get(self, "pysparkJobInput"))

    @builtins.property
    @jsii.member(jsii_name="schedulingInput")
    def scheduling_input(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateJobsScheduling"]:
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsScheduling"], jsii.get(self, "schedulingInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkJobInput")
    def spark_job_input(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateJobsSparkJob"]:
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsSparkJob"], jsii.get(self, "sparkJobInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkRJobInput")
    def spark_r_job_input(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateJobsSparkRJob"]:
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsSparkRJob"], jsii.get(self, "sparkRJobInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkSqlJobInput")
    def spark_sql_job_input(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateJobsSparkSqlJob"]:
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsSparkSqlJob"], jsii.get(self, "sparkSqlJobInput"))

    @builtins.property
    @jsii.member(jsii_name="stepIdInput")
    def step_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stepIdInput"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5614fcd8fd1c7f3e88485acce76dfc53acc4a263d840ea791e386dadbb43280f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prerequisiteStepIds")
    def prerequisite_step_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "prerequisiteStepIds"))

    @prerequisite_step_ids.setter
    def prerequisite_step_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__149d710609cd1975f56f3fe6bfc1b5a31ad8ec1804b1847ab083f5b8cfb6ad45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prerequisiteStepIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stepId")
    def step_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stepId"))

    @step_id.setter
    def step_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceb207187755c8ff30bf28c194628073cea2a949aacfcfb6346a37f6bc9201fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stepId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplateJobs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplateJobs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplateJobs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72f2c78edd8f0fb36250e5db924b975a3afc8f9ee8534a439e7eff1b8bce0762)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsPigJob",
    jsii_struct_bases=[],
    name_mapping={
        "continue_on_failure": "continueOnFailure",
        "jar_file_uris": "jarFileUris",
        "logging_config": "loggingConfig",
        "properties": "properties",
        "query_file_uri": "queryFileUri",
        "query_list": "queryList",
        "script_variables": "scriptVariables",
    },
)
class DataprocWorkflowTemplateJobsPigJob:
    def __init__(
        self,
        *,
        continue_on_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsPigJobLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        query_file_uri: typing.Optional[builtins.str] = None,
        query_list: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsPigJobQueryListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
        script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param continue_on_failure: Optional. Whether to continue executing queries if a query fails. The default value is ``false``. Setting to ``true`` can be useful when executing independent parallel queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#continue_on_failure DataprocWorkflowTemplate#continue_on_failure}
        :param jar_file_uris: Optional. HCFS URIs of jar files to add to the CLASSPATH of the Pig Client and Hadoop MapReduce (MR) tasks. Can contain Pig UDFs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#jar_file_uris DataprocWorkflowTemplate#jar_file_uris}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#logging_config DataprocWorkflowTemplate#logging_config}
        :param properties: Optional. A mapping of property names to values, used to configure Pig. Properties that conflict with values set by the Dataproc API may be overwritten. Can include properties set in /etc/hadoop/conf/*-site.xml, /etc/pig/conf/pig.properties, and classes in user code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        :param query_file_uri: The HCFS URI of the script that contains the Pig queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_file_uri DataprocWorkflowTemplate#query_file_uri}
        :param query_list: query_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_list DataprocWorkflowTemplate#query_list}
        :param script_variables: Optional. Mapping of query variable names to values (equivalent to the Pig command: ``name=[value]``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#script_variables DataprocWorkflowTemplate#script_variables}
        '''
        if isinstance(logging_config, dict):
            logging_config = DataprocWorkflowTemplateJobsPigJobLoggingConfig(**logging_config)
        if isinstance(query_list, dict):
            query_list = DataprocWorkflowTemplateJobsPigJobQueryListStruct(**query_list)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d246fa2df3d1d2e3f9ee84209c93a27c27485bf5af0202671e76653d8eed6ff4)
            check_type(argname="argument continue_on_failure", value=continue_on_failure, expected_type=type_hints["continue_on_failure"])
            check_type(argname="argument jar_file_uris", value=jar_file_uris, expected_type=type_hints["jar_file_uris"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument query_file_uri", value=query_file_uri, expected_type=type_hints["query_file_uri"])
            check_type(argname="argument query_list", value=query_list, expected_type=type_hints["query_list"])
            check_type(argname="argument script_variables", value=script_variables, expected_type=type_hints["script_variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if continue_on_failure is not None:
            self._values["continue_on_failure"] = continue_on_failure
        if jar_file_uris is not None:
            self._values["jar_file_uris"] = jar_file_uris
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if properties is not None:
            self._values["properties"] = properties
        if query_file_uri is not None:
            self._values["query_file_uri"] = query_file_uri
        if query_list is not None:
            self._values["query_list"] = query_list
        if script_variables is not None:
            self._values["script_variables"] = script_variables

    @builtins.property
    def continue_on_failure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Whether to continue executing queries if a query fails. The default value is ``false``. Setting to ``true`` can be useful when executing independent parallel queries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#continue_on_failure DataprocWorkflowTemplate#continue_on_failure}
        '''
        result = self._values.get("continue_on_failure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def jar_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        HCFS URIs of jar files to add to the CLASSPATH of the Pig Client and Hadoop MapReduce (MR) tasks. Can contain Pig UDFs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#jar_file_uris DataprocWorkflowTemplate#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateJobsPigJobLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#logging_config DataprocWorkflowTemplate#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsPigJobLoggingConfig"], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        A mapping of property names to values, used to configure Pig. Properties that conflict with values set by the Dataproc API may be overwritten. Can include properties set in /etc/hadoop/conf/*-site.xml, /etc/pig/conf/pig.properties, and classes in user code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def query_file_uri(self) -> typing.Optional[builtins.str]:
        '''The HCFS URI of the script that contains the Pig queries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_file_uri DataprocWorkflowTemplate#query_file_uri}
        '''
        result = self._values.get("query_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_list(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateJobsPigJobQueryListStruct"]:
        '''query_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_list DataprocWorkflowTemplate#query_list}
        '''
        result = self._values.get("query_list")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsPigJobQueryListStruct"], result)

    @builtins.property
    def script_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. Mapping of query variable names to values (equivalent to the Pig command: ``name=[value]``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#script_variables DataprocWorkflowTemplate#script_variables}
        '''
        result = self._values.get("script_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateJobsPigJob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsPigJobLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"driver_log_levels": "driverLogLevels"},
)
class DataprocWorkflowTemplateJobsPigJobLoggingConfig:
    def __init__(
        self,
        *,
        driver_log_levels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param driver_log_levels: The per-package log levels for the driver. This may include "root" package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#driver_log_levels DataprocWorkflowTemplate#driver_log_levels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e3f46064852264f395f34d3195f3c3267f3673b9f35a5ef584244ae598be7f7)
            check_type(argname="argument driver_log_levels", value=driver_log_levels, expected_type=type_hints["driver_log_levels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if driver_log_levels is not None:
            self._values["driver_log_levels"] = driver_log_levels

    @builtins.property
    def driver_log_levels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The per-package log levels for the driver.

        This may include "root" package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#driver_log_levels DataprocWorkflowTemplate#driver_log_levels}
        '''
        result = self._values.get("driver_log_levels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateJobsPigJobLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplateJobsPigJobLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsPigJobLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a72415eddee1ce67f1864410184cc7fcc90f395895005d9480b561937772ac66)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDriverLogLevels")
    def reset_driver_log_levels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDriverLogLevels", []))

    @builtins.property
    @jsii.member(jsii_name="driverLogLevelsInput")
    def driver_log_levels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "driverLogLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="driverLogLevels")
    def driver_log_levels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "driverLogLevels"))

    @driver_log_levels.setter
    def driver_log_levels(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a30fa73b2389adb699429ca7ac6b36a3f7d1049d76389d883c076e3ee47ef841)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverLogLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateJobsPigJobLoggingConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsPigJobLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateJobsPigJobLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab8d57e4455a75706d07f84043663089c634df51e749291b000bb1344b2b150)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplateJobsPigJobOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsPigJobOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d3cecb366f26a903b9434dd8d912901c6271048100132950ffa527c63850c1e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        driver_log_levels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param driver_log_levels: The per-package log levels for the driver. This may include "root" package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#driver_log_levels DataprocWorkflowTemplate#driver_log_levels}
        '''
        value = DataprocWorkflowTemplateJobsPigJobLoggingConfig(
            driver_log_levels=driver_log_levels
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

    @jsii.member(jsii_name="putQueryList")
    def put_query_list(self, *, queries: typing.Sequence[builtins.str]) -> None:
        '''
        :param queries: Required. The queries to execute. You do not need to end a query expression with a semicolon. Multiple queries can be specified in one string by separating each with a semicolon. Here is an example of a Dataproc API snippet that uses a QueryList to specify a HiveJob: "hiveJob": { "queryList": { "queries": [ "query1", "query2", "query3;query4", ] } } Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#queries DataprocWorkflowTemplate#queries}
        '''
        value = DataprocWorkflowTemplateJobsPigJobQueryListStruct(queries=queries)

        return typing.cast(None, jsii.invoke(self, "putQueryList", [value]))

    @jsii.member(jsii_name="resetContinueOnFailure")
    def reset_continue_on_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContinueOnFailure", []))

    @jsii.member(jsii_name="resetJarFileUris")
    def reset_jar_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJarFileUris", []))

    @jsii.member(jsii_name="resetLoggingConfig")
    def reset_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfig", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @jsii.member(jsii_name="resetQueryFileUri")
    def reset_query_file_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryFileUri", []))

    @jsii.member(jsii_name="resetQueryList")
    def reset_query_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryList", []))

    @jsii.member(jsii_name="resetScriptVariables")
    def reset_script_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScriptVariables", []))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(
        self,
    ) -> DataprocWorkflowTemplateJobsPigJobLoggingConfigOutputReference:
        return typing.cast(DataprocWorkflowTemplateJobsPigJobLoggingConfigOutputReference, jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="queryList")
    def query_list(
        self,
    ) -> "DataprocWorkflowTemplateJobsPigJobQueryListStructOutputReference":
        return typing.cast("DataprocWorkflowTemplateJobsPigJobQueryListStructOutputReference", jsii.get(self, "queryList"))

    @builtins.property
    @jsii.member(jsii_name="continueOnFailureInput")
    def continue_on_failure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "continueOnFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="jarFileUrisInput")
    def jar_file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jarFileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfigInput")
    def logging_config_input(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateJobsPigJobLoggingConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsPigJobLoggingConfig], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="queryFileUriInput")
    def query_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="queryListInput")
    def query_list_input(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateJobsPigJobQueryListStruct"]:
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsPigJobQueryListStruct"], jsii.get(self, "queryListInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptVariablesInput")
    def script_variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "scriptVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="continueOnFailure")
    def continue_on_failure(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "continueOnFailure"))

    @continue_on_failure.setter
    def continue_on_failure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__709624242e832269495c809571926fd53e32dd427f53eca4b387ed08259456ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "continueOnFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jarFileUris")
    def jar_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jarFileUris"))

    @jar_file_uris.setter
    def jar_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__895e270faf9720e5ae60b7e2db879834aee485853264ad326f016cb17769d667)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5169d836fbb6a47a76f940862bb743e62ca4871bbee9e1f1eef29758b7aa29f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryFileUri")
    def query_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryFileUri"))

    @query_file_uri.setter
    def query_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7728a1d8581717494354ce5f9733b7b96d3a6c72f23036aff0a364b64de48651)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scriptVariables")
    def script_variables(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "scriptVariables"))

    @script_variables.setter
    def script_variables(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b92c813ae48f54b6915e27ec571ed27add20134b26d197f4b6778d5d884ae75a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocWorkflowTemplateJobsPigJob]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsPigJob], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateJobsPigJob],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0632df1daf907133d726fb62c1d1dc059c848f5e4f47b4a2b114e5faada9483a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsPigJobQueryListStruct",
    jsii_struct_bases=[],
    name_mapping={"queries": "queries"},
)
class DataprocWorkflowTemplateJobsPigJobQueryListStruct:
    def __init__(self, *, queries: typing.Sequence[builtins.str]) -> None:
        '''
        :param queries: Required. The queries to execute. You do not need to end a query expression with a semicolon. Multiple queries can be specified in one string by separating each with a semicolon. Here is an example of a Dataproc API snippet that uses a QueryList to specify a HiveJob: "hiveJob": { "queryList": { "queries": [ "query1", "query2", "query3;query4", ] } } Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#queries DataprocWorkflowTemplate#queries}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24e7fb35447ec25bca10b10cd29def897ab680da505b7797ce58514a49e256d0)
            check_type(argname="argument queries", value=queries, expected_type=type_hints["queries"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "queries": queries,
        }

    @builtins.property
    def queries(self) -> typing.List[builtins.str]:
        '''Required.

        The queries to execute. You do not need to end a query expression with a semicolon. Multiple queries can be specified in one string by separating each with a semicolon. Here is an example of a Dataproc API snippet that uses a QueryList to specify a HiveJob: "hiveJob": { "queryList": { "queries": [ "query1", "query2", "query3;query4", ] } }

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#queries DataprocWorkflowTemplate#queries}
        '''
        result = self._values.get("queries")
        assert result is not None, "Required property 'queries' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateJobsPigJobQueryListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplateJobsPigJobQueryListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsPigJobQueryListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ec9dda42a5e0c4279745829d39cf9aa07dbc39ddf53133604e22d5d910e5823)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="queriesInput")
    def queries_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queriesInput"))

    @builtins.property
    @jsii.member(jsii_name="queries")
    def queries(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queries"))

    @queries.setter
    def queries(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4a495bdb029a21c5a5ffd4efcda221584886e7301ed09657f20d03d460d16cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateJobsPigJobQueryListStruct]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsPigJobQueryListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateJobsPigJobQueryListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97fcc008a8ddafe406c5049908086693be0b83a1bd5c8eb89bb18c53d6fe3fc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsPrestoJob",
    jsii_struct_bases=[],
    name_mapping={
        "client_tags": "clientTags",
        "continue_on_failure": "continueOnFailure",
        "logging_config": "loggingConfig",
        "output_format": "outputFormat",
        "properties": "properties",
        "query_file_uri": "queryFileUri",
        "query_list": "queryList",
    },
)
class DataprocWorkflowTemplateJobsPrestoJob:
    def __init__(
        self,
        *,
        client_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        continue_on_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        logging_config: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsPrestoJobLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        output_format: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        query_file_uri: typing.Optional[builtins.str] = None,
        query_list: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsPrestoJobQueryListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_tags: Optional. Presto client tags to attach to this query. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#client_tags DataprocWorkflowTemplate#client_tags}
        :param continue_on_failure: Optional. Whether to continue executing queries if a query fails. The default value is ``false``. Setting to ``true`` can be useful when executing independent parallel queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#continue_on_failure DataprocWorkflowTemplate#continue_on_failure}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#logging_config DataprocWorkflowTemplate#logging_config}
        :param output_format: Optional. The format in which query output will be displayed. See the Presto documentation for supported output formats. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#output_format DataprocWorkflowTemplate#output_format}
        :param properties: Optional. A mapping of property names to values. Used to set Presto `session properties <https://prestodb.io/docs/current/sql/set-session.html>`_ Equivalent to using the --session flag in the Presto CLI Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        :param query_file_uri: The HCFS URI of the script that contains SQL queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_file_uri DataprocWorkflowTemplate#query_file_uri}
        :param query_list: query_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_list DataprocWorkflowTemplate#query_list}
        '''
        if isinstance(logging_config, dict):
            logging_config = DataprocWorkflowTemplateJobsPrestoJobLoggingConfig(**logging_config)
        if isinstance(query_list, dict):
            query_list = DataprocWorkflowTemplateJobsPrestoJobQueryListStruct(**query_list)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03c5c7c3460f89d594225a5853097b340bd804f839c94b3990f54ab221eb0c18)
            check_type(argname="argument client_tags", value=client_tags, expected_type=type_hints["client_tags"])
            check_type(argname="argument continue_on_failure", value=continue_on_failure, expected_type=type_hints["continue_on_failure"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument output_format", value=output_format, expected_type=type_hints["output_format"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument query_file_uri", value=query_file_uri, expected_type=type_hints["query_file_uri"])
            check_type(argname="argument query_list", value=query_list, expected_type=type_hints["query_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_tags is not None:
            self._values["client_tags"] = client_tags
        if continue_on_failure is not None:
            self._values["continue_on_failure"] = continue_on_failure
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if output_format is not None:
            self._values["output_format"] = output_format
        if properties is not None:
            self._values["properties"] = properties
        if query_file_uri is not None:
            self._values["query_file_uri"] = query_file_uri
        if query_list is not None:
            self._values["query_list"] = query_list

    @builtins.property
    def client_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. Presto client tags to attach to this query.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#client_tags DataprocWorkflowTemplate#client_tags}
        '''
        result = self._values.get("client_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def continue_on_failure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Whether to continue executing queries if a query fails. The default value is ``false``. Setting to ``true`` can be useful when executing independent parallel queries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#continue_on_failure DataprocWorkflowTemplate#continue_on_failure}
        '''
        result = self._values.get("continue_on_failure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateJobsPrestoJobLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#logging_config DataprocWorkflowTemplate#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsPrestoJobLoggingConfig"], result)

    @builtins.property
    def output_format(self) -> typing.Optional[builtins.str]:
        '''Optional. The format in which query output will be displayed. See the Presto documentation for supported output formats.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#output_format DataprocWorkflowTemplate#output_format}
        '''
        result = self._values.get("output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        A mapping of property names to values. Used to set Presto `session properties <https://prestodb.io/docs/current/sql/set-session.html>`_ Equivalent to using the --session flag in the Presto CLI

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def query_file_uri(self) -> typing.Optional[builtins.str]:
        '''The HCFS URI of the script that contains SQL queries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_file_uri DataprocWorkflowTemplate#query_file_uri}
        '''
        result = self._values.get("query_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_list(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateJobsPrestoJobQueryListStruct"]:
        '''query_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_list DataprocWorkflowTemplate#query_list}
        '''
        result = self._values.get("query_list")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsPrestoJobQueryListStruct"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateJobsPrestoJob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsPrestoJobLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"driver_log_levels": "driverLogLevels"},
)
class DataprocWorkflowTemplateJobsPrestoJobLoggingConfig:
    def __init__(
        self,
        *,
        driver_log_levels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param driver_log_levels: The per-package log levels for the driver. This may include "root" package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#driver_log_levels DataprocWorkflowTemplate#driver_log_levels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86493b92af14208f3ed21348de0cd9fafe0925dbb07da668c97a58cae4463eb6)
            check_type(argname="argument driver_log_levels", value=driver_log_levels, expected_type=type_hints["driver_log_levels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if driver_log_levels is not None:
            self._values["driver_log_levels"] = driver_log_levels

    @builtins.property
    def driver_log_levels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The per-package log levels for the driver.

        This may include "root" package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#driver_log_levels DataprocWorkflowTemplate#driver_log_levels}
        '''
        result = self._values.get("driver_log_levels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateJobsPrestoJobLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplateJobsPrestoJobLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsPrestoJobLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b62f24de4aab44a82912b044abcd4763f42cb19ef4785822992424262de112d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDriverLogLevels")
    def reset_driver_log_levels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDriverLogLevels", []))

    @builtins.property
    @jsii.member(jsii_name="driverLogLevelsInput")
    def driver_log_levels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "driverLogLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="driverLogLevels")
    def driver_log_levels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "driverLogLevels"))

    @driver_log_levels.setter
    def driver_log_levels(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7371cf999882470dcef470fd88fca58d4140133d404675e6499056b4ff2e5374)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverLogLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateJobsPrestoJobLoggingConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsPrestoJobLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateJobsPrestoJobLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f48ff54e3649aaf19c589ac4ca8d102d8d2983e82b5ba40d3f2ed52b606b584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplateJobsPrestoJobOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsPrestoJobOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dffe6ab95d3bcc61e2e2b7ba2f7ec1416b74e513a960e02523f51d7b74613a84)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        driver_log_levels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param driver_log_levels: The per-package log levels for the driver. This may include "root" package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#driver_log_levels DataprocWorkflowTemplate#driver_log_levels}
        '''
        value = DataprocWorkflowTemplateJobsPrestoJobLoggingConfig(
            driver_log_levels=driver_log_levels
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

    @jsii.member(jsii_name="putQueryList")
    def put_query_list(self, *, queries: typing.Sequence[builtins.str]) -> None:
        '''
        :param queries: Required. The queries to execute. You do not need to end a query expression with a semicolon. Multiple queries can be specified in one string by separating each with a semicolon. Here is an example of a Dataproc API snippet that uses a QueryList to specify a HiveJob: "hiveJob": { "queryList": { "queries": [ "query1", "query2", "query3;query4", ] } } Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#queries DataprocWorkflowTemplate#queries}
        '''
        value = DataprocWorkflowTemplateJobsPrestoJobQueryListStruct(queries=queries)

        return typing.cast(None, jsii.invoke(self, "putQueryList", [value]))

    @jsii.member(jsii_name="resetClientTags")
    def reset_client_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientTags", []))

    @jsii.member(jsii_name="resetContinueOnFailure")
    def reset_continue_on_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContinueOnFailure", []))

    @jsii.member(jsii_name="resetLoggingConfig")
    def reset_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfig", []))

    @jsii.member(jsii_name="resetOutputFormat")
    def reset_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputFormat", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @jsii.member(jsii_name="resetQueryFileUri")
    def reset_query_file_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryFileUri", []))

    @jsii.member(jsii_name="resetQueryList")
    def reset_query_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryList", []))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(
        self,
    ) -> DataprocWorkflowTemplateJobsPrestoJobLoggingConfigOutputReference:
        return typing.cast(DataprocWorkflowTemplateJobsPrestoJobLoggingConfigOutputReference, jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="queryList")
    def query_list(
        self,
    ) -> "DataprocWorkflowTemplateJobsPrestoJobQueryListStructOutputReference":
        return typing.cast("DataprocWorkflowTemplateJobsPrestoJobQueryListStructOutputReference", jsii.get(self, "queryList"))

    @builtins.property
    @jsii.member(jsii_name="clientTagsInput")
    def client_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "clientTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="continueOnFailureInput")
    def continue_on_failure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "continueOnFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfigInput")
    def logging_config_input(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateJobsPrestoJobLoggingConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsPrestoJobLoggingConfig], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="outputFormatInput")
    def output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="queryFileUriInput")
    def query_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="queryListInput")
    def query_list_input(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateJobsPrestoJobQueryListStruct"]:
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsPrestoJobQueryListStruct"], jsii.get(self, "queryListInput"))

    @builtins.property
    @jsii.member(jsii_name="clientTags")
    def client_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "clientTags"))

    @client_tags.setter
    def client_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24a79e08a2dc7b4825bb02bdc2bc617d3b0b43109bf206b300efc75c96b20d26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="continueOnFailure")
    def continue_on_failure(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "continueOnFailure"))

    @continue_on_failure.setter
    def continue_on_failure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75125443181f87a79cfa8c1c63563dc294dbe7cd3fb6946bb3bdbc5eb7597675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "continueOnFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputFormat")
    def output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputFormat"))

    @output_format.setter
    def output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acc48cd95932b01b36c1eb1372d2804eaee0e35d2463f8d9afc5eea75efac37a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a93496507a0cb656330ebf092ae4469950d587731696a9c6d1be54a1c68ccff9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryFileUri")
    def query_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryFileUri"))

    @query_file_uri.setter
    def query_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e315c8ea464ff00f083ecab149aad344515afda48355dde4cd2e00f3b88b2b61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocWorkflowTemplateJobsPrestoJob]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsPrestoJob], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateJobsPrestoJob],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fde21aff89d5c7025ad822808c34d9e79ba073c967fe1bb3ae58e519639dc1d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsPrestoJobQueryListStruct",
    jsii_struct_bases=[],
    name_mapping={"queries": "queries"},
)
class DataprocWorkflowTemplateJobsPrestoJobQueryListStruct:
    def __init__(self, *, queries: typing.Sequence[builtins.str]) -> None:
        '''
        :param queries: Required. The queries to execute. You do not need to end a query expression with a semicolon. Multiple queries can be specified in one string by separating each with a semicolon. Here is an example of a Dataproc API snippet that uses a QueryList to specify a HiveJob: "hiveJob": { "queryList": { "queries": [ "query1", "query2", "query3;query4", ] } } Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#queries DataprocWorkflowTemplate#queries}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f22fcb1dd828c5046c366fb52d9fa5a54b8857761e7cc8fcd35ba9b4c735ebcf)
            check_type(argname="argument queries", value=queries, expected_type=type_hints["queries"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "queries": queries,
        }

    @builtins.property
    def queries(self) -> typing.List[builtins.str]:
        '''Required.

        The queries to execute. You do not need to end a query expression with a semicolon. Multiple queries can be specified in one string by separating each with a semicolon. Here is an example of a Dataproc API snippet that uses a QueryList to specify a HiveJob: "hiveJob": { "queryList": { "queries": [ "query1", "query2", "query3;query4", ] } }

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#queries DataprocWorkflowTemplate#queries}
        '''
        result = self._values.get("queries")
        assert result is not None, "Required property 'queries' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateJobsPrestoJobQueryListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplateJobsPrestoJobQueryListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsPrestoJobQueryListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__634ddc7d037c52825c7c2ef95152f6554c568fe1eed6c118043dbf8c56f219c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="queriesInput")
    def queries_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queriesInput"))

    @builtins.property
    @jsii.member(jsii_name="queries")
    def queries(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queries"))

    @queries.setter
    def queries(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aea5a3ec8fe7b9596afb1c93b257c469530af000aecd88729bd416df7c6f3c2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateJobsPrestoJobQueryListStruct]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsPrestoJobQueryListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateJobsPrestoJobQueryListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf3f3f1c7f53b6b3a3b69eca79fce4e2b3f825f0ec5110fa06ed2376ea9d8ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsPysparkJob",
    jsii_struct_bases=[],
    name_mapping={
        "main_python_file_uri": "mainPythonFileUri",
        "archive_uris": "archiveUris",
        "args": "args",
        "file_uris": "fileUris",
        "jar_file_uris": "jarFileUris",
        "logging_config": "loggingConfig",
        "properties": "properties",
        "python_file_uris": "pythonFileUris",
    },
)
class DataprocWorkflowTemplateJobsPysparkJob:
    def __init__(
        self,
        *,
        main_python_file_uri: builtins.str,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsPysparkJobLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        python_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param main_python_file_uri: Required. The HCFS URI of the main Python file to use as the driver. Must be a .py file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#main_python_file_uri DataprocWorkflowTemplate#main_python_file_uri}
        :param archive_uris: Optional. HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#archive_uris DataprocWorkflowTemplate#archive_uris}
        :param args: Optional. The arguments to pass to the driver. Do not include arguments, such as ``--conf``, that can be set as job properties, since a collision may occur that causes an incorrect job submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#args DataprocWorkflowTemplate#args}
        :param file_uris: Optional. HCFS URIs of files to be placed in the working directory of each executor. Useful for naively parallel tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#file_uris DataprocWorkflowTemplate#file_uris}
        :param jar_file_uris: Optional. HCFS URIs of jar files to add to the CLASSPATHs of the Python driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#jar_file_uris DataprocWorkflowTemplate#jar_file_uris}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#logging_config DataprocWorkflowTemplate#logging_config}
        :param properties: Optional. A mapping of property names to values, used to configure PySpark. Properties that conflict with values set by the Dataproc API may be overwritten. Can include properties set in /etc/spark/conf/spark-defaults.conf and classes in user code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        :param python_file_uris: Optional. HCFS file URIs of Python files to pass to the PySpark framework. Supported file types: .py, .egg, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#python_file_uris DataprocWorkflowTemplate#python_file_uris}
        '''
        if isinstance(logging_config, dict):
            logging_config = DataprocWorkflowTemplateJobsPysparkJobLoggingConfig(**logging_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e27f847c6a1e2a32ffb33b12df4bb4b902d4fe3624f36f5b5b1602639aeb9d6)
            check_type(argname="argument main_python_file_uri", value=main_python_file_uri, expected_type=type_hints["main_python_file_uri"])
            check_type(argname="argument archive_uris", value=archive_uris, expected_type=type_hints["archive_uris"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument file_uris", value=file_uris, expected_type=type_hints["file_uris"])
            check_type(argname="argument jar_file_uris", value=jar_file_uris, expected_type=type_hints["jar_file_uris"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument python_file_uris", value=python_file_uris, expected_type=type_hints["python_file_uris"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "main_python_file_uri": main_python_file_uri,
        }
        if archive_uris is not None:
            self._values["archive_uris"] = archive_uris
        if args is not None:
            self._values["args"] = args
        if file_uris is not None:
            self._values["file_uris"] = file_uris
        if jar_file_uris is not None:
            self._values["jar_file_uris"] = jar_file_uris
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if properties is not None:
            self._values["properties"] = properties
        if python_file_uris is not None:
            self._values["python_file_uris"] = python_file_uris

    @builtins.property
    def main_python_file_uri(self) -> builtins.str:
        '''Required. The HCFS URI of the main Python file to use as the driver. Must be a .py file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#main_python_file_uri DataprocWorkflowTemplate#main_python_file_uri}
        '''
        result = self._values.get("main_python_file_uri")
        assert result is not None, "Required property 'main_python_file_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def archive_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#archive_uris DataprocWorkflowTemplate#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        The arguments to pass to the driver. Do not include arguments, such as ``--conf``, that can be set as job properties, since a collision may occur that causes an incorrect job submission.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#args DataprocWorkflowTemplate#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        HCFS URIs of files to be placed in the working directory of each executor. Useful for naively parallel tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#file_uris DataprocWorkflowTemplate#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jar_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. HCFS URIs of jar files to add to the CLASSPATHs of the Python driver and tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#jar_file_uris DataprocWorkflowTemplate#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateJobsPysparkJobLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#logging_config DataprocWorkflowTemplate#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsPysparkJobLoggingConfig"], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        A mapping of property names to values, used to configure PySpark. Properties that conflict with values set by the Dataproc API may be overwritten. Can include properties set in /etc/spark/conf/spark-defaults.conf and classes in user code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def python_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        HCFS file URIs of Python files to pass to the PySpark framework. Supported file types: .py, .egg, and .zip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#python_file_uris DataprocWorkflowTemplate#python_file_uris}
        '''
        result = self._values.get("python_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateJobsPysparkJob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsPysparkJobLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"driver_log_levels": "driverLogLevels"},
)
class DataprocWorkflowTemplateJobsPysparkJobLoggingConfig:
    def __init__(
        self,
        *,
        driver_log_levels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param driver_log_levels: The per-package log levels for the driver. This may include "root" package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#driver_log_levels DataprocWorkflowTemplate#driver_log_levels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b6eafad1e760e83c652beb434f25cca62cddc60c913384ff5f4880853c771a6)
            check_type(argname="argument driver_log_levels", value=driver_log_levels, expected_type=type_hints["driver_log_levels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if driver_log_levels is not None:
            self._values["driver_log_levels"] = driver_log_levels

    @builtins.property
    def driver_log_levels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The per-package log levels for the driver.

        This may include "root" package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#driver_log_levels DataprocWorkflowTemplate#driver_log_levels}
        '''
        result = self._values.get("driver_log_levels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateJobsPysparkJobLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplateJobsPysparkJobLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsPysparkJobLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__396c67149c271e8220006e6c6a911567d4951968f27ca54084ac56ecdf66035c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDriverLogLevels")
    def reset_driver_log_levels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDriverLogLevels", []))

    @builtins.property
    @jsii.member(jsii_name="driverLogLevelsInput")
    def driver_log_levels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "driverLogLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="driverLogLevels")
    def driver_log_levels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "driverLogLevels"))

    @driver_log_levels.setter
    def driver_log_levels(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d71f29374d009494e73cd8ce42e9d881825e69a99ee5c33935fb95f1bc24d62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverLogLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateJobsPysparkJobLoggingConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsPysparkJobLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateJobsPysparkJobLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__234e3fcfdcae736ccc4dc7d7b8dd28bc0faecf23d0da54134528faf838cb458e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplateJobsPysparkJobOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsPysparkJobOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2de970a25747733be1c91239c756e70efe11cb320ad5e8a81bd02985b0cc139)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        driver_log_levels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param driver_log_levels: The per-package log levels for the driver. This may include "root" package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#driver_log_levels DataprocWorkflowTemplate#driver_log_levels}
        '''
        value = DataprocWorkflowTemplateJobsPysparkJobLoggingConfig(
            driver_log_levels=driver_log_levels
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

    @jsii.member(jsii_name="resetArchiveUris")
    def reset_archive_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchiveUris", []))

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetFileUris")
    def reset_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileUris", []))

    @jsii.member(jsii_name="resetJarFileUris")
    def reset_jar_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJarFileUris", []))

    @jsii.member(jsii_name="resetLoggingConfig")
    def reset_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfig", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @jsii.member(jsii_name="resetPythonFileUris")
    def reset_python_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPythonFileUris", []))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(
        self,
    ) -> DataprocWorkflowTemplateJobsPysparkJobLoggingConfigOutputReference:
        return typing.cast(DataprocWorkflowTemplateJobsPysparkJobLoggingConfigOutputReference, jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="archiveUrisInput")
    def archive_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "archiveUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="fileUrisInput")
    def file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "fileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="jarFileUrisInput")
    def jar_file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jarFileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfigInput")
    def logging_config_input(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateJobsPysparkJobLoggingConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsPysparkJobLoggingConfig], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="mainPythonFileUriInput")
    def main_python_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mainPythonFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="pythonFileUrisInput")
    def python_file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pythonFileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="archiveUris")
    def archive_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "archiveUris"))

    @archive_uris.setter
    def archive_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae1326d4ac711cec314a4216374ffa7122b5c75b536e5144d7c78d554191d67e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb8442e1d942f1bee50c187f78bf6bdaac0e1061fee3f434fc12e2e05783f8c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4be511ba1f217a10d8ea962c073b624219476ebdd76b5b1f4a31f9a47d16adbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jarFileUris")
    def jar_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jarFileUris"))

    @jar_file_uris.setter
    def jar_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16cba5d1399821b992b6da0607b544109f023e18fb266de6bd39fcdfd3790eb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainPythonFileUri")
    def main_python_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainPythonFileUri"))

    @main_python_file_uri.setter
    def main_python_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19732f1002c5a97af0d1a24609cab151614a0cc7c457fbcdc9853adb19780a66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainPythonFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f959532d17220837ba95fa44375767e517bdb86be62ed247d663bdb54238d403)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pythonFileUris")
    def python_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pythonFileUris"))

    @python_file_uris.setter
    def python_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cc79695b8ff98424f21eaa921e2ad9a52396f2186adae7b187d40d3ef97f9a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pythonFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocWorkflowTemplateJobsPysparkJob]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsPysparkJob], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateJobsPysparkJob],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85dbfb002f20e5a4ceb0e0f188a43d049af3c93b67db7053008d2ba251bfd9bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsScheduling",
    jsii_struct_bases=[],
    name_mapping={
        "max_failures_per_hour": "maxFailuresPerHour",
        "max_failures_total": "maxFailuresTotal",
    },
)
class DataprocWorkflowTemplateJobsScheduling:
    def __init__(
        self,
        *,
        max_failures_per_hour: typing.Optional[jsii.Number] = None,
        max_failures_total: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_failures_per_hour: Optional. Maximum number of times per hour a driver may be restarted as a result of driver exiting with non-zero code before job is reported failed. A job may be reported as thrashing if driver exits with non-zero code 4 times within 10 minute window. Maximum value is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#max_failures_per_hour DataprocWorkflowTemplate#max_failures_per_hour}
        :param max_failures_total: Optional. Maximum number of times in total a driver may be restarted as a result of driver exiting with non-zero code before job is reported failed. Maximum value is 240. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#max_failures_total DataprocWorkflowTemplate#max_failures_total}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__573546374997b26b384569f3a2c3e571c61d64d304af25ab42adaac2af5e79f9)
            check_type(argname="argument max_failures_per_hour", value=max_failures_per_hour, expected_type=type_hints["max_failures_per_hour"])
            check_type(argname="argument max_failures_total", value=max_failures_total, expected_type=type_hints["max_failures_total"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_failures_per_hour is not None:
            self._values["max_failures_per_hour"] = max_failures_per_hour
        if max_failures_total is not None:
            self._values["max_failures_total"] = max_failures_total

    @builtins.property
    def max_failures_per_hour(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        Maximum number of times per hour a driver may be restarted as a result of driver exiting with non-zero code before job is reported failed. A job may be reported as thrashing if driver exits with non-zero code 4 times within 10 minute window. Maximum value is 10.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#max_failures_per_hour DataprocWorkflowTemplate#max_failures_per_hour}
        '''
        result = self._values.get("max_failures_per_hour")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_failures_total(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        Maximum number of times in total a driver may be restarted as a result of driver exiting with non-zero code before job is reported failed. Maximum value is 240.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#max_failures_total DataprocWorkflowTemplate#max_failures_total}
        '''
        result = self._values.get("max_failures_total")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateJobsScheduling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplateJobsSchedulingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsSchedulingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efd1d68671a3b5d849133b690e68ed88f663652a48b5d710385b568d8da09284)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxFailuresPerHour")
    def reset_max_failures_per_hour(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxFailuresPerHour", []))

    @jsii.member(jsii_name="resetMaxFailuresTotal")
    def reset_max_failures_total(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxFailuresTotal", []))

    @builtins.property
    @jsii.member(jsii_name="maxFailuresPerHourInput")
    def max_failures_per_hour_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxFailuresPerHourInput"))

    @builtins.property
    @jsii.member(jsii_name="maxFailuresTotalInput")
    def max_failures_total_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxFailuresTotalInput"))

    @builtins.property
    @jsii.member(jsii_name="maxFailuresPerHour")
    def max_failures_per_hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxFailuresPerHour"))

    @max_failures_per_hour.setter
    def max_failures_per_hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd461e51ec41b82db0533a98e4e50dfdfd6aab5e50ce2b6125872dcbd9553113)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFailuresPerHour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxFailuresTotal")
    def max_failures_total(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxFailuresTotal"))

    @max_failures_total.setter
    def max_failures_total(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6612d73e552de66a0f077a9c59c8bb690c34818e5ec6f25b7e27952b5725f2d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFailuresTotal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocWorkflowTemplateJobsScheduling]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsScheduling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateJobsScheduling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bc267373857a021b5be798788dd03e0480f0838e57562997adb6bc0fe56c7a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsSparkJob",
    jsii_struct_bases=[],
    name_mapping={
        "archive_uris": "archiveUris",
        "args": "args",
        "file_uris": "fileUris",
        "jar_file_uris": "jarFileUris",
        "logging_config": "loggingConfig",
        "main_class": "mainClass",
        "main_jar_file_uri": "mainJarFileUri",
        "properties": "properties",
    },
)
class DataprocWorkflowTemplateJobsSparkJob:
    def __init__(
        self,
        *,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsSparkJobLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        main_class: typing.Optional[builtins.str] = None,
        main_jar_file_uri: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param archive_uris: Optional. HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#archive_uris DataprocWorkflowTemplate#archive_uris}
        :param args: Optional. The arguments to pass to the driver. Do not include arguments, such as ``--conf``, that can be set as job properties, since a collision may occur that causes an incorrect job submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#args DataprocWorkflowTemplate#args}
        :param file_uris: Optional. HCFS URIs of files to be placed in the working directory of each executor. Useful for naively parallel tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#file_uris DataprocWorkflowTemplate#file_uris}
        :param jar_file_uris: Optional. HCFS URIs of jar files to add to the CLASSPATHs of the Spark driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#jar_file_uris DataprocWorkflowTemplate#jar_file_uris}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#logging_config DataprocWorkflowTemplate#logging_config}
        :param main_class: The name of the driver's main class. The jar file that contains the class must be in the default CLASSPATH or specified in ``jar_file_uris``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#main_class DataprocWorkflowTemplate#main_class}
        :param main_jar_file_uri: The HCFS URI of the jar file that contains the main class. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#main_jar_file_uri DataprocWorkflowTemplate#main_jar_file_uri}
        :param properties: Optional. A mapping of property names to values, used to configure Spark. Properties that conflict with values set by the Dataproc API may be overwritten. Can include properties set in /etc/spark/conf/spark-defaults.conf and classes in user code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        '''
        if isinstance(logging_config, dict):
            logging_config = DataprocWorkflowTemplateJobsSparkJobLoggingConfig(**logging_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1688b4bf5eebec385b4216634bbdab24ee87e0a3325b0be9ad194ad78ccdf94)
            check_type(argname="argument archive_uris", value=archive_uris, expected_type=type_hints["archive_uris"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument file_uris", value=file_uris, expected_type=type_hints["file_uris"])
            check_type(argname="argument jar_file_uris", value=jar_file_uris, expected_type=type_hints["jar_file_uris"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument main_class", value=main_class, expected_type=type_hints["main_class"])
            check_type(argname="argument main_jar_file_uri", value=main_jar_file_uri, expected_type=type_hints["main_jar_file_uri"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if archive_uris is not None:
            self._values["archive_uris"] = archive_uris
        if args is not None:
            self._values["args"] = args
        if file_uris is not None:
            self._values["file_uris"] = file_uris
        if jar_file_uris is not None:
            self._values["jar_file_uris"] = jar_file_uris
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if main_class is not None:
            self._values["main_class"] = main_class
        if main_jar_file_uri is not None:
            self._values["main_jar_file_uri"] = main_jar_file_uri
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def archive_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#archive_uris DataprocWorkflowTemplate#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        The arguments to pass to the driver. Do not include arguments, such as ``--conf``, that can be set as job properties, since a collision may occur that causes an incorrect job submission.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#args DataprocWorkflowTemplate#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        HCFS URIs of files to be placed in the working directory of each executor. Useful for naively parallel tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#file_uris DataprocWorkflowTemplate#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jar_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. HCFS URIs of jar files to add to the CLASSPATHs of the Spark driver and tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#jar_file_uris DataprocWorkflowTemplate#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateJobsSparkJobLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#logging_config DataprocWorkflowTemplate#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsSparkJobLoggingConfig"], result)

    @builtins.property
    def main_class(self) -> typing.Optional[builtins.str]:
        '''The name of the driver's main class.

        The jar file that contains the class must be in the default CLASSPATH or specified in ``jar_file_uris``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#main_class DataprocWorkflowTemplate#main_class}
        '''
        result = self._values.get("main_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def main_jar_file_uri(self) -> typing.Optional[builtins.str]:
        '''The HCFS URI of the jar file that contains the main class.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#main_jar_file_uri DataprocWorkflowTemplate#main_jar_file_uri}
        '''
        result = self._values.get("main_jar_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        A mapping of property names to values, used to configure Spark. Properties that conflict with values set by the Dataproc API may be overwritten. Can include properties set in /etc/spark/conf/spark-defaults.conf and classes in user code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateJobsSparkJob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsSparkJobLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"driver_log_levels": "driverLogLevels"},
)
class DataprocWorkflowTemplateJobsSparkJobLoggingConfig:
    def __init__(
        self,
        *,
        driver_log_levels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param driver_log_levels: The per-package log levels for the driver. This may include "root" package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#driver_log_levels DataprocWorkflowTemplate#driver_log_levels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e0dd814cada24ac4be6bf95e663387c5bfb309e20981a6477585d61e929dd0a)
            check_type(argname="argument driver_log_levels", value=driver_log_levels, expected_type=type_hints["driver_log_levels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if driver_log_levels is not None:
            self._values["driver_log_levels"] = driver_log_levels

    @builtins.property
    def driver_log_levels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The per-package log levels for the driver.

        This may include "root" package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#driver_log_levels DataprocWorkflowTemplate#driver_log_levels}
        '''
        result = self._values.get("driver_log_levels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateJobsSparkJobLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplateJobsSparkJobLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsSparkJobLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__438a8f2d10491b888ef6aca3c1e2d3c66a521b119c690372fa96452593093d4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDriverLogLevels")
    def reset_driver_log_levels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDriverLogLevels", []))

    @builtins.property
    @jsii.member(jsii_name="driverLogLevelsInput")
    def driver_log_levels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "driverLogLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="driverLogLevels")
    def driver_log_levels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "driverLogLevels"))

    @driver_log_levels.setter
    def driver_log_levels(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab8485b53f33dff774179e3b580ce602eef22695954098a54429241bc608f5fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverLogLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateJobsSparkJobLoggingConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsSparkJobLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateJobsSparkJobLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41664378fbec199ed18ce72e7f6e2b521bd73c3373aa8259f8430e273e4584ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplateJobsSparkJobOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsSparkJobOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba608f333aa09b2e8b686009d01788e39464c97ba4feda24096858d4848401c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        driver_log_levels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param driver_log_levels: The per-package log levels for the driver. This may include "root" package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#driver_log_levels DataprocWorkflowTemplate#driver_log_levels}
        '''
        value = DataprocWorkflowTemplateJobsSparkJobLoggingConfig(
            driver_log_levels=driver_log_levels
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

    @jsii.member(jsii_name="resetArchiveUris")
    def reset_archive_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchiveUris", []))

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetFileUris")
    def reset_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileUris", []))

    @jsii.member(jsii_name="resetJarFileUris")
    def reset_jar_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJarFileUris", []))

    @jsii.member(jsii_name="resetLoggingConfig")
    def reset_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfig", []))

    @jsii.member(jsii_name="resetMainClass")
    def reset_main_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMainClass", []))

    @jsii.member(jsii_name="resetMainJarFileUri")
    def reset_main_jar_file_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMainJarFileUri", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(
        self,
    ) -> DataprocWorkflowTemplateJobsSparkJobLoggingConfigOutputReference:
        return typing.cast(DataprocWorkflowTemplateJobsSparkJobLoggingConfigOutputReference, jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="archiveUrisInput")
    def archive_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "archiveUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="fileUrisInput")
    def file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "fileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="jarFileUrisInput")
    def jar_file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jarFileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfigInput")
    def logging_config_input(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateJobsSparkJobLoggingConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsSparkJobLoggingConfig], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="mainClassInput")
    def main_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mainClassInput"))

    @builtins.property
    @jsii.member(jsii_name="mainJarFileUriInput")
    def main_jar_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mainJarFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="archiveUris")
    def archive_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "archiveUris"))

    @archive_uris.setter
    def archive_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b867d7ae0f1270091479c0b179fb85327b0c79d64dbd01d610e10d7e29c9e662)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4e305dd7d2009b14e74af5a4e49191bc92db92a8a2ca69b629cc7d0d37af07b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d4a4eb1548c136eb50b2a711d0f93b3f0a505224c410e2cc8ff08cb4b72a9ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jarFileUris")
    def jar_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jarFileUris"))

    @jar_file_uris.setter
    def jar_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ab02762e7fb36720378b9f6c12eeda7f2dee954c8769bd4405234d204c67b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainClass")
    def main_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainClass"))

    @main_class.setter
    def main_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cde973b152685e71eb5ec39391ad1c8acb679788af871b3902a2e2bd5378436)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainJarFileUri")
    def main_jar_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainJarFileUri"))

    @main_jar_file_uri.setter
    def main_jar_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d36d1d7a0208b5369a4900f330b971b3e3e7a25c1e34cb419b65f0f2325ef80e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainJarFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8679cc6f307ffadb6bea9079014a69eac66b34ae02e31d33f4ce7cba38a9fdf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocWorkflowTemplateJobsSparkJob]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsSparkJob], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateJobsSparkJob],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e11d6bd41091343762c1be825a5f545a2857c3c512e6da6de439fc98e652d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsSparkRJob",
    jsii_struct_bases=[],
    name_mapping={
        "main_r_file_uri": "mainRFileUri",
        "archive_uris": "archiveUris",
        "args": "args",
        "file_uris": "fileUris",
        "logging_config": "loggingConfig",
        "properties": "properties",
    },
)
class DataprocWorkflowTemplateJobsSparkRJob:
    def __init__(
        self,
        *,
        main_r_file_uri: builtins.str,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsSparkRJobLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param main_r_file_uri: Required. The HCFS URI of the main R file to use as the driver. Must be a .R file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#main_r_file_uri DataprocWorkflowTemplate#main_r_file_uri}
        :param archive_uris: Optional. HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#archive_uris DataprocWorkflowTemplate#archive_uris}
        :param args: Optional. The arguments to pass to the driver. Do not include arguments, such as ``--conf``, that can be set as job properties, since a collision may occur that causes an incorrect job submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#args DataprocWorkflowTemplate#args}
        :param file_uris: Optional. HCFS URIs of files to be placed in the working directory of each executor. Useful for naively parallel tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#file_uris DataprocWorkflowTemplate#file_uris}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#logging_config DataprocWorkflowTemplate#logging_config}
        :param properties: Optional. A mapping of property names to values, used to configure SparkR. Properties that conflict with values set by the Dataproc API may be overwritten. Can include properties set in /etc/spark/conf/spark-defaults.conf and classes in user code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        '''
        if isinstance(logging_config, dict):
            logging_config = DataprocWorkflowTemplateJobsSparkRJobLoggingConfig(**logging_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2f98ba1085c9ffd8cc7435e6a284840fcd4c87b63e54480977b75c4e32c6ff5)
            check_type(argname="argument main_r_file_uri", value=main_r_file_uri, expected_type=type_hints["main_r_file_uri"])
            check_type(argname="argument archive_uris", value=archive_uris, expected_type=type_hints["archive_uris"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument file_uris", value=file_uris, expected_type=type_hints["file_uris"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "main_r_file_uri": main_r_file_uri,
        }
        if archive_uris is not None:
            self._values["archive_uris"] = archive_uris
        if args is not None:
            self._values["args"] = args
        if file_uris is not None:
            self._values["file_uris"] = file_uris
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def main_r_file_uri(self) -> builtins.str:
        '''Required. The HCFS URI of the main R file to use as the driver. Must be a .R file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#main_r_file_uri DataprocWorkflowTemplate#main_r_file_uri}
        '''
        result = self._values.get("main_r_file_uri")
        assert result is not None, "Required property 'main_r_file_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def archive_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#archive_uris DataprocWorkflowTemplate#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        The arguments to pass to the driver. Do not include arguments, such as ``--conf``, that can be set as job properties, since a collision may occur that causes an incorrect job submission.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#args DataprocWorkflowTemplate#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        HCFS URIs of files to be placed in the working directory of each executor. Useful for naively parallel tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#file_uris DataprocWorkflowTemplate#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateJobsSparkRJobLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#logging_config DataprocWorkflowTemplate#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsSparkRJobLoggingConfig"], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        A mapping of property names to values, used to configure SparkR. Properties that conflict with values set by the Dataproc API may be overwritten. Can include properties set in /etc/spark/conf/spark-defaults.conf and classes in user code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateJobsSparkRJob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsSparkRJobLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"driver_log_levels": "driverLogLevels"},
)
class DataprocWorkflowTemplateJobsSparkRJobLoggingConfig:
    def __init__(
        self,
        *,
        driver_log_levels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param driver_log_levels: The per-package log levels for the driver. This may include "root" package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#driver_log_levels DataprocWorkflowTemplate#driver_log_levels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74642c516bc70c6bdb1bb62bd56991d698215b3619d73919d9727416ac5ddffc)
            check_type(argname="argument driver_log_levels", value=driver_log_levels, expected_type=type_hints["driver_log_levels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if driver_log_levels is not None:
            self._values["driver_log_levels"] = driver_log_levels

    @builtins.property
    def driver_log_levels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The per-package log levels for the driver.

        This may include "root" package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#driver_log_levels DataprocWorkflowTemplate#driver_log_levels}
        '''
        result = self._values.get("driver_log_levels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateJobsSparkRJobLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplateJobsSparkRJobLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsSparkRJobLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d3dd4e359e19ca9728d9afaf8d2d7e8c187f1b80330721a85da39e83e6f0872)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDriverLogLevels")
    def reset_driver_log_levels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDriverLogLevels", []))

    @builtins.property
    @jsii.member(jsii_name="driverLogLevelsInput")
    def driver_log_levels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "driverLogLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="driverLogLevels")
    def driver_log_levels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "driverLogLevels"))

    @driver_log_levels.setter
    def driver_log_levels(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd0252e74bb20b5e0a4ac60ea401461c4813b80982322d69089bd976a275ec4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverLogLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateJobsSparkRJobLoggingConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsSparkRJobLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateJobsSparkRJobLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__333123b3b9307ee06bc99222ba9d68f7e5e363c770bac269e2c7116e595432ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplateJobsSparkRJobOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsSparkRJobOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b3d33d6e67b151db5e000571d08abc0c0db69004222dc35b4913144018d1873)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        driver_log_levels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param driver_log_levels: The per-package log levels for the driver. This may include "root" package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#driver_log_levels DataprocWorkflowTemplate#driver_log_levels}
        '''
        value = DataprocWorkflowTemplateJobsSparkRJobLoggingConfig(
            driver_log_levels=driver_log_levels
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

    @jsii.member(jsii_name="resetArchiveUris")
    def reset_archive_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchiveUris", []))

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetFileUris")
    def reset_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileUris", []))

    @jsii.member(jsii_name="resetLoggingConfig")
    def reset_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfig", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(
        self,
    ) -> DataprocWorkflowTemplateJobsSparkRJobLoggingConfigOutputReference:
        return typing.cast(DataprocWorkflowTemplateJobsSparkRJobLoggingConfigOutputReference, jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="archiveUrisInput")
    def archive_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "archiveUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="fileUrisInput")
    def file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "fileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfigInput")
    def logging_config_input(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateJobsSparkRJobLoggingConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsSparkRJobLoggingConfig], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="mainRFileUriInput")
    def main_r_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mainRFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="archiveUris")
    def archive_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "archiveUris"))

    @archive_uris.setter
    def archive_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e40d8d2930b2a196b9a1e570c2cbc96f886e701b3c9f909946a18cf75fe5680)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12e9c48268ecc9545bbfebaeafedf87f425f49ba6c0ccc8812807f24563a0d27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fb2dbffb452b42554d8c823eb4c07bb9dd9cbe62a9918c0ae8b9a2356827f91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainRFileUri")
    def main_r_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainRFileUri"))

    @main_r_file_uri.setter
    def main_r_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4e2fca9f3be70a175a68d0ae0f1d6d647e4776fc93006273cc61b746fb3e8ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainRFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83716ec4ff9a6c9d7c48b683ba05aa8b41878e65dfc04ad5c947caf81a6509ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocWorkflowTemplateJobsSparkRJob]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsSparkRJob], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateJobsSparkRJob],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a2fcf07240fc8dbc9c0af9ecfc3fd31eea19e7c3a25f9db92edf2c499cac013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsSparkSqlJob",
    jsii_struct_bases=[],
    name_mapping={
        "jar_file_uris": "jarFileUris",
        "logging_config": "loggingConfig",
        "properties": "properties",
        "query_file_uri": "queryFileUri",
        "query_list": "queryList",
        "script_variables": "scriptVariables",
    },
)
class DataprocWorkflowTemplateJobsSparkSqlJob:
    def __init__(
        self,
        *,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsSparkSqlJobLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        query_file_uri: typing.Optional[builtins.str] = None,
        query_list: typing.Optional[typing.Union["DataprocWorkflowTemplateJobsSparkSqlJobQueryListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
        script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param jar_file_uris: Optional. HCFS URIs of jar files to be added to the Spark CLASSPATH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#jar_file_uris DataprocWorkflowTemplate#jar_file_uris}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#logging_config DataprocWorkflowTemplate#logging_config}
        :param properties: Optional. A mapping of property names to values, used to configure Spark SQL's SparkConf. Properties that conflict with values set by the Dataproc API may be overwritten. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        :param query_file_uri: The HCFS URI of the script that contains SQL queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_file_uri DataprocWorkflowTemplate#query_file_uri}
        :param query_list: query_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_list DataprocWorkflowTemplate#query_list}
        :param script_variables: Optional. Mapping of query variable names to values (equivalent to the Spark SQL command: SET ``name="value";``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#script_variables DataprocWorkflowTemplate#script_variables}
        '''
        if isinstance(logging_config, dict):
            logging_config = DataprocWorkflowTemplateJobsSparkSqlJobLoggingConfig(**logging_config)
        if isinstance(query_list, dict):
            query_list = DataprocWorkflowTemplateJobsSparkSqlJobQueryListStruct(**query_list)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd20e37b4f5d2fce4b18d8af05c3e36c5d9afbcf9b7e20c856602e113b844f40)
            check_type(argname="argument jar_file_uris", value=jar_file_uris, expected_type=type_hints["jar_file_uris"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument query_file_uri", value=query_file_uri, expected_type=type_hints["query_file_uri"])
            check_type(argname="argument query_list", value=query_list, expected_type=type_hints["query_list"])
            check_type(argname="argument script_variables", value=script_variables, expected_type=type_hints["script_variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if jar_file_uris is not None:
            self._values["jar_file_uris"] = jar_file_uris
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if properties is not None:
            self._values["properties"] = properties
        if query_file_uri is not None:
            self._values["query_file_uri"] = query_file_uri
        if query_list is not None:
            self._values["query_list"] = query_list
        if script_variables is not None:
            self._values["script_variables"] = script_variables

    @builtins.property
    def jar_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. HCFS URIs of jar files to be added to the Spark CLASSPATH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#jar_file_uris DataprocWorkflowTemplate#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateJobsSparkSqlJobLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#logging_config DataprocWorkflowTemplate#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsSparkSqlJobLoggingConfig"], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        A mapping of property names to values, used to configure Spark SQL's SparkConf. Properties that conflict with values set by the Dataproc API may be overwritten.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def query_file_uri(self) -> typing.Optional[builtins.str]:
        '''The HCFS URI of the script that contains SQL queries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_file_uri DataprocWorkflowTemplate#query_file_uri}
        '''
        result = self._values.get("query_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_list(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateJobsSparkSqlJobQueryListStruct"]:
        '''query_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#query_list DataprocWorkflowTemplate#query_list}
        '''
        result = self._values.get("query_list")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsSparkSqlJobQueryListStruct"], result)

    @builtins.property
    def script_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. Mapping of query variable names to values (equivalent to the Spark SQL command: SET ``name="value";``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#script_variables DataprocWorkflowTemplate#script_variables}
        '''
        result = self._values.get("script_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateJobsSparkSqlJob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsSparkSqlJobLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"driver_log_levels": "driverLogLevels"},
)
class DataprocWorkflowTemplateJobsSparkSqlJobLoggingConfig:
    def __init__(
        self,
        *,
        driver_log_levels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param driver_log_levels: The per-package log levels for the driver. This may include "root" package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#driver_log_levels DataprocWorkflowTemplate#driver_log_levels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c076e3fc3e3187d9d3e9554b66020dd297ae52430d77db8acae1911bbb4c32b6)
            check_type(argname="argument driver_log_levels", value=driver_log_levels, expected_type=type_hints["driver_log_levels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if driver_log_levels is not None:
            self._values["driver_log_levels"] = driver_log_levels

    @builtins.property
    def driver_log_levels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The per-package log levels for the driver.

        This may include "root" package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#driver_log_levels DataprocWorkflowTemplate#driver_log_levels}
        '''
        result = self._values.get("driver_log_levels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateJobsSparkSqlJobLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplateJobsSparkSqlJobLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsSparkSqlJobLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a0173c1c1e05a67c154c6a5a15e0f35fce4552f2f86c95a697bcd109c043342)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDriverLogLevels")
    def reset_driver_log_levels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDriverLogLevels", []))

    @builtins.property
    @jsii.member(jsii_name="driverLogLevelsInput")
    def driver_log_levels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "driverLogLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="driverLogLevels")
    def driver_log_levels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "driverLogLevels"))

    @driver_log_levels.setter
    def driver_log_levels(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a071fd896094de051904487b2fe0fe605a3afdea9c9375ab6c782987f9bf4a4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverLogLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateJobsSparkSqlJobLoggingConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsSparkSqlJobLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateJobsSparkSqlJobLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86f617f7c467ca723e667e8cbcfb2e7caf93c009d5d2a65ba6fd90538b2e4eea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplateJobsSparkSqlJobOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsSparkSqlJobOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__657f9b6645fe732e5d5698b3d82b33bee8ee7cf524600d898dfb6e2a35ab60a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        driver_log_levels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param driver_log_levels: The per-package log levels for the driver. This may include "root" package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#driver_log_levels DataprocWorkflowTemplate#driver_log_levels}
        '''
        value = DataprocWorkflowTemplateJobsSparkSqlJobLoggingConfig(
            driver_log_levels=driver_log_levels
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

    @jsii.member(jsii_name="putQueryList")
    def put_query_list(self, *, queries: typing.Sequence[builtins.str]) -> None:
        '''
        :param queries: Required. The queries to execute. You do not need to end a query expression with a semicolon. Multiple queries can be specified in one string by separating each with a semicolon. Here is an example of a Dataproc API snippet that uses a QueryList to specify a HiveJob: "hiveJob": { "queryList": { "queries": [ "query1", "query2", "query3;query4", ] } } Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#queries DataprocWorkflowTemplate#queries}
        '''
        value = DataprocWorkflowTemplateJobsSparkSqlJobQueryListStruct(queries=queries)

        return typing.cast(None, jsii.invoke(self, "putQueryList", [value]))

    @jsii.member(jsii_name="resetJarFileUris")
    def reset_jar_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJarFileUris", []))

    @jsii.member(jsii_name="resetLoggingConfig")
    def reset_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfig", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @jsii.member(jsii_name="resetQueryFileUri")
    def reset_query_file_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryFileUri", []))

    @jsii.member(jsii_name="resetQueryList")
    def reset_query_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryList", []))

    @jsii.member(jsii_name="resetScriptVariables")
    def reset_script_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScriptVariables", []))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(
        self,
    ) -> DataprocWorkflowTemplateJobsSparkSqlJobLoggingConfigOutputReference:
        return typing.cast(DataprocWorkflowTemplateJobsSparkSqlJobLoggingConfigOutputReference, jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="queryList")
    def query_list(
        self,
    ) -> "DataprocWorkflowTemplateJobsSparkSqlJobQueryListStructOutputReference":
        return typing.cast("DataprocWorkflowTemplateJobsSparkSqlJobQueryListStructOutputReference", jsii.get(self, "queryList"))

    @builtins.property
    @jsii.member(jsii_name="jarFileUrisInput")
    def jar_file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jarFileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfigInput")
    def logging_config_input(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateJobsSparkSqlJobLoggingConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsSparkSqlJobLoggingConfig], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="queryFileUriInput")
    def query_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="queryListInput")
    def query_list_input(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateJobsSparkSqlJobQueryListStruct"]:
        return typing.cast(typing.Optional["DataprocWorkflowTemplateJobsSparkSqlJobQueryListStruct"], jsii.get(self, "queryListInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptVariablesInput")
    def script_variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "scriptVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="jarFileUris")
    def jar_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jarFileUris"))

    @jar_file_uris.setter
    def jar_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6040aac8ee6bff08baf0ac1ed3f38c88431f771137762869e616f50d7e560d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__451df9286052fb703643e7ceec79c645941d833ac9ec53d48dc7bb223a0f8b3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryFileUri")
    def query_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryFileUri"))

    @query_file_uri.setter
    def query_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b7b6fa58214986a331d29dc40ba6fdb9d9c8165b27b6ed2edf6ae078f08f000)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scriptVariables")
    def script_variables(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "scriptVariables"))

    @script_variables.setter
    def script_variables(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7aaa40f452b1182305b8a60366929e7c97ab6e0207270649121cb76c4402846)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateJobsSparkSqlJob]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsSparkSqlJob], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateJobsSparkSqlJob],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36db09b5e2997527266339ca5d0fe5a2aa7ed6f5f14fe3975ffdc1b0c9498822)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsSparkSqlJobQueryListStruct",
    jsii_struct_bases=[],
    name_mapping={"queries": "queries"},
)
class DataprocWorkflowTemplateJobsSparkSqlJobQueryListStruct:
    def __init__(self, *, queries: typing.Sequence[builtins.str]) -> None:
        '''
        :param queries: Required. The queries to execute. You do not need to end a query expression with a semicolon. Multiple queries can be specified in one string by separating each with a semicolon. Here is an example of a Dataproc API snippet that uses a QueryList to specify a HiveJob: "hiveJob": { "queryList": { "queries": [ "query1", "query2", "query3;query4", ] } } Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#queries DataprocWorkflowTemplate#queries}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e2572365ece78ea1e64d330b2d7c8cb575a9b386bb4f6aafe3f41a094dae8e3)
            check_type(argname="argument queries", value=queries, expected_type=type_hints["queries"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "queries": queries,
        }

    @builtins.property
    def queries(self) -> typing.List[builtins.str]:
        '''Required.

        The queries to execute. You do not need to end a query expression with a semicolon. Multiple queries can be specified in one string by separating each with a semicolon. Here is an example of a Dataproc API snippet that uses a QueryList to specify a HiveJob: "hiveJob": { "queryList": { "queries": [ "query1", "query2", "query3;query4", ] } }

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#queries DataprocWorkflowTemplate#queries}
        '''
        result = self._values.get("queries")
        assert result is not None, "Required property 'queries' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateJobsSparkSqlJobQueryListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplateJobsSparkSqlJobQueryListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateJobsSparkSqlJobQueryListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c475d84e589a7fe1d0e6e577f5812f8dd31a88d49604173597d5bccd7dc97521)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="queriesInput")
    def queries_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queriesInput"))

    @builtins.property
    @jsii.member(jsii_name="queries")
    def queries(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queries"))

    @queries.setter
    def queries(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57bccdf78c306961816e28f1679129b9829e5d932e9a9a6fdb27d00e2eb3d868)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateJobsSparkSqlJobQueryListStruct]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateJobsSparkSqlJobQueryListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateJobsSparkSqlJobQueryListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adbc533850c4372f5292d966b42d58498eeb45a230adb3d42d35336c3d4a0505)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateParameters",
    jsii_struct_bases=[],
    name_mapping={
        "fields": "fields",
        "name": "name",
        "description": "description",
        "validation": "validation",
    },
)
class DataprocWorkflowTemplateParameters:
    def __init__(
        self,
        *,
        fields: typing.Sequence[builtins.str],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        validation: typing.Optional[typing.Union["DataprocWorkflowTemplateParametersValidation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param fields: Required. Paths to all fields that the parameter replaces. A field is allowed to appear in at most one parameter's list of field paths. A field path is similar in syntax to a google.protobuf.FieldMask. For example, a field path that references the zone field of a workflow template's cluster selector would be specified as ``placement.clusterSelector.zone``. Also, field paths can reference fields using the following syntax: * Values in maps can be referenced by key: * labels['key'] * placement.clusterSelector.clusterLabels['key'] * placement.managedCluster.labels['key'] * placement.clusterSelector.clusterLabels['key'] * jobs['step-id'].labels['key'] * Jobs in the jobs list can be referenced by step-id: * jobs['step-id'].hadoopJob.mainJarFileUri * jobs['step-id'].hiveJob.queryFileUri * jobs['step-id'].pySparkJob.mainPythonFileUri * jobs['step-id'].hadoopJob.jarFileUris[0] * jobs['step-id'].hadoopJob.archiveUris[0] * jobs['step-id'].hadoopJob.fileUris[0] * jobs['step-id'].pySparkJob.pythonFileUris[0] * Items in repeated fields can be referenced by a zero-based index: * jobs['step-id'].sparkJob.args[0] * Other examples: * jobs['step-id'].hadoopJob.properties['key'] * jobs['step-id'].hadoopJob.args[0] * jobs['step-id'].hiveJob.scriptVariables['key'] * jobs['step-id'].hadoopJob.mainJarFileUri * placement.clusterSelector.zone It may not be possible to parameterize maps and repeated fields in their entirety since only individual map values and individual items in repeated fields can be referenced. For example, the following field paths are invalid: - placement.clusterSelector.clusterLabels - jobs['step-id'].sparkJob.args Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#fields DataprocWorkflowTemplate#fields}
        :param name: Required. Parameter name. The parameter name is used as the key, and paired with the parameter value, which are passed to the template when the template is instantiated. The name must contain only capital letters (A-Z), numbers (0-9), and underscores (_), and must not start with a number. The maximum length is 40 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#name DataprocWorkflowTemplate#name}
        :param description: Optional. Brief description of the parameter. Must not exceed 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#description DataprocWorkflowTemplate#description}
        :param validation: validation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#validation DataprocWorkflowTemplate#validation}
        '''
        if isinstance(validation, dict):
            validation = DataprocWorkflowTemplateParametersValidation(**validation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df619c94601b1bd82e27acb6dfbc36d6f5ecc83e6bf66b2a9ff3e2affb42ca92)
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument validation", value=validation, expected_type=type_hints["validation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fields": fields,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if validation is not None:
            self._values["validation"] = validation

    @builtins.property
    def fields(self) -> typing.List[builtins.str]:
        '''Required.

        Paths to all fields that the parameter replaces. A field is allowed to appear in at most one parameter's list of field paths. A field path is similar in syntax to a google.protobuf.FieldMask. For example, a field path that references the zone field of a workflow template's cluster selector would be specified as ``placement.clusterSelector.zone``. Also, field paths can reference fields using the following syntax: * Values in maps can be referenced by key: * labels['key'] * placement.clusterSelector.clusterLabels['key'] * placement.managedCluster.labels['key'] * placement.clusterSelector.clusterLabels['key'] * jobs['step-id'].labels['key'] * Jobs in the jobs list can be referenced by step-id: * jobs['step-id'].hadoopJob.mainJarFileUri * jobs['step-id'].hiveJob.queryFileUri * jobs['step-id'].pySparkJob.mainPythonFileUri * jobs['step-id'].hadoopJob.jarFileUris[0] * jobs['step-id'].hadoopJob.archiveUris[0] * jobs['step-id'].hadoopJob.fileUris[0] * jobs['step-id'].pySparkJob.pythonFileUris[0] * Items in repeated fields can be referenced by a zero-based index: * jobs['step-id'].sparkJob.args[0] * Other examples: * jobs['step-id'].hadoopJob.properties['key'] * jobs['step-id'].hadoopJob.args[0] * jobs['step-id'].hiveJob.scriptVariables['key'] * jobs['step-id'].hadoopJob.mainJarFileUri * placement.clusterSelector.zone It may not be possible to parameterize maps and repeated fields in their entirety since only individual map values and individual items in repeated fields can be referenced. For example, the following field paths are invalid: - placement.clusterSelector.clusterLabels - jobs['step-id'].sparkJob.args

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#fields DataprocWorkflowTemplate#fields}
        '''
        result = self._values.get("fields")
        assert result is not None, "Required property 'fields' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Required.

        Parameter name. The parameter name is used as the key, and paired with the parameter value, which are passed to the template when the template is instantiated. The name must contain only capital letters (A-Z), numbers (0-9), and underscores (_), and must not start with a number. The maximum length is 40 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#name DataprocWorkflowTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. Brief description of the parameter. Must not exceed 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#description DataprocWorkflowTemplate#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validation(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateParametersValidation"]:
        '''validation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#validation DataprocWorkflowTemplate#validation}
        '''
        result = self._values.get("validation")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateParametersValidation"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplateParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db213347acc785ba21edeb7992e6e69bb45c1522caf0e78f04d7cae849a68979)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataprocWorkflowTemplateParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a96250d9a5faeb7090d01dcdef34b054537f3236f3972c4b5a3fd86c9cd7ad57)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataprocWorkflowTemplateParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c719b6cf1172e52d39e5ef234d331235283b319723d942fda948bc1ee7384ada)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b35cabd54f545fb453d8dd60679cf298001fe1a9db5d326d87a83175d46a668)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f27494add0073347c782656e63f91152a469f6c343797f3893d5b786d99403f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplateParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplateParameters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplateParameters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0796e7ab882938ded30b30ab73a383a54b7099767ae1eb24d8430dbd5d226555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplateParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8643cd043ea796cf71f03f784733e52e39a8d43ccfd81176080e9f9da5c1ae7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putValidation")
    def put_validation(
        self,
        *,
        regex: typing.Optional[typing.Union["DataprocWorkflowTemplateParametersValidationRegex", typing.Dict[builtins.str, typing.Any]]] = None,
        values: typing.Optional[typing.Union["DataprocWorkflowTemplateParametersValidationValues", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param regex: regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#regex DataprocWorkflowTemplate#regex}
        :param values: values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#values DataprocWorkflowTemplate#values}
        '''
        value = DataprocWorkflowTemplateParametersValidation(
            regex=regex, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putValidation", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetValidation")
    def reset_validation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidation", []))

    @builtins.property
    @jsii.member(jsii_name="validation")
    def validation(
        self,
    ) -> "DataprocWorkflowTemplateParametersValidationOutputReference":
        return typing.cast("DataprocWorkflowTemplateParametersValidationOutputReference", jsii.get(self, "validation"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldsInput")
    def fields_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "fieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="validationInput")
    def validation_input(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateParametersValidation"]:
        return typing.cast(typing.Optional["DataprocWorkflowTemplateParametersValidation"], jsii.get(self, "validationInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__853f03eea58322c4613aa7b31557520d954e30b1f8e11eb808602d963881f71c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fields")
    def fields(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fields"))

    @fields.setter
    def fields(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b874788ec2c35ad57b3f5afa605fa7dc61c8420ede84b29ace5f8e8f0ec1f95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fields", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78c8d3fb41ab1395e47cb58581da4bbdfe6c3f7eb4ea4311e473b49ba591d3a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplateParameters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplateParameters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplateParameters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8edc3a3f93b2e2100d7e4d2bbcc110e35543454d09864d9e9356a2559910f62e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateParametersValidation",
    jsii_struct_bases=[],
    name_mapping={"regex": "regex", "values": "values"},
)
class DataprocWorkflowTemplateParametersValidation:
    def __init__(
        self,
        *,
        regex: typing.Optional[typing.Union["DataprocWorkflowTemplateParametersValidationRegex", typing.Dict[builtins.str, typing.Any]]] = None,
        values: typing.Optional[typing.Union["DataprocWorkflowTemplateParametersValidationValues", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param regex: regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#regex DataprocWorkflowTemplate#regex}
        :param values: values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#values DataprocWorkflowTemplate#values}
        '''
        if isinstance(regex, dict):
            regex = DataprocWorkflowTemplateParametersValidationRegex(**regex)
        if isinstance(values, dict):
            values = DataprocWorkflowTemplateParametersValidationValues(**values)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c05a7915ac32fda101d8105e515a66e74c0f83be48c27cbfaf5dbc552e1deb2d)
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if regex is not None:
            self._values["regex"] = regex
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def regex(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateParametersValidationRegex"]:
        '''regex block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#regex DataprocWorkflowTemplate#regex}
        '''
        result = self._values.get("regex")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateParametersValidationRegex"], result)

    @builtins.property
    def values(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateParametersValidationValues"]:
        '''values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#values DataprocWorkflowTemplate#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional["DataprocWorkflowTemplateParametersValidationValues"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateParametersValidation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplateParametersValidationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateParametersValidationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42e1ed620b8377c90fce346f6adee60319a3e51676b0795935adc0146be88ee0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRegex")
    def put_regex(self, *, regexes: typing.Sequence[builtins.str]) -> None:
        '''
        :param regexes: Required. RE2 regular expressions used to validate the parameter's value. The value must match the regex in its entirety (substring matches are not sufficient). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#regexes DataprocWorkflowTemplate#regexes}
        '''
        value = DataprocWorkflowTemplateParametersValidationRegex(regexes=regexes)

        return typing.cast(None, jsii.invoke(self, "putRegex", [value]))

    @jsii.member(jsii_name="putValues")
    def put_values(self, *, values: typing.Sequence[builtins.str]) -> None:
        '''
        :param values: Required. List of allowed values for the parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#values DataprocWorkflowTemplate#values}
        '''
        value = DataprocWorkflowTemplateParametersValidationValues(values=values)

        return typing.cast(None, jsii.invoke(self, "putValues", [value]))

    @jsii.member(jsii_name="resetRegex")
    def reset_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegex", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(
        self,
    ) -> "DataprocWorkflowTemplateParametersValidationRegexOutputReference":
        return typing.cast("DataprocWorkflowTemplateParametersValidationRegexOutputReference", jsii.get(self, "regex"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(
        self,
    ) -> "DataprocWorkflowTemplateParametersValidationValuesOutputReference":
        return typing.cast("DataprocWorkflowTemplateParametersValidationValuesOutputReference", jsii.get(self, "values"))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateParametersValidationRegex"]:
        return typing.cast(typing.Optional["DataprocWorkflowTemplateParametersValidationRegex"], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplateParametersValidationValues"]:
        return typing.cast(typing.Optional["DataprocWorkflowTemplateParametersValidationValues"], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateParametersValidation]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateParametersValidation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateParametersValidation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abd9c29f854d3e069db36591402cd393d0ee31a32d378718d3912f0946acc7a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateParametersValidationRegex",
    jsii_struct_bases=[],
    name_mapping={"regexes": "regexes"},
)
class DataprocWorkflowTemplateParametersValidationRegex:
    def __init__(self, *, regexes: typing.Sequence[builtins.str]) -> None:
        '''
        :param regexes: Required. RE2 regular expressions used to validate the parameter's value. The value must match the regex in its entirety (substring matches are not sufficient). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#regexes DataprocWorkflowTemplate#regexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8e83b18a6e75c4388993aee5931e294c71e520235ed3218892d3f859bebfa69)
            check_type(argname="argument regexes", value=regexes, expected_type=type_hints["regexes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "regexes": regexes,
        }

    @builtins.property
    def regexes(self) -> typing.List[builtins.str]:
        '''Required.

        RE2 regular expressions used to validate the parameter's value. The value must match the regex in its entirety (substring matches are not sufficient).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#regexes DataprocWorkflowTemplate#regexes}
        '''
        result = self._values.get("regexes")
        assert result is not None, "Required property 'regexes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateParametersValidationRegex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplateParametersValidationRegexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateParametersValidationRegexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10442fb4fd87c736b35ecd4eb05520abdbb3f7ccbabafd53d375420129d37b82)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="regexesInput")
    def regexes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "regexesInput"))

    @builtins.property
    @jsii.member(jsii_name="regexes")
    def regexes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "regexes"))

    @regexes.setter
    def regexes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbdc6d6ee9551913b9912890f7f7bea341782616a6f3a3041ffcb092f0d0b0cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateParametersValidationRegex]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateParametersValidationRegex], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateParametersValidationRegex],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc07c5af2de16cc1889c87801264a77b9cb47db9a92c30006ffe9fddafb1fda4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateParametersValidationValues",
    jsii_struct_bases=[],
    name_mapping={"values": "values"},
)
class DataprocWorkflowTemplateParametersValidationValues:
    def __init__(self, *, values: typing.Sequence[builtins.str]) -> None:
        '''
        :param values: Required. List of allowed values for the parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#values DataprocWorkflowTemplate#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6b72b1b19b8770f38bf228842ab3279ea113092463a15c89fdacfd814f2601a)
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "values": values,
        }

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Required. List of allowed values for the parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#values DataprocWorkflowTemplate#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateParametersValidationValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplateParametersValidationValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateParametersValidationValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92b04b521a595fd857db05e970da2b6cf75d4dcbf3389cfef05d39be29abecc9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40a616213707bedb5d3973a8d306733e32f15dc12c096069362d928fe6bb6206)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplateParametersValidationValues]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplateParametersValidationValues], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplateParametersValidationValues],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bb43706ef49074c31d381624c55ec5249ed0d5cdddf40e911048ce0fe7bbc7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacement",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_selector": "clusterSelector",
        "managed_cluster": "managedCluster",
    },
)
class DataprocWorkflowTemplatePlacement:
    def __init__(
        self,
        *,
        cluster_selector: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementClusterSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_cluster: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementManagedCluster", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cluster_selector: cluster_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#cluster_selector DataprocWorkflowTemplate#cluster_selector}
        :param managed_cluster: managed_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#managed_cluster DataprocWorkflowTemplate#managed_cluster}
        '''
        if isinstance(cluster_selector, dict):
            cluster_selector = DataprocWorkflowTemplatePlacementClusterSelector(**cluster_selector)
        if isinstance(managed_cluster, dict):
            managed_cluster = DataprocWorkflowTemplatePlacementManagedCluster(**managed_cluster)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3f5b357371b44d183264e4f5f6bb16a59bdbc3d9835ecd221768b4465033ab5)
            check_type(argname="argument cluster_selector", value=cluster_selector, expected_type=type_hints["cluster_selector"])
            check_type(argname="argument managed_cluster", value=managed_cluster, expected_type=type_hints["managed_cluster"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster_selector is not None:
            self._values["cluster_selector"] = cluster_selector
        if managed_cluster is not None:
            self._values["managed_cluster"] = managed_cluster

    @builtins.property
    def cluster_selector(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementClusterSelector"]:
        '''cluster_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#cluster_selector DataprocWorkflowTemplate#cluster_selector}
        '''
        result = self._values.get("cluster_selector")
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementClusterSelector"], result)

    @builtins.property
    def managed_cluster(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedCluster"]:
        '''managed_cluster block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#managed_cluster DataprocWorkflowTemplate#managed_cluster}
        '''
        result = self._values.get("managed_cluster")
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedCluster"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementClusterSelector",
    jsii_struct_bases=[],
    name_mapping={"cluster_labels": "clusterLabels", "zone": "zone"},
)
class DataprocWorkflowTemplatePlacementClusterSelector:
    def __init__(
        self,
        *,
        cluster_labels: typing.Mapping[builtins.str, builtins.str],
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster_labels: Required. The cluster labels. Cluster must have all labels to match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#cluster_labels DataprocWorkflowTemplate#cluster_labels}
        :param zone: Optional. The zone where workflow process executes. This parameter does not affect the selection of the cluster. If unspecified, the zone of the first cluster matching the selector is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#zone DataprocWorkflowTemplate#zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8df5e3246eccd593fed28d0937bb1b10628826dfac6452ce774aac75ccf6e154)
            check_type(argname="argument cluster_labels", value=cluster_labels, expected_type=type_hints["cluster_labels"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_labels": cluster_labels,
        }
        if zone is not None:
            self._values["zone"] = zone

    @builtins.property
    def cluster_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Required. The cluster labels. Cluster must have all labels to match.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#cluster_labels DataprocWorkflowTemplate#cluster_labels}
        '''
        result = self._values.get("cluster_labels")
        assert result is not None, "Required property 'cluster_labels' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The zone where workflow process executes. This parameter does not affect the selection of the cluster. If unspecified, the zone of the first cluster matching the selector is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#zone DataprocWorkflowTemplate#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementClusterSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplatePlacementClusterSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementClusterSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f6fb7218f052005beaac0f8f6de41640f806976bcd2d95270eee4288f70da33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

    @builtins.property
    @jsii.member(jsii_name="clusterLabelsInput")
    def cluster_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "clusterLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterLabels")
    def cluster_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "clusterLabels"))

    @cluster_labels.setter
    def cluster_labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07f1ea51b7348e488969e57a573a352b8f4afbc7c7ff42e7790fe91de4e57b1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3df2c2b907009d467cec4da39a5c7b34a393ab72f9f26764fa3cb57b268e5fa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementClusterSelector]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementClusterSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacementClusterSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ddc81834e50b0a20488fc6998afca59ec5c1388784b0fc8f7c32e50d73d3ca0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedCluster",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_name": "clusterName",
        "config": "config",
        "labels": "labels",
    },
)
class DataprocWorkflowTemplatePlacementManagedCluster:
    def __init__(
        self,
        *,
        cluster_name: builtins.str,
        config: typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfig", typing.Dict[builtins.str, typing.Any]],
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param cluster_name: Required. The cluster name prefix. A unique cluster name will be formed by appending a random suffix. The name must contain only lower-case letters (a-z), numbers (0-9), and hyphens (-). Must begin with a letter. Cannot begin or end with hyphen. Must consist of between 2 and 35 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#cluster_name DataprocWorkflowTemplate#cluster_name}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#config DataprocWorkflowTemplate#config}
        :param labels: Optional. The labels to associate with this cluster. Label keys must be between 1 and 63 characters long, and must conform to the following PCRE regular expression: p{Ll}p{Lo}{0,62} Label values must be between 1 and 63 characters long, and must conform to the following PCRE regular expression: [p{Ll}p{Lo}p{N}_-]{0,63} No more than 32 labels can be associated with a given cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#labels DataprocWorkflowTemplate#labels}
        '''
        if isinstance(config, dict):
            config = DataprocWorkflowTemplatePlacementManagedClusterConfig(**config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4963d5f162a64b2e6bad1b736fc6f22cfa0c125b40f38ca4af8a41f1e92c9fa2)
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_name": cluster_name,
            "config": config,
        }
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def cluster_name(self) -> builtins.str:
        '''Required.

        The cluster name prefix. A unique cluster name will be formed by appending a random suffix. The name must contain only lower-case letters (a-z), numbers (0-9), and hyphens (-). Must begin with a letter. Cannot begin or end with hyphen. Must consist of between 2 and 35 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#cluster_name DataprocWorkflowTemplate#cluster_name}
        '''
        result = self._values.get("cluster_name")
        assert result is not None, "Required property 'cluster_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(self) -> "DataprocWorkflowTemplatePlacementManagedClusterConfig":
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#config DataprocWorkflowTemplate#config}
        '''
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return typing.cast("DataprocWorkflowTemplatePlacementManagedClusterConfig", result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        The labels to associate with this cluster. Label keys must be between 1 and 63 characters long, and must conform to the following PCRE regular expression: p{Ll}p{Lo}{0,62} Label values must be between 1 and 63 characters long, and must conform to the following PCRE regular expression: [p{Ll}p{Lo}p{N}_-]{0,63} No more than 32 labels can be associated with a given cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#labels DataprocWorkflowTemplate#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedCluster(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "autoscaling_config": "autoscalingConfig",
        "encryption_config": "encryptionConfig",
        "endpoint_config": "endpointConfig",
        "gce_cluster_config": "gceClusterConfig",
        "initialization_actions": "initializationActions",
        "lifecycle_config": "lifecycleConfig",
        "master_config": "masterConfig",
        "secondary_worker_config": "secondaryWorkerConfig",
        "security_config": "securityConfig",
        "software_config": "softwareConfig",
        "staging_bucket": "stagingBucket",
        "temp_bucket": "tempBucket",
        "worker_config": "workerConfig",
    },
)
class DataprocWorkflowTemplatePlacementManagedClusterConfig:
    def __init__(
        self,
        *,
        autoscaling_config: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigAutoscalingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        encryption_config: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_config: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigEndpointConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        gce_cluster_config: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        initialization_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        lifecycle_config: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigLifecycleConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        master_config: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        secondary_worker_config: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        security_config: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        software_config: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigSoftwareConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        staging_bucket: typing.Optional[builtins.str] = None,
        temp_bucket: typing.Optional[builtins.str] = None,
        worker_config: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param autoscaling_config: autoscaling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#autoscaling_config DataprocWorkflowTemplate#autoscaling_config}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#encryption_config DataprocWorkflowTemplate#encryption_config}
        :param endpoint_config: endpoint_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#endpoint_config DataprocWorkflowTemplate#endpoint_config}
        :param gce_cluster_config: gce_cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#gce_cluster_config DataprocWorkflowTemplate#gce_cluster_config}
        :param initialization_actions: initialization_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#initialization_actions DataprocWorkflowTemplate#initialization_actions}
        :param lifecycle_config: lifecycle_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#lifecycle_config DataprocWorkflowTemplate#lifecycle_config}
        :param master_config: master_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#master_config DataprocWorkflowTemplate#master_config}
        :param secondary_worker_config: secondary_worker_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#secondary_worker_config DataprocWorkflowTemplate#secondary_worker_config}
        :param security_config: security_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#security_config DataprocWorkflowTemplate#security_config}
        :param software_config: software_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#software_config DataprocWorkflowTemplate#software_config}
        :param staging_bucket: Optional. A Cloud Storage bucket used to stage job dependencies, config files, and job driver console output. If you do not specify a staging bucket, Cloud Dataproc will determine a Cloud Storage location (US, ASIA, or EU) for your cluster's staging bucket according to the Compute Engine zone where your cluster is deployed, and then create and manage this project-level, per-location bucket (see `Dataproc staging bucket <https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/staging-bucket>`_). **This field requires a Cloud Storage bucket name, not a URI to a Cloud Storage bucket.** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#staging_bucket DataprocWorkflowTemplate#staging_bucket}
        :param temp_bucket: Optional. A Cloud Storage bucket used to store ephemeral cluster and jobs data, such as Spark and MapReduce history files. If you do not specify a temp bucket, Dataproc will determine a Cloud Storage location (US, ASIA, or EU) for your cluster's temp bucket according to the Compute Engine zone where your cluster is deployed, and then create and manage this project-level, per-location bucket. The default bucket has a TTL of 90 days, but you can use any TTL (or none) if you specify a bucket. **This field requires a Cloud Storage bucket name, not a URI to a Cloud Storage bucket.** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#temp_bucket DataprocWorkflowTemplate#temp_bucket}
        :param worker_config: worker_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#worker_config DataprocWorkflowTemplate#worker_config}
        '''
        if isinstance(autoscaling_config, dict):
            autoscaling_config = DataprocWorkflowTemplatePlacementManagedClusterConfigAutoscalingConfig(**autoscaling_config)
        if isinstance(encryption_config, dict):
            encryption_config = DataprocWorkflowTemplatePlacementManagedClusterConfigEncryptionConfig(**encryption_config)
        if isinstance(endpoint_config, dict):
            endpoint_config = DataprocWorkflowTemplatePlacementManagedClusterConfigEndpointConfig(**endpoint_config)
        if isinstance(gce_cluster_config, dict):
            gce_cluster_config = DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfig(**gce_cluster_config)
        if isinstance(lifecycle_config, dict):
            lifecycle_config = DataprocWorkflowTemplatePlacementManagedClusterConfigLifecycleConfig(**lifecycle_config)
        if isinstance(master_config, dict):
            master_config = DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfig(**master_config)
        if isinstance(secondary_worker_config, dict):
            secondary_worker_config = DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfig(**secondary_worker_config)
        if isinstance(security_config, dict):
            security_config = DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfig(**security_config)
        if isinstance(software_config, dict):
            software_config = DataprocWorkflowTemplatePlacementManagedClusterConfigSoftwareConfig(**software_config)
        if isinstance(worker_config, dict):
            worker_config = DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfig(**worker_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78e997e314ca77040c63199bf3e146799df3ba159b3b88b7b820b13b98c41160)
            check_type(argname="argument autoscaling_config", value=autoscaling_config, expected_type=type_hints["autoscaling_config"])
            check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            check_type(argname="argument endpoint_config", value=endpoint_config, expected_type=type_hints["endpoint_config"])
            check_type(argname="argument gce_cluster_config", value=gce_cluster_config, expected_type=type_hints["gce_cluster_config"])
            check_type(argname="argument initialization_actions", value=initialization_actions, expected_type=type_hints["initialization_actions"])
            check_type(argname="argument lifecycle_config", value=lifecycle_config, expected_type=type_hints["lifecycle_config"])
            check_type(argname="argument master_config", value=master_config, expected_type=type_hints["master_config"])
            check_type(argname="argument secondary_worker_config", value=secondary_worker_config, expected_type=type_hints["secondary_worker_config"])
            check_type(argname="argument security_config", value=security_config, expected_type=type_hints["security_config"])
            check_type(argname="argument software_config", value=software_config, expected_type=type_hints["software_config"])
            check_type(argname="argument staging_bucket", value=staging_bucket, expected_type=type_hints["staging_bucket"])
            check_type(argname="argument temp_bucket", value=temp_bucket, expected_type=type_hints["temp_bucket"])
            check_type(argname="argument worker_config", value=worker_config, expected_type=type_hints["worker_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if autoscaling_config is not None:
            self._values["autoscaling_config"] = autoscaling_config
        if encryption_config is not None:
            self._values["encryption_config"] = encryption_config
        if endpoint_config is not None:
            self._values["endpoint_config"] = endpoint_config
        if gce_cluster_config is not None:
            self._values["gce_cluster_config"] = gce_cluster_config
        if initialization_actions is not None:
            self._values["initialization_actions"] = initialization_actions
        if lifecycle_config is not None:
            self._values["lifecycle_config"] = lifecycle_config
        if master_config is not None:
            self._values["master_config"] = master_config
        if secondary_worker_config is not None:
            self._values["secondary_worker_config"] = secondary_worker_config
        if security_config is not None:
            self._values["security_config"] = security_config
        if software_config is not None:
            self._values["software_config"] = software_config
        if staging_bucket is not None:
            self._values["staging_bucket"] = staging_bucket
        if temp_bucket is not None:
            self._values["temp_bucket"] = temp_bucket
        if worker_config is not None:
            self._values["worker_config"] = worker_config

    @builtins.property
    def autoscaling_config(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigAutoscalingConfig"]:
        '''autoscaling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#autoscaling_config DataprocWorkflowTemplate#autoscaling_config}
        '''
        result = self._values.get("autoscaling_config")
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigAutoscalingConfig"], result)

    @builtins.property
    def encryption_config(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigEncryptionConfig"]:
        '''encryption_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#encryption_config DataprocWorkflowTemplate#encryption_config}
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigEncryptionConfig"], result)

    @builtins.property
    def endpoint_config(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigEndpointConfig"]:
        '''endpoint_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#endpoint_config DataprocWorkflowTemplate#endpoint_config}
        '''
        result = self._values.get("endpoint_config")
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigEndpointConfig"], result)

    @builtins.property
    def gce_cluster_config(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfig"]:
        '''gce_cluster_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#gce_cluster_config DataprocWorkflowTemplate#gce_cluster_config}
        '''
        result = self._values.get("gce_cluster_config")
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfig"], result)

    @builtins.property
    def initialization_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActions"]]]:
        '''initialization_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#initialization_actions DataprocWorkflowTemplate#initialization_actions}
        '''
        result = self._values.get("initialization_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActions"]]], result)

    @builtins.property
    def lifecycle_config(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigLifecycleConfig"]:
        '''lifecycle_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#lifecycle_config DataprocWorkflowTemplate#lifecycle_config}
        '''
        result = self._values.get("lifecycle_config")
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigLifecycleConfig"], result)

    @builtins.property
    def master_config(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfig"]:
        '''master_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#master_config DataprocWorkflowTemplate#master_config}
        '''
        result = self._values.get("master_config")
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfig"], result)

    @builtins.property
    def secondary_worker_config(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfig"]:
        '''secondary_worker_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#secondary_worker_config DataprocWorkflowTemplate#secondary_worker_config}
        '''
        result = self._values.get("secondary_worker_config")
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfig"], result)

    @builtins.property
    def security_config(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfig"]:
        '''security_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#security_config DataprocWorkflowTemplate#security_config}
        '''
        result = self._values.get("security_config")
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfig"], result)

    @builtins.property
    def software_config(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigSoftwareConfig"]:
        '''software_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#software_config DataprocWorkflowTemplate#software_config}
        '''
        result = self._values.get("software_config")
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigSoftwareConfig"], result)

    @builtins.property
    def staging_bucket(self) -> typing.Optional[builtins.str]:
        '''Optional.

        A Cloud Storage bucket used to stage job dependencies, config files, and job driver console output. If you do not specify a staging bucket, Cloud Dataproc will determine a Cloud Storage location (US, ASIA, or EU) for your cluster's staging bucket according to the Compute Engine zone where your cluster is deployed, and then create and manage this project-level, per-location bucket (see `Dataproc staging bucket <https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/staging-bucket>`_). **This field requires a Cloud Storage bucket name, not a URI to a Cloud Storage bucket.**

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#staging_bucket DataprocWorkflowTemplate#staging_bucket}
        '''
        result = self._values.get("staging_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def temp_bucket(self) -> typing.Optional[builtins.str]:
        '''Optional.

        A Cloud Storage bucket used to store ephemeral cluster and jobs data, such as Spark and MapReduce history files. If you do not specify a temp bucket, Dataproc will determine a Cloud Storage location (US, ASIA, or EU) for your cluster's temp bucket according to the Compute Engine zone where your cluster is deployed, and then create and manage this project-level, per-location bucket. The default bucket has a TTL of 90 days, but you can use any TTL (or none) if you specify a bucket. **This field requires a Cloud Storage bucket name, not a URI to a Cloud Storage bucket.**

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#temp_bucket DataprocWorkflowTemplate#temp_bucket}
        '''
        result = self._values.get("temp_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def worker_config(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfig"]:
        '''worker_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#worker_config DataprocWorkflowTemplate#worker_config}
        '''
        result = self._values.get("worker_config")
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigAutoscalingConfig",
    jsii_struct_bases=[],
    name_mapping={"policy": "policy"},
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigAutoscalingConfig:
    def __init__(self, *, policy: typing.Optional[builtins.str] = None) -> None:
        '''
        :param policy: Optional. The autoscaling policy used by the cluster. Only resource names including projectid and location (region) are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/locations/[dataproc_region]/autoscalingPolicies/[policy_id]`` * ``projects/[project_id]/locations/[dataproc_region]/autoscalingPolicies/[policy_id]`` Note that the policy must be in the same project and Dataproc region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#policy DataprocWorkflowTemplate#policy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1d4cc3428d02607a48ddc80aa2d38a938b16f652a1516d81977eeb5b7419cd7)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy is not None:
            self._values["policy"] = policy

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The autoscaling policy used by the cluster. Only resource names including projectid and location (region) are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/locations/[dataproc_region]/autoscalingPolicies/[policy_id]`` * ``projects/[project_id]/locations/[dataproc_region]/autoscalingPolicies/[policy_id]`` Note that the policy must be in the same project and Dataproc region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#policy DataprocWorkflowTemplate#policy}
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigAutoscalingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplatePlacementManagedClusterConfigAutoscalingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigAutoscalingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfa85a0d833ef61d91ca33b06d6bc07499ef840004e815d1722a4df69fe6aaa9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPolicy")
    def reset_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="policyInput")
    def policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyInput"))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72d0ee42e0a135bb56a137a194f84e826a8fc3ee7a418bafbf36987dc60fddbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigAutoscalingConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigAutoscalingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigAutoscalingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b231ae6bb40dd5e756b52171f3f339109b3194eee87c1e412e0647c59711fe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigEncryptionConfig",
    jsii_struct_bases=[],
    name_mapping={"gce_pd_kms_key_name": "gcePdKmsKeyName"},
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigEncryptionConfig:
    def __init__(
        self,
        *,
        gce_pd_kms_key_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gce_pd_kms_key_name: Optional. The Cloud KMS key name to use for PD disk encryption for all instances in the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#gce_pd_kms_key_name DataprocWorkflowTemplate#gce_pd_kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__115783f75de11ccb091fe724e99efba1dcc1bbde4d8e06e434853b2163608fbb)
            check_type(argname="argument gce_pd_kms_key_name", value=gce_pd_kms_key_name, expected_type=type_hints["gce_pd_kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gce_pd_kms_key_name is not None:
            self._values["gce_pd_kms_key_name"] = gce_pd_kms_key_name

    @builtins.property
    def gce_pd_kms_key_name(self) -> typing.Optional[builtins.str]:
        '''Optional. The Cloud KMS key name to use for PD disk encryption for all instances in the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#gce_pd_kms_key_name DataprocWorkflowTemplate#gce_pd_kms_key_name}
        '''
        result = self._values.get("gce_pd_kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigEncryptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplatePlacementManagedClusterConfigEncryptionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigEncryptionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae7dee1401ff8e8aedb5d9c89b0d4fa3d4d92b454710838c6fd3856914d170cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGcePdKmsKeyName")
    def reset_gce_pd_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcePdKmsKeyName", []))

    @builtins.property
    @jsii.member(jsii_name="gcePdKmsKeyNameInput")
    def gce_pd_kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcePdKmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="gcePdKmsKeyName")
    def gce_pd_kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcePdKmsKeyName"))

    @gce_pd_kms_key_name.setter
    def gce_pd_kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e20ab0f3e8aaba5223d7e42b914c82b6ead00b497d06ba8b80c8c7626cbc7f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcePdKmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigEncryptionConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigEncryptionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigEncryptionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ded699f040a41d67a419b3f194df9225c5bc6d7553a38cd8f672e80f10c7e2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigEndpointConfig",
    jsii_struct_bases=[],
    name_mapping={"enable_http_port_access": "enableHttpPortAccess"},
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigEndpointConfig:
    def __init__(
        self,
        *,
        enable_http_port_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_http_port_access: Optional. If true, enable http access to specific ports on the cluster from external sources. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#enable_http_port_access DataprocWorkflowTemplate#enable_http_port_access}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa3a817c989f342827dff5864150be48ff0e4bee26f65d74a66d04de2199f7e2)
            check_type(argname="argument enable_http_port_access", value=enable_http_port_access, expected_type=type_hints["enable_http_port_access"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_http_port_access is not None:
            self._values["enable_http_port_access"] = enable_http_port_access

    @builtins.property
    def enable_http_port_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. If true, enable http access to specific ports on the cluster from external sources. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#enable_http_port_access DataprocWorkflowTemplate#enable_http_port_access}
        '''
        result = self._values.get("enable_http_port_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigEndpointConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplatePlacementManagedClusterConfigEndpointConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigEndpointConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bccaf9a034adf8182363467cfbd59b3d473efed64db62f2c86e353cf95a7dbc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableHttpPortAccess")
    def reset_enable_http_port_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableHttpPortAccess", []))

    @builtins.property
    @jsii.member(jsii_name="httpPorts")
    def http_ports(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "httpPorts"))

    @builtins.property
    @jsii.member(jsii_name="enableHttpPortAccessInput")
    def enable_http_port_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableHttpPortAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="enableHttpPortAccess")
    def enable_http_port_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableHttpPortAccess"))

    @enable_http_port_access.setter
    def enable_http_port_access(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04a2d2446ef79b2352eda0fa12e4d97c988cda626f532b2f70e48a2d536776d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableHttpPortAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigEndpointConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigEndpointConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigEndpointConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2326c6c3975189f644c08c8fff2079d3a2c741515fcf210323c96d96509f82b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "internal_ip_only": "internalIpOnly",
        "metadata": "metadata",
        "network": "network",
        "node_group_affinity": "nodeGroupAffinity",
        "private_ipv6_google_access": "privateIpv6GoogleAccess",
        "reservation_affinity": "reservationAffinity",
        "service_account": "serviceAccount",
        "service_account_scopes": "serviceAccountScopes",
        "shielded_instance_config": "shieldedInstanceConfig",
        "subnetwork": "subnetwork",
        "tags": "tags",
        "zone": "zone",
    },
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfig:
    def __init__(
        self,
        *,
        internal_ip_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network: typing.Optional[builtins.str] = None,
        node_group_affinity: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigNodeGroupAffinity", typing.Dict[builtins.str, typing.Any]]] = None,
        private_ipv6_google_access: typing.Optional[builtins.str] = None,
        reservation_affinity: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigReservationAffinity", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[builtins.str] = None,
        service_account_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        shielded_instance_config: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param internal_ip_only: Optional. If true, all instances in the cluster will only have internal IP addresses. By default, clusters are not restricted to internal IP addresses, and will have ephemeral external IP addresses assigned to each instance. This ``internal_ip_only`` restriction can only be enabled for subnetwork enabled networks, and all off-cluster dependencies must be configured to be accessible without external IP addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#internal_ip_only DataprocWorkflowTemplate#internal_ip_only}
        :param metadata: The Compute Engine metadata entries to add to all instances (see `Project and instance metadata <https://cloud.google.com/compute/docs/storing-retrieving-metadata#project_and_instance_metadata>`_). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#metadata DataprocWorkflowTemplate#metadata}
        :param network: Optional. The Compute Engine network to be used for machine communications. Cannot be specified with subnetwork_uri. If neither ``network_uri`` nor ``subnetwork_uri`` is specified, the "default" network of the project is used, if it exists. Cannot be a "Custom Subnet Network" (see `Using Subnetworks <https://cloud.google.com/compute/docs/subnetworks>`_ for more information). A full URL, partial URI, or short name are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/regions/global/default`` * ``projects/[project_id]/regions/global/default`` * ``default`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#network DataprocWorkflowTemplate#network}
        :param node_group_affinity: node_group_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#node_group_affinity DataprocWorkflowTemplate#node_group_affinity}
        :param private_ipv6_google_access: Optional. The type of IPv6 access for a cluster. Possible values: PRIVATE_IPV6_GOOGLE_ACCESS_UNSPECIFIED, INHERIT_FROM_SUBNETWORK, OUTBOUND, BIDIRECTIONAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#private_ipv6_google_access DataprocWorkflowTemplate#private_ipv6_google_access}
        :param reservation_affinity: reservation_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#reservation_affinity DataprocWorkflowTemplate#reservation_affinity}
        :param service_account: Optional. The `Dataproc service account <https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/service-accounts#service_accounts_in_dataproc>`_ (also see `VM Data Plane identity <https://cloud.google.com/dataproc/docs/concepts/iam/dataproc-principals#vm_service_account_data_plane_identity>`_) used by Dataproc cluster VM instances to access Google Cloud Platform services. If not specified, the `Compute Engine default service account <https://cloud.google.com/compute/docs/access/service-accounts#default_service_account>`_ is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#service_account DataprocWorkflowTemplate#service_account}
        :param service_account_scopes: Optional. The URIs of service account scopes to be included in Compute Engine instances. The following base set of scopes is always included: * https://www.googleapis.com/auth/cloud.useraccounts.readonly * https://www.googleapis.com/auth/devstorage.read_write * https://www.googleapis.com/auth/logging.write If no scopes are specified, the following defaults are also provided: * https://www.googleapis.com/auth/bigquery * https://www.googleapis.com/auth/bigtable.admin.table * https://www.googleapis.com/auth/bigtable.data * https://www.googleapis.com/auth/devstorage.full_control Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#service_account_scopes DataprocWorkflowTemplate#service_account_scopes}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#shielded_instance_config DataprocWorkflowTemplate#shielded_instance_config}
        :param subnetwork: Optional. The Compute Engine subnetwork to be used for machine communications. Cannot be specified with network_uri. A full URL, partial URI, or short name are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/regions/us-east1/subnetworks/sub0`` * ``projects/[project_id]/regions/us-east1/subnetworks/sub0`` * ``sub0`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#subnetwork DataprocWorkflowTemplate#subnetwork}
        :param tags: The Compute Engine tags to add to all instances (see `Tagging instances <https://cloud.google.com/compute/docs/label-or-tag-resources#tags>`_). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#tags DataprocWorkflowTemplate#tags}
        :param zone: Optional. The zone where the Compute Engine cluster will be located. On a create request, it is required in the "global" region. If omitted in a non-global Dataproc region, the service will pick a zone in the corresponding Compute Engine region. On a get request, zone will always be present. A full URL, partial URI, or short name are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/zones/[zone]`` * ``projects/[project_id]/zones/[zone]`` * ``us-central1-f`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#zone DataprocWorkflowTemplate#zone}
        '''
        if isinstance(node_group_affinity, dict):
            node_group_affinity = DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigNodeGroupAffinity(**node_group_affinity)
        if isinstance(reservation_affinity, dict):
            reservation_affinity = DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigReservationAffinity(**reservation_affinity)
        if isinstance(shielded_instance_config, dict):
            shielded_instance_config = DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigShieldedInstanceConfig(**shielded_instance_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c313c02647fb89efcea66083e9684355cd67ce381fd1f80624a3fed756ed9ad)
            check_type(argname="argument internal_ip_only", value=internal_ip_only, expected_type=type_hints["internal_ip_only"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument node_group_affinity", value=node_group_affinity, expected_type=type_hints["node_group_affinity"])
            check_type(argname="argument private_ipv6_google_access", value=private_ipv6_google_access, expected_type=type_hints["private_ipv6_google_access"])
            check_type(argname="argument reservation_affinity", value=reservation_affinity, expected_type=type_hints["reservation_affinity"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument service_account_scopes", value=service_account_scopes, expected_type=type_hints["service_account_scopes"])
            check_type(argname="argument shielded_instance_config", value=shielded_instance_config, expected_type=type_hints["shielded_instance_config"])
            check_type(argname="argument subnetwork", value=subnetwork, expected_type=type_hints["subnetwork"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if internal_ip_only is not None:
            self._values["internal_ip_only"] = internal_ip_only
        if metadata is not None:
            self._values["metadata"] = metadata
        if network is not None:
            self._values["network"] = network
        if node_group_affinity is not None:
            self._values["node_group_affinity"] = node_group_affinity
        if private_ipv6_google_access is not None:
            self._values["private_ipv6_google_access"] = private_ipv6_google_access
        if reservation_affinity is not None:
            self._values["reservation_affinity"] = reservation_affinity
        if service_account is not None:
            self._values["service_account"] = service_account
        if service_account_scopes is not None:
            self._values["service_account_scopes"] = service_account_scopes
        if shielded_instance_config is not None:
            self._values["shielded_instance_config"] = shielded_instance_config
        if subnetwork is not None:
            self._values["subnetwork"] = subnetwork
        if tags is not None:
            self._values["tags"] = tags
        if zone is not None:
            self._values["zone"] = zone

    @builtins.property
    def internal_ip_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        If true, all instances in the cluster will only have internal IP addresses. By default, clusters are not restricted to internal IP addresses, and will have ephemeral external IP addresses assigned to each instance. This ``internal_ip_only`` restriction can only be enabled for subnetwork enabled networks, and all off-cluster dependencies must be configured to be accessible without external IP addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#internal_ip_only DataprocWorkflowTemplate#internal_ip_only}
        '''
        result = self._values.get("internal_ip_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The Compute Engine metadata entries to add to all instances (see `Project and instance metadata <https://cloud.google.com/compute/docs/storing-retrieving-metadata#project_and_instance_metadata>`_).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#metadata DataprocWorkflowTemplate#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The Compute Engine network to be used for machine communications. Cannot be specified with subnetwork_uri. If neither ``network_uri`` nor ``subnetwork_uri`` is specified, the "default" network of the project is used, if it exists. Cannot be a "Custom Subnet Network" (see `Using Subnetworks <https://cloud.google.com/compute/docs/subnetworks>`_ for more information). A full URL, partial URI, or short name are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/regions/global/default`` * ``projects/[project_id]/regions/global/default`` * ``default``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#network DataprocWorkflowTemplate#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_group_affinity(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigNodeGroupAffinity"]:
        '''node_group_affinity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#node_group_affinity DataprocWorkflowTemplate#node_group_affinity}
        '''
        result = self._values.get("node_group_affinity")
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigNodeGroupAffinity"], result)

    @builtins.property
    def private_ipv6_google_access(self) -> typing.Optional[builtins.str]:
        '''Optional. The type of IPv6 access for a cluster. Possible values: PRIVATE_IPV6_GOOGLE_ACCESS_UNSPECIFIED, INHERIT_FROM_SUBNETWORK, OUTBOUND, BIDIRECTIONAL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#private_ipv6_google_access DataprocWorkflowTemplate#private_ipv6_google_access}
        '''
        result = self._values.get("private_ipv6_google_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reservation_affinity(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigReservationAffinity"]:
        '''reservation_affinity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#reservation_affinity DataprocWorkflowTemplate#reservation_affinity}
        '''
        result = self._values.get("reservation_affinity")
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigReservationAffinity"], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The `Dataproc service account <https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/service-accounts#service_accounts_in_dataproc>`_ (also see `VM Data Plane identity <https://cloud.google.com/dataproc/docs/concepts/iam/dataproc-principals#vm_service_account_data_plane_identity>`_) used by Dataproc cluster VM instances to access Google Cloud Platform services. If not specified, the `Compute Engine default service account <https://cloud.google.com/compute/docs/access/service-accounts#default_service_account>`_ is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#service_account DataprocWorkflowTemplate#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        The URIs of service account scopes to be included in Compute Engine instances. The following base set of scopes is always included: * https://www.googleapis.com/auth/cloud.useraccounts.readonly * https://www.googleapis.com/auth/devstorage.read_write * https://www.googleapis.com/auth/logging.write If no scopes are specified, the following defaults are also provided: * https://www.googleapis.com/auth/bigquery * https://www.googleapis.com/auth/bigtable.admin.table * https://www.googleapis.com/auth/bigtable.data * https://www.googleapis.com/auth/devstorage.full_control

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#service_account_scopes DataprocWorkflowTemplate#service_account_scopes}
        '''
        result = self._values.get("service_account_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def shielded_instance_config(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigShieldedInstanceConfig"]:
        '''shielded_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#shielded_instance_config DataprocWorkflowTemplate#shielded_instance_config}
        '''
        result = self._values.get("shielded_instance_config")
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigShieldedInstanceConfig"], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The Compute Engine subnetwork to be used for machine communications. Cannot be specified with network_uri. A full URL, partial URI, or short name are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/regions/us-east1/subnetworks/sub0`` * ``projects/[project_id]/regions/us-east1/subnetworks/sub0`` * ``sub0``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#subnetwork DataprocWorkflowTemplate#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Compute Engine tags to add to all instances (see `Tagging instances <https://cloud.google.com/compute/docs/label-or-tag-resources#tags>`_).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#tags DataprocWorkflowTemplate#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The zone where the Compute Engine cluster will be located. On a create request, it is required in the "global" region. If omitted in a non-global Dataproc region, the service will pick a zone in the corresponding Compute Engine region. On a get request, zone will always be present. A full URL, partial URI, or short name are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/zones/[zone]`` * ``projects/[project_id]/zones/[zone]`` * ``us-central1-f``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#zone DataprocWorkflowTemplate#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigNodeGroupAffinity",
    jsii_struct_bases=[],
    name_mapping={"node_group": "nodeGroup"},
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigNodeGroupAffinity:
    def __init__(self, *, node_group: builtins.str) -> None:
        '''
        :param node_group: Required. The URI of a sole-tenant `node group resource <https://cloud.google.com/compute/docs/reference/rest/v1/nodeGroups>`_ that the cluster will be created on. A full URL, partial URI, or node group name are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/zones/us-central1-a/nodeGroups/node-group-1`` * ``projects/[project_id]/zones/us-central1-a/nodeGroups/node-group-1`` * ``node-group-1`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#node_group DataprocWorkflowTemplate#node_group}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61428df75697a69d165ce0a0540d7ddbd3c87d7d7d5ee10fa59128ac91352dcd)
            check_type(argname="argument node_group", value=node_group, expected_type=type_hints["node_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "node_group": node_group,
        }

    @builtins.property
    def node_group(self) -> builtins.str:
        '''Required.

        The URI of a sole-tenant `node group resource <https://cloud.google.com/compute/docs/reference/rest/v1/nodeGroups>`_ that the cluster will be created on. A full URL, partial URI, or node group name are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/zones/us-central1-a/nodeGroups/node-group-1`` * ``projects/[project_id]/zones/us-central1-a/nodeGroups/node-group-1`` * ``node-group-1``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#node_group DataprocWorkflowTemplate#node_group}
        '''
        result = self._values.get("node_group")
        assert result is not None, "Required property 'node_group' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigNodeGroupAffinity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigNodeGroupAffinityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigNodeGroupAffinityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__631b5f8b9805ebf3876fbaca621349b28d556ba3cc8fbec794630414fd39b365)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nodeGroupInput")
    def node_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeGroup")
    def node_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeGroup"))

    @node_group.setter
    def node_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82e80561f42f2488af14790c6e2fe56e81f4cd89753a6d58867c030263c8a9db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigNodeGroupAffinity]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigNodeGroupAffinity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigNodeGroupAffinity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9230d8ab0f759abac30dfbda8a516663268888eea33463ce8da994e08ba4b3a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6243b61dcd890dcfeab4f7513a3f3bfba8d71b6321748f69c3afd72301ec52e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodeGroupAffinity")
    def put_node_group_affinity(self, *, node_group: builtins.str) -> None:
        '''
        :param node_group: Required. The URI of a sole-tenant `node group resource <https://cloud.google.com/compute/docs/reference/rest/v1/nodeGroups>`_ that the cluster will be created on. A full URL, partial URI, or node group name are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/zones/us-central1-a/nodeGroups/node-group-1`` * ``projects/[project_id]/zones/us-central1-a/nodeGroups/node-group-1`` * ``node-group-1`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#node_group DataprocWorkflowTemplate#node_group}
        '''
        value = DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigNodeGroupAffinity(
            node_group=node_group
        )

        return typing.cast(None, jsii.invoke(self, "putNodeGroupAffinity", [value]))

    @jsii.member(jsii_name="putReservationAffinity")
    def put_reservation_affinity(
        self,
        *,
        consume_reservation_type: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param consume_reservation_type: Optional. Type of reservation to consume Possible values: TYPE_UNSPECIFIED, NO_RESERVATION, ANY_RESERVATION, SPECIFIC_RESERVATION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#consume_reservation_type DataprocWorkflowTemplate#consume_reservation_type}
        :param key: Optional. Corresponds to the label key of reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#key DataprocWorkflowTemplate#key}
        :param values: Optional. Corresponds to the label values of reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#values DataprocWorkflowTemplate#values}
        '''
        value = DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigReservationAffinity(
            consume_reservation_type=consume_reservation_type, key=key, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putReservationAffinity", [value]))

    @jsii.member(jsii_name="putShieldedInstanceConfig")
    def put_shielded_instance_config(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Optional. Defines whether instances have integrity monitoring enabled. Integrity monitoring compares the most recent boot measurements to the integrity policy baseline and returns a pair of pass/fail results depending on whether they match or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#enable_integrity_monitoring DataprocWorkflowTemplate#enable_integrity_monitoring}
        :param enable_secure_boot: Optional. Defines whether the instances have Secure Boot enabled. Secure Boot helps ensure that the system only runs authentic software by verifying the digital signature of all boot components, and halting the boot process if signature verification fails. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#enable_secure_boot DataprocWorkflowTemplate#enable_secure_boot}
        :param enable_vtpm: Optional. Defines whether the instance have the vTPM enabled. Virtual Trusted Platform Module protects objects like keys, certificates and enables Measured Boot by performing the measurements needed to create a known good boot baseline, called the integrity policy baseline. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#enable_vtpm DataprocWorkflowTemplate#enable_vtpm}
        '''
        value = DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigShieldedInstanceConfig(
            enable_integrity_monitoring=enable_integrity_monitoring,
            enable_secure_boot=enable_secure_boot,
            enable_vtpm=enable_vtpm,
        )

        return typing.cast(None, jsii.invoke(self, "putShieldedInstanceConfig", [value]))

    @jsii.member(jsii_name="resetInternalIpOnly")
    def reset_internal_ip_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternalIpOnly", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetNodeGroupAffinity")
    def reset_node_group_affinity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeGroupAffinity", []))

    @jsii.member(jsii_name="resetPrivateIpv6GoogleAccess")
    def reset_private_ipv6_google_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIpv6GoogleAccess", []))

    @jsii.member(jsii_name="resetReservationAffinity")
    def reset_reservation_affinity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservationAffinity", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetServiceAccountScopes")
    def reset_service_account_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccountScopes", []))

    @jsii.member(jsii_name="resetShieldedInstanceConfig")
    def reset_shielded_instance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShieldedInstanceConfig", []))

    @jsii.member(jsii_name="resetSubnetwork")
    def reset_subnetwork(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetwork", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

    @builtins.property
    @jsii.member(jsii_name="nodeGroupAffinity")
    def node_group_affinity(
        self,
    ) -> DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigNodeGroupAffinityOutputReference:
        return typing.cast(DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigNodeGroupAffinityOutputReference, jsii.get(self, "nodeGroupAffinity"))

    @builtins.property
    @jsii.member(jsii_name="reservationAffinity")
    def reservation_affinity(
        self,
    ) -> "DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigReservationAffinityOutputReference":
        return typing.cast("DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigReservationAffinityOutputReference", jsii.get(self, "reservationAffinity"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfig")
    def shielded_instance_config(
        self,
    ) -> "DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigShieldedInstanceConfigOutputReference":
        return typing.cast("DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigShieldedInstanceConfigOutputReference", jsii.get(self, "shieldedInstanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="internalIpOnlyInput")
    def internal_ip_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalIpOnlyInput"))

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
    @jsii.member(jsii_name="nodeGroupAffinityInput")
    def node_group_affinity_input(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigNodeGroupAffinity]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigNodeGroupAffinity], jsii.get(self, "nodeGroupAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpv6GoogleAccessInput")
    def private_ipv6_google_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpv6GoogleAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="reservationAffinityInput")
    def reservation_affinity_input(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigReservationAffinity"]:
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigReservationAffinity"], jsii.get(self, "reservationAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountScopesInput")
    def service_account_scopes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "serviceAccountScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfigInput")
    def shielded_instance_config_input(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigShieldedInstanceConfig"]:
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigShieldedInstanceConfig"], jsii.get(self, "shieldedInstanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkInput")
    def subnetwork_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f1e6417cf992b2bd24c21b4d46d2bb210c8b1ea14b52f8b3b2144795fbbc4ac4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalIpOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b971782125968ac068544f5d0bf9e6428af58d371d62d59d23e7cbfff0e58a31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eccb89e558aa649fb999129d05ed32188f0ba07c72bd8a2b4e3bd0bf8ee313af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIpv6GoogleAccess")
    def private_ipv6_google_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpv6GoogleAccess"))

    @private_ipv6_google_access.setter
    def private_ipv6_google_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3cbbf4b3e6106cd0a69bc3597dfb0782136946b3df9b0d587b85d6d77cccaf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpv6GoogleAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed0ac363d57a2a12d5835b3ea10711bf6eb636c61a5183c076e36b1fc9c016dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountScopes")
    def service_account_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceAccountScopes"))

    @service_account_scopes.setter
    def service_account_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5807ec2835ea2b0400313d2bf52f2dba69615ce4f1b0e58767fb756f60d7f3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fd1bfc2670e9578e2b037a3d8fc27c0b5deb9690d6b2c0f3ccdd592e30544f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3a7790d3ce212e001ba5df312d49ef532b5b990f7a2f7937a6ce85f44a2f27a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__359064bef650801a8a9abf5a33b100eb353e07ddccab17d15e1e3a793b73a555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c371d22b11e37ec967e1f87c6804745ae43013996f4fec4c73228bd9109fdcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigReservationAffinity",
    jsii_struct_bases=[],
    name_mapping={
        "consume_reservation_type": "consumeReservationType",
        "key": "key",
        "values": "values",
    },
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigReservationAffinity:
    def __init__(
        self,
        *,
        consume_reservation_type: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param consume_reservation_type: Optional. Type of reservation to consume Possible values: TYPE_UNSPECIFIED, NO_RESERVATION, ANY_RESERVATION, SPECIFIC_RESERVATION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#consume_reservation_type DataprocWorkflowTemplate#consume_reservation_type}
        :param key: Optional. Corresponds to the label key of reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#key DataprocWorkflowTemplate#key}
        :param values: Optional. Corresponds to the label values of reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#values DataprocWorkflowTemplate#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4fee7e038636a3210599c6a847ba654c9acab840480ec0852cfc2d4258e1298)
            check_type(argname="argument consume_reservation_type", value=consume_reservation_type, expected_type=type_hints["consume_reservation_type"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if consume_reservation_type is not None:
            self._values["consume_reservation_type"] = consume_reservation_type
        if key is not None:
            self._values["key"] = key
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def consume_reservation_type(self) -> typing.Optional[builtins.str]:
        '''Optional. Type of reservation to consume Possible values: TYPE_UNSPECIFIED, NO_RESERVATION, ANY_RESERVATION, SPECIFIC_RESERVATION.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#consume_reservation_type DataprocWorkflowTemplate#consume_reservation_type}
        '''
        result = self._values.get("consume_reservation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Optional. Corresponds to the label key of reservation resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#key DataprocWorkflowTemplate#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. Corresponds to the label values of reservation resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#values DataprocWorkflowTemplate#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigReservationAffinity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigReservationAffinityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigReservationAffinityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42f77d732d6478dc8ea1b3a24edb13c1fc23933021b18b90430e126390131500)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConsumeReservationType")
    def reset_consume_reservation_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumeReservationType", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="consumeReservationTypeInput")
    def consume_reservation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumeReservationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="consumeReservationType")
    def consume_reservation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumeReservationType"))

    @consume_reservation_type.setter
    def consume_reservation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc91835498f28da4c7bfd40875106f0b5d284c61f8c77e0d2d41724c468b84b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumeReservationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__312d6f3f1dc2d6a7719ceb50bc7c56b1f501c7b2a8f4aaa70683514c78c32175)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3de14ad08bfc22e81534320a4079904a90c122cc00092af568caaa8ee55ba14a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigReservationAffinity]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigReservationAffinity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigReservationAffinity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79588976dfcb7560e062af0292c34d99dca5d7c9da971454cc3621f01e1b4899)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigShieldedInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_integrity_monitoring": "enableIntegrityMonitoring",
        "enable_secure_boot": "enableSecureBoot",
        "enable_vtpm": "enableVtpm",
    },
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigShieldedInstanceConfig:
    def __init__(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Optional. Defines whether instances have integrity monitoring enabled. Integrity monitoring compares the most recent boot measurements to the integrity policy baseline and returns a pair of pass/fail results depending on whether they match or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#enable_integrity_monitoring DataprocWorkflowTemplate#enable_integrity_monitoring}
        :param enable_secure_boot: Optional. Defines whether the instances have Secure Boot enabled. Secure Boot helps ensure that the system only runs authentic software by verifying the digital signature of all boot components, and halting the boot process if signature verification fails. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#enable_secure_boot DataprocWorkflowTemplate#enable_secure_boot}
        :param enable_vtpm: Optional. Defines whether the instance have the vTPM enabled. Virtual Trusted Platform Module protects objects like keys, certificates and enables Measured Boot by performing the measurements needed to create a known good boot baseline, called the integrity policy baseline. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#enable_vtpm DataprocWorkflowTemplate#enable_vtpm}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbfee862d33b60cf6e4b2ca1aecef2bf0eb85f14925a74d5aca790ff30c79894)
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

        Defines whether instances have integrity monitoring enabled. Integrity monitoring compares the most recent boot measurements to the integrity policy baseline and returns a pair of pass/fail results depending on whether they match or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#enable_integrity_monitoring DataprocWorkflowTemplate#enable_integrity_monitoring}
        '''
        result = self._values.get("enable_integrity_monitoring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_secure_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Defines whether the instances have Secure Boot enabled. Secure Boot helps ensure that the system only runs authentic software by verifying the digital signature of all boot components, and halting the boot process if signature verification fails.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#enable_secure_boot DataprocWorkflowTemplate#enable_secure_boot}
        '''
        result = self._values.get("enable_secure_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_vtpm(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Defines whether the instance have the vTPM enabled. Virtual Trusted Platform Module protects objects like keys, certificates and enables Measured Boot by performing the measurements needed to create a known good boot baseline, called the integrity policy baseline.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#enable_vtpm DataprocWorkflowTemplate#enable_vtpm}
        '''
        result = self._values.get("enable_vtpm")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigShieldedInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigShieldedInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigShieldedInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bff2ea28f9b90883f339191892f3f7568277d1658a3432d0840c43cca175e8a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b8217d9cbbdac3430a6feeaa8545bae91727f95b0213e27b2241e2c4f24c96a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa1e9ae740505e5b187b913311e3d87c6b92765834d83d31b1fb718621be0f5a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9a52ad242aad035ea40205e3e3d5cbed8ede36e7df8cb7bc836bd66ba280515)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableVtpm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigShieldedInstanceConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigShieldedInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigShieldedInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9786e0ad666f4e7f2c81ed7147f7bb2b3dad964d4a5803039ba73b2cf621f64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActions",
    jsii_struct_bases=[],
    name_mapping={
        "executable_file": "executableFile",
        "execution_timeout": "executionTimeout",
    },
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActions:
    def __init__(
        self,
        *,
        executable_file: typing.Optional[builtins.str] = None,
        execution_timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param executable_file: Required. Cloud Storage URI of executable file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#executable_file DataprocWorkflowTemplate#executable_file}
        :param execution_timeout: Optional. Amount of time executable has to complete. Default is 10 minutes (see JSON representation of `Duration <https://developers.google.com/protocol-buffers/docs/proto3#json>`_). Cluster creation fails with an explanatory error message (the name of the executable that caused the error and the exceeded timeout period) if the executable is not completed at end of the timeout period. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#execution_timeout DataprocWorkflowTemplate#execution_timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec70abb13c4c28511c350bd64bfc0d6d1a18db161873cfebc5122d4d062505a6)
            check_type(argname="argument executable_file", value=executable_file, expected_type=type_hints["executable_file"])
            check_type(argname="argument execution_timeout", value=execution_timeout, expected_type=type_hints["execution_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if executable_file is not None:
            self._values["executable_file"] = executable_file
        if execution_timeout is not None:
            self._values["execution_timeout"] = execution_timeout

    @builtins.property
    def executable_file(self) -> typing.Optional[builtins.str]:
        '''Required. Cloud Storage URI of executable file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#executable_file DataprocWorkflowTemplate#executable_file}
        '''
        result = self._values.get("executable_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_timeout(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Amount of time executable has to complete. Default is 10 minutes (see JSON representation of `Duration <https://developers.google.com/protocol-buffers/docs/proto3#json>`_). Cluster creation fails with an explanatory error message (the name of the executable that caused the error and the exceeded timeout period) if the executable is not completed at end of the timeout period.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#execution_timeout DataprocWorkflowTemplate#execution_timeout}
        '''
        result = self._values.get("execution_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b20fc3bcbda47bcbaed8dfb0c7f4f3fcd8f69cd695441b7595f2ff7522474bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ab6176f3cf9a722823b763a31eb002df9daee0742ac02f6d9cb4dfbb7bdc740)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0abbb3a9072ee66d0d5c7b667ed40fbb3cf3233f6359b07d7dade46646e8375c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d95250058af8b64a86e9cb550e63eb64a6501d46806fdcff297187908c09c755)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c044d49ab98ec4c91a01c2359c9080e18fbe88d0ff54264ef3508c640049823f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae86f9ab962b85c1ba1cc622462c86f28f6755168ba5052df637a2e48e973334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef7e80df590bc9b2b2e87723b36100c9d00ce7585ec4996cf15b4f794f340284)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExecutableFile")
    def reset_executable_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutableFile", []))

    @jsii.member(jsii_name="resetExecutionTimeout")
    def reset_execution_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="executableFileInput")
    def executable_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executableFileInput"))

    @builtins.property
    @jsii.member(jsii_name="executionTimeoutInput")
    def execution_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="executableFile")
    def executable_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executableFile"))

    @executable_file.setter
    def executable_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f31446bce4d87812db67e83ef7cca4fef9301aea70dbfc4754b2dc34281c2b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executableFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionTimeout")
    def execution_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionTimeout"))

    @execution_timeout.setter
    def execution_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2a40f825e45c5d2dc2a71723c2a23c30e6a1de86bd771815b1ca37195225241)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ace9220126cea92189d613392ddcbf1ea325d7132b7cc760246218d47b7076a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigLifecycleConfig",
    jsii_struct_bases=[],
    name_mapping={
        "auto_delete_time": "autoDeleteTime",
        "auto_delete_ttl": "autoDeleteTtl",
        "idle_delete_ttl": "idleDeleteTtl",
    },
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigLifecycleConfig:
    def __init__(
        self,
        *,
        auto_delete_time: typing.Optional[builtins.str] = None,
        auto_delete_ttl: typing.Optional[builtins.str] = None,
        idle_delete_ttl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auto_delete_time: Optional. The time when cluster will be auto-deleted (see JSON representation of `Timestamp <https://developers.google.com/protocol-buffers/docs/proto3#json>`_). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#auto_delete_time DataprocWorkflowTemplate#auto_delete_time}
        :param auto_delete_ttl: Optional. The lifetime duration of cluster. The cluster will be auto-deleted at the end of this period. Minimum value is 10 minutes; maximum value is 14 days (see JSON representation of `Duration <https://developers.google.com/protocol-buffers/docs/proto3#json>`_). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#auto_delete_ttl DataprocWorkflowTemplate#auto_delete_ttl}
        :param idle_delete_ttl: Optional. The duration to keep the cluster alive while idling (when no jobs are running). Passing this threshold will cause the cluster to be deleted. Minimum value is 5 minutes; maximum value is 14 days (see JSON representation of `Duration <https://developers.google.com/protocol-buffers/docs/proto3#json>`_). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#idle_delete_ttl DataprocWorkflowTemplate#idle_delete_ttl}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f3225a864a3460898c26aff121d46ad0d022fd7913f784d394ad4566870fcb5)
            check_type(argname="argument auto_delete_time", value=auto_delete_time, expected_type=type_hints["auto_delete_time"])
            check_type(argname="argument auto_delete_ttl", value=auto_delete_ttl, expected_type=type_hints["auto_delete_ttl"])
            check_type(argname="argument idle_delete_ttl", value=idle_delete_ttl, expected_type=type_hints["idle_delete_ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_delete_time is not None:
            self._values["auto_delete_time"] = auto_delete_time
        if auto_delete_ttl is not None:
            self._values["auto_delete_ttl"] = auto_delete_ttl
        if idle_delete_ttl is not None:
            self._values["idle_delete_ttl"] = idle_delete_ttl

    @builtins.property
    def auto_delete_time(self) -> typing.Optional[builtins.str]:
        '''Optional. The time when cluster will be auto-deleted (see JSON representation of `Timestamp <https://developers.google.com/protocol-buffers/docs/proto3#json>`_).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#auto_delete_time DataprocWorkflowTemplate#auto_delete_time}
        '''
        result = self._values.get("auto_delete_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_delete_ttl(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The lifetime duration of cluster. The cluster will be auto-deleted at the end of this period. Minimum value is 10 minutes; maximum value is 14 days (see JSON representation of `Duration <https://developers.google.com/protocol-buffers/docs/proto3#json>`_).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#auto_delete_ttl DataprocWorkflowTemplate#auto_delete_ttl}
        '''
        result = self._values.get("auto_delete_ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idle_delete_ttl(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The duration to keep the cluster alive while idling (when no jobs are running). Passing this threshold will cause the cluster to be deleted. Minimum value is 5 minutes; maximum value is 14 days (see JSON representation of `Duration <https://developers.google.com/protocol-buffers/docs/proto3#json>`_).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#idle_delete_ttl DataprocWorkflowTemplate#idle_delete_ttl}
        '''
        result = self._values.get("idle_delete_ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigLifecycleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplatePlacementManagedClusterConfigLifecycleConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigLifecycleConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b92e4577ba64f4d3fbe27193ea3378944208b926a953b67acf2e04157c2df94)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAutoDeleteTime")
    def reset_auto_delete_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoDeleteTime", []))

    @jsii.member(jsii_name="resetAutoDeleteTtl")
    def reset_auto_delete_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoDeleteTtl", []))

    @jsii.member(jsii_name="resetIdleDeleteTtl")
    def reset_idle_delete_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdleDeleteTtl", []))

    @builtins.property
    @jsii.member(jsii_name="idleStartTime")
    def idle_start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idleStartTime"))

    @builtins.property
    @jsii.member(jsii_name="autoDeleteTimeInput")
    def auto_delete_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoDeleteTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDeleteTtlInput")
    def auto_delete_ttl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoDeleteTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="idleDeleteTtlInput")
    def idle_delete_ttl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idleDeleteTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDeleteTime")
    def auto_delete_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoDeleteTime"))

    @auto_delete_time.setter
    def auto_delete_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__751dae482320b18fa4a1337cbfe4f968d898457f87958b6ab6987b4e12cf3c5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDeleteTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoDeleteTtl")
    def auto_delete_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoDeleteTtl"))

    @auto_delete_ttl.setter
    def auto_delete_ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7abf5c14a00e5a75085570cd4d9059db73d75677eca3f9ff98ecac4ce3bd9a9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDeleteTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idleDeleteTtl")
    def idle_delete_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idleDeleteTtl"))

    @idle_delete_ttl.setter
    def idle_delete_ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd59f5ac4a12f81262c0e87a8bbd9cc4325c86f66a61e20045a4e6a2103d811)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleDeleteTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigLifecycleConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigLifecycleConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigLifecycleConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80d102040cd6e69fc9c9b87a2092f74de4b514798f52acad275409da775443be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "accelerators": "accelerators",
        "disk_config": "diskConfig",
        "image": "image",
        "machine_type": "machineType",
        "min_cpu_platform": "minCpuPlatform",
        "num_instances": "numInstances",
        "preemptibility": "preemptibility",
    },
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfig:
    def __init__(
        self,
        *,
        accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAccelerators", typing.Dict[builtins.str, typing.Any]]]]] = None,
        disk_config: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigDiskConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        image: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        num_instances: typing.Optional[jsii.Number] = None,
        preemptibility: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accelerators: accelerators block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#accelerators DataprocWorkflowTemplate#accelerators}
        :param disk_config: disk_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#disk_config DataprocWorkflowTemplate#disk_config}
        :param image: Optional. The Compute Engine image resource used for cluster instances. The URI can represent an image or image family. Image examples: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/global/images/[image-id]`` * ``projects/[project_id]/global/images/[image-id]`` * ``image-id`` Image family examples. Dataproc will use the most recent image from the family: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/global/images/family/[custom-image-family-name]`` * ``projects/[project_id]/global/images/family/[custom-image-family-name]`` If the URI is unspecified, it will be inferred from ``SoftwareConfig.image_version`` or the system default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#image DataprocWorkflowTemplate#image}
        :param machine_type: Optional. The Compute Engine machine type used for cluster instances. A full URL, partial URI, or short name are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/zones/us-east1-a/machineTypes/n1-standard-2`` * ``projects/[project_id]/zones/us-east1-a/machineTypes/n1-standard-2`` * ``n1-standard-2`` **Auto Zone Exception**: If you are using the Dataproc `Auto Zone Placement <https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/auto-zone#using_auto_zone_placement>`_ feature, you must use the short name of the machine type resource, for example, ``n1-standard-2``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#machine_type DataprocWorkflowTemplate#machine_type}
        :param min_cpu_platform: Optional. Specifies the minimum cpu platform for the Instance Group. See `Dataproc -> Minimum CPU Platform <https://cloud.google.com/dataproc/docs/concepts/compute/dataproc-min-cpu>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#min_cpu_platform DataprocWorkflowTemplate#min_cpu_platform}
        :param num_instances: Optional. The number of VM instances in the instance group. For `HA cluster </dataproc/docs/concepts/configuring-clusters/high-availability>`_ `master_config <#FIELDS.master_config>`_ groups, **must be set to 3**. For standard cluster `master_config <#FIELDS.master_config>`_ groups, **must be set to 1**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#num_instances DataprocWorkflowTemplate#num_instances}
        :param preemptibility: Optional. Specifies the preemptibility of the instance group. The default value for master and worker groups is ``NON_PREEMPTIBLE``. This default cannot be changed. The default value for secondary instances is ``PREEMPTIBLE``. Possible values: PREEMPTIBILITY_UNSPECIFIED, NON_PREEMPTIBLE, PREEMPTIBLE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#preemptibility DataprocWorkflowTemplate#preemptibility}
        '''
        if isinstance(disk_config, dict):
            disk_config = DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigDiskConfig(**disk_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d861a64500cf3201d0cd5ac1211290ed0b7fe8831e83cf3f82592f96c05e335)
            check_type(argname="argument accelerators", value=accelerators, expected_type=type_hints["accelerators"])
            check_type(argname="argument disk_config", value=disk_config, expected_type=type_hints["disk_config"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument min_cpu_platform", value=min_cpu_platform, expected_type=type_hints["min_cpu_platform"])
            check_type(argname="argument num_instances", value=num_instances, expected_type=type_hints["num_instances"])
            check_type(argname="argument preemptibility", value=preemptibility, expected_type=type_hints["preemptibility"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerators is not None:
            self._values["accelerators"] = accelerators
        if disk_config is not None:
            self._values["disk_config"] = disk_config
        if image is not None:
            self._values["image"] = image
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if min_cpu_platform is not None:
            self._values["min_cpu_platform"] = min_cpu_platform
        if num_instances is not None:
            self._values["num_instances"] = num_instances
        if preemptibility is not None:
            self._values["preemptibility"] = preemptibility

    @builtins.property
    def accelerators(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAccelerators"]]]:
        '''accelerators block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#accelerators DataprocWorkflowTemplate#accelerators}
        '''
        result = self._values.get("accelerators")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAccelerators"]]], result)

    @builtins.property
    def disk_config(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigDiskConfig"]:
        '''disk_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#disk_config DataprocWorkflowTemplate#disk_config}
        '''
        result = self._values.get("disk_config")
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigDiskConfig"], result)

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The Compute Engine image resource used for cluster instances. The URI can represent an image or image family. Image examples: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/global/images/[image-id]`` * ``projects/[project_id]/global/images/[image-id]`` * ``image-id`` Image family examples. Dataproc will use the most recent image from the family: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/global/images/family/[custom-image-family-name]`` * ``projects/[project_id]/global/images/family/[custom-image-family-name]`` If the URI is unspecified, it will be inferred from ``SoftwareConfig.image_version`` or the system default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#image DataprocWorkflowTemplate#image}
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The Compute Engine machine type used for cluster instances. A full URL, partial URI, or short name are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/zones/us-east1-a/machineTypes/n1-standard-2`` * ``projects/[project_id]/zones/us-east1-a/machineTypes/n1-standard-2`` * ``n1-standard-2`` **Auto Zone Exception**: If you are using the Dataproc `Auto Zone Placement <https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/auto-zone#using_auto_zone_placement>`_ feature, you must use the short name of the machine type resource, for example, ``n1-standard-2``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#machine_type DataprocWorkflowTemplate#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_cpu_platform(self) -> typing.Optional[builtins.str]:
        '''Optional. Specifies the minimum cpu platform for the Instance Group. See `Dataproc -> Minimum CPU Platform <https://cloud.google.com/dataproc/docs/concepts/compute/dataproc-min-cpu>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#min_cpu_platform DataprocWorkflowTemplate#min_cpu_platform}
        '''
        result = self._values.get("min_cpu_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_instances(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The number of VM instances in the instance group. For `HA cluster </dataproc/docs/concepts/configuring-clusters/high-availability>`_ `master_config <#FIELDS.master_config>`_ groups, **must be set to 3**. For standard cluster `master_config <#FIELDS.master_config>`_ groups, **must be set to 1**.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#num_instances DataprocWorkflowTemplate#num_instances}
        '''
        result = self._values.get("num_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preemptibility(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Specifies the preemptibility of the instance group. The default value for master and worker groups is ``NON_PREEMPTIBLE``. This default cannot be changed. The default value for secondary instances is ``PREEMPTIBLE``. Possible values: PREEMPTIBILITY_UNSPECIFIED, NON_PREEMPTIBLE, PREEMPTIBLE

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#preemptibility DataprocWorkflowTemplate#preemptibility}
        '''
        result = self._values.get("preemptibility")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAccelerators",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_count": "acceleratorCount",
        "accelerator_type": "acceleratorType",
    },
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAccelerators:
    def __init__(
        self,
        *,
        accelerator_count: typing.Optional[jsii.Number] = None,
        accelerator_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accelerator_count: The number of the accelerator cards of this type exposed to this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#accelerator_count DataprocWorkflowTemplate#accelerator_count}
        :param accelerator_type: Full URL, partial URI, or short name of the accelerator type resource to expose to this instance. See `Compute Engine AcceleratorTypes <https://cloud.google.com/compute/docs/reference/beta/acceleratorTypes>`_. Examples: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/zones/us-east1-a/acceleratorTypes/nvidia-tesla-k80`` * ``projects/[project_id]/zones/us-east1-a/acceleratorTypes/nvidia-tesla-k80`` * ``nvidia-tesla-k80`` **Auto Zone Exception**: If you are using the Dataproc `Auto Zone Placement <https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/auto-zone#using_auto_zone_placement>`_ feature, you must use the short name of the accelerator type resource, for example, ``nvidia-tesla-k80``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#accelerator_type DataprocWorkflowTemplate#accelerator_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08a29aa389e6f97cff955327e704c020e4e216d36b102739e306b65d3d0aa980)
            check_type(argname="argument accelerator_count", value=accelerator_count, expected_type=type_hints["accelerator_count"])
            check_type(argname="argument accelerator_type", value=accelerator_type, expected_type=type_hints["accelerator_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerator_count is not None:
            self._values["accelerator_count"] = accelerator_count
        if accelerator_type is not None:
            self._values["accelerator_type"] = accelerator_type

    @builtins.property
    def accelerator_count(self) -> typing.Optional[jsii.Number]:
        '''The number of the accelerator cards of this type exposed to this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#accelerator_count DataprocWorkflowTemplate#accelerator_count}
        '''
        result = self._values.get("accelerator_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def accelerator_type(self) -> typing.Optional[builtins.str]:
        '''Full URL, partial URI, or short name of the accelerator type resource to expose to this instance.

        See `Compute Engine AcceleratorTypes <https://cloud.google.com/compute/docs/reference/beta/acceleratorTypes>`_. Examples: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/zones/us-east1-a/acceleratorTypes/nvidia-tesla-k80`` * ``projects/[project_id]/zones/us-east1-a/acceleratorTypes/nvidia-tesla-k80`` * ``nvidia-tesla-k80`` **Auto Zone Exception**: If you are using the Dataproc `Auto Zone Placement <https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/auto-zone#using_auto_zone_placement>`_ feature, you must use the short name of the accelerator type resource, for example, ``nvidia-tesla-k80``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#accelerator_type DataprocWorkflowTemplate#accelerator_type}
        '''
        result = self._values.get("accelerator_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAccelerators(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAcceleratorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAcceleratorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f6c827b8bcb4a328c2eaae36ee2d6501de6a4661043764e2b0540a049676fad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAcceleratorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__462405789289c74f29da03115c4049a7800bd46a7e9207a97bc44c27c070b601)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAcceleratorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__041e3aa3caed2257061e4937541633091ee3347bc3a0d9798905047a3e4141a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb25dca68ab9a8bfcda11e0216875091db273d7259dc86c2869ff838a8735d02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fc5cf8b8fa588ac3bc1bed9502663b7948545a32d8d927771159604baa20dea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAccelerators]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAccelerators]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__614f0e8499da3aded1818975d9fc0329b0cb259036252df0ec0f3f43bb7e68f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAcceleratorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAcceleratorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0383b106adc1995b018857a27e17ccc8149cf0883240e71bdc23949d5dca674)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAcceleratorCount")
    def reset_accelerator_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorCount", []))

    @jsii.member(jsii_name="resetAcceleratorType")
    def reset_accelerator_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorType", []))

    @builtins.property
    @jsii.member(jsii_name="acceleratorCountInput")
    def accelerator_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "acceleratorCountInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTypeInput")
    def accelerator_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceleratorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorCount")
    def accelerator_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "acceleratorCount"))

    @accelerator_count.setter
    def accelerator_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6460b6bfb76a8ea963c82f78a93c314fd8e4136d566631332195ee5ac3be104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6f9d751b3f3b2c1737516e3d38fc6d93b5a020aa99048c008c6f2f2d00779a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAccelerators]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAccelerators]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAccelerators]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93e00e629f6fb5369e83112504175ab10eec83c5f1dd3573cb4d6bb0e01ea0d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigDiskConfig",
    jsii_struct_bases=[],
    name_mapping={
        "boot_disk_size_gb": "bootDiskSizeGb",
        "boot_disk_type": "bootDiskType",
        "num_local_ssds": "numLocalSsds",
    },
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigDiskConfig:
    def __init__(
        self,
        *,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        boot_disk_type: typing.Optional[builtins.str] = None,
        num_local_ssds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param boot_disk_size_gb: Optional. Size in GB of the boot disk (default is 500GB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#boot_disk_size_gb DataprocWorkflowTemplate#boot_disk_size_gb}
        :param boot_disk_type: Optional. Type of the boot disk (default is "pd-standard"). Valid values: "pd-balanced" (Persistent Disk Balanced Solid State Drive), "pd-ssd" (Persistent Disk Solid State Drive), or "pd-standard" (Persistent Disk Hard Disk Drive). See `Disk types <https://cloud.google.com/compute/docs/disks#disk-types>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#boot_disk_type DataprocWorkflowTemplate#boot_disk_type}
        :param num_local_ssds: Optional. Number of attached SSDs, from 0 to 4 (default is 0). If SSDs are not attached, the boot disk is used to store runtime logs and `HDFS <https://hadoop.apache.org/docs/r1.2.1/hdfs_user_guide.html>`_ data. If one or more SSDs are attached, this runtime bulk data is spread across them, and the boot disk contains only basic config and installed binaries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#num_local_ssds DataprocWorkflowTemplate#num_local_ssds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b224dcb65dd77665e628a2b17994f2e32d23bcb3650a7afea8c18db128e3f88)
            check_type(argname="argument boot_disk_size_gb", value=boot_disk_size_gb, expected_type=type_hints["boot_disk_size_gb"])
            check_type(argname="argument boot_disk_type", value=boot_disk_type, expected_type=type_hints["boot_disk_type"])
            check_type(argname="argument num_local_ssds", value=num_local_ssds, expected_type=type_hints["num_local_ssds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if boot_disk_size_gb is not None:
            self._values["boot_disk_size_gb"] = boot_disk_size_gb
        if boot_disk_type is not None:
            self._values["boot_disk_type"] = boot_disk_type
        if num_local_ssds is not None:
            self._values["num_local_ssds"] = num_local_ssds

    @builtins.property
    def boot_disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Optional. Size in GB of the boot disk (default is 500GB).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#boot_disk_size_gb DataprocWorkflowTemplate#boot_disk_size_gb}
        '''
        result = self._values.get("boot_disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def boot_disk_type(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Type of the boot disk (default is "pd-standard"). Valid values: "pd-balanced" (Persistent Disk Balanced Solid State Drive), "pd-ssd" (Persistent Disk Solid State Drive), or "pd-standard" (Persistent Disk Hard Disk Drive). See `Disk types <https://cloud.google.com/compute/docs/disks#disk-types>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#boot_disk_type DataprocWorkflowTemplate#boot_disk_type}
        '''
        result = self._values.get("boot_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_local_ssds(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        Number of attached SSDs, from 0 to 4 (default is 0). If SSDs are not attached, the boot disk is used to store runtime logs and `HDFS <https://hadoop.apache.org/docs/r1.2.1/hdfs_user_guide.html>`_ data. If one or more SSDs are attached, this runtime bulk data is spread across them, and the boot disk contains only basic config and installed binaries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#num_local_ssds DataprocWorkflowTemplate#num_local_ssds}
        '''
        result = self._values.get("num_local_ssds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigDiskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigDiskConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigDiskConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a29e14453e1d4375a06cc8bb6469682dd47f3187dd4fdf9893b05af3f80593f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBootDiskSizeGb")
    def reset_boot_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskSizeGb", []))

    @jsii.member(jsii_name="resetBootDiskType")
    def reset_boot_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskType", []))

    @jsii.member(jsii_name="resetNumLocalSsds")
    def reset_num_local_ssds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumLocalSsds", []))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGbInput")
    def boot_disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootDiskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskTypeInput")
    def boot_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="numLocalSsdsInput")
    def num_local_ssds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numLocalSsdsInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGb")
    def boot_disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bootDiskSizeGb"))

    @boot_disk_size_gb.setter
    def boot_disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d278512c7b0720e35530464f14d9a4276b1f18f5fe6bde00dc79c6b293f051ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bootDiskType")
    def boot_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootDiskType"))

    @boot_disk_type.setter
    def boot_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39462ee36aee2314acf7b7dc69abd3b683f25a7ec386b01954d0bf1fc679920e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numLocalSsds")
    def num_local_ssds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numLocalSsds"))

    @num_local_ssds.setter
    def num_local_ssds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71c4148188cbaa0c86b0bc1656ac2acdf535eb29103e449f0a236c1dbaf0da73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numLocalSsds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigDiskConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigDiskConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigDiskConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccfc0a527a592466f10844deb1cff46c91d17eb8d2ca466e5a8569c2d9fa45cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigManagedGroupConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigManagedGroupConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigManagedGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigManagedGroupConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigManagedGroupConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d942dc030b28887ef66f62d3b784337d889573063fe16fcc1215fe23f2f1ac41)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigManagedGroupConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__631d19f42619e9de48f9230c12073e95b779b5fa0ba863e818bd73724ee8cecc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigManagedGroupConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e8eb562df29c03bc7808c87b658c6a403201a8d2e1db0e94004ecd04673000b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__396c8d509da2ff9155ae702bceab77e0a425f18610764ca3553d0f2b4c33d73b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93380cc938ba1e499e056df27b9f88f33991199ea374318991a133d7b710d654)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigManagedGroupConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigManagedGroupConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8e261868845ef3eee4544a69f993b2049460801f4a27d8336b90473043a4175)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="instanceGroupManagerName")
    def instance_group_manager_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceGroupManagerName"))

    @builtins.property
    @jsii.member(jsii_name="instanceTemplateName")
    def instance_template_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceTemplateName"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigManagedGroupConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigManagedGroupConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigManagedGroupConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6f32866110649253bbf32d729c52d8b0da9aee8c30dc016ec78cfac301f3cd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc057b0f331298aa05d2f8d9ab818c6a6286eb8fbfd4fd69fd8ab7fa0e40ad2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccelerators")
    def put_accelerators(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32c14d1aaa5e80edd6db9409315a08a350c479c95a45ca78e1bd530634a50a6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccelerators", [value]))

    @jsii.member(jsii_name="putDiskConfig")
    def put_disk_config(
        self,
        *,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        boot_disk_type: typing.Optional[builtins.str] = None,
        num_local_ssds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param boot_disk_size_gb: Optional. Size in GB of the boot disk (default is 500GB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#boot_disk_size_gb DataprocWorkflowTemplate#boot_disk_size_gb}
        :param boot_disk_type: Optional. Type of the boot disk (default is "pd-standard"). Valid values: "pd-balanced" (Persistent Disk Balanced Solid State Drive), "pd-ssd" (Persistent Disk Solid State Drive), or "pd-standard" (Persistent Disk Hard Disk Drive). See `Disk types <https://cloud.google.com/compute/docs/disks#disk-types>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#boot_disk_type DataprocWorkflowTemplate#boot_disk_type}
        :param num_local_ssds: Optional. Number of attached SSDs, from 0 to 4 (default is 0). If SSDs are not attached, the boot disk is used to store runtime logs and `HDFS <https://hadoop.apache.org/docs/r1.2.1/hdfs_user_guide.html>`_ data. If one or more SSDs are attached, this runtime bulk data is spread across them, and the boot disk contains only basic config and installed binaries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#num_local_ssds DataprocWorkflowTemplate#num_local_ssds}
        '''
        value = DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigDiskConfig(
            boot_disk_size_gb=boot_disk_size_gb,
            boot_disk_type=boot_disk_type,
            num_local_ssds=num_local_ssds,
        )

        return typing.cast(None, jsii.invoke(self, "putDiskConfig", [value]))

    @jsii.member(jsii_name="resetAccelerators")
    def reset_accelerators(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccelerators", []))

    @jsii.member(jsii_name="resetDiskConfig")
    def reset_disk_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskConfig", []))

    @jsii.member(jsii_name="resetImage")
    def reset_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImage", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @jsii.member(jsii_name="resetMinCpuPlatform")
    def reset_min_cpu_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinCpuPlatform", []))

    @jsii.member(jsii_name="resetNumInstances")
    def reset_num_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumInstances", []))

    @jsii.member(jsii_name="resetPreemptibility")
    def reset_preemptibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreemptibility", []))

    @builtins.property
    @jsii.member(jsii_name="accelerators")
    def accelerators(
        self,
    ) -> DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAcceleratorsList:
        return typing.cast(DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAcceleratorsList, jsii.get(self, "accelerators"))

    @builtins.property
    @jsii.member(jsii_name="diskConfig")
    def disk_config(
        self,
    ) -> DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigDiskConfigOutputReference:
        return typing.cast(DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigDiskConfigOutputReference, jsii.get(self, "diskConfig"))

    @builtins.property
    @jsii.member(jsii_name="instanceNames")
    def instance_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceNames"))

    @builtins.property
    @jsii.member(jsii_name="isPreemptible")
    def is_preemptible(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isPreemptible"))

    @builtins.property
    @jsii.member(jsii_name="managedGroupConfig")
    def managed_group_config(
        self,
    ) -> DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigManagedGroupConfigList:
        return typing.cast(DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigManagedGroupConfigList, jsii.get(self, "managedGroupConfig"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorsInput")
    def accelerators_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAccelerators]]], jsii.get(self, "acceleratorsInput"))

    @builtins.property
    @jsii.member(jsii_name="diskConfigInput")
    def disk_config_input(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigDiskConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigDiskConfig], jsii.get(self, "diskConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatformInput")
    def min_cpu_platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minCpuPlatformInput"))

    @builtins.property
    @jsii.member(jsii_name="numInstancesInput")
    def num_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="preemptibilityInput")
    def preemptibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preemptibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__759c2b8e332279d9a965c3db9d6877d1365518c2cf755f0c8fafd28aef1762ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__797aee0031ee759b50dc5bd2c1d069d9d176df626c1df79a67b7a12c5ba51a71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatform")
    def min_cpu_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minCpuPlatform"))

    @min_cpu_platform.setter
    def min_cpu_platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db0a33f6ed1a4c815aed61b0a8ab2b95a93cc320e8ae7514a4b2814e4870f58a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCpuPlatform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numInstances")
    def num_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numInstances"))

    @num_instances.setter
    def num_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e45d95f30e9c429d8eed5725fdbfe041d5e8fe5452b0ea90e929abfe565783a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preemptibility")
    def preemptibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preemptibility"))

    @preemptibility.setter
    def preemptibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__444d36afdced6ab6680d2da53813634230ff6e2089475f2ed2e640a64b50db78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preemptibility", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__594c813b56ee26ff0cc0c3ed8054b37f25d4e2172f8798ebf39eb78a820251a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplatePlacementManagedClusterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b88054c718dc117ae1e31322e6eb5dd72dddce9639e4cb01e72442793f679b9c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscalingConfig")
    def put_autoscaling_config(
        self,
        *,
        policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param policy: Optional. The autoscaling policy used by the cluster. Only resource names including projectid and location (region) are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/locations/[dataproc_region]/autoscalingPolicies/[policy_id]`` * ``projects/[project_id]/locations/[dataproc_region]/autoscalingPolicies/[policy_id]`` Note that the policy must be in the same project and Dataproc region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#policy DataprocWorkflowTemplate#policy}
        '''
        value = DataprocWorkflowTemplatePlacementManagedClusterConfigAutoscalingConfig(
            policy=policy
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscalingConfig", [value]))

    @jsii.member(jsii_name="putEncryptionConfig")
    def put_encryption_config(
        self,
        *,
        gce_pd_kms_key_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gce_pd_kms_key_name: Optional. The Cloud KMS key name to use for PD disk encryption for all instances in the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#gce_pd_kms_key_name DataprocWorkflowTemplate#gce_pd_kms_key_name}
        '''
        value = DataprocWorkflowTemplatePlacementManagedClusterConfigEncryptionConfig(
            gce_pd_kms_key_name=gce_pd_kms_key_name
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfig", [value]))

    @jsii.member(jsii_name="putEndpointConfig")
    def put_endpoint_config(
        self,
        *,
        enable_http_port_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_http_port_access: Optional. If true, enable http access to specific ports on the cluster from external sources. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#enable_http_port_access DataprocWorkflowTemplate#enable_http_port_access}
        '''
        value = DataprocWorkflowTemplatePlacementManagedClusterConfigEndpointConfig(
            enable_http_port_access=enable_http_port_access
        )

        return typing.cast(None, jsii.invoke(self, "putEndpointConfig", [value]))

    @jsii.member(jsii_name="putGceClusterConfig")
    def put_gce_cluster_config(
        self,
        *,
        internal_ip_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network: typing.Optional[builtins.str] = None,
        node_group_affinity: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigNodeGroupAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
        private_ipv6_google_access: typing.Optional[builtins.str] = None,
        reservation_affinity: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigReservationAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[builtins.str] = None,
        service_account_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        shielded_instance_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param internal_ip_only: Optional. If true, all instances in the cluster will only have internal IP addresses. By default, clusters are not restricted to internal IP addresses, and will have ephemeral external IP addresses assigned to each instance. This ``internal_ip_only`` restriction can only be enabled for subnetwork enabled networks, and all off-cluster dependencies must be configured to be accessible without external IP addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#internal_ip_only DataprocWorkflowTemplate#internal_ip_only}
        :param metadata: The Compute Engine metadata entries to add to all instances (see `Project and instance metadata <https://cloud.google.com/compute/docs/storing-retrieving-metadata#project_and_instance_metadata>`_). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#metadata DataprocWorkflowTemplate#metadata}
        :param network: Optional. The Compute Engine network to be used for machine communications. Cannot be specified with subnetwork_uri. If neither ``network_uri`` nor ``subnetwork_uri`` is specified, the "default" network of the project is used, if it exists. Cannot be a "Custom Subnet Network" (see `Using Subnetworks <https://cloud.google.com/compute/docs/subnetworks>`_ for more information). A full URL, partial URI, or short name are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/regions/global/default`` * ``projects/[project_id]/regions/global/default`` * ``default`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#network DataprocWorkflowTemplate#network}
        :param node_group_affinity: node_group_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#node_group_affinity DataprocWorkflowTemplate#node_group_affinity}
        :param private_ipv6_google_access: Optional. The type of IPv6 access for a cluster. Possible values: PRIVATE_IPV6_GOOGLE_ACCESS_UNSPECIFIED, INHERIT_FROM_SUBNETWORK, OUTBOUND, BIDIRECTIONAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#private_ipv6_google_access DataprocWorkflowTemplate#private_ipv6_google_access}
        :param reservation_affinity: reservation_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#reservation_affinity DataprocWorkflowTemplate#reservation_affinity}
        :param service_account: Optional. The `Dataproc service account <https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/service-accounts#service_accounts_in_dataproc>`_ (also see `VM Data Plane identity <https://cloud.google.com/dataproc/docs/concepts/iam/dataproc-principals#vm_service_account_data_plane_identity>`_) used by Dataproc cluster VM instances to access Google Cloud Platform services. If not specified, the `Compute Engine default service account <https://cloud.google.com/compute/docs/access/service-accounts#default_service_account>`_ is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#service_account DataprocWorkflowTemplate#service_account}
        :param service_account_scopes: Optional. The URIs of service account scopes to be included in Compute Engine instances. The following base set of scopes is always included: * https://www.googleapis.com/auth/cloud.useraccounts.readonly * https://www.googleapis.com/auth/devstorage.read_write * https://www.googleapis.com/auth/logging.write If no scopes are specified, the following defaults are also provided: * https://www.googleapis.com/auth/bigquery * https://www.googleapis.com/auth/bigtable.admin.table * https://www.googleapis.com/auth/bigtable.data * https://www.googleapis.com/auth/devstorage.full_control Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#service_account_scopes DataprocWorkflowTemplate#service_account_scopes}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#shielded_instance_config DataprocWorkflowTemplate#shielded_instance_config}
        :param subnetwork: Optional. The Compute Engine subnetwork to be used for machine communications. Cannot be specified with network_uri. A full URL, partial URI, or short name are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/regions/us-east1/subnetworks/sub0`` * ``projects/[project_id]/regions/us-east1/subnetworks/sub0`` * ``sub0`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#subnetwork DataprocWorkflowTemplate#subnetwork}
        :param tags: The Compute Engine tags to add to all instances (see `Tagging instances <https://cloud.google.com/compute/docs/label-or-tag-resources#tags>`_). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#tags DataprocWorkflowTemplate#tags}
        :param zone: Optional. The zone where the Compute Engine cluster will be located. On a create request, it is required in the "global" region. If omitted in a non-global Dataproc region, the service will pick a zone in the corresponding Compute Engine region. On a get request, zone will always be present. A full URL, partial URI, or short name are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/zones/[zone]`` * ``projects/[project_id]/zones/[zone]`` * ``us-central1-f`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#zone DataprocWorkflowTemplate#zone}
        '''
        value = DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfig(
            internal_ip_only=internal_ip_only,
            metadata=metadata,
            network=network,
            node_group_affinity=node_group_affinity,
            private_ipv6_google_access=private_ipv6_google_access,
            reservation_affinity=reservation_affinity,
            service_account=service_account,
            service_account_scopes=service_account_scopes,
            shielded_instance_config=shielded_instance_config,
            subnetwork=subnetwork,
            tags=tags,
            zone=zone,
        )

        return typing.cast(None, jsii.invoke(self, "putGceClusterConfig", [value]))

    @jsii.member(jsii_name="putInitializationActions")
    def put_initialization_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc6f8d5b328078083d23a699123c00bdc2402ff9700dc8d583d06207535a25a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInitializationActions", [value]))

    @jsii.member(jsii_name="putLifecycleConfig")
    def put_lifecycle_config(
        self,
        *,
        auto_delete_time: typing.Optional[builtins.str] = None,
        auto_delete_ttl: typing.Optional[builtins.str] = None,
        idle_delete_ttl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auto_delete_time: Optional. The time when cluster will be auto-deleted (see JSON representation of `Timestamp <https://developers.google.com/protocol-buffers/docs/proto3#json>`_). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#auto_delete_time DataprocWorkflowTemplate#auto_delete_time}
        :param auto_delete_ttl: Optional. The lifetime duration of cluster. The cluster will be auto-deleted at the end of this period. Minimum value is 10 minutes; maximum value is 14 days (see JSON representation of `Duration <https://developers.google.com/protocol-buffers/docs/proto3#json>`_). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#auto_delete_ttl DataprocWorkflowTemplate#auto_delete_ttl}
        :param idle_delete_ttl: Optional. The duration to keep the cluster alive while idling (when no jobs are running). Passing this threshold will cause the cluster to be deleted. Minimum value is 5 minutes; maximum value is 14 days (see JSON representation of `Duration <https://developers.google.com/protocol-buffers/docs/proto3#json>`_). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#idle_delete_ttl DataprocWorkflowTemplate#idle_delete_ttl}
        '''
        value = DataprocWorkflowTemplatePlacementManagedClusterConfigLifecycleConfig(
            auto_delete_time=auto_delete_time,
            auto_delete_ttl=auto_delete_ttl,
            idle_delete_ttl=idle_delete_ttl,
        )

        return typing.cast(None, jsii.invoke(self, "putLifecycleConfig", [value]))

    @jsii.member(jsii_name="putMasterConfig")
    def put_master_config(
        self,
        *,
        accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
        disk_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigDiskConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        image: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        num_instances: typing.Optional[jsii.Number] = None,
        preemptibility: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accelerators: accelerators block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#accelerators DataprocWorkflowTemplate#accelerators}
        :param disk_config: disk_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#disk_config DataprocWorkflowTemplate#disk_config}
        :param image: Optional. The Compute Engine image resource used for cluster instances. The URI can represent an image or image family. Image examples: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/global/images/[image-id]`` * ``projects/[project_id]/global/images/[image-id]`` * ``image-id`` Image family examples. Dataproc will use the most recent image from the family: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/global/images/family/[custom-image-family-name]`` * ``projects/[project_id]/global/images/family/[custom-image-family-name]`` If the URI is unspecified, it will be inferred from ``SoftwareConfig.image_version`` or the system default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#image DataprocWorkflowTemplate#image}
        :param machine_type: Optional. The Compute Engine machine type used for cluster instances. A full URL, partial URI, or short name are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/zones/us-east1-a/machineTypes/n1-standard-2`` * ``projects/[project_id]/zones/us-east1-a/machineTypes/n1-standard-2`` * ``n1-standard-2`` **Auto Zone Exception**: If you are using the Dataproc `Auto Zone Placement <https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/auto-zone#using_auto_zone_placement>`_ feature, you must use the short name of the machine type resource, for example, ``n1-standard-2``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#machine_type DataprocWorkflowTemplate#machine_type}
        :param min_cpu_platform: Optional. Specifies the minimum cpu platform for the Instance Group. See `Dataproc -> Minimum CPU Platform <https://cloud.google.com/dataproc/docs/concepts/compute/dataproc-min-cpu>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#min_cpu_platform DataprocWorkflowTemplate#min_cpu_platform}
        :param num_instances: Optional. The number of VM instances in the instance group. For `HA cluster </dataproc/docs/concepts/configuring-clusters/high-availability>`_ `master_config <#FIELDS.master_config>`_ groups, **must be set to 3**. For standard cluster `master_config <#FIELDS.master_config>`_ groups, **must be set to 1**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#num_instances DataprocWorkflowTemplate#num_instances}
        :param preemptibility: Optional. Specifies the preemptibility of the instance group. The default value for master and worker groups is ``NON_PREEMPTIBLE``. This default cannot be changed. The default value for secondary instances is ``PREEMPTIBLE``. Possible values: PREEMPTIBILITY_UNSPECIFIED, NON_PREEMPTIBLE, PREEMPTIBLE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#preemptibility DataprocWorkflowTemplate#preemptibility}
        '''
        value = DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfig(
            accelerators=accelerators,
            disk_config=disk_config,
            image=image,
            machine_type=machine_type,
            min_cpu_platform=min_cpu_platform,
            num_instances=num_instances,
            preemptibility=preemptibility,
        )

        return typing.cast(None, jsii.invoke(self, "putMasterConfig", [value]))

    @jsii.member(jsii_name="putSecondaryWorkerConfig")
    def put_secondary_worker_config(
        self,
        *,
        accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAccelerators", typing.Dict[builtins.str, typing.Any]]]]] = None,
        disk_config: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigDiskConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        image: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        num_instances: typing.Optional[jsii.Number] = None,
        preemptibility: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accelerators: accelerators block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#accelerators DataprocWorkflowTemplate#accelerators}
        :param disk_config: disk_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#disk_config DataprocWorkflowTemplate#disk_config}
        :param image: Optional. The Compute Engine image resource used for cluster instances. The URI can represent an image or image family. Image examples: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/global/images/[image-id]`` * ``projects/[project_id]/global/images/[image-id]`` * ``image-id`` Image family examples. Dataproc will use the most recent image from the family: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/global/images/family/[custom-image-family-name]`` * ``projects/[project_id]/global/images/family/[custom-image-family-name]`` If the URI is unspecified, it will be inferred from ``SoftwareConfig.image_version`` or the system default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#image DataprocWorkflowTemplate#image}
        :param machine_type: Optional. The Compute Engine machine type used for cluster instances. A full URL, partial URI, or short name are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/zones/us-east1-a/machineTypes/n1-standard-2`` * ``projects/[project_id]/zones/us-east1-a/machineTypes/n1-standard-2`` * ``n1-standard-2`` **Auto Zone Exception**: If you are using the Dataproc `Auto Zone Placement <https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/auto-zone#using_auto_zone_placement>`_ feature, you must use the short name of the machine type resource, for example, ``n1-standard-2``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#machine_type DataprocWorkflowTemplate#machine_type}
        :param min_cpu_platform: Optional. Specifies the minimum cpu platform for the Instance Group. See `Dataproc -> Minimum CPU Platform <https://cloud.google.com/dataproc/docs/concepts/compute/dataproc-min-cpu>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#min_cpu_platform DataprocWorkflowTemplate#min_cpu_platform}
        :param num_instances: Optional. The number of VM instances in the instance group. For `HA cluster </dataproc/docs/concepts/configuring-clusters/high-availability>`_ `master_config <#FIELDS.master_config>`_ groups, **must be set to 3**. For standard cluster `master_config <#FIELDS.master_config>`_ groups, **must be set to 1**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#num_instances DataprocWorkflowTemplate#num_instances}
        :param preemptibility: Optional. Specifies the preemptibility of the instance group. The default value for master and worker groups is ``NON_PREEMPTIBLE``. This default cannot be changed. The default value for secondary instances is ``PREEMPTIBLE``. Possible values: PREEMPTIBILITY_UNSPECIFIED, NON_PREEMPTIBLE, PREEMPTIBLE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#preemptibility DataprocWorkflowTemplate#preemptibility}
        '''
        value = DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfig(
            accelerators=accelerators,
            disk_config=disk_config,
            image=image,
            machine_type=machine_type,
            min_cpu_platform=min_cpu_platform,
            num_instances=num_instances,
            preemptibility=preemptibility,
        )

        return typing.cast(None, jsii.invoke(self, "putSecondaryWorkerConfig", [value]))

    @jsii.member(jsii_name="putSecurityConfig")
    def put_security_config(
        self,
        *,
        kerberos_config: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigKerberosConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param kerberos_config: kerberos_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#kerberos_config DataprocWorkflowTemplate#kerberos_config}
        '''
        value = DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfig(
            kerberos_config=kerberos_config
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityConfig", [value]))

    @jsii.member(jsii_name="putSoftwareConfig")
    def put_software_config(
        self,
        *,
        image_version: typing.Optional[builtins.str] = None,
        optional_components: typing.Optional[typing.Sequence[builtins.str]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param image_version: Optional. The version of software inside the cluster. It must be one of the supported `Dataproc Versions <https://cloud.google.com/dataproc/docs/concepts/versioning/dataproc-versions#supported_dataproc_versions>`_, such as "1.2" (including a subminor version, such as "1.2.29"), or the `"preview" version <https://cloud.google.com/dataproc/docs/concepts/versioning/dataproc-versions#other_versions>`_. If unspecified, it defaults to the latest Debian version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#image_version DataprocWorkflowTemplate#image_version}
        :param optional_components: Optional. The set of components to activate on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#optional_components DataprocWorkflowTemplate#optional_components}
        :param properties: Optional. The properties to set on daemon config files. Property keys are specified in ``prefix:property`` format, for example ``core:hadoop.tmp.dir``. The following are supported prefixes and their mappings: * capacity-scheduler: ``capacity-scheduler.xml`` * core: ``core-site.xml`` * distcp: ``distcp-default.xml`` * hdfs: ``hdfs-site.xml`` * hive: ``hive-site.xml`` * mapred: ``mapred-site.xml`` * pig: ``pig.properties`` * spark: ``spark-defaults.conf`` * yarn: ``yarn-site.xml`` For more information, see `Cluster properties <https://cloud.google.com/dataproc/docs/concepts/cluster-properties>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        '''
        value = DataprocWorkflowTemplatePlacementManagedClusterConfigSoftwareConfig(
            image_version=image_version,
            optional_components=optional_components,
            properties=properties,
        )

        return typing.cast(None, jsii.invoke(self, "putSoftwareConfig", [value]))

    @jsii.member(jsii_name="putWorkerConfig")
    def put_worker_config(
        self,
        *,
        accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAccelerators", typing.Dict[builtins.str, typing.Any]]]]] = None,
        disk_config: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigDiskConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        image: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        num_instances: typing.Optional[jsii.Number] = None,
        preemptibility: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accelerators: accelerators block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#accelerators DataprocWorkflowTemplate#accelerators}
        :param disk_config: disk_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#disk_config DataprocWorkflowTemplate#disk_config}
        :param image: Optional. The Compute Engine image resource used for cluster instances. The URI can represent an image or image family. Image examples: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/global/images/[image-id]`` * ``projects/[project_id]/global/images/[image-id]`` * ``image-id`` Image family examples. Dataproc will use the most recent image from the family: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/global/images/family/[custom-image-family-name]`` * ``projects/[project_id]/global/images/family/[custom-image-family-name]`` If the URI is unspecified, it will be inferred from ``SoftwareConfig.image_version`` or the system default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#image DataprocWorkflowTemplate#image}
        :param machine_type: Optional. The Compute Engine machine type used for cluster instances. A full URL, partial URI, or short name are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/zones/us-east1-a/machineTypes/n1-standard-2`` * ``projects/[project_id]/zones/us-east1-a/machineTypes/n1-standard-2`` * ``n1-standard-2`` **Auto Zone Exception**: If you are using the Dataproc `Auto Zone Placement <https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/auto-zone#using_auto_zone_placement>`_ feature, you must use the short name of the machine type resource, for example, ``n1-standard-2``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#machine_type DataprocWorkflowTemplate#machine_type}
        :param min_cpu_platform: Optional. Specifies the minimum cpu platform for the Instance Group. See `Dataproc -> Minimum CPU Platform <https://cloud.google.com/dataproc/docs/concepts/compute/dataproc-min-cpu>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#min_cpu_platform DataprocWorkflowTemplate#min_cpu_platform}
        :param num_instances: Optional. The number of VM instances in the instance group. For `HA cluster </dataproc/docs/concepts/configuring-clusters/high-availability>`_ `master_config <#FIELDS.master_config>`_ groups, **must be set to 3**. For standard cluster `master_config <#FIELDS.master_config>`_ groups, **must be set to 1**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#num_instances DataprocWorkflowTemplate#num_instances}
        :param preemptibility: Optional. Specifies the preemptibility of the instance group. The default value for master and worker groups is ``NON_PREEMPTIBLE``. This default cannot be changed. The default value for secondary instances is ``PREEMPTIBLE``. Possible values: PREEMPTIBILITY_UNSPECIFIED, NON_PREEMPTIBLE, PREEMPTIBLE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#preemptibility DataprocWorkflowTemplate#preemptibility}
        '''
        value = DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfig(
            accelerators=accelerators,
            disk_config=disk_config,
            image=image,
            machine_type=machine_type,
            min_cpu_platform=min_cpu_platform,
            num_instances=num_instances,
            preemptibility=preemptibility,
        )

        return typing.cast(None, jsii.invoke(self, "putWorkerConfig", [value]))

    @jsii.member(jsii_name="resetAutoscalingConfig")
    def reset_autoscaling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscalingConfig", []))

    @jsii.member(jsii_name="resetEncryptionConfig")
    def reset_encryption_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfig", []))

    @jsii.member(jsii_name="resetEndpointConfig")
    def reset_endpoint_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointConfig", []))

    @jsii.member(jsii_name="resetGceClusterConfig")
    def reset_gce_cluster_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGceClusterConfig", []))

    @jsii.member(jsii_name="resetInitializationActions")
    def reset_initialization_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitializationActions", []))

    @jsii.member(jsii_name="resetLifecycleConfig")
    def reset_lifecycle_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfig", []))

    @jsii.member(jsii_name="resetMasterConfig")
    def reset_master_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMasterConfig", []))

    @jsii.member(jsii_name="resetSecondaryWorkerConfig")
    def reset_secondary_worker_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryWorkerConfig", []))

    @jsii.member(jsii_name="resetSecurityConfig")
    def reset_security_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityConfig", []))

    @jsii.member(jsii_name="resetSoftwareConfig")
    def reset_software_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSoftwareConfig", []))

    @jsii.member(jsii_name="resetStagingBucket")
    def reset_staging_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStagingBucket", []))

    @jsii.member(jsii_name="resetTempBucket")
    def reset_temp_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTempBucket", []))

    @jsii.member(jsii_name="resetWorkerConfig")
    def reset_worker_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerConfig", []))

    @builtins.property
    @jsii.member(jsii_name="autoscalingConfig")
    def autoscaling_config(
        self,
    ) -> DataprocWorkflowTemplatePlacementManagedClusterConfigAutoscalingConfigOutputReference:
        return typing.cast(DataprocWorkflowTemplatePlacementManagedClusterConfigAutoscalingConfigOutputReference, jsii.get(self, "autoscalingConfig"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfig")
    def encryption_config(
        self,
    ) -> DataprocWorkflowTemplatePlacementManagedClusterConfigEncryptionConfigOutputReference:
        return typing.cast(DataprocWorkflowTemplatePlacementManagedClusterConfigEncryptionConfigOutputReference, jsii.get(self, "encryptionConfig"))

    @builtins.property
    @jsii.member(jsii_name="endpointConfig")
    def endpoint_config(
        self,
    ) -> DataprocWorkflowTemplatePlacementManagedClusterConfigEndpointConfigOutputReference:
        return typing.cast(DataprocWorkflowTemplatePlacementManagedClusterConfigEndpointConfigOutputReference, jsii.get(self, "endpointConfig"))

    @builtins.property
    @jsii.member(jsii_name="gceClusterConfig")
    def gce_cluster_config(
        self,
    ) -> DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigOutputReference:
        return typing.cast(DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigOutputReference, jsii.get(self, "gceClusterConfig"))

    @builtins.property
    @jsii.member(jsii_name="initializationActions")
    def initialization_actions(
        self,
    ) -> DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActionsList:
        return typing.cast(DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActionsList, jsii.get(self, "initializationActions"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfig")
    def lifecycle_config(
        self,
    ) -> DataprocWorkflowTemplatePlacementManagedClusterConfigLifecycleConfigOutputReference:
        return typing.cast(DataprocWorkflowTemplatePlacementManagedClusterConfigLifecycleConfigOutputReference, jsii.get(self, "lifecycleConfig"))

    @builtins.property
    @jsii.member(jsii_name="masterConfig")
    def master_config(
        self,
    ) -> DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigOutputReference:
        return typing.cast(DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigOutputReference, jsii.get(self, "masterConfig"))

    @builtins.property
    @jsii.member(jsii_name="secondaryWorkerConfig")
    def secondary_worker_config(
        self,
    ) -> "DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigOutputReference":
        return typing.cast("DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigOutputReference", jsii.get(self, "secondaryWorkerConfig"))

    @builtins.property
    @jsii.member(jsii_name="securityConfig")
    def security_config(
        self,
    ) -> "DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigOutputReference":
        return typing.cast("DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigOutputReference", jsii.get(self, "securityConfig"))

    @builtins.property
    @jsii.member(jsii_name="softwareConfig")
    def software_config(
        self,
    ) -> "DataprocWorkflowTemplatePlacementManagedClusterConfigSoftwareConfigOutputReference":
        return typing.cast("DataprocWorkflowTemplatePlacementManagedClusterConfigSoftwareConfigOutputReference", jsii.get(self, "softwareConfig"))

    @builtins.property
    @jsii.member(jsii_name="workerConfig")
    def worker_config(
        self,
    ) -> "DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigOutputReference":
        return typing.cast("DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigOutputReference", jsii.get(self, "workerConfig"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingConfigInput")
    def autoscaling_config_input(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigAutoscalingConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigAutoscalingConfig], jsii.get(self, "autoscalingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigInput")
    def encryption_config_input(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigEncryptionConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigEncryptionConfig], jsii.get(self, "encryptionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointConfigInput")
    def endpoint_config_input(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigEndpointConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigEndpointConfig], jsii.get(self, "endpointConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="gceClusterConfigInput")
    def gce_cluster_config_input(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfig], jsii.get(self, "gceClusterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="initializationActionsInput")
    def initialization_actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActions]]], jsii.get(self, "initializationActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigInput")
    def lifecycle_config_input(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigLifecycleConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigLifecycleConfig], jsii.get(self, "lifecycleConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="masterConfigInput")
    def master_config_input(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfig], jsii.get(self, "masterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryWorkerConfigInput")
    def secondary_worker_config_input(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfig"]:
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfig"], jsii.get(self, "secondaryWorkerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="securityConfigInput")
    def security_config_input(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfig"]:
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfig"], jsii.get(self, "securityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="softwareConfigInput")
    def software_config_input(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigSoftwareConfig"]:
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigSoftwareConfig"], jsii.get(self, "softwareConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="stagingBucketInput")
    def staging_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stagingBucketInput"))

    @builtins.property
    @jsii.member(jsii_name="tempBucketInput")
    def temp_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tempBucketInput"))

    @builtins.property
    @jsii.member(jsii_name="workerConfigInput")
    def worker_config_input(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfig"]:
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfig"], jsii.get(self, "workerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="stagingBucket")
    def staging_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stagingBucket"))

    @staging_bucket.setter
    def staging_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e301e870ce72b6b876c30e2dbf6775ab92faff3b16b3f7562600dd93f44d01c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stagingBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tempBucket")
    def temp_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tempBucket"))

    @temp_bucket.setter
    def temp_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e2bfead03ce73a68fd1c3e02050d8164f0e0654944f5d7f9b638a8b2936241f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tempBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f7adbd4c601479eeda393001d512620987051a91e7dd062b4094fd3b7ff33b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "accelerators": "accelerators",
        "disk_config": "diskConfig",
        "image": "image",
        "machine_type": "machineType",
        "min_cpu_platform": "minCpuPlatform",
        "num_instances": "numInstances",
        "preemptibility": "preemptibility",
    },
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfig:
    def __init__(
        self,
        *,
        accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAccelerators", typing.Dict[builtins.str, typing.Any]]]]] = None,
        disk_config: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigDiskConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        image: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        num_instances: typing.Optional[jsii.Number] = None,
        preemptibility: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accelerators: accelerators block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#accelerators DataprocWorkflowTemplate#accelerators}
        :param disk_config: disk_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#disk_config DataprocWorkflowTemplate#disk_config}
        :param image: Optional. The Compute Engine image resource used for cluster instances. The URI can represent an image or image family. Image examples: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/global/images/[image-id]`` * ``projects/[project_id]/global/images/[image-id]`` * ``image-id`` Image family examples. Dataproc will use the most recent image from the family: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/global/images/family/[custom-image-family-name]`` * ``projects/[project_id]/global/images/family/[custom-image-family-name]`` If the URI is unspecified, it will be inferred from ``SoftwareConfig.image_version`` or the system default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#image DataprocWorkflowTemplate#image}
        :param machine_type: Optional. The Compute Engine machine type used for cluster instances. A full URL, partial URI, or short name are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/zones/us-east1-a/machineTypes/n1-standard-2`` * ``projects/[project_id]/zones/us-east1-a/machineTypes/n1-standard-2`` * ``n1-standard-2`` **Auto Zone Exception**: If you are using the Dataproc `Auto Zone Placement <https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/auto-zone#using_auto_zone_placement>`_ feature, you must use the short name of the machine type resource, for example, ``n1-standard-2``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#machine_type DataprocWorkflowTemplate#machine_type}
        :param min_cpu_platform: Optional. Specifies the minimum cpu platform for the Instance Group. See `Dataproc -> Minimum CPU Platform <https://cloud.google.com/dataproc/docs/concepts/compute/dataproc-min-cpu>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#min_cpu_platform DataprocWorkflowTemplate#min_cpu_platform}
        :param num_instances: Optional. The number of VM instances in the instance group. For `HA cluster </dataproc/docs/concepts/configuring-clusters/high-availability>`_ `master_config <#FIELDS.master_config>`_ groups, **must be set to 3**. For standard cluster `master_config <#FIELDS.master_config>`_ groups, **must be set to 1**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#num_instances DataprocWorkflowTemplate#num_instances}
        :param preemptibility: Optional. Specifies the preemptibility of the instance group. The default value for master and worker groups is ``NON_PREEMPTIBLE``. This default cannot be changed. The default value for secondary instances is ``PREEMPTIBLE``. Possible values: PREEMPTIBILITY_UNSPECIFIED, NON_PREEMPTIBLE, PREEMPTIBLE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#preemptibility DataprocWorkflowTemplate#preemptibility}
        '''
        if isinstance(disk_config, dict):
            disk_config = DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigDiskConfig(**disk_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c00fe29f9abdc543d8f89e6154537d1100e78a9fb4b4b1fc867b59963c18c017)
            check_type(argname="argument accelerators", value=accelerators, expected_type=type_hints["accelerators"])
            check_type(argname="argument disk_config", value=disk_config, expected_type=type_hints["disk_config"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument min_cpu_platform", value=min_cpu_platform, expected_type=type_hints["min_cpu_platform"])
            check_type(argname="argument num_instances", value=num_instances, expected_type=type_hints["num_instances"])
            check_type(argname="argument preemptibility", value=preemptibility, expected_type=type_hints["preemptibility"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerators is not None:
            self._values["accelerators"] = accelerators
        if disk_config is not None:
            self._values["disk_config"] = disk_config
        if image is not None:
            self._values["image"] = image
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if min_cpu_platform is not None:
            self._values["min_cpu_platform"] = min_cpu_platform
        if num_instances is not None:
            self._values["num_instances"] = num_instances
        if preemptibility is not None:
            self._values["preemptibility"] = preemptibility

    @builtins.property
    def accelerators(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAccelerators"]]]:
        '''accelerators block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#accelerators DataprocWorkflowTemplate#accelerators}
        '''
        result = self._values.get("accelerators")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAccelerators"]]], result)

    @builtins.property
    def disk_config(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigDiskConfig"]:
        '''disk_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#disk_config DataprocWorkflowTemplate#disk_config}
        '''
        result = self._values.get("disk_config")
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigDiskConfig"], result)

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The Compute Engine image resource used for cluster instances. The URI can represent an image or image family. Image examples: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/global/images/[image-id]`` * ``projects/[project_id]/global/images/[image-id]`` * ``image-id`` Image family examples. Dataproc will use the most recent image from the family: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/global/images/family/[custom-image-family-name]`` * ``projects/[project_id]/global/images/family/[custom-image-family-name]`` If the URI is unspecified, it will be inferred from ``SoftwareConfig.image_version`` or the system default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#image DataprocWorkflowTemplate#image}
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The Compute Engine machine type used for cluster instances. A full URL, partial URI, or short name are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/zones/us-east1-a/machineTypes/n1-standard-2`` * ``projects/[project_id]/zones/us-east1-a/machineTypes/n1-standard-2`` * ``n1-standard-2`` **Auto Zone Exception**: If you are using the Dataproc `Auto Zone Placement <https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/auto-zone#using_auto_zone_placement>`_ feature, you must use the short name of the machine type resource, for example, ``n1-standard-2``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#machine_type DataprocWorkflowTemplate#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_cpu_platform(self) -> typing.Optional[builtins.str]:
        '''Optional. Specifies the minimum cpu platform for the Instance Group. See `Dataproc -> Minimum CPU Platform <https://cloud.google.com/dataproc/docs/concepts/compute/dataproc-min-cpu>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#min_cpu_platform DataprocWorkflowTemplate#min_cpu_platform}
        '''
        result = self._values.get("min_cpu_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_instances(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The number of VM instances in the instance group. For `HA cluster </dataproc/docs/concepts/configuring-clusters/high-availability>`_ `master_config <#FIELDS.master_config>`_ groups, **must be set to 3**. For standard cluster `master_config <#FIELDS.master_config>`_ groups, **must be set to 1**.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#num_instances DataprocWorkflowTemplate#num_instances}
        '''
        result = self._values.get("num_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preemptibility(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Specifies the preemptibility of the instance group. The default value for master and worker groups is ``NON_PREEMPTIBLE``. This default cannot be changed. The default value for secondary instances is ``PREEMPTIBLE``. Possible values: PREEMPTIBILITY_UNSPECIFIED, NON_PREEMPTIBLE, PREEMPTIBLE

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#preemptibility DataprocWorkflowTemplate#preemptibility}
        '''
        result = self._values.get("preemptibility")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAccelerators",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_count": "acceleratorCount",
        "accelerator_type": "acceleratorType",
    },
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAccelerators:
    def __init__(
        self,
        *,
        accelerator_count: typing.Optional[jsii.Number] = None,
        accelerator_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accelerator_count: The number of the accelerator cards of this type exposed to this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#accelerator_count DataprocWorkflowTemplate#accelerator_count}
        :param accelerator_type: Full URL, partial URI, or short name of the accelerator type resource to expose to this instance. See `Compute Engine AcceleratorTypes <https://cloud.google.com/compute/docs/reference/beta/acceleratorTypes>`_. Examples: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/zones/us-east1-a/acceleratorTypes/nvidia-tesla-k80`` * ``projects/[project_id]/zones/us-east1-a/acceleratorTypes/nvidia-tesla-k80`` * ``nvidia-tesla-k80`` **Auto Zone Exception**: If you are using the Dataproc `Auto Zone Placement <https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/auto-zone#using_auto_zone_placement>`_ feature, you must use the short name of the accelerator type resource, for example, ``nvidia-tesla-k80``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#accelerator_type DataprocWorkflowTemplate#accelerator_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f7b0f3ef0c859588d5ed283ad3c5ceea0df38cb92e70d20303d1dd65a365235)
            check_type(argname="argument accelerator_count", value=accelerator_count, expected_type=type_hints["accelerator_count"])
            check_type(argname="argument accelerator_type", value=accelerator_type, expected_type=type_hints["accelerator_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerator_count is not None:
            self._values["accelerator_count"] = accelerator_count
        if accelerator_type is not None:
            self._values["accelerator_type"] = accelerator_type

    @builtins.property
    def accelerator_count(self) -> typing.Optional[jsii.Number]:
        '''The number of the accelerator cards of this type exposed to this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#accelerator_count DataprocWorkflowTemplate#accelerator_count}
        '''
        result = self._values.get("accelerator_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def accelerator_type(self) -> typing.Optional[builtins.str]:
        '''Full URL, partial URI, or short name of the accelerator type resource to expose to this instance.

        See `Compute Engine AcceleratorTypes <https://cloud.google.com/compute/docs/reference/beta/acceleratorTypes>`_. Examples: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/zones/us-east1-a/acceleratorTypes/nvidia-tesla-k80`` * ``projects/[project_id]/zones/us-east1-a/acceleratorTypes/nvidia-tesla-k80`` * ``nvidia-tesla-k80`` **Auto Zone Exception**: If you are using the Dataproc `Auto Zone Placement <https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/auto-zone#using_auto_zone_placement>`_ feature, you must use the short name of the accelerator type resource, for example, ``nvidia-tesla-k80``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#accelerator_type DataprocWorkflowTemplate#accelerator_type}
        '''
        result = self._values.get("accelerator_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAccelerators(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAcceleratorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAcceleratorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a57cacf23e54dc8558d8d585b9839e61666cb6a81cdc149fe47fc5a0d0819490)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAcceleratorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__709964bb29a3826700fd4088f2ddbab785a3bc50412b3d697e387706d4eab744)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAcceleratorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb0ce27ce23b142bb835f5adb754babdf938e2b3bf50f39d59421f9b2927b0a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c2b7a71bd531a2022b5212b6aee5d9968836c8eca345fc5b0c0e846f59ed44b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b162d1c26aed25ed3cbcce019e815a0f8d5a1a94168149fcd273b550189cd7e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAccelerators]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAccelerators]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37117b3a769e5622c6a71efaf65bd87d199e3ca1136690610368ca48b17749b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAcceleratorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAcceleratorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3d476e390595ef4ddb953fd03c8f35f40560655539edcad9e5b8030604d827e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAcceleratorCount")
    def reset_accelerator_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorCount", []))

    @jsii.member(jsii_name="resetAcceleratorType")
    def reset_accelerator_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorType", []))

    @builtins.property
    @jsii.member(jsii_name="acceleratorCountInput")
    def accelerator_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "acceleratorCountInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTypeInput")
    def accelerator_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceleratorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorCount")
    def accelerator_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "acceleratorCount"))

    @accelerator_count.setter
    def accelerator_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ee736e169ff10aba57fb9840afcf8da96714fd8c1e349972445abb514f25a9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1146d6939c1573dec88ec780a67077d840283d28a2cc2b659093c02f93e681f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAccelerators]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAccelerators]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAccelerators]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0e29f2f35859a40b29d3c6fea5684a491f913944a1a601ceb5e3a28278c7353)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigDiskConfig",
    jsii_struct_bases=[],
    name_mapping={
        "boot_disk_size_gb": "bootDiskSizeGb",
        "boot_disk_type": "bootDiskType",
        "num_local_ssds": "numLocalSsds",
    },
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigDiskConfig:
    def __init__(
        self,
        *,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        boot_disk_type: typing.Optional[builtins.str] = None,
        num_local_ssds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param boot_disk_size_gb: Optional. Size in GB of the boot disk (default is 500GB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#boot_disk_size_gb DataprocWorkflowTemplate#boot_disk_size_gb}
        :param boot_disk_type: Optional. Type of the boot disk (default is "pd-standard"). Valid values: "pd-balanced" (Persistent Disk Balanced Solid State Drive), "pd-ssd" (Persistent Disk Solid State Drive), or "pd-standard" (Persistent Disk Hard Disk Drive). See `Disk types <https://cloud.google.com/compute/docs/disks#disk-types>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#boot_disk_type DataprocWorkflowTemplate#boot_disk_type}
        :param num_local_ssds: Optional. Number of attached SSDs, from 0 to 4 (default is 0). If SSDs are not attached, the boot disk is used to store runtime logs and `HDFS <https://hadoop.apache.org/docs/r1.2.1/hdfs_user_guide.html>`_ data. If one or more SSDs are attached, this runtime bulk data is spread across them, and the boot disk contains only basic config and installed binaries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#num_local_ssds DataprocWorkflowTemplate#num_local_ssds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__703bf1fcef40f226c50fd9373c337c3d3c5f38ad0e3f23de69c73ba3ffd881ef)
            check_type(argname="argument boot_disk_size_gb", value=boot_disk_size_gb, expected_type=type_hints["boot_disk_size_gb"])
            check_type(argname="argument boot_disk_type", value=boot_disk_type, expected_type=type_hints["boot_disk_type"])
            check_type(argname="argument num_local_ssds", value=num_local_ssds, expected_type=type_hints["num_local_ssds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if boot_disk_size_gb is not None:
            self._values["boot_disk_size_gb"] = boot_disk_size_gb
        if boot_disk_type is not None:
            self._values["boot_disk_type"] = boot_disk_type
        if num_local_ssds is not None:
            self._values["num_local_ssds"] = num_local_ssds

    @builtins.property
    def boot_disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Optional. Size in GB of the boot disk (default is 500GB).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#boot_disk_size_gb DataprocWorkflowTemplate#boot_disk_size_gb}
        '''
        result = self._values.get("boot_disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def boot_disk_type(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Type of the boot disk (default is "pd-standard"). Valid values: "pd-balanced" (Persistent Disk Balanced Solid State Drive), "pd-ssd" (Persistent Disk Solid State Drive), or "pd-standard" (Persistent Disk Hard Disk Drive). See `Disk types <https://cloud.google.com/compute/docs/disks#disk-types>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#boot_disk_type DataprocWorkflowTemplate#boot_disk_type}
        '''
        result = self._values.get("boot_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_local_ssds(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        Number of attached SSDs, from 0 to 4 (default is 0). If SSDs are not attached, the boot disk is used to store runtime logs and `HDFS <https://hadoop.apache.org/docs/r1.2.1/hdfs_user_guide.html>`_ data. If one or more SSDs are attached, this runtime bulk data is spread across them, and the boot disk contains only basic config and installed binaries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#num_local_ssds DataprocWorkflowTemplate#num_local_ssds}
        '''
        result = self._values.get("num_local_ssds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigDiskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigDiskConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigDiskConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__674b376b2917c9e7f47c3a3d732481310ee53de713f2dcf31b0a1f71a0df023e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBootDiskSizeGb")
    def reset_boot_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskSizeGb", []))

    @jsii.member(jsii_name="resetBootDiskType")
    def reset_boot_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskType", []))

    @jsii.member(jsii_name="resetNumLocalSsds")
    def reset_num_local_ssds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumLocalSsds", []))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGbInput")
    def boot_disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootDiskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskTypeInput")
    def boot_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="numLocalSsdsInput")
    def num_local_ssds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numLocalSsdsInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGb")
    def boot_disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bootDiskSizeGb"))

    @boot_disk_size_gb.setter
    def boot_disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b98519b03ec66f7268a585a22a5c550ae0366ad3463078a79906b22e4ec75a7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bootDiskType")
    def boot_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootDiskType"))

    @boot_disk_type.setter
    def boot_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa37fbee758c3a8e9fb969659bbf9aed01dd9c7bd784ff61e951265988fba6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numLocalSsds")
    def num_local_ssds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numLocalSsds"))

    @num_local_ssds.setter
    def num_local_ssds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f671df4286aeca45f4ffffcf5e8d9d0fe9582a708289dd00996b97de439a089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numLocalSsds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigDiskConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigDiskConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigDiskConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d3b4154662e6af3b0c643d124b258603e48b4ec77c4b79ffcc4530f20171713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigManagedGroupConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigManagedGroupConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigManagedGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigManagedGroupConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigManagedGroupConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e30732efa713c08fd632b6557e91f1290bb2a096e70e323b8ec793014912875)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigManagedGroupConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74d9b8882c730508214c639f6f768f0e85c657c9b7ef7be5c10abd49b2016a15)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigManagedGroupConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecfcdf11d868252417a6070468df5bdb8bf100e1b4ceaa41a1c8568ae8a3eda8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__edca7978175a67c3aa87bc8d138f82f90dd0b5013b184e63f201f147ba58bdb7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8a2705880be7bcc3b8f3e5f4e359dd6b0727dbd53c18a6c43d70a22b83252dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigManagedGroupConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigManagedGroupConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__269fa1ea01d192f8d617d6c342af2b1a6fb26d9c0f5450ae207856cc0dca8dfd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="instanceGroupManagerName")
    def instance_group_manager_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceGroupManagerName"))

    @builtins.property
    @jsii.member(jsii_name="instanceTemplateName")
    def instance_template_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceTemplateName"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigManagedGroupConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigManagedGroupConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigManagedGroupConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beb2426e08ee339e7a0b8a1896b04998f3c842e896412bc9edce180e11162b6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cc03c135191b3627280d737990d59a9cda1210a2fd63f18b3af82dca01edbd2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccelerators")
    def put_accelerators(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb755b3436efa91b836616821b16c0bbe3cf68ac2ad47d017d0cde291db366e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccelerators", [value]))

    @jsii.member(jsii_name="putDiskConfig")
    def put_disk_config(
        self,
        *,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        boot_disk_type: typing.Optional[builtins.str] = None,
        num_local_ssds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param boot_disk_size_gb: Optional. Size in GB of the boot disk (default is 500GB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#boot_disk_size_gb DataprocWorkflowTemplate#boot_disk_size_gb}
        :param boot_disk_type: Optional. Type of the boot disk (default is "pd-standard"). Valid values: "pd-balanced" (Persistent Disk Balanced Solid State Drive), "pd-ssd" (Persistent Disk Solid State Drive), or "pd-standard" (Persistent Disk Hard Disk Drive). See `Disk types <https://cloud.google.com/compute/docs/disks#disk-types>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#boot_disk_type DataprocWorkflowTemplate#boot_disk_type}
        :param num_local_ssds: Optional. Number of attached SSDs, from 0 to 4 (default is 0). If SSDs are not attached, the boot disk is used to store runtime logs and `HDFS <https://hadoop.apache.org/docs/r1.2.1/hdfs_user_guide.html>`_ data. If one or more SSDs are attached, this runtime bulk data is spread across them, and the boot disk contains only basic config and installed binaries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#num_local_ssds DataprocWorkflowTemplate#num_local_ssds}
        '''
        value = DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigDiskConfig(
            boot_disk_size_gb=boot_disk_size_gb,
            boot_disk_type=boot_disk_type,
            num_local_ssds=num_local_ssds,
        )

        return typing.cast(None, jsii.invoke(self, "putDiskConfig", [value]))

    @jsii.member(jsii_name="resetAccelerators")
    def reset_accelerators(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccelerators", []))

    @jsii.member(jsii_name="resetDiskConfig")
    def reset_disk_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskConfig", []))

    @jsii.member(jsii_name="resetImage")
    def reset_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImage", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @jsii.member(jsii_name="resetMinCpuPlatform")
    def reset_min_cpu_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinCpuPlatform", []))

    @jsii.member(jsii_name="resetNumInstances")
    def reset_num_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumInstances", []))

    @jsii.member(jsii_name="resetPreemptibility")
    def reset_preemptibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreemptibility", []))

    @builtins.property
    @jsii.member(jsii_name="accelerators")
    def accelerators(
        self,
    ) -> DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAcceleratorsList:
        return typing.cast(DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAcceleratorsList, jsii.get(self, "accelerators"))

    @builtins.property
    @jsii.member(jsii_name="diskConfig")
    def disk_config(
        self,
    ) -> DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigDiskConfigOutputReference:
        return typing.cast(DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigDiskConfigOutputReference, jsii.get(self, "diskConfig"))

    @builtins.property
    @jsii.member(jsii_name="instanceNames")
    def instance_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceNames"))

    @builtins.property
    @jsii.member(jsii_name="isPreemptible")
    def is_preemptible(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isPreemptible"))

    @builtins.property
    @jsii.member(jsii_name="managedGroupConfig")
    def managed_group_config(
        self,
    ) -> DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigManagedGroupConfigList:
        return typing.cast(DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigManagedGroupConfigList, jsii.get(self, "managedGroupConfig"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorsInput")
    def accelerators_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAccelerators]]], jsii.get(self, "acceleratorsInput"))

    @builtins.property
    @jsii.member(jsii_name="diskConfigInput")
    def disk_config_input(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigDiskConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigDiskConfig], jsii.get(self, "diskConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatformInput")
    def min_cpu_platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minCpuPlatformInput"))

    @builtins.property
    @jsii.member(jsii_name="numInstancesInput")
    def num_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="preemptibilityInput")
    def preemptibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preemptibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__388b191e3c7a415f9cf3596faebef7b5d9a0f099cb8049becf421d7ca23b9cc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86c007d0fe996e9fc639b76a3818ab594c876dc5c27b5c9f29027a59520553d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatform")
    def min_cpu_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minCpuPlatform"))

    @min_cpu_platform.setter
    def min_cpu_platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__741e0aa3b8e1a99c96c1507a6efc306e85366320fd5db11c9c162555da1cd996)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCpuPlatform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numInstances")
    def num_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numInstances"))

    @num_instances.setter
    def num_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f6a6edc7ef769eee0d7114ae5f16be0ac5fd5de3ca0f441bd27d7423a06d481)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preemptibility")
    def preemptibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preemptibility"))

    @preemptibility.setter
    def preemptibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bffa271b3af2dc0406326aba9321cee351285c4791e18d68ddb7f40e7c1d01ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preemptibility", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9edd934f6b1b24e6827a41c5be06ba4fce413697a6865b5f8e84f29cd1ef3249)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfig",
    jsii_struct_bases=[],
    name_mapping={"kerberos_config": "kerberosConfig"},
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfig:
    def __init__(
        self,
        *,
        kerberos_config: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigKerberosConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param kerberos_config: kerberos_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#kerberos_config DataprocWorkflowTemplate#kerberos_config}
        '''
        if isinstance(kerberos_config, dict):
            kerberos_config = DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigKerberosConfig(**kerberos_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__628f6e5e1b8af39595c48cd835f47fc136a34258b8a05ce26b1f24a565ea9f21)
            check_type(argname="argument kerberos_config", value=kerberos_config, expected_type=type_hints["kerberos_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kerberos_config is not None:
            self._values["kerberos_config"] = kerberos_config

    @builtins.property
    def kerberos_config(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigKerberosConfig"]:
        '''kerberos_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#kerberos_config DataprocWorkflowTemplate#kerberos_config}
        '''
        result = self._values.get("kerberos_config")
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigKerberosConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigKerberosConfig",
    jsii_struct_bases=[],
    name_mapping={
        "cross_realm_trust_admin_server": "crossRealmTrustAdminServer",
        "cross_realm_trust_kdc": "crossRealmTrustKdc",
        "cross_realm_trust_realm": "crossRealmTrustRealm",
        "cross_realm_trust_shared_password": "crossRealmTrustSharedPassword",
        "enable_kerberos": "enableKerberos",
        "kdc_db_key": "kdcDbKey",
        "key_password": "keyPassword",
        "keystore": "keystore",
        "keystore_password": "keystorePassword",
        "kms_key": "kmsKey",
        "realm": "realm",
        "root_principal_password": "rootPrincipalPassword",
        "tgt_lifetime_hours": "tgtLifetimeHours",
        "truststore": "truststore",
        "truststore_password": "truststorePassword",
    },
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigKerberosConfig:
    def __init__(
        self,
        *,
        cross_realm_trust_admin_server: typing.Optional[builtins.str] = None,
        cross_realm_trust_kdc: typing.Optional[builtins.str] = None,
        cross_realm_trust_realm: typing.Optional[builtins.str] = None,
        cross_realm_trust_shared_password: typing.Optional[builtins.str] = None,
        enable_kerberos: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kdc_db_key: typing.Optional[builtins.str] = None,
        key_password: typing.Optional[builtins.str] = None,
        keystore: typing.Optional[builtins.str] = None,
        keystore_password: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        realm: typing.Optional[builtins.str] = None,
        root_principal_password: typing.Optional[builtins.str] = None,
        tgt_lifetime_hours: typing.Optional[jsii.Number] = None,
        truststore: typing.Optional[builtins.str] = None,
        truststore_password: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cross_realm_trust_admin_server: Optional. The admin server (IP or hostname) for the remote trusted realm in a cross realm trust relationship. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#cross_realm_trust_admin_server DataprocWorkflowTemplate#cross_realm_trust_admin_server}
        :param cross_realm_trust_kdc: Optional. The KDC (IP or hostname) for the remote trusted realm in a cross realm trust relationship. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#cross_realm_trust_kdc DataprocWorkflowTemplate#cross_realm_trust_kdc}
        :param cross_realm_trust_realm: Optional. The remote realm the Dataproc on-cluster KDC will trust, should the user enable cross realm trust. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#cross_realm_trust_realm DataprocWorkflowTemplate#cross_realm_trust_realm}
        :param cross_realm_trust_shared_password: Optional. The Cloud Storage URI of a KMS encrypted file containing the shared password between the on-cluster Kerberos realm and the remote trusted realm, in a cross realm trust relationship. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#cross_realm_trust_shared_password DataprocWorkflowTemplate#cross_realm_trust_shared_password}
        :param enable_kerberos: Optional. Flag to indicate whether to Kerberize the cluster (default: false). Set this field to true to enable Kerberos on a cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#enable_kerberos DataprocWorkflowTemplate#enable_kerberos}
        :param kdc_db_key: Optional. The Cloud Storage URI of a KMS encrypted file containing the master key of the KDC database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#kdc_db_key DataprocWorkflowTemplate#kdc_db_key}
        :param key_password: Optional. The Cloud Storage URI of a KMS encrypted file containing the password to the user provided key. For the self-signed certificate, this password is generated by Dataproc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#key_password DataprocWorkflowTemplate#key_password}
        :param keystore: Optional. The Cloud Storage URI of the keystore file used for SSL encryption. If not provided, Dataproc will provide a self-signed certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#keystore DataprocWorkflowTemplate#keystore}
        :param keystore_password: Optional. The Cloud Storage URI of a KMS encrypted file containing the password to the user provided keystore. For the self-signed certificate, this password is generated by Dataproc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#keystore_password DataprocWorkflowTemplate#keystore_password}
        :param kms_key: Optional. The uri of the KMS key used to encrypt various sensitive files. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#kms_key DataprocWorkflowTemplate#kms_key}
        :param realm: Optional. The name of the on-cluster Kerberos realm. If not specified, the uppercased domain of hostnames will be the realm. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#realm DataprocWorkflowTemplate#realm}
        :param root_principal_password: Optional. The Cloud Storage URI of a KMS encrypted file containing the root principal password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#root_principal_password DataprocWorkflowTemplate#root_principal_password}
        :param tgt_lifetime_hours: Optional. The lifetime of the ticket granting ticket, in hours. If not specified, or user specifies 0, then default value 10 will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#tgt_lifetime_hours DataprocWorkflowTemplate#tgt_lifetime_hours}
        :param truststore: Optional. The Cloud Storage URI of the truststore file used for SSL encryption. If not provided, Dataproc will provide a self-signed certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#truststore DataprocWorkflowTemplate#truststore}
        :param truststore_password: Optional. The Cloud Storage URI of a KMS encrypted file containing the password to the user provided truststore. For the self-signed certificate, this password is generated by Dataproc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#truststore_password DataprocWorkflowTemplate#truststore_password}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__457e5bf7fe1dc1b5182e1a1e81b66bfde13540329d3b59bc336cd8021354608e)
            check_type(argname="argument cross_realm_trust_admin_server", value=cross_realm_trust_admin_server, expected_type=type_hints["cross_realm_trust_admin_server"])
            check_type(argname="argument cross_realm_trust_kdc", value=cross_realm_trust_kdc, expected_type=type_hints["cross_realm_trust_kdc"])
            check_type(argname="argument cross_realm_trust_realm", value=cross_realm_trust_realm, expected_type=type_hints["cross_realm_trust_realm"])
            check_type(argname="argument cross_realm_trust_shared_password", value=cross_realm_trust_shared_password, expected_type=type_hints["cross_realm_trust_shared_password"])
            check_type(argname="argument enable_kerberos", value=enable_kerberos, expected_type=type_hints["enable_kerberos"])
            check_type(argname="argument kdc_db_key", value=kdc_db_key, expected_type=type_hints["kdc_db_key"])
            check_type(argname="argument key_password", value=key_password, expected_type=type_hints["key_password"])
            check_type(argname="argument keystore", value=keystore, expected_type=type_hints["keystore"])
            check_type(argname="argument keystore_password", value=keystore_password, expected_type=type_hints["keystore_password"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument realm", value=realm, expected_type=type_hints["realm"])
            check_type(argname="argument root_principal_password", value=root_principal_password, expected_type=type_hints["root_principal_password"])
            check_type(argname="argument tgt_lifetime_hours", value=tgt_lifetime_hours, expected_type=type_hints["tgt_lifetime_hours"])
            check_type(argname="argument truststore", value=truststore, expected_type=type_hints["truststore"])
            check_type(argname="argument truststore_password", value=truststore_password, expected_type=type_hints["truststore_password"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cross_realm_trust_admin_server is not None:
            self._values["cross_realm_trust_admin_server"] = cross_realm_trust_admin_server
        if cross_realm_trust_kdc is not None:
            self._values["cross_realm_trust_kdc"] = cross_realm_trust_kdc
        if cross_realm_trust_realm is not None:
            self._values["cross_realm_trust_realm"] = cross_realm_trust_realm
        if cross_realm_trust_shared_password is not None:
            self._values["cross_realm_trust_shared_password"] = cross_realm_trust_shared_password
        if enable_kerberos is not None:
            self._values["enable_kerberos"] = enable_kerberos
        if kdc_db_key is not None:
            self._values["kdc_db_key"] = kdc_db_key
        if key_password is not None:
            self._values["key_password"] = key_password
        if keystore is not None:
            self._values["keystore"] = keystore
        if keystore_password is not None:
            self._values["keystore_password"] = keystore_password
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if realm is not None:
            self._values["realm"] = realm
        if root_principal_password is not None:
            self._values["root_principal_password"] = root_principal_password
        if tgt_lifetime_hours is not None:
            self._values["tgt_lifetime_hours"] = tgt_lifetime_hours
        if truststore is not None:
            self._values["truststore"] = truststore
        if truststore_password is not None:
            self._values["truststore_password"] = truststore_password

    @builtins.property
    def cross_realm_trust_admin_server(self) -> typing.Optional[builtins.str]:
        '''Optional. The admin server (IP or hostname) for the remote trusted realm in a cross realm trust relationship.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#cross_realm_trust_admin_server DataprocWorkflowTemplate#cross_realm_trust_admin_server}
        '''
        result = self._values.get("cross_realm_trust_admin_server")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cross_realm_trust_kdc(self) -> typing.Optional[builtins.str]:
        '''Optional. The KDC (IP or hostname) for the remote trusted realm in a cross realm trust relationship.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#cross_realm_trust_kdc DataprocWorkflowTemplate#cross_realm_trust_kdc}
        '''
        result = self._values.get("cross_realm_trust_kdc")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cross_realm_trust_realm(self) -> typing.Optional[builtins.str]:
        '''Optional. The remote realm the Dataproc on-cluster KDC will trust, should the user enable cross realm trust.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#cross_realm_trust_realm DataprocWorkflowTemplate#cross_realm_trust_realm}
        '''
        result = self._values.get("cross_realm_trust_realm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cross_realm_trust_shared_password(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The Cloud Storage URI of a KMS encrypted file containing the shared password between the on-cluster Kerberos realm and the remote trusted realm, in a cross realm trust relationship.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#cross_realm_trust_shared_password DataprocWorkflowTemplate#cross_realm_trust_shared_password}
        '''
        result = self._values.get("cross_realm_trust_shared_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_kerberos(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Flag to indicate whether to Kerberize the cluster (default: false). Set this field to true to enable Kerberos on a cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#enable_kerberos DataprocWorkflowTemplate#enable_kerberos}
        '''
        result = self._values.get("enable_kerberos")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def kdc_db_key(self) -> typing.Optional[builtins.str]:
        '''Optional. The Cloud Storage URI of a KMS encrypted file containing the master key of the KDC database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#kdc_db_key DataprocWorkflowTemplate#kdc_db_key}
        '''
        result = self._values.get("kdc_db_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_password(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The Cloud Storage URI of a KMS encrypted file containing the password to the user provided key. For the self-signed certificate, this password is generated by Dataproc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#key_password DataprocWorkflowTemplate#key_password}
        '''
        result = self._values.get("key_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keystore(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The Cloud Storage URI of the keystore file used for SSL encryption. If not provided, Dataproc will provide a self-signed certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#keystore DataprocWorkflowTemplate#keystore}
        '''
        result = self._values.get("keystore")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keystore_password(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The Cloud Storage URI of a KMS encrypted file containing the password to the user provided keystore. For the self-signed certificate, this password is generated by Dataproc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#keystore_password DataprocWorkflowTemplate#keystore_password}
        '''
        result = self._values.get("keystore_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''Optional. The uri of the KMS key used to encrypt various sensitive files.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#kms_key DataprocWorkflowTemplate#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def realm(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The name of the on-cluster Kerberos realm. If not specified, the uppercased domain of hostnames will be the realm.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#realm DataprocWorkflowTemplate#realm}
        '''
        result = self._values.get("realm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_principal_password(self) -> typing.Optional[builtins.str]:
        '''Optional. The Cloud Storage URI of a KMS encrypted file containing the root principal password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#root_principal_password DataprocWorkflowTemplate#root_principal_password}
        '''
        result = self._values.get("root_principal_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tgt_lifetime_hours(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The lifetime of the ticket granting ticket, in hours. If not specified, or user specifies 0, then default value 10 will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#tgt_lifetime_hours DataprocWorkflowTemplate#tgt_lifetime_hours}
        '''
        result = self._values.get("tgt_lifetime_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def truststore(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The Cloud Storage URI of the truststore file used for SSL encryption. If not provided, Dataproc will provide a self-signed certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#truststore DataprocWorkflowTemplate#truststore}
        '''
        result = self._values.get("truststore")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def truststore_password(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The Cloud Storage URI of a KMS encrypted file containing the password to the user provided truststore. For the self-signed certificate, this password is generated by Dataproc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#truststore_password DataprocWorkflowTemplate#truststore_password}
        '''
        result = self._values.get("truststore_password")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigKerberosConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigKerberosConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigKerberosConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88835a49b3e95ce7c3fd1084fa3f97ac30c20ed6e941d13df29b7a92505517b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCrossRealmTrustAdminServer")
    def reset_cross_realm_trust_admin_server(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossRealmTrustAdminServer", []))

    @jsii.member(jsii_name="resetCrossRealmTrustKdc")
    def reset_cross_realm_trust_kdc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossRealmTrustKdc", []))

    @jsii.member(jsii_name="resetCrossRealmTrustRealm")
    def reset_cross_realm_trust_realm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossRealmTrustRealm", []))

    @jsii.member(jsii_name="resetCrossRealmTrustSharedPassword")
    def reset_cross_realm_trust_shared_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossRealmTrustSharedPassword", []))

    @jsii.member(jsii_name="resetEnableKerberos")
    def reset_enable_kerberos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableKerberos", []))

    @jsii.member(jsii_name="resetKdcDbKey")
    def reset_kdc_db_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKdcDbKey", []))

    @jsii.member(jsii_name="resetKeyPassword")
    def reset_key_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyPassword", []))

    @jsii.member(jsii_name="resetKeystore")
    def reset_keystore(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeystore", []))

    @jsii.member(jsii_name="resetKeystorePassword")
    def reset_keystore_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeystorePassword", []))

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

    @jsii.member(jsii_name="resetRealm")
    def reset_realm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRealm", []))

    @jsii.member(jsii_name="resetRootPrincipalPassword")
    def reset_root_principal_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootPrincipalPassword", []))

    @jsii.member(jsii_name="resetTgtLifetimeHours")
    def reset_tgt_lifetime_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTgtLifetimeHours", []))

    @jsii.member(jsii_name="resetTruststore")
    def reset_truststore(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTruststore", []))

    @jsii.member(jsii_name="resetTruststorePassword")
    def reset_truststore_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTruststorePassword", []))

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustAdminServerInput")
    def cross_realm_trust_admin_server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crossRealmTrustAdminServerInput"))

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustKdcInput")
    def cross_realm_trust_kdc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crossRealmTrustKdcInput"))

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustRealmInput")
    def cross_realm_trust_realm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crossRealmTrustRealmInput"))

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustSharedPasswordInput")
    def cross_realm_trust_shared_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crossRealmTrustSharedPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="enableKerberosInput")
    def enable_kerberos_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableKerberosInput"))

    @builtins.property
    @jsii.member(jsii_name="kdcDbKeyInput")
    def kdc_db_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kdcDbKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="keyPasswordInput")
    def key_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="keystoreInput")
    def keystore_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keystoreInput"))

    @builtins.property
    @jsii.member(jsii_name="keystorePasswordInput")
    def keystore_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keystorePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="realmInput")
    def realm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "realmInput"))

    @builtins.property
    @jsii.member(jsii_name="rootPrincipalPasswordInput")
    def root_principal_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rootPrincipalPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="tgtLifetimeHoursInput")
    def tgt_lifetime_hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tgtLifetimeHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="truststoreInput")
    def truststore_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "truststoreInput"))

    @builtins.property
    @jsii.member(jsii_name="truststorePasswordInput")
    def truststore_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "truststorePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustAdminServer")
    def cross_realm_trust_admin_server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crossRealmTrustAdminServer"))

    @cross_realm_trust_admin_server.setter
    def cross_realm_trust_admin_server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51bb8ce3c9d104daa70839df5fe37fa20e0aea79788c62068fc09b66439d7bb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crossRealmTrustAdminServer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustKdc")
    def cross_realm_trust_kdc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crossRealmTrustKdc"))

    @cross_realm_trust_kdc.setter
    def cross_realm_trust_kdc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__040fd558d346a4ecf841b2be5f4a94b9223f45a03625a74ddbf62a85dec96dad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crossRealmTrustKdc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustRealm")
    def cross_realm_trust_realm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crossRealmTrustRealm"))

    @cross_realm_trust_realm.setter
    def cross_realm_trust_realm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20ebe66891ddecb2377b8d20fbf6c041844b43c695c38224b8779816a4a12cb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crossRealmTrustRealm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustSharedPassword")
    def cross_realm_trust_shared_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crossRealmTrustSharedPassword"))

    @cross_realm_trust_shared_password.setter
    def cross_realm_trust_shared_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__723e9bd8a32ecee7c24d02ed4a64a56ad4f4c50de955542f08d7dc427829d465)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crossRealmTrustSharedPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableKerberos")
    def enable_kerberos(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableKerberos"))

    @enable_kerberos.setter
    def enable_kerberos(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20413b95c322fcfd3a175df6b2f34893b80b259bc646f208360ae048c5a88ae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableKerberos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kdcDbKey")
    def kdc_db_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kdcDbKey"))

    @kdc_db_key.setter
    def kdc_db_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afb8cd340abbe1162e2ec3a1722cb5bc90b9185ad4a082718af83e477aa5c41b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kdcDbKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyPassword")
    def key_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyPassword"))

    @key_password.setter
    def key_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4523e6b409f55db6146bc14ef6280eaa6f8fa71f9467cdcb999f3b7adaca314)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keystore")
    def keystore(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keystore"))

    @keystore.setter
    def keystore(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a9f0f37c59df5aa3859f60b94c7b46b966b2dc21389fd66ad938817229ee24e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keystore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keystorePassword")
    def keystore_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keystorePassword"))

    @keystore_password.setter
    def keystore_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e872486fbba83cdf8f6cc815e2474002498b44ce578947f645d28847ef65771e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keystorePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0643f76e1fde4d301b03d27b57cc1aa1e2c1f42ab5f92f757ad513afc6451231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="realm")
    def realm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "realm"))

    @realm.setter
    def realm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81507bec2ca02f660aa44bff4e7fec729327565624a366cd36825e4afbf42c3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "realm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rootPrincipalPassword")
    def root_principal_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootPrincipalPassword"))

    @root_principal_password.setter
    def root_principal_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e42b0c5996646a1731053b4ad6e2b711ff1779143ba5f0122b4464519495f20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootPrincipalPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tgtLifetimeHours")
    def tgt_lifetime_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tgtLifetimeHours"))

    @tgt_lifetime_hours.setter
    def tgt_lifetime_hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__820334721ec724d9abbfa1c04ed9b1e608b0a263147f4591e8ddd7c248c82d6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tgtLifetimeHours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="truststore")
    def truststore(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "truststore"))

    @truststore.setter
    def truststore(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fbce1375227aaed11ce4f79ad91ec9dd45eb2dfd08c6de11a5c8eb52bd4edc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "truststore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="truststorePassword")
    def truststore_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "truststorePassword"))

    @truststore_password.setter
    def truststore_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31338cb5a501ef6e4e6ca604e3e1b2526fc01e3804d115f68fd20160934d2648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "truststorePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigKerberosConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigKerberosConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigKerberosConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c79afd5e2bd0d6b67fb86872779ec10291ff680a9223fa760906e64ef475a735)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2097e6f9f646278af06a9267172fc17e5ab2770bfdaf04630e80d4e21d7584f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putKerberosConfig")
    def put_kerberos_config(
        self,
        *,
        cross_realm_trust_admin_server: typing.Optional[builtins.str] = None,
        cross_realm_trust_kdc: typing.Optional[builtins.str] = None,
        cross_realm_trust_realm: typing.Optional[builtins.str] = None,
        cross_realm_trust_shared_password: typing.Optional[builtins.str] = None,
        enable_kerberos: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kdc_db_key: typing.Optional[builtins.str] = None,
        key_password: typing.Optional[builtins.str] = None,
        keystore: typing.Optional[builtins.str] = None,
        keystore_password: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        realm: typing.Optional[builtins.str] = None,
        root_principal_password: typing.Optional[builtins.str] = None,
        tgt_lifetime_hours: typing.Optional[jsii.Number] = None,
        truststore: typing.Optional[builtins.str] = None,
        truststore_password: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cross_realm_trust_admin_server: Optional. The admin server (IP or hostname) for the remote trusted realm in a cross realm trust relationship. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#cross_realm_trust_admin_server DataprocWorkflowTemplate#cross_realm_trust_admin_server}
        :param cross_realm_trust_kdc: Optional. The KDC (IP or hostname) for the remote trusted realm in a cross realm trust relationship. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#cross_realm_trust_kdc DataprocWorkflowTemplate#cross_realm_trust_kdc}
        :param cross_realm_trust_realm: Optional. The remote realm the Dataproc on-cluster KDC will trust, should the user enable cross realm trust. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#cross_realm_trust_realm DataprocWorkflowTemplate#cross_realm_trust_realm}
        :param cross_realm_trust_shared_password: Optional. The Cloud Storage URI of a KMS encrypted file containing the shared password between the on-cluster Kerberos realm and the remote trusted realm, in a cross realm trust relationship. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#cross_realm_trust_shared_password DataprocWorkflowTemplate#cross_realm_trust_shared_password}
        :param enable_kerberos: Optional. Flag to indicate whether to Kerberize the cluster (default: false). Set this field to true to enable Kerberos on a cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#enable_kerberos DataprocWorkflowTemplate#enable_kerberos}
        :param kdc_db_key: Optional. The Cloud Storage URI of a KMS encrypted file containing the master key of the KDC database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#kdc_db_key DataprocWorkflowTemplate#kdc_db_key}
        :param key_password: Optional. The Cloud Storage URI of a KMS encrypted file containing the password to the user provided key. For the self-signed certificate, this password is generated by Dataproc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#key_password DataprocWorkflowTemplate#key_password}
        :param keystore: Optional. The Cloud Storage URI of the keystore file used for SSL encryption. If not provided, Dataproc will provide a self-signed certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#keystore DataprocWorkflowTemplate#keystore}
        :param keystore_password: Optional. The Cloud Storage URI of a KMS encrypted file containing the password to the user provided keystore. For the self-signed certificate, this password is generated by Dataproc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#keystore_password DataprocWorkflowTemplate#keystore_password}
        :param kms_key: Optional. The uri of the KMS key used to encrypt various sensitive files. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#kms_key DataprocWorkflowTemplate#kms_key}
        :param realm: Optional. The name of the on-cluster Kerberos realm. If not specified, the uppercased domain of hostnames will be the realm. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#realm DataprocWorkflowTemplate#realm}
        :param root_principal_password: Optional. The Cloud Storage URI of a KMS encrypted file containing the root principal password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#root_principal_password DataprocWorkflowTemplate#root_principal_password}
        :param tgt_lifetime_hours: Optional. The lifetime of the ticket granting ticket, in hours. If not specified, or user specifies 0, then default value 10 will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#tgt_lifetime_hours DataprocWorkflowTemplate#tgt_lifetime_hours}
        :param truststore: Optional. The Cloud Storage URI of the truststore file used for SSL encryption. If not provided, Dataproc will provide a self-signed certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#truststore DataprocWorkflowTemplate#truststore}
        :param truststore_password: Optional. The Cloud Storage URI of a KMS encrypted file containing the password to the user provided truststore. For the self-signed certificate, this password is generated by Dataproc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#truststore_password DataprocWorkflowTemplate#truststore_password}
        '''
        value = DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigKerberosConfig(
            cross_realm_trust_admin_server=cross_realm_trust_admin_server,
            cross_realm_trust_kdc=cross_realm_trust_kdc,
            cross_realm_trust_realm=cross_realm_trust_realm,
            cross_realm_trust_shared_password=cross_realm_trust_shared_password,
            enable_kerberos=enable_kerberos,
            kdc_db_key=kdc_db_key,
            key_password=key_password,
            keystore=keystore,
            keystore_password=keystore_password,
            kms_key=kms_key,
            realm=realm,
            root_principal_password=root_principal_password,
            tgt_lifetime_hours=tgt_lifetime_hours,
            truststore=truststore,
            truststore_password=truststore_password,
        )

        return typing.cast(None, jsii.invoke(self, "putKerberosConfig", [value]))

    @jsii.member(jsii_name="resetKerberosConfig")
    def reset_kerberos_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKerberosConfig", []))

    @builtins.property
    @jsii.member(jsii_name="kerberosConfig")
    def kerberos_config(
        self,
    ) -> DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigKerberosConfigOutputReference:
        return typing.cast(DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigKerberosConfigOutputReference, jsii.get(self, "kerberosConfig"))

    @builtins.property
    @jsii.member(jsii_name="kerberosConfigInput")
    def kerberos_config_input(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigKerberosConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigKerberosConfig], jsii.get(self, "kerberosConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fa14dbfac4be4e48a63a4eeb9d5f15bab0111c9f991c714e19b2dbdbaca5b8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigSoftwareConfig",
    jsii_struct_bases=[],
    name_mapping={
        "image_version": "imageVersion",
        "optional_components": "optionalComponents",
        "properties": "properties",
    },
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigSoftwareConfig:
    def __init__(
        self,
        *,
        image_version: typing.Optional[builtins.str] = None,
        optional_components: typing.Optional[typing.Sequence[builtins.str]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param image_version: Optional. The version of software inside the cluster. It must be one of the supported `Dataproc Versions <https://cloud.google.com/dataproc/docs/concepts/versioning/dataproc-versions#supported_dataproc_versions>`_, such as "1.2" (including a subminor version, such as "1.2.29"), or the `"preview" version <https://cloud.google.com/dataproc/docs/concepts/versioning/dataproc-versions#other_versions>`_. If unspecified, it defaults to the latest Debian version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#image_version DataprocWorkflowTemplate#image_version}
        :param optional_components: Optional. The set of components to activate on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#optional_components DataprocWorkflowTemplate#optional_components}
        :param properties: Optional. The properties to set on daemon config files. Property keys are specified in ``prefix:property`` format, for example ``core:hadoop.tmp.dir``. The following are supported prefixes and their mappings: * capacity-scheduler: ``capacity-scheduler.xml`` * core: ``core-site.xml`` * distcp: ``distcp-default.xml`` * hdfs: ``hdfs-site.xml`` * hive: ``hive-site.xml`` * mapred: ``mapred-site.xml`` * pig: ``pig.properties`` * spark: ``spark-defaults.conf`` * yarn: ``yarn-site.xml`` For more information, see `Cluster properties <https://cloud.google.com/dataproc/docs/concepts/cluster-properties>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15a7b63981dae2ee44362a706c3e00460c08f47305da6fc5ce312393147d2a67)
            check_type(argname="argument image_version", value=image_version, expected_type=type_hints["image_version"])
            check_type(argname="argument optional_components", value=optional_components, expected_type=type_hints["optional_components"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if image_version is not None:
            self._values["image_version"] = image_version
        if optional_components is not None:
            self._values["optional_components"] = optional_components
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def image_version(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The version of software inside the cluster. It must be one of the supported `Dataproc Versions <https://cloud.google.com/dataproc/docs/concepts/versioning/dataproc-versions#supported_dataproc_versions>`_, such as "1.2" (including a subminor version, such as "1.2.29"), or the `"preview" version <https://cloud.google.com/dataproc/docs/concepts/versioning/dataproc-versions#other_versions>`_. If unspecified, it defaults to the latest Debian version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#image_version DataprocWorkflowTemplate#image_version}
        '''
        result = self._values.get("image_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional_components(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. The set of components to activate on the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#optional_components DataprocWorkflowTemplate#optional_components}
        '''
        result = self._values.get("optional_components")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        The properties to set on daemon config files. Property keys are specified in ``prefix:property`` format, for example ``core:hadoop.tmp.dir``. The following are supported prefixes and their mappings: * capacity-scheduler: ``capacity-scheduler.xml`` * core: ``core-site.xml`` * distcp: ``distcp-default.xml`` * hdfs: ``hdfs-site.xml`` * hive: ``hive-site.xml`` * mapred: ``mapred-site.xml`` * pig: ``pig.properties`` * spark: ``spark-defaults.conf`` * yarn: ``yarn-site.xml`` For more information, see `Cluster properties <https://cloud.google.com/dataproc/docs/concepts/cluster-properties>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#properties DataprocWorkflowTemplate#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigSoftwareConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplatePlacementManagedClusterConfigSoftwareConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigSoftwareConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c869331717948fdb011e0454935b4879093c9bc4d85551e3940b5097cf7a7789)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetImageVersion")
    def reset_image_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageVersion", []))

    @jsii.member(jsii_name="resetOptionalComponents")
    def reset_optional_components(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptionalComponents", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @builtins.property
    @jsii.member(jsii_name="imageVersionInput")
    def image_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="optionalComponentsInput")
    def optional_components_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "optionalComponentsInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="imageVersion")
    def image_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageVersion"))

    @image_version.setter
    def image_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d47e10f249f6b26c7884f7d663274a8b1d54855d32f31612975ecfe07902a40b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="optionalComponents")
    def optional_components(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "optionalComponents"))

    @optional_components.setter
    def optional_components(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b652a3702cb1a6d59a9da984ad9c6d3824e9b8deb32bb2d32305cc5f9a1eaa2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optionalComponents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0542084736348b3b16c8dc8d4e11ef8a8ae084a0030f1458cf561964145e1c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSoftwareConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSoftwareConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSoftwareConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2496cd1086e8d2e9dec4ea77d21babf0cc00b11e50288d30be1b3d236d9122e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "accelerators": "accelerators",
        "disk_config": "diskConfig",
        "image": "image",
        "machine_type": "machineType",
        "min_cpu_platform": "minCpuPlatform",
        "num_instances": "numInstances",
        "preemptibility": "preemptibility",
    },
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfig:
    def __init__(
        self,
        *,
        accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAccelerators", typing.Dict[builtins.str, typing.Any]]]]] = None,
        disk_config: typing.Optional[typing.Union["DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigDiskConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        image: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        num_instances: typing.Optional[jsii.Number] = None,
        preemptibility: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accelerators: accelerators block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#accelerators DataprocWorkflowTemplate#accelerators}
        :param disk_config: disk_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#disk_config DataprocWorkflowTemplate#disk_config}
        :param image: Optional. The Compute Engine image resource used for cluster instances. The URI can represent an image or image family. Image examples: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/global/images/[image-id]`` * ``projects/[project_id]/global/images/[image-id]`` * ``image-id`` Image family examples. Dataproc will use the most recent image from the family: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/global/images/family/[custom-image-family-name]`` * ``projects/[project_id]/global/images/family/[custom-image-family-name]`` If the URI is unspecified, it will be inferred from ``SoftwareConfig.image_version`` or the system default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#image DataprocWorkflowTemplate#image}
        :param machine_type: Optional. The Compute Engine machine type used for cluster instances. A full URL, partial URI, or short name are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/zones/us-east1-a/machineTypes/n1-standard-2`` * ``projects/[project_id]/zones/us-east1-a/machineTypes/n1-standard-2`` * ``n1-standard-2`` **Auto Zone Exception**: If you are using the Dataproc `Auto Zone Placement <https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/auto-zone#using_auto_zone_placement>`_ feature, you must use the short name of the machine type resource, for example, ``n1-standard-2``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#machine_type DataprocWorkflowTemplate#machine_type}
        :param min_cpu_platform: Optional. Specifies the minimum cpu platform for the Instance Group. See `Dataproc -> Minimum CPU Platform <https://cloud.google.com/dataproc/docs/concepts/compute/dataproc-min-cpu>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#min_cpu_platform DataprocWorkflowTemplate#min_cpu_platform}
        :param num_instances: Optional. The number of VM instances in the instance group. For `HA cluster </dataproc/docs/concepts/configuring-clusters/high-availability>`_ `master_config <#FIELDS.master_config>`_ groups, **must be set to 3**. For standard cluster `master_config <#FIELDS.master_config>`_ groups, **must be set to 1**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#num_instances DataprocWorkflowTemplate#num_instances}
        :param preemptibility: Optional. Specifies the preemptibility of the instance group. The default value for master and worker groups is ``NON_PREEMPTIBLE``. This default cannot be changed. The default value for secondary instances is ``PREEMPTIBLE``. Possible values: PREEMPTIBILITY_UNSPECIFIED, NON_PREEMPTIBLE, PREEMPTIBLE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#preemptibility DataprocWorkflowTemplate#preemptibility}
        '''
        if isinstance(disk_config, dict):
            disk_config = DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigDiskConfig(**disk_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87b23e9ff9c59eef8dd0d9c46f05ff55e167b38e40547abda83b20afbdf9b153)
            check_type(argname="argument accelerators", value=accelerators, expected_type=type_hints["accelerators"])
            check_type(argname="argument disk_config", value=disk_config, expected_type=type_hints["disk_config"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument min_cpu_platform", value=min_cpu_platform, expected_type=type_hints["min_cpu_platform"])
            check_type(argname="argument num_instances", value=num_instances, expected_type=type_hints["num_instances"])
            check_type(argname="argument preemptibility", value=preemptibility, expected_type=type_hints["preemptibility"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerators is not None:
            self._values["accelerators"] = accelerators
        if disk_config is not None:
            self._values["disk_config"] = disk_config
        if image is not None:
            self._values["image"] = image
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if min_cpu_platform is not None:
            self._values["min_cpu_platform"] = min_cpu_platform
        if num_instances is not None:
            self._values["num_instances"] = num_instances
        if preemptibility is not None:
            self._values["preemptibility"] = preemptibility

    @builtins.property
    def accelerators(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAccelerators"]]]:
        '''accelerators block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#accelerators DataprocWorkflowTemplate#accelerators}
        '''
        result = self._values.get("accelerators")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAccelerators"]]], result)

    @builtins.property
    def disk_config(
        self,
    ) -> typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigDiskConfig"]:
        '''disk_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#disk_config DataprocWorkflowTemplate#disk_config}
        '''
        result = self._values.get("disk_config")
        return typing.cast(typing.Optional["DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigDiskConfig"], result)

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The Compute Engine image resource used for cluster instances. The URI can represent an image or image family. Image examples: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/global/images/[image-id]`` * ``projects/[project_id]/global/images/[image-id]`` * ``image-id`` Image family examples. Dataproc will use the most recent image from the family: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/global/images/family/[custom-image-family-name]`` * ``projects/[project_id]/global/images/family/[custom-image-family-name]`` If the URI is unspecified, it will be inferred from ``SoftwareConfig.image_version`` or the system default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#image DataprocWorkflowTemplate#image}
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The Compute Engine machine type used for cluster instances. A full URL, partial URI, or short name are valid. Examples: * ``https://www.googleapis.com/compute/v1/projects/[project_id]/zones/us-east1-a/machineTypes/n1-standard-2`` * ``projects/[project_id]/zones/us-east1-a/machineTypes/n1-standard-2`` * ``n1-standard-2`` **Auto Zone Exception**: If you are using the Dataproc `Auto Zone Placement <https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/auto-zone#using_auto_zone_placement>`_ feature, you must use the short name of the machine type resource, for example, ``n1-standard-2``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#machine_type DataprocWorkflowTemplate#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_cpu_platform(self) -> typing.Optional[builtins.str]:
        '''Optional. Specifies the minimum cpu platform for the Instance Group. See `Dataproc -> Minimum CPU Platform <https://cloud.google.com/dataproc/docs/concepts/compute/dataproc-min-cpu>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#min_cpu_platform DataprocWorkflowTemplate#min_cpu_platform}
        '''
        result = self._values.get("min_cpu_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_instances(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The number of VM instances in the instance group. For `HA cluster </dataproc/docs/concepts/configuring-clusters/high-availability>`_ `master_config <#FIELDS.master_config>`_ groups, **must be set to 3**. For standard cluster `master_config <#FIELDS.master_config>`_ groups, **must be set to 1**.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#num_instances DataprocWorkflowTemplate#num_instances}
        '''
        result = self._values.get("num_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preemptibility(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Specifies the preemptibility of the instance group. The default value for master and worker groups is ``NON_PREEMPTIBLE``. This default cannot be changed. The default value for secondary instances is ``PREEMPTIBLE``. Possible values: PREEMPTIBILITY_UNSPECIFIED, NON_PREEMPTIBLE, PREEMPTIBLE

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#preemptibility DataprocWorkflowTemplate#preemptibility}
        '''
        result = self._values.get("preemptibility")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAccelerators",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_count": "acceleratorCount",
        "accelerator_type": "acceleratorType",
    },
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAccelerators:
    def __init__(
        self,
        *,
        accelerator_count: typing.Optional[jsii.Number] = None,
        accelerator_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accelerator_count: The number of the accelerator cards of this type exposed to this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#accelerator_count DataprocWorkflowTemplate#accelerator_count}
        :param accelerator_type: Full URL, partial URI, or short name of the accelerator type resource to expose to this instance. See `Compute Engine AcceleratorTypes <https://cloud.google.com/compute/docs/reference/beta/acceleratorTypes>`_. Examples: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/zones/us-east1-a/acceleratorTypes/nvidia-tesla-k80`` * ``projects/[project_id]/zones/us-east1-a/acceleratorTypes/nvidia-tesla-k80`` * ``nvidia-tesla-k80`` **Auto Zone Exception**: If you are using the Dataproc `Auto Zone Placement <https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/auto-zone#using_auto_zone_placement>`_ feature, you must use the short name of the accelerator type resource, for example, ``nvidia-tesla-k80``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#accelerator_type DataprocWorkflowTemplate#accelerator_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9fce16afa287b9285d81c474559c59186cbcbd37c510fad3f1a58054e39ee37)
            check_type(argname="argument accelerator_count", value=accelerator_count, expected_type=type_hints["accelerator_count"])
            check_type(argname="argument accelerator_type", value=accelerator_type, expected_type=type_hints["accelerator_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerator_count is not None:
            self._values["accelerator_count"] = accelerator_count
        if accelerator_type is not None:
            self._values["accelerator_type"] = accelerator_type

    @builtins.property
    def accelerator_count(self) -> typing.Optional[jsii.Number]:
        '''The number of the accelerator cards of this type exposed to this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#accelerator_count DataprocWorkflowTemplate#accelerator_count}
        '''
        result = self._values.get("accelerator_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def accelerator_type(self) -> typing.Optional[builtins.str]:
        '''Full URL, partial URI, or short name of the accelerator type resource to expose to this instance.

        See `Compute Engine AcceleratorTypes <https://cloud.google.com/compute/docs/reference/beta/acceleratorTypes>`_. Examples: * ``https://www.googleapis.com/compute/beta/projects/[project_id]/zones/us-east1-a/acceleratorTypes/nvidia-tesla-k80`` * ``projects/[project_id]/zones/us-east1-a/acceleratorTypes/nvidia-tesla-k80`` * ``nvidia-tesla-k80`` **Auto Zone Exception**: If you are using the Dataproc `Auto Zone Placement <https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/auto-zone#using_auto_zone_placement>`_ feature, you must use the short name of the accelerator type resource, for example, ``nvidia-tesla-k80``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#accelerator_type DataprocWorkflowTemplate#accelerator_type}
        '''
        result = self._values.get("accelerator_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAccelerators(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAcceleratorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAcceleratorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a04b523ff6a4f80d3b1899d059b06170800309a8d196eeab589bba86810673a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAcceleratorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e014a309a0f2c43929aaef3cc00f4bb8b3e87d40fe02772026a1b0e7d984704)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAcceleratorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e203ce42938a621a718af90ba33274329249692c4542251a663c348c24d774d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd895fb858b05c48f304f54c129da9f8744fae948ea9560ac7931c01a255a626)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5773a07342fc214280f91a9c1dde8b19c5175dafe3cc6821ba36a287f558b90c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAccelerators]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAccelerators]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80b94e6aab7a14f76a71a645f5b323f2998c5f77b39a91d726a002272e4045bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAcceleratorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAcceleratorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e628cf0dbcc44b2a0bbe045ce0f1337f3be8b9ade6873f5478bc011056bcda7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAcceleratorCount")
    def reset_accelerator_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorCount", []))

    @jsii.member(jsii_name="resetAcceleratorType")
    def reset_accelerator_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorType", []))

    @builtins.property
    @jsii.member(jsii_name="acceleratorCountInput")
    def accelerator_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "acceleratorCountInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTypeInput")
    def accelerator_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceleratorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorCount")
    def accelerator_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "acceleratorCount"))

    @accelerator_count.setter
    def accelerator_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81a7d371c2fe83f3a126580df01cf221e0f5893b03f1eb43d42b307e1088ef3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de0a0143951b78698b0c687f1810e2dd2ed7ed3356b088c5d76b0b3a9857b777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAccelerators]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAccelerators]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAccelerators]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a2fe541d881146cea222b494b3953c2cf3290dadfb35fc91d38b7e3eac3026d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigDiskConfig",
    jsii_struct_bases=[],
    name_mapping={
        "boot_disk_size_gb": "bootDiskSizeGb",
        "boot_disk_type": "bootDiskType",
        "num_local_ssds": "numLocalSsds",
    },
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigDiskConfig:
    def __init__(
        self,
        *,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        boot_disk_type: typing.Optional[builtins.str] = None,
        num_local_ssds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param boot_disk_size_gb: Optional. Size in GB of the boot disk (default is 500GB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#boot_disk_size_gb DataprocWorkflowTemplate#boot_disk_size_gb}
        :param boot_disk_type: Optional. Type of the boot disk (default is "pd-standard"). Valid values: "pd-balanced" (Persistent Disk Balanced Solid State Drive), "pd-ssd" (Persistent Disk Solid State Drive), or "pd-standard" (Persistent Disk Hard Disk Drive). See `Disk types <https://cloud.google.com/compute/docs/disks#disk-types>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#boot_disk_type DataprocWorkflowTemplate#boot_disk_type}
        :param num_local_ssds: Optional. Number of attached SSDs, from 0 to 4 (default is 0). If SSDs are not attached, the boot disk is used to store runtime logs and `HDFS <https://hadoop.apache.org/docs/r1.2.1/hdfs_user_guide.html>`_ data. If one or more SSDs are attached, this runtime bulk data is spread across them, and the boot disk contains only basic config and installed binaries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#num_local_ssds DataprocWorkflowTemplate#num_local_ssds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71c684606c53202c61009e5ef18f1f9856d3236c830871cd508c7dea719d79de)
            check_type(argname="argument boot_disk_size_gb", value=boot_disk_size_gb, expected_type=type_hints["boot_disk_size_gb"])
            check_type(argname="argument boot_disk_type", value=boot_disk_type, expected_type=type_hints["boot_disk_type"])
            check_type(argname="argument num_local_ssds", value=num_local_ssds, expected_type=type_hints["num_local_ssds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if boot_disk_size_gb is not None:
            self._values["boot_disk_size_gb"] = boot_disk_size_gb
        if boot_disk_type is not None:
            self._values["boot_disk_type"] = boot_disk_type
        if num_local_ssds is not None:
            self._values["num_local_ssds"] = num_local_ssds

    @builtins.property
    def boot_disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Optional. Size in GB of the boot disk (default is 500GB).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#boot_disk_size_gb DataprocWorkflowTemplate#boot_disk_size_gb}
        '''
        result = self._values.get("boot_disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def boot_disk_type(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Type of the boot disk (default is "pd-standard"). Valid values: "pd-balanced" (Persistent Disk Balanced Solid State Drive), "pd-ssd" (Persistent Disk Solid State Drive), or "pd-standard" (Persistent Disk Hard Disk Drive). See `Disk types <https://cloud.google.com/compute/docs/disks#disk-types>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#boot_disk_type DataprocWorkflowTemplate#boot_disk_type}
        '''
        result = self._values.get("boot_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_local_ssds(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        Number of attached SSDs, from 0 to 4 (default is 0). If SSDs are not attached, the boot disk is used to store runtime logs and `HDFS <https://hadoop.apache.org/docs/r1.2.1/hdfs_user_guide.html>`_ data. If one or more SSDs are attached, this runtime bulk data is spread across them, and the boot disk contains only basic config and installed binaries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#num_local_ssds DataprocWorkflowTemplate#num_local_ssds}
        '''
        result = self._values.get("num_local_ssds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigDiskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigDiskConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigDiskConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffe2644414d085f93615f348cef10ab316050a97b6b2a74fa7b8b1d389ab0250)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBootDiskSizeGb")
    def reset_boot_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskSizeGb", []))

    @jsii.member(jsii_name="resetBootDiskType")
    def reset_boot_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskType", []))

    @jsii.member(jsii_name="resetNumLocalSsds")
    def reset_num_local_ssds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumLocalSsds", []))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGbInput")
    def boot_disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootDiskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskTypeInput")
    def boot_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="numLocalSsdsInput")
    def num_local_ssds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numLocalSsdsInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGb")
    def boot_disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bootDiskSizeGb"))

    @boot_disk_size_gb.setter
    def boot_disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d77044befb73ea2f61602820d2977b2afae2b5f480f67c675512f5a19361b7db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bootDiskType")
    def boot_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootDiskType"))

    @boot_disk_type.setter
    def boot_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b0a1cfb66889d088dfcc3a41501a4dbf48a3a4f3624ee7ec6e016fa5e0c543)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numLocalSsds")
    def num_local_ssds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numLocalSsds"))

    @num_local_ssds.setter
    def num_local_ssds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62bc6f8dc256d96f9c26b24b1f5d694c38ede01d20ddc82b2cc44ef8875c799f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numLocalSsds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigDiskConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigDiskConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigDiskConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eee1cfc07af0fa430fc61f73324ea1a45782c9365ddb024f814f87b415af854)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigManagedGroupConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigManagedGroupConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigManagedGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigManagedGroupConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigManagedGroupConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c91cd8f51934956f2f8267e65dda3cfd56fc59933fd71a099e841b26d94c4af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigManagedGroupConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21746934340ac258a4a72b7dd6168be8af7cae4fa9add4a0b6a54f9cbb2c6ed5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigManagedGroupConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__097dc1d6184e00e4fa467982937c7da29fa6b349d7467a510a62f0dfbb547c60)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87e32d37a0f61c489e4eee7bdbc55bf73f6bd8cde9baefba4aa2d1f683accf3b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5e85e2fe53f287864e3f1f19745355ec74e79c2b2f8bf6db985b9f5deb910c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigManagedGroupConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigManagedGroupConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__906e41d05208fb9f473343c83597dbe5f1fb5428b2facaa1859679b81e046215)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="instanceGroupManagerName")
    def instance_group_manager_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceGroupManagerName"))

    @builtins.property
    @jsii.member(jsii_name="instanceTemplateName")
    def instance_template_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceTemplateName"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigManagedGroupConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigManagedGroupConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigManagedGroupConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c91671b142497e0e9e4384294ec0616ad5489594031735114abf9af0d9d9091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99b0c07763ecc66d6629a075805a0517df78ec5bba178fab136f3a672774045d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccelerators")
    def put_accelerators(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__780977930c6e44a70c97b0b6295f518c840152b2d8a1c71c13d3fb18cb57e4a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccelerators", [value]))

    @jsii.member(jsii_name="putDiskConfig")
    def put_disk_config(
        self,
        *,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        boot_disk_type: typing.Optional[builtins.str] = None,
        num_local_ssds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param boot_disk_size_gb: Optional. Size in GB of the boot disk (default is 500GB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#boot_disk_size_gb DataprocWorkflowTemplate#boot_disk_size_gb}
        :param boot_disk_type: Optional. Type of the boot disk (default is "pd-standard"). Valid values: "pd-balanced" (Persistent Disk Balanced Solid State Drive), "pd-ssd" (Persistent Disk Solid State Drive), or "pd-standard" (Persistent Disk Hard Disk Drive). See `Disk types <https://cloud.google.com/compute/docs/disks#disk-types>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#boot_disk_type DataprocWorkflowTemplate#boot_disk_type}
        :param num_local_ssds: Optional. Number of attached SSDs, from 0 to 4 (default is 0). If SSDs are not attached, the boot disk is used to store runtime logs and `HDFS <https://hadoop.apache.org/docs/r1.2.1/hdfs_user_guide.html>`_ data. If one or more SSDs are attached, this runtime bulk data is spread across them, and the boot disk contains only basic config and installed binaries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#num_local_ssds DataprocWorkflowTemplate#num_local_ssds}
        '''
        value = DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigDiskConfig(
            boot_disk_size_gb=boot_disk_size_gb,
            boot_disk_type=boot_disk_type,
            num_local_ssds=num_local_ssds,
        )

        return typing.cast(None, jsii.invoke(self, "putDiskConfig", [value]))

    @jsii.member(jsii_name="resetAccelerators")
    def reset_accelerators(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccelerators", []))

    @jsii.member(jsii_name="resetDiskConfig")
    def reset_disk_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskConfig", []))

    @jsii.member(jsii_name="resetImage")
    def reset_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImage", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @jsii.member(jsii_name="resetMinCpuPlatform")
    def reset_min_cpu_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinCpuPlatform", []))

    @jsii.member(jsii_name="resetNumInstances")
    def reset_num_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumInstances", []))

    @jsii.member(jsii_name="resetPreemptibility")
    def reset_preemptibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreemptibility", []))

    @builtins.property
    @jsii.member(jsii_name="accelerators")
    def accelerators(
        self,
    ) -> DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAcceleratorsList:
        return typing.cast(DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAcceleratorsList, jsii.get(self, "accelerators"))

    @builtins.property
    @jsii.member(jsii_name="diskConfig")
    def disk_config(
        self,
    ) -> DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigDiskConfigOutputReference:
        return typing.cast(DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigDiskConfigOutputReference, jsii.get(self, "diskConfig"))

    @builtins.property
    @jsii.member(jsii_name="instanceNames")
    def instance_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceNames"))

    @builtins.property
    @jsii.member(jsii_name="isPreemptible")
    def is_preemptible(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isPreemptible"))

    @builtins.property
    @jsii.member(jsii_name="managedGroupConfig")
    def managed_group_config(
        self,
    ) -> DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigManagedGroupConfigList:
        return typing.cast(DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigManagedGroupConfigList, jsii.get(self, "managedGroupConfig"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorsInput")
    def accelerators_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAccelerators]]], jsii.get(self, "acceleratorsInput"))

    @builtins.property
    @jsii.member(jsii_name="diskConfigInput")
    def disk_config_input(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigDiskConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigDiskConfig], jsii.get(self, "diskConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatformInput")
    def min_cpu_platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minCpuPlatformInput"))

    @builtins.property
    @jsii.member(jsii_name="numInstancesInput")
    def num_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="preemptibilityInput")
    def preemptibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preemptibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b238422558e3c28576421616554c5b010d1586127613fbabea8f4b9bc09e5ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__612eaf2684c86c869eb59ddd8fda11e9d419ec1e9444a9d6fc2f5276ef3da0c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatform")
    def min_cpu_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minCpuPlatform"))

    @min_cpu_platform.setter
    def min_cpu_platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fece6ebcc3fb028e2ced195cb32432271c86f2c3949f5f5c6de3c035944d2a18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCpuPlatform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numInstances")
    def num_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numInstances"))

    @num_instances.setter
    def num_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__def67c72b9d3ac53cd049c0519bb91572d435a84c882dcc9f01c33f3bbbf2bac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preemptibility")
    def preemptibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preemptibility"))

    @preemptibility.setter
    def preemptibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__480d5c790faa49b98163dc516467244d97102abd385e5b121a79ae8423c1a0d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preemptibility", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2511fb284e25fb6a1f73fa37c6dcdfba21157c3a03090c322c58fbb3e7391495)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplatePlacementManagedClusterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementManagedClusterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4625626c4e3b090e80bf89da2cd01174924b18759b907b99e9d99a09fda1530)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        autoscaling_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigAutoscalingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        encryption_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigEndpointConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        gce_cluster_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        initialization_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
        lifecycle_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigLifecycleConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        master_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        secondary_worker_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        security_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        software_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigSoftwareConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        staging_bucket: typing.Optional[builtins.str] = None,
        temp_bucket: typing.Optional[builtins.str] = None,
        worker_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param autoscaling_config: autoscaling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#autoscaling_config DataprocWorkflowTemplate#autoscaling_config}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#encryption_config DataprocWorkflowTemplate#encryption_config}
        :param endpoint_config: endpoint_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#endpoint_config DataprocWorkflowTemplate#endpoint_config}
        :param gce_cluster_config: gce_cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#gce_cluster_config DataprocWorkflowTemplate#gce_cluster_config}
        :param initialization_actions: initialization_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#initialization_actions DataprocWorkflowTemplate#initialization_actions}
        :param lifecycle_config: lifecycle_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#lifecycle_config DataprocWorkflowTemplate#lifecycle_config}
        :param master_config: master_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#master_config DataprocWorkflowTemplate#master_config}
        :param secondary_worker_config: secondary_worker_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#secondary_worker_config DataprocWorkflowTemplate#secondary_worker_config}
        :param security_config: security_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#security_config DataprocWorkflowTemplate#security_config}
        :param software_config: software_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#software_config DataprocWorkflowTemplate#software_config}
        :param staging_bucket: Optional. A Cloud Storage bucket used to stage job dependencies, config files, and job driver console output. If you do not specify a staging bucket, Cloud Dataproc will determine a Cloud Storage location (US, ASIA, or EU) for your cluster's staging bucket according to the Compute Engine zone where your cluster is deployed, and then create and manage this project-level, per-location bucket (see `Dataproc staging bucket <https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/staging-bucket>`_). **This field requires a Cloud Storage bucket name, not a URI to a Cloud Storage bucket.** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#staging_bucket DataprocWorkflowTemplate#staging_bucket}
        :param temp_bucket: Optional. A Cloud Storage bucket used to store ephemeral cluster and jobs data, such as Spark and MapReduce history files. If you do not specify a temp bucket, Dataproc will determine a Cloud Storage location (US, ASIA, or EU) for your cluster's temp bucket according to the Compute Engine zone where your cluster is deployed, and then create and manage this project-level, per-location bucket. The default bucket has a TTL of 90 days, but you can use any TTL (or none) if you specify a bucket. **This field requires a Cloud Storage bucket name, not a URI to a Cloud Storage bucket.** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#temp_bucket DataprocWorkflowTemplate#temp_bucket}
        :param worker_config: worker_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#worker_config DataprocWorkflowTemplate#worker_config}
        '''
        value = DataprocWorkflowTemplatePlacementManagedClusterConfig(
            autoscaling_config=autoscaling_config,
            encryption_config=encryption_config,
            endpoint_config=endpoint_config,
            gce_cluster_config=gce_cluster_config,
            initialization_actions=initialization_actions,
            lifecycle_config=lifecycle_config,
            master_config=master_config,
            secondary_worker_config=secondary_worker_config,
            security_config=security_config,
            software_config=software_config,
            staging_bucket=staging_bucket,
            temp_bucket=temp_bucket,
            worker_config=worker_config,
        )

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(
        self,
    ) -> DataprocWorkflowTemplatePlacementManagedClusterConfigOutputReference:
        return typing.cast(DataprocWorkflowTemplatePlacementManagedClusterConfigOutputReference, jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="clusterNameInput")
    def cluster_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfig]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfig], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e901edd7b10b681e2ce82df77500301427e49f773212c21520bfe4e97ee2ee0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffb54874e62c78cdf3a4606bbbe27ba6e04ef8c333e517114446d0f1f30333ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedCluster]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedCluster], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacementManagedCluster],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab3d63ca3c5eb5a1c826d2aa812d574de374581137c3a2004da5ba8848516e5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocWorkflowTemplatePlacementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplatePlacementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9921a33f2f6b52bb44662ef7d327aef5b4d998608b7a40f2f4e97bf4d1f46c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClusterSelector")
    def put_cluster_selector(
        self,
        *,
        cluster_labels: typing.Mapping[builtins.str, builtins.str],
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster_labels: Required. The cluster labels. Cluster must have all labels to match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#cluster_labels DataprocWorkflowTemplate#cluster_labels}
        :param zone: Optional. The zone where workflow process executes. This parameter does not affect the selection of the cluster. If unspecified, the zone of the first cluster matching the selector is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#zone DataprocWorkflowTemplate#zone}
        '''
        value = DataprocWorkflowTemplatePlacementClusterSelector(
            cluster_labels=cluster_labels, zone=zone
        )

        return typing.cast(None, jsii.invoke(self, "putClusterSelector", [value]))

    @jsii.member(jsii_name="putManagedCluster")
    def put_managed_cluster(
        self,
        *,
        cluster_name: builtins.str,
        config: typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfig, typing.Dict[builtins.str, typing.Any]],
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param cluster_name: Required. The cluster name prefix. A unique cluster name will be formed by appending a random suffix. The name must contain only lower-case letters (a-z), numbers (0-9), and hyphens (-). Must begin with a letter. Cannot begin or end with hyphen. Must consist of between 2 and 35 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#cluster_name DataprocWorkflowTemplate#cluster_name}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#config DataprocWorkflowTemplate#config}
        :param labels: Optional. The labels to associate with this cluster. Label keys must be between 1 and 63 characters long, and must conform to the following PCRE regular expression: p{Ll}p{Lo}{0,62} Label values must be between 1 and 63 characters long, and must conform to the following PCRE regular expression: [p{Ll}p{Lo}p{N}_-]{0,63} No more than 32 labels can be associated with a given cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#labels DataprocWorkflowTemplate#labels}
        '''
        value = DataprocWorkflowTemplatePlacementManagedCluster(
            cluster_name=cluster_name, config=config, labels=labels
        )

        return typing.cast(None, jsii.invoke(self, "putManagedCluster", [value]))

    @jsii.member(jsii_name="resetClusterSelector")
    def reset_cluster_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterSelector", []))

    @jsii.member(jsii_name="resetManagedCluster")
    def reset_managed_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedCluster", []))

    @builtins.property
    @jsii.member(jsii_name="clusterSelector")
    def cluster_selector(
        self,
    ) -> DataprocWorkflowTemplatePlacementClusterSelectorOutputReference:
        return typing.cast(DataprocWorkflowTemplatePlacementClusterSelectorOutputReference, jsii.get(self, "clusterSelector"))

    @builtins.property
    @jsii.member(jsii_name="managedCluster")
    def managed_cluster(
        self,
    ) -> DataprocWorkflowTemplatePlacementManagedClusterOutputReference:
        return typing.cast(DataprocWorkflowTemplatePlacementManagedClusterOutputReference, jsii.get(self, "managedCluster"))

    @builtins.property
    @jsii.member(jsii_name="clusterSelectorInput")
    def cluster_selector_input(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementClusterSelector]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementClusterSelector], jsii.get(self, "clusterSelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="managedClusterInput")
    def managed_cluster_input(
        self,
    ) -> typing.Optional[DataprocWorkflowTemplatePlacementManagedCluster]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacementManagedCluster], jsii.get(self, "managedClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocWorkflowTemplatePlacement]:
        return typing.cast(typing.Optional[DataprocWorkflowTemplatePlacement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocWorkflowTemplatePlacement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b94969ba8688393c5e6a9e6189078426e4eb9d2fff62176648662051e3da3c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DataprocWorkflowTemplateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#create DataprocWorkflowTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#delete DataprocWorkflowTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#update DataprocWorkflowTemplate#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__460de6c7e0f8a64d50a58c4bd6ecb3c084ba2846494a6cbbd351e88145cf047f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#create DataprocWorkflowTemplate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#delete DataprocWorkflowTemplate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_workflow_template#update DataprocWorkflowTemplate#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocWorkflowTemplateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocWorkflowTemplateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocWorkflowTemplate.DataprocWorkflowTemplateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbefc1f4149e43537e30319053da2c9615974e1a7de20d8168f60cb0619f7a9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09ff9de513ad75a93302eb7a4283dab6e53da0be5262c2a476bd33b01e57920b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b225d8d5ced29ddfd8709ddef78c587aedf937842765d5d081aeecd64cf4342)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__967944da9e068b696ac01fc3f03faca71a0a3cfc42477a98ac5db4e727cbd598)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04670f17a941cda992e00d8d159b07d49b148f3fe05361ed19c4209b2a895e33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataprocWorkflowTemplate",
    "DataprocWorkflowTemplateConfig",
    "DataprocWorkflowTemplateEncryptionConfig",
    "DataprocWorkflowTemplateEncryptionConfigOutputReference",
    "DataprocWorkflowTemplateJobs",
    "DataprocWorkflowTemplateJobsHadoopJob",
    "DataprocWorkflowTemplateJobsHadoopJobLoggingConfig",
    "DataprocWorkflowTemplateJobsHadoopJobLoggingConfigOutputReference",
    "DataprocWorkflowTemplateJobsHadoopJobOutputReference",
    "DataprocWorkflowTemplateJobsHiveJob",
    "DataprocWorkflowTemplateJobsHiveJobOutputReference",
    "DataprocWorkflowTemplateJobsHiveJobQueryListStruct",
    "DataprocWorkflowTemplateJobsHiveJobQueryListStructOutputReference",
    "DataprocWorkflowTemplateJobsList",
    "DataprocWorkflowTemplateJobsOutputReference",
    "DataprocWorkflowTemplateJobsPigJob",
    "DataprocWorkflowTemplateJobsPigJobLoggingConfig",
    "DataprocWorkflowTemplateJobsPigJobLoggingConfigOutputReference",
    "DataprocWorkflowTemplateJobsPigJobOutputReference",
    "DataprocWorkflowTemplateJobsPigJobQueryListStruct",
    "DataprocWorkflowTemplateJobsPigJobQueryListStructOutputReference",
    "DataprocWorkflowTemplateJobsPrestoJob",
    "DataprocWorkflowTemplateJobsPrestoJobLoggingConfig",
    "DataprocWorkflowTemplateJobsPrestoJobLoggingConfigOutputReference",
    "DataprocWorkflowTemplateJobsPrestoJobOutputReference",
    "DataprocWorkflowTemplateJobsPrestoJobQueryListStruct",
    "DataprocWorkflowTemplateJobsPrestoJobQueryListStructOutputReference",
    "DataprocWorkflowTemplateJobsPysparkJob",
    "DataprocWorkflowTemplateJobsPysparkJobLoggingConfig",
    "DataprocWorkflowTemplateJobsPysparkJobLoggingConfigOutputReference",
    "DataprocWorkflowTemplateJobsPysparkJobOutputReference",
    "DataprocWorkflowTemplateJobsScheduling",
    "DataprocWorkflowTemplateJobsSchedulingOutputReference",
    "DataprocWorkflowTemplateJobsSparkJob",
    "DataprocWorkflowTemplateJobsSparkJobLoggingConfig",
    "DataprocWorkflowTemplateJobsSparkJobLoggingConfigOutputReference",
    "DataprocWorkflowTemplateJobsSparkJobOutputReference",
    "DataprocWorkflowTemplateJobsSparkRJob",
    "DataprocWorkflowTemplateJobsSparkRJobLoggingConfig",
    "DataprocWorkflowTemplateJobsSparkRJobLoggingConfigOutputReference",
    "DataprocWorkflowTemplateJobsSparkRJobOutputReference",
    "DataprocWorkflowTemplateJobsSparkSqlJob",
    "DataprocWorkflowTemplateJobsSparkSqlJobLoggingConfig",
    "DataprocWorkflowTemplateJobsSparkSqlJobLoggingConfigOutputReference",
    "DataprocWorkflowTemplateJobsSparkSqlJobOutputReference",
    "DataprocWorkflowTemplateJobsSparkSqlJobQueryListStruct",
    "DataprocWorkflowTemplateJobsSparkSqlJobQueryListStructOutputReference",
    "DataprocWorkflowTemplateParameters",
    "DataprocWorkflowTemplateParametersList",
    "DataprocWorkflowTemplateParametersOutputReference",
    "DataprocWorkflowTemplateParametersValidation",
    "DataprocWorkflowTemplateParametersValidationOutputReference",
    "DataprocWorkflowTemplateParametersValidationRegex",
    "DataprocWorkflowTemplateParametersValidationRegexOutputReference",
    "DataprocWorkflowTemplateParametersValidationValues",
    "DataprocWorkflowTemplateParametersValidationValuesOutputReference",
    "DataprocWorkflowTemplatePlacement",
    "DataprocWorkflowTemplatePlacementClusterSelector",
    "DataprocWorkflowTemplatePlacementClusterSelectorOutputReference",
    "DataprocWorkflowTemplatePlacementManagedCluster",
    "DataprocWorkflowTemplatePlacementManagedClusterConfig",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigAutoscalingConfig",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigAutoscalingConfigOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigEncryptionConfig",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigEncryptionConfigOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigEndpointConfig",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigEndpointConfigOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfig",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigNodeGroupAffinity",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigNodeGroupAffinityOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigReservationAffinity",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigReservationAffinityOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigShieldedInstanceConfig",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigShieldedInstanceConfigOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActions",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActionsList",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActionsOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigLifecycleConfig",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigLifecycleConfigOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfig",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAccelerators",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAcceleratorsList",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAcceleratorsOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigDiskConfig",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigDiskConfigOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigManagedGroupConfig",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigManagedGroupConfigList",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigManagedGroupConfigOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfig",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAccelerators",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAcceleratorsList",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAcceleratorsOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigDiskConfig",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigDiskConfigOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigManagedGroupConfig",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigManagedGroupConfigList",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigManagedGroupConfigOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfig",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigKerberosConfig",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigKerberosConfigOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigSoftwareConfig",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigSoftwareConfigOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfig",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAccelerators",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAcceleratorsList",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAcceleratorsOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigDiskConfig",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigDiskConfigOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigManagedGroupConfig",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigManagedGroupConfigList",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigManagedGroupConfigOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigOutputReference",
    "DataprocWorkflowTemplatePlacementManagedClusterOutputReference",
    "DataprocWorkflowTemplatePlacementOutputReference",
    "DataprocWorkflowTemplateTimeouts",
    "DataprocWorkflowTemplateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__9830cc9f26a89586c2c6b6abe4442c509d35f14cc92942a386cf1f41201434b8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    jobs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocWorkflowTemplateJobs, typing.Dict[builtins.str, typing.Any]]]],
    location: builtins.str,
    name: builtins.str,
    placement: typing.Union[DataprocWorkflowTemplatePlacement, typing.Dict[builtins.str, typing.Any]],
    dag_timeout: typing.Optional[builtins.str] = None,
    encryption_config: typing.Optional[typing.Union[DataprocWorkflowTemplateEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocWorkflowTemplateParameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataprocWorkflowTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__f985950335ab131271164edc200e9112b7c74216e9e2cadfca0b93a64c758bb4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b8382b5345d5a741523c60fa964aa30313cc3086e45adc21eb9c159ca54b25f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocWorkflowTemplateJobs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ae39eb98d79839d93bf02d68e83aeeeb8c531a070340a3bc509dae82ab0f0b8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocWorkflowTemplateParameters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5610ad25355a5fb2dbac7af1674896e0232a13e70ec8ca81616e9efdfecfeb6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0a15632f88ff9973bd18afc8188aafacfbecb46148f17028be1b9751e74a2e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ce9dcab23c03a5aaf4daa0425d19474835b66116621702190b5ec1035132c8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e869f89d1322c38e727892a4455afb8847631531f90f94c111c4275cd863f905(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4480355dcf97e700c09636e3c4c817e43489569e1a76a1057ec2d42d5d6237e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e20168a74ab2570d6975144af96d7c0df997f1d0defa59302004e60b3117280b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb7814abbbc35bff2cd6446d9633551989a46bab30eed5939f66ee7d190d72d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b50eb05c4c9f00e119d3886b927e492be1879301ab49d75050dd9c8374f25f4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    jobs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocWorkflowTemplateJobs, typing.Dict[builtins.str, typing.Any]]]],
    location: builtins.str,
    name: builtins.str,
    placement: typing.Union[DataprocWorkflowTemplatePlacement, typing.Dict[builtins.str, typing.Any]],
    dag_timeout: typing.Optional[builtins.str] = None,
    encryption_config: typing.Optional[typing.Union[DataprocWorkflowTemplateEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocWorkflowTemplateParameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataprocWorkflowTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d439bebb6863495086a504766ad25cedc9a572fd8d32852935dff1748d510e0f(
    *,
    kms_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22e2cf7ae0906f920b6eaef791eca2bfc6d507654f1343865c6f2d13efa05fac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19a9eb7f23795c9654f65f2ffc447348285a76a25fe55d6d096f04892f3773bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32f8645946a33096d80f8a9718fda93b50e6f54356055de530514617314f2fa3(
    value: typing.Optional[DataprocWorkflowTemplateEncryptionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c0d1b66dd50b722b6da850985a1c1527c42676592b8ecebc1ef11cae1cabd0a(
    *,
    step_id: builtins.str,
    hadoop_job: typing.Optional[typing.Union[DataprocWorkflowTemplateJobsHadoopJob, typing.Dict[builtins.str, typing.Any]]] = None,
    hive_job: typing.Optional[typing.Union[DataprocWorkflowTemplateJobsHiveJob, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    pig_job: typing.Optional[typing.Union[DataprocWorkflowTemplateJobsPigJob, typing.Dict[builtins.str, typing.Any]]] = None,
    prerequisite_step_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    presto_job: typing.Optional[typing.Union[DataprocWorkflowTemplateJobsPrestoJob, typing.Dict[builtins.str, typing.Any]]] = None,
    pyspark_job: typing.Optional[typing.Union[DataprocWorkflowTemplateJobsPysparkJob, typing.Dict[builtins.str, typing.Any]]] = None,
    scheduling: typing.Optional[typing.Union[DataprocWorkflowTemplateJobsScheduling, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_job: typing.Optional[typing.Union[DataprocWorkflowTemplateJobsSparkJob, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_r_job: typing.Optional[typing.Union[DataprocWorkflowTemplateJobsSparkRJob, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_sql_job: typing.Optional[typing.Union[DataprocWorkflowTemplateJobsSparkSqlJob, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e33c355518e475289849858a0b682d48445ffce3a23633ca54de2528b3b8a7d1(
    *,
    archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    logging_config: typing.Optional[typing.Union[DataprocWorkflowTemplateJobsHadoopJobLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    main_class: typing.Optional[builtins.str] = None,
    main_jar_file_uri: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f131cce8b64a118408aca7e0cec717d00843bbad284dd88e9c3c85711430d58(
    *,
    driver_log_levels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e1fd30ee46295a0dbaff2999a064b2b1865a4e7041e635bff66613004b33159(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e82f7b27771a1520df4d962dd1002803d1ab9a3e80302dcf0cf893715b83a5a1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b92f337a8343155b805703af004a47dc1bb11a443967c3c684dbba10a11ffcdb(
    value: typing.Optional[DataprocWorkflowTemplateJobsHadoopJobLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a8dbbc6ce15d10cd1c87f0bf1b8ff1ae150ca141946c58503328180d9852d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b42ef617021d95fd5064d5367d6419d585c52e040b588dc609e78be3cdbf94(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__544a6fdbaea92c59d6d6cf26d8b6d52174c329fcc258c15fdab70a53558a45d0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__223718cb1f153ed4a359f1964555cc4ee6634a75fdc4e5d8310b6a4cb6717b39(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8db64929038fb9a9ef351ed917380e7e0aaa7668281cef823999884b53ec85a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03e9da5ab51fc0656af44b81c2f8061231caa885aab1140ec930facaacbbd1f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcd0bc418dbbf0ed3c10b2d8ba1781f46af8864976b07a8c7271311e13eca9ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d26818d6ed07ab6ad4cc7797639b5eb991bbb12c09d382426650c4dbb784895(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d7426b0ed4b8de107b31eb807cae95ba6a836564ef7741359fb49e70f600f3b(
    value: typing.Optional[DataprocWorkflowTemplateJobsHadoopJob],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1a39c4daa737734d1f6b801d9af93f698fcef024af64bc69ec2d69819eb3cb2(
    *,
    continue_on_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    query_file_uri: typing.Optional[builtins.str] = None,
    query_list: typing.Optional[typing.Union[DataprocWorkflowTemplateJobsHiveJobQueryListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
    script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__562de03011484117b184c6a51022467ee4aa02aa60ac1180b5675c33cc8058a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f695be95aeab0822e6c381ca0c2164f0472030e254c684cfff5deb997e145e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c30e4504039dfd98eeac48711f13855b5919e6e5afacc785ea409c06d743c68(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50052ca4ab890fccaf9b29ebe8801665b33410d60f4f3629ccb52a71a8e80bc3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae78151622f6fb9a415f00beca6d6dda6d448d642bdbe0fc0e42859231f03432(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7df0c4025468cf473a27a5a56d5296c8fc38fa80e86cb4b4387fc286259742d1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb63d22a3cb20d91913c73b979ef9d749947788e952b3774e96b5f06e902fc1(
    value: typing.Optional[DataprocWorkflowTemplateJobsHiveJob],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbca1c8603e5944f31137811503c01f8c988675f262483b25aed8fb278c650f9(
    *,
    queries: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20116c617692fb9e566d5dd18da5be186b124344560dbdcf6dcd92045aa874a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd6a6a975f4787b98ebe66d55887248c97dc677e999818574ab83ed5057f478c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c787e3876a998d0dc15ea024f324dca1eb6e37725ed3eebb2f01fd759d8f02ef(
    value: typing.Optional[DataprocWorkflowTemplateJobsHiveJobQueryListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090a56b73373cd95c8f4a49c6fbd5e4a7f65192a35d467d4e3c5da0e14389193(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__014bb647252a938f25cbbc70e82a4d7a82a94dd0e80e1ba662b0480e5e1acbe7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da0a9131c66c4d097f4584251465b9b920f60d8e007b0e77fc802916d506209e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bb9c20c6e8f1d24947d308b2ece27f76403e0ed43738084f509d4f9db2a3544(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__885c751b85992db26ebe91be7b9f9166afc5d745bf93734741f63abc076bfcf4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d006f0760b989718f7e14cb8e48d088241cd54f5216e00e32796e5b6a445235c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplateJobs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db04c30a58e21d31fa29eb006b30ed9a673b1ac947968c14f8077b88b48ccc65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5614fcd8fd1c7f3e88485acce76dfc53acc4a263d840ea791e386dadbb43280f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__149d710609cd1975f56f3fe6bfc1b5a31ad8ec1804b1847ab083f5b8cfb6ad45(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceb207187755c8ff30bf28c194628073cea2a949aacfcfb6346a37f6bc9201fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72f2c78edd8f0fb36250e5db924b975a3afc8f9ee8534a439e7eff1b8bce0762(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplateJobs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d246fa2df3d1d2e3f9ee84209c93a27c27485bf5af0202671e76653d8eed6ff4(
    *,
    continue_on_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    logging_config: typing.Optional[typing.Union[DataprocWorkflowTemplateJobsPigJobLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    query_file_uri: typing.Optional[builtins.str] = None,
    query_list: typing.Optional[typing.Union[DataprocWorkflowTemplateJobsPigJobQueryListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
    script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e3f46064852264f395f34d3195f3c3267f3673b9f35a5ef584244ae598be7f7(
    *,
    driver_log_levels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a72415eddee1ce67f1864410184cc7fcc90f395895005d9480b561937772ac66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a30fa73b2389adb699429ca7ac6b36a3f7d1049d76389d883c076e3ee47ef841(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab8d57e4455a75706d07f84043663089c634df51e749291b000bb1344b2b150(
    value: typing.Optional[DataprocWorkflowTemplateJobsPigJobLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d3cecb366f26a903b9434dd8d912901c6271048100132950ffa527c63850c1e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__709624242e832269495c809571926fd53e32dd427f53eca4b387ed08259456ae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__895e270faf9720e5ae60b7e2db879834aee485853264ad326f016cb17769d667(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5169d836fbb6a47a76f940862bb743e62ca4871bbee9e1f1eef29758b7aa29f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7728a1d8581717494354ce5f9733b7b96d3a6c72f23036aff0a364b64de48651(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b92c813ae48f54b6915e27ec571ed27add20134b26d197f4b6778d5d884ae75a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0632df1daf907133d726fb62c1d1dc059c848f5e4f47b4a2b114e5faada9483a(
    value: typing.Optional[DataprocWorkflowTemplateJobsPigJob],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e7fb35447ec25bca10b10cd29def897ab680da505b7797ce58514a49e256d0(
    *,
    queries: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ec9dda42a5e0c4279745829d39cf9aa07dbc39ddf53133604e22d5d910e5823(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4a495bdb029a21c5a5ffd4efcda221584886e7301ed09657f20d03d460d16cf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97fcc008a8ddafe406c5049908086693be0b83a1bd5c8eb89bb18c53d6fe3fc2(
    value: typing.Optional[DataprocWorkflowTemplateJobsPigJobQueryListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03c5c7c3460f89d594225a5853097b340bd804f839c94b3990f54ab221eb0c18(
    *,
    client_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    continue_on_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    logging_config: typing.Optional[typing.Union[DataprocWorkflowTemplateJobsPrestoJobLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    output_format: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    query_file_uri: typing.Optional[builtins.str] = None,
    query_list: typing.Optional[typing.Union[DataprocWorkflowTemplateJobsPrestoJobQueryListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86493b92af14208f3ed21348de0cd9fafe0925dbb07da668c97a58cae4463eb6(
    *,
    driver_log_levels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b62f24de4aab44a82912b044abcd4763f42cb19ef4785822992424262de112d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7371cf999882470dcef470fd88fca58d4140133d404675e6499056b4ff2e5374(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f48ff54e3649aaf19c589ac4ca8d102d8d2983e82b5ba40d3f2ed52b606b584(
    value: typing.Optional[DataprocWorkflowTemplateJobsPrestoJobLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dffe6ab95d3bcc61e2e2b7ba2f7ec1416b74e513a960e02523f51d7b74613a84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a79e08a2dc7b4825bb02bdc2bc617d3b0b43109bf206b300efc75c96b20d26(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75125443181f87a79cfa8c1c63563dc294dbe7cd3fb6946bb3bdbc5eb7597675(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acc48cd95932b01b36c1eb1372d2804eaee0e35d2463f8d9afc5eea75efac37a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a93496507a0cb656330ebf092ae4469950d587731696a9c6d1be54a1c68ccff9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e315c8ea464ff00f083ecab149aad344515afda48355dde4cd2e00f3b88b2b61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fde21aff89d5c7025ad822808c34d9e79ba073c967fe1bb3ae58e519639dc1d9(
    value: typing.Optional[DataprocWorkflowTemplateJobsPrestoJob],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f22fcb1dd828c5046c366fb52d9fa5a54b8857761e7cc8fcd35ba9b4c735ebcf(
    *,
    queries: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__634ddc7d037c52825c7c2ef95152f6554c568fe1eed6c118043dbf8c56f219c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aea5a3ec8fe7b9596afb1c93b257c469530af000aecd88729bd416df7c6f3c2e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf3f3f1c7f53b6b3a3b69eca79fce4e2b3f825f0ec5110fa06ed2376ea9d8ef(
    value: typing.Optional[DataprocWorkflowTemplateJobsPrestoJobQueryListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e27f847c6a1e2a32ffb33b12df4bb4b902d4fe3624f36f5b5b1602639aeb9d6(
    *,
    main_python_file_uri: builtins.str,
    archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    logging_config: typing.Optional[typing.Union[DataprocWorkflowTemplateJobsPysparkJobLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    python_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b6eafad1e760e83c652beb434f25cca62cddc60c913384ff5f4880853c771a6(
    *,
    driver_log_levels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__396c67149c271e8220006e6c6a911567d4951968f27ca54084ac56ecdf66035c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d71f29374d009494e73cd8ce42e9d881825e69a99ee5c33935fb95f1bc24d62(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__234e3fcfdcae736ccc4dc7d7b8dd28bc0faecf23d0da54134528faf838cb458e(
    value: typing.Optional[DataprocWorkflowTemplateJobsPysparkJobLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2de970a25747733be1c91239c756e70efe11cb320ad5e8a81bd02985b0cc139(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae1326d4ac711cec314a4216374ffa7122b5c75b536e5144d7c78d554191d67e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb8442e1d942f1bee50c187f78bf6bdaac0e1061fee3f434fc12e2e05783f8c5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4be511ba1f217a10d8ea962c073b624219476ebdd76b5b1f4a31f9a47d16adbf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16cba5d1399821b992b6da0607b544109f023e18fb266de6bd39fcdfd3790eb6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19732f1002c5a97af0d1a24609cab151614a0cc7c457fbcdc9853adb19780a66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f959532d17220837ba95fa44375767e517bdb86be62ed247d663bdb54238d403(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc79695b8ff98424f21eaa921e2ad9a52396f2186adae7b187d40d3ef97f9a7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85dbfb002f20e5a4ceb0e0f188a43d049af3c93b67db7053008d2ba251bfd9bc(
    value: typing.Optional[DataprocWorkflowTemplateJobsPysparkJob],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__573546374997b26b384569f3a2c3e571c61d64d304af25ab42adaac2af5e79f9(
    *,
    max_failures_per_hour: typing.Optional[jsii.Number] = None,
    max_failures_total: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd1d68671a3b5d849133b690e68ed88f663652a48b5d710385b568d8da09284(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd461e51ec41b82db0533a98e4e50dfdfd6aab5e50ce2b6125872dcbd9553113(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6612d73e552de66a0f077a9c59c8bb690c34818e5ec6f25b7e27952b5725f2d2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bc267373857a021b5be798788dd03e0480f0838e57562997adb6bc0fe56c7a7(
    value: typing.Optional[DataprocWorkflowTemplateJobsScheduling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1688b4bf5eebec385b4216634bbdab24ee87e0a3325b0be9ad194ad78ccdf94(
    *,
    archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    logging_config: typing.Optional[typing.Union[DataprocWorkflowTemplateJobsSparkJobLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    main_class: typing.Optional[builtins.str] = None,
    main_jar_file_uri: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e0dd814cada24ac4be6bf95e663387c5bfb309e20981a6477585d61e929dd0a(
    *,
    driver_log_levels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__438a8f2d10491b888ef6aca3c1e2d3c66a521b119c690372fa96452593093d4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab8485b53f33dff774179e3b580ce602eef22695954098a54429241bc608f5fb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41664378fbec199ed18ce72e7f6e2b521bd73c3373aa8259f8430e273e4584ef(
    value: typing.Optional[DataprocWorkflowTemplateJobsSparkJobLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba608f333aa09b2e8b686009d01788e39464c97ba4feda24096858d4848401c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b867d7ae0f1270091479c0b179fb85327b0c79d64dbd01d610e10d7e29c9e662(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4e305dd7d2009b14e74af5a4e49191bc92db92a8a2ca69b629cc7d0d37af07b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d4a4eb1548c136eb50b2a711d0f93b3f0a505224c410e2cc8ff08cb4b72a9ec(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ab02762e7fb36720378b9f6c12eeda7f2dee954c8769bd4405234d204c67b2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cde973b152685e71eb5ec39391ad1c8acb679788af871b3902a2e2bd5378436(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d36d1d7a0208b5369a4900f330b971b3e3e7a25c1e34cb419b65f0f2325ef80e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8679cc6f307ffadb6bea9079014a69eac66b34ae02e31d33f4ce7cba38a9fdf3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e11d6bd41091343762c1be825a5f545a2857c3c512e6da6de439fc98e652d9(
    value: typing.Optional[DataprocWorkflowTemplateJobsSparkJob],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f98ba1085c9ffd8cc7435e6a284840fcd4c87b63e54480977b75c4e32c6ff5(
    *,
    main_r_file_uri: builtins.str,
    archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    logging_config: typing.Optional[typing.Union[DataprocWorkflowTemplateJobsSparkRJobLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74642c516bc70c6bdb1bb62bd56991d698215b3619d73919d9727416ac5ddffc(
    *,
    driver_log_levels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d3dd4e359e19ca9728d9afaf8d2d7e8c187f1b80330721a85da39e83e6f0872(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd0252e74bb20b5e0a4ac60ea401461c4813b80982322d69089bd976a275ec4c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__333123b3b9307ee06bc99222ba9d68f7e5e363c770bac269e2c7116e595432ee(
    value: typing.Optional[DataprocWorkflowTemplateJobsSparkRJobLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b3d33d6e67b151db5e000571d08abc0c0db69004222dc35b4913144018d1873(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e40d8d2930b2a196b9a1e570c2cbc96f886e701b3c9f909946a18cf75fe5680(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12e9c48268ecc9545bbfebaeafedf87f425f49ba6c0ccc8812807f24563a0d27(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fb2dbffb452b42554d8c823eb4c07bb9dd9cbe62a9918c0ae8b9a2356827f91(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4e2fca9f3be70a175a68d0ae0f1d6d647e4776fc93006273cc61b746fb3e8ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83716ec4ff9a6c9d7c48b683ba05aa8b41878e65dfc04ad5c947caf81a6509ff(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a2fcf07240fc8dbc9c0af9ecfc3fd31eea19e7c3a25f9db92edf2c499cac013(
    value: typing.Optional[DataprocWorkflowTemplateJobsSparkRJob],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd20e37b4f5d2fce4b18d8af05c3e36c5d9afbcf9b7e20c856602e113b844f40(
    *,
    jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    logging_config: typing.Optional[typing.Union[DataprocWorkflowTemplateJobsSparkSqlJobLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    query_file_uri: typing.Optional[builtins.str] = None,
    query_list: typing.Optional[typing.Union[DataprocWorkflowTemplateJobsSparkSqlJobQueryListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
    script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c076e3fc3e3187d9d3e9554b66020dd297ae52430d77db8acae1911bbb4c32b6(
    *,
    driver_log_levels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a0173c1c1e05a67c154c6a5a15e0f35fce4552f2f86c95a697bcd109c043342(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a071fd896094de051904487b2fe0fe605a3afdea9c9375ab6c782987f9bf4a4c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86f617f7c467ca723e667e8cbcfb2e7caf93c009d5d2a65ba6fd90538b2e4eea(
    value: typing.Optional[DataprocWorkflowTemplateJobsSparkSqlJobLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__657f9b6645fe732e5d5698b3d82b33bee8ee7cf524600d898dfb6e2a35ab60a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6040aac8ee6bff08baf0ac1ed3f38c88431f771137762869e616f50d7e560d5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__451df9286052fb703643e7ceec79c645941d833ac9ec53d48dc7bb223a0f8b3a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b7b6fa58214986a331d29dc40ba6fdb9d9c8165b27b6ed2edf6ae078f08f000(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7aaa40f452b1182305b8a60366929e7c97ab6e0207270649121cb76c4402846(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36db09b5e2997527266339ca5d0fe5a2aa7ed6f5f14fe3975ffdc1b0c9498822(
    value: typing.Optional[DataprocWorkflowTemplateJobsSparkSqlJob],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e2572365ece78ea1e64d330b2d7c8cb575a9b386bb4f6aafe3f41a094dae8e3(
    *,
    queries: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c475d84e589a7fe1d0e6e577f5812f8dd31a88d49604173597d5bccd7dc97521(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57bccdf78c306961816e28f1679129b9829e5d932e9a9a6fdb27d00e2eb3d868(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adbc533850c4372f5292d966b42d58498eeb45a230adb3d42d35336c3d4a0505(
    value: typing.Optional[DataprocWorkflowTemplateJobsSparkSqlJobQueryListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df619c94601b1bd82e27acb6dfbc36d6f5ecc83e6bf66b2a9ff3e2affb42ca92(
    *,
    fields: typing.Sequence[builtins.str],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    validation: typing.Optional[typing.Union[DataprocWorkflowTemplateParametersValidation, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db213347acc785ba21edeb7992e6e69bb45c1522caf0e78f04d7cae849a68979(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a96250d9a5faeb7090d01dcdef34b054537f3236f3972c4b5a3fd86c9cd7ad57(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c719b6cf1172e52d39e5ef234d331235283b319723d942fda948bc1ee7384ada(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b35cabd54f545fb453d8dd60679cf298001fe1a9db5d326d87a83175d46a668(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f27494add0073347c782656e63f91152a469f6c343797f3893d5b786d99403f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0796e7ab882938ded30b30ab73a383a54b7099767ae1eb24d8430dbd5d226555(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplateParameters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8643cd043ea796cf71f03f784733e52e39a8d43ccfd81176080e9f9da5c1ae7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__853f03eea58322c4613aa7b31557520d954e30b1f8e11eb808602d963881f71c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b874788ec2c35ad57b3f5afa605fa7dc61c8420ede84b29ace5f8e8f0ec1f95(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78c8d3fb41ab1395e47cb58581da4bbdfe6c3f7eb4ea4311e473b49ba591d3a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8edc3a3f93b2e2100d7e4d2bbcc110e35543454d09864d9e9356a2559910f62e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplateParameters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05a7915ac32fda101d8105e515a66e74c0f83be48c27cbfaf5dbc552e1deb2d(
    *,
    regex: typing.Optional[typing.Union[DataprocWorkflowTemplateParametersValidationRegex, typing.Dict[builtins.str, typing.Any]]] = None,
    values: typing.Optional[typing.Union[DataprocWorkflowTemplateParametersValidationValues, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42e1ed620b8377c90fce346f6adee60319a3e51676b0795935adc0146be88ee0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd9c29f854d3e069db36591402cd393d0ee31a32d378718d3912f0946acc7a0(
    value: typing.Optional[DataprocWorkflowTemplateParametersValidation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e83b18a6e75c4388993aee5931e294c71e520235ed3218892d3f859bebfa69(
    *,
    regexes: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10442fb4fd87c736b35ecd4eb05520abdbb3f7ccbabafd53d375420129d37b82(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbdc6d6ee9551913b9912890f7f7bea341782616a6f3a3041ffcb092f0d0b0cc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc07c5af2de16cc1889c87801264a77b9cb47db9a92c30006ffe9fddafb1fda4(
    value: typing.Optional[DataprocWorkflowTemplateParametersValidationRegex],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b72b1b19b8770f38bf228842ab3279ea113092463a15c89fdacfd814f2601a(
    *,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b04b521a595fd857db05e970da2b6cf75d4dcbf3389cfef05d39be29abecc9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a616213707bedb5d3973a8d306733e32f15dc12c096069362d928fe6bb6206(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb43706ef49074c31d381624c55ec5249ed0d5cdddf40e911048ce0fe7bbc7a(
    value: typing.Optional[DataprocWorkflowTemplateParametersValidationValues],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3f5b357371b44d183264e4f5f6bb16a59bdbc3d9835ecd221768b4465033ab5(
    *,
    cluster_selector: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementClusterSelector, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_cluster: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedCluster, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8df5e3246eccd593fed28d0937bb1b10628826dfac6452ce774aac75ccf6e154(
    *,
    cluster_labels: typing.Mapping[builtins.str, builtins.str],
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f6fb7218f052005beaac0f8f6de41640f806976bcd2d95270eee4288f70da33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f1ea51b7348e488969e57a573a352b8f4afbc7c7ff42e7790fe91de4e57b1a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3df2c2b907009d467cec4da39a5c7b34a393ab72f9f26764fa3cb57b268e5fa1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ddc81834e50b0a20488fc6998afca59ec5c1388784b0fc8f7c32e50d73d3ca0(
    value: typing.Optional[DataprocWorkflowTemplatePlacementClusterSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4963d5f162a64b2e6bad1b736fc6f22cfa0c125b40f38ca4af8a41f1e92c9fa2(
    *,
    cluster_name: builtins.str,
    config: typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfig, typing.Dict[builtins.str, typing.Any]],
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e997e314ca77040c63199bf3e146799df3ba159b3b88b7b820b13b98c41160(
    *,
    autoscaling_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigAutoscalingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    encryption_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoint_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigEndpointConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    gce_cluster_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    initialization_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    lifecycle_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigLifecycleConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    master_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    secondary_worker_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    security_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    software_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigSoftwareConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    staging_bucket: typing.Optional[builtins.str] = None,
    temp_bucket: typing.Optional[builtins.str] = None,
    worker_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d4cc3428d02607a48ddc80aa2d38a938b16f652a1516d81977eeb5b7419cd7(
    *,
    policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa85a0d833ef61d91ca33b06d6bc07499ef840004e815d1722a4df69fe6aaa9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72d0ee42e0a135bb56a137a194f84e826a8fc3ee7a418bafbf36987dc60fddbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b231ae6bb40dd5e756b52171f3f339109b3194eee87c1e412e0647c59711fe6(
    value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigAutoscalingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__115783f75de11ccb091fe724e99efba1dcc1bbde4d8e06e434853b2163608fbb(
    *,
    gce_pd_kms_key_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae7dee1401ff8e8aedb5d9c89b0d4fa3d4d92b454710838c6fd3856914d170cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e20ab0f3e8aaba5223d7e42b914c82b6ead00b497d06ba8b80c8c7626cbc7f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ded699f040a41d67a419b3f194df9225c5bc6d7553a38cd8f672e80f10c7e2d(
    value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigEncryptionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3a817c989f342827dff5864150be48ff0e4bee26f65d74a66d04de2199f7e2(
    *,
    enable_http_port_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bccaf9a034adf8182363467cfbd59b3d473efed64db62f2c86e353cf95a7dbc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a2d2446ef79b2352eda0fa12e4d97c988cda626f532b2f70e48a2d536776d5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2326c6c3975189f644c08c8fff2079d3a2c741515fcf210323c96d96509f82b1(
    value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigEndpointConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c313c02647fb89efcea66083e9684355cd67ce381fd1f80624a3fed756ed9ad(
    *,
    internal_ip_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    network: typing.Optional[builtins.str] = None,
    node_group_affinity: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigNodeGroupAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
    private_ipv6_google_access: typing.Optional[builtins.str] = None,
    reservation_affinity: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigReservationAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
    service_account: typing.Optional[builtins.str] = None,
    service_account_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    shielded_instance_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61428df75697a69d165ce0a0540d7ddbd3c87d7d7d5ee10fa59128ac91352dcd(
    *,
    node_group: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631b5f8b9805ebf3876fbaca621349b28d556ba3cc8fbec794630414fd39b365(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82e80561f42f2488af14790c6e2fe56e81f4cd89753a6d58867c030263c8a9db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9230d8ab0f759abac30dfbda8a516663268888eea33463ce8da994e08ba4b3a9(
    value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigNodeGroupAffinity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6243b61dcd890dcfeab4f7513a3f3bfba8d71b6321748f69c3afd72301ec52e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1e6417cf992b2bd24c21b4d46d2bb210c8b1ea14b52f8b3b2144795fbbc4ac4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b971782125968ac068544f5d0bf9e6428af58d371d62d59d23e7cbfff0e58a31(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eccb89e558aa649fb999129d05ed32188f0ba07c72bd8a2b4e3bd0bf8ee313af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3cbbf4b3e6106cd0a69bc3597dfb0782136946b3df9b0d587b85d6d77cccaf7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed0ac363d57a2a12d5835b3ea10711bf6eb636c61a5183c076e36b1fc9c016dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5807ec2835ea2b0400313d2bf52f2dba69615ce4f1b0e58767fb756f60d7f3f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fd1bfc2670e9578e2b037a3d8fc27c0b5deb9690d6b2c0f3ccdd592e30544f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a7790d3ce212e001ba5df312d49ef532b5b990f7a2f7937a6ce85f44a2f27a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__359064bef650801a8a9abf5a33b100eb353e07ddccab17d15e1e3a793b73a555(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c371d22b11e37ec967e1f87c6804745ae43013996f4fec4c73228bd9109fdcc(
    value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4fee7e038636a3210599c6a847ba654c9acab840480ec0852cfc2d4258e1298(
    *,
    consume_reservation_type: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f77d732d6478dc8ea1b3a24edb13c1fc23933021b18b90430e126390131500(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc91835498f28da4c7bfd40875106f0b5d284c61f8c77e0d2d41724c468b84b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__312d6f3f1dc2d6a7719ceb50bc7c56b1f501c7b2a8f4aaa70683514c78c32175(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3de14ad08bfc22e81534320a4079904a90c122cc00092af568caaa8ee55ba14a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79588976dfcb7560e062af0292c34d99dca5d7c9da971454cc3621f01e1b4899(
    value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigReservationAffinity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbfee862d33b60cf6e4b2ca1aecef2bf0eb85f14925a74d5aca790ff30c79894(
    *,
    enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bff2ea28f9b90883f339191892f3f7568277d1658a3432d0840c43cca175e8a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b8217d9cbbdac3430a6feeaa8545bae91727f95b0213e27b2241e2c4f24c96a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1e9ae740505e5b187b913311e3d87c6b92765834d83d31b1fb718621be0f5a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a52ad242aad035ea40205e3e3d5cbed8ede36e7df8cb7bc836bd66ba280515(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9786e0ad666f4e7f2c81ed7147f7bb2b3dad964d4a5803039ba73b2cf621f64(
    value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigGceClusterConfigShieldedInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec70abb13c4c28511c350bd64bfc0d6d1a18db161873cfebc5122d4d062505a6(
    *,
    executable_file: typing.Optional[builtins.str] = None,
    execution_timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b20fc3bcbda47bcbaed8dfb0c7f4f3fcd8f69cd695441b7595f2ff7522474bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab6176f3cf9a722823b763a31eb002df9daee0742ac02f6d9cb4dfbb7bdc740(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0abbb3a9072ee66d0d5c7b667ed40fbb3cf3233f6359b07d7dade46646e8375c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d95250058af8b64a86e9cb550e63eb64a6501d46806fdcff297187908c09c755(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c044d49ab98ec4c91a01c2359c9080e18fbe88d0ff54264ef3508c640049823f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae86f9ab962b85c1ba1cc622462c86f28f6755168ba5052df637a2e48e973334(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef7e80df590bc9b2b2e87723b36100c9d00ce7585ec4996cf15b4f794f340284(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f31446bce4d87812db67e83ef7cca4fef9301aea70dbfc4754b2dc34281c2b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2a40f825e45c5d2dc2a71723c2a23c30e6a1de86bd771815b1ca37195225241(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ace9220126cea92189d613392ddcbf1ea325d7132b7cc760246218d47b7076a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f3225a864a3460898c26aff121d46ad0d022fd7913f784d394ad4566870fcb5(
    *,
    auto_delete_time: typing.Optional[builtins.str] = None,
    auto_delete_ttl: typing.Optional[builtins.str] = None,
    idle_delete_ttl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b92e4577ba64f4d3fbe27193ea3378944208b926a953b67acf2e04157c2df94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__751dae482320b18fa4a1337cbfe4f968d898457f87958b6ab6987b4e12cf3c5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7abf5c14a00e5a75085570cd4d9059db73d75677eca3f9ff98ecac4ce3bd9a9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd59f5ac4a12f81262c0e87a8bbd9cc4325c86f66a61e20045a4e6a2103d811(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d102040cd6e69fc9c9b87a2092f74de4b514798f52acad275409da775443be(
    value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigLifecycleConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d861a64500cf3201d0cd5ac1211290ed0b7fe8831e83cf3f82592f96c05e335(
    *,
    accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
    disk_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigDiskConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    image: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    min_cpu_platform: typing.Optional[builtins.str] = None,
    num_instances: typing.Optional[jsii.Number] = None,
    preemptibility: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08a29aa389e6f97cff955327e704c020e4e216d36b102739e306b65d3d0aa980(
    *,
    accelerator_count: typing.Optional[jsii.Number] = None,
    accelerator_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f6c827b8bcb4a328c2eaae36ee2d6501de6a4661043764e2b0540a049676fad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__462405789289c74f29da03115c4049a7800bd46a7e9207a97bc44c27c070b601(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__041e3aa3caed2257061e4937541633091ee3347bc3a0d9798905047a3e4141a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb25dca68ab9a8bfcda11e0216875091db273d7259dc86c2869ff838a8735d02(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc5cf8b8fa588ac3bc1bed9502663b7948545a32d8d927771159604baa20dea(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__614f0e8499da3aded1818975d9fc0329b0cb259036252df0ec0f3f43bb7e68f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAccelerators]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0383b106adc1995b018857a27e17ccc8149cf0883240e71bdc23949d5dca674(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6460b6bfb76a8ea963c82f78a93c314fd8e4136d566631332195ee5ac3be104(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f9d751b3f3b2c1737516e3d38fc6d93b5a020aa99048c008c6f2f2d00779a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93e00e629f6fb5369e83112504175ab10eec83c5f1dd3573cb4d6bb0e01ea0d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAccelerators]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b224dcb65dd77665e628a2b17994f2e32d23bcb3650a7afea8c18db128e3f88(
    *,
    boot_disk_size_gb: typing.Optional[jsii.Number] = None,
    boot_disk_type: typing.Optional[builtins.str] = None,
    num_local_ssds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a29e14453e1d4375a06cc8bb6469682dd47f3187dd4fdf9893b05af3f80593f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d278512c7b0720e35530464f14d9a4276b1f18f5fe6bde00dc79c6b293f051ba(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39462ee36aee2314acf7b7dc69abd3b683f25a7ec386b01954d0bf1fc679920e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c4148188cbaa0c86b0bc1656ac2acdf535eb29103e449f0a236c1dbaf0da73(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccfc0a527a592466f10844deb1cff46c91d17eb8d2ca466e5a8569c2d9fa45cd(
    value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigDiskConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d942dc030b28887ef66f62d3b784337d889573063fe16fcc1215fe23f2f1ac41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631d19f42619e9de48f9230c12073e95b779b5fa0ba863e818bd73724ee8cecc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e8eb562df29c03bc7808c87b658c6a403201a8d2e1db0e94004ecd04673000b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__396c8d509da2ff9155ae702bceab77e0a425f18610764ca3553d0f2b4c33d73b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93380cc938ba1e499e056df27b9f88f33991199ea374318991a133d7b710d654(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e261868845ef3eee4544a69f993b2049460801f4a27d8336b90473043a4175(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6f32866110649253bbf32d729c52d8b0da9aee8c30dc016ec78cfac301f3cd7(
    value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigManagedGroupConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc057b0f331298aa05d2f8d9ab818c6a6286eb8fbfd4fd69fd8ab7fa0e40ad2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32c14d1aaa5e80edd6db9409315a08a350c479c95a45ca78e1bd530634a50a6f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__759c2b8e332279d9a965c3db9d6877d1365518c2cf755f0c8fafd28aef1762ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797aee0031ee759b50dc5bd2c1d069d9d176df626c1df79a67b7a12c5ba51a71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0a33f6ed1a4c815aed61b0a8ab2b95a93cc320e8ae7514a4b2814e4870f58a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e45d95f30e9c429d8eed5725fdbfe041d5e8fe5452b0ea90e929abfe565783a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__444d36afdced6ab6680d2da53813634230ff6e2089475f2ed2e640a64b50db78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__594c813b56ee26ff0cc0c3ed8054b37f25d4e2172f8798ebf39eb78a820251a2(
    value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigMasterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88054c718dc117ae1e31322e6eb5dd72dddce9639e4cb01e72442793f679b9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc6f8d5b328078083d23a699123c00bdc2402ff9700dc8d583d06207535a25a6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigInitializationActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e301e870ce72b6b876c30e2dbf6775ab92faff3b16b3f7562600dd93f44d01c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e2bfead03ce73a68fd1c3e02050d8164f0e0654944f5d7f9b638a8b2936241f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f7adbd4c601479eeda393001d512620987051a91e7dd062b4094fd3b7ff33b2(
    value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c00fe29f9abdc543d8f89e6154537d1100e78a9fb4b4b1fc867b59963c18c017(
    *,
    accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
    disk_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigDiskConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    image: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    min_cpu_platform: typing.Optional[builtins.str] = None,
    num_instances: typing.Optional[jsii.Number] = None,
    preemptibility: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f7b0f3ef0c859588d5ed283ad3c5ceea0df38cb92e70d20303d1dd65a365235(
    *,
    accelerator_count: typing.Optional[jsii.Number] = None,
    accelerator_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a57cacf23e54dc8558d8d585b9839e61666cb6a81cdc149fe47fc5a0d0819490(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__709964bb29a3826700fd4088f2ddbab785a3bc50412b3d697e387706d4eab744(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb0ce27ce23b142bb835f5adb754babdf938e2b3bf50f39d59421f9b2927b0a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2b7a71bd531a2022b5212b6aee5d9968836c8eca345fc5b0c0e846f59ed44b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b162d1c26aed25ed3cbcce019e815a0f8d5a1a94168149fcd273b550189cd7e3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37117b3a769e5622c6a71efaf65bd87d199e3ca1136690610368ca48b17749b8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAccelerators]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3d476e390595ef4ddb953fd03c8f35f40560655539edcad9e5b8030604d827e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ee736e169ff10aba57fb9840afcf8da96714fd8c1e349972445abb514f25a9c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1146d6939c1573dec88ec780a67077d840283d28a2cc2b659093c02f93e681f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0e29f2f35859a40b29d3c6fea5684a491f913944a1a601ceb5e3a28278c7353(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAccelerators]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__703bf1fcef40f226c50fd9373c337c3d3c5f38ad0e3f23de69c73ba3ffd881ef(
    *,
    boot_disk_size_gb: typing.Optional[jsii.Number] = None,
    boot_disk_type: typing.Optional[builtins.str] = None,
    num_local_ssds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__674b376b2917c9e7f47c3a3d732481310ee53de713f2dcf31b0a1f71a0df023e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b98519b03ec66f7268a585a22a5c550ae0366ad3463078a79906b22e4ec75a7b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa37fbee758c3a8e9fb969659bbf9aed01dd9c7bd784ff61e951265988fba6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f671df4286aeca45f4ffffcf5e8d9d0fe9582a708289dd00996b97de439a089(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d3b4154662e6af3b0c643d124b258603e48b4ec77c4b79ffcc4530f20171713(
    value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigDiskConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e30732efa713c08fd632b6557e91f1290bb2a096e70e323b8ec793014912875(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74d9b8882c730508214c639f6f768f0e85c657c9b7ef7be5c10abd49b2016a15(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecfcdf11d868252417a6070468df5bdb8bf100e1b4ceaa41a1c8568ae8a3eda8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edca7978175a67c3aa87bc8d138f82f90dd0b5013b184e63f201f147ba58bdb7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a2705880be7bcc3b8f3e5f4e359dd6b0727dbd53c18a6c43d70a22b83252dc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__269fa1ea01d192f8d617d6c342af2b1a6fb26d9c0f5450ae207856cc0dca8dfd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb2426e08ee339e7a0b8a1896b04998f3c842e896412bc9edce180e11162b6d(
    value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigManagedGroupConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc03c135191b3627280d737990d59a9cda1210a2fd63f18b3af82dca01edbd2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb755b3436efa91b836616821b16c0bbe3cf68ac2ad47d017d0cde291db366e3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388b191e3c7a415f9cf3596faebef7b5d9a0f099cb8049becf421d7ca23b9cc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c007d0fe996e9fc639b76a3818ab594c876dc5c27b5c9f29027a59520553d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__741e0aa3b8e1a99c96c1507a6efc306e85366320fd5db11c9c162555da1cd996(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f6a6edc7ef769eee0d7114ae5f16be0ac5fd5de3ca0f441bd27d7423a06d481(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bffa271b3af2dc0406326aba9321cee351285c4791e18d68ddb7f40e7c1d01ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9edd934f6b1b24e6827a41c5be06ba4fce413697a6865b5f8e84f29cd1ef3249(
    value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecondaryWorkerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__628f6e5e1b8af39595c48cd835f47fc136a34258b8a05ce26b1f24a565ea9f21(
    *,
    kerberos_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigKerberosConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__457e5bf7fe1dc1b5182e1a1e81b66bfde13540329d3b59bc336cd8021354608e(
    *,
    cross_realm_trust_admin_server: typing.Optional[builtins.str] = None,
    cross_realm_trust_kdc: typing.Optional[builtins.str] = None,
    cross_realm_trust_realm: typing.Optional[builtins.str] = None,
    cross_realm_trust_shared_password: typing.Optional[builtins.str] = None,
    enable_kerberos: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    kdc_db_key: typing.Optional[builtins.str] = None,
    key_password: typing.Optional[builtins.str] = None,
    keystore: typing.Optional[builtins.str] = None,
    keystore_password: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
    realm: typing.Optional[builtins.str] = None,
    root_principal_password: typing.Optional[builtins.str] = None,
    tgt_lifetime_hours: typing.Optional[jsii.Number] = None,
    truststore: typing.Optional[builtins.str] = None,
    truststore_password: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88835a49b3e95ce7c3fd1084fa3f97ac30c20ed6e941d13df29b7a92505517b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51bb8ce3c9d104daa70839df5fe37fa20e0aea79788c62068fc09b66439d7bb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__040fd558d346a4ecf841b2be5f4a94b9223f45a03625a74ddbf62a85dec96dad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ebe66891ddecb2377b8d20fbf6c041844b43c695c38224b8779816a4a12cb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__723e9bd8a32ecee7c24d02ed4a64a56ad4f4c50de955542f08d7dc427829d465(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20413b95c322fcfd3a175df6b2f34893b80b259bc646f208360ae048c5a88ae4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afb8cd340abbe1162e2ec3a1722cb5bc90b9185ad4a082718af83e477aa5c41b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4523e6b409f55db6146bc14ef6280eaa6f8fa71f9467cdcb999f3b7adaca314(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9f0f37c59df5aa3859f60b94c7b46b966b2dc21389fd66ad938817229ee24e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e872486fbba83cdf8f6cc815e2474002498b44ce578947f645d28847ef65771e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0643f76e1fde4d301b03d27b57cc1aa1e2c1f42ab5f92f757ad513afc6451231(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81507bec2ca02f660aa44bff4e7fec729327565624a366cd36825e4afbf42c3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e42b0c5996646a1731053b4ad6e2b711ff1779143ba5f0122b4464519495f20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__820334721ec724d9abbfa1c04ed9b1e608b0a263147f4591e8ddd7c248c82d6c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fbce1375227aaed11ce4f79ad91ec9dd45eb2dfd08c6de11a5c8eb52bd4edc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31338cb5a501ef6e4e6ca604e3e1b2526fc01e3804d115f68fd20160934d2648(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c79afd5e2bd0d6b67fb86872779ec10291ff680a9223fa760906e64ef475a735(
    value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfigKerberosConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2097e6f9f646278af06a9267172fc17e5ab2770bfdaf04630e80d4e21d7584f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fa14dbfac4be4e48a63a4eeb9d5f15bab0111c9f991c714e19b2dbdbaca5b8d(
    value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSecurityConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a7b63981dae2ee44362a706c3e00460c08f47305da6fc5ce312393147d2a67(
    *,
    image_version: typing.Optional[builtins.str] = None,
    optional_components: typing.Optional[typing.Sequence[builtins.str]] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c869331717948fdb011e0454935b4879093c9bc4d85551e3940b5097cf7a7789(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d47e10f249f6b26c7884f7d663274a8b1d54855d32f31612975ecfe07902a40b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b652a3702cb1a6d59a9da984ad9c6d3824e9b8deb32bb2d32305cc5f9a1eaa2e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0542084736348b3b16c8dc8d4e11ef8a8ae084a0030f1458cf561964145e1c0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2496cd1086e8d2e9dec4ea77d21babf0cc00b11e50288d30be1b3d236d9122e9(
    value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigSoftwareConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b23e9ff9c59eef8dd0d9c46f05ff55e167b38e40547abda83b20afbdf9b153(
    *,
    accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
    disk_config: typing.Optional[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigDiskConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    image: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    min_cpu_platform: typing.Optional[builtins.str] = None,
    num_instances: typing.Optional[jsii.Number] = None,
    preemptibility: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9fce16afa287b9285d81c474559c59186cbcbd37c510fad3f1a58054e39ee37(
    *,
    accelerator_count: typing.Optional[jsii.Number] = None,
    accelerator_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a04b523ff6a4f80d3b1899d059b06170800309a8d196eeab589bba86810673a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e014a309a0f2c43929aaef3cc00f4bb8b3e87d40fe02772026a1b0e7d984704(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e203ce42938a621a718af90ba33274329249692c4542251a663c348c24d774d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd895fb858b05c48f304f54c129da9f8744fae948ea9560ac7931c01a255a626(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5773a07342fc214280f91a9c1dde8b19c5175dafe3cc6821ba36a287f558b90c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80b94e6aab7a14f76a71a645f5b323f2998c5f77b39a91d726a002272e4045bf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAccelerators]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e628cf0dbcc44b2a0bbe045ce0f1337f3be8b9ade6873f5478bc011056bcda7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81a7d371c2fe83f3a126580df01cf221e0f5893b03f1eb43d42b307e1088ef3a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de0a0143951b78698b0c687f1810e2dd2ed7ed3356b088c5d76b0b3a9857b777(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a2fe541d881146cea222b494b3953c2cf3290dadfb35fc91d38b7e3eac3026d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAccelerators]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c684606c53202c61009e5ef18f1f9856d3236c830871cd508c7dea719d79de(
    *,
    boot_disk_size_gb: typing.Optional[jsii.Number] = None,
    boot_disk_type: typing.Optional[builtins.str] = None,
    num_local_ssds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffe2644414d085f93615f348cef10ab316050a97b6b2a74fa7b8b1d389ab0250(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d77044befb73ea2f61602820d2977b2afae2b5f480f67c675512f5a19361b7db(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b0a1cfb66889d088dfcc3a41501a4dbf48a3a4f3624ee7ec6e016fa5e0c543(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62bc6f8dc256d96f9c26b24b1f5d694c38ede01d20ddc82b2cc44ef8875c799f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eee1cfc07af0fa430fc61f73324ea1a45782c9365ddb024f814f87b415af854(
    value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigDiskConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c91cd8f51934956f2f8267e65dda3cfd56fc59933fd71a099e841b26d94c4af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21746934340ac258a4a72b7dd6168be8af7cae4fa9add4a0b6a54f9cbb2c6ed5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__097dc1d6184e00e4fa467982937c7da29fa6b349d7467a510a62f0dfbb547c60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e32d37a0f61c489e4eee7bdbc55bf73f6bd8cde9baefba4aa2d1f683accf3b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e85e2fe53f287864e3f1f19745355ec74e79c2b2f8bf6db985b9f5deb910c2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906e41d05208fb9f473343c83597dbe5f1fb5428b2facaa1859679b81e046215(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c91671b142497e0e9e4384294ec0616ad5489594031735114abf9af0d9d9091(
    value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigManagedGroupConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99b0c07763ecc66d6629a075805a0517df78ec5bba178fab136f3a672774045d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__780977930c6e44a70c97b0b6295f518c840152b2d8a1c71c13d3fb18cb57e4a7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b238422558e3c28576421616554c5b010d1586127613fbabea8f4b9bc09e5ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__612eaf2684c86c869eb59ddd8fda11e9d419ec1e9444a9d6fc2f5276ef3da0c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fece6ebcc3fb028e2ced195cb32432271c86f2c3949f5f5c6de3c035944d2a18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def67c72b9d3ac53cd049c0519bb91572d435a84c882dcc9f01c33f3bbbf2bac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480d5c790faa49b98163dc516467244d97102abd385e5b121a79ae8423c1a0d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2511fb284e25fb6a1f73fa37c6dcdfba21157c3a03090c322c58fbb3e7391495(
    value: typing.Optional[DataprocWorkflowTemplatePlacementManagedClusterConfigWorkerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4625626c4e3b090e80bf89da2cd01174924b18759b907b99e9d99a09fda1530(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e901edd7b10b681e2ce82df77500301427e49f773212c21520bfe4e97ee2ee0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffb54874e62c78cdf3a4606bbbe27ba6e04ef8c333e517114446d0f1f30333ba(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab3d63ca3c5eb5a1c826d2aa812d574de374581137c3a2004da5ba8848516e5e(
    value: typing.Optional[DataprocWorkflowTemplatePlacementManagedCluster],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9921a33f2f6b52bb44662ef7d327aef5b4d998608b7a40f2f4e97bf4d1f46c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b94969ba8688393c5e6a9e6189078426e4eb9d2fff62176648662051e3da3c7(
    value: typing.Optional[DataprocWorkflowTemplatePlacement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__460de6c7e0f8a64d50a58c4bd6ecb3c084ba2846494a6cbbd351e88145cf047f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbefc1f4149e43537e30319053da2c9615974e1a7de20d8168f60cb0619f7a9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ff9de513ad75a93302eb7a4283dab6e53da0be5262c2a476bd33b01e57920b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b225d8d5ced29ddfd8709ddef78c587aedf937842765d5d081aeecd64cf4342(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967944da9e068b696ac01fc3f03faca71a0a3cfc42477a98ac5db4e727cbd598(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04670f17a941cda992e00d8d159b07d49b148f3fe05361ed19c4209b2a895e33(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocWorkflowTemplateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
