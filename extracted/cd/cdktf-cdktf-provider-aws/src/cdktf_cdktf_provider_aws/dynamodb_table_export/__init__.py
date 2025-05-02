r'''
# `aws_dynamodb_table_export`

Refer to the Terraform Registry for docs: [`aws_dynamodb_table_export`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export).
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


class DynamodbTableExport(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dynamodbTableExport.DynamodbTableExport",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export aws_dynamodb_table_export}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        s3_bucket: builtins.str,
        table_arn: builtins.str,
        export_format: typing.Optional[builtins.str] = None,
        export_time: typing.Optional[builtins.str] = None,
        export_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        incremental_export_specification: typing.Optional[typing.Union["DynamodbTableExportIncrementalExportSpecification", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_bucket_owner: typing.Optional[builtins.str] = None,
        s3_prefix: typing.Optional[builtins.str] = None,
        s3_sse_algorithm: typing.Optional[builtins.str] = None,
        s3_sse_kms_key_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DynamodbTableExportTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export aws_dynamodb_table_export} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param s3_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#s3_bucket DynamodbTableExport#s3_bucket}.
        :param table_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#table_arn DynamodbTableExport#table_arn}.
        :param export_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#export_format DynamodbTableExport#export_format}.
        :param export_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#export_time DynamodbTableExport#export_time}.
        :param export_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#export_type DynamodbTableExport#export_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#id DynamodbTableExport#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param incremental_export_specification: incremental_export_specification block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#incremental_export_specification DynamodbTableExport#incremental_export_specification}
        :param s3_bucket_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#s3_bucket_owner DynamodbTableExport#s3_bucket_owner}.
        :param s3_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#s3_prefix DynamodbTableExport#s3_prefix}.
        :param s3_sse_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#s3_sse_algorithm DynamodbTableExport#s3_sse_algorithm}.
        :param s3_sse_kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#s3_sse_kms_key_id DynamodbTableExport#s3_sse_kms_key_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#timeouts DynamodbTableExport#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85239f9f7c68c3f03bd2e2457d4f7e827c567f6814d844fb37fdd84d9c64f73f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DynamodbTableExportConfig(
            s3_bucket=s3_bucket,
            table_arn=table_arn,
            export_format=export_format,
            export_time=export_time,
            export_type=export_type,
            id=id,
            incremental_export_specification=incremental_export_specification,
            s3_bucket_owner=s3_bucket_owner,
            s3_prefix=s3_prefix,
            s3_sse_algorithm=s3_sse_algorithm,
            s3_sse_kms_key_id=s3_sse_kms_key_id,
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
        '''Generates CDKTF code for importing a DynamodbTableExport resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DynamodbTableExport to import.
        :param import_from_id: The id of the existing DynamodbTableExport that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DynamodbTableExport to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9407636766d1637660ebc425ddcd5a6f7c7dc9aadfe1cd3bbae9504d36c12b2b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIncrementalExportSpecification")
    def put_incremental_export_specification(
        self,
        *,
        export_from_time: typing.Optional[builtins.str] = None,
        export_to_time: typing.Optional[builtins.str] = None,
        export_view_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param export_from_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#export_from_time DynamodbTableExport#export_from_time}.
        :param export_to_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#export_to_time DynamodbTableExport#export_to_time}.
        :param export_view_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#export_view_type DynamodbTableExport#export_view_type}.
        '''
        value = DynamodbTableExportIncrementalExportSpecification(
            export_from_time=export_from_time,
            export_to_time=export_to_time,
            export_view_type=export_view_type,
        )

        return typing.cast(None, jsii.invoke(self, "putIncrementalExportSpecification", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#create DynamodbTableExport#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#delete DynamodbTableExport#delete}.
        '''
        value = DynamodbTableExportTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetExportFormat")
    def reset_export_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportFormat", []))

    @jsii.member(jsii_name="resetExportTime")
    def reset_export_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportTime", []))

    @jsii.member(jsii_name="resetExportType")
    def reset_export_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportType", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIncrementalExportSpecification")
    def reset_incremental_export_specification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncrementalExportSpecification", []))

    @jsii.member(jsii_name="resetS3BucketOwner")
    def reset_s3_bucket_owner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3BucketOwner", []))

    @jsii.member(jsii_name="resetS3Prefix")
    def reset_s3_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Prefix", []))

    @jsii.member(jsii_name="resetS3SseAlgorithm")
    def reset_s3_sse_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3SseAlgorithm", []))

    @jsii.member(jsii_name="resetS3SseKmsKeyId")
    def reset_s3_sse_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3SseKmsKeyId", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="billedSizeInBytes")
    def billed_size_in_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "billedSizeInBytes"))

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @builtins.property
    @jsii.member(jsii_name="exportStatus")
    def export_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exportStatus"))

    @builtins.property
    @jsii.member(jsii_name="incrementalExportSpecification")
    def incremental_export_specification(
        self,
    ) -> "DynamodbTableExportIncrementalExportSpecificationOutputReference":
        return typing.cast("DynamodbTableExportIncrementalExportSpecificationOutputReference", jsii.get(self, "incrementalExportSpecification"))

    @builtins.property
    @jsii.member(jsii_name="itemCount")
    def item_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "itemCount"))

    @builtins.property
    @jsii.member(jsii_name="manifestFilesS3Key")
    def manifest_files_s3_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "manifestFilesS3Key"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DynamodbTableExportTimeoutsOutputReference":
        return typing.cast("DynamodbTableExportTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="exportFormatInput")
    def export_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exportFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="exportTimeInput")
    def export_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exportTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="exportTypeInput")
    def export_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exportTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="incrementalExportSpecificationInput")
    def incremental_export_specification_input(
        self,
    ) -> typing.Optional["DynamodbTableExportIncrementalExportSpecification"]:
        return typing.cast(typing.Optional["DynamodbTableExportIncrementalExportSpecification"], jsii.get(self, "incrementalExportSpecificationInput"))

    @builtins.property
    @jsii.member(jsii_name="s3BucketInput")
    def s3_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3BucketInput"))

    @builtins.property
    @jsii.member(jsii_name="s3BucketOwnerInput")
    def s3_bucket_owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3BucketOwnerInput"))

    @builtins.property
    @jsii.member(jsii_name="s3PrefixInput")
    def s3_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3PrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="s3SseAlgorithmInput")
    def s3_sse_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3SseAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="s3SseKmsKeyIdInput")
    def s3_sse_kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3SseKmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tableArnInput")
    def table_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableArnInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DynamodbTableExportTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DynamodbTableExportTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="exportFormat")
    def export_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exportFormat"))

    @export_format.setter
    def export_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46682d4777c80b92a06999f6f7972d9bffee40a3b229290116fc354b07bb8c5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exportFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exportTime")
    def export_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exportTime"))

    @export_time.setter
    def export_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7530ab051be5c9a7e5650eeefe26a0f070ac4850c3ad4208a8ed9d6a607735ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exportTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exportType")
    def export_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exportType"))

    @export_type.setter
    def export_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8cc1099915c57d9be33a2f61c50c1486717fd3ac93682088f94e03512c1b7b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exportType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__368baff4e71e82672594b4f1710fa52d2343d7ff953738c87cd58d6d23718a2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3Bucket")
    def s3_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Bucket"))

    @s3_bucket.setter
    def s3_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d89fb972a6a21a108fa7836c797cc6eab0468fbf0df486ae988c906192d0530)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3BucketOwner")
    def s3_bucket_owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3BucketOwner"))

    @s3_bucket_owner.setter
    def s3_bucket_owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec01bbfb87e04414402f4fcdefb84a8aa95cab38737615669a3dbee2a1099b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3BucketOwner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3Prefix")
    def s3_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Prefix"))

    @s3_prefix.setter
    def s3_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a15d5dda64081180e71082bed3a5cbde6e01afda233a84dcee295d9cb6d19b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3SseAlgorithm")
    def s3_sse_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3SseAlgorithm"))

    @s3_sse_algorithm.setter
    def s3_sse_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f59bce9871274279ed15947ca5c8465c9c30b9c5abe8d39d37ccd05660de53f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3SseAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3SseKmsKeyId")
    def s3_sse_kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3SseKmsKeyId"))

    @s3_sse_kms_key_id.setter
    def s3_sse_kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb57f7d4656116ad134fd0041c4b46ec5ce84e1dfe80203c0bc52b75e407e210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3SseKmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableArn"))

    @table_arn.setter
    def table_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__454ede8434d583f55ec96f4bf145a3bd6e75156d524d2a65174c3dae21993861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableArn", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dynamodbTableExport.DynamodbTableExportConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "s3_bucket": "s3Bucket",
        "table_arn": "tableArn",
        "export_format": "exportFormat",
        "export_time": "exportTime",
        "export_type": "exportType",
        "id": "id",
        "incremental_export_specification": "incrementalExportSpecification",
        "s3_bucket_owner": "s3BucketOwner",
        "s3_prefix": "s3Prefix",
        "s3_sse_algorithm": "s3SseAlgorithm",
        "s3_sse_kms_key_id": "s3SseKmsKeyId",
        "timeouts": "timeouts",
    },
)
class DynamodbTableExportConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        s3_bucket: builtins.str,
        table_arn: builtins.str,
        export_format: typing.Optional[builtins.str] = None,
        export_time: typing.Optional[builtins.str] = None,
        export_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        incremental_export_specification: typing.Optional[typing.Union["DynamodbTableExportIncrementalExportSpecification", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_bucket_owner: typing.Optional[builtins.str] = None,
        s3_prefix: typing.Optional[builtins.str] = None,
        s3_sse_algorithm: typing.Optional[builtins.str] = None,
        s3_sse_kms_key_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DynamodbTableExportTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param s3_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#s3_bucket DynamodbTableExport#s3_bucket}.
        :param table_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#table_arn DynamodbTableExport#table_arn}.
        :param export_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#export_format DynamodbTableExport#export_format}.
        :param export_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#export_time DynamodbTableExport#export_time}.
        :param export_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#export_type DynamodbTableExport#export_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#id DynamodbTableExport#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param incremental_export_specification: incremental_export_specification block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#incremental_export_specification DynamodbTableExport#incremental_export_specification}
        :param s3_bucket_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#s3_bucket_owner DynamodbTableExport#s3_bucket_owner}.
        :param s3_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#s3_prefix DynamodbTableExport#s3_prefix}.
        :param s3_sse_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#s3_sse_algorithm DynamodbTableExport#s3_sse_algorithm}.
        :param s3_sse_kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#s3_sse_kms_key_id DynamodbTableExport#s3_sse_kms_key_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#timeouts DynamodbTableExport#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(incremental_export_specification, dict):
            incremental_export_specification = DynamodbTableExportIncrementalExportSpecification(**incremental_export_specification)
        if isinstance(timeouts, dict):
            timeouts = DynamodbTableExportTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__100f394ea759da624f051b3d65e88ec12d3f22c291d68d4082d58c9eb7583bb1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            check_type(argname="argument table_arn", value=table_arn, expected_type=type_hints["table_arn"])
            check_type(argname="argument export_format", value=export_format, expected_type=type_hints["export_format"])
            check_type(argname="argument export_time", value=export_time, expected_type=type_hints["export_time"])
            check_type(argname="argument export_type", value=export_type, expected_type=type_hints["export_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument incremental_export_specification", value=incremental_export_specification, expected_type=type_hints["incremental_export_specification"])
            check_type(argname="argument s3_bucket_owner", value=s3_bucket_owner, expected_type=type_hints["s3_bucket_owner"])
            check_type(argname="argument s3_prefix", value=s3_prefix, expected_type=type_hints["s3_prefix"])
            check_type(argname="argument s3_sse_algorithm", value=s3_sse_algorithm, expected_type=type_hints["s3_sse_algorithm"])
            check_type(argname="argument s3_sse_kms_key_id", value=s3_sse_kms_key_id, expected_type=type_hints["s3_sse_kms_key_id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_bucket": s3_bucket,
            "table_arn": table_arn,
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
        if export_format is not None:
            self._values["export_format"] = export_format
        if export_time is not None:
            self._values["export_time"] = export_time
        if export_type is not None:
            self._values["export_type"] = export_type
        if id is not None:
            self._values["id"] = id
        if incremental_export_specification is not None:
            self._values["incremental_export_specification"] = incremental_export_specification
        if s3_bucket_owner is not None:
            self._values["s3_bucket_owner"] = s3_bucket_owner
        if s3_prefix is not None:
            self._values["s3_prefix"] = s3_prefix
        if s3_sse_algorithm is not None:
            self._values["s3_sse_algorithm"] = s3_sse_algorithm
        if s3_sse_kms_key_id is not None:
            self._values["s3_sse_kms_key_id"] = s3_sse_kms_key_id
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
    def s3_bucket(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#s3_bucket DynamodbTableExport#s3_bucket}.'''
        result = self._values.get("s3_bucket")
        assert result is not None, "Required property 's3_bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#table_arn DynamodbTableExport#table_arn}.'''
        result = self._values.get("table_arn")
        assert result is not None, "Required property 'table_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def export_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#export_format DynamodbTableExport#export_format}.'''
        result = self._values.get("export_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def export_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#export_time DynamodbTableExport#export_time}.'''
        result = self._values.get("export_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def export_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#export_type DynamodbTableExport#export_type}.'''
        result = self._values.get("export_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#id DynamodbTableExport#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def incremental_export_specification(
        self,
    ) -> typing.Optional["DynamodbTableExportIncrementalExportSpecification"]:
        '''incremental_export_specification block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#incremental_export_specification DynamodbTableExport#incremental_export_specification}
        '''
        result = self._values.get("incremental_export_specification")
        return typing.cast(typing.Optional["DynamodbTableExportIncrementalExportSpecification"], result)

    @builtins.property
    def s3_bucket_owner(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#s3_bucket_owner DynamodbTableExport#s3_bucket_owner}.'''
        result = self._values.get("s3_bucket_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#s3_prefix DynamodbTableExport#s3_prefix}.'''
        result = self._values.get("s3_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_sse_algorithm(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#s3_sse_algorithm DynamodbTableExport#s3_sse_algorithm}.'''
        result = self._values.get("s3_sse_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_sse_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#s3_sse_kms_key_id DynamodbTableExport#s3_sse_kms_key_id}.'''
        result = self._values.get("s3_sse_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DynamodbTableExportTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#timeouts DynamodbTableExport#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DynamodbTableExportTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DynamodbTableExportConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dynamodbTableExport.DynamodbTableExportIncrementalExportSpecification",
    jsii_struct_bases=[],
    name_mapping={
        "export_from_time": "exportFromTime",
        "export_to_time": "exportToTime",
        "export_view_type": "exportViewType",
    },
)
class DynamodbTableExportIncrementalExportSpecification:
    def __init__(
        self,
        *,
        export_from_time: typing.Optional[builtins.str] = None,
        export_to_time: typing.Optional[builtins.str] = None,
        export_view_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param export_from_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#export_from_time DynamodbTableExport#export_from_time}.
        :param export_to_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#export_to_time DynamodbTableExport#export_to_time}.
        :param export_view_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#export_view_type DynamodbTableExport#export_view_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4192730b8c79dfb8bd2ddec4ba733443a940058014bbf0fa1c36cb04174f6bc5)
            check_type(argname="argument export_from_time", value=export_from_time, expected_type=type_hints["export_from_time"])
            check_type(argname="argument export_to_time", value=export_to_time, expected_type=type_hints["export_to_time"])
            check_type(argname="argument export_view_type", value=export_view_type, expected_type=type_hints["export_view_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if export_from_time is not None:
            self._values["export_from_time"] = export_from_time
        if export_to_time is not None:
            self._values["export_to_time"] = export_to_time
        if export_view_type is not None:
            self._values["export_view_type"] = export_view_type

    @builtins.property
    def export_from_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#export_from_time DynamodbTableExport#export_from_time}.'''
        result = self._values.get("export_from_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def export_to_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#export_to_time DynamodbTableExport#export_to_time}.'''
        result = self._values.get("export_to_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def export_view_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#export_view_type DynamodbTableExport#export_view_type}.'''
        result = self._values.get("export_view_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DynamodbTableExportIncrementalExportSpecification(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DynamodbTableExportIncrementalExportSpecificationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dynamodbTableExport.DynamodbTableExportIncrementalExportSpecificationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff340dec9dd2648de016d4a29eef8892723921334134e94c23868a3aaa240035)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExportFromTime")
    def reset_export_from_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportFromTime", []))

    @jsii.member(jsii_name="resetExportToTime")
    def reset_export_to_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportToTime", []))

    @jsii.member(jsii_name="resetExportViewType")
    def reset_export_view_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportViewType", []))

    @builtins.property
    @jsii.member(jsii_name="exportFromTimeInput")
    def export_from_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exportFromTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="exportToTimeInput")
    def export_to_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exportToTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="exportViewTypeInput")
    def export_view_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exportViewTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="exportFromTime")
    def export_from_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exportFromTime"))

    @export_from_time.setter
    def export_from_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6ea01a3f530ad2b2b7d3191c6c58ddc949b0f58a88c13a1cf66bc9fff383eea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exportFromTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exportToTime")
    def export_to_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exportToTime"))

    @export_to_time.setter
    def export_to_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95f0376be3681b409f90fd81844e09e9b9b9329887e905545ee687818bfe6052)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exportToTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exportViewType")
    def export_view_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exportViewType"))

    @export_view_type.setter
    def export_view_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1515be73df8364248f1da4a343cd11956be49ec46371c294cade9c23c4fe33c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exportViewType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DynamodbTableExportIncrementalExportSpecification]:
        return typing.cast(typing.Optional[DynamodbTableExportIncrementalExportSpecification], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DynamodbTableExportIncrementalExportSpecification],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4c4eca75654c4776eff023bc4bb34e26f2fd48aacecd580e1fcc7b464dffd81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dynamodbTableExport.DynamodbTableExportTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class DynamodbTableExportTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#create DynamodbTableExport#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#delete DynamodbTableExport#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f727d38c40c1c4a51072b1cde26265ae6379133011d9880bc3d4a1b33cd4a9bc)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#create DynamodbTableExport#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/dynamodb_table_export#delete DynamodbTableExport#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DynamodbTableExportTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DynamodbTableExportTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dynamodbTableExport.DynamodbTableExportTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__734b46cb98b856f9dcde996da5fac77d7f86d4478edfbb7f312b2abeb55264d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__643bd48dee00175826ea3a0069da40ea514129f82c987161fe7b6806f3c441ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd0f22dc26bd4193513f126fb93cc71c92e5d7ac06b836c6c3aab30e1a242049)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DynamodbTableExportTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DynamodbTableExportTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DynamodbTableExportTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1737f2d9336aae4164c0cd115e92c8785adea5f3a9b24e6bfcae728ab4132f48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DynamodbTableExport",
    "DynamodbTableExportConfig",
    "DynamodbTableExportIncrementalExportSpecification",
    "DynamodbTableExportIncrementalExportSpecificationOutputReference",
    "DynamodbTableExportTimeouts",
    "DynamodbTableExportTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__85239f9f7c68c3f03bd2e2457d4f7e827c567f6814d844fb37fdd84d9c64f73f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    s3_bucket: builtins.str,
    table_arn: builtins.str,
    export_format: typing.Optional[builtins.str] = None,
    export_time: typing.Optional[builtins.str] = None,
    export_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    incremental_export_specification: typing.Optional[typing.Union[DynamodbTableExportIncrementalExportSpecification, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_bucket_owner: typing.Optional[builtins.str] = None,
    s3_prefix: typing.Optional[builtins.str] = None,
    s3_sse_algorithm: typing.Optional[builtins.str] = None,
    s3_sse_kms_key_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DynamodbTableExportTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9407636766d1637660ebc425ddcd5a6f7c7dc9aadfe1cd3bbae9504d36c12b2b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46682d4777c80b92a06999f6f7972d9bffee40a3b229290116fc354b07bb8c5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7530ab051be5c9a7e5650eeefe26a0f070ac4850c3ad4208a8ed9d6a607735ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8cc1099915c57d9be33a2f61c50c1486717fd3ac93682088f94e03512c1b7b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__368baff4e71e82672594b4f1710fa52d2343d7ff953738c87cd58d6d23718a2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d89fb972a6a21a108fa7836c797cc6eab0468fbf0df486ae988c906192d0530(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec01bbfb87e04414402f4fcdefb84a8aa95cab38737615669a3dbee2a1099b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a15d5dda64081180e71082bed3a5cbde6e01afda233a84dcee295d9cb6d19b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f59bce9871274279ed15947ca5c8465c9c30b9c5abe8d39d37ccd05660de53f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb57f7d4656116ad134fd0041c4b46ec5ce84e1dfe80203c0bc52b75e407e210(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__454ede8434d583f55ec96f4bf145a3bd6e75156d524d2a65174c3dae21993861(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__100f394ea759da624f051b3d65e88ec12d3f22c291d68d4082d58c9eb7583bb1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    s3_bucket: builtins.str,
    table_arn: builtins.str,
    export_format: typing.Optional[builtins.str] = None,
    export_time: typing.Optional[builtins.str] = None,
    export_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    incremental_export_specification: typing.Optional[typing.Union[DynamodbTableExportIncrementalExportSpecification, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_bucket_owner: typing.Optional[builtins.str] = None,
    s3_prefix: typing.Optional[builtins.str] = None,
    s3_sse_algorithm: typing.Optional[builtins.str] = None,
    s3_sse_kms_key_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DynamodbTableExportTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4192730b8c79dfb8bd2ddec4ba733443a940058014bbf0fa1c36cb04174f6bc5(
    *,
    export_from_time: typing.Optional[builtins.str] = None,
    export_to_time: typing.Optional[builtins.str] = None,
    export_view_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff340dec9dd2648de016d4a29eef8892723921334134e94c23868a3aaa240035(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ea01a3f530ad2b2b7d3191c6c58ddc949b0f58a88c13a1cf66bc9fff383eea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f0376be3681b409f90fd81844e09e9b9b9329887e905545ee687818bfe6052(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1515be73df8364248f1da4a343cd11956be49ec46371c294cade9c23c4fe33c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4c4eca75654c4776eff023bc4bb34e26f2fd48aacecd580e1fcc7b464dffd81(
    value: typing.Optional[DynamodbTableExportIncrementalExportSpecification],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f727d38c40c1c4a51072b1cde26265ae6379133011d9880bc3d4a1b33cd4a9bc(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__734b46cb98b856f9dcde996da5fac77d7f86d4478edfbb7f312b2abeb55264d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643bd48dee00175826ea3a0069da40ea514129f82c987161fe7b6806f3c441ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd0f22dc26bd4193513f126fb93cc71c92e5d7ac06b836c6c3aab30e1a242049(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1737f2d9336aae4164c0cd115e92c8785adea5f3a9b24e6bfcae728ab4132f48(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DynamodbTableExportTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
