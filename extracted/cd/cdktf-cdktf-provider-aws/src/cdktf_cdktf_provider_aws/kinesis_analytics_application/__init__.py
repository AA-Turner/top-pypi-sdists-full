r'''
# `aws_kinesis_analytics_application`

Refer to the Terraform Registry for docs: [`aws_kinesis_analytics_application`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application).
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


class KinesisAnalyticsApplication(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplication",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application aws_kinesis_analytics_application}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        cloudwatch_logging_options: typing.Optional[typing.Union["KinesisAnalyticsApplicationCloudwatchLoggingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        code: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        inputs: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputs", typing.Dict[builtins.str, typing.Any]]] = None,
        outputs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationOutputs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        reference_data_sources: typing.Optional[typing.Union["KinesisAnalyticsApplicationReferenceDataSources", typing.Dict[builtins.str, typing.Any]]] = None,
        start_application: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application aws_kinesis_analytics_application} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#name KinesisAnalyticsApplication#name}.
        :param cloudwatch_logging_options: cloudwatch_logging_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#cloudwatch_logging_options KinesisAnalyticsApplication#cloudwatch_logging_options}
        :param code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#code KinesisAnalyticsApplication#code}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#description KinesisAnalyticsApplication#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#id KinesisAnalyticsApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inputs: inputs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#inputs KinesisAnalyticsApplication#inputs}
        :param outputs: outputs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#outputs KinesisAnalyticsApplication#outputs}
        :param reference_data_sources: reference_data_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#reference_data_sources KinesisAnalyticsApplication#reference_data_sources}
        :param start_application: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#start_application KinesisAnalyticsApplication#start_application}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#tags KinesisAnalyticsApplication#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#tags_all KinesisAnalyticsApplication#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e38973a0043bfc6faa16a1919fb99aaa63b9e48bd15caa532c505e2c197eb588)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = KinesisAnalyticsApplicationConfig(
            name=name,
            cloudwatch_logging_options=cloudwatch_logging_options,
            code=code,
            description=description,
            id=id,
            inputs=inputs,
            outputs=outputs,
            reference_data_sources=reference_data_sources,
            start_application=start_application,
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
        '''Generates CDKTF code for importing a KinesisAnalyticsApplication resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the KinesisAnalyticsApplication to import.
        :param import_from_id: The id of the existing KinesisAnalyticsApplication that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the KinesisAnalyticsApplication to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2b5de6fe667f552c0afe96c8c556b05018f5e7e73743b172e657306a96b5ace)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCloudwatchLoggingOptions")
    def put_cloudwatch_logging_options(
        self,
        *,
        log_stream_arn: builtins.str,
        role_arn: builtins.str,
    ) -> None:
        '''
        :param log_stream_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#log_stream_arn KinesisAnalyticsApplication#log_stream_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        value = KinesisAnalyticsApplicationCloudwatchLoggingOptions(
            log_stream_arn=log_stream_arn, role_arn=role_arn
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLoggingOptions", [value]))

    @jsii.member(jsii_name="putInputs")
    def put_inputs(
        self,
        *,
        name_prefix: builtins.str,
        schema: typing.Union["KinesisAnalyticsApplicationInputsSchema", typing.Dict[builtins.str, typing.Any]],
        kinesis_firehose: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsKinesisFirehose", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis_stream: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsKinesisStream", typing.Dict[builtins.str, typing.Any]]] = None,
        parallelism: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsParallelism", typing.Dict[builtins.str, typing.Any]]] = None,
        processing_configuration: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsProcessingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        starting_position_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationInputsStartingPositionConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#name_prefix KinesisAnalyticsApplication#name_prefix}.
        :param schema: schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#schema KinesisAnalyticsApplication#schema}
        :param kinesis_firehose: kinesis_firehose block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#kinesis_firehose KinesisAnalyticsApplication#kinesis_firehose}
        :param kinesis_stream: kinesis_stream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#kinesis_stream KinesisAnalyticsApplication#kinesis_stream}
        :param parallelism: parallelism block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#parallelism KinesisAnalyticsApplication#parallelism}
        :param processing_configuration: processing_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#processing_configuration KinesisAnalyticsApplication#processing_configuration}
        :param starting_position_configuration: starting_position_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#starting_position_configuration KinesisAnalyticsApplication#starting_position_configuration}
        '''
        value = KinesisAnalyticsApplicationInputs(
            name_prefix=name_prefix,
            schema=schema,
            kinesis_firehose=kinesis_firehose,
            kinesis_stream=kinesis_stream,
            parallelism=parallelism,
            processing_configuration=processing_configuration,
            starting_position_configuration=starting_position_configuration,
        )

        return typing.cast(None, jsii.invoke(self, "putInputs", [value]))

    @jsii.member(jsii_name="putOutputs")
    def put_outputs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationOutputs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3541e46204fa4c3006fbc4df47ce50097ebd36fc4afaee13f659df7af1749f46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOutputs", [value]))

    @jsii.member(jsii_name="putReferenceDataSources")
    def put_reference_data_sources(
        self,
        *,
        s3: typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesS3", typing.Dict[builtins.str, typing.Any]],
        schema: typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesSchema", typing.Dict[builtins.str, typing.Any]],
        table_name: builtins.str,
    ) -> None:
        '''
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#s3 KinesisAnalyticsApplication#s3}
        :param schema: schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#schema KinesisAnalyticsApplication#schema}
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#table_name KinesisAnalyticsApplication#table_name}.
        '''
        value = KinesisAnalyticsApplicationReferenceDataSources(
            s3=s3, schema=schema, table_name=table_name
        )

        return typing.cast(None, jsii.invoke(self, "putReferenceDataSources", [value]))

    @jsii.member(jsii_name="resetCloudwatchLoggingOptions")
    def reset_cloudwatch_logging_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLoggingOptions", []))

    @jsii.member(jsii_name="resetCode")
    def reset_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCode", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInputs")
    def reset_inputs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputs", []))

    @jsii.member(jsii_name="resetOutputs")
    def reset_outputs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputs", []))

    @jsii.member(jsii_name="resetReferenceDataSources")
    def reset_reference_data_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReferenceDataSources", []))

    @jsii.member(jsii_name="resetStartApplication")
    def reset_start_application(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartApplication", []))

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
    @jsii.member(jsii_name="cloudwatchLoggingOptions")
    def cloudwatch_logging_options(
        self,
    ) -> "KinesisAnalyticsApplicationCloudwatchLoggingOptionsOutputReference":
        return typing.cast("KinesisAnalyticsApplicationCloudwatchLoggingOptionsOutputReference", jsii.get(self, "cloudwatchLoggingOptions"))

    @builtins.property
    @jsii.member(jsii_name="createTimestamp")
    def create_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="inputs")
    def inputs(self) -> "KinesisAnalyticsApplicationInputsOutputReference":
        return typing.cast("KinesisAnalyticsApplicationInputsOutputReference", jsii.get(self, "inputs"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdateTimestamp")
    def last_update_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastUpdateTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> "KinesisAnalyticsApplicationOutputsList":
        return typing.cast("KinesisAnalyticsApplicationOutputsList", jsii.get(self, "outputs"))

    @builtins.property
    @jsii.member(jsii_name="referenceDataSources")
    def reference_data_sources(
        self,
    ) -> "KinesisAnalyticsApplicationReferenceDataSourcesOutputReference":
        return typing.cast("KinesisAnalyticsApplicationReferenceDataSourcesOutputReference", jsii.get(self, "referenceDataSources"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingOptionsInput")
    def cloudwatch_logging_options_input(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationCloudwatchLoggingOptions"]:
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationCloudwatchLoggingOptions"], jsii.get(self, "cloudwatchLoggingOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="codeInput")
    def code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "codeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inputsInput")
    def inputs_input(self) -> typing.Optional["KinesisAnalyticsApplicationInputs"]:
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputs"], jsii.get(self, "inputsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="outputsInput")
    def outputs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationOutputs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationOutputs"]]], jsii.get(self, "outputsInput"))

    @builtins.property
    @jsii.member(jsii_name="referenceDataSourcesInput")
    def reference_data_sources_input(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationReferenceDataSources"]:
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationReferenceDataSources"], jsii.get(self, "referenceDataSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="startApplicationInput")
    def start_application_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "startApplicationInput"))

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
    @jsii.member(jsii_name="code")
    def code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "code"))

    @code.setter
    def code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4562f7f20420ca8b3620249f73ae8a656eb0a14c923a19be094f9a13a1f96841)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "code", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c07f70b8d5bd6abf858fa75b7fd99570a742d87fb1dd1daf07aa06750ff42d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f82235ade391105c6796d2ef82ded78b60f9f2411b09f32b00b864eafdd82be1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__140d479e4a0428a53731586e63bcb12ab9d7bb9f154e2ebea86ac602ce4c499b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startApplication")
    def start_application(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "startApplication"))

    @start_application.setter
    def start_application(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a8139aa6f446842cea3dc8e22f856fa0b3e8f28ba9088cf4f1a366536404e9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startApplication", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff42409f95f597212b3a02906d68c7264a5df19045bb4ba87b881ba0c0b4eb4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eddee7b19a988a0339ec6c6884633ac3ca903ef74d3339b44592492e143cdbba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationCloudwatchLoggingOptions",
    jsii_struct_bases=[],
    name_mapping={"log_stream_arn": "logStreamArn", "role_arn": "roleArn"},
)
class KinesisAnalyticsApplicationCloudwatchLoggingOptions:
    def __init__(self, *, log_stream_arn: builtins.str, role_arn: builtins.str) -> None:
        '''
        :param log_stream_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#log_stream_arn KinesisAnalyticsApplication#log_stream_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fc482b09d384c43e62def631a7fb8039a30450ecfeda622887bb88254082101)
            check_type(argname="argument log_stream_arn", value=log_stream_arn, expected_type=type_hints["log_stream_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_stream_arn": log_stream_arn,
            "role_arn": role_arn,
        }

    @builtins.property
    def log_stream_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#log_stream_arn KinesisAnalyticsApplication#log_stream_arn}.'''
        result = self._values.get("log_stream_arn")
        assert result is not None, "Required property 'log_stream_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationCloudwatchLoggingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationCloudwatchLoggingOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationCloudwatchLoggingOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__581e84bab74599343e9b0efa0aa4b2a05bfeee982daae070cac6de4644ead7aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="logStreamArnInput")
    def log_stream_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamArnInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamArn")
    def log_stream_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamArn"))

    @log_stream_arn.setter
    def log_stream_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21b4317d42b9d7fd670dc530fa0955858d5a311a2426cb71b76a5d4728857f17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc8c4744ac8feb928eee6ac08c9bff24c292c9eb03f1b3cb15323a8365cdacdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationCloudwatchLoggingOptions]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationCloudwatchLoggingOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationCloudwatchLoggingOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b160d954e4af909661f5334854a513686d495973bb77fb1cbbb53f83bcb1b82e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationConfig",
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
        "cloudwatch_logging_options": "cloudwatchLoggingOptions",
        "code": "code",
        "description": "description",
        "id": "id",
        "inputs": "inputs",
        "outputs": "outputs",
        "reference_data_sources": "referenceDataSources",
        "start_application": "startApplication",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class KinesisAnalyticsApplicationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cloudwatch_logging_options: typing.Optional[typing.Union[KinesisAnalyticsApplicationCloudwatchLoggingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        code: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        inputs: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputs", typing.Dict[builtins.str, typing.Any]]] = None,
        outputs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationOutputs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        reference_data_sources: typing.Optional[typing.Union["KinesisAnalyticsApplicationReferenceDataSources", typing.Dict[builtins.str, typing.Any]]] = None,
        start_application: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#name KinesisAnalyticsApplication#name}.
        :param cloudwatch_logging_options: cloudwatch_logging_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#cloudwatch_logging_options KinesisAnalyticsApplication#cloudwatch_logging_options}
        :param code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#code KinesisAnalyticsApplication#code}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#description KinesisAnalyticsApplication#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#id KinesisAnalyticsApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inputs: inputs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#inputs KinesisAnalyticsApplication#inputs}
        :param outputs: outputs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#outputs KinesisAnalyticsApplication#outputs}
        :param reference_data_sources: reference_data_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#reference_data_sources KinesisAnalyticsApplication#reference_data_sources}
        :param start_application: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#start_application KinesisAnalyticsApplication#start_application}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#tags KinesisAnalyticsApplication#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#tags_all KinesisAnalyticsApplication#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cloudwatch_logging_options, dict):
            cloudwatch_logging_options = KinesisAnalyticsApplicationCloudwatchLoggingOptions(**cloudwatch_logging_options)
        if isinstance(inputs, dict):
            inputs = KinesisAnalyticsApplicationInputs(**inputs)
        if isinstance(reference_data_sources, dict):
            reference_data_sources = KinesisAnalyticsApplicationReferenceDataSources(**reference_data_sources)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da1f38cfc966de0216aca724ceb70f6a1a45abd59246b4fe6ad85c0b3a6d0199)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument cloudwatch_logging_options", value=cloudwatch_logging_options, expected_type=type_hints["cloudwatch_logging_options"])
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument inputs", value=inputs, expected_type=type_hints["inputs"])
            check_type(argname="argument outputs", value=outputs, expected_type=type_hints["outputs"])
            check_type(argname="argument reference_data_sources", value=reference_data_sources, expected_type=type_hints["reference_data_sources"])
            check_type(argname="argument start_application", value=start_application, expected_type=type_hints["start_application"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
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
        if cloudwatch_logging_options is not None:
            self._values["cloudwatch_logging_options"] = cloudwatch_logging_options
        if code is not None:
            self._values["code"] = code
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if inputs is not None:
            self._values["inputs"] = inputs
        if outputs is not None:
            self._values["outputs"] = outputs
        if reference_data_sources is not None:
            self._values["reference_data_sources"] = reference_data_sources
        if start_application is not None:
            self._values["start_application"] = start_application
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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#name KinesisAnalyticsApplication#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloudwatch_logging_options(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationCloudwatchLoggingOptions]:
        '''cloudwatch_logging_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#cloudwatch_logging_options KinesisAnalyticsApplication#cloudwatch_logging_options}
        '''
        result = self._values.get("cloudwatch_logging_options")
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationCloudwatchLoggingOptions], result)

    @builtins.property
    def code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#code KinesisAnalyticsApplication#code}.'''
        result = self._values.get("code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#description KinesisAnalyticsApplication#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#id KinesisAnalyticsApplication#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inputs(self) -> typing.Optional["KinesisAnalyticsApplicationInputs"]:
        '''inputs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#inputs KinesisAnalyticsApplication#inputs}
        '''
        result = self._values.get("inputs")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputs"], result)

    @builtins.property
    def outputs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationOutputs"]]]:
        '''outputs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#outputs KinesisAnalyticsApplication#outputs}
        '''
        result = self._values.get("outputs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationOutputs"]]], result)

    @builtins.property
    def reference_data_sources(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationReferenceDataSources"]:
        '''reference_data_sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#reference_data_sources KinesisAnalyticsApplication#reference_data_sources}
        '''
        result = self._values.get("reference_data_sources")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationReferenceDataSources"], result)

    @builtins.property
    def start_application(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#start_application KinesisAnalyticsApplication#start_application}.'''
        result = self._values.get("start_application")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#tags KinesisAnalyticsApplication#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#tags_all KinesisAnalyticsApplication#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputs",
    jsii_struct_bases=[],
    name_mapping={
        "name_prefix": "namePrefix",
        "schema": "schema",
        "kinesis_firehose": "kinesisFirehose",
        "kinesis_stream": "kinesisStream",
        "parallelism": "parallelism",
        "processing_configuration": "processingConfiguration",
        "starting_position_configuration": "startingPositionConfiguration",
    },
)
class KinesisAnalyticsApplicationInputs:
    def __init__(
        self,
        *,
        name_prefix: builtins.str,
        schema: typing.Union["KinesisAnalyticsApplicationInputsSchema", typing.Dict[builtins.str, typing.Any]],
        kinesis_firehose: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsKinesisFirehose", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis_stream: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsKinesisStream", typing.Dict[builtins.str, typing.Any]]] = None,
        parallelism: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsParallelism", typing.Dict[builtins.str, typing.Any]]] = None,
        processing_configuration: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsProcessingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        starting_position_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationInputsStartingPositionConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#name_prefix KinesisAnalyticsApplication#name_prefix}.
        :param schema: schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#schema KinesisAnalyticsApplication#schema}
        :param kinesis_firehose: kinesis_firehose block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#kinesis_firehose KinesisAnalyticsApplication#kinesis_firehose}
        :param kinesis_stream: kinesis_stream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#kinesis_stream KinesisAnalyticsApplication#kinesis_stream}
        :param parallelism: parallelism block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#parallelism KinesisAnalyticsApplication#parallelism}
        :param processing_configuration: processing_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#processing_configuration KinesisAnalyticsApplication#processing_configuration}
        :param starting_position_configuration: starting_position_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#starting_position_configuration KinesisAnalyticsApplication#starting_position_configuration}
        '''
        if isinstance(schema, dict):
            schema = KinesisAnalyticsApplicationInputsSchema(**schema)
        if isinstance(kinesis_firehose, dict):
            kinesis_firehose = KinesisAnalyticsApplicationInputsKinesisFirehose(**kinesis_firehose)
        if isinstance(kinesis_stream, dict):
            kinesis_stream = KinesisAnalyticsApplicationInputsKinesisStream(**kinesis_stream)
        if isinstance(parallelism, dict):
            parallelism = KinesisAnalyticsApplicationInputsParallelism(**parallelism)
        if isinstance(processing_configuration, dict):
            processing_configuration = KinesisAnalyticsApplicationInputsProcessingConfiguration(**processing_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef6a433392e81ebdbe5f6f96194d08c71f8309cf06197c55d78617d5ba9e55f4)
            check_type(argname="argument name_prefix", value=name_prefix, expected_type=type_hints["name_prefix"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument kinesis_firehose", value=kinesis_firehose, expected_type=type_hints["kinesis_firehose"])
            check_type(argname="argument kinesis_stream", value=kinesis_stream, expected_type=type_hints["kinesis_stream"])
            check_type(argname="argument parallelism", value=parallelism, expected_type=type_hints["parallelism"])
            check_type(argname="argument processing_configuration", value=processing_configuration, expected_type=type_hints["processing_configuration"])
            check_type(argname="argument starting_position_configuration", value=starting_position_configuration, expected_type=type_hints["starting_position_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name_prefix": name_prefix,
            "schema": schema,
        }
        if kinesis_firehose is not None:
            self._values["kinesis_firehose"] = kinesis_firehose
        if kinesis_stream is not None:
            self._values["kinesis_stream"] = kinesis_stream
        if parallelism is not None:
            self._values["parallelism"] = parallelism
        if processing_configuration is not None:
            self._values["processing_configuration"] = processing_configuration
        if starting_position_configuration is not None:
            self._values["starting_position_configuration"] = starting_position_configuration

    @builtins.property
    def name_prefix(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#name_prefix KinesisAnalyticsApplication#name_prefix}.'''
        result = self._values.get("name_prefix")
        assert result is not None, "Required property 'name_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> "KinesisAnalyticsApplicationInputsSchema":
        '''schema block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#schema KinesisAnalyticsApplication#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast("KinesisAnalyticsApplicationInputsSchema", result)

    @builtins.property
    def kinesis_firehose(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationInputsKinesisFirehose"]:
        '''kinesis_firehose block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#kinesis_firehose KinesisAnalyticsApplication#kinesis_firehose}
        '''
        result = self._values.get("kinesis_firehose")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputsKinesisFirehose"], result)

    @builtins.property
    def kinesis_stream(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationInputsKinesisStream"]:
        '''kinesis_stream block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#kinesis_stream KinesisAnalyticsApplication#kinesis_stream}
        '''
        result = self._values.get("kinesis_stream")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputsKinesisStream"], result)

    @builtins.property
    def parallelism(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationInputsParallelism"]:
        '''parallelism block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#parallelism KinesisAnalyticsApplication#parallelism}
        '''
        result = self._values.get("parallelism")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputsParallelism"], result)

    @builtins.property
    def processing_configuration(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationInputsProcessingConfiguration"]:
        '''processing_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#processing_configuration KinesisAnalyticsApplication#processing_configuration}
        '''
        result = self._values.get("processing_configuration")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputsProcessingConfiguration"], result)

    @builtins.property
    def starting_position_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationInputsStartingPositionConfiguration"]]]:
        '''starting_position_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#starting_position_configuration KinesisAnalyticsApplication#starting_position_configuration}
        '''
        result = self._values.get("starting_position_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationInputsStartingPositionConfiguration"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsKinesisFirehose",
    jsii_struct_bases=[],
    name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
)
class KinesisAnalyticsApplicationInputsKinesisFirehose:
    def __init__(self, *, resource_arn: builtins.str, role_arn: builtins.str) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c13d8eabee723d5834b01929a820686107c1e9bb089467326e7f157667e6e02e)
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_arn": resource_arn,
            "role_arn": role_arn,
        }

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.'''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsKinesisFirehose(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationInputsKinesisFirehoseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsKinesisFirehoseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__801c4560404c27483f74ba3f29c3f7fd187ac0bbb9c3eacfb5e4a2c09ca38520)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resourceArnInput")
    def resource_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @resource_arn.setter
    def resource_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9d6f88c2efeb97c51bef3a8d0c0d0f0cdfb5ecc5a7ebcc3bba6a3e191a67f68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8476cd886f650140bcd35962c32256a55b3b32976437fd7c7ed4c8f676d3976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsKinesisFirehose]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsKinesisFirehose], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationInputsKinesisFirehose],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5a10e729493bcf538424e03ef0c9f390e80e8824c175c76000d39d791805221)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsKinesisStream",
    jsii_struct_bases=[],
    name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
)
class KinesisAnalyticsApplicationInputsKinesisStream:
    def __init__(self, *, resource_arn: builtins.str, role_arn: builtins.str) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c916b479a129f0e2564479cb95f66987e078abe9d8ef230f00c37a1c5059c5fb)
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_arn": resource_arn,
            "role_arn": role_arn,
        }

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.'''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsKinesisStream(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationInputsKinesisStreamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsKinesisStreamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1d47ed154f5a1b76c1d27056569aac1c1b7eb84e1de78bacc957b6719bd79b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resourceArnInput")
    def resource_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @resource_arn.setter
    def resource_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e98ddba1d6c05329675a7f8b0bc3e106baf8ede912496658050d907039aaf7ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e6703b4ac3cfababeb49375ba4b09dbae75cad01d70c2d6df76ca63bf8e9a22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsKinesisStream]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsKinesisStream], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationInputsKinesisStream],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a94d4b93dfadb61ea454b4befc3f268097e3a1ddd1c7de6c6c5c2988b10246)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KinesisAnalyticsApplicationInputsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60a17cf020bdcf864102304888c288381e6c9857fe8b569e556e0f877cc70e28)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putKinesisFirehose")
    def put_kinesis_firehose(
        self,
        *,
        resource_arn: builtins.str,
        role_arn: builtins.str,
    ) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        value = KinesisAnalyticsApplicationInputsKinesisFirehose(
            resource_arn=resource_arn, role_arn=role_arn
        )

        return typing.cast(None, jsii.invoke(self, "putKinesisFirehose", [value]))

    @jsii.member(jsii_name="putKinesisStream")
    def put_kinesis_stream(
        self,
        *,
        resource_arn: builtins.str,
        role_arn: builtins.str,
    ) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        value = KinesisAnalyticsApplicationInputsKinesisStream(
            resource_arn=resource_arn, role_arn=role_arn
        )

        return typing.cast(None, jsii.invoke(self, "putKinesisStream", [value]))

    @jsii.member(jsii_name="putParallelism")
    def put_parallelism(self, *, count: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#count KinesisAnalyticsApplication#count}.
        '''
        value = KinesisAnalyticsApplicationInputsParallelism(count=count)

        return typing.cast(None, jsii.invoke(self, "putParallelism", [value]))

    @jsii.member(jsii_name="putProcessingConfiguration")
    def put_processing_configuration(
        self,
        *,
        lambda_: typing.Union["KinesisAnalyticsApplicationInputsProcessingConfigurationLambda", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param lambda_: lambda block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#lambda KinesisAnalyticsApplication#lambda}
        '''
        value = KinesisAnalyticsApplicationInputsProcessingConfiguration(
            lambda_=lambda_
        )

        return typing.cast(None, jsii.invoke(self, "putProcessingConfiguration", [value]))

    @jsii.member(jsii_name="putSchema")
    def put_schema(
        self,
        *,
        record_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationInputsSchemaRecordColumns", typing.Dict[builtins.str, typing.Any]]]],
        record_format: typing.Union["KinesisAnalyticsApplicationInputsSchemaRecordFormat", typing.Dict[builtins.str, typing.Any]],
        record_encoding: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param record_columns: record_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_columns KinesisAnalyticsApplication#record_columns}
        :param record_format: record_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_format KinesisAnalyticsApplication#record_format}
        :param record_encoding: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_encoding KinesisAnalyticsApplication#record_encoding}.
        '''
        value = KinesisAnalyticsApplicationInputsSchema(
            record_columns=record_columns,
            record_format=record_format,
            record_encoding=record_encoding,
        )

        return typing.cast(None, jsii.invoke(self, "putSchema", [value]))

    @jsii.member(jsii_name="putStartingPositionConfiguration")
    def put_starting_position_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationInputsStartingPositionConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eff11d2639814152e11929e5a45dc047416075e00d45d1dbb43120b8c55d66f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStartingPositionConfiguration", [value]))

    @jsii.member(jsii_name="resetKinesisFirehose")
    def reset_kinesis_firehose(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesisFirehose", []))

    @jsii.member(jsii_name="resetKinesisStream")
    def reset_kinesis_stream(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesisStream", []))

    @jsii.member(jsii_name="resetParallelism")
    def reset_parallelism(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelism", []))

    @jsii.member(jsii_name="resetProcessingConfiguration")
    def reset_processing_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcessingConfiguration", []))

    @jsii.member(jsii_name="resetStartingPositionConfiguration")
    def reset_starting_position_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartingPositionConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="kinesisFirehose")
    def kinesis_firehose(
        self,
    ) -> KinesisAnalyticsApplicationInputsKinesisFirehoseOutputReference:
        return typing.cast(KinesisAnalyticsApplicationInputsKinesisFirehoseOutputReference, jsii.get(self, "kinesisFirehose"))

    @builtins.property
    @jsii.member(jsii_name="kinesisStream")
    def kinesis_stream(
        self,
    ) -> KinesisAnalyticsApplicationInputsKinesisStreamOutputReference:
        return typing.cast(KinesisAnalyticsApplicationInputsKinesisStreamOutputReference, jsii.get(self, "kinesisStream"))

    @builtins.property
    @jsii.member(jsii_name="parallelism")
    def parallelism(
        self,
    ) -> "KinesisAnalyticsApplicationInputsParallelismOutputReference":
        return typing.cast("KinesisAnalyticsApplicationInputsParallelismOutputReference", jsii.get(self, "parallelism"))

    @builtins.property
    @jsii.member(jsii_name="processingConfiguration")
    def processing_configuration(
        self,
    ) -> "KinesisAnalyticsApplicationInputsProcessingConfigurationOutputReference":
        return typing.cast("KinesisAnalyticsApplicationInputsProcessingConfigurationOutputReference", jsii.get(self, "processingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> "KinesisAnalyticsApplicationInputsSchemaOutputReference":
        return typing.cast("KinesisAnalyticsApplicationInputsSchemaOutputReference", jsii.get(self, "schema"))

    @builtins.property
    @jsii.member(jsii_name="startingPositionConfiguration")
    def starting_position_configuration(
        self,
    ) -> "KinesisAnalyticsApplicationInputsStartingPositionConfigurationList":
        return typing.cast("KinesisAnalyticsApplicationInputsStartingPositionConfigurationList", jsii.get(self, "startingPositionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="streamNames")
    def stream_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "streamNames"))

    @builtins.property
    @jsii.member(jsii_name="kinesisFirehoseInput")
    def kinesis_firehose_input(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsKinesisFirehose]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsKinesisFirehose], jsii.get(self, "kinesisFirehoseInput"))

    @builtins.property
    @jsii.member(jsii_name="kinesisStreamInput")
    def kinesis_stream_input(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsKinesisStream]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsKinesisStream], jsii.get(self, "kinesisStreamInput"))

    @builtins.property
    @jsii.member(jsii_name="namePrefixInput")
    def name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelismInput")
    def parallelism_input(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationInputsParallelism"]:
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputsParallelism"], jsii.get(self, "parallelismInput"))

    @builtins.property
    @jsii.member(jsii_name="processingConfigurationInput")
    def processing_configuration_input(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationInputsProcessingConfiguration"]:
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputsProcessingConfiguration"], jsii.get(self, "processingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationInputsSchema"]:
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputsSchema"], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="startingPositionConfigurationInput")
    def starting_position_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationInputsStartingPositionConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationInputsStartingPositionConfiguration"]]], jsii.get(self, "startingPositionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="namePrefix")
    def name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namePrefix"))

    @name_prefix.setter
    def name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99ac7b351c061d4fcb156521e53d0b08739d074e3f890abfed8ec75b7bbc7a83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KinesisAnalyticsApplicationInputs]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationInputs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b6218574e2918d3fb955a373608700c431aef0a26c2ef6b0ad257914565b9a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsParallelism",
    jsii_struct_bases=[],
    name_mapping={"count": "count"},
)
class KinesisAnalyticsApplicationInputsParallelism:
    def __init__(self, *, count: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#count KinesisAnalyticsApplication#count}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d464bc16627118debc2b19acfbcab7e258bd64b3163f05924dfc1f71d87434fc)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#count KinesisAnalyticsApplication#count}.'''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsParallelism(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationInputsParallelismOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsParallelismOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9b198877dcf96c6f4eb31bf05ec717d3dd4b3f5aec84acb387cd56d5ae8d274)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0de5211b2edff7942dd5500d64b65af81d72670ffc715b24860a5e7ab66a4435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsParallelism]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsParallelism], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationInputsParallelism],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f4407622c6b8bafd43de0cc65ce87f500757e5f4c06a88ff7178f4e2099ae6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsProcessingConfiguration",
    jsii_struct_bases=[],
    name_mapping={"lambda_": "lambda"},
)
class KinesisAnalyticsApplicationInputsProcessingConfiguration:
    def __init__(
        self,
        *,
        lambda_: typing.Union["KinesisAnalyticsApplicationInputsProcessingConfigurationLambda", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param lambda_: lambda block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#lambda KinesisAnalyticsApplication#lambda}
        '''
        if isinstance(lambda_, dict):
            lambda_ = KinesisAnalyticsApplicationInputsProcessingConfigurationLambda(**lambda_)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1725b7567300af1f5e968283dadb3aba5fa6d2958d61e3db7ca3648b7f04597)
            check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lambda_": lambda_,
        }

    @builtins.property
    def lambda_(
        self,
    ) -> "KinesisAnalyticsApplicationInputsProcessingConfigurationLambda":
        '''lambda block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#lambda KinesisAnalyticsApplication#lambda}
        '''
        result = self._values.get("lambda_")
        assert result is not None, "Required property 'lambda_' is missing"
        return typing.cast("KinesisAnalyticsApplicationInputsProcessingConfigurationLambda", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsProcessingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsProcessingConfigurationLambda",
    jsii_struct_bases=[],
    name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
)
class KinesisAnalyticsApplicationInputsProcessingConfigurationLambda:
    def __init__(self, *, resource_arn: builtins.str, role_arn: builtins.str) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7664cdf98ddfafcbd248308bf4682b39378422b9170d585eef15e9bd8883abde)
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_arn": resource_arn,
            "role_arn": role_arn,
        }

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.'''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsProcessingConfigurationLambda(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationInputsProcessingConfigurationLambdaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsProcessingConfigurationLambdaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47b0ba1385c25b2ffc6fcbe20ae0ada76c1bc163363e924054492238fff35913)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resourceArnInput")
    def resource_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @resource_arn.setter
    def resource_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b67fe80d7a70e3fa09b9cba3adaeecfbdac36813f043c3a6c5a6dfbe98207e43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb0beb90ba0c020e0ddf289ccab8fc4e5a6297a115ed166cc0c819c36c552a92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsProcessingConfigurationLambda]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsProcessingConfigurationLambda], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationInputsProcessingConfigurationLambda],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__291c711f5589173abad49a155550e64abe1c4857785ae02b8d3d85281f1b510f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KinesisAnalyticsApplicationInputsProcessingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsProcessingConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fa5ff22330a0079bf1ecfde5b810202a4e9be26ee364ee56773bd46dd57ba72)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLambda")
    def put_lambda(self, *, resource_arn: builtins.str, role_arn: builtins.str) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        value = KinesisAnalyticsApplicationInputsProcessingConfigurationLambda(
            resource_arn=resource_arn, role_arn=role_arn
        )

        return typing.cast(None, jsii.invoke(self, "putLambda", [value]))

    @builtins.property
    @jsii.member(jsii_name="lambda")
    def lambda_(
        self,
    ) -> KinesisAnalyticsApplicationInputsProcessingConfigurationLambdaOutputReference:
        return typing.cast(KinesisAnalyticsApplicationInputsProcessingConfigurationLambdaOutputReference, jsii.get(self, "lambda"))

    @builtins.property
    @jsii.member(jsii_name="lambdaInput")
    def lambda_input(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsProcessingConfigurationLambda]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsProcessingConfigurationLambda], jsii.get(self, "lambdaInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsProcessingConfiguration]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsProcessingConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationInputsProcessingConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6b057285593d75be495d0d30449e365c75d1c1ec679c5bc0601ee803513c788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchema",
    jsii_struct_bases=[],
    name_mapping={
        "record_columns": "recordColumns",
        "record_format": "recordFormat",
        "record_encoding": "recordEncoding",
    },
)
class KinesisAnalyticsApplicationInputsSchema:
    def __init__(
        self,
        *,
        record_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationInputsSchemaRecordColumns", typing.Dict[builtins.str, typing.Any]]]],
        record_format: typing.Union["KinesisAnalyticsApplicationInputsSchemaRecordFormat", typing.Dict[builtins.str, typing.Any]],
        record_encoding: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param record_columns: record_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_columns KinesisAnalyticsApplication#record_columns}
        :param record_format: record_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_format KinesisAnalyticsApplication#record_format}
        :param record_encoding: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_encoding KinesisAnalyticsApplication#record_encoding}.
        '''
        if isinstance(record_format, dict):
            record_format = KinesisAnalyticsApplicationInputsSchemaRecordFormat(**record_format)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1b091e028ac3a276eda411b6f6bce759116af4a7ac0dc4ed615328c3671449f)
            check_type(argname="argument record_columns", value=record_columns, expected_type=type_hints["record_columns"])
            check_type(argname="argument record_format", value=record_format, expected_type=type_hints["record_format"])
            check_type(argname="argument record_encoding", value=record_encoding, expected_type=type_hints["record_encoding"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "record_columns": record_columns,
            "record_format": record_format,
        }
        if record_encoding is not None:
            self._values["record_encoding"] = record_encoding

    @builtins.property
    def record_columns(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationInputsSchemaRecordColumns"]]:
        '''record_columns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_columns KinesisAnalyticsApplication#record_columns}
        '''
        result = self._values.get("record_columns")
        assert result is not None, "Required property 'record_columns' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationInputsSchemaRecordColumns"]], result)

    @builtins.property
    def record_format(self) -> "KinesisAnalyticsApplicationInputsSchemaRecordFormat":
        '''record_format block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_format KinesisAnalyticsApplication#record_format}
        '''
        result = self._values.get("record_format")
        assert result is not None, "Required property 'record_format' is missing"
        return typing.cast("KinesisAnalyticsApplicationInputsSchemaRecordFormat", result)

    @builtins.property
    def record_encoding(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_encoding KinesisAnalyticsApplication#record_encoding}.'''
        result = self._values.get("record_encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsSchema(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationInputsSchemaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00b533872fd223a32bfd584d659a2a3814469ef7a5d1b9264c56cc816894fa8c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRecordColumns")
    def put_record_columns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationInputsSchemaRecordColumns", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad31b38ef572532ea205258a545805b0ba713c641bff56b09ecb3979692599f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRecordColumns", [value]))

    @jsii.member(jsii_name="putRecordFormat")
    def put_record_format(
        self,
        *,
        mapping_parameters: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param mapping_parameters: mapping_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#mapping_parameters KinesisAnalyticsApplication#mapping_parameters}
        '''
        value = KinesisAnalyticsApplicationInputsSchemaRecordFormat(
            mapping_parameters=mapping_parameters
        )

        return typing.cast(None, jsii.invoke(self, "putRecordFormat", [value]))

    @jsii.member(jsii_name="resetRecordEncoding")
    def reset_record_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecordEncoding", []))

    @builtins.property
    @jsii.member(jsii_name="recordColumns")
    def record_columns(
        self,
    ) -> "KinesisAnalyticsApplicationInputsSchemaRecordColumnsList":
        return typing.cast("KinesisAnalyticsApplicationInputsSchemaRecordColumnsList", jsii.get(self, "recordColumns"))

    @builtins.property
    @jsii.member(jsii_name="recordFormat")
    def record_format(
        self,
    ) -> "KinesisAnalyticsApplicationInputsSchemaRecordFormatOutputReference":
        return typing.cast("KinesisAnalyticsApplicationInputsSchemaRecordFormatOutputReference", jsii.get(self, "recordFormat"))

    @builtins.property
    @jsii.member(jsii_name="recordColumnsInput")
    def record_columns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationInputsSchemaRecordColumns"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationInputsSchemaRecordColumns"]]], jsii.get(self, "recordColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="recordEncodingInput")
    def record_encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordEncodingInput"))

    @builtins.property
    @jsii.member(jsii_name="recordFormatInput")
    def record_format_input(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationInputsSchemaRecordFormat"]:
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputsSchemaRecordFormat"], jsii.get(self, "recordFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="recordEncoding")
    def record_encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordEncoding"))

    @record_encoding.setter
    def record_encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a77b06aad4c1791d85a4e7ced3f1d0ec4921517cfab9cb31444b1e524dad3d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordEncoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsSchema]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsSchema], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationInputsSchema],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__102ee02fd0f97ab768203dd312e9250c080dfea99ae3f9f1c4e00e890b3716b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaRecordColumns",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "sql_type": "sqlType", "mapping": "mapping"},
)
class KinesisAnalyticsApplicationInputsSchemaRecordColumns:
    def __init__(
        self,
        *,
        name: builtins.str,
        sql_type: builtins.str,
        mapping: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#name KinesisAnalyticsApplication#name}.
        :param sql_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#sql_type KinesisAnalyticsApplication#sql_type}.
        :param mapping: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#mapping KinesisAnalyticsApplication#mapping}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5890167aa814bd3070c07c8075611d8c75adff1eb2eef910b867e5f15e4e1cb9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sql_type", value=sql_type, expected_type=type_hints["sql_type"])
            check_type(argname="argument mapping", value=mapping, expected_type=type_hints["mapping"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "sql_type": sql_type,
        }
        if mapping is not None:
            self._values["mapping"] = mapping

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#name KinesisAnalyticsApplication#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sql_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#sql_type KinesisAnalyticsApplication#sql_type}.'''
        result = self._values.get("sql_type")
        assert result is not None, "Required property 'sql_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mapping(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#mapping KinesisAnalyticsApplication#mapping}.'''
        result = self._values.get("mapping")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsSchemaRecordColumns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationInputsSchemaRecordColumnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaRecordColumnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4ca7637395b69c827a305c7e2007bb8988b1e06302b2dd17d7bc0d2a1d4acc9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KinesisAnalyticsApplicationInputsSchemaRecordColumnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dca42dced15bbb2b9ef9c434245d25883cedb682a75289f13bf0af338dd057a8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KinesisAnalyticsApplicationInputsSchemaRecordColumnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64585c4923cd77fff9fc52ca8de12b0dca951954a8f437a0e84413bbf3228fa6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c8d3dc70e2f9a5da0491709b6d79fcd7ada5b2d563b67b38e751318dbf4436f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9f8a9c121ecd2ccf8c387b8740bf2a74ec10539a4f5ab8f1b0979e92b775bcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationInputsSchemaRecordColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationInputsSchemaRecordColumns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationInputsSchemaRecordColumns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__400902fdba4ae7bba98e7a4a2e6653897d3000dd06d79144da33574b880f2610)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KinesisAnalyticsApplicationInputsSchemaRecordColumnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaRecordColumnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f48651006dbb9324b5cd5a118feb0b7616786b2c7a08481be747186f20ed4c9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMapping")
    def reset_mapping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMapping", []))

    @builtins.property
    @jsii.member(jsii_name="mappingInput")
    def mapping_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mappingInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlTypeInput")
    def sql_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="mapping")
    def mapping(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mapping"))

    @mapping.setter
    def mapping(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ac3b096fcb1f5eff4aed032679e6c2661c0c6aa83a320f68d073d3e10c96b54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c645f71118b88c4ae018b913d75cf2e99ba3cc1ab5748f80f005df2881c4a9ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlType")
    def sql_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlType"))

    @sql_type.setter
    def sql_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb15fb7f8cbd3b26b11e9c4a51b7ca8314d96a3ca729466c9f5664b6353775cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationInputsSchemaRecordColumns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationInputsSchemaRecordColumns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationInputsSchemaRecordColumns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a081bd6380080e691911dd4efe7d0a39643b7263599ae2e5f5e6b865313615b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaRecordFormat",
    jsii_struct_bases=[],
    name_mapping={"mapping_parameters": "mappingParameters"},
)
class KinesisAnalyticsApplicationInputsSchemaRecordFormat:
    def __init__(
        self,
        *,
        mapping_parameters: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param mapping_parameters: mapping_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#mapping_parameters KinesisAnalyticsApplication#mapping_parameters}
        '''
        if isinstance(mapping_parameters, dict):
            mapping_parameters = KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters(**mapping_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e35de60531b0a6ffec3fcd81aad9212e8be7248c6e06adf98420c636b78a3f23)
            check_type(argname="argument mapping_parameters", value=mapping_parameters, expected_type=type_hints["mapping_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mapping_parameters is not None:
            self._values["mapping_parameters"] = mapping_parameters

    @builtins.property
    def mapping_parameters(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters"]:
        '''mapping_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#mapping_parameters KinesisAnalyticsApplication#mapping_parameters}
        '''
        result = self._values.get("mapping_parameters")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsSchemaRecordFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters",
    jsii_struct_bases=[],
    name_mapping={"csv": "csv", "json": "json"},
)
class KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters:
    def __init__(
        self,
        *,
        csv: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv", typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param csv: csv block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#csv KinesisAnalyticsApplication#csv}
        :param json: json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#json KinesisAnalyticsApplication#json}
        '''
        if isinstance(csv, dict):
            csv = KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv(**csv)
        if isinstance(json, dict):
            json = KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson(**json)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2829c3d55e1ca8b72d64f9d8a21f16c1bc8e52382aee26b8bf55bbdf27083441)
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
    ) -> typing.Optional["KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv"]:
        '''csv block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#csv KinesisAnalyticsApplication#csv}
        '''
        result = self._values.get("csv")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv"], result)

    @builtins.property
    def json(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson"]:
        '''json block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#json KinesisAnalyticsApplication#json}
        '''
        result = self._values.get("json")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv",
    jsii_struct_bases=[],
    name_mapping={
        "record_column_delimiter": "recordColumnDelimiter",
        "record_row_delimiter": "recordRowDelimiter",
    },
)
class KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv:
    def __init__(
        self,
        *,
        record_column_delimiter: builtins.str,
        record_row_delimiter: builtins.str,
    ) -> None:
        '''
        :param record_column_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_column_delimiter KinesisAnalyticsApplication#record_column_delimiter}.
        :param record_row_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_row_delimiter KinesisAnalyticsApplication#record_row_delimiter}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a78fec386106e5123fb35b057363b98a3535966564d726451f149db4104121f5)
            check_type(argname="argument record_column_delimiter", value=record_column_delimiter, expected_type=type_hints["record_column_delimiter"])
            check_type(argname="argument record_row_delimiter", value=record_row_delimiter, expected_type=type_hints["record_row_delimiter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "record_column_delimiter": record_column_delimiter,
            "record_row_delimiter": record_row_delimiter,
        }

    @builtins.property
    def record_column_delimiter(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_column_delimiter KinesisAnalyticsApplication#record_column_delimiter}.'''
        result = self._values.get("record_column_delimiter")
        assert result is not None, "Required property 'record_column_delimiter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def record_row_delimiter(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_row_delimiter KinesisAnalyticsApplication#record_row_delimiter}.'''
        result = self._values.get("record_row_delimiter")
        assert result is not None, "Required property 'record_row_delimiter' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsvOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsvOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10c847fecc381bf51220db333a46e9ff1afdf3e3b73107464531a93c6bbfd08b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="recordColumnDelimiterInput")
    def record_column_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordColumnDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="recordRowDelimiterInput")
    def record_row_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordRowDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="recordColumnDelimiter")
    def record_column_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordColumnDelimiter"))

    @record_column_delimiter.setter
    def record_column_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94d64d2d4498274d14db4eb695f965aa952329ff7fb656c58b576033732f123f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordColumnDelimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recordRowDelimiter")
    def record_row_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordRowDelimiter"))

    @record_row_delimiter.setter
    def record_row_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8f8a761f5047c1203121a1b0511a73abf1531bc4f361cbe89ba8e76416a8b32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordRowDelimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beb042e53f1fa2b0a8127761c995bf5a89ab5121476f2e31ba4c739a080566b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson",
    jsii_struct_bases=[],
    name_mapping={"record_row_path": "recordRowPath"},
)
class KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson:
    def __init__(self, *, record_row_path: builtins.str) -> None:
        '''
        :param record_row_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_row_path KinesisAnalyticsApplication#record_row_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48bbfa38f8712d6f10670573ef4c6d56da775bf160642f3d47e9ada9363ac460)
            check_type(argname="argument record_row_path", value=record_row_path, expected_type=type_hints["record_row_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "record_row_path": record_row_path,
        }

    @builtins.property
    def record_row_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_row_path KinesisAnalyticsApplication#record_row_path}.'''
        result = self._values.get("record_row_path")
        assert result is not None, "Required property 'record_row_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJsonOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJsonOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e74afdb3d0a7a5488ebeeadd913594dee0485259e198f7c282eba4b95db5abf7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="recordRowPathInput")
    def record_row_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordRowPathInput"))

    @builtins.property
    @jsii.member(jsii_name="recordRowPath")
    def record_row_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordRowPath"))

    @record_row_path.setter
    def record_row_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8d7d4ac18676296c54882b243e039f2006c7e6b53bcdac5e1340785aaf2a10b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordRowPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0645e0fe45f8948792107d5c836ccf3f0442db63a9cb8c7194f85a5b30171d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfa187c917d2b084ca181b5b8ac3bc2e66164444d9525428167a81421c9be072)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCsv")
    def put_csv(
        self,
        *,
        record_column_delimiter: builtins.str,
        record_row_delimiter: builtins.str,
    ) -> None:
        '''
        :param record_column_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_column_delimiter KinesisAnalyticsApplication#record_column_delimiter}.
        :param record_row_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_row_delimiter KinesisAnalyticsApplication#record_row_delimiter}.
        '''
        value = KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv(
            record_column_delimiter=record_column_delimiter,
            record_row_delimiter=record_row_delimiter,
        )

        return typing.cast(None, jsii.invoke(self, "putCsv", [value]))

    @jsii.member(jsii_name="putJson")
    def put_json(self, *, record_row_path: builtins.str) -> None:
        '''
        :param record_row_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_row_path KinesisAnalyticsApplication#record_row_path}.
        '''
        value = KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson(
            record_row_path=record_row_path
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
    ) -> KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsvOutputReference:
        return typing.cast(KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsvOutputReference, jsii.get(self, "csv"))

    @builtins.property
    @jsii.member(jsii_name="json")
    def json(
        self,
    ) -> KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJsonOutputReference:
        return typing.cast(KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJsonOutputReference, jsii.get(self, "json"))

    @builtins.property
    @jsii.member(jsii_name="csvInput")
    def csv_input(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv], jsii.get(self, "csvInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonInput")
    def json_input(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson], jsii.get(self, "jsonInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f250ddae6948e306b6ce50d5790eec025c5a2cf81c0397e541f96c4f7d23a03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KinesisAnalyticsApplicationInputsSchemaRecordFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaRecordFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e101afce70412221d190408a11ef9459de148120488a2a2a903bb85a1274a71d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMappingParameters")
    def put_mapping_parameters(
        self,
        *,
        csv: typing.Optional[typing.Union[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv, typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param csv: csv block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#csv KinesisAnalyticsApplication#csv}
        :param json: json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#json KinesisAnalyticsApplication#json}
        '''
        value = KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters(
            csv=csv, json=json
        )

        return typing.cast(None, jsii.invoke(self, "putMappingParameters", [value]))

    @jsii.member(jsii_name="resetMappingParameters")
    def reset_mapping_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMappingParameters", []))

    @builtins.property
    @jsii.member(jsii_name="mappingParameters")
    def mapping_parameters(
        self,
    ) -> KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersOutputReference:
        return typing.cast(KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersOutputReference, jsii.get(self, "mappingParameters"))

    @builtins.property
    @jsii.member(jsii_name="recordFormatType")
    def record_format_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordFormatType"))

    @builtins.property
    @jsii.member(jsii_name="mappingParametersInput")
    def mapping_parameters_input(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters], jsii.get(self, "mappingParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormat]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__888e78309d640d7c9d0c9ddfb66d9521dc754e45abbc592f55dda0c0acc312d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsStartingPositionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"starting_position": "startingPosition"},
)
class KinesisAnalyticsApplicationInputsStartingPositionConfiguration:
    def __init__(
        self,
        *,
        starting_position: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param starting_position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#starting_position KinesisAnalyticsApplication#starting_position}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5ed85bbc816bc1568d1c1237580b55929d4b5c864fd9bc3ae8e0c11399ba333)
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if starting_position is not None:
            self._values["starting_position"] = starting_position

    @builtins.property
    def starting_position(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#starting_position KinesisAnalyticsApplication#starting_position}.'''
        result = self._values.get("starting_position")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsStartingPositionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationInputsStartingPositionConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsStartingPositionConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc8c1cb6f0ab8502c7ab9ec45288c0c2d1197c6e652266ebfcd1a7fd48c62a4c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KinesisAnalyticsApplicationInputsStartingPositionConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60cb183a2f670a7b4e010665f60f9ca5dc8cb94db6821ec322f1959f307cfc53)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KinesisAnalyticsApplicationInputsStartingPositionConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c0ea6eec7fcb0f92cd4b50fe011cb8403f68502e79f48dbf4fe7abf8545b689)
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
            type_hints = typing.get_type_hints(_typecheckingstub__541afa535cf83f0adbc11ddee49691811ff2201ba852e785f84dfe5b10f9b85d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2eca98f2c14a3525f95fd30bfe6de7d637766063c4ed27ced6842e7de677bf8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationInputsStartingPositionConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationInputsStartingPositionConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationInputsStartingPositionConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c26b738fa9f891047d337d12905daef38a86423c48593e3e58cad637b385c4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KinesisAnalyticsApplicationInputsStartingPositionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsStartingPositionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c31b232bcaaa2f64ca23205cd28f2b87cee7d65db6057c500c6c0143313e0f3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetStartingPosition")
    def reset_starting_position(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartingPosition", []))

    @builtins.property
    @jsii.member(jsii_name="startingPositionInput")
    def starting_position_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startingPositionInput"))

    @builtins.property
    @jsii.member(jsii_name="startingPosition")
    def starting_position(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startingPosition"))

    @starting_position.setter
    def starting_position(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c07ea3cb19abcd1e6ee33936f0ef50083777824ec4f38c31c0dc4fb956ec7700)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startingPosition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationInputsStartingPositionConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationInputsStartingPositionConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationInputsStartingPositionConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40227226e92eda3eed46b4dd5e0e2f89524910339ed19c8d8c0ab7260be629f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationOutputs",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "schema": "schema",
        "kinesis_firehose": "kinesisFirehose",
        "kinesis_stream": "kinesisStream",
        "lambda_": "lambda",
    },
)
class KinesisAnalyticsApplicationOutputs:
    def __init__(
        self,
        *,
        name: builtins.str,
        schema: typing.Union["KinesisAnalyticsApplicationOutputsSchema", typing.Dict[builtins.str, typing.Any]],
        kinesis_firehose: typing.Optional[typing.Union["KinesisAnalyticsApplicationOutputsKinesisFirehose", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis_stream: typing.Optional[typing.Union["KinesisAnalyticsApplicationOutputsKinesisStream", typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_: typing.Optional[typing.Union["KinesisAnalyticsApplicationOutputsLambda", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#name KinesisAnalyticsApplication#name}.
        :param schema: schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#schema KinesisAnalyticsApplication#schema}
        :param kinesis_firehose: kinesis_firehose block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#kinesis_firehose KinesisAnalyticsApplication#kinesis_firehose}
        :param kinesis_stream: kinesis_stream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#kinesis_stream KinesisAnalyticsApplication#kinesis_stream}
        :param lambda_: lambda block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#lambda KinesisAnalyticsApplication#lambda}
        '''
        if isinstance(schema, dict):
            schema = KinesisAnalyticsApplicationOutputsSchema(**schema)
        if isinstance(kinesis_firehose, dict):
            kinesis_firehose = KinesisAnalyticsApplicationOutputsKinesisFirehose(**kinesis_firehose)
        if isinstance(kinesis_stream, dict):
            kinesis_stream = KinesisAnalyticsApplicationOutputsKinesisStream(**kinesis_stream)
        if isinstance(lambda_, dict):
            lambda_ = KinesisAnalyticsApplicationOutputsLambda(**lambda_)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14aacc0b4ffa736ee336eb6147ed6b0c50a9c4301004632523080d61b97b1d3b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument kinesis_firehose", value=kinesis_firehose, expected_type=type_hints["kinesis_firehose"])
            check_type(argname="argument kinesis_stream", value=kinesis_stream, expected_type=type_hints["kinesis_stream"])
            check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "schema": schema,
        }
        if kinesis_firehose is not None:
            self._values["kinesis_firehose"] = kinesis_firehose
        if kinesis_stream is not None:
            self._values["kinesis_stream"] = kinesis_stream
        if lambda_ is not None:
            self._values["lambda_"] = lambda_

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#name KinesisAnalyticsApplication#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> "KinesisAnalyticsApplicationOutputsSchema":
        '''schema block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#schema KinesisAnalyticsApplication#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast("KinesisAnalyticsApplicationOutputsSchema", result)

    @builtins.property
    def kinesis_firehose(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationOutputsKinesisFirehose"]:
        '''kinesis_firehose block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#kinesis_firehose KinesisAnalyticsApplication#kinesis_firehose}
        '''
        result = self._values.get("kinesis_firehose")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationOutputsKinesisFirehose"], result)

    @builtins.property
    def kinesis_stream(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationOutputsKinesisStream"]:
        '''kinesis_stream block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#kinesis_stream KinesisAnalyticsApplication#kinesis_stream}
        '''
        result = self._values.get("kinesis_stream")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationOutputsKinesisStream"], result)

    @builtins.property
    def lambda_(self) -> typing.Optional["KinesisAnalyticsApplicationOutputsLambda"]:
        '''lambda block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#lambda KinesisAnalyticsApplication#lambda}
        '''
        result = self._values.get("lambda_")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationOutputsLambda"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationOutputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationOutputsKinesisFirehose",
    jsii_struct_bases=[],
    name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
)
class KinesisAnalyticsApplicationOutputsKinesisFirehose:
    def __init__(self, *, resource_arn: builtins.str, role_arn: builtins.str) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0bd33ab6599ed3bf8c76e168bfe5191c6e1cac0de2ba26ef06a357cba8b23ab)
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_arn": resource_arn,
            "role_arn": role_arn,
        }

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.'''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationOutputsKinesisFirehose(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationOutputsKinesisFirehoseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationOutputsKinesisFirehoseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59f4d57772da694f523bcb2e32c6677c444bf462fcbe03eb1e669695b8eee61f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resourceArnInput")
    def resource_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @resource_arn.setter
    def resource_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5950452d01e31fbf1092e0f0b62a8edbc335d2f81bd1e22c135b7271d503e85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f8b753101f57ff14c503d82fdfa82c1c07166f6e48e8c9e4f641f9170c795e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationOutputsKinesisFirehose]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationOutputsKinesisFirehose], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationOutputsKinesisFirehose],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aba0b5fe0812659166fc7890cfc6df32943cdca7698296528a2ebf1121b97a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationOutputsKinesisStream",
    jsii_struct_bases=[],
    name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
)
class KinesisAnalyticsApplicationOutputsKinesisStream:
    def __init__(self, *, resource_arn: builtins.str, role_arn: builtins.str) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd8794e5aae52d6aeebafe7df2af47d0591c54e72938bbbce124bfbb8fa7c71c)
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_arn": resource_arn,
            "role_arn": role_arn,
        }

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.'''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationOutputsKinesisStream(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationOutputsKinesisStreamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationOutputsKinesisStreamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f34a2caf0dfc58c7aa7c5fb6f9c37c32b5b12eb7802004716772d3e2e4ef706)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resourceArnInput")
    def resource_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @resource_arn.setter
    def resource_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09d96a14c0cf540e380bfcdb9257e1510f661a17b307fd0d5bf8ebf478ee05e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1953324cfb14d5c1304d197da60dda8746c065fefef134f5348cfade27f6a539)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationOutputsKinesisStream]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationOutputsKinesisStream], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationOutputsKinesisStream],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bf141d37c4e0019f3b66fcb070742f4127637f306d283601da156bee4ada9fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationOutputsLambda",
    jsii_struct_bases=[],
    name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
)
class KinesisAnalyticsApplicationOutputsLambda:
    def __init__(self, *, resource_arn: builtins.str, role_arn: builtins.str) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bb77c7a7d26d0d63b9c3a4ed029ef94e166706fe45d4e894587b1f05abefb12)
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_arn": resource_arn,
            "role_arn": role_arn,
        }

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.'''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationOutputsLambda(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationOutputsLambdaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationOutputsLambdaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__711b559e331acf671fe6b32c2dda8d7ebbe7d3e4f77cf49d6f4c5761301fe868)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resourceArnInput")
    def resource_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @resource_arn.setter
    def resource_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7008da51159af9e73983f0849306c7c0b6ef0d2f57781e8bbd673a4a9bbe86bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9806c3de0d4d91a656a4815d870d0f1042ff67d508fc86e234ce66a5eb57ade9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationOutputsLambda]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationOutputsLambda], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationOutputsLambda],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b13e808e969196bdd14991ad847d0e9baae884469bbdcffe719e33e9afe30ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KinesisAnalyticsApplicationOutputsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationOutputsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c96ce66f55ef546f64477d3844bb999f626f2e2929964e1d0f30ee79e4417ee0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KinesisAnalyticsApplicationOutputsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaf45268a4e56b2619eebeb0fc02a9d63c00a533dd466c2c830284012bdf2b0f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KinesisAnalyticsApplicationOutputsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cab46d923e99e41c52e9ab5dada5311fb50573916680ea1a47c148758ea45b41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__58189701db44984f17ac2783bf30c85320d839629ce40a5c8b917b13dec81cc9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9aac40598e1b10172708fdb4805d50dccad6211374a4fe38014a672a770e857a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationOutputs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationOutputs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationOutputs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0859f97b93e61a4129c55e74f68a0974a1047cfaeaa14b5a92d486068309a4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KinesisAnalyticsApplicationOutputsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationOutputsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e976141fb524f97dadd6db0f8a8f312af6536d8bfa6c6c46ec19aa1bf38dbd55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putKinesisFirehose")
    def put_kinesis_firehose(
        self,
        *,
        resource_arn: builtins.str,
        role_arn: builtins.str,
    ) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        value = KinesisAnalyticsApplicationOutputsKinesisFirehose(
            resource_arn=resource_arn, role_arn=role_arn
        )

        return typing.cast(None, jsii.invoke(self, "putKinesisFirehose", [value]))

    @jsii.member(jsii_name="putKinesisStream")
    def put_kinesis_stream(
        self,
        *,
        resource_arn: builtins.str,
        role_arn: builtins.str,
    ) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        value = KinesisAnalyticsApplicationOutputsKinesisStream(
            resource_arn=resource_arn, role_arn=role_arn
        )

        return typing.cast(None, jsii.invoke(self, "putKinesisStream", [value]))

    @jsii.member(jsii_name="putLambda")
    def put_lambda(self, *, resource_arn: builtins.str, role_arn: builtins.str) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        value = KinesisAnalyticsApplicationOutputsLambda(
            resource_arn=resource_arn, role_arn=role_arn
        )

        return typing.cast(None, jsii.invoke(self, "putLambda", [value]))

    @jsii.member(jsii_name="putSchema")
    def put_schema(self, *, record_format_type: builtins.str) -> None:
        '''
        :param record_format_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_format_type KinesisAnalyticsApplication#record_format_type}.
        '''
        value = KinesisAnalyticsApplicationOutputsSchema(
            record_format_type=record_format_type
        )

        return typing.cast(None, jsii.invoke(self, "putSchema", [value]))

    @jsii.member(jsii_name="resetKinesisFirehose")
    def reset_kinesis_firehose(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesisFirehose", []))

    @jsii.member(jsii_name="resetKinesisStream")
    def reset_kinesis_stream(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesisStream", []))

    @jsii.member(jsii_name="resetLambda")
    def reset_lambda(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambda", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="kinesisFirehose")
    def kinesis_firehose(
        self,
    ) -> KinesisAnalyticsApplicationOutputsKinesisFirehoseOutputReference:
        return typing.cast(KinesisAnalyticsApplicationOutputsKinesisFirehoseOutputReference, jsii.get(self, "kinesisFirehose"))

    @builtins.property
    @jsii.member(jsii_name="kinesisStream")
    def kinesis_stream(
        self,
    ) -> KinesisAnalyticsApplicationOutputsKinesisStreamOutputReference:
        return typing.cast(KinesisAnalyticsApplicationOutputsKinesisStreamOutputReference, jsii.get(self, "kinesisStream"))

    @builtins.property
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> KinesisAnalyticsApplicationOutputsLambdaOutputReference:
        return typing.cast(KinesisAnalyticsApplicationOutputsLambdaOutputReference, jsii.get(self, "lambda"))

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> "KinesisAnalyticsApplicationOutputsSchemaOutputReference":
        return typing.cast("KinesisAnalyticsApplicationOutputsSchemaOutputReference", jsii.get(self, "schema"))

    @builtins.property
    @jsii.member(jsii_name="kinesisFirehoseInput")
    def kinesis_firehose_input(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationOutputsKinesisFirehose]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationOutputsKinesisFirehose], jsii.get(self, "kinesisFirehoseInput"))

    @builtins.property
    @jsii.member(jsii_name="kinesisStreamInput")
    def kinesis_stream_input(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationOutputsKinesisStream]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationOutputsKinesisStream], jsii.get(self, "kinesisStreamInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaInput")
    def lambda_input(self) -> typing.Optional[KinesisAnalyticsApplicationOutputsLambda]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationOutputsLambda], jsii.get(self, "lambdaInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationOutputsSchema"]:
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationOutputsSchema"], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acdd731b009597a4dff303532a9c45ff6b3b55e900bcd14adfd8c0a319beae63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationOutputs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationOutputs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationOutputs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__990afbcedd563cf440182c8d197be8c701e0ff129a13bd7a6f4aed4ea8c089e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationOutputsSchema",
    jsii_struct_bases=[],
    name_mapping={"record_format_type": "recordFormatType"},
)
class KinesisAnalyticsApplicationOutputsSchema:
    def __init__(self, *, record_format_type: builtins.str) -> None:
        '''
        :param record_format_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_format_type KinesisAnalyticsApplication#record_format_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9be3443f7f78bc54c7740c71db98725d7c6514134c3411123f42a6c350f8b1d)
            check_type(argname="argument record_format_type", value=record_format_type, expected_type=type_hints["record_format_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "record_format_type": record_format_type,
        }

    @builtins.property
    def record_format_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_format_type KinesisAnalyticsApplication#record_format_type}.'''
        result = self._values.get("record_format_type")
        assert result is not None, "Required property 'record_format_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationOutputsSchema(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationOutputsSchemaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationOutputsSchemaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0943865d7c29a3b87b59e768c814520c2f8241589921cfdf3f74dfbde1778207)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="recordFormatTypeInput")
    def record_format_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordFormatTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="recordFormatType")
    def record_format_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordFormatType"))

    @record_format_type.setter
    def record_format_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1cb425ec1dc1c3e77a3ae08c1d39366c9c33fa8845734e09fc32fb1ee34e3c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordFormatType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationOutputsSchema]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationOutputsSchema], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationOutputsSchema],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a0bc1f2c6980efd9966adf90568d782525f2c3850e1f24aef48524c5f62de19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSources",
    jsii_struct_bases=[],
    name_mapping={"s3": "s3", "schema": "schema", "table_name": "tableName"},
)
class KinesisAnalyticsApplicationReferenceDataSources:
    def __init__(
        self,
        *,
        s3: typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesS3", typing.Dict[builtins.str, typing.Any]],
        schema: typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesSchema", typing.Dict[builtins.str, typing.Any]],
        table_name: builtins.str,
    ) -> None:
        '''
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#s3 KinesisAnalyticsApplication#s3}
        :param schema: schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#schema KinesisAnalyticsApplication#schema}
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#table_name KinesisAnalyticsApplication#table_name}.
        '''
        if isinstance(s3, dict):
            s3 = KinesisAnalyticsApplicationReferenceDataSourcesS3(**s3)
        if isinstance(schema, dict):
            schema = KinesisAnalyticsApplicationReferenceDataSourcesSchema(**schema)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__687431bc283aab9ba01cc33681de0aa7239e13498a62a6527371a79bdab8f495)
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3": s3,
            "schema": schema,
            "table_name": table_name,
        }

    @builtins.property
    def s3(self) -> "KinesisAnalyticsApplicationReferenceDataSourcesS3":
        '''s3 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#s3 KinesisAnalyticsApplication#s3}
        '''
        result = self._values.get("s3")
        assert result is not None, "Required property 's3' is missing"
        return typing.cast("KinesisAnalyticsApplicationReferenceDataSourcesS3", result)

    @builtins.property
    def schema(self) -> "KinesisAnalyticsApplicationReferenceDataSourcesSchema":
        '''schema block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#schema KinesisAnalyticsApplication#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast("KinesisAnalyticsApplicationReferenceDataSourcesSchema", result)

    @builtins.property
    def table_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#table_name KinesisAnalyticsApplication#table_name}.'''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationReferenceDataSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationReferenceDataSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3e509c3476c3a1a98e8ba01619efce26dd9a2ed3c934b959eacbdfac61d1c53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putS3")
    def put_s3(
        self,
        *,
        bucket_arn: builtins.str,
        file_key: builtins.str,
        role_arn: builtins.str,
    ) -> None:
        '''
        :param bucket_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#bucket_arn KinesisAnalyticsApplication#bucket_arn}.
        :param file_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#file_key KinesisAnalyticsApplication#file_key}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        value = KinesisAnalyticsApplicationReferenceDataSourcesS3(
            bucket_arn=bucket_arn, file_key=file_key, role_arn=role_arn
        )

        return typing.cast(None, jsii.invoke(self, "putS3", [value]))

    @jsii.member(jsii_name="putSchema")
    def put_schema(
        self,
        *,
        record_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns", typing.Dict[builtins.str, typing.Any]]]],
        record_format: typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat", typing.Dict[builtins.str, typing.Any]],
        record_encoding: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param record_columns: record_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_columns KinesisAnalyticsApplication#record_columns}
        :param record_format: record_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_format KinesisAnalyticsApplication#record_format}
        :param record_encoding: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_encoding KinesisAnalyticsApplication#record_encoding}.
        '''
        value = KinesisAnalyticsApplicationReferenceDataSourcesSchema(
            record_columns=record_columns,
            record_format=record_format,
            record_encoding=record_encoding,
        )

        return typing.cast(None, jsii.invoke(self, "putSchema", [value]))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="s3")
    def s3(self) -> "KinesisAnalyticsApplicationReferenceDataSourcesS3OutputReference":
        return typing.cast("KinesisAnalyticsApplicationReferenceDataSourcesS3OutputReference", jsii.get(self, "s3"))

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(
        self,
    ) -> "KinesisAnalyticsApplicationReferenceDataSourcesSchemaOutputReference":
        return typing.cast("KinesisAnalyticsApplicationReferenceDataSourcesSchemaOutputReference", jsii.get(self, "schema"))

    @builtins.property
    @jsii.member(jsii_name="s3Input")
    def s3_input(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesS3"]:
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesS3"], jsii.get(self, "s3Input"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesSchema"]:
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesSchema"], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b4c2b5d2ceffec6c873eb261e80d04605b60dd214989246bfdaf354256b37b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationReferenceDataSources]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationReferenceDataSources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e717d0e2e2f997889e02e46c95af70d27a75a14ea9c8c09e136cd33c54404a00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesS3",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_arn": "bucketArn",
        "file_key": "fileKey",
        "role_arn": "roleArn",
    },
)
class KinesisAnalyticsApplicationReferenceDataSourcesS3:
    def __init__(
        self,
        *,
        bucket_arn: builtins.str,
        file_key: builtins.str,
        role_arn: builtins.str,
    ) -> None:
        '''
        :param bucket_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#bucket_arn KinesisAnalyticsApplication#bucket_arn}.
        :param file_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#file_key KinesisAnalyticsApplication#file_key}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4527d006c73958bd5b0607f7705d4798229dd6fb0feb13dde39169bf7720e10)
            check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
            check_type(argname="argument file_key", value=file_key, expected_type=type_hints["file_key"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_arn": bucket_arn,
            "file_key": file_key,
            "role_arn": role_arn,
        }

    @builtins.property
    def bucket_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#bucket_arn KinesisAnalyticsApplication#bucket_arn}.'''
        result = self._values.get("bucket_arn")
        assert result is not None, "Required property 'bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def file_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#file_key KinesisAnalyticsApplication#file_key}.'''
        result = self._values.get("file_key")
        assert result is not None, "Required property 'file_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationReferenceDataSourcesS3(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationReferenceDataSourcesS3OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesS3OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93e8997bcc285c60baf8ce8d207cdc03c5e1b3a65c1ed6e992f43b1052ce4973)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="bucketArnInput")
    def bucket_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketArnInput"))

    @builtins.property
    @jsii.member(jsii_name="fileKeyInput")
    def file_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketArn"))

    @bucket_arn.setter
    def bucket_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fda44dd7d463bfce71383cc561cdf8a1a9c24ac4211069ad33bef1e0427b4e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileKey")
    def file_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileKey"))

    @file_key.setter
    def file_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f646e03d346a2b96477d100ac4cc7b715d8a03ef24e9d7ef40e31205f804048c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a754888f53ef393ce9f42ac061f53a10b123296746262a3ba0b58f673cd3d40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesS3]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesS3], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesS3],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9fbca70b8d0d6a0db713232fb154c0b8bf91fc25e746ba529453a3eff7b2676)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchema",
    jsii_struct_bases=[],
    name_mapping={
        "record_columns": "recordColumns",
        "record_format": "recordFormat",
        "record_encoding": "recordEncoding",
    },
)
class KinesisAnalyticsApplicationReferenceDataSourcesSchema:
    def __init__(
        self,
        *,
        record_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns", typing.Dict[builtins.str, typing.Any]]]],
        record_format: typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat", typing.Dict[builtins.str, typing.Any]],
        record_encoding: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param record_columns: record_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_columns KinesisAnalyticsApplication#record_columns}
        :param record_format: record_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_format KinesisAnalyticsApplication#record_format}
        :param record_encoding: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_encoding KinesisAnalyticsApplication#record_encoding}.
        '''
        if isinstance(record_format, dict):
            record_format = KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat(**record_format)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b8993e1581615fd98d8d4874dfbecff32559648790e9232ab7772717a82725a)
            check_type(argname="argument record_columns", value=record_columns, expected_type=type_hints["record_columns"])
            check_type(argname="argument record_format", value=record_format, expected_type=type_hints["record_format"])
            check_type(argname="argument record_encoding", value=record_encoding, expected_type=type_hints["record_encoding"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "record_columns": record_columns,
            "record_format": record_format,
        }
        if record_encoding is not None:
            self._values["record_encoding"] = record_encoding

    @builtins.property
    def record_columns(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns"]]:
        '''record_columns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_columns KinesisAnalyticsApplication#record_columns}
        '''
        result = self._values.get("record_columns")
        assert result is not None, "Required property 'record_columns' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns"]], result)

    @builtins.property
    def record_format(
        self,
    ) -> "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat":
        '''record_format block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_format KinesisAnalyticsApplication#record_format}
        '''
        result = self._values.get("record_format")
        assert result is not None, "Required property 'record_format' is missing"
        return typing.cast("KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat", result)

    @builtins.property
    def record_encoding(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_encoding KinesisAnalyticsApplication#record_encoding}.'''
        result = self._values.get("record_encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationReferenceDataSourcesSchema(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationReferenceDataSourcesSchemaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de0914871541b83b59af5e906013ef37e4a1454f67dafd2b15d3a44b8716f539)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRecordColumns")
    def put_record_columns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4abae0cb2709814df837a8153f93c21959ecdd75056acfd27abd15d9fbd4a632)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRecordColumns", [value]))

    @jsii.member(jsii_name="putRecordFormat")
    def put_record_format(
        self,
        *,
        mapping_parameters: typing.Optional[typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param mapping_parameters: mapping_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#mapping_parameters KinesisAnalyticsApplication#mapping_parameters}
        '''
        value = KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat(
            mapping_parameters=mapping_parameters
        )

        return typing.cast(None, jsii.invoke(self, "putRecordFormat", [value]))

    @jsii.member(jsii_name="resetRecordEncoding")
    def reset_record_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecordEncoding", []))

    @builtins.property
    @jsii.member(jsii_name="recordColumns")
    def record_columns(
        self,
    ) -> "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumnsList":
        return typing.cast("KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumnsList", jsii.get(self, "recordColumns"))

    @builtins.property
    @jsii.member(jsii_name="recordFormat")
    def record_format(
        self,
    ) -> "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatOutputReference":
        return typing.cast("KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatOutputReference", jsii.get(self, "recordFormat"))

    @builtins.property
    @jsii.member(jsii_name="recordColumnsInput")
    def record_columns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns"]]], jsii.get(self, "recordColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="recordEncodingInput")
    def record_encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordEncodingInput"))

    @builtins.property
    @jsii.member(jsii_name="recordFormatInput")
    def record_format_input(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat"]:
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat"], jsii.get(self, "recordFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="recordEncoding")
    def record_encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordEncoding"))

    @record_encoding.setter
    def record_encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__495bc23f1d2b7fbcd61feba6f446aa744d55b87570b62b042133f62c5632bef9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordEncoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchema]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchema], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchema],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df35f05c89b48a985a6475c517f1ff00857c979b90636c58c2ab821ee22441d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "sql_type": "sqlType", "mapping": "mapping"},
)
class KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns:
    def __init__(
        self,
        *,
        name: builtins.str,
        sql_type: builtins.str,
        mapping: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#name KinesisAnalyticsApplication#name}.
        :param sql_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#sql_type KinesisAnalyticsApplication#sql_type}.
        :param mapping: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#mapping KinesisAnalyticsApplication#mapping}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd4230a079c3370c7710a438b584c8b48f1ff892cbca4d96cdb247b25a3ba49f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sql_type", value=sql_type, expected_type=type_hints["sql_type"])
            check_type(argname="argument mapping", value=mapping, expected_type=type_hints["mapping"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "sql_type": sql_type,
        }
        if mapping is not None:
            self._values["mapping"] = mapping

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#name KinesisAnalyticsApplication#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sql_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#sql_type KinesisAnalyticsApplication#sql_type}.'''
        result = self._values.get("sql_type")
        assert result is not None, "Required property 'sql_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mapping(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#mapping KinesisAnalyticsApplication#mapping}.'''
        result = self._values.get("mapping")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42dc72ce873ecb05bd569fee2507aaf30e8d20c6bcb0a0282a3e282d650e579c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bc531bdd93dc4f583a44e12ab092b0a9d3ea15f51e34b8ffcedb45d733e4b64)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10a82167832c45f845abcee88da64845ac8ae7494b142e12712b9dfce421c5fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54256aed8f6d86eeede12f785e52b6ae814f3dc8fcaabdd3a50cb025f56d9bce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7948dd22c7de93089334a944df04537ca7cd7c8924dfe53b2443a749b90281b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94aa264b44d1e610adfe083a724626e863b772dfeeadf622a999a7a4c14bb17f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd2dccdbc9e5848f5b4693e4d83e806ce9584f3763cce8580673394a8d6ef778)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMapping")
    def reset_mapping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMapping", []))

    @builtins.property
    @jsii.member(jsii_name="mappingInput")
    def mapping_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mappingInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlTypeInput")
    def sql_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="mapping")
    def mapping(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mapping"))

    @mapping.setter
    def mapping(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__868919ccd58c5cbab2d7b90b715d0f8ecd1737c25e3f4e73aa51df1095ef8d53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e91a2fec1ca03b654620c5541ba9ff247d4ca9e94a752391a01f317a69c6c70e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlType")
    def sql_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlType"))

    @sql_type.setter
    def sql_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c958e667f4b92d49ff890b3ef6d45feaf7feedea01d5de118e3960787b6e6d9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7b7eaa95aa67d4fa34317e789a2bc493a3a788ce038137120eaa5ae3176914b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat",
    jsii_struct_bases=[],
    name_mapping={"mapping_parameters": "mappingParameters"},
)
class KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat:
    def __init__(
        self,
        *,
        mapping_parameters: typing.Optional[typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param mapping_parameters: mapping_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#mapping_parameters KinesisAnalyticsApplication#mapping_parameters}
        '''
        if isinstance(mapping_parameters, dict):
            mapping_parameters = KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters(**mapping_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__110e8c06603047010af9fdd078dde895968a7921c26595d1142c6b49546523b1)
            check_type(argname="argument mapping_parameters", value=mapping_parameters, expected_type=type_hints["mapping_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mapping_parameters is not None:
            self._values["mapping_parameters"] = mapping_parameters

    @builtins.property
    def mapping_parameters(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters"]:
        '''mapping_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#mapping_parameters KinesisAnalyticsApplication#mapping_parameters}
        '''
        result = self._values.get("mapping_parameters")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters",
    jsii_struct_bases=[],
    name_mapping={"csv": "csv", "json": "json"},
)
class KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters:
    def __init__(
        self,
        *,
        csv: typing.Optional[typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv", typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param csv: csv block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#csv KinesisAnalyticsApplication#csv}
        :param json: json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#json KinesisAnalyticsApplication#json}
        '''
        if isinstance(csv, dict):
            csv = KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv(**csv)
        if isinstance(json, dict):
            json = KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson(**json)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c17225f63572292e4406189d4297ef89f2c8c13f0c7be8efdb409a7be3fb9f2)
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
    ) -> typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv"]:
        '''csv block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#csv KinesisAnalyticsApplication#csv}
        '''
        result = self._values.get("csv")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv"], result)

    @builtins.property
    def json(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson"]:
        '''json block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#json KinesisAnalyticsApplication#json}
        '''
        result = self._values.get("json")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv",
    jsii_struct_bases=[],
    name_mapping={
        "record_column_delimiter": "recordColumnDelimiter",
        "record_row_delimiter": "recordRowDelimiter",
    },
)
class KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv:
    def __init__(
        self,
        *,
        record_column_delimiter: builtins.str,
        record_row_delimiter: builtins.str,
    ) -> None:
        '''
        :param record_column_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_column_delimiter KinesisAnalyticsApplication#record_column_delimiter}.
        :param record_row_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_row_delimiter KinesisAnalyticsApplication#record_row_delimiter}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b3424f3dba7eae5082cf5003937d4b0213d65d4aea29032151d4d01b38500dc)
            check_type(argname="argument record_column_delimiter", value=record_column_delimiter, expected_type=type_hints["record_column_delimiter"])
            check_type(argname="argument record_row_delimiter", value=record_row_delimiter, expected_type=type_hints["record_row_delimiter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "record_column_delimiter": record_column_delimiter,
            "record_row_delimiter": record_row_delimiter,
        }

    @builtins.property
    def record_column_delimiter(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_column_delimiter KinesisAnalyticsApplication#record_column_delimiter}.'''
        result = self._values.get("record_column_delimiter")
        assert result is not None, "Required property 'record_column_delimiter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def record_row_delimiter(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_row_delimiter KinesisAnalyticsApplication#record_row_delimiter}.'''
        result = self._values.get("record_row_delimiter")
        assert result is not None, "Required property 'record_row_delimiter' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsvOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsvOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__348305412479ad225e958d9efdd3ec40e9bef22322daa7a24f1f4e333e921079)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="recordColumnDelimiterInput")
    def record_column_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordColumnDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="recordRowDelimiterInput")
    def record_row_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordRowDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="recordColumnDelimiter")
    def record_column_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordColumnDelimiter"))

    @record_column_delimiter.setter
    def record_column_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94d88b3629a6bb9b08189366c1270f64838e8c7cd1926160fc47b538e61f27b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordColumnDelimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recordRowDelimiter")
    def record_row_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordRowDelimiter"))

    @record_row_delimiter.setter
    def record_row_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f288f87a3f5886e20c439a4ad9eb93e7b5ea58fd86aea7f0f044ef06386e99a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordRowDelimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b6ce65440b2d2eb8590e22977db2fa704778dfaf4c859ba10ea0340b3c1ed2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson",
    jsii_struct_bases=[],
    name_mapping={"record_row_path": "recordRowPath"},
)
class KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson:
    def __init__(self, *, record_row_path: builtins.str) -> None:
        '''
        :param record_row_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_row_path KinesisAnalyticsApplication#record_row_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47fc4d7f2e94fa9e768a5d6f958bc4fbb80dd80167ef042b0c9d2152e0e0f032)
            check_type(argname="argument record_row_path", value=record_row_path, expected_type=type_hints["record_row_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "record_row_path": record_row_path,
        }

    @builtins.property
    def record_row_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_row_path KinesisAnalyticsApplication#record_row_path}.'''
        result = self._values.get("record_row_path")
        assert result is not None, "Required property 'record_row_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJsonOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJsonOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4f0158fb04ed103306cc398d26893372f07696c809dce4477873010dd4498b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="recordRowPathInput")
    def record_row_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordRowPathInput"))

    @builtins.property
    @jsii.member(jsii_name="recordRowPath")
    def record_row_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordRowPath"))

    @record_row_path.setter
    def record_row_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bd5a59f5b2014754442d0f8828cea484207565527777573750b970bf607c083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordRowPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7a55e05161d175e5a9018ff48e1f3c36ebbc07bfcc985b87b09f30558a81904)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee5675133084a4ceecf1879f89ade5883dc2b8b6ec60e7691c92fc8cd722b433)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCsv")
    def put_csv(
        self,
        *,
        record_column_delimiter: builtins.str,
        record_row_delimiter: builtins.str,
    ) -> None:
        '''
        :param record_column_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_column_delimiter KinesisAnalyticsApplication#record_column_delimiter}.
        :param record_row_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_row_delimiter KinesisAnalyticsApplication#record_row_delimiter}.
        '''
        value = KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv(
            record_column_delimiter=record_column_delimiter,
            record_row_delimiter=record_row_delimiter,
        )

        return typing.cast(None, jsii.invoke(self, "putCsv", [value]))

    @jsii.member(jsii_name="putJson")
    def put_json(self, *, record_row_path: builtins.str) -> None:
        '''
        :param record_row_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#record_row_path KinesisAnalyticsApplication#record_row_path}.
        '''
        value = KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson(
            record_row_path=record_row_path
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
    ) -> KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsvOutputReference:
        return typing.cast(KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsvOutputReference, jsii.get(self, "csv"))

    @builtins.property
    @jsii.member(jsii_name="json")
    def json(
        self,
    ) -> KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJsonOutputReference:
        return typing.cast(KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJsonOutputReference, jsii.get(self, "json"))

    @builtins.property
    @jsii.member(jsii_name="csvInput")
    def csv_input(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv], jsii.get(self, "csvInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonInput")
    def json_input(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson], jsii.get(self, "jsonInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d65251c482ff10ec944773cd9b2bf27bd1962b2509acbb1ae710e22ae0dbd53d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c09cc7c7d330e8a1900a9da3b786d0680d25e6f4016829feda2642eda568cf4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMappingParameters")
    def put_mapping_parameters(
        self,
        *,
        csv: typing.Optional[typing.Union[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv, typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param csv: csv block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#csv KinesisAnalyticsApplication#csv}
        :param json: json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kinesis_analytics_application#json KinesisAnalyticsApplication#json}
        '''
        value = KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters(
            csv=csv, json=json
        )

        return typing.cast(None, jsii.invoke(self, "putMappingParameters", [value]))

    @jsii.member(jsii_name="resetMappingParameters")
    def reset_mapping_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMappingParameters", []))

    @builtins.property
    @jsii.member(jsii_name="mappingParameters")
    def mapping_parameters(
        self,
    ) -> KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersOutputReference:
        return typing.cast(KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersOutputReference, jsii.get(self, "mappingParameters"))

    @builtins.property
    @jsii.member(jsii_name="recordFormatType")
    def record_format_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordFormatType"))

    @builtins.property
    @jsii.member(jsii_name="mappingParametersInput")
    def mapping_parameters_input(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters], jsii.get(self, "mappingParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e64f77fff423815db3a87d435e48ecf3ed57d66b6d7b7b76308f10b37b25c92d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "KinesisAnalyticsApplication",
    "KinesisAnalyticsApplicationCloudwatchLoggingOptions",
    "KinesisAnalyticsApplicationCloudwatchLoggingOptionsOutputReference",
    "KinesisAnalyticsApplicationConfig",
    "KinesisAnalyticsApplicationInputs",
    "KinesisAnalyticsApplicationInputsKinesisFirehose",
    "KinesisAnalyticsApplicationInputsKinesisFirehoseOutputReference",
    "KinesisAnalyticsApplicationInputsKinesisStream",
    "KinesisAnalyticsApplicationInputsKinesisStreamOutputReference",
    "KinesisAnalyticsApplicationInputsOutputReference",
    "KinesisAnalyticsApplicationInputsParallelism",
    "KinesisAnalyticsApplicationInputsParallelismOutputReference",
    "KinesisAnalyticsApplicationInputsProcessingConfiguration",
    "KinesisAnalyticsApplicationInputsProcessingConfigurationLambda",
    "KinesisAnalyticsApplicationInputsProcessingConfigurationLambdaOutputReference",
    "KinesisAnalyticsApplicationInputsProcessingConfigurationOutputReference",
    "KinesisAnalyticsApplicationInputsSchema",
    "KinesisAnalyticsApplicationInputsSchemaOutputReference",
    "KinesisAnalyticsApplicationInputsSchemaRecordColumns",
    "KinesisAnalyticsApplicationInputsSchemaRecordColumnsList",
    "KinesisAnalyticsApplicationInputsSchemaRecordColumnsOutputReference",
    "KinesisAnalyticsApplicationInputsSchemaRecordFormat",
    "KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters",
    "KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv",
    "KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsvOutputReference",
    "KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson",
    "KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJsonOutputReference",
    "KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersOutputReference",
    "KinesisAnalyticsApplicationInputsSchemaRecordFormatOutputReference",
    "KinesisAnalyticsApplicationInputsStartingPositionConfiguration",
    "KinesisAnalyticsApplicationInputsStartingPositionConfigurationList",
    "KinesisAnalyticsApplicationInputsStartingPositionConfigurationOutputReference",
    "KinesisAnalyticsApplicationOutputs",
    "KinesisAnalyticsApplicationOutputsKinesisFirehose",
    "KinesisAnalyticsApplicationOutputsKinesisFirehoseOutputReference",
    "KinesisAnalyticsApplicationOutputsKinesisStream",
    "KinesisAnalyticsApplicationOutputsKinesisStreamOutputReference",
    "KinesisAnalyticsApplicationOutputsLambda",
    "KinesisAnalyticsApplicationOutputsLambdaOutputReference",
    "KinesisAnalyticsApplicationOutputsList",
    "KinesisAnalyticsApplicationOutputsOutputReference",
    "KinesisAnalyticsApplicationOutputsSchema",
    "KinesisAnalyticsApplicationOutputsSchemaOutputReference",
    "KinesisAnalyticsApplicationReferenceDataSources",
    "KinesisAnalyticsApplicationReferenceDataSourcesOutputReference",
    "KinesisAnalyticsApplicationReferenceDataSourcesS3",
    "KinesisAnalyticsApplicationReferenceDataSourcesS3OutputReference",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchema",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaOutputReference",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumnsList",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumnsOutputReference",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsvOutputReference",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJsonOutputReference",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersOutputReference",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatOutputReference",
]

publication.publish()

def _typecheckingstub__e38973a0043bfc6faa16a1919fb99aaa63b9e48bd15caa532c505e2c197eb588(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    cloudwatch_logging_options: typing.Optional[typing.Union[KinesisAnalyticsApplicationCloudwatchLoggingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    code: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    inputs: typing.Optional[typing.Union[KinesisAnalyticsApplicationInputs, typing.Dict[builtins.str, typing.Any]]] = None,
    outputs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisAnalyticsApplicationOutputs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    reference_data_sources: typing.Optional[typing.Union[KinesisAnalyticsApplicationReferenceDataSources, typing.Dict[builtins.str, typing.Any]]] = None,
    start_application: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__d2b5de6fe667f552c0afe96c8c556b05018f5e7e73743b172e657306a96b5ace(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3541e46204fa4c3006fbc4df47ce50097ebd36fc4afaee13f659df7af1749f46(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisAnalyticsApplicationOutputs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4562f7f20420ca8b3620249f73ae8a656eb0a14c923a19be094f9a13a1f96841(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c07f70b8d5bd6abf858fa75b7fd99570a742d87fb1dd1daf07aa06750ff42d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f82235ade391105c6796d2ef82ded78b60f9f2411b09f32b00b864eafdd82be1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140d479e4a0428a53731586e63bcb12ab9d7bb9f154e2ebea86ac602ce4c499b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a8139aa6f446842cea3dc8e22f856fa0b3e8f28ba9088cf4f1a366536404e9c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff42409f95f597212b3a02906d68c7264a5df19045bb4ba87b881ba0c0b4eb4a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eddee7b19a988a0339ec6c6884633ac3ca903ef74d3339b44592492e143cdbba(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc482b09d384c43e62def631a7fb8039a30450ecfeda622887bb88254082101(
    *,
    log_stream_arn: builtins.str,
    role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__581e84bab74599343e9b0efa0aa4b2a05bfeee982daae070cac6de4644ead7aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21b4317d42b9d7fd670dc530fa0955858d5a311a2426cb71b76a5d4728857f17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc8c4744ac8feb928eee6ac08c9bff24c292c9eb03f1b3cb15323a8365cdacdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b160d954e4af909661f5334854a513686d495973bb77fb1cbbb53f83bcb1b82e(
    value: typing.Optional[KinesisAnalyticsApplicationCloudwatchLoggingOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1f38cfc966de0216aca724ceb70f6a1a45abd59246b4fe6ad85c0b3a6d0199(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    cloudwatch_logging_options: typing.Optional[typing.Union[KinesisAnalyticsApplicationCloudwatchLoggingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    code: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    inputs: typing.Optional[typing.Union[KinesisAnalyticsApplicationInputs, typing.Dict[builtins.str, typing.Any]]] = None,
    outputs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisAnalyticsApplicationOutputs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    reference_data_sources: typing.Optional[typing.Union[KinesisAnalyticsApplicationReferenceDataSources, typing.Dict[builtins.str, typing.Any]]] = None,
    start_application: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef6a433392e81ebdbe5f6f96194d08c71f8309cf06197c55d78617d5ba9e55f4(
    *,
    name_prefix: builtins.str,
    schema: typing.Union[KinesisAnalyticsApplicationInputsSchema, typing.Dict[builtins.str, typing.Any]],
    kinesis_firehose: typing.Optional[typing.Union[KinesisAnalyticsApplicationInputsKinesisFirehose, typing.Dict[builtins.str, typing.Any]]] = None,
    kinesis_stream: typing.Optional[typing.Union[KinesisAnalyticsApplicationInputsKinesisStream, typing.Dict[builtins.str, typing.Any]]] = None,
    parallelism: typing.Optional[typing.Union[KinesisAnalyticsApplicationInputsParallelism, typing.Dict[builtins.str, typing.Any]]] = None,
    processing_configuration: typing.Optional[typing.Union[KinesisAnalyticsApplicationInputsProcessingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    starting_position_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisAnalyticsApplicationInputsStartingPositionConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13d8eabee723d5834b01929a820686107c1e9bb089467326e7f157667e6e02e(
    *,
    resource_arn: builtins.str,
    role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__801c4560404c27483f74ba3f29c3f7fd187ac0bbb9c3eacfb5e4a2c09ca38520(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d6f88c2efeb97c51bef3a8d0c0d0f0cdfb5ecc5a7ebcc3bba6a3e191a67f68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8476cd886f650140bcd35962c32256a55b3b32976437fd7c7ed4c8f676d3976(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a10e729493bcf538424e03ef0c9f390e80e8824c175c76000d39d791805221(
    value: typing.Optional[KinesisAnalyticsApplicationInputsKinesisFirehose],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c916b479a129f0e2564479cb95f66987e078abe9d8ef230f00c37a1c5059c5fb(
    *,
    resource_arn: builtins.str,
    role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d47ed154f5a1b76c1d27056569aac1c1b7eb84e1de78bacc957b6719bd79b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e98ddba1d6c05329675a7f8b0bc3e106baf8ede912496658050d907039aaf7ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e6703b4ac3cfababeb49375ba4b09dbae75cad01d70c2d6df76ca63bf8e9a22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a94d4b93dfadb61ea454b4befc3f268097e3a1ddd1c7de6c6c5c2988b10246(
    value: typing.Optional[KinesisAnalyticsApplicationInputsKinesisStream],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60a17cf020bdcf864102304888c288381e6c9857fe8b569e556e0f877cc70e28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eff11d2639814152e11929e5a45dc047416075e00d45d1dbb43120b8c55d66f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisAnalyticsApplicationInputsStartingPositionConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ac7b351c061d4fcb156521e53d0b08739d074e3f890abfed8ec75b7bbc7a83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6218574e2918d3fb955a373608700c431aef0a26c2ef6b0ad257914565b9a8(
    value: typing.Optional[KinesisAnalyticsApplicationInputs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d464bc16627118debc2b19acfbcab7e258bd64b3163f05924dfc1f71d87434fc(
    *,
    count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9b198877dcf96c6f4eb31bf05ec717d3dd4b3f5aec84acb387cd56d5ae8d274(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0de5211b2edff7942dd5500d64b65af81d72670ffc715b24860a5e7ab66a4435(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f4407622c6b8bafd43de0cc65ce87f500757e5f4c06a88ff7178f4e2099ae6c(
    value: typing.Optional[KinesisAnalyticsApplicationInputsParallelism],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1725b7567300af1f5e968283dadb3aba5fa6d2958d61e3db7ca3648b7f04597(
    *,
    lambda_: typing.Union[KinesisAnalyticsApplicationInputsProcessingConfigurationLambda, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7664cdf98ddfafcbd248308bf4682b39378422b9170d585eef15e9bd8883abde(
    *,
    resource_arn: builtins.str,
    role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47b0ba1385c25b2ffc6fcbe20ae0ada76c1bc163363e924054492238fff35913(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b67fe80d7a70e3fa09b9cba3adaeecfbdac36813f043c3a6c5a6dfbe98207e43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb0beb90ba0c020e0ddf289ccab8fc4e5a6297a115ed166cc0c819c36c552a92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__291c711f5589173abad49a155550e64abe1c4857785ae02b8d3d85281f1b510f(
    value: typing.Optional[KinesisAnalyticsApplicationInputsProcessingConfigurationLambda],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa5ff22330a0079bf1ecfde5b810202a4e9be26ee364ee56773bd46dd57ba72(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b057285593d75be495d0d30449e365c75d1c1ec679c5bc0601ee803513c788(
    value: typing.Optional[KinesisAnalyticsApplicationInputsProcessingConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b091e028ac3a276eda411b6f6bce759116af4a7ac0dc4ed615328c3671449f(
    *,
    record_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisAnalyticsApplicationInputsSchemaRecordColumns, typing.Dict[builtins.str, typing.Any]]]],
    record_format: typing.Union[KinesisAnalyticsApplicationInputsSchemaRecordFormat, typing.Dict[builtins.str, typing.Any]],
    record_encoding: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b533872fd223a32bfd584d659a2a3814469ef7a5d1b9264c56cc816894fa8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad31b38ef572532ea205258a545805b0ba713c641bff56b09ecb3979692599f3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisAnalyticsApplicationInputsSchemaRecordColumns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a77b06aad4c1791d85a4e7ced3f1d0ec4921517cfab9cb31444b1e524dad3d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__102ee02fd0f97ab768203dd312e9250c080dfea99ae3f9f1c4e00e890b3716b4(
    value: typing.Optional[KinesisAnalyticsApplicationInputsSchema],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5890167aa814bd3070c07c8075611d8c75adff1eb2eef910b867e5f15e4e1cb9(
    *,
    name: builtins.str,
    sql_type: builtins.str,
    mapping: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ca7637395b69c827a305c7e2007bb8988b1e06302b2dd17d7bc0d2a1d4acc9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca42dced15bbb2b9ef9c434245d25883cedb682a75289f13bf0af338dd057a8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64585c4923cd77fff9fc52ca8de12b0dca951954a8f437a0e84413bbf3228fa6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c8d3dc70e2f9a5da0491709b6d79fcd7ada5b2d563b67b38e751318dbf4436f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9f8a9c121ecd2ccf8c387b8740bf2a74ec10539a4f5ab8f1b0979e92b775bcd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400902fdba4ae7bba98e7a4a2e6653897d3000dd06d79144da33574b880f2610(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationInputsSchemaRecordColumns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f48651006dbb9324b5cd5a118feb0b7616786b2c7a08481be747186f20ed4c9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ac3b096fcb1f5eff4aed032679e6c2661c0c6aa83a320f68d073d3e10c96b54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c645f71118b88c4ae018b913d75cf2e99ba3cc1ab5748f80f005df2881c4a9ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb15fb7f8cbd3b26b11e9c4a51b7ca8314d96a3ca729466c9f5664b6353775cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a081bd6380080e691911dd4efe7d0a39643b7263599ae2e5f5e6b865313615b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationInputsSchemaRecordColumns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e35de60531b0a6ffec3fcd81aad9212e8be7248c6e06adf98420c636b78a3f23(
    *,
    mapping_parameters: typing.Optional[typing.Union[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2829c3d55e1ca8b72d64f9d8a21f16c1bc8e52382aee26b8bf55bbdf27083441(
    *,
    csv: typing.Optional[typing.Union[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv, typing.Dict[builtins.str, typing.Any]]] = None,
    json: typing.Optional[typing.Union[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a78fec386106e5123fb35b057363b98a3535966564d726451f149db4104121f5(
    *,
    record_column_delimiter: builtins.str,
    record_row_delimiter: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10c847fecc381bf51220db333a46e9ff1afdf3e3b73107464531a93c6bbfd08b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d64d2d4498274d14db4eb695f965aa952329ff7fb656c58b576033732f123f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f8a761f5047c1203121a1b0511a73abf1531bc4f361cbe89ba8e76416a8b32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb042e53f1fa2b0a8127761c995bf5a89ab5121476f2e31ba4c739a080566b7(
    value: typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48bbfa38f8712d6f10670573ef4c6d56da775bf160642f3d47e9ada9363ac460(
    *,
    record_row_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e74afdb3d0a7a5488ebeeadd913594dee0485259e198f7c282eba4b95db5abf7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d7d4ac18676296c54882b243e039f2006c7e6b53bcdac5e1340785aaf2a10b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0645e0fe45f8948792107d5c836ccf3f0442db63a9cb8c7194f85a5b30171d4(
    value: typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfa187c917d2b084ca181b5b8ac3bc2e66164444d9525428167a81421c9be072(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f250ddae6948e306b6ce50d5790eec025c5a2cf81c0397e541f96c4f7d23a03(
    value: typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e101afce70412221d190408a11ef9459de148120488a2a2a903bb85a1274a71d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__888e78309d640d7c9d0c9ddfb66d9521dc754e45abbc592f55dda0c0acc312d7(
    value: typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5ed85bbc816bc1568d1c1237580b55929d4b5c864fd9bc3ae8e0c11399ba333(
    *,
    starting_position: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc8c1cb6f0ab8502c7ab9ec45288c0c2d1197c6e652266ebfcd1a7fd48c62a4c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60cb183a2f670a7b4e010665f60f9ca5dc8cb94db6821ec322f1959f307cfc53(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c0ea6eec7fcb0f92cd4b50fe011cb8403f68502e79f48dbf4fe7abf8545b689(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__541afa535cf83f0adbc11ddee49691811ff2201ba852e785f84dfe5b10f9b85d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eca98f2c14a3525f95fd30bfe6de7d637766063c4ed27ced6842e7de677bf8a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c26b738fa9f891047d337d12905daef38a86423c48593e3e58cad637b385c4a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationInputsStartingPositionConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c31b232bcaaa2f64ca23205cd28f2b87cee7d65db6057c500c6c0143313e0f3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c07ea3cb19abcd1e6ee33936f0ef50083777824ec4f38c31c0dc4fb956ec7700(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40227226e92eda3eed46b4dd5e0e2f89524910339ed19c8d8c0ab7260be629f6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationInputsStartingPositionConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14aacc0b4ffa736ee336eb6147ed6b0c50a9c4301004632523080d61b97b1d3b(
    *,
    name: builtins.str,
    schema: typing.Union[KinesisAnalyticsApplicationOutputsSchema, typing.Dict[builtins.str, typing.Any]],
    kinesis_firehose: typing.Optional[typing.Union[KinesisAnalyticsApplicationOutputsKinesisFirehose, typing.Dict[builtins.str, typing.Any]]] = None,
    kinesis_stream: typing.Optional[typing.Union[KinesisAnalyticsApplicationOutputsKinesisStream, typing.Dict[builtins.str, typing.Any]]] = None,
    lambda_: typing.Optional[typing.Union[KinesisAnalyticsApplicationOutputsLambda, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0bd33ab6599ed3bf8c76e168bfe5191c6e1cac0de2ba26ef06a357cba8b23ab(
    *,
    resource_arn: builtins.str,
    role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f4d57772da694f523bcb2e32c6677c444bf462fcbe03eb1e669695b8eee61f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5950452d01e31fbf1092e0f0b62a8edbc335d2f81bd1e22c135b7271d503e85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f8b753101f57ff14c503d82fdfa82c1c07166f6e48e8c9e4f641f9170c795e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aba0b5fe0812659166fc7890cfc6df32943cdca7698296528a2ebf1121b97a0(
    value: typing.Optional[KinesisAnalyticsApplicationOutputsKinesisFirehose],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd8794e5aae52d6aeebafe7df2af47d0591c54e72938bbbce124bfbb8fa7c71c(
    *,
    resource_arn: builtins.str,
    role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f34a2caf0dfc58c7aa7c5fb6f9c37c32b5b12eb7802004716772d3e2e4ef706(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d96a14c0cf540e380bfcdb9257e1510f661a17b307fd0d5bf8ebf478ee05e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1953324cfb14d5c1304d197da60dda8746c065fefef134f5348cfade27f6a539(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bf141d37c4e0019f3b66fcb070742f4127637f306d283601da156bee4ada9fb(
    value: typing.Optional[KinesisAnalyticsApplicationOutputsKinesisStream],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb77c7a7d26d0d63b9c3a4ed029ef94e166706fe45d4e894587b1f05abefb12(
    *,
    resource_arn: builtins.str,
    role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__711b559e331acf671fe6b32c2dda8d7ebbe7d3e4f77cf49d6f4c5761301fe868(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7008da51159af9e73983f0849306c7c0b6ef0d2f57781e8bbd673a4a9bbe86bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9806c3de0d4d91a656a4815d870d0f1042ff67d508fc86e234ce66a5eb57ade9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b13e808e969196bdd14991ad847d0e9baae884469bbdcffe719e33e9afe30ed(
    value: typing.Optional[KinesisAnalyticsApplicationOutputsLambda],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96ce66f55ef546f64477d3844bb999f626f2e2929964e1d0f30ee79e4417ee0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaf45268a4e56b2619eebeb0fc02a9d63c00a533dd466c2c830284012bdf2b0f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cab46d923e99e41c52e9ab5dada5311fb50573916680ea1a47c148758ea45b41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58189701db44984f17ac2783bf30c85320d839629ce40a5c8b917b13dec81cc9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aac40598e1b10172708fdb4805d50dccad6211374a4fe38014a672a770e857a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0859f97b93e61a4129c55e74f68a0974a1047cfaeaa14b5a92d486068309a4a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationOutputs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e976141fb524f97dadd6db0f8a8f312af6536d8bfa6c6c46ec19aa1bf38dbd55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acdd731b009597a4dff303532a9c45ff6b3b55e900bcd14adfd8c0a319beae63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__990afbcedd563cf440182c8d197be8c701e0ff129a13bd7a6f4aed4ea8c089e9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationOutputs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9be3443f7f78bc54c7740c71db98725d7c6514134c3411123f42a6c350f8b1d(
    *,
    record_format_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0943865d7c29a3b87b59e768c814520c2f8241589921cfdf3f74dfbde1778207(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1cb425ec1dc1c3e77a3ae08c1d39366c9c33fa8845734e09fc32fb1ee34e3c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a0bc1f2c6980efd9966adf90568d782525f2c3850e1f24aef48524c5f62de19(
    value: typing.Optional[KinesisAnalyticsApplicationOutputsSchema],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__687431bc283aab9ba01cc33681de0aa7239e13498a62a6527371a79bdab8f495(
    *,
    s3: typing.Union[KinesisAnalyticsApplicationReferenceDataSourcesS3, typing.Dict[builtins.str, typing.Any]],
    schema: typing.Union[KinesisAnalyticsApplicationReferenceDataSourcesSchema, typing.Dict[builtins.str, typing.Any]],
    table_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e509c3476c3a1a98e8ba01619efce26dd9a2ed3c934b959eacbdfac61d1c53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b4c2b5d2ceffec6c873eb261e80d04605b60dd214989246bfdaf354256b37b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e717d0e2e2f997889e02e46c95af70d27a75a14ea9c8c09e136cd33c54404a00(
    value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4527d006c73958bd5b0607f7705d4798229dd6fb0feb13dde39169bf7720e10(
    *,
    bucket_arn: builtins.str,
    file_key: builtins.str,
    role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93e8997bcc285c60baf8ce8d207cdc03c5e1b3a65c1ed6e992f43b1052ce4973(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fda44dd7d463bfce71383cc561cdf8a1a9c24ac4211069ad33bef1e0427b4e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f646e03d346a2b96477d100ac4cc7b715d8a03ef24e9d7ef40e31205f804048c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a754888f53ef393ce9f42ac061f53a10b123296746262a3ba0b58f673cd3d40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fbca70b8d0d6a0db713232fb154c0b8bf91fc25e746ba529453a3eff7b2676(
    value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesS3],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b8993e1581615fd98d8d4874dfbecff32559648790e9232ab7772717a82725a(
    *,
    record_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns, typing.Dict[builtins.str, typing.Any]]]],
    record_format: typing.Union[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat, typing.Dict[builtins.str, typing.Any]],
    record_encoding: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de0914871541b83b59af5e906013ef37e4a1454f67dafd2b15d3a44b8716f539(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4abae0cb2709814df837a8153f93c21959ecdd75056acfd27abd15d9fbd4a632(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__495bc23f1d2b7fbcd61feba6f446aa744d55b87570b62b042133f62c5632bef9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df35f05c89b48a985a6475c517f1ff00857c979b90636c58c2ab821ee22441d8(
    value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchema],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd4230a079c3370c7710a438b584c8b48f1ff892cbca4d96cdb247b25a3ba49f(
    *,
    name: builtins.str,
    sql_type: builtins.str,
    mapping: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42dc72ce873ecb05bd569fee2507aaf30e8d20c6bcb0a0282a3e282d650e579c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc531bdd93dc4f583a44e12ab092b0a9d3ea15f51e34b8ffcedb45d733e4b64(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10a82167832c45f845abcee88da64845ac8ae7494b142e12712b9dfce421c5fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54256aed8f6d86eeede12f785e52b6ae814f3dc8fcaabdd3a50cb025f56d9bce(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7948dd22c7de93089334a944df04537ca7cd7c8924dfe53b2443a749b90281b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94aa264b44d1e610adfe083a724626e863b772dfeeadf622a999a7a4c14bb17f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2dccdbc9e5848f5b4693e4d83e806ce9584f3763cce8580673394a8d6ef778(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__868919ccd58c5cbab2d7b90b715d0f8ecd1737c25e3f4e73aa51df1095ef8d53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e91a2fec1ca03b654620c5541ba9ff247d4ca9e94a752391a01f317a69c6c70e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c958e667f4b92d49ff890b3ef6d45feaf7feedea01d5de118e3960787b6e6d9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7b7eaa95aa67d4fa34317e789a2bc493a3a788ce038137120eaa5ae3176914b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__110e8c06603047010af9fdd078dde895968a7921c26595d1142c6b49546523b1(
    *,
    mapping_parameters: typing.Optional[typing.Union[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c17225f63572292e4406189d4297ef89f2c8c13f0c7be8efdb409a7be3fb9f2(
    *,
    csv: typing.Optional[typing.Union[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv, typing.Dict[builtins.str, typing.Any]]] = None,
    json: typing.Optional[typing.Union[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3424f3dba7eae5082cf5003937d4b0213d65d4aea29032151d4d01b38500dc(
    *,
    record_column_delimiter: builtins.str,
    record_row_delimiter: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__348305412479ad225e958d9efdd3ec40e9bef22322daa7a24f1f4e333e921079(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d88b3629a6bb9b08189366c1270f64838e8c7cd1926160fc47b538e61f27b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f288f87a3f5886e20c439a4ad9eb93e7b5ea58fd86aea7f0f044ef06386e99a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b6ce65440b2d2eb8590e22977db2fa704778dfaf4c859ba10ea0340b3c1ed2e(
    value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47fc4d7f2e94fa9e768a5d6f958bc4fbb80dd80167ef042b0c9d2152e0e0f032(
    *,
    record_row_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4f0158fb04ed103306cc398d26893372f07696c809dce4477873010dd4498b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bd5a59f5b2014754442d0f8828cea484207565527777573750b970bf607c083(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7a55e05161d175e5a9018ff48e1f3c36ebbc07bfcc985b87b09f30558a81904(
    value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee5675133084a4ceecf1879f89ade5883dc2b8b6ec60e7691c92fc8cd722b433(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65251c482ff10ec944773cd9b2bf27bd1962b2509acbb1ae710e22ae0dbd53d(
    value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c09cc7c7d330e8a1900a9da3b786d0680d25e6f4016829feda2642eda568cf4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e64f77fff423815db3a87d435e48ecf3ed57d66b6d7b7b76308f10b37b25c92d(
    value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat],
) -> None:
    """Type checking stubs"""
    pass
