r'''
# `google_storage_batch_operations_job`

Refer to the Terraform Registry for docs: [`google_storage_batch_operations_job`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job).
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


class StorageBatchOperationsJob(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBatchOperationsJob.StorageBatchOperationsJob",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job google_storage_batch_operations_job}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        bucket_list: typing.Optional[typing.Union["StorageBatchOperationsJobBucketListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
        delete_object: typing.Optional[typing.Union["StorageBatchOperationsJobDeleteObject", typing.Dict[builtins.str, typing.Any]]] = None,
        delete_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        job_id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        put_metadata: typing.Optional[typing.Union["StorageBatchOperationsJobPutMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        put_object_hold: typing.Optional[typing.Union["StorageBatchOperationsJobPutObjectHold", typing.Dict[builtins.str, typing.Any]]] = None,
        rewrite_object: typing.Optional[typing.Union["StorageBatchOperationsJobRewriteObject", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["StorageBatchOperationsJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job google_storage_batch_operations_job} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bucket_list: bucket_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#bucket_list StorageBatchOperationsJob#bucket_list}
        :param delete_object: delete_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#delete_object StorageBatchOperationsJob#delete_object}
        :param delete_protection: If set to 'true', the storage batch operation job will not be deleted and new job will be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#delete_protection StorageBatchOperationsJob#delete_protection}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#id StorageBatchOperationsJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param job_id: The ID of the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#job_id StorageBatchOperationsJob#job_id}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#project StorageBatchOperationsJob#project}.
        :param put_metadata: put_metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#put_metadata StorageBatchOperationsJob#put_metadata}
        :param put_object_hold: put_object_hold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#put_object_hold StorageBatchOperationsJob#put_object_hold}
        :param rewrite_object: rewrite_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#rewrite_object StorageBatchOperationsJob#rewrite_object}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#timeouts StorageBatchOperationsJob#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdab4588ccc346f41ba93fd31f280ddea74fdc0600abc48726d358bd43dd3f2c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = StorageBatchOperationsJobConfig(
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
        '''Generates CDKTF code for importing a StorageBatchOperationsJob resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the StorageBatchOperationsJob to import.
        :param import_from_id: The id of the existing StorageBatchOperationsJob that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the StorageBatchOperationsJob to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8533c5bb9f47312d3d34c389f61da7f5b513001ec6c206316646a3972c995d1b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBucketList")
    def put_bucket_list(
        self,
        *,
        buckets: typing.Union["StorageBatchOperationsJobBucketListBuckets", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param buckets: buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#buckets StorageBatchOperationsJob#buckets}
        '''
        value = StorageBatchOperationsJobBucketListStruct(buckets=buckets)

        return typing.cast(None, jsii.invoke(self, "putBucketList", [value]))

    @jsii.member(jsii_name="putDeleteObject")
    def put_delete_object(
        self,
        *,
        permanent_object_deletion_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param permanent_object_deletion_enabled: enable flag to permanently delete object and all object versions if versioning is enabled on bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#permanent_object_deletion_enabled StorageBatchOperationsJob#permanent_object_deletion_enabled}
        '''
        value = StorageBatchOperationsJobDeleteObject(
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
        :param cache_control: Cache-Control directive to specify caching behavior of object data. If omitted and object is accessible to all anonymous users, the default will be public, max-age=3600 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#cache_control StorageBatchOperationsJob#cache_control}
        :param content_disposition: Content-Disposition of the object data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#content_disposition StorageBatchOperationsJob#content_disposition}
        :param content_encoding: Content Encoding of the object data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#content_encoding StorageBatchOperationsJob#content_encoding}
        :param content_language: Content-Language of the object data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#content_language StorageBatchOperationsJob#content_language}
        :param content_type: Content-Type of the object data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#content_type StorageBatchOperationsJob#content_type}
        :param custom_metadata: User-provided metadata, in key/value pairs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#custom_metadata StorageBatchOperationsJob#custom_metadata}
        :param custom_time: Updates the objects fixed custom time metadata. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#custom_time StorageBatchOperationsJob#custom_time}
        '''
        value = StorageBatchOperationsJobPutMetadata(
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
        :param event_based_hold: set/unset to update event based hold for objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#event_based_hold StorageBatchOperationsJob#event_based_hold}
        :param temporary_hold: set/unset to update temporary based hold for objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#temporary_hold StorageBatchOperationsJob#temporary_hold}
        '''
        value = StorageBatchOperationsJobPutObjectHold(
            event_based_hold=event_based_hold, temporary_hold=temporary_hold
        )

        return typing.cast(None, jsii.invoke(self, "putPutObjectHold", [value]))

    @jsii.member(jsii_name="putRewriteObject")
    def put_rewrite_object(self, *, kms_key: builtins.str) -> None:
        '''
        :param kms_key: valid kms key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#kms_key StorageBatchOperationsJob#kms_key}
        '''
        value = StorageBatchOperationsJobRewriteObject(kms_key=kms_key)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#create StorageBatchOperationsJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#delete StorageBatchOperationsJob#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#update StorageBatchOperationsJob#update}.
        '''
        value = StorageBatchOperationsJobTimeouts(
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
    def bucket_list(self) -> "StorageBatchOperationsJobBucketListStructOutputReference":
        return typing.cast("StorageBatchOperationsJobBucketListStructOutputReference", jsii.get(self, "bucketList"))

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
    def delete_object(self) -> "StorageBatchOperationsJobDeleteObjectOutputReference":
        return typing.cast("StorageBatchOperationsJobDeleteObjectOutputReference", jsii.get(self, "deleteObject"))

    @builtins.property
    @jsii.member(jsii_name="putMetadata")
    def put_metadata(self) -> "StorageBatchOperationsJobPutMetadataOutputReference":
        return typing.cast("StorageBatchOperationsJobPutMetadataOutputReference", jsii.get(self, "putMetadata"))

    @builtins.property
    @jsii.member(jsii_name="putObjectHold")
    def put_object_hold(
        self,
    ) -> "StorageBatchOperationsJobPutObjectHoldOutputReference":
        return typing.cast("StorageBatchOperationsJobPutObjectHoldOutputReference", jsii.get(self, "putObjectHold"))

    @builtins.property
    @jsii.member(jsii_name="rewriteObject")
    def rewrite_object(self) -> "StorageBatchOperationsJobRewriteObjectOutputReference":
        return typing.cast("StorageBatchOperationsJobRewriteObjectOutputReference", jsii.get(self, "rewriteObject"))

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
    def timeouts(self) -> "StorageBatchOperationsJobTimeoutsOutputReference":
        return typing.cast("StorageBatchOperationsJobTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="bucketListInput")
    def bucket_list_input(
        self,
    ) -> typing.Optional["StorageBatchOperationsJobBucketListStruct"]:
        return typing.cast(typing.Optional["StorageBatchOperationsJobBucketListStruct"], jsii.get(self, "bucketListInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteObjectInput")
    def delete_object_input(
        self,
    ) -> typing.Optional["StorageBatchOperationsJobDeleteObject"]:
        return typing.cast(typing.Optional["StorageBatchOperationsJobDeleteObject"], jsii.get(self, "deleteObjectInput"))

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
    ) -> typing.Optional["StorageBatchOperationsJobPutMetadata"]:
        return typing.cast(typing.Optional["StorageBatchOperationsJobPutMetadata"], jsii.get(self, "putMetadataInput"))

    @builtins.property
    @jsii.member(jsii_name="putObjectHoldInput")
    def put_object_hold_input(
        self,
    ) -> typing.Optional["StorageBatchOperationsJobPutObjectHold"]:
        return typing.cast(typing.Optional["StorageBatchOperationsJobPutObjectHold"], jsii.get(self, "putObjectHoldInput"))

    @builtins.property
    @jsii.member(jsii_name="rewriteObjectInput")
    def rewrite_object_input(
        self,
    ) -> typing.Optional["StorageBatchOperationsJobRewriteObject"]:
        return typing.cast(typing.Optional["StorageBatchOperationsJobRewriteObject"], jsii.get(self, "rewriteObjectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StorageBatchOperationsJobTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StorageBatchOperationsJobTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4427d7837cb06c8615f341096bb5294d1a34d34892b460964a9ced55d12f0e02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be75722a302fd939e54cbe2aa83171496dddbb43edea2ef3fe03da914cf30999)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobId")
    def job_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobId"))

    @job_id.setter
    def job_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ef22b8df9a473f85687928963d342cfc18b907a01ead348db202e6a1e9bf3fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42d24945ccf2ae14112991ca6e07e11792c0db4c77af3f71bbcf9817748a8f6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBatchOperationsJob.StorageBatchOperationsJobBucketListBuckets",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "manifest": "manifest",
        "prefix_list": "prefixList",
    },
)
class StorageBatchOperationsJobBucketListBuckets:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        manifest: typing.Optional[typing.Union["StorageBatchOperationsJobBucketListBucketsManifest", typing.Dict[builtins.str, typing.Any]]] = None,
        prefix_list: typing.Optional[typing.Union["StorageBatchOperationsJobBucketListBucketsPrefixListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket: Bucket name for the objects to be transformed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#bucket StorageBatchOperationsJob#bucket}
        :param manifest: manifest block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#manifest StorageBatchOperationsJob#manifest}
        :param prefix_list: prefix_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#prefix_list StorageBatchOperationsJob#prefix_list}
        '''
        if isinstance(manifest, dict):
            manifest = StorageBatchOperationsJobBucketListBucketsManifest(**manifest)
        if isinstance(prefix_list, dict):
            prefix_list = StorageBatchOperationsJobBucketListBucketsPrefixListStruct(**prefix_list)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07b33054826c83308596f4a9610d192e2e66c4efc7a728e8ec701329f45d5323)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#bucket StorageBatchOperationsJob#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def manifest(
        self,
    ) -> typing.Optional["StorageBatchOperationsJobBucketListBucketsManifest"]:
        '''manifest block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#manifest StorageBatchOperationsJob#manifest}
        '''
        result = self._values.get("manifest")
        return typing.cast(typing.Optional["StorageBatchOperationsJobBucketListBucketsManifest"], result)

    @builtins.property
    def prefix_list(
        self,
    ) -> typing.Optional["StorageBatchOperationsJobBucketListBucketsPrefixListStruct"]:
        '''prefix_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#prefix_list StorageBatchOperationsJob#prefix_list}
        '''
        result = self._values.get("prefix_list")
        return typing.cast(typing.Optional["StorageBatchOperationsJobBucketListBucketsPrefixListStruct"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBatchOperationsJobBucketListBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBatchOperationsJob.StorageBatchOperationsJobBucketListBucketsManifest",
    jsii_struct_bases=[],
    name_mapping={"manifest_location": "manifestLocation"},
)
class StorageBatchOperationsJobBucketListBucketsManifest:
    def __init__(
        self,
        *,
        manifest_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param manifest_location: Specifies objects in a manifest file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#manifest_location StorageBatchOperationsJob#manifest_location}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ab9ee2a73f6b5f84828103cf8af2f0f84f39efa1ec8b855bef087dfe5a97f76)
            check_type(argname="argument manifest_location", value=manifest_location, expected_type=type_hints["manifest_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if manifest_location is not None:
            self._values["manifest_location"] = manifest_location

    @builtins.property
    def manifest_location(self) -> typing.Optional[builtins.str]:
        '''Specifies objects in a manifest file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#manifest_location StorageBatchOperationsJob#manifest_location}
        '''
        result = self._values.get("manifest_location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBatchOperationsJobBucketListBucketsManifest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBatchOperationsJobBucketListBucketsManifestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBatchOperationsJob.StorageBatchOperationsJobBucketListBucketsManifestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__affeece0cf53729eeca627ceb27fabcdefbb2d01f1fcf80e75aec82e9a8d6fc9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a64ff610f36745cf978178710f7bcdeda1aa2deba1fada22e67399d03ad56759)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manifestLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageBatchOperationsJobBucketListBucketsManifest]:
        return typing.cast(typing.Optional[StorageBatchOperationsJobBucketListBucketsManifest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageBatchOperationsJobBucketListBucketsManifest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26774f918f7bd8680535138fa8eb0a481c751f4d8e20b6079163f3f13abc289b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageBatchOperationsJobBucketListBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBatchOperationsJob.StorageBatchOperationsJobBucketListBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b004a25824ab6774fa7d66ac29ccf858c19da6a3759fb419a94451effbc4f35)
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
        :param manifest_location: Specifies objects in a manifest file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#manifest_location StorageBatchOperationsJob#manifest_location}
        '''
        value = StorageBatchOperationsJobBucketListBucketsManifest(
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
        :param included_object_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#included_object_prefixes StorageBatchOperationsJob#included_object_prefixes}.
        '''
        value = StorageBatchOperationsJobBucketListBucketsPrefixListStruct(
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
    ) -> StorageBatchOperationsJobBucketListBucketsManifestOutputReference:
        return typing.cast(StorageBatchOperationsJobBucketListBucketsManifestOutputReference, jsii.get(self, "manifest"))

    @builtins.property
    @jsii.member(jsii_name="prefixList")
    def prefix_list(
        self,
    ) -> "StorageBatchOperationsJobBucketListBucketsPrefixListStructOutputReference":
        return typing.cast("StorageBatchOperationsJobBucketListBucketsPrefixListStructOutputReference", jsii.get(self, "prefixList"))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="manifestInput")
    def manifest_input(
        self,
    ) -> typing.Optional[StorageBatchOperationsJobBucketListBucketsManifest]:
        return typing.cast(typing.Optional[StorageBatchOperationsJobBucketListBucketsManifest], jsii.get(self, "manifestInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixListInput")
    def prefix_list_input(
        self,
    ) -> typing.Optional["StorageBatchOperationsJobBucketListBucketsPrefixListStruct"]:
        return typing.cast(typing.Optional["StorageBatchOperationsJobBucketListBucketsPrefixListStruct"], jsii.get(self, "prefixListInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c72614ba06687d93e68728ad8437218e11b77bae9ef0f9631a8bb85c4278e8c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageBatchOperationsJobBucketListBuckets]:
        return typing.cast(typing.Optional[StorageBatchOperationsJobBucketListBuckets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageBatchOperationsJobBucketListBuckets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d91de2142e56cffbc9033b9050612b02873978b37a1e54c5904acf4605ef645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBatchOperationsJob.StorageBatchOperationsJobBucketListBucketsPrefixListStruct",
    jsii_struct_bases=[],
    name_mapping={"included_object_prefixes": "includedObjectPrefixes"},
)
class StorageBatchOperationsJobBucketListBucketsPrefixListStruct:
    def __init__(
        self,
        *,
        included_object_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param included_object_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#included_object_prefixes StorageBatchOperationsJob#included_object_prefixes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10993284b421db083e1f3e66a9eeb9e510c31355caf70cf39a5199d2669b1983)
            check_type(argname="argument included_object_prefixes", value=included_object_prefixes, expected_type=type_hints["included_object_prefixes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if included_object_prefixes is not None:
            self._values["included_object_prefixes"] = included_object_prefixes

    @builtins.property
    def included_object_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#included_object_prefixes StorageBatchOperationsJob#included_object_prefixes}.'''
        result = self._values.get("included_object_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBatchOperationsJobBucketListBucketsPrefixListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBatchOperationsJobBucketListBucketsPrefixListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBatchOperationsJob.StorageBatchOperationsJobBucketListBucketsPrefixListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ac51b1b6fd1b5960db874bf2d3910b7096bb3685132dcf6cf253b8312ecbfa0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a13035ceaf781d20c7cfa2182c7acbbd73d13b30a127a59cd1d349d0c98956f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedObjectPrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageBatchOperationsJobBucketListBucketsPrefixListStruct]:
        return typing.cast(typing.Optional[StorageBatchOperationsJobBucketListBucketsPrefixListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageBatchOperationsJobBucketListBucketsPrefixListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f218ae62adaa810c640574675a2c3dcea1b194888cfc75cea346cfdd00c5fb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBatchOperationsJob.StorageBatchOperationsJobBucketListStruct",
    jsii_struct_bases=[],
    name_mapping={"buckets": "buckets"},
)
class StorageBatchOperationsJobBucketListStruct:
    def __init__(
        self,
        *,
        buckets: typing.Union[StorageBatchOperationsJobBucketListBuckets, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param buckets: buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#buckets StorageBatchOperationsJob#buckets}
        '''
        if isinstance(buckets, dict):
            buckets = StorageBatchOperationsJobBucketListBuckets(**buckets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82cad4be2b0d311551bb6ed08bb44177f407e1b99e3ec971002717534d60bedc)
            check_type(argname="argument buckets", value=buckets, expected_type=type_hints["buckets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "buckets": buckets,
        }

    @builtins.property
    def buckets(self) -> StorageBatchOperationsJobBucketListBuckets:
        '''buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#buckets StorageBatchOperationsJob#buckets}
        '''
        result = self._values.get("buckets")
        assert result is not None, "Required property 'buckets' is missing"
        return typing.cast(StorageBatchOperationsJobBucketListBuckets, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBatchOperationsJobBucketListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBatchOperationsJobBucketListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBatchOperationsJob.StorageBatchOperationsJobBucketListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c8a88305de197a8f25d9efa8a299d5292200cdf321614952fbe1d4740661f9b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBuckets")
    def put_buckets(
        self,
        *,
        bucket: builtins.str,
        manifest: typing.Optional[typing.Union[StorageBatchOperationsJobBucketListBucketsManifest, typing.Dict[builtins.str, typing.Any]]] = None,
        prefix_list: typing.Optional[typing.Union[StorageBatchOperationsJobBucketListBucketsPrefixListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket: Bucket name for the objects to be transformed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#bucket StorageBatchOperationsJob#bucket}
        :param manifest: manifest block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#manifest StorageBatchOperationsJob#manifest}
        :param prefix_list: prefix_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#prefix_list StorageBatchOperationsJob#prefix_list}
        '''
        value = StorageBatchOperationsJobBucketListBuckets(
            bucket=bucket, manifest=manifest, prefix_list=prefix_list
        )

        return typing.cast(None, jsii.invoke(self, "putBuckets", [value]))

    @builtins.property
    @jsii.member(jsii_name="buckets")
    def buckets(self) -> StorageBatchOperationsJobBucketListBucketsOutputReference:
        return typing.cast(StorageBatchOperationsJobBucketListBucketsOutputReference, jsii.get(self, "buckets"))

    @builtins.property
    @jsii.member(jsii_name="bucketsInput")
    def buckets_input(
        self,
    ) -> typing.Optional[StorageBatchOperationsJobBucketListBuckets]:
        return typing.cast(typing.Optional[StorageBatchOperationsJobBucketListBuckets], jsii.get(self, "bucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageBatchOperationsJobBucketListStruct]:
        return typing.cast(typing.Optional[StorageBatchOperationsJobBucketListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageBatchOperationsJobBucketListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b5b47ccd6a446b66816d0a26170ef233daf350a938fb8eea5201d60a9cec8f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBatchOperationsJob.StorageBatchOperationsJobConfig",
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
class StorageBatchOperationsJobConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bucket_list: typing.Optional[typing.Union[StorageBatchOperationsJobBucketListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
        delete_object: typing.Optional[typing.Union["StorageBatchOperationsJobDeleteObject", typing.Dict[builtins.str, typing.Any]]] = None,
        delete_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        job_id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        put_metadata: typing.Optional[typing.Union["StorageBatchOperationsJobPutMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        put_object_hold: typing.Optional[typing.Union["StorageBatchOperationsJobPutObjectHold", typing.Dict[builtins.str, typing.Any]]] = None,
        rewrite_object: typing.Optional[typing.Union["StorageBatchOperationsJobRewriteObject", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["StorageBatchOperationsJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bucket_list: bucket_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#bucket_list StorageBatchOperationsJob#bucket_list}
        :param delete_object: delete_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#delete_object StorageBatchOperationsJob#delete_object}
        :param delete_protection: If set to 'true', the storage batch operation job will not be deleted and new job will be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#delete_protection StorageBatchOperationsJob#delete_protection}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#id StorageBatchOperationsJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param job_id: The ID of the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#job_id StorageBatchOperationsJob#job_id}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#project StorageBatchOperationsJob#project}.
        :param put_metadata: put_metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#put_metadata StorageBatchOperationsJob#put_metadata}
        :param put_object_hold: put_object_hold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#put_object_hold StorageBatchOperationsJob#put_object_hold}
        :param rewrite_object: rewrite_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#rewrite_object StorageBatchOperationsJob#rewrite_object}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#timeouts StorageBatchOperationsJob#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(bucket_list, dict):
            bucket_list = StorageBatchOperationsJobBucketListStruct(**bucket_list)
        if isinstance(delete_object, dict):
            delete_object = StorageBatchOperationsJobDeleteObject(**delete_object)
        if isinstance(put_metadata, dict):
            put_metadata = StorageBatchOperationsJobPutMetadata(**put_metadata)
        if isinstance(put_object_hold, dict):
            put_object_hold = StorageBatchOperationsJobPutObjectHold(**put_object_hold)
        if isinstance(rewrite_object, dict):
            rewrite_object = StorageBatchOperationsJobRewriteObject(**rewrite_object)
        if isinstance(timeouts, dict):
            timeouts = StorageBatchOperationsJobTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__568ae76d3c3657922de592a05fc0e4405b8acc04fd1da9e79be162869324de6f)
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
    def bucket_list(self) -> typing.Optional[StorageBatchOperationsJobBucketListStruct]:
        '''bucket_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#bucket_list StorageBatchOperationsJob#bucket_list}
        '''
        result = self._values.get("bucket_list")
        return typing.cast(typing.Optional[StorageBatchOperationsJobBucketListStruct], result)

    @builtins.property
    def delete_object(self) -> typing.Optional["StorageBatchOperationsJobDeleteObject"]:
        '''delete_object block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#delete_object StorageBatchOperationsJob#delete_object}
        '''
        result = self._values.get("delete_object")
        return typing.cast(typing.Optional["StorageBatchOperationsJobDeleteObject"], result)

    @builtins.property
    def delete_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to 'true', the storage batch operation job will not be deleted and new job will be created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#delete_protection StorageBatchOperationsJob#delete_protection}
        '''
        result = self._values.get("delete_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#id StorageBatchOperationsJob#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#job_id StorageBatchOperationsJob#job_id}
        '''
        result = self._values.get("job_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#project StorageBatchOperationsJob#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def put_metadata(self) -> typing.Optional["StorageBatchOperationsJobPutMetadata"]:
        '''put_metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#put_metadata StorageBatchOperationsJob#put_metadata}
        '''
        result = self._values.get("put_metadata")
        return typing.cast(typing.Optional["StorageBatchOperationsJobPutMetadata"], result)

    @builtins.property
    def put_object_hold(
        self,
    ) -> typing.Optional["StorageBatchOperationsJobPutObjectHold"]:
        '''put_object_hold block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#put_object_hold StorageBatchOperationsJob#put_object_hold}
        '''
        result = self._values.get("put_object_hold")
        return typing.cast(typing.Optional["StorageBatchOperationsJobPutObjectHold"], result)

    @builtins.property
    def rewrite_object(
        self,
    ) -> typing.Optional["StorageBatchOperationsJobRewriteObject"]:
        '''rewrite_object block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#rewrite_object StorageBatchOperationsJob#rewrite_object}
        '''
        result = self._values.get("rewrite_object")
        return typing.cast(typing.Optional["StorageBatchOperationsJobRewriteObject"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["StorageBatchOperationsJobTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#timeouts StorageBatchOperationsJob#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["StorageBatchOperationsJobTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBatchOperationsJobConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBatchOperationsJob.StorageBatchOperationsJobDeleteObject",
    jsii_struct_bases=[],
    name_mapping={
        "permanent_object_deletion_enabled": "permanentObjectDeletionEnabled",
    },
)
class StorageBatchOperationsJobDeleteObject:
    def __init__(
        self,
        *,
        permanent_object_deletion_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param permanent_object_deletion_enabled: enable flag to permanently delete object and all object versions if versioning is enabled on bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#permanent_object_deletion_enabled StorageBatchOperationsJob#permanent_object_deletion_enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c02f82e44a3dbccf60d52d182e19579558f472a7318520ce462fad2c9ca118b1)
            check_type(argname="argument permanent_object_deletion_enabled", value=permanent_object_deletion_enabled, expected_type=type_hints["permanent_object_deletion_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "permanent_object_deletion_enabled": permanent_object_deletion_enabled,
        }

    @builtins.property
    def permanent_object_deletion_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''enable flag to permanently delete object and all object versions if versioning is enabled on bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#permanent_object_deletion_enabled StorageBatchOperationsJob#permanent_object_deletion_enabled}
        '''
        result = self._values.get("permanent_object_deletion_enabled")
        assert result is not None, "Required property 'permanent_object_deletion_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBatchOperationsJobDeleteObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBatchOperationsJobDeleteObjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBatchOperationsJob.StorageBatchOperationsJobDeleteObjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60e061b0e2e2664663cbb0d69588b141500f442c35150fe670a4d332c2cc0742)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2850cbefb54cd154c5758f97fbf8396368f0a40f1589b604a092652ae9dff477)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permanentObjectDeletionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageBatchOperationsJobDeleteObject]:
        return typing.cast(typing.Optional[StorageBatchOperationsJobDeleteObject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageBatchOperationsJobDeleteObject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9ce20cd96b22822efc47c026d8fc4c64366996d6acabfa01a063cbd856c0b41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBatchOperationsJob.StorageBatchOperationsJobPutMetadata",
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
class StorageBatchOperationsJobPutMetadata:
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
        :param cache_control: Cache-Control directive to specify caching behavior of object data. If omitted and object is accessible to all anonymous users, the default will be public, max-age=3600 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#cache_control StorageBatchOperationsJob#cache_control}
        :param content_disposition: Content-Disposition of the object data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#content_disposition StorageBatchOperationsJob#content_disposition}
        :param content_encoding: Content Encoding of the object data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#content_encoding StorageBatchOperationsJob#content_encoding}
        :param content_language: Content-Language of the object data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#content_language StorageBatchOperationsJob#content_language}
        :param content_type: Content-Type of the object data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#content_type StorageBatchOperationsJob#content_type}
        :param custom_metadata: User-provided metadata, in key/value pairs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#custom_metadata StorageBatchOperationsJob#custom_metadata}
        :param custom_time: Updates the objects fixed custom time metadata. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#custom_time StorageBatchOperationsJob#custom_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71baa3b3e14a95b6ab153f34ea4c3a513d1e5e428d46b11a7813a89ca3be08e8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#cache_control StorageBatchOperationsJob#cache_control}
        '''
        result = self._values.get("cache_control")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_disposition(self) -> typing.Optional[builtins.str]:
        '''Content-Disposition of the object data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#content_disposition StorageBatchOperationsJob#content_disposition}
        '''
        result = self._values.get("content_disposition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_encoding(self) -> typing.Optional[builtins.str]:
        '''Content Encoding of the object data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#content_encoding StorageBatchOperationsJob#content_encoding}
        '''
        result = self._values.get("content_encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_language(self) -> typing.Optional[builtins.str]:
        '''Content-Language of the object data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#content_language StorageBatchOperationsJob#content_language}
        '''
        result = self._values.get("content_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''Content-Type of the object data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#content_type StorageBatchOperationsJob#content_type}
        '''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_metadata(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-provided metadata, in key/value pairs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#custom_metadata StorageBatchOperationsJob#custom_metadata}
        '''
        result = self._values.get("custom_metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def custom_time(self) -> typing.Optional[builtins.str]:
        '''Updates the objects fixed custom time metadata.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#custom_time StorageBatchOperationsJob#custom_time}
        '''
        result = self._values.get("custom_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBatchOperationsJobPutMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBatchOperationsJobPutMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBatchOperationsJob.StorageBatchOperationsJobPutMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8e40e2171adbce192e63092d1004487c782df6a2c957fd4f0c28d0976ae9ddb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__079c1f491dd2b11e1838df80c0208e4abecd0643475cea58276ce50b3af6df09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheControl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentDisposition")
    def content_disposition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentDisposition"))

    @content_disposition.setter
    def content_disposition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f7a7858354638a80d18eb49736e29fd72c7ed5b45b8adaf679655c33aa09c62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentDisposition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentEncoding")
    def content_encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentEncoding"))

    @content_encoding.setter
    def content_encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e88ee91941a163f1bd9a547d637ce3ac9272d564536dfc617514a7a257846272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentEncoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentLanguage")
    def content_language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentLanguage"))

    @content_language.setter
    def content_language(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68af0986e16c5cebb75f43dd21e2743f546fa6873bbb62b5f4b8d4dc6eab1e0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentLanguage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5496de69db9a163495c3e42ed8edcfc16b083ab2fe7096383fb00edf15974afb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bb6e9689baac46ab84e3c94c8562bf9027d4a748140c883605a3c72f67ca777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customMetadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customTime")
    def custom_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customTime"))

    @custom_time.setter
    def custom_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de9478a8ed03646201e85170e3754c1170015c04d421726b9767851e2864297a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageBatchOperationsJobPutMetadata]:
        return typing.cast(typing.Optional[StorageBatchOperationsJobPutMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageBatchOperationsJobPutMetadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b88794edff1bccab51b1545f260710f32f2d48121fb3d6057a39ab6c5108928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBatchOperationsJob.StorageBatchOperationsJobPutObjectHold",
    jsii_struct_bases=[],
    name_mapping={
        "event_based_hold": "eventBasedHold",
        "temporary_hold": "temporaryHold",
    },
)
class StorageBatchOperationsJobPutObjectHold:
    def __init__(
        self,
        *,
        event_based_hold: typing.Optional[builtins.str] = None,
        temporary_hold: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param event_based_hold: set/unset to update event based hold for objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#event_based_hold StorageBatchOperationsJob#event_based_hold}
        :param temporary_hold: set/unset to update temporary based hold for objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#temporary_hold StorageBatchOperationsJob#temporary_hold}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__277f6be2847c45fac2e748d1a28e196e48ec77a1abff22278b8bda752cb3574f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#event_based_hold StorageBatchOperationsJob#event_based_hold}
        '''
        result = self._values.get("event_based_hold")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def temporary_hold(self) -> typing.Optional[builtins.str]:
        '''set/unset to update temporary based hold for objects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#temporary_hold StorageBatchOperationsJob#temporary_hold}
        '''
        result = self._values.get("temporary_hold")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBatchOperationsJobPutObjectHold(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBatchOperationsJobPutObjectHoldOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBatchOperationsJob.StorageBatchOperationsJobPutObjectHoldOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a2253092899fc9ec6830dfa0d7435408c8c9faeb0c69fe4563f1e1eeb27d470)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ced42d3c9e61a744a2ac1774dc5ba8e49625b106ceb154718f487956e35fb54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventBasedHold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="temporaryHold")
    def temporary_hold(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "temporaryHold"))

    @temporary_hold.setter
    def temporary_hold(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2bb78588f3bf37f1c51d9b601b48e468388568a3f312b203556f05229301508)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "temporaryHold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageBatchOperationsJobPutObjectHold]:
        return typing.cast(typing.Optional[StorageBatchOperationsJobPutObjectHold], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageBatchOperationsJobPutObjectHold],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf454020b964210ec588266ef1f3075be3304daacae3eecc73fbabcc819793df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBatchOperationsJob.StorageBatchOperationsJobRewriteObject",
    jsii_struct_bases=[],
    name_mapping={"kms_key": "kmsKey"},
)
class StorageBatchOperationsJobRewriteObject:
    def __init__(self, *, kms_key: builtins.str) -> None:
        '''
        :param kms_key: valid kms key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#kms_key StorageBatchOperationsJob#kms_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__720be509064ef6b577ab2a6c645aeb1790d78b72a939649ad1242ccc0e42af4f)
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key": kms_key,
        }

    @builtins.property
    def kms_key(self) -> builtins.str:
        '''valid kms key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#kms_key StorageBatchOperationsJob#kms_key}
        '''
        result = self._values.get("kms_key")
        assert result is not None, "Required property 'kms_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBatchOperationsJobRewriteObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBatchOperationsJobRewriteObjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBatchOperationsJob.StorageBatchOperationsJobRewriteObjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad0b25d59052bf2fbbead097a1c4a9c2e7f2f5f977611169fafbb8d211533226)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c58896beda2c586a7deabe1639be714aaae8a7afaaf3da6f945c056a7c033c34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageBatchOperationsJobRewriteObject]:
        return typing.cast(typing.Optional[StorageBatchOperationsJobRewriteObject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageBatchOperationsJobRewriteObject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22a807d17587a88d4fa731ccb0c5a502db9bde621121a1b6000e6daf58e0535b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBatchOperationsJob.StorageBatchOperationsJobTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class StorageBatchOperationsJobTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#create StorageBatchOperationsJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#delete StorageBatchOperationsJob#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#update StorageBatchOperationsJob#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__788418463ed07a0c09d62ea4088438e676defe88a145fc54f653f17899880c2a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#create StorageBatchOperationsJob#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#delete StorageBatchOperationsJob#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_batch_operations_job#update StorageBatchOperationsJob#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBatchOperationsJobTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBatchOperationsJobTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBatchOperationsJob.StorageBatchOperationsJobTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb7e2aa0d4648f1c303ab1d4c335148020e6d335d135be08f468119120cc275e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__497074ef8fcd826a04e301c88de0a36d24b1718b8132b7e0a7e7488f3731fc44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9205b30ea1518a3a6e562b8ac72e9f63028a88058a4260edf5b656df6b5234d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94ab853b62a30837969212924db62ff0e87afe6d6e33833b790b4b5bd2192ace)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageBatchOperationsJobTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageBatchOperationsJobTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageBatchOperationsJobTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83d28e728222425b10539ad6656996d1f1a16787c67972f7992034e23946b8fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "StorageBatchOperationsJob",
    "StorageBatchOperationsJobBucketListBuckets",
    "StorageBatchOperationsJobBucketListBucketsManifest",
    "StorageBatchOperationsJobBucketListBucketsManifestOutputReference",
    "StorageBatchOperationsJobBucketListBucketsOutputReference",
    "StorageBatchOperationsJobBucketListBucketsPrefixListStruct",
    "StorageBatchOperationsJobBucketListBucketsPrefixListStructOutputReference",
    "StorageBatchOperationsJobBucketListStruct",
    "StorageBatchOperationsJobBucketListStructOutputReference",
    "StorageBatchOperationsJobConfig",
    "StorageBatchOperationsJobDeleteObject",
    "StorageBatchOperationsJobDeleteObjectOutputReference",
    "StorageBatchOperationsJobPutMetadata",
    "StorageBatchOperationsJobPutMetadataOutputReference",
    "StorageBatchOperationsJobPutObjectHold",
    "StorageBatchOperationsJobPutObjectHoldOutputReference",
    "StorageBatchOperationsJobRewriteObject",
    "StorageBatchOperationsJobRewriteObjectOutputReference",
    "StorageBatchOperationsJobTimeouts",
    "StorageBatchOperationsJobTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__cdab4588ccc346f41ba93fd31f280ddea74fdc0600abc48726d358bd43dd3f2c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    bucket_list: typing.Optional[typing.Union[StorageBatchOperationsJobBucketListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
    delete_object: typing.Optional[typing.Union[StorageBatchOperationsJobDeleteObject, typing.Dict[builtins.str, typing.Any]]] = None,
    delete_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    job_id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    put_metadata: typing.Optional[typing.Union[StorageBatchOperationsJobPutMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    put_object_hold: typing.Optional[typing.Union[StorageBatchOperationsJobPutObjectHold, typing.Dict[builtins.str, typing.Any]]] = None,
    rewrite_object: typing.Optional[typing.Union[StorageBatchOperationsJobRewriteObject, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[StorageBatchOperationsJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8533c5bb9f47312d3d34c389f61da7f5b513001ec6c206316646a3972c995d1b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4427d7837cb06c8615f341096bb5294d1a34d34892b460964a9ced55d12f0e02(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be75722a302fd939e54cbe2aa83171496dddbb43edea2ef3fe03da914cf30999(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ef22b8df9a473f85687928963d342cfc18b907a01ead348db202e6a1e9bf3fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42d24945ccf2ae14112991ca6e07e11792c0db4c77af3f71bbcf9817748a8f6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07b33054826c83308596f4a9610d192e2e66c4efc7a728e8ec701329f45d5323(
    *,
    bucket: builtins.str,
    manifest: typing.Optional[typing.Union[StorageBatchOperationsJobBucketListBucketsManifest, typing.Dict[builtins.str, typing.Any]]] = None,
    prefix_list: typing.Optional[typing.Union[StorageBatchOperationsJobBucketListBucketsPrefixListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ab9ee2a73f6b5f84828103cf8af2f0f84f39efa1ec8b855bef087dfe5a97f76(
    *,
    manifest_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__affeece0cf53729eeca627ceb27fabcdefbb2d01f1fcf80e75aec82e9a8d6fc9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a64ff610f36745cf978178710f7bcdeda1aa2deba1fada22e67399d03ad56759(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26774f918f7bd8680535138fa8eb0a481c751f4d8e20b6079163f3f13abc289b(
    value: typing.Optional[StorageBatchOperationsJobBucketListBucketsManifest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b004a25824ab6774fa7d66ac29ccf858c19da6a3759fb419a94451effbc4f35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c72614ba06687d93e68728ad8437218e11b77bae9ef0f9631a8bb85c4278e8c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d91de2142e56cffbc9033b9050612b02873978b37a1e54c5904acf4605ef645(
    value: typing.Optional[StorageBatchOperationsJobBucketListBuckets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10993284b421db083e1f3e66a9eeb9e510c31355caf70cf39a5199d2669b1983(
    *,
    included_object_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac51b1b6fd1b5960db874bf2d3910b7096bb3685132dcf6cf253b8312ecbfa0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a13035ceaf781d20c7cfa2182c7acbbd73d13b30a127a59cd1d349d0c98956f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f218ae62adaa810c640574675a2c3dcea1b194888cfc75cea346cfdd00c5fb4(
    value: typing.Optional[StorageBatchOperationsJobBucketListBucketsPrefixListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82cad4be2b0d311551bb6ed08bb44177f407e1b99e3ec971002717534d60bedc(
    *,
    buckets: typing.Union[StorageBatchOperationsJobBucketListBuckets, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c8a88305de197a8f25d9efa8a299d5292200cdf321614952fbe1d4740661f9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b5b47ccd6a446b66816d0a26170ef233daf350a938fb8eea5201d60a9cec8f5(
    value: typing.Optional[StorageBatchOperationsJobBucketListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__568ae76d3c3657922de592a05fc0e4405b8acc04fd1da9e79be162869324de6f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bucket_list: typing.Optional[typing.Union[StorageBatchOperationsJobBucketListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
    delete_object: typing.Optional[typing.Union[StorageBatchOperationsJobDeleteObject, typing.Dict[builtins.str, typing.Any]]] = None,
    delete_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    job_id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    put_metadata: typing.Optional[typing.Union[StorageBatchOperationsJobPutMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    put_object_hold: typing.Optional[typing.Union[StorageBatchOperationsJobPutObjectHold, typing.Dict[builtins.str, typing.Any]]] = None,
    rewrite_object: typing.Optional[typing.Union[StorageBatchOperationsJobRewriteObject, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[StorageBatchOperationsJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c02f82e44a3dbccf60d52d182e19579558f472a7318520ce462fad2c9ca118b1(
    *,
    permanent_object_deletion_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e061b0e2e2664663cbb0d69588b141500f442c35150fe670a4d332c2cc0742(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2850cbefb54cd154c5758f97fbf8396368f0a40f1589b604a092652ae9dff477(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9ce20cd96b22822efc47c026d8fc4c64366996d6acabfa01a063cbd856c0b41(
    value: typing.Optional[StorageBatchOperationsJobDeleteObject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71baa3b3e14a95b6ab153f34ea4c3a513d1e5e428d46b11a7813a89ca3be08e8(
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

def _typecheckingstub__e8e40e2171adbce192e63092d1004487c782df6a2c957fd4f0c28d0976ae9ddb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__079c1f491dd2b11e1838df80c0208e4abecd0643475cea58276ce50b3af6df09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f7a7858354638a80d18eb49736e29fd72c7ed5b45b8adaf679655c33aa09c62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e88ee91941a163f1bd9a547d637ce3ac9272d564536dfc617514a7a257846272(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68af0986e16c5cebb75f43dd21e2743f546fa6873bbb62b5f4b8d4dc6eab1e0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5496de69db9a163495c3e42ed8edcfc16b083ab2fe7096383fb00edf15974afb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bb6e9689baac46ab84e3c94c8562bf9027d4a748140c883605a3c72f67ca777(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de9478a8ed03646201e85170e3754c1170015c04d421726b9767851e2864297a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b88794edff1bccab51b1545f260710f32f2d48121fb3d6057a39ab6c5108928(
    value: typing.Optional[StorageBatchOperationsJobPutMetadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__277f6be2847c45fac2e748d1a28e196e48ec77a1abff22278b8bda752cb3574f(
    *,
    event_based_hold: typing.Optional[builtins.str] = None,
    temporary_hold: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a2253092899fc9ec6830dfa0d7435408c8c9faeb0c69fe4563f1e1eeb27d470(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ced42d3c9e61a744a2ac1774dc5ba8e49625b106ceb154718f487956e35fb54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2bb78588f3bf37f1c51d9b601b48e468388568a3f312b203556f05229301508(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf454020b964210ec588266ef1f3075be3304daacae3eecc73fbabcc819793df(
    value: typing.Optional[StorageBatchOperationsJobPutObjectHold],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__720be509064ef6b577ab2a6c645aeb1790d78b72a939649ad1242ccc0e42af4f(
    *,
    kms_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0b25d59052bf2fbbead097a1c4a9c2e7f2f5f977611169fafbb8d211533226(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58896beda2c586a7deabe1639be714aaae8a7afaaf3da6f945c056a7c033c34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a807d17587a88d4fa731ccb0c5a502db9bde621121a1b6000e6daf58e0535b(
    value: typing.Optional[StorageBatchOperationsJobRewriteObject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__788418463ed07a0c09d62ea4088438e676defe88a145fc54f653f17899880c2a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb7e2aa0d4648f1c303ab1d4c335148020e6d335d135be08f468119120cc275e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__497074ef8fcd826a04e301c88de0a36d24b1718b8132b7e0a7e7488f3731fc44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9205b30ea1518a3a6e562b8ac72e9f63028a88058a4260edf5b656df6b5234d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ab853b62a30837969212924db62ff0e87afe6d6e33833b790b4b5bd2192ace(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d28e728222425b10539ad6656996d1f1a16787c67972f7992034e23946b8fe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageBatchOperationsJobTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
