r'''
# `aws_sagemaker_data_quality_job_definition`

Refer to the Terraform Registry for docs: [`aws_sagemaker_data_quality_job_definition`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition).
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


class SagemakerDataQualityJobDefinition(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinition",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition aws_sagemaker_data_quality_job_definition}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        data_quality_app_specification: typing.Union["SagemakerDataQualityJobDefinitionDataQualityAppSpecification", typing.Dict[builtins.str, typing.Any]],
        data_quality_job_input: typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobInput", typing.Dict[builtins.str, typing.Any]],
        data_quality_job_output_config: typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig", typing.Dict[builtins.str, typing.Any]],
        job_resources: typing.Union["SagemakerDataQualityJobDefinitionJobResources", typing.Dict[builtins.str, typing.Any]],
        role_arn: builtins.str,
        data_quality_baseline_config: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityBaselineConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        network_config: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        stopping_condition: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionStoppingCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition aws_sagemaker_data_quality_job_definition} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_quality_app_specification: data_quality_app_specification block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_app_specification SagemakerDataQualityJobDefinition#data_quality_app_specification}
        :param data_quality_job_input: data_quality_job_input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_job_input SagemakerDataQualityJobDefinition#data_quality_job_input}
        :param data_quality_job_output_config: data_quality_job_output_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_job_output_config SagemakerDataQualityJobDefinition#data_quality_job_output_config}
        :param job_resources: job_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#job_resources SagemakerDataQualityJobDefinition#job_resources}
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#role_arn SagemakerDataQualityJobDefinition#role_arn}.
        :param data_quality_baseline_config: data_quality_baseline_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_baseline_config SagemakerDataQualityJobDefinition#data_quality_baseline_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#id SagemakerDataQualityJobDefinition#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#name SagemakerDataQualityJobDefinition#name}.
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#network_config SagemakerDataQualityJobDefinition#network_config}
        :param stopping_condition: stopping_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#stopping_condition SagemakerDataQualityJobDefinition#stopping_condition}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#tags SagemakerDataQualityJobDefinition#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#tags_all SagemakerDataQualityJobDefinition#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6775f129c3139679cf62ade89df0d84ae7473fcd265d328c9c85b4dadd876db0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SagemakerDataQualityJobDefinitionConfig(
            data_quality_app_specification=data_quality_app_specification,
            data_quality_job_input=data_quality_job_input,
            data_quality_job_output_config=data_quality_job_output_config,
            job_resources=job_resources,
            role_arn=role_arn,
            data_quality_baseline_config=data_quality_baseline_config,
            id=id,
            name=name,
            network_config=network_config,
            stopping_condition=stopping_condition,
            tags=tags,
            tags_all=tags_all,
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
        '''Generates CDKTF code for importing a SagemakerDataQualityJobDefinition resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SagemakerDataQualityJobDefinition to import.
        :param import_from_id: The id of the existing SagemakerDataQualityJobDefinition that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SagemakerDataQualityJobDefinition to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41dfd7babdbaa10c5b55052271654a39ed0b85472438f5ab103a126804c089c5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDataQualityAppSpecification")
    def put_data_quality_app_specification(
        self,
        *,
        image_uri: builtins.str,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        post_analytics_processor_source_uri: typing.Optional[builtins.str] = None,
        record_preprocessor_source_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#image_uri SagemakerDataQualityJobDefinition#image_uri}.
        :param environment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#environment SagemakerDataQualityJobDefinition#environment}.
        :param post_analytics_processor_source_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#post_analytics_processor_source_uri SagemakerDataQualityJobDefinition#post_analytics_processor_source_uri}.
        :param record_preprocessor_source_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#record_preprocessor_source_uri SagemakerDataQualityJobDefinition#record_preprocessor_source_uri}.
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityAppSpecification(
            image_uri=image_uri,
            environment=environment,
            post_analytics_processor_source_uri=post_analytics_processor_source_uri,
            record_preprocessor_source_uri=record_preprocessor_source_uri,
        )

        return typing.cast(None, jsii.invoke(self, "putDataQualityAppSpecification", [value]))

    @jsii.member(jsii_name="putDataQualityBaselineConfig")
    def put_data_quality_baseline_config(
        self,
        *,
        constraints_resource: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource", typing.Dict[builtins.str, typing.Any]]] = None,
        statistics_resource: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param constraints_resource: constraints_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#constraints_resource SagemakerDataQualityJobDefinition#constraints_resource}
        :param statistics_resource: statistics_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#statistics_resource SagemakerDataQualityJobDefinition#statistics_resource}
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityBaselineConfig(
            constraints_resource=constraints_resource,
            statistics_resource=statistics_resource,
        )

        return typing.cast(None, jsii.invoke(self, "putDataQualityBaselineConfig", [value]))

    @jsii.member(jsii_name="putDataQualityJobInput")
    def put_data_quality_job_input(
        self,
        *,
        batch_transform_input: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_input: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param batch_transform_input: batch_transform_input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#batch_transform_input SagemakerDataQualityJobDefinition#batch_transform_input}
        :param endpoint_input: endpoint_input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#endpoint_input SagemakerDataQualityJobDefinition#endpoint_input}
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityJobInput(
            batch_transform_input=batch_transform_input, endpoint_input=endpoint_input
        )

        return typing.cast(None, jsii.invoke(self, "putDataQualityJobInput", [value]))

    @jsii.member(jsii_name="putDataQualityJobOutputConfig")
    def put_data_quality_job_output_config(
        self,
        *,
        monitoring_outputs: typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs", typing.Dict[builtins.str, typing.Any]],
        kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param monitoring_outputs: monitoring_outputs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#monitoring_outputs SagemakerDataQualityJobDefinition#monitoring_outputs}
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#kms_key_id SagemakerDataQualityJobDefinition#kms_key_id}.
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig(
            monitoring_outputs=monitoring_outputs, kms_key_id=kms_key_id
        )

        return typing.cast(None, jsii.invoke(self, "putDataQualityJobOutputConfig", [value]))

    @jsii.member(jsii_name="putJobResources")
    def put_job_resources(
        self,
        *,
        cluster_config: typing.Union["SagemakerDataQualityJobDefinitionJobResourcesClusterConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param cluster_config: cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#cluster_config SagemakerDataQualityJobDefinition#cluster_config}
        '''
        value = SagemakerDataQualityJobDefinitionJobResources(
            cluster_config=cluster_config
        )

        return typing.cast(None, jsii.invoke(self, "putJobResources", [value]))

    @jsii.member(jsii_name="putNetworkConfig")
    def put_network_config(
        self,
        *,
        enable_inter_container_traffic_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_network_isolation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vpc_config: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enable_inter_container_traffic_encryption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#enable_inter_container_traffic_encryption SagemakerDataQualityJobDefinition#enable_inter_container_traffic_encryption}.
        :param enable_network_isolation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#enable_network_isolation SagemakerDataQualityJobDefinition#enable_network_isolation}.
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#vpc_config SagemakerDataQualityJobDefinition#vpc_config}
        '''
        value = SagemakerDataQualityJobDefinitionNetworkConfig(
            enable_inter_container_traffic_encryption=enable_inter_container_traffic_encryption,
            enable_network_isolation=enable_network_isolation,
            vpc_config=vpc_config,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfig", [value]))

    @jsii.member(jsii_name="putStoppingCondition")
    def put_stopping_condition(
        self,
        *,
        max_runtime_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_runtime_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#max_runtime_in_seconds SagemakerDataQualityJobDefinition#max_runtime_in_seconds}.
        '''
        value = SagemakerDataQualityJobDefinitionStoppingCondition(
            max_runtime_in_seconds=max_runtime_in_seconds
        )

        return typing.cast(None, jsii.invoke(self, "putStoppingCondition", [value]))

    @jsii.member(jsii_name="resetDataQualityBaselineConfig")
    def reset_data_quality_baseline_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataQualityBaselineConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNetworkConfig")
    def reset_network_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConfig", []))

    @jsii.member(jsii_name="resetStoppingCondition")
    def reset_stopping_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStoppingCondition", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="dataQualityAppSpecification")
    def data_quality_app_specification(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityAppSpecificationOutputReference":
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityAppSpecificationOutputReference", jsii.get(self, "dataQualityAppSpecification"))

    @builtins.property
    @jsii.member(jsii_name="dataQualityBaselineConfig")
    def data_quality_baseline_config(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityBaselineConfigOutputReference":
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityBaselineConfigOutputReference", jsii.get(self, "dataQualityBaselineConfig"))

    @builtins.property
    @jsii.member(jsii_name="dataQualityJobInput")
    def data_quality_job_input(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityJobInputOutputReference":
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityJobInputOutputReference", jsii.get(self, "dataQualityJobInput"))

    @builtins.property
    @jsii.member(jsii_name="dataQualityJobOutputConfig")
    def data_quality_job_output_config(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigOutputReference":
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigOutputReference", jsii.get(self, "dataQualityJobOutputConfig"))

    @builtins.property
    @jsii.member(jsii_name="jobResources")
    def job_resources(
        self,
    ) -> "SagemakerDataQualityJobDefinitionJobResourcesOutputReference":
        return typing.cast("SagemakerDataQualityJobDefinitionJobResourcesOutputReference", jsii.get(self, "jobResources"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(
        self,
    ) -> "SagemakerDataQualityJobDefinitionNetworkConfigOutputReference":
        return typing.cast("SagemakerDataQualityJobDefinitionNetworkConfigOutputReference", jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="stoppingCondition")
    def stopping_condition(
        self,
    ) -> "SagemakerDataQualityJobDefinitionStoppingConditionOutputReference":
        return typing.cast("SagemakerDataQualityJobDefinitionStoppingConditionOutputReference", jsii.get(self, "stoppingCondition"))

    @builtins.property
    @jsii.member(jsii_name="dataQualityAppSpecificationInput")
    def data_quality_app_specification_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityAppSpecification"]:
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityAppSpecification"], jsii.get(self, "dataQualityAppSpecificationInput"))

    @builtins.property
    @jsii.member(jsii_name="dataQualityBaselineConfigInput")
    def data_quality_baseline_config_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityBaselineConfig"]:
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityBaselineConfig"], jsii.get(self, "dataQualityBaselineConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="dataQualityJobInputInput")
    def data_quality_job_input_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobInput"]:
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobInput"], jsii.get(self, "dataQualityJobInputInput"))

    @builtins.property
    @jsii.member(jsii_name="dataQualityJobOutputConfigInput")
    def data_quality_job_output_config_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig"]:
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig"], jsii.get(self, "dataQualityJobOutputConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="jobResourcesInput")
    def job_resources_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionJobResources"]:
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionJobResources"], jsii.get(self, "jobResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigInput")
    def network_config_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionNetworkConfig"]:
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionNetworkConfig"], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="stoppingConditionInput")
    def stopping_condition_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionStoppingCondition"]:
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionStoppingCondition"], jsii.get(self, "stoppingConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bda65a834d68df3576c96100e964f072b0b8dd9fcfc82977d77d22e0c25aa58d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62e862b6d59b95809aa9f4f953f95e9a292a9c5bae72e38fbf66d2c90467cb3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b386a88bac4df7422e41bc8610fb3f023b628d1d9339ac960a24fe5c4ab56185)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22b2d1695a819c1b8839f0c77c1a70d73a34ad94bbc8721a05abdd5fc3491bd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7024c8cfe8154b3b9bc8c870f9c408dc0cec4e440101fa63329859819313aeae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "data_quality_app_specification": "dataQualityAppSpecification",
        "data_quality_job_input": "dataQualityJobInput",
        "data_quality_job_output_config": "dataQualityJobOutputConfig",
        "job_resources": "jobResources",
        "role_arn": "roleArn",
        "data_quality_baseline_config": "dataQualityBaselineConfig",
        "id": "id",
        "name": "name",
        "network_config": "networkConfig",
        "stopping_condition": "stoppingCondition",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class SagemakerDataQualityJobDefinitionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        data_quality_app_specification: typing.Union["SagemakerDataQualityJobDefinitionDataQualityAppSpecification", typing.Dict[builtins.str, typing.Any]],
        data_quality_job_input: typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobInput", typing.Dict[builtins.str, typing.Any]],
        data_quality_job_output_config: typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig", typing.Dict[builtins.str, typing.Any]],
        job_resources: typing.Union["SagemakerDataQualityJobDefinitionJobResources", typing.Dict[builtins.str, typing.Any]],
        role_arn: builtins.str,
        data_quality_baseline_config: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityBaselineConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        network_config: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        stopping_condition: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionStoppingCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param data_quality_app_specification: data_quality_app_specification block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_app_specification SagemakerDataQualityJobDefinition#data_quality_app_specification}
        :param data_quality_job_input: data_quality_job_input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_job_input SagemakerDataQualityJobDefinition#data_quality_job_input}
        :param data_quality_job_output_config: data_quality_job_output_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_job_output_config SagemakerDataQualityJobDefinition#data_quality_job_output_config}
        :param job_resources: job_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#job_resources SagemakerDataQualityJobDefinition#job_resources}
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#role_arn SagemakerDataQualityJobDefinition#role_arn}.
        :param data_quality_baseline_config: data_quality_baseline_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_baseline_config SagemakerDataQualityJobDefinition#data_quality_baseline_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#id SagemakerDataQualityJobDefinition#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#name SagemakerDataQualityJobDefinition#name}.
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#network_config SagemakerDataQualityJobDefinition#network_config}
        :param stopping_condition: stopping_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#stopping_condition SagemakerDataQualityJobDefinition#stopping_condition}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#tags SagemakerDataQualityJobDefinition#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#tags_all SagemakerDataQualityJobDefinition#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(data_quality_app_specification, dict):
            data_quality_app_specification = SagemakerDataQualityJobDefinitionDataQualityAppSpecification(**data_quality_app_specification)
        if isinstance(data_quality_job_input, dict):
            data_quality_job_input = SagemakerDataQualityJobDefinitionDataQualityJobInput(**data_quality_job_input)
        if isinstance(data_quality_job_output_config, dict):
            data_quality_job_output_config = SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig(**data_quality_job_output_config)
        if isinstance(job_resources, dict):
            job_resources = SagemakerDataQualityJobDefinitionJobResources(**job_resources)
        if isinstance(data_quality_baseline_config, dict):
            data_quality_baseline_config = SagemakerDataQualityJobDefinitionDataQualityBaselineConfig(**data_quality_baseline_config)
        if isinstance(network_config, dict):
            network_config = SagemakerDataQualityJobDefinitionNetworkConfig(**network_config)
        if isinstance(stopping_condition, dict):
            stopping_condition = SagemakerDataQualityJobDefinitionStoppingCondition(**stopping_condition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74b6a0a1dc77bc32bc67f1c84f0f1866ee7115be14def3d541476133afd7c0bd)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument data_quality_app_specification", value=data_quality_app_specification, expected_type=type_hints["data_quality_app_specification"])
            check_type(argname="argument data_quality_job_input", value=data_quality_job_input, expected_type=type_hints["data_quality_job_input"])
            check_type(argname="argument data_quality_job_output_config", value=data_quality_job_output_config, expected_type=type_hints["data_quality_job_output_config"])
            check_type(argname="argument job_resources", value=job_resources, expected_type=type_hints["job_resources"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument data_quality_baseline_config", value=data_quality_baseline_config, expected_type=type_hints["data_quality_baseline_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_config", value=network_config, expected_type=type_hints["network_config"])
            check_type(argname="argument stopping_condition", value=stopping_condition, expected_type=type_hints["stopping_condition"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_quality_app_specification": data_quality_app_specification,
            "data_quality_job_input": data_quality_job_input,
            "data_quality_job_output_config": data_quality_job_output_config,
            "job_resources": job_resources,
            "role_arn": role_arn,
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
        if data_quality_baseline_config is not None:
            self._values["data_quality_baseline_config"] = data_quality_baseline_config
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name
        if network_config is not None:
            self._values["network_config"] = network_config
        if stopping_condition is not None:
            self._values["stopping_condition"] = stopping_condition
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all

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
    def data_quality_app_specification(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityAppSpecification":
        '''data_quality_app_specification block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_app_specification SagemakerDataQualityJobDefinition#data_quality_app_specification}
        '''
        result = self._values.get("data_quality_app_specification")
        assert result is not None, "Required property 'data_quality_app_specification' is missing"
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityAppSpecification", result)

    @builtins.property
    def data_quality_job_input(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityJobInput":
        '''data_quality_job_input block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_job_input SagemakerDataQualityJobDefinition#data_quality_job_input}
        '''
        result = self._values.get("data_quality_job_input")
        assert result is not None, "Required property 'data_quality_job_input' is missing"
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityJobInput", result)

    @builtins.property
    def data_quality_job_output_config(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig":
        '''data_quality_job_output_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_job_output_config SagemakerDataQualityJobDefinition#data_quality_job_output_config}
        '''
        result = self._values.get("data_quality_job_output_config")
        assert result is not None, "Required property 'data_quality_job_output_config' is missing"
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig", result)

    @builtins.property
    def job_resources(self) -> "SagemakerDataQualityJobDefinitionJobResources":
        '''job_resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#job_resources SagemakerDataQualityJobDefinition#job_resources}
        '''
        result = self._values.get("job_resources")
        assert result is not None, "Required property 'job_resources' is missing"
        return typing.cast("SagemakerDataQualityJobDefinitionJobResources", result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#role_arn SagemakerDataQualityJobDefinition#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_quality_baseline_config(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityBaselineConfig"]:
        '''data_quality_baseline_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_baseline_config SagemakerDataQualityJobDefinition#data_quality_baseline_config}
        '''
        result = self._values.get("data_quality_baseline_config")
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityBaselineConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#id SagemakerDataQualityJobDefinition#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#name SagemakerDataQualityJobDefinition#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_config(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionNetworkConfig"]:
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#network_config SagemakerDataQualityJobDefinition#network_config}
        '''
        result = self._values.get("network_config")
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionNetworkConfig"], result)

    @builtins.property
    def stopping_condition(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionStoppingCondition"]:
        '''stopping_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#stopping_condition SagemakerDataQualityJobDefinition#stopping_condition}
        '''
        result = self._values.get("stopping_condition")
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionStoppingCondition"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#tags SagemakerDataQualityJobDefinition#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#tags_all SagemakerDataQualityJobDefinition#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityAppSpecification",
    jsii_struct_bases=[],
    name_mapping={
        "image_uri": "imageUri",
        "environment": "environment",
        "post_analytics_processor_source_uri": "postAnalyticsProcessorSourceUri",
        "record_preprocessor_source_uri": "recordPreprocessorSourceUri",
    },
)
class SagemakerDataQualityJobDefinitionDataQualityAppSpecification:
    def __init__(
        self,
        *,
        image_uri: builtins.str,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        post_analytics_processor_source_uri: typing.Optional[builtins.str] = None,
        record_preprocessor_source_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#image_uri SagemakerDataQualityJobDefinition#image_uri}.
        :param environment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#environment SagemakerDataQualityJobDefinition#environment}.
        :param post_analytics_processor_source_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#post_analytics_processor_source_uri SagemakerDataQualityJobDefinition#post_analytics_processor_source_uri}.
        :param record_preprocessor_source_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#record_preprocessor_source_uri SagemakerDataQualityJobDefinition#record_preprocessor_source_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33271098954b556f4acde17bbd57afa7ee9cfaf5a2d271e7f781b89877c12c12)
            check_type(argname="argument image_uri", value=image_uri, expected_type=type_hints["image_uri"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument post_analytics_processor_source_uri", value=post_analytics_processor_source_uri, expected_type=type_hints["post_analytics_processor_source_uri"])
            check_type(argname="argument record_preprocessor_source_uri", value=record_preprocessor_source_uri, expected_type=type_hints["record_preprocessor_source_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_uri": image_uri,
        }
        if environment is not None:
            self._values["environment"] = environment
        if post_analytics_processor_source_uri is not None:
            self._values["post_analytics_processor_source_uri"] = post_analytics_processor_source_uri
        if record_preprocessor_source_uri is not None:
            self._values["record_preprocessor_source_uri"] = record_preprocessor_source_uri

    @builtins.property
    def image_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#image_uri SagemakerDataQualityJobDefinition#image_uri}.'''
        result = self._values.get("image_uri")
        assert result is not None, "Required property 'image_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#environment SagemakerDataQualityJobDefinition#environment}.'''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def post_analytics_processor_source_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#post_analytics_processor_source_uri SagemakerDataQualityJobDefinition#post_analytics_processor_source_uri}.'''
        result = self._values.get("post_analytics_processor_source_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def record_preprocessor_source_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#record_preprocessor_source_uri SagemakerDataQualityJobDefinition#record_preprocessor_source_uri}.'''
        result = self._values.get("record_preprocessor_source_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityAppSpecification(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionDataQualityAppSpecificationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityAppSpecificationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7669f779938ef7d2f1c68bb9b5ea40b08fb2f0bcfff2668625a8495677465a34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnvironment")
    def reset_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironment", []))

    @jsii.member(jsii_name="resetPostAnalyticsProcessorSourceUri")
    def reset_post_analytics_processor_source_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostAnalyticsProcessorSourceUri", []))

    @jsii.member(jsii_name="resetRecordPreprocessorSourceUri")
    def reset_record_preprocessor_source_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecordPreprocessorSourceUri", []))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="imageUriInput")
    def image_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageUriInput"))

    @builtins.property
    @jsii.member(jsii_name="postAnalyticsProcessorSourceUriInput")
    def post_analytics_processor_source_uri_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postAnalyticsProcessorSourceUriInput"))

    @builtins.property
    @jsii.member(jsii_name="recordPreprocessorSourceUriInput")
    def record_preprocessor_source_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordPreprocessorSourceUriInput"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "environment"))

    @environment.setter
    def environment(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__044a8a9eac1c60ad63fd5caa7fe5f0fa2f476b0654f707009a36409164232192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageUri")
    def image_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageUri"))

    @image_uri.setter
    def image_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb95664fd1d428a11b14614abc5c4d87e0d599c77c188cba00ca11f0583205af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postAnalyticsProcessorSourceUri")
    def post_analytics_processor_source_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postAnalyticsProcessorSourceUri"))

    @post_analytics_processor_source_uri.setter
    def post_analytics_processor_source_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e986f5b62f2ab4439992f3b12b14844d262cc4e7c25ced48f022f5507eed9539)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postAnalyticsProcessorSourceUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recordPreprocessorSourceUri")
    def record_preprocessor_source_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordPreprocessorSourceUri"))

    @record_preprocessor_source_uri.setter
    def record_preprocessor_source_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70c4737c816afdcc1e669e7e88701436a90ffe5be1c5d00f64bd71067e58f6b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordPreprocessorSourceUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityAppSpecification]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityAppSpecification], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityAppSpecification],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb957deb6cb929f4844baf18031ef43422eb16d15a489162fe8ba3560e4ac41e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityBaselineConfig",
    jsii_struct_bases=[],
    name_mapping={
        "constraints_resource": "constraintsResource",
        "statistics_resource": "statisticsResource",
    },
)
class SagemakerDataQualityJobDefinitionDataQualityBaselineConfig:
    def __init__(
        self,
        *,
        constraints_resource: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource", typing.Dict[builtins.str, typing.Any]]] = None,
        statistics_resource: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param constraints_resource: constraints_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#constraints_resource SagemakerDataQualityJobDefinition#constraints_resource}
        :param statistics_resource: statistics_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#statistics_resource SagemakerDataQualityJobDefinition#statistics_resource}
        '''
        if isinstance(constraints_resource, dict):
            constraints_resource = SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource(**constraints_resource)
        if isinstance(statistics_resource, dict):
            statistics_resource = SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource(**statistics_resource)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de15957fc62f32427e325123a895a96f1b76d25e8522d988e623acde62921a31)
            check_type(argname="argument constraints_resource", value=constraints_resource, expected_type=type_hints["constraints_resource"])
            check_type(argname="argument statistics_resource", value=statistics_resource, expected_type=type_hints["statistics_resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if constraints_resource is not None:
            self._values["constraints_resource"] = constraints_resource
        if statistics_resource is not None:
            self._values["statistics_resource"] = statistics_resource

    @builtins.property
    def constraints_resource(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource"]:
        '''constraints_resource block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#constraints_resource SagemakerDataQualityJobDefinition#constraints_resource}
        '''
        result = self._values.get("constraints_resource")
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource"], result)

    @builtins.property
    def statistics_resource(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource"]:
        '''statistics_resource block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#statistics_resource SagemakerDataQualityJobDefinition#statistics_resource}
        '''
        result = self._values.get("statistics_resource")
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityBaselineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource",
    jsii_struct_bases=[],
    name_mapping={"s3_uri": "s3Uri"},
)
class SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource:
    def __init__(self, *, s3_uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_uri SagemakerDataQualityJobDefinition#s3_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94c7360c077f02b21a1ae57f62773934d4881f5d08d992ca44cac86316dd445f)
            check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if s3_uri is not None:
            self._values["s3_uri"] = s3_uri

    @builtins.property
    def s3_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_uri SagemakerDataQualityJobDefinition#s3_uri}.'''
        result = self._values.get("s3_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3ca1d6e754e9554797c0b4b75931f7953104983c8faeb2bb8097b378555922b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetS3Uri")
    def reset_s3_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Uri", []))

    @builtins.property
    @jsii.member(jsii_name="s3UriInput")
    def s3_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3UriInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Uri")
    def s3_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Uri"))

    @s3_uri.setter
    def s3_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__816d77cdfcc408e3b941b31f85433a57b13239a2b1f1b99ca5ab91696fc17ea9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba9698ff8c8ac983ab72d307a6aaaadaa0c9c2d1a4c9923a38470e0b3d978f9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerDataQualityJobDefinitionDataQualityBaselineConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityBaselineConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19a92a3397817d024b4e26a1ce46a83e90d39c4a382a2eb861b82da9461914b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConstraintsResource")
    def put_constraints_resource(
        self,
        *,
        s3_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_uri SagemakerDataQualityJobDefinition#s3_uri}.
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource(
            s3_uri=s3_uri
        )

        return typing.cast(None, jsii.invoke(self, "putConstraintsResource", [value]))

    @jsii.member(jsii_name="putStatisticsResource")
    def put_statistics_resource(
        self,
        *,
        s3_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_uri SagemakerDataQualityJobDefinition#s3_uri}.
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource(
            s3_uri=s3_uri
        )

        return typing.cast(None, jsii.invoke(self, "putStatisticsResource", [value]))

    @jsii.member(jsii_name="resetConstraintsResource")
    def reset_constraints_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConstraintsResource", []))

    @jsii.member(jsii_name="resetStatisticsResource")
    def reset_statistics_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatisticsResource", []))

    @builtins.property
    @jsii.member(jsii_name="constraintsResource")
    def constraints_resource(
        self,
    ) -> SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResourceOutputReference:
        return typing.cast(SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResourceOutputReference, jsii.get(self, "constraintsResource"))

    @builtins.property
    @jsii.member(jsii_name="statisticsResource")
    def statistics_resource(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResourceOutputReference":
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResourceOutputReference", jsii.get(self, "statisticsResource"))

    @builtins.property
    @jsii.member(jsii_name="constraintsResourceInput")
    def constraints_resource_input(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource], jsii.get(self, "constraintsResourceInput"))

    @builtins.property
    @jsii.member(jsii_name="statisticsResourceInput")
    def statistics_resource_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource"]:
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource"], jsii.get(self, "statisticsResourceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfig]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09b91325b685b41b00892b25e53ee510728eb478017c42e617068eae074a66ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource",
    jsii_struct_bases=[],
    name_mapping={"s3_uri": "s3Uri"},
)
class SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource:
    def __init__(self, *, s3_uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_uri SagemakerDataQualityJobDefinition#s3_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bd19c142ff88a6a831c175f07091711417376bd06c7e28b47f80d7c7491628a)
            check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if s3_uri is not None:
            self._values["s3_uri"] = s3_uri

    @builtins.property
    def s3_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_uri SagemakerDataQualityJobDefinition#s3_uri}.'''
        result = self._values.get("s3_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c62f555aa2a5da7593b8fb9162405e1b2fb7abe85b0430f7d88b9a3cfc5d4d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetS3Uri")
    def reset_s3_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Uri", []))

    @builtins.property
    @jsii.member(jsii_name="s3UriInput")
    def s3_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3UriInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Uri")
    def s3_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Uri"))

    @s3_uri.setter
    def s3_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7686fbd094dd79f5207c27e3b19f2d6b72af5f7172450e2b61e8d7131e60068a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8445755be2d4ac49e112e9109a5703584beaf24196c3e69b1805a48f89201d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInput",
    jsii_struct_bases=[],
    name_mapping={
        "batch_transform_input": "batchTransformInput",
        "endpoint_input": "endpointInput",
    },
)
class SagemakerDataQualityJobDefinitionDataQualityJobInput:
    def __init__(
        self,
        *,
        batch_transform_input: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_input: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param batch_transform_input: batch_transform_input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#batch_transform_input SagemakerDataQualityJobDefinition#batch_transform_input}
        :param endpoint_input: endpoint_input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#endpoint_input SagemakerDataQualityJobDefinition#endpoint_input}
        '''
        if isinstance(batch_transform_input, dict):
            batch_transform_input = SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput(**batch_transform_input)
        if isinstance(endpoint_input, dict):
            endpoint_input = SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput(**endpoint_input)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ac3e0a3f5899fffeaa9bbeaf757bb6c1a5a5194fd6463ae0bded86214b28e7c)
            check_type(argname="argument batch_transform_input", value=batch_transform_input, expected_type=type_hints["batch_transform_input"])
            check_type(argname="argument endpoint_input", value=endpoint_input, expected_type=type_hints["endpoint_input"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if batch_transform_input is not None:
            self._values["batch_transform_input"] = batch_transform_input
        if endpoint_input is not None:
            self._values["endpoint_input"] = endpoint_input

    @builtins.property
    def batch_transform_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput"]:
        '''batch_transform_input block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#batch_transform_input SagemakerDataQualityJobDefinition#batch_transform_input}
        '''
        result = self._values.get("batch_transform_input")
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput"], result)

    @builtins.property
    def endpoint_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput"]:
        '''endpoint_input block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#endpoint_input SagemakerDataQualityJobDefinition#endpoint_input}
        '''
        result = self._values.get("endpoint_input")
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityJobInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput",
    jsii_struct_bases=[],
    name_mapping={
        "data_captured_destination_s3_uri": "dataCapturedDestinationS3Uri",
        "dataset_format": "datasetFormat",
        "local_path": "localPath",
        "s3_data_distribution_type": "s3DataDistributionType",
        "s3_input_mode": "s3InputMode",
    },
)
class SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput:
    def __init__(
        self,
        *,
        data_captured_destination_s3_uri: builtins.str,
        dataset_format: typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat", typing.Dict[builtins.str, typing.Any]],
        local_path: typing.Optional[builtins.str] = None,
        s3_data_distribution_type: typing.Optional[builtins.str] = None,
        s3_input_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_captured_destination_s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#data_captured_destination_s3_uri SagemakerDataQualityJobDefinition#data_captured_destination_s3_uri}.
        :param dataset_format: dataset_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#dataset_format SagemakerDataQualityJobDefinition#dataset_format}
        :param local_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#local_path SagemakerDataQualityJobDefinition#local_path}.
        :param s3_data_distribution_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_data_distribution_type SagemakerDataQualityJobDefinition#s3_data_distribution_type}.
        :param s3_input_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_input_mode SagemakerDataQualityJobDefinition#s3_input_mode}.
        '''
        if isinstance(dataset_format, dict):
            dataset_format = SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat(**dataset_format)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa600b232e5da006570fbaa5cee8a7b5b09d98355d9d72d1f3c271f409694d43)
            check_type(argname="argument data_captured_destination_s3_uri", value=data_captured_destination_s3_uri, expected_type=type_hints["data_captured_destination_s3_uri"])
            check_type(argname="argument dataset_format", value=dataset_format, expected_type=type_hints["dataset_format"])
            check_type(argname="argument local_path", value=local_path, expected_type=type_hints["local_path"])
            check_type(argname="argument s3_data_distribution_type", value=s3_data_distribution_type, expected_type=type_hints["s3_data_distribution_type"])
            check_type(argname="argument s3_input_mode", value=s3_input_mode, expected_type=type_hints["s3_input_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_captured_destination_s3_uri": data_captured_destination_s3_uri,
            "dataset_format": dataset_format,
        }
        if local_path is not None:
            self._values["local_path"] = local_path
        if s3_data_distribution_type is not None:
            self._values["s3_data_distribution_type"] = s3_data_distribution_type
        if s3_input_mode is not None:
            self._values["s3_input_mode"] = s3_input_mode

    @builtins.property
    def data_captured_destination_s3_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#data_captured_destination_s3_uri SagemakerDataQualityJobDefinition#data_captured_destination_s3_uri}.'''
        result = self._values.get("data_captured_destination_s3_uri")
        assert result is not None, "Required property 'data_captured_destination_s3_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dataset_format(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat":
        '''dataset_format block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#dataset_format SagemakerDataQualityJobDefinition#dataset_format}
        '''
        result = self._values.get("dataset_format")
        assert result is not None, "Required property 'dataset_format' is missing"
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat", result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#local_path SagemakerDataQualityJobDefinition#local_path}.'''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_data_distribution_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_data_distribution_type SagemakerDataQualityJobDefinition#s3_data_distribution_type}.'''
        result = self._values.get("s3_data_distribution_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_input_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_input_mode SagemakerDataQualityJobDefinition#s3_input_mode}.'''
        result = self._values.get("s3_input_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat",
    jsii_struct_bases=[],
    name_mapping={"csv": "csv", "json": "json"},
)
class SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat:
    def __init__(
        self,
        *,
        csv: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv", typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param csv: csv block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#csv SagemakerDataQualityJobDefinition#csv}
        :param json: json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#json SagemakerDataQualityJobDefinition#json}
        '''
        if isinstance(csv, dict):
            csv = SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv(**csv)
        if isinstance(json, dict):
            json = SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson(**json)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da1edd9b168856f5d9415254ef3e57f3b1604dfd1a2841befd6c405a5b528e44)
            check_type(argname="argument csv", value=csv, expected_type=type_hints["csv"])
            check_type(argname="argument json", value=json, expected_type=type_hints["json"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if csv is not None:
            self._values["csv"] = csv
        if json is not None:
            self._values["json"] = json

    @builtins.property
    def csv(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv"]:
        '''csv block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#csv SagemakerDataQualityJobDefinition#csv}
        '''
        result = self._values.get("csv")
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv"], result)

    @builtins.property
    def json(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson"]:
        '''json block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#json SagemakerDataQualityJobDefinition#json}
        '''
        result = self._values.get("json")
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv",
    jsii_struct_bases=[],
    name_mapping={"header": "header"},
)
class SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv:
    def __init__(
        self,
        *,
        header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#header SagemakerDataQualityJobDefinition#header}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd39e861c417a5ba0c4224d3b01a6d4b7017c3cb2be5740243b0c38c4270d5b1)
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if header is not None:
            self._values["header"] = header

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#header SagemakerDataQualityJobDefinition#header}.'''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsvOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsvOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__813ab6da8da775616957acfd2e032515fdc29f13dee619e1c968b9f71b0232ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "header"))

    @header.setter
    def header(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18fd1599f72265bcc2fbe9dc6236880596d455ee6bfd5e8a1bc6b6fbe00c8c2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "header", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a203fd13fbe91558eba6f4f5e3696d3d6ba0f1c14530575c79eaf56665f0246f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson",
    jsii_struct_bases=[],
    name_mapping={"line": "line"},
)
class SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson:
    def __init__(
        self,
        *,
        line: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param line: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#line SagemakerDataQualityJobDefinition#line}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eb532b7c71e8597a6984cb0b51b6be466b258472deb7c911b36c2cb5b145aa5)
            check_type(argname="argument line", value=line, expected_type=type_hints["line"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if line is not None:
            self._values["line"] = line

    @builtins.property
    def line(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#line SagemakerDataQualityJobDefinition#line}.'''
        result = self._values.get("line")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJsonOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJsonOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43a6339e7f1d1a944e48dc11614abe6ecbb28f252cc363fefbd795ad07f0d561)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLine")
    def reset_line(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLine", []))

    @builtins.property
    @jsii.member(jsii_name="lineInput")
    def line_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "lineInput"))

    @builtins.property
    @jsii.member(jsii_name="line")
    def line(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "line"))

    @line.setter
    def line(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0201845ecbd64c47e252d23882f57bff80aee09935f4c9415b263da8da5764eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "line", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47bc5b209fb136caf10406e686d1199aa66cb73ee580f169e5331788fc5112f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6ffa3a24eb653fec6dff454ed1fc85d4c1837cc13c35edc12a89a7a7231f911)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCsv")
    def put_csv(
        self,
        *,
        header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#header SagemakerDataQualityJobDefinition#header}.
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv(
            header=header
        )

        return typing.cast(None, jsii.invoke(self, "putCsv", [value]))

    @jsii.member(jsii_name="putJson")
    def put_json(
        self,
        *,
        line: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param line: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#line SagemakerDataQualityJobDefinition#line}.
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson(
            line=line
        )

        return typing.cast(None, jsii.invoke(self, "putJson", [value]))

    @jsii.member(jsii_name="resetCsv")
    def reset_csv(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCsv", []))

    @jsii.member(jsii_name="resetJson")
    def reset_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJson", []))

    @builtins.property
    @jsii.member(jsii_name="csv")
    def csv(
        self,
    ) -> SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsvOutputReference:
        return typing.cast(SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsvOutputReference, jsii.get(self, "csv"))

    @builtins.property
    @jsii.member(jsii_name="json")
    def json(
        self,
    ) -> SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJsonOutputReference:
        return typing.cast(SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJsonOutputReference, jsii.get(self, "json"))

    @builtins.property
    @jsii.member(jsii_name="csvInput")
    def csv_input(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv], jsii.get(self, "csvInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonInput")
    def json_input(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson], jsii.get(self, "jsonInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ab0608ba5e4efb49955a25179cb119c10298a93a635776fcd795e5f5a49d4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__418acc4cb246e1f28ef842d9f430081c982c6e74364bcf40f98b65f04e076b15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDatasetFormat")
    def put_dataset_format(
        self,
        *,
        csv: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv, typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param csv: csv block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#csv SagemakerDataQualityJobDefinition#csv}
        :param json: json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#json SagemakerDataQualityJobDefinition#json}
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat(
            csv=csv, json=json
        )

        return typing.cast(None, jsii.invoke(self, "putDatasetFormat", [value]))

    @jsii.member(jsii_name="resetLocalPath")
    def reset_local_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalPath", []))

    @jsii.member(jsii_name="resetS3DataDistributionType")
    def reset_s3_data_distribution_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3DataDistributionType", []))

    @jsii.member(jsii_name="resetS3InputMode")
    def reset_s3_input_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3InputMode", []))

    @builtins.property
    @jsii.member(jsii_name="datasetFormat")
    def dataset_format(
        self,
    ) -> SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatOutputReference:
        return typing.cast(SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatOutputReference, jsii.get(self, "datasetFormat"))

    @builtins.property
    @jsii.member(jsii_name="dataCapturedDestinationS3UriInput")
    def data_captured_destination_s3_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataCapturedDestinationS3UriInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetFormatInput")
    def dataset_format_input(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat], jsii.get(self, "datasetFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="s3DataDistributionTypeInput")
    def s3_data_distribution_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3DataDistributionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="s3InputModeInput")
    def s3_input_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3InputModeInput"))

    @builtins.property
    @jsii.member(jsii_name="dataCapturedDestinationS3Uri")
    def data_captured_destination_s3_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataCapturedDestinationS3Uri"))

    @data_captured_destination_s3_uri.setter
    def data_captured_destination_s3_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397b59d80ae30a01403913619fa611e2c111e07100661c8e80877c08ecddf9e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataCapturedDestinationS3Uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a70b561ebc475be9a26e9d324e51aab19279433d8ea4b92fc1021ca2be3376c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3DataDistributionType")
    def s3_data_distribution_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3DataDistributionType"))

    @s3_data_distribution_type.setter
    def s3_data_distribution_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38136d478d4d1ea78ca383f0df2311b8bc43c16246c7d98f73536297ef5deb0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3DataDistributionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3InputMode")
    def s3_input_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3InputMode"))

    @s3_input_mode.setter
    def s3_input_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b90f2c3ef518066672f61bdf8761b33533cc58337f99dff8af254027297c8907)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3InputMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03808872de74676633ef7ac12597fe715134e9ecd7b18693ce53e1c1e127db9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint_name": "endpointName",
        "local_path": "localPath",
        "s3_data_distribution_type": "s3DataDistributionType",
        "s3_input_mode": "s3InputMode",
    },
)
class SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput:
    def __init__(
        self,
        *,
        endpoint_name: builtins.str,
        local_path: typing.Optional[builtins.str] = None,
        s3_data_distribution_type: typing.Optional[builtins.str] = None,
        s3_input_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoint_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#endpoint_name SagemakerDataQualityJobDefinition#endpoint_name}.
        :param local_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#local_path SagemakerDataQualityJobDefinition#local_path}.
        :param s3_data_distribution_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_data_distribution_type SagemakerDataQualityJobDefinition#s3_data_distribution_type}.
        :param s3_input_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_input_mode SagemakerDataQualityJobDefinition#s3_input_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36387650c9fe0bc0ddd09f8a15f4f8b50afd95a6dce2045fa5ffb163b21d1ae0)
            check_type(argname="argument endpoint_name", value=endpoint_name, expected_type=type_hints["endpoint_name"])
            check_type(argname="argument local_path", value=local_path, expected_type=type_hints["local_path"])
            check_type(argname="argument s3_data_distribution_type", value=s3_data_distribution_type, expected_type=type_hints["s3_data_distribution_type"])
            check_type(argname="argument s3_input_mode", value=s3_input_mode, expected_type=type_hints["s3_input_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint_name": endpoint_name,
        }
        if local_path is not None:
            self._values["local_path"] = local_path
        if s3_data_distribution_type is not None:
            self._values["s3_data_distribution_type"] = s3_data_distribution_type
        if s3_input_mode is not None:
            self._values["s3_input_mode"] = s3_input_mode

    @builtins.property
    def endpoint_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#endpoint_name SagemakerDataQualityJobDefinition#endpoint_name}.'''
        result = self._values.get("endpoint_name")
        assert result is not None, "Required property 'endpoint_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#local_path SagemakerDataQualityJobDefinition#local_path}.'''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_data_distribution_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_data_distribution_type SagemakerDataQualityJobDefinition#s3_data_distribution_type}.'''
        result = self._values.get("s3_data_distribution_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_input_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_input_mode SagemakerDataQualityJobDefinition#s3_input_mode}.'''
        result = self._values.get("s3_input_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6663067965cb8bba100ca1216d3b164921f0ac63bd4f080a044ea64fa4f60af2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLocalPath")
    def reset_local_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalPath", []))

    @jsii.member(jsii_name="resetS3DataDistributionType")
    def reset_s3_data_distribution_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3DataDistributionType", []))

    @jsii.member(jsii_name="resetS3InputMode")
    def reset_s3_input_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3InputMode", []))

    @builtins.property
    @jsii.member(jsii_name="endpointNameInput")
    def endpoint_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointNameInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="s3DataDistributionTypeInput")
    def s3_data_distribution_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3DataDistributionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="s3InputModeInput")
    def s3_input_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3InputModeInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointName")
    def endpoint_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointName"))

    @endpoint_name.setter
    def endpoint_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f128e6bfbf4a4d25271b8b4335799cbcc187914fb86840b416ec30c4de7d3089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b034cdfb419d29a1a096dda83fae70a0a87841e6707706da643c3bd8d5eec843)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3DataDistributionType")
    def s3_data_distribution_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3DataDistributionType"))

    @s3_data_distribution_type.setter
    def s3_data_distribution_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2977bdf781f953f4b6ceca7ce335a641f4f8a5b51a684f8273d65a4738078b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3DataDistributionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3InputMode")
    def s3_input_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3InputMode"))

    @s3_input_mode.setter
    def s3_input_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88303cf79a8c8b2e5ea35b9198192a6131c63a49967e976c3a18d9aa47e94519)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3InputMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecdb54a900792e2cd9d939be91a3fede225ed51fd3cd6b85b7cfe7ee90a80a2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerDataQualityJobDefinitionDataQualityJobInputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa4f19ae18a2557174a0a5650104f4efc9909f3be65d14c8d111646349e7420c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBatchTransformInput")
    def put_batch_transform_input(
        self,
        *,
        data_captured_destination_s3_uri: builtins.str,
        dataset_format: typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat, typing.Dict[builtins.str, typing.Any]],
        local_path: typing.Optional[builtins.str] = None,
        s3_data_distribution_type: typing.Optional[builtins.str] = None,
        s3_input_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_captured_destination_s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#data_captured_destination_s3_uri SagemakerDataQualityJobDefinition#data_captured_destination_s3_uri}.
        :param dataset_format: dataset_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#dataset_format SagemakerDataQualityJobDefinition#dataset_format}
        :param local_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#local_path SagemakerDataQualityJobDefinition#local_path}.
        :param s3_data_distribution_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_data_distribution_type SagemakerDataQualityJobDefinition#s3_data_distribution_type}.
        :param s3_input_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_input_mode SagemakerDataQualityJobDefinition#s3_input_mode}.
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput(
            data_captured_destination_s3_uri=data_captured_destination_s3_uri,
            dataset_format=dataset_format,
            local_path=local_path,
            s3_data_distribution_type=s3_data_distribution_type,
            s3_input_mode=s3_input_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putBatchTransformInput", [value]))

    @jsii.member(jsii_name="putEndpointInput")
    def put_endpoint_input(
        self,
        *,
        endpoint_name: builtins.str,
        local_path: typing.Optional[builtins.str] = None,
        s3_data_distribution_type: typing.Optional[builtins.str] = None,
        s3_input_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoint_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#endpoint_name SagemakerDataQualityJobDefinition#endpoint_name}.
        :param local_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#local_path SagemakerDataQualityJobDefinition#local_path}.
        :param s3_data_distribution_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_data_distribution_type SagemakerDataQualityJobDefinition#s3_data_distribution_type}.
        :param s3_input_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_input_mode SagemakerDataQualityJobDefinition#s3_input_mode}.
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput(
            endpoint_name=endpoint_name,
            local_path=local_path,
            s3_data_distribution_type=s3_data_distribution_type,
            s3_input_mode=s3_input_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putEndpointInput", [value]))

    @jsii.member(jsii_name="resetBatchTransformInput")
    def reset_batch_transform_input(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchTransformInput", []))

    @jsii.member(jsii_name="resetEndpointInput")
    def reset_endpoint_input(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointInput", []))

    @builtins.property
    @jsii.member(jsii_name="batchTransformInput")
    def batch_transform_input(
        self,
    ) -> SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputOutputReference:
        return typing.cast(SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputOutputReference, jsii.get(self, "batchTransformInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(
        self,
    ) -> SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInputOutputReference:
        return typing.cast(SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInputOutputReference, jsii.get(self, "endpointInput"))

    @builtins.property
    @jsii.member(jsii_name="batchTransformInputInput")
    def batch_transform_input_input(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput], jsii.get(self, "batchTransformInputInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointInputInput")
    def endpoint_input_input(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput], jsii.get(self, "endpointInputInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInput]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd1ffcae90c094114dc07778d45d2a603a6b5570f3372139de34ac39fd53d7a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig",
    jsii_struct_bases=[],
    name_mapping={"monitoring_outputs": "monitoringOutputs", "kms_key_id": "kmsKeyId"},
)
class SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig:
    def __init__(
        self,
        *,
        monitoring_outputs: typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs", typing.Dict[builtins.str, typing.Any]],
        kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param monitoring_outputs: monitoring_outputs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#monitoring_outputs SagemakerDataQualityJobDefinition#monitoring_outputs}
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#kms_key_id SagemakerDataQualityJobDefinition#kms_key_id}.
        '''
        if isinstance(monitoring_outputs, dict):
            monitoring_outputs = SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs(**monitoring_outputs)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38f1b543dd1acbb394cc14ea14dad86b5e1059224705561b0a8b8c68920c263b)
            check_type(argname="argument monitoring_outputs", value=monitoring_outputs, expected_type=type_hints["monitoring_outputs"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "monitoring_outputs": monitoring_outputs,
        }
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id

    @builtins.property
    def monitoring_outputs(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs":
        '''monitoring_outputs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#monitoring_outputs SagemakerDataQualityJobDefinition#monitoring_outputs}
        '''
        result = self._values.get("monitoring_outputs")
        assert result is not None, "Required property 'monitoring_outputs' is missing"
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs", result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#kms_key_id SagemakerDataQualityJobDefinition#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs",
    jsii_struct_bases=[],
    name_mapping={"s3_output": "s3Output"},
)
class SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs:
    def __init__(
        self,
        *,
        s3_output: typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param s3_output: s3_output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_output SagemakerDataQualityJobDefinition#s3_output}
        '''
        if isinstance(s3_output, dict):
            s3_output = SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output(**s3_output)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a06512b5e920838fe9ac133d26ea909b04f40f52065a0f9fe2bb757d2c84b15)
            check_type(argname="argument s3_output", value=s3_output, expected_type=type_hints["s3_output"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_output": s3_output,
        }

    @builtins.property
    def s3_output(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output":
        '''s3_output block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_output SagemakerDataQualityJobDefinition#s3_output}
        '''
        result = self._values.get("s3_output")
        assert result is not None, "Required property 's3_output' is missing"
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef89dd4c6b31beb9d2f9e7e409d31211e7cd6c7d5d33ea24ea032b5857b60f82)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putS3Output")
    def put_s3_output(
        self,
        *,
        s3_uri: builtins.str,
        local_path: typing.Optional[builtins.str] = None,
        s3_upload_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_uri SagemakerDataQualityJobDefinition#s3_uri}.
        :param local_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#local_path SagemakerDataQualityJobDefinition#local_path}.
        :param s3_upload_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_upload_mode SagemakerDataQualityJobDefinition#s3_upload_mode}.
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output(
            s3_uri=s3_uri, local_path=local_path, s3_upload_mode=s3_upload_mode
        )

        return typing.cast(None, jsii.invoke(self, "putS3Output", [value]))

    @builtins.property
    @jsii.member(jsii_name="s3Output")
    def s3_output(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3OutputOutputReference":
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3OutputOutputReference", jsii.get(self, "s3Output"))

    @builtins.property
    @jsii.member(jsii_name="s3OutputInput")
    def s3_output_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output"]:
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output"], jsii.get(self, "s3OutputInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f12452eb8b12f9f6be5c48324e299897427de2c7e548fcc55cbdda3ad96a6ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output",
    jsii_struct_bases=[],
    name_mapping={
        "s3_uri": "s3Uri",
        "local_path": "localPath",
        "s3_upload_mode": "s3UploadMode",
    },
)
class SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output:
    def __init__(
        self,
        *,
        s3_uri: builtins.str,
        local_path: typing.Optional[builtins.str] = None,
        s3_upload_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_uri SagemakerDataQualityJobDefinition#s3_uri}.
        :param local_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#local_path SagemakerDataQualityJobDefinition#local_path}.
        :param s3_upload_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_upload_mode SagemakerDataQualityJobDefinition#s3_upload_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b767b87952396763eac8f25f6d6ca0e9da18178e06e9961cfcfb0d88af777391)
            check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
            check_type(argname="argument local_path", value=local_path, expected_type=type_hints["local_path"])
            check_type(argname="argument s3_upload_mode", value=s3_upload_mode, expected_type=type_hints["s3_upload_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_uri": s3_uri,
        }
        if local_path is not None:
            self._values["local_path"] = local_path
        if s3_upload_mode is not None:
            self._values["s3_upload_mode"] = s3_upload_mode

    @builtins.property
    def s3_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_uri SagemakerDataQualityJobDefinition#s3_uri}.'''
        result = self._values.get("s3_uri")
        assert result is not None, "Required property 's3_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#local_path SagemakerDataQualityJobDefinition#local_path}.'''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_upload_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_upload_mode SagemakerDataQualityJobDefinition#s3_upload_mode}.'''
        result = self._values.get("s3_upload_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3OutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3OutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9887c2703586868ce89aa5b439b22d49f3e72fda3d9e94666cc91ca098082669)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLocalPath")
    def reset_local_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalPath", []))

    @jsii.member(jsii_name="resetS3UploadMode")
    def reset_s3_upload_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3UploadMode", []))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="s3UploadModeInput")
    def s3_upload_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3UploadModeInput"))

    @builtins.property
    @jsii.member(jsii_name="s3UriInput")
    def s3_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3UriInput"))

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f6c031761598729608d3322f6925a2b4dc06dd30ac66cf5e5c8e2ecfde34a50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3UploadMode")
    def s3_upload_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3UploadMode"))

    @s3_upload_mode.setter
    def s3_upload_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3464f6aeab5422a6644c40780d45b3fa1772d2e684e0f2b24a46ca28f82eb9d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3UploadMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3Uri")
    def s3_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Uri"))

    @s3_uri.setter
    def s3_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__736e3debf9260fbef209e51756e328c9b670cd46cc91ad144f697ef966f520aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4946297d581f942ba72b91b1943250e132bdc0ebc677bc1db97862fb715319f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75725460d8ecf3d2691b1b6e7f23836641e05423a2681f9a2ce6e0b60e1e7978)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMonitoringOutputs")
    def put_monitoring_outputs(
        self,
        *,
        s3_output: typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param s3_output: s3_output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#s3_output SagemakerDataQualityJobDefinition#s3_output}
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs(
            s3_output=s3_output
        )

        return typing.cast(None, jsii.invoke(self, "putMonitoringOutputs", [value]))

    @jsii.member(jsii_name="resetKmsKeyId")
    def reset_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyId", []))

    @builtins.property
    @jsii.member(jsii_name="monitoringOutputs")
    def monitoring_outputs(
        self,
    ) -> SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsOutputReference:
        return typing.cast(SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsOutputReference, jsii.get(self, "monitoringOutputs"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="monitoringOutputsInput")
    def monitoring_outputs_input(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs], jsii.get(self, "monitoringOutputsInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf51871ebc0d54ee0b57165db9d4c783bdbbe6628ba26661aec60fc080c72433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa0590798168c066a9df57e89b7be291164e3c383a9ee19bc20ce4848a6395f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionJobResources",
    jsii_struct_bases=[],
    name_mapping={"cluster_config": "clusterConfig"},
)
class SagemakerDataQualityJobDefinitionJobResources:
    def __init__(
        self,
        *,
        cluster_config: typing.Union["SagemakerDataQualityJobDefinitionJobResourcesClusterConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param cluster_config: cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#cluster_config SagemakerDataQualityJobDefinition#cluster_config}
        '''
        if isinstance(cluster_config, dict):
            cluster_config = SagemakerDataQualityJobDefinitionJobResourcesClusterConfig(**cluster_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6659dde8d0ad6d5227f732f96e75dc10a834cea8ea43beece6ae47d9661ceba)
            check_type(argname="argument cluster_config", value=cluster_config, expected_type=type_hints["cluster_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_config": cluster_config,
        }

    @builtins.property
    def cluster_config(
        self,
    ) -> "SagemakerDataQualityJobDefinitionJobResourcesClusterConfig":
        '''cluster_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#cluster_config SagemakerDataQualityJobDefinition#cluster_config}
        '''
        result = self._values.get("cluster_config")
        assert result is not None, "Required property 'cluster_config' is missing"
        return typing.cast("SagemakerDataQualityJobDefinitionJobResourcesClusterConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionJobResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionJobResourcesClusterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "instance_count": "instanceCount",
        "instance_type": "instanceType",
        "volume_size_in_gb": "volumeSizeInGb",
        "volume_kms_key_id": "volumeKmsKeyId",
    },
)
class SagemakerDataQualityJobDefinitionJobResourcesClusterConfig:
    def __init__(
        self,
        *,
        instance_count: jsii.Number,
        instance_type: builtins.str,
        volume_size_in_gb: jsii.Number,
        volume_kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#instance_count SagemakerDataQualityJobDefinition#instance_count}.
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#instance_type SagemakerDataQualityJobDefinition#instance_type}.
        :param volume_size_in_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#volume_size_in_gb SagemakerDataQualityJobDefinition#volume_size_in_gb}.
        :param volume_kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#volume_kms_key_id SagemakerDataQualityJobDefinition#volume_kms_key_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1be0e1c2ec00e5ffe670e21b8195d3b187bbc5708396694d2f99fb1fc82e9053)
            check_type(argname="argument instance_count", value=instance_count, expected_type=type_hints["instance_count"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument volume_size_in_gb", value=volume_size_in_gb, expected_type=type_hints["volume_size_in_gb"])
            check_type(argname="argument volume_kms_key_id", value=volume_kms_key_id, expected_type=type_hints["volume_kms_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_count": instance_count,
            "instance_type": instance_type,
            "volume_size_in_gb": volume_size_in_gb,
        }
        if volume_kms_key_id is not None:
            self._values["volume_kms_key_id"] = volume_kms_key_id

    @builtins.property
    def instance_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#instance_count SagemakerDataQualityJobDefinition#instance_count}.'''
        result = self._values.get("instance_count")
        assert result is not None, "Required property 'instance_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def instance_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#instance_type SagemakerDataQualityJobDefinition#instance_type}.'''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def volume_size_in_gb(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#volume_size_in_gb SagemakerDataQualityJobDefinition#volume_size_in_gb}.'''
        result = self._values.get("volume_size_in_gb")
        assert result is not None, "Required property 'volume_size_in_gb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def volume_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#volume_kms_key_id SagemakerDataQualityJobDefinition#volume_kms_key_id}.'''
        result = self._values.get("volume_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionJobResourcesClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionJobResourcesClusterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionJobResourcesClusterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4a5a0ea1e1daaca1ca7c5f927f1c98fc1a8a046d3fb781e369b806cb3433ca1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetVolumeKmsKeyId")
    def reset_volume_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeKmsKeyId", []))

    @builtins.property
    @jsii.member(jsii_name="instanceCountInput")
    def instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "instanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeKmsKeyIdInput")
    def volume_kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeKmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeSizeInGbInput")
    def volume_size_in_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "volumeSizeInGbInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceCount")
    def instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "instanceCount"))

    @instance_count.setter
    def instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58bfa807e4dd0b95eb352ccc6f095a4e84c8c25ebd00a8df031d098e1e594574)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfa708cc72ac8f3f108a6743dc8d7814598573939ec79eaac859ce61450a1706)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeKmsKeyId")
    def volume_kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeKmsKeyId"))

    @volume_kms_key_id.setter
    def volume_kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29cb4fe2be600acfa5f7c64e06f081f52308ea1bdf471122716d90fd8a2de261)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeKmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeSizeInGb")
    def volume_size_in_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "volumeSizeInGb"))

    @volume_size_in_gb.setter
    def volume_size_in_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26d88fd0c0548ae9ac595a1c0e306982d0afa077156dab7483221ee6f001d14c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeSizeInGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionJobResourcesClusterConfig]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionJobResourcesClusterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionJobResourcesClusterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d376e72523ee143780a1c9d73de8d780946f63efa8b5d57fdfdfad263dfe1fe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerDataQualityJobDefinitionJobResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionJobResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__090cdb5c41d118ebab74d270c048a2567d9a83d435da378d2994c9072d0110e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClusterConfig")
    def put_cluster_config(
        self,
        *,
        instance_count: jsii.Number,
        instance_type: builtins.str,
        volume_size_in_gb: jsii.Number,
        volume_kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#instance_count SagemakerDataQualityJobDefinition#instance_count}.
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#instance_type SagemakerDataQualityJobDefinition#instance_type}.
        :param volume_size_in_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#volume_size_in_gb SagemakerDataQualityJobDefinition#volume_size_in_gb}.
        :param volume_kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#volume_kms_key_id SagemakerDataQualityJobDefinition#volume_kms_key_id}.
        '''
        value = SagemakerDataQualityJobDefinitionJobResourcesClusterConfig(
            instance_count=instance_count,
            instance_type=instance_type,
            volume_size_in_gb=volume_size_in_gb,
            volume_kms_key_id=volume_kms_key_id,
        )

        return typing.cast(None, jsii.invoke(self, "putClusterConfig", [value]))

    @builtins.property
    @jsii.member(jsii_name="clusterConfig")
    def cluster_config(
        self,
    ) -> SagemakerDataQualityJobDefinitionJobResourcesClusterConfigOutputReference:
        return typing.cast(SagemakerDataQualityJobDefinitionJobResourcesClusterConfigOutputReference, jsii.get(self, "clusterConfig"))

    @builtins.property
    @jsii.member(jsii_name="clusterConfigInput")
    def cluster_config_input(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionJobResourcesClusterConfig]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionJobResourcesClusterConfig], jsii.get(self, "clusterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionJobResources]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionJobResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionJobResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__819f012bad08b952fcfa015bf526a834b4f3542dcc68c3369f4ad4aed5bca94b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_inter_container_traffic_encryption": "enableInterContainerTrafficEncryption",
        "enable_network_isolation": "enableNetworkIsolation",
        "vpc_config": "vpcConfig",
    },
)
class SagemakerDataQualityJobDefinitionNetworkConfig:
    def __init__(
        self,
        *,
        enable_inter_container_traffic_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_network_isolation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vpc_config: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enable_inter_container_traffic_encryption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#enable_inter_container_traffic_encryption SagemakerDataQualityJobDefinition#enable_inter_container_traffic_encryption}.
        :param enable_network_isolation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#enable_network_isolation SagemakerDataQualityJobDefinition#enable_network_isolation}.
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#vpc_config SagemakerDataQualityJobDefinition#vpc_config}
        '''
        if isinstance(vpc_config, dict):
            vpc_config = SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig(**vpc_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc385a8336d99ee325fb1dd52cf476cc2e8c35ce9d239251346a7bfef8d8d8e6)
            check_type(argname="argument enable_inter_container_traffic_encryption", value=enable_inter_container_traffic_encryption, expected_type=type_hints["enable_inter_container_traffic_encryption"])
            check_type(argname="argument enable_network_isolation", value=enable_network_isolation, expected_type=type_hints["enable_network_isolation"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_inter_container_traffic_encryption is not None:
            self._values["enable_inter_container_traffic_encryption"] = enable_inter_container_traffic_encryption
        if enable_network_isolation is not None:
            self._values["enable_network_isolation"] = enable_network_isolation
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def enable_inter_container_traffic_encryption(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#enable_inter_container_traffic_encryption SagemakerDataQualityJobDefinition#enable_inter_container_traffic_encryption}.'''
        result = self._values.get("enable_inter_container_traffic_encryption")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_network_isolation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#enable_network_isolation SagemakerDataQualityJobDefinition#enable_network_isolation}.'''
        result = self._values.get("enable_network_isolation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig"]:
        '''vpc_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#vpc_config SagemakerDataQualityJobDefinition#vpc_config}
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__caf8cb54a386c95eea2f205c71731cc16967c4271624dd4e29fa2e1911f24d6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVpcConfig")
    def put_vpc_config(
        self,
        *,
        security_group_ids: typing.Sequence[builtins.str],
        subnets: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#security_group_ids SagemakerDataQualityJobDefinition#security_group_ids}.
        :param subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#subnets SagemakerDataQualityJobDefinition#subnets}.
        '''
        value = SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig(
            security_group_ids=security_group_ids, subnets=subnets
        )

        return typing.cast(None, jsii.invoke(self, "putVpcConfig", [value]))

    @jsii.member(jsii_name="resetEnableInterContainerTrafficEncryption")
    def reset_enable_inter_container_traffic_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableInterContainerTrafficEncryption", []))

    @jsii.member(jsii_name="resetEnableNetworkIsolation")
    def reset_enable_network_isolation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableNetworkIsolation", []))

    @jsii.member(jsii_name="resetVpcConfig")
    def reset_vpc_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcConfig", []))

    @builtins.property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(
        self,
    ) -> "SagemakerDataQualityJobDefinitionNetworkConfigVpcConfigOutputReference":
        return typing.cast("SagemakerDataQualityJobDefinitionNetworkConfigVpcConfigOutputReference", jsii.get(self, "vpcConfig"))

    @builtins.property
    @jsii.member(jsii_name="enableInterContainerTrafficEncryptionInput")
    def enable_inter_container_traffic_encryption_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableInterContainerTrafficEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableNetworkIsolationInput")
    def enable_network_isolation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableNetworkIsolationInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcConfigInput")
    def vpc_config_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig"]:
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig"], jsii.get(self, "vpcConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="enableInterContainerTrafficEncryption")
    def enable_inter_container_traffic_encryption(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableInterContainerTrafficEncryption"))

    @enable_inter_container_traffic_encryption.setter
    def enable_inter_container_traffic_encryption(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__175ef0e59f0761c591da0e880bc6e59be73291794064c2cc69847b2acd29fa54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableInterContainerTrafficEncryption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableNetworkIsolation")
    def enable_network_isolation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableNetworkIsolation"))

    @enable_network_isolation.setter
    def enable_network_isolation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f09f0206e066b2c8e914f5a5a75c2cc0d631e12b4739e1e5344a740e0b611fc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableNetworkIsolation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionNetworkConfig]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b95269948983271c2ec81565980604ac62ecc2406ec92e60038fb53c118e8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig",
    jsii_struct_bases=[],
    name_mapping={"security_group_ids": "securityGroupIds", "subnets": "subnets"},
)
class SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig:
    def __init__(
        self,
        *,
        security_group_ids: typing.Sequence[builtins.str],
        subnets: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#security_group_ids SagemakerDataQualityJobDefinition#security_group_ids}.
        :param subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#subnets SagemakerDataQualityJobDefinition#subnets}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b27c29fba0a1d5c970f0935c8320ff53e691c6da7b58616b0890c570a24df144)
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "security_group_ids": security_group_ids,
            "subnets": subnets,
        }

    @builtins.property
    def security_group_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#security_group_ids SagemakerDataQualityJobDefinition#security_group_ids}.'''
        result = self._values.get("security_group_ids")
        assert result is not None, "Required property 'security_group_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def subnets(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#subnets SagemakerDataQualityJobDefinition#subnets}.'''
        result = self._values.get("subnets")
        assert result is not None, "Required property 'subnets' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionNetworkConfigVpcConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionNetworkConfigVpcConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d1c141e9ee073bdcaa4b5557c474db0a649a0b920a03c801f2fb8b9947622d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetsInput")
    def subnets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ded9449f7928645da2010b4b9bf5340aab8117b49723093debcd829830917541)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnets"))

    @subnets.setter
    def subnets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be65124eb9af29599107d66a483f54e5084e12fb7420b6d5cedb634e186ef588)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__416adeb85cded6580dd4c1beb575a3f05ed3893486aa8e46c04c29580870d8e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionStoppingCondition",
    jsii_struct_bases=[],
    name_mapping={"max_runtime_in_seconds": "maxRuntimeInSeconds"},
)
class SagemakerDataQualityJobDefinitionStoppingCondition:
    def __init__(
        self,
        *,
        max_runtime_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_runtime_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#max_runtime_in_seconds SagemakerDataQualityJobDefinition#max_runtime_in_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b44e6911b98bb92655e379e89a7805d926c03bab6b32ffe00dc0a5c71e68d01)
            check_type(argname="argument max_runtime_in_seconds", value=max_runtime_in_seconds, expected_type=type_hints["max_runtime_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_runtime_in_seconds is not None:
            self._values["max_runtime_in_seconds"] = max_runtime_in_seconds

    @builtins.property
    def max_runtime_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_data_quality_job_definition#max_runtime_in_seconds SagemakerDataQualityJobDefinition#max_runtime_in_seconds}.'''
        result = self._values.get("max_runtime_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionStoppingCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionStoppingConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionStoppingConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad9fb2076daa2b9c9a974f51335e2d0b29e2a085abda97fdf529d5289a68c820)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxRuntimeInSeconds")
    def reset_max_runtime_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRuntimeInSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="maxRuntimeInSecondsInput")
    def max_runtime_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRuntimeInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRuntimeInSeconds")
    def max_runtime_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRuntimeInSeconds"))

    @max_runtime_in_seconds.setter
    def max_runtime_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67bc1279984c181f417715cb571e68b8bd7178a0c4834c6f50843173df160d25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRuntimeInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionStoppingCondition]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionStoppingCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionStoppingCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f00be5a1c93cc77a900bd40905be4b429d97e9bc3b36fc3d936e6527e1db0355)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SagemakerDataQualityJobDefinition",
    "SagemakerDataQualityJobDefinitionConfig",
    "SagemakerDataQualityJobDefinitionDataQualityAppSpecification",
    "SagemakerDataQualityJobDefinitionDataQualityAppSpecificationOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityBaselineConfig",
    "SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource",
    "SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResourceOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityBaselineConfigOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource",
    "SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResourceOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityJobInput",
    "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput",
    "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat",
    "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv",
    "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsvOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson",
    "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJsonOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput",
    "SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInputOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityJobInputOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig",
    "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs",
    "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output",
    "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3OutputOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigOutputReference",
    "SagemakerDataQualityJobDefinitionJobResources",
    "SagemakerDataQualityJobDefinitionJobResourcesClusterConfig",
    "SagemakerDataQualityJobDefinitionJobResourcesClusterConfigOutputReference",
    "SagemakerDataQualityJobDefinitionJobResourcesOutputReference",
    "SagemakerDataQualityJobDefinitionNetworkConfig",
    "SagemakerDataQualityJobDefinitionNetworkConfigOutputReference",
    "SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig",
    "SagemakerDataQualityJobDefinitionNetworkConfigVpcConfigOutputReference",
    "SagemakerDataQualityJobDefinitionStoppingCondition",
    "SagemakerDataQualityJobDefinitionStoppingConditionOutputReference",
]

publication.publish()

def _typecheckingstub__6775f129c3139679cf62ade89df0d84ae7473fcd265d328c9c85b4dadd876db0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    data_quality_app_specification: typing.Union[SagemakerDataQualityJobDefinitionDataQualityAppSpecification, typing.Dict[builtins.str, typing.Any]],
    data_quality_job_input: typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobInput, typing.Dict[builtins.str, typing.Any]],
    data_quality_job_output_config: typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig, typing.Dict[builtins.str, typing.Any]],
    job_resources: typing.Union[SagemakerDataQualityJobDefinitionJobResources, typing.Dict[builtins.str, typing.Any]],
    role_arn: builtins.str,
    data_quality_baseline_config: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionDataQualityBaselineConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    network_config: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    stopping_condition: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionStoppingCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__41dfd7babdbaa10c5b55052271654a39ed0b85472438f5ab103a126804c089c5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda65a834d68df3576c96100e964f072b0b8dd9fcfc82977d77d22e0c25aa58d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62e862b6d59b95809aa9f4f953f95e9a292a9c5bae72e38fbf66d2c90467cb3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b386a88bac4df7422e41bc8610fb3f023b628d1d9339ac960a24fe5c4ab56185(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22b2d1695a819c1b8839f0c77c1a70d73a34ad94bbc8721a05abdd5fc3491bd7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7024c8cfe8154b3b9bc8c870f9c408dc0cec4e440101fa63329859819313aeae(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b6a0a1dc77bc32bc67f1c84f0f1866ee7115be14def3d541476133afd7c0bd(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_quality_app_specification: typing.Union[SagemakerDataQualityJobDefinitionDataQualityAppSpecification, typing.Dict[builtins.str, typing.Any]],
    data_quality_job_input: typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobInput, typing.Dict[builtins.str, typing.Any]],
    data_quality_job_output_config: typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig, typing.Dict[builtins.str, typing.Any]],
    job_resources: typing.Union[SagemakerDataQualityJobDefinitionJobResources, typing.Dict[builtins.str, typing.Any]],
    role_arn: builtins.str,
    data_quality_baseline_config: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionDataQualityBaselineConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    network_config: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    stopping_condition: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionStoppingCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33271098954b556f4acde17bbd57afa7ee9cfaf5a2d271e7f781b89877c12c12(
    *,
    image_uri: builtins.str,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    post_analytics_processor_source_uri: typing.Optional[builtins.str] = None,
    record_preprocessor_source_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7669f779938ef7d2f1c68bb9b5ea40b08fb2f0bcfff2668625a8495677465a34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__044a8a9eac1c60ad63fd5caa7fe5f0fa2f476b0654f707009a36409164232192(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb95664fd1d428a11b14614abc5c4d87e0d599c77c188cba00ca11f0583205af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e986f5b62f2ab4439992f3b12b14844d262cc4e7c25ced48f022f5507eed9539(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70c4737c816afdcc1e669e7e88701436a90ffe5be1c5d00f64bd71067e58f6b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb957deb6cb929f4844baf18031ef43422eb16d15a489162fe8ba3560e4ac41e(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityAppSpecification],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de15957fc62f32427e325123a895a96f1b76d25e8522d988e623acde62921a31(
    *,
    constraints_resource: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource, typing.Dict[builtins.str, typing.Any]]] = None,
    statistics_resource: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94c7360c077f02b21a1ae57f62773934d4881f5d08d992ca44cac86316dd445f(
    *,
    s3_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ca1d6e754e9554797c0b4b75931f7953104983c8faeb2bb8097b378555922b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__816d77cdfcc408e3b941b31f85433a57b13239a2b1f1b99ca5ab91696fc17ea9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba9698ff8c8ac983ab72d307a6aaaadaa0c9c2d1a4c9923a38470e0b3d978f9e(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19a92a3397817d024b4e26a1ce46a83e90d39c4a382a2eb861b82da9461914b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b91325b685b41b00892b25e53ee510728eb478017c42e617068eae074a66ba(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bd19c142ff88a6a831c175f07091711417376bd06c7e28b47f80d7c7491628a(
    *,
    s3_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c62f555aa2a5da7593b8fb9162405e1b2fb7abe85b0430f7d88b9a3cfc5d4d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7686fbd094dd79f5207c27e3b19f2d6b72af5f7172450e2b61e8d7131e60068a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8445755be2d4ac49e112e9109a5703584beaf24196c3e69b1805a48f89201d0(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ac3e0a3f5899fffeaa9bbeaf757bb6c1a5a5194fd6463ae0bded86214b28e7c(
    *,
    batch_transform_input: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoint_input: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa600b232e5da006570fbaa5cee8a7b5b09d98355d9d72d1f3c271f409694d43(
    *,
    data_captured_destination_s3_uri: builtins.str,
    dataset_format: typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat, typing.Dict[builtins.str, typing.Any]],
    local_path: typing.Optional[builtins.str] = None,
    s3_data_distribution_type: typing.Optional[builtins.str] = None,
    s3_input_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1edd9b168856f5d9415254ef3e57f3b1604dfd1a2841befd6c405a5b528e44(
    *,
    csv: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv, typing.Dict[builtins.str, typing.Any]]] = None,
    json: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd39e861c417a5ba0c4224d3b01a6d4b7017c3cb2be5740243b0c38c4270d5b1(
    *,
    header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__813ab6da8da775616957acfd2e032515fdc29f13dee619e1c968b9f71b0232ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18fd1599f72265bcc2fbe9dc6236880596d455ee6bfd5e8a1bc6b6fbe00c8c2a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a203fd13fbe91558eba6f4f5e3696d3d6ba0f1c14530575c79eaf56665f0246f(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eb532b7c71e8597a6984cb0b51b6be466b258472deb7c911b36c2cb5b145aa5(
    *,
    line: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43a6339e7f1d1a944e48dc11614abe6ecbb28f252cc363fefbd795ad07f0d561(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0201845ecbd64c47e252d23882f57bff80aee09935f4c9415b263da8da5764eb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47bc5b209fb136caf10406e686d1199aa66cb73ee580f169e5331788fc5112f3(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ffa3a24eb653fec6dff454ed1fc85d4c1837cc13c35edc12a89a7a7231f911(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ab0608ba5e4efb49955a25179cb119c10298a93a635776fcd795e5f5a49d4f(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__418acc4cb246e1f28ef842d9f430081c982c6e74364bcf40f98b65f04e076b15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397b59d80ae30a01403913619fa611e2c111e07100661c8e80877c08ecddf9e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a70b561ebc475be9a26e9d324e51aab19279433d8ea4b92fc1021ca2be3376c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38136d478d4d1ea78ca383f0df2311b8bc43c16246c7d98f73536297ef5deb0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90f2c3ef518066672f61bdf8761b33533cc58337f99dff8af254027297c8907(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03808872de74676633ef7ac12597fe715134e9ecd7b18693ce53e1c1e127db9b(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36387650c9fe0bc0ddd09f8a15f4f8b50afd95a6dce2045fa5ffb163b21d1ae0(
    *,
    endpoint_name: builtins.str,
    local_path: typing.Optional[builtins.str] = None,
    s3_data_distribution_type: typing.Optional[builtins.str] = None,
    s3_input_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6663067965cb8bba100ca1216d3b164921f0ac63bd4f080a044ea64fa4f60af2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f128e6bfbf4a4d25271b8b4335799cbcc187914fb86840b416ec30c4de7d3089(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b034cdfb419d29a1a096dda83fae70a0a87841e6707706da643c3bd8d5eec843(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2977bdf781f953f4b6ceca7ce335a641f4f8a5b51a684f8273d65a4738078b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88303cf79a8c8b2e5ea35b9198192a6131c63a49967e976c3a18d9aa47e94519(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecdb54a900792e2cd9d939be91a3fede225ed51fd3cd6b85b7cfe7ee90a80a2f(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa4f19ae18a2557174a0a5650104f4efc9909f3be65d14c8d111646349e7420c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd1ffcae90c094114dc07778d45d2a603a6b5570f3372139de34ac39fd53d7a6(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38f1b543dd1acbb394cc14ea14dad86b5e1059224705561b0a8b8c68920c263b(
    *,
    monitoring_outputs: typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs, typing.Dict[builtins.str, typing.Any]],
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a06512b5e920838fe9ac133d26ea909b04f40f52065a0f9fe2bb757d2c84b15(
    *,
    s3_output: typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef89dd4c6b31beb9d2f9e7e409d31211e7cd6c7d5d33ea24ea032b5857b60f82(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f12452eb8b12f9f6be5c48324e299897427de2c7e548fcc55cbdda3ad96a6ff(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b767b87952396763eac8f25f6d6ca0e9da18178e06e9961cfcfb0d88af777391(
    *,
    s3_uri: builtins.str,
    local_path: typing.Optional[builtins.str] = None,
    s3_upload_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9887c2703586868ce89aa5b439b22d49f3e72fda3d9e94666cc91ca098082669(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f6c031761598729608d3322f6925a2b4dc06dd30ac66cf5e5c8e2ecfde34a50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3464f6aeab5422a6644c40780d45b3fa1772d2e684e0f2b24a46ca28f82eb9d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__736e3debf9260fbef209e51756e328c9b670cd46cc91ad144f697ef966f520aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4946297d581f942ba72b91b1943250e132bdc0ebc677bc1db97862fb715319f(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75725460d8ecf3d2691b1b6e7f23836641e05423a2681f9a2ce6e0b60e1e7978(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf51871ebc0d54ee0b57165db9d4c783bdbbe6628ba26661aec60fc080c72433(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa0590798168c066a9df57e89b7be291164e3c383a9ee19bc20ce4848a6395f4(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6659dde8d0ad6d5227f732f96e75dc10a834cea8ea43beece6ae47d9661ceba(
    *,
    cluster_config: typing.Union[SagemakerDataQualityJobDefinitionJobResourcesClusterConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1be0e1c2ec00e5ffe670e21b8195d3b187bbc5708396694d2f99fb1fc82e9053(
    *,
    instance_count: jsii.Number,
    instance_type: builtins.str,
    volume_size_in_gb: jsii.Number,
    volume_kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a5a0ea1e1daaca1ca7c5f927f1c98fc1a8a046d3fb781e369b806cb3433ca1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58bfa807e4dd0b95eb352ccc6f095a4e84c8c25ebd00a8df031d098e1e594574(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfa708cc72ac8f3f108a6743dc8d7814598573939ec79eaac859ce61450a1706(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29cb4fe2be600acfa5f7c64e06f081f52308ea1bdf471122716d90fd8a2de261(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26d88fd0c0548ae9ac595a1c0e306982d0afa077156dab7483221ee6f001d14c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d376e72523ee143780a1c9d73de8d780946f63efa8b5d57fdfdfad263dfe1fe0(
    value: typing.Optional[SagemakerDataQualityJobDefinitionJobResourcesClusterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090cdb5c41d118ebab74d270c048a2567d9a83d435da378d2994c9072d0110e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__819f012bad08b952fcfa015bf526a834b4f3542dcc68c3369f4ad4aed5bca94b(
    value: typing.Optional[SagemakerDataQualityJobDefinitionJobResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc385a8336d99ee325fb1dd52cf476cc2e8c35ce9d239251346a7bfef8d8d8e6(
    *,
    enable_inter_container_traffic_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_network_isolation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vpc_config: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caf8cb54a386c95eea2f205c71731cc16967c4271624dd4e29fa2e1911f24d6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__175ef0e59f0761c591da0e880bc6e59be73291794064c2cc69847b2acd29fa54(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f09f0206e066b2c8e914f5a5a75c2cc0d631e12b4739e1e5344a740e0b611fc1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b95269948983271c2ec81565980604ac62ecc2406ec92e60038fb53c118e8e(
    value: typing.Optional[SagemakerDataQualityJobDefinitionNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b27c29fba0a1d5c970f0935c8320ff53e691c6da7b58616b0890c570a24df144(
    *,
    security_group_ids: typing.Sequence[builtins.str],
    subnets: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d1c141e9ee073bdcaa4b5557c474db0a649a0b920a03c801f2fb8b9947622d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ded9449f7928645da2010b4b9bf5340aab8117b49723093debcd829830917541(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be65124eb9af29599107d66a483f54e5084e12fb7420b6d5cedb634e186ef588(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__416adeb85cded6580dd4c1beb575a3f05ed3893486aa8e46c04c29580870d8e5(
    value: typing.Optional[SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b44e6911b98bb92655e379e89a7805d926c03bab6b32ffe00dc0a5c71e68d01(
    *,
    max_runtime_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad9fb2076daa2b9c9a974f51335e2d0b29e2a085abda97fdf529d5289a68c820(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67bc1279984c181f417715cb571e68b8bd7178a0c4834c6f50843173df160d25(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00be5a1c93cc77a900bd40905be4b429d97e9bc3b36fc3d936e6527e1db0355(
    value: typing.Optional[SagemakerDataQualityJobDefinitionStoppingCondition],
) -> None:
    """Type checking stubs"""
    pass
