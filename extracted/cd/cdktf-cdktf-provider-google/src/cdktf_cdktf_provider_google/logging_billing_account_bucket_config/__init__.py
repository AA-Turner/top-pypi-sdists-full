r'''
# `google_logging_billing_account_bucket_config`

Refer to the Terraform Registry for docs: [`google_logging_billing_account_bucket_config`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config).
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


class LoggingBillingAccountBucketConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.loggingBillingAccountBucketConfig.LoggingBillingAccountBucketConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config google_logging_billing_account_bucket_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        billing_account: builtins.str,
        bucket_id: builtins.str,
        location: builtins.str,
        cmek_settings: typing.Optional[typing.Union["LoggingBillingAccountBucketConfigCmekSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        index_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoggingBillingAccountBucketConfigIndexConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        retention_days: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config google_logging_billing_account_bucket_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param billing_account: The parent resource that contains the logging bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#billing_account LoggingBillingAccountBucketConfig#billing_account}
        :param bucket_id: The name of the logging bucket. Logging automatically creates two log buckets: _Required and _Default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#bucket_id LoggingBillingAccountBucketConfig#bucket_id}
        :param location: The location of the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#location LoggingBillingAccountBucketConfig#location}
        :param cmek_settings: cmek_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#cmek_settings LoggingBillingAccountBucketConfig#cmek_settings}
        :param description: An optional description for this bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#description LoggingBillingAccountBucketConfig#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#id LoggingBillingAccountBucketConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param index_configs: index_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#index_configs LoggingBillingAccountBucketConfig#index_configs}
        :param retention_days: Logs will be retained by default for this amount of time, after which they will automatically be deleted. The minimum retention period is 1 day. If this value is set to zero at bucket creation time, the default time of 30 days will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#retention_days LoggingBillingAccountBucketConfig#retention_days}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c8df6e8e885be404b3f81d14d1e6318bbed91b890c9e510875b779952c10263)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LoggingBillingAccountBucketConfigConfig(
            billing_account=billing_account,
            bucket_id=bucket_id,
            location=location,
            cmek_settings=cmek_settings,
            description=description,
            id=id,
            index_configs=index_configs,
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
        '''Generates CDKTF code for importing a LoggingBillingAccountBucketConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LoggingBillingAccountBucketConfig to import.
        :param import_from_id: The id of the existing LoggingBillingAccountBucketConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LoggingBillingAccountBucketConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__185e52e2a46b4f0d2cc0d22a6ac9695726dc6e6d84f7c5a6999a008a268a3198)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCmekSettings")
    def put_cmek_settings(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: The resource name for the configured Cloud KMS key. KMS key name format: "projects/[PROJECT_ID]/locations/[LOCATION]/keyRings/[KEYRING]/cryptoKeys/[KEY]" To enable CMEK for the bucket, set this field to a valid kmsKeyName for which the associated service account has the required cloudkms.cryptoKeyEncrypterDecrypter roles assigned for the key. The Cloud KMS key used by the bucket can be updated by changing the kmsKeyName to a new valid key name. Encryption operations that are in progress will be completed with the key that was in use when they started. Decryption operations will be completed using the key that was used at the time of encryption unless access to that key has been revoked. See `Enabling CMEK for Logging Buckets <https://cloud.google.com/logging/docs/routing/managed-encryption-storage>`_ for more information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#kms_key_name LoggingBillingAccountBucketConfig#kms_key_name}
        '''
        value = LoggingBillingAccountBucketConfigCmekSettings(
            kms_key_name=kms_key_name
        )

        return typing.cast(None, jsii.invoke(self, "putCmekSettings", [value]))

    @jsii.member(jsii_name="putIndexConfigs")
    def put_index_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoggingBillingAccountBucketConfigIndexConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__631a534e3e5b44684b43aa1b29a33489bd7e5498ad053452480ec43a962e6f0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIndexConfigs", [value]))

    @jsii.member(jsii_name="resetCmekSettings")
    def reset_cmek_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCmekSettings", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIndexConfigs")
    def reset_index_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIndexConfigs", []))

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
    def cmek_settings(
        self,
    ) -> "LoggingBillingAccountBucketConfigCmekSettingsOutputReference":
        return typing.cast("LoggingBillingAccountBucketConfigCmekSettingsOutputReference", jsii.get(self, "cmekSettings"))

    @builtins.property
    @jsii.member(jsii_name="indexConfigs")
    def index_configs(self) -> "LoggingBillingAccountBucketConfigIndexConfigsList":
        return typing.cast("LoggingBillingAccountBucketConfigIndexConfigsList", jsii.get(self, "indexConfigs"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleState")
    def lifecycle_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifecycleState"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="billingAccountInput")
    def billing_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "billingAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketIdInput")
    def bucket_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cmekSettingsInput")
    def cmek_settings_input(
        self,
    ) -> typing.Optional["LoggingBillingAccountBucketConfigCmekSettings"]:
        return typing.cast(typing.Optional["LoggingBillingAccountBucketConfigCmekSettings"], jsii.get(self, "cmekSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="indexConfigsInput")
    def index_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoggingBillingAccountBucketConfigIndexConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoggingBillingAccountBucketConfigIndexConfigs"]]], jsii.get(self, "indexConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionDaysInput")
    def retention_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="billingAccount")
    def billing_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "billingAccount"))

    @billing_account.setter
    def billing_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbea3665760c1cdc3421b70a2d58b62118f41773ea26579dd40c439e9b0a7f1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketId")
    def bucket_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketId"))

    @bucket_id.setter
    def bucket_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3c88aa729bba41d5659c9154a3bd9028871b135b2dff2f5d5cc617ca7b113b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ed0de2d4c5dded6f1e0e622aa71fe0f4d787782417124c356bab6d69bb93e5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddf66838a0faafd3864d58f21edaa2cc2bacc38e4872f23f5754fe2bfffdd0ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b5e254ea89da77ace77237abfe5b0ad6895cd5c75618ed1f0f92f763940a5cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionDays")
    def retention_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionDays"))

    @retention_days.setter
    def retention_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73f6fdca65b56130b6ca08e7bfae033d2b5f4c4ced23df4e347fdbe982ab17d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionDays", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.loggingBillingAccountBucketConfig.LoggingBillingAccountBucketConfigCmekSettings",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class LoggingBillingAccountBucketConfigCmekSettings:
    def __init__(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: The resource name for the configured Cloud KMS key. KMS key name format: "projects/[PROJECT_ID]/locations/[LOCATION]/keyRings/[KEYRING]/cryptoKeys/[KEY]" To enable CMEK for the bucket, set this field to a valid kmsKeyName for which the associated service account has the required cloudkms.cryptoKeyEncrypterDecrypter roles assigned for the key. The Cloud KMS key used by the bucket can be updated by changing the kmsKeyName to a new valid key name. Encryption operations that are in progress will be completed with the key that was in use when they started. Decryption operations will be completed using the key that was used at the time of encryption unless access to that key has been revoked. See `Enabling CMEK for Logging Buckets <https://cloud.google.com/logging/docs/routing/managed-encryption-storage>`_ for more information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#kms_key_name LoggingBillingAccountBucketConfig#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cd981eb3235367cc90b6a94e6423bb4fa4d24fa1675fc8974b6ca4db24f0c01)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#kms_key_name LoggingBillingAccountBucketConfig#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        assert result is not None, "Required property 'kms_key_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingBillingAccountBucketConfigCmekSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoggingBillingAccountBucketConfigCmekSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.loggingBillingAccountBucketConfig.LoggingBillingAccountBucketConfigCmekSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b01f5d0302b55f988be419089a6c6a0a346dd292a80f3806e7bb805b8a77b6ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53158a5f848b1e195821e0079de00ec50e19e5e25307741d66c9669b3ea66c2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LoggingBillingAccountBucketConfigCmekSettings]:
        return typing.cast(typing.Optional[LoggingBillingAccountBucketConfigCmekSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LoggingBillingAccountBucketConfigCmekSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d442a6c5ac3071a762fde23ad2c78c062f3fce966f4c870883f9ddac03dc99f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.loggingBillingAccountBucketConfig.LoggingBillingAccountBucketConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "billing_account": "billingAccount",
        "bucket_id": "bucketId",
        "location": "location",
        "cmek_settings": "cmekSettings",
        "description": "description",
        "id": "id",
        "index_configs": "indexConfigs",
        "retention_days": "retentionDays",
    },
)
class LoggingBillingAccountBucketConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        billing_account: builtins.str,
        bucket_id: builtins.str,
        location: builtins.str,
        cmek_settings: typing.Optional[typing.Union[LoggingBillingAccountBucketConfigCmekSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        index_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoggingBillingAccountBucketConfigIndexConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param billing_account: The parent resource that contains the logging bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#billing_account LoggingBillingAccountBucketConfig#billing_account}
        :param bucket_id: The name of the logging bucket. Logging automatically creates two log buckets: _Required and _Default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#bucket_id LoggingBillingAccountBucketConfig#bucket_id}
        :param location: The location of the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#location LoggingBillingAccountBucketConfig#location}
        :param cmek_settings: cmek_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#cmek_settings LoggingBillingAccountBucketConfig#cmek_settings}
        :param description: An optional description for this bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#description LoggingBillingAccountBucketConfig#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#id LoggingBillingAccountBucketConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param index_configs: index_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#index_configs LoggingBillingAccountBucketConfig#index_configs}
        :param retention_days: Logs will be retained by default for this amount of time, after which they will automatically be deleted. The minimum retention period is 1 day. If this value is set to zero at bucket creation time, the default time of 30 days will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#retention_days LoggingBillingAccountBucketConfig#retention_days}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cmek_settings, dict):
            cmek_settings = LoggingBillingAccountBucketConfigCmekSettings(**cmek_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__770acca8d7b2973fd1d753016510e1949c2d453afc3e683b1d250fe520dc155e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument billing_account", value=billing_account, expected_type=type_hints["billing_account"])
            check_type(argname="argument bucket_id", value=bucket_id, expected_type=type_hints["bucket_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument cmek_settings", value=cmek_settings, expected_type=type_hints["cmek_settings"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument index_configs", value=index_configs, expected_type=type_hints["index_configs"])
            check_type(argname="argument retention_days", value=retention_days, expected_type=type_hints["retention_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "billing_account": billing_account,
            "bucket_id": bucket_id,
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
        if cmek_settings is not None:
            self._values["cmek_settings"] = cmek_settings
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if index_configs is not None:
            self._values["index_configs"] = index_configs
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
    def billing_account(self) -> builtins.str:
        '''The parent resource that contains the logging bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#billing_account LoggingBillingAccountBucketConfig#billing_account}
        '''
        result = self._values.get("billing_account")
        assert result is not None, "Required property 'billing_account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_id(self) -> builtins.str:
        '''The name of the logging bucket. Logging automatically creates two log buckets: _Required and _Default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#bucket_id LoggingBillingAccountBucketConfig#bucket_id}
        '''
        result = self._values.get("bucket_id")
        assert result is not None, "Required property 'bucket_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#location LoggingBillingAccountBucketConfig#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cmek_settings(
        self,
    ) -> typing.Optional[LoggingBillingAccountBucketConfigCmekSettings]:
        '''cmek_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#cmek_settings LoggingBillingAccountBucketConfig#cmek_settings}
        '''
        result = self._values.get("cmek_settings")
        return typing.cast(typing.Optional[LoggingBillingAccountBucketConfigCmekSettings], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for this bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#description LoggingBillingAccountBucketConfig#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#id LoggingBillingAccountBucketConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def index_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoggingBillingAccountBucketConfigIndexConfigs"]]]:
        '''index_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#index_configs LoggingBillingAccountBucketConfig#index_configs}
        '''
        result = self._values.get("index_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoggingBillingAccountBucketConfigIndexConfigs"]]], result)

    @builtins.property
    def retention_days(self) -> typing.Optional[jsii.Number]:
        '''Logs will be retained by default for this amount of time, after which they will automatically be deleted.

        The minimum retention period is 1 day. If this value is set to zero at bucket creation time, the default time of 30 days will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#retention_days LoggingBillingAccountBucketConfig#retention_days}
        '''
        result = self._values.get("retention_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingBillingAccountBucketConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.loggingBillingAccountBucketConfig.LoggingBillingAccountBucketConfigIndexConfigs",
    jsii_struct_bases=[],
    name_mapping={"field_path": "fieldPath", "type": "type"},
)
class LoggingBillingAccountBucketConfigIndexConfigs:
    def __init__(self, *, field_path: builtins.str, type: builtins.str) -> None:
        '''
        :param field_path: The LogEntry field path to index. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#field_path LoggingBillingAccountBucketConfig#field_path}
        :param type: The type of data in this index Note that some paths are automatically indexed, and other paths are not eligible for indexing. See `indexing documentation <https://cloud.google.com/logging/docs/view/advanced-queries#indexed-fields>`_ for details. For example: jsonPayload.request.status Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#type LoggingBillingAccountBucketConfig#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbdcf09582d629fd16ef1f4cbfd271bfc41eed53742f7873a21820f113238950)
            check_type(argname="argument field_path", value=field_path, expected_type=type_hints["field_path"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "field_path": field_path,
            "type": type,
        }

    @builtins.property
    def field_path(self) -> builtins.str:
        '''The LogEntry field path to index.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#field_path LoggingBillingAccountBucketConfig#field_path}
        '''
        result = self._values.get("field_path")
        assert result is not None, "Required property 'field_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of data in this index Note that some paths are automatically indexed, and other paths are not eligible for indexing.

        See `indexing documentation <https://cloud.google.com/logging/docs/view/advanced-queries#indexed-fields>`_ for details.
        For example: jsonPayload.request.status

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_billing_account_bucket_config#type LoggingBillingAccountBucketConfig#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingBillingAccountBucketConfigIndexConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoggingBillingAccountBucketConfigIndexConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.loggingBillingAccountBucketConfig.LoggingBillingAccountBucketConfigIndexConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a2efb993690e80d68860de9ce1db48b9dfca8b05bf8145517dd1ad28fd7ad1f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LoggingBillingAccountBucketConfigIndexConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__494d417fcc5fa91bbd1d0a7b951466db51c6abdf12ad73c32bd2199495e74b7b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LoggingBillingAccountBucketConfigIndexConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f951d5831787ef8bbc6c9bd22840ca3fded7ef02345ec5f6869e12c91861b670)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53af868f2f40df421592dfff7e9e84140f47be2b4a475bcebaea9e14e84425a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e701d7bc317138ad97a45ef7e91903db585760ed4a31b1f666621cdb757c106a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoggingBillingAccountBucketConfigIndexConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoggingBillingAccountBucketConfigIndexConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoggingBillingAccountBucketConfigIndexConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dd77d8ad354ccdf4a09a1fa1931ac5643079e6919b40743dc0d4451a09ae99a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LoggingBillingAccountBucketConfigIndexConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.loggingBillingAccountBucketConfig.LoggingBillingAccountBucketConfigIndexConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e52152a78f5cb32a480a8b99c5b93c7f82c7ddc9bd531020d774e2f1e4e5f0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe6f9b5ee96d498fbf41622b62e70a4f444b6f22a2bd813d8bb49f1817ac413d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaa61e637ff705f767107371ddcc92023dc373adfedd361cbf50cfe606c8e49d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LoggingBillingAccountBucketConfigIndexConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LoggingBillingAccountBucketConfigIndexConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LoggingBillingAccountBucketConfigIndexConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d49ba9c440dbad07b72e323c9bdf49a9c7e0cfe023901eef6f9c479e7544f4ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LoggingBillingAccountBucketConfig",
    "LoggingBillingAccountBucketConfigCmekSettings",
    "LoggingBillingAccountBucketConfigCmekSettingsOutputReference",
    "LoggingBillingAccountBucketConfigConfig",
    "LoggingBillingAccountBucketConfigIndexConfigs",
    "LoggingBillingAccountBucketConfigIndexConfigsList",
    "LoggingBillingAccountBucketConfigIndexConfigsOutputReference",
]

publication.publish()

def _typecheckingstub__0c8df6e8e885be404b3f81d14d1e6318bbed91b890c9e510875b779952c10263(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    billing_account: builtins.str,
    bucket_id: builtins.str,
    location: builtins.str,
    cmek_settings: typing.Optional[typing.Union[LoggingBillingAccountBucketConfigCmekSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    index_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoggingBillingAccountBucketConfigIndexConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__185e52e2a46b4f0d2cc0d22a6ac9695726dc6e6d84f7c5a6999a008a268a3198(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631a534e3e5b44684b43aa1b29a33489bd7e5498ad053452480ec43a962e6f0a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoggingBillingAccountBucketConfigIndexConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbea3665760c1cdc3421b70a2d58b62118f41773ea26579dd40c439e9b0a7f1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c88aa729bba41d5659c9154a3bd9028871b135b2dff2f5d5cc617ca7b113b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed0de2d4c5dded6f1e0e622aa71fe0f4d787782417124c356bab6d69bb93e5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddf66838a0faafd3864d58f21edaa2cc2bacc38e4872f23f5754fe2bfffdd0ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b5e254ea89da77ace77237abfe5b0ad6895cd5c75618ed1f0f92f763940a5cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f6fdca65b56130b6ca08e7bfae033d2b5f4c4ced23df4e347fdbe982ab17d1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cd981eb3235367cc90b6a94e6423bb4fa4d24fa1675fc8974b6ca4db24f0c01(
    *,
    kms_key_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b01f5d0302b55f988be419089a6c6a0a346dd292a80f3806e7bb805b8a77b6ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53158a5f848b1e195821e0079de00ec50e19e5e25307741d66c9669b3ea66c2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d442a6c5ac3071a762fde23ad2c78c062f3fce966f4c870883f9ddac03dc99f9(
    value: typing.Optional[LoggingBillingAccountBucketConfigCmekSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__770acca8d7b2973fd1d753016510e1949c2d453afc3e683b1d250fe520dc155e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    billing_account: builtins.str,
    bucket_id: builtins.str,
    location: builtins.str,
    cmek_settings: typing.Optional[typing.Union[LoggingBillingAccountBucketConfigCmekSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    index_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoggingBillingAccountBucketConfigIndexConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    retention_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbdcf09582d629fd16ef1f4cbfd271bfc41eed53742f7873a21820f113238950(
    *,
    field_path: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2efb993690e80d68860de9ce1db48b9dfca8b05bf8145517dd1ad28fd7ad1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__494d417fcc5fa91bbd1d0a7b951466db51c6abdf12ad73c32bd2199495e74b7b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f951d5831787ef8bbc6c9bd22840ca3fded7ef02345ec5f6869e12c91861b670(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53af868f2f40df421592dfff7e9e84140f47be2b4a475bcebaea9e14e84425a1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e701d7bc317138ad97a45ef7e91903db585760ed4a31b1f666621cdb757c106a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dd77d8ad354ccdf4a09a1fa1931ac5643079e6919b40743dc0d4451a09ae99a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoggingBillingAccountBucketConfigIndexConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e52152a78f5cb32a480a8b99c5b93c7f82c7ddc9bd531020d774e2f1e4e5f0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe6f9b5ee96d498fbf41622b62e70a4f444b6f22a2bd813d8bb49f1817ac413d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa61e637ff705f767107371ddcc92023dc373adfedd361cbf50cfe606c8e49d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d49ba9c440dbad07b72e323c9bdf49a9c7e0cfe023901eef6f9c479e7544f4ae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LoggingBillingAccountBucketConfigIndexConfigs]],
) -> None:
    """Type checking stubs"""
    pass
