r'''
# `datadog_organization_settings`

Refer to the Terraform Registry for docs: [`datadog_organization_settings`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings).
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


class OrganizationSettings(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.organizationSettings.OrganizationSettings",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings datadog_organization_settings}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        security_contacts: typing.Optional[typing.Sequence[builtins.str]] = None,
        settings: typing.Optional[typing.Union["OrganizationSettingsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings datadog_organization_settings} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#id OrganizationSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Name for Organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#name OrganizationSettings#name}
        :param security_contacts: List of emails used for security event notifications from the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#security_contacts OrganizationSettings#security_contacts}
        :param settings: settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#settings OrganizationSettings#settings}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__843c814cbc419f483a5a9d3d3810b64954105c44044d3d573841eefbe1de7e79)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OrganizationSettingsConfig(
            id=id,
            name=name,
            security_contacts=security_contacts,
            settings=settings,
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
        '''Generates CDKTF code for importing a OrganizationSettings resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OrganizationSettings to import.
        :param import_from_id: The id of the existing OrganizationSettings that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OrganizationSettings to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__758a8b5a3268bde00ac293c857d5bc0ea6fff1c8becef350ca7b6486cdbcb75f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSettings")
    def put_settings(
        self,
        *,
        saml: typing.Union["OrganizationSettingsSettingsSaml", typing.Dict[builtins.str, typing.Any]],
        saml_autocreate_users_domains: typing.Union["OrganizationSettingsSettingsSamlAutocreateUsersDomains", typing.Dict[builtins.str, typing.Any]],
        saml_idp_initiated_login: typing.Union["OrganizationSettingsSettingsSamlIdpInitiatedLogin", typing.Dict[builtins.str, typing.Any]],
        saml_strict_mode: typing.Union["OrganizationSettingsSettingsSamlStrictMode", typing.Dict[builtins.str, typing.Any]],
        private_widget_share: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        saml_autocreate_access_role: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param saml: saml block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#saml OrganizationSettings#saml}
        :param saml_autocreate_users_domains: saml_autocreate_users_domains block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#saml_autocreate_users_domains OrganizationSettings#saml_autocreate_users_domains}
        :param saml_idp_initiated_login: saml_idp_initiated_login block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#saml_idp_initiated_login OrganizationSettings#saml_idp_initiated_login}
        :param saml_strict_mode: saml_strict_mode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#saml_strict_mode OrganizationSettings#saml_strict_mode}
        :param private_widget_share: Whether or not the organization users can share widgets outside of Datadog. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#private_widget_share OrganizationSettings#private_widget_share}
        :param saml_autocreate_access_role: The access role of the user. Options are ``st`` (standard user), ``adm`` (admin user), or ``ro`` (read-only user). Allowed enum values: ``st``, ``adm`` , ``ro``, ``ERROR`` Defaults to ``"st"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#saml_autocreate_access_role OrganizationSettings#saml_autocreate_access_role}
        '''
        value = OrganizationSettingsSettings(
            saml=saml,
            saml_autocreate_users_domains=saml_autocreate_users_domains,
            saml_idp_initiated_login=saml_idp_initiated_login,
            saml_strict_mode=saml_strict_mode,
            private_widget_share=private_widget_share,
            saml_autocreate_access_role=saml_autocreate_access_role,
        )

        return typing.cast(None, jsii.invoke(self, "putSettings", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSecurityContacts")
    def reset_security_contacts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityContacts", []))

    @jsii.member(jsii_name="resetSettings")
    def reset_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSettings", []))

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
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="publicId")
    def public_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicId"))

    @builtins.property
    @jsii.member(jsii_name="settings")
    def settings(self) -> "OrganizationSettingsSettingsOutputReference":
        return typing.cast("OrganizationSettingsSettingsOutputReference", jsii.get(self, "settings"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="securityContactsInput")
    def security_contacts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityContactsInput"))

    @builtins.property
    @jsii.member(jsii_name="settingsInput")
    def settings_input(self) -> typing.Optional["OrganizationSettingsSettings"]:
        return typing.cast(typing.Optional["OrganizationSettingsSettings"], jsii.get(self, "settingsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14315dc8a7b2b49f00584e8cbc6d44794ea4acc6e9f3a0ae2089363c84fbbb72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__613d43b78e0d02359d3a3b7a701a46d8d1f49e74dfa11461c723cb871dcf6919)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityContacts")
    def security_contacts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityContacts"))

    @security_contacts.setter
    def security_contacts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ab83bed16d5e372c8b5a35da48b862d58f7075be1fd928f7e5aec2061bb34f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityContacts", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.organizationSettings.OrganizationSettingsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "id": "id",
        "name": "name",
        "security_contacts": "securityContacts",
        "settings": "settings",
    },
)
class OrganizationSettingsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        security_contacts: typing.Optional[typing.Sequence[builtins.str]] = None,
        settings: typing.Optional[typing.Union["OrganizationSettingsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#id OrganizationSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Name for Organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#name OrganizationSettings#name}
        :param security_contacts: List of emails used for security event notifications from the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#security_contacts OrganizationSettings#security_contacts}
        :param settings: settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#settings OrganizationSettings#settings}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(settings, dict):
            settings = OrganizationSettingsSettings(**settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aad4b47ce594899bece1f3eb24b610c81e3bb15dfda0befcce9fd2bc0cb21b8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument security_contacts", value=security_contacts, expected_type=type_hints["security_contacts"])
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
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
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name
        if security_contacts is not None:
            self._values["security_contacts"] = security_contacts
        if settings is not None:
            self._values["settings"] = settings

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
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#id OrganizationSettings#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name for Organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#name OrganizationSettings#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_contacts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of emails used for security event notifications from the organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#security_contacts OrganizationSettings#security_contacts}
        '''
        result = self._values.get("security_contacts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def settings(self) -> typing.Optional["OrganizationSettingsSettings"]:
        '''settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#settings OrganizationSettings#settings}
        '''
        result = self._values.get("settings")
        return typing.cast(typing.Optional["OrganizationSettingsSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationSettingsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.organizationSettings.OrganizationSettingsSettings",
    jsii_struct_bases=[],
    name_mapping={
        "saml": "saml",
        "saml_autocreate_users_domains": "samlAutocreateUsersDomains",
        "saml_idp_initiated_login": "samlIdpInitiatedLogin",
        "saml_strict_mode": "samlStrictMode",
        "private_widget_share": "privateWidgetShare",
        "saml_autocreate_access_role": "samlAutocreateAccessRole",
    },
)
class OrganizationSettingsSettings:
    def __init__(
        self,
        *,
        saml: typing.Union["OrganizationSettingsSettingsSaml", typing.Dict[builtins.str, typing.Any]],
        saml_autocreate_users_domains: typing.Union["OrganizationSettingsSettingsSamlAutocreateUsersDomains", typing.Dict[builtins.str, typing.Any]],
        saml_idp_initiated_login: typing.Union["OrganizationSettingsSettingsSamlIdpInitiatedLogin", typing.Dict[builtins.str, typing.Any]],
        saml_strict_mode: typing.Union["OrganizationSettingsSettingsSamlStrictMode", typing.Dict[builtins.str, typing.Any]],
        private_widget_share: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        saml_autocreate_access_role: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param saml: saml block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#saml OrganizationSettings#saml}
        :param saml_autocreate_users_domains: saml_autocreate_users_domains block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#saml_autocreate_users_domains OrganizationSettings#saml_autocreate_users_domains}
        :param saml_idp_initiated_login: saml_idp_initiated_login block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#saml_idp_initiated_login OrganizationSettings#saml_idp_initiated_login}
        :param saml_strict_mode: saml_strict_mode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#saml_strict_mode OrganizationSettings#saml_strict_mode}
        :param private_widget_share: Whether or not the organization users can share widgets outside of Datadog. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#private_widget_share OrganizationSettings#private_widget_share}
        :param saml_autocreate_access_role: The access role of the user. Options are ``st`` (standard user), ``adm`` (admin user), or ``ro`` (read-only user). Allowed enum values: ``st``, ``adm`` , ``ro``, ``ERROR`` Defaults to ``"st"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#saml_autocreate_access_role OrganizationSettings#saml_autocreate_access_role}
        '''
        if isinstance(saml, dict):
            saml = OrganizationSettingsSettingsSaml(**saml)
        if isinstance(saml_autocreate_users_domains, dict):
            saml_autocreate_users_domains = OrganizationSettingsSettingsSamlAutocreateUsersDomains(**saml_autocreate_users_domains)
        if isinstance(saml_idp_initiated_login, dict):
            saml_idp_initiated_login = OrganizationSettingsSettingsSamlIdpInitiatedLogin(**saml_idp_initiated_login)
        if isinstance(saml_strict_mode, dict):
            saml_strict_mode = OrganizationSettingsSettingsSamlStrictMode(**saml_strict_mode)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70810e42f9b1ba1901a51395905d75deae6b041ee8a84eef7649e9942b099530)
            check_type(argname="argument saml", value=saml, expected_type=type_hints["saml"])
            check_type(argname="argument saml_autocreate_users_domains", value=saml_autocreate_users_domains, expected_type=type_hints["saml_autocreate_users_domains"])
            check_type(argname="argument saml_idp_initiated_login", value=saml_idp_initiated_login, expected_type=type_hints["saml_idp_initiated_login"])
            check_type(argname="argument saml_strict_mode", value=saml_strict_mode, expected_type=type_hints["saml_strict_mode"])
            check_type(argname="argument private_widget_share", value=private_widget_share, expected_type=type_hints["private_widget_share"])
            check_type(argname="argument saml_autocreate_access_role", value=saml_autocreate_access_role, expected_type=type_hints["saml_autocreate_access_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "saml": saml,
            "saml_autocreate_users_domains": saml_autocreate_users_domains,
            "saml_idp_initiated_login": saml_idp_initiated_login,
            "saml_strict_mode": saml_strict_mode,
        }
        if private_widget_share is not None:
            self._values["private_widget_share"] = private_widget_share
        if saml_autocreate_access_role is not None:
            self._values["saml_autocreate_access_role"] = saml_autocreate_access_role

    @builtins.property
    def saml(self) -> "OrganizationSettingsSettingsSaml":
        '''saml block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#saml OrganizationSettings#saml}
        '''
        result = self._values.get("saml")
        assert result is not None, "Required property 'saml' is missing"
        return typing.cast("OrganizationSettingsSettingsSaml", result)

    @builtins.property
    def saml_autocreate_users_domains(
        self,
    ) -> "OrganizationSettingsSettingsSamlAutocreateUsersDomains":
        '''saml_autocreate_users_domains block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#saml_autocreate_users_domains OrganizationSettings#saml_autocreate_users_domains}
        '''
        result = self._values.get("saml_autocreate_users_domains")
        assert result is not None, "Required property 'saml_autocreate_users_domains' is missing"
        return typing.cast("OrganizationSettingsSettingsSamlAutocreateUsersDomains", result)

    @builtins.property
    def saml_idp_initiated_login(
        self,
    ) -> "OrganizationSettingsSettingsSamlIdpInitiatedLogin":
        '''saml_idp_initiated_login block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#saml_idp_initiated_login OrganizationSettings#saml_idp_initiated_login}
        '''
        result = self._values.get("saml_idp_initiated_login")
        assert result is not None, "Required property 'saml_idp_initiated_login' is missing"
        return typing.cast("OrganizationSettingsSettingsSamlIdpInitiatedLogin", result)

    @builtins.property
    def saml_strict_mode(self) -> "OrganizationSettingsSettingsSamlStrictMode":
        '''saml_strict_mode block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#saml_strict_mode OrganizationSettings#saml_strict_mode}
        '''
        result = self._values.get("saml_strict_mode")
        assert result is not None, "Required property 'saml_strict_mode' is missing"
        return typing.cast("OrganizationSettingsSettingsSamlStrictMode", result)

    @builtins.property
    def private_widget_share(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the organization users can share widgets outside of Datadog. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#private_widget_share OrganizationSettings#private_widget_share}
        '''
        result = self._values.get("private_widget_share")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def saml_autocreate_access_role(self) -> typing.Optional[builtins.str]:
        '''The access role of the user.

        Options are ``st`` (standard user), ``adm`` (admin user), or ``ro`` (read-only user). Allowed enum values: ``st``, ``adm`` , ``ro``, ``ERROR`` Defaults to ``"st"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#saml_autocreate_access_role OrganizationSettings#saml_autocreate_access_role}
        '''
        result = self._values.get("saml_autocreate_access_role")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationSettingsSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationSettingsSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.organizationSettings.OrganizationSettingsSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9550495c6a7d0dd0cabef8ed12b44fe3d96042be44868e5fda211369f6267569)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSaml")
    def put_saml(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether or not SAML is enabled for this organization. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#enabled OrganizationSettings#enabled}
        '''
        value = OrganizationSettingsSettingsSaml(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putSaml", [value]))

    @jsii.member(jsii_name="putSamlAutocreateUsersDomains")
    def put_saml_autocreate_users_domains(
        self,
        *,
        domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param domains: List of domains where the SAML automated user creation is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#domains OrganizationSettings#domains}
        :param enabled: Whether or not the automated user creation based on SAML domain is enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#enabled OrganizationSettings#enabled}
        '''
        value = OrganizationSettingsSettingsSamlAutocreateUsersDomains(
            domains=domains, enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putSamlAutocreateUsersDomains", [value]))

    @jsii.member(jsii_name="putSamlIdpInitiatedLogin")
    def put_saml_idp_initiated_login(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether or not a SAML identity provider metadata file was provided to the Datadog organization. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#enabled OrganizationSettings#enabled}
        '''
        value = OrganizationSettingsSettingsSamlIdpInitiatedLogin(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putSamlIdpInitiatedLogin", [value]))

    @jsii.member(jsii_name="putSamlStrictMode")
    def put_saml_strict_mode(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether or not the SAML strict mode is enabled. If true, all users must log in with SAML. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#enabled OrganizationSettings#enabled}
        '''
        value = OrganizationSettingsSettingsSamlStrictMode(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putSamlStrictMode", [value]))

    @jsii.member(jsii_name="resetPrivateWidgetShare")
    def reset_private_widget_share(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateWidgetShare", []))

    @jsii.member(jsii_name="resetSamlAutocreateAccessRole")
    def reset_saml_autocreate_access_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSamlAutocreateAccessRole", []))

    @builtins.property
    @jsii.member(jsii_name="saml")
    def saml(self) -> "OrganizationSettingsSettingsSamlOutputReference":
        return typing.cast("OrganizationSettingsSettingsSamlOutputReference", jsii.get(self, "saml"))

    @builtins.property
    @jsii.member(jsii_name="samlAutocreateUsersDomains")
    def saml_autocreate_users_domains(
        self,
    ) -> "OrganizationSettingsSettingsSamlAutocreateUsersDomainsOutputReference":
        return typing.cast("OrganizationSettingsSettingsSamlAutocreateUsersDomainsOutputReference", jsii.get(self, "samlAutocreateUsersDomains"))

    @builtins.property
    @jsii.member(jsii_name="samlCanBeEnabled")
    def saml_can_be_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "samlCanBeEnabled"))

    @builtins.property
    @jsii.member(jsii_name="samlIdpEndpoint")
    def saml_idp_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "samlIdpEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="samlIdpInitiatedLogin")
    def saml_idp_initiated_login(
        self,
    ) -> "OrganizationSettingsSettingsSamlIdpInitiatedLoginOutputReference":
        return typing.cast("OrganizationSettingsSettingsSamlIdpInitiatedLoginOutputReference", jsii.get(self, "samlIdpInitiatedLogin"))

    @builtins.property
    @jsii.member(jsii_name="samlIdpMetadataUploaded")
    def saml_idp_metadata_uploaded(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "samlIdpMetadataUploaded"))

    @builtins.property
    @jsii.member(jsii_name="samlLoginUrl")
    def saml_login_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "samlLoginUrl"))

    @builtins.property
    @jsii.member(jsii_name="samlStrictMode")
    def saml_strict_mode(
        self,
    ) -> "OrganizationSettingsSettingsSamlStrictModeOutputReference":
        return typing.cast("OrganizationSettingsSettingsSamlStrictModeOutputReference", jsii.get(self, "samlStrictMode"))

    @builtins.property
    @jsii.member(jsii_name="privateWidgetShareInput")
    def private_widget_share_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "privateWidgetShareInput"))

    @builtins.property
    @jsii.member(jsii_name="samlAutocreateAccessRoleInput")
    def saml_autocreate_access_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "samlAutocreateAccessRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="samlAutocreateUsersDomainsInput")
    def saml_autocreate_users_domains_input(
        self,
    ) -> typing.Optional["OrganizationSettingsSettingsSamlAutocreateUsersDomains"]:
        return typing.cast(typing.Optional["OrganizationSettingsSettingsSamlAutocreateUsersDomains"], jsii.get(self, "samlAutocreateUsersDomainsInput"))

    @builtins.property
    @jsii.member(jsii_name="samlIdpInitiatedLoginInput")
    def saml_idp_initiated_login_input(
        self,
    ) -> typing.Optional["OrganizationSettingsSettingsSamlIdpInitiatedLogin"]:
        return typing.cast(typing.Optional["OrganizationSettingsSettingsSamlIdpInitiatedLogin"], jsii.get(self, "samlIdpInitiatedLoginInput"))

    @builtins.property
    @jsii.member(jsii_name="samlInput")
    def saml_input(self) -> typing.Optional["OrganizationSettingsSettingsSaml"]:
        return typing.cast(typing.Optional["OrganizationSettingsSettingsSaml"], jsii.get(self, "samlInput"))

    @builtins.property
    @jsii.member(jsii_name="samlStrictModeInput")
    def saml_strict_mode_input(
        self,
    ) -> typing.Optional["OrganizationSettingsSettingsSamlStrictMode"]:
        return typing.cast(typing.Optional["OrganizationSettingsSettingsSamlStrictMode"], jsii.get(self, "samlStrictModeInput"))

    @builtins.property
    @jsii.member(jsii_name="privateWidgetShare")
    def private_widget_share(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "privateWidgetShare"))

    @private_widget_share.setter
    def private_widget_share(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10d5bfc1e75dd3d9229c73c32182299d48148c080e9023d95c2c4f41b4c56875)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateWidgetShare", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="samlAutocreateAccessRole")
    def saml_autocreate_access_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "samlAutocreateAccessRole"))

    @saml_autocreate_access_role.setter
    def saml_autocreate_access_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf9bc643484efda4cb8cb5f6cb947c4637af7e04c74ddec08e8c9f262e942e4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samlAutocreateAccessRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrganizationSettingsSettings]:
        return typing.cast(typing.Optional[OrganizationSettingsSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrganizationSettingsSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03444b9affe9da3ed7f36160fe875ad9ef0736ff3a9afc45cbc7b371a16b4cdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.organizationSettings.OrganizationSettingsSettingsSaml",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class OrganizationSettingsSettingsSaml:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether or not SAML is enabled for this organization. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#enabled OrganizationSettings#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51489f2682f9bf67093a3d7fb96fe358f89423d29100802d2db01dde18248c85)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not SAML is enabled for this organization. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#enabled OrganizationSettings#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationSettingsSettingsSaml(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.organizationSettings.OrganizationSettingsSettingsSamlAutocreateUsersDomains",
    jsii_struct_bases=[],
    name_mapping={"domains": "domains", "enabled": "enabled"},
)
class OrganizationSettingsSettingsSamlAutocreateUsersDomains:
    def __init__(
        self,
        *,
        domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param domains: List of domains where the SAML automated user creation is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#domains OrganizationSettings#domains}
        :param enabled: Whether or not the automated user creation based on SAML domain is enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#enabled OrganizationSettings#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0591b2ed70b122eef7f4b5968b121437becf57c10a9635a6cfd373f3df2a07f2)
            check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domains is not None:
            self._values["domains"] = domains
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of domains where the SAML automated user creation is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#domains OrganizationSettings#domains}
        '''
        result = self._values.get("domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the automated user creation based on SAML domain is enabled. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#enabled OrganizationSettings#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationSettingsSettingsSamlAutocreateUsersDomains(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationSettingsSettingsSamlAutocreateUsersDomainsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.organizationSettings.OrganizationSettingsSettingsSamlAutocreateUsersDomainsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c8fc88a89e31910ea07cc7047e832b16e9fe21d6ea195cadd8e9e8f7711ab71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDomains")
    def reset_domains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomains", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="domainsInput")
    def domains_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "domainsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="domains")
    def domains(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domains"))

    @domains.setter
    def domains(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea4f8accce1ce06275496b8020d433fcbdc5e3984c3d9de85b61ed3286a7174c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53c3e2c91184afbfec198d9cdee22124bbc0e92cf940d59519ea92864956be85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrganizationSettingsSettingsSamlAutocreateUsersDomains]:
        return typing.cast(typing.Optional[OrganizationSettingsSettingsSamlAutocreateUsersDomains], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrganizationSettingsSettingsSamlAutocreateUsersDomains],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e94c40274878efbaf7e3745611e8085a65c4b2094004f28f0fcbf7646e2360d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.organizationSettings.OrganizationSettingsSettingsSamlIdpInitiatedLogin",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class OrganizationSettingsSettingsSamlIdpInitiatedLogin:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether or not a SAML identity provider metadata file was provided to the Datadog organization. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#enabled OrganizationSettings#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bff96c42256f11d86cb1a15f355dd8c626744a22032f65993e83e25cb3d62867)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not a SAML identity provider metadata file was provided to the Datadog organization. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#enabled OrganizationSettings#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationSettingsSettingsSamlIdpInitiatedLogin(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationSettingsSettingsSamlIdpInitiatedLoginOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.organizationSettings.OrganizationSettingsSettingsSamlIdpInitiatedLoginOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd098928cf7738b35d6cee12efee8e2a992c85b57bef3cc1efe36a2f66b8150c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b71bf531cad0f73f461fcb9599463605576fb1705ef88addf7ad2ac7dbce81cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrganizationSettingsSettingsSamlIdpInitiatedLogin]:
        return typing.cast(typing.Optional[OrganizationSettingsSettingsSamlIdpInitiatedLogin], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrganizationSettingsSettingsSamlIdpInitiatedLogin],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ffb23078c1c00a3f2ebe073ed31365b35ee47f51acc635ec51bf81091101a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrganizationSettingsSettingsSamlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.organizationSettings.OrganizationSettingsSettingsSamlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b9cbad80cd8e307abcd0c97e8b459178e95f3ac02b3720c7a16a8875f5c73f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__767b9ba81576628ce938afa16fd945afa7c1abe76eb99e933bfc12727bb2d75d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrganizationSettingsSettingsSaml]:
        return typing.cast(typing.Optional[OrganizationSettingsSettingsSaml], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrganizationSettingsSettingsSaml],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f5c5380de39db223948049445e302a2984363dfdd2deaf453c8bb2ea7c86f43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.organizationSettings.OrganizationSettingsSettingsSamlStrictMode",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class OrganizationSettingsSettingsSamlStrictMode:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether or not the SAML strict mode is enabled. If true, all users must log in with SAML. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#enabled OrganizationSettings#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__330099d6558762594debe829fb3446f21ed0deef95c37a77f3863b437995cd75)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the SAML strict mode is enabled.

        If true, all users must log in with SAML. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/organization_settings#enabled OrganizationSettings#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationSettingsSettingsSamlStrictMode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationSettingsSettingsSamlStrictModeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.organizationSettings.OrganizationSettingsSettingsSamlStrictModeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e42573e3649e8201095e22942d482ad332a4cd618ca8966516a85e3d33364db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4263b293381b0121e918d9ed59b513f5aacde7341633072c5073473f26fbdbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrganizationSettingsSettingsSamlStrictMode]:
        return typing.cast(typing.Optional[OrganizationSettingsSettingsSamlStrictMode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrganizationSettingsSettingsSamlStrictMode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7268489c703194fe867ded63a5a880b8282448e90727ad0e4fa48ceebd61726a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "OrganizationSettings",
    "OrganizationSettingsConfig",
    "OrganizationSettingsSettings",
    "OrganizationSettingsSettingsOutputReference",
    "OrganizationSettingsSettingsSaml",
    "OrganizationSettingsSettingsSamlAutocreateUsersDomains",
    "OrganizationSettingsSettingsSamlAutocreateUsersDomainsOutputReference",
    "OrganizationSettingsSettingsSamlIdpInitiatedLogin",
    "OrganizationSettingsSettingsSamlIdpInitiatedLoginOutputReference",
    "OrganizationSettingsSettingsSamlOutputReference",
    "OrganizationSettingsSettingsSamlStrictMode",
    "OrganizationSettingsSettingsSamlStrictModeOutputReference",
]

publication.publish()

def _typecheckingstub__843c814cbc419f483a5a9d3d3810b64954105c44044d3d573841eefbe1de7e79(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    security_contacts: typing.Optional[typing.Sequence[builtins.str]] = None,
    settings: typing.Optional[typing.Union[OrganizationSettingsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__758a8b5a3268bde00ac293c857d5bc0ea6fff1c8becef350ca7b6486cdbcb75f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14315dc8a7b2b49f00584e8cbc6d44794ea4acc6e9f3a0ae2089363c84fbbb72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__613d43b78e0d02359d3a3b7a701a46d8d1f49e74dfa11461c723cb871dcf6919(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ab83bed16d5e372c8b5a35da48b862d58f7075be1fd928f7e5aec2061bb34f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aad4b47ce594899bece1f3eb24b610c81e3bb15dfda0befcce9fd2bc0cb21b8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    security_contacts: typing.Optional[typing.Sequence[builtins.str]] = None,
    settings: typing.Optional[typing.Union[OrganizationSettingsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70810e42f9b1ba1901a51395905d75deae6b041ee8a84eef7649e9942b099530(
    *,
    saml: typing.Union[OrganizationSettingsSettingsSaml, typing.Dict[builtins.str, typing.Any]],
    saml_autocreate_users_domains: typing.Union[OrganizationSettingsSettingsSamlAutocreateUsersDomains, typing.Dict[builtins.str, typing.Any]],
    saml_idp_initiated_login: typing.Union[OrganizationSettingsSettingsSamlIdpInitiatedLogin, typing.Dict[builtins.str, typing.Any]],
    saml_strict_mode: typing.Union[OrganizationSettingsSettingsSamlStrictMode, typing.Dict[builtins.str, typing.Any]],
    private_widget_share: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    saml_autocreate_access_role: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9550495c6a7d0dd0cabef8ed12b44fe3d96042be44868e5fda211369f6267569(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10d5bfc1e75dd3d9229c73c32182299d48148c080e9023d95c2c4f41b4c56875(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf9bc643484efda4cb8cb5f6cb947c4637af7e04c74ddec08e8c9f262e942e4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03444b9affe9da3ed7f36160fe875ad9ef0736ff3a9afc45cbc7b371a16b4cdb(
    value: typing.Optional[OrganizationSettingsSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51489f2682f9bf67093a3d7fb96fe358f89423d29100802d2db01dde18248c85(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0591b2ed70b122eef7f4b5968b121437becf57c10a9635a6cfd373f3df2a07f2(
    *,
    domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c8fc88a89e31910ea07cc7047e832b16e9fe21d6ea195cadd8e9e8f7711ab71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea4f8accce1ce06275496b8020d433fcbdc5e3984c3d9de85b61ed3286a7174c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53c3e2c91184afbfec198d9cdee22124bbc0e92cf940d59519ea92864956be85(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e94c40274878efbaf7e3745611e8085a65c4b2094004f28f0fcbf7646e2360d(
    value: typing.Optional[OrganizationSettingsSettingsSamlAutocreateUsersDomains],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bff96c42256f11d86cb1a15f355dd8c626744a22032f65993e83e25cb3d62867(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd098928cf7738b35d6cee12efee8e2a992c85b57bef3cc1efe36a2f66b8150c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b71bf531cad0f73f461fcb9599463605576fb1705ef88addf7ad2ac7dbce81cf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ffb23078c1c00a3f2ebe073ed31365b35ee47f51acc635ec51bf81091101a3(
    value: typing.Optional[OrganizationSettingsSettingsSamlIdpInitiatedLogin],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b9cbad80cd8e307abcd0c97e8b459178e95f3ac02b3720c7a16a8875f5c73f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__767b9ba81576628ce938afa16fd945afa7c1abe76eb99e933bfc12727bb2d75d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f5c5380de39db223948049445e302a2984363dfdd2deaf453c8bb2ea7c86f43(
    value: typing.Optional[OrganizationSettingsSettingsSaml],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__330099d6558762594debe829fb3446f21ed0deef95c37a77f3863b437995cd75(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e42573e3649e8201095e22942d482ad332a4cd618ca8966516a85e3d33364db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4263b293381b0121e918d9ed59b513f5aacde7341633072c5073473f26fbdbf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7268489c703194fe867ded63a5a880b8282448e90727ad0e4fa48ceebd61726a(
    value: typing.Optional[OrganizationSettingsSettingsSamlStrictMode],
) -> None:
    """Type checking stubs"""
    pass
