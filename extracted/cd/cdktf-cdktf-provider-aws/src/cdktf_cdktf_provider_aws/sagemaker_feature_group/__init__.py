r'''
# `aws_sagemaker_feature_group`

Refer to the Terraform Registry for docs: [`aws_sagemaker_feature_group`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group).
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


class SagemakerFeatureGroup(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroup",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group aws_sagemaker_feature_group}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        event_time_feature_name: builtins.str,
        feature_definition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerFeatureGroupFeatureDefinition", typing.Dict[builtins.str, typing.Any]]]],
        feature_group_name: builtins.str,
        record_identifier_feature_name: builtins.str,
        role_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        offline_store_config: typing.Optional[typing.Union["SagemakerFeatureGroupOfflineStoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        online_store_config: typing.Optional[typing.Union["SagemakerFeatureGroupOnlineStoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        throughput_config: typing.Optional[typing.Union["SagemakerFeatureGroupThroughputConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group aws_sagemaker_feature_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param event_time_feature_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#event_time_feature_name SagemakerFeatureGroup#event_time_feature_name}.
        :param feature_definition: feature_definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#feature_definition SagemakerFeatureGroup#feature_definition}
        :param feature_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#feature_group_name SagemakerFeatureGroup#feature_group_name}.
        :param record_identifier_feature_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#record_identifier_feature_name SagemakerFeatureGroup#record_identifier_feature_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#role_arn SagemakerFeatureGroup#role_arn}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#description SagemakerFeatureGroup#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#id SagemakerFeatureGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param offline_store_config: offline_store_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#offline_store_config SagemakerFeatureGroup#offline_store_config}
        :param online_store_config: online_store_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#online_store_config SagemakerFeatureGroup#online_store_config}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#tags SagemakerFeatureGroup#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#tags_all SagemakerFeatureGroup#tags_all}.
        :param throughput_config: throughput_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#throughput_config SagemakerFeatureGroup#throughput_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9c91ef1bb5461ff2a3c7186550b944001c7f829d03146414e1e2cf9493c4c31)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SagemakerFeatureGroupConfig(
            event_time_feature_name=event_time_feature_name,
            feature_definition=feature_definition,
            feature_group_name=feature_group_name,
            record_identifier_feature_name=record_identifier_feature_name,
            role_arn=role_arn,
            description=description,
            id=id,
            offline_store_config=offline_store_config,
            online_store_config=online_store_config,
            tags=tags,
            tags_all=tags_all,
            throughput_config=throughput_config,
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
        '''Generates CDKTF code for importing a SagemakerFeatureGroup resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SagemakerFeatureGroup to import.
        :param import_from_id: The id of the existing SagemakerFeatureGroup that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SagemakerFeatureGroup to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f0315c4d270d00d59489ff44c5ad6ad8ef514f4ac4f27516b053d820f756f3f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFeatureDefinition")
    def put_feature_definition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerFeatureGroupFeatureDefinition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f2de7932f37b777e95eb6662069644c82c6c36b1c6c4106c7fecca1dd69d29d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFeatureDefinition", [value]))

    @jsii.member(jsii_name="putOfflineStoreConfig")
    def put_offline_store_config(
        self,
        *,
        s3_storage_config: typing.Union["SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig", typing.Dict[builtins.str, typing.Any]],
        data_catalog_config: typing.Optional[typing.Union["SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disable_glue_table_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        table_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_storage_config: s3_storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#s3_storage_config SagemakerFeatureGroup#s3_storage_config}
        :param data_catalog_config: data_catalog_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#data_catalog_config SagemakerFeatureGroup#data_catalog_config}
        :param disable_glue_table_creation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#disable_glue_table_creation SagemakerFeatureGroup#disable_glue_table_creation}.
        :param table_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#table_format SagemakerFeatureGroup#table_format}.
        '''
        value = SagemakerFeatureGroupOfflineStoreConfig(
            s3_storage_config=s3_storage_config,
            data_catalog_config=data_catalog_config,
            disable_glue_table_creation=disable_glue_table_creation,
            table_format=table_format,
        )

        return typing.cast(None, jsii.invoke(self, "putOfflineStoreConfig", [value]))

    @jsii.member(jsii_name="putOnlineStoreConfig")
    def put_online_store_config(
        self,
        *,
        enable_online_store: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_config: typing.Optional[typing.Union["SagemakerFeatureGroupOnlineStoreConfigSecurityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_type: typing.Optional[builtins.str] = None,
        ttl_duration: typing.Optional[typing.Union["SagemakerFeatureGroupOnlineStoreConfigTtlDuration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enable_online_store: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#enable_online_store SagemakerFeatureGroup#enable_online_store}.
        :param security_config: security_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#security_config SagemakerFeatureGroup#security_config}
        :param storage_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#storage_type SagemakerFeatureGroup#storage_type}.
        :param ttl_duration: ttl_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#ttl_duration SagemakerFeatureGroup#ttl_duration}
        '''
        value = SagemakerFeatureGroupOnlineStoreConfig(
            enable_online_store=enable_online_store,
            security_config=security_config,
            storage_type=storage_type,
            ttl_duration=ttl_duration,
        )

        return typing.cast(None, jsii.invoke(self, "putOnlineStoreConfig", [value]))

    @jsii.member(jsii_name="putThroughputConfig")
    def put_throughput_config(
        self,
        *,
        provisioned_read_capacity_units: typing.Optional[jsii.Number] = None,
        provisioned_write_capacity_units: typing.Optional[jsii.Number] = None,
        throughput_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param provisioned_read_capacity_units: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#provisioned_read_capacity_units SagemakerFeatureGroup#provisioned_read_capacity_units}.
        :param provisioned_write_capacity_units: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#provisioned_write_capacity_units SagemakerFeatureGroup#provisioned_write_capacity_units}.
        :param throughput_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#throughput_mode SagemakerFeatureGroup#throughput_mode}.
        '''
        value = SagemakerFeatureGroupThroughputConfig(
            provisioned_read_capacity_units=provisioned_read_capacity_units,
            provisioned_write_capacity_units=provisioned_write_capacity_units,
            throughput_mode=throughput_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putThroughputConfig", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOfflineStoreConfig")
    def reset_offline_store_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOfflineStoreConfig", []))

    @jsii.member(jsii_name="resetOnlineStoreConfig")
    def reset_online_store_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnlineStoreConfig", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetThroughputConfig")
    def reset_throughput_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThroughputConfig", []))

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
    @jsii.member(jsii_name="featureDefinition")
    def feature_definition(self) -> "SagemakerFeatureGroupFeatureDefinitionList":
        return typing.cast("SagemakerFeatureGroupFeatureDefinitionList", jsii.get(self, "featureDefinition"))

    @builtins.property
    @jsii.member(jsii_name="offlineStoreConfig")
    def offline_store_config(
        self,
    ) -> "SagemakerFeatureGroupOfflineStoreConfigOutputReference":
        return typing.cast("SagemakerFeatureGroupOfflineStoreConfigOutputReference", jsii.get(self, "offlineStoreConfig"))

    @builtins.property
    @jsii.member(jsii_name="onlineStoreConfig")
    def online_store_config(
        self,
    ) -> "SagemakerFeatureGroupOnlineStoreConfigOutputReference":
        return typing.cast("SagemakerFeatureGroupOnlineStoreConfigOutputReference", jsii.get(self, "onlineStoreConfig"))

    @builtins.property
    @jsii.member(jsii_name="throughputConfig")
    def throughput_config(
        self,
    ) -> "SagemakerFeatureGroupThroughputConfigOutputReference":
        return typing.cast("SagemakerFeatureGroupThroughputConfigOutputReference", jsii.get(self, "throughputConfig"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="eventTimeFeatureNameInput")
    def event_time_feature_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventTimeFeatureNameInput"))

    @builtins.property
    @jsii.member(jsii_name="featureDefinitionInput")
    def feature_definition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerFeatureGroupFeatureDefinition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerFeatureGroupFeatureDefinition"]]], jsii.get(self, "featureDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="featureGroupNameInput")
    def feature_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "featureGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="offlineStoreConfigInput")
    def offline_store_config_input(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOfflineStoreConfig"]:
        return typing.cast(typing.Optional["SagemakerFeatureGroupOfflineStoreConfig"], jsii.get(self, "offlineStoreConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="onlineStoreConfigInput")
    def online_store_config_input(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOnlineStoreConfig"]:
        return typing.cast(typing.Optional["SagemakerFeatureGroupOnlineStoreConfig"], jsii.get(self, "onlineStoreConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="recordIdentifierFeatureNameInput")
    def record_identifier_feature_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordIdentifierFeatureNameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

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
    @jsii.member(jsii_name="throughputConfigInput")
    def throughput_config_input(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupThroughputConfig"]:
        return typing.cast(typing.Optional["SagemakerFeatureGroupThroughputConfig"], jsii.get(self, "throughputConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce93cdcfe3c93deb74350d340d2a5377eaec6f6a9c24694e9b549b5578cf6ddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventTimeFeatureName")
    def event_time_feature_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventTimeFeatureName"))

    @event_time_feature_name.setter
    def event_time_feature_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29ed91340de29fee123af2b2791b2399d18a233f5e3f0ddeb530343f756b63b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventTimeFeatureName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="featureGroupName")
    def feature_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "featureGroupName"))

    @feature_group_name.setter
    def feature_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4781ac5037a62f4cf2f1ac4ee77661ca9ba385a3a2ede76e33427636926c5d8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "featureGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ab127bd874f0a0effd6a6cbb4d60de2bc769bc4b95037c4967137ff071555ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recordIdentifierFeatureName")
    def record_identifier_feature_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordIdentifierFeatureName"))

    @record_identifier_feature_name.setter
    def record_identifier_feature_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20fb40824f17ca9ab70382c14d7806c36df83ac3f11c3e77593020c7405d4568)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordIdentifierFeatureName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce674253b30475b85d92cdcebb678b1d424bb93231c75bea90032ac401ea95b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__347132f965339567d931d8d0c86e78e846312d822cc7d36f24b5ac3880401859)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd4d766541ef7bedb9ae130a71a0abddbafabf3c3ea7a2fdda59456113fe00fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "event_time_feature_name": "eventTimeFeatureName",
        "feature_definition": "featureDefinition",
        "feature_group_name": "featureGroupName",
        "record_identifier_feature_name": "recordIdentifierFeatureName",
        "role_arn": "roleArn",
        "description": "description",
        "id": "id",
        "offline_store_config": "offlineStoreConfig",
        "online_store_config": "onlineStoreConfig",
        "tags": "tags",
        "tags_all": "tagsAll",
        "throughput_config": "throughputConfig",
    },
)
class SagemakerFeatureGroupConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        event_time_feature_name: builtins.str,
        feature_definition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerFeatureGroupFeatureDefinition", typing.Dict[builtins.str, typing.Any]]]],
        feature_group_name: builtins.str,
        record_identifier_feature_name: builtins.str,
        role_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        offline_store_config: typing.Optional[typing.Union["SagemakerFeatureGroupOfflineStoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        online_store_config: typing.Optional[typing.Union["SagemakerFeatureGroupOnlineStoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        throughput_config: typing.Optional[typing.Union["SagemakerFeatureGroupThroughputConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param event_time_feature_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#event_time_feature_name SagemakerFeatureGroup#event_time_feature_name}.
        :param feature_definition: feature_definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#feature_definition SagemakerFeatureGroup#feature_definition}
        :param feature_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#feature_group_name SagemakerFeatureGroup#feature_group_name}.
        :param record_identifier_feature_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#record_identifier_feature_name SagemakerFeatureGroup#record_identifier_feature_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#role_arn SagemakerFeatureGroup#role_arn}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#description SagemakerFeatureGroup#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#id SagemakerFeatureGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param offline_store_config: offline_store_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#offline_store_config SagemakerFeatureGroup#offline_store_config}
        :param online_store_config: online_store_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#online_store_config SagemakerFeatureGroup#online_store_config}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#tags SagemakerFeatureGroup#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#tags_all SagemakerFeatureGroup#tags_all}.
        :param throughput_config: throughput_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#throughput_config SagemakerFeatureGroup#throughput_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(offline_store_config, dict):
            offline_store_config = SagemakerFeatureGroupOfflineStoreConfig(**offline_store_config)
        if isinstance(online_store_config, dict):
            online_store_config = SagemakerFeatureGroupOnlineStoreConfig(**online_store_config)
        if isinstance(throughput_config, dict):
            throughput_config = SagemakerFeatureGroupThroughputConfig(**throughput_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__861775ad630b3d6478d6b4387d0af30f35c6c93a92148b2c5377dae9fcfb87d3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument event_time_feature_name", value=event_time_feature_name, expected_type=type_hints["event_time_feature_name"])
            check_type(argname="argument feature_definition", value=feature_definition, expected_type=type_hints["feature_definition"])
            check_type(argname="argument feature_group_name", value=feature_group_name, expected_type=type_hints["feature_group_name"])
            check_type(argname="argument record_identifier_feature_name", value=record_identifier_feature_name, expected_type=type_hints["record_identifier_feature_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument offline_store_config", value=offline_store_config, expected_type=type_hints["offline_store_config"])
            check_type(argname="argument online_store_config", value=online_store_config, expected_type=type_hints["online_store_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument throughput_config", value=throughput_config, expected_type=type_hints["throughput_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_time_feature_name": event_time_feature_name,
            "feature_definition": feature_definition,
            "feature_group_name": feature_group_name,
            "record_identifier_feature_name": record_identifier_feature_name,
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if offline_store_config is not None:
            self._values["offline_store_config"] = offline_store_config
        if online_store_config is not None:
            self._values["online_store_config"] = online_store_config
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if throughput_config is not None:
            self._values["throughput_config"] = throughput_config

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
    def event_time_feature_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#event_time_feature_name SagemakerFeatureGroup#event_time_feature_name}.'''
        result = self._values.get("event_time_feature_name")
        assert result is not None, "Required property 'event_time_feature_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def feature_definition(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerFeatureGroupFeatureDefinition"]]:
        '''feature_definition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#feature_definition SagemakerFeatureGroup#feature_definition}
        '''
        result = self._values.get("feature_definition")
        assert result is not None, "Required property 'feature_definition' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerFeatureGroupFeatureDefinition"]], result)

    @builtins.property
    def feature_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#feature_group_name SagemakerFeatureGroup#feature_group_name}.'''
        result = self._values.get("feature_group_name")
        assert result is not None, "Required property 'feature_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def record_identifier_feature_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#record_identifier_feature_name SagemakerFeatureGroup#record_identifier_feature_name}.'''
        result = self._values.get("record_identifier_feature_name")
        assert result is not None, "Required property 'record_identifier_feature_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#role_arn SagemakerFeatureGroup#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#description SagemakerFeatureGroup#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#id SagemakerFeatureGroup#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def offline_store_config(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOfflineStoreConfig"]:
        '''offline_store_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#offline_store_config SagemakerFeatureGroup#offline_store_config}
        '''
        result = self._values.get("offline_store_config")
        return typing.cast(typing.Optional["SagemakerFeatureGroupOfflineStoreConfig"], result)

    @builtins.property
    def online_store_config(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOnlineStoreConfig"]:
        '''online_store_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#online_store_config SagemakerFeatureGroup#online_store_config}
        '''
        result = self._values.get("online_store_config")
        return typing.cast(typing.Optional["SagemakerFeatureGroupOnlineStoreConfig"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#tags SagemakerFeatureGroup#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#tags_all SagemakerFeatureGroup#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def throughput_config(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupThroughputConfig"]:
        '''throughput_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#throughput_config SagemakerFeatureGroup#throughput_config}
        '''
        result = self._values.get("throughput_config")
        return typing.cast(typing.Optional["SagemakerFeatureGroupThroughputConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupFeatureDefinition",
    jsii_struct_bases=[],
    name_mapping={
        "collection_config": "collectionConfig",
        "collection_type": "collectionType",
        "feature_name": "featureName",
        "feature_type": "featureType",
    },
)
class SagemakerFeatureGroupFeatureDefinition:
    def __init__(
        self,
        *,
        collection_config: typing.Optional[typing.Union["SagemakerFeatureGroupFeatureDefinitionCollectionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        collection_type: typing.Optional[builtins.str] = None,
        feature_name: typing.Optional[builtins.str] = None,
        feature_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param collection_config: collection_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#collection_config SagemakerFeatureGroup#collection_config}
        :param collection_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#collection_type SagemakerFeatureGroup#collection_type}.
        :param feature_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#feature_name SagemakerFeatureGroup#feature_name}.
        :param feature_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#feature_type SagemakerFeatureGroup#feature_type}.
        '''
        if isinstance(collection_config, dict):
            collection_config = SagemakerFeatureGroupFeatureDefinitionCollectionConfig(**collection_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e6eedc76255d0dab12ba340b1de4b9c5b780e2db9a7924143c5bdf6a34a0944)
            check_type(argname="argument collection_config", value=collection_config, expected_type=type_hints["collection_config"])
            check_type(argname="argument collection_type", value=collection_type, expected_type=type_hints["collection_type"])
            check_type(argname="argument feature_name", value=feature_name, expected_type=type_hints["feature_name"])
            check_type(argname="argument feature_type", value=feature_type, expected_type=type_hints["feature_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if collection_config is not None:
            self._values["collection_config"] = collection_config
        if collection_type is not None:
            self._values["collection_type"] = collection_type
        if feature_name is not None:
            self._values["feature_name"] = feature_name
        if feature_type is not None:
            self._values["feature_type"] = feature_type

    @builtins.property
    def collection_config(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupFeatureDefinitionCollectionConfig"]:
        '''collection_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#collection_config SagemakerFeatureGroup#collection_config}
        '''
        result = self._values.get("collection_config")
        return typing.cast(typing.Optional["SagemakerFeatureGroupFeatureDefinitionCollectionConfig"], result)

    @builtins.property
    def collection_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#collection_type SagemakerFeatureGroup#collection_type}.'''
        result = self._values.get("collection_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def feature_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#feature_name SagemakerFeatureGroup#feature_name}.'''
        result = self._values.get("feature_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def feature_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#feature_type SagemakerFeatureGroup#feature_type}.'''
        result = self._values.get("feature_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupFeatureDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupFeatureDefinitionCollectionConfig",
    jsii_struct_bases=[],
    name_mapping={"vector_config": "vectorConfig"},
)
class SagemakerFeatureGroupFeatureDefinitionCollectionConfig:
    def __init__(
        self,
        *,
        vector_config: typing.Optional[typing.Union["SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param vector_config: vector_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#vector_config SagemakerFeatureGroup#vector_config}
        '''
        if isinstance(vector_config, dict):
            vector_config = SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig(**vector_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__455ddca59ac9f90a934eaa54c48a224dca368db8344ef43b1bbff571d3a65e1f)
            check_type(argname="argument vector_config", value=vector_config, expected_type=type_hints["vector_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if vector_config is not None:
            self._values["vector_config"] = vector_config

    @builtins.property
    def vector_config(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig"]:
        '''vector_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#vector_config SagemakerFeatureGroup#vector_config}
        '''
        result = self._values.get("vector_config")
        return typing.cast(typing.Optional["SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupFeatureDefinitionCollectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerFeatureGroupFeatureDefinitionCollectionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupFeatureDefinitionCollectionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04e39f0e4e0c3f8e1c08361e361ace0879a4a57345b8e8c108ab77ffa2d60edc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVectorConfig")
    def put_vector_config(
        self,
        *,
        dimension: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param dimension: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#dimension SagemakerFeatureGroup#dimension}.
        '''
        value = SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig(
            dimension=dimension
        )

        return typing.cast(None, jsii.invoke(self, "putVectorConfig", [value]))

    @jsii.member(jsii_name="resetVectorConfig")
    def reset_vector_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVectorConfig", []))

    @builtins.property
    @jsii.member(jsii_name="vectorConfig")
    def vector_config(
        self,
    ) -> "SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfigOutputReference":
        return typing.cast("SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfigOutputReference", jsii.get(self, "vectorConfig"))

    @builtins.property
    @jsii.member(jsii_name="vectorConfigInput")
    def vector_config_input(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig"]:
        return typing.cast(typing.Optional["SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig"], jsii.get(self, "vectorConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerFeatureGroupFeatureDefinitionCollectionConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupFeatureDefinitionCollectionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerFeatureGroupFeatureDefinitionCollectionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10ac235d4ad876b9a1c98d4473cf5b8c885b27a529c1f96603258e9c0b9297b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig",
    jsii_struct_bases=[],
    name_mapping={"dimension": "dimension"},
)
class SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig:
    def __init__(self, *, dimension: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param dimension: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#dimension SagemakerFeatureGroup#dimension}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0be7d3c94928aa7abbc728434a76c819c9cd06fb460e8e325923772ed72b1acd)
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dimension is not None:
            self._values["dimension"] = dimension

    @builtins.property
    def dimension(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#dimension SagemakerFeatureGroup#dimension}.'''
        result = self._values.get("dimension")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd1e38d751772fd597fd99518dc324afec1d9619c1b063c3ccc57bb6477edc54)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDimension")
    def reset_dimension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDimension", []))

    @builtins.property
    @jsii.member(jsii_name="dimensionInput")
    def dimension_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dimensionInput"))

    @builtins.property
    @jsii.member(jsii_name="dimension")
    def dimension(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dimension"))

    @dimension.setter
    def dimension(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80783e513ef407198d658c6bd752ffcec72c1f811d4b5f9738ee1f28aea7935c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dimension", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75a18eab5653e8423d7c9cf2a17df5170ad35d300756f5e5e982a334b0018b74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerFeatureGroupFeatureDefinitionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupFeatureDefinitionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0f6bbea9a1d48ee01d23af83dce8a4961e496ebfefee50c336bf730a92c690b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerFeatureGroupFeatureDefinitionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__368c85b1d5df5bb9cf37989cda3bbd5310a1fec7c5d0ee80206dbc62e0e9646b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerFeatureGroupFeatureDefinitionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31378e2885cc834747e93c343f1c3b28c7c9b0a64db180e578942819ab7f8643)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bf85ba093ddfa7140d7b758b793072e72b71a0f1950a465d8c69aefd5c5a2c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01151c73b99098dd965a2359421e038281a938d7164f55c0a3149fa659b1400a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerFeatureGroupFeatureDefinition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerFeatureGroupFeatureDefinition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerFeatureGroupFeatureDefinition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b93fba276ec50bb3b4b5b6e233c86b2a289ae208eff54bfd739301359da93213)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerFeatureGroupFeatureDefinitionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupFeatureDefinitionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9674c82c678d33b7506969f1862ef9a2a329e01af1c76cad07a03f52d2969e3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCollectionConfig")
    def put_collection_config(
        self,
        *,
        vector_config: typing.Optional[typing.Union[SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param vector_config: vector_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#vector_config SagemakerFeatureGroup#vector_config}
        '''
        value = SagemakerFeatureGroupFeatureDefinitionCollectionConfig(
            vector_config=vector_config
        )

        return typing.cast(None, jsii.invoke(self, "putCollectionConfig", [value]))

    @jsii.member(jsii_name="resetCollectionConfig")
    def reset_collection_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollectionConfig", []))

    @jsii.member(jsii_name="resetCollectionType")
    def reset_collection_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollectionType", []))

    @jsii.member(jsii_name="resetFeatureName")
    def reset_feature_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFeatureName", []))

    @jsii.member(jsii_name="resetFeatureType")
    def reset_feature_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFeatureType", []))

    @builtins.property
    @jsii.member(jsii_name="collectionConfig")
    def collection_config(
        self,
    ) -> SagemakerFeatureGroupFeatureDefinitionCollectionConfigOutputReference:
        return typing.cast(SagemakerFeatureGroupFeatureDefinitionCollectionConfigOutputReference, jsii.get(self, "collectionConfig"))

    @builtins.property
    @jsii.member(jsii_name="collectionConfigInput")
    def collection_config_input(
        self,
    ) -> typing.Optional[SagemakerFeatureGroupFeatureDefinitionCollectionConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupFeatureDefinitionCollectionConfig], jsii.get(self, "collectionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="collectionTypeInput")
    def collection_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collectionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="featureNameInput")
    def feature_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "featureNameInput"))

    @builtins.property
    @jsii.member(jsii_name="featureTypeInput")
    def feature_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "featureTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="collectionType")
    def collection_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collectionType"))

    @collection_type.setter
    def collection_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2a849c377dce350ccfd2d3b7bc8f49ddf017cb430730822b5761515ba3cec26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collectionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="featureName")
    def feature_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "featureName"))

    @feature_name.setter
    def feature_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc52de7ba6656292fac139223154d10062a8d48433aacc56552a225235be7b1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "featureName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="featureType")
    def feature_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "featureType"))

    @feature_type.setter
    def feature_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__330650f237758561954c21cfae24369f565116da3731e40db80f0c2f16499b68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "featureType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerFeatureGroupFeatureDefinition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerFeatureGroupFeatureDefinition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerFeatureGroupFeatureDefinition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad4556ba2ffa88d3076f49222f4204a9ef042b09c7021e9e8f945e0e73546267)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOfflineStoreConfig",
    jsii_struct_bases=[],
    name_mapping={
        "s3_storage_config": "s3StorageConfig",
        "data_catalog_config": "dataCatalogConfig",
        "disable_glue_table_creation": "disableGlueTableCreation",
        "table_format": "tableFormat",
    },
)
class SagemakerFeatureGroupOfflineStoreConfig:
    def __init__(
        self,
        *,
        s3_storage_config: typing.Union["SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig", typing.Dict[builtins.str, typing.Any]],
        data_catalog_config: typing.Optional[typing.Union["SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disable_glue_table_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        table_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_storage_config: s3_storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#s3_storage_config SagemakerFeatureGroup#s3_storage_config}
        :param data_catalog_config: data_catalog_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#data_catalog_config SagemakerFeatureGroup#data_catalog_config}
        :param disable_glue_table_creation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#disable_glue_table_creation SagemakerFeatureGroup#disable_glue_table_creation}.
        :param table_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#table_format SagemakerFeatureGroup#table_format}.
        '''
        if isinstance(s3_storage_config, dict):
            s3_storage_config = SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig(**s3_storage_config)
        if isinstance(data_catalog_config, dict):
            data_catalog_config = SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig(**data_catalog_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad9faef9544994fc2a7fa3833bf1730143d7164e904ea1635160e779628df790)
            check_type(argname="argument s3_storage_config", value=s3_storage_config, expected_type=type_hints["s3_storage_config"])
            check_type(argname="argument data_catalog_config", value=data_catalog_config, expected_type=type_hints["data_catalog_config"])
            check_type(argname="argument disable_glue_table_creation", value=disable_glue_table_creation, expected_type=type_hints["disable_glue_table_creation"])
            check_type(argname="argument table_format", value=table_format, expected_type=type_hints["table_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_storage_config": s3_storage_config,
        }
        if data_catalog_config is not None:
            self._values["data_catalog_config"] = data_catalog_config
        if disable_glue_table_creation is not None:
            self._values["disable_glue_table_creation"] = disable_glue_table_creation
        if table_format is not None:
            self._values["table_format"] = table_format

    @builtins.property
    def s3_storage_config(
        self,
    ) -> "SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig":
        '''s3_storage_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#s3_storage_config SagemakerFeatureGroup#s3_storage_config}
        '''
        result = self._values.get("s3_storage_config")
        assert result is not None, "Required property 's3_storage_config' is missing"
        return typing.cast("SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig", result)

    @builtins.property
    def data_catalog_config(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig"]:
        '''data_catalog_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#data_catalog_config SagemakerFeatureGroup#data_catalog_config}
        '''
        result = self._values.get("data_catalog_config")
        return typing.cast(typing.Optional["SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig"], result)

    @builtins.property
    def disable_glue_table_creation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#disable_glue_table_creation SagemakerFeatureGroup#disable_glue_table_creation}.'''
        result = self._values.get("disable_glue_table_creation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def table_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#table_format SagemakerFeatureGroup#table_format}.'''
        result = self._values.get("table_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupOfflineStoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig",
    jsii_struct_bases=[],
    name_mapping={
        "catalog": "catalog",
        "database": "database",
        "table_name": "tableName",
    },
)
class SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig:
    def __init__(
        self,
        *,
        catalog: typing.Optional[builtins.str] = None,
        database: typing.Optional[builtins.str] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param catalog: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#catalog SagemakerFeatureGroup#catalog}.
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#database SagemakerFeatureGroup#database}.
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#table_name SagemakerFeatureGroup#table_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb4c8164be71c6181be17ddc68e74a8a07b93fb60b02743b722131ebc9b1aa5)
            check_type(argname="argument catalog", value=catalog, expected_type=type_hints["catalog"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if catalog is not None:
            self._values["catalog"] = catalog
        if database is not None:
            self._values["database"] = database
        if table_name is not None:
            self._values["table_name"] = table_name

    @builtins.property
    def catalog(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#catalog SagemakerFeatureGroup#catalog}.'''
        result = self._values.get("catalog")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#database SagemakerFeatureGroup#database}.'''
        result = self._values.get("database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#table_name SagemakerFeatureGroup#table_name}.'''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35e54bd70d779b4f1cc7fb68c15e289c683d38093b167f55661a612d66b1171c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCatalog")
    def reset_catalog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCatalog", []))

    @jsii.member(jsii_name="resetDatabase")
    def reset_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabase", []))

    @jsii.member(jsii_name="resetTableName")
    def reset_table_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTableName", []))

    @builtins.property
    @jsii.member(jsii_name="catalogInput")
    def catalog_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "catalogInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="catalog")
    def catalog(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "catalog"))

    @catalog.setter
    def catalog(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e29e2c0a5b9abb18fc8fe3ea0b657fbb9896c18ce259d9875c858e18fa58c40f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "catalog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09b80fc1fe2806e2e9c78489c5918f9d751d2f16099d14716bc0fafc8fcb5db7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c62c032b156044fb8e752b936d2edec2b19678b3d690e9509e22a7dc9629a3a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0da08df1b7cf5110cd3a0241655b35a8d02bcd89f687fa4cb147be316ff77de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerFeatureGroupOfflineStoreConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOfflineStoreConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a77affbf109fd633cbed112763c946d5e26813a32ece9e749d27e8a8c049f10)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataCatalogConfig")
    def put_data_catalog_config(
        self,
        *,
        catalog: typing.Optional[builtins.str] = None,
        database: typing.Optional[builtins.str] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param catalog: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#catalog SagemakerFeatureGroup#catalog}.
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#database SagemakerFeatureGroup#database}.
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#table_name SagemakerFeatureGroup#table_name}.
        '''
        value = SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig(
            catalog=catalog, database=database, table_name=table_name
        )

        return typing.cast(None, jsii.invoke(self, "putDataCatalogConfig", [value]))

    @jsii.member(jsii_name="putS3StorageConfig")
    def put_s3_storage_config(
        self,
        *,
        s3_uri: builtins.str,
        kms_key_id: typing.Optional[builtins.str] = None,
        resolved_output_s3_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#s3_uri SagemakerFeatureGroup#s3_uri}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#kms_key_id SagemakerFeatureGroup#kms_key_id}.
        :param resolved_output_s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#resolved_output_s3_uri SagemakerFeatureGroup#resolved_output_s3_uri}.
        '''
        value = SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig(
            s3_uri=s3_uri,
            kms_key_id=kms_key_id,
            resolved_output_s3_uri=resolved_output_s3_uri,
        )

        return typing.cast(None, jsii.invoke(self, "putS3StorageConfig", [value]))

    @jsii.member(jsii_name="resetDataCatalogConfig")
    def reset_data_catalog_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataCatalogConfig", []))

    @jsii.member(jsii_name="resetDisableGlueTableCreation")
    def reset_disable_glue_table_creation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableGlueTableCreation", []))

    @jsii.member(jsii_name="resetTableFormat")
    def reset_table_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTableFormat", []))

    @builtins.property
    @jsii.member(jsii_name="dataCatalogConfig")
    def data_catalog_config(
        self,
    ) -> SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfigOutputReference:
        return typing.cast(SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfigOutputReference, jsii.get(self, "dataCatalogConfig"))

    @builtins.property
    @jsii.member(jsii_name="s3StorageConfig")
    def s3_storage_config(
        self,
    ) -> "SagemakerFeatureGroupOfflineStoreConfigS3StorageConfigOutputReference":
        return typing.cast("SagemakerFeatureGroupOfflineStoreConfigS3StorageConfigOutputReference", jsii.get(self, "s3StorageConfig"))

    @builtins.property
    @jsii.member(jsii_name="dataCatalogConfigInput")
    def data_catalog_config_input(
        self,
    ) -> typing.Optional[SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig], jsii.get(self, "dataCatalogConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="disableGlueTableCreationInput")
    def disable_glue_table_creation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableGlueTableCreationInput"))

    @builtins.property
    @jsii.member(jsii_name="s3StorageConfigInput")
    def s3_storage_config_input(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig"]:
        return typing.cast(typing.Optional["SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig"], jsii.get(self, "s3StorageConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="tableFormatInput")
    def table_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="disableGlueTableCreation")
    def disable_glue_table_creation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableGlueTableCreation"))

    @disable_glue_table_creation.setter
    def disable_glue_table_creation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef9c1796c004820ba3e35d6f74763abe6f85bf54a5a422ae1d2db30416e83e03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableGlueTableCreation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableFormat")
    def table_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableFormat"))

    @table_format.setter
    def table_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de2f13f8ba8f071803d7c1cfa79141e8df6b42e6f36736a603e762a9151231a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerFeatureGroupOfflineStoreConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupOfflineStoreConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerFeatureGroupOfflineStoreConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fefb34ad884af5f9576c1fa3f4bd7830d0034c8bfbd622964f240332f946b67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig",
    jsii_struct_bases=[],
    name_mapping={
        "s3_uri": "s3Uri",
        "kms_key_id": "kmsKeyId",
        "resolved_output_s3_uri": "resolvedOutputS3Uri",
    },
)
class SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig:
    def __init__(
        self,
        *,
        s3_uri: builtins.str,
        kms_key_id: typing.Optional[builtins.str] = None,
        resolved_output_s3_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#s3_uri SagemakerFeatureGroup#s3_uri}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#kms_key_id SagemakerFeatureGroup#kms_key_id}.
        :param resolved_output_s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#resolved_output_s3_uri SagemakerFeatureGroup#resolved_output_s3_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2f12aa114b55b0a8c6fbcff2160da3c756f952f41afb70bfbce9863a1f1c1ef)
            check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument resolved_output_s3_uri", value=resolved_output_s3_uri, expected_type=type_hints["resolved_output_s3_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_uri": s3_uri,
        }
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if resolved_output_s3_uri is not None:
            self._values["resolved_output_s3_uri"] = resolved_output_s3_uri

    @builtins.property
    def s3_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#s3_uri SagemakerFeatureGroup#s3_uri}.'''
        result = self._values.get("s3_uri")
        assert result is not None, "Required property 's3_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#kms_key_id SagemakerFeatureGroup#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resolved_output_s3_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#resolved_output_s3_uri SagemakerFeatureGroup#resolved_output_s3_uri}.'''
        result = self._values.get("resolved_output_s3_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerFeatureGroupOfflineStoreConfigS3StorageConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOfflineStoreConfigS3StorageConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8dd0a276ab23170abeb40c6b1e01cfde1ce1963d4956ff954a75ab1b28b85557)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyId")
    def reset_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyId", []))

    @jsii.member(jsii_name="resetResolvedOutputS3Uri")
    def reset_resolved_output_s3_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResolvedOutputS3Uri", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resolvedOutputS3UriInput")
    def resolved_output_s3_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resolvedOutputS3UriInput"))

    @builtins.property
    @jsii.member(jsii_name="s3UriInput")
    def s3_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3UriInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82f59e0df8c7d615a714f6fcf4524611e726fea2557d46d601ce3285ed57bf6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resolvedOutputS3Uri")
    def resolved_output_s3_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resolvedOutputS3Uri"))

    @resolved_output_s3_uri.setter
    def resolved_output_s3_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67d07835ed2af8ba093642b2d3cdf2bcbb5bda045c6821eb5b9e85eed86062b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resolvedOutputS3Uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3Uri")
    def s3_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Uri"))

    @s3_uri.setter
    def s3_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba2a26e287eaeaf2b40803b833b44bc0510ecae085c8c014212e782322dbe48e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b759b3977dfc64448d06dab3ce1a3acd5179cf41aebba5c8001e8bbda265aa63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOnlineStoreConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_online_store": "enableOnlineStore",
        "security_config": "securityConfig",
        "storage_type": "storageType",
        "ttl_duration": "ttlDuration",
    },
)
class SagemakerFeatureGroupOnlineStoreConfig:
    def __init__(
        self,
        *,
        enable_online_store: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_config: typing.Optional[typing.Union["SagemakerFeatureGroupOnlineStoreConfigSecurityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_type: typing.Optional[builtins.str] = None,
        ttl_duration: typing.Optional[typing.Union["SagemakerFeatureGroupOnlineStoreConfigTtlDuration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enable_online_store: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#enable_online_store SagemakerFeatureGroup#enable_online_store}.
        :param security_config: security_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#security_config SagemakerFeatureGroup#security_config}
        :param storage_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#storage_type SagemakerFeatureGroup#storage_type}.
        :param ttl_duration: ttl_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#ttl_duration SagemakerFeatureGroup#ttl_duration}
        '''
        if isinstance(security_config, dict):
            security_config = SagemakerFeatureGroupOnlineStoreConfigSecurityConfig(**security_config)
        if isinstance(ttl_duration, dict):
            ttl_duration = SagemakerFeatureGroupOnlineStoreConfigTtlDuration(**ttl_duration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee38a4265fcad3cd94a875cfe91cdbdda34067619e0331af86857fc065525f70)
            check_type(argname="argument enable_online_store", value=enable_online_store, expected_type=type_hints["enable_online_store"])
            check_type(argname="argument security_config", value=security_config, expected_type=type_hints["security_config"])
            check_type(argname="argument storage_type", value=storage_type, expected_type=type_hints["storage_type"])
            check_type(argname="argument ttl_duration", value=ttl_duration, expected_type=type_hints["ttl_duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_online_store is not None:
            self._values["enable_online_store"] = enable_online_store
        if security_config is not None:
            self._values["security_config"] = security_config
        if storage_type is not None:
            self._values["storage_type"] = storage_type
        if ttl_duration is not None:
            self._values["ttl_duration"] = ttl_duration

    @builtins.property
    def enable_online_store(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#enable_online_store SagemakerFeatureGroup#enable_online_store}.'''
        result = self._values.get("enable_online_store")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def security_config(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOnlineStoreConfigSecurityConfig"]:
        '''security_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#security_config SagemakerFeatureGroup#security_config}
        '''
        result = self._values.get("security_config")
        return typing.cast(typing.Optional["SagemakerFeatureGroupOnlineStoreConfigSecurityConfig"], result)

    @builtins.property
    def storage_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#storage_type SagemakerFeatureGroup#storage_type}.'''
        result = self._values.get("storage_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ttl_duration(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOnlineStoreConfigTtlDuration"]:
        '''ttl_duration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#ttl_duration SagemakerFeatureGroup#ttl_duration}
        '''
        result = self._values.get("ttl_duration")
        return typing.cast(typing.Optional["SagemakerFeatureGroupOnlineStoreConfigTtlDuration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupOnlineStoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerFeatureGroupOnlineStoreConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOnlineStoreConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98e465bc2b7251e530bb3eb7b175f3f18e1ecf6cee9d8a7b0a263b3adf589732)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSecurityConfig")
    def put_security_config(
        self,
        *,
        kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#kms_key_id SagemakerFeatureGroup#kms_key_id}.
        '''
        value = SagemakerFeatureGroupOnlineStoreConfigSecurityConfig(
            kms_key_id=kms_key_id
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityConfig", [value]))

    @jsii.member(jsii_name="putTtlDuration")
    def put_ttl_duration(
        self,
        *,
        unit: typing.Optional[builtins.str] = None,
        value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#unit SagemakerFeatureGroup#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#value SagemakerFeatureGroup#value}.
        '''
        value_ = SagemakerFeatureGroupOnlineStoreConfigTtlDuration(
            unit=unit, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putTtlDuration", [value_]))

    @jsii.member(jsii_name="resetEnableOnlineStore")
    def reset_enable_online_store(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableOnlineStore", []))

    @jsii.member(jsii_name="resetSecurityConfig")
    def reset_security_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityConfig", []))

    @jsii.member(jsii_name="resetStorageType")
    def reset_storage_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageType", []))

    @jsii.member(jsii_name="resetTtlDuration")
    def reset_ttl_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTtlDuration", []))

    @builtins.property
    @jsii.member(jsii_name="securityConfig")
    def security_config(
        self,
    ) -> "SagemakerFeatureGroupOnlineStoreConfigSecurityConfigOutputReference":
        return typing.cast("SagemakerFeatureGroupOnlineStoreConfigSecurityConfigOutputReference", jsii.get(self, "securityConfig"))

    @builtins.property
    @jsii.member(jsii_name="ttlDuration")
    def ttl_duration(
        self,
    ) -> "SagemakerFeatureGroupOnlineStoreConfigTtlDurationOutputReference":
        return typing.cast("SagemakerFeatureGroupOnlineStoreConfigTtlDurationOutputReference", jsii.get(self, "ttlDuration"))

    @builtins.property
    @jsii.member(jsii_name="enableOnlineStoreInput")
    def enable_online_store_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableOnlineStoreInput"))

    @builtins.property
    @jsii.member(jsii_name="securityConfigInput")
    def security_config_input(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOnlineStoreConfigSecurityConfig"]:
        return typing.cast(typing.Optional["SagemakerFeatureGroupOnlineStoreConfigSecurityConfig"], jsii.get(self, "securityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="storageTypeInput")
    def storage_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="ttlDurationInput")
    def ttl_duration_input(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOnlineStoreConfigTtlDuration"]:
        return typing.cast(typing.Optional["SagemakerFeatureGroupOnlineStoreConfigTtlDuration"], jsii.get(self, "ttlDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="enableOnlineStore")
    def enable_online_store(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableOnlineStore"))

    @enable_online_store.setter
    def enable_online_store(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a74eeba363b265caff78cd9277ecafb7cdb319301f34301ae0c5360998b52403)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableOnlineStore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageType")
    def storage_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageType"))

    @storage_type.setter
    def storage_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bda68a3f0423e4505dc92618099b1499323d4ca4edcb635018189402383570fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SagemakerFeatureGroupOnlineStoreConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupOnlineStoreConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerFeatureGroupOnlineStoreConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf126879ae2cefdedbdf03be7795481e816ca36f92a5637790f0015537737df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOnlineStoreConfigSecurityConfig",
    jsii_struct_bases=[],
    name_mapping={"kms_key_id": "kmsKeyId"},
)
class SagemakerFeatureGroupOnlineStoreConfigSecurityConfig:
    def __init__(self, *, kms_key_id: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#kms_key_id SagemakerFeatureGroup#kms_key_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc686ddcfc2e3b1f14913382f521b738fb7b984a7539cef33008175b5c960ff)
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#kms_key_id SagemakerFeatureGroup#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupOnlineStoreConfigSecurityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerFeatureGroupOnlineStoreConfigSecurityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOnlineStoreConfigSecurityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4730cde9d9e63ec7353b59ba007e962d7ca7a1b87ce14bd65d04d3cd297f2ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyId")
    def reset_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyId", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85d322ea30ecc45d77cc90d3c4ed0f7fbc1b3fa7b5423734fb56744ad73613bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerFeatureGroupOnlineStoreConfigSecurityConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupOnlineStoreConfigSecurityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerFeatureGroupOnlineStoreConfigSecurityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb6481d9b571161f96816872fe152bec1157d35db024fef078703d21bb8bb049)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOnlineStoreConfigTtlDuration",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class SagemakerFeatureGroupOnlineStoreConfigTtlDuration:
    def __init__(
        self,
        *,
        unit: typing.Optional[builtins.str] = None,
        value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#unit SagemakerFeatureGroup#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#value SagemakerFeatureGroup#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf07da641a1e96f95283bc4a80314ef5c078127e93775ec723f3cb705cbdd761)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if unit is not None:
            self._values["unit"] = unit
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def unit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#unit SagemakerFeatureGroup#unit}.'''
        result = self._values.get("unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#value SagemakerFeatureGroup#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupOnlineStoreConfigTtlDuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerFeatureGroupOnlineStoreConfigTtlDurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOnlineStoreConfigTtlDurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1b5670a58cda1aab1aa689eb8802e4f5cd31217153a5e0bcaba7a021f047eae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUnit")
    def reset_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnit", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="unitInput")
    def unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unitInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unit"))

    @unit.setter
    def unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e633672a168188b90ab2b63fc9f4f9fcb334959c3fdf331cca290c4cbe95055a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e2b862066ecbc49dfecc1e2b700fc3c764802e2d68f1650199fc41cb79d66e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerFeatureGroupOnlineStoreConfigTtlDuration]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupOnlineStoreConfigTtlDuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerFeatureGroupOnlineStoreConfigTtlDuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1921c83108514508a9b7dca7c0982e8b5ce728875129fe8bd2193acd7e7fb0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupThroughputConfig",
    jsii_struct_bases=[],
    name_mapping={
        "provisioned_read_capacity_units": "provisionedReadCapacityUnits",
        "provisioned_write_capacity_units": "provisionedWriteCapacityUnits",
        "throughput_mode": "throughputMode",
    },
)
class SagemakerFeatureGroupThroughputConfig:
    def __init__(
        self,
        *,
        provisioned_read_capacity_units: typing.Optional[jsii.Number] = None,
        provisioned_write_capacity_units: typing.Optional[jsii.Number] = None,
        throughput_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param provisioned_read_capacity_units: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#provisioned_read_capacity_units SagemakerFeatureGroup#provisioned_read_capacity_units}.
        :param provisioned_write_capacity_units: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#provisioned_write_capacity_units SagemakerFeatureGroup#provisioned_write_capacity_units}.
        :param throughput_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#throughput_mode SagemakerFeatureGroup#throughput_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f6744c5bf4df4df2b569e55a5927cd83a8277b442899c25f0df56da01368c2f)
            check_type(argname="argument provisioned_read_capacity_units", value=provisioned_read_capacity_units, expected_type=type_hints["provisioned_read_capacity_units"])
            check_type(argname="argument provisioned_write_capacity_units", value=provisioned_write_capacity_units, expected_type=type_hints["provisioned_write_capacity_units"])
            check_type(argname="argument throughput_mode", value=throughput_mode, expected_type=type_hints["throughput_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if provisioned_read_capacity_units is not None:
            self._values["provisioned_read_capacity_units"] = provisioned_read_capacity_units
        if provisioned_write_capacity_units is not None:
            self._values["provisioned_write_capacity_units"] = provisioned_write_capacity_units
        if throughput_mode is not None:
            self._values["throughput_mode"] = throughput_mode

    @builtins.property
    def provisioned_read_capacity_units(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#provisioned_read_capacity_units SagemakerFeatureGroup#provisioned_read_capacity_units}.'''
        result = self._values.get("provisioned_read_capacity_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def provisioned_write_capacity_units(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#provisioned_write_capacity_units SagemakerFeatureGroup#provisioned_write_capacity_units}.'''
        result = self._values.get("provisioned_write_capacity_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throughput_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_feature_group#throughput_mode SagemakerFeatureGroup#throughput_mode}.'''
        result = self._values.get("throughput_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupThroughputConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerFeatureGroupThroughputConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupThroughputConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d913d0096a49f057604e0c4cc4e57fb458c448967fafe446faed0ebba12cbfe2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetProvisionedReadCapacityUnits")
    def reset_provisioned_read_capacity_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisionedReadCapacityUnits", []))

    @jsii.member(jsii_name="resetProvisionedWriteCapacityUnits")
    def reset_provisioned_write_capacity_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisionedWriteCapacityUnits", []))

    @jsii.member(jsii_name="resetThroughputMode")
    def reset_throughput_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThroughputMode", []))

    @builtins.property
    @jsii.member(jsii_name="provisionedReadCapacityUnitsInput")
    def provisioned_read_capacity_units_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "provisionedReadCapacityUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="provisionedWriteCapacityUnitsInput")
    def provisioned_write_capacity_units_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "provisionedWriteCapacityUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="throughputModeInput")
    def throughput_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "throughputModeInput"))

    @builtins.property
    @jsii.member(jsii_name="provisionedReadCapacityUnits")
    def provisioned_read_capacity_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedReadCapacityUnits"))

    @provisioned_read_capacity_units.setter
    def provisioned_read_capacity_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd2c868e570665c05da033f59ecd0b8ad01b61f2fc8809125e7949ab985e3d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedReadCapacityUnits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisionedWriteCapacityUnits")
    def provisioned_write_capacity_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedWriteCapacityUnits"))

    @provisioned_write_capacity_units.setter
    def provisioned_write_capacity_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff1e313b1d26714b6917ce2241eefde01c6b35a7d2c95efae313f57d28b92d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedWriteCapacityUnits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="throughputMode")
    def throughput_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "throughputMode"))

    @throughput_mode.setter
    def throughput_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d4b08df8a8602fccc32bb08614976189dbb4cd7382289a956f822a5404cba30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throughputMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SagemakerFeatureGroupThroughputConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupThroughputConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerFeatureGroupThroughputConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f0c2e9ba4c62aadf4beb62577fa9dbd4566081950e2b99c4cc2165615e56b48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SagemakerFeatureGroup",
    "SagemakerFeatureGroupConfig",
    "SagemakerFeatureGroupFeatureDefinition",
    "SagemakerFeatureGroupFeatureDefinitionCollectionConfig",
    "SagemakerFeatureGroupFeatureDefinitionCollectionConfigOutputReference",
    "SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig",
    "SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfigOutputReference",
    "SagemakerFeatureGroupFeatureDefinitionList",
    "SagemakerFeatureGroupFeatureDefinitionOutputReference",
    "SagemakerFeatureGroupOfflineStoreConfig",
    "SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig",
    "SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfigOutputReference",
    "SagemakerFeatureGroupOfflineStoreConfigOutputReference",
    "SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig",
    "SagemakerFeatureGroupOfflineStoreConfigS3StorageConfigOutputReference",
    "SagemakerFeatureGroupOnlineStoreConfig",
    "SagemakerFeatureGroupOnlineStoreConfigOutputReference",
    "SagemakerFeatureGroupOnlineStoreConfigSecurityConfig",
    "SagemakerFeatureGroupOnlineStoreConfigSecurityConfigOutputReference",
    "SagemakerFeatureGroupOnlineStoreConfigTtlDuration",
    "SagemakerFeatureGroupOnlineStoreConfigTtlDurationOutputReference",
    "SagemakerFeatureGroupThroughputConfig",
    "SagemakerFeatureGroupThroughputConfigOutputReference",
]

publication.publish()

def _typecheckingstub__a9c91ef1bb5461ff2a3c7186550b944001c7f829d03146414e1e2cf9493c4c31(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    event_time_feature_name: builtins.str,
    feature_definition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerFeatureGroupFeatureDefinition, typing.Dict[builtins.str, typing.Any]]]],
    feature_group_name: builtins.str,
    record_identifier_feature_name: builtins.str,
    role_arn: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    offline_store_config: typing.Optional[typing.Union[SagemakerFeatureGroupOfflineStoreConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    online_store_config: typing.Optional[typing.Union[SagemakerFeatureGroupOnlineStoreConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    throughput_config: typing.Optional[typing.Union[SagemakerFeatureGroupThroughputConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7f0315c4d270d00d59489ff44c5ad6ad8ef514f4ac4f27516b053d820f756f3f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2de7932f37b777e95eb6662069644c82c6c36b1c6c4106c7fecca1dd69d29d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerFeatureGroupFeatureDefinition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce93cdcfe3c93deb74350d340d2a5377eaec6f6a9c24694e9b549b5578cf6ddf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29ed91340de29fee123af2b2791b2399d18a233f5e3f0ddeb530343f756b63b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4781ac5037a62f4cf2f1ac4ee77661ca9ba385a3a2ede76e33427636926c5d8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab127bd874f0a0effd6a6cbb4d60de2bc769bc4b95037c4967137ff071555ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20fb40824f17ca9ab70382c14d7806c36df83ac3f11c3e77593020c7405d4568(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce674253b30475b85d92cdcebb678b1d424bb93231c75bea90032ac401ea95b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__347132f965339567d931d8d0c86e78e846312d822cc7d36f24b5ac3880401859(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd4d766541ef7bedb9ae130a71a0abddbafabf3c3ea7a2fdda59456113fe00fa(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__861775ad630b3d6478d6b4387d0af30f35c6c93a92148b2c5377dae9fcfb87d3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_time_feature_name: builtins.str,
    feature_definition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerFeatureGroupFeatureDefinition, typing.Dict[builtins.str, typing.Any]]]],
    feature_group_name: builtins.str,
    record_identifier_feature_name: builtins.str,
    role_arn: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    offline_store_config: typing.Optional[typing.Union[SagemakerFeatureGroupOfflineStoreConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    online_store_config: typing.Optional[typing.Union[SagemakerFeatureGroupOnlineStoreConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    throughput_config: typing.Optional[typing.Union[SagemakerFeatureGroupThroughputConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e6eedc76255d0dab12ba340b1de4b9c5b780e2db9a7924143c5bdf6a34a0944(
    *,
    collection_config: typing.Optional[typing.Union[SagemakerFeatureGroupFeatureDefinitionCollectionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    collection_type: typing.Optional[builtins.str] = None,
    feature_name: typing.Optional[builtins.str] = None,
    feature_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__455ddca59ac9f90a934eaa54c48a224dca368db8344ef43b1bbff571d3a65e1f(
    *,
    vector_config: typing.Optional[typing.Union[SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e39f0e4e0c3f8e1c08361e361ace0879a4a57345b8e8c108ab77ffa2d60edc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10ac235d4ad876b9a1c98d4473cf5b8c885b27a529c1f96603258e9c0b9297b1(
    value: typing.Optional[SagemakerFeatureGroupFeatureDefinitionCollectionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0be7d3c94928aa7abbc728434a76c819c9cd06fb460e8e325923772ed72b1acd(
    *,
    dimension: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd1e38d751772fd597fd99518dc324afec1d9619c1b063c3ccc57bb6477edc54(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80783e513ef407198d658c6bd752ffcec72c1f811d4b5f9738ee1f28aea7935c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a18eab5653e8423d7c9cf2a17df5170ad35d300756f5e5e982a334b0018b74(
    value: typing.Optional[SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0f6bbea9a1d48ee01d23af83dce8a4961e496ebfefee50c336bf730a92c690b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__368c85b1d5df5bb9cf37989cda3bbd5310a1fec7c5d0ee80206dbc62e0e9646b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31378e2885cc834747e93c343f1c3b28c7c9b0a64db180e578942819ab7f8643(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bf85ba093ddfa7140d7b758b793072e72b71a0f1950a465d8c69aefd5c5a2c5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01151c73b99098dd965a2359421e038281a938d7164f55c0a3149fa659b1400a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b93fba276ec50bb3b4b5b6e233c86b2a289ae208eff54bfd739301359da93213(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerFeatureGroupFeatureDefinition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9674c82c678d33b7506969f1862ef9a2a329e01af1c76cad07a03f52d2969e3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2a849c377dce350ccfd2d3b7bc8f49ddf017cb430730822b5761515ba3cec26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc52de7ba6656292fac139223154d10062a8d48433aacc56552a225235be7b1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__330650f237758561954c21cfae24369f565116da3731e40db80f0c2f16499b68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad4556ba2ffa88d3076f49222f4204a9ef042b09c7021e9e8f945e0e73546267(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerFeatureGroupFeatureDefinition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad9faef9544994fc2a7fa3833bf1730143d7164e904ea1635160e779628df790(
    *,
    s3_storage_config: typing.Union[SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig, typing.Dict[builtins.str, typing.Any]],
    data_catalog_config: typing.Optional[typing.Union[SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disable_glue_table_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    table_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb4c8164be71c6181be17ddc68e74a8a07b93fb60b02743b722131ebc9b1aa5(
    *,
    catalog: typing.Optional[builtins.str] = None,
    database: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35e54bd70d779b4f1cc7fb68c15e289c683d38093b167f55661a612d66b1171c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e29e2c0a5b9abb18fc8fe3ea0b657fbb9896c18ce259d9875c858e18fa58c40f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b80fc1fe2806e2e9c78489c5918f9d751d2f16099d14716bc0fafc8fcb5db7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62c032b156044fb8e752b936d2edec2b19678b3d690e9509e22a7dc9629a3a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0da08df1b7cf5110cd3a0241655b35a8d02bcd89f687fa4cb147be316ff77de(
    value: typing.Optional[SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a77affbf109fd633cbed112763c946d5e26813a32ece9e749d27e8a8c049f10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef9c1796c004820ba3e35d6f74763abe6f85bf54a5a422ae1d2db30416e83e03(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de2f13f8ba8f071803d7c1cfa79141e8df6b42e6f36736a603e762a9151231a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fefb34ad884af5f9576c1fa3f4bd7830d0034c8bfbd622964f240332f946b67(
    value: typing.Optional[SagemakerFeatureGroupOfflineStoreConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f12aa114b55b0a8c6fbcff2160da3c756f952f41afb70bfbce9863a1f1c1ef(
    *,
    s3_uri: builtins.str,
    kms_key_id: typing.Optional[builtins.str] = None,
    resolved_output_s3_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd0a276ab23170abeb40c6b1e01cfde1ce1963d4956ff954a75ab1b28b85557(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f59e0df8c7d615a714f6fcf4524611e726fea2557d46d601ce3285ed57bf6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d07835ed2af8ba093642b2d3cdf2bcbb5bda045c6821eb5b9e85eed86062b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba2a26e287eaeaf2b40803b833b44bc0510ecae085c8c014212e782322dbe48e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b759b3977dfc64448d06dab3ce1a3acd5179cf41aebba5c8001e8bbda265aa63(
    value: typing.Optional[SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee38a4265fcad3cd94a875cfe91cdbdda34067619e0331af86857fc065525f70(
    *,
    enable_online_store: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security_config: typing.Optional[typing.Union[SagemakerFeatureGroupOnlineStoreConfigSecurityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_type: typing.Optional[builtins.str] = None,
    ttl_duration: typing.Optional[typing.Union[SagemakerFeatureGroupOnlineStoreConfigTtlDuration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e465bc2b7251e530bb3eb7b175f3f18e1ecf6cee9d8a7b0a263b3adf589732(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a74eeba363b265caff78cd9277ecafb7cdb319301f34301ae0c5360998b52403(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda68a3f0423e4505dc92618099b1499323d4ca4edcb635018189402383570fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf126879ae2cefdedbdf03be7795481e816ca36f92a5637790f0015537737df(
    value: typing.Optional[SagemakerFeatureGroupOnlineStoreConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc686ddcfc2e3b1f14913382f521b738fb7b984a7539cef33008175b5c960ff(
    *,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4730cde9d9e63ec7353b59ba007e962d7ca7a1b87ce14bd65d04d3cd297f2ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d322ea30ecc45d77cc90d3c4ed0f7fbc1b3fa7b5423734fb56744ad73613bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb6481d9b571161f96816872fe152bec1157d35db024fef078703d21bb8bb049(
    value: typing.Optional[SagemakerFeatureGroupOnlineStoreConfigSecurityConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf07da641a1e96f95283bc4a80314ef5c078127e93775ec723f3cb705cbdd761(
    *,
    unit: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1b5670a58cda1aab1aa689eb8802e4f5cd31217153a5e0bcaba7a021f047eae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e633672a168188b90ab2b63fc9f4f9fcb334959c3fdf331cca290c4cbe95055a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e2b862066ecbc49dfecc1e2b700fc3c764802e2d68f1650199fc41cb79d66e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1921c83108514508a9b7dca7c0982e8b5ce728875129fe8bd2193acd7e7fb0c(
    value: typing.Optional[SagemakerFeatureGroupOnlineStoreConfigTtlDuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f6744c5bf4df4df2b569e55a5927cd83a8277b442899c25f0df56da01368c2f(
    *,
    provisioned_read_capacity_units: typing.Optional[jsii.Number] = None,
    provisioned_write_capacity_units: typing.Optional[jsii.Number] = None,
    throughput_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d913d0096a49f057604e0c4cc4e57fb458c448967fafe446faed0ebba12cbfe2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd2c868e570665c05da033f59ecd0b8ad01b61f2fc8809125e7949ab985e3d8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff1e313b1d26714b6917ce2241eefde01c6b35a7d2c95efae313f57d28b92d9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d4b08df8a8602fccc32bb08614976189dbb4cd7382289a956f822a5404cba30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0c2e9ba4c62aadf4beb62577fa9dbd4566081950e2b99c4cc2165615e56b48(
    value: typing.Optional[SagemakerFeatureGroupThroughputConfig],
) -> None:
    """Type checking stubs"""
    pass
