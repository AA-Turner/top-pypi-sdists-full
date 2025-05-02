r'''
# `aws_transfer_connector`

Refer to the Terraform Registry for docs: [`aws_transfer_connector`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector).
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


class TransferConnector(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.transferConnector.TransferConnector",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector aws_transfer_connector}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        access_role: builtins.str,
        url: builtins.str,
        as2_config: typing.Optional[typing.Union["TransferConnectorAs2Config", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        logging_role: typing.Optional[builtins.str] = None,
        security_policy_name: typing.Optional[builtins.str] = None,
        sftp_config: typing.Optional[typing.Union["TransferConnectorSftpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector aws_transfer_connector} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param access_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#access_role TransferConnector#access_role}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#url TransferConnector#url}.
        :param as2_config: as2_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#as2_config TransferConnector#as2_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#id TransferConnector#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#logging_role TransferConnector#logging_role}.
        :param security_policy_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#security_policy_name TransferConnector#security_policy_name}.
        :param sftp_config: sftp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#sftp_config TransferConnector#sftp_config}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#tags TransferConnector#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#tags_all TransferConnector#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ec6565a91f0fae136aae65a3710e64f2840d824d3d7dfdb95d7c998d55c2ff4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = TransferConnectorConfig(
            access_role=access_role,
            url=url,
            as2_config=as2_config,
            id=id,
            logging_role=logging_role,
            security_policy_name=security_policy_name,
            sftp_config=sftp_config,
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
        '''Generates CDKTF code for importing a TransferConnector resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the TransferConnector to import.
        :param import_from_id: The id of the existing TransferConnector that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the TransferConnector to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6063194d6925b6d3354417766fed7aed668078f3e567d7af65320c1d76c48f08)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAs2Config")
    def put_as2_config(
        self,
        *,
        compression: builtins.str,
        encryption_algorithm: builtins.str,
        local_profile_id: builtins.str,
        mdn_response: builtins.str,
        partner_profile_id: builtins.str,
        signing_algorithm: builtins.str,
        mdn_signing_algorithm: typing.Optional[builtins.str] = None,
        message_subject: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param compression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#compression TransferConnector#compression}.
        :param encryption_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#encryption_algorithm TransferConnector#encryption_algorithm}.
        :param local_profile_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#local_profile_id TransferConnector#local_profile_id}.
        :param mdn_response: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#mdn_response TransferConnector#mdn_response}.
        :param partner_profile_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#partner_profile_id TransferConnector#partner_profile_id}.
        :param signing_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#signing_algorithm TransferConnector#signing_algorithm}.
        :param mdn_signing_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#mdn_signing_algorithm TransferConnector#mdn_signing_algorithm}.
        :param message_subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#message_subject TransferConnector#message_subject}.
        '''
        value = TransferConnectorAs2Config(
            compression=compression,
            encryption_algorithm=encryption_algorithm,
            local_profile_id=local_profile_id,
            mdn_response=mdn_response,
            partner_profile_id=partner_profile_id,
            signing_algorithm=signing_algorithm,
            mdn_signing_algorithm=mdn_signing_algorithm,
            message_subject=message_subject,
        )

        return typing.cast(None, jsii.invoke(self, "putAs2Config", [value]))

    @jsii.member(jsii_name="putSftpConfig")
    def put_sftp_config(
        self,
        *,
        trusted_host_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_secret_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param trusted_host_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#trusted_host_keys TransferConnector#trusted_host_keys}.
        :param user_secret_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#user_secret_id TransferConnector#user_secret_id}.
        '''
        value = TransferConnectorSftpConfig(
            trusted_host_keys=trusted_host_keys, user_secret_id=user_secret_id
        )

        return typing.cast(None, jsii.invoke(self, "putSftpConfig", [value]))

    @jsii.member(jsii_name="resetAs2Config")
    def reset_as2_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAs2Config", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLoggingRole")
    def reset_logging_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingRole", []))

    @jsii.member(jsii_name="resetSecurityPolicyName")
    def reset_security_policy_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityPolicyName", []))

    @jsii.member(jsii_name="resetSftpConfig")
    def reset_sftp_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSftpConfig", []))

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
    @jsii.member(jsii_name="as2Config")
    def as2_config(self) -> "TransferConnectorAs2ConfigOutputReference":
        return typing.cast("TransferConnectorAs2ConfigOutputReference", jsii.get(self, "as2Config"))

    @builtins.property
    @jsii.member(jsii_name="connectorId")
    def connector_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorId"))

    @builtins.property
    @jsii.member(jsii_name="sftpConfig")
    def sftp_config(self) -> "TransferConnectorSftpConfigOutputReference":
        return typing.cast("TransferConnectorSftpConfigOutputReference", jsii.get(self, "sftpConfig"))

    @builtins.property
    @jsii.member(jsii_name="accessRoleInput")
    def access_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="as2ConfigInput")
    def as2_config_input(self) -> typing.Optional["TransferConnectorAs2Config"]:
        return typing.cast(typing.Optional["TransferConnectorAs2Config"], jsii.get(self, "as2ConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingRoleInput")
    def logging_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loggingRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="securityPolicyNameInput")
    def security_policy_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityPolicyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sftpConfigInput")
    def sftp_config_input(self) -> typing.Optional["TransferConnectorSftpConfig"]:
        return typing.cast(typing.Optional["TransferConnectorSftpConfig"], jsii.get(self, "sftpConfigInput"))

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
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="accessRole")
    def access_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessRole"))

    @access_role.setter
    def access_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81a32d343d5ba59c99d73633f59e661f56f942b230fe33b2ec0492f5b091c37d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8fd38b27a7f12da6a705dc02875e0bd65ea1dd09f2c6b870e3f1128d25671bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loggingRole")
    def logging_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loggingRole"))

    @logging_role.setter
    def logging_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6e9c4f4ebc41b04f91f1afd41f250ce2e358a410e08cf3cf218cbfe0c484db9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityPolicyName")
    def security_policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityPolicyName"))

    @security_policy_name.setter
    def security_policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94d9a9a87ad0a860bc65752516e72d63231620974f5b2cf91edf85fa74997f2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityPolicyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__442bfa34f4660f50d4ab3e9debbfa0bcde3db743cbd38f61a1500267303220ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d3407a9d0b534af2b82c49327c7623ba233eb51e9e75a8af6cd685c8180da73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__081bedc786f925c169005dadba9c91d6ea434ae55220e639f883f40827592fa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.transferConnector.TransferConnectorAs2Config",
    jsii_struct_bases=[],
    name_mapping={
        "compression": "compression",
        "encryption_algorithm": "encryptionAlgorithm",
        "local_profile_id": "localProfileId",
        "mdn_response": "mdnResponse",
        "partner_profile_id": "partnerProfileId",
        "signing_algorithm": "signingAlgorithm",
        "mdn_signing_algorithm": "mdnSigningAlgorithm",
        "message_subject": "messageSubject",
    },
)
class TransferConnectorAs2Config:
    def __init__(
        self,
        *,
        compression: builtins.str,
        encryption_algorithm: builtins.str,
        local_profile_id: builtins.str,
        mdn_response: builtins.str,
        partner_profile_id: builtins.str,
        signing_algorithm: builtins.str,
        mdn_signing_algorithm: typing.Optional[builtins.str] = None,
        message_subject: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param compression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#compression TransferConnector#compression}.
        :param encryption_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#encryption_algorithm TransferConnector#encryption_algorithm}.
        :param local_profile_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#local_profile_id TransferConnector#local_profile_id}.
        :param mdn_response: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#mdn_response TransferConnector#mdn_response}.
        :param partner_profile_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#partner_profile_id TransferConnector#partner_profile_id}.
        :param signing_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#signing_algorithm TransferConnector#signing_algorithm}.
        :param mdn_signing_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#mdn_signing_algorithm TransferConnector#mdn_signing_algorithm}.
        :param message_subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#message_subject TransferConnector#message_subject}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26c0f80590f8bd58e3c9c26f029020edc326448199cf237d5d92e6b01c87d8d0)
            check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
            check_type(argname="argument encryption_algorithm", value=encryption_algorithm, expected_type=type_hints["encryption_algorithm"])
            check_type(argname="argument local_profile_id", value=local_profile_id, expected_type=type_hints["local_profile_id"])
            check_type(argname="argument mdn_response", value=mdn_response, expected_type=type_hints["mdn_response"])
            check_type(argname="argument partner_profile_id", value=partner_profile_id, expected_type=type_hints["partner_profile_id"])
            check_type(argname="argument signing_algorithm", value=signing_algorithm, expected_type=type_hints["signing_algorithm"])
            check_type(argname="argument mdn_signing_algorithm", value=mdn_signing_algorithm, expected_type=type_hints["mdn_signing_algorithm"])
            check_type(argname="argument message_subject", value=message_subject, expected_type=type_hints["message_subject"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compression": compression,
            "encryption_algorithm": encryption_algorithm,
            "local_profile_id": local_profile_id,
            "mdn_response": mdn_response,
            "partner_profile_id": partner_profile_id,
            "signing_algorithm": signing_algorithm,
        }
        if mdn_signing_algorithm is not None:
            self._values["mdn_signing_algorithm"] = mdn_signing_algorithm
        if message_subject is not None:
            self._values["message_subject"] = message_subject

    @builtins.property
    def compression(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#compression TransferConnector#compression}.'''
        result = self._values.get("compression")
        assert result is not None, "Required property 'compression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_algorithm(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#encryption_algorithm TransferConnector#encryption_algorithm}.'''
        result = self._values.get("encryption_algorithm")
        assert result is not None, "Required property 'encryption_algorithm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def local_profile_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#local_profile_id TransferConnector#local_profile_id}.'''
        result = self._values.get("local_profile_id")
        assert result is not None, "Required property 'local_profile_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mdn_response(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#mdn_response TransferConnector#mdn_response}.'''
        result = self._values.get("mdn_response")
        assert result is not None, "Required property 'mdn_response' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def partner_profile_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#partner_profile_id TransferConnector#partner_profile_id}.'''
        result = self._values.get("partner_profile_id")
        assert result is not None, "Required property 'partner_profile_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signing_algorithm(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#signing_algorithm TransferConnector#signing_algorithm}.'''
        result = self._values.get("signing_algorithm")
        assert result is not None, "Required property 'signing_algorithm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mdn_signing_algorithm(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#mdn_signing_algorithm TransferConnector#mdn_signing_algorithm}.'''
        result = self._values.get("mdn_signing_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_subject(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#message_subject TransferConnector#message_subject}.'''
        result = self._values.get("message_subject")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferConnectorAs2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferConnectorAs2ConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.transferConnector.TransferConnectorAs2ConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b392b4bb616eb6da60261a31233eda1afea29fe660b77e06e20ddc3b93db16b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMdnSigningAlgorithm")
    def reset_mdn_signing_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMdnSigningAlgorithm", []))

    @jsii.member(jsii_name="resetMessageSubject")
    def reset_message_subject(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageSubject", []))

    @builtins.property
    @jsii.member(jsii_name="compressionInput")
    def compression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionAlgorithmInput")
    def encryption_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="localProfileIdInput")
    def local_profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="mdnResponseInput")
    def mdn_response_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mdnResponseInput"))

    @builtins.property
    @jsii.member(jsii_name="mdnSigningAlgorithmInput")
    def mdn_signing_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mdnSigningAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="messageSubjectInput")
    def message_subject_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageSubjectInput"))

    @builtins.property
    @jsii.member(jsii_name="partnerProfileIdInput")
    def partner_profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partnerProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="signingAlgorithmInput")
    def signing_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signingAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="compression")
    def compression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compression"))

    @compression.setter
    def compression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29c3214b93f08286330044f82612b31e88389793766f2a00b866dd184c5160e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionAlgorithm")
    def encryption_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionAlgorithm"))

    @encryption_algorithm.setter
    def encryption_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80a038e67c922f3d1dcf7d680cb8a559e01fe2ccfb427f94ed701a92964b52cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localProfileId")
    def local_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localProfileId"))

    @local_profile_id.setter
    def local_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ef5e1b8845f273ecf5d94f88615fce4b534c99466e25b2d1dc5e72a4e2ec63c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localProfileId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mdnResponse")
    def mdn_response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mdnResponse"))

    @mdn_response.setter
    def mdn_response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f363e4198b4e81a239e4800f0e465a59c6877ae45067fc80b5fe57970dca30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mdnResponse", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mdnSigningAlgorithm")
    def mdn_signing_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mdnSigningAlgorithm"))

    @mdn_signing_algorithm.setter
    def mdn_signing_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b69101f743ff34fb36520cdbe63e415b26a9bcc855e8150aa57633da2ecb030f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mdnSigningAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="messageSubject")
    def message_subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageSubject"))

    @message_subject.setter
    def message_subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b32a254db4059925e5cb7373358fe9f13465f277b3eecd6932089c6064ebb17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageSubject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partnerProfileId")
    def partner_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partnerProfileId"))

    @partner_profile_id.setter
    def partner_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9df0fd0d1cea455030fce5b85cd5198cca10ffdcdbc2975905715393fa91761d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partnerProfileId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signingAlgorithm")
    def signing_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signingAlgorithm"))

    @signing_algorithm.setter
    def signing_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ed127bd6abda7150dd41e409f4aae61568602b940281c65cebc13bdd1a1d136)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signingAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TransferConnectorAs2Config]:
        return typing.cast(typing.Optional[TransferConnectorAs2Config], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferConnectorAs2Config],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5739e72ea10000e088e207a13f3e10e17f03f8aee16827375c1d919b8ac64c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.transferConnector.TransferConnectorConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "access_role": "accessRole",
        "url": "url",
        "as2_config": "as2Config",
        "id": "id",
        "logging_role": "loggingRole",
        "security_policy_name": "securityPolicyName",
        "sftp_config": "sftpConfig",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class TransferConnectorConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        access_role: builtins.str,
        url: builtins.str,
        as2_config: typing.Optional[typing.Union[TransferConnectorAs2Config, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        logging_role: typing.Optional[builtins.str] = None,
        security_policy_name: typing.Optional[builtins.str] = None,
        sftp_config: typing.Optional[typing.Union["TransferConnectorSftpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param access_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#access_role TransferConnector#access_role}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#url TransferConnector#url}.
        :param as2_config: as2_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#as2_config TransferConnector#as2_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#id TransferConnector#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#logging_role TransferConnector#logging_role}.
        :param security_policy_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#security_policy_name TransferConnector#security_policy_name}.
        :param sftp_config: sftp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#sftp_config TransferConnector#sftp_config}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#tags TransferConnector#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#tags_all TransferConnector#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(as2_config, dict):
            as2_config = TransferConnectorAs2Config(**as2_config)
        if isinstance(sftp_config, dict):
            sftp_config = TransferConnectorSftpConfig(**sftp_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb771b25dd768720e0320cd8f19721bb55f4e97f27f1e26535fd26da45b63173)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument access_role", value=access_role, expected_type=type_hints["access_role"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument as2_config", value=as2_config, expected_type=type_hints["as2_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument logging_role", value=logging_role, expected_type=type_hints["logging_role"])
            check_type(argname="argument security_policy_name", value=security_policy_name, expected_type=type_hints["security_policy_name"])
            check_type(argname="argument sftp_config", value=sftp_config, expected_type=type_hints["sftp_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_role": access_role,
            "url": url,
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
        if as2_config is not None:
            self._values["as2_config"] = as2_config
        if id is not None:
            self._values["id"] = id
        if logging_role is not None:
            self._values["logging_role"] = logging_role
        if security_policy_name is not None:
            self._values["security_policy_name"] = security_policy_name
        if sftp_config is not None:
            self._values["sftp_config"] = sftp_config
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
    def access_role(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#access_role TransferConnector#access_role}.'''
        result = self._values.get("access_role")
        assert result is not None, "Required property 'access_role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#url TransferConnector#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def as2_config(self) -> typing.Optional[TransferConnectorAs2Config]:
        '''as2_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#as2_config TransferConnector#as2_config}
        '''
        result = self._values.get("as2_config")
        return typing.cast(typing.Optional[TransferConnectorAs2Config], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#id TransferConnector#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_role(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#logging_role TransferConnector#logging_role}.'''
        result = self._values.get("logging_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_policy_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#security_policy_name TransferConnector#security_policy_name}.'''
        result = self._values.get("security_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sftp_config(self) -> typing.Optional["TransferConnectorSftpConfig"]:
        '''sftp_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#sftp_config TransferConnector#sftp_config}
        '''
        result = self._values.get("sftp_config")
        return typing.cast(typing.Optional["TransferConnectorSftpConfig"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#tags TransferConnector#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#tags_all TransferConnector#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferConnectorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.transferConnector.TransferConnectorSftpConfig",
    jsii_struct_bases=[],
    name_mapping={
        "trusted_host_keys": "trustedHostKeys",
        "user_secret_id": "userSecretId",
    },
)
class TransferConnectorSftpConfig:
    def __init__(
        self,
        *,
        trusted_host_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_secret_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param trusted_host_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#trusted_host_keys TransferConnector#trusted_host_keys}.
        :param user_secret_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#user_secret_id TransferConnector#user_secret_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__465816d9fa093d439128cce499af83ca014d8f583001b5326212ee0d2a6a4c87)
            check_type(argname="argument trusted_host_keys", value=trusted_host_keys, expected_type=type_hints["trusted_host_keys"])
            check_type(argname="argument user_secret_id", value=user_secret_id, expected_type=type_hints["user_secret_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if trusted_host_keys is not None:
            self._values["trusted_host_keys"] = trusted_host_keys
        if user_secret_id is not None:
            self._values["user_secret_id"] = user_secret_id

    @builtins.property
    def trusted_host_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#trusted_host_keys TransferConnector#trusted_host_keys}.'''
        result = self._values.get("trusted_host_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_secret_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/transfer_connector#user_secret_id TransferConnector#user_secret_id}.'''
        result = self._values.get("user_secret_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferConnectorSftpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferConnectorSftpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.transferConnector.TransferConnectorSftpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56211b74a3c79df55bb8b0aad821aa9a8cad8c2dd9d200c4efe3bc764f55e5e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTrustedHostKeys")
    def reset_trusted_host_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedHostKeys", []))

    @jsii.member(jsii_name="resetUserSecretId")
    def reset_user_secret_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserSecretId", []))

    @builtins.property
    @jsii.member(jsii_name="trustedHostKeysInput")
    def trusted_host_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "trustedHostKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="userSecretIdInput")
    def user_secret_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userSecretIdInput"))

    @builtins.property
    @jsii.member(jsii_name="trustedHostKeys")
    def trusted_host_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "trustedHostKeys"))

    @trusted_host_keys.setter
    def trusted_host_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__499d0a91bddfbf90cb84c752b2adab32124ee5bcf3c368ad96aa52181f48fb60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustedHostKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userSecretId")
    def user_secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userSecretId"))

    @user_secret_id.setter
    def user_secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c52c8fa01e015fdd8c4ac03b4aedeab98e902fdefd2a66bafff302583759a7ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userSecretId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TransferConnectorSftpConfig]:
        return typing.cast(typing.Optional[TransferConnectorSftpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferConnectorSftpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28cef99d0d3105593f846571d22a937522b8c934271e133d27b839446ca23f00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "TransferConnector",
    "TransferConnectorAs2Config",
    "TransferConnectorAs2ConfigOutputReference",
    "TransferConnectorConfig",
    "TransferConnectorSftpConfig",
    "TransferConnectorSftpConfigOutputReference",
]

publication.publish()

def _typecheckingstub__4ec6565a91f0fae136aae65a3710e64f2840d824d3d7dfdb95d7c998d55c2ff4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    access_role: builtins.str,
    url: builtins.str,
    as2_config: typing.Optional[typing.Union[TransferConnectorAs2Config, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    logging_role: typing.Optional[builtins.str] = None,
    security_policy_name: typing.Optional[builtins.str] = None,
    sftp_config: typing.Optional[typing.Union[TransferConnectorSftpConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6063194d6925b6d3354417766fed7aed668078f3e567d7af65320c1d76c48f08(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81a32d343d5ba59c99d73633f59e661f56f942b230fe33b2ec0492f5b091c37d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8fd38b27a7f12da6a705dc02875e0bd65ea1dd09f2c6b870e3f1128d25671bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6e9c4f4ebc41b04f91f1afd41f250ce2e358a410e08cf3cf218cbfe0c484db9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d9a9a87ad0a860bc65752516e72d63231620974f5b2cf91edf85fa74997f2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__442bfa34f4660f50d4ab3e9debbfa0bcde3db743cbd38f61a1500267303220ac(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d3407a9d0b534af2b82c49327c7623ba233eb51e9e75a8af6cd685c8180da73(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081bedc786f925c169005dadba9c91d6ea434ae55220e639f883f40827592fa5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26c0f80590f8bd58e3c9c26f029020edc326448199cf237d5d92e6b01c87d8d0(
    *,
    compression: builtins.str,
    encryption_algorithm: builtins.str,
    local_profile_id: builtins.str,
    mdn_response: builtins.str,
    partner_profile_id: builtins.str,
    signing_algorithm: builtins.str,
    mdn_signing_algorithm: typing.Optional[builtins.str] = None,
    message_subject: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b392b4bb616eb6da60261a31233eda1afea29fe660b77e06e20ddc3b93db16b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c3214b93f08286330044f82612b31e88389793766f2a00b866dd184c5160e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80a038e67c922f3d1dcf7d680cb8a559e01fe2ccfb427f94ed701a92964b52cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ef5e1b8845f273ecf5d94f88615fce4b534c99466e25b2d1dc5e72a4e2ec63c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f363e4198b4e81a239e4800f0e465a59c6877ae45067fc80b5fe57970dca30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69101f743ff34fb36520cdbe63e415b26a9bcc855e8150aa57633da2ecb030f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b32a254db4059925e5cb7373358fe9f13465f277b3eecd6932089c6064ebb17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df0fd0d1cea455030fce5b85cd5198cca10ffdcdbc2975905715393fa91761d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed127bd6abda7150dd41e409f4aae61568602b940281c65cebc13bdd1a1d136(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5739e72ea10000e088e207a13f3e10e17f03f8aee16827375c1d919b8ac64c3(
    value: typing.Optional[TransferConnectorAs2Config],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb771b25dd768720e0320cd8f19721bb55f4e97f27f1e26535fd26da45b63173(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    access_role: builtins.str,
    url: builtins.str,
    as2_config: typing.Optional[typing.Union[TransferConnectorAs2Config, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    logging_role: typing.Optional[builtins.str] = None,
    security_policy_name: typing.Optional[builtins.str] = None,
    sftp_config: typing.Optional[typing.Union[TransferConnectorSftpConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__465816d9fa093d439128cce499af83ca014d8f583001b5326212ee0d2a6a4c87(
    *,
    trusted_host_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_secret_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56211b74a3c79df55bb8b0aad821aa9a8cad8c2dd9d200c4efe3bc764f55e5e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__499d0a91bddfbf90cb84c752b2adab32124ee5bcf3c368ad96aa52181f48fb60(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52c8fa01e015fdd8c4ac03b4aedeab98e902fdefd2a66bafff302583759a7ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28cef99d0d3105593f846571d22a937522b8c934271e133d27b839446ca23f00(
    value: typing.Optional[TransferConnectorSftpConfig],
) -> None:
    """Type checking stubs"""
    pass
