r'''
# `google_identity_platform_tenant_inbound_saml_config`

Refer to the Terraform Registry for docs: [`google_identity_platform_tenant_inbound_saml_config`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config).
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


class IdentityPlatformTenantInboundSamlConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformTenantInboundSamlConfig.IdentityPlatformTenantInboundSamlConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config google_identity_platform_tenant_inbound_saml_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        idp_config: typing.Union["IdentityPlatformTenantInboundSamlConfigIdpConfig", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        sp_config: typing.Union["IdentityPlatformTenantInboundSamlConfigSpConfig", typing.Dict[builtins.str, typing.Any]],
        tenant: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["IdentityPlatformTenantInboundSamlConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config google_identity_platform_tenant_inbound_saml_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: Human friendly display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#display_name IdentityPlatformTenantInboundSamlConfig#display_name}
        :param idp_config: idp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#idp_config IdentityPlatformTenantInboundSamlConfig#idp_config}
        :param name: The name of the InboundSamlConfig resource. Must start with 'saml.' and can only have alphanumeric characters, hyphens, underscores or periods. The part after 'saml.' must also start with a lowercase letter, end with an alphanumeric character, and have at least 2 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#name IdentityPlatformTenantInboundSamlConfig#name}
        :param sp_config: sp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#sp_config IdentityPlatformTenantInboundSamlConfig#sp_config}
        :param tenant: The name of the tenant where this inbound SAML config resource exists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#tenant IdentityPlatformTenantInboundSamlConfig#tenant}
        :param enabled: If this config allows users to sign in with the provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#enabled IdentityPlatformTenantInboundSamlConfig#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#id IdentityPlatformTenantInboundSamlConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#project IdentityPlatformTenantInboundSamlConfig#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#timeouts IdentityPlatformTenantInboundSamlConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fb38c347c1d3b15aa3ca0a272c52038426ad62dd8b5064a49b38d6ae0864ccd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IdentityPlatformTenantInboundSamlConfigConfig(
            display_name=display_name,
            idp_config=idp_config,
            name=name,
            sp_config=sp_config,
            tenant=tenant,
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
        '''Generates CDKTF code for importing a IdentityPlatformTenantInboundSamlConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IdentityPlatformTenantInboundSamlConfig to import.
        :param import_from_id: The id of the existing IdentityPlatformTenantInboundSamlConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IdentityPlatformTenantInboundSamlConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10d87cf9ac6405484bb0bddb4edad7fa51c715dc3da20d9284e75fc4d4c6f11d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIdpConfig")
    def put_idp_config(
        self,
        *,
        idp_certificates: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificates", typing.Dict[builtins.str, typing.Any]]]],
        idp_entity_id: builtins.str,
        sso_url: builtins.str,
        sign_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param idp_certificates: idp_certificates block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#idp_certificates IdentityPlatformTenantInboundSamlConfig#idp_certificates}
        :param idp_entity_id: Unique identifier for all SAML entities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#idp_entity_id IdentityPlatformTenantInboundSamlConfig#idp_entity_id}
        :param sso_url: URL to send Authentication request to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#sso_url IdentityPlatformTenantInboundSamlConfig#sso_url}
        :param sign_request: Indicates if outbounding SAMLRequest should be signed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#sign_request IdentityPlatformTenantInboundSamlConfig#sign_request}
        '''
        value = IdentityPlatformTenantInboundSamlConfigIdpConfig(
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
        callback_uri: builtins.str,
        sp_entity_id: builtins.str,
    ) -> None:
        '''
        :param callback_uri: Callback URI where responses from IDP are handled. Must start with 'https://'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#callback_uri IdentityPlatformTenantInboundSamlConfig#callback_uri}
        :param sp_entity_id: Unique identifier for all SAML entities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#sp_entity_id IdentityPlatformTenantInboundSamlConfig#sp_entity_id}
        '''
        value = IdentityPlatformTenantInboundSamlConfigSpConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#create IdentityPlatformTenantInboundSamlConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#delete IdentityPlatformTenantInboundSamlConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#update IdentityPlatformTenantInboundSamlConfig#update}.
        '''
        value = IdentityPlatformTenantInboundSamlConfigTimeouts(
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
    ) -> "IdentityPlatformTenantInboundSamlConfigIdpConfigOutputReference":
        return typing.cast("IdentityPlatformTenantInboundSamlConfigIdpConfigOutputReference", jsii.get(self, "idpConfig"))

    @builtins.property
    @jsii.member(jsii_name="spConfig")
    def sp_config(
        self,
    ) -> "IdentityPlatformTenantInboundSamlConfigSpConfigOutputReference":
        return typing.cast("IdentityPlatformTenantInboundSamlConfigSpConfigOutputReference", jsii.get(self, "spConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "IdentityPlatformTenantInboundSamlConfigTimeoutsOutputReference":
        return typing.cast("IdentityPlatformTenantInboundSamlConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["IdentityPlatformTenantInboundSamlConfigIdpConfig"]:
        return typing.cast(typing.Optional["IdentityPlatformTenantInboundSamlConfigIdpConfig"], jsii.get(self, "idpConfigInput"))

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
    ) -> typing.Optional["IdentityPlatformTenantInboundSamlConfigSpConfig"]:
        return typing.cast(typing.Optional["IdentityPlatformTenantInboundSamlConfigSpConfig"], jsii.get(self, "spConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantInput")
    def tenant_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IdentityPlatformTenantInboundSamlConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IdentityPlatformTenantInboundSamlConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c73f0e1cd6840667e4ee555815d2daa3b9d206e39e18c7776faceb8badee5dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0f2a4356c7bbfafe06b5940030ee1f9300598830102d4b4ebdaa5f9f41ec76d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37ec3c75e1038c1fd756905f5187c5ad8861cea34445b177b6eb28f10d32b0a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cda47463607dfefe8127a64649b94e9b22f8d2010cd4be1393ab7c1254df1d91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9bfa8e0792a39124db3b6baf5ec67864eff7f529e59d3df99e2f51bc21ef767)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenant")
    def tenant(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenant"))

    @tenant.setter
    def tenant(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af7d7e44f08bf42acbbf42e6984426cdbbfa0980f6a85427f46584b090bbe9b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenant", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.identityPlatformTenantInboundSamlConfig.IdentityPlatformTenantInboundSamlConfigConfig",
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
        "tenant": "tenant",
        "enabled": "enabled",
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class IdentityPlatformTenantInboundSamlConfigConfig(
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
        idp_config: typing.Union["IdentityPlatformTenantInboundSamlConfigIdpConfig", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        sp_config: typing.Union["IdentityPlatformTenantInboundSamlConfigSpConfig", typing.Dict[builtins.str, typing.Any]],
        tenant: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["IdentityPlatformTenantInboundSamlConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: Human friendly display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#display_name IdentityPlatformTenantInboundSamlConfig#display_name}
        :param idp_config: idp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#idp_config IdentityPlatformTenantInboundSamlConfig#idp_config}
        :param name: The name of the InboundSamlConfig resource. Must start with 'saml.' and can only have alphanumeric characters, hyphens, underscores or periods. The part after 'saml.' must also start with a lowercase letter, end with an alphanumeric character, and have at least 2 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#name IdentityPlatformTenantInboundSamlConfig#name}
        :param sp_config: sp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#sp_config IdentityPlatformTenantInboundSamlConfig#sp_config}
        :param tenant: The name of the tenant where this inbound SAML config resource exists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#tenant IdentityPlatformTenantInboundSamlConfig#tenant}
        :param enabled: If this config allows users to sign in with the provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#enabled IdentityPlatformTenantInboundSamlConfig#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#id IdentityPlatformTenantInboundSamlConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#project IdentityPlatformTenantInboundSamlConfig#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#timeouts IdentityPlatformTenantInboundSamlConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(idp_config, dict):
            idp_config = IdentityPlatformTenantInboundSamlConfigIdpConfig(**idp_config)
        if isinstance(sp_config, dict):
            sp_config = IdentityPlatformTenantInboundSamlConfigSpConfig(**sp_config)
        if isinstance(timeouts, dict):
            timeouts = IdentityPlatformTenantInboundSamlConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ab5bd95a99b004e50816f4866d9e1824761a335820ffd04d741347b015ca5be)
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
            check_type(argname="argument tenant", value=tenant, expected_type=type_hints["tenant"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "idp_config": idp_config,
            "name": name,
            "sp_config": sp_config,
            "tenant": tenant,
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#display_name IdentityPlatformTenantInboundSamlConfig#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def idp_config(self) -> "IdentityPlatformTenantInboundSamlConfigIdpConfig":
        '''idp_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#idp_config IdentityPlatformTenantInboundSamlConfig#idp_config}
        '''
        result = self._values.get("idp_config")
        assert result is not None, "Required property 'idp_config' is missing"
        return typing.cast("IdentityPlatformTenantInboundSamlConfigIdpConfig", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the InboundSamlConfig resource.

        Must start with 'saml.' and can only have alphanumeric characters,
        hyphens, underscores or periods. The part after 'saml.' must also start with a lowercase letter, end with an
        alphanumeric character, and have at least 2 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#name IdentityPlatformTenantInboundSamlConfig#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sp_config(self) -> "IdentityPlatformTenantInboundSamlConfigSpConfig":
        '''sp_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#sp_config IdentityPlatformTenantInboundSamlConfig#sp_config}
        '''
        result = self._values.get("sp_config")
        assert result is not None, "Required property 'sp_config' is missing"
        return typing.cast("IdentityPlatformTenantInboundSamlConfigSpConfig", result)

    @builtins.property
    def tenant(self) -> builtins.str:
        '''The name of the tenant where this inbound SAML config resource exists.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#tenant IdentityPlatformTenantInboundSamlConfig#tenant}
        '''
        result = self._values.get("tenant")
        assert result is not None, "Required property 'tenant' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If this config allows users to sign in with the provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#enabled IdentityPlatformTenantInboundSamlConfig#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#id IdentityPlatformTenantInboundSamlConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#project IdentityPlatformTenantInboundSamlConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["IdentityPlatformTenantInboundSamlConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#timeouts IdentityPlatformTenantInboundSamlConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["IdentityPlatformTenantInboundSamlConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPlatformTenantInboundSamlConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.identityPlatformTenantInboundSamlConfig.IdentityPlatformTenantInboundSamlConfigIdpConfig",
    jsii_struct_bases=[],
    name_mapping={
        "idp_certificates": "idpCertificates",
        "idp_entity_id": "idpEntityId",
        "sso_url": "ssoUrl",
        "sign_request": "signRequest",
    },
)
class IdentityPlatformTenantInboundSamlConfigIdpConfig:
    def __init__(
        self,
        *,
        idp_certificates: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificates", typing.Dict[builtins.str, typing.Any]]]],
        idp_entity_id: builtins.str,
        sso_url: builtins.str,
        sign_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param idp_certificates: idp_certificates block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#idp_certificates IdentityPlatformTenantInboundSamlConfig#idp_certificates}
        :param idp_entity_id: Unique identifier for all SAML entities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#idp_entity_id IdentityPlatformTenantInboundSamlConfig#idp_entity_id}
        :param sso_url: URL to send Authentication request to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#sso_url IdentityPlatformTenantInboundSamlConfig#sso_url}
        :param sign_request: Indicates if outbounding SAMLRequest should be signed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#sign_request IdentityPlatformTenantInboundSamlConfig#sign_request}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a41b680046b7b3a2441cc5b960c59230dc8f867aca405995158ad8dd405ec84c)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificates"]]:
        '''idp_certificates block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#idp_certificates IdentityPlatformTenantInboundSamlConfig#idp_certificates}
        '''
        result = self._values.get("idp_certificates")
        assert result is not None, "Required property 'idp_certificates' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificates"]], result)

    @builtins.property
    def idp_entity_id(self) -> builtins.str:
        '''Unique identifier for all SAML entities.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#idp_entity_id IdentityPlatformTenantInboundSamlConfig#idp_entity_id}
        '''
        result = self._values.get("idp_entity_id")
        assert result is not None, "Required property 'idp_entity_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sso_url(self) -> builtins.str:
        '''URL to send Authentication request to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#sso_url IdentityPlatformTenantInboundSamlConfig#sso_url}
        '''
        result = self._values.get("sso_url")
        assert result is not None, "Required property 'sso_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sign_request(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if outbounding SAMLRequest should be signed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#sign_request IdentityPlatformTenantInboundSamlConfig#sign_request}
        '''
        result = self._values.get("sign_request")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPlatformTenantInboundSamlConfigIdpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.identityPlatformTenantInboundSamlConfig.IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificates",
    jsii_struct_bases=[],
    name_mapping={"x509_certificate": "x509Certificate"},
)
class IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificates:
    def __init__(
        self,
        *,
        x509_certificate: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param x509_certificate: The x509 certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#x509_certificate IdentityPlatformTenantInboundSamlConfig#x509_certificate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b6b4bc23ebdbe84f7076de22dc46f3e2a0662d75d2904e735c4e5eb65fb7afb)
            check_type(argname="argument x509_certificate", value=x509_certificate, expected_type=type_hints["x509_certificate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if x509_certificate is not None:
            self._values["x509_certificate"] = x509_certificate

    @builtins.property
    def x509_certificate(self) -> typing.Optional[builtins.str]:
        '''The x509 certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#x509_certificate IdentityPlatformTenantInboundSamlConfig#x509_certificate}
        '''
        result = self._values.get("x509_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificates(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificatesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformTenantInboundSamlConfig.IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificatesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bc1a644463d3cff63490f73541078f0e339974c305d67f7882d6c65ebcde38a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificatesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef9d0befb37a142b4588cb366986b76141aa21017cb6103ca766fb5a4394a435)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificatesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dc37c5212fd2a3ed4529b1713c3921dfb01facb44691f10e404b32af965a89f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f8b6c528984730dbd5bfad227ba260527fac9f6189c81f4b0119bc7e59c8b15)
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
            type_hints = typing.get_type_hints(_typecheckingstub__622bce1db4e83da558329c4866f428beea88417b0ed96d1d9aff405d358413c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificates]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificates]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificates]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2b3d59b2fcfa7b03a264abdaa5384d38d7cc7117c4eeea069d61f33396e5b03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificatesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformTenantInboundSamlConfig.IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificatesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__081bbe1e5b87b163d4df2217133a59f972ce709b82f2b40cb7c076a074eea9af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48a4d38554ca74b5b4ed679a56747b5061235c5bb3a073683444d5fdd45756f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "x509Certificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificates]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificates]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificates]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__608f96cf1142dd878fdda4ab5c4d193e07d548e8ff51e76702d74901fb76fa2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IdentityPlatformTenantInboundSamlConfigIdpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformTenantInboundSamlConfig.IdentityPlatformTenantInboundSamlConfigIdpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fefe135f3d1f8580e19556c40984f9fff14e4195557a5a031e3a23340d9713ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIdpCertificates")
    def put_idp_certificates(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificates, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f41baf809c1005956cc116eae4c5fb1f029ae91ac0c48dd6ab7a437153fa0a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIdpCertificates", [value]))

    @jsii.member(jsii_name="resetSignRequest")
    def reset_sign_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignRequest", []))

    @builtins.property
    @jsii.member(jsii_name="idpCertificates")
    def idp_certificates(
        self,
    ) -> IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificatesList:
        return typing.cast(IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificatesList, jsii.get(self, "idpCertificates"))

    @builtins.property
    @jsii.member(jsii_name="idpCertificatesInput")
    def idp_certificates_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificates]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificates]]], jsii.get(self, "idpCertificatesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e06bbb4a31bf5596448e81da150ac77509629a649321bddb1997377c8a374993)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa3c5e74c182efb49c15bffd5b832930d50d8a2a8818460d1d8bb85076f1250f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signRequest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ssoUrl")
    def sso_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ssoUrl"))

    @sso_url.setter
    def sso_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ab3f0af7e4f43883a620a2c7c65240fbbf3568836687142c8658621d70dff9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssoUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IdentityPlatformTenantInboundSamlConfigIdpConfig]:
        return typing.cast(typing.Optional[IdentityPlatformTenantInboundSamlConfigIdpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IdentityPlatformTenantInboundSamlConfigIdpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23331ff64384652db6fefec485bcfcc46c05a8afa637aa99c443e6f66861e33d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.identityPlatformTenantInboundSamlConfig.IdentityPlatformTenantInboundSamlConfigSpConfig",
    jsii_struct_bases=[],
    name_mapping={"callback_uri": "callbackUri", "sp_entity_id": "spEntityId"},
)
class IdentityPlatformTenantInboundSamlConfigSpConfig:
    def __init__(
        self,
        *,
        callback_uri: builtins.str,
        sp_entity_id: builtins.str,
    ) -> None:
        '''
        :param callback_uri: Callback URI where responses from IDP are handled. Must start with 'https://'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#callback_uri IdentityPlatformTenantInboundSamlConfig#callback_uri}
        :param sp_entity_id: Unique identifier for all SAML entities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#sp_entity_id IdentityPlatformTenantInboundSamlConfig#sp_entity_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd16326d913ec3432ca7306030be0b9ac944fdfe213f410a530ecf4e16332f3e)
            check_type(argname="argument callback_uri", value=callback_uri, expected_type=type_hints["callback_uri"])
            check_type(argname="argument sp_entity_id", value=sp_entity_id, expected_type=type_hints["sp_entity_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "callback_uri": callback_uri,
            "sp_entity_id": sp_entity_id,
        }

    @builtins.property
    def callback_uri(self) -> builtins.str:
        '''Callback URI where responses from IDP are handled. Must start with 'https://'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#callback_uri IdentityPlatformTenantInboundSamlConfig#callback_uri}
        '''
        result = self._values.get("callback_uri")
        assert result is not None, "Required property 'callback_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sp_entity_id(self) -> builtins.str:
        '''Unique identifier for all SAML entities.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#sp_entity_id IdentityPlatformTenantInboundSamlConfig#sp_entity_id}
        '''
        result = self._values.get("sp_entity_id")
        assert result is not None, "Required property 'sp_entity_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPlatformTenantInboundSamlConfigSpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IdentityPlatformTenantInboundSamlConfigSpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformTenantInboundSamlConfig.IdentityPlatformTenantInboundSamlConfigSpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39bd3d1124089f7087253f2920faf5286f4de7fe66d05a16c52b20957b32ee60)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="spCertificates")
    def sp_certificates(
        self,
    ) -> "IdentityPlatformTenantInboundSamlConfigSpConfigSpCertificatesList":
        return typing.cast("IdentityPlatformTenantInboundSamlConfigSpConfigSpCertificatesList", jsii.get(self, "spCertificates"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__12cd9f3a54e810ce9cd9cf1e1583d8e7c460527158199cfb2e766f89d2e07a62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "callbackUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="spEntityId")
    def sp_entity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "spEntityId"))

    @sp_entity_id.setter
    def sp_entity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__485c11404396a9c5dd15863d31f2047abcc9bcc9c5426757610e60e009496654)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spEntityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IdentityPlatformTenantInboundSamlConfigSpConfig]:
        return typing.cast(typing.Optional[IdentityPlatformTenantInboundSamlConfigSpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IdentityPlatformTenantInboundSamlConfigSpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8453244d7bbccd5c8d9ce7dae4eb66600388f77d8cba405171981479d66216a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.identityPlatformTenantInboundSamlConfig.IdentityPlatformTenantInboundSamlConfigSpConfigSpCertificates",
    jsii_struct_bases=[],
    name_mapping={},
)
class IdentityPlatformTenantInboundSamlConfigSpConfigSpCertificates:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPlatformTenantInboundSamlConfigSpConfigSpCertificates(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IdentityPlatformTenantInboundSamlConfigSpConfigSpCertificatesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformTenantInboundSamlConfig.IdentityPlatformTenantInboundSamlConfigSpConfigSpCertificatesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22b6fc03f2a34e71ffa1c85e888c895231d0b069cae38fd324a1bdfd0a0ef78d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IdentityPlatformTenantInboundSamlConfigSpConfigSpCertificatesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8c8a0dc724b30e1e7d4251182eaaac38a774a719816e2a1d9da9d07f7018325)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IdentityPlatformTenantInboundSamlConfigSpConfigSpCertificatesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d21eb31eb026a72c461f030a0e587adaf36625a188f2ec32aeb0d5cd0aebd445)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a201e0728127c2dee1d22b55bf39ae30445b30ce4f5ff503ce8a75b6c8a39d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2b340348865d730d562b1322888e6d9481cfd3f7c6939e50a42510f15cd9743)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class IdentityPlatformTenantInboundSamlConfigSpConfigSpCertificatesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformTenantInboundSamlConfig.IdentityPlatformTenantInboundSamlConfigSpConfigSpCertificatesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9185ec32a3cc7343586c5eeb516847e6b2fb315593147e5082b30ec9fd054847)
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
    ) -> typing.Optional[IdentityPlatformTenantInboundSamlConfigSpConfigSpCertificates]:
        return typing.cast(typing.Optional[IdentityPlatformTenantInboundSamlConfigSpConfigSpCertificates], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IdentityPlatformTenantInboundSamlConfigSpConfigSpCertificates],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04057f73f791dcba6e98c571738e8a4e9a9ff812e5248ab68c99aa6e760d7901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.identityPlatformTenantInboundSamlConfig.IdentityPlatformTenantInboundSamlConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class IdentityPlatformTenantInboundSamlConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#create IdentityPlatformTenantInboundSamlConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#delete IdentityPlatformTenantInboundSamlConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#update IdentityPlatformTenantInboundSamlConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0efb5ae3bc0a3163d3f58edc10365b72a4b1338d5730d986e5f50399a7805be2)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#create IdentityPlatformTenantInboundSamlConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#delete IdentityPlatformTenantInboundSamlConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_tenant_inbound_saml_config#update IdentityPlatformTenantInboundSamlConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPlatformTenantInboundSamlConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IdentityPlatformTenantInboundSamlConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformTenantInboundSamlConfig.IdentityPlatformTenantInboundSamlConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__995fddc9866f5f7c7eb383d5efa28266e33583cfb099ddd9e858d19332c19f46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be7f613ae3bb66fd2aadb9f769751d7d9a2aa9c87eeb7fd545d19f3bab2bd782)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0c30759a5059a2b36734e851b69137753d41eaa57e9fafac2875326ae4e0742)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3cfe870a5961e642ed787210ee8738674985056e94915e327b62cbd31cbd1a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IdentityPlatformTenantInboundSamlConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IdentityPlatformTenantInboundSamlConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IdentityPlatformTenantInboundSamlConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__756c5f5c00408123bd97955bfe04fa3c9e644441294e5340c1867709a1cfbd10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "IdentityPlatformTenantInboundSamlConfig",
    "IdentityPlatformTenantInboundSamlConfigConfig",
    "IdentityPlatformTenantInboundSamlConfigIdpConfig",
    "IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificates",
    "IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificatesList",
    "IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificatesOutputReference",
    "IdentityPlatformTenantInboundSamlConfigIdpConfigOutputReference",
    "IdentityPlatformTenantInboundSamlConfigSpConfig",
    "IdentityPlatformTenantInboundSamlConfigSpConfigOutputReference",
    "IdentityPlatformTenantInboundSamlConfigSpConfigSpCertificates",
    "IdentityPlatformTenantInboundSamlConfigSpConfigSpCertificatesList",
    "IdentityPlatformTenantInboundSamlConfigSpConfigSpCertificatesOutputReference",
    "IdentityPlatformTenantInboundSamlConfigTimeouts",
    "IdentityPlatformTenantInboundSamlConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0fb38c347c1d3b15aa3ca0a272c52038426ad62dd8b5064a49b38d6ae0864ccd(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    idp_config: typing.Union[IdentityPlatformTenantInboundSamlConfigIdpConfig, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    sp_config: typing.Union[IdentityPlatformTenantInboundSamlConfigSpConfig, typing.Dict[builtins.str, typing.Any]],
    tenant: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[IdentityPlatformTenantInboundSamlConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__10d87cf9ac6405484bb0bddb4edad7fa51c715dc3da20d9284e75fc4d4c6f11d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c73f0e1cd6840667e4ee555815d2daa3b9d206e39e18c7776faceb8badee5dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f2a4356c7bbfafe06b5940030ee1f9300598830102d4b4ebdaa5f9f41ec76d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37ec3c75e1038c1fd756905f5187c5ad8861cea34445b177b6eb28f10d32b0a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda47463607dfefe8127a64649b94e9b22f8d2010cd4be1393ab7c1254df1d91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9bfa8e0792a39124db3b6baf5ec67864eff7f529e59d3df99e2f51bc21ef767(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7d7e44f08bf42acbbf42e6984426cdbbfa0980f6a85427f46584b090bbe9b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ab5bd95a99b004e50816f4866d9e1824761a335820ffd04d741347b015ca5be(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    idp_config: typing.Union[IdentityPlatformTenantInboundSamlConfigIdpConfig, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    sp_config: typing.Union[IdentityPlatformTenantInboundSamlConfigSpConfig, typing.Dict[builtins.str, typing.Any]],
    tenant: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[IdentityPlatformTenantInboundSamlConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41b680046b7b3a2441cc5b960c59230dc8f867aca405995158ad8dd405ec84c(
    *,
    idp_certificates: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificates, typing.Dict[builtins.str, typing.Any]]]],
    idp_entity_id: builtins.str,
    sso_url: builtins.str,
    sign_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6b4bc23ebdbe84f7076de22dc46f3e2a0662d75d2904e735c4e5eb65fb7afb(
    *,
    x509_certificate: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc1a644463d3cff63490f73541078f0e339974c305d67f7882d6c65ebcde38a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef9d0befb37a142b4588cb366986b76141aa21017cb6103ca766fb5a4394a435(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dc37c5212fd2a3ed4529b1713c3921dfb01facb44691f10e404b32af965a89f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f8b6c528984730dbd5bfad227ba260527fac9f6189c81f4b0119bc7e59c8b15(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622bce1db4e83da558329c4866f428beea88417b0ed96d1d9aff405d358413c4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2b3d59b2fcfa7b03a264abdaa5384d38d7cc7117c4eeea069d61f33396e5b03(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificates]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081bbe1e5b87b163d4df2217133a59f972ce709b82f2b40cb7c076a074eea9af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48a4d38554ca74b5b4ed679a56747b5061235c5bb3a073683444d5fdd45756f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__608f96cf1142dd878fdda4ab5c4d193e07d548e8ff51e76702d74901fb76fa2c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificates]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fefe135f3d1f8580e19556c40984f9fff14e4195557a5a031e3a23340d9713ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f41baf809c1005956cc116eae4c5fb1f029ae91ac0c48dd6ab7a437153fa0a8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IdentityPlatformTenantInboundSamlConfigIdpConfigIdpCertificates, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e06bbb4a31bf5596448e81da150ac77509629a649321bddb1997377c8a374993(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3c5e74c182efb49c15bffd5b832930d50d8a2a8818460d1d8bb85076f1250f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab3f0af7e4f43883a620a2c7c65240fbbf3568836687142c8658621d70dff9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23331ff64384652db6fefec485bcfcc46c05a8afa637aa99c443e6f66861e33d(
    value: typing.Optional[IdentityPlatformTenantInboundSamlConfigIdpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd16326d913ec3432ca7306030be0b9ac944fdfe213f410a530ecf4e16332f3e(
    *,
    callback_uri: builtins.str,
    sp_entity_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39bd3d1124089f7087253f2920faf5286f4de7fe66d05a16c52b20957b32ee60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12cd9f3a54e810ce9cd9cf1e1583d8e7c460527158199cfb2e766f89d2e07a62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__485c11404396a9c5dd15863d31f2047abcc9bcc9c5426757610e60e009496654(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8453244d7bbccd5c8d9ce7dae4eb66600388f77d8cba405171981479d66216a7(
    value: typing.Optional[IdentityPlatformTenantInboundSamlConfigSpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22b6fc03f2a34e71ffa1c85e888c895231d0b069cae38fd324a1bdfd0a0ef78d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8c8a0dc724b30e1e7d4251182eaaac38a774a719816e2a1d9da9d07f7018325(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d21eb31eb026a72c461f030a0e587adaf36625a188f2ec32aeb0d5cd0aebd445(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a201e0728127c2dee1d22b55bf39ae30445b30ce4f5ff503ce8a75b6c8a39d9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b340348865d730d562b1322888e6d9481cfd3f7c6939e50a42510f15cd9743(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9185ec32a3cc7343586c5eeb516847e6b2fb315593147e5082b30ec9fd054847(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04057f73f791dcba6e98c571738e8a4e9a9ff812e5248ab68c99aa6e760d7901(
    value: typing.Optional[IdentityPlatformTenantInboundSamlConfigSpConfigSpCertificates],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0efb5ae3bc0a3163d3f58edc10365b72a4b1338d5730d986e5f50399a7805be2(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__995fddc9866f5f7c7eb383d5efa28266e33583cfb099ddd9e858d19332c19f46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be7f613ae3bb66fd2aadb9f769751d7d9a2aa9c87eeb7fd545d19f3bab2bd782(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c30759a5059a2b36734e851b69137753d41eaa57e9fafac2875326ae4e0742(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3cfe870a5961e642ed787210ee8738674985056e94915e327b62cbd31cbd1a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__756c5f5c00408123bd97955bfe04fa3c9e644441294e5340c1867709a1cfbd10(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IdentityPlatformTenantInboundSamlConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
