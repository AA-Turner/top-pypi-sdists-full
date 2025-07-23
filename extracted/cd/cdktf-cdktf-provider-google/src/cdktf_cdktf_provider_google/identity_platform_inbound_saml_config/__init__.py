r'''
# `google_identity_platform_inbound_saml_config`

Refer to the Terraform Registry for docs: [`google_identity_platform_inbound_saml_config`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config).
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


class IdentityPlatformInboundSamlConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformInboundSamlConfig.IdentityPlatformInboundSamlConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config google_identity_platform_inbound_saml_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        idp_config: typing.Union["IdentityPlatformInboundSamlConfigIdpConfig", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        sp_config: typing.Union["IdentityPlatformInboundSamlConfigSpConfig", typing.Dict[builtins.str, typing.Any]],
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["IdentityPlatformInboundSamlConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config google_identity_platform_inbound_saml_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: Human friendly display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#display_name IdentityPlatformInboundSamlConfig#display_name}
        :param idp_config: idp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#idp_config IdentityPlatformInboundSamlConfig#idp_config}
        :param name: The name of the InboundSamlConfig resource. Must start with 'saml.' and can only have alphanumeric characters, hyphens, underscores or periods. The part after 'saml.' must also start with a lowercase letter, end with an alphanumeric character, and have at least 2 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#name IdentityPlatformInboundSamlConfig#name}
        :param sp_config: sp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#sp_config IdentityPlatformInboundSamlConfig#sp_config}
        :param enabled: If this config allows users to sign in with the provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#enabled IdentityPlatformInboundSamlConfig#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#id IdentityPlatformInboundSamlConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#project IdentityPlatformInboundSamlConfig#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#timeouts IdentityPlatformInboundSamlConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bd8819cabe4f7c27c7141c9016b6809f5ade90f68d08d546dd920a74dc420ba)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IdentityPlatformInboundSamlConfigConfig(
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
        '''Generates CDKTF code for importing a IdentityPlatformInboundSamlConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IdentityPlatformInboundSamlConfig to import.
        :param import_from_id: The id of the existing IdentityPlatformInboundSamlConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IdentityPlatformInboundSamlConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__554d5b4f5e2d963d8dfbc25c980fdd3d53013d84be13216f257ba76b65487d33)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIdpConfig")
    def put_idp_config(
        self,
        *,
        idp_certificates: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IdentityPlatformInboundSamlConfigIdpConfigIdpCertificates", typing.Dict[builtins.str, typing.Any]]]],
        idp_entity_id: builtins.str,
        sso_url: builtins.str,
        sign_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param idp_certificates: idp_certificates block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#idp_certificates IdentityPlatformInboundSamlConfig#idp_certificates}
        :param idp_entity_id: Unique identifier for all SAML entities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#idp_entity_id IdentityPlatformInboundSamlConfig#idp_entity_id}
        :param sso_url: URL to send Authentication request to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#sso_url IdentityPlatformInboundSamlConfig#sso_url}
        :param sign_request: Indicates if outbounding SAMLRequest should be signed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#sign_request IdentityPlatformInboundSamlConfig#sign_request}
        '''
        value = IdentityPlatformInboundSamlConfigIdpConfig(
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
        :param callback_uri: Callback URI where responses from IDP are handled. Must start with 'https://'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#callback_uri IdentityPlatformInboundSamlConfig#callback_uri}
        :param sp_entity_id: Unique identifier for all SAML entities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#sp_entity_id IdentityPlatformInboundSamlConfig#sp_entity_id}
        '''
        value = IdentityPlatformInboundSamlConfigSpConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#create IdentityPlatformInboundSamlConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#delete IdentityPlatformInboundSamlConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#update IdentityPlatformInboundSamlConfig#update}.
        '''
        value = IdentityPlatformInboundSamlConfigTimeouts(
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
    def idp_config(self) -> "IdentityPlatformInboundSamlConfigIdpConfigOutputReference":
        return typing.cast("IdentityPlatformInboundSamlConfigIdpConfigOutputReference", jsii.get(self, "idpConfig"))

    @builtins.property
    @jsii.member(jsii_name="spConfig")
    def sp_config(self) -> "IdentityPlatformInboundSamlConfigSpConfigOutputReference":
        return typing.cast("IdentityPlatformInboundSamlConfigSpConfigOutputReference", jsii.get(self, "spConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "IdentityPlatformInboundSamlConfigTimeoutsOutputReference":
        return typing.cast("IdentityPlatformInboundSamlConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["IdentityPlatformInboundSamlConfigIdpConfig"]:
        return typing.cast(typing.Optional["IdentityPlatformInboundSamlConfigIdpConfig"], jsii.get(self, "idpConfigInput"))

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
    ) -> typing.Optional["IdentityPlatformInboundSamlConfigSpConfig"]:
        return typing.cast(typing.Optional["IdentityPlatformInboundSamlConfigSpConfig"], jsii.get(self, "spConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IdentityPlatformInboundSamlConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IdentityPlatformInboundSamlConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__272681820181cf99603889ba1232d92b6ce94feccc1d27d026fad65347bf59b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc928566175c417a149ccebe316a307b7b27de8e51e8923e67af74b5906ac15c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eaad1eccb7d4780b81794026ccb9a74f2045287b33369084e620c1f72aacb03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b5cda37fd272a00985781745f7ac85ff4f0283b01faabea3a81e0735982efa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d569aa22792e32ea8f9ff8065b363cde8fee4d299f8dd077a1434175ea60fbc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.identityPlatformInboundSamlConfig.IdentityPlatformInboundSamlConfigConfig",
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
class IdentityPlatformInboundSamlConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        idp_config: typing.Union["IdentityPlatformInboundSamlConfigIdpConfig", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        sp_config: typing.Union["IdentityPlatformInboundSamlConfigSpConfig", typing.Dict[builtins.str, typing.Any]],
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["IdentityPlatformInboundSamlConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: Human friendly display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#display_name IdentityPlatformInboundSamlConfig#display_name}
        :param idp_config: idp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#idp_config IdentityPlatformInboundSamlConfig#idp_config}
        :param name: The name of the InboundSamlConfig resource. Must start with 'saml.' and can only have alphanumeric characters, hyphens, underscores or periods. The part after 'saml.' must also start with a lowercase letter, end with an alphanumeric character, and have at least 2 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#name IdentityPlatformInboundSamlConfig#name}
        :param sp_config: sp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#sp_config IdentityPlatformInboundSamlConfig#sp_config}
        :param enabled: If this config allows users to sign in with the provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#enabled IdentityPlatformInboundSamlConfig#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#id IdentityPlatformInboundSamlConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#project IdentityPlatformInboundSamlConfig#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#timeouts IdentityPlatformInboundSamlConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(idp_config, dict):
            idp_config = IdentityPlatformInboundSamlConfigIdpConfig(**idp_config)
        if isinstance(sp_config, dict):
            sp_config = IdentityPlatformInboundSamlConfigSpConfig(**sp_config)
        if isinstance(timeouts, dict):
            timeouts = IdentityPlatformInboundSamlConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb014a31c4f757a03c90cf8be804e69f28483d7ece0c8106cd8b1ec445cf1d30)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#display_name IdentityPlatformInboundSamlConfig#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def idp_config(self) -> "IdentityPlatformInboundSamlConfigIdpConfig":
        '''idp_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#idp_config IdentityPlatformInboundSamlConfig#idp_config}
        '''
        result = self._values.get("idp_config")
        assert result is not None, "Required property 'idp_config' is missing"
        return typing.cast("IdentityPlatformInboundSamlConfigIdpConfig", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the InboundSamlConfig resource.

        Must start with 'saml.' and can only have alphanumeric characters,
        hyphens, underscores or periods. The part after 'saml.' must also start with a lowercase letter, end with an
        alphanumeric character, and have at least 2 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#name IdentityPlatformInboundSamlConfig#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sp_config(self) -> "IdentityPlatformInboundSamlConfigSpConfig":
        '''sp_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#sp_config IdentityPlatformInboundSamlConfig#sp_config}
        '''
        result = self._values.get("sp_config")
        assert result is not None, "Required property 'sp_config' is missing"
        return typing.cast("IdentityPlatformInboundSamlConfigSpConfig", result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If this config allows users to sign in with the provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#enabled IdentityPlatformInboundSamlConfig#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#id IdentityPlatformInboundSamlConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#project IdentityPlatformInboundSamlConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["IdentityPlatformInboundSamlConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#timeouts IdentityPlatformInboundSamlConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["IdentityPlatformInboundSamlConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPlatformInboundSamlConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.identityPlatformInboundSamlConfig.IdentityPlatformInboundSamlConfigIdpConfig",
    jsii_struct_bases=[],
    name_mapping={
        "idp_certificates": "idpCertificates",
        "idp_entity_id": "idpEntityId",
        "sso_url": "ssoUrl",
        "sign_request": "signRequest",
    },
)
class IdentityPlatformInboundSamlConfigIdpConfig:
    def __init__(
        self,
        *,
        idp_certificates: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IdentityPlatformInboundSamlConfigIdpConfigIdpCertificates", typing.Dict[builtins.str, typing.Any]]]],
        idp_entity_id: builtins.str,
        sso_url: builtins.str,
        sign_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param idp_certificates: idp_certificates block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#idp_certificates IdentityPlatformInboundSamlConfig#idp_certificates}
        :param idp_entity_id: Unique identifier for all SAML entities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#idp_entity_id IdentityPlatformInboundSamlConfig#idp_entity_id}
        :param sso_url: URL to send Authentication request to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#sso_url IdentityPlatformInboundSamlConfig#sso_url}
        :param sign_request: Indicates if outbounding SAMLRequest should be signed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#sign_request IdentityPlatformInboundSamlConfig#sign_request}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__659d4863035910073ade85fbf4db703a82eb897d66e8ecd0db4689bdd31d92f3)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IdentityPlatformInboundSamlConfigIdpConfigIdpCertificates"]]:
        '''idp_certificates block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#idp_certificates IdentityPlatformInboundSamlConfig#idp_certificates}
        '''
        result = self._values.get("idp_certificates")
        assert result is not None, "Required property 'idp_certificates' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IdentityPlatformInboundSamlConfigIdpConfigIdpCertificates"]], result)

    @builtins.property
    def idp_entity_id(self) -> builtins.str:
        '''Unique identifier for all SAML entities.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#idp_entity_id IdentityPlatformInboundSamlConfig#idp_entity_id}
        '''
        result = self._values.get("idp_entity_id")
        assert result is not None, "Required property 'idp_entity_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sso_url(self) -> builtins.str:
        '''URL to send Authentication request to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#sso_url IdentityPlatformInboundSamlConfig#sso_url}
        '''
        result = self._values.get("sso_url")
        assert result is not None, "Required property 'sso_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sign_request(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if outbounding SAMLRequest should be signed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#sign_request IdentityPlatformInboundSamlConfig#sign_request}
        '''
        result = self._values.get("sign_request")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPlatformInboundSamlConfigIdpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.identityPlatformInboundSamlConfig.IdentityPlatformInboundSamlConfigIdpConfigIdpCertificates",
    jsii_struct_bases=[],
    name_mapping={"x509_certificate": "x509Certificate"},
)
class IdentityPlatformInboundSamlConfigIdpConfigIdpCertificates:
    def __init__(
        self,
        *,
        x509_certificate: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param x509_certificate: The IdP's x509 certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#x509_certificate IdentityPlatformInboundSamlConfig#x509_certificate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e34b149dac548380562c285c03155e710699687ea1b9729d84d1c9b85f57847)
            check_type(argname="argument x509_certificate", value=x509_certificate, expected_type=type_hints["x509_certificate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if x509_certificate is not None:
            self._values["x509_certificate"] = x509_certificate

    @builtins.property
    def x509_certificate(self) -> typing.Optional[builtins.str]:
        '''The IdP's x509 certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#x509_certificate IdentityPlatformInboundSamlConfig#x509_certificate}
        '''
        result = self._values.get("x509_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPlatformInboundSamlConfigIdpConfigIdpCertificates(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IdentityPlatformInboundSamlConfigIdpConfigIdpCertificatesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformInboundSamlConfig.IdentityPlatformInboundSamlConfigIdpConfigIdpCertificatesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a2840715c42ced8b8a175780d224a2df23f06ff92d887802e117ffb576269a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IdentityPlatformInboundSamlConfigIdpConfigIdpCertificatesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f36a3d0dd4f904c88b2a7a2b44299b8d9e5c2cb9816f1afed217b49bf0bffa0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IdentityPlatformInboundSamlConfigIdpConfigIdpCertificatesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af2e77c76b3532a0545a85f48f149c7664fd0f04bdecb4600c70247a9c97421c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a18e9f435ac6673224aab2760758930467c971af4361cd5e3795da56e053f938)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0242af7d9a2539bd308eea9fef8c39e8177c5e78ec75f496f0ce25ee5555f811)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IdentityPlatformInboundSamlConfigIdpConfigIdpCertificates]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IdentityPlatformInboundSamlConfigIdpConfigIdpCertificates]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IdentityPlatformInboundSamlConfigIdpConfigIdpCertificates]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5417179b7319922aea0cf90d8fdef40fb0e78767380061a5bc81291d16d1dec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IdentityPlatformInboundSamlConfigIdpConfigIdpCertificatesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformInboundSamlConfig.IdentityPlatformInboundSamlConfigIdpConfigIdpCertificatesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd3400e2074adfad6d52c1b2b2be649c2ecb9653135ed943ab0a076b7bb33c79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49e02432140f343e5e39f06d2aa6c6ecac69b0bc6115cf7c6c85975373c93496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "x509Certificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IdentityPlatformInboundSamlConfigIdpConfigIdpCertificates]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IdentityPlatformInboundSamlConfigIdpConfigIdpCertificates]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IdentityPlatformInboundSamlConfigIdpConfigIdpCertificates]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__824cb007e845454891ce17c02f8865dfecdaf2ae3a7e881d2baf8739b4517c90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IdentityPlatformInboundSamlConfigIdpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformInboundSamlConfig.IdentityPlatformInboundSamlConfigIdpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5f5ad3a7dbd4d4c127ac6b8bb106c8e4c065a61800e95df1fde810ec9ae1297)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIdpCertificates")
    def put_idp_certificates(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IdentityPlatformInboundSamlConfigIdpConfigIdpCertificates, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e1ce43338ac9b1b4a26f56642c586b7aa06cfa922bec9f05272cee34b552c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIdpCertificates", [value]))

    @jsii.member(jsii_name="resetSignRequest")
    def reset_sign_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignRequest", []))

    @builtins.property
    @jsii.member(jsii_name="idpCertificates")
    def idp_certificates(
        self,
    ) -> IdentityPlatformInboundSamlConfigIdpConfigIdpCertificatesList:
        return typing.cast(IdentityPlatformInboundSamlConfigIdpConfigIdpCertificatesList, jsii.get(self, "idpCertificates"))

    @builtins.property
    @jsii.member(jsii_name="idpCertificatesInput")
    def idp_certificates_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IdentityPlatformInboundSamlConfigIdpConfigIdpCertificates]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IdentityPlatformInboundSamlConfigIdpConfigIdpCertificates]]], jsii.get(self, "idpCertificatesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__01a097c33108f29a811fb435eabdefa1a3e6d356c20011d32260474fd0d2526a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fa1ca50f82599b1b0289fc69606fe90216c37d673169cd49bce88e8cde2789b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signRequest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ssoUrl")
    def sso_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ssoUrl"))

    @sso_url.setter
    def sso_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f37796a92a3977d4974faa2971a8f7e7e7206e9dcd918daad1d2c358fb24521e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssoUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IdentityPlatformInboundSamlConfigIdpConfig]:
        return typing.cast(typing.Optional[IdentityPlatformInboundSamlConfigIdpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IdentityPlatformInboundSamlConfigIdpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cedb6435cf3823ce36bf4b33bb3dbff0fc0cd1cc80ebb2ab739fb838d065827a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.identityPlatformInboundSamlConfig.IdentityPlatformInboundSamlConfigSpConfig",
    jsii_struct_bases=[],
    name_mapping={"callback_uri": "callbackUri", "sp_entity_id": "spEntityId"},
)
class IdentityPlatformInboundSamlConfigSpConfig:
    def __init__(
        self,
        *,
        callback_uri: typing.Optional[builtins.str] = None,
        sp_entity_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param callback_uri: Callback URI where responses from IDP are handled. Must start with 'https://'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#callback_uri IdentityPlatformInboundSamlConfig#callback_uri}
        :param sp_entity_id: Unique identifier for all SAML entities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#sp_entity_id IdentityPlatformInboundSamlConfig#sp_entity_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b89c69cd6c8524e6efcb0b370069f6911aec8f412ffca842dafa12826bda753)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#callback_uri IdentityPlatformInboundSamlConfig#callback_uri}
        '''
        result = self._values.get("callback_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sp_entity_id(self) -> typing.Optional[builtins.str]:
        '''Unique identifier for all SAML entities.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#sp_entity_id IdentityPlatformInboundSamlConfig#sp_entity_id}
        '''
        result = self._values.get("sp_entity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPlatformInboundSamlConfigSpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IdentityPlatformInboundSamlConfigSpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformInboundSamlConfig.IdentityPlatformInboundSamlConfigSpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50e389cc97e6bd320c7f4f3509e9bd529698f5fabc7cf9eddac3297b0ac4a9f4)
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
    ) -> "IdentityPlatformInboundSamlConfigSpConfigSpCertificatesList":
        return typing.cast("IdentityPlatformInboundSamlConfigSpConfigSpCertificatesList", jsii.get(self, "spCertificates"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3413890b4e3b0d7bb9543882f589135c950814017e684f6e24d44a8a2c2e335a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "callbackUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="spEntityId")
    def sp_entity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "spEntityId"))

    @sp_entity_id.setter
    def sp_entity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__590ce139c029b3a2cfc509f7307db83cab749f0450f562d76e065d336ac49a8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spEntityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IdentityPlatformInboundSamlConfigSpConfig]:
        return typing.cast(typing.Optional[IdentityPlatformInboundSamlConfigSpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IdentityPlatformInboundSamlConfigSpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7d04507a2c4878bf88b416fa3b366bb1cb6cc1b30fc9f3ad8c1aa2d6a3aef5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.identityPlatformInboundSamlConfig.IdentityPlatformInboundSamlConfigSpConfigSpCertificates",
    jsii_struct_bases=[],
    name_mapping={},
)
class IdentityPlatformInboundSamlConfigSpConfigSpCertificates:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPlatformInboundSamlConfigSpConfigSpCertificates(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IdentityPlatformInboundSamlConfigSpConfigSpCertificatesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformInboundSamlConfig.IdentityPlatformInboundSamlConfigSpConfigSpCertificatesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__947a6c232bfe5eb97d1af9ab42e329c532461684a4427b129f4b1c558297ab3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IdentityPlatformInboundSamlConfigSpConfigSpCertificatesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf47c9dcfea157143c9c30ac06d3554511611aefa56a1595809e553dd3511415)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IdentityPlatformInboundSamlConfigSpConfigSpCertificatesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__062ed8f92dd481c5181db9158efc08aa25aef63dfaf1394d958ce8442c4db73a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34e1c789eb6a6d9ca828540a96eab63d7d1d6328ef6ed072ca67788977ad7564)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9205568abec2a782a82e65358055de1abe8890c067f9228a0121f50607e0802a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class IdentityPlatformInboundSamlConfigSpConfigSpCertificatesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformInboundSamlConfig.IdentityPlatformInboundSamlConfigSpConfigSpCertificatesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6aad8d85b6640424c5128c6e6aad2517251ede9a108a4ede71cfa37373e6a73)
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
    ) -> typing.Optional[IdentityPlatformInboundSamlConfigSpConfigSpCertificates]:
        return typing.cast(typing.Optional[IdentityPlatformInboundSamlConfigSpConfigSpCertificates], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IdentityPlatformInboundSamlConfigSpConfigSpCertificates],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7ed4353a41f38cc41d1d0724291e8ca4d084e727eb144de34cea0cf1c71d8af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.identityPlatformInboundSamlConfig.IdentityPlatformInboundSamlConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class IdentityPlatformInboundSamlConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#create IdentityPlatformInboundSamlConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#delete IdentityPlatformInboundSamlConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#update IdentityPlatformInboundSamlConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd9f1d2d46a029af3578ba412cf470445c9f4cba8bf7223d56c86af9b76a9705)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#create IdentityPlatformInboundSamlConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#delete IdentityPlatformInboundSamlConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/identity_platform_inbound_saml_config#update IdentityPlatformInboundSamlConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPlatformInboundSamlConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IdentityPlatformInboundSamlConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformInboundSamlConfig.IdentityPlatformInboundSamlConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9632c08645b6032d0ce4f7d21fc9e7e1dfacad794e76a1f3971dbd517bf3a94e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0800f392df7dbbbe62f2823a6786e5a2e22f54347fcdbdb84009d0ea804056c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8b820163b047506faaacd839d9bd8bfe19f0b2da1f9ef10eab914372435db0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__155c4f551b85140cb4c5fc909e809ea121ed13712e492935ed70462db4d6c019)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IdentityPlatformInboundSamlConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IdentityPlatformInboundSamlConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IdentityPlatformInboundSamlConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe548a2410e39d59fd61ed5ea8a109323a5673a5e724fa089d5bfc91a2bc0d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "IdentityPlatformInboundSamlConfig",
    "IdentityPlatformInboundSamlConfigConfig",
    "IdentityPlatformInboundSamlConfigIdpConfig",
    "IdentityPlatformInboundSamlConfigIdpConfigIdpCertificates",
    "IdentityPlatformInboundSamlConfigIdpConfigIdpCertificatesList",
    "IdentityPlatformInboundSamlConfigIdpConfigIdpCertificatesOutputReference",
    "IdentityPlatformInboundSamlConfigIdpConfigOutputReference",
    "IdentityPlatformInboundSamlConfigSpConfig",
    "IdentityPlatformInboundSamlConfigSpConfigOutputReference",
    "IdentityPlatformInboundSamlConfigSpConfigSpCertificates",
    "IdentityPlatformInboundSamlConfigSpConfigSpCertificatesList",
    "IdentityPlatformInboundSamlConfigSpConfigSpCertificatesOutputReference",
    "IdentityPlatformInboundSamlConfigTimeouts",
    "IdentityPlatformInboundSamlConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__8bd8819cabe4f7c27c7141c9016b6809f5ade90f68d08d546dd920a74dc420ba(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    idp_config: typing.Union[IdentityPlatformInboundSamlConfigIdpConfig, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    sp_config: typing.Union[IdentityPlatformInboundSamlConfigSpConfig, typing.Dict[builtins.str, typing.Any]],
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[IdentityPlatformInboundSamlConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__554d5b4f5e2d963d8dfbc25c980fdd3d53013d84be13216f257ba76b65487d33(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__272681820181cf99603889ba1232d92b6ce94feccc1d27d026fad65347bf59b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc928566175c417a149ccebe316a307b7b27de8e51e8923e67af74b5906ac15c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eaad1eccb7d4780b81794026ccb9a74f2045287b33369084e620c1f72aacb03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5cda37fd272a00985781745f7ac85ff4f0283b01faabea3a81e0735982efa7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d569aa22792e32ea8f9ff8065b363cde8fee4d299f8dd077a1434175ea60fbc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb014a31c4f757a03c90cf8be804e69f28483d7ece0c8106cd8b1ec445cf1d30(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    idp_config: typing.Union[IdentityPlatformInboundSamlConfigIdpConfig, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    sp_config: typing.Union[IdentityPlatformInboundSamlConfigSpConfig, typing.Dict[builtins.str, typing.Any]],
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[IdentityPlatformInboundSamlConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__659d4863035910073ade85fbf4db703a82eb897d66e8ecd0db4689bdd31d92f3(
    *,
    idp_certificates: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IdentityPlatformInboundSamlConfigIdpConfigIdpCertificates, typing.Dict[builtins.str, typing.Any]]]],
    idp_entity_id: builtins.str,
    sso_url: builtins.str,
    sign_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e34b149dac548380562c285c03155e710699687ea1b9729d84d1c9b85f57847(
    *,
    x509_certificate: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2840715c42ced8b8a175780d224a2df23f06ff92d887802e117ffb576269a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f36a3d0dd4f904c88b2a7a2b44299b8d9e5c2cb9816f1afed217b49bf0bffa0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af2e77c76b3532a0545a85f48f149c7664fd0f04bdecb4600c70247a9c97421c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a18e9f435ac6673224aab2760758930467c971af4361cd5e3795da56e053f938(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0242af7d9a2539bd308eea9fef8c39e8177c5e78ec75f496f0ce25ee5555f811(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5417179b7319922aea0cf90d8fdef40fb0e78767380061a5bc81291d16d1dec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IdentityPlatformInboundSamlConfigIdpConfigIdpCertificates]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd3400e2074adfad6d52c1b2b2be649c2ecb9653135ed943ab0a076b7bb33c79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e02432140f343e5e39f06d2aa6c6ecac69b0bc6115cf7c6c85975373c93496(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__824cb007e845454891ce17c02f8865dfecdaf2ae3a7e881d2baf8739b4517c90(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IdentityPlatformInboundSamlConfigIdpConfigIdpCertificates]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f5ad3a7dbd4d4c127ac6b8bb106c8e4c065a61800e95df1fde810ec9ae1297(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e1ce43338ac9b1b4a26f56642c586b7aa06cfa922bec9f05272cee34b552c0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IdentityPlatformInboundSamlConfigIdpConfigIdpCertificates, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a097c33108f29a811fb435eabdefa1a3e6d356c20011d32260474fd0d2526a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fa1ca50f82599b1b0289fc69606fe90216c37d673169cd49bce88e8cde2789b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37796a92a3977d4974faa2971a8f7e7e7206e9dcd918daad1d2c358fb24521e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cedb6435cf3823ce36bf4b33bb3dbff0fc0cd1cc80ebb2ab739fb838d065827a(
    value: typing.Optional[IdentityPlatformInboundSamlConfigIdpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b89c69cd6c8524e6efcb0b370069f6911aec8f412ffca842dafa12826bda753(
    *,
    callback_uri: typing.Optional[builtins.str] = None,
    sp_entity_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e389cc97e6bd320c7f4f3509e9bd529698f5fabc7cf9eddac3297b0ac4a9f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3413890b4e3b0d7bb9543882f589135c950814017e684f6e24d44a8a2c2e335a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__590ce139c029b3a2cfc509f7307db83cab749f0450f562d76e065d336ac49a8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d04507a2c4878bf88b416fa3b366bb1cb6cc1b30fc9f3ad8c1aa2d6a3aef5f(
    value: typing.Optional[IdentityPlatformInboundSamlConfigSpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947a6c232bfe5eb97d1af9ab42e329c532461684a4427b129f4b1c558297ab3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf47c9dcfea157143c9c30ac06d3554511611aefa56a1595809e553dd3511415(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__062ed8f92dd481c5181db9158efc08aa25aef63dfaf1394d958ce8442c4db73a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e1c789eb6a6d9ca828540a96eab63d7d1d6328ef6ed072ca67788977ad7564(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9205568abec2a782a82e65358055de1abe8890c067f9228a0121f50607e0802a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6aad8d85b6640424c5128c6e6aad2517251ede9a108a4ede71cfa37373e6a73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7ed4353a41f38cc41d1d0724291e8ca4d084e727eb144de34cea0cf1c71d8af(
    value: typing.Optional[IdentityPlatformInboundSamlConfigSpConfigSpCertificates],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd9f1d2d46a029af3578ba412cf470445c9f4cba8bf7223d56c86af9b76a9705(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9632c08645b6032d0ce4f7d21fc9e7e1dfacad794e76a1f3971dbd517bf3a94e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0800f392df7dbbbe62f2823a6786e5a2e22f54347fcdbdb84009d0ea804056c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b820163b047506faaacd839d9bd8bfe19f0b2da1f9ef10eab914372435db0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__155c4f551b85140cb4c5fc909e809ea121ed13712e492935ed70462db4d6c019(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe548a2410e39d59fd61ed5ea8a109323a5673a5e724fa089d5bfc91a2bc0d2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IdentityPlatformInboundSamlConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
