r'''
# `google_storage_batch_operations_job`

Refer to the Terraform Registry for docs: [`google_storage_batch_operations_job`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job).
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


class GoogleStorageBatchOperationsJob(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBatchOperationsJob.GoogleStorageBatchOperationsJob",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job google_storage_batch_operations_job}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        bucket_list: typing.Optional[typing.Union["GoogleStorageBatchOperationsJobBucketListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
        delete_object: typing.Optional[typing.Union["GoogleStorageBatchOperationsJobDeleteObject", typing.Dict[builtins.str, typing.Any]]] = None,
        delete_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        job_id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        put_metadata: typing.Optional[typing.Union["GoogleStorageBatchOperationsJobPutMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        put_object_hold: typing.Optional[typing.Union["GoogleStorageBatchOperationsJobPutObjectHold", typing.Dict[builtins.str, typing.Any]]] = None,
        rewrite_object: typing.Optional[typing.Union["GoogleStorageBatchOperationsJobRewriteObject", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleStorageBatchOperationsJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job google_storage_batch_operations_job} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bucket_list: bucket_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#bucket_list GoogleStorageBatchOperationsJob#bucket_list}
        :param delete_object: delete_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#delete_object GoogleStorageBatchOperationsJob#delete_object}
        :param delete_protection: If set to 'true', the storage batch operation job will not be deleted and new job will be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#delete_protection GoogleStorageBatchOperationsJob#delete_protection}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#id GoogleStorageBatchOperationsJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param job_id: The ID of the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#job_id GoogleStorageBatchOperationsJob#job_id}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#project GoogleStorageBatchOperationsJob#project}.
        :param put_metadata: put_metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#put_metadata GoogleStorageBatchOperationsJob#put_metadata}
        :param put_object_hold: put_object_hold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#put_object_hold GoogleStorageBatchOperationsJob#put_object_hold}
        :param rewrite_object: rewrite_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#rewrite_object GoogleStorageBatchOperationsJob#rewrite_object}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#timeouts GoogleStorageBatchOperationsJob#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__705b718e96f9e415ab41dbb19ad0ab3d60084937bb35bde493275d0f3cf8a77e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleStorageBatchOperationsJobConfig(
            bucket_list=bucket_list,
            delete_object=delete_object,
            delete_protection=delete_protection,
            id=id,
            job_id=job_id,
            project=project,
            put_metadata=put_metadata,
            put_object_hold=put_object_hold,
            rewrite_object=rewrite_object,
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
        '''Generates CDKTF code for importing a GoogleStorageBatchOperationsJob resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleStorageBatchOperationsJob to import.
        :param import_from_id: The id of the existing GoogleStorageBatchOperationsJob that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleStorageBatchOperationsJob to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__603f215b4b93e83f8eaff21497e340c552674ad52f70770bcff3ccbfdc4ed928)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBucketList")
    def put_bucket_list(
        self,
        *,
        buckets: typing.Union["GoogleStorageBatchOperationsJobBucketListBuckets", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param buckets: buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#buckets GoogleStorageBatchOperationsJob#buckets}
        '''
        value = GoogleStorageBatchOperationsJobBucketListStruct(buckets=buckets)

        return typing.cast(None, jsii.invoke(self, "putBucketList", [value]))

    @jsii.member(jsii_name="putDeleteObject")
    def put_delete_object(
        self,
        *,
        permanent_object_deletion_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param permanent_object_deletion_enabled: enable flag to permanently delete object and all object versions if versioning is enabled on bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#permanent_object_deletion_enabled GoogleStorageBatchOperationsJob#permanent_object_deletion_enabled}
        '''
        value = GoogleStorageBatchOperationsJobDeleteObject(
            permanent_object_deletion_enabled=permanent_object_deletion_enabled
        )

        return typing.cast(None, jsii.invoke(self, "putDeleteObject", [value]))

    @jsii.member(jsii_name="putPutMetadata")
    def put_put_metadata(
        self,
        *,
        cache_control: typing.Optional[builtins.str] = None,
        content_disposition: typing.Optional[builtins.str] = None,
        content_encoding: typing.Optional[builtins.str] = None,
        content_language: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
        custom_metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        custom_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cache_control: Cache-Control directive to specify caching behavior of object data. If omitted and object is accessible to all anonymous users, the default will be public, max-age=3600 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#cache_control GoogleStorageBatchOperationsJob#cache_control}
        :param content_disposition: Content-Disposition of the object data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#content_disposition GoogleStorageBatchOperationsJob#content_disposition}
        :param content_encoding: Content Encoding of the object data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#content_encoding GoogleStorageBatchOperationsJob#content_encoding}
        :param content_language: Content-Language of the object data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#content_language GoogleStorageBatchOperationsJob#content_language}
        :param content_type: Content-Type of the object data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#content_type GoogleStorageBatchOperationsJob#content_type}
        :param custom_metadata: User-provided metadata, in key/value pairs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#custom_metadata GoogleStorageBatchOperationsJob#custom_metadata}
        :param custom_time: Updates the objects fixed custom time metadata. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#custom_time GoogleStorageBatchOperationsJob#custom_time}
        '''
        value = GoogleStorageBatchOperationsJobPutMetadata(
            cache_control=cache_control,
            content_disposition=content_disposition,
            content_encoding=content_encoding,
            content_language=content_language,
            content_type=content_type,
            custom_metadata=custom_metadata,
            custom_time=custom_time,
        )

        return typing.cast(None, jsii.invoke(self, "putPutMetadata", [value]))

    @jsii.member(jsii_name="putPutObjectHold")
    def put_put_object_hold(
        self,
        *,
        event_based_hold: typing.Optional[builtins.str] = None,
        temporary_hold: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param event_based_hold: set/unset to update event based hold for objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#event_based_hold GoogleStorageBatchOperationsJob#event_based_hold}
        :param temporary_hold: set/unset to update temporary based hold for objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#temporary_hold GoogleStorageBatchOperationsJob#temporary_hold}
        '''
        value = GoogleStorageBatchOperationsJobPutObjectHold(
            event_based_hold=event_based_hold, temporary_hold=temporary_hold
        )

        return typing.cast(None, jsii.invoke(self, "putPutObjectHold", [value]))

    @jsii.member(jsii_name="putRewriteObject")
    def put_rewrite_object(self, *, kms_key: builtins.str) -> None:
        '''
        :param kms_key: valid kms key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#kms_key GoogleStorageBatchOperationsJob#kms_key}
        '''
        value = GoogleStorageBatchOperationsJobRewriteObject(kms_key=kms_key)

        return typing.cast(None, jsii.invoke(self, "putRewriteObject", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#create GoogleStorageBatchOperationsJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#delete GoogleStorageBatchOperationsJob#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#update GoogleStorageBatchOperationsJob#update}.
        '''
        value = GoogleStorageBatchOperationsJobTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBucketList")
    def reset_bucket_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketList", []))

    @jsii.member(jsii_name="resetDeleteObject")
    def reset_delete_object(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteObject", []))

    @jsii.member(jsii_name="resetDeleteProtection")
    def reset_delete_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteProtection", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetJobId")
    def reset_job_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJobId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPutMetadata")
    def reset_put_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPutMetadata", []))

    @jsii.member(jsii_name="resetPutObjectHold")
    def reset_put_object_hold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPutObjectHold", []))

    @jsii.member(jsii_name="resetRewriteObject")
    def reset_rewrite_object(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRewriteObject", []))

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
    @jsii.member(jsii_name="bucketList")
    def bucket_list(
        self,
    ) -> "GoogleStorageBatchOperationsJobBucketListStructOutputReference":
        return typing.cast("GoogleStorageBatchOperationsJobBucketListStructOutputReference", jsii.get(self, "bucketList"))

    @builtins.property
    @jsii.member(jsii_name="completeTime")
    def complete_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "completeTime"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="deleteObject")
    def delete_object(
        self,
    ) -> "GoogleStorageBatchOperationsJobDeleteObjectOutputReference":
        return typing.cast("GoogleStorageBatchOperationsJobDeleteObjectOutputReference", jsii.get(self, "deleteObject"))

    @builtins.property
    @jsii.member(jsii_name="putMetadata")
    def put_metadata(
        self,
    ) -> "GoogleStorageBatchOperationsJobPutMetadataOutputReference":
        return typing.cast("GoogleStorageBatchOperationsJobPutMetadataOutputReference", jsii.get(self, "putMetadata"))

    @builtins.property
    @jsii.member(jsii_name="putObjectHold")
    def put_object_hold(
        self,
    ) -> "GoogleStorageBatchOperationsJobPutObjectHoldOutputReference":
        return typing.cast("GoogleStorageBatchOperationsJobPutObjectHoldOutputReference", jsii.get(self, "putObjectHold"))

    @builtins.property
    @jsii.member(jsii_name="rewriteObject")
    def rewrite_object(
        self,
    ) -> "GoogleStorageBatchOperationsJobRewriteObjectOutputReference":
        return typing.cast("GoogleStorageBatchOperationsJobRewriteObjectOutputReference", jsii.get(self, "rewriteObject"))

    @builtins.property
    @jsii.member(jsii_name="scheduleTime")
    def schedule_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheduleTime"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleStorageBatchOperationsJobTimeoutsOutputReference":
        return typing.cast("GoogleStorageBatchOperationsJobTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="bucketListInput")
    def bucket_list_input(
        self,
    ) -> typing.Optional["GoogleStorageBatchOperationsJobBucketListStruct"]:
        return typing.cast(typing.Optional["GoogleStorageBatchOperationsJobBucketListStruct"], jsii.get(self, "bucketListInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteObjectInput")
    def delete_object_input(
        self,
    ) -> typing.Optional["GoogleStorageBatchOperationsJobDeleteObject"]:
        return typing.cast(typing.Optional["GoogleStorageBatchOperationsJobDeleteObject"], jsii.get(self, "deleteObjectInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteProtectionInput")
    def delete_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="jobIdInput")
    def job_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="putMetadataInput")
    def put_metadata_input(
        self,
    ) -> typing.Optional["GoogleStorageBatchOperationsJobPutMetadata"]:
        return typing.cast(typing.Optional["GoogleStorageBatchOperationsJobPutMetadata"], jsii.get(self, "putMetadataInput"))

    @builtins.property
    @jsii.member(jsii_name="putObjectHoldInput")
    def put_object_hold_input(
        self,
    ) -> typing.Optional["GoogleStorageBatchOperationsJobPutObjectHold"]:
        return typing.cast(typing.Optional["GoogleStorageBatchOperationsJobPutObjectHold"], jsii.get(self, "putObjectHoldInput"))

    @builtins.property
    @jsii.member(jsii_name="rewriteObjectInput")
    def rewrite_object_input(
        self,
    ) -> typing.Optional["GoogleStorageBatchOperationsJobRewriteObject"]:
        return typing.cast(typing.Optional["GoogleStorageBatchOperationsJobRewriteObject"], jsii.get(self, "rewriteObjectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleStorageBatchOperationsJobTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleStorageBatchOperationsJobTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteProtection")
    def delete_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteProtection"))

    @delete_protection.setter
    def delete_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16a9ba97fe93c0f84158ef92fd486b8d3b113672df19a3b89837d48d9c0e26df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e2fa323eb795bc4d7d2c11d09d9a4f4a6ef07b245e05c8e5b0d2723baa7fdb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobId")
    def job_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobId"))

    @job_id.setter
    def job_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a8643f08afa668de7d34b2a3f4f409d436b8bdeabf48d27a1a7c40d1602e7b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3662ac88128d5d694e4ced9a24abc5339ee512ec35a3b209245954fe33f523d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBatchOperationsJob.GoogleStorageBatchOperationsJobBucketListBuckets",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "manifest": "manifest",
        "prefix_list": "prefixList",
    },
)
class GoogleStorageBatchOperationsJobBucketListBuckets:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        manifest: typing.Optional[typing.Union["GoogleStorageBatchOperationsJobBucketListBucketsManifest", typing.Dict[builtins.str, typing.Any]]] = None,
        prefix_list: typing.Optional[typing.Union["GoogleStorageBatchOperationsJobBucketListBucketsPrefixListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket: Bucket name for the objects to be transformed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#bucket GoogleStorageBatchOperationsJob#bucket}
        :param manifest: manifest block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#manifest GoogleStorageBatchOperationsJob#manifest}
        :param prefix_list: prefix_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#prefix_list GoogleStorageBatchOperationsJob#prefix_list}
        '''
        if isinstance(manifest, dict):
            manifest = GoogleStorageBatchOperationsJobBucketListBucketsManifest(**manifest)
        if isinstance(prefix_list, dict):
            prefix_list = GoogleStorageBatchOperationsJobBucketListBucketsPrefixListStruct(**prefix_list)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d575e7e0f7f90eaabbbe2d4a1d5e118c0914a21a1f9fa93d5c9f83a8385c295)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument manifest", value=manifest, expected_type=type_hints["manifest"])
            check_type(argname="argument prefix_list", value=prefix_list, expected_type=type_hints["prefix_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }
        if manifest is not None:
            self._values["manifest"] = manifest
        if prefix_list is not None:
            self._values["prefix_list"] = prefix_list

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Bucket name for the objects to be transformed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#bucket GoogleStorageBatchOperationsJob#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def manifest(
        self,
    ) -> typing.Optional["GoogleStorageBatchOperationsJobBucketListBucketsManifest"]:
        '''manifest block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#manifest GoogleStorageBatchOperationsJob#manifest}
        '''
        result = self._values.get("manifest")
        return typing.cast(typing.Optional["GoogleStorageBatchOperationsJobBucketListBucketsManifest"], result)

    @builtins.property
    def prefix_list(
        self,
    ) -> typing.Optional["GoogleStorageBatchOperationsJobBucketListBucketsPrefixListStruct"]:
        '''prefix_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#prefix_list GoogleStorageBatchOperationsJob#prefix_list}
        '''
        result = self._values.get("prefix_list")
        return typing.cast(typing.Optional["GoogleStorageBatchOperationsJobBucketListBucketsPrefixListStruct"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBatchOperationsJobBucketListBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBatchOperationsJob.GoogleStorageBatchOperationsJobBucketListBucketsManifest",
    jsii_struct_bases=[],
    name_mapping={"manifest_location": "manifestLocation"},
)
class GoogleStorageBatchOperationsJobBucketListBucketsManifest:
    def __init__(
        self,
        *,
        manifest_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param manifest_location: Specifies objects in a manifest file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#manifest_location GoogleStorageBatchOperationsJob#manifest_location}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7963fc59265aefcc8a4490781442b612119050812566ac11962c322964b9ab4)
            check_type(argname="argument manifest_location", value=manifest_location, expected_type=type_hints["manifest_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if manifest_location is not None:
            self._values["manifest_location"] = manifest_location

    @builtins.property
    def manifest_location(self) -> typing.Optional[builtins.str]:
        '''Specifies objects in a manifest file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#manifest_location GoogleStorageBatchOperationsJob#manifest_location}
        '''
        result = self._values.get("manifest_location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBatchOperationsJobBucketListBucketsManifest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBatchOperationsJobBucketListBucketsManifestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBatchOperationsJob.GoogleStorageBatchOperationsJobBucketListBucketsManifestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe017daf4cd40eaf4e332460cd8fd70771a9c1790fb48d1189be949982a7f177)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetManifestLocation")
    def reset_manifest_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManifestLocation", []))

    @builtins.property
    @jsii.member(jsii_name="manifestLocationInput")
    def manifest_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "manifestLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="manifestLocation")
    def manifest_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "manifestLocation"))

    @manifest_location.setter
    def manifest_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0f4587d46aaa6488497d87ac6bfe8f6a45b47d679459ac7d8b443358dd9ff41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manifestLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageBatchOperationsJobBucketListBucketsManifest]:
        return typing.cast(typing.Optional[GoogleStorageBatchOperationsJobBucketListBucketsManifest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageBatchOperationsJobBucketListBucketsManifest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d2d79a65f02c6590f2700bae776635d173aa2db0851dd10cbf608c43315e001)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleStorageBatchOperationsJobBucketListBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBatchOperationsJob.GoogleStorageBatchOperationsJobBucketListBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__650e3cadcf1f0af53806fc062d97ccc8647935960cdc64ee98fa1ee6590c2c10)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putManifest")
    def put_manifest(
        self,
        *,
        manifest_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param manifest_location: Specifies objects in a manifest file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#manifest_location GoogleStorageBatchOperationsJob#manifest_location}
        '''
        value = GoogleStorageBatchOperationsJobBucketListBucketsManifest(
            manifest_location=manifest_location
        )

        return typing.cast(None, jsii.invoke(self, "putManifest", [value]))

    @jsii.member(jsii_name="putPrefixList")
    def put_prefix_list(
        self,
        *,
        included_object_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param included_object_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#included_object_prefixes GoogleStorageBatchOperationsJob#included_object_prefixes}.
        '''
        value = GoogleStorageBatchOperationsJobBucketListBucketsPrefixListStruct(
            included_object_prefixes=included_object_prefixes
        )

        return typing.cast(None, jsii.invoke(self, "putPrefixList", [value]))

    @jsii.member(jsii_name="resetManifest")
    def reset_manifest(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManifest", []))

    @jsii.member(jsii_name="resetPrefixList")
    def reset_prefix_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixList", []))

    @builtins.property
    @jsii.member(jsii_name="manifest")
    def manifest(
        self,
    ) -> GoogleStorageBatchOperationsJobBucketListBucketsManifestOutputReference:
        return typing.cast(GoogleStorageBatchOperationsJobBucketListBucketsManifestOutputReference, jsii.get(self, "manifest"))

    @builtins.property
    @jsii.member(jsii_name="prefixList")
    def prefix_list(
        self,
    ) -> "GoogleStorageBatchOperationsJobBucketListBucketsPrefixListStructOutputReference":
        return typing.cast("GoogleStorageBatchOperationsJobBucketListBucketsPrefixListStructOutputReference", jsii.get(self, "prefixList"))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="manifestInput")
    def manifest_input(
        self,
    ) -> typing.Optional[GoogleStorageBatchOperationsJobBucketListBucketsManifest]:
        return typing.cast(typing.Optional[GoogleStorageBatchOperationsJobBucketListBucketsManifest], jsii.get(self, "manifestInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixListInput")
    def prefix_list_input(
        self,
    ) -> typing.Optional["GoogleStorageBatchOperationsJobBucketListBucketsPrefixListStruct"]:
        return typing.cast(typing.Optional["GoogleStorageBatchOperationsJobBucketListBucketsPrefixListStruct"], jsii.get(self, "prefixListInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a90b71818988d7da12373b596030a087dc7dad7027f733513e7200897f60c78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageBatchOperationsJobBucketListBuckets]:
        return typing.cast(typing.Optional[GoogleStorageBatchOperationsJobBucketListBuckets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageBatchOperationsJobBucketListBuckets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d24f09f70cc33799b3fd0bdc113efc9cb7665eba46426aa2a5293b476c5c612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBatchOperationsJob.GoogleStorageBatchOperationsJobBucketListBucketsPrefixListStruct",
    jsii_struct_bases=[],
    name_mapping={"included_object_prefixes": "includedObjectPrefixes"},
)
class GoogleStorageBatchOperationsJobBucketListBucketsPrefixListStruct:
    def __init__(
        self,
        *,
        included_object_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param included_object_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#included_object_prefixes GoogleStorageBatchOperationsJob#included_object_prefixes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e816eb3f25ded2443ff02523c4cd5e2e50ea603881bc4802c1a34c65f39204e)
            check_type(argname="argument included_object_prefixes", value=included_object_prefixes, expected_type=type_hints["included_object_prefixes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if included_object_prefixes is not None:
            self._values["included_object_prefixes"] = included_object_prefixes

    @builtins.property
    def included_object_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#included_object_prefixes GoogleStorageBatchOperationsJob#included_object_prefixes}.'''
        result = self._values.get("included_object_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBatchOperationsJobBucketListBucketsPrefixListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBatchOperationsJobBucketListBucketsPrefixListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBatchOperationsJob.GoogleStorageBatchOperationsJobBucketListBucketsPrefixListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff1437ff3878c10a48dfca852758c1e9e4e23f685c1b365c2aed5550e95c80ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIncludedObjectPrefixes")
    def reset_included_object_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedObjectPrefixes", []))

    @builtins.property
    @jsii.member(jsii_name="includedObjectPrefixesInput")
    def included_object_prefixes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedObjectPrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="includedObjectPrefixes")
    def included_object_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedObjectPrefixes"))

    @included_object_prefixes.setter
    def included_object_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9672234acb4e79e416e445a17d82ba2bfc386e1ae57f2dab67ff0ff5b026ba6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedObjectPrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageBatchOperationsJobBucketListBucketsPrefixListStruct]:
        return typing.cast(typing.Optional[GoogleStorageBatchOperationsJobBucketListBucketsPrefixListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageBatchOperationsJobBucketListBucketsPrefixListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54e1bb2ff2abf08c7aa06982f54cddf35dd8b84961e5a0c8c79c6dfddf39b40b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBatchOperationsJob.GoogleStorageBatchOperationsJobBucketListStruct",
    jsii_struct_bases=[],
    name_mapping={"buckets": "buckets"},
)
class GoogleStorageBatchOperationsJobBucketListStruct:
    def __init__(
        self,
        *,
        buckets: typing.Union[GoogleStorageBatchOperationsJobBucketListBuckets, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param buckets: buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#buckets GoogleStorageBatchOperationsJob#buckets}
        '''
        if isinstance(buckets, dict):
            buckets = GoogleStorageBatchOperationsJobBucketListBuckets(**buckets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee3bd9ff4541731f7f188b7893eedb7c7e63a9a216aeec4bf6f9adb963e0b710)
            check_type(argname="argument buckets", value=buckets, expected_type=type_hints["buckets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "buckets": buckets,
        }

    @builtins.property
    def buckets(self) -> GoogleStorageBatchOperationsJobBucketListBuckets:
        '''buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#buckets GoogleStorageBatchOperationsJob#buckets}
        '''
        result = self._values.get("buckets")
        assert result is not None, "Required property 'buckets' is missing"
        return typing.cast(GoogleStorageBatchOperationsJobBucketListBuckets, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBatchOperationsJobBucketListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBatchOperationsJobBucketListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBatchOperationsJob.GoogleStorageBatchOperationsJobBucketListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f2f03e0a84c8c9d2f1b213e6ea4bd5134b88d54254dbb49b0fb80727e97c7bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBuckets")
    def put_buckets(
        self,
        *,
        bucket: builtins.str,
        manifest: typing.Optional[typing.Union[GoogleStorageBatchOperationsJobBucketListBucketsManifest, typing.Dict[builtins.str, typing.Any]]] = None,
        prefix_list: typing.Optional[typing.Union[GoogleStorageBatchOperationsJobBucketListBucketsPrefixListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket: Bucket name for the objects to be transformed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#bucket GoogleStorageBatchOperationsJob#bucket}
        :param manifest: manifest block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#manifest GoogleStorageBatchOperationsJob#manifest}
        :param prefix_list: prefix_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#prefix_list GoogleStorageBatchOperationsJob#prefix_list}
        '''
        value = GoogleStorageBatchOperationsJobBucketListBuckets(
            bucket=bucket, manifest=manifest, prefix_list=prefix_list
        )

        return typing.cast(None, jsii.invoke(self, "putBuckets", [value]))

    @builtins.property
    @jsii.member(jsii_name="buckets")
    def buckets(
        self,
    ) -> GoogleStorageBatchOperationsJobBucketListBucketsOutputReference:
        return typing.cast(GoogleStorageBatchOperationsJobBucketListBucketsOutputReference, jsii.get(self, "buckets"))

    @builtins.property
    @jsii.member(jsii_name="bucketsInput")
    def buckets_input(
        self,
    ) -> typing.Optional[GoogleStorageBatchOperationsJobBucketListBuckets]:
        return typing.cast(typing.Optional[GoogleStorageBatchOperationsJobBucketListBuckets], jsii.get(self, "bucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageBatchOperationsJobBucketListStruct]:
        return typing.cast(typing.Optional[GoogleStorageBatchOperationsJobBucketListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageBatchOperationsJobBucketListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d449702ae2e062c69bae1b6eb7b16c8e317e5b34385b2e21824fe3ea515f184e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBatchOperationsJob.GoogleStorageBatchOperationsJobConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "bucket_list": "bucketList",
        "delete_object": "deleteObject",
        "delete_protection": "deleteProtection",
        "id": "id",
        "job_id": "jobId",
        "project": "project",
        "put_metadata": "putMetadata",
        "put_object_hold": "putObjectHold",
        "rewrite_object": "rewriteObject",
        "timeouts": "timeouts",
    },
)
class GoogleStorageBatchOperationsJobConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bucket_list: typing.Optional[typing.Union[GoogleStorageBatchOperationsJobBucketListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
        delete_object: typing.Optional[typing.Union["GoogleStorageBatchOperationsJobDeleteObject", typing.Dict[builtins.str, typing.Any]]] = None,
        delete_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        job_id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        put_metadata: typing.Optional[typing.Union["GoogleStorageBatchOperationsJobPutMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        put_object_hold: typing.Optional[typing.Union["GoogleStorageBatchOperationsJobPutObjectHold", typing.Dict[builtins.str, typing.Any]]] = None,
        rewrite_object: typing.Optional[typing.Union["GoogleStorageBatchOperationsJobRewriteObject", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleStorageBatchOperationsJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bucket_list: bucket_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#bucket_list GoogleStorageBatchOperationsJob#bucket_list}
        :param delete_object: delete_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#delete_object GoogleStorageBatchOperationsJob#delete_object}
        :param delete_protection: If set to 'true', the storage batch operation job will not be deleted and new job will be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#delete_protection GoogleStorageBatchOperationsJob#delete_protection}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#id GoogleStorageBatchOperationsJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param job_id: The ID of the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#job_id GoogleStorageBatchOperationsJob#job_id}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#project GoogleStorageBatchOperationsJob#project}.
        :param put_metadata: put_metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#put_metadata GoogleStorageBatchOperationsJob#put_metadata}
        :param put_object_hold: put_object_hold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#put_object_hold GoogleStorageBatchOperationsJob#put_object_hold}
        :param rewrite_object: rewrite_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#rewrite_object GoogleStorageBatchOperationsJob#rewrite_object}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#timeouts GoogleStorageBatchOperationsJob#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(bucket_list, dict):
            bucket_list = GoogleStorageBatchOperationsJobBucketListStruct(**bucket_list)
        if isinstance(delete_object, dict):
            delete_object = GoogleStorageBatchOperationsJobDeleteObject(**delete_object)
        if isinstance(put_metadata, dict):
            put_metadata = GoogleStorageBatchOperationsJobPutMetadata(**put_metadata)
        if isinstance(put_object_hold, dict):
            put_object_hold = GoogleStorageBatchOperationsJobPutObjectHold(**put_object_hold)
        if isinstance(rewrite_object, dict):
            rewrite_object = GoogleStorageBatchOperationsJobRewriteObject(**rewrite_object)
        if isinstance(timeouts, dict):
            timeouts = GoogleStorageBatchOperationsJobTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f3d5d20391d3032982e0bb6df93b9868c9498aab4e6d2c1448a45c15db01d64)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument bucket_list", value=bucket_list, expected_type=type_hints["bucket_list"])
            check_type(argname="argument delete_object", value=delete_object, expected_type=type_hints["delete_object"])
            check_type(argname="argument delete_protection", value=delete_protection, expected_type=type_hints["delete_protection"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument job_id", value=job_id, expected_type=type_hints["job_id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument put_metadata", value=put_metadata, expected_type=type_hints["put_metadata"])
            check_type(argname="argument put_object_hold", value=put_object_hold, expected_type=type_hints["put_object_hold"])
            check_type(argname="argument rewrite_object", value=rewrite_object, expected_type=type_hints["rewrite_object"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if bucket_list is not None:
            self._values["bucket_list"] = bucket_list
        if delete_object is not None:
            self._values["delete_object"] = delete_object
        if delete_protection is not None:
            self._values["delete_protection"] = delete_protection
        if id is not None:
            self._values["id"] = id
        if job_id is not None:
            self._values["job_id"] = job_id
        if project is not None:
            self._values["project"] = project
        if put_metadata is not None:
            self._values["put_metadata"] = put_metadata
        if put_object_hold is not None:
            self._values["put_object_hold"] = put_object_hold
        if rewrite_object is not None:
            self._values["rewrite_object"] = rewrite_object
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
    def bucket_list(
        self,
    ) -> typing.Optional[GoogleStorageBatchOperationsJobBucketListStruct]:
        '''bucket_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#bucket_list GoogleStorageBatchOperationsJob#bucket_list}
        '''
        result = self._values.get("bucket_list")
        return typing.cast(typing.Optional[GoogleStorageBatchOperationsJobBucketListStruct], result)

    @builtins.property
    def delete_object(
        self,
    ) -> typing.Optional["GoogleStorageBatchOperationsJobDeleteObject"]:
        '''delete_object block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#delete_object GoogleStorageBatchOperationsJob#delete_object}
        '''
        result = self._values.get("delete_object")
        return typing.cast(typing.Optional["GoogleStorageBatchOperationsJobDeleteObject"], result)

    @builtins.property
    def delete_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to 'true', the storage batch operation job will not be deleted and new job will be created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#delete_protection GoogleStorageBatchOperationsJob#delete_protection}
        '''
        result = self._values.get("delete_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#id GoogleStorageBatchOperationsJob#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#job_id GoogleStorageBatchOperationsJob#job_id}
        '''
        result = self._values.get("job_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#project GoogleStorageBatchOperationsJob#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def put_metadata(
        self,
    ) -> typing.Optional["GoogleStorageBatchOperationsJobPutMetadata"]:
        '''put_metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#put_metadata GoogleStorageBatchOperationsJob#put_metadata}
        '''
        result = self._values.get("put_metadata")
        return typing.cast(typing.Optional["GoogleStorageBatchOperationsJobPutMetadata"], result)

    @builtins.property
    def put_object_hold(
        self,
    ) -> typing.Optional["GoogleStorageBatchOperationsJobPutObjectHold"]:
        '''put_object_hold block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#put_object_hold GoogleStorageBatchOperationsJob#put_object_hold}
        '''
        result = self._values.get("put_object_hold")
        return typing.cast(typing.Optional["GoogleStorageBatchOperationsJobPutObjectHold"], result)

    @builtins.property
    def rewrite_object(
        self,
    ) -> typing.Optional["GoogleStorageBatchOperationsJobRewriteObject"]:
        '''rewrite_object block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#rewrite_object GoogleStorageBatchOperationsJob#rewrite_object}
        '''
        result = self._values.get("rewrite_object")
        return typing.cast(typing.Optional["GoogleStorageBatchOperationsJobRewriteObject"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleStorageBatchOperationsJobTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#timeouts GoogleStorageBatchOperationsJob#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleStorageBatchOperationsJobTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBatchOperationsJobConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBatchOperationsJob.GoogleStorageBatchOperationsJobDeleteObject",
    jsii_struct_bases=[],
    name_mapping={
        "permanent_object_deletion_enabled": "permanentObjectDeletionEnabled",
    },
)
class GoogleStorageBatchOperationsJobDeleteObject:
    def __init__(
        self,
        *,
        permanent_object_deletion_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param permanent_object_deletion_enabled: enable flag to permanently delete object and all object versions if versioning is enabled on bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#permanent_object_deletion_enabled GoogleStorageBatchOperationsJob#permanent_object_deletion_enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13af6fdc5d60385c28263c629ae61b358d892ea7cf4969ee70529da4fa05cedd)
            check_type(argname="argument permanent_object_deletion_enabled", value=permanent_object_deletion_enabled, expected_type=type_hints["permanent_object_deletion_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "permanent_object_deletion_enabled": permanent_object_deletion_enabled,
        }

    @builtins.property
    def permanent_object_deletion_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''enable flag to permanently delete object and all object versions if versioning is enabled on bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#permanent_object_deletion_enabled GoogleStorageBatchOperationsJob#permanent_object_deletion_enabled}
        '''
        result = self._values.get("permanent_object_deletion_enabled")
        assert result is not None, "Required property 'permanent_object_deletion_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBatchOperationsJobDeleteObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBatchOperationsJobDeleteObjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBatchOperationsJob.GoogleStorageBatchOperationsJobDeleteObjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35bfa0152ef69801456b8a4d8e3e2a585648fa11d6dfc695c5f9723e65ed0bd3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="permanentObjectDeletionEnabledInput")
    def permanent_object_deletion_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "permanentObjectDeletionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="permanentObjectDeletionEnabled")
    def permanent_object_deletion_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "permanentObjectDeletionEnabled"))

    @permanent_object_deletion_enabled.setter
    def permanent_object_deletion_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba08c0d32a47628c1466705f0bd4c38bbe32f4a09951de351cd2283d28de1841)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permanentObjectDeletionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageBatchOperationsJobDeleteObject]:
        return typing.cast(typing.Optional[GoogleStorageBatchOperationsJobDeleteObject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageBatchOperationsJobDeleteObject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d81bcf5b09739efdff2b0773dc081a7561d2b89622cf6afe5ff094cbe9d1369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBatchOperationsJob.GoogleStorageBatchOperationsJobPutMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "cache_control": "cacheControl",
        "content_disposition": "contentDisposition",
        "content_encoding": "contentEncoding",
        "content_language": "contentLanguage",
        "content_type": "contentType",
        "custom_metadata": "customMetadata",
        "custom_time": "customTime",
    },
)
class GoogleStorageBatchOperationsJobPutMetadata:
    def __init__(
        self,
        *,
        cache_control: typing.Optional[builtins.str] = None,
        content_disposition: typing.Optional[builtins.str] = None,
        content_encoding: typing.Optional[builtins.str] = None,
        content_language: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
        custom_metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        custom_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cache_control: Cache-Control directive to specify caching behavior of object data. If omitted and object is accessible to all anonymous users, the default will be public, max-age=3600 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#cache_control GoogleStorageBatchOperationsJob#cache_control}
        :param content_disposition: Content-Disposition of the object data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#content_disposition GoogleStorageBatchOperationsJob#content_disposition}
        :param content_encoding: Content Encoding of the object data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#content_encoding GoogleStorageBatchOperationsJob#content_encoding}
        :param content_language: Content-Language of the object data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#content_language GoogleStorageBatchOperationsJob#content_language}
        :param content_type: Content-Type of the object data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#content_type GoogleStorageBatchOperationsJob#content_type}
        :param custom_metadata: User-provided metadata, in key/value pairs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#custom_metadata GoogleStorageBatchOperationsJob#custom_metadata}
        :param custom_time: Updates the objects fixed custom time metadata. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#custom_time GoogleStorageBatchOperationsJob#custom_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0dc88480b09a0d7cd9bab9c5172fe32a81683cd58f5c0c6899e8d6754410353)
            check_type(argname="argument cache_control", value=cache_control, expected_type=type_hints["cache_control"])
            check_type(argname="argument content_disposition", value=content_disposition, expected_type=type_hints["content_disposition"])
            check_type(argname="argument content_encoding", value=content_encoding, expected_type=type_hints["content_encoding"])
            check_type(argname="argument content_language", value=content_language, expected_type=type_hints["content_language"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument custom_metadata", value=custom_metadata, expected_type=type_hints["custom_metadata"])
            check_type(argname="argument custom_time", value=custom_time, expected_type=type_hints["custom_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cache_control is not None:
            self._values["cache_control"] = cache_control
        if content_disposition is not None:
            self._values["content_disposition"] = content_disposition
        if content_encoding is not None:
            self._values["content_encoding"] = content_encoding
        if content_language is not None:
            self._values["content_language"] = content_language
        if content_type is not None:
            self._values["content_type"] = content_type
        if custom_metadata is not None:
            self._values["custom_metadata"] = custom_metadata
        if custom_time is not None:
            self._values["custom_time"] = custom_time

    @builtins.property
    def cache_control(self) -> typing.Optional[builtins.str]:
        '''Cache-Control directive to specify caching behavior of object data.

        If omitted and object is accessible to all anonymous users, the default will be public, max-age=3600

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#cache_control GoogleStorageBatchOperationsJob#cache_control}
        '''
        result = self._values.get("cache_control")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_disposition(self) -> typing.Optional[builtins.str]:
        '''Content-Disposition of the object data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#content_disposition GoogleStorageBatchOperationsJob#content_disposition}
        '''
        result = self._values.get("content_disposition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_encoding(self) -> typing.Optional[builtins.str]:
        '''Content Encoding of the object data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#content_encoding GoogleStorageBatchOperationsJob#content_encoding}
        '''
        result = self._values.get("content_encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_language(self) -> typing.Optional[builtins.str]:
        '''Content-Language of the object data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#content_language GoogleStorageBatchOperationsJob#content_language}
        '''
        result = self._values.get("content_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''Content-Type of the object data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#content_type GoogleStorageBatchOperationsJob#content_type}
        '''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_metadata(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-provided metadata, in key/value pairs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#custom_metadata GoogleStorageBatchOperationsJob#custom_metadata}
        '''
        result = self._values.get("custom_metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def custom_time(self) -> typing.Optional[builtins.str]:
        '''Updates the objects fixed custom time metadata.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#custom_time GoogleStorageBatchOperationsJob#custom_time}
        '''
        result = self._values.get("custom_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBatchOperationsJobPutMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBatchOperationsJobPutMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBatchOperationsJob.GoogleStorageBatchOperationsJobPutMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b69b48a28b0f33200f37337de6b7e08eb7348f2511982d7785411f65410892df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCacheControl")
    def reset_cache_control(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheControl", []))

    @jsii.member(jsii_name="resetContentDisposition")
    def reset_content_disposition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentDisposition", []))

    @jsii.member(jsii_name="resetContentEncoding")
    def reset_content_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentEncoding", []))

    @jsii.member(jsii_name="resetContentLanguage")
    def reset_content_language(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentLanguage", []))

    @jsii.member(jsii_name="resetContentType")
    def reset_content_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentType", []))

    @jsii.member(jsii_name="resetCustomMetadata")
    def reset_custom_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomMetadata", []))

    @jsii.member(jsii_name="resetCustomTime")
    def reset_custom_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomTime", []))

    @builtins.property
    @jsii.member(jsii_name="cacheControlInput")
    def cache_control_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheControlInput"))

    @builtins.property
    @jsii.member(jsii_name="contentDispositionInput")
    def content_disposition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentDispositionInput"))

    @builtins.property
    @jsii.member(jsii_name="contentEncodingInput")
    def content_encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentEncodingInput"))

    @builtins.property
    @jsii.member(jsii_name="contentLanguageInput")
    def content_language_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentLanguageInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="customMetadataInput")
    def custom_metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "customMetadataInput"))

    @builtins.property
    @jsii.member(jsii_name="customTimeInput")
    def custom_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheControl")
    def cache_control(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacheControl"))

    @cache_control.setter
    def cache_control(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49cc4f187483f7131ed06ab7310b3128339498a576ce4873d60e42c8aebd9d32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheControl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentDisposition")
    def content_disposition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentDisposition"))

    @content_disposition.setter
    def content_disposition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a5a6ca24c5ac3a7c6aa35e7bbcdfe2d1860f463ae8d33c10b153268dd411402)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentDisposition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentEncoding")
    def content_encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentEncoding"))

    @content_encoding.setter
    def content_encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc0cdc32586d65ec348df1092dee423207d8bb2a7ee7c989815cb153d189ad48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentEncoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentLanguage")
    def content_language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentLanguage"))

    @content_language.setter
    def content_language(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9a5a1b2e7369daa728815fd2513d05b6473ebbf7a53ad494cad42ff6fd6ea87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentLanguage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__697cddbd76b03b293304a0e89e124a1e71403a3efad8a0755810bc0043a62246)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customMetadata")
    def custom_metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "customMetadata"))

    @custom_metadata.setter
    def custom_metadata(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3faad9d712c84f35d01ce9fa4d6ebb878e03bb01835b368c71f264c57389093)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customMetadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customTime")
    def custom_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customTime"))

    @custom_time.setter
    def custom_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72dd07c9f3c98907a1ad42f49d6847e81278f783d40eb5064fc1869098483e92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageBatchOperationsJobPutMetadata]:
        return typing.cast(typing.Optional[GoogleStorageBatchOperationsJobPutMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageBatchOperationsJobPutMetadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c8ea569f043086e546edd85a2690da48e9f8d405b5711421ba519c7e0e27129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBatchOperationsJob.GoogleStorageBatchOperationsJobPutObjectHold",
    jsii_struct_bases=[],
    name_mapping={
        "event_based_hold": "eventBasedHold",
        "temporary_hold": "temporaryHold",
    },
)
class GoogleStorageBatchOperationsJobPutObjectHold:
    def __init__(
        self,
        *,
        event_based_hold: typing.Optional[builtins.str] = None,
        temporary_hold: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param event_based_hold: set/unset to update event based hold for objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#event_based_hold GoogleStorageBatchOperationsJob#event_based_hold}
        :param temporary_hold: set/unset to update temporary based hold for objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#temporary_hold GoogleStorageBatchOperationsJob#temporary_hold}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5603291c35e37009870c17080226ede17141123dfef0c804cb806ff15b9f5bb)
            check_type(argname="argument event_based_hold", value=event_based_hold, expected_type=type_hints["event_based_hold"])
            check_type(argname="argument temporary_hold", value=temporary_hold, expected_type=type_hints["temporary_hold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if event_based_hold is not None:
            self._values["event_based_hold"] = event_based_hold
        if temporary_hold is not None:
            self._values["temporary_hold"] = temporary_hold

    @builtins.property
    def event_based_hold(self) -> typing.Optional[builtins.str]:
        '''set/unset to update event based hold for objects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#event_based_hold GoogleStorageBatchOperationsJob#event_based_hold}
        '''
        result = self._values.get("event_based_hold")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def temporary_hold(self) -> typing.Optional[builtins.str]:
        '''set/unset to update temporary based hold for objects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#temporary_hold GoogleStorageBatchOperationsJob#temporary_hold}
        '''
        result = self._values.get("temporary_hold")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBatchOperationsJobPutObjectHold(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBatchOperationsJobPutObjectHoldOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBatchOperationsJob.GoogleStorageBatchOperationsJobPutObjectHoldOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17a60fb9730bd51ea0dd2be3b0f5f85f7b6789d1193b36698fd9fd4a92431036)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEventBasedHold")
    def reset_event_based_hold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventBasedHold", []))

    @jsii.member(jsii_name="resetTemporaryHold")
    def reset_temporary_hold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemporaryHold", []))

    @builtins.property
    @jsii.member(jsii_name="eventBasedHoldInput")
    def event_based_hold_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventBasedHoldInput"))

    @builtins.property
    @jsii.member(jsii_name="temporaryHoldInput")
    def temporary_hold_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "temporaryHoldInput"))

    @builtins.property
    @jsii.member(jsii_name="eventBasedHold")
    def event_based_hold(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventBasedHold"))

    @event_based_hold.setter
    def event_based_hold(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d7e4140b94cd74a940cf3dfbedc5c1495dc8bbd3069ef5bf40d3b98e617831f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventBasedHold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="temporaryHold")
    def temporary_hold(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "temporaryHold"))

    @temporary_hold.setter
    def temporary_hold(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29f7d82e34ca42dcd53396aa7ed6339b01573e7b9ccf79b64faba8dcc2f97297)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "temporaryHold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageBatchOperationsJobPutObjectHold]:
        return typing.cast(typing.Optional[GoogleStorageBatchOperationsJobPutObjectHold], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageBatchOperationsJobPutObjectHold],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc8186f72cee2450fbb0df1fed8c84ce81d7789b57a4b41574e78e0d6310c9b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBatchOperationsJob.GoogleStorageBatchOperationsJobRewriteObject",
    jsii_struct_bases=[],
    name_mapping={"kms_key": "kmsKey"},
)
class GoogleStorageBatchOperationsJobRewriteObject:
    def __init__(self, *, kms_key: builtins.str) -> None:
        '''
        :param kms_key: valid kms key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#kms_key GoogleStorageBatchOperationsJob#kms_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__595c10d03e4368ed26f04017d76165642a3c0775e08622d45176494a2bbefd65)
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key": kms_key,
        }

    @builtins.property
    def kms_key(self) -> builtins.str:
        '''valid kms key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#kms_key GoogleStorageBatchOperationsJob#kms_key}
        '''
        result = self._values.get("kms_key")
        assert result is not None, "Required property 'kms_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBatchOperationsJobRewriteObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBatchOperationsJobRewriteObjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBatchOperationsJob.GoogleStorageBatchOperationsJobRewriteObjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed246bd468b47ff2c4060a2b026f873a9a94ef2357a0c351e2e0c6da9ebf7fe2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__464c0b7e5c6c03affe2b0ffec3d49f5c4f3433036d643aa1776c123dc5fbe48c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageBatchOperationsJobRewriteObject]:
        return typing.cast(typing.Optional[GoogleStorageBatchOperationsJobRewriteObject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageBatchOperationsJobRewriteObject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a374db3cdd6c280a68d1be3bce7919f853a7adaafec7cd5ed2097ec93fee3086)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBatchOperationsJob.GoogleStorageBatchOperationsJobTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleStorageBatchOperationsJobTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#create GoogleStorageBatchOperationsJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#delete GoogleStorageBatchOperationsJob#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#update GoogleStorageBatchOperationsJob#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b86115d64afb661f806314433d69bfc68804c874763800253f1e9a4462bec0a2)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#create GoogleStorageBatchOperationsJob#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#delete GoogleStorageBatchOperationsJob#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_batch_operations_job#update GoogleStorageBatchOperationsJob#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBatchOperationsJobTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBatchOperationsJobTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBatchOperationsJob.GoogleStorageBatchOperationsJobTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0862c36b5686e5ec7f313520e7f1050543efa42b3297039355a3f28c386307af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2a10daf892b204cc558f203641e51074233aa76012f295de833d8a49510116d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab400acc8512407b2b87969a8530a9233e0cbb8e2611325383c8966a1f516329)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f9b79096300735a82267b753679f0ebc96c4f0282fb245a3fa9bdbfde5b3e2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageBatchOperationsJobTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageBatchOperationsJobTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageBatchOperationsJobTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4940916926ffa18c2b7dc9de12082d1be856b58973a1d05b6b019ea1b770a805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleStorageBatchOperationsJob",
    "GoogleStorageBatchOperationsJobBucketListBuckets",
    "GoogleStorageBatchOperationsJobBucketListBucketsManifest",
    "GoogleStorageBatchOperationsJobBucketListBucketsManifestOutputReference",
    "GoogleStorageBatchOperationsJobBucketListBucketsOutputReference",
    "GoogleStorageBatchOperationsJobBucketListBucketsPrefixListStruct",
    "GoogleStorageBatchOperationsJobBucketListBucketsPrefixListStructOutputReference",
    "GoogleStorageBatchOperationsJobBucketListStruct",
    "GoogleStorageBatchOperationsJobBucketListStructOutputReference",
    "GoogleStorageBatchOperationsJobConfig",
    "GoogleStorageBatchOperationsJobDeleteObject",
    "GoogleStorageBatchOperationsJobDeleteObjectOutputReference",
    "GoogleStorageBatchOperationsJobPutMetadata",
    "GoogleStorageBatchOperationsJobPutMetadataOutputReference",
    "GoogleStorageBatchOperationsJobPutObjectHold",
    "GoogleStorageBatchOperationsJobPutObjectHoldOutputReference",
    "GoogleStorageBatchOperationsJobRewriteObject",
    "GoogleStorageBatchOperationsJobRewriteObjectOutputReference",
    "GoogleStorageBatchOperationsJobTimeouts",
    "GoogleStorageBatchOperationsJobTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__705b718e96f9e415ab41dbb19ad0ab3d60084937bb35bde493275d0f3cf8a77e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    bucket_list: typing.Optional[typing.Union[GoogleStorageBatchOperationsJobBucketListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
    delete_object: typing.Optional[typing.Union[GoogleStorageBatchOperationsJobDeleteObject, typing.Dict[builtins.str, typing.Any]]] = None,
    delete_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    job_id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    put_metadata: typing.Optional[typing.Union[GoogleStorageBatchOperationsJobPutMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    put_object_hold: typing.Optional[typing.Union[GoogleStorageBatchOperationsJobPutObjectHold, typing.Dict[builtins.str, typing.Any]]] = None,
    rewrite_object: typing.Optional[typing.Union[GoogleStorageBatchOperationsJobRewriteObject, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleStorageBatchOperationsJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__603f215b4b93e83f8eaff21497e340c552674ad52f70770bcff3ccbfdc4ed928(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a9ba97fe93c0f84158ef92fd486b8d3b113672df19a3b89837d48d9c0e26df(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e2fa323eb795bc4d7d2c11d09d9a4f4a6ef07b245e05c8e5b0d2723baa7fdb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a8643f08afa668de7d34b2a3f4f409d436b8bdeabf48d27a1a7c40d1602e7b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3662ac88128d5d694e4ced9a24abc5339ee512ec35a3b209245954fe33f523d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d575e7e0f7f90eaabbbe2d4a1d5e118c0914a21a1f9fa93d5c9f83a8385c295(
    *,
    bucket: builtins.str,
    manifest: typing.Optional[typing.Union[GoogleStorageBatchOperationsJobBucketListBucketsManifest, typing.Dict[builtins.str, typing.Any]]] = None,
    prefix_list: typing.Optional[typing.Union[GoogleStorageBatchOperationsJobBucketListBucketsPrefixListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7963fc59265aefcc8a4490781442b612119050812566ac11962c322964b9ab4(
    *,
    manifest_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe017daf4cd40eaf4e332460cd8fd70771a9c1790fb48d1189be949982a7f177(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0f4587d46aaa6488497d87ac6bfe8f6a45b47d679459ac7d8b443358dd9ff41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d2d79a65f02c6590f2700bae776635d173aa2db0851dd10cbf608c43315e001(
    value: typing.Optional[GoogleStorageBatchOperationsJobBucketListBucketsManifest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__650e3cadcf1f0af53806fc062d97ccc8647935960cdc64ee98fa1ee6590c2c10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a90b71818988d7da12373b596030a087dc7dad7027f733513e7200897f60c78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d24f09f70cc33799b3fd0bdc113efc9cb7665eba46426aa2a5293b476c5c612(
    value: typing.Optional[GoogleStorageBatchOperationsJobBucketListBuckets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e816eb3f25ded2443ff02523c4cd5e2e50ea603881bc4802c1a34c65f39204e(
    *,
    included_object_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff1437ff3878c10a48dfca852758c1e9e4e23f685c1b365c2aed5550e95c80ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9672234acb4e79e416e445a17d82ba2bfc386e1ae57f2dab67ff0ff5b026ba6b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54e1bb2ff2abf08c7aa06982f54cddf35dd8b84961e5a0c8c79c6dfddf39b40b(
    value: typing.Optional[GoogleStorageBatchOperationsJobBucketListBucketsPrefixListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee3bd9ff4541731f7f188b7893eedb7c7e63a9a216aeec4bf6f9adb963e0b710(
    *,
    buckets: typing.Union[GoogleStorageBatchOperationsJobBucketListBuckets, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f2f03e0a84c8c9d2f1b213e6ea4bd5134b88d54254dbb49b0fb80727e97c7bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d449702ae2e062c69bae1b6eb7b16c8e317e5b34385b2e21824fe3ea515f184e(
    value: typing.Optional[GoogleStorageBatchOperationsJobBucketListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f3d5d20391d3032982e0bb6df93b9868c9498aab4e6d2c1448a45c15db01d64(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bucket_list: typing.Optional[typing.Union[GoogleStorageBatchOperationsJobBucketListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
    delete_object: typing.Optional[typing.Union[GoogleStorageBatchOperationsJobDeleteObject, typing.Dict[builtins.str, typing.Any]]] = None,
    delete_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    job_id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    put_metadata: typing.Optional[typing.Union[GoogleStorageBatchOperationsJobPutMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    put_object_hold: typing.Optional[typing.Union[GoogleStorageBatchOperationsJobPutObjectHold, typing.Dict[builtins.str, typing.Any]]] = None,
    rewrite_object: typing.Optional[typing.Union[GoogleStorageBatchOperationsJobRewriteObject, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleStorageBatchOperationsJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13af6fdc5d60385c28263c629ae61b358d892ea7cf4969ee70529da4fa05cedd(
    *,
    permanent_object_deletion_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35bfa0152ef69801456b8a4d8e3e2a585648fa11d6dfc695c5f9723e65ed0bd3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba08c0d32a47628c1466705f0bd4c38bbe32f4a09951de351cd2283d28de1841(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d81bcf5b09739efdff2b0773dc081a7561d2b89622cf6afe5ff094cbe9d1369(
    value: typing.Optional[GoogleStorageBatchOperationsJobDeleteObject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0dc88480b09a0d7cd9bab9c5172fe32a81683cd58f5c0c6899e8d6754410353(
    *,
    cache_control: typing.Optional[builtins.str] = None,
    content_disposition: typing.Optional[builtins.str] = None,
    content_encoding: typing.Optional[builtins.str] = None,
    content_language: typing.Optional[builtins.str] = None,
    content_type: typing.Optional[builtins.str] = None,
    custom_metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    custom_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69b48a28b0f33200f37337de6b7e08eb7348f2511982d7785411f65410892df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49cc4f187483f7131ed06ab7310b3128339498a576ce4873d60e42c8aebd9d32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5a6ca24c5ac3a7c6aa35e7bbcdfe2d1860f463ae8d33c10b153268dd411402(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc0cdc32586d65ec348df1092dee423207d8bb2a7ee7c989815cb153d189ad48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a5a1b2e7369daa728815fd2513d05b6473ebbf7a53ad494cad42ff6fd6ea87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__697cddbd76b03b293304a0e89e124a1e71403a3efad8a0755810bc0043a62246(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3faad9d712c84f35d01ce9fa4d6ebb878e03bb01835b368c71f264c57389093(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72dd07c9f3c98907a1ad42f49d6847e81278f783d40eb5064fc1869098483e92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c8ea569f043086e546edd85a2690da48e9f8d405b5711421ba519c7e0e27129(
    value: typing.Optional[GoogleStorageBatchOperationsJobPutMetadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5603291c35e37009870c17080226ede17141123dfef0c804cb806ff15b9f5bb(
    *,
    event_based_hold: typing.Optional[builtins.str] = None,
    temporary_hold: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a60fb9730bd51ea0dd2be3b0f5f85f7b6789d1193b36698fd9fd4a92431036(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d7e4140b94cd74a940cf3dfbedc5c1495dc8bbd3069ef5bf40d3b98e617831f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f7d82e34ca42dcd53396aa7ed6339b01573e7b9ccf79b64faba8dcc2f97297(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc8186f72cee2450fbb0df1fed8c84ce81d7789b57a4b41574e78e0d6310c9b3(
    value: typing.Optional[GoogleStorageBatchOperationsJobPutObjectHold],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__595c10d03e4368ed26f04017d76165642a3c0775e08622d45176494a2bbefd65(
    *,
    kms_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed246bd468b47ff2c4060a2b026f873a9a94ef2357a0c351e2e0c6da9ebf7fe2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__464c0b7e5c6c03affe2b0ffec3d49f5c4f3433036d643aa1776c123dc5fbe48c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a374db3cdd6c280a68d1be3bce7919f853a7adaafec7cd5ed2097ec93fee3086(
    value: typing.Optional[GoogleStorageBatchOperationsJobRewriteObject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b86115d64afb661f806314433d69bfc68804c874763800253f1e9a4462bec0a2(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0862c36b5686e5ec7f313520e7f1050543efa42b3297039355a3f28c386307af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2a10daf892b204cc558f203641e51074233aa76012f295de833d8a49510116d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab400acc8512407b2b87969a8530a9233e0cbb8e2611325383c8966a1f516329(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9b79096300735a82267b753679f0ebc96c4f0282fb245a3fa9bdbfde5b3e2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4940916926ffa18c2b7dc9de12082d1be856b58973a1d05b6b019ea1b770a805(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageBatchOperationsJobTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
