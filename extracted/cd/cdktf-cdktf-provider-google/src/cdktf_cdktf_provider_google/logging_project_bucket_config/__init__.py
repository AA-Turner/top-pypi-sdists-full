r'''
# `google_logging_project_bucket_config`

Refer to the Terraform Registry for docs: [`google_logging_project_bucket_config`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config).
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


class LoggingProjectBucketConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.loggingProjectBucketConfig.LoggingProjectBucketConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config google_logging_project_bucket_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        bucket_id: builtins.str,
        location: builtins.str,
        project: builtins.str,
        cmek_settings: typing.Optional[typing.Union["LoggingProjectBucketConfigCmekSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_analytics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        index_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoggingProjectBucketConfigIndexConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retention_days: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config google_logging_project_bucket_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bucket_id: The name of the logging bucket. Logging automatically creates two log buckets: _Required and _Default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#bucket_id LoggingProjectBucketConfig#bucket_id}
        :param location: The location of the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#location LoggingProjectBucketConfig#location}
        :param project: The parent project that contains the logging bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#project LoggingProjectBucketConfig#project}
        :param cmek_settings: cmek_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#cmek_settings LoggingProjectBucketConfig#cmek_settings}
        :param description: An optional description for this bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#description LoggingProjectBucketConfig#description}
        :param enable_analytics: Enable log analytics for the bucket. Cannot be disabled once enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#enable_analytics LoggingProjectBucketConfig#enable_analytics}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#id LoggingProjectBucketConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param index_configs: index_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#index_configs LoggingProjectBucketConfig#index_configs}
        :param locked: Whether the bucket is locked. The retention period on a locked bucket cannot be changed. Locked buckets may only be deleted if they are empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#locked LoggingProjectBucketConfig#locked}
        :param retention_days: Logs will be retained by default for this amount of time, after which they will automatically be deleted. The minimum retention period is 1 day. If this value is set to zero at bucket creation time, the default time of 30 days will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#retention_days LoggingProjectBucketConfig#retention_days}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d60cdb6752e0e4bf9016fc0b1bfa9a309159c7762e2d76d86644fa611409e9f4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LoggingProjectBucketConfigConfig(
            bucket_id=bucket_id,
            location=location,
            project=project,
            cmek_settings=cmek_settings,
            description=description,
            enable_analytics=enable_analytics,
            id=id,
            index_configs=index_configs,
            locked=locked,
            retention_days=retention_days,
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
        '''Generates CDKTF code for importing a LoggingProjectBucketConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LoggingProjectBucketConfig to import.
        :param import_from_id: The id of the existing LoggingProjectBucketConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LoggingProjectBucketConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d454f1b31750b0bb0c9b1f6b5ab6c29596e7d6fffbb34a0af205b0363f5ab74d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCmekSettings")
    def put_cmek_settings(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: The resource name for the configured Cloud KMS key. KMS key name format: "projects/[PROJECT_ID]/locations/[LOCATION]/keyRings/[KEYRING]/cryptoKeys/[KEY]" To enable CMEK for the bucket, set this field to a valid kmsKeyName for which the associated service account has the required cloudkms.cryptoKeyEncrypterDecrypter roles assigned for the key. The Cloud KMS key used by the bucket can be updated by changing the kmsKeyName to a new valid key name. Encryption operations that are in progress will be completed with the key that was in use when they started. Decryption operations will be completed using the key that was used at the time of encryption unless access to that key has been revoked. See `Enabling CMEK for Logging Buckets <https://cloud.google.com/logging/docs/routing/managed-encryption-storage>`_ for more information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#kms_key_name LoggingProjectBucketConfig#kms_key_name}
        '''
        value = LoggingProjectBucketConfigCmekSettings(kms_key_name=kms_key_name)

        return typing.cast(None, jsii.invoke(self, "putCmekSettings", [value]))

    @jsii.member(jsii_name="putIndexConfigs")
    def put_index_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoggingProjectBucketConfigIndexConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a330eb957e5b5ea8c04039b15b86428dfa73c8a2d90f44a2079dcccdce94f74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIndexConfigs", [value]))

    @jsii.member(jsii_name="resetCmekSettings")
    def reset_cmek_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCmekSettings", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnableAnalytics")
    def reset_enable_analytics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableAnalytics", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIndexConfigs")
    def reset_index_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIndexConfigs", []))

    @jsii.member(jsii_name="resetLocked")
    def reset_locked(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocked", []))

    @jsii.member(jsii_name="resetRetentionDays")
    def reset_retention_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionDays", []))

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
    @jsii.member(jsii_name="cmekSettings")
    def cmek_settings(self) -> "LoggingProjectBucketConfigCmekSettingsOutputReference":
        return typing.cast("LoggingProjectBucketConfigCmekSettingsOutputReference", jsii.get(self, "cmekSettings"))

    @builtins.property
    @jsii.member(jsii_name="indexConfigs")
    def index_configs(self) -> "LoggingProjectBucketConfigIndexConfigsList":
        return typing.cast("LoggingProjectBucketConfigIndexConfigsList", jsii.get(self, "indexConfigs"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleState")
    def lifecycle_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifecycleState"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="bucketIdInput")
    def bucket_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cmekSettingsInput")
    def cmek_settings_input(
        self,
    ) -> typing.Optional["LoggingProjectBucketConfigCmekSettings"]:
        return typing.cast(typing.Optional["LoggingProjectBucketConfigCmekSettings"], jsii.get(self, "cmekSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableAnalyticsInput")
    def enable_analytics_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableAnalyticsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="indexConfigsInput")
    def index_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoggingProjectBucketConfigIndexConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoggingProjectBucketConfigIndexConfigs"]]], jsii.get(self, "indexConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="lockedInput")
    def locked_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "lockedInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionDaysInput")
    def retention_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketId")
    def bucket_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketId"))

    @bucket_id.setter
    def bucket_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cbddc69f32730c8b1ac2b30b18e4c915ac3c2d1a016a7f1007c4b59e7b96a09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aac66079155697d9c5afcd11768964e46a1e644305be2076cf3738ea58b32859)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableAnalytics")
    def enable_analytics(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableAnalytics"))

    @enable_analytics.setter
    def enable_analytics(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf97e53e1fb586b58a913deb6cb1df337dfd5f5ba95310df6ffb1c40a79a7154)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAnalytics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae375fc0f47d2acf6c6d05b9ef4eff58467da2c35d090d1c632ae7097d094346)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5989e87adaf084283ed13f93b736b10cfad3110ea2f20b6ba1cb62c519fe7a01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="locked")
    def locked(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "locked"))

    @locked.setter
    def locked(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74c510a8d23157bbe8a246447c5d046d8a42340e7d0b81074aa1978c680d20ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locked", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad8793a599322ece0369a04887bb17ffd3acb1944ecae2d1b54dff0f72d3901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionDays")
    def retention_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionDays"))

    @retention_days.setter
    def retention_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6777dd901df032a267b3209f6f463e4be270e7817ff8ef0bcab9479dfda153b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionDays", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.loggingProjectBucketConfig.LoggingProjectBucketConfigCmekSettings",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class LoggingProjectBucketConfigCmekSettings:
    def __init__(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: The resource name for the configured Cloud KMS key. KMS key name format: "projects/[PROJECT_ID]/locations/[LOCATION]/keyRings/[KEYRING]/cryptoKeys/[KEY]" To enable CMEK for the bucket, set this field to a valid kmsKeyName for which the associated service account has the required cloudkms.cryptoKeyEncrypterDecrypter roles assigned for the key. The Cloud KMS key used by the bucket can be updated by changing the kmsKeyName to a new valid key name. Encryption operations that are in progress will be completed with the key that was in use when they started. Decryption operations will be completed using the key that was used at the time of encryption unless access to that key has been revoked. See `Enabling CMEK for Logging Buckets <https://cloud.google.com/logging/docs/routing/managed-encryption-storage>`_ for more information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#kms_key_name LoggingProjectBucketConfig#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__398831ed2cfc9c780022f4726f6c25c0af44b8fdf564d048035aa84deed25014)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_name": kms_key_name,
        }

    @builtins.property
    def kms_key_name(self) -> builtins.str:
        '''The resource name for the configured Cloud KMS key.

        KMS key name format:
        "projects/[PROJECT_ID]/locations/[LOCATION]/keyRings/[KEYRING]/cryptoKeys/[KEY]"
        To enable CMEK for the bucket, set this field to a valid kmsKeyName for which the associated service account has the required cloudkms.cryptoKeyEncrypterDecrypter roles assigned for the key.
        The Cloud KMS key used by the bucket can be updated by changing the kmsKeyName to a new valid key name. Encryption operations that are in progress will be completed with the key that was in use when they started. Decryption operations will be completed using the key that was used at the time of encryption unless access to that key has been revoked.
        See `Enabling CMEK for Logging Buckets <https://cloud.google.com/logging/docs/routing/managed-encryption-storage>`_ for more information.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#kms_key_name LoggingProjectBucketConfig#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        assert result is not None, "Required property 'kms_key_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingProjectBucketConfigCmekSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoggingProjectBucketConfigCmekSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.loggingProjectBucketConfig.LoggingProjectBucketConfigCmekSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8759598f699a2c3392fd23022a3468548237c2033129bc2c9dd4f19295045f30)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="kmsKeyVersionName")
    def kms_key_version_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyVersionName"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountId")
    def service_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountId"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__26b143a6a4dfdec044c9cabc4c2c369cf824489b57bf92751a57d51ae11ccfff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LoggingProjectBucketConfigCmekSettings]:
        return typing.cast(typing.Optional[LoggingProjectBucketConfigCmekSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LoggingProjectBucketConfigCmekSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5065cc4fe30012b28849a0a4df03e0afba359a7d5a5a67b4b4b938778059cfeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.loggingProjectBucketConfig.LoggingProjectBucketConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "bucket_id": "bucketId",
        "location": "location",
        "project": "project",
        "cmek_settings": "cmekSettings",
        "description": "description",
        "enable_analytics": "enableAnalytics",
        "id": "id",
        "index_configs": "indexConfigs",
        "locked": "locked",
        "retention_days": "retentionDays",
    },
)
class LoggingProjectBucketConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bucket_id: builtins.str,
        location: builtins.str,
        project: builtins.str,
        cmek_settings: typing.Optional[typing.Union[LoggingProjectBucketConfigCmekSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_analytics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        index_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoggingProjectBucketConfigIndexConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retention_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bucket_id: The name of the logging bucket. Logging automatically creates two log buckets: _Required and _Default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#bucket_id LoggingProjectBucketConfig#bucket_id}
        :param location: The location of the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#location LoggingProjectBucketConfig#location}
        :param project: The parent project that contains the logging bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#project LoggingProjectBucketConfig#project}
        :param cmek_settings: cmek_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#cmek_settings LoggingProjectBucketConfig#cmek_settings}
        :param description: An optional description for this bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#description LoggingProjectBucketConfig#description}
        :param enable_analytics: Enable log analytics for the bucket. Cannot be disabled once enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#enable_analytics LoggingProjectBucketConfig#enable_analytics}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#id LoggingProjectBucketConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param index_configs: index_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#index_configs LoggingProjectBucketConfig#index_configs}
        :param locked: Whether the bucket is locked. The retention period on a locked bucket cannot be changed. Locked buckets may only be deleted if they are empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#locked LoggingProjectBucketConfig#locked}
        :param retention_days: Logs will be retained by default for this amount of time, after which they will automatically be deleted. The minimum retention period is 1 day. If this value is set to zero at bucket creation time, the default time of 30 days will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#retention_days LoggingProjectBucketConfig#retention_days}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cmek_settings, dict):
            cmek_settings = LoggingProjectBucketConfigCmekSettings(**cmek_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8a16f59ba4c9cb4b3ba1620ef8af75cf38ad8c99c95f4aa69dde79a51f51a4d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument bucket_id", value=bucket_id, expected_type=type_hints["bucket_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument cmek_settings", value=cmek_settings, expected_type=type_hints["cmek_settings"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_analytics", value=enable_analytics, expected_type=type_hints["enable_analytics"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument index_configs", value=index_configs, expected_type=type_hints["index_configs"])
            check_type(argname="argument locked", value=locked, expected_type=type_hints["locked"])
            check_type(argname="argument retention_days", value=retention_days, expected_type=type_hints["retention_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_id": bucket_id,
            "location": location,
            "project": project,
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
        if cmek_settings is not None:
            self._values["cmek_settings"] = cmek_settings
        if description is not None:
            self._values["description"] = description
        if enable_analytics is not None:
            self._values["enable_analytics"] = enable_analytics
        if id is not None:
            self._values["id"] = id
        if index_configs is not None:
            self._values["index_configs"] = index_configs
        if locked is not None:
            self._values["locked"] = locked
        if retention_days is not None:
            self._values["retention_days"] = retention_days

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
    def bucket_id(self) -> builtins.str:
        '''The name of the logging bucket. Logging automatically creates two log buckets: _Required and _Default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#bucket_id LoggingProjectBucketConfig#bucket_id}
        '''
        result = self._values.get("bucket_id")
        assert result is not None, "Required property 'bucket_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#location LoggingProjectBucketConfig#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        '''The parent project that contains the logging bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#project LoggingProjectBucketConfig#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cmek_settings(self) -> typing.Optional[LoggingProjectBucketConfigCmekSettings]:
        '''cmek_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#cmek_settings LoggingProjectBucketConfig#cmek_settings}
        '''
        result = self._values.get("cmek_settings")
        return typing.cast(typing.Optional[LoggingProjectBucketConfigCmekSettings], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for this bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#description LoggingProjectBucketConfig#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_analytics(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable log analytics for the bucket. Cannot be disabled once enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#enable_analytics LoggingProjectBucketConfig#enable_analytics}
        '''
        result = self._values.get("enable_analytics")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#id LoggingProjectBucketConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def index_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoggingProjectBucketConfigIndexConfigs"]]]:
        '''index_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#index_configs LoggingProjectBucketConfig#index_configs}
        '''
        result = self._values.get("index_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoggingProjectBucketConfigIndexConfigs"]]], result)

    @builtins.property
    def locked(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the bucket is locked.

        The retention period on a locked bucket cannot be changed. Locked buckets may only be deleted if they are empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#locked LoggingProjectBucketConfig#locked}
        '''
        result = self._values.get("locked")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def retention_days(self) -> typing.Optional[jsii.Number]:
        '''Logs will be retained by default for this amount of time, after which they will automatically be deleted.

        The minimum retention period is 1 day. If this value is set to zero at bucket creation time, the default time of 30 days will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#retention_days LoggingProjectBucketConfig#retention_days}
        '''
        result = self._values.get("retention_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingProjectBucketConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.loggingProjectBucketConfig.LoggingProjectBucketConfigIndexConfigs",
    jsii_struct_bases=[],
    name_mapping={"field_path": "fieldPath", "type": "type"},
)
class LoggingProjectBucketConfigIndexConfigs:
    def __init__(self, *, field_path: builtins.str, type: builtins.str) -> None:
        '''
        :param field_path: The LogEntry field path to index. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#field_path LoggingProjectBucketConfig#field_path}
        :param type: The type of data in this index Note that some paths are automatically indexed, and other paths are not eligible for indexing. See `indexing documentation <https://cloud.google.com/logging/docs/view/advanced-queries#indexed-fields>`_ for details. For example: jsonPayload.request.status Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#type LoggingProjectBucketConfig#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fab17aed02a938f13c111b40f9fdd830c003581a9339125a9b9253bb53182b5)
            check_type(argname="argument field_path", value=field_path, expected_type=type_hints["field_path"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "field_path": field_path,
            "type": type,
        }

    @builtins.property
    def field_path(self) -> builtins.str:
        '''The LogEntry field path to index.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#field_path LoggingProjectBucketConfig#field_path}
        '''
        result = self._values.get("field_path")
        assert result is not None, "Required property 'field_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of data in this index Note that some paths are automatically indexed, and other paths are not eligible for indexing.

        See `indexing documentation <https://cloud.google.com/logging/docs/view/advanced-queries#indexed-fields>`_ for details.
        For example: jsonPayload.request.status

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_project_bucket_config#type LoggingProjectBucketConfig#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingProjectBucketConfigIndexConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoggingProjectBucketConfigIndexConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.loggingProjectBucketConfig.LoggingProjectBucketConfigIndexConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddddbf9b1ccfc47f00dfd6aea99f6067206692725c18cb60fc75b342b417d77d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LoggingProjectBucketConfigIndexConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe6f416988cde764cd868747070442832e13e3bb5dae09e5a39c3ca77746f4dc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LoggingProjectBucketConfigIndexConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab4155d796d092be6dfbe2a2d139c1ec8a030abb5d5d64270bd11e9f466d1d97)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd3c47ea7f2d88f81457b16c7276a91137c2854868b86894d9e71b4d89dd9023)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37df621840792ce1d546cbc4cde2a08dfccf7c1dc32b16e9f83427664440fa0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoggingProjectBucketConfigIndexConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoggingProjectBucketConfigIndexConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoggingProjectBucketConfigIndexConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ff48d2c825023f545118098926fed94e21f4cb9ce9f35cb4fc412683a7ba8a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LoggingProjectBucketConfigIndexConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.loggingProjectBucketConfig.LoggingProjectBucketConfigIndexConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eaa7c7823c055968ad1c7b2f20409799bc4f6f3aee548ece637a50c7ef7df118)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="fieldPathInput")
    def field_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldPathInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldPath")
    def field_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldPath"))

    @field_path.setter
    def field_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f410839f2060ad3455c976765c96567636f361b6515021473b724ae8e8f876f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f48974dbb1807e7af055bd1e73a0525409374be0f1873c7c5188102da111346)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LoggingProjectBucketConfigIndexConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LoggingProjectBucketConfigIndexConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LoggingProjectBucketConfigIndexConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c311b2a638ded3fb03982f37385a02618c2c498d8c15e4b153648dcb0c92643)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LoggingProjectBucketConfig",
    "LoggingProjectBucketConfigCmekSettings",
    "LoggingProjectBucketConfigCmekSettingsOutputReference",
    "LoggingProjectBucketConfigConfig",
    "LoggingProjectBucketConfigIndexConfigs",
    "LoggingProjectBucketConfigIndexConfigsList",
    "LoggingProjectBucketConfigIndexConfigsOutputReference",
]

publication.publish()

def _typecheckingstub__d60cdb6752e0e4bf9016fc0b1bfa9a309159c7762e2d76d86644fa611409e9f4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    bucket_id: builtins.str,
    location: builtins.str,
    project: builtins.str,
    cmek_settings: typing.Optional[typing.Union[LoggingProjectBucketConfigCmekSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_analytics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    index_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoggingProjectBucketConfigIndexConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retention_days: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__d454f1b31750b0bb0c9b1f6b5ab6c29596e7d6fffbb34a0af205b0363f5ab74d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a330eb957e5b5ea8c04039b15b86428dfa73c8a2d90f44a2079dcccdce94f74(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoggingProjectBucketConfigIndexConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cbddc69f32730c8b1ac2b30b18e4c915ac3c2d1a016a7f1007c4b59e7b96a09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aac66079155697d9c5afcd11768964e46a1e644305be2076cf3738ea58b32859(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf97e53e1fb586b58a913deb6cb1df337dfd5f5ba95310df6ffb1c40a79a7154(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae375fc0f47d2acf6c6d05b9ef4eff58467da2c35d090d1c632ae7097d094346(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5989e87adaf084283ed13f93b736b10cfad3110ea2f20b6ba1cb62c519fe7a01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c510a8d23157bbe8a246447c5d046d8a42340e7d0b81074aa1978c680d20ef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad8793a599322ece0369a04887bb17ffd3acb1944ecae2d1b54dff0f72d3901(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6777dd901df032a267b3209f6f463e4be270e7817ff8ef0bcab9479dfda153b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398831ed2cfc9c780022f4726f6c25c0af44b8fdf564d048035aa84deed25014(
    *,
    kms_key_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8759598f699a2c3392fd23022a3468548237c2033129bc2c9dd4f19295045f30(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26b143a6a4dfdec044c9cabc4c2c369cf824489b57bf92751a57d51ae11ccfff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5065cc4fe30012b28849a0a4df03e0afba359a7d5a5a67b4b4b938778059cfeb(
    value: typing.Optional[LoggingProjectBucketConfigCmekSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8a16f59ba4c9cb4b3ba1620ef8af75cf38ad8c99c95f4aa69dde79a51f51a4d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bucket_id: builtins.str,
    location: builtins.str,
    project: builtins.str,
    cmek_settings: typing.Optional[typing.Union[LoggingProjectBucketConfigCmekSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_analytics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    index_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoggingProjectBucketConfigIndexConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retention_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fab17aed02a938f13c111b40f9fdd830c003581a9339125a9b9253bb53182b5(
    *,
    field_path: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddddbf9b1ccfc47f00dfd6aea99f6067206692725c18cb60fc75b342b417d77d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe6f416988cde764cd868747070442832e13e3bb5dae09e5a39c3ca77746f4dc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab4155d796d092be6dfbe2a2d139c1ec8a030abb5d5d64270bd11e9f466d1d97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd3c47ea7f2d88f81457b16c7276a91137c2854868b86894d9e71b4d89dd9023(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37df621840792ce1d546cbc4cde2a08dfccf7c1dc32b16e9f83427664440fa0b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ff48d2c825023f545118098926fed94e21f4cb9ce9f35cb4fc412683a7ba8a0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoggingProjectBucketConfigIndexConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa7c7823c055968ad1c7b2f20409799bc4f6f3aee548ece637a50c7ef7df118(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f410839f2060ad3455c976765c96567636f361b6515021473b724ae8e8f876f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f48974dbb1807e7af055bd1e73a0525409374be0f1873c7c5188102da111346(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c311b2a638ded3fb03982f37385a02618c2c498d8c15e4b153648dcb0c92643(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LoggingProjectBucketConfigIndexConfigs]],
) -> None:
    """Type checking stubs"""
    pass
