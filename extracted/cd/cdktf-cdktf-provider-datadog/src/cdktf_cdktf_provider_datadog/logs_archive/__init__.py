r'''
# `datadog_logs_archive`

Refer to the Terraform Registry for docs: [`datadog_logs_archive`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive).
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


class LogsArchive(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsArchive.LogsArchive",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive datadog_logs_archive}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        query: builtins.str,
        azure_archive: typing.Optional[typing.Union["LogsArchiveAzureArchive", typing.Dict[builtins.str, typing.Any]]] = None,
        gcs_archive: typing.Optional[typing.Union["LogsArchiveGcsArchive", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        include_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rehydration_max_scan_size_in_gb: typing.Optional[jsii.Number] = None,
        rehydration_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        s3_archive: typing.Optional[typing.Union["LogsArchiveS3Archive", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive datadog_logs_archive} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Your archive name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#name LogsArchive#name}
        :param query: The archive query/filter. Logs matching this query are included in the archive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#query LogsArchive#query}
        :param azure_archive: azure_archive block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#azure_archive LogsArchive#azure_archive}
        :param gcs_archive: gcs_archive block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#gcs_archive LogsArchive#gcs_archive}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#id LogsArchive#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include_tags: To store the tags in the archive, set the value ``true``. If it is set to ``false``, the tags will be dropped when the logs are sent to the archive. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#include_tags LogsArchive#include_tags}
        :param rehydration_max_scan_size_in_gb: To limit the rehydration scan size for the archive, set a value in GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#rehydration_max_scan_size_in_gb LogsArchive#rehydration_max_scan_size_in_gb}
        :param rehydration_tags: An array of tags to add to rehydrated logs from an archive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#rehydration_tags LogsArchive#rehydration_tags}
        :param s3_archive: s3_archive block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#s3_archive LogsArchive#s3_archive}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85c096907faabee57f3d9412a01deecc62a69d390e213f8f3760195ad3091c5f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LogsArchiveConfig(
            name=name,
            query=query,
            azure_archive=azure_archive,
            gcs_archive=gcs_archive,
            id=id,
            include_tags=include_tags,
            rehydration_max_scan_size_in_gb=rehydration_max_scan_size_in_gb,
            rehydration_tags=rehydration_tags,
            s3_archive=s3_archive,
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
        '''Generates CDKTF code for importing a LogsArchive resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LogsArchive to import.
        :param import_from_id: The id of the existing LogsArchive that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LogsArchive to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33b79d4cec0cae5ef69b4bbcdf2375211ac0fa409a4e219841a3c3d5c7687b6f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAzureArchive")
    def put_azure_archive(
        self,
        *,
        client_id: builtins.str,
        container: builtins.str,
        storage_account: builtins.str,
        tenant_id: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: Your client id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#client_id LogsArchive#client_id}
        :param container: The container where the archive is stored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#container LogsArchive#container}
        :param storage_account: The associated storage account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#storage_account LogsArchive#storage_account}
        :param tenant_id: Your tenant id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#tenant_id LogsArchive#tenant_id}
        :param path: The path where the archive is stored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#path LogsArchive#path}
        '''
        value = LogsArchiveAzureArchive(
            client_id=client_id,
            container=container,
            storage_account=storage_account,
            tenant_id=tenant_id,
            path=path,
        )

        return typing.cast(None, jsii.invoke(self, "putAzureArchive", [value]))

    @jsii.member(jsii_name="putGcsArchive")
    def put_gcs_archive(
        self,
        *,
        bucket: builtins.str,
        client_email: builtins.str,
        path: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Name of your GCS bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#bucket LogsArchive#bucket}
        :param client_email: Your client email. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#client_email LogsArchive#client_email}
        :param path: Path where the archive is stored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#path LogsArchive#path}
        :param project_id: Your project id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#project_id LogsArchive#project_id}
        '''
        value = LogsArchiveGcsArchive(
            bucket=bucket, client_email=client_email, path=path, project_id=project_id
        )

        return typing.cast(None, jsii.invoke(self, "putGcsArchive", [value]))

    @jsii.member(jsii_name="putS3Archive")
    def put_s3_archive(
        self,
        *,
        account_id: builtins.str,
        bucket: builtins.str,
        role_name: builtins.str,
        encryption_key: typing.Optional[builtins.str] = None,
        encryption_type: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        storage_class: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_id: Your AWS account id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#account_id LogsArchive#account_id}
        :param bucket: Name of your s3 bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#bucket LogsArchive#bucket}
        :param role_name: Your AWS role name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#role_name LogsArchive#role_name}
        :param encryption_key: The AWS KMS encryption key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#encryption_key LogsArchive#encryption_key}
        :param encryption_type: The type of encryption on your archive. Valid values are ``NO_OVERRIDE``, ``SSE_S3``, ``SSE_KMS``. Defaults to ``"NO_OVERRIDE"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#encryption_type LogsArchive#encryption_type}
        :param path: Path where the archive is stored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#path LogsArchive#path}
        :param storage_class: The AWS S3 storage class used to upload the logs. Valid values are ``STANDARD``, ``STANDARD_IA``, ``ONEZONE_IA``, ``INTELLIGENT_TIERING``, ``GLACIER_IR``. Defaults to ``"STANDARD"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#storage_class LogsArchive#storage_class}
        '''
        value = LogsArchiveS3Archive(
            account_id=account_id,
            bucket=bucket,
            role_name=role_name,
            encryption_key=encryption_key,
            encryption_type=encryption_type,
            path=path,
            storage_class=storage_class,
        )

        return typing.cast(None, jsii.invoke(self, "putS3Archive", [value]))

    @jsii.member(jsii_name="resetAzureArchive")
    def reset_azure_archive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureArchive", []))

    @jsii.member(jsii_name="resetGcsArchive")
    def reset_gcs_archive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcsArchive", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIncludeTags")
    def reset_include_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeTags", []))

    @jsii.member(jsii_name="resetRehydrationMaxScanSizeInGb")
    def reset_rehydration_max_scan_size_in_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRehydrationMaxScanSizeInGb", []))

    @jsii.member(jsii_name="resetRehydrationTags")
    def reset_rehydration_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRehydrationTags", []))

    @jsii.member(jsii_name="resetS3Archive")
    def reset_s3_archive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Archive", []))

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
    @jsii.member(jsii_name="azureArchive")
    def azure_archive(self) -> "LogsArchiveAzureArchiveOutputReference":
        return typing.cast("LogsArchiveAzureArchiveOutputReference", jsii.get(self, "azureArchive"))

    @builtins.property
    @jsii.member(jsii_name="gcsArchive")
    def gcs_archive(self) -> "LogsArchiveGcsArchiveOutputReference":
        return typing.cast("LogsArchiveGcsArchiveOutputReference", jsii.get(self, "gcsArchive"))

    @builtins.property
    @jsii.member(jsii_name="s3Archive")
    def s3_archive(self) -> "LogsArchiveS3ArchiveOutputReference":
        return typing.cast("LogsArchiveS3ArchiveOutputReference", jsii.get(self, "s3Archive"))

    @builtins.property
    @jsii.member(jsii_name="azureArchiveInput")
    def azure_archive_input(self) -> typing.Optional["LogsArchiveAzureArchive"]:
        return typing.cast(typing.Optional["LogsArchiveAzureArchive"], jsii.get(self, "azureArchiveInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsArchiveInput")
    def gcs_archive_input(self) -> typing.Optional["LogsArchiveGcsArchive"]:
        return typing.cast(typing.Optional["LogsArchiveGcsArchive"], jsii.get(self, "gcsArchiveInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includeTagsInput")
    def include_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="rehydrationMaxScanSizeInGbInput")
    def rehydration_max_scan_size_in_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rehydrationMaxScanSizeInGbInput"))

    @builtins.property
    @jsii.member(jsii_name="rehydrationTagsInput")
    def rehydration_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rehydrationTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="s3ArchiveInput")
    def s3_archive_input(self) -> typing.Optional["LogsArchiveS3Archive"]:
        return typing.cast(typing.Optional["LogsArchiveS3Archive"], jsii.get(self, "s3ArchiveInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c268d8ab2f16ce33058607a19d72709d7af3289710bfff43b40ca2fcd22cf70c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeTags")
    def include_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeTags"))

    @include_tags.setter
    def include_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63a3cad81c553606c17251ed8bd08679dcc7ad7efb1ee2ca7ee76d4e2f4c4c4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1176767de3b55dc763e152cccc96458f23040c1fbfa17a1695a3aa92cc2daa1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e182ec9a0335fd2994b213b1f3aaeda64608323a594b3baf9c8d799918a62bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rehydrationMaxScanSizeInGb")
    def rehydration_max_scan_size_in_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rehydrationMaxScanSizeInGb"))

    @rehydration_max_scan_size_in_gb.setter
    def rehydration_max_scan_size_in_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06d0da49b2c60ae73020c11f7c94ff24994dd08504210ca56c00078dc9ee5c9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rehydrationMaxScanSizeInGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rehydrationTags")
    def rehydration_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rehydrationTags"))

    @rehydration_tags.setter
    def rehydration_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24e155308a17e10d03b1bd2f050c93e6d2675a9ce91868f0580e5a4048d41e8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rehydrationTags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsArchive.LogsArchiveAzureArchive",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "container": "container",
        "storage_account": "storageAccount",
        "tenant_id": "tenantId",
        "path": "path",
    },
)
class LogsArchiveAzureArchive:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        container: builtins.str,
        storage_account: builtins.str,
        tenant_id: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: Your client id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#client_id LogsArchive#client_id}
        :param container: The container where the archive is stored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#container LogsArchive#container}
        :param storage_account: The associated storage account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#storage_account LogsArchive#storage_account}
        :param tenant_id: Your tenant id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#tenant_id LogsArchive#tenant_id}
        :param path: The path where the archive is stored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#path LogsArchive#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__906b6ccc3905851f42ff1e28473feeda76202af64e9d12d49392ebeac20966fb)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument storage_account", value=storage_account, expected_type=type_hints["storage_account"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "container": container,
            "storage_account": storage_account,
            "tenant_id": tenant_id,
        }
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Your client id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#client_id LogsArchive#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container(self) -> builtins.str:
        '''The container where the archive is stored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#container LogsArchive#container}
        '''
        result = self._values.get("container")
        assert result is not None, "Required property 'container' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_account(self) -> builtins.str:
        '''The associated storage account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#storage_account LogsArchive#storage_account}
        '''
        result = self._values.get("storage_account")
        assert result is not None, "Required property 'storage_account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tenant_id(self) -> builtins.str:
        '''Your tenant id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#tenant_id LogsArchive#tenant_id}
        '''
        result = self._values.get("tenant_id")
        assert result is not None, "Required property 'tenant_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path where the archive is stored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#path LogsArchive#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsArchiveAzureArchive(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsArchiveAzureArchiveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsArchive.LogsArchiveAzureArchiveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__478e09bc88e9f0053fd92eff09193718e547d59409bc631206218f52ea178b76)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="containerInput")
    def container_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountInput")
    def storage_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09f5b7129de5baa0f113393f273d04bb40a7e2825f1ea6f8a79089746b9e608d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "container"))

    @container.setter
    def container(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e437ca9c8bde2816d5447b3c181969af3aa3f0211c962db49970b53c30370e71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "container", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c90342a7f22945ca2ae5125d61795c259056191733d2f82cfaf1723b4f5c5d06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccount")
    def storage_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccount"))

    @storage_account.setter
    def storage_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e75335dca3bee16acd3a8e83b54a3718811b36714aa245ece36e25272a111f9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4beb26040e28f03bed81cbb9be45661b1275141d427a9001ac7c1700cf682ae9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LogsArchiveAzureArchive]:
        return typing.cast(typing.Optional[LogsArchiveAzureArchive], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LogsArchiveAzureArchive]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b5ce57235e09c8859e5e597da148db52d2a937eb94fe60637dca53d67337349)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsArchive.LogsArchiveConfig",
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
        "query": "query",
        "azure_archive": "azureArchive",
        "gcs_archive": "gcsArchive",
        "id": "id",
        "include_tags": "includeTags",
        "rehydration_max_scan_size_in_gb": "rehydrationMaxScanSizeInGb",
        "rehydration_tags": "rehydrationTags",
        "s3_archive": "s3Archive",
    },
)
class LogsArchiveConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        query: builtins.str,
        azure_archive: typing.Optional[typing.Union[LogsArchiveAzureArchive, typing.Dict[builtins.str, typing.Any]]] = None,
        gcs_archive: typing.Optional[typing.Union["LogsArchiveGcsArchive", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        include_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rehydration_max_scan_size_in_gb: typing.Optional[jsii.Number] = None,
        rehydration_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        s3_archive: typing.Optional[typing.Union["LogsArchiveS3Archive", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Your archive name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#name LogsArchive#name}
        :param query: The archive query/filter. Logs matching this query are included in the archive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#query LogsArchive#query}
        :param azure_archive: azure_archive block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#azure_archive LogsArchive#azure_archive}
        :param gcs_archive: gcs_archive block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#gcs_archive LogsArchive#gcs_archive}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#id LogsArchive#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include_tags: To store the tags in the archive, set the value ``true``. If it is set to ``false``, the tags will be dropped when the logs are sent to the archive. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#include_tags LogsArchive#include_tags}
        :param rehydration_max_scan_size_in_gb: To limit the rehydration scan size for the archive, set a value in GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#rehydration_max_scan_size_in_gb LogsArchive#rehydration_max_scan_size_in_gb}
        :param rehydration_tags: An array of tags to add to rehydrated logs from an archive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#rehydration_tags LogsArchive#rehydration_tags}
        :param s3_archive: s3_archive block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#s3_archive LogsArchive#s3_archive}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(azure_archive, dict):
            azure_archive = LogsArchiveAzureArchive(**azure_archive)
        if isinstance(gcs_archive, dict):
            gcs_archive = LogsArchiveGcsArchive(**gcs_archive)
        if isinstance(s3_archive, dict):
            s3_archive = LogsArchiveS3Archive(**s3_archive)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce6ab933bf4a808b5000bd43487a3cb74e73162d6fa25903373ae2967bf6e196)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument azure_archive", value=azure_archive, expected_type=type_hints["azure_archive"])
            check_type(argname="argument gcs_archive", value=gcs_archive, expected_type=type_hints["gcs_archive"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument include_tags", value=include_tags, expected_type=type_hints["include_tags"])
            check_type(argname="argument rehydration_max_scan_size_in_gb", value=rehydration_max_scan_size_in_gb, expected_type=type_hints["rehydration_max_scan_size_in_gb"])
            check_type(argname="argument rehydration_tags", value=rehydration_tags, expected_type=type_hints["rehydration_tags"])
            check_type(argname="argument s3_archive", value=s3_archive, expected_type=type_hints["s3_archive"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "query": query,
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
        if azure_archive is not None:
            self._values["azure_archive"] = azure_archive
        if gcs_archive is not None:
            self._values["gcs_archive"] = gcs_archive
        if id is not None:
            self._values["id"] = id
        if include_tags is not None:
            self._values["include_tags"] = include_tags
        if rehydration_max_scan_size_in_gb is not None:
            self._values["rehydration_max_scan_size_in_gb"] = rehydration_max_scan_size_in_gb
        if rehydration_tags is not None:
            self._values["rehydration_tags"] = rehydration_tags
        if s3_archive is not None:
            self._values["s3_archive"] = s3_archive

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
        '''Your archive name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#name LogsArchive#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def query(self) -> builtins.str:
        '''The archive query/filter. Logs matching this query are included in the archive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#query LogsArchive#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def azure_archive(self) -> typing.Optional[LogsArchiveAzureArchive]:
        '''azure_archive block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#azure_archive LogsArchive#azure_archive}
        '''
        result = self._values.get("azure_archive")
        return typing.cast(typing.Optional[LogsArchiveAzureArchive], result)

    @builtins.property
    def gcs_archive(self) -> typing.Optional["LogsArchiveGcsArchive"]:
        '''gcs_archive block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#gcs_archive LogsArchive#gcs_archive}
        '''
        result = self._values.get("gcs_archive")
        return typing.cast(typing.Optional["LogsArchiveGcsArchive"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#id LogsArchive#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''To store the tags in the archive, set the value ``true``.

        If it is set to ``false``, the tags will be dropped when the logs are sent to the archive. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#include_tags LogsArchive#include_tags}
        '''
        result = self._values.get("include_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rehydration_max_scan_size_in_gb(self) -> typing.Optional[jsii.Number]:
        '''To limit the rehydration scan size for the archive, set a value in GB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#rehydration_max_scan_size_in_gb LogsArchive#rehydration_max_scan_size_in_gb}
        '''
        result = self._values.get("rehydration_max_scan_size_in_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rehydration_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of tags to add to rehydrated logs from an archive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#rehydration_tags LogsArchive#rehydration_tags}
        '''
        result = self._values.get("rehydration_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def s3_archive(self) -> typing.Optional["LogsArchiveS3Archive"]:
        '''s3_archive block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#s3_archive LogsArchive#s3_archive}
        '''
        result = self._values.get("s3_archive")
        return typing.cast(typing.Optional["LogsArchiveS3Archive"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsArchiveConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsArchive.LogsArchiveGcsArchive",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "client_email": "clientEmail",
        "path": "path",
        "project_id": "projectId",
    },
)
class LogsArchiveGcsArchive:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        client_email: builtins.str,
        path: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Name of your GCS bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#bucket LogsArchive#bucket}
        :param client_email: Your client email. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#client_email LogsArchive#client_email}
        :param path: Path where the archive is stored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#path LogsArchive#path}
        :param project_id: Your project id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#project_id LogsArchive#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cde829daff0fc4cc97d6cb6900074d4fc0b14d9d1c0478e07057eed34368f8b9)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument client_email", value=client_email, expected_type=type_hints["client_email"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "client_email": client_email,
        }
        if path is not None:
            self._values["path"] = path
        if project_id is not None:
            self._values["project_id"] = project_id

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Name of your GCS bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#bucket LogsArchive#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_email(self) -> builtins.str:
        '''Your client email.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#client_email LogsArchive#client_email}
        '''
        result = self._values.get("client_email")
        assert result is not None, "Required property 'client_email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path where the archive is stored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#path LogsArchive#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''Your project id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#project_id LogsArchive#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsArchiveGcsArchive(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsArchiveGcsArchiveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsArchive.LogsArchiveGcsArchiveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18d1aaf81d78c61f049eefb43bbb1cbad45fddeda3ac7b07229df4c3f44f350a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="clientEmailInput")
    def client_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ed24b2329aadcf8e1d007785c7d6297df224a354ae98af4348ab499f71ab716)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientEmail")
    def client_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientEmail"))

    @client_email.setter
    def client_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__375982b5e188630598781099f91980e5042dfab15c5484e64c6b03d6d9924e58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363b2d3b6c72adf3b82f338fe07a550461e5bc8d19d53143b2528c9e2c07850e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__361ccd25a1127c98168bec048d8f6863cf3c72a406f83922ad1d30093fa2b7ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LogsArchiveGcsArchive]:
        return typing.cast(typing.Optional[LogsArchiveGcsArchive], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LogsArchiveGcsArchive]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2171aba37938e5b090212f9ce2e6fadf9b1b30fe5b762059e4c713ae8a4962b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsArchive.LogsArchiveS3Archive",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "bucket": "bucket",
        "role_name": "roleName",
        "encryption_key": "encryptionKey",
        "encryption_type": "encryptionType",
        "path": "path",
        "storage_class": "storageClass",
    },
)
class LogsArchiveS3Archive:
    def __init__(
        self,
        *,
        account_id: builtins.str,
        bucket: builtins.str,
        role_name: builtins.str,
        encryption_key: typing.Optional[builtins.str] = None,
        encryption_type: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        storage_class: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_id: Your AWS account id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#account_id LogsArchive#account_id}
        :param bucket: Name of your s3 bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#bucket LogsArchive#bucket}
        :param role_name: Your AWS role name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#role_name LogsArchive#role_name}
        :param encryption_key: The AWS KMS encryption key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#encryption_key LogsArchive#encryption_key}
        :param encryption_type: The type of encryption on your archive. Valid values are ``NO_OVERRIDE``, ``SSE_S3``, ``SSE_KMS``. Defaults to ``"NO_OVERRIDE"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#encryption_type LogsArchive#encryption_type}
        :param path: Path where the archive is stored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#path LogsArchive#path}
        :param storage_class: The AWS S3 storage class used to upload the logs. Valid values are ``STANDARD``, ``STANDARD_IA``, ``ONEZONE_IA``, ``INTELLIGENT_TIERING``, ``GLACIER_IR``. Defaults to ``"STANDARD"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#storage_class LogsArchive#storage_class}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd454c112015d42664507b0b6b9127ec63733b12fde93e61ff860c1edb1b979e)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "bucket": bucket,
            "role_name": role_name,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if encryption_type is not None:
            self._values["encryption_type"] = encryption_type
        if path is not None:
            self._values["path"] = path
        if storage_class is not None:
            self._values["storage_class"] = storage_class

    @builtins.property
    def account_id(self) -> builtins.str:
        '''Your AWS account id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#account_id LogsArchive#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Name of your s3 bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#bucket LogsArchive#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_name(self) -> builtins.str:
        '''Your AWS role name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#role_name LogsArchive#role_name}
        '''
        result = self._values.get("role_name")
        assert result is not None, "Required property 'role_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[builtins.str]:
        '''The AWS KMS encryption key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#encryption_key LogsArchive#encryption_key}
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_type(self) -> typing.Optional[builtins.str]:
        '''The type of encryption on your archive. Valid values are ``NO_OVERRIDE``, ``SSE_S3``, ``SSE_KMS``. Defaults to ``"NO_OVERRIDE"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#encryption_type LogsArchive#encryption_type}
        '''
        result = self._values.get("encryption_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path where the archive is stored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#path LogsArchive#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_class(self) -> typing.Optional[builtins.str]:
        '''The AWS S3 storage class used to upload the logs.

        Valid values are ``STANDARD``, ``STANDARD_IA``, ``ONEZONE_IA``, ``INTELLIGENT_TIERING``, ``GLACIER_IR``. Defaults to ``"STANDARD"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_archive#storage_class LogsArchive#storage_class}
        '''
        result = self._values.get("storage_class")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsArchiveS3Archive(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsArchiveS3ArchiveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsArchive.LogsArchiveS3ArchiveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8813206619c5a25c41463ecfb20fed48438b2100e7773843292891c2ed4ba11b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEncryptionKey")
    def reset_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKey", []))

    @jsii.member(jsii_name="resetEncryptionType")
    def reset_encryption_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionType", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetStorageClass")
    def reset_storage_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageClass", []))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyInput")
    def encryption_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionTypeInput")
    def encryption_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="roleNameInput")
    def role_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageClassInput")
    def storage_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageClassInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e41ed42ff93fe7f019bf484058ce7100265314494d26eaf541461103109107f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df6e73db1126ea1dc807970982536141b458633560b9cda1c8309f2dd070480d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionKey"))

    @encryption_key.setter
    def encryption_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a3d6aa56e6d4558dde680a16419ef399a4fa54d29abbfb04930cd9af46245ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionType")
    def encryption_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionType"))

    @encryption_type.setter
    def encryption_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__524d8ab87fae149fe8250e8ac83756c6f283433f2945d3fcfc7d261457be493f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0110d375dab195cb675d113212d646bd863136f580351dd4c8716ff8dee54fca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleName"))

    @role_name.setter
    def role_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9110e3b99384190317ad98f6b766081c0ae9d98f2325122a80f743ce2c9301df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageClass")
    def storage_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageClass"))

    @storage_class.setter
    def storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91da952f35fb529de79636b9dc950e659562ebf99652c849a55efc91ad5052e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LogsArchiveS3Archive]:
        return typing.cast(typing.Optional[LogsArchiveS3Archive], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LogsArchiveS3Archive]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e976626d23fed10b3c538086bd76838072b036560540e4eabef02de72f0ff2ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LogsArchive",
    "LogsArchiveAzureArchive",
    "LogsArchiveAzureArchiveOutputReference",
    "LogsArchiveConfig",
    "LogsArchiveGcsArchive",
    "LogsArchiveGcsArchiveOutputReference",
    "LogsArchiveS3Archive",
    "LogsArchiveS3ArchiveOutputReference",
]

publication.publish()

def _typecheckingstub__85c096907faabee57f3d9412a01deecc62a69d390e213f8f3760195ad3091c5f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    query: builtins.str,
    azure_archive: typing.Optional[typing.Union[LogsArchiveAzureArchive, typing.Dict[builtins.str, typing.Any]]] = None,
    gcs_archive: typing.Optional[typing.Union[LogsArchiveGcsArchive, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    include_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rehydration_max_scan_size_in_gb: typing.Optional[jsii.Number] = None,
    rehydration_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_archive: typing.Optional[typing.Union[LogsArchiveS3Archive, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__33b79d4cec0cae5ef69b4bbcdf2375211ac0fa409a4e219841a3c3d5c7687b6f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c268d8ab2f16ce33058607a19d72709d7af3289710bfff43b40ca2fcd22cf70c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63a3cad81c553606c17251ed8bd08679dcc7ad7efb1ee2ca7ee76d4e2f4c4c4c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1176767de3b55dc763e152cccc96458f23040c1fbfa17a1695a3aa92cc2daa1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e182ec9a0335fd2994b213b1f3aaeda64608323a594b3baf9c8d799918a62bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06d0da49b2c60ae73020c11f7c94ff24994dd08504210ca56c00078dc9ee5c9f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e155308a17e10d03b1bd2f050c93e6d2675a9ce91868f0580e5a4048d41e8e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906b6ccc3905851f42ff1e28473feeda76202af64e9d12d49392ebeac20966fb(
    *,
    client_id: builtins.str,
    container: builtins.str,
    storage_account: builtins.str,
    tenant_id: builtins.str,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__478e09bc88e9f0053fd92eff09193718e547d59409bc631206218f52ea178b76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09f5b7129de5baa0f113393f273d04bb40a7e2825f1ea6f8a79089746b9e608d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e437ca9c8bde2816d5447b3c181969af3aa3f0211c962db49970b53c30370e71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c90342a7f22945ca2ae5125d61795c259056191733d2f82cfaf1723b4f5c5d06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e75335dca3bee16acd3a8e83b54a3718811b36714aa245ece36e25272a111f9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4beb26040e28f03bed81cbb9be45661b1275141d427a9001ac7c1700cf682ae9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b5ce57235e09c8859e5e597da148db52d2a937eb94fe60637dca53d67337349(
    value: typing.Optional[LogsArchiveAzureArchive],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce6ab933bf4a808b5000bd43487a3cb74e73162d6fa25903373ae2967bf6e196(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    query: builtins.str,
    azure_archive: typing.Optional[typing.Union[LogsArchiveAzureArchive, typing.Dict[builtins.str, typing.Any]]] = None,
    gcs_archive: typing.Optional[typing.Union[LogsArchiveGcsArchive, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    include_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rehydration_max_scan_size_in_gb: typing.Optional[jsii.Number] = None,
    rehydration_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_archive: typing.Optional[typing.Union[LogsArchiveS3Archive, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cde829daff0fc4cc97d6cb6900074d4fc0b14d9d1c0478e07057eed34368f8b9(
    *,
    bucket: builtins.str,
    client_email: builtins.str,
    path: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d1aaf81d78c61f049eefb43bbb1cbad45fddeda3ac7b07229df4c3f44f350a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ed24b2329aadcf8e1d007785c7d6297df224a354ae98af4348ab499f71ab716(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__375982b5e188630598781099f91980e5042dfab15c5484e64c6b03d6d9924e58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363b2d3b6c72adf3b82f338fe07a550461e5bc8d19d53143b2528c9e2c07850e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361ccd25a1127c98168bec048d8f6863cf3c72a406f83922ad1d30093fa2b7ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2171aba37938e5b090212f9ce2e6fadf9b1b30fe5b762059e4c713ae8a4962b0(
    value: typing.Optional[LogsArchiveGcsArchive],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd454c112015d42664507b0b6b9127ec63733b12fde93e61ff860c1edb1b979e(
    *,
    account_id: builtins.str,
    bucket: builtins.str,
    role_name: builtins.str,
    encryption_key: typing.Optional[builtins.str] = None,
    encryption_type: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    storage_class: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8813206619c5a25c41463ecfb20fed48438b2100e7773843292891c2ed4ba11b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e41ed42ff93fe7f019bf484058ce7100265314494d26eaf541461103109107f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df6e73db1126ea1dc807970982536141b458633560b9cda1c8309f2dd070480d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a3d6aa56e6d4558dde680a16419ef399a4fa54d29abbfb04930cd9af46245ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__524d8ab87fae149fe8250e8ac83756c6f283433f2945d3fcfc7d261457be493f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0110d375dab195cb675d113212d646bd863136f580351dd4c8716ff8dee54fca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9110e3b99384190317ad98f6b766081c0ae9d98f2325122a80f743ce2c9301df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91da952f35fb529de79636b9dc950e659562ebf99652c849a55efc91ad5052e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e976626d23fed10b3c538086bd76838072b036560540e4eabef02de72f0ff2ac(
    value: typing.Optional[LogsArchiveS3Archive],
) -> None:
    """Type checking stubs"""
    pass
