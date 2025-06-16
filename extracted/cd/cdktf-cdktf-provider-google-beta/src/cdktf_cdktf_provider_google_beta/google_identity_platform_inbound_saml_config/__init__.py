r'''
# `google_identity_platform_inbound_saml_config`

Refer to the Terraform Registry for docs: [`google_identity_platform_inbound_saml_config`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config).
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


class GoogleIdentityPlatformInboundSamlConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformInboundSamlConfig.GoogleIdentityPlatformInboundSamlConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config google_identity_platform_inbound_saml_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        idp_config: typing.Union["GoogleIdentityPlatformInboundSamlConfigIdpConfig", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        sp_config: typing.Union["GoogleIdentityPlatformInboundSamlConfigSpConfig", typing.Dict[builtins.str, typing.Any]],
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleIdentityPlatformInboundSamlConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config google_identity_platform_inbound_saml_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: Human friendly display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#display_name GoogleIdentityPlatformInboundSamlConfig#display_name}
        :param idp_config: idp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#idp_config GoogleIdentityPlatformInboundSamlConfig#idp_config}
        :param name: The name of the InboundSamlConfig resource. Must start with 'saml.' and can only have alphanumeric characters, hyphens, underscores or periods. The part after 'saml.' must also start with a lowercase letter, end with an alphanumeric character, and have at least 2 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#name GoogleIdentityPlatformInboundSamlConfig#name}
        :param sp_config: sp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#sp_config GoogleIdentityPlatformInboundSamlConfig#sp_config}
        :param enabled: If this config allows users to sign in with the provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#enabled GoogleIdentityPlatformInboundSamlConfig#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#id GoogleIdentityPlatformInboundSamlConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#project GoogleIdentityPlatformInboundSamlConfig#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#timeouts GoogleIdentityPlatformInboundSamlConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98a33115f7670a576942ff78226b4310068fc3620dde267c5e577cf528102334)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleIdentityPlatformInboundSamlConfigConfig(
            display_name=display_name,
            idp_config=idp_config,
            name=name,
            sp_config=sp_config,
            enabled=enabled,
            id=id,
            project=project,
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
        '''Generates CDKTF code for importing a GoogleIdentityPlatformInboundSamlConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleIdentityPlatformInboundSamlConfig to import.
        :param import_from_id: The id of the existing GoogleIdentityPlatformInboundSamlConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleIdentityPlatformInboundSamlConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80610a0b1cc1f85dcf786ca68ae4e27ddb8d50dfc866a5e9c56d6089820bf02f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIdpConfig")
    def put_idp_config(
        self,
        *,
        idp_certificates: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificates", typing.Dict[builtins.str, typing.Any]]]],
        idp_entity_id: builtins.str,
        sso_url: builtins.str,
        sign_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param idp_certificates: idp_certificates block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#idp_certificates GoogleIdentityPlatformInboundSamlConfig#idp_certificates}
        :param idp_entity_id: Unique identifier for all SAML entities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#idp_entity_id GoogleIdentityPlatformInboundSamlConfig#idp_entity_id}
        :param sso_url: URL to send Authentication request to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#sso_url GoogleIdentityPlatformInboundSamlConfig#sso_url}
        :param sign_request: Indicates if outbounding SAMLRequest should be signed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#sign_request GoogleIdentityPlatformInboundSamlConfig#sign_request}
        '''
        value = GoogleIdentityPlatformInboundSamlConfigIdpConfig(
            idp_certificates=idp_certificates,
            idp_entity_id=idp_entity_id,
            sso_url=sso_url,
            sign_request=sign_request,
        )

        return typing.cast(None, jsii.invoke(self, "putIdpConfig", [value]))

    @jsii.member(jsii_name="putSpConfig")
    def put_sp_config(
        self,
        *,
        callback_uri: typing.Optional[builtins.str] = None,
        sp_entity_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param callback_uri: Callback URI where responses from IDP are handled. Must start with 'https://'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#callback_uri GoogleIdentityPlatformInboundSamlConfig#callback_uri}
        :param sp_entity_id: Unique identifier for all SAML entities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#sp_entity_id GoogleIdentityPlatformInboundSamlConfig#sp_entity_id}
        '''
        value = GoogleIdentityPlatformInboundSamlConfigSpConfig(
            callback_uri=callback_uri, sp_entity_id=sp_entity_id
        )

        return typing.cast(None, jsii.invoke(self, "putSpConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#create GoogleIdentityPlatformInboundSamlConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#delete GoogleIdentityPlatformInboundSamlConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#update GoogleIdentityPlatformInboundSamlConfig#update}.
        '''
        value = GoogleIdentityPlatformInboundSamlConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="idpConfig")
    def idp_config(
        self,
    ) -> "GoogleIdentityPlatformInboundSamlConfigIdpConfigOutputReference":
        return typing.cast("GoogleIdentityPlatformInboundSamlConfigIdpConfigOutputReference", jsii.get(self, "idpConfig"))

    @builtins.property
    @jsii.member(jsii_name="spConfig")
    def sp_config(
        self,
    ) -> "GoogleIdentityPlatformInboundSamlConfigSpConfigOutputReference":
        return typing.cast("GoogleIdentityPlatformInboundSamlConfigSpConfigOutputReference", jsii.get(self, "spConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleIdentityPlatformInboundSamlConfigTimeoutsOutputReference":
        return typing.cast("GoogleIdentityPlatformInboundSamlConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="idpConfigInput")
    def idp_config_input(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformInboundSamlConfigIdpConfig"]:
        return typing.cast(typing.Optional["GoogleIdentityPlatformInboundSamlConfigIdpConfig"], jsii.get(self, "idpConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="spConfigInput")
    def sp_config_input(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformInboundSamlConfigSpConfig"]:
        return typing.cast(typing.Optional["GoogleIdentityPlatformInboundSamlConfigSpConfig"], jsii.get(self, "spConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleIdentityPlatformInboundSamlConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleIdentityPlatformInboundSamlConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bba59df1f3674d8d9b98f54f62a660458232f722e2fc57872d8a0debeac9cad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__ec9a636b592241797d5434e4b6f219b3754ec6c5bb61c69a198b05f360a859eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51edcdd4d4f0791d1c8c4f8601897be6406e0cc78c9cfd43b9f0345745c54168)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0430250f83b9256b2a3b8c5e1b0e4c0e76790ceb3ecf7a819ff14fad261a1dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f4098f30730031fcf13241a6c6fcc6c329c3aa00c3cd4b42dacdc5ac31fc805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformInboundSamlConfig.GoogleIdentityPlatformInboundSamlConfigConfig",
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
        "idp_config": "idpConfig",
        "name": "name",
        "sp_config": "spConfig",
        "enabled": "enabled",
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleIdentityPlatformInboundSamlConfigConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        idp_config: typing.Union["GoogleIdentityPlatformInboundSamlConfigIdpConfig", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        sp_config: typing.Union["GoogleIdentityPlatformInboundSamlConfigSpConfig", typing.Dict[builtins.str, typing.Any]],
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleIdentityPlatformInboundSamlConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: Human friendly display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#display_name GoogleIdentityPlatformInboundSamlConfig#display_name}
        :param idp_config: idp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#idp_config GoogleIdentityPlatformInboundSamlConfig#idp_config}
        :param name: The name of the InboundSamlConfig resource. Must start with 'saml.' and can only have alphanumeric characters, hyphens, underscores or periods. The part after 'saml.' must also start with a lowercase letter, end with an alphanumeric character, and have at least 2 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#name GoogleIdentityPlatformInboundSamlConfig#name}
        :param sp_config: sp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#sp_config GoogleIdentityPlatformInboundSamlConfig#sp_config}
        :param enabled: If this config allows users to sign in with the provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#enabled GoogleIdentityPlatformInboundSamlConfig#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#id GoogleIdentityPlatformInboundSamlConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#project GoogleIdentityPlatformInboundSamlConfig#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#timeouts GoogleIdentityPlatformInboundSamlConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(idp_config, dict):
            idp_config = GoogleIdentityPlatformInboundSamlConfigIdpConfig(**idp_config)
        if isinstance(sp_config, dict):
            sp_config = GoogleIdentityPlatformInboundSamlConfigSpConfig(**sp_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleIdentityPlatformInboundSamlConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9edc077ea15de81489d521cc97666bde7b364c1e3fcb6794e3e3ea12000a2be)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument idp_config", value=idp_config, expected_type=type_hints["idp_config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sp_config", value=sp_config, expected_type=type_hints["sp_config"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "idp_config": idp_config,
            "name": name,
            "sp_config": sp_config,
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
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
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
    def display_name(self) -> builtins.str:
        '''Human friendly display name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#display_name GoogleIdentityPlatformInboundSamlConfig#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def idp_config(self) -> "GoogleIdentityPlatformInboundSamlConfigIdpConfig":
        '''idp_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#idp_config GoogleIdentityPlatformInboundSamlConfig#idp_config}
        '''
        result = self._values.get("idp_config")
        assert result is not None, "Required property 'idp_config' is missing"
        return typing.cast("GoogleIdentityPlatformInboundSamlConfigIdpConfig", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the InboundSamlConfig resource.

        Must start with 'saml.' and can only have alphanumeric characters,
        hyphens, underscores or periods. The part after 'saml.' must also start with a lowercase letter, end with an
        alphanumeric character, and have at least 2 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#name GoogleIdentityPlatformInboundSamlConfig#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sp_config(self) -> "GoogleIdentityPlatformInboundSamlConfigSpConfig":
        '''sp_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#sp_config GoogleIdentityPlatformInboundSamlConfig#sp_config}
        '''
        result = self._values.get("sp_config")
        assert result is not None, "Required property 'sp_config' is missing"
        return typing.cast("GoogleIdentityPlatformInboundSamlConfigSpConfig", result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If this config allows users to sign in with the provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#enabled GoogleIdentityPlatformInboundSamlConfig#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#id GoogleIdentityPlatformInboundSamlConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#project GoogleIdentityPlatformInboundSamlConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformInboundSamlConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#timeouts GoogleIdentityPlatformInboundSamlConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleIdentityPlatformInboundSamlConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformInboundSamlConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformInboundSamlConfig.GoogleIdentityPlatformInboundSamlConfigIdpConfig",
    jsii_struct_bases=[],
    name_mapping={
        "idp_certificates": "idpCertificates",
        "idp_entity_id": "idpEntityId",
        "sso_url": "ssoUrl",
        "sign_request": "signRequest",
    },
)
class GoogleIdentityPlatformInboundSamlConfigIdpConfig:
    def __init__(
        self,
        *,
        idp_certificates: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificates", typing.Dict[builtins.str, typing.Any]]]],
        idp_entity_id: builtins.str,
        sso_url: builtins.str,
        sign_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param idp_certificates: idp_certificates block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#idp_certificates GoogleIdentityPlatformInboundSamlConfig#idp_certificates}
        :param idp_entity_id: Unique identifier for all SAML entities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#idp_entity_id GoogleIdentityPlatformInboundSamlConfig#idp_entity_id}
        :param sso_url: URL to send Authentication request to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#sso_url GoogleIdentityPlatformInboundSamlConfig#sso_url}
        :param sign_request: Indicates if outbounding SAMLRequest should be signed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#sign_request GoogleIdentityPlatformInboundSamlConfig#sign_request}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af71df490e4e6f44fde7dcd65091cb0fa544b353ee4fbbecfa699f009b45fa3)
            check_type(argname="argument idp_certificates", value=idp_certificates, expected_type=type_hints["idp_certificates"])
            check_type(argname="argument idp_entity_id", value=idp_entity_id, expected_type=type_hints["idp_entity_id"])
            check_type(argname="argument sso_url", value=sso_url, expected_type=type_hints["sso_url"])
            check_type(argname="argument sign_request", value=sign_request, expected_type=type_hints["sign_request"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "idp_certificates": idp_certificates,
            "idp_entity_id": idp_entity_id,
            "sso_url": sso_url,
        }
        if sign_request is not None:
            self._values["sign_request"] = sign_request

    @builtins.property
    def idp_certificates(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificates"]]:
        '''idp_certificates block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#idp_certificates GoogleIdentityPlatformInboundSamlConfig#idp_certificates}
        '''
        result = self._values.get("idp_certificates")
        assert result is not None, "Required property 'idp_certificates' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificates"]], result)

    @builtins.property
    def idp_entity_id(self) -> builtins.str:
        '''Unique identifier for all SAML entities.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#idp_entity_id GoogleIdentityPlatformInboundSamlConfig#idp_entity_id}
        '''
        result = self._values.get("idp_entity_id")
        assert result is not None, "Required property 'idp_entity_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sso_url(self) -> builtins.str:
        '''URL to send Authentication request to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#sso_url GoogleIdentityPlatformInboundSamlConfig#sso_url}
        '''
        result = self._values.get("sso_url")
        assert result is not None, "Required property 'sso_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sign_request(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if outbounding SAMLRequest should be signed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#sign_request GoogleIdentityPlatformInboundSamlConfig#sign_request}
        '''
        result = self._values.get("sign_request")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformInboundSamlConfigIdpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformInboundSamlConfig.GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificates",
    jsii_struct_bases=[],
    name_mapping={"x509_certificate": "x509Certificate"},
)
class GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificates:
    def __init__(
        self,
        *,
        x509_certificate: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param x509_certificate: The IdP's x509 certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#x509_certificate GoogleIdentityPlatformInboundSamlConfig#x509_certificate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac11b7d0c1cdf783398a543b307840216b5fde470b25587df2656063050b5bb5)
            check_type(argname="argument x509_certificate", value=x509_certificate, expected_type=type_hints["x509_certificate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if x509_certificate is not None:
            self._values["x509_certificate"] = x509_certificate

    @builtins.property
    def x509_certificate(self) -> typing.Optional[builtins.str]:
        '''The IdP's x509 certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#x509_certificate GoogleIdentityPlatformInboundSamlConfig#x509_certificate}
        '''
        result = self._values.get("x509_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificates(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificatesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformInboundSamlConfig.GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificatesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9015c2df8b721b7f32826c8dd1594a27327b8003ef117b6158cbae029a85c65)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificatesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb2be6d3a9b499a7a4a3b3ea39a1dbe88c46113dbd06f0f177c26d595a6700d7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificatesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8bf1f304a84dbfdcbffb152ac9de927f5169a10f31485cf7ed7669b7fe4b937)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47a271ef4eaab894cf1c5b875cfd1538435ded1401a91d60a9c0e764a44a0529)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09d4d747ce1f6bfe6410981e10c3a204150773c7dcf960b244354452e3f2c459)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificates]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificates]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificates]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d372b61ce9a145215222ade0b4e1a560c5797be8a5fba5b7e7379f626a5710d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificatesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformInboundSamlConfig.GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificatesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac97eec91fa996577e28fe568a4453766ab3f0d6bc6f70c1d21be29484a22987)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetX509Certificate")
    def reset_x509_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetX509Certificate", []))

    @builtins.property
    @jsii.member(jsii_name="x509CertificateInput")
    def x509_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "x509CertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="x509Certificate")
    def x509_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "x509Certificate"))

    @x509_certificate.setter
    def x509_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a664cee19a2918e0f760a592420202ab895740aee16aa50e1fe246e57338bcfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "x509Certificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificates]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificates]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificates]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__145799a5f9f344bbd7fc47fc0dbee364f408dee3e5bfb569021addf940b750b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIdentityPlatformInboundSamlConfigIdpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformInboundSamlConfig.GoogleIdentityPlatformInboundSamlConfigIdpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98ce12e914d63f126c5f6939fd994b70641e5c9245071b4d86a47b0b7c7d1219)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIdpCertificates")
    def put_idp_certificates(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificates, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd17170ce5cf9b14b9d25d257a92ca7098e16f1274f10b26f5930a9ff7d4e968)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIdpCertificates", [value]))

    @jsii.member(jsii_name="resetSignRequest")
    def reset_sign_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignRequest", []))

    @builtins.property
    @jsii.member(jsii_name="idpCertificates")
    def idp_certificates(
        self,
    ) -> GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificatesList:
        return typing.cast(GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificatesList, jsii.get(self, "idpCertificates"))

    @builtins.property
    @jsii.member(jsii_name="idpCertificatesInput")
    def idp_certificates_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificates]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificates]]], jsii.get(self, "idpCertificatesInput"))

    @builtins.property
    @jsii.member(jsii_name="idpEntityIdInput")
    def idp_entity_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idpEntityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="signRequestInput")
    def sign_request_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "signRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="ssoUrlInput")
    def sso_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ssoUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="idpEntityId")
    def idp_entity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idpEntityId"))

    @idp_entity_id.setter
    def idp_entity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__605f67605173a6304403922b03cac2a84553475a3ada9d1e8814b53c00a8d1e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idpEntityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signRequest")
    def sign_request(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "signRequest"))

    @sign_request.setter
    def sign_request(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a9210702639d9ea5488fc2db36f6083b32fcd80cedb2aa4032a7c3052d53d83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signRequest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ssoUrl")
    def sso_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ssoUrl"))

    @sso_url.setter
    def sso_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74a43b4aa58c6496a1dbe330b8a8727ae9b2eb93720b7273c0f661446ce34482)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssoUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformInboundSamlConfigIdpConfig]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformInboundSamlConfigIdpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformInboundSamlConfigIdpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92e57b979e6d47ae15bb7fca94e662e36a29e2df685b11a5ed742659c994681e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformInboundSamlConfig.GoogleIdentityPlatformInboundSamlConfigSpConfig",
    jsii_struct_bases=[],
    name_mapping={"callback_uri": "callbackUri", "sp_entity_id": "spEntityId"},
)
class GoogleIdentityPlatformInboundSamlConfigSpConfig:
    def __init__(
        self,
        *,
        callback_uri: typing.Optional[builtins.str] = None,
        sp_entity_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param callback_uri: Callback URI where responses from IDP are handled. Must start with 'https://'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#callback_uri GoogleIdentityPlatformInboundSamlConfig#callback_uri}
        :param sp_entity_id: Unique identifier for all SAML entities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#sp_entity_id GoogleIdentityPlatformInboundSamlConfig#sp_entity_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd331293d2752fc19a02684ff6a15068a1fe182330c70cfccb3681672d25ccee)
            check_type(argname="argument callback_uri", value=callback_uri, expected_type=type_hints["callback_uri"])
            check_type(argname="argument sp_entity_id", value=sp_entity_id, expected_type=type_hints["sp_entity_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if callback_uri is not None:
            self._values["callback_uri"] = callback_uri
        if sp_entity_id is not None:
            self._values["sp_entity_id"] = sp_entity_id

    @builtins.property
    def callback_uri(self) -> typing.Optional[builtins.str]:
        '''Callback URI where responses from IDP are handled. Must start with 'https://'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#callback_uri GoogleIdentityPlatformInboundSamlConfig#callback_uri}
        '''
        result = self._values.get("callback_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sp_entity_id(self) -> typing.Optional[builtins.str]:
        '''Unique identifier for all SAML entities.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#sp_entity_id GoogleIdentityPlatformInboundSamlConfig#sp_entity_id}
        '''
        result = self._values.get("sp_entity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformInboundSamlConfigSpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformInboundSamlConfigSpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformInboundSamlConfig.GoogleIdentityPlatformInboundSamlConfigSpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68a8289db6ee0e9de68765fae7e2596fd32decb3930a31e9638295e8917a3c48)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCallbackUri")
    def reset_callback_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCallbackUri", []))

    @jsii.member(jsii_name="resetSpEntityId")
    def reset_sp_entity_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpEntityId", []))

    @builtins.property
    @jsii.member(jsii_name="spCertificates")
    def sp_certificates(
        self,
    ) -> "GoogleIdentityPlatformInboundSamlConfigSpConfigSpCertificatesList":
        return typing.cast("GoogleIdentityPlatformInboundSamlConfigSpConfigSpCertificatesList", jsii.get(self, "spCertificates"))

    @builtins.property
    @jsii.member(jsii_name="callbackUriInput")
    def callback_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "callbackUriInput"))

    @builtins.property
    @jsii.member(jsii_name="spEntityIdInput")
    def sp_entity_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "spEntityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="callbackUri")
    def callback_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "callbackUri"))

    @callback_uri.setter
    def callback_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1b5eb0a435e7bc86cdeb679d00623381d460bf8f875dd748ad254554dec69ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "callbackUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="spEntityId")
    def sp_entity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "spEntityId"))

    @sp_entity_id.setter
    def sp_entity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c4513f97eb47168959c06821bdf4e744c75188dd642d3c175f70fe0677d4e2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spEntityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformInboundSamlConfigSpConfig]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformInboundSamlConfigSpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformInboundSamlConfigSpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70759fe7819cee63f3128988ba28d35e43d878f92ea7d57840959665f346f519)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformInboundSamlConfig.GoogleIdentityPlatformInboundSamlConfigSpConfigSpCertificates",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleIdentityPlatformInboundSamlConfigSpConfigSpCertificates:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformInboundSamlConfigSpConfigSpCertificates(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformInboundSamlConfigSpConfigSpCertificatesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformInboundSamlConfig.GoogleIdentityPlatformInboundSamlConfigSpConfigSpCertificatesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c88083d6922d095c477bfea0139b3442801699c937c67e575d52e6d8f8be153)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleIdentityPlatformInboundSamlConfigSpConfigSpCertificatesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__151c0b7c013f779fd9dad9570641fba38a36cda91f781e6736f2aa931e2050ca)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleIdentityPlatformInboundSamlConfigSpConfigSpCertificatesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c374bb4df1f16c16bcce0a9952ff9bb662eb044885baff3c30aec7dd3d81069)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76e9dad2cc392c96fa28f268fd9a179838cafe99654f07e97f887fee05249ee7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62b7388b8b87ae3477fe5bbb8b446191b062de6cd00e5f73f6a2888da8c4abe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleIdentityPlatformInboundSamlConfigSpConfigSpCertificatesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformInboundSamlConfig.GoogleIdentityPlatformInboundSamlConfigSpConfigSpCertificatesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f021848dfa36bf3f7500b7198a8ddf71d4023646892ef7962b7040a85983d03)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="x509Certificate")
    def x509_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "x509Certificate"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformInboundSamlConfigSpConfigSpCertificates]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformInboundSamlConfigSpConfigSpCertificates], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformInboundSamlConfigSpConfigSpCertificates],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fee937cdebf92a850ce2d0484cc9191536c1a74c0f11c007c3776620d84fcd58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformInboundSamlConfig.GoogleIdentityPlatformInboundSamlConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleIdentityPlatformInboundSamlConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#create GoogleIdentityPlatformInboundSamlConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#delete GoogleIdentityPlatformInboundSamlConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#update GoogleIdentityPlatformInboundSamlConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e999b18ce545b64bac2d25444a78a2edf13251e96f5affdbd34496f2d8dbe204)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#create GoogleIdentityPlatformInboundSamlConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#delete GoogleIdentityPlatformInboundSamlConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_inbound_saml_config#update GoogleIdentityPlatformInboundSamlConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformInboundSamlConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformInboundSamlConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformInboundSamlConfig.GoogleIdentityPlatformInboundSamlConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c32850c0c586ba0111dad3130ec35ca32f44ba92251699c4b1120ec737afe23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcf92b9b5a14a596eac21fa1a4ac0907371c2d17744af541152c21f0267a0371)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c7b03c62c38c25b2aca41709799ecde0e0b69fbd43101dc4c280352d3a3c3f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__949f5c25f252f812b52feeeb3aaa127fa503dac62177b440dcf400c652a22772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformInboundSamlConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformInboundSamlConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformInboundSamlConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85dc778b4a2c7ecc8cb3313bb9044a0317137dc053a99b573a1001af8ee01e23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleIdentityPlatformInboundSamlConfig",
    "GoogleIdentityPlatformInboundSamlConfigConfig",
    "GoogleIdentityPlatformInboundSamlConfigIdpConfig",
    "GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificates",
    "GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificatesList",
    "GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificatesOutputReference",
    "GoogleIdentityPlatformInboundSamlConfigIdpConfigOutputReference",
    "GoogleIdentityPlatformInboundSamlConfigSpConfig",
    "GoogleIdentityPlatformInboundSamlConfigSpConfigOutputReference",
    "GoogleIdentityPlatformInboundSamlConfigSpConfigSpCertificates",
    "GoogleIdentityPlatformInboundSamlConfigSpConfigSpCertificatesList",
    "GoogleIdentityPlatformInboundSamlConfigSpConfigSpCertificatesOutputReference",
    "GoogleIdentityPlatformInboundSamlConfigTimeouts",
    "GoogleIdentityPlatformInboundSamlConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__98a33115f7670a576942ff78226b4310068fc3620dde267c5e577cf528102334(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    idp_config: typing.Union[GoogleIdentityPlatformInboundSamlConfigIdpConfig, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    sp_config: typing.Union[GoogleIdentityPlatformInboundSamlConfigSpConfig, typing.Dict[builtins.str, typing.Any]],
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleIdentityPlatformInboundSamlConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__80610a0b1cc1f85dcf786ca68ae4e27ddb8d50dfc866a5e9c56d6089820bf02f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bba59df1f3674d8d9b98f54f62a660458232f722e2fc57872d8a0debeac9cad9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec9a636b592241797d5434e4b6f219b3754ec6c5bb61c69a198b05f360a859eb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51edcdd4d4f0791d1c8c4f8601897be6406e0cc78c9cfd43b9f0345745c54168(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0430250f83b9256b2a3b8c5e1b0e4c0e76790ceb3ecf7a819ff14fad261a1dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f4098f30730031fcf13241a6c6fcc6c329c3aa00c3cd4b42dacdc5ac31fc805(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9edc077ea15de81489d521cc97666bde7b364c1e3fcb6794e3e3ea12000a2be(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    idp_config: typing.Union[GoogleIdentityPlatformInboundSamlConfigIdpConfig, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    sp_config: typing.Union[GoogleIdentityPlatformInboundSamlConfigSpConfig, typing.Dict[builtins.str, typing.Any]],
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleIdentityPlatformInboundSamlConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af71df490e4e6f44fde7dcd65091cb0fa544b353ee4fbbecfa699f009b45fa3(
    *,
    idp_certificates: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificates, typing.Dict[builtins.str, typing.Any]]]],
    idp_entity_id: builtins.str,
    sso_url: builtins.str,
    sign_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac11b7d0c1cdf783398a543b307840216b5fde470b25587df2656063050b5bb5(
    *,
    x509_certificate: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9015c2df8b721b7f32826c8dd1594a27327b8003ef117b6158cbae029a85c65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb2be6d3a9b499a7a4a3b3ea39a1dbe88c46113dbd06f0f177c26d595a6700d7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8bf1f304a84dbfdcbffb152ac9de927f5169a10f31485cf7ed7669b7fe4b937(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a271ef4eaab894cf1c5b875cfd1538435ded1401a91d60a9c0e764a44a0529(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d4d747ce1f6bfe6410981e10c3a204150773c7dcf960b244354452e3f2c459(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d372b61ce9a145215222ade0b4e1a560c5797be8a5fba5b7e7379f626a5710d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificates]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac97eec91fa996577e28fe568a4453766ab3f0d6bc6f70c1d21be29484a22987(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a664cee19a2918e0f760a592420202ab895740aee16aa50e1fe246e57338bcfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145799a5f9f344bbd7fc47fc0dbee364f408dee3e5bfb569021addf940b750b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificates]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ce12e914d63f126c5f6939fd994b70641e5c9245071b4d86a47b0b7c7d1219(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd17170ce5cf9b14b9d25d257a92ca7098e16f1274f10b26f5930a9ff7d4e968(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIdentityPlatformInboundSamlConfigIdpConfigIdpCertificates, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__605f67605173a6304403922b03cac2a84553475a3ada9d1e8814b53c00a8d1e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a9210702639d9ea5488fc2db36f6083b32fcd80cedb2aa4032a7c3052d53d83(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a43b4aa58c6496a1dbe330b8a8727ae9b2eb93720b7273c0f661446ce34482(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e57b979e6d47ae15bb7fca94e662e36a29e2df685b11a5ed742659c994681e(
    value: typing.Optional[GoogleIdentityPlatformInboundSamlConfigIdpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd331293d2752fc19a02684ff6a15068a1fe182330c70cfccb3681672d25ccee(
    *,
    callback_uri: typing.Optional[builtins.str] = None,
    sp_entity_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68a8289db6ee0e9de68765fae7e2596fd32decb3930a31e9638295e8917a3c48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1b5eb0a435e7bc86cdeb679d00623381d460bf8f875dd748ad254554dec69ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c4513f97eb47168959c06821bdf4e744c75188dd642d3c175f70fe0677d4e2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70759fe7819cee63f3128988ba28d35e43d878f92ea7d57840959665f346f519(
    value: typing.Optional[GoogleIdentityPlatformInboundSamlConfigSpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c88083d6922d095c477bfea0139b3442801699c937c67e575d52e6d8f8be153(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151c0b7c013f779fd9dad9570641fba38a36cda91f781e6736f2aa931e2050ca(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c374bb4df1f16c16bcce0a9952ff9bb662eb044885baff3c30aec7dd3d81069(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e9dad2cc392c96fa28f268fd9a179838cafe99654f07e97f887fee05249ee7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b7388b8b87ae3477fe5bbb8b446191b062de6cd00e5f73f6a2888da8c4abe6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f021848dfa36bf3f7500b7198a8ddf71d4023646892ef7962b7040a85983d03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fee937cdebf92a850ce2d0484cc9191536c1a74c0f11c007c3776620d84fcd58(
    value: typing.Optional[GoogleIdentityPlatformInboundSamlConfigSpConfigSpCertificates],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e999b18ce545b64bac2d25444a78a2edf13251e96f5affdbd34496f2d8dbe204(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c32850c0c586ba0111dad3130ec35ca32f44ba92251699c4b1120ec737afe23(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf92b9b5a14a596eac21fa1a4ac0907371c2d17744af541152c21f0267a0371(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7b03c62c38c25b2aca41709799ecde0e0b69fbd43101dc4c280352d3a3c3f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__949f5c25f252f812b52feeeb3aaa127fa503dac62177b440dcf400c652a22772(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85dc778b4a2c7ecc8cb3313bb9044a0317137dc053a99b573a1001af8ee01e23(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformInboundSamlConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
