r'''
# `aws_kendra_index`

Refer to the Terraform Registry for docs: [`aws_kendra_index`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index).
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


class KendraIndex(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndex",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index aws_kendra_index}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        role_arn: builtins.str,
        capacity_units: typing.Optional[typing.Union["KendraIndexCapacityUnits", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        document_metadata_configuration_updates: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KendraIndexDocumentMetadataConfigurationUpdates", typing.Dict[builtins.str, typing.Any]]]]] = None,
        edition: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        server_side_encryption_configuration: typing.Optional[typing.Union["KendraIndexServerSideEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["KendraIndexTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_context_policy: typing.Optional[builtins.str] = None,
        user_group_resolution_configuration: typing.Optional[typing.Union["KendraIndexUserGroupResolutionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        user_token_configurations: typing.Optional[typing.Union["KendraIndexUserTokenConfigurations", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index aws_kendra_index} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#name KendraIndex#name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#role_arn KendraIndex#role_arn}.
        :param capacity_units: capacity_units block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#capacity_units KendraIndex#capacity_units}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#description KendraIndex#description}.
        :param document_metadata_configuration_updates: document_metadata_configuration_updates block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#document_metadata_configuration_updates KendraIndex#document_metadata_configuration_updates}
        :param edition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#edition KendraIndex#edition}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#id KendraIndex#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param server_side_encryption_configuration: server_side_encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#server_side_encryption_configuration KendraIndex#server_side_encryption_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#tags KendraIndex#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#tags_all KendraIndex#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#timeouts KendraIndex#timeouts}
        :param user_context_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#user_context_policy KendraIndex#user_context_policy}.
        :param user_group_resolution_configuration: user_group_resolution_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#user_group_resolution_configuration KendraIndex#user_group_resolution_configuration}
        :param user_token_configurations: user_token_configurations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#user_token_configurations KendraIndex#user_token_configurations}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8357299f22249368ebb8347396a3d11c587eeaa4847c7812f8051c2151222995)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = KendraIndexConfig(
            name=name,
            role_arn=role_arn,
            capacity_units=capacity_units,
            description=description,
            document_metadata_configuration_updates=document_metadata_configuration_updates,
            edition=edition,
            id=id,
            server_side_encryption_configuration=server_side_encryption_configuration,
            tags=tags,
            tags_all=tags_all,
            timeouts=timeouts,
            user_context_policy=user_context_policy,
            user_group_resolution_configuration=user_group_resolution_configuration,
            user_token_configurations=user_token_configurations,
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
        '''Generates CDKTF code for importing a KendraIndex resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the KendraIndex to import.
        :param import_from_id: The id of the existing KendraIndex that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the KendraIndex to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae752bfc668eb65172863cc0bcaa7a3895c6c591ea4ffd25d6c546dfe949b876)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCapacityUnits")
    def put_capacity_units(
        self,
        *,
        query_capacity_units: typing.Optional[jsii.Number] = None,
        storage_capacity_units: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param query_capacity_units: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#query_capacity_units KendraIndex#query_capacity_units}.
        :param storage_capacity_units: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#storage_capacity_units KendraIndex#storage_capacity_units}.
        '''
        value = KendraIndexCapacityUnits(
            query_capacity_units=query_capacity_units,
            storage_capacity_units=storage_capacity_units,
        )

        return typing.cast(None, jsii.invoke(self, "putCapacityUnits", [value]))

    @jsii.member(jsii_name="putDocumentMetadataConfigurationUpdates")
    def put_document_metadata_configuration_updates(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KendraIndexDocumentMetadataConfigurationUpdates", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58196ae8abf03314b2fd454586dda8a70e5da916081cf74ab09237eae74eb07b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDocumentMetadataConfigurationUpdates", [value]))

    @jsii.member(jsii_name="putServerSideEncryptionConfiguration")
    def put_server_side_encryption_configuration(
        self,
        *,
        kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#kms_key_id KendraIndex#kms_key_id}.
        '''
        value = KendraIndexServerSideEncryptionConfiguration(kms_key_id=kms_key_id)

        return typing.cast(None, jsii.invoke(self, "putServerSideEncryptionConfiguration", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#create KendraIndex#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#delete KendraIndex#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#update KendraIndex#update}.
        '''
        value = KendraIndexTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUserGroupResolutionConfiguration")
    def put_user_group_resolution_configuration(
        self,
        *,
        user_group_resolution_mode: builtins.str,
    ) -> None:
        '''
        :param user_group_resolution_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#user_group_resolution_mode KendraIndex#user_group_resolution_mode}.
        '''
        value = KendraIndexUserGroupResolutionConfiguration(
            user_group_resolution_mode=user_group_resolution_mode
        )

        return typing.cast(None, jsii.invoke(self, "putUserGroupResolutionConfiguration", [value]))

    @jsii.member(jsii_name="putUserTokenConfigurations")
    def put_user_token_configurations(
        self,
        *,
        json_token_type_configuration: typing.Optional[typing.Union["KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        jwt_token_type_configuration: typing.Optional[typing.Union["KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param json_token_type_configuration: json_token_type_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#json_token_type_configuration KendraIndex#json_token_type_configuration}
        :param jwt_token_type_configuration: jwt_token_type_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#jwt_token_type_configuration KendraIndex#jwt_token_type_configuration}
        '''
        value = KendraIndexUserTokenConfigurations(
            json_token_type_configuration=json_token_type_configuration,
            jwt_token_type_configuration=jwt_token_type_configuration,
        )

        return typing.cast(None, jsii.invoke(self, "putUserTokenConfigurations", [value]))

    @jsii.member(jsii_name="resetCapacityUnits")
    def reset_capacity_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapacityUnits", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDocumentMetadataConfigurationUpdates")
    def reset_document_metadata_configuration_updates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentMetadataConfigurationUpdates", []))

    @jsii.member(jsii_name="resetEdition")
    def reset_edition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdition", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetServerSideEncryptionConfiguration")
    def reset_server_side_encryption_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerSideEncryptionConfiguration", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUserContextPolicy")
    def reset_user_context_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserContextPolicy", []))

    @jsii.member(jsii_name="resetUserGroupResolutionConfiguration")
    def reset_user_group_resolution_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserGroupResolutionConfiguration", []))

    @jsii.member(jsii_name="resetUserTokenConfigurations")
    def reset_user_token_configurations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserTokenConfigurations", []))

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
    @jsii.member(jsii_name="capacityUnits")
    def capacity_units(self) -> "KendraIndexCapacityUnitsOutputReference":
        return typing.cast("KendraIndexCapacityUnitsOutputReference", jsii.get(self, "capacityUnits"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="documentMetadataConfigurationUpdates")
    def document_metadata_configuration_updates(
        self,
    ) -> "KendraIndexDocumentMetadataConfigurationUpdatesList":
        return typing.cast("KendraIndexDocumentMetadataConfigurationUpdatesList", jsii.get(self, "documentMetadataConfigurationUpdates"))

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="indexStatistics")
    def index_statistics(self) -> "KendraIndexIndexStatisticsList":
        return typing.cast("KendraIndexIndexStatisticsList", jsii.get(self, "indexStatistics"))

    @builtins.property
    @jsii.member(jsii_name="serverSideEncryptionConfiguration")
    def server_side_encryption_configuration(
        self,
    ) -> "KendraIndexServerSideEncryptionConfigurationOutputReference":
        return typing.cast("KendraIndexServerSideEncryptionConfigurationOutputReference", jsii.get(self, "serverSideEncryptionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "KendraIndexTimeoutsOutputReference":
        return typing.cast("KendraIndexTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="userGroupResolutionConfiguration")
    def user_group_resolution_configuration(
        self,
    ) -> "KendraIndexUserGroupResolutionConfigurationOutputReference":
        return typing.cast("KendraIndexUserGroupResolutionConfigurationOutputReference", jsii.get(self, "userGroupResolutionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="userTokenConfigurations")
    def user_token_configurations(
        self,
    ) -> "KendraIndexUserTokenConfigurationsOutputReference":
        return typing.cast("KendraIndexUserTokenConfigurationsOutputReference", jsii.get(self, "userTokenConfigurations"))

    @builtins.property
    @jsii.member(jsii_name="capacityUnitsInput")
    def capacity_units_input(self) -> typing.Optional["KendraIndexCapacityUnits"]:
        return typing.cast(typing.Optional["KendraIndexCapacityUnits"], jsii.get(self, "capacityUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="documentMetadataConfigurationUpdatesInput")
    def document_metadata_configuration_updates_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KendraIndexDocumentMetadataConfigurationUpdates"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KendraIndexDocumentMetadataConfigurationUpdates"]]], jsii.get(self, "documentMetadataConfigurationUpdatesInput"))

    @builtins.property
    @jsii.member(jsii_name="editionInput")
    def edition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "editionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="serverSideEncryptionConfigurationInput")
    def server_side_encryption_configuration_input(
        self,
    ) -> typing.Optional["KendraIndexServerSideEncryptionConfiguration"]:
        return typing.cast(typing.Optional["KendraIndexServerSideEncryptionConfiguration"], jsii.get(self, "serverSideEncryptionConfigurationInput"))

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
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KendraIndexTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KendraIndexTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userContextPolicyInput")
    def user_context_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userContextPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="userGroupResolutionConfigurationInput")
    def user_group_resolution_configuration_input(
        self,
    ) -> typing.Optional["KendraIndexUserGroupResolutionConfiguration"]:
        return typing.cast(typing.Optional["KendraIndexUserGroupResolutionConfiguration"], jsii.get(self, "userGroupResolutionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="userTokenConfigurationsInput")
    def user_token_configurations_input(
        self,
    ) -> typing.Optional["KendraIndexUserTokenConfigurations"]:
        return typing.cast(typing.Optional["KendraIndexUserTokenConfigurations"], jsii.get(self, "userTokenConfigurationsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__689130dbab945784ef9d26ecdfe7b2fcaec0218e9c1af8e742be3fca3bec4d53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edition")
    def edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edition"))

    @edition.setter
    def edition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e69ebb1dbcab00799de1c94a5dab5fdf2edecf8fd26d32f849d396781d612c7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16c3e94aa23faa937a068db88f3ec3568be19bc2cc0ca53172606f9e45e8f49c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54ff118b1e60a29925e3c75306e438142febce5ac5307182f46f3cb8ef9dec83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__949da671620c820590af00ef968576427d7c6ddbdb1e3103e606988d866c379e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1b405ea15f36593e991eeb5a01aa6a017bb608c392c00d28d2454cd7f742f6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65bba0df399ce2f549a74b1e582653b02ec866cb1b77500d93d27cd5eaf7d3a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userContextPolicy")
    def user_context_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userContextPolicy"))

    @user_context_policy.setter
    def user_context_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__794f24bab7867519572eb36080b27fffb5397ff0bb472c827b74ae5d47e1deb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userContextPolicy", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexCapacityUnits",
    jsii_struct_bases=[],
    name_mapping={
        "query_capacity_units": "queryCapacityUnits",
        "storage_capacity_units": "storageCapacityUnits",
    },
)
class KendraIndexCapacityUnits:
    def __init__(
        self,
        *,
        query_capacity_units: typing.Optional[jsii.Number] = None,
        storage_capacity_units: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param query_capacity_units: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#query_capacity_units KendraIndex#query_capacity_units}.
        :param storage_capacity_units: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#storage_capacity_units KendraIndex#storage_capacity_units}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b619c670ad9c2e2acabc591d3e9bd971f1bef683797373abaaa1e4f6651bfad)
            check_type(argname="argument query_capacity_units", value=query_capacity_units, expected_type=type_hints["query_capacity_units"])
            check_type(argname="argument storage_capacity_units", value=storage_capacity_units, expected_type=type_hints["storage_capacity_units"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if query_capacity_units is not None:
            self._values["query_capacity_units"] = query_capacity_units
        if storage_capacity_units is not None:
            self._values["storage_capacity_units"] = storage_capacity_units

    @builtins.property
    def query_capacity_units(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#query_capacity_units KendraIndex#query_capacity_units}.'''
        result = self._values.get("query_capacity_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_capacity_units(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#storage_capacity_units KendraIndex#storage_capacity_units}.'''
        result = self._values.get("storage_capacity_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexCapacityUnits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraIndexCapacityUnitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexCapacityUnitsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e8e342adc064db25aa8d09e37752e3aba5cc26c418b9d372be73d8d44cf071c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetQueryCapacityUnits")
    def reset_query_capacity_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryCapacityUnits", []))

    @jsii.member(jsii_name="resetStorageCapacityUnits")
    def reset_storage_capacity_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageCapacityUnits", []))

    @builtins.property
    @jsii.member(jsii_name="queryCapacityUnitsInput")
    def query_capacity_units_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "queryCapacityUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="storageCapacityUnitsInput")
    def storage_capacity_units_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "storageCapacityUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="queryCapacityUnits")
    def query_capacity_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queryCapacityUnits"))

    @query_capacity_units.setter
    def query_capacity_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a0b24dbcad6e97081333fdf3144b0cb9021a06c838c5fa1981763305536e128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryCapacityUnits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageCapacityUnits")
    def storage_capacity_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageCapacityUnits"))

    @storage_capacity_units.setter
    def storage_capacity_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6a46609fe5bb48f01df22822d3dc031ee43e672764bae3c562650a824743186)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageCapacityUnits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KendraIndexCapacityUnits]:
        return typing.cast(typing.Optional[KendraIndexCapacityUnits], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[KendraIndexCapacityUnits]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3ff27c3c8dda0a253eca4ae082aa0ab470f3006f5c21a70b2d728ad19ca5c6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexConfig",
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
        "role_arn": "roleArn",
        "capacity_units": "capacityUnits",
        "description": "description",
        "document_metadata_configuration_updates": "documentMetadataConfigurationUpdates",
        "edition": "edition",
        "id": "id",
        "server_side_encryption_configuration": "serverSideEncryptionConfiguration",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
        "user_context_policy": "userContextPolicy",
        "user_group_resolution_configuration": "userGroupResolutionConfiguration",
        "user_token_configurations": "userTokenConfigurations",
    },
)
class KendraIndexConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        role_arn: builtins.str,
        capacity_units: typing.Optional[typing.Union[KendraIndexCapacityUnits, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        document_metadata_configuration_updates: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KendraIndexDocumentMetadataConfigurationUpdates", typing.Dict[builtins.str, typing.Any]]]]] = None,
        edition: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        server_side_encryption_configuration: typing.Optional[typing.Union["KendraIndexServerSideEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["KendraIndexTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_context_policy: typing.Optional[builtins.str] = None,
        user_group_resolution_configuration: typing.Optional[typing.Union["KendraIndexUserGroupResolutionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        user_token_configurations: typing.Optional[typing.Union["KendraIndexUserTokenConfigurations", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#name KendraIndex#name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#role_arn KendraIndex#role_arn}.
        :param capacity_units: capacity_units block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#capacity_units KendraIndex#capacity_units}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#description KendraIndex#description}.
        :param document_metadata_configuration_updates: document_metadata_configuration_updates block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#document_metadata_configuration_updates KendraIndex#document_metadata_configuration_updates}
        :param edition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#edition KendraIndex#edition}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#id KendraIndex#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param server_side_encryption_configuration: server_side_encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#server_side_encryption_configuration KendraIndex#server_side_encryption_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#tags KendraIndex#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#tags_all KendraIndex#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#timeouts KendraIndex#timeouts}
        :param user_context_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#user_context_policy KendraIndex#user_context_policy}.
        :param user_group_resolution_configuration: user_group_resolution_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#user_group_resolution_configuration KendraIndex#user_group_resolution_configuration}
        :param user_token_configurations: user_token_configurations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#user_token_configurations KendraIndex#user_token_configurations}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(capacity_units, dict):
            capacity_units = KendraIndexCapacityUnits(**capacity_units)
        if isinstance(server_side_encryption_configuration, dict):
            server_side_encryption_configuration = KendraIndexServerSideEncryptionConfiguration(**server_side_encryption_configuration)
        if isinstance(timeouts, dict):
            timeouts = KendraIndexTimeouts(**timeouts)
        if isinstance(user_group_resolution_configuration, dict):
            user_group_resolution_configuration = KendraIndexUserGroupResolutionConfiguration(**user_group_resolution_configuration)
        if isinstance(user_token_configurations, dict):
            user_token_configurations = KendraIndexUserTokenConfigurations(**user_token_configurations)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1000b1a8ccebad4f01aa0fc6dd2d189e6c7952e0ae95a05cca8ce5bfbc4f7c5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument capacity_units", value=capacity_units, expected_type=type_hints["capacity_units"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument document_metadata_configuration_updates", value=document_metadata_configuration_updates, expected_type=type_hints["document_metadata_configuration_updates"])
            check_type(argname="argument edition", value=edition, expected_type=type_hints["edition"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument server_side_encryption_configuration", value=server_side_encryption_configuration, expected_type=type_hints["server_side_encryption_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument user_context_policy", value=user_context_policy, expected_type=type_hints["user_context_policy"])
            check_type(argname="argument user_group_resolution_configuration", value=user_group_resolution_configuration, expected_type=type_hints["user_group_resolution_configuration"])
            check_type(argname="argument user_token_configurations", value=user_token_configurations, expected_type=type_hints["user_token_configurations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
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
        if capacity_units is not None:
            self._values["capacity_units"] = capacity_units
        if description is not None:
            self._values["description"] = description
        if document_metadata_configuration_updates is not None:
            self._values["document_metadata_configuration_updates"] = document_metadata_configuration_updates
        if edition is not None:
            self._values["edition"] = edition
        if id is not None:
            self._values["id"] = id
        if server_side_encryption_configuration is not None:
            self._values["server_side_encryption_configuration"] = server_side_encryption_configuration
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if user_context_policy is not None:
            self._values["user_context_policy"] = user_context_policy
        if user_group_resolution_configuration is not None:
            self._values["user_group_resolution_configuration"] = user_group_resolution_configuration
        if user_token_configurations is not None:
            self._values["user_token_configurations"] = user_token_configurations

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#name KendraIndex#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#role_arn KendraIndex#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def capacity_units(self) -> typing.Optional[KendraIndexCapacityUnits]:
        '''capacity_units block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#capacity_units KendraIndex#capacity_units}
        '''
        result = self._values.get("capacity_units")
        return typing.cast(typing.Optional[KendraIndexCapacityUnits], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#description KendraIndex#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_metadata_configuration_updates(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KendraIndexDocumentMetadataConfigurationUpdates"]]]:
        '''document_metadata_configuration_updates block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#document_metadata_configuration_updates KendraIndex#document_metadata_configuration_updates}
        '''
        result = self._values.get("document_metadata_configuration_updates")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KendraIndexDocumentMetadataConfigurationUpdates"]]], result)

    @builtins.property
    def edition(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#edition KendraIndex#edition}.'''
        result = self._values.get("edition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#id KendraIndex#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_side_encryption_configuration(
        self,
    ) -> typing.Optional["KendraIndexServerSideEncryptionConfiguration"]:
        '''server_side_encryption_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#server_side_encryption_configuration KendraIndex#server_side_encryption_configuration}
        '''
        result = self._values.get("server_side_encryption_configuration")
        return typing.cast(typing.Optional["KendraIndexServerSideEncryptionConfiguration"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#tags KendraIndex#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#tags_all KendraIndex#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["KendraIndexTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#timeouts KendraIndex#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["KendraIndexTimeouts"], result)

    @builtins.property
    def user_context_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#user_context_policy KendraIndex#user_context_policy}.'''
        result = self._values.get("user_context_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_group_resolution_configuration(
        self,
    ) -> typing.Optional["KendraIndexUserGroupResolutionConfiguration"]:
        '''user_group_resolution_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#user_group_resolution_configuration KendraIndex#user_group_resolution_configuration}
        '''
        result = self._values.get("user_group_resolution_configuration")
        return typing.cast(typing.Optional["KendraIndexUserGroupResolutionConfiguration"], result)

    @builtins.property
    def user_token_configurations(
        self,
    ) -> typing.Optional["KendraIndexUserTokenConfigurations"]:
        '''user_token_configurations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#user_token_configurations KendraIndex#user_token_configurations}
        '''
        result = self._values.get("user_token_configurations")
        return typing.cast(typing.Optional["KendraIndexUserTokenConfigurations"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexDocumentMetadataConfigurationUpdates",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "type": "type",
        "relevance": "relevance",
        "search": "search",
    },
)
class KendraIndexDocumentMetadataConfigurationUpdates:
    def __init__(
        self,
        *,
        name: builtins.str,
        type: builtins.str,
        relevance: typing.Optional[typing.Union["KendraIndexDocumentMetadataConfigurationUpdatesRelevance", typing.Dict[builtins.str, typing.Any]]] = None,
        search: typing.Optional[typing.Union["KendraIndexDocumentMetadataConfigurationUpdatesSearch", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#name KendraIndex#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#type KendraIndex#type}.
        :param relevance: relevance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#relevance KendraIndex#relevance}
        :param search: search block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#search KendraIndex#search}
        '''
        if isinstance(relevance, dict):
            relevance = KendraIndexDocumentMetadataConfigurationUpdatesRelevance(**relevance)
        if isinstance(search, dict):
            search = KendraIndexDocumentMetadataConfigurationUpdatesSearch(**search)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe5bb0b1fa3363f1e97e38957f6a1452ab2fb2901decb58e77c0b5785625485b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument relevance", value=relevance, expected_type=type_hints["relevance"])
            check_type(argname="argument search", value=search, expected_type=type_hints["search"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }
        if relevance is not None:
            self._values["relevance"] = relevance
        if search is not None:
            self._values["search"] = search

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#name KendraIndex#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#type KendraIndex#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def relevance(
        self,
    ) -> typing.Optional["KendraIndexDocumentMetadataConfigurationUpdatesRelevance"]:
        '''relevance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#relevance KendraIndex#relevance}
        '''
        result = self._values.get("relevance")
        return typing.cast(typing.Optional["KendraIndexDocumentMetadataConfigurationUpdatesRelevance"], result)

    @builtins.property
    def search(
        self,
    ) -> typing.Optional["KendraIndexDocumentMetadataConfigurationUpdatesSearch"]:
        '''search block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#search KendraIndex#search}
        '''
        result = self._values.get("search")
        return typing.cast(typing.Optional["KendraIndexDocumentMetadataConfigurationUpdatesSearch"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexDocumentMetadataConfigurationUpdates(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraIndexDocumentMetadataConfigurationUpdatesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexDocumentMetadataConfigurationUpdatesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab28b2c1ad68fd976c06172ee430a2751c6099ad4c54548abf7c4d1ee86276ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KendraIndexDocumentMetadataConfigurationUpdatesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75b68cbd98c4d092a68f6d707954b2cb3229b41cf4161ded719ef156eb3a4f05)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KendraIndexDocumentMetadataConfigurationUpdatesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3dc0b93767a857d481ca5415f823c588365ecbce681df626c11b57e58bb67b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b96eb89d8f7da9d8453c6168514f3e42561d0d64292fc99e592dc2932c38014a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d05cc4f5b14361fe7fb92d82c0aad8e87de23427ecd48ed2f1ea77ccc5fe477a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraIndexDocumentMetadataConfigurationUpdates]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraIndexDocumentMetadataConfigurationUpdates]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraIndexDocumentMetadataConfigurationUpdates]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fb2cfa98ba886e59b517b4969b3a6ed46b2fcb9f8af31d54c95c440a46238c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraIndexDocumentMetadataConfigurationUpdatesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexDocumentMetadataConfigurationUpdatesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7955061eba11454ef60434fec990c33bd59d13fd3634f7d683bf4c67c5addf4a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRelevance")
    def put_relevance(
        self,
        *,
        duration: typing.Optional[builtins.str] = None,
        freshness: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        importance: typing.Optional[jsii.Number] = None,
        rank_order: typing.Optional[builtins.str] = None,
        values_importance_map: typing.Optional[typing.Mapping[builtins.str, jsii.Number]] = None,
    ) -> None:
        '''
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#duration KendraIndex#duration}.
        :param freshness: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#freshness KendraIndex#freshness}.
        :param importance: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#importance KendraIndex#importance}.
        :param rank_order: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#rank_order KendraIndex#rank_order}.
        :param values_importance_map: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#values_importance_map KendraIndex#values_importance_map}.
        '''
        value = KendraIndexDocumentMetadataConfigurationUpdatesRelevance(
            duration=duration,
            freshness=freshness,
            importance=importance,
            rank_order=rank_order,
            values_importance_map=values_importance_map,
        )

        return typing.cast(None, jsii.invoke(self, "putRelevance", [value]))

    @jsii.member(jsii_name="putSearch")
    def put_search(
        self,
        *,
        displayable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        facetable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        searchable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sortable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param displayable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#displayable KendraIndex#displayable}.
        :param facetable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#facetable KendraIndex#facetable}.
        :param searchable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#searchable KendraIndex#searchable}.
        :param sortable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#sortable KendraIndex#sortable}.
        '''
        value = KendraIndexDocumentMetadataConfigurationUpdatesSearch(
            displayable=displayable,
            facetable=facetable,
            searchable=searchable,
            sortable=sortable,
        )

        return typing.cast(None, jsii.invoke(self, "putSearch", [value]))

    @jsii.member(jsii_name="resetRelevance")
    def reset_relevance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRelevance", []))

    @jsii.member(jsii_name="resetSearch")
    def reset_search(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSearch", []))

    @builtins.property
    @jsii.member(jsii_name="relevance")
    def relevance(
        self,
    ) -> "KendraIndexDocumentMetadataConfigurationUpdatesRelevanceOutputReference":
        return typing.cast("KendraIndexDocumentMetadataConfigurationUpdatesRelevanceOutputReference", jsii.get(self, "relevance"))

    @builtins.property
    @jsii.member(jsii_name="search")
    def search(
        self,
    ) -> "KendraIndexDocumentMetadataConfigurationUpdatesSearchOutputReference":
        return typing.cast("KendraIndexDocumentMetadataConfigurationUpdatesSearchOutputReference", jsii.get(self, "search"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="relevanceInput")
    def relevance_input(
        self,
    ) -> typing.Optional["KendraIndexDocumentMetadataConfigurationUpdatesRelevance"]:
        return typing.cast(typing.Optional["KendraIndexDocumentMetadataConfigurationUpdatesRelevance"], jsii.get(self, "relevanceInput"))

    @builtins.property
    @jsii.member(jsii_name="searchInput")
    def search_input(
        self,
    ) -> typing.Optional["KendraIndexDocumentMetadataConfigurationUpdatesSearch"]:
        return typing.cast(typing.Optional["KendraIndexDocumentMetadataConfigurationUpdatesSearch"], jsii.get(self, "searchInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2005ec203b85b9a4a21580d7df86c73f493768bfe0853b9cba233a1a9e96a641)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa969b46a6f073b4379aa61d8990c100116efc363d932df0fc5dcd66f80b05ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraIndexDocumentMetadataConfigurationUpdates]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraIndexDocumentMetadataConfigurationUpdates]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraIndexDocumentMetadataConfigurationUpdates]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b26863a7c86e4f021043d6cd001d0ac529d4455053af05467e9f1dd9696a7404)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexDocumentMetadataConfigurationUpdatesRelevance",
    jsii_struct_bases=[],
    name_mapping={
        "duration": "duration",
        "freshness": "freshness",
        "importance": "importance",
        "rank_order": "rankOrder",
        "values_importance_map": "valuesImportanceMap",
    },
)
class KendraIndexDocumentMetadataConfigurationUpdatesRelevance:
    def __init__(
        self,
        *,
        duration: typing.Optional[builtins.str] = None,
        freshness: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        importance: typing.Optional[jsii.Number] = None,
        rank_order: typing.Optional[builtins.str] = None,
        values_importance_map: typing.Optional[typing.Mapping[builtins.str, jsii.Number]] = None,
    ) -> None:
        '''
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#duration KendraIndex#duration}.
        :param freshness: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#freshness KendraIndex#freshness}.
        :param importance: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#importance KendraIndex#importance}.
        :param rank_order: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#rank_order KendraIndex#rank_order}.
        :param values_importance_map: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#values_importance_map KendraIndex#values_importance_map}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22491698088a5fa4ab0013e57ed1ef19a98146a6128798e354d35a175cae87f4)
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument freshness", value=freshness, expected_type=type_hints["freshness"])
            check_type(argname="argument importance", value=importance, expected_type=type_hints["importance"])
            check_type(argname="argument rank_order", value=rank_order, expected_type=type_hints["rank_order"])
            check_type(argname="argument values_importance_map", value=values_importance_map, expected_type=type_hints["values_importance_map"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if duration is not None:
            self._values["duration"] = duration
        if freshness is not None:
            self._values["freshness"] = freshness
        if importance is not None:
            self._values["importance"] = importance
        if rank_order is not None:
            self._values["rank_order"] = rank_order
        if values_importance_map is not None:
            self._values["values_importance_map"] = values_importance_map

    @builtins.property
    def duration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#duration KendraIndex#duration}.'''
        result = self._values.get("duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def freshness(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#freshness KendraIndex#freshness}.'''
        result = self._values.get("freshness")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def importance(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#importance KendraIndex#importance}.'''
        result = self._values.get("importance")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rank_order(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#rank_order KendraIndex#rank_order}.'''
        result = self._values.get("rank_order")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values_importance_map(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#values_importance_map KendraIndex#values_importance_map}.'''
        result = self._values.get("values_importance_map")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexDocumentMetadataConfigurationUpdatesRelevance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraIndexDocumentMetadataConfigurationUpdatesRelevanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexDocumentMetadataConfigurationUpdatesRelevanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e46ab035eb94af8e79bd11d9814beb4b8fbf404aef9a12a2a46c52b72dd0213)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDuration")
    def reset_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDuration", []))

    @jsii.member(jsii_name="resetFreshness")
    def reset_freshness(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFreshness", []))

    @jsii.member(jsii_name="resetImportance")
    def reset_importance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImportance", []))

    @jsii.member(jsii_name="resetRankOrder")
    def reset_rank_order(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRankOrder", []))

    @jsii.member(jsii_name="resetValuesImportanceMap")
    def reset_values_importance_map(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValuesImportanceMap", []))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="freshnessInput")
    def freshness_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "freshnessInput"))

    @builtins.property
    @jsii.member(jsii_name="importanceInput")
    def importance_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "importanceInput"))

    @builtins.property
    @jsii.member(jsii_name="rankOrderInput")
    def rank_order_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rankOrderInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesImportanceMapInput")
    def values_importance_map_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, jsii.Number]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, jsii.Number]], jsii.get(self, "valuesImportanceMapInput"))

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__249d7ca1245893f88287024ce9b65155b5fecf29774484746092ca33879e7864)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="freshness")
    def freshness(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "freshness"))

    @freshness.setter
    def freshness(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c769071a1c86df5075181dbcfe0a6a1cb8a95ef513c374581cd9e7d2d480f95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "freshness", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="importance")
    def importance(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "importance"))

    @importance.setter
    def importance(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9a03ba0aa9b560dbe9094b50ece09916e51daa60ac83b7a5953d309da2ab672)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rankOrder")
    def rank_order(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rankOrder"))

    @rank_order.setter
    def rank_order(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81dab0a29bcf582fa3287ca1da239077cac45003f32444f95d5345aafc1ab879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rankOrder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="valuesImportanceMap")
    def values_importance_map(self) -> typing.Mapping[builtins.str, jsii.Number]:
        return typing.cast(typing.Mapping[builtins.str, jsii.Number], jsii.get(self, "valuesImportanceMap"))

    @values_importance_map.setter
    def values_importance_map(
        self,
        value: typing.Mapping[builtins.str, jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e5553a533b6fafbbd77998013bb16fa2fea1d557807e2edb31d90955225f56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valuesImportanceMap", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraIndexDocumentMetadataConfigurationUpdatesRelevance]:
        return typing.cast(typing.Optional[KendraIndexDocumentMetadataConfigurationUpdatesRelevance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraIndexDocumentMetadataConfigurationUpdatesRelevance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3e9982cc5c1f35719c977c2126b2ff944e74225a66fc1cf1e64fa8ada2b2081)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexDocumentMetadataConfigurationUpdatesSearch",
    jsii_struct_bases=[],
    name_mapping={
        "displayable": "displayable",
        "facetable": "facetable",
        "searchable": "searchable",
        "sortable": "sortable",
    },
)
class KendraIndexDocumentMetadataConfigurationUpdatesSearch:
    def __init__(
        self,
        *,
        displayable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        facetable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        searchable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sortable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param displayable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#displayable KendraIndex#displayable}.
        :param facetable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#facetable KendraIndex#facetable}.
        :param searchable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#searchable KendraIndex#searchable}.
        :param sortable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#sortable KendraIndex#sortable}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70a59d367aabf614ba96722f0dbf3a0a5ac459214efb5d48e231b4d54d9fc1ab)
            check_type(argname="argument displayable", value=displayable, expected_type=type_hints["displayable"])
            check_type(argname="argument facetable", value=facetable, expected_type=type_hints["facetable"])
            check_type(argname="argument searchable", value=searchable, expected_type=type_hints["searchable"])
            check_type(argname="argument sortable", value=sortable, expected_type=type_hints["sortable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if displayable is not None:
            self._values["displayable"] = displayable
        if facetable is not None:
            self._values["facetable"] = facetable
        if searchable is not None:
            self._values["searchable"] = searchable
        if sortable is not None:
            self._values["sortable"] = sortable

    @builtins.property
    def displayable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#displayable KendraIndex#displayable}.'''
        result = self._values.get("displayable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def facetable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#facetable KendraIndex#facetable}.'''
        result = self._values.get("facetable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def searchable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#searchable KendraIndex#searchable}.'''
        result = self._values.get("searchable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sortable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#sortable KendraIndex#sortable}.'''
        result = self._values.get("sortable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexDocumentMetadataConfigurationUpdatesSearch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraIndexDocumentMetadataConfigurationUpdatesSearchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexDocumentMetadataConfigurationUpdatesSearchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24a5c1ec1edaaeff1b65c94d3a82ca4629e7be18ab8b9094fc41db220dedee8c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisplayable")
    def reset_displayable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayable", []))

    @jsii.member(jsii_name="resetFacetable")
    def reset_facetable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFacetable", []))

    @jsii.member(jsii_name="resetSearchable")
    def reset_searchable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSearchable", []))

    @jsii.member(jsii_name="resetSortable")
    def reset_sortable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSortable", []))

    @builtins.property
    @jsii.member(jsii_name="displayableInput")
    def displayable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "displayableInput"))

    @builtins.property
    @jsii.member(jsii_name="facetableInput")
    def facetable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "facetableInput"))

    @builtins.property
    @jsii.member(jsii_name="searchableInput")
    def searchable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "searchableInput"))

    @builtins.property
    @jsii.member(jsii_name="sortableInput")
    def sortable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sortableInput"))

    @builtins.property
    @jsii.member(jsii_name="displayable")
    def displayable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "displayable"))

    @displayable.setter
    def displayable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01848820c95faa0b998701b1abb32b15260bef19554ec9dc5084d7fb3e6d4cc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="facetable")
    def facetable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "facetable"))

    @facetable.setter
    def facetable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d35dd690550c7a9963d60b091b5e218e8c5953c9cba3516a084665d94c475f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "facetable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="searchable")
    def searchable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "searchable"))

    @searchable.setter
    def searchable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2b875d8fa215af129f8d0b722a2affcb597ed20eb41fd9a7f06731ae101c2d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "searchable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sortable")
    def sortable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sortable"))

    @sortable.setter
    def sortable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1601e913b5b73c62b9d30f3f65fca17eb5d304f7c64c35d44f396e757a27d15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sortable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraIndexDocumentMetadataConfigurationUpdatesSearch]:
        return typing.cast(typing.Optional[KendraIndexDocumentMetadataConfigurationUpdatesSearch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraIndexDocumentMetadataConfigurationUpdatesSearch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__039c20ac82f438c93f23c48e9b2772087c848edb0ea0bfd85127d41567990863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexIndexStatistics",
    jsii_struct_bases=[],
    name_mapping={},
)
class KendraIndexIndexStatistics:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexIndexStatistics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexIndexStatisticsFaqStatistics",
    jsii_struct_bases=[],
    name_mapping={},
)
class KendraIndexIndexStatisticsFaqStatistics:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexIndexStatisticsFaqStatistics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraIndexIndexStatisticsFaqStatisticsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexIndexStatisticsFaqStatisticsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7ebc89f48c5bf584dd0079fc3b27d66f8f35fb37a116ad58fcdd8b431ed0a40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KendraIndexIndexStatisticsFaqStatisticsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07672783dbfbda216c0bb63a9d46624d3a439cdf27537cbfa45634a8ce08e5b6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KendraIndexIndexStatisticsFaqStatisticsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33559274a1040b7c6b601e8928e5a863b625f4592e9d400b2c0d0160aa66dd22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0c94daaef5b328d7024e313d4449c6d142e883abd21cf31c526b12f462df1ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebd1e1b8808989f8a25b6a2295ecb7a973201e876aace69ec67ae81e9eccc813)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class KendraIndexIndexStatisticsFaqStatisticsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexIndexStatisticsFaqStatisticsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bff2e8f4660bf8df49e5f4bbf2ee45a4cafc3af3b099f9da99f4b9bf0d02f9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="indexedQuestionAnswersCount")
    def indexed_question_answers_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "indexedQuestionAnswersCount"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraIndexIndexStatisticsFaqStatistics]:
        return typing.cast(typing.Optional[KendraIndexIndexStatisticsFaqStatistics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraIndexIndexStatisticsFaqStatistics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48297c161b2309193b29eb0d5a4b7602aaaf8eec8efa60deecd8cac19189b143)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraIndexIndexStatisticsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexIndexStatisticsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de3e60a5296f685a6757b817b0f0df1db566202ffd1d5969e8de8ddf8f7926fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "KendraIndexIndexStatisticsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5049bee2ff137b77f36e704a062311ad331d5e37e2c96724c9922fff9fd333a3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KendraIndexIndexStatisticsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e816ce94419ac0663c4d817c5ec210b30834d93115bd2f98ab29c6e7437230d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__33ea733e87154c091cf5324dfed00af1830067176b1507256731e74196f559ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7eed4d858e14e8a8ce09180ad3672ad4feda56678214c74091a9676d00ff30a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class KendraIndexIndexStatisticsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexIndexStatisticsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bbdf5b5b5dcdd7c5384b31ab91bdb81ea5b849b2df4744e3a533c6e607f36a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="faqStatistics")
    def faq_statistics(self) -> KendraIndexIndexStatisticsFaqStatisticsList:
        return typing.cast(KendraIndexIndexStatisticsFaqStatisticsList, jsii.get(self, "faqStatistics"))

    @builtins.property
    @jsii.member(jsii_name="textDocumentStatistics")
    def text_document_statistics(
        self,
    ) -> "KendraIndexIndexStatisticsTextDocumentStatisticsList":
        return typing.cast("KendraIndexIndexStatisticsTextDocumentStatisticsList", jsii.get(self, "textDocumentStatistics"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KendraIndexIndexStatistics]:
        return typing.cast(typing.Optional[KendraIndexIndexStatistics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraIndexIndexStatistics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dc4b540a1a972c9da6d88882141c37809ebe3d7de60f43a78b1784cf93cc434)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexIndexStatisticsTextDocumentStatistics",
    jsii_struct_bases=[],
    name_mapping={},
)
class KendraIndexIndexStatisticsTextDocumentStatistics:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexIndexStatisticsTextDocumentStatistics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraIndexIndexStatisticsTextDocumentStatisticsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexIndexStatisticsTextDocumentStatisticsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ce120e488f322bce2791287a1302af8a5ef988af08a3bd3636f5b81125fbe6c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KendraIndexIndexStatisticsTextDocumentStatisticsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86ea46fcf791eb9c7031d04b9a011e1a02b319f924e86abc606bbf6e3e332732)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KendraIndexIndexStatisticsTextDocumentStatisticsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad547f8bd9927155525651ec193ddc2e726a15ab9aaf04e589439170308b0b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b58cc15273a2f6fbea24c83dddaed19c676ac66e931e2037e0718b3f41052aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98121192345cee97b9ad3f3e6dc3b04d047a14dfe06e40d8b72b5a98744aeed0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class KendraIndexIndexStatisticsTextDocumentStatisticsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexIndexStatisticsTextDocumentStatisticsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e520a3d6f0f357b3e29e1d7412d379de7e09d9f7d9eb84e51078c07be192ec2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="indexedTextBytes")
    def indexed_text_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "indexedTextBytes"))

    @builtins.property
    @jsii.member(jsii_name="indexedTextDocumentsCount")
    def indexed_text_documents_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "indexedTextDocumentsCount"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraIndexIndexStatisticsTextDocumentStatistics]:
        return typing.cast(typing.Optional[KendraIndexIndexStatisticsTextDocumentStatistics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraIndexIndexStatisticsTextDocumentStatistics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b78c1fafad49ee0dda81ce6415bc498ca9a1ad1025fd43b899244873321c17f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexServerSideEncryptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"kms_key_id": "kmsKeyId"},
)
class KendraIndexServerSideEncryptionConfiguration:
    def __init__(self, *, kms_key_id: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#kms_key_id KendraIndex#kms_key_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__437080790511b646aea1dc32e8c8369912a8ccf5ce5831526124b3cf86d18a34)
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#kms_key_id KendraIndex#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexServerSideEncryptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraIndexServerSideEncryptionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexServerSideEncryptionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff30dadaf14b530eed0a235ff72b696b65033763f675e7b6b3b3d53c6fd877bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebd381efc27453b191c5801623147fb00bca5364f239979aca80f70ad4d1c371)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraIndexServerSideEncryptionConfiguration]:
        return typing.cast(typing.Optional[KendraIndexServerSideEncryptionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraIndexServerSideEncryptionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a2f4b0ef6ccb07112a31ca99a9a65c1a8cde66ab845530bc0705b2c263ec6ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class KendraIndexTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#create KendraIndex#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#delete KendraIndex#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#update KendraIndex#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99851d73bc44f3bc4038cca58891226ee7271f99c6f9593d008c03269eb0b984)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#create KendraIndex#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#delete KendraIndex#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#update KendraIndex#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraIndexTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6a24918474cb9451e6cac1255336a8a2ef2a073b574a9736f3a3ea8eca986b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b151ba59f0f529b5d50bf450c5d1fe691e07ba2a64d837e8f8cdc64b0f65e908)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79658f9a7c4983f6f00c74eb03213ac6c629b4c189f56065ba22878e965fda3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3338cdc383cf980a4c44e6810d7798f2d9a5c41362011b6f1c0d1f2ca4db30a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraIndexTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraIndexTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraIndexTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ba5e1af7719ee2cc0a5cd9cfd08dbb5a1193ef23af18700b6099a2f33830750)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexUserGroupResolutionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"user_group_resolution_mode": "userGroupResolutionMode"},
)
class KendraIndexUserGroupResolutionConfiguration:
    def __init__(self, *, user_group_resolution_mode: builtins.str) -> None:
        '''
        :param user_group_resolution_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#user_group_resolution_mode KendraIndex#user_group_resolution_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29a0318fee6074834e4d4e95594b77f197500ab93e909178363202cdff7c9564)
            check_type(argname="argument user_group_resolution_mode", value=user_group_resolution_mode, expected_type=type_hints["user_group_resolution_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_group_resolution_mode": user_group_resolution_mode,
        }

    @builtins.property
    def user_group_resolution_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#user_group_resolution_mode KendraIndex#user_group_resolution_mode}.'''
        result = self._values.get("user_group_resolution_mode")
        assert result is not None, "Required property 'user_group_resolution_mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexUserGroupResolutionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraIndexUserGroupResolutionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexUserGroupResolutionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32096b1ce8d47c3ac76a1c3f1496988f66e0a50ab1d5447932045147994df52e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="userGroupResolutionModeInput")
    def user_group_resolution_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userGroupResolutionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="userGroupResolutionMode")
    def user_group_resolution_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userGroupResolutionMode"))

    @user_group_resolution_mode.setter
    def user_group_resolution_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5bbfb126822e2d086dd982fec68fd95b3f83100cb93d94051525d8acb153744)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userGroupResolutionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraIndexUserGroupResolutionConfiguration]:
        return typing.cast(typing.Optional[KendraIndexUserGroupResolutionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraIndexUserGroupResolutionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdf6d673cdca783c4ce3ee09e8378f6dc539ce149ced6462e3d84eef3074518f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexUserTokenConfigurations",
    jsii_struct_bases=[],
    name_mapping={
        "json_token_type_configuration": "jsonTokenTypeConfiguration",
        "jwt_token_type_configuration": "jwtTokenTypeConfiguration",
    },
)
class KendraIndexUserTokenConfigurations:
    def __init__(
        self,
        *,
        json_token_type_configuration: typing.Optional[typing.Union["KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        jwt_token_type_configuration: typing.Optional[typing.Union["KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param json_token_type_configuration: json_token_type_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#json_token_type_configuration KendraIndex#json_token_type_configuration}
        :param jwt_token_type_configuration: jwt_token_type_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#jwt_token_type_configuration KendraIndex#jwt_token_type_configuration}
        '''
        if isinstance(json_token_type_configuration, dict):
            json_token_type_configuration = KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration(**json_token_type_configuration)
        if isinstance(jwt_token_type_configuration, dict):
            jwt_token_type_configuration = KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration(**jwt_token_type_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff6de1e38f9de020f0582f7472791638a497a800b640949f6013021ce10a4c2d)
            check_type(argname="argument json_token_type_configuration", value=json_token_type_configuration, expected_type=type_hints["json_token_type_configuration"])
            check_type(argname="argument jwt_token_type_configuration", value=jwt_token_type_configuration, expected_type=type_hints["jwt_token_type_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if json_token_type_configuration is not None:
            self._values["json_token_type_configuration"] = json_token_type_configuration
        if jwt_token_type_configuration is not None:
            self._values["jwt_token_type_configuration"] = jwt_token_type_configuration

    @builtins.property
    def json_token_type_configuration(
        self,
    ) -> typing.Optional["KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration"]:
        '''json_token_type_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#json_token_type_configuration KendraIndex#json_token_type_configuration}
        '''
        result = self._values.get("json_token_type_configuration")
        return typing.cast(typing.Optional["KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration"], result)

    @builtins.property
    def jwt_token_type_configuration(
        self,
    ) -> typing.Optional["KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration"]:
        '''jwt_token_type_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#jwt_token_type_configuration KendraIndex#jwt_token_type_configuration}
        '''
        result = self._values.get("jwt_token_type_configuration")
        return typing.cast(typing.Optional["KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexUserTokenConfigurations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "group_attribute_field": "groupAttributeField",
        "user_name_attribute_field": "userNameAttributeField",
    },
)
class KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration:
    def __init__(
        self,
        *,
        group_attribute_field: builtins.str,
        user_name_attribute_field: builtins.str,
    ) -> None:
        '''
        :param group_attribute_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#group_attribute_field KendraIndex#group_attribute_field}.
        :param user_name_attribute_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#user_name_attribute_field KendraIndex#user_name_attribute_field}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f18f7f2a475216926d030fbd4a5eae87a618dd4f5a8740d083abbcb2e79fcdf)
            check_type(argname="argument group_attribute_field", value=group_attribute_field, expected_type=type_hints["group_attribute_field"])
            check_type(argname="argument user_name_attribute_field", value=user_name_attribute_field, expected_type=type_hints["user_name_attribute_field"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_attribute_field": group_attribute_field,
            "user_name_attribute_field": user_name_attribute_field,
        }

    @builtins.property
    def group_attribute_field(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#group_attribute_field KendraIndex#group_attribute_field}.'''
        result = self._values.get("group_attribute_field")
        assert result is not None, "Required property 'group_attribute_field' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_name_attribute_field(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#user_name_attribute_field KendraIndex#user_name_attribute_field}.'''
        result = self._values.get("user_name_attribute_field")
        assert result is not None, "Required property 'user_name_attribute_field' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraIndexUserTokenConfigurationsJsonTokenTypeConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexUserTokenConfigurationsJsonTokenTypeConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df46c3dcada1607ba8b3c9fdbd4225053bed62cb15859e695f11a181e1e68656)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="groupAttributeFieldInput")
    def group_attribute_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupAttributeFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="userNameAttributeFieldInput")
    def user_name_attribute_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userNameAttributeFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="groupAttributeField")
    def group_attribute_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupAttributeField"))

    @group_attribute_field.setter
    def group_attribute_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65ff8cd6a4f2758de8e84cc6bcf400c3387a224c10e6be5fad3e2ae6478748c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupAttributeField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userNameAttributeField")
    def user_name_attribute_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameAttributeField"))

    @user_name_attribute_field.setter
    def user_name_attribute_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad153aa299f53f919686ae961b6a79ef671d6914786a675c8d407f57c943c2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameAttributeField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration]:
        return typing.cast(typing.Optional[KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f35817edfc83f04ced37837a762f9b3e00739fec14e630c2b839a759141d4f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "key_location": "keyLocation",
        "claim_regex": "claimRegex",
        "group_attribute_field": "groupAttributeField",
        "issuer": "issuer",
        "secrets_manager_arn": "secretsManagerArn",
        "url": "url",
        "user_name_attribute_field": "userNameAttributeField",
    },
)
class KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration:
    def __init__(
        self,
        *,
        key_location: builtins.str,
        claim_regex: typing.Optional[builtins.str] = None,
        group_attribute_field: typing.Optional[builtins.str] = None,
        issuer: typing.Optional[builtins.str] = None,
        secrets_manager_arn: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
        user_name_attribute_field: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#key_location KendraIndex#key_location}.
        :param claim_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#claim_regex KendraIndex#claim_regex}.
        :param group_attribute_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#group_attribute_field KendraIndex#group_attribute_field}.
        :param issuer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#issuer KendraIndex#issuer}.
        :param secrets_manager_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#secrets_manager_arn KendraIndex#secrets_manager_arn}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#url KendraIndex#url}.
        :param user_name_attribute_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#user_name_attribute_field KendraIndex#user_name_attribute_field}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54dbf9577601ac61e3eb4950faeaf7407d9a3526ae97fa9b82027812da0d4e4f)
            check_type(argname="argument key_location", value=key_location, expected_type=type_hints["key_location"])
            check_type(argname="argument claim_regex", value=claim_regex, expected_type=type_hints["claim_regex"])
            check_type(argname="argument group_attribute_field", value=group_attribute_field, expected_type=type_hints["group_attribute_field"])
            check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
            check_type(argname="argument secrets_manager_arn", value=secrets_manager_arn, expected_type=type_hints["secrets_manager_arn"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument user_name_attribute_field", value=user_name_attribute_field, expected_type=type_hints["user_name_attribute_field"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_location": key_location,
        }
        if claim_regex is not None:
            self._values["claim_regex"] = claim_regex
        if group_attribute_field is not None:
            self._values["group_attribute_field"] = group_attribute_field
        if issuer is not None:
            self._values["issuer"] = issuer
        if secrets_manager_arn is not None:
            self._values["secrets_manager_arn"] = secrets_manager_arn
        if url is not None:
            self._values["url"] = url
        if user_name_attribute_field is not None:
            self._values["user_name_attribute_field"] = user_name_attribute_field

    @builtins.property
    def key_location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#key_location KendraIndex#key_location}.'''
        result = self._values.get("key_location")
        assert result is not None, "Required property 'key_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def claim_regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#claim_regex KendraIndex#claim_regex}.'''
        result = self._values.get("claim_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_attribute_field(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#group_attribute_field KendraIndex#group_attribute_field}.'''
        result = self._values.get("group_attribute_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issuer(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#issuer KendraIndex#issuer}.'''
        result = self._values.get("issuer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secrets_manager_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#secrets_manager_arn KendraIndex#secrets_manager_arn}.'''
        result = self._values.get("secrets_manager_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#url KendraIndex#url}.'''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name_attribute_field(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#user_name_attribute_field KendraIndex#user_name_attribute_field}.'''
        result = self._values.get("user_name_attribute_field")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraIndexUserTokenConfigurationsJwtTokenTypeConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexUserTokenConfigurationsJwtTokenTypeConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35cd63667ed8c5e56cbb681c8fb0bdcbf9e4b47129e3086efc78053d5042fd07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClaimRegex")
    def reset_claim_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClaimRegex", []))

    @jsii.member(jsii_name="resetGroupAttributeField")
    def reset_group_attribute_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupAttributeField", []))

    @jsii.member(jsii_name="resetIssuer")
    def reset_issuer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuer", []))

    @jsii.member(jsii_name="resetSecretsManagerArn")
    def reset_secrets_manager_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretsManagerArn", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @jsii.member(jsii_name="resetUserNameAttributeField")
    def reset_user_name_attribute_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserNameAttributeField", []))

    @builtins.property
    @jsii.member(jsii_name="claimRegexInput")
    def claim_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "claimRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="groupAttributeFieldInput")
    def group_attribute_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupAttributeFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerInput")
    def issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerInput"))

    @builtins.property
    @jsii.member(jsii_name="keyLocationInput")
    def key_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="secretsManagerArnInput")
    def secrets_manager_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretsManagerArnInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="userNameAttributeFieldInput")
    def user_name_attribute_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userNameAttributeFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="claimRegex")
    def claim_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "claimRegex"))

    @claim_regex.setter
    def claim_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e05828baf471fcf0afff3d3d88fd479ee9c2de66fbea0d613a6ad08f0d73ce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "claimRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupAttributeField")
    def group_attribute_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupAttributeField"))

    @group_attribute_field.setter
    def group_attribute_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a4db67ca77bd025728820227999f28927227a93544e0d2a76ac99b60f55bcf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupAttributeField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @issuer.setter
    def issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3291af8e4d633eb90c3bc9a6fd5ae129c89379b5e128b4e9781a2c72615cebfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyLocation")
    def key_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyLocation"))

    @key_location.setter
    def key_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea0fba5b06f7ce9e7830b1dc6b5529e13804abc651e06764095717bfea974f50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretsManagerArn")
    def secrets_manager_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretsManagerArn"))

    @secrets_manager_arn.setter
    def secrets_manager_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c032c857967053f44b6cfa213c62adbc925999b01346cc65a509b95a02b4d46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretsManagerArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b107f7f316b162df119a569c730fcd1afabb2c78244efc8d719361bd69ae14ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userNameAttributeField")
    def user_name_attribute_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameAttributeField"))

    @user_name_attribute_field.setter
    def user_name_attribute_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57246b54baa353a6df0e3b84b6cbedb3a4f13d8de69ab8366f03e25de3e746ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameAttributeField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration]:
        return typing.cast(typing.Optional[KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__380d60b27a66ad9ca2fc83a4b709330085cec159a1d17585a51eede21a36b9ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraIndexUserTokenConfigurationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraIndex.KendraIndexUserTokenConfigurationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b5a9a7221ca9abd2974932b19972d9c250925fe1caf7d57060d43230a0d4ee8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putJsonTokenTypeConfiguration")
    def put_json_token_type_configuration(
        self,
        *,
        group_attribute_field: builtins.str,
        user_name_attribute_field: builtins.str,
    ) -> None:
        '''
        :param group_attribute_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#group_attribute_field KendraIndex#group_attribute_field}.
        :param user_name_attribute_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#user_name_attribute_field KendraIndex#user_name_attribute_field}.
        '''
        value = KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration(
            group_attribute_field=group_attribute_field,
            user_name_attribute_field=user_name_attribute_field,
        )

        return typing.cast(None, jsii.invoke(self, "putJsonTokenTypeConfiguration", [value]))

    @jsii.member(jsii_name="putJwtTokenTypeConfiguration")
    def put_jwt_token_type_configuration(
        self,
        *,
        key_location: builtins.str,
        claim_regex: typing.Optional[builtins.str] = None,
        group_attribute_field: typing.Optional[builtins.str] = None,
        issuer: typing.Optional[builtins.str] = None,
        secrets_manager_arn: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
        user_name_attribute_field: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#key_location KendraIndex#key_location}.
        :param claim_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#claim_regex KendraIndex#claim_regex}.
        :param group_attribute_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#group_attribute_field KendraIndex#group_attribute_field}.
        :param issuer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#issuer KendraIndex#issuer}.
        :param secrets_manager_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#secrets_manager_arn KendraIndex#secrets_manager_arn}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#url KendraIndex#url}.
        :param user_name_attribute_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_index#user_name_attribute_field KendraIndex#user_name_attribute_field}.
        '''
        value = KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration(
            key_location=key_location,
            claim_regex=claim_regex,
            group_attribute_field=group_attribute_field,
            issuer=issuer,
            secrets_manager_arn=secrets_manager_arn,
            url=url,
            user_name_attribute_field=user_name_attribute_field,
        )

        return typing.cast(None, jsii.invoke(self, "putJwtTokenTypeConfiguration", [value]))

    @jsii.member(jsii_name="resetJsonTokenTypeConfiguration")
    def reset_json_token_type_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJsonTokenTypeConfiguration", []))

    @jsii.member(jsii_name="resetJwtTokenTypeConfiguration")
    def reset_jwt_token_type_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJwtTokenTypeConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="jsonTokenTypeConfiguration")
    def json_token_type_configuration(
        self,
    ) -> KendraIndexUserTokenConfigurationsJsonTokenTypeConfigurationOutputReference:
        return typing.cast(KendraIndexUserTokenConfigurationsJsonTokenTypeConfigurationOutputReference, jsii.get(self, "jsonTokenTypeConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="jwtTokenTypeConfiguration")
    def jwt_token_type_configuration(
        self,
    ) -> KendraIndexUserTokenConfigurationsJwtTokenTypeConfigurationOutputReference:
        return typing.cast(KendraIndexUserTokenConfigurationsJwtTokenTypeConfigurationOutputReference, jsii.get(self, "jwtTokenTypeConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="jsonTokenTypeConfigurationInput")
    def json_token_type_configuration_input(
        self,
    ) -> typing.Optional[KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration]:
        return typing.cast(typing.Optional[KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration], jsii.get(self, "jsonTokenTypeConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="jwtTokenTypeConfigurationInput")
    def jwt_token_type_configuration_input(
        self,
    ) -> typing.Optional[KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration]:
        return typing.cast(typing.Optional[KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration], jsii.get(self, "jwtTokenTypeConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KendraIndexUserTokenConfigurations]:
        return typing.cast(typing.Optional[KendraIndexUserTokenConfigurations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraIndexUserTokenConfigurations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88cddb64623efe5b35bb418aca3970ccf2ae54ffc5607dcd51e4e6acbbae38a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "KendraIndex",
    "KendraIndexCapacityUnits",
    "KendraIndexCapacityUnitsOutputReference",
    "KendraIndexConfig",
    "KendraIndexDocumentMetadataConfigurationUpdates",
    "KendraIndexDocumentMetadataConfigurationUpdatesList",
    "KendraIndexDocumentMetadataConfigurationUpdatesOutputReference",
    "KendraIndexDocumentMetadataConfigurationUpdatesRelevance",
    "KendraIndexDocumentMetadataConfigurationUpdatesRelevanceOutputReference",
    "KendraIndexDocumentMetadataConfigurationUpdatesSearch",
    "KendraIndexDocumentMetadataConfigurationUpdatesSearchOutputReference",
    "KendraIndexIndexStatistics",
    "KendraIndexIndexStatisticsFaqStatistics",
    "KendraIndexIndexStatisticsFaqStatisticsList",
    "KendraIndexIndexStatisticsFaqStatisticsOutputReference",
    "KendraIndexIndexStatisticsList",
    "KendraIndexIndexStatisticsOutputReference",
    "KendraIndexIndexStatisticsTextDocumentStatistics",
    "KendraIndexIndexStatisticsTextDocumentStatisticsList",
    "KendraIndexIndexStatisticsTextDocumentStatisticsOutputReference",
    "KendraIndexServerSideEncryptionConfiguration",
    "KendraIndexServerSideEncryptionConfigurationOutputReference",
    "KendraIndexTimeouts",
    "KendraIndexTimeoutsOutputReference",
    "KendraIndexUserGroupResolutionConfiguration",
    "KendraIndexUserGroupResolutionConfigurationOutputReference",
    "KendraIndexUserTokenConfigurations",
    "KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration",
    "KendraIndexUserTokenConfigurationsJsonTokenTypeConfigurationOutputReference",
    "KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration",
    "KendraIndexUserTokenConfigurationsJwtTokenTypeConfigurationOutputReference",
    "KendraIndexUserTokenConfigurationsOutputReference",
]

publication.publish()

def _typecheckingstub__8357299f22249368ebb8347396a3d11c587eeaa4847c7812f8051c2151222995(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    role_arn: builtins.str,
    capacity_units: typing.Optional[typing.Union[KendraIndexCapacityUnits, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    document_metadata_configuration_updates: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KendraIndexDocumentMetadataConfigurationUpdates, typing.Dict[builtins.str, typing.Any]]]]] = None,
    edition: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    server_side_encryption_configuration: typing.Optional[typing.Union[KendraIndexServerSideEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[KendraIndexTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_context_policy: typing.Optional[builtins.str] = None,
    user_group_resolution_configuration: typing.Optional[typing.Union[KendraIndexUserGroupResolutionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    user_token_configurations: typing.Optional[typing.Union[KendraIndexUserTokenConfigurations, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ae752bfc668eb65172863cc0bcaa7a3895c6c591ea4ffd25d6c546dfe949b876(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58196ae8abf03314b2fd454586dda8a70e5da916081cf74ab09237eae74eb07b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KendraIndexDocumentMetadataConfigurationUpdates, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__689130dbab945784ef9d26ecdfe7b2fcaec0218e9c1af8e742be3fca3bec4d53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e69ebb1dbcab00799de1c94a5dab5fdf2edecf8fd26d32f849d396781d612c7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c3e94aa23faa937a068db88f3ec3568be19bc2cc0ca53172606f9e45e8f49c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ff118b1e60a29925e3c75306e438142febce5ac5307182f46f3cb8ef9dec83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__949da671620c820590af00ef968576427d7c6ddbdb1e3103e606988d866c379e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1b405ea15f36593e991eeb5a01aa6a017bb608c392c00d28d2454cd7f742f6b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65bba0df399ce2f549a74b1e582653b02ec866cb1b77500d93d27cd5eaf7d3a6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__794f24bab7867519572eb36080b27fffb5397ff0bb472c827b74ae5d47e1deb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b619c670ad9c2e2acabc591d3e9bd971f1bef683797373abaaa1e4f6651bfad(
    *,
    query_capacity_units: typing.Optional[jsii.Number] = None,
    storage_capacity_units: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e8e342adc064db25aa8d09e37752e3aba5cc26c418b9d372be73d8d44cf071c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a0b24dbcad6e97081333fdf3144b0cb9021a06c838c5fa1981763305536e128(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a46609fe5bb48f01df22822d3dc031ee43e672764bae3c562650a824743186(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ff27c3c8dda0a253eca4ae082aa0ab470f3006f5c21a70b2d728ad19ca5c6a(
    value: typing.Optional[KendraIndexCapacityUnits],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1000b1a8ccebad4f01aa0fc6dd2d189e6c7952e0ae95a05cca8ce5bfbc4f7c5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    role_arn: builtins.str,
    capacity_units: typing.Optional[typing.Union[KendraIndexCapacityUnits, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    document_metadata_configuration_updates: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KendraIndexDocumentMetadataConfigurationUpdates, typing.Dict[builtins.str, typing.Any]]]]] = None,
    edition: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    server_side_encryption_configuration: typing.Optional[typing.Union[KendraIndexServerSideEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[KendraIndexTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_context_policy: typing.Optional[builtins.str] = None,
    user_group_resolution_configuration: typing.Optional[typing.Union[KendraIndexUserGroupResolutionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    user_token_configurations: typing.Optional[typing.Union[KendraIndexUserTokenConfigurations, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe5bb0b1fa3363f1e97e38957f6a1452ab2fb2901decb58e77c0b5785625485b(
    *,
    name: builtins.str,
    type: builtins.str,
    relevance: typing.Optional[typing.Union[KendraIndexDocumentMetadataConfigurationUpdatesRelevance, typing.Dict[builtins.str, typing.Any]]] = None,
    search: typing.Optional[typing.Union[KendraIndexDocumentMetadataConfigurationUpdatesSearch, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab28b2c1ad68fd976c06172ee430a2751c6099ad4c54548abf7c4d1ee86276ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b68cbd98c4d092a68f6d707954b2cb3229b41cf4161ded719ef156eb3a4f05(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3dc0b93767a857d481ca5415f823c588365ecbce681df626c11b57e58bb67b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b96eb89d8f7da9d8453c6168514f3e42561d0d64292fc99e592dc2932c38014a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d05cc4f5b14361fe7fb92d82c0aad8e87de23427ecd48ed2f1ea77ccc5fe477a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb2cfa98ba886e59b517b4969b3a6ed46b2fcb9f8af31d54c95c440a46238c7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraIndexDocumentMetadataConfigurationUpdates]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7955061eba11454ef60434fec990c33bd59d13fd3634f7d683bf4c67c5addf4a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2005ec203b85b9a4a21580d7df86c73f493768bfe0853b9cba233a1a9e96a641(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa969b46a6f073b4379aa61d8990c100116efc363d932df0fc5dcd66f80b05ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b26863a7c86e4f021043d6cd001d0ac529d4455053af05467e9f1dd9696a7404(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraIndexDocumentMetadataConfigurationUpdates]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22491698088a5fa4ab0013e57ed1ef19a98146a6128798e354d35a175cae87f4(
    *,
    duration: typing.Optional[builtins.str] = None,
    freshness: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    importance: typing.Optional[jsii.Number] = None,
    rank_order: typing.Optional[builtins.str] = None,
    values_importance_map: typing.Optional[typing.Mapping[builtins.str, jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e46ab035eb94af8e79bd11d9814beb4b8fbf404aef9a12a2a46c52b72dd0213(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__249d7ca1245893f88287024ce9b65155b5fecf29774484746092ca33879e7864(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c769071a1c86df5075181dbcfe0a6a1cb8a95ef513c374581cd9e7d2d480f95(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a03ba0aa9b560dbe9094b50ece09916e51daa60ac83b7a5953d309da2ab672(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81dab0a29bcf582fa3287ca1da239077cac45003f32444f95d5345aafc1ab879(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e5553a533b6fafbbd77998013bb16fa2fea1d557807e2edb31d90955225f56(
    value: typing.Mapping[builtins.str, jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e9982cc5c1f35719c977c2126b2ff944e74225a66fc1cf1e64fa8ada2b2081(
    value: typing.Optional[KendraIndexDocumentMetadataConfigurationUpdatesRelevance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70a59d367aabf614ba96722f0dbf3a0a5ac459214efb5d48e231b4d54d9fc1ab(
    *,
    displayable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    facetable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    searchable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sortable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a5c1ec1edaaeff1b65c94d3a82ca4629e7be18ab8b9094fc41db220dedee8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01848820c95faa0b998701b1abb32b15260bef19554ec9dc5084d7fb3e6d4cc7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d35dd690550c7a9963d60b091b5e218e8c5953c9cba3516a084665d94c475f5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2b875d8fa215af129f8d0b722a2affcb597ed20eb41fd9a7f06731ae101c2d9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1601e913b5b73c62b9d30f3f65fca17eb5d304f7c64c35d44f396e757a27d15(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__039c20ac82f438c93f23c48e9b2772087c848edb0ea0bfd85127d41567990863(
    value: typing.Optional[KendraIndexDocumentMetadataConfigurationUpdatesSearch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7ebc89f48c5bf584dd0079fc3b27d66f8f35fb37a116ad58fcdd8b431ed0a40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07672783dbfbda216c0bb63a9d46624d3a439cdf27537cbfa45634a8ce08e5b6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33559274a1040b7c6b601e8928e5a863b625f4592e9d400b2c0d0160aa66dd22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c94daaef5b328d7024e313d4449c6d142e883abd21cf31c526b12f462df1ef(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebd1e1b8808989f8a25b6a2295ecb7a973201e876aace69ec67ae81e9eccc813(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bff2e8f4660bf8df49e5f4bbf2ee45a4cafc3af3b099f9da99f4b9bf0d02f9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48297c161b2309193b29eb0d5a4b7602aaaf8eec8efa60deecd8cac19189b143(
    value: typing.Optional[KendraIndexIndexStatisticsFaqStatistics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3e60a5296f685a6757b817b0f0df1db566202ffd1d5969e8de8ddf8f7926fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5049bee2ff137b77f36e704a062311ad331d5e37e2c96724c9922fff9fd333a3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e816ce94419ac0663c4d817c5ec210b30834d93115bd2f98ab29c6e7437230d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ea733e87154c091cf5324dfed00af1830067176b1507256731e74196f559ec(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eed4d858e14e8a8ce09180ad3672ad4feda56678214c74091a9676d00ff30a6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bbdf5b5b5dcdd7c5384b31ab91bdb81ea5b849b2df4744e3a533c6e607f36a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dc4b540a1a972c9da6d88882141c37809ebe3d7de60f43a78b1784cf93cc434(
    value: typing.Optional[KendraIndexIndexStatistics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ce120e488f322bce2791287a1302af8a5ef988af08a3bd3636f5b81125fbe6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ea46fcf791eb9c7031d04b9a011e1a02b319f924e86abc606bbf6e3e332732(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad547f8bd9927155525651ec193ddc2e726a15ab9aaf04e589439170308b0b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b58cc15273a2f6fbea24c83dddaed19c676ac66e931e2037e0718b3f41052aa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98121192345cee97b9ad3f3e6dc3b04d047a14dfe06e40d8b72b5a98744aeed0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e520a3d6f0f357b3e29e1d7412d379de7e09d9f7d9eb84e51078c07be192ec2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b78c1fafad49ee0dda81ce6415bc498ca9a1ad1025fd43b899244873321c17f9(
    value: typing.Optional[KendraIndexIndexStatisticsTextDocumentStatistics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__437080790511b646aea1dc32e8c8369912a8ccf5ce5831526124b3cf86d18a34(
    *,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff30dadaf14b530eed0a235ff72b696b65033763f675e7b6b3b3d53c6fd877bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebd381efc27453b191c5801623147fb00bca5364f239979aca80f70ad4d1c371(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a2f4b0ef6ccb07112a31ca99a9a65c1a8cde66ab845530bc0705b2c263ec6ea(
    value: typing.Optional[KendraIndexServerSideEncryptionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99851d73bc44f3bc4038cca58891226ee7271f99c6f9593d008c03269eb0b984(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a24918474cb9451e6cac1255336a8a2ef2a073b574a9736f3a3ea8eca986b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b151ba59f0f529b5d50bf450c5d1fe691e07ba2a64d837e8f8cdc64b0f65e908(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79658f9a7c4983f6f00c74eb03213ac6c629b4c189f56065ba22878e965fda3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3338cdc383cf980a4c44e6810d7798f2d9a5c41362011b6f1c0d1f2ca4db30a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ba5e1af7719ee2cc0a5cd9cfd08dbb5a1193ef23af18700b6099a2f33830750(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraIndexTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29a0318fee6074834e4d4e95594b77f197500ab93e909178363202cdff7c9564(
    *,
    user_group_resolution_mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32096b1ce8d47c3ac76a1c3f1496988f66e0a50ab1d5447932045147994df52e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5bbfb126822e2d086dd982fec68fd95b3f83100cb93d94051525d8acb153744(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf6d673cdca783c4ce3ee09e8378f6dc539ce149ced6462e3d84eef3074518f(
    value: typing.Optional[KendraIndexUserGroupResolutionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff6de1e38f9de020f0582f7472791638a497a800b640949f6013021ce10a4c2d(
    *,
    json_token_type_configuration: typing.Optional[typing.Union[KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    jwt_token_type_configuration: typing.Optional[typing.Union[KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f18f7f2a475216926d030fbd4a5eae87a618dd4f5a8740d083abbcb2e79fcdf(
    *,
    group_attribute_field: builtins.str,
    user_name_attribute_field: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df46c3dcada1607ba8b3c9fdbd4225053bed62cb15859e695f11a181e1e68656(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65ff8cd6a4f2758de8e84cc6bcf400c3387a224c10e6be5fad3e2ae6478748c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad153aa299f53f919686ae961b6a79ef671d6914786a675c8d407f57c943c2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f35817edfc83f04ced37837a762f9b3e00739fec14e630c2b839a759141d4f8(
    value: typing.Optional[KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54dbf9577601ac61e3eb4950faeaf7407d9a3526ae97fa9b82027812da0d4e4f(
    *,
    key_location: builtins.str,
    claim_regex: typing.Optional[builtins.str] = None,
    group_attribute_field: typing.Optional[builtins.str] = None,
    issuer: typing.Optional[builtins.str] = None,
    secrets_manager_arn: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
    user_name_attribute_field: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35cd63667ed8c5e56cbb681c8fb0bdcbf9e4b47129e3086efc78053d5042fd07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e05828baf471fcf0afff3d3d88fd479ee9c2de66fbea0d613a6ad08f0d73ce7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a4db67ca77bd025728820227999f28927227a93544e0d2a76ac99b60f55bcf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3291af8e4d633eb90c3bc9a6fd5ae129c89379b5e128b4e9781a2c72615cebfa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea0fba5b06f7ce9e7830b1dc6b5529e13804abc651e06764095717bfea974f50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c032c857967053f44b6cfa213c62adbc925999b01346cc65a509b95a02b4d46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b107f7f316b162df119a569c730fcd1afabb2c78244efc8d719361bd69ae14ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57246b54baa353a6df0e3b84b6cbedb3a4f13d8de69ab8366f03e25de3e746ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__380d60b27a66ad9ca2fc83a4b709330085cec159a1d17585a51eede21a36b9ee(
    value: typing.Optional[KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b5a9a7221ca9abd2974932b19972d9c250925fe1caf7d57060d43230a0d4ee8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88cddb64623efe5b35bb418aca3970ccf2ae54ffc5607dcd51e4e6acbbae38a6(
    value: typing.Optional[KendraIndexUserTokenConfigurations],
) -> None:
    """Type checking stubs"""
    pass
