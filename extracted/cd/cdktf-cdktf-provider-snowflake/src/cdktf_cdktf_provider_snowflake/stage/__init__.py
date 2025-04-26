r'''
# `snowflake_stage`

Refer to the Terraform Registry for docs: [`snowflake_stage`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage).
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


class Stage(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.stage.Stage",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage snowflake_stage}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        database: builtins.str,
        name: builtins.str,
        schema: builtins.str,
        aws_external_id: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        copy_options: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[builtins.str] = None,
        directory: typing.Optional[builtins.str] = None,
        encryption: typing.Optional[builtins.str] = None,
        file_format: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        snowflake_iam_user: typing.Optional[builtins.str] = None,
        storage_integration: typing.Optional[builtins.str] = None,
        tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StageTag", typing.Dict[builtins.str, typing.Any]]]]] = None,
        url: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage snowflake_stage} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param database: The database in which to create the stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#database Stage#database}
        :param name: Specifies the identifier for the stage; must be unique for the database and schema in which the stage is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#name Stage#name}
        :param schema: The schema in which to create the stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#schema Stage#schema}
        :param aws_external_id: A unique ID assigned to the specific stage. The ID has the following format: <snowflakeAccount>*SFCRole=<snowflakeRoleId>*<randomId> Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#aws_external_id Stage#aws_external_id}
        :param comment: Specifies a comment for the stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#comment Stage#comment}
        :param copy_options: Specifies the copy options for the stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#copy_options Stage#copy_options}
        :param credentials: Specifies the credentials for the stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#credentials Stage#credentials}
        :param directory: Specifies the directory settings for the stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#directory Stage#directory}
        :param encryption: Specifies the encryption settings for the stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#encryption Stage#encryption}
        :param file_format: Specifies the file format for the stage. Specifying the default Snowflake value (e.g. TYPE = CSV) will currently result in a permadiff (check `#2679 <https://github.com/Snowflake-Labs/terraform-provider-snowflake/issues/2679>`_). For now, omit the default values; it will be fixed in the upcoming provider versions. Examples of usage: 1. with hardcoding value: ``file_format="FORMAT_NAME = DB.SCHEMA.FORMATNAME"`` 2. from dynamic value: ``file_format = "FORMAT_NAME = ${snowflake_file_format.myfileformat.fully_qualified_name}"`` 3. from expression: ``file_format = format("FORMAT_NAME =%s.%s.MYFILEFORMAT", var.db_name, each.value.schema_name)``. Reference: `#265 <https://github.com/Snowflake-Labs/terraform-provider-snowflake/issues/265>`_ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#file_format Stage#file_format}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#id Stage#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param snowflake_iam_user: An AWS IAM user created for your Snowflake account. This user is the same for every external S3 stage created in your account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#snowflake_iam_user Stage#snowflake_iam_user}
        :param storage_integration: Specifies the name of the storage integration used to delegate authentication responsibility for external cloud storage to a Snowflake identity and access management (IAM) entity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#storage_integration Stage#storage_integration}
        :param tag: tag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#tag Stage#tag}
        :param url: Specifies the URL for the stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#url Stage#url}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__025c4985fd039422518086ad481eb8d0db0de27de22ebbf9742881cf337be234)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = StageConfig(
            database=database,
            name=name,
            schema=schema,
            aws_external_id=aws_external_id,
            comment=comment,
            copy_options=copy_options,
            credentials=credentials,
            directory=directory,
            encryption=encryption,
            file_format=file_format,
            id=id,
            snowflake_iam_user=snowflake_iam_user,
            storage_integration=storage_integration,
            tag=tag,
            url=url,
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
        '''Generates CDKTF code for importing a Stage resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Stage to import.
        :param import_from_id: The id of the existing Stage that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Stage to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1e3b6b11c5ad9e6303ba7a05c241481593d358395ba505adb73ec93c9a092aa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTag")
    def put_tag(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StageTag", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd2b3ec2e26bef4b9fa94c2b3be89bbabcaa039d816a5f462baa46ac05f09b93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTag", [value]))

    @jsii.member(jsii_name="resetAwsExternalId")
    def reset_aws_external_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsExternalId", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetCopyOptions")
    def reset_copy_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyOptions", []))

    @jsii.member(jsii_name="resetCredentials")
    def reset_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentials", []))

    @jsii.member(jsii_name="resetDirectory")
    def reset_directory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirectory", []))

    @jsii.member(jsii_name="resetEncryption")
    def reset_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryption", []))

    @jsii.member(jsii_name="resetFileFormat")
    def reset_file_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileFormat", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSnowflakeIamUser")
    def reset_snowflake_iam_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnowflakeIamUser", []))

    @jsii.member(jsii_name="resetStorageIntegration")
    def reset_storage_integration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageIntegration", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

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
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> "StageTagList":
        return typing.cast("StageTagList", jsii.get(self, "tag"))

    @builtins.property
    @jsii.member(jsii_name="awsExternalIdInput")
    def aws_external_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsExternalIdInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="copyOptionsInput")
    def copy_options_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "copyOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialsInput")
    def credentials_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="directoryInput")
    def directory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directoryInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionInput")
    def encryption_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="fileFormatInput")
    def file_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="snowflakeIamUserInput")
    def snowflake_iam_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snowflakeIamUserInput"))

    @builtins.property
    @jsii.member(jsii_name="storageIntegrationInput")
    def storage_integration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageIntegrationInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StageTag"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StageTag"]]], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="awsExternalId")
    def aws_external_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsExternalId"))

    @aws_external_id.setter
    def aws_external_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30550c72ff262176a23dc08d13f0b2eb0253e5a55df1ab3d4b2817e021e1f665)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsExternalId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91c70c6e5481fc27f1e9ea3a4832c97b47b2f55bec74de3f5fbc088c5ff1400a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="copyOptions")
    def copy_options(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "copyOptions"))

    @copy_options.setter
    def copy_options(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cff2e4f4842826e4b994c6f471fb88c85a771b1c41c62f01ddc949cac954004)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="credentials")
    def credentials(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentials"))

    @credentials.setter
    def credentials(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8382ce101d7b4492e7f713a607a666da96e63cc9b5e91b546c12e14b9ca37067)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__874cc697b78e22fa9ea9412f5c66f24397f8b45db50abaa159784e4a1649aead)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="directory")
    def directory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "directory"))

    @directory.setter
    def directory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab608e05913f91ec6b1728c54815144c2213828a1132750848ce67a3017a9708)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "directory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryption")
    def encryption(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryption"))

    @encryption.setter
    def encryption(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9ba099e544e8e5317c8a91d56ce9d210fef4c0f62d42acc6268a6ec8f4ad0f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileFormat")
    def file_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileFormat"))

    @file_format.setter
    def file_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fb276cfddd4492009caceb790ffed6fe61370f446cb0d912969df11382b77fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac699dc255c3f8c317414fa11e58059799d864e2756c73e82e56b24da7ca41e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__498bfef39f2a39b58deb96689522e69f708e4f99d498ea7994e562ba3fbce0e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46d69a4c0b0e34029124e730322f1107b2ddcde704b09b2a435d5f3b4bf932a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snowflakeIamUser")
    def snowflake_iam_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snowflakeIamUser"))

    @snowflake_iam_user.setter
    def snowflake_iam_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6efe54198c03d682904ae3e6da3b4943027b85b3f2eb129ab8b93f6ec4654eb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snowflakeIamUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageIntegration")
    def storage_integration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageIntegration"))

    @storage_integration.setter
    def storage_integration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82094dceb7549b92569d47f41daef3bc1f6836e004a34aade153af5342306546)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageIntegration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26dd6849a22ab41e82c1336539bb04e6a6af959e9eff083b2925139dd10a500a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.stage.StageConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "database": "database",
        "name": "name",
        "schema": "schema",
        "aws_external_id": "awsExternalId",
        "comment": "comment",
        "copy_options": "copyOptions",
        "credentials": "credentials",
        "directory": "directory",
        "encryption": "encryption",
        "file_format": "fileFormat",
        "id": "id",
        "snowflake_iam_user": "snowflakeIamUser",
        "storage_integration": "storageIntegration",
        "tag": "tag",
        "url": "url",
    },
)
class StageConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        database: builtins.str,
        name: builtins.str,
        schema: builtins.str,
        aws_external_id: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        copy_options: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[builtins.str] = None,
        directory: typing.Optional[builtins.str] = None,
        encryption: typing.Optional[builtins.str] = None,
        file_format: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        snowflake_iam_user: typing.Optional[builtins.str] = None,
        storage_integration: typing.Optional[builtins.str] = None,
        tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StageTag", typing.Dict[builtins.str, typing.Any]]]]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param database: The database in which to create the stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#database Stage#database}
        :param name: Specifies the identifier for the stage; must be unique for the database and schema in which the stage is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#name Stage#name}
        :param schema: The schema in which to create the stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#schema Stage#schema}
        :param aws_external_id: A unique ID assigned to the specific stage. The ID has the following format: <snowflakeAccount>*SFCRole=<snowflakeRoleId>*<randomId> Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#aws_external_id Stage#aws_external_id}
        :param comment: Specifies a comment for the stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#comment Stage#comment}
        :param copy_options: Specifies the copy options for the stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#copy_options Stage#copy_options}
        :param credentials: Specifies the credentials for the stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#credentials Stage#credentials}
        :param directory: Specifies the directory settings for the stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#directory Stage#directory}
        :param encryption: Specifies the encryption settings for the stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#encryption Stage#encryption}
        :param file_format: Specifies the file format for the stage. Specifying the default Snowflake value (e.g. TYPE = CSV) will currently result in a permadiff (check `#2679 <https://github.com/Snowflake-Labs/terraform-provider-snowflake/issues/2679>`_). For now, omit the default values; it will be fixed in the upcoming provider versions. Examples of usage: 1. with hardcoding value: ``file_format="FORMAT_NAME = DB.SCHEMA.FORMATNAME"`` 2. from dynamic value: ``file_format = "FORMAT_NAME = ${snowflake_file_format.myfileformat.fully_qualified_name}"`` 3. from expression: ``file_format = format("FORMAT_NAME =%s.%s.MYFILEFORMAT", var.db_name, each.value.schema_name)``. Reference: `#265 <https://github.com/Snowflake-Labs/terraform-provider-snowflake/issues/265>`_ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#file_format Stage#file_format}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#id Stage#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param snowflake_iam_user: An AWS IAM user created for your Snowflake account. This user is the same for every external S3 stage created in your account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#snowflake_iam_user Stage#snowflake_iam_user}
        :param storage_integration: Specifies the name of the storage integration used to delegate authentication responsibility for external cloud storage to a Snowflake identity and access management (IAM) entity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#storage_integration Stage#storage_integration}
        :param tag: tag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#tag Stage#tag}
        :param url: Specifies the URL for the stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#url Stage#url}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47afda064353a35c21e0d797c466775a551709033505444fa172964f40eb432e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument aws_external_id", value=aws_external_id, expected_type=type_hints["aws_external_id"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument copy_options", value=copy_options, expected_type=type_hints["copy_options"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument directory", value=directory, expected_type=type_hints["directory"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument file_format", value=file_format, expected_type=type_hints["file_format"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument snowflake_iam_user", value=snowflake_iam_user, expected_type=type_hints["snowflake_iam_user"])
            check_type(argname="argument storage_integration", value=storage_integration, expected_type=type_hints["storage_integration"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "name": name,
            "schema": schema,
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
        if aws_external_id is not None:
            self._values["aws_external_id"] = aws_external_id
        if comment is not None:
            self._values["comment"] = comment
        if copy_options is not None:
            self._values["copy_options"] = copy_options
        if credentials is not None:
            self._values["credentials"] = credentials
        if directory is not None:
            self._values["directory"] = directory
        if encryption is not None:
            self._values["encryption"] = encryption
        if file_format is not None:
            self._values["file_format"] = file_format
        if id is not None:
            self._values["id"] = id
        if snowflake_iam_user is not None:
            self._values["snowflake_iam_user"] = snowflake_iam_user
        if storage_integration is not None:
            self._values["storage_integration"] = storage_integration
        if tag is not None:
            self._values["tag"] = tag
        if url is not None:
            self._values["url"] = url

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
    def database(self) -> builtins.str:
        '''The database in which to create the stage.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#database Stage#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the identifier for the stage;

        must be unique for the database and schema in which the stage is created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#name Stage#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> builtins.str:
        '''The schema in which to create the stage.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#schema Stage#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_external_id(self) -> typing.Optional[builtins.str]:
        '''A unique ID assigned to the specific stage. The ID has the following format: <snowflakeAccount>*SFCRole=<snowflakeRoleId>*<randomId>

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#aws_external_id Stage#aws_external_id}
        '''
        result = self._values.get("aws_external_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the stage.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#comment Stage#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def copy_options(self) -> typing.Optional[builtins.str]:
        '''Specifies the copy options for the stage.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#copy_options Stage#copy_options}
        '''
        result = self._values.get("copy_options")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def credentials(self) -> typing.Optional[builtins.str]:
        '''Specifies the credentials for the stage.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#credentials Stage#credentials}
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def directory(self) -> typing.Optional[builtins.str]:
        '''Specifies the directory settings for the stage.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#directory Stage#directory}
        '''
        result = self._values.get("directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption(self) -> typing.Optional[builtins.str]:
        '''Specifies the encryption settings for the stage.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#encryption Stage#encryption}
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the file format for the stage.

        Specifying the default Snowflake value (e.g. TYPE = CSV) will currently result in a permadiff (check `#2679 <https://github.com/Snowflake-Labs/terraform-provider-snowflake/issues/2679>`_). For now, omit the default values; it will be fixed in the upcoming provider versions. Examples of usage: 1. with hardcoding value: ``file_format="FORMAT_NAME = DB.SCHEMA.FORMATNAME"`` 2. from dynamic value: ``file_format = "FORMAT_NAME = ${snowflake_file_format.myfileformat.fully_qualified_name}"`` 3. from expression: ``file_format = format("FORMAT_NAME =%s.%s.MYFILEFORMAT", var.db_name, each.value.schema_name)``. Reference: `#265 <https://github.com/Snowflake-Labs/terraform-provider-snowflake/issues/265>`_

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#file_format Stage#file_format}
        '''
        result = self._values.get("file_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#id Stage#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snowflake_iam_user(self) -> typing.Optional[builtins.str]:
        '''An AWS IAM user created for your Snowflake account.

        This user is the same for every external S3 stage created in your account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#snowflake_iam_user Stage#snowflake_iam_user}
        '''
        result = self._values.get("snowflake_iam_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_integration(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the storage integration used to delegate authentication responsibility for external cloud storage to a Snowflake identity and access management (IAM) entity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#storage_integration Stage#storage_integration}
        '''
        result = self._values.get("storage_integration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StageTag"]]]:
        '''tag block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#tag Stage#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StageTag"]]], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''Specifies the URL for the stage.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#url Stage#url}
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.stage.StageTag",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "value": "value",
        "database": "database",
        "schema": "schema",
    },
)
class StageTag:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: builtins.str,
        database: typing.Optional[builtins.str] = None,
        schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Tag name, e.g. department. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#name Stage#name}
        :param value: Tag value, e.g. marketing_info. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#value Stage#value}
        :param database: Name of the database that the tag was created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#database Stage#database}
        :param schema: Name of the schema that the tag was created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#schema Stage#schema}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b37b96ab2079a51de572f8ea1d80e14e16c3b959b12a50edc76bc0fa28f6fac0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }
        if database is not None:
            self._values["database"] = database
        if schema is not None:
            self._values["schema"] = schema

    @builtins.property
    def name(self) -> builtins.str:
        '''Tag name, e.g. department.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#name Stage#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Tag value, e.g. marketing_info.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#value Stage#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database(self) -> typing.Optional[builtins.str]:
        '''Name of the database that the tag was created in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#database Stage#database}
        '''
        result = self._values.get("database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema(self) -> typing.Optional[builtins.str]:
        '''Name of the schema that the tag was created in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stage#schema Stage#schema}
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StageTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StageTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.stage.StageTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ce642f1a5954c5f8d118eaf57f6ef23d4b22c156a75eb88c9dd076898ad6029)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "StageTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f84e5e36cba7be8c8d08ac22f35b47416772e752accb82fc0bcccb41137993d4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StageTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2416b606bed8ad530722aa667368efed24166034a79c93331f24e378d0823a05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4edbc6aba3b87ed1392615b3c5a32b393a9d965fed626e8e1858a61492b2048e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de51876fc395eda286c778825ab5cd196680d1fc279ba71cdf6065fecb7d6ff3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StageTag]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StageTag]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StageTag]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__873a81832c04baba98825133906fdf688d8620f93fe698366227307203a3a8c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StageTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.stage.StageTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffbcf6b2d2b96a11cf30ffb3350eccc3019c21d77de8906f187a7eec35a88fc2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDatabase")
    def reset_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabase", []))

    @jsii.member(jsii_name="resetSchema")
    def reset_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchema", []))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2046c77c2837e9c4afc7ec8b22068bbe0f4d433b76b3a7e5ee92db120a83e1dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__737806830d311742b1889342aca9ae7e22f0cc6de2096d72e4d8b5797a639846)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3816f8bfa8a5bd83ea796ed3ab86f4c91f54943965396be78ba3072e704b9fc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb8b897f2700218c95abc6a729596c221d2d072c7a18927c6c216c1e87f89ab7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StageTag]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StageTag]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StageTag]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3e123dc48fae6f206b0ffca4dfea20ec42ad0b0c3f373cce0c6866b48c6b213)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Stage",
    "StageConfig",
    "StageTag",
    "StageTagList",
    "StageTagOutputReference",
]

publication.publish()

def _typecheckingstub__025c4985fd039422518086ad481eb8d0db0de27de22ebbf9742881cf337be234(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    database: builtins.str,
    name: builtins.str,
    schema: builtins.str,
    aws_external_id: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    copy_options: typing.Optional[builtins.str] = None,
    credentials: typing.Optional[builtins.str] = None,
    directory: typing.Optional[builtins.str] = None,
    encryption: typing.Optional[builtins.str] = None,
    file_format: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    snowflake_iam_user: typing.Optional[builtins.str] = None,
    storage_integration: typing.Optional[builtins.str] = None,
    tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StageTag, typing.Dict[builtins.str, typing.Any]]]]] = None,
    url: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__a1e3b6b11c5ad9e6303ba7a05c241481593d358395ba505adb73ec93c9a092aa(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd2b3ec2e26bef4b9fa94c2b3be89bbabcaa039d816a5f462baa46ac05f09b93(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StageTag, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30550c72ff262176a23dc08d13f0b2eb0253e5a55df1ab3d4b2817e021e1f665(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91c70c6e5481fc27f1e9ea3a4832c97b47b2f55bec74de3f5fbc088c5ff1400a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cff2e4f4842826e4b994c6f471fb88c85a771b1c41c62f01ddc949cac954004(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8382ce101d7b4492e7f713a607a666da96e63cc9b5e91b546c12e14b9ca37067(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__874cc697b78e22fa9ea9412f5c66f24397f8b45db50abaa159784e4a1649aead(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab608e05913f91ec6b1728c54815144c2213828a1132750848ce67a3017a9708(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9ba099e544e8e5317c8a91d56ce9d210fef4c0f62d42acc6268a6ec8f4ad0f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fb276cfddd4492009caceb790ffed6fe61370f446cb0d912969df11382b77fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac699dc255c3f8c317414fa11e58059799d864e2756c73e82e56b24da7ca41e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__498bfef39f2a39b58deb96689522e69f708e4f99d498ea7994e562ba3fbce0e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d69a4c0b0e34029124e730322f1107b2ddcde704b09b2a435d5f3b4bf932a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6efe54198c03d682904ae3e6da3b4943027b85b3f2eb129ab8b93f6ec4654eb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82094dceb7549b92569d47f41daef3bc1f6836e004a34aade153af5342306546(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26dd6849a22ab41e82c1336539bb04e6a6af959e9eff083b2925139dd10a500a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47afda064353a35c21e0d797c466775a551709033505444fa172964f40eb432e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    database: builtins.str,
    name: builtins.str,
    schema: builtins.str,
    aws_external_id: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    copy_options: typing.Optional[builtins.str] = None,
    credentials: typing.Optional[builtins.str] = None,
    directory: typing.Optional[builtins.str] = None,
    encryption: typing.Optional[builtins.str] = None,
    file_format: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    snowflake_iam_user: typing.Optional[builtins.str] = None,
    storage_integration: typing.Optional[builtins.str] = None,
    tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StageTag, typing.Dict[builtins.str, typing.Any]]]]] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b37b96ab2079a51de572f8ea1d80e14e16c3b959b12a50edc76bc0fa28f6fac0(
    *,
    name: builtins.str,
    value: builtins.str,
    database: typing.Optional[builtins.str] = None,
    schema: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ce642f1a5954c5f8d118eaf57f6ef23d4b22c156a75eb88c9dd076898ad6029(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f84e5e36cba7be8c8d08ac22f35b47416772e752accb82fc0bcccb41137993d4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2416b606bed8ad530722aa667368efed24166034a79c93331f24e378d0823a05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4edbc6aba3b87ed1392615b3c5a32b393a9d965fed626e8e1858a61492b2048e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de51876fc395eda286c778825ab5cd196680d1fc279ba71cdf6065fecb7d6ff3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873a81832c04baba98825133906fdf688d8620f93fe698366227307203a3a8c8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StageTag]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffbcf6b2d2b96a11cf30ffb3350eccc3019c21d77de8906f187a7eec35a88fc2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2046c77c2837e9c4afc7ec8b22068bbe0f4d433b76b3a7e5ee92db120a83e1dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__737806830d311742b1889342aca9ae7e22f0cc6de2096d72e4d8b5797a639846(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3816f8bfa8a5bd83ea796ed3ab86f4c91f54943965396be78ba3072e704b9fc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb8b897f2700218c95abc6a729596c221d2d072c7a18927c6c216c1e87f89ab7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e123dc48fae6f206b0ffca4dfea20ec42ad0b0c3f373cce0c6866b48c6b213(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StageTag]],
) -> None:
    """Type checking stubs"""
    pass
