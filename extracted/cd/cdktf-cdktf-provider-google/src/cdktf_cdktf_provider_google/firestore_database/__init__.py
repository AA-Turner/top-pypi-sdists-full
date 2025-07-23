r'''
# `google_firestore_database`

Refer to the Terraform Registry for docs: [`google_firestore_database`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database).
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


class FirestoreDatabase(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firestoreDatabase.FirestoreDatabase",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database google_firestore_database}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location_id: builtins.str,
        name: builtins.str,
        type: builtins.str,
        app_engine_integration_mode: typing.Optional[builtins.str] = None,
        cmek_config: typing.Optional[typing.Union["FirestoreDatabaseCmekConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        concurrency_mode: typing.Optional[builtins.str] = None,
        database_edition: typing.Optional[builtins.str] = None,
        delete_protection_state: typing.Optional[builtins.str] = None,
        deletion_policy: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        point_in_time_recovery_enablement: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["FirestoreDatabaseTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database google_firestore_database} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location_id: The location of the database. Available locations are listed at https://cloud.google.com/firestore/docs/locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#location_id FirestoreDatabase#location_id}
        :param name: The ID to use for the database, which will become the final component of the database's resource name. This value should be 4-63 characters. Valid characters are /[a-z][0-9]-/ with first character a letter and the last a letter or a number. Must not be UUID-like /[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}/. "(default)" database id is also valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#name FirestoreDatabase#name}
        :param type: The type of the database. See https://cloud.google.com/datastore/docs/firestore-or-datastore for information about how to choose. Possible values: ["FIRESTORE_NATIVE", "DATASTORE_MODE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#type FirestoreDatabase#type}
        :param app_engine_integration_mode: The App Engine integration mode to use for this database. Possible values: ["ENABLED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#app_engine_integration_mode FirestoreDatabase#app_engine_integration_mode}
        :param cmek_config: cmek_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#cmek_config FirestoreDatabase#cmek_config}
        :param concurrency_mode: The concurrency control mode to use for this database. Possible values: ["OPTIMISTIC", "PESSIMISTIC", "OPTIMISTIC_WITH_ENTITY_GROUPS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#concurrency_mode FirestoreDatabase#concurrency_mode}
        :param database_edition: The database edition. Possible values: ["STANDARD", "ENTERPRISE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#database_edition FirestoreDatabase#database_edition}
        :param delete_protection_state: State of delete protection for the database. When delete protection is enabled, this database cannot be deleted. The default value is 'DELETE_PROTECTION_STATE_UNSPECIFIED', which is currently equivalent to 'DELETE_PROTECTION_DISABLED'. **Note:** Additionally, to delete this database using 'terraform destroy', 'deletion_policy' must be set to 'DELETE'. Possible values: ["DELETE_PROTECTION_STATE_UNSPECIFIED", "DELETE_PROTECTION_ENABLED", "DELETE_PROTECTION_DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#delete_protection_state FirestoreDatabase#delete_protection_state}
        :param deletion_policy: Deletion behavior for this database. If the deletion policy is 'ABANDON', the database will be removed from Terraform state but not deleted from Google Cloud upon destruction. If the deletion policy is 'DELETE', the database will both be removed from Terraform state and deleted from Google Cloud upon destruction. The default value is 'ABANDON'. See also 'delete_protection'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#deletion_policy FirestoreDatabase#deletion_policy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#id FirestoreDatabase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param point_in_time_recovery_enablement: Whether to enable the PITR feature on this database. If 'POINT_IN_TIME_RECOVERY_ENABLED' is selected, reads are supported on selected versions of the data from within the past 7 days. versionRetentionPeriod and earliestVersionTime can be used to determine the supported versions. These include reads against any timestamp within the past hour and reads against 1-minute snapshots beyond 1 hour and within 7 days. If 'POINT_IN_TIME_RECOVERY_DISABLED' is selected, reads are supported on any version of the data from within the past 1 hour. Default value: "POINT_IN_TIME_RECOVERY_DISABLED" Possible values: ["POINT_IN_TIME_RECOVERY_ENABLED", "POINT_IN_TIME_RECOVERY_DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#point_in_time_recovery_enablement FirestoreDatabase#point_in_time_recovery_enablement}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#project FirestoreDatabase#project}.
        :param tags: Input only. A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored when empty. The field is immutable and causes resource replacement when mutated. To apply tags to an existing resource, see the 'google_tags_tag_value' resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#tags FirestoreDatabase#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#timeouts FirestoreDatabase#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa57576feaeea9846b25e7ac5c4acdd0360ddbab4347df332e8404a8c9a9acfd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FirestoreDatabaseConfig(
            location_id=location_id,
            name=name,
            type=type,
            app_engine_integration_mode=app_engine_integration_mode,
            cmek_config=cmek_config,
            concurrency_mode=concurrency_mode,
            database_edition=database_edition,
            delete_protection_state=delete_protection_state,
            deletion_policy=deletion_policy,
            id=id,
            point_in_time_recovery_enablement=point_in_time_recovery_enablement,
            project=project,
            tags=tags,
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
        '''Generates CDKTF code for importing a FirestoreDatabase resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the FirestoreDatabase to import.
        :param import_from_id: The id of the existing FirestoreDatabase that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the FirestoreDatabase to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a02dd8ab690db89f9d979b7d507795336307c0746266a87144aab7de55025ee)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCmekConfig")
    def put_cmek_config(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: The resource ID of a Cloud KMS key. If set, the database created will be a Customer-managed Encryption Key (CMEK) database encrypted with this key. This feature is allowlist only in initial launch. Only keys in the same location as this database are allowed to be used for encryption. For Firestore's nam5 multi-region, this corresponds to Cloud KMS multi-region us. For Firestore's eur3 multi-region, this corresponds to Cloud KMS multi-region europe. See https://cloud.google.com/kms/docs/locations. This value should be the KMS key resource ID in the format of 'projects/{project_id}/locations/{kms_location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}'. How to retrieve this resource ID is listed at https://cloud.google.com/kms/docs/getting-resource-ids#getting_the_id_for_a_key_and_version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#kms_key_name FirestoreDatabase#kms_key_name}
        '''
        value = FirestoreDatabaseCmekConfig(kms_key_name=kms_key_name)

        return typing.cast(None, jsii.invoke(self, "putCmekConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#create FirestoreDatabase#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#delete FirestoreDatabase#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#update FirestoreDatabase#update}.
        '''
        value = FirestoreDatabaseTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAppEngineIntegrationMode")
    def reset_app_engine_integration_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppEngineIntegrationMode", []))

    @jsii.member(jsii_name="resetCmekConfig")
    def reset_cmek_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCmekConfig", []))

    @jsii.member(jsii_name="resetConcurrencyMode")
    def reset_concurrency_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConcurrencyMode", []))

    @jsii.member(jsii_name="resetDatabaseEdition")
    def reset_database_edition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseEdition", []))

    @jsii.member(jsii_name="resetDeleteProtectionState")
    def reset_delete_protection_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteProtectionState", []))

    @jsii.member(jsii_name="resetDeletionPolicy")
    def reset_deletion_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionPolicy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPointInTimeRecoveryEnablement")
    def reset_point_in_time_recovery_enablement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPointInTimeRecoveryEnablement", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="cmekConfig")
    def cmek_config(self) -> "FirestoreDatabaseCmekConfigOutputReference":
        return typing.cast("FirestoreDatabaseCmekConfigOutputReference", jsii.get(self, "cmekConfig"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="earliestVersionTime")
    def earliest_version_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "earliestVersionTime"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="keyPrefix")
    def key_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyPrefix"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "FirestoreDatabaseTimeoutsOutputReference":
        return typing.cast("FirestoreDatabaseTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="versionRetentionPeriod")
    def version_retention_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionRetentionPeriod"))

    @builtins.property
    @jsii.member(jsii_name="appEngineIntegrationModeInput")
    def app_engine_integration_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appEngineIntegrationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="cmekConfigInput")
    def cmek_config_input(self) -> typing.Optional["FirestoreDatabaseCmekConfig"]:
        return typing.cast(typing.Optional["FirestoreDatabaseCmekConfig"], jsii.get(self, "cmekConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="concurrencyModeInput")
    def concurrency_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "concurrencyModeInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseEditionInput")
    def database_edition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseEditionInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteProtectionStateInput")
    def delete_protection_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteProtectionStateInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionPolicyInput")
    def deletion_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deletionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationIdInput")
    def location_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pointInTimeRecoveryEnablementInput")
    def point_in_time_recovery_enablement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pointInTimeRecoveryEnablementInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FirestoreDatabaseTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FirestoreDatabaseTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="appEngineIntegrationMode")
    def app_engine_integration_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appEngineIntegrationMode"))

    @app_engine_integration_mode.setter
    def app_engine_integration_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f6b3e056e38e3da8dc6ab1b5b2a30aab9f07d4a3df4a71a1ac743e05c019e9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appEngineIntegrationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="concurrencyMode")
    def concurrency_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "concurrencyMode"))

    @concurrency_mode.setter
    def concurrency_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42972fa1a39a100cb88ea3fd10c7423ff03ba56d9e59f49d573cbb72f4942d1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "concurrencyMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseEdition")
    def database_edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseEdition"))

    @database_edition.setter
    def database_edition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b80c1d9500f5a4b935ca50d5eb1b44ab69dc926b5f533f766ee845c3b5d453e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseEdition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteProtectionState")
    def delete_protection_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteProtectionState"))

    @delete_protection_state.setter
    def delete_protection_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1894cf7b92200cebd3c24f3bcdc59fa5c15f679bf60faed72c3c5d47e5d202f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteProtectionState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionPolicy")
    def deletion_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deletionPolicy"))

    @deletion_policy.setter
    def deletion_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1e9608cb519c39bc315d9ba5fe350e5cedc5731bb4ff00cec582af2ae747fb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c7affc181a0f06155f8560c9552457722e59f073b0e53a3cdf28aeeebeee9f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="locationId")
    def location_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locationId"))

    @location_id.setter
    def location_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__645ab942e90f5d956093cf5c1ad13df71d17f8e07adaea7a810834fa0e924ac4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69c90b7e2a80cc7e0dda24c106821fbefae2f4f016d68fdde0d19ba0748a0c32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pointInTimeRecoveryEnablement")
    def point_in_time_recovery_enablement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pointInTimeRecoveryEnablement"))

    @point_in_time_recovery_enablement.setter
    def point_in_time_recovery_enablement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15e036a622234b9bf5a97bd67b258c3a3a3aea18b32c54b2619854b6042d97fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pointInTimeRecoveryEnablement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3dcd185b5b4419d7c590d36eb6a36b2d74778a8f756b1b25436d5da84c97905)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fdd366c43bdb37dd4d99f14e75683658460003affbf23ec48f0b3718c25cef3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b3f1d416c9861fc24f179a34a9da52f2fa0dd054b589517647139bf1387052e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firestoreDatabase.FirestoreDatabaseCmekConfig",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class FirestoreDatabaseCmekConfig:
    def __init__(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: The resource ID of a Cloud KMS key. If set, the database created will be a Customer-managed Encryption Key (CMEK) database encrypted with this key. This feature is allowlist only in initial launch. Only keys in the same location as this database are allowed to be used for encryption. For Firestore's nam5 multi-region, this corresponds to Cloud KMS multi-region us. For Firestore's eur3 multi-region, this corresponds to Cloud KMS multi-region europe. See https://cloud.google.com/kms/docs/locations. This value should be the KMS key resource ID in the format of 'projects/{project_id}/locations/{kms_location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}'. How to retrieve this resource ID is listed at https://cloud.google.com/kms/docs/getting-resource-ids#getting_the_id_for_a_key_and_version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#kms_key_name FirestoreDatabase#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c11ba4d6fbedfaf4a105e4a610fb20783a1283e4d3098d09f9ca35de40e0d2c)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_name": kms_key_name,
        }

    @builtins.property
    def kms_key_name(self) -> builtins.str:
        '''The resource ID of a Cloud KMS key.

        If set, the database created will
        be a Customer-managed Encryption Key (CMEK) database encrypted with
        this key. This feature is allowlist only in initial launch.

        Only keys in the same location as this database are allowed to be used
        for encryption. For Firestore's nam5 multi-region, this corresponds to Cloud KMS
        multi-region us. For Firestore's eur3 multi-region, this corresponds to
        Cloud KMS multi-region europe. See https://cloud.google.com/kms/docs/locations.

        This value should be the KMS key resource ID in the format of
        'projects/{project_id}/locations/{kms_location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}'.
        How to retrieve this resource ID is listed at
        https://cloud.google.com/kms/docs/getting-resource-ids#getting_the_id_for_a_key_and_version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#kms_key_name FirestoreDatabase#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        assert result is not None, "Required property 'kms_key_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirestoreDatabaseCmekConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirestoreDatabaseCmekConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firestoreDatabase.FirestoreDatabaseCmekConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__997bd3ec9dab590396e4c8f5f5ef68b565bfef66cc222567e735d2a09107e780)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="activeKeyVersion")
    def active_key_version(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "activeKeyVersion"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad83f3abb1f70dc532a1a94b8498c967bce147522e0616f6df6749f871417601)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FirestoreDatabaseCmekConfig]:
        return typing.cast(typing.Optional[FirestoreDatabaseCmekConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FirestoreDatabaseCmekConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ea8116de200a110eb9aa62778687bed91f50e77344b107b3e1194c8728758bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firestoreDatabase.FirestoreDatabaseConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location_id": "locationId",
        "name": "name",
        "type": "type",
        "app_engine_integration_mode": "appEngineIntegrationMode",
        "cmek_config": "cmekConfig",
        "concurrency_mode": "concurrencyMode",
        "database_edition": "databaseEdition",
        "delete_protection_state": "deleteProtectionState",
        "deletion_policy": "deletionPolicy",
        "id": "id",
        "point_in_time_recovery_enablement": "pointInTimeRecoveryEnablement",
        "project": "project",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class FirestoreDatabaseConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location_id: builtins.str,
        name: builtins.str,
        type: builtins.str,
        app_engine_integration_mode: typing.Optional[builtins.str] = None,
        cmek_config: typing.Optional[typing.Union[FirestoreDatabaseCmekConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        concurrency_mode: typing.Optional[builtins.str] = None,
        database_edition: typing.Optional[builtins.str] = None,
        delete_protection_state: typing.Optional[builtins.str] = None,
        deletion_policy: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        point_in_time_recovery_enablement: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["FirestoreDatabaseTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location_id: The location of the database. Available locations are listed at https://cloud.google.com/firestore/docs/locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#location_id FirestoreDatabase#location_id}
        :param name: The ID to use for the database, which will become the final component of the database's resource name. This value should be 4-63 characters. Valid characters are /[a-z][0-9]-/ with first character a letter and the last a letter or a number. Must not be UUID-like /[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}/. "(default)" database id is also valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#name FirestoreDatabase#name}
        :param type: The type of the database. See https://cloud.google.com/datastore/docs/firestore-or-datastore for information about how to choose. Possible values: ["FIRESTORE_NATIVE", "DATASTORE_MODE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#type FirestoreDatabase#type}
        :param app_engine_integration_mode: The App Engine integration mode to use for this database. Possible values: ["ENABLED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#app_engine_integration_mode FirestoreDatabase#app_engine_integration_mode}
        :param cmek_config: cmek_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#cmek_config FirestoreDatabase#cmek_config}
        :param concurrency_mode: The concurrency control mode to use for this database. Possible values: ["OPTIMISTIC", "PESSIMISTIC", "OPTIMISTIC_WITH_ENTITY_GROUPS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#concurrency_mode FirestoreDatabase#concurrency_mode}
        :param database_edition: The database edition. Possible values: ["STANDARD", "ENTERPRISE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#database_edition FirestoreDatabase#database_edition}
        :param delete_protection_state: State of delete protection for the database. When delete protection is enabled, this database cannot be deleted. The default value is 'DELETE_PROTECTION_STATE_UNSPECIFIED', which is currently equivalent to 'DELETE_PROTECTION_DISABLED'. **Note:** Additionally, to delete this database using 'terraform destroy', 'deletion_policy' must be set to 'DELETE'. Possible values: ["DELETE_PROTECTION_STATE_UNSPECIFIED", "DELETE_PROTECTION_ENABLED", "DELETE_PROTECTION_DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#delete_protection_state FirestoreDatabase#delete_protection_state}
        :param deletion_policy: Deletion behavior for this database. If the deletion policy is 'ABANDON', the database will be removed from Terraform state but not deleted from Google Cloud upon destruction. If the deletion policy is 'DELETE', the database will both be removed from Terraform state and deleted from Google Cloud upon destruction. The default value is 'ABANDON'. See also 'delete_protection'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#deletion_policy FirestoreDatabase#deletion_policy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#id FirestoreDatabase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param point_in_time_recovery_enablement: Whether to enable the PITR feature on this database. If 'POINT_IN_TIME_RECOVERY_ENABLED' is selected, reads are supported on selected versions of the data from within the past 7 days. versionRetentionPeriod and earliestVersionTime can be used to determine the supported versions. These include reads against any timestamp within the past hour and reads against 1-minute snapshots beyond 1 hour and within 7 days. If 'POINT_IN_TIME_RECOVERY_DISABLED' is selected, reads are supported on any version of the data from within the past 1 hour. Default value: "POINT_IN_TIME_RECOVERY_DISABLED" Possible values: ["POINT_IN_TIME_RECOVERY_ENABLED", "POINT_IN_TIME_RECOVERY_DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#point_in_time_recovery_enablement FirestoreDatabase#point_in_time_recovery_enablement}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#project FirestoreDatabase#project}.
        :param tags: Input only. A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored when empty. The field is immutable and causes resource replacement when mutated. To apply tags to an existing resource, see the 'google_tags_tag_value' resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#tags FirestoreDatabase#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#timeouts FirestoreDatabase#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cmek_config, dict):
            cmek_config = FirestoreDatabaseCmekConfig(**cmek_config)
        if isinstance(timeouts, dict):
            timeouts = FirestoreDatabaseTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5153dd49f9a02a9777e07e581cfbafe3b2752604fb1c84b9483c03c2a6e38624)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location_id", value=location_id, expected_type=type_hints["location_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument app_engine_integration_mode", value=app_engine_integration_mode, expected_type=type_hints["app_engine_integration_mode"])
            check_type(argname="argument cmek_config", value=cmek_config, expected_type=type_hints["cmek_config"])
            check_type(argname="argument concurrency_mode", value=concurrency_mode, expected_type=type_hints["concurrency_mode"])
            check_type(argname="argument database_edition", value=database_edition, expected_type=type_hints["database_edition"])
            check_type(argname="argument delete_protection_state", value=delete_protection_state, expected_type=type_hints["delete_protection_state"])
            check_type(argname="argument deletion_policy", value=deletion_policy, expected_type=type_hints["deletion_policy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument point_in_time_recovery_enablement", value=point_in_time_recovery_enablement, expected_type=type_hints["point_in_time_recovery_enablement"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location_id": location_id,
            "name": name,
            "type": type,
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
        if app_engine_integration_mode is not None:
            self._values["app_engine_integration_mode"] = app_engine_integration_mode
        if cmek_config is not None:
            self._values["cmek_config"] = cmek_config
        if concurrency_mode is not None:
            self._values["concurrency_mode"] = concurrency_mode
        if database_edition is not None:
            self._values["database_edition"] = database_edition
        if delete_protection_state is not None:
            self._values["delete_protection_state"] = delete_protection_state
        if deletion_policy is not None:
            self._values["deletion_policy"] = deletion_policy
        if id is not None:
            self._values["id"] = id
        if point_in_time_recovery_enablement is not None:
            self._values["point_in_time_recovery_enablement"] = point_in_time_recovery_enablement
        if project is not None:
            self._values["project"] = project
        if tags is not None:
            self._values["tags"] = tags
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
    def location_id(self) -> builtins.str:
        '''The location of the database. Available locations are listed at https://cloud.google.com/firestore/docs/locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#location_id FirestoreDatabase#location_id}
        '''
        result = self._values.get("location_id")
        assert result is not None, "Required property 'location_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The ID to use for the database, which will become the final component of the database's resource name.

        This value should be 4-63
        characters. Valid characters are /[a-z][0-9]-/ with first character
        a letter and the last a letter or a number. Must not be
        UUID-like /[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}/.
        "(default)" database id is also valid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#name FirestoreDatabase#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of the database. See https://cloud.google.com/datastore/docs/firestore-or-datastore for information about how to choose. Possible values: ["FIRESTORE_NATIVE", "DATASTORE_MODE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#type FirestoreDatabase#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_engine_integration_mode(self) -> typing.Optional[builtins.str]:
        '''The App Engine integration mode to use for this database. Possible values: ["ENABLED", "DISABLED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#app_engine_integration_mode FirestoreDatabase#app_engine_integration_mode}
        '''
        result = self._values.get("app_engine_integration_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cmek_config(self) -> typing.Optional[FirestoreDatabaseCmekConfig]:
        '''cmek_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#cmek_config FirestoreDatabase#cmek_config}
        '''
        result = self._values.get("cmek_config")
        return typing.cast(typing.Optional[FirestoreDatabaseCmekConfig], result)

    @builtins.property
    def concurrency_mode(self) -> typing.Optional[builtins.str]:
        '''The concurrency control mode to use for this database. Possible values: ["OPTIMISTIC", "PESSIMISTIC", "OPTIMISTIC_WITH_ENTITY_GROUPS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#concurrency_mode FirestoreDatabase#concurrency_mode}
        '''
        result = self._values.get("concurrency_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_edition(self) -> typing.Optional[builtins.str]:
        '''The database edition. Possible values: ["STANDARD", "ENTERPRISE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#database_edition FirestoreDatabase#database_edition}
        '''
        result = self._values.get("database_edition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete_protection_state(self) -> typing.Optional[builtins.str]:
        '''State of delete protection for the database.

        When delete protection is enabled, this database cannot be deleted.
        The default value is 'DELETE_PROTECTION_STATE_UNSPECIFIED', which is currently equivalent to 'DELETE_PROTECTION_DISABLED'.
        **Note:** Additionally, to delete this database using 'terraform destroy', 'deletion_policy' must be set to 'DELETE'. Possible values: ["DELETE_PROTECTION_STATE_UNSPECIFIED", "DELETE_PROTECTION_ENABLED", "DELETE_PROTECTION_DISABLED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#delete_protection_state FirestoreDatabase#delete_protection_state}
        '''
        result = self._values.get("delete_protection_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deletion_policy(self) -> typing.Optional[builtins.str]:
        '''Deletion behavior for this database.

        If the deletion policy is 'ABANDON', the database will be removed from Terraform state but not deleted from Google Cloud upon destruction.
        If the deletion policy is 'DELETE', the database will both be removed from Terraform state and deleted from Google Cloud upon destruction.
        The default value is 'ABANDON'.
        See also 'delete_protection'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#deletion_policy FirestoreDatabase#deletion_policy}
        '''
        result = self._values.get("deletion_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#id FirestoreDatabase#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def point_in_time_recovery_enablement(self) -> typing.Optional[builtins.str]:
        '''Whether to enable the PITR feature on this database.

        If 'POINT_IN_TIME_RECOVERY_ENABLED' is selected, reads are supported on selected versions of the data from within the past 7 days.
        versionRetentionPeriod and earliestVersionTime can be used to determine the supported versions. These include reads against any timestamp within the past hour
        and reads against 1-minute snapshots beyond 1 hour and within 7 days.
        If 'POINT_IN_TIME_RECOVERY_DISABLED' is selected, reads are supported on any version of the data from within the past 1 hour. Default value: "POINT_IN_TIME_RECOVERY_DISABLED" Possible values: ["POINT_IN_TIME_RECOVERY_ENABLED", "POINT_IN_TIME_RECOVERY_DISABLED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#point_in_time_recovery_enablement FirestoreDatabase#point_in_time_recovery_enablement}
        '''
        result = self._values.get("point_in_time_recovery_enablement")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#project FirestoreDatabase#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Input only.

        A map of resource manager tags. Resource manager tag keys
        and values have the same definition as resource manager tags.
        Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456.
        The field is ignored when empty. The field is immutable and causes
        resource replacement when mutated. To apply tags to an existing resource, see
        the 'google_tags_tag_value' resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#tags FirestoreDatabase#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["FirestoreDatabaseTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#timeouts FirestoreDatabase#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["FirestoreDatabaseTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirestoreDatabaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firestoreDatabase.FirestoreDatabaseTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class FirestoreDatabaseTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#create FirestoreDatabase#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#delete FirestoreDatabase#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#update FirestoreDatabase#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cca6271ed05b89ef31d59d957fb39e3fca506ee3f4ff2ea33d58d5b9384856c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#create FirestoreDatabase#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#delete FirestoreDatabase#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_database#update FirestoreDatabase#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirestoreDatabaseTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirestoreDatabaseTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firestoreDatabase.FirestoreDatabaseTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a6d6d3e7bb1e3a08758929178d0277aef3cd29ac771e443c855f1ea15aaa774)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c8e1a89d6aafdbc117db905e398574b9d94e97e3b0d818408a4602268cfb638)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dd57ab36dff50cb01f3aac44d0ee9cb37490f304e7abfa7ce9588a14c86e092)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2118f6350106f8d0ed92e01440cac4d28d33b6030826b4621d30495f85949f5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirestoreDatabaseTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirestoreDatabaseTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirestoreDatabaseTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efa097ff1f396fe84179619b5921a380f90af48aa22ae60e7af12f644aba9111)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "FirestoreDatabase",
    "FirestoreDatabaseCmekConfig",
    "FirestoreDatabaseCmekConfigOutputReference",
    "FirestoreDatabaseConfig",
    "FirestoreDatabaseTimeouts",
    "FirestoreDatabaseTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__fa57576feaeea9846b25e7ac5c4acdd0360ddbab4347df332e8404a8c9a9acfd(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location_id: builtins.str,
    name: builtins.str,
    type: builtins.str,
    app_engine_integration_mode: typing.Optional[builtins.str] = None,
    cmek_config: typing.Optional[typing.Union[FirestoreDatabaseCmekConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    concurrency_mode: typing.Optional[builtins.str] = None,
    database_edition: typing.Optional[builtins.str] = None,
    delete_protection_state: typing.Optional[builtins.str] = None,
    deletion_policy: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    point_in_time_recovery_enablement: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[FirestoreDatabaseTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__0a02dd8ab690db89f9d979b7d507795336307c0746266a87144aab7de55025ee(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f6b3e056e38e3da8dc6ab1b5b2a30aab9f07d4a3df4a71a1ac743e05c019e9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42972fa1a39a100cb88ea3fd10c7423ff03ba56d9e59f49d573cbb72f4942d1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b80c1d9500f5a4b935ca50d5eb1b44ab69dc926b5f533f766ee845c3b5d453e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1894cf7b92200cebd3c24f3bcdc59fa5c15f679bf60faed72c3c5d47e5d202f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e9608cb519c39bc315d9ba5fe350e5cedc5731bb4ff00cec582af2ae747fb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c7affc181a0f06155f8560c9552457722e59f073b0e53a3cdf28aeeebeee9f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645ab942e90f5d956093cf5c1ad13df71d17f8e07adaea7a810834fa0e924ac4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c90b7e2a80cc7e0dda24c106821fbefae2f4f016d68fdde0d19ba0748a0c32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e036a622234b9bf5a97bd67b258c3a3a3aea18b32c54b2619854b6042d97fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3dcd185b5b4419d7c590d36eb6a36b2d74778a8f756b1b25436d5da84c97905(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fdd366c43bdb37dd4d99f14e75683658460003affbf23ec48f0b3718c25cef3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b3f1d416c9861fc24f179a34a9da52f2fa0dd054b589517647139bf1387052e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c11ba4d6fbedfaf4a105e4a610fb20783a1283e4d3098d09f9ca35de40e0d2c(
    *,
    kms_key_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997bd3ec9dab590396e4c8f5f5ef68b565bfef66cc222567e735d2a09107e780(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad83f3abb1f70dc532a1a94b8498c967bce147522e0616f6df6749f871417601(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ea8116de200a110eb9aa62778687bed91f50e77344b107b3e1194c8728758bd(
    value: typing.Optional[FirestoreDatabaseCmekConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5153dd49f9a02a9777e07e581cfbafe3b2752604fb1c84b9483c03c2a6e38624(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location_id: builtins.str,
    name: builtins.str,
    type: builtins.str,
    app_engine_integration_mode: typing.Optional[builtins.str] = None,
    cmek_config: typing.Optional[typing.Union[FirestoreDatabaseCmekConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    concurrency_mode: typing.Optional[builtins.str] = None,
    database_edition: typing.Optional[builtins.str] = None,
    delete_protection_state: typing.Optional[builtins.str] = None,
    deletion_policy: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    point_in_time_recovery_enablement: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[FirestoreDatabaseTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cca6271ed05b89ef31d59d957fb39e3fca506ee3f4ff2ea33d58d5b9384856c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a6d6d3e7bb1e3a08758929178d0277aef3cd29ac771e443c855f1ea15aaa774(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c8e1a89d6aafdbc117db905e398574b9d94e97e3b0d818408a4602268cfb638(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd57ab36dff50cb01f3aac44d0ee9cb37490f304e7abfa7ce9588a14c86e092(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2118f6350106f8d0ed92e01440cac4d28d33b6030826b4621d30495f85949f5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efa097ff1f396fe84179619b5921a380f90af48aa22ae60e7af12f644aba9111(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirestoreDatabaseTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
