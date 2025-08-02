r'''
# `opentelekomcloud_identity_provider`

Refer to the Terraform Registry for docs: [`opentelekomcloud_identity_provider`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider).
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


class IdentityProvider(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.identityProvider.IdentityProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider opentelekomcloud_identity_provider}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        protocol: builtins.str,
        access_config: typing.Optional[typing.Union["IdentityProviderAccessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        mapping_rules: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[builtins.str] = None,
        status: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider opentelekomcloud_identity_provider} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#name IdentityProvider#name}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#protocol IdentityProvider#protocol}.
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#access_config IdentityProvider#access_config}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#description IdentityProvider#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#id IdentityProvider#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mapping_rules: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#mapping_rules IdentityProvider#mapping_rules}.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#metadata IdentityProvider#metadata}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#status IdentityProvider#status}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c10abcffb2d6f89a609e8f5145578794fb0642fcb93c3d424980de9cbc503f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IdentityProviderConfig(
            name=name,
            protocol=protocol,
            access_config=access_config,
            description=description,
            id=id,
            mapping_rules=mapping_rules,
            metadata=metadata,
            status=status,
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
        '''Generates CDKTF code for importing a IdentityProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IdentityProvider to import.
        :param import_from_id: The id of the existing IdentityProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IdentityProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52c8d759175327e3a3d53057440dfccefc037d7599ea8711d115d87540a4089a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAccessConfig")
    def put_access_config(
        self,
        *,
        access_type: builtins.str,
        client_id: builtins.str,
        provider_url: builtins.str,
        signing_key: builtins.str,
        authorization_endpoint: typing.Optional[builtins.str] = None,
        response_mode: typing.Optional[builtins.str] = None,
        response_type: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param access_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#access_type IdentityProvider#access_type}.
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#client_id IdentityProvider#client_id}.
        :param provider_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#provider_url IdentityProvider#provider_url}.
        :param signing_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#signing_key IdentityProvider#signing_key}.
        :param authorization_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#authorization_endpoint IdentityProvider#authorization_endpoint}.
        :param response_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#response_mode IdentityProvider#response_mode}.
        :param response_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#response_type IdentityProvider#response_type}.
        :param scopes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#scopes IdentityProvider#scopes}.
        '''
        value = IdentityProviderAccessConfig(
            access_type=access_type,
            client_id=client_id,
            provider_url=provider_url,
            signing_key=signing_key,
            authorization_endpoint=authorization_endpoint,
            response_mode=response_mode,
            response_type=response_type,
            scopes=scopes,
        )

        return typing.cast(None, jsii.invoke(self, "putAccessConfig", [value]))

    @jsii.member(jsii_name="resetAccessConfig")
    def reset_access_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessConfig", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMappingRules")
    def reset_mapping_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMappingRules", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

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
    @jsii.member(jsii_name="accessConfig")
    def access_config(self) -> "IdentityProviderAccessConfigOutputReference":
        return typing.cast("IdentityProviderAccessConfigOutputReference", jsii.get(self, "accessConfig"))

    @builtins.property
    @jsii.member(jsii_name="conversionRules")
    def conversion_rules(self) -> "IdentityProviderConversionRulesList":
        return typing.cast("IdentityProviderConversionRulesList", jsii.get(self, "conversionRules"))

    @builtins.property
    @jsii.member(jsii_name="links")
    def links(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "links"))

    @builtins.property
    @jsii.member(jsii_name="loginLink")
    def login_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loginLink"))

    @builtins.property
    @jsii.member(jsii_name="accessConfigInput")
    def access_config_input(self) -> typing.Optional["IdentityProviderAccessConfig"]:
        return typing.cast(typing.Optional["IdentityProviderAccessConfig"], jsii.get(self, "accessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="mappingRulesInput")
    def mapping_rules_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mappingRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1ea8c9d853ce3ea4bfc326150167fcc563e076519aee864e3269fbf4b227af7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34c31b65e53ba3507b3c229590ce45222cfd0cb69a4246f353824a418a3870c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mappingRules")
    def mapping_rules(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mappingRules"))

    @mapping_rules.setter
    def mapping_rules(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59aaba358024bec1ab1b5d4bd7ffb0cd338073f1bb1b39cf1f8170200b52fbc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mappingRules", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4508449010b67d11eb2cc4a2f1e573b1ddabb4bb1b11b593ff2fc4e19497e0bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7eb16a091cc900bb58d7883287b78f8302384fae22c3b4a12050fed63a4f350)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d5c99f002319c34daf514f33afd37178d5718c4fa74280a858a514bd5313057)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "status"))

    @status.setter
    def status(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__508e81265a2305a63b12aed41677b828dc11199f00aa24ba645dd3cef1efc728)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.identityProvider.IdentityProviderAccessConfig",
    jsii_struct_bases=[],
    name_mapping={
        "access_type": "accessType",
        "client_id": "clientId",
        "provider_url": "providerUrl",
        "signing_key": "signingKey",
        "authorization_endpoint": "authorizationEndpoint",
        "response_mode": "responseMode",
        "response_type": "responseType",
        "scopes": "scopes",
    },
)
class IdentityProviderAccessConfig:
    def __init__(
        self,
        *,
        access_type: builtins.str,
        client_id: builtins.str,
        provider_url: builtins.str,
        signing_key: builtins.str,
        authorization_endpoint: typing.Optional[builtins.str] = None,
        response_mode: typing.Optional[builtins.str] = None,
        response_type: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param access_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#access_type IdentityProvider#access_type}.
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#client_id IdentityProvider#client_id}.
        :param provider_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#provider_url IdentityProvider#provider_url}.
        :param signing_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#signing_key IdentityProvider#signing_key}.
        :param authorization_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#authorization_endpoint IdentityProvider#authorization_endpoint}.
        :param response_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#response_mode IdentityProvider#response_mode}.
        :param response_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#response_type IdentityProvider#response_type}.
        :param scopes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#scopes IdentityProvider#scopes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3bc16e057515f882725962bcacc32d28402307d80934ce96a494574bac04d2b)
            check_type(argname="argument access_type", value=access_type, expected_type=type_hints["access_type"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument provider_url", value=provider_url, expected_type=type_hints["provider_url"])
            check_type(argname="argument signing_key", value=signing_key, expected_type=type_hints["signing_key"])
            check_type(argname="argument authorization_endpoint", value=authorization_endpoint, expected_type=type_hints["authorization_endpoint"])
            check_type(argname="argument response_mode", value=response_mode, expected_type=type_hints["response_mode"])
            check_type(argname="argument response_type", value=response_type, expected_type=type_hints["response_type"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_type": access_type,
            "client_id": client_id,
            "provider_url": provider_url,
            "signing_key": signing_key,
        }
        if authorization_endpoint is not None:
            self._values["authorization_endpoint"] = authorization_endpoint
        if response_mode is not None:
            self._values["response_mode"] = response_mode
        if response_type is not None:
            self._values["response_type"] = response_type
        if scopes is not None:
            self._values["scopes"] = scopes

    @builtins.property
    def access_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#access_type IdentityProvider#access_type}.'''
        result = self._values.get("access_type")
        assert result is not None, "Required property 'access_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#client_id IdentityProvider#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#provider_url IdentityProvider#provider_url}.'''
        result = self._values.get("provider_url")
        assert result is not None, "Required property 'provider_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signing_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#signing_key IdentityProvider#signing_key}.'''
        result = self._values.get("signing_key")
        assert result is not None, "Required property 'signing_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorization_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#authorization_endpoint IdentityProvider#authorization_endpoint}.'''
        result = self._values.get("authorization_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#response_mode IdentityProvider#response_mode}.'''
        result = self._values.get("response_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#response_type IdentityProvider#response_type}.'''
        result = self._values.get("response_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#scopes IdentityProvider#scopes}.'''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityProviderAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IdentityProviderAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.identityProvider.IdentityProviderAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__808b49084bd0aee2b3c48ff225c690887627726aa57a921785491ce2297e793d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthorizationEndpoint")
    def reset_authorization_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizationEndpoint", []))

    @jsii.member(jsii_name="resetResponseMode")
    def reset_response_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseMode", []))

    @jsii.member(jsii_name="resetResponseType")
    def reset_response_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseType", []))

    @jsii.member(jsii_name="resetScopes")
    def reset_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScopes", []))

    @builtins.property
    @jsii.member(jsii_name="accessTypeInput")
    def access_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationEndpointInput")
    def authorization_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="providerUrlInput")
    def provider_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="responseModeInput")
    def response_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseModeInput"))

    @builtins.property
    @jsii.member(jsii_name="responseTypeInput")
    def response_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="scopesInput")
    def scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopesInput"))

    @builtins.property
    @jsii.member(jsii_name="signingKeyInput")
    def signing_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signingKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="accessType")
    def access_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessType"))

    @access_type.setter
    def access_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eacf2a2ce167710e9f4f3e14fa9a5d1f94162a8ed159e0a93396d572ef93be37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authorizationEndpoint")
    def authorization_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationEndpoint"))

    @authorization_endpoint.setter
    def authorization_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c233e1d336bd4e8b3d9bba9468196f8da9122bcc8c80791cded3351aeeccf37e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89f5ab69f556c0a69f12c43e60f3973c208bddec9a57c58551594219e9c76e93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="providerUrl")
    def provider_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerUrl"))

    @provider_url.setter
    def provider_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57f0187d1aaa607b61d47fa84be02e3f8929f8bf13a58a9628f19430ea9912ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseMode")
    def response_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseMode"))

    @response_mode.setter
    def response_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd76d6897db159aa5bb8e465d54d42348d5327861bbc607329a204e28bfc465d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseType")
    def response_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseType"))

    @response_type.setter
    def response_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f5702d3a388024b9f280674782ceb97bcde76cf6a8701e043e71368dc6f921)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e6b89783a63d0e4f8e86a153a1b7b6936c76a7c4c6f378fb7c5f20ac6e9869d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signingKey")
    def signing_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signingKey"))

    @signing_key.setter
    def signing_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b915c141b44758822f6bff83216cf8642ab6ecfac4a51d72de2fff3c7fe1f605)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signingKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IdentityProviderAccessConfig]:
        return typing.cast(typing.Optional[IdentityProviderAccessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IdentityProviderAccessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbbd8402836a0b7314ed0c63872006b723b600f07dbf9036450cbff303095240)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.identityProvider.IdentityProviderConfig",
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
        "protocol": "protocol",
        "access_config": "accessConfig",
        "description": "description",
        "id": "id",
        "mapping_rules": "mappingRules",
        "metadata": "metadata",
        "status": "status",
    },
)
class IdentityProviderConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        protocol: builtins.str,
        access_config: typing.Optional[typing.Union[IdentityProviderAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        mapping_rules: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[builtins.str] = None,
        status: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#name IdentityProvider#name}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#protocol IdentityProvider#protocol}.
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#access_config IdentityProvider#access_config}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#description IdentityProvider#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#id IdentityProvider#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mapping_rules: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#mapping_rules IdentityProvider#mapping_rules}.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#metadata IdentityProvider#metadata}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#status IdentityProvider#status}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(access_config, dict):
            access_config = IdentityProviderAccessConfig(**access_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d158fe2e4a6825917d1abd9e5a81adcaf4f98ad26f39edae381dfb9dd7d35045)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument access_config", value=access_config, expected_type=type_hints["access_config"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument mapping_rules", value=mapping_rules, expected_type=type_hints["mapping_rules"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "protocol": protocol,
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
        if access_config is not None:
            self._values["access_config"] = access_config
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if mapping_rules is not None:
            self._values["mapping_rules"] = mapping_rules
        if metadata is not None:
            self._values["metadata"] = metadata
        if status is not None:
            self._values["status"] = status

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#name IdentityProvider#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#protocol IdentityProvider#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_config(self) -> typing.Optional[IdentityProviderAccessConfig]:
        '''access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#access_config IdentityProvider#access_config}
        '''
        result = self._values.get("access_config")
        return typing.cast(typing.Optional[IdentityProviderAccessConfig], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#description IdentityProvider#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#id IdentityProvider#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mapping_rules(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#mapping_rules IdentityProvider#mapping_rules}.'''
        result = self._values.get("mapping_rules")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#metadata IdentityProvider#metadata}.'''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_provider#status IdentityProvider#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.identityProvider.IdentityProviderConversionRules",
    jsii_struct_bases=[],
    name_mapping={},
)
class IdentityProviderConversionRules:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityProviderConversionRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IdentityProviderConversionRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.identityProvider.IdentityProviderConversionRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7185cf544d00afc303f2f350861be30fdf18b101c28c80cfefaaaec3d2de1ffe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IdentityProviderConversionRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2183b54e3fe1cd700cf26687fbeae2761e53ffe80ffd21e2098c1a41ae661b15)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IdentityProviderConversionRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbce4cb8be8c9c3936b0789d8e1ed6f149af7c023b4b81e64d91cb38ea5bd4c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47fecef47acea400c3b92992f2c1558ae5f851bf936b46cd3a034f3fa659cb0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__887661cb993ee2b96d2ffee12a66e2131ed1416822e3d2d6cbcd16ca17ad41ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.identityProvider.IdentityProviderConversionRulesLocal",
    jsii_struct_bases=[],
    name_mapping={},
)
class IdentityProviderConversionRulesLocal:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityProviderConversionRulesLocal(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IdentityProviderConversionRulesLocalList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.identityProvider.IdentityProviderConversionRulesLocalList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c027df5a6b38cce4bc1b5aee6a93a68e4b756011c639916ba027f289573b3fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IdentityProviderConversionRulesLocalOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89142c1fea5ada358ee0261ac047642feb6d6c108353ef870cffccc6a10660b5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IdentityProviderConversionRulesLocalOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__133cb80e7a6283c446f540e49385d89d0e1770141d59f1649d0df2aea8679489)
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
            type_hints = typing.get_type_hints(_typecheckingstub__707d1b075ef3be9878f58b1b5d9d7be4c91f451e4aaed8254cfece0fe6f641f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40cd831aa8a99c5ea955df2697160178d93f058d5cc645765cd58485baa92359)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class IdentityProviderConversionRulesLocalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.identityProvider.IdentityProviderConversionRulesLocalOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d83db3525b1ceaa18dd4ec3502ca6e98c4c7138716cabf4a183fd9b27cff0831)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "group"))

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groups"))

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IdentityProviderConversionRulesLocal]:
        return typing.cast(typing.Optional[IdentityProviderConversionRulesLocal], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IdentityProviderConversionRulesLocal],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7683578d43a36151582f2c0b4aa7dd5a670a7fce941ac4ef06213e6231e54702)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IdentityProviderConversionRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.identityProvider.IdentityProviderConversionRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6e3d0cc33a75d7229b165b86ccc004266ebf67717b10bb129590439dfeccc04)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="local")
    def local(self) -> IdentityProviderConversionRulesLocalList:
        return typing.cast(IdentityProviderConversionRulesLocalList, jsii.get(self, "local"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(self) -> "IdentityProviderConversionRulesRemoteList":
        return typing.cast("IdentityProviderConversionRulesRemoteList", jsii.get(self, "remote"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IdentityProviderConversionRules]:
        return typing.cast(typing.Optional[IdentityProviderConversionRules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IdentityProviderConversionRules],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3e067f22c61bf6ab74735a99d47e3857ba0d8d70ac234397583cdab32a85790)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.identityProvider.IdentityProviderConversionRulesRemote",
    jsii_struct_bases=[],
    name_mapping={},
)
class IdentityProviderConversionRulesRemote:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityProviderConversionRulesRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IdentityProviderConversionRulesRemoteList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.identityProvider.IdentityProviderConversionRulesRemoteList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d1b9e0594a3ea61808b9abd69ea22f1b2107b01d96dc7b6e372f1c0b2871eb9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IdentityProviderConversionRulesRemoteOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d3575bb5d9e57f0d4e93cb7725e0f26757fa07e23446c0bbe6f332ea5462e43)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IdentityProviderConversionRulesRemoteOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae74fb09bed7c331e951dd6121f6fe616ae2e75198f153f8fab293f6fdcaee45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8957cd9c7ed150d778ad8b91b1903f8c7702edd5f57537813ba96c8b72c504bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e26bf4032ed189551fdcd7f40e582d69ee052c9530721f9a45366773ba096b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class IdentityProviderConversionRulesRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.identityProvider.IdentityProviderConversionRulesRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb6a6b92889b31d11452381365e6a715fcafcf96d31cbe97912836e94d1f5bfe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="attribute")
    def attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attribute"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IdentityProviderConversionRulesRemote]:
        return typing.cast(typing.Optional[IdentityProviderConversionRulesRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IdentityProviderConversionRulesRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__470b494e8275ba724e6c08f470420366163b9898ef22dd52c4de5bc99361153f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "IdentityProvider",
    "IdentityProviderAccessConfig",
    "IdentityProviderAccessConfigOutputReference",
    "IdentityProviderConfig",
    "IdentityProviderConversionRules",
    "IdentityProviderConversionRulesList",
    "IdentityProviderConversionRulesLocal",
    "IdentityProviderConversionRulesLocalList",
    "IdentityProviderConversionRulesLocalOutputReference",
    "IdentityProviderConversionRulesOutputReference",
    "IdentityProviderConversionRulesRemote",
    "IdentityProviderConversionRulesRemoteList",
    "IdentityProviderConversionRulesRemoteOutputReference",
]

publication.publish()

def _typecheckingstub__d5c10abcffb2d6f89a609e8f5145578794fb0642fcb93c3d424980de9cbc503f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    protocol: builtins.str,
    access_config: typing.Optional[typing.Union[IdentityProviderAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    mapping_rules: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[builtins.str] = None,
    status: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__52c8d759175327e3a3d53057440dfccefc037d7599ea8711d115d87540a4089a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ea8c9d853ce3ea4bfc326150167fcc563e076519aee864e3269fbf4b227af7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34c31b65e53ba3507b3c229590ce45222cfd0cb69a4246f353824a418a3870c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59aaba358024bec1ab1b5d4bd7ffb0cd338073f1bb1b39cf1f8170200b52fbc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4508449010b67d11eb2cc4a2f1e573b1ddabb4bb1b11b593ff2fc4e19497e0bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7eb16a091cc900bb58d7883287b78f8302384fae22c3b4a12050fed63a4f350(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d5c99f002319c34daf514f33afd37178d5718c4fa74280a858a514bd5313057(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__508e81265a2305a63b12aed41677b828dc11199f00aa24ba645dd3cef1efc728(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3bc16e057515f882725962bcacc32d28402307d80934ce96a494574bac04d2b(
    *,
    access_type: builtins.str,
    client_id: builtins.str,
    provider_url: builtins.str,
    signing_key: builtins.str,
    authorization_endpoint: typing.Optional[builtins.str] = None,
    response_mode: typing.Optional[builtins.str] = None,
    response_type: typing.Optional[builtins.str] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__808b49084bd0aee2b3c48ff225c690887627726aa57a921785491ce2297e793d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eacf2a2ce167710e9f4f3e14fa9a5d1f94162a8ed159e0a93396d572ef93be37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c233e1d336bd4e8b3d9bba9468196f8da9122bcc8c80791cded3351aeeccf37e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f5ab69f556c0a69f12c43e60f3973c208bddec9a57c58551594219e9c76e93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f0187d1aaa607b61d47fa84be02e3f8929f8bf13a58a9628f19430ea9912ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd76d6897db159aa5bb8e465d54d42348d5327861bbc607329a204e28bfc465d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f5702d3a388024b9f280674782ceb97bcde76cf6a8701e043e71368dc6f921(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e6b89783a63d0e4f8e86a153a1b7b6936c76a7c4c6f378fb7c5f20ac6e9869d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b915c141b44758822f6bff83216cf8642ab6ecfac4a51d72de2fff3c7fe1f605(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbbd8402836a0b7314ed0c63872006b723b600f07dbf9036450cbff303095240(
    value: typing.Optional[IdentityProviderAccessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d158fe2e4a6825917d1abd9e5a81adcaf4f98ad26f39edae381dfb9dd7d35045(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    protocol: builtins.str,
    access_config: typing.Optional[typing.Union[IdentityProviderAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    mapping_rules: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[builtins.str] = None,
    status: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7185cf544d00afc303f2f350861be30fdf18b101c28c80cfefaaaec3d2de1ffe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2183b54e3fe1cd700cf26687fbeae2761e53ffe80ffd21e2098c1a41ae661b15(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbce4cb8be8c9c3936b0789d8e1ed6f149af7c023b4b81e64d91cb38ea5bd4c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47fecef47acea400c3b92992f2c1558ae5f851bf936b46cd3a034f3fa659cb0b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887661cb993ee2b96d2ffee12a66e2131ed1416822e3d2d6cbcd16ca17ad41ca(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c027df5a6b38cce4bc1b5aee6a93a68e4b756011c639916ba027f289573b3fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89142c1fea5ada358ee0261ac047642feb6d6c108353ef870cffccc6a10660b5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__133cb80e7a6283c446f540e49385d89d0e1770141d59f1649d0df2aea8679489(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__707d1b075ef3be9878f58b1b5d9d7be4c91f451e4aaed8254cfece0fe6f641f0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40cd831aa8a99c5ea955df2697160178d93f058d5cc645765cd58485baa92359(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83db3525b1ceaa18dd4ec3502ca6e98c4c7138716cabf4a183fd9b27cff0831(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7683578d43a36151582f2c0b4aa7dd5a670a7fce941ac4ef06213e6231e54702(
    value: typing.Optional[IdentityProviderConversionRulesLocal],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6e3d0cc33a75d7229b165b86ccc004266ebf67717b10bb129590439dfeccc04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e067f22c61bf6ab74735a99d47e3857ba0d8d70ac234397583cdab32a85790(
    value: typing.Optional[IdentityProviderConversionRules],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d1b9e0594a3ea61808b9abd69ea22f1b2107b01d96dc7b6e372f1c0b2871eb9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d3575bb5d9e57f0d4e93cb7725e0f26757fa07e23446c0bbe6f332ea5462e43(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae74fb09bed7c331e951dd6121f6fe616ae2e75198f153f8fab293f6fdcaee45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8957cd9c7ed150d778ad8b91b1903f8c7702edd5f57537813ba96c8b72c504bd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e26bf4032ed189551fdcd7f40e582d69ee052c9530721f9a45366773ba096b2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6a6b92889b31d11452381365e6a715fcafcf96d31cbe97912836e94d1f5bfe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__470b494e8275ba724e6c08f470420366163b9898ef22dd52c4de5bc99361153f(
    value: typing.Optional[IdentityProviderConversionRulesRemote],
) -> None:
    """Type checking stubs"""
    pass
