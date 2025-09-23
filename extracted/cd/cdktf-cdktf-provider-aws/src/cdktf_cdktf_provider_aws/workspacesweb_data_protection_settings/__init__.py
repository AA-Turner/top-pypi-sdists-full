r'''
# `aws_workspacesweb_data_protection_settings`

Refer to the Terraform Registry for docs: [`aws_workspacesweb_data_protection_settings`](https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings).
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


class WorkspaceswebDataProtectionSettings(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.workspaceswebDataProtectionSettings.WorkspaceswebDataProtectionSettings",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings aws_workspacesweb_data_protection_settings}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        display_name: builtins.str,
        additional_encryption_context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        customer_managed_key: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        inline_redaction_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkspaceswebDataProtectionSettingsInlineRedactionConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings aws_workspacesweb_data_protection_settings} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#display_name WorkspaceswebDataProtectionSettings#display_name}.
        :param additional_encryption_context: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#additional_encryption_context WorkspaceswebDataProtectionSettings#additional_encryption_context}.
        :param customer_managed_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#customer_managed_key WorkspaceswebDataProtectionSettings#customer_managed_key}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#description WorkspaceswebDataProtectionSettings#description}.
        :param inline_redaction_configuration: inline_redaction_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#inline_redaction_configuration WorkspaceswebDataProtectionSettings#inline_redaction_configuration}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#region WorkspaceswebDataProtectionSettings#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#tags WorkspaceswebDataProtectionSettings#tags}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de20a6968745e69e1e8f24c91de9c333c06ca2c1e5a557075323ff12e2f0a68b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = WorkspaceswebDataProtectionSettingsConfig(
            display_name=display_name,
            additional_encryption_context=additional_encryption_context,
            customer_managed_key=customer_managed_key,
            description=description,
            inline_redaction_configuration=inline_redaction_configuration,
            region=region,
            tags=tags,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a WorkspaceswebDataProtectionSettings resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WorkspaceswebDataProtectionSettings to import.
        :param import_from_id: The id of the existing WorkspaceswebDataProtectionSettings that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WorkspaceswebDataProtectionSettings to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46889e635d1af4f0bd917c6a8e0cc6a48c320656c1dff0e53a23751a28cbd9d7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putInlineRedactionConfiguration")
    def put_inline_redaction_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkspaceswebDataProtectionSettingsInlineRedactionConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cac933c197336add193029f15653bc26688049cb69ea6b32476f1f1087d2c7c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInlineRedactionConfiguration", [value]))

    @jsii.member(jsii_name="resetAdditionalEncryptionContext")
    def reset_additional_encryption_context(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalEncryptionContext", []))

    @jsii.member(jsii_name="resetCustomerManagedKey")
    def reset_customer_managed_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerManagedKey", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetInlineRedactionConfiguration")
    def reset_inline_redaction_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInlineRedactionConfiguration", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="associatedPortalArns")
    def associated_portal_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "associatedPortalArns"))

    @builtins.property
    @jsii.member(jsii_name="dataProtectionSettingsArn")
    def data_protection_settings_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataProtectionSettingsArn"))

    @builtins.property
    @jsii.member(jsii_name="inlineRedactionConfiguration")
    def inline_redaction_configuration(
        self,
    ) -> "WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationList":
        return typing.cast("WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationList", jsii.get(self, "inlineRedactionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tagsAll"))

    @builtins.property
    @jsii.member(jsii_name="additionalEncryptionContextInput")
    def additional_encryption_context_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "additionalEncryptionContextInput"))

    @builtins.property
    @jsii.member(jsii_name="customerManagedKeyInput")
    def customer_managed_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customerManagedKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="inlineRedactionConfigurationInput")
    def inline_redaction_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebDataProtectionSettingsInlineRedactionConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebDataProtectionSettingsInlineRedactionConfiguration"]]], jsii.get(self, "inlineRedactionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalEncryptionContext")
    def additional_encryption_context(
        self,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "additionalEncryptionContext"))

    @additional_encryption_context.setter
    def additional_encryption_context(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__880de5337f72e8bbc24925c209c03cf95c16bae3287c611446d34fec0a037aad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalEncryptionContext", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customerManagedKey")
    def customer_managed_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerManagedKey"))

    @customer_managed_key.setter
    def customer_managed_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a866e24f63a70755970bbeaabbe3b34f4b77c099eeeb000631261fc68a61c3d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerManagedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef2fb100a131b7faac85ced907663f692a3e3f733af3ead83fe7ea42f7205d98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6667c2f75d81c92e0445776b755caa849d5a6eefa5392980b4ee4d4f23b326b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2841cf45ccdf8366f8b62175600614ff238a1ebd3335ac2250dabf332eb9d19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b047cf75f5608a4fbeac52cb087e63ad1389660e239c250fde9a9e4f2fe7d003)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.workspaceswebDataProtectionSettings.WorkspaceswebDataProtectionSettingsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "display_name": "displayName",
        "additional_encryption_context": "additionalEncryptionContext",
        "customer_managed_key": "customerManagedKey",
        "description": "description",
        "inline_redaction_configuration": "inlineRedactionConfiguration",
        "region": "region",
        "tags": "tags",
    },
)
class WorkspaceswebDataProtectionSettingsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        display_name: builtins.str,
        additional_encryption_context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        customer_managed_key: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        inline_redaction_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkspaceswebDataProtectionSettingsInlineRedactionConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#display_name WorkspaceswebDataProtectionSettings#display_name}.
        :param additional_encryption_context: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#additional_encryption_context WorkspaceswebDataProtectionSettings#additional_encryption_context}.
        :param customer_managed_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#customer_managed_key WorkspaceswebDataProtectionSettings#customer_managed_key}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#description WorkspaceswebDataProtectionSettings#description}.
        :param inline_redaction_configuration: inline_redaction_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#inline_redaction_configuration WorkspaceswebDataProtectionSettings#inline_redaction_configuration}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#region WorkspaceswebDataProtectionSettings#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#tags WorkspaceswebDataProtectionSettings#tags}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4dff913e156dcdb0839ef3eb9a34c0c0b1e6e27d4aa33343b50b096ac8b2923)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument additional_encryption_context", value=additional_encryption_context, expected_type=type_hints["additional_encryption_context"])
            check_type(argname="argument customer_managed_key", value=customer_managed_key, expected_type=type_hints["customer_managed_key"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument inline_redaction_configuration", value=inline_redaction_configuration, expected_type=type_hints["inline_redaction_configuration"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
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
        if additional_encryption_context is not None:
            self._values["additional_encryption_context"] = additional_encryption_context
        if customer_managed_key is not None:
            self._values["customer_managed_key"] = customer_managed_key
        if description is not None:
            self._values["description"] = description
        if inline_redaction_configuration is not None:
            self._values["inline_redaction_configuration"] = inline_redaction_configuration
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags

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
    def display_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#display_name WorkspaceswebDataProtectionSettings#display_name}.'''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_encryption_context(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#additional_encryption_context WorkspaceswebDataProtectionSettings#additional_encryption_context}.'''
        result = self._values.get("additional_encryption_context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def customer_managed_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#customer_managed_key WorkspaceswebDataProtectionSettings#customer_managed_key}.'''
        result = self._values.get("customer_managed_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#description WorkspaceswebDataProtectionSettings#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inline_redaction_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebDataProtectionSettingsInlineRedactionConfiguration"]]]:
        '''inline_redaction_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#inline_redaction_configuration WorkspaceswebDataProtectionSettings#inline_redaction_configuration}
        '''
        result = self._values.get("inline_redaction_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebDataProtectionSettingsInlineRedactionConfiguration"]]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#region WorkspaceswebDataProtectionSettings#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#tags WorkspaceswebDataProtectionSettings#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspaceswebDataProtectionSettingsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.workspaceswebDataProtectionSettings.WorkspaceswebDataProtectionSettingsInlineRedactionConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "global_confidence_level": "globalConfidenceLevel",
        "global_enforced_urls": "globalEnforcedUrls",
        "global_exempt_urls": "globalExemptUrls",
        "inline_redaction_pattern": "inlineRedactionPattern",
    },
)
class WorkspaceswebDataProtectionSettingsInlineRedactionConfiguration:
    def __init__(
        self,
        *,
        global_confidence_level: typing.Optional[jsii.Number] = None,
        global_enforced_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
        global_exempt_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
        inline_redaction_pattern: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPattern", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param global_confidence_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#global_confidence_level WorkspaceswebDataProtectionSettings#global_confidence_level}.
        :param global_enforced_urls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#global_enforced_urls WorkspaceswebDataProtectionSettings#global_enforced_urls}.
        :param global_exempt_urls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#global_exempt_urls WorkspaceswebDataProtectionSettings#global_exempt_urls}.
        :param inline_redaction_pattern: inline_redaction_pattern block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#inline_redaction_pattern WorkspaceswebDataProtectionSettings#inline_redaction_pattern}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6f549d3f9d402e392dceb98a4b4ed6040586063134a6bb31fdb4e326a6b044c)
            check_type(argname="argument global_confidence_level", value=global_confidence_level, expected_type=type_hints["global_confidence_level"])
            check_type(argname="argument global_enforced_urls", value=global_enforced_urls, expected_type=type_hints["global_enforced_urls"])
            check_type(argname="argument global_exempt_urls", value=global_exempt_urls, expected_type=type_hints["global_exempt_urls"])
            check_type(argname="argument inline_redaction_pattern", value=inline_redaction_pattern, expected_type=type_hints["inline_redaction_pattern"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if global_confidence_level is not None:
            self._values["global_confidence_level"] = global_confidence_level
        if global_enforced_urls is not None:
            self._values["global_enforced_urls"] = global_enforced_urls
        if global_exempt_urls is not None:
            self._values["global_exempt_urls"] = global_exempt_urls
        if inline_redaction_pattern is not None:
            self._values["inline_redaction_pattern"] = inline_redaction_pattern

    @builtins.property
    def global_confidence_level(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#global_confidence_level WorkspaceswebDataProtectionSettings#global_confidence_level}.'''
        result = self._values.get("global_confidence_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def global_enforced_urls(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#global_enforced_urls WorkspaceswebDataProtectionSettings#global_enforced_urls}.'''
        result = self._values.get("global_enforced_urls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def global_exempt_urls(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#global_exempt_urls WorkspaceswebDataProtectionSettings#global_exempt_urls}.'''
        result = self._values.get("global_exempt_urls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def inline_redaction_pattern(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPattern"]]]:
        '''inline_redaction_pattern block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#inline_redaction_pattern WorkspaceswebDataProtectionSettings#inline_redaction_pattern}
        '''
        result = self._values.get("inline_redaction_pattern")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPattern"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspaceswebDataProtectionSettingsInlineRedactionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.workspaceswebDataProtectionSettings.WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPattern",
    jsii_struct_bases=[],
    name_mapping={
        "built_in_pattern_id": "builtInPatternId",
        "confidence_level": "confidenceLevel",
        "custom_pattern": "customPattern",
        "enforced_urls": "enforcedUrls",
        "exempt_urls": "exemptUrls",
        "redaction_place_holder": "redactionPlaceHolder",
    },
)
class WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPattern:
    def __init__(
        self,
        *,
        built_in_pattern_id: typing.Optional[builtins.str] = None,
        confidence_level: typing.Optional[jsii.Number] = None,
        custom_pattern: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPattern", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enforced_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
        exempt_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
        redaction_place_holder: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolder", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param built_in_pattern_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#built_in_pattern_id WorkspaceswebDataProtectionSettings#built_in_pattern_id}.
        :param confidence_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#confidence_level WorkspaceswebDataProtectionSettings#confidence_level}.
        :param custom_pattern: custom_pattern block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#custom_pattern WorkspaceswebDataProtectionSettings#custom_pattern}
        :param enforced_urls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#enforced_urls WorkspaceswebDataProtectionSettings#enforced_urls}.
        :param exempt_urls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#exempt_urls WorkspaceswebDataProtectionSettings#exempt_urls}.
        :param redaction_place_holder: redaction_place_holder block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#redaction_place_holder WorkspaceswebDataProtectionSettings#redaction_place_holder}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__805493039ac7b56952059d34324d6a9d8dc0c0e007868f92f277c1c69e626c9c)
            check_type(argname="argument built_in_pattern_id", value=built_in_pattern_id, expected_type=type_hints["built_in_pattern_id"])
            check_type(argname="argument confidence_level", value=confidence_level, expected_type=type_hints["confidence_level"])
            check_type(argname="argument custom_pattern", value=custom_pattern, expected_type=type_hints["custom_pattern"])
            check_type(argname="argument enforced_urls", value=enforced_urls, expected_type=type_hints["enforced_urls"])
            check_type(argname="argument exempt_urls", value=exempt_urls, expected_type=type_hints["exempt_urls"])
            check_type(argname="argument redaction_place_holder", value=redaction_place_holder, expected_type=type_hints["redaction_place_holder"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if built_in_pattern_id is not None:
            self._values["built_in_pattern_id"] = built_in_pattern_id
        if confidence_level is not None:
            self._values["confidence_level"] = confidence_level
        if custom_pattern is not None:
            self._values["custom_pattern"] = custom_pattern
        if enforced_urls is not None:
            self._values["enforced_urls"] = enforced_urls
        if exempt_urls is not None:
            self._values["exempt_urls"] = exempt_urls
        if redaction_place_holder is not None:
            self._values["redaction_place_holder"] = redaction_place_holder

    @builtins.property
    def built_in_pattern_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#built_in_pattern_id WorkspaceswebDataProtectionSettings#built_in_pattern_id}.'''
        result = self._values.get("built_in_pattern_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def confidence_level(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#confidence_level WorkspaceswebDataProtectionSettings#confidence_level}.'''
        result = self._values.get("confidence_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def custom_pattern(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPattern"]]]:
        '''custom_pattern block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#custom_pattern WorkspaceswebDataProtectionSettings#custom_pattern}
        '''
        result = self._values.get("custom_pattern")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPattern"]]], result)

    @builtins.property
    def enforced_urls(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#enforced_urls WorkspaceswebDataProtectionSettings#enforced_urls}.'''
        result = self._values.get("enforced_urls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exempt_urls(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#exempt_urls WorkspaceswebDataProtectionSettings#exempt_urls}.'''
        result = self._values.get("exempt_urls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def redaction_place_holder(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolder"]]]:
        '''redaction_place_holder block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#redaction_place_holder WorkspaceswebDataProtectionSettings#redaction_place_holder}
        '''
        result = self._values.get("redaction_place_holder")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolder"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPattern(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.workspaceswebDataProtectionSettings.WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPattern",
    jsii_struct_bases=[],
    name_mapping={
        "pattern_name": "patternName",
        "pattern_regex": "patternRegex",
        "keyword_regex": "keywordRegex",
        "pattern_description": "patternDescription",
    },
)
class WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPattern:
    def __init__(
        self,
        *,
        pattern_name: builtins.str,
        pattern_regex: builtins.str,
        keyword_regex: typing.Optional[builtins.str] = None,
        pattern_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pattern_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#pattern_name WorkspaceswebDataProtectionSettings#pattern_name}.
        :param pattern_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#pattern_regex WorkspaceswebDataProtectionSettings#pattern_regex}.
        :param keyword_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#keyword_regex WorkspaceswebDataProtectionSettings#keyword_regex}.
        :param pattern_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#pattern_description WorkspaceswebDataProtectionSettings#pattern_description}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cd2cfb238551cae37d4c5f3d859825655533ab4f91daf665d11d2ec46d34e32)
            check_type(argname="argument pattern_name", value=pattern_name, expected_type=type_hints["pattern_name"])
            check_type(argname="argument pattern_regex", value=pattern_regex, expected_type=type_hints["pattern_regex"])
            check_type(argname="argument keyword_regex", value=keyword_regex, expected_type=type_hints["keyword_regex"])
            check_type(argname="argument pattern_description", value=pattern_description, expected_type=type_hints["pattern_description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pattern_name": pattern_name,
            "pattern_regex": pattern_regex,
        }
        if keyword_regex is not None:
            self._values["keyword_regex"] = keyword_regex
        if pattern_description is not None:
            self._values["pattern_description"] = pattern_description

    @builtins.property
    def pattern_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#pattern_name WorkspaceswebDataProtectionSettings#pattern_name}.'''
        result = self._values.get("pattern_name")
        assert result is not None, "Required property 'pattern_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pattern_regex(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#pattern_regex WorkspaceswebDataProtectionSettings#pattern_regex}.'''
        result = self._values.get("pattern_regex")
        assert result is not None, "Required property 'pattern_regex' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def keyword_regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#keyword_regex WorkspaceswebDataProtectionSettings#keyword_regex}.'''
        result = self._values.get("keyword_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pattern_description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#pattern_description WorkspaceswebDataProtectionSettings#pattern_description}.'''
        result = self._values.get("pattern_description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPattern(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPatternList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.workspaceswebDataProtectionSettings.WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPatternList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdce75c791e06a13c25843afc71f8b8c8dd5c23de54dd500d2828c2d7a644930)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPatternOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebb1ba835bf0708f212453dd6335d93e2e57aba3e8bd3bc7e988693fab5b7139)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPatternOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4f5741aa01384df9ab7618153a185249f3bc74f8fb2348c22b851c98bb457d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8df064618dc620c4f87a57f44ea9b3419739053cf6d1a390b21d54b92ca268a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ecc4fa8d9a91cd7f2575ce810558b158772feacc48c9de75377e9fcacfea793)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPattern]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPattern]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPattern]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbdf304afde3c0fc2134e0ac79a5e952a2fa491cf5cec1c220c701be69463d8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPatternOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.workspaceswebDataProtectionSettings.WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPatternOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41176d7f0a7f74763e787a8c40888b65accff2e30b432f601951dd3dfe72e41e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKeywordRegex")
    def reset_keyword_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeywordRegex", []))

    @jsii.member(jsii_name="resetPatternDescription")
    def reset_pattern_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPatternDescription", []))

    @builtins.property
    @jsii.member(jsii_name="keywordRegexInput")
    def keyword_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keywordRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="patternDescriptionInput")
    def pattern_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="patternNameInput")
    def pattern_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternNameInput"))

    @builtins.property
    @jsii.member(jsii_name="patternRegexInput")
    def pattern_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="keywordRegex")
    def keyword_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keywordRegex"))

    @keyword_regex.setter
    def keyword_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e81473705e662cd5e4e66c39d9d619068b9375090315ff71c391e235f3704ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keywordRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="patternDescription")
    def pattern_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "patternDescription"))

    @pattern_description.setter
    def pattern_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bed98c1d95a60778ed0b66f8096675c48d03d8a0df3e72b9762675c5bdb6e266)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "patternDescription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="patternName")
    def pattern_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "patternName"))

    @pattern_name.setter
    def pattern_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fffc667784d3b6a76fc8454e75d92b0e1e7a85596429df92179243c195cb87f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "patternName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="patternRegex")
    def pattern_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "patternRegex"))

    @pattern_regex.setter
    def pattern_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c10c4b89cd2fe86e1a3c784ed7b88165374bc47497ed794ad056e4b12d2e57f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "patternRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPattern]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPattern]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPattern]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e60e1798e0a3538324506702d73e6d9b36deb8393870b4de003ab559b9c82521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.workspaceswebDataProtectionSettings.WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a9625d544203c16ed2c71659d16f8ae13e748712ec1ddea25987600f0f4896c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7fb74551641fa7c16af8e62d0af7278ad4ea6ad6717a11b606256f76b7a6516)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e6476eef597e120f37800b9c708b24dd33c22f0674109a18155f8dd8a65bc26)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec3f4a3ef297550e413de79f4cf13b201ed487585ac135e1f3d27e42acb76c91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9741b998d68cfd81ba456aab5e9cfb536bb53e7352a98a16408f1c147c38d949)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPattern]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPattern]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPattern]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff14136fb30ff36905c667658491035894aa4e37f8c6fbe08b593452db2b0d44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.workspaceswebDataProtectionSettings.WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17681d60dd84d2913258df6abcb2cce9f051fc4af38cf8d8a8135e5ca637dd2e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCustomPattern")
    def put_custom_pattern(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPattern, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__491b4c54aac755c9ca5f235db7a121fe81e531475992a02c1a1ac92d4f547ec4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomPattern", [value]))

    @jsii.member(jsii_name="putRedactionPlaceHolder")
    def put_redaction_place_holder(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolder", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab4d1c81e31ef1626435cbb71ed33df73174bcbea05fc3770f398ef1e7f484f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRedactionPlaceHolder", [value]))

    @jsii.member(jsii_name="resetBuiltInPatternId")
    def reset_built_in_pattern_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuiltInPatternId", []))

    @jsii.member(jsii_name="resetConfidenceLevel")
    def reset_confidence_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidenceLevel", []))

    @jsii.member(jsii_name="resetCustomPattern")
    def reset_custom_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomPattern", []))

    @jsii.member(jsii_name="resetEnforcedUrls")
    def reset_enforced_urls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforcedUrls", []))

    @jsii.member(jsii_name="resetExemptUrls")
    def reset_exempt_urls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExemptUrls", []))

    @jsii.member(jsii_name="resetRedactionPlaceHolder")
    def reset_redaction_place_holder(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedactionPlaceHolder", []))

    @builtins.property
    @jsii.member(jsii_name="customPattern")
    def custom_pattern(
        self,
    ) -> WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPatternList:
        return typing.cast(WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPatternList, jsii.get(self, "customPattern"))

    @builtins.property
    @jsii.member(jsii_name="redactionPlaceHolder")
    def redaction_place_holder(
        self,
    ) -> "WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolderList":
        return typing.cast("WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolderList", jsii.get(self, "redactionPlaceHolder"))

    @builtins.property
    @jsii.member(jsii_name="builtInPatternIdInput")
    def built_in_pattern_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "builtInPatternIdInput"))

    @builtins.property
    @jsii.member(jsii_name="confidenceLevelInput")
    def confidence_level_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "confidenceLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="customPatternInput")
    def custom_pattern_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPattern]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPattern]]], jsii.get(self, "customPatternInput"))

    @builtins.property
    @jsii.member(jsii_name="enforcedUrlsInput")
    def enforced_urls_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "enforcedUrlsInput"))

    @builtins.property
    @jsii.member(jsii_name="exemptUrlsInput")
    def exempt_urls_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exemptUrlsInput"))

    @builtins.property
    @jsii.member(jsii_name="redactionPlaceHolderInput")
    def redaction_place_holder_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolder"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolder"]]], jsii.get(self, "redactionPlaceHolderInput"))

    @builtins.property
    @jsii.member(jsii_name="builtInPatternId")
    def built_in_pattern_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "builtInPatternId"))

    @built_in_pattern_id.setter
    def built_in_pattern_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__148aa7637c2173d8b2b69f928329aae9e57caed53344afa89ef17573b0dcdc4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "builtInPatternId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="confidenceLevel")
    def confidence_level(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "confidenceLevel"))

    @confidence_level.setter
    def confidence_level(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0bfbc2e6f3415dad7bfe4502bec3f62142fedee9042c8e3c27ac9620a542a63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidenceLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforcedUrls")
    def enforced_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "enforcedUrls"))

    @enforced_urls.setter
    def enforced_urls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd852a18f47437a026aa4155ed9341046aa03479719b8bc3269e486322043d4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforcedUrls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exemptUrls")
    def exempt_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exemptUrls"))

    @exempt_urls.setter
    def exempt_urls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a578bb67d4b5459ebcb96ac0f7f6d8cc77fee4cb002eaf73bfe697b31e498aca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exemptUrls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPattern]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPattern]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPattern]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21cd6e65ed8949c2cd54032fa3d1d4d4f6b0aff09361172b33f04c4ca8997437)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.workspaceswebDataProtectionSettings.WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolder",
    jsii_struct_bases=[],
    name_mapping={
        "redaction_place_holder_type": "redactionPlaceHolderType",
        "redaction_place_holder_text": "redactionPlaceHolderText",
    },
)
class WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolder:
    def __init__(
        self,
        *,
        redaction_place_holder_type: builtins.str,
        redaction_place_holder_text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param redaction_place_holder_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#redaction_place_holder_type WorkspaceswebDataProtectionSettings#redaction_place_holder_type}.
        :param redaction_place_holder_text: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#redaction_place_holder_text WorkspaceswebDataProtectionSettings#redaction_place_holder_text}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ecd6fc81ac0142e54d4bc19038a23751a12eea0fce54482b8426493b808fa1)
            check_type(argname="argument redaction_place_holder_type", value=redaction_place_holder_type, expected_type=type_hints["redaction_place_holder_type"])
            check_type(argname="argument redaction_place_holder_text", value=redaction_place_holder_text, expected_type=type_hints["redaction_place_holder_text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "redaction_place_holder_type": redaction_place_holder_type,
        }
        if redaction_place_holder_text is not None:
            self._values["redaction_place_holder_text"] = redaction_place_holder_text

    @builtins.property
    def redaction_place_holder_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#redaction_place_holder_type WorkspaceswebDataProtectionSettings#redaction_place_holder_type}.'''
        result = self._values.get("redaction_place_holder_type")
        assert result is not None, "Required property 'redaction_place_holder_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def redaction_place_holder_text(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_data_protection_settings#redaction_place_holder_text WorkspaceswebDataProtectionSettings#redaction_place_holder_text}.'''
        result = self._values.get("redaction_place_holder_text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolder(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.workspaceswebDataProtectionSettings.WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0be26b29c4e10c51fc08fc95151961a27ca9ae4296d03cf7fac7950b6d120422)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__067ada90df1af0356e1babc093d4a8ae6893d0756a70d52375b1854b1e912d74)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d3391ff70eb31857aded869f4bd62249f25396512bd4ad979c96c2a187088b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19b4f561ea0e761881a4773411049eb2158e926b43fa09a51d544b7c9685a9c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6478fb67b069c8d8f0d2fc1349d8196358e77078bec54e04cf4c4ec134654edb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolder]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolder]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolder]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8bac106025d2ebfb865dc98954620859d41152c639aa955d40b87a08775b728)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.workspaceswebDataProtectionSettings.WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0a54753e87ec7dc2d200c30005ed70ec78d85a25d27e667830bd63a23932a69)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetRedactionPlaceHolderText")
    def reset_redaction_place_holder_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedactionPlaceHolderText", []))

    @builtins.property
    @jsii.member(jsii_name="redactionPlaceHolderTextInput")
    def redaction_place_holder_text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redactionPlaceHolderTextInput"))

    @builtins.property
    @jsii.member(jsii_name="redactionPlaceHolderTypeInput")
    def redaction_place_holder_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redactionPlaceHolderTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="redactionPlaceHolderText")
    def redaction_place_holder_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redactionPlaceHolderText"))

    @redaction_place_holder_text.setter
    def redaction_place_holder_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8a0571bc5f3c39428f6e8edc1e453b17a08b8c69171a6caa405e53687a73b57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redactionPlaceHolderText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redactionPlaceHolderType")
    def redaction_place_holder_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redactionPlaceHolderType"))

    @redaction_place_holder_type.setter
    def redaction_place_holder_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79b4d289214838ce47628208f25d7c8c429ef6528fd28385e4a51ed5157eaa3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redactionPlaceHolderType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolder]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolder]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolder]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c18a67d5a41a0efe60d4a07ccbf286a935e299fbfded1b66f8a642c013dae053)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.workspaceswebDataProtectionSettings.WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f598f3a72ae8f604aba75a6c0139b5808a305811a36377b9ebb701c34514426)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25bb822c5c9e34ad50a0fa4f7a8e00876525262b87a2259aad0c0ad1783571c3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d21ec1f468819129331cbef29afdeb4592ead14faaf97ae9a08d2a8acce90f73)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddc7b43272dadfac6494027cc52e85aa06381bb22747203fec748d5419aabd87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c5981c5a7a85c453c22479194cdf6cd8b3a870be5bf018432f8b64d68b2ca68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebDataProtectionSettingsInlineRedactionConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebDataProtectionSettingsInlineRedactionConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebDataProtectionSettingsInlineRedactionConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b0cbd1643b5b0b98ea4fe435ba7884a549095e249084e9bd079efb0d1ab9294)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.workspaceswebDataProtectionSettings.WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5460495724a37db8000d897a42824dece3ea4f030f973e4cd29e00030cb8acb2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putInlineRedactionPattern")
    def put_inline_redaction_pattern(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPattern, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e00c015cd14b0e4007e863db430ead463d93b49fdd7de6509d90ba67c920d956)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInlineRedactionPattern", [value]))

    @jsii.member(jsii_name="resetGlobalConfidenceLevel")
    def reset_global_confidence_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGlobalConfidenceLevel", []))

    @jsii.member(jsii_name="resetGlobalEnforcedUrls")
    def reset_global_enforced_urls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGlobalEnforcedUrls", []))

    @jsii.member(jsii_name="resetGlobalExemptUrls")
    def reset_global_exempt_urls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGlobalExemptUrls", []))

    @jsii.member(jsii_name="resetInlineRedactionPattern")
    def reset_inline_redaction_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInlineRedactionPattern", []))

    @builtins.property
    @jsii.member(jsii_name="inlineRedactionPattern")
    def inline_redaction_pattern(
        self,
    ) -> WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternList:
        return typing.cast(WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternList, jsii.get(self, "inlineRedactionPattern"))

    @builtins.property
    @jsii.member(jsii_name="globalConfidenceLevelInput")
    def global_confidence_level_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "globalConfidenceLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="globalEnforcedUrlsInput")
    def global_enforced_urls_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "globalEnforcedUrlsInput"))

    @builtins.property
    @jsii.member(jsii_name="globalExemptUrlsInput")
    def global_exempt_urls_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "globalExemptUrlsInput"))

    @builtins.property
    @jsii.member(jsii_name="inlineRedactionPatternInput")
    def inline_redaction_pattern_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPattern]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPattern]]], jsii.get(self, "inlineRedactionPatternInput"))

    @builtins.property
    @jsii.member(jsii_name="globalConfidenceLevel")
    def global_confidence_level(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "globalConfidenceLevel"))

    @global_confidence_level.setter
    def global_confidence_level(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__705dc9aa435160ffc605fe370775c92485c6d8db06cc513e5763691f85ee1839)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "globalConfidenceLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="globalEnforcedUrls")
    def global_enforced_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "globalEnforcedUrls"))

    @global_enforced_urls.setter
    def global_enforced_urls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaa405939b8465b220ca9832ac15a6f309b73eef22aa27b81314931266518233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "globalEnforcedUrls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="globalExemptUrls")
    def global_exempt_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "globalExemptUrls"))

    @global_exempt_urls.setter
    def global_exempt_urls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c43d7419bfc3e94befe78920ac4ba351714f8cf8970ea16cd79b951d351ba32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "globalExemptUrls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebDataProtectionSettingsInlineRedactionConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebDataProtectionSettingsInlineRedactionConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebDataProtectionSettingsInlineRedactionConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__993b276391c7904dd8aeb991f262f636e22c18841aed3c30d241593d39bf0eb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "WorkspaceswebDataProtectionSettings",
    "WorkspaceswebDataProtectionSettingsConfig",
    "WorkspaceswebDataProtectionSettingsInlineRedactionConfiguration",
    "WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPattern",
    "WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPattern",
    "WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPatternList",
    "WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPatternOutputReference",
    "WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternList",
    "WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternOutputReference",
    "WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolder",
    "WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolderList",
    "WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolderOutputReference",
    "WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationList",
    "WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__de20a6968745e69e1e8f24c91de9c333c06ca2c1e5a557075323ff12e2f0a68b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    display_name: builtins.str,
    additional_encryption_context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    customer_managed_key: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    inline_redaction_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkspaceswebDataProtectionSettingsInlineRedactionConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__46889e635d1af4f0bd917c6a8e0cc6a48c320656c1dff0e53a23751a28cbd9d7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cac933c197336add193029f15653bc26688049cb69ea6b32476f1f1087d2c7c1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkspaceswebDataProtectionSettingsInlineRedactionConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880de5337f72e8bbc24925c209c03cf95c16bae3287c611446d34fec0a037aad(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a866e24f63a70755970bbeaabbe3b34f4b77c099eeeb000631261fc68a61c3d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef2fb100a131b7faac85ced907663f692a3e3f733af3ead83fe7ea42f7205d98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6667c2f75d81c92e0445776b755caa849d5a6eefa5392980b4ee4d4f23b326b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2841cf45ccdf8366f8b62175600614ff238a1ebd3335ac2250dabf332eb9d19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b047cf75f5608a4fbeac52cb087e63ad1389660e239c250fde9a9e4f2fe7d003(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4dff913e156dcdb0839ef3eb9a34c0c0b1e6e27d4aa33343b50b096ac8b2923(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    additional_encryption_context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    customer_managed_key: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    inline_redaction_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkspaceswebDataProtectionSettingsInlineRedactionConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f549d3f9d402e392dceb98a4b4ed6040586063134a6bb31fdb4e326a6b044c(
    *,
    global_confidence_level: typing.Optional[jsii.Number] = None,
    global_enforced_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    global_exempt_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    inline_redaction_pattern: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPattern, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__805493039ac7b56952059d34324d6a9d8dc0c0e007868f92f277c1c69e626c9c(
    *,
    built_in_pattern_id: typing.Optional[builtins.str] = None,
    confidence_level: typing.Optional[jsii.Number] = None,
    custom_pattern: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPattern, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enforced_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    exempt_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    redaction_place_holder: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolder, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cd2cfb238551cae37d4c5f3d859825655533ab4f91daf665d11d2ec46d34e32(
    *,
    pattern_name: builtins.str,
    pattern_regex: builtins.str,
    keyword_regex: typing.Optional[builtins.str] = None,
    pattern_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdce75c791e06a13c25843afc71f8b8c8dd5c23de54dd500d2828c2d7a644930(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebb1ba835bf0708f212453dd6335d93e2e57aba3e8bd3bc7e988693fab5b7139(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4f5741aa01384df9ab7618153a185249f3bc74f8fb2348c22b851c98bb457d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8df064618dc620c4f87a57f44ea9b3419739053cf6d1a390b21d54b92ca268a4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ecc4fa8d9a91cd7f2575ce810558b158772feacc48c9de75377e9fcacfea793(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbdf304afde3c0fc2134e0ac79a5e952a2fa491cf5cec1c220c701be69463d8b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPattern]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41176d7f0a7f74763e787a8c40888b65accff2e30b432f601951dd3dfe72e41e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e81473705e662cd5e4e66c39d9d619068b9375090315ff71c391e235f3704ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed98c1d95a60778ed0b66f8096675c48d03d8a0df3e72b9762675c5bdb6e266(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fffc667784d3b6a76fc8454e75d92b0e1e7a85596429df92179243c195cb87f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c10c4b89cd2fe86e1a3c784ed7b88165374bc47497ed794ad056e4b12d2e57f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e60e1798e0a3538324506702d73e6d9b36deb8393870b4de003ab559b9c82521(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPattern]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a9625d544203c16ed2c71659d16f8ae13e748712ec1ddea25987600f0f4896c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7fb74551641fa7c16af8e62d0af7278ad4ea6ad6717a11b606256f76b7a6516(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e6476eef597e120f37800b9c708b24dd33c22f0674109a18155f8dd8a65bc26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec3f4a3ef297550e413de79f4cf13b201ed487585ac135e1f3d27e42acb76c91(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9741b998d68cfd81ba456aab5e9cfb536bb53e7352a98a16408f1c147c38d949(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff14136fb30ff36905c667658491035894aa4e37f8c6fbe08b593452db2b0d44(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPattern]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17681d60dd84d2913258df6abcb2cce9f051fc4af38cf8d8a8135e5ca637dd2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__491b4c54aac755c9ca5f235db7a121fe81e531475992a02c1a1ac92d4f547ec4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternCustomPattern, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab4d1c81e31ef1626435cbb71ed33df73174bcbea05fc3770f398ef1e7f484f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolder, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__148aa7637c2173d8b2b69f928329aae9e57caed53344afa89ef17573b0dcdc4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0bfbc2e6f3415dad7bfe4502bec3f62142fedee9042c8e3c27ac9620a542a63(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd852a18f47437a026aa4155ed9341046aa03479719b8bc3269e486322043d4c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a578bb67d4b5459ebcb96ac0f7f6d8cc77fee4cb002eaf73bfe697b31e498aca(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21cd6e65ed8949c2cd54032fa3d1d4d4f6b0aff09361172b33f04c4ca8997437(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPattern]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ecd6fc81ac0142e54d4bc19038a23751a12eea0fce54482b8426493b808fa1(
    *,
    redaction_place_holder_type: builtins.str,
    redaction_place_holder_text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0be26b29c4e10c51fc08fc95151961a27ca9ae4296d03cf7fac7950b6d120422(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__067ada90df1af0356e1babc093d4a8ae6893d0756a70d52375b1854b1e912d74(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d3391ff70eb31857aded869f4bd62249f25396512bd4ad979c96c2a187088b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19b4f561ea0e761881a4773411049eb2158e926b43fa09a51d544b7c9685a9c1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6478fb67b069c8d8f0d2fc1349d8196358e77078bec54e04cf4c4ec134654edb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8bac106025d2ebfb865dc98954620859d41152c639aa955d40b87a08775b728(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolder]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0a54753e87ec7dc2d200c30005ed70ec78d85a25d27e667830bd63a23932a69(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a0571bc5f3c39428f6e8edc1e453b17a08b8c69171a6caa405e53687a73b57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79b4d289214838ce47628208f25d7c8c429ef6528fd28385e4a51ed5157eaa3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c18a67d5a41a0efe60d4a07ccbf286a935e299fbfded1b66f8a642c013dae053(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPatternRedactionPlaceHolder]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f598f3a72ae8f604aba75a6c0139b5808a305811a36377b9ebb701c34514426(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25bb822c5c9e34ad50a0fa4f7a8e00876525262b87a2259aad0c0ad1783571c3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d21ec1f468819129331cbef29afdeb4592ead14faaf97ae9a08d2a8acce90f73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddc7b43272dadfac6494027cc52e85aa06381bb22747203fec748d5419aabd87(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c5981c5a7a85c453c22479194cdf6cd8b3a870be5bf018432f8b64d68b2ca68(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b0cbd1643b5b0b98ea4fe435ba7884a549095e249084e9bd079efb0d1ab9294(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebDataProtectionSettingsInlineRedactionConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5460495724a37db8000d897a42824dece3ea4f030f973e4cd29e00030cb8acb2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e00c015cd14b0e4007e863db430ead463d93b49fdd7de6509d90ba67c920d956(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkspaceswebDataProtectionSettingsInlineRedactionConfigurationInlineRedactionPattern, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__705dc9aa435160ffc605fe370775c92485c6d8db06cc513e5763691f85ee1839(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa405939b8465b220ca9832ac15a6f309b73eef22aa27b81314931266518233(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c43d7419bfc3e94befe78920ac4ba351714f8cf8970ea16cd79b951d351ba32(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__993b276391c7904dd8aeb991f262f636e22c18841aed3c30d241593d39bf0eb5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebDataProtectionSettingsInlineRedactionConfiguration]],
) -> None:
    """Type checking stubs"""
    pass
