r'''
# `aws_quicksight_theme`

Refer to the Terraform Registry for docs: [`aws_quicksight_theme`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme).
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


class QuicksightTheme(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightTheme",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme aws_quicksight_theme}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        base_theme_id: builtins.str,
        name: builtins.str,
        theme_id: builtins.str,
        aws_account_id: typing.Optional[builtins.str] = None,
        configuration: typing.Optional[typing.Union["QuicksightThemeConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightThemePermissions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["QuicksightThemeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version_description: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme aws_quicksight_theme} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param base_theme_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#base_theme_id QuicksightTheme#base_theme_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#name QuicksightTheme#name}.
        :param theme_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#theme_id QuicksightTheme#theme_id}.
        :param aws_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#aws_account_id QuicksightTheme#aws_account_id}.
        :param configuration: configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#configuration QuicksightTheme#configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#id QuicksightTheme#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param permissions: permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#permissions QuicksightTheme#permissions}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#tags QuicksightTheme#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#tags_all QuicksightTheme#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#timeouts QuicksightTheme#timeouts}
        :param version_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#version_description QuicksightTheme#version_description}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee134fc0a32f306bbe9fa24ed642881f4e3bd778c2c0f96e71bc6f58f901d62c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = QuicksightThemeConfig(
            base_theme_id=base_theme_id,
            name=name,
            theme_id=theme_id,
            aws_account_id=aws_account_id,
            configuration=configuration,
            id=id,
            permissions=permissions,
            tags=tags,
            tags_all=tags_all,
            timeouts=timeouts,
            version_description=version_description,
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
        '''Generates CDKTF code for importing a QuicksightTheme resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the QuicksightTheme to import.
        :param import_from_id: The id of the existing QuicksightTheme that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the QuicksightTheme to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acc69245597977147e9eda065bcc5c0c395c49c4c88de4779c7a522eb69637e6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfiguration")
    def put_configuration(
        self,
        *,
        data_color_palette: typing.Optional[typing.Union["QuicksightThemeConfigurationDataColorPalette", typing.Dict[builtins.str, typing.Any]]] = None,
        sheet: typing.Optional[typing.Union["QuicksightThemeConfigurationSheet", typing.Dict[builtins.str, typing.Any]]] = None,
        typography: typing.Optional[typing.Union["QuicksightThemeConfigurationTypography", typing.Dict[builtins.str, typing.Any]]] = None,
        ui_color_palette: typing.Optional[typing.Union["QuicksightThemeConfigurationUiColorPalette", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param data_color_palette: data_color_palette block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#data_color_palette QuicksightTheme#data_color_palette}
        :param sheet: sheet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#sheet QuicksightTheme#sheet}
        :param typography: typography block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#typography QuicksightTheme#typography}
        :param ui_color_palette: ui_color_palette block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#ui_color_palette QuicksightTheme#ui_color_palette}
        '''
        value = QuicksightThemeConfiguration(
            data_color_palette=data_color_palette,
            sheet=sheet,
            typography=typography,
            ui_color_palette=ui_color_palette,
        )

        return typing.cast(None, jsii.invoke(self, "putConfiguration", [value]))

    @jsii.member(jsii_name="putPermissions")
    def put_permissions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightThemePermissions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cdcdb7ca8985ddc99e9fa11fa4e35a9f54b20a420eb63673450d6377979b553)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPermissions", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#create QuicksightTheme#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#delete QuicksightTheme#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#update QuicksightTheme#update}.
        '''
        value = QuicksightThemeTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAwsAccountId")
    def reset_aws_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAccountId", []))

    @jsii.member(jsii_name="resetConfiguration")
    def reset_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfiguration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPermissions")
    def reset_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermissions", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVersionDescription")
    def reset_version_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersionDescription", []))

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
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> "QuicksightThemeConfigurationOutputReference":
        return typing.cast("QuicksightThemeConfigurationOutputReference", jsii.get(self, "configuration"))

    @builtins.property
    @jsii.member(jsii_name="createdTime")
    def created_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdTime"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdatedTime")
    def last_updated_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastUpdatedTime"))

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> "QuicksightThemePermissionsList":
        return typing.cast("QuicksightThemePermissionsList", jsii.get(self, "permissions"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "QuicksightThemeTimeoutsOutputReference":
        return typing.cast("QuicksightThemeTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="versionNumber")
    def version_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "versionNumber"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountIdInput")
    def aws_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="baseThemeIdInput")
    def base_theme_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseThemeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="configurationInput")
    def configuration_input(self) -> typing.Optional["QuicksightThemeConfiguration"]:
        return typing.cast(typing.Optional["QuicksightThemeConfiguration"], jsii.get(self, "configurationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionsInput")
    def permissions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightThemePermissions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightThemePermissions"]]], jsii.get(self, "permissionsInput"))

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
    @jsii.member(jsii_name="themeIdInput")
    def theme_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "themeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "QuicksightThemeTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "QuicksightThemeTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionDescriptionInput")
    def version_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsAccountId"))

    @aws_account_id.setter
    def aws_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d46046d8597fc97ffe3527689c549dc9fd2c369f2d9edfbcd4e626677787c6ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="baseThemeId")
    def base_theme_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseThemeId"))

    @base_theme_id.setter
    def base_theme_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__885c42e200779be97e08a8453cb9ee4e55733a98fa8aee8700d8636e5ef2cfaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseThemeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88a25ddfc5f309bf1d5253410daa1583b3836f1032e8a958b8b09f3c3083e0ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__059abd652a81ad69327c3655fa8ee24e0586b6a9a91a17216452480463666cb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c793062b9f7a12e14d3c1cbdebb0cf882d479cae450da1a00ea0e902dff334c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8dc9507533d07e269f6049a68ae3962f946a81a8738accb35d453fc016eb04c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="themeId")
    def theme_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "themeId"))

    @theme_id.setter
    def theme_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f5190e574d8fb0f5a300f0f6f300bd7ff3ebf2f57cbdc5024c0921e21ccf52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "themeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versionDescription")
    def version_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionDescription"))

    @version_description.setter
    def version_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__862a576ef782487fc04da7b6634bcc1ba6ef4aaabe189769cc838d8b444d4684)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionDescription", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "base_theme_id": "baseThemeId",
        "name": "name",
        "theme_id": "themeId",
        "aws_account_id": "awsAccountId",
        "configuration": "configuration",
        "id": "id",
        "permissions": "permissions",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
        "version_description": "versionDescription",
    },
)
class QuicksightThemeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        base_theme_id: builtins.str,
        name: builtins.str,
        theme_id: builtins.str,
        aws_account_id: typing.Optional[builtins.str] = None,
        configuration: typing.Optional[typing.Union["QuicksightThemeConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightThemePermissions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["QuicksightThemeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param base_theme_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#base_theme_id QuicksightTheme#base_theme_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#name QuicksightTheme#name}.
        :param theme_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#theme_id QuicksightTheme#theme_id}.
        :param aws_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#aws_account_id QuicksightTheme#aws_account_id}.
        :param configuration: configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#configuration QuicksightTheme#configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#id QuicksightTheme#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param permissions: permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#permissions QuicksightTheme#permissions}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#tags QuicksightTheme#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#tags_all QuicksightTheme#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#timeouts QuicksightTheme#timeouts}
        :param version_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#version_description QuicksightTheme#version_description}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(configuration, dict):
            configuration = QuicksightThemeConfiguration(**configuration)
        if isinstance(timeouts, dict):
            timeouts = QuicksightThemeTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b80da406ce468fb56ee4d58d1a47c5ac8195a474ec0c8a72f09236df28270077)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument base_theme_id", value=base_theme_id, expected_type=type_hints["base_theme_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument theme_id", value=theme_id, expected_type=type_hints["theme_id"])
            check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument version_description", value=version_description, expected_type=type_hints["version_description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "base_theme_id": base_theme_id,
            "name": name,
            "theme_id": theme_id,
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
        if aws_account_id is not None:
            self._values["aws_account_id"] = aws_account_id
        if configuration is not None:
            self._values["configuration"] = configuration
        if id is not None:
            self._values["id"] = id
        if permissions is not None:
            self._values["permissions"] = permissions
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if version_description is not None:
            self._values["version_description"] = version_description

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
    def base_theme_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#base_theme_id QuicksightTheme#base_theme_id}.'''
        result = self._values.get("base_theme_id")
        assert result is not None, "Required property 'base_theme_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#name QuicksightTheme#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def theme_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#theme_id QuicksightTheme#theme_id}.'''
        result = self._values.get("theme_id")
        assert result is not None, "Required property 'theme_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#aws_account_id QuicksightTheme#aws_account_id}.'''
        result = self._values.get("aws_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration(self) -> typing.Optional["QuicksightThemeConfiguration"]:
        '''configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#configuration QuicksightTheme#configuration}
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional["QuicksightThemeConfiguration"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#id QuicksightTheme#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightThemePermissions"]]]:
        '''permissions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#permissions QuicksightTheme#permissions}
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightThemePermissions"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#tags QuicksightTheme#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#tags_all QuicksightTheme#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["QuicksightThemeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#timeouts QuicksightTheme#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["QuicksightThemeTimeouts"], result)

    @builtins.property
    def version_description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#version_description QuicksightTheme#version_description}.'''
        result = self._values.get("version_description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "data_color_palette": "dataColorPalette",
        "sheet": "sheet",
        "typography": "typography",
        "ui_color_palette": "uiColorPalette",
    },
)
class QuicksightThemeConfiguration:
    def __init__(
        self,
        *,
        data_color_palette: typing.Optional[typing.Union["QuicksightThemeConfigurationDataColorPalette", typing.Dict[builtins.str, typing.Any]]] = None,
        sheet: typing.Optional[typing.Union["QuicksightThemeConfigurationSheet", typing.Dict[builtins.str, typing.Any]]] = None,
        typography: typing.Optional[typing.Union["QuicksightThemeConfigurationTypography", typing.Dict[builtins.str, typing.Any]]] = None,
        ui_color_palette: typing.Optional[typing.Union["QuicksightThemeConfigurationUiColorPalette", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param data_color_palette: data_color_palette block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#data_color_palette QuicksightTheme#data_color_palette}
        :param sheet: sheet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#sheet QuicksightTheme#sheet}
        :param typography: typography block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#typography QuicksightTheme#typography}
        :param ui_color_palette: ui_color_palette block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#ui_color_palette QuicksightTheme#ui_color_palette}
        '''
        if isinstance(data_color_palette, dict):
            data_color_palette = QuicksightThemeConfigurationDataColorPalette(**data_color_palette)
        if isinstance(sheet, dict):
            sheet = QuicksightThemeConfigurationSheet(**sheet)
        if isinstance(typography, dict):
            typography = QuicksightThemeConfigurationTypography(**typography)
        if isinstance(ui_color_palette, dict):
            ui_color_palette = QuicksightThemeConfigurationUiColorPalette(**ui_color_palette)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__716a6c3da8a867c95c9753af4453c925749043dd37d223c57c8b4197886c0b3e)
            check_type(argname="argument data_color_palette", value=data_color_palette, expected_type=type_hints["data_color_palette"])
            check_type(argname="argument sheet", value=sheet, expected_type=type_hints["sheet"])
            check_type(argname="argument typography", value=typography, expected_type=type_hints["typography"])
            check_type(argname="argument ui_color_palette", value=ui_color_palette, expected_type=type_hints["ui_color_palette"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_color_palette is not None:
            self._values["data_color_palette"] = data_color_palette
        if sheet is not None:
            self._values["sheet"] = sheet
        if typography is not None:
            self._values["typography"] = typography
        if ui_color_palette is not None:
            self._values["ui_color_palette"] = ui_color_palette

    @builtins.property
    def data_color_palette(
        self,
    ) -> typing.Optional["QuicksightThemeConfigurationDataColorPalette"]:
        '''data_color_palette block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#data_color_palette QuicksightTheme#data_color_palette}
        '''
        result = self._values.get("data_color_palette")
        return typing.cast(typing.Optional["QuicksightThemeConfigurationDataColorPalette"], result)

    @builtins.property
    def sheet(self) -> typing.Optional["QuicksightThemeConfigurationSheet"]:
        '''sheet block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#sheet QuicksightTheme#sheet}
        '''
        result = self._values.get("sheet")
        return typing.cast(typing.Optional["QuicksightThemeConfigurationSheet"], result)

    @builtins.property
    def typography(self) -> typing.Optional["QuicksightThemeConfigurationTypography"]:
        '''typography block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#typography QuicksightTheme#typography}
        '''
        result = self._values.get("typography")
        return typing.cast(typing.Optional["QuicksightThemeConfigurationTypography"], result)

    @builtins.property
    def ui_color_palette(
        self,
    ) -> typing.Optional["QuicksightThemeConfigurationUiColorPalette"]:
        '''ui_color_palette block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#ui_color_palette QuicksightTheme#ui_color_palette}
        '''
        result = self._values.get("ui_color_palette")
        return typing.cast(typing.Optional["QuicksightThemeConfigurationUiColorPalette"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfigurationDataColorPalette",
    jsii_struct_bases=[],
    name_mapping={
        "colors": "colors",
        "empty_fill_color": "emptyFillColor",
        "min_max_gradient": "minMaxGradient",
    },
)
class QuicksightThemeConfigurationDataColorPalette:
    def __init__(
        self,
        *,
        colors: typing.Optional[typing.Sequence[builtins.str]] = None,
        empty_fill_color: typing.Optional[builtins.str] = None,
        min_max_gradient: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param colors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#colors QuicksightTheme#colors}.
        :param empty_fill_color: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#empty_fill_color QuicksightTheme#empty_fill_color}.
        :param min_max_gradient: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#min_max_gradient QuicksightTheme#min_max_gradient}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3818ff653239253f52b8176917be93bc465e3fddc4af05f7b1ee144022e57e5)
            check_type(argname="argument colors", value=colors, expected_type=type_hints["colors"])
            check_type(argname="argument empty_fill_color", value=empty_fill_color, expected_type=type_hints["empty_fill_color"])
            check_type(argname="argument min_max_gradient", value=min_max_gradient, expected_type=type_hints["min_max_gradient"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if colors is not None:
            self._values["colors"] = colors
        if empty_fill_color is not None:
            self._values["empty_fill_color"] = empty_fill_color
        if min_max_gradient is not None:
            self._values["min_max_gradient"] = min_max_gradient

    @builtins.property
    def colors(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#colors QuicksightTheme#colors}.'''
        result = self._values.get("colors")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def empty_fill_color(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#empty_fill_color QuicksightTheme#empty_fill_color}.'''
        result = self._values.get("empty_fill_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_max_gradient(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#min_max_gradient QuicksightTheme#min_max_gradient}.'''
        result = self._values.get("min_max_gradient")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfigurationDataColorPalette(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightThemeConfigurationDataColorPaletteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfigurationDataColorPaletteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d849759e16ba4a1b1192696ac0acc1294960302cd46163d3cf801493e0a47654)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetColors")
    def reset_colors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColors", []))

    @jsii.member(jsii_name="resetEmptyFillColor")
    def reset_empty_fill_color(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmptyFillColor", []))

    @jsii.member(jsii_name="resetMinMaxGradient")
    def reset_min_max_gradient(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinMaxGradient", []))

    @builtins.property
    @jsii.member(jsii_name="colorsInput")
    def colors_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "colorsInput"))

    @builtins.property
    @jsii.member(jsii_name="emptyFillColorInput")
    def empty_fill_color_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emptyFillColorInput"))

    @builtins.property
    @jsii.member(jsii_name="minMaxGradientInput")
    def min_max_gradient_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "minMaxGradientInput"))

    @builtins.property
    @jsii.member(jsii_name="colors")
    def colors(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "colors"))

    @colors.setter
    def colors(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c7cc6423dab7295144e20c5d48f66a613b68e93f9c763801f8e755f1e5e7036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "colors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emptyFillColor")
    def empty_fill_color(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emptyFillColor"))

    @empty_fill_color.setter
    def empty_fill_color(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be867a0ca021f5b2ca98f3f42a64fb816394e6cdff66bc01b284ca0e1bf5a91f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emptyFillColor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minMaxGradient")
    def min_max_gradient(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "minMaxGradient"))

    @min_max_gradient.setter
    def min_max_gradient(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa879c270b4740b5566a2a475869d8db1789e2c231fa262e9cd37076bcc2b1e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minMaxGradient", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightThemeConfigurationDataColorPalette]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationDataColorPalette], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightThemeConfigurationDataColorPalette],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80503b26c7b2c40a2c69ca3e5d044cb036feb68b4f55cf76c4c65949e2084870)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightThemeConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ab4921180d27dfb0d303e9d8d471ffce1bf2fa6060184ffe49ea5ffbe8a19d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataColorPalette")
    def put_data_color_palette(
        self,
        *,
        colors: typing.Optional[typing.Sequence[builtins.str]] = None,
        empty_fill_color: typing.Optional[builtins.str] = None,
        min_max_gradient: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param colors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#colors QuicksightTheme#colors}.
        :param empty_fill_color: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#empty_fill_color QuicksightTheme#empty_fill_color}.
        :param min_max_gradient: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#min_max_gradient QuicksightTheme#min_max_gradient}.
        '''
        value = QuicksightThemeConfigurationDataColorPalette(
            colors=colors,
            empty_fill_color=empty_fill_color,
            min_max_gradient=min_max_gradient,
        )

        return typing.cast(None, jsii.invoke(self, "putDataColorPalette", [value]))

    @jsii.member(jsii_name="putSheet")
    def put_sheet(
        self,
        *,
        tile: typing.Optional[typing.Union["QuicksightThemeConfigurationSheetTile", typing.Dict[builtins.str, typing.Any]]] = None,
        tile_layout: typing.Optional[typing.Union["QuicksightThemeConfigurationSheetTileLayout", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param tile: tile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#tile QuicksightTheme#tile}
        :param tile_layout: tile_layout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#tile_layout QuicksightTheme#tile_layout}
        '''
        value = QuicksightThemeConfigurationSheet(tile=tile, tile_layout=tile_layout)

        return typing.cast(None, jsii.invoke(self, "putSheet", [value]))

    @jsii.member(jsii_name="putTypography")
    def put_typography(
        self,
        *,
        font_families: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightThemeConfigurationTypographyFontFamilies", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param font_families: font_families block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#font_families QuicksightTheme#font_families}
        '''
        value = QuicksightThemeConfigurationTypography(font_families=font_families)

        return typing.cast(None, jsii.invoke(self, "putTypography", [value]))

    @jsii.member(jsii_name="putUiColorPalette")
    def put_ui_color_palette(
        self,
        *,
        accent: typing.Optional[builtins.str] = None,
        accent_foreground: typing.Optional[builtins.str] = None,
        danger: typing.Optional[builtins.str] = None,
        danger_foreground: typing.Optional[builtins.str] = None,
        dimension: typing.Optional[builtins.str] = None,
        dimension_foreground: typing.Optional[builtins.str] = None,
        measure: typing.Optional[builtins.str] = None,
        measure_foreground: typing.Optional[builtins.str] = None,
        primary_background: typing.Optional[builtins.str] = None,
        primary_foreground: typing.Optional[builtins.str] = None,
        secondary_background: typing.Optional[builtins.str] = None,
        secondary_foreground: typing.Optional[builtins.str] = None,
        success: typing.Optional[builtins.str] = None,
        success_foreground: typing.Optional[builtins.str] = None,
        warning: typing.Optional[builtins.str] = None,
        warning_foreground: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#accent QuicksightTheme#accent}.
        :param accent_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#accent_foreground QuicksightTheme#accent_foreground}.
        :param danger: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#danger QuicksightTheme#danger}.
        :param danger_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#danger_foreground QuicksightTheme#danger_foreground}.
        :param dimension: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#dimension QuicksightTheme#dimension}.
        :param dimension_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#dimension_foreground QuicksightTheme#dimension_foreground}.
        :param measure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#measure QuicksightTheme#measure}.
        :param measure_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#measure_foreground QuicksightTheme#measure_foreground}.
        :param primary_background: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#primary_background QuicksightTheme#primary_background}.
        :param primary_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#primary_foreground QuicksightTheme#primary_foreground}.
        :param secondary_background: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#secondary_background QuicksightTheme#secondary_background}.
        :param secondary_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#secondary_foreground QuicksightTheme#secondary_foreground}.
        :param success: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#success QuicksightTheme#success}.
        :param success_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#success_foreground QuicksightTheme#success_foreground}.
        :param warning: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#warning QuicksightTheme#warning}.
        :param warning_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#warning_foreground QuicksightTheme#warning_foreground}.
        '''
        value = QuicksightThemeConfigurationUiColorPalette(
            accent=accent,
            accent_foreground=accent_foreground,
            danger=danger,
            danger_foreground=danger_foreground,
            dimension=dimension,
            dimension_foreground=dimension_foreground,
            measure=measure,
            measure_foreground=measure_foreground,
            primary_background=primary_background,
            primary_foreground=primary_foreground,
            secondary_background=secondary_background,
            secondary_foreground=secondary_foreground,
            success=success,
            success_foreground=success_foreground,
            warning=warning,
            warning_foreground=warning_foreground,
        )

        return typing.cast(None, jsii.invoke(self, "putUiColorPalette", [value]))

    @jsii.member(jsii_name="resetDataColorPalette")
    def reset_data_color_palette(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataColorPalette", []))

    @jsii.member(jsii_name="resetSheet")
    def reset_sheet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSheet", []))

    @jsii.member(jsii_name="resetTypography")
    def reset_typography(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTypography", []))

    @jsii.member(jsii_name="resetUiColorPalette")
    def reset_ui_color_palette(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUiColorPalette", []))

    @builtins.property
    @jsii.member(jsii_name="dataColorPalette")
    def data_color_palette(
        self,
    ) -> QuicksightThemeConfigurationDataColorPaletteOutputReference:
        return typing.cast(QuicksightThemeConfigurationDataColorPaletteOutputReference, jsii.get(self, "dataColorPalette"))

    @builtins.property
    @jsii.member(jsii_name="sheet")
    def sheet(self) -> "QuicksightThemeConfigurationSheetOutputReference":
        return typing.cast("QuicksightThemeConfigurationSheetOutputReference", jsii.get(self, "sheet"))

    @builtins.property
    @jsii.member(jsii_name="typography")
    def typography(self) -> "QuicksightThemeConfigurationTypographyOutputReference":
        return typing.cast("QuicksightThemeConfigurationTypographyOutputReference", jsii.get(self, "typography"))

    @builtins.property
    @jsii.member(jsii_name="uiColorPalette")
    def ui_color_palette(
        self,
    ) -> "QuicksightThemeConfigurationUiColorPaletteOutputReference":
        return typing.cast("QuicksightThemeConfigurationUiColorPaletteOutputReference", jsii.get(self, "uiColorPalette"))

    @builtins.property
    @jsii.member(jsii_name="dataColorPaletteInput")
    def data_color_palette_input(
        self,
    ) -> typing.Optional[QuicksightThemeConfigurationDataColorPalette]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationDataColorPalette], jsii.get(self, "dataColorPaletteInput"))

    @builtins.property
    @jsii.member(jsii_name="sheetInput")
    def sheet_input(self) -> typing.Optional["QuicksightThemeConfigurationSheet"]:
        return typing.cast(typing.Optional["QuicksightThemeConfigurationSheet"], jsii.get(self, "sheetInput"))

    @builtins.property
    @jsii.member(jsii_name="typographyInput")
    def typography_input(
        self,
    ) -> typing.Optional["QuicksightThemeConfigurationTypography"]:
        return typing.cast(typing.Optional["QuicksightThemeConfigurationTypography"], jsii.get(self, "typographyInput"))

    @builtins.property
    @jsii.member(jsii_name="uiColorPaletteInput")
    def ui_color_palette_input(
        self,
    ) -> typing.Optional["QuicksightThemeConfigurationUiColorPalette"]:
        return typing.cast(typing.Optional["QuicksightThemeConfigurationUiColorPalette"], jsii.get(self, "uiColorPaletteInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightThemeConfiguration]:
        return typing.cast(typing.Optional[QuicksightThemeConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightThemeConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d02fbba1243610ed0abf1203921ea60d44d81612b9e9cb792ac0280607f8eabf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheet",
    jsii_struct_bases=[],
    name_mapping={"tile": "tile", "tile_layout": "tileLayout"},
)
class QuicksightThemeConfigurationSheet:
    def __init__(
        self,
        *,
        tile: typing.Optional[typing.Union["QuicksightThemeConfigurationSheetTile", typing.Dict[builtins.str, typing.Any]]] = None,
        tile_layout: typing.Optional[typing.Union["QuicksightThemeConfigurationSheetTileLayout", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param tile: tile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#tile QuicksightTheme#tile}
        :param tile_layout: tile_layout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#tile_layout QuicksightTheme#tile_layout}
        '''
        if isinstance(tile, dict):
            tile = QuicksightThemeConfigurationSheetTile(**tile)
        if isinstance(tile_layout, dict):
            tile_layout = QuicksightThemeConfigurationSheetTileLayout(**tile_layout)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9cede00e2ea92d36a8d8d7218098252a0eb37271434cfc7600a38385d074776)
            check_type(argname="argument tile", value=tile, expected_type=type_hints["tile"])
            check_type(argname="argument tile_layout", value=tile_layout, expected_type=type_hints["tile_layout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tile is not None:
            self._values["tile"] = tile
        if tile_layout is not None:
            self._values["tile_layout"] = tile_layout

    @builtins.property
    def tile(self) -> typing.Optional["QuicksightThemeConfigurationSheetTile"]:
        '''tile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#tile QuicksightTheme#tile}
        '''
        result = self._values.get("tile")
        return typing.cast(typing.Optional["QuicksightThemeConfigurationSheetTile"], result)

    @builtins.property
    def tile_layout(
        self,
    ) -> typing.Optional["QuicksightThemeConfigurationSheetTileLayout"]:
        '''tile_layout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#tile_layout QuicksightTheme#tile_layout}
        '''
        result = self._values.get("tile_layout")
        return typing.cast(typing.Optional["QuicksightThemeConfigurationSheetTileLayout"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfigurationSheet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightThemeConfigurationSheetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24ee7e4967dd8b7fe95e35a9f32f4aebb15e6978ad521ee7e6514d38a56fbcdc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTile")
    def put_tile(
        self,
        *,
        border: typing.Optional[typing.Union["QuicksightThemeConfigurationSheetTileBorder", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param border: border block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#border QuicksightTheme#border}
        '''
        value = QuicksightThemeConfigurationSheetTile(border=border)

        return typing.cast(None, jsii.invoke(self, "putTile", [value]))

    @jsii.member(jsii_name="putTileLayout")
    def put_tile_layout(
        self,
        *,
        gutter: typing.Optional[typing.Union["QuicksightThemeConfigurationSheetTileLayoutGutter", typing.Dict[builtins.str, typing.Any]]] = None,
        margin: typing.Optional[typing.Union["QuicksightThemeConfigurationSheetTileLayoutMargin", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param gutter: gutter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#gutter QuicksightTheme#gutter}
        :param margin: margin block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#margin QuicksightTheme#margin}
        '''
        value = QuicksightThemeConfigurationSheetTileLayout(
            gutter=gutter, margin=margin
        )

        return typing.cast(None, jsii.invoke(self, "putTileLayout", [value]))

    @jsii.member(jsii_name="resetTile")
    def reset_tile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTile", []))

    @jsii.member(jsii_name="resetTileLayout")
    def reset_tile_layout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTileLayout", []))

    @builtins.property
    @jsii.member(jsii_name="tile")
    def tile(self) -> "QuicksightThemeConfigurationSheetTileOutputReference":
        return typing.cast("QuicksightThemeConfigurationSheetTileOutputReference", jsii.get(self, "tile"))

    @builtins.property
    @jsii.member(jsii_name="tileLayout")
    def tile_layout(
        self,
    ) -> "QuicksightThemeConfigurationSheetTileLayoutOutputReference":
        return typing.cast("QuicksightThemeConfigurationSheetTileLayoutOutputReference", jsii.get(self, "tileLayout"))

    @builtins.property
    @jsii.member(jsii_name="tileInput")
    def tile_input(self) -> typing.Optional["QuicksightThemeConfigurationSheetTile"]:
        return typing.cast(typing.Optional["QuicksightThemeConfigurationSheetTile"], jsii.get(self, "tileInput"))

    @builtins.property
    @jsii.member(jsii_name="tileLayoutInput")
    def tile_layout_input(
        self,
    ) -> typing.Optional["QuicksightThemeConfigurationSheetTileLayout"]:
        return typing.cast(typing.Optional["QuicksightThemeConfigurationSheetTileLayout"], jsii.get(self, "tileLayoutInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightThemeConfigurationSheet]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationSheet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightThemeConfigurationSheet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__108298dfba0c01aec6407aae5e4060c9ed85dc73034ded357b4e09fda7c32aa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheetTile",
    jsii_struct_bases=[],
    name_mapping={"border": "border"},
)
class QuicksightThemeConfigurationSheetTile:
    def __init__(
        self,
        *,
        border: typing.Optional[typing.Union["QuicksightThemeConfigurationSheetTileBorder", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param border: border block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#border QuicksightTheme#border}
        '''
        if isinstance(border, dict):
            border = QuicksightThemeConfigurationSheetTileBorder(**border)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc0d0dffc8db4869b2ae1a14791dbfbe3509b63f0a8d3ab3c1bb5675454609a5)
            check_type(argname="argument border", value=border, expected_type=type_hints["border"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if border is not None:
            self._values["border"] = border

    @builtins.property
    def border(self) -> typing.Optional["QuicksightThemeConfigurationSheetTileBorder"]:
        '''border block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#border QuicksightTheme#border}
        '''
        result = self._values.get("border")
        return typing.cast(typing.Optional["QuicksightThemeConfigurationSheetTileBorder"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfigurationSheetTile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheetTileBorder",
    jsii_struct_bases=[],
    name_mapping={"show": "show"},
)
class QuicksightThemeConfigurationSheetTileBorder:
    def __init__(
        self,
        *,
        show: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param show: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#show QuicksightTheme#show}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0be25645d493ee3ca5141175c510ecafc6a00159bb7bc49aaa2e062cea03d8ae)
            check_type(argname="argument show", value=show, expected_type=type_hints["show"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if show is not None:
            self._values["show"] = show

    @builtins.property
    def show(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#show QuicksightTheme#show}.'''
        result = self._values.get("show")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfigurationSheetTileBorder(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightThemeConfigurationSheetTileBorderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheetTileBorderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5aa49123f76879f8274a277eecd16cb45c41ff16179c03f1dd30ffdaf9d63e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetShow")
    def reset_show(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShow", []))

    @builtins.property
    @jsii.member(jsii_name="showInput")
    def show_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "showInput"))

    @builtins.property
    @jsii.member(jsii_name="show")
    def show(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "show"))

    @show.setter
    def show(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88aef4cf11bf2d2b6e91e6e5b4512d89ba61cc718539d2f325ed77d24d1de852)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "show", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightThemeConfigurationSheetTileBorder]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationSheetTileBorder], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightThemeConfigurationSheetTileBorder],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42602e1339bda58f2d8ebacf450429495a8c579e7b4bc81eba5b5d9506217c8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheetTileLayout",
    jsii_struct_bases=[],
    name_mapping={"gutter": "gutter", "margin": "margin"},
)
class QuicksightThemeConfigurationSheetTileLayout:
    def __init__(
        self,
        *,
        gutter: typing.Optional[typing.Union["QuicksightThemeConfigurationSheetTileLayoutGutter", typing.Dict[builtins.str, typing.Any]]] = None,
        margin: typing.Optional[typing.Union["QuicksightThemeConfigurationSheetTileLayoutMargin", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param gutter: gutter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#gutter QuicksightTheme#gutter}
        :param margin: margin block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#margin QuicksightTheme#margin}
        '''
        if isinstance(gutter, dict):
            gutter = QuicksightThemeConfigurationSheetTileLayoutGutter(**gutter)
        if isinstance(margin, dict):
            margin = QuicksightThemeConfigurationSheetTileLayoutMargin(**margin)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98b6fb17ee1fff5912318102046c3baf1c738105d388bd1f874944302f554271)
            check_type(argname="argument gutter", value=gutter, expected_type=type_hints["gutter"])
            check_type(argname="argument margin", value=margin, expected_type=type_hints["margin"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gutter is not None:
            self._values["gutter"] = gutter
        if margin is not None:
            self._values["margin"] = margin

    @builtins.property
    def gutter(
        self,
    ) -> typing.Optional["QuicksightThemeConfigurationSheetTileLayoutGutter"]:
        '''gutter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#gutter QuicksightTheme#gutter}
        '''
        result = self._values.get("gutter")
        return typing.cast(typing.Optional["QuicksightThemeConfigurationSheetTileLayoutGutter"], result)

    @builtins.property
    def margin(
        self,
    ) -> typing.Optional["QuicksightThemeConfigurationSheetTileLayoutMargin"]:
        '''margin block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#margin QuicksightTheme#margin}
        '''
        result = self._values.get("margin")
        return typing.cast(typing.Optional["QuicksightThemeConfigurationSheetTileLayoutMargin"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfigurationSheetTileLayout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheetTileLayoutGutter",
    jsii_struct_bases=[],
    name_mapping={"show": "show"},
)
class QuicksightThemeConfigurationSheetTileLayoutGutter:
    def __init__(
        self,
        *,
        show: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param show: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#show QuicksightTheme#show}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b967b2404bae9c2d27369b4bc631d8b07e78c44adbb467b47879a2fd2075bb9f)
            check_type(argname="argument show", value=show, expected_type=type_hints["show"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if show is not None:
            self._values["show"] = show

    @builtins.property
    def show(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#show QuicksightTheme#show}.'''
        result = self._values.get("show")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfigurationSheetTileLayoutGutter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightThemeConfigurationSheetTileLayoutGutterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheetTileLayoutGutterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0109d32cf4c0cd636639175b1c76d89328889fd5a1abd67ab6b38bb43e01821c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetShow")
    def reset_show(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShow", []))

    @builtins.property
    @jsii.member(jsii_name="showInput")
    def show_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "showInput"))

    @builtins.property
    @jsii.member(jsii_name="show")
    def show(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "show"))

    @show.setter
    def show(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3292ec90f6421392dafee09ef2cde2db4902eb0e6ad9548851a243acc3a700bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "show", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightThemeConfigurationSheetTileLayoutGutter]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationSheetTileLayoutGutter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightThemeConfigurationSheetTileLayoutGutter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b64539c68c6b31f10d8923d19585d64935a054efd9b8299d6f7a31a9f0a5fe11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheetTileLayoutMargin",
    jsii_struct_bases=[],
    name_mapping={"show": "show"},
)
class QuicksightThemeConfigurationSheetTileLayoutMargin:
    def __init__(
        self,
        *,
        show: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param show: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#show QuicksightTheme#show}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e1394f3790d73d0ad60683f1fc02a6bbb21a99f3e5e7775d24850bf54aa035c)
            check_type(argname="argument show", value=show, expected_type=type_hints["show"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if show is not None:
            self._values["show"] = show

    @builtins.property
    def show(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#show QuicksightTheme#show}.'''
        result = self._values.get("show")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfigurationSheetTileLayoutMargin(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightThemeConfigurationSheetTileLayoutMarginOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheetTileLayoutMarginOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f41edfb4d55502da4bb586b20c9c3ec922a8623963e3f1a6898e1a3de5fd00d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetShow")
    def reset_show(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShow", []))

    @builtins.property
    @jsii.member(jsii_name="showInput")
    def show_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "showInput"))

    @builtins.property
    @jsii.member(jsii_name="show")
    def show(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "show"))

    @show.setter
    def show(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c081a66da479cc105c6cdce675663b6b87e403cda45271cbecebb02bf53a7a80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "show", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightThemeConfigurationSheetTileLayoutMargin]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationSheetTileLayoutMargin], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightThemeConfigurationSheetTileLayoutMargin],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45ddc6fdad3ba0efedc4b88117a6962e38c32bf384f5dc4915d4c17d8002e014)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightThemeConfigurationSheetTileLayoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheetTileLayoutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26c0095141b64319eaf735a727cf3f27a0ae6778079a3819a406509553d05c38)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGutter")
    def put_gutter(
        self,
        *,
        show: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param show: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#show QuicksightTheme#show}.
        '''
        value = QuicksightThemeConfigurationSheetTileLayoutGutter(show=show)

        return typing.cast(None, jsii.invoke(self, "putGutter", [value]))

    @jsii.member(jsii_name="putMargin")
    def put_margin(
        self,
        *,
        show: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param show: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#show QuicksightTheme#show}.
        '''
        value = QuicksightThemeConfigurationSheetTileLayoutMargin(show=show)

        return typing.cast(None, jsii.invoke(self, "putMargin", [value]))

    @jsii.member(jsii_name="resetGutter")
    def reset_gutter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGutter", []))

    @jsii.member(jsii_name="resetMargin")
    def reset_margin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMargin", []))

    @builtins.property
    @jsii.member(jsii_name="gutter")
    def gutter(
        self,
    ) -> QuicksightThemeConfigurationSheetTileLayoutGutterOutputReference:
        return typing.cast(QuicksightThemeConfigurationSheetTileLayoutGutterOutputReference, jsii.get(self, "gutter"))

    @builtins.property
    @jsii.member(jsii_name="margin")
    def margin(
        self,
    ) -> QuicksightThemeConfigurationSheetTileLayoutMarginOutputReference:
        return typing.cast(QuicksightThemeConfigurationSheetTileLayoutMarginOutputReference, jsii.get(self, "margin"))

    @builtins.property
    @jsii.member(jsii_name="gutterInput")
    def gutter_input(
        self,
    ) -> typing.Optional[QuicksightThemeConfigurationSheetTileLayoutGutter]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationSheetTileLayoutGutter], jsii.get(self, "gutterInput"))

    @builtins.property
    @jsii.member(jsii_name="marginInput")
    def margin_input(
        self,
    ) -> typing.Optional[QuicksightThemeConfigurationSheetTileLayoutMargin]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationSheetTileLayoutMargin], jsii.get(self, "marginInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightThemeConfigurationSheetTileLayout]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationSheetTileLayout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightThemeConfigurationSheetTileLayout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df5c458ff33583b980b09980cfb8af1ffa4b8c944e8c071c03d7afd1940d6ce5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightThemeConfigurationSheetTileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheetTileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0469479e8fa97f4a00664f90e2fe6591be7b7c5307b2be5bd415864c43ece6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBorder")
    def put_border(
        self,
        *,
        show: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param show: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#show QuicksightTheme#show}.
        '''
        value = QuicksightThemeConfigurationSheetTileBorder(show=show)

        return typing.cast(None, jsii.invoke(self, "putBorder", [value]))

    @jsii.member(jsii_name="resetBorder")
    def reset_border(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBorder", []))

    @builtins.property
    @jsii.member(jsii_name="border")
    def border(self) -> QuicksightThemeConfigurationSheetTileBorderOutputReference:
        return typing.cast(QuicksightThemeConfigurationSheetTileBorderOutputReference, jsii.get(self, "border"))

    @builtins.property
    @jsii.member(jsii_name="borderInput")
    def border_input(
        self,
    ) -> typing.Optional[QuicksightThemeConfigurationSheetTileBorder]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationSheetTileBorder], jsii.get(self, "borderInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightThemeConfigurationSheetTile]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationSheetTile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightThemeConfigurationSheetTile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__682bbe4f008c6e0ffe9c92c946afe3a53a84dec3f3d57ac1fbd159cf7e204cb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfigurationTypography",
    jsii_struct_bases=[],
    name_mapping={"font_families": "fontFamilies"},
)
class QuicksightThemeConfigurationTypography:
    def __init__(
        self,
        *,
        font_families: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightThemeConfigurationTypographyFontFamilies", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param font_families: font_families block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#font_families QuicksightTheme#font_families}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d11bb2a814c3e025aed20ea2ea86a45859dadb9aa3b89d481b3e774172d2f63)
            check_type(argname="argument font_families", value=font_families, expected_type=type_hints["font_families"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if font_families is not None:
            self._values["font_families"] = font_families

    @builtins.property
    def font_families(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightThemeConfigurationTypographyFontFamilies"]]]:
        '''font_families block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#font_families QuicksightTheme#font_families}
        '''
        result = self._values.get("font_families")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightThemeConfigurationTypographyFontFamilies"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfigurationTypography(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfigurationTypographyFontFamilies",
    jsii_struct_bases=[],
    name_mapping={"font_family": "fontFamily"},
)
class QuicksightThemeConfigurationTypographyFontFamilies:
    def __init__(self, *, font_family: typing.Optional[builtins.str] = None) -> None:
        '''
        :param font_family: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#font_family QuicksightTheme#font_family}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c81e0289cb375ba774cc00dc70b542280b977b6c219635bd4b4a13948a30dc86)
            check_type(argname="argument font_family", value=font_family, expected_type=type_hints["font_family"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if font_family is not None:
            self._values["font_family"] = font_family

    @builtins.property
    def font_family(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#font_family QuicksightTheme#font_family}.'''
        result = self._values.get("font_family")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfigurationTypographyFontFamilies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightThemeConfigurationTypographyFontFamiliesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfigurationTypographyFontFamiliesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6c7bb54a433f2ee3666e4f969b8cd7b6406fc40d5973598e2cff3e8135cbdea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightThemeConfigurationTypographyFontFamiliesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fb24fe384a792344f41f60e92a8256952e2829b73aef6c7c79e8601fb30a662)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightThemeConfigurationTypographyFontFamiliesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b28badced9dc4d7e38bb6da6f2fc85a4fbf8bb36ece0c061b356a58abd0f2e9d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30896a5bbdb6229ded29f8c48a2495e0b8612ceaeaeb62af2ca9396afdeca549)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcba23099077e8c280e0afdbf0b3c8d1de1403d4abaa4e28a70abb80df39fc4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightThemeConfigurationTypographyFontFamilies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightThemeConfigurationTypographyFontFamilies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightThemeConfigurationTypographyFontFamilies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9ffe95a1b4f38c332fc40cc3359d67cde14201bd906d39253cea97a89e53a95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightThemeConfigurationTypographyFontFamiliesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfigurationTypographyFontFamiliesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2aa167e2ebc9ac51c60ca445da8fa5cf0b16ee8c60276425cc81123edd48435a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFontFamily")
    def reset_font_family(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFontFamily", []))

    @builtins.property
    @jsii.member(jsii_name="fontFamilyInput")
    def font_family_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fontFamilyInput"))

    @builtins.property
    @jsii.member(jsii_name="fontFamily")
    def font_family(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fontFamily"))

    @font_family.setter
    def font_family(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d47b259fe34727907b3e39b1d27d236412a30c1a2a72a049fb496bfdc8f8a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fontFamily", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemeConfigurationTypographyFontFamilies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemeConfigurationTypographyFontFamilies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemeConfigurationTypographyFontFamilies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea078f6e776517c399ddb54c4614b3797ed79ffd362c749a0f21a0f099d3b053)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightThemeConfigurationTypographyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfigurationTypographyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7181d24a8e18d74e42ccb5b28c8f1989c053fe8e2114264400982d336248fec3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFontFamilies")
    def put_font_families(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightThemeConfigurationTypographyFontFamilies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac474130bcf4e777969015aaa44184a1f03c17b779abdb3f40229a8218077e25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFontFamilies", [value]))

    @jsii.member(jsii_name="resetFontFamilies")
    def reset_font_families(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFontFamilies", []))

    @builtins.property
    @jsii.member(jsii_name="fontFamilies")
    def font_families(self) -> QuicksightThemeConfigurationTypographyFontFamiliesList:
        return typing.cast(QuicksightThemeConfigurationTypographyFontFamiliesList, jsii.get(self, "fontFamilies"))

    @builtins.property
    @jsii.member(jsii_name="fontFamiliesInput")
    def font_families_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightThemeConfigurationTypographyFontFamilies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightThemeConfigurationTypographyFontFamilies]]], jsii.get(self, "fontFamiliesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightThemeConfigurationTypography]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationTypography], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightThemeConfigurationTypography],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a488952e3808ee39d178beede369fb3ee32efbabdc567678ee89585f6e83e35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfigurationUiColorPalette",
    jsii_struct_bases=[],
    name_mapping={
        "accent": "accent",
        "accent_foreground": "accentForeground",
        "danger": "danger",
        "danger_foreground": "dangerForeground",
        "dimension": "dimension",
        "dimension_foreground": "dimensionForeground",
        "measure": "measure",
        "measure_foreground": "measureForeground",
        "primary_background": "primaryBackground",
        "primary_foreground": "primaryForeground",
        "secondary_background": "secondaryBackground",
        "secondary_foreground": "secondaryForeground",
        "success": "success",
        "success_foreground": "successForeground",
        "warning": "warning",
        "warning_foreground": "warningForeground",
    },
)
class QuicksightThemeConfigurationUiColorPalette:
    def __init__(
        self,
        *,
        accent: typing.Optional[builtins.str] = None,
        accent_foreground: typing.Optional[builtins.str] = None,
        danger: typing.Optional[builtins.str] = None,
        danger_foreground: typing.Optional[builtins.str] = None,
        dimension: typing.Optional[builtins.str] = None,
        dimension_foreground: typing.Optional[builtins.str] = None,
        measure: typing.Optional[builtins.str] = None,
        measure_foreground: typing.Optional[builtins.str] = None,
        primary_background: typing.Optional[builtins.str] = None,
        primary_foreground: typing.Optional[builtins.str] = None,
        secondary_background: typing.Optional[builtins.str] = None,
        secondary_foreground: typing.Optional[builtins.str] = None,
        success: typing.Optional[builtins.str] = None,
        success_foreground: typing.Optional[builtins.str] = None,
        warning: typing.Optional[builtins.str] = None,
        warning_foreground: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#accent QuicksightTheme#accent}.
        :param accent_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#accent_foreground QuicksightTheme#accent_foreground}.
        :param danger: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#danger QuicksightTheme#danger}.
        :param danger_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#danger_foreground QuicksightTheme#danger_foreground}.
        :param dimension: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#dimension QuicksightTheme#dimension}.
        :param dimension_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#dimension_foreground QuicksightTheme#dimension_foreground}.
        :param measure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#measure QuicksightTheme#measure}.
        :param measure_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#measure_foreground QuicksightTheme#measure_foreground}.
        :param primary_background: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#primary_background QuicksightTheme#primary_background}.
        :param primary_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#primary_foreground QuicksightTheme#primary_foreground}.
        :param secondary_background: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#secondary_background QuicksightTheme#secondary_background}.
        :param secondary_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#secondary_foreground QuicksightTheme#secondary_foreground}.
        :param success: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#success QuicksightTheme#success}.
        :param success_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#success_foreground QuicksightTheme#success_foreground}.
        :param warning: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#warning QuicksightTheme#warning}.
        :param warning_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#warning_foreground QuicksightTheme#warning_foreground}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__420bdb7c662a19a89fc65f2538589de688438a2c24fc436f9a6d4bf28667b8f6)
            check_type(argname="argument accent", value=accent, expected_type=type_hints["accent"])
            check_type(argname="argument accent_foreground", value=accent_foreground, expected_type=type_hints["accent_foreground"])
            check_type(argname="argument danger", value=danger, expected_type=type_hints["danger"])
            check_type(argname="argument danger_foreground", value=danger_foreground, expected_type=type_hints["danger_foreground"])
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
            check_type(argname="argument dimension_foreground", value=dimension_foreground, expected_type=type_hints["dimension_foreground"])
            check_type(argname="argument measure", value=measure, expected_type=type_hints["measure"])
            check_type(argname="argument measure_foreground", value=measure_foreground, expected_type=type_hints["measure_foreground"])
            check_type(argname="argument primary_background", value=primary_background, expected_type=type_hints["primary_background"])
            check_type(argname="argument primary_foreground", value=primary_foreground, expected_type=type_hints["primary_foreground"])
            check_type(argname="argument secondary_background", value=secondary_background, expected_type=type_hints["secondary_background"])
            check_type(argname="argument secondary_foreground", value=secondary_foreground, expected_type=type_hints["secondary_foreground"])
            check_type(argname="argument success", value=success, expected_type=type_hints["success"])
            check_type(argname="argument success_foreground", value=success_foreground, expected_type=type_hints["success_foreground"])
            check_type(argname="argument warning", value=warning, expected_type=type_hints["warning"])
            check_type(argname="argument warning_foreground", value=warning_foreground, expected_type=type_hints["warning_foreground"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accent is not None:
            self._values["accent"] = accent
        if accent_foreground is not None:
            self._values["accent_foreground"] = accent_foreground
        if danger is not None:
            self._values["danger"] = danger
        if danger_foreground is not None:
            self._values["danger_foreground"] = danger_foreground
        if dimension is not None:
            self._values["dimension"] = dimension
        if dimension_foreground is not None:
            self._values["dimension_foreground"] = dimension_foreground
        if measure is not None:
            self._values["measure"] = measure
        if measure_foreground is not None:
            self._values["measure_foreground"] = measure_foreground
        if primary_background is not None:
            self._values["primary_background"] = primary_background
        if primary_foreground is not None:
            self._values["primary_foreground"] = primary_foreground
        if secondary_background is not None:
            self._values["secondary_background"] = secondary_background
        if secondary_foreground is not None:
            self._values["secondary_foreground"] = secondary_foreground
        if success is not None:
            self._values["success"] = success
        if success_foreground is not None:
            self._values["success_foreground"] = success_foreground
        if warning is not None:
            self._values["warning"] = warning
        if warning_foreground is not None:
            self._values["warning_foreground"] = warning_foreground

    @builtins.property
    def accent(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#accent QuicksightTheme#accent}.'''
        result = self._values.get("accent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def accent_foreground(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#accent_foreground QuicksightTheme#accent_foreground}.'''
        result = self._values.get("accent_foreground")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def danger(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#danger QuicksightTheme#danger}.'''
        result = self._values.get("danger")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def danger_foreground(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#danger_foreground QuicksightTheme#danger_foreground}.'''
        result = self._values.get("danger_foreground")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dimension(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#dimension QuicksightTheme#dimension}.'''
        result = self._values.get("dimension")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dimension_foreground(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#dimension_foreground QuicksightTheme#dimension_foreground}.'''
        result = self._values.get("dimension_foreground")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def measure(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#measure QuicksightTheme#measure}.'''
        result = self._values.get("measure")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def measure_foreground(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#measure_foreground QuicksightTheme#measure_foreground}.'''
        result = self._values.get("measure_foreground")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_background(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#primary_background QuicksightTheme#primary_background}.'''
        result = self._values.get("primary_background")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_foreground(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#primary_foreground QuicksightTheme#primary_foreground}.'''
        result = self._values.get("primary_foreground")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_background(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#secondary_background QuicksightTheme#secondary_background}.'''
        result = self._values.get("secondary_background")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_foreground(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#secondary_foreground QuicksightTheme#secondary_foreground}.'''
        result = self._values.get("secondary_foreground")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def success(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#success QuicksightTheme#success}.'''
        result = self._values.get("success")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def success_foreground(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#success_foreground QuicksightTheme#success_foreground}.'''
        result = self._values.get("success_foreground")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def warning(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#warning QuicksightTheme#warning}.'''
        result = self._values.get("warning")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def warning_foreground(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#warning_foreground QuicksightTheme#warning_foreground}.'''
        result = self._values.get("warning_foreground")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfigurationUiColorPalette(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightThemeConfigurationUiColorPaletteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeConfigurationUiColorPaletteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6679e3b4f16a1582ad0a5978de2e204be0ab312919f27c88725e149c943dd14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccent")
    def reset_accent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccent", []))

    @jsii.member(jsii_name="resetAccentForeground")
    def reset_accent_foreground(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccentForeground", []))

    @jsii.member(jsii_name="resetDanger")
    def reset_danger(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDanger", []))

    @jsii.member(jsii_name="resetDangerForeground")
    def reset_danger_foreground(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDangerForeground", []))

    @jsii.member(jsii_name="resetDimension")
    def reset_dimension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDimension", []))

    @jsii.member(jsii_name="resetDimensionForeground")
    def reset_dimension_foreground(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDimensionForeground", []))

    @jsii.member(jsii_name="resetMeasure")
    def reset_measure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMeasure", []))

    @jsii.member(jsii_name="resetMeasureForeground")
    def reset_measure_foreground(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMeasureForeground", []))

    @jsii.member(jsii_name="resetPrimaryBackground")
    def reset_primary_background(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryBackground", []))

    @jsii.member(jsii_name="resetPrimaryForeground")
    def reset_primary_foreground(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryForeground", []))

    @jsii.member(jsii_name="resetSecondaryBackground")
    def reset_secondary_background(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryBackground", []))

    @jsii.member(jsii_name="resetSecondaryForeground")
    def reset_secondary_foreground(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryForeground", []))

    @jsii.member(jsii_name="resetSuccess")
    def reset_success(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccess", []))

    @jsii.member(jsii_name="resetSuccessForeground")
    def reset_success_foreground(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessForeground", []))

    @jsii.member(jsii_name="resetWarning")
    def reset_warning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWarning", []))

    @jsii.member(jsii_name="resetWarningForeground")
    def reset_warning_foreground(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWarningForeground", []))

    @builtins.property
    @jsii.member(jsii_name="accentForegroundInput")
    def accent_foreground_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accentForegroundInput"))

    @builtins.property
    @jsii.member(jsii_name="accentInput")
    def accent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accentInput"))

    @builtins.property
    @jsii.member(jsii_name="dangerForegroundInput")
    def danger_foreground_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dangerForegroundInput"))

    @builtins.property
    @jsii.member(jsii_name="dangerInput")
    def danger_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dangerInput"))

    @builtins.property
    @jsii.member(jsii_name="dimensionForegroundInput")
    def dimension_foreground_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dimensionForegroundInput"))

    @builtins.property
    @jsii.member(jsii_name="dimensionInput")
    def dimension_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dimensionInput"))

    @builtins.property
    @jsii.member(jsii_name="measureForegroundInput")
    def measure_foreground_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "measureForegroundInput"))

    @builtins.property
    @jsii.member(jsii_name="measureInput")
    def measure_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "measureInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryBackgroundInput")
    def primary_background_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryBackgroundInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryForegroundInput")
    def primary_foreground_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryForegroundInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryBackgroundInput")
    def secondary_background_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secondaryBackgroundInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryForegroundInput")
    def secondary_foreground_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secondaryForegroundInput"))

    @builtins.property
    @jsii.member(jsii_name="successForegroundInput")
    def success_foreground_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "successForegroundInput"))

    @builtins.property
    @jsii.member(jsii_name="successInput")
    def success_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "successInput"))

    @builtins.property
    @jsii.member(jsii_name="warningForegroundInput")
    def warning_foreground_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "warningForegroundInput"))

    @builtins.property
    @jsii.member(jsii_name="warningInput")
    def warning_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "warningInput"))

    @builtins.property
    @jsii.member(jsii_name="accent")
    def accent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accent"))

    @accent.setter
    def accent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4fbc993ef7beea663311c3ba182736980fcda6fd3e610df8af66d51ce1a3efc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accentForeground")
    def accent_foreground(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accentForeground"))

    @accent_foreground.setter
    def accent_foreground(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca766200d0f2543cead5246e65a1fe6c9767e42fccfb5307cb8780c05decce1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accentForeground", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="danger")
    def danger(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "danger"))

    @danger.setter
    def danger(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d89dcebef38b687d1bac9270b5a2e57ec7fc3b84e78d2f6d1c334bb8f9e416f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "danger", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dangerForeground")
    def danger_foreground(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dangerForeground"))

    @danger_foreground.setter
    def danger_foreground(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beb31fbcb18105d735c751786e4bbd1270f823dcfef6372c58cedbf166b7621e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dangerForeground", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dimension")
    def dimension(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dimension"))

    @dimension.setter
    def dimension(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__904147790c20460c1e83dda7b926962bc8d676596a69a4dbaf9380bfbd65e57e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dimension", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dimensionForeground")
    def dimension_foreground(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dimensionForeground"))

    @dimension_foreground.setter
    def dimension_foreground(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5bc381441211e14c60d5101333da963b713007771c646c60d0ad3fcc4282bd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dimensionForeground", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="measure")
    def measure(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "measure"))

    @measure.setter
    def measure(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__374dab6077df0a87e719cadd9b26344473c7855ba15b90ea4e0093f7873f9c8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "measure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="measureForeground")
    def measure_foreground(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "measureForeground"))

    @measure_foreground.setter
    def measure_foreground(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3b6d00fbffc877c40a0f609543c9291e7aacffd0bcc98c1fc7122385609bbc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "measureForeground", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryBackground")
    def primary_background(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryBackground"))

    @primary_background.setter
    def primary_background(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bf33e512c773c7f53219929cb587c595ccd10295456e886c83a6eb4eb4aa3f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryBackground", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryForeground")
    def primary_foreground(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryForeground"))

    @primary_foreground.setter
    def primary_foreground(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa3a505fa9da85a533b1ec55163864d151f7c0d32dd0b8d03d94fcf38867269f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryForeground", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secondaryBackground")
    def secondary_background(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryBackground"))

    @secondary_background.setter
    def secondary_background(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__447e3e7d2b2bbad8c3f69bcc8497f30f07345941fdcd459879ffbfa5902623e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryBackground", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secondaryForeground")
    def secondary_foreground(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryForeground"))

    @secondary_foreground.setter
    def secondary_foreground(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__666e4d9ec0991056d676902f3e8b31668f7deabba855d5e81c81d576554518ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryForeground", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="success")
    def success(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "success"))

    @success.setter
    def success(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff004a938b348374c1d31f9e9c506aa6517bf3a5a21b39a51a1b2cb8957be81a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "success", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successForeground")
    def success_foreground(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "successForeground"))

    @success_foreground.setter
    def success_foreground(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__921182ad9fe45bd1f21068df154a82d6177500d1bbc37c28562d081d147e38c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successForeground", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="warning")
    def warning(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "warning"))

    @warning.setter
    def warning(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eda9455652c8efb32ff4cf489407d840559c8d0f788488bc0dd6a1b46f49f541)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "warning", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="warningForeground")
    def warning_foreground(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "warningForeground"))

    @warning_foreground.setter
    def warning_foreground(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57669c3933bf9f5eb8a330310ba7a509ea029edc02e55f406ac3f84b795389cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "warningForeground", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightThemeConfigurationUiColorPalette]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationUiColorPalette], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightThemeConfigurationUiColorPalette],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65bdad130eb5496572b1b63a028ec3174ae6807271f6f903f2bcd0caafa59925)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemePermissions",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions", "principal": "principal"},
)
class QuicksightThemePermissions:
    def __init__(
        self,
        *,
        actions: typing.Sequence[builtins.str],
        principal: builtins.str,
    ) -> None:
        '''
        :param actions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#actions QuicksightTheme#actions}.
        :param principal: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#principal QuicksightTheme#principal}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__190453c2e1402a3b6745bd76c794d0448e00adebcb008ad79948bd6f3246b734)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "principal": principal,
        }

    @builtins.property
    def actions(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#actions QuicksightTheme#actions}.'''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def principal(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#principal QuicksightTheme#principal}.'''
        result = self._values.get("principal")
        assert result is not None, "Required property 'principal' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemePermissions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightThemePermissionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemePermissionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcad7f59d22122c5bf7b22824cbff54d86e644c664acf9b99f3cf1bf3116d7af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "QuicksightThemePermissionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b39d73b4825779f8f8465a053371899776cc3d2d351dc563bb8b1d75e4806bf2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightThemePermissionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c5ba3a3d14de64bc94a7c33e82a062a2d1fe6c43b83fb028184b25854368874)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c2de763043353d63f02d414b8384cfe0c5a919fd26b0e3d6b60762f7112868d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__471be37cec573f36542e0341945e6502e966ddcd613e700bc7831f71eb7da8fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightThemePermissions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightThemePermissions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightThemePermissions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39964dfbd42cef61cb3ec57d902b22cc55367807c3e92ab6fa963981dca06cc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightThemePermissionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemePermissionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54c5bbbd2d7432d2ccf5b61d5a32bff06d3636f09de6335ae22a5dbb51e391ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="principalInput")
    def principal_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalInput"))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actions"))

    @actions.setter
    def actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d56059d21d0da08859a6fc5ef0f686b7fe61a3845ff615ef791a4a3f55dbedd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="principal")
    def principal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principal"))

    @principal.setter
    def principal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__451d4cd43c006c9966496a200f525f01f26be2693b7af8bbe96456ab6d73fa7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemePermissions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemePermissions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemePermissions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa1bb2e3761ec51f82fb523d9bf23d4fbe57f87d1394d0f2c7dcdf58caf67aa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class QuicksightThemeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#create QuicksightTheme#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#delete QuicksightTheme#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#update QuicksightTheme#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10fa624a7349879ab349e7669152967e0b61c53a23a6359af70a78b5e9b8f791)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#create QuicksightTheme#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#delete QuicksightTheme#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_theme#update QuicksightTheme#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightThemeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightTheme.QuicksightThemeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7542067818c181ba73e36383f920a82faafa9264248061492c6966c5203e1ce3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9d9938b18dbf9b41fd50c07be5bd2b9cd2b22e8e1565d82c45b0d17c6183e25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db5d789e93cc946210942ac8b07868cc316d19ece17454ca4b81043ad18c485a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8937f687386c630fe53f8f34fb86d15af70c581d0ad1d18cab4d0a7b7865b5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemeTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemeTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemeTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f43b90a9ad1342132a253f58122007a49b86d67497ce16d52f0aa7060c8fd11c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "QuicksightTheme",
    "QuicksightThemeConfig",
    "QuicksightThemeConfiguration",
    "QuicksightThemeConfigurationDataColorPalette",
    "QuicksightThemeConfigurationDataColorPaletteOutputReference",
    "QuicksightThemeConfigurationOutputReference",
    "QuicksightThemeConfigurationSheet",
    "QuicksightThemeConfigurationSheetOutputReference",
    "QuicksightThemeConfigurationSheetTile",
    "QuicksightThemeConfigurationSheetTileBorder",
    "QuicksightThemeConfigurationSheetTileBorderOutputReference",
    "QuicksightThemeConfigurationSheetTileLayout",
    "QuicksightThemeConfigurationSheetTileLayoutGutter",
    "QuicksightThemeConfigurationSheetTileLayoutGutterOutputReference",
    "QuicksightThemeConfigurationSheetTileLayoutMargin",
    "QuicksightThemeConfigurationSheetTileLayoutMarginOutputReference",
    "QuicksightThemeConfigurationSheetTileLayoutOutputReference",
    "QuicksightThemeConfigurationSheetTileOutputReference",
    "QuicksightThemeConfigurationTypography",
    "QuicksightThemeConfigurationTypographyFontFamilies",
    "QuicksightThemeConfigurationTypographyFontFamiliesList",
    "QuicksightThemeConfigurationTypographyFontFamiliesOutputReference",
    "QuicksightThemeConfigurationTypographyOutputReference",
    "QuicksightThemeConfigurationUiColorPalette",
    "QuicksightThemeConfigurationUiColorPaletteOutputReference",
    "QuicksightThemePermissions",
    "QuicksightThemePermissionsList",
    "QuicksightThemePermissionsOutputReference",
    "QuicksightThemeTimeouts",
    "QuicksightThemeTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ee134fc0a32f306bbe9fa24ed642881f4e3bd778c2c0f96e71bc6f58f901d62c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    base_theme_id: builtins.str,
    name: builtins.str,
    theme_id: builtins.str,
    aws_account_id: typing.Optional[builtins.str] = None,
    configuration: typing.Optional[typing.Union[QuicksightThemeConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightThemePermissions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[QuicksightThemeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version_description: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__acc69245597977147e9eda065bcc5c0c395c49c4c88de4779c7a522eb69637e6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cdcdb7ca8985ddc99e9fa11fa4e35a9f54b20a420eb63673450d6377979b553(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightThemePermissions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d46046d8597fc97ffe3527689c549dc9fd2c369f2d9edfbcd4e626677787c6ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__885c42e200779be97e08a8453cb9ee4e55733a98fa8aee8700d8636e5ef2cfaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a25ddfc5f309bf1d5253410daa1583b3836f1032e8a958b8b09f3c3083e0ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__059abd652a81ad69327c3655fa8ee24e0586b6a9a91a17216452480463666cb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c793062b9f7a12e14d3c1cbdebb0cf882d479cae450da1a00ea0e902dff334c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8dc9507533d07e269f6049a68ae3962f946a81a8738accb35d453fc016eb04c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f5190e574d8fb0f5a300f0f6f300bd7ff3ebf2f57cbdc5024c0921e21ccf52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__862a576ef782487fc04da7b6634bcc1ba6ef4aaabe189769cc838d8b444d4684(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b80da406ce468fb56ee4d58d1a47c5ac8195a474ec0c8a72f09236df28270077(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    base_theme_id: builtins.str,
    name: builtins.str,
    theme_id: builtins.str,
    aws_account_id: typing.Optional[builtins.str] = None,
    configuration: typing.Optional[typing.Union[QuicksightThemeConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightThemePermissions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[QuicksightThemeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716a6c3da8a867c95c9753af4453c925749043dd37d223c57c8b4197886c0b3e(
    *,
    data_color_palette: typing.Optional[typing.Union[QuicksightThemeConfigurationDataColorPalette, typing.Dict[builtins.str, typing.Any]]] = None,
    sheet: typing.Optional[typing.Union[QuicksightThemeConfigurationSheet, typing.Dict[builtins.str, typing.Any]]] = None,
    typography: typing.Optional[typing.Union[QuicksightThemeConfigurationTypography, typing.Dict[builtins.str, typing.Any]]] = None,
    ui_color_palette: typing.Optional[typing.Union[QuicksightThemeConfigurationUiColorPalette, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3818ff653239253f52b8176917be93bc465e3fddc4af05f7b1ee144022e57e5(
    *,
    colors: typing.Optional[typing.Sequence[builtins.str]] = None,
    empty_fill_color: typing.Optional[builtins.str] = None,
    min_max_gradient: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d849759e16ba4a1b1192696ac0acc1294960302cd46163d3cf801493e0a47654(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c7cc6423dab7295144e20c5d48f66a613b68e93f9c763801f8e755f1e5e7036(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be867a0ca021f5b2ca98f3f42a64fb816394e6cdff66bc01b284ca0e1bf5a91f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa879c270b4740b5566a2a475869d8db1789e2c231fa262e9cd37076bcc2b1e3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80503b26c7b2c40a2c69ca3e5d044cb036feb68b4f55cf76c4c65949e2084870(
    value: typing.Optional[QuicksightThemeConfigurationDataColorPalette],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab4921180d27dfb0d303e9d8d471ffce1bf2fa6060184ffe49ea5ffbe8a19d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d02fbba1243610ed0abf1203921ea60d44d81612b9e9cb792ac0280607f8eabf(
    value: typing.Optional[QuicksightThemeConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9cede00e2ea92d36a8d8d7218098252a0eb37271434cfc7600a38385d074776(
    *,
    tile: typing.Optional[typing.Union[QuicksightThemeConfigurationSheetTile, typing.Dict[builtins.str, typing.Any]]] = None,
    tile_layout: typing.Optional[typing.Union[QuicksightThemeConfigurationSheetTileLayout, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24ee7e4967dd8b7fe95e35a9f32f4aebb15e6978ad521ee7e6514d38a56fbcdc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__108298dfba0c01aec6407aae5e4060c9ed85dc73034ded357b4e09fda7c32aa3(
    value: typing.Optional[QuicksightThemeConfigurationSheet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc0d0dffc8db4869b2ae1a14791dbfbe3509b63f0a8d3ab3c1bb5675454609a5(
    *,
    border: typing.Optional[typing.Union[QuicksightThemeConfigurationSheetTileBorder, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0be25645d493ee3ca5141175c510ecafc6a00159bb7bc49aaa2e062cea03d8ae(
    *,
    show: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5aa49123f76879f8274a277eecd16cb45c41ff16179c03f1dd30ffdaf9d63e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88aef4cf11bf2d2b6e91e6e5b4512d89ba61cc718539d2f325ed77d24d1de852(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42602e1339bda58f2d8ebacf450429495a8c579e7b4bc81eba5b5d9506217c8a(
    value: typing.Optional[QuicksightThemeConfigurationSheetTileBorder],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b6fb17ee1fff5912318102046c3baf1c738105d388bd1f874944302f554271(
    *,
    gutter: typing.Optional[typing.Union[QuicksightThemeConfigurationSheetTileLayoutGutter, typing.Dict[builtins.str, typing.Any]]] = None,
    margin: typing.Optional[typing.Union[QuicksightThemeConfigurationSheetTileLayoutMargin, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b967b2404bae9c2d27369b4bc631d8b07e78c44adbb467b47879a2fd2075bb9f(
    *,
    show: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0109d32cf4c0cd636639175b1c76d89328889fd5a1abd67ab6b38bb43e01821c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3292ec90f6421392dafee09ef2cde2db4902eb0e6ad9548851a243acc3a700bc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b64539c68c6b31f10d8923d19585d64935a054efd9b8299d6f7a31a9f0a5fe11(
    value: typing.Optional[QuicksightThemeConfigurationSheetTileLayoutGutter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e1394f3790d73d0ad60683f1fc02a6bbb21a99f3e5e7775d24850bf54aa035c(
    *,
    show: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f41edfb4d55502da4bb586b20c9c3ec922a8623963e3f1a6898e1a3de5fd00d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c081a66da479cc105c6cdce675663b6b87e403cda45271cbecebb02bf53a7a80(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ddc6fdad3ba0efedc4b88117a6962e38c32bf384f5dc4915d4c17d8002e014(
    value: typing.Optional[QuicksightThemeConfigurationSheetTileLayoutMargin],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26c0095141b64319eaf735a727cf3f27a0ae6778079a3819a406509553d05c38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df5c458ff33583b980b09980cfb8af1ffa4b8c944e8c071c03d7afd1940d6ce5(
    value: typing.Optional[QuicksightThemeConfigurationSheetTileLayout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0469479e8fa97f4a00664f90e2fe6591be7b7c5307b2be5bd415864c43ece6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__682bbe4f008c6e0ffe9c92c946afe3a53a84dec3f3d57ac1fbd159cf7e204cb2(
    value: typing.Optional[QuicksightThemeConfigurationSheetTile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d11bb2a814c3e025aed20ea2ea86a45859dadb9aa3b89d481b3e774172d2f63(
    *,
    font_families: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightThemeConfigurationTypographyFontFamilies, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c81e0289cb375ba774cc00dc70b542280b977b6c219635bd4b4a13948a30dc86(
    *,
    font_family: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c7bb54a433f2ee3666e4f969b8cd7b6406fc40d5973598e2cff3e8135cbdea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fb24fe384a792344f41f60e92a8256952e2829b73aef6c7c79e8601fb30a662(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b28badced9dc4d7e38bb6da6f2fc85a4fbf8bb36ece0c061b356a58abd0f2e9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30896a5bbdb6229ded29f8c48a2495e0b8612ceaeaeb62af2ca9396afdeca549(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcba23099077e8c280e0afdbf0b3c8d1de1403d4abaa4e28a70abb80df39fc4c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ffe95a1b4f38c332fc40cc3359d67cde14201bd906d39253cea97a89e53a95(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightThemeConfigurationTypographyFontFamilies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa167e2ebc9ac51c60ca445da8fa5cf0b16ee8c60276425cc81123edd48435a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d47b259fe34727907b3e39b1d27d236412a30c1a2a72a049fb496bfdc8f8a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea078f6e776517c399ddb54c4614b3797ed79ffd362c749a0f21a0f099d3b053(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemeConfigurationTypographyFontFamilies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7181d24a8e18d74e42ccb5b28c8f1989c053fe8e2114264400982d336248fec3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac474130bcf4e777969015aaa44184a1f03c17b779abdb3f40229a8218077e25(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightThemeConfigurationTypographyFontFamilies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a488952e3808ee39d178beede369fb3ee32efbabdc567678ee89585f6e83e35(
    value: typing.Optional[QuicksightThemeConfigurationTypography],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__420bdb7c662a19a89fc65f2538589de688438a2c24fc436f9a6d4bf28667b8f6(
    *,
    accent: typing.Optional[builtins.str] = None,
    accent_foreground: typing.Optional[builtins.str] = None,
    danger: typing.Optional[builtins.str] = None,
    danger_foreground: typing.Optional[builtins.str] = None,
    dimension: typing.Optional[builtins.str] = None,
    dimension_foreground: typing.Optional[builtins.str] = None,
    measure: typing.Optional[builtins.str] = None,
    measure_foreground: typing.Optional[builtins.str] = None,
    primary_background: typing.Optional[builtins.str] = None,
    primary_foreground: typing.Optional[builtins.str] = None,
    secondary_background: typing.Optional[builtins.str] = None,
    secondary_foreground: typing.Optional[builtins.str] = None,
    success: typing.Optional[builtins.str] = None,
    success_foreground: typing.Optional[builtins.str] = None,
    warning: typing.Optional[builtins.str] = None,
    warning_foreground: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6679e3b4f16a1582ad0a5978de2e204be0ab312919f27c88725e149c943dd14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4fbc993ef7beea663311c3ba182736980fcda6fd3e610df8af66d51ce1a3efc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca766200d0f2543cead5246e65a1fe6c9767e42fccfb5307cb8780c05decce1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d89dcebef38b687d1bac9270b5a2e57ec7fc3b84e78d2f6d1c334bb8f9e416f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb31fbcb18105d735c751786e4bbd1270f823dcfef6372c58cedbf166b7621e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__904147790c20460c1e83dda7b926962bc8d676596a69a4dbaf9380bfbd65e57e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5bc381441211e14c60d5101333da963b713007771c646c60d0ad3fcc4282bd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374dab6077df0a87e719cadd9b26344473c7855ba15b90ea4e0093f7873f9c8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3b6d00fbffc877c40a0f609543c9291e7aacffd0bcc98c1fc7122385609bbc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bf33e512c773c7f53219929cb587c595ccd10295456e886c83a6eb4eb4aa3f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3a505fa9da85a533b1ec55163864d151f7c0d32dd0b8d03d94fcf38867269f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__447e3e7d2b2bbad8c3f69bcc8497f30f07345941fdcd459879ffbfa5902623e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__666e4d9ec0991056d676902f3e8b31668f7deabba855d5e81c81d576554518ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff004a938b348374c1d31f9e9c506aa6517bf3a5a21b39a51a1b2cb8957be81a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__921182ad9fe45bd1f21068df154a82d6177500d1bbc37c28562d081d147e38c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda9455652c8efb32ff4cf489407d840559c8d0f788488bc0dd6a1b46f49f541(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57669c3933bf9f5eb8a330310ba7a509ea029edc02e55f406ac3f84b795389cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65bdad130eb5496572b1b63a028ec3174ae6807271f6f903f2bcd0caafa59925(
    value: typing.Optional[QuicksightThemeConfigurationUiColorPalette],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__190453c2e1402a3b6745bd76c794d0448e00adebcb008ad79948bd6f3246b734(
    *,
    actions: typing.Sequence[builtins.str],
    principal: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcad7f59d22122c5bf7b22824cbff54d86e644c664acf9b99f3cf1bf3116d7af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39d73b4825779f8f8465a053371899776cc3d2d351dc563bb8b1d75e4806bf2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c5ba3a3d14de64bc94a7c33e82a062a2d1fe6c43b83fb028184b25854368874(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c2de763043353d63f02d414b8384cfe0c5a919fd26b0e3d6b60762f7112868d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__471be37cec573f36542e0341945e6502e966ddcd613e700bc7831f71eb7da8fc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39964dfbd42cef61cb3ec57d902b22cc55367807c3e92ab6fa963981dca06cc5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightThemePermissions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c5bbbd2d7432d2ccf5b61d5a32bff06d3636f09de6335ae22a5dbb51e391ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d56059d21d0da08859a6fc5ef0f686b7fe61a3845ff615ef791a4a3f55dbedd2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__451d4cd43c006c9966496a200f525f01f26be2693b7af8bbe96456ab6d73fa7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa1bb2e3761ec51f82fb523d9bf23d4fbe57f87d1394d0f2c7dcdf58caf67aa4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemePermissions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10fa624a7349879ab349e7669152967e0b61c53a23a6359af70a78b5e9b8f791(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7542067818c181ba73e36383f920a82faafa9264248061492c6966c5203e1ce3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d9938b18dbf9b41fd50c07be5bd2b9cd2b22e8e1565d82c45b0d17c6183e25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db5d789e93cc946210942ac8b07868cc316d19ece17454ca4b81043ad18c485a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8937f687386c630fe53f8f34fb86d15af70c581d0ad1d18cab4d0a7b7865b5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f43b90a9ad1342132a253f58122007a49b86d67497ce16d52f0aa7060c8fd11c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemeTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
